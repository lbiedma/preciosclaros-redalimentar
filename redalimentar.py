from datetime import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
from zipfile import ZipFile

from dictionaries import (
    locations,
    lookup_products,
)

BASE_URL = "https://d3e6htiiul5ek9.cloudfront.net/prod/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
sucursales_url = "sucursales?lat={}&lng={}&limit=30"
lookup_url = "productos?string={}&array_sucursales={}&offset=0&limit=100&id_categoria={}"
product_url = "producto?limit=50&id_producto={}&array_sucursales={}"

get_precio_lista = lambda x: x["preciosProducto"].get("precioLista")

today_string = datetime.today().strftime("%Y%m%d")

def get_csvs_for_region(locate):
    sucurl = BASE_URL + sucursales_url.format(locate["lat"], locate["lon"])
    response = requests.get(sucurl, headers=HEADERS)
    sucursales = pd.DataFrame.from_records(json.loads(response.content.decode("latin-1")).get("sucursales", []))
    locate["array"] = str(list(sucursales.id)).strip("[]\'").replace("', '", ",")
    sucsarray = locate["array"]
    
    for productstr, lookupstr in lookup_products.items():
        lookingurl = BASE_URL + lookup_url.format(lookupstr["term"], sucsarray, lookupstr.get("category", "0"))
        response = requests.get(lookingurl, headers=HEADERS)
        productos = pd.DataFrame.from_records(json.loads(response.content.decode("latin-1")).get("productos", []))
        productos = productos[productos["presentacion"].str.contains(lookupstr["packagings"])].sort_values("precioMin").iloc[:4]
        candidates = productos.id.to_list()
        
        finalproductdf = pd.DataFrame()

        for candidate in candidates:
            candidate_url = BASE_URL + product_url.format(candidate, sucsarray)
            response = requests.get(candidate_url, headers=HEADERS)
            productdf = pd.DataFrame.from_records(
                           json.loads(
                               response.content.decode("latin-1")).get('sucursales', [])
                           ).dropna(subset=["actualizadoHoy"]
                        )
            productdf["precio"] = productdf.apply(get_precio_lista, axis=1)
            productdf["id"] = candidate
            finalproductdf = pd.concat([finalproductdf, productdf[["id", "banderaDescripcion", "direccion", "precio"]]])
        
        finalproductdf = finalproductdf.merge(productos[["id", "nombre"]], on="id", how="right")
        finalproductdf["comercio"] = finalproductdf["banderaDescripcion"] + " - " + finalproductdf["direccion"]
        finalproductdf["precio"] = pd.to_numeric(finalproductdf["precio"])
        finalproductdf.sort_values("precio", inplace=True)
        
        csv_string = "{}/{}/{}.csv".format(today_string, locate["code"], productstr)
        finalproductdf[["nombre", "comercio", "precio"]].reset_index(drop=True).to_csv(csv_string)

        print("Saved {}".format(csv_string))


def main():
    os.mkdir(today_string)
    for locate in locations:
        region = locations.get(locate)
        os.mkdir("{}/{}".format(today_string, region.get("code")))
        get_csvs_for_region(region)

    with ZipFile('{}.zip'.format(today_string), 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(today_string):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)
    print("Archivos zipeados!")

    
if __name__ == "__main__":
    main()

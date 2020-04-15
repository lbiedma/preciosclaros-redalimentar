import json
import os
import pandas as pd
import requests
from zipfile import ZipFile


BASE_URL = "https://d3e6htiiul5ek9.cloudfront.net/dev/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
sucursales_url = "sucursales?lat={}&lng={}&limit=30"
lookup_url = "productos?string={}&array_sucursales={}&offset=0&limit=100&id_categoria={}"
product_url = "producto?limit=50&id_producto={}&array_sucursales={}"
grouped_url = "categoria?id_categoria={}&string={}&array_sucursales={}&lat={}&lng={}"
suc_grouped_url = "sucursal?string={}&id_categoria={}&id_sucursal={}&sort=precio_lista"


def get_precio_lista(row):
    return row["preciosProducto"].get("precioLista")


def get_array_sucursales(latitude, longitude):
    sucurl = BASE_URL + sucursales_url.format(latitude, longitude)
    response = requests.get(sucurl, headers=HEADERS)
    sucursales = pd.DataFrame.from_records(
        json.loads(response.content.decode("latin-1")).get("sucursales", [])
    )
    sucursales = sucursales[sucursales["banderaDescripcion"].str.contains("Mercamax|Express|Carrefour|Libertad|Mariano")]
    array = str(list(sucursales.id)).strip("[]\'").replace("', '", ",")

    return array


def get_products_from_sucursales(lookupstr, sucsarray):
    lookingurl = BASE_URL + lookup_url.format(lookupstr["term"], sucsarray, lookupstr.get("category", "0"))
    response = requests.get(lookingurl, headers=HEADERS)
    productos = pd.DataFrame()
    if response.status_code == 200:
        productos = pd.DataFrame.from_records(
            json.loads(response.content.decode("latin-1")).get("productos", [])
        )
        if not productos.empty:
            productos = productos[
                (productos["presentacion"].str.contains(lookupstr["packagings"]))
                & (~productos["nombre"].str.lower().str.contains(lookupstr.get("remove", "___")))
                & (productos["nombre"].str.lower().str.contains(lookupstr.get("contain", "")))
            ].sort_values("precioMin").iloc[:5]

    return productos


def create_productsdf_from_candidates_sucursales(candidates, sucsarray):
    finalproductdf = pd.DataFrame()

    for candidate in candidates:
        candidate_url = BASE_URL + product_url.format(candidate, sucsarray)
        response = requests.get(candidate_url, headers=HEADERS)
        productdf = pd.DataFrame.from_records(
            json.loads(
                response.content.decode("latin-1")
            ).get('sucursales', [])
        ).dropna(subset=["actualizadoHoy"])
        productdf["precio"] = productdf.apply(get_precio_lista, axis=1)
        productdf["id"] = candidate
        finalproductdf = pd.concat(
            [finalproductdf, productdf[["id", "banderaDescripcion", "direccion", "precio"]]]
        )

    return finalproductdf


def get_sucs_for_product(lookupstr, sucsarray, locate):
    groupproduct_url = BASE_URL + grouped_url.format(
        lookupstr["category"],
        lookupstr["term"],
        sucsarray,
        locate["lat"],
        locate["lon"],
    )

    response = requests.get(groupproduct_url, headers=HEADERS)
    datos = pd.DataFrame.from_records(json.loads(response.content.decode("latin-1")).get("sucursales", []))
    datos["sucursal"] = datos["comercio_id"].apply(str) + "-" + datos["bandera_id"].apply(str) + "-" + datos[
        "sucursal_id"]
    datos["comercio"] = datos["bandera_descripcion"] + " - " + datos["direccion"]
    datos = datos[["comercio", "sucursal"]]

    return datos


def create_grouped_productdf(lookupstr, sucursal):
    lookup_url = BASE_URL + suc_grouped_url.format(lookupstr["term"], lookupstr["category"], sucursal)
    response = requests.get(lookup_url, headers=HEADERS)
    prod_in_suc = pd.DataFrame.from_records(
        json.loads(response.content.decode("latin-1")).get("result", {}).get("productos", [])
    )
    if not prod_in_suc.empty:
        prod_in_suc = prod_in_suc[prod_in_suc["presentacion"].str.contains(lookupstr["packagings"])]
        prod_in_suc["sucursal"] = sucursal
        prod_in_suc = prod_in_suc[["sucursal", "producto_descripcion", "precio_lista"]]

    return prod_in_suc


def get_zip_from_directory(directorystr):
    with ZipFile('{}.zip'.format(directorystr), 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(directorystr):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)
    print("Archivos zipeados!")

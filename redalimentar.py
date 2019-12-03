from datetime import datetime
import os
import pandas as pd
from zipfile import ZipFile

from dictionaries import (
    grouped_products,
    locations,
    lookup_products,
)
from helpers import (
    create_grouped_productdf,
    create_productsdf_from_candidates_sucursales,
    get_array_sucursales,
    get_sucs_for_product,
    get_products_from_sucursales,
)

today_string = datetime.today().strftime("%Y%m%d")


def get_csvs_for_region(locate, sucsarray):

    for productstr, lookupstr in lookup_products.items():
        productos = get_products_from_sucursales(lookupstr, sucsarray)
        candidates = productos.id.to_list()

        finalproductdf = create_productsdf_from_candidates_sucursales(
            candidates,
            sucsarray,
        )
        finalproductdf = finalproductdf.merge(
            productos[["id", "nombre"]], on="id", how="right"
        )
        finalproductdf["comercio"] = finalproductdf["banderaDescripcion"] + " - " + finalproductdf["direccion"]
        finalproductdf["precio"] = pd.to_numeric(
            finalproductdf["precio"]
        )
        finalproductdf.sort_values("precio", inplace=True)
        
        csv_string = "{}/{}/{}.csv".format(today_string, locate["code"], productstr)
        finalproductdf[["nombre", "comercio", "precio"]].reset_index(
            drop=True
        ).to_csv(csv_string)

        print("Saved {}".format(csv_string))


def get_groupables_for_region(locate, sucsarray):
    for product in grouped_products.keys():
        lookupstr = grouped_products.get(product)

        datos = get_sucs_for_product(lookupstr, sucsarray, locate)
        finaldf = pd.DataFrame()
        for sucursal in datos["sucursal"]:
            productdf = create_grouped_productdf(lookupstr, sucursal)
            finaldf = finaldf.append(productdf)

        datos = datos.merge(
            finaldf, on="sucursal",
        ).sort_values(
            "precio_lista",
        ).rename(
            columns={
                "producto_descripcion": "nombre",
                "precio_lista": "precio",
            },
        )

        csv_string = "{}/{}/{}.csv".format(today_string, locate["code"], product)
        datos[["nombre", "comercio", "precio"]].to_csv(csv_string)

        print("Saved {}".format(csv_string))


def main():
    if not os.path.exists(today_string):
        os.makedirs(today_string)
    for locate in locations:
        region = locations.get(locate)
        region_string = "{}/{}".format(today_string, region.get("code"))
        if not os.path.exists(region_string):
            os.makedirs(region_string)
        sucsarray = get_array_sucursales(region.get("lat"), region.get("lon"))
        get_csvs_for_region(region, sucsarray)
        get_groupables_for_region(region, sucsarray)

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

from datetime import datetime
from multiprocessing import Pool
import os
import pandas as pd

from auth_pydrive import upload_to_drive
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

        csv_string = "data/{}/{}/{}.csv".format(today_string, locate["code"], productstr)
        if os.path.isfile(csv_string):
            print("{} already exists, skipping...".format(csv_string))
            continue

        productos = get_products_from_sucursales(lookupstr, sucsarray)
        if productos.empty:
            print("Couldn't find {} in {}, skipping...".format(productstr, locate["code"]))
            continue

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
        
        finalproductdf[["nombre", "comercio", "precio"]].reset_index(
            drop=True
        ).to_csv(csv_string)

        print("Saved {}".format(csv_string))


def get_groupables_for_region(locate, sucsarray):

    for product in grouped_products.keys():
        csv_string = "data/{}/{}/{}.csv".format(today_string, locate["code"], product)
        if os.path.isfile(csv_string):
            print("{} already exists, skipping...".format(csv_string))
            continue

        lookupstr = grouped_products.get(product)
        datos = get_sucs_for_product(lookupstr, sucsarray, locate)
        finaldf = pd.DataFrame()
        for sucursal in datos["sucursal"]:
            productdf = create_grouped_productdf(lookupstr, sucursal)
            finaldf = finaldf.append(productdf)

        finaldf["precio_lista"] = pd.to_numeric(finaldf["precio_lista"], errors="coerce")
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

        datos[["nombre", "comercio", "precio"]].to_csv(csv_string)

        print("Saved {}".format(csv_string))


def process_data_for_region(region):
    sucsarray = get_array_sucursales(region.get("lat"), region.get("lon"))
    get_csvs_for_region(region, sucsarray)
    get_groupables_for_region(region, sucsarray)


def main():
    regions = []
    for locate in locations:
        region = locations.get(locate)
        region_string = "data/{}/{}".format(today_string, region.get("code"))
        if not os.path.exists(region_string):
            os.makedirs(region_string)
        regions.append(region)

    with Pool(processes=4) as pool:
        pool.map(process_data_for_region, regions)

    directorystr = "data/{}".format(today_string)
    upload_to_drive(directorystr=directorystr)


if __name__ == "__main__":
    main()

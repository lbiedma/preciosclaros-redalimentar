# 8 coordenadas para el proyecto.
locations = {
    "Noroeste": {
        "code": "NO",
        "lat": "-31.3417943",
        "lon": "-64.2538802",
    },
    "Norte": {
        "code": "N",
        "lat": "-31.3613381",
        "lon": "-64.2066416",
    },
    "Centro-oeste": {
        "code": "CO",
        "lat": "-31.4086063",
        "lon": "-64.2084814",
    },
    "Centro-este": {
        "code": "CE",
        "lat": "-31.4054267",
        "lon": "-64.1956076",
    },
    "Oeste": {
        "code": "O",
        "lat": "-31.4068982",
        "lon": "-64.2413965",
    },
    "Sudoeste": {
        "code": "SO",
        "lat": "-31.4671374",
        "lon": "-64.2272544",
    },
    "Sudeste": {
        "code": "SE",
        "lat": "-31.4696984",
        "lon": "-64.1715217",
    },
    "Este": {
        "code": "E",
        "lat": "-31.4215951",
        "lon": "-64.1226057",
    },
}

# Diccionario de búsquedas de productos

lookup_products = {
    "Aceite Girasol": {
        "term": "aceite girasol 1.5 lt",
        "packagings": "1.5 lt",
    },
    "Agua Bidón": {
        "term": "agua 6 lt",
        "packagings": "6.0 lt|6.25 lt|6.3 lt|6.5 lt",
        "category": "05",
    },
    "Arroz Integral": {
        "term": "arroz integral 1 kg",
        "packagings": "1.0 kg",
    },
    "Arroz Largo Fino": {
        "term": "arroz largo fino 1 kg",
        "packagings": "1.0 kg",
    },
    "Arvejas Conserva": {
        "term": "arvejas 3",
        "packagings": "300.0 gr|320.0 gr|340.0 gr|350.0 gr",
    },
    "Arvejas Secas": {
        "term": "arvejas",
        "packagings": "500.0 gr",
    },
    "Avena Instántanea": {
        "term": "avena instantanea",
        "packagings": "350.0 gr|400.0 gr|500.0 gr",
    },
    "Azúcar": {
        "term": "azucar 1 kg",
        "packagings": "1.0 kg",
    },
    "Cacao en Polvo": {
        "term": "cacao en polvo 360",
        "packagings": "360.0 gr",
    },
    "Café Tostado": {
        "term": "cafe molido 250",
        "packagings": "250.0 gr",
    },
    "Caldo de Verduras": {
        "term": "caldo 12",
        "contain": "carne|verdura",
        "packagings": "12.0 un",
    },
    "Choclo Grano": {
        "term": "choclo grano lata",
        "packagings": "300.0 gr|350.0 gr",
        "remove": "crema|cremoso",
    },
    "Copos de Maiz": {
        "term": "copos maiz",
        "packagings": "400.0 gr",
        "remove": "azucarados|zucaritas",
        "category": "02",
    },
    "Durazno en Lata": {
        "term": "durazno 8",
        "packagings": "800.0 gr|820.0 gr|1.0 un",
        "category": "0205",
    },
    "Dulce de Leche": {
        "term": "dulce de leche 400",
        "packagings": "400.0 gr",
        "category": "020607",
    },
    "Edulcorante Líquido": {
        "term": "edulcorante liquido 2",
        "packagings": "200.0 cc|200.0 ml|250.0 cc|250.0 ml",
    },
    "Fideos Largos": {
        "term": "tallarin",
        "packagings": "500.0 gr",
    },
    "Galletas Crackers": {
        "term": "galletitas pack 3",
        "packagings": " ",
        "remove": "vainilla|chocolate",
    },
    "Garbanzos Secos": {
        "term": "garbanzo 500",
        "packagings": "500.0 gr",
    },
    "Gelatina Light": {
        "term": "gelatina light",
        "packagings": "20.0 gr|25.0 gr|30.0 gr",
    },
    "Harina 000": {
        "term": "harina 000",
        "packagings": "1.0 kg",
        "remove": "0000",
    },
    "Harina Maiz": {
        "term": "harina maiz",
        "packagings": "500.0 gr",
    },
    "Harina Integral": {
        "term": "harina integral 1",
        "packagings": "1.0 kg",
    },
    "Jugo en Polvo": {
        "term": "jugo en polvo",
        "packagings": " ",
    },
    "Leche Descremada (SachetCaja)": {
        "term": "leche descremada 1",
        "packagings": "1.0 lt",
    },
    "Leche en Polvo Descremada": {
        "term": "leche en polvo descremada 400",
        "packagings": "400.0 gr",
    },
    "Leche Maternizada": {
        "term": "leche formula",
        "packagings": " ",
    },
    "Lentejas Secas": {
        "term": "lentejas 400",
        "packagings": "400.0 gr",
    },
    "Levadura Seca": {
        "term": "levadura 20",
        "packagings": "20.0 gr",
    },
    "Lomitos de Atun": {
        "term": "atun 1",
        "packagings": "160.0 gr|170.0 gr",
        "contain": "lomito|lomo",
        "remove": "aceite",
    },
    "Manteca": {
        "term": "manteca 200",
        "packagings": "200.0 gr",
        "category": "06",
    },
    "Masa de Tarta": {
        "term": "pascualina",
        "packagings": " ",
    },
    "Mermelada": {
        "term": "mermelada 500",
        "packagings": "500.0 gr",
    },
    "Poroto Alubia": {
        "term": "poroto alubia",
        "packagings": "500.0 gr",
    },
    "Puré de Tomate": {
        "term": "pure tomate",
        "packagings": "520.0 gr|530.0 gr",
    },
    "Queso Untable Light": {
        "term": "queso untable light",
        "packagings": "290.0 gr|300.0 gr",
    },
    "Sal Fina": {
        "term": "sal fina",
        "packagings": "500.0 gr",
    },
    "Té en Saquitos": {
        "term": "te saquitos 25",
        "packagings": "25.0 un",
    },
    "Tomate Perita en Lata": {
        "term": "tomate perita 400",
        "packagings": "400.0 gr",
    },
    "Yerba": {
        "term": "yerba 1 kg",
        "packagings": "1.0 kg",
    },
    "Yogur Bebible Descremado": {
        "term": "yogur bebible descremado 1",
        "packagings": "1.0 lt|1.0 kg|900.0 gr",
    },
}


grouped_products = {
    "Queso Cuartirolo": {
        "term": "queso",
        "packagings": "1 Kg",
        "category": "060608004",
    },
    "Huevos": {
        "term": "huevos",
        "packagings": "12 Un",
        "category": "060501001",
    },
    "Pan Integral": {
        "term": "pan salvado",
        "packagings": " ",
        "category": "021003002",
    },
}


# Productos que solo aparecian en fiestas
holiday_products = {
    "Aceitunas": {
        "term": "aceitunas verdes 1 kg",
        "packagings": "1.0 kg",
        "remove": "descarozadas|despepitadas|rellenas"
    },
    "Budín Inglés": {
        "term": "budin",
        "packagings": "190.0 gr|220.0 gr",
    },
    "Garrapiñada de maní": {
        "term": "garrapi",
        "packagings": "70.0 gr|80.0 gr|100.0 gr",
    },
    "Maní Sin Sal": {
        "term": "mani sin sal 1 kg",
        "packagings": "1.0 kg",
    },
    "Mayonesa Light": {
        "term": "mayonesa light",
        "packagings": "450.0 gr|475.0 gr|495.0 gr|500.0 gr",
    },
    "Mostaza": {
        "term": "mostaza 2",
        "packagings": "200.0 gr|220.0 gr|250.0 gr",
        "remove": "miel",
    },
    "Pionono": {
        "term": "pionono",
        "packagings": "150.0 gr|180.0 gr|200.0 gr",
        "remove": "chocolate",
    },
    "Turrón de Maní": {
        "term": "turron de mani",
        "packagings": "120.0 gr",
        "remove": "yema",
    }
}


grouped_holidays = {
    "Pan Dulce": {
        "term": "pan dulce 400",
        "packagings": "400 Gr",
        "category": "021099018",
    },
    "Queso Tybo": {
        "term": "queso tybo",
        "packagings": "1 Kg",
        "category": "060611020",
    }
}


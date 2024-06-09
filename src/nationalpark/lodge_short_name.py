from enum import Enum


class NationalPark(Enum):
    GLACIER = "glaciernationalparklodges"
    YELLOWSTONE = "yellowstonenationalparklodges"
    GRAND_CANYON = "grandcanyonlodges"
    ZION = "zionlodge"


SHORT_NAME = {
    NationalPark.ZION: {"UTZN": "ZION LODGE"},
    NationalPark.GLACIER: {
        "GLCC": "Cedar Creek Lodge",
        "GLLM": "Lake McDonald Lodge",
        "GLMG": "Many Glacier Hotel",
        "GLRS": "Rising Sun Motor Inn",
        "GLSC": "Swiftcurrent Motor Inn",
        "GLVI": "Village Inn at Apgar",
    },
    NationalPark.YELLOWSTONE: {
        "YLCL": "Canyon LODGE",
        "YLGV": "GRANT VILLAGE",
        "YLMH": "MAMMOTH HOTEL",
        "YLLH": "LAKE HOTEL",
        "YLLL": "LAKE LODGE",
        "YLOI": "OLD FAITHFUL INN",
        "YLOL": "OLD FAITHFUL LODGE",
        "YLOS": "OLD FAITHFUL SNOW LODGE",
        "YLRL": "ROOSEVELT LODGE",
    },
    NationalPark.GRAND_CANYON: {
        "GCET": "El Tovar",
        "GCTL": "Thunderbird lodge",
        "GCKL": "Kachina Lodge",
        "GCML": "Masik Lodge",
        "GCBA": "Bright Angel Lodge",
        "GCGH": "The Grand Hotel",
    },
}

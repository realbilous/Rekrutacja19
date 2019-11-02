import pandas as pd
import os.path
import matplotlib.pyplot
import re
import math
from skimage import io
import numpy as np
from scipy.spatial import distance

def ramka_danych(input):
    """
    Funkcja przyjmuje sciezke do folderu z obrazami a zwraca ramke danych z informacjami dotyczacymi kazdego obrazu
    w tym folderze.

    :param input: sciezka do folderu z obrazami
    :type input: path as string
    :return: ramka danych z informacjami o obrazach
    :rtype: <class 'pandas.core.frame.DataFrame'>
    """
    # height, width, channels = matplotlib.pyplot.imread(kat + pliki[1]).shape

    # 1. Tworzymy ramke
    ramka = pd.DataFrame()

    # 2. Nazwa pliku
    pliki = os.listdir(kat)
    ramka["Nazwa pliku"] = pliki

    # 3:6. Opis zawartosci zdjecia & Id zdjecia & Szerokosc & Wysokosc
    opis_zawartosci = []
    id_zdjecia = []
    wysokosc = []
    szerokosc = []
    for nazwa_pliku in pliki:
        wynik = re.match(r'stock-photo-(.*)-(\d*)', nazwa_pliku)
        opis_zawartosci.append(wynik.group(1).replace(r"-", r" "))
        id_zdjecia.append(wynik.group(2))
        wys, szer, _w = matplotlib.pyplot.imread(kat + nazwa_pliku).shape
        wysokosc.append(wys)
        szerokosc.append(szer)

    ramka["Opis zawartosci zdjecia"] = opis_zawartosci
    ramka["Id zdjecia"] = id_zdjecia
    ramka["Szerokosc"] = szerokosc
    ramka["Wysokosc"] = wysokosc

    # 7. Sredni kolor
    sredni_kolor = []
    for nazwa_pliku in pliki:
        obraz = io.imread(kat + nazwa_pliku)
        sredni_kolor.append(list(obraz.mean(axis=0).mean(axis=0)))
    ramka["Sredni kolor"] = sredni_kolor

    # 8:10. Mediana & Pozioma najjas. pixela & Pionowa najjas. pixela
    _mediana = []
    _pozioma = []
    _pionowa = []
    for nazwa_pliku in pliki:
        image = io.imread(kat + nazwa_pliku, as_gray=True)
        _mediana.append(np.median(image))
        max_wart = 0
        max_wys = 0
        max_szer = 0
        max_norm = 0
        wys, szer = image.shape
        for i in range(wys):
            for j in range(szer):
                if image[i][j] > max_wart:
                    max_wart = image[i][j]
                    max_wys = i
                    max_szer = j
                    max_norm = distance.euclidean(image[0][0], image[i][j])
                elif image[i][j] == max_wart:
                    aktual_norm = distance.euclidean(image[0][0], image[i][j])
                    if aktual_norm < max_norm:
                        max_wart = image[i][j]
                        max_wys = i
                        max_szer = j
                        max_norm = aktual_norm
        _pionowa.append(max_wys)
        _pozioma.append(max_szer)
    ramka["Mediana jasnosci po przekonwertowaniu na odcienie szarosci"] = _mediana
    ramka["Pozioma wspolrzedna najjasnieszego pixela po przekonwertowaniu na odcienie szarosci"] = _pozioma
    ramka["Pionowa wspolrzedna najjasniejszego pixela po przekonwertowaniu na odcienie szarosci"] = _pionowa
    ramka.to_csv("images.csv")
    return ramka

kat = "C:/Users/admin/Desktop/Kolo_DS/images/"
ramka_danych(kat)
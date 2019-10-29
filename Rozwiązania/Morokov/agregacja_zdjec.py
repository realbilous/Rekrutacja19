import os
import pandas as pd
import shutil

def dzielenie_listy(l, n):
    """
    Funkcja do dzielenia listy na n podlist.

    :param l: lista wejsiowa
    :type l: list
    :param n: liczba na ile podlist dzielono liste l
    :type n: int
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]

def agregacja_zdjec(input):
    """
    :param input: sciezka do folderu z obrazami
    :type input: path as string
    """
    ramka = pd.read_csv("images.csv")
    ramka_sort = ramka.sort_values(by="Mediana jasnosci po przekonwertowaniu na odcienie szarosci", ascending=True)
    nazwy_plikow = list(ramka_sort["Nazwa pliku"])
    nazwy_plikow = list(dzielenie_listy(nazwy_plikow, 4))

    for i in range(len(nazwy_plikow)):
        os.makedirs('agg-images/' + f'{i + 1}-images')
        for plik in nazwy_plikow[i]:
            shutil.copy(input + plik, 'agg-images/' + f'{i+1}-images')

    shutil.make_archive('agg-images', 'zip', 'agg-images')


kat = "C:/Users/admin/Desktop/Kolo_DS/images/"
agregacja_zdjec(kat)
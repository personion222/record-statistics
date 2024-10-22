from bs4 import BeautifulSoup
from skimage import io
import skimage
import numpy as np
import requests
import cv2


def download_img(url: str, res: tuple[int, int]) -> np.array:
    return cv2.resize(io.imread(url), res, interpolation=cv2.INTER_LANCZOS4)

def get_img_url(img_name: str) -> str:
    # e.g. https://www.google.com/search?q=test&tbm=isch
    # img class: DS1iW

    search_url = f"https://www.google.com/search?q={img_name.replace('&', '%26')}&tbm=isch"
    htmlpage = requests.get(search_url).content

    websoup = BeautifulSoup(htmlpage, "html.parser")
    img_soup = websoup.find_all("img", class_="DS1iW")[0]
    return img_soup["src"]


def get_img(img_name: str, res: tuple[int, int]) -> np.array:
    img = download_img(get_img_url(img_name), res)
    print(img)
    return img

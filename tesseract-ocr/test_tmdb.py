from tmdbv3api import TMDb, Search
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

img = cv2.imread("pulp_fiction.png")


def convert_grayscale(img):
    img = cv2.cvtcolor(img, cv2.COLOR_BGR2GRAY)
    return img
# thresholding


def threshold(img):
    img = cv2. threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img


tmdb = TMDb()

tmdb.api_key = "f875c12dc125c6f6f5e2f09aa016ba0a"

search = Search()
custom_config = r'--oem 3 --psm 6'
results = {}
with open("recognized.txt") as file:
    for line in file:
        l = line.rstrip()
        if l:
            results[l] = (search.movies(
                {"query": l}))

for l in results:
    for r in results[l]:
        print(r.title)

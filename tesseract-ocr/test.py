# importing libraries
import glob
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

images = [(cv2.imread(file), file) for file in glob.glob("./*.png")]

for (img, name) in images:
    def convert_grayscale(img):
        img = cv2.cvtcolor(img, cv2.COLOR_BGR2GRAY)
        return img
# noise removal

    def blur(img, param):
        img = cv2.medianBlur(img, param)
        return img
# thresholding

    def threshold(img):
        img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return img


custom_config = r'--oem 3 --psm 6'
for (img, name) in images:
    print("-------------" + name)
    print(pytesseract.image_to_string(img, config=custom_config))

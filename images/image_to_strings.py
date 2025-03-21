#这里建议使用Linux环境运行
#提前准备安装sudo apt install tesseract-ocr
from PIL import Image
import pytesseract

image_path='misc3.png'
image=Image.open(image_path)


test=pytesseract.image_to_string(image,lang='eng')

print("the content in the photo:")
print(test)
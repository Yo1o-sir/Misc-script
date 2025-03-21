#这里进行了多文件的提取，顺序是按照文件名排的，使用时候可以进行调整
from PIL import Image
import pytesseract
import os

files=os.listdir('.')
files=[f for f in files if os.path.isfile(f)]

image_extensions=['.png','.jpg','.bmp','.gif','.tif']
image_files=[f for f in files if os.path.splitext(f)[1].lower() in image_extensions]

image_files.sort(key=lambda x: int(''.join(filter(str.isdigit,x))))
combined_text=""
for image_file in image_files:
    try:
        image=Image.open(image_file)
        text=pytesseract.image_to_string(image,lang='eng')

        combined_text += text.strip()+""

        print(f"file:{image_file}")
        print("the content:")
        print(text)
        print("-"*40)
    except Exception as e:
        print(f"find error in {image_file},and the error is{e}")
        

print(f"the complete content is {combined_text.lower()}")
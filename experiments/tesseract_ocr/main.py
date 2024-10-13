import pytesseract
from PIL import Image
import os

# # For Windows: specify the path to the tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# os.environ['TESSDATA_PREFIX'] = "/usr/share/tesseract-ocr/"
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/'

# Load the image from which you want to extract text
image_path = 'img102.png'  # replace with your image file path
image = Image.open(image_path)

# Extract text from the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
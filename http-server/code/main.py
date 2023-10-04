import os
import string
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTasks
import uvicorn
from dotenv import load_dotenv
import cv2

load_dotenv()

try:
    from typing_extensions import Annotated
except ImportError:
    from typing import Annotated

from fastapi import FastAPI, File, UploadFile

import CaptchaCracker as cc

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def remove_file(path: str) -> None:
    os.unlink(path)

def remove_noise(img):
  kernel_size = 3
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
  closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

  # Apply binary thresholding with a threshold value of 190
  threshold_value = 190
  max_value = 255
  ret, thresholded_img = cv2.threshold(closing, threshold_value, max_value, cv2.THRESH_BINARY)

  kernel_size = 3
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
  dilation = cv2.morphologyEx(thresholded_img, cv2.MORPH_DILATE, kernel)
  return dilation

def process(img_path, new_img_path='tmp.png'):
  img = cv2.imread(img_path, 0)
  final = remove_noise(img)
  cv2.imwrite(new_img_path, final)

def predict(captcha_path, temp_captcha_path):

  process(captcha_path, temp_captcha_path)

  pred = AM.predict(temp_captcha_path).strip()
  output = eval(pred)

  return output

#Target image data size
img_width = int(os.getenv('CAPTCHA_WIDTH', '180'))
img_height = int(os.getenv('CAPTCHA_HEIGHT', '50'))
# Target image label length
max_length = int(os.getenv('CAPTCHA_CHARS', '5'))

characters = set()
char_mode = int(os.getenv('CHAR_MODE', '0'))

if char_mode >= 1:
    characters = characters.union(map(chr, range(48, 58)))

if char_mode >= 2:
    characters = characters.union(map(chr, range(65, 91)))

if char_mode >= 3:
    characters = characters.union(map(chr, range(97, 123)))

# Characters to add
include = set(json.loads(os.getenv('CHAR_INCLUDE', '[]')))

# Characters to omit
exclude = set(json.loads(os.getenv('CHAR_EXCLUDE', '[]')))

# Target image label component
characters = characters.union(include) - exclude

# Model weight file path
weights_path = os.getenv('WEIGHTS_PATH', "./model/weights.h5")

AM = None

@app.on_event("startup")
def startup():
    try:
        global AM
        if AM is None:
            AM = cc.ApplyModel(weights_path, img_width, img_height, max_length, characters)
    except Exception as e:
        print("Couldn't load the model properly! Closing...")
        exit(-1)

@app.get("/")
def root():
    return {"message": "Hi!"}

@app.post("/solve/")
def solve_captcha(file: Annotated[bytes, File()], background_tasks: BackgroundTasks):

    full_filename = 'image.png'
    with open(full_filename, 'wb') as image:
        image.write(file)
        image.close()

    processed_captcha = 'temp.png'
    pred = predict(full_filename, processed_captcha)
    
    background_tasks.add_task(remove_file, full_filename)
    background_tasks.add_task(remove_file, processed_captcha)    

    return {"result": pred}

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', '8008')), log_level="info", reload=True)

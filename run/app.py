from flask import Flask, request, send_file
import os
import cv2
import numpy as np
from PIL import Image
import base64
app = Flask(__name__)

def check_file_exists(file_path):
    return os.path.exists(file_path)

@app.route('/')
def get():
    category = int(request.args.get('category'))
    if category == 0:
       result_path = f"images_output/out_hd_0.png"
    else:
       result_path = f"images_output/out_dc_0.png"

    return send_file(result_path)

@app.route('/', methods=['GET', 'POST'])
def try_on():
    category = int(request.args.get('category'))
    category = 0
    os.makedirs("tmp", exist_ok = True)

    model = request.files['model']
    img = Image.open(model).convert('RGB')
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    model_name = os.path.splitext(model.filename)[0] + "_model.jpg"
    cv2.imwrite(f"tmp/{model_name}", img)

    cloth = request.files['cloth']
    img = Image.open(cloth).convert('RGB')
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cloth_name = os.path.splitext(cloth.filename)[0] + "_cloth.jpg"
    cv2.imwrite(f"tmp/{cloth_name}", img)

    if category == 0:
        model_type = "hd"
    else:
        model_type = "dc"

    os.system(f"python run_ootd.py --model_path tmp/{model_name} --cloth_path tmp/{cloth_name} --scale 2.0 --sample 1 -c {category} --model_type {model_type}")

    result_path = f"images_output/out_{model_type}_0.png"

    # with open(result_path, 'rb') as file:
    #     image_bytes = file.read()
    #     # Convert image to base64
    #     base64_image = base64.b64encode(image_bytes).decode('utf-8')

    #clean
    os.system(f"rm -rf tmp")
    # os.system(f"rm -rf images_output/*")

    # return base64_image
    return send_file(result_path)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8000)

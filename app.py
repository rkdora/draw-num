from flask import Flask, render_template, request, jsonify
import re
import base64
import cv2
import numpy as np
from datetime import datetime

from dnn import predict

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        ans, per, now_time = judge_img(request.form['img'])
        return jsonify({'ans': ans, 'per': per, 'now_time': now_time})
    else:
        return render_template('index.html')

def judge_img(base64_img):
    now_time = datetime.now().strftime('%s')
    img_str = re.search(r'base64,(.*)', base64_img).group(1)
    nparr = np.frombuffer(base64.b64decode(img_str), np.uint8)
    img_src = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img_resize = cv2.resize(img_src,(28,28))
    img_name = "static/images/pure/" + now_time + ".jpg"
    cv2.imwrite(img_name,img_resize)
    img_inverse = 255 - img_resize
    img_inverse_name = "static/images/inverse/" + now_time + ".jpg"
    cv2.imwrite(img_inverse_name,img_inverse)
    ans, per = predict.predict(img_inverse)

    return ans, per, now_time

if __name__ == "__main__":
    app.run()

import numpy as np
import matplotlib.pyplot as plt
from dnn.deep_convnet import DeepConvNet
from dnn.common.functions import softmax

import math

network = DeepConvNet()

network.load_params("dnn/deep_convnet_params.pkl")

def predict(x):
    pre = network.predict(x.reshape(1,1,28,28))
    pre_label = int(np.argmax(pre))
    pre_score = math.floor(max(softmax(pre[0])) * 1000)/ 10
    print("predict", pre_label, pre_score, softmax(pre[0]))
    return pre_label, pre_score

def generate_adv(x, label, eps=0.3):
    d = np.zeros_like(x)
    # advsが生成されなかった時、生成されるまで繰り返す
    while (d == np.zeros_like(x)).all():
        d, g = network.gradient_for_fgsm(x.reshape(1, 1, 28, 28), np.array([label]))
        d = d.reshape(28, 28)

    p = eps * np.sign(d)
    adv = (x + p).clip(min=0, max=1)
    p = np.clip(p * 255, 0, 255).astype(np.uint8)
    adv = np.clip(adv * 255, 0, 255).astype(np.uint8)
    return p, adv

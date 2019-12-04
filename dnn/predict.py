import numpy as np
import matplotlib.pyplot as plt
from dnn.deep_convnet import DeepConvNet
from dnn.common.functions import softmax

network = DeepConvNet()

network.load_params("dnn/deep_convnet_params.pkl")

def predict(x):
    pre = network.predict(x.reshape(1,1,28,28))
    pre_label = int(np.argmax(pre))
    pre_score = round(max(softmax(pre[0])), 2) * 100
    return pre_label, pre_score

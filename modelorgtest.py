import cv2
import numpy as np
from sklearn.metrics import f1_score
import tensorflow as tf
import requests
import xmltodict
import json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'




def f1score(y, y_pred):
  return f1_score(y, tf.math.argmax(y_pred, axis=1), average='micro') 

def custom_f1score(y, y_pred):
  return tf.py_function(f1score, (y, y_pred), tf.double)

from keras.models import load_model
model = load_model("model_5testneworg.h5", custom_objects={"custom_f1score": custom_f1score})


# Predicting the output
def fix_dimension(img): 
  new_img = np.zeros((28,28,3))
  for i in range(1):
    new_img[:,:,i] = img
  return new_img
  
def show_results(char):
    dic = {}
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i,c in enumerate(characters):
        dic[i] = c

    output = []
    for i,ch in enumerate(char): #iterating over the characters
        img_ = cv2.resize(ch, (28,28), interpolation=cv2.INTER_AREA)
        img = fix_dimension(img_)
        img = img.reshape(1, 28,28,3) #preparing image for the model
        y_ = np.argmax(model.predict(img, batch_size=1)[0], axis=-1) #predicting the class
        character = dic[y_] #
        output.append(character) #storing the result in a list
        
    plate_number = ''.join(output)
    
    return plate_number

def vehicle_info(plate_number):
    r = requests.get("http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={0}&username=theman123".format(str(plate_number)))
    data = xmltodict.parse(r.content)
    jdata = json.dumps(data)
    df = json.loads(jdata)
    df1 = json.loads(df['Vehicle']['vehicleJson'])
    return df1

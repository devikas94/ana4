#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
# from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
dic = {0 : 'NORMAL', 1 : 'PNEUMONIA'}
model = load_model('classification_model.h5')
model.make_predict_function()

def predict_label(img_path):
    i = image.load_img(img_path, target_size=(100,100))
    i = image.img_to_array(i)/255.0
    i = np.expand_dims(i, axis=0)
    p = model.predict(i).astype("int32")
    return dic[p[0][0]]

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/" + img.filename
        img.save(img_path)
        p = predict_label(img_path)
        return render_template("index.html", prediction = p, img_path = img_path)

if __name__ =='__main__':
 #   app.debug = True
    app.run(debug= False)
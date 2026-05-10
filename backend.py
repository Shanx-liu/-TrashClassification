import numpy as np
import tensorflow as tf
import io
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, jsonify, request
from flask_cors import CORS


#相關參數
IMG_SIZE = (224, 224)

app = Flask(__name__)
CORS(app)     #啟動CORS，允許所有來源存取

model = load_model('MobileNet.keras')   #載入訓練好的模型權重

#預測的結果種類(有順序，依照tensorflow讀取時之順序(非資料夾名稱))
trashClass = ['一般垃圾', '塑膠類', '廚餘類', '照明光源(增強)', 
              '玻璃類', '紙類', '舊衣類', '金屬類', '電子電器', '電池類']    

@app.route('/api/data', methods=['POST'])       # "/api/data" 為Flask虛擬路由
def getData():                                  #伺服器接收到請求時自動呼叫此函式
    if 'image' not in request.files:
        return 'No file part', 400
    
    imageFile = request.files['image']      #接收客戶端傳來的圖片
    img_bytes = io.BytesIO(imageFile.read())    #將物件讀取並轉為 BytesIO 虛擬檔案
    img = img = Image.open(img_bytes)   #使用 Image.open 直接讀取 BytesIO(取代image.load_img)
    img = img.convert('RGB')    #強制轉為 RGB (避免 PNG 等透明通道導致維度變 4)
    img = img.resize(IMG_SIZE)
    
    #將 PIL 物件轉回 Keras 用的 numpy 陣列
    img_array = image.img_to_array(img)     #將圖片轉成numpy陣列(224,224,3)
    img_array = np.expand_dims(img_array, axis=0)    #加上批次維度(1,224,224,3)

    #此處不需再做預處理，因模型內部自訂層已有預處理層

    predictions = model.predict(img_array)   #丟進模型預測
    print(predictions)

    #對第一維取最大值，[0]因為批次只有一張
    classIndex = np.argmax(predictions, axis=1)[0]  
    trashResult = trashClass[classIndex] 
       
    return jsonify({        #回傳客戶端之json格式內容
        'status': 'success', 
        'trashClass': trashResult
        })


if __name__ == '__main__':      #當其他程式import本檔案時不執行本檔，只有當本檔為主執行時才會開啟監聽
    app.run(port=5000, debug=True)

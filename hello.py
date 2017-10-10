from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from google.cloud import vision
import requests
import io
import os
import time
#from PIL import Image
#import pytesseract
#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =''


app = Flask(__name__, template_folder='C:\\Users\\HP\\Desktop\\final\\',static_folder='C:\\Users\\HP\\Desktop\\final\\static')


photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
configure_uploads(app, photos)

@app.route('/index', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        vision_client = vision.Client()
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()
            image = vision_client.image(
                content=content, )
        text=image.detect_full_text().text
        myList = [item for item in text.split('\n')]
        newString = ' '.join(myList)
        #print(newString)
        return render_template('x.html',t=newString)
        #return filename
        
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

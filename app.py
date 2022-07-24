import csv
import sqlite3
from datetime import datetime
# from flask import Flask, g, render_template, request
import pathlib
from flask import Flask,flash, url_for, redirect,  render_template, request
import os
from werkzeug.utils import secure_filename
# 取得目前檔案所在的資料夾 
SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','mp4'}
# rsplit('.', 1)[1]取得副檔名，1是只切一刀(兩等分),從'.'開始切故[0]為filename
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER          # 設置儲存上傳檔的資料夾 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  * 1024  # 上傳檔最大16MB

@app.route('/')
def index():
    category=['Openpose','Yolo','Flow Chart','category','category','category']
    projectName=['運動員骨架抓取','辨識球員','相關技術','Project Name','Project Name','Project Name']
    className=['Openpose-Result','Yolo-Result','Flow-Chart','Project-Name','Project-Name','Project-Name']
    linkName=['Openpose Result','Yolo Result','Flow Chart','Project Name','Project Name','Project Name']
    return render_template('index.html',projectName=projectName,category=category,className=className,linkName=linkName)

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/video.html')
def video():
    return render_template('video.html')

@app.route("/user.html")
def user():
    return render_template('user.html')
@app.route('/user.html', methods=['POST'])
def upload_file():
    if 'filename' not in request.files:   # 如果表單的「檔案」欄位沒有'filename'
        flash('沒有上傳檔案')
        # return redirect(url_for('index'))

    file = request.files['filename']    # 取得上傳的檔案 
    if file.filename == '':           #  若上傳的檔名是空白的… 
        flash('請選擇要上傳的影像')   # 發出快閃訊息 
        # return redirect(url_for('index'))   # 令瀏覽器跳回首頁 
    if file and allowed_file(file.filename):   # 確認有檔案且副檔名在允許之列
        filename = secure_filename(file.filename)  # 轉成「安全的檔名」 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('影像上傳完畢！')
        # 顯示頁面並傳入上傳的檔名
        return render_template('user.html', filename=filename)
    else:
        errorMsg='<i class="bi bi-exclamation-triangle-fill"></i> 僅允許上傳png, jpg, jpeg和mp4影像檔'
        return render_template('user.html',errorMsg=errorMsg)  # 令瀏覽器跳回首頁
@app.errorhandler(413)
def page_not_found(e):
    errorMsg='<i class="bi bi-exclamation-triangle-fill"></i>僅允許上傳16GB的影像檔'
    return render_template('user.html',errorMsg=errorMsg)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', error = 'Not Found'), 404
if __name__ == '__main__':
    app.run(debug = True)

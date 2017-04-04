# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, render_template, url_for, send_from_directory, jsonify

#定数指定
UPLOAD_PIC = '/files/pic'
UPLOAD_STYLE = '/files/style'
UPLOAD_CONVERTED = '/files/converted_pic'
PHISICAL_ROOT = os.path.dirname( os.path.abspath( __file__ ) )
ALLOWED_EXTENSIONS = set(['PNG', 'png', 'JPG', 'jpg', 'jpeg', 'gif'])

#フォルダパス指定
app = Flask(__name__)
app.config['UPLOAD_PIC'] = PHISICAL_ROOT + UPLOAD_PIC
app.config['UPLOAD_STYLE'] = PHISICAL_ROOT + UPLOAD_STYLE
app.config['UPLOAD_CONVERTED'] = PHISICAL_ROOT + UPLOAD_CONVERTED

#Uploadされたファイルの種類を確認し、拡張子を返す。
def allowed_file(filename):
    if '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return filename.rsplit('.',1)[1]


#フォルダの中身を空にする
def clean_dir(dir_url):
    file_list = os.listdir(dir_url)
    if not len(file_list) == 0:
        for a_file in file_list:
            link = os.path.join(dir_url, a_file)
            os.remove(link)
    return True

def :

@app.route('/files/converted_pic/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_CONVERTED'], filename, as_attachment=True)

@app.route('/', methods=['GET'])
def index(message=""):
    if request.method == 'GET':
        pass
    return render_template('index.html')

@app.route('/post/<int:post_id>', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #フォルダ内削除
        clean_dir(app.config['UPLOAD_CONVERTED'])

        #ファイルのアップロード確認
        pic = request.files['input_pic']
        if pic and allowed_file(pic.filename):
            pic_url = os.path.join(app.config['UPLOAD_PIC'], "pct.jpg")
            pic.save(pic_url)
        else:
            message = "Picture File is Invalid."
            app.logger.info(message)
            return jsonify(render_template('index.html', message=message))

        style = request.files['input_style']
        if style and allowed_file(style.filename):
            style_url = os.path.join(app.config['UPLOAD_STYLE'], "style.jpg")
            style.save(style_url)
        else:
            message = "Style File is Invalid."
            app.logger.info(message)
            return jsonify(render_template('index.html', message=message))

        num = int(request.form['num'])
        print(num)

        #outputファイル作成
        output_url = app.config['UPLOAD_CONVERTED']

        #画像変換
        from artStyleTransfer import transfer_process
        transfer_process(output_url, num)

        files = []
        for i in range(num):
            one_file = 'output%d.jpg' % i
            link = os.path.join(app.config['UPLOAD_CONVERTED'], one_file)
            dic_file = {}
            flink = url_for("download_file", filename=one_file, _external=True)
            dic_file['url'] = flink
            dic_file['file_name'] = "cov_%d" %i
            dic_file['flag'] = False
            if i != 0 and (i+1) % 3 == 0: dic_file['flag'] = True
            print(dic_file)
            files.append(dic_file)

        return jsonify(render_template('index.html', files=files))


if __name__ == '__main__':
    host = "ec2-35-163-153-242.us-west-2.compute.amazonaws.com"
    app.run(host=host, port=3002)
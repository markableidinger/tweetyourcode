#!/usr/bin/env python3

from flask import Flask, render_template, request, send_file, jsonify,\
send_from_directory
from text2img import draw_highlighted_text
import io
import base64

app = Flask('__name__')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/download', methods=['POST'])
def download_img():
    img = draw_highlighted_text(request.form['text'], request.form['language'])
    img_io = io.BytesIO(img)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', attachment_filename='code.png', as_attachment=True)


@app.route('/preview', methods=['GET'])
def preview_img():
    img = draw_highlighted_text(request.args.get('text', '', type=str), request.args.get('language', 'python', type=str))
    img_io = io.BytesIO(base64.b64encode(img))
    img_io.seek(0)
    img_tag = '<img src="data:image/png;base64,' + img_io.getvalue() + '"/>'
    return jsonify(tag=img_tag)


if __name__ == "__main__":
    app.run(debug=True)

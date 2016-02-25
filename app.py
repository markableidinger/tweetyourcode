#!/usr/bin/env python3

from flask import Flask, render_template, request, send_file, jsonify,\
send_from_directory
from text2img import draw_text
import io, json, base64

app = Flask('__name__')


def image_to_io(image):
    img_io = io.BytesIO()
    image.save(img_io, 'PNG', quality=100)
    img_io.seek(0)
    return img_io


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/download', methods=['POST'])
def download_img():
    img = draw_text(request.form['text'])
    img_io = image_to_io(img)
    return send_file(img_io, mimetype='image/png', attachment_filename='code.png', as_attachment=True)


@app.route('/preview', methods=['GET'])
def preview_img():
    img = draw_text(request.args.get('text', '', type=str))
    img_io = image_to_io(img)
    # I need to make this binary/string conversion less ugly.
    img_tag = b'<img src="data:image/png;base64,' + base64.b64encode(img_io.getvalue()) + b'"/>'
    img_tag = str(img_tag)
    return jsonify(tag=img_tag[2:-1])


if __name__ == "__main__":
    app.run(debug=True)

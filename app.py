from flask import Flask, render_template, request, send_file
from text2img import draw_text
import io

app = Flask('__name__')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/download', methods=['POST'])
def download_img():
    img = draw_text(request.form['text'])
    print(request.form)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', attachment_filename='code.png', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

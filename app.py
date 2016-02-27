#!/usr/bin/env python3

from flask import Flask, render_template, request, send_file, jsonify,\
send_from_directory, session, redirect
import io
import base64
import json
from twython import Twython
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name


SUPPORTED_LEXERS = ['Text', 'Python', 'Python3', 'NumPy', 'Javascript',
                    'Java', 'Ruby', 'C', 'C++', 'C#', 'JQuery', 'PHP', 'Swift',
                    'HTML', 'CSS', 'R', 'SQL', 'Brainfuck']


def draw_highlighted_text(text, lexer_name):
    """Take a string as input, return an image of the string."""
    return highlight(text, get_lexer_by_name(lexer_name), ImageFormatter(font_name='UbuntuMono'))

app = Flask('__name__')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path) #should probably serve files with nginx


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', lexers=SUPPORTED_LEXERS)


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


@app.route('/tweet_auth', methods=['POST'])
def tweet_auth():
    with open('credentials.json') as creds_file:
        credentials = json.load(creds_file)
    session['app_key'] = credentials['consumer_key']
    session['app_secret'] = credentials['consumer_secret']
    twitter = Twython(session['app_key'], session['app_secret'])
    auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:5000/tweet')
    session['oauth_token'] = auth['oauth_token']
    session['oauth_token_secret'] = auth['oauth_token_secret']
    session['tweet_text'] = request.form['text']
    session['tweet_language'] = request.form['language']
    return redirect(auth['auth_url'])


@app.route('/tweet', methods=['GET'])
def tweet_pic():
    oauth_verifier = request.args['oauth_verifier']
    twitter = Twython(session['app_key'], session['app_secret'],
                      session['oauth_token'], session['oauth_token_secret'])
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    final_oauth_token = final_step['oauth_token']
    final_oauth_token_secret = final_step['oauth_token_secret']
    twitter = Twython(session['app_key'], session['app_secret'],
                      final_oauth_token, final_oauth_token_secret)
    img = draw_highlighted_text(session['tweet_text'], session['tweet_language'])
    img_io = io.BytesIO(img)
    img_io.seek(0)
    response = twitter.upload_media(media=img_io)
    twitter.update_status(status='Testing', media_ids=[response['media_id']])
    return 'success'


if __name__ == "__main__":
    with open('credentials.json') as creds_file:
        credentials = json.load(creds_file)
    app.secret_key = credentials['secret_key']
    app.run(debug=True)

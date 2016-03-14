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
from pygments.styles import get_style_by_name, get_all_styles


SUPPORTED_LEXERS = ['Python3', 'Python', 'NumPy', 'Javascript',
                    'Java', 'Ruby', 'C', 'C++', 'C#', 'JQuery', 'PHP', 'Swift',
                    'HTML', 'CSS', 'R', 'SQL', 'Brainfuck']


def draw_highlighted_text(text, lexer_name, style_name, line_numbers):
    """Take a string as input, return an image of the string."""
    return highlight(text, get_lexer_by_name(lexer_name),
     ImageFormatter(style=get_style_by_name(style_name), line_numbers=line_numbers,
                    font_name='UbuntuMono', font_size=18))

app = Flask('__name__')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', lexers=SUPPORTED_LEXERS, styles=get_all_styles())


@app.route('/download', methods=['POST'])
def download_img():
    img = draw_highlighted_text(request.form['code_text'], request.form['language'],
                                request.form['style'], request.form.get('line_numbers', False))
    img_io = io.BytesIO(img)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', attachment_filename='code.png', as_attachment=True)


@app.route('/preview', methods=['GET'])
def preview_img():
    img = draw_highlighted_text(request.args.get('text', '', type=str),
        request.args.get('language', 'python', type=str),
        request.args.get('style', 'default', type=str),
        request.args.get('line_numbers', 0, type=int))
    img_io = io.BytesIO(base64.b64encode(img))
    img_io.seek(0)
    img_tag = '<img class="preview-img" src="data:image/png;base64,' + img_io.getvalue() + '"/>'
    return jsonify(tag=img_tag)


@app.route('/submit_form', methods=['POST'])
def tweet_auth():
    with open('credentials.json') as creds_file:
        credentials = json.load(creds_file)
    session['app_key'] = credentials['consumer_key']
    session['app_secret'] = credentials['consumer_secret']
    twitter = Twython(session['app_key'], session['app_secret'])
    auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:5000/tweet')
    session['oauth_token'] = auth['oauth_token']
    session['oauth_token_secret'] = auth['oauth_token_secret']
    session['code_text'] = request.form['code_text']
    session['tweet_text'] = request.form['tweet_text']
    session['tweet_language'] = request.form['language']
    session['image_style'] = request.form['style']
    session['line_numbers'] = request.form.get('line_numbers', False)
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
    img = draw_highlighted_text(session['code_text'], session['tweet_language'],
                                session['image_style'], session['line_numbers'])
    img_io = io.BytesIO(img)
    img_io.seek(0)
    response = twitter.upload_media(media=img_io)
    post = twitter.update_status(status=session['tweet_text'], media_ids=[response['media_id']])
    return redirect(post['entities']['media'][0]['url'])

# OLD CODE - Replaced by nginx static file service.
# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('static/js', path) #should probably serve files with nginx


# @app.route('/bootstrap/<path:path>')
# def send_boostrap(path):
#     return send_from_directory('static/bootstrap-3.3.6-dist', path) #should probably serve files with nginx



if __name__ == "__main__":
    with open('credentials.json') as creds_file:
        credentials = json.load(creds_file)
    app.secret_key = credentials['secret_key']
    print(app.run.__doc__)
    app.run(debug=True, host='127.0.0.1')

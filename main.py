from flask import Flask, request, render_template
import re

pattern = r'&t=\d+s'

app = Flask(__name__)

@app.route('/')
def homepage():
    return ("homepage")

@app.route('/<path:url>')
def embed_youtube(url):
    full_url = request.full_path
    video_id = full_url.replace("/https://www.youtube.com/watch?v=", "")
    if "&t=" in video_id:
        video_id = re.sub(pattern, '', video_id)
    else:
        pass
    embed_code = f'<iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
    return render_template('index.html', video_embed=embed_code)

if __name__ == '__main__':
    app.run(port=5000)

    #app.run(host="0.0.0.0", port=5000)   ->    if you want to run it on a server

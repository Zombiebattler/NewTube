from flask import Flask, request, render_template, jsonify
import re
try:
    from pytube import YouTube
except Exception:
    pass


pattern = r'&t=\d+s'

app = Flask(__name__)

def load_likes():
    try:
        with open("static/likes.txt", "r") as file:
            likes = [line.strip() for line in file]
        return likes
    except FileNotFoundError:
        return []

def save_likes(likes):
    with open("static/likes.txt", "w") as file:
        for like in likes:
            file.write(like + "\n")

@app.route('/beta/add_like/<path:id>')
def add_like(id):
    if not "https://www.youtube.com/watch" in id:
        url = f"https://www.youtube.com/watch?v={id}"
        likes = load_likes()
        if url not in likes:
            likes.append(url)
            save_likes(likes)
            return jsonify({"message": "Like wurde hinzugefügt."})
        else:
            return jsonify({"message": "Like bereits vorhanden."})
    else:
        return jsonify({"error": "please only submit youtube id's"})


@app.route('/beta/delete_like/<path:id>')
def delete_like(id):
    if not "https://www.youtube.com/watch" in id:
        url = f"https://www.youtube.com/watch?v={id}"
        likes = load_likes()
        if url in likes:
            likes.remove(url)
            save_likes(likes)
            return jsonify({"message": "Like wurde entfernt."})
        else:
            return jsonify({"error": "Like nicht gefunden."})
    else:
        return jsonify({"error": "please only submit youtube id's"})


@app.route('/beta/likes')
def likes():
    likes = []
    try:
        with open("static/likes.txt", 'r') as file:
            for zeile in file:
                likes.append(zeile.strip())
            return jsonify(likes)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/beta/<path:id>')
def download(id):
    url = f"https://www.youtube.com/watch?v={id}"
    try:
        yt = YouTube(url).streams.get_highest_resolution().download()
        return jsonify(f"Downloaded {yt.title()}")
    except Exception as e:
        return jsonify(f"Error: {e}")

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/<path:url>')
def embed_youtube(url):
    full_url = request.full_path

    print(url)
    if "youtube.com/watch" in url:
        full_url = request.full_path
        if "www." in full_url:
            video_id = full_url.replace("/https://www.youtube.com/watch?v=", "")
        else:
            video_id = full_url.replace("/https://youtube.com/watch?v=", "")
        if "&t=" in video_id:
            video_id = re.sub(pattern, '', video_id)
        else:
            pass
    else:
        video_id = url
    embed_code = f'<iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
    return render_template('index.html', video_embed=embed_code)

if __name__ == '__main__':
    app.run(port=5010)#, host="0.0.0.0")

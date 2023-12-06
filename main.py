from flask import Flask, request, render_template, jsonify
from pytube import YouTube
import logging
import re

pattern = r'&t=\d+s'
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#╔════════ Variables ════════╗


PORT = 5010
open_server = False


#╚════════ Variables ════════╝

class C:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'

def startup():
    version = 1.7
    print(C.GREEN + f"""  _   _            _______    _          
 | \ | |          |__   __|  | |         
 |  \| | _____      _| |_   _| |__   ___ 
 | . ` |/ _ \ \ /\ / / | | | | '_ \ / _ 
 | |\  |  __/\ V  V /| | |_| | |_) |  __/
 |_| \_|\___| \_/\_/ |_|\__,_|_.__/ \___|{C.GREEN} 

[*] - venx0f - Zombiebattler - Verpxnter(mental support)
    
[*] ╔ {C.BLUE}https://github.com/Zombiebattler/NewTube{C.GREEN}     
[*] ╠ {C.BLUE}https://github.com/Zombiebattler{C.GREEN} 
[*] ╚ {C.BLUE}https://github.com/DEanozyp{C.GREEN} 

{C.GREEN}[{C.YELLOW}!{C.GREEN}] - Version: {version}
{C.GREEN}[{C.YELLOW}!{C.GREEN}] - Running on port: {PORT}
{C.GREEN}[{C.YELLOW}!{C.GREEN}] - Open Server: {open_server}
{C.YELLOW}
╔════════ Console-Log ════════╗

    """)
@app.route('/beta/<path:id>')
def download(id):
    url = f"https://www.youtube.com/watch?v={id}"
    print(f"\n{C.GREEN}[{C.YELLOW}*{C.GREEN}] - Downloading {url} . . .")
    try:
        yt = YouTube(url).streams.get_highest_resolution().download()
        print(f"\n{C.GREEN}[{C.GREEN}*{C.GREEN}] - downloaded {yt.title()}")
        return jsonify(f"Downloaded {yt.title()}")
    except Exception as e:
        print(f"\n{C.GREEN}[{C.RED}!{C.GREEN}] - error Downloading video {url}")
        print(f"\n{C.RED}[!] - {e}")
        return jsonify(f"Error: {e}")

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/<path:url>')
def embed_youtube(url):
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
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        print(f"\n{C.GREEN}[{C.YELLOW}*{C.GREEN}] - {yt.title}")
    except Exception:
        print(f"\n{C.GREEN}[{C.RED}!{C.GREEN}] - Youtube Title Not Found")
    return render_template('index.html', video_embed=embed_code)

if __name__ == '__main__':
    startup()
    try:
        if open_server == True:
            app.run(port=PORT, host="0.0.0.0")
        else:
            app.run(port=PORT)
    except Exception:
        print(f"\n{C.RED}[!] - Error while open server\n{C.YELLOW}Try to change the port")
    print("Thanks for using NewTube")

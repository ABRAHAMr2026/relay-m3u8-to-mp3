from flask import Flask, Response, stream_with_context
import subprocess

app = Flask(__name__)

SOURCE_STREAM_URL = "https://stream100.radioarmeria.com:3049/stream/play.m3u8"

def generate():
    command = [
        'ffmpeg',
        '-i', SOURCE_STREAM_URL,
        '-vn',
        '-codec:a', 'libmp3lame',
        '-b:a', '128k',
        '-f', 'mp3',
        '-'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=4096)

    try:
        while True:
            data = process.stdout.read(4096)
            if not data:
                break
            yield data
    finally:
        process.kill()

@app.route('/stream.mp3')
def stream():
    return Response(stream_with_context(generate()), mimetype='audio/mpeg')

@app.route('/')
def index():
    return "Relay M3U8 to MP3 running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


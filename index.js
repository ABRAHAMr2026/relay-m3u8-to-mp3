const express = require('express');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

const streamUrl = 'https://stream100.radioarmeria.com:3049/stream/play.m3u8';

app.get('/stream', (req, res) => {
  res.set({
    'Content-Type': 'audio/mpeg',
    'Transfer-Encoding': 'chunked',
  });

  const ffmpeg = spawn('ffmpeg', [
    '-i', streamUrl,
    '-vn',
    '-acodec', 'libmp3lame',
    '-ab', '128k',
    '-f', 'mp3',
    'pipe:1'
  ]);

  ffmpeg.stdout.pipe(res);

  ffmpeg.stderr.on('data', data => {
    console.error(`FFmpeg error: ${data}`);
  });

  req.on('close', () => {
    ffmpeg.kill('SIGINT');
  });
});

app.listen(PORT, () => {
  console.log(`Servidor funcionando en el puerto ${PORT}`);
});

<h1 align="center">Cassette</h1>

<p align="center">
  <img width="256" src="https://github.com/lohanjs/cassette/blob/main/Cassette.png" alt="Logo">
</p>

<p align="center">A self-hosted Discord music bot.</p>

## Requirements
- py-cord
- pynacl
- pytube
- FFmpeg

## Build for Docker
First, clone the repo and move your working directory into it
```
https://github.com/lohanjs/cassette.git
cd cassette
```
Then build and run with docker
```
docker build -t {IMAGE NAME}
docker run -e TOKEN={YOUR DISCORD TOKEN} -d {IMAGE NAME FROM ABOVE}
```

## Commands
```
Prefix: !
Music:
  leave   Stops music, clears queue and leaves
  now     Shows current song
  pause   Pauses music
  play    Searches or plays link
  queue   Shows queue
  remove  Removes song from queue at selected index
  resume  Resumes music
  shuffle Shuffles queue until disabled
  skip    Skips current song
  skipto  Skips to selected index in queue
  stop    Stops music and clears queue
  stream  Streams audio from live stream URL
No Category:
  help    Shows this message
  ping    Shows bot latency
```

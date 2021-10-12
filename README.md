<h1 align="center">Cassette</h1>

<p align="center">
  <img width="256" src="https://github.com/lohanjs/cassette/blob/main/Cassette.png" alt="Logo">
</p>

<p align="center">A self-hosted Discord music bot.</p>

## Requirements
- py-cord
- pynacl
- pytube

## Setup
Intended to be hosted on Heroku.
- Fork or clone this repo.
- Create a Discord bot and Heroku application.
- Create a Config Var on Heroku called "TOKEN" with your created bot's token as the value.
- Deploy your repo from Heroku.

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
No Category:
  help    Shows this message
  ping    Shows bot latency
```

from typing import List
import mido
from timecode import Timecode
import questionary
import os
import json
import re
import mpvex
import mtc


midi_port = questionary.select(
    "select MIDI in port",
    choices=mido.get_input_names()
).ask()

m3u_path = questionary.path(
    "set m3u path",
    #file_filter=lambda path: os.path.splitext(path)[1] == ".m3u"
).ask()

timeline_path = questionary.path(
    "set timeline path",
    #file_filter=lambda path: os.path.splitext(path)[1] == ".json"
).ask()

with open(timeline_path, "r", encoding="utf-8") as f:
    text = f.read()
re_text = re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
timeline_json = json.loads(re_text)

config_id = questionary.select(
    "select machine id",
    choices=[questionary.Choice(title=f"{c['id']} {c['name']}",value=f"{c['id']}") for c in timeline_json["config"]]
).ask()

port = mido.open_input(midi_port)
timeline = timeline_json["timeline"]
timecodes: List[str] = [t["time"] for t in timeline if config_id in t.keys()]

tc: Timecode = Timecode("30", frames=1)
btc: Timecode = Timecode("30", frames=1)

player: mpvex.MPVEX = mpvex.MPVEX(config="yes", input_default_bindings=True)
decoder: mtc.Decoder = mtc.Decoder()

player.loadlist(m3u_path)

player.playlist_pos = 0

player.pause()

print("Ready")

while player.con:
    msg = port.receive(block=False)
    if msg is not None:
        tc = decoder.receive_message(tc, msg)

    if btc == tc:
        continue

    if tc in timecodes:
        pos = timecodes.index(tc)

        player.playlist_pos = pos

        player.resume()
        print(f"play at {tc}")

    btc = tc

print("Quit")

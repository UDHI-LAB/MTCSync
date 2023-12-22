from typing import List
import mido
from timecode import Timecode
import questionary
import os
import json
import re
import mpvex
import mtc


def file_filter(path: str,ext: str) -> bool:
    return os.path.splitext(path)[1] == ext or not os.path.splitext(path)[1]


midi_port = questionary.select(
    "select MIDI in port",
    choices=mido.get_input_names()
).ask()

m3u_path = questionary.path(
    "set m3u path",
    file_filter=lambda path: file_filter(path, ".m3u")
).ask()

timeline_path = questionary.path(
    "set timeline path",
    file_filter=lambda path: file_filter(path, ".json")
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
playlist = timeline_json["playlist"]
myconfig = [c for c in timeline_json["config"] if c["id"] == config_id][0]
timecodes: List[str] = [t["time"] for t in timeline]

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

        #現在の楽曲の表示
        print(f"{playlist[pos]} play now")

        #タイムラインに自身の指示がない場合はスキップ
        if timeline[pos].get(config_id) is None:
            continue

        #MIDIモードの場合はここがMIDI messageになる
        print(f"{timeline[pos][config_id]}")

        if myconfig["output"] == "player":
            player.resume()
            print(f"play at {tc}")

    btc = tc

print("Quit")

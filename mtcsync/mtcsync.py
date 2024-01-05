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

def check_playlist(player: mpvex.MPVEX):
    if (none_files := [p["filename"] for p in player.playlist if not os.path.isfile(p["filename"])]):
        print("warning: some files are not found")
        print("\n".join(none_files))
        exit(1)

if not (midi_names := mido.get_input_names()):
    print("no MIDI port ;;")
    exit(1)

answers: dict[str, str, str] = questionary.form(
    midi_port = questionary.select(
        "select MIDI in port",
        choices=midi_names
    ),
    m3u_path = questionary.path(
        "set m3u path",
        file_filter=lambda path: file_filter(path, ".m3u")
    ),
    timeline_path = questionary.path(
        "set timeline path",
        file_filter=lambda path: file_filter(path, ".json")
    )
).ask()

if not answers:
    exit()

with open(os.path.expanduser(answers["timeline_path"]), "r", encoding="utf-8") as f:
    text: str = f.read()

re_text: str = re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
timeline_json: dict = json.loads(re_text)

#質問内容の取得にファイルオープンが必要なのでここで行う
config_id: str = questionary.select(
    "select machine id",
    choices=[questionary.Choice(title=f"{c['id']} {c['name']}",value=f"{c['id']}") for c in timeline_json["config"]]
).ask()

if not config_id:
    exit()

port = mido.open_input(answers["midi_port"])
timeline: list[dict]  = timeline_json["timeline"]

playlist: list[dict] = timeline_json["playlist"]
playlist_timeline: list[str] = [p["time"] for p in playlist]
playlist_names: list[str] = [p["name"] for p in playlist]

myconfig: dict = [c for c in timeline_json["config"] if c["id"] == config_id][0]
timecodes: list[str] = [t["time"] for t in timeline]

tc: Timecode = Timecode("30", frames=1)

decoder: mtc.Decoder = mtc.Decoder()

player: mpvex.MPVEX = mpvex.MPVEX(
    config="yes",
    input_builtin_bindings=False,
    pause=True,
    idle=True
)

player.loadlist(os.path.expanduser(answers["m3u_path"]))

check_playlist(player=player)

player.playlist_pos = 0

print("Ready")

while player.is_active:
    msg = port.receive(block=False)
    if msg is not None:
        tc = decoder.receive_message(tc, msg)
    else:
        continue

    if tc in playlist_timeline:
        pos = playlist_timeline.index(tc)

        #現在の楽曲の表示
        print(f"{playlist_names[pos]} is now")

    if tc in timecodes:
        pos = timecodes.index(tc)

        player.playlist_pos = pos

        #タイムラインに自身の指示がない場合はスキップ
        if timeline[pos].get(config_id) is None:
            continue

        #MIDIモードの場合はここがMIDI messageになる
        print(f"{timeline[pos][config_id]}")

        if myconfig["output"] == "player":
            player.resume()
            print(f"play at {tc}")

print("Quit")

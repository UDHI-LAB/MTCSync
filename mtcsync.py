from typing import List
import mido
from timecode import Timecode
import questionary
import os
import mpvex
import mtc


midi_port = questionary.select(
    "select MIDI port",
    choices=mido.get_input_names()
).ask()

m3u_path = questionary.path(
    "set m3u path",
    file_filter=lambda path: os.path.splitext(path)[1] == ".m3u"
).ask()

port = mido.open_input(midi_port)
timecodes: List[str] = ["00:00:05:00", "00:00:20:00"]
i: int = 0
tc: Timecode = Timecode("30", frames=1)

player: mpvex.MPVEX = mpvex.MPVEX(config="yes", input_default_bindings=True)
decoder: mtc.Decoder = mtc.Decoder()

player.loadlist(m3u_path)

player.playlist_pos = 0

player.pause()

while player.con:
    msg = port.receive(block=False)
    if msg is not None:
        tc = decoder.receive_message(tc, msg)

    if len(timecodes) == i:
        continue

    if tc == timecodes[i]:
        if player.is_playing:
            player.playlist_next()

        player.resume()
        print(f"play at {tc}")
        i += 1

print("Quit")

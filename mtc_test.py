import mido
from timecode import Timecode
import questionary
import os

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, "dlls")
os.environ["PATH"] = dllspath + os.pathsep + os.environ["PATH"]

import mpv

def mtc_decode(mtc_bytes):
  rhh, mins, secs, frs = mtc_bytes
  rateflag = rhh >> 5
  hrs = rhh & 31
  fps = ['24', '25', '29.97', '30'][rateflag]
  total_frames = int(frs + float(fps) * (secs + mins * 60 + hrs * 60 * 60))
  # total frames must always be an integer above zero
  if total_frames < 1:
    total_frames = 1
  return Timecode(fps, frames=total_frames)

def mtc_decode_quarter_frames(frame_pieces):
  mtc_bytes = bytearray(4)
  if len(frame_pieces) < 8:
    return None
  for piece in range(8):
    mtc_index = 3 - piece//2    # quarter frame pieces are in reverse order of mtc_encode
    this_frame = frame_pieces[piece]
    if this_frame is bytearray or this_frame is list:
      this_frame = this_frame[1]
    data = this_frame & 15      # ignore the frame_piece marker bits
    if piece % 2 == 0:
      # 'even' pieces came from the low nibble
      # and the first piece is 0, so it's even
      mtc_bytes[mtc_index] += data
    else:
      # 'odd' pieces came from the high nibble
      mtc_bytes[mtc_index] += data * 16
  return mtc_decode(mtc_bytes)

def receive_message(tc, msg) -> Timecode:
  if msg.type == "quarter_frame":
    quarter_frames[msg.frame_type] = msg.frame_value
    if msg.frame_type == 3:
      tc = tc + Timecode("30", frames=1)
    if msg.frame_type == 7:
      tc = mtc_decode_quarter_frames(quarter_frames)
  elif msg.type == "sysex":
    if len(msg.data) == 8 and msg.data[0:4] == (127, 127, 1, 1):
      data = msg.data[4:]
      tc = mtc_decode(data)
  else:
    print(msg)

  return tc

quarter_frames = [0 for _i in range(8)]

midi_port = questionary.select(
  "select MIDI port",
  choices = mido.get_input_names()
).ask() 

port = mido.open_input(midi_port)
timecodes = ["00:00:05:00","00:00:10:00"]
i = 0
tc = Timecode("30", frames=0)

player = mpv.MPV()

player.loadlist("test.m3u")

player.playlist_pos = 0

player._set_property("pause", True)

while True:
  msg = port.receive(block=True)
  tc = receive_message(tc, msg)

  if len(timecodes) == i:
    continue

  if tc == timecodes[i]:
    player._set_property("pause", False)
    print(f"play at {tc}")
    i += 1

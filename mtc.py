from timecode import Timecode

class Decoder:
  def __init__(self) -> None:
    self.quarter_frames = [0 for _i in range(8)]

  def mtc_decode(self, mtc_bytes):
    rhh, mins, secs, frs = mtc_bytes
    rateflag = rhh >> 5
    hrs = rhh & 31
    fps = ['24', '25', '29.97', '30'][rateflag]
    total_frames = int(frs + float(fps) * (secs + mins * 60 + hrs * 60 * 60))
    # total frames must always be an integer above zero
    if total_frames < 1:
      total_frames = 1
    return Timecode(fps, frames=total_frames)

  def mtc_decode_quarter_frames(self, frame_pieces):
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
    return self.mtc_decode(mtc_bytes)

  def receive_message(self, tc, msg) -> Timecode:
    if msg.type == "quarter_frame":
      self.quarter_frames[msg.frame_type] = msg.frame_value
      if msg.frame_type == 3:
        tc = tc + Timecode("30", frames=1)
      if msg.frame_type == 7:
        tc = self.mtc_decode_quarter_frames(self.quarter_frames)
    elif msg.type == "sysex":
      if len(msg.data) == 8 and msg.data[0:4] == (127, 127, 1, 1):
        data = msg.data[4:]
        tc = self.mtc_decode(data)
    else:
      print(msg)

    return tc
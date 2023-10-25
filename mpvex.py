import os

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, "dlls")
os.environ["PATH"] = dllspath + os.pathsep + os.environ["PATH"]

import mpv

class MPVEX(mpv.MPV):
  def __init__(self, *extra_mpv_flags, log_handler=None, start_event_thread=True, loglevel=None, **extra_mpv_opts):
    super().__init__(*extra_mpv_flags, log_handler=log_handler, start_event_thread=start_event_thread, loglevel=loglevel, **extra_mpv_opts)
    self.register_key_binding("CLOSE_WIN", self.q)
    self.register_event_callback("end-file", self.endf)
    self.is_playing = True
    self.con = True

  def pause(self):
    self._set_property("pause", True)
    self.is_playing = False

  def unpause(self):
    self._set_property("pause", False)
    self.is_playing = True

  def q(self):
    self.con = False

  def endf(self, event):
    reason = event.as_dict()["reason"].decode(encoding="utf-8")
    if reason == "eof":
      self.pause()
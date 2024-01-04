import os

basepath: str = os.path.dirname(os.path.abspath(__file__))
dllspath: str = os.path.join(basepath, "lib")
os.environ["PATH"] = dllspath + os.pathsep + os.environ["PATH"]

import mpv

class MPVEX(mpv.MPV):
    def __init__(self, *extra_mpv_flags, log_handler=None, start_event_thread=True, loglevel=None, **extra_mpv_opts):
        super().__init__(*extra_mpv_flags, log_handler=log_handler,
                         start_event_thread=start_event_thread, loglevel=loglevel, **extra_mpv_opts)
        self.on_key_press("CLOSE_WIN")(self.close)
        self.on_key_press("f")(self.toggle_fullscreen)
        self.register_event_callback(self.handler)
        self.is_playing: bool = False
        self.is_active: bool = True
        self.is_fullscreen: bool = False

    def play(self, filename):
        self.is_playing = True
        return super().play(filename)

    def loadlist(self, filename):
        self.is_playing = True
        return super().loadlist(filename)

    def pause(self):
        self._set_property("pause", True)
        self.is_playing = False

    def resume(self):
        self._set_property("pause", False)
        self.is_playing = True

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self._set_property("fullscreen", False)
        else:
            self._set_property("fullscreen", True)

        self.is_fullscreen = not self.is_fullscreen

    def close(self):
        self.is_active = False

    def handler(self, event):
        if event.as_dict()["event"].decode(encoding="utf-8") != "end-file":
            return
        reason = event.as_dict()["reason"].decode(encoding="utf-8")
        if reason == "eof":
            self.pause()

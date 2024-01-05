import os

basepath: str = os.path.dirname(os.path.abspath(__file__))
dllspath: str = os.path.join(basepath, "lib")

if os.name == "nt":
    os.environ["PATH"] = dllspath + os.pathsep + os.environ.get("PATH", "")
else:
    os.environ["DYLD_LIBRARY_PATH"] = dllspath + os.pathsep + os.environ.get("DYLD_LIBRARY_PATH", "")


import mpv

class MPVEX(mpv.MPV):
    def __init__(self, *extra_mpv_flags, log_handler=None, start_event_thread=True, loglevel=None, **extra_mpv_opts):
        super().__init__(*extra_mpv_flags, log_handler=log_handler,
                         start_event_thread=start_event_thread, loglevel=loglevel, **extra_mpv_opts)

        self.on_key_press("CLOSE_WIN")(self.close)
        self.on_key_press("F11")(self.toggle_fullscreen)
        self.register_event_callback(self.handler)

        self.is_active: bool = True

    def play(self, filename):
        return super().play(filename)

    def loadlist(self, filename):
        return super().loadlist(filename)

    def pause(self):
        self._set_property("pause", True)

    def resume(self):
        self._set_property("pause", False)

    def toggle_fullscreen(self):
        if self._get_property("fullscreen"):
            self._set_property("fullscreen", False)
        else:
            self._set_property("fullscreen", True)

    def close(self):
        self.is_active = False

    def handler(self, event):
        if event.as_dict()["event"].decode(encoding="utf-8") != "end-file":
            return
        reason = event.as_dict()["reason"].decode(encoding="utf-8")
        if reason == "eof":
            self.pause()

# MTCSync

# Overview

MTC(MIDI Time Code)を用いたライブ全体の同期システム

# Requirement

MTC 送信ツール  
(Recommended [MTCsender](https://www.styletronix.net/Software/MTC/Default.aspx))

MIDI ループバックツール(照明等操作用)  
(Recommended [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html))

libmpv

# Usage

```# poetry run py(thon) mtcsync.py```

# Features

- [x] MTC decode
- [x] mpv link
- [x] load timeline
- [x] support full screen
- [ ] check timeline
- [ ] timeline create tool
- [ ] output MIDI
- [ ] setting GUI
- [ ] auto stop

# License
[MIT License](LICENSE.md)

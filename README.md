# MTCSync

# Overview

MTC(MIDI Time Code)を用いたライブ全体の同期システム

# Requirement

[MTCsender](https://www.styletronix.net/Software/MTC/Default.aspx)
MTCを送信できるアプリケーションこのデータを用いて同期を行う

[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
ローカルPC内でMIDI信号をループバックできるアプリケーション
照明操作やVJアプリの対応はこのアプリケーションを用いて行う

## macOS
- libmpv.so
- mido
- python-rtmidi(requirement mido)
- timecode
- questionary

## Windows
- libmpv.dll
- mido
- python-rtmidi(requirement mido)
- timecode
- questionary

# Usage

```# py(thon) mtcsync.py```

# Features

- [x] MTC decode
- [x] mpv link
- [ ] load timeline
- [ ] output MIDI
- [ ] setting GUI
- [ ] auto stop

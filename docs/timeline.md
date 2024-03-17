# MTCSync 統合シナリオファイル

ファイル形式はjsonもしくはjsoncである

```jsonc
{
    "header": {
        "frameRate":"30 or 60" //recommend 30
    },
    "config":[
        {
            "id":"unique", //unique,require
            "name":"opt", //option  
            "output":"midi,player"
        }
    ],      

    "playlist":[
        {
            "name":"{name}",
            "time":"HH:MM:SS:FF"
        },
        {
            "name":"{name}",
            "time":"HH:MM:SS:FF"
        }
    ],

    "timeline":[
        {
            "time":"HH:MM:SS:FF", //require,MasterClockの経過時計(絶対値)
            "{configID}":"MIDI Message",
            "{configID}":"play"
        },
        {   
            "time":"HH:MM:SS:FF", //require
            "{configID}":"MIDI Message",
            "{configID}":"play"
        }
    ]
}
```

### header

MTCSync自体の設定等

| key | value | require | default |
| ---- | ---- | ---- | ---- |
| framerate | MTCのフレームレート | × | "30" |

### config

端末設定の配列

| key | value | require | default |
| ---- | ---- | ---- | ---- |
| id | 端末識別ID | 〇 |  |
| name | 端末識別名 | × |  |
| output | 動画プレイヤーかMIDIアウトプットかを区別 | 〇 |  |

### playlist

演目の配列

| key | value | require | default |
| ---- | ---- | ---- | ---- |
| name | 演目名 | 〇 |  |
| time | 演目の開始時間 | 〇 |  |

### timeline

タイムラインタスクの配列

| key | value | require | default |
| ---- | ---- | ---- | ---- |
| time | タスクの開始時間 | 〇 |  |
| {configID} | {configID}がやること | 〇 |  |

### 動画プレイヤータスク

動画プレイヤーではあらかじめ設定されたコマンドのみが使用可能

| command | action |
| ---- | ---- |
| play | 次の動画の再生を行う |

### MIDIアウトプットタスク

MIDIアウトプットでは自由なMIDIメッセージの送信が可能
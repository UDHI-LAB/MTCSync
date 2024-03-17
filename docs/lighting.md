# MTCSync ライティングファイル

ファイル形式はjsonもしくはjsoncである  
ライティングファイルは一曲ごとに作成しintegratorを通すことで全体シナリオファイルへと統合される

```jsonc
{ //曲名を書くと後からわかりやすくできる
    "header": {
        "programID":"unique", //シナリオファイルのplaylist.id
        "configID":"unique", //シナリオファイルのconfig.id
    },

    "order":{
        "FOG":{
            "ON":"MIDI Message",
            "OFF":"MIDI Message"
        },
        "WASH":{
            "ON":"MIDI Message",
            "OFF":"MIDI Message"
        },
    },

    "timeline":[
        {
            "time":"00:00:00:00",
            "order":"FOG.ON"
        },
        {
            "time":"00:00:10:00",
            "order":"WASH.ON"
        }
    ]
}
```

### header

このライティングファイルがどの端末のどの演目用のものかを定義

| key | value | require | default |
| ---- | ---- | ---- | ---- |
| playlistID | シナリオファイルのplaypistID | 〇 |  |
| configID | シナリオファイル内のconfigID | 〇 |  |

### order

MIDIメッセージの識別をしやすくするための定義  
次の2種の形式を許容する

#### 基本形式
1つのMIDIメッセージ一式を1つの命令を紐づける
```jsonc
{
    "SPIN": "MIDI Message"
}
```

#### 拡張形式
基本形式の命令をタグ付けし拡張する  
この拡張は入れ子構造に繰り返すことができる
```jsonc
{
    "FOG": {
        "ON": "MIDI Message",
        "OFF": "MIDI Message"
    }
}
```
呼び出す場合は次のように記載する
`FOG.ON` `FOG.OFF`


### timeline

演目中の動作を設定

| key | value | require | default |
| ---- | ---- | ---- | ---- |
| time | 演目開始後からの相対時間 | 〇 |  |
| order | 上記orderで定義したアクションを使用 | 〇 |  |

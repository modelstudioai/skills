# 调用官方Agent

多模态交互开发套件提供一系列Agent，可应用于生活、学习、工作等不同场景。

<a id="新闻电台"></a>

<a id="a257ea22fehol"></a>

## 新闻电台

新闻电台每日更新科技、娱乐等不同领域的热门资讯，由两位AI主播进行播报和讨论。

用户可以选择节目进行收听，也可以发言打断电台节目，加入到讨论中与两位AI主播进行交流。

本Agent目前仅在多模态交互应用中支持。

<a id="设置方式"></a>

<a id="0df625e5cbb4k"></a>

#### 设置方式

| 入参 | 配置方式 | 是否必传 | 说明 |
| --- | --- | --- | --- |
| podcast\_channel | sdk | 否 | 支持参数：technology / entertainment / social |
| podcast\_name | 管控台 | 否 | 用户指定的电台节目名称，通常会在节目首句进行播报，默认名称为“新闻电台”，支持管控台配置 |
| speaker\_1\_voice | 管控台 | 否 | 指定第一个播报人的声音，音色取值范围取决于应用中配置的tts模型支持的声音列表 |
| speaker\_2\_voice | 管控台 | 否 | 指定第二个播报人的声音，音色取值范围取决于应用中配置的tts模型支持的声音列表 |

客户端调用示例，在Start消息的payload.biz\_params节点下，通过如下格式设置要播放的新闻类别：

<a id="code-block"></a>

```json
{
  "user_defined_params": {
    "news_radio": {
      "podcast_channel": "technology"
    }
  }
}
```

<a id="使用方式"></a>

<a id="3eea3a3f397ir"></a>

#### 使用方式

在语音通话中说“进入新闻电台”。

<a id="语音翻译"></a>

<a id="231a402a82pkh"></a>

## 语音翻译

**注意：本Agent仅支持在duplex模式下使用，过程中无论用户是否在说话，都必须持续上传音频数据。**

提供类似同传翻译的实时翻译能力，在持续收音的同时输出翻译结果，适用于演讲，会议等大段语音场景。

目前支持对部分语言的翻译结果进行实时语音播报：

-   翻译语言为中文或英文：使用用户指定的音色播报
-   翻译语言为日文或韩文：使用系统默认的音色播报

<a id="设置方式-2"></a>

<a id="0e75f83e1feva"></a>

#### 设置方式

要开启语音播报能力，请在管控台语音翻译Agent选项中勾选“翻译语音”。

要指定默认翻译语种，请在开始会话的Start指令中传参：

<table><thead><tr><th><p><strong>入参</strong></p></th><th><p><strong>配置方式</strong></p></th><th><p><strong>是否必传</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>modelName</p></td><td><p>sdk</p></td><td><p>否</p></td><td><p>翻译模型，目前只支持&quot;gummy&quot;</p></td></tr><tr><td><p>sourceLanguage</p></td><td><p>sdk</p></td><td><p>否</p></td><td><p>源语言，也就是用户说的语言，目前支持的语言代码：</p><ul><li><p>zh: 中文</p></li><li><p>en: 英文</p></li><li><p>ja: 日语</p></li><li><p>yue: 粤语</p></li><li><p>ko: 韩语</p></li><li><p>de: 德语</p></li><li><p>fr: 法语</p></li><li><p>ru: 俄语</p></li><li><p>it: 意大利语</p></li><li><p>es: 西班牙语</p></li><li><p>th: 泰语</p></li><li><p>ms: 马来语</p></li><li><p>id: 印尼语</p></li></ul></td></tr><tr><td><p>translationLanguages</p></td><td><p>sdk</p></td><td><p>否</p></td><td><p>翻译的目标语言，是一个列表，不过目前只支持传入一个语种，语种代码与<code>source_language</code>参数一致。模型支持的源语言到目标语言翻译组合包括：</p><p>中-&gt;英，中-&gt;日，中-&gt;韩，</p><p>英-&gt;中，英-&gt;日，英-&gt;韩，</p><p>（日、韩、粤、德、法、俄、意、西、泰、马来、印尼）-&gt;（中、英）</p></td></tr><tr><td><p>翻译语音</p></td><td><p>管控台</p></td><td><p>否</p></td><td><p>设置是否把翻译结果合成语音播报出来，默认为不播报。</p></td></tr></tbody></table>

客户端调用示例，在Start消息的payload.biz\_params节点下，通过如下格式设置源语种和要翻译到的目标语种：

<a id="code-block-2"></a>

```json
{
    "user_defined_params": {
        "voice_translate": {
            "modelName": "gummy",
            "translationLanguages": "[\"en\"]",
            "sourceLanguage": "zh"
        }
    }
}
```

<a id="使用方式-2"></a>

<a id="efa43b4961z6u"></a>

#### 使用方式

-   在语音通话中说“打开语音翻译”。此时如果sdk请求时设置了源语言和目标语言，则会直接进入翻译模式；否则会追问从哪种语言翻译到哪种语言。
-   在语音通话中说”打开语音翻译，把中文翻译成英文“，则会直接进入翻译模式，按指令中的语种进行翻译。
-   在翻译模式中说”退出语音翻译“，则会退出翻译模式。

<a id="拍照问答"></a>

<a id="d7ae29429ek0s"></a>

## 拍照问答

当识别到用户有理解当前画面的意图（如“我面前有什么”）时，自动下发拍照指令，并对照片进行理解分析并回复。无需用户手动拍照。

本Agent仅在多模态交互应用中支持。

<a id="设置方式-3"></a>

<a id="df55da64716r6"></a>

#### 设置方式

管控台拍照问答Agent配置界面中可以设置Agent人设，还可以添加自定义触发指令。

<a id="使用方式-3"></a>

<a id="d19533bcfaqsb"></a>

#### 使用方式

在语音通话中说“拍照看看我手里拿着什么？”此时服务会下发拍照问答指令，客户端收到指令后，需要等待StateChanged消息，确定状态切换到Listening之后，再按指定格式上传图片数据，服务会分析图片并语音返回分析结果。

服务端拍照问答指令示例，在RespondingContent事件中output.extra\_info.commands的值是一个JSON格式字符串，其中 name="visual\_qa"

<a id="code-block-3"></a>

```json
{
    "extra_info": {
        "commands": "[{\"name\":\"visual_qa\",\"params\":[{\"name\":\"shot\",\"value\":\"拍照看看\",\"normValue\":\"True\"}]}]"
    }
}
```

客户端上传图片消息示例：

<a id="code-block-4"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "9B32878******************3D053",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "RequestToRespond",
          "dialog_id": "b3939********************81f7",
          "type": "prompt",
          "text": "看我手里拿着什么？"
        },
        "parameters":{
          "images":[{
              "type": "url",
              "value": "https://your.server.name/path/abc.jpg"
          }]
        }
    }
}
```

<a id="视频通话"></a>

<a id="f02e7eab12wvo"></a>

## 视频通话

能够与用户实时视频对话，分析用户动作、环境等视觉信息，客户端需要通过UpdateInfo消息（websocket链路）上传摄像头截图供服务分析，发送频率建议每秒2张。

本Agent仅在多模态交互应用中支持。

<a id="设置方式-4"></a>

<a id="98c55677f371l"></a>

#### 设置方式

管控台视频通话Agent配置界面中可以设置Agent人设，还可以添加自定义启动、退出指令。

<a id="使用方式-4"></a>

<a id="748841382dbnj"></a>

#### 使用方式

进入视频通话：客户端在听（Listening）状态时，发送RequestToRespond指令，biz\_params中包括进入视频通话的信息，服务就会进入视频通话模式，而且会下发提示语。提示语播放完StateChanged回到听（Listening）状态就已经是视频通话模式了。

<a id="code-block-5"></a>

```json
{
    "biz_params": {
        "videos": [
            {
                "action": "connect",
                "type": "voicechat_video_channel"
            }
        ]
    }
}
```

进入视频通话模式后，对话流程与普通语音对话相同，只是客户端额外需要每隔 500ms 通过 UpdateInfo 指令上传一张视频截图，建议为720p或480p的jpeg图像，大小不超过180KB。图像二进制数据经过base64编码直接放在参数中，不需要加其他信息。注意目前每条指令只能传一张图。

<a id="code-block-6"></a>

```json
{
    "parameters":{
        "images":[{
            "type": "base64",
            "value": "base64String"
        }]
    }
}
```

退出视频通话：客户端在听（Listening）状态时，发送RequestToRespond指令，biz\_params中包括退出视频通话的信息，服务就会退出视频通话模式，而且会下发提示语。

<a id="code-block-7"></a>

```json
{
    "biz_params": {
        "videos": [
            {
                "action": "exit",
                "type": "voicechat_video_channel"
            }
        ]
    }
}
```

<a id="辅助指令"></a>

<a id="b91f033bc98ba"></a>

#### 辅助指令

为了能在普通对话过程中自然地进入/退出视频通话模式，服务也提供了意图识别指令，可通知客户端用户的对应意图。客户端收到指令后，需要等待StateChanged消息，确定状态切换到Listening之后，再发起RequestToRespond请求。

例如，在语音通话中用户说“进入视频通话”此时服务会识别到用户意图，在RespondingContent消息中下发进入视频通话指令：

<a id="code-block-8"></a>

```json
{
    "extra_info": {
        "commands": "[{\"name\":\"open_videochat\",\"params\":[]}]"
    }
}
```

在视频通话模式中用户说“退出视频通话”此时服务会识别到用户意图，在RespondingContent消息中下发退出视频通话指令：

<a id="code-block-9"></a>

```json
{
    "extra_info": {
        "commands": "[{\"name\":\"quit_videochat\",\"params\":[]}]"
    }
}
```

<a id="极速视频通话"></a>

<a id="c93ac4aab3x24"></a>

## 极速视频通话

**注意：本Agent仅支持多模态交互应用的duplex模式，语音应用和其他模式下无法使用。对话过程中无论用户是否在说话，都必须持续上传音频数据。视频对话时，必须按要求上传图片数据。**

基于千问-Omni模型，支持实时视频对话，可分析用户动作、环境等视觉信息。客户端需要通过UpdateInfo消息（WebSocket链路）上传摄像头截图供服务分析，发送频率建议每秒2张。

相比于视频通话Agent，本极速视频通话响应速度更快，但只支持闲聊，不支持任何指令、插件功能。

<a id="设置方式-5"></a>

<a id="2589c8cf12ypc"></a>

#### 设置方式

要启用极速视频通话能力，请在管控台Agent->百炼应用中添加“极速视频通话”。

在“极速视频通话”Agent界面中还可以添加自定义启动指令和退出指令。

<a id="使用方式-5"></a>

<a id="e378a4f705acl"></a>

#### 使用方式

在语音通话中说出启动指令，如“打开极速视频通话”。服务正确识别到意图后，会下发提示语音和开始发送视频信息的指令，然后进入视频通话模式。客户端收到指令后应当等对话状态切换到Listening之后开始上传摄像头截图数据。

<a id="code-block-10"></a>

```json
{
    "extra_info": {
        "commands": "[{\"name\":\"send_video_stream\",\"params\":[]}]"
    }
}
```

在视频对话过程中说出退出指令，如“退出极速视频通话”。服务正确识别到意图后，会下发提示语音和停止发送视频信息的指令，然后退出视频通话模式。客户端收到指令后应当停止上传摄像头截图数据。

<a id="code-block-11"></a>

```json
{
    "extra_info": {
        "commands": "[{\"name\":\"stop_video_stream\",\"params\":[]}]"
    }
}
```

<a id="儿童故事"></a>

<a id="679ba260bbn6t"></a>

## 儿童故事

儿童故事配有丰富故事库，通过联网搜索和大模型能力补充故事范围。

支持用户点播故事内容，可在讲故事中途随时打断，发起故事问答or故事续改写，并在结束问答后无缝衔接原故事进度。

本Agent仅在多模态交互应用中支持。

<a id="设置方式-6"></a>

<a id="94d1e02316h9w"></a>

#### 设置方式

| 入参 | 配置方式 | 是否必传 | 说明 |
| --- | --- | --- | --- |
| speaker\_1\_voice | 管控台 | 否 | 指定故事播报的声音，音色取值范围取决于应用中配置的tts模型支持的声音列表 |

客户端调用示例，在Start消息的payload.biz\_params节点下，通过如下格式设置要使用的播报音色：

<a id="code-block-12"></a>

```json
{
  "user_defined_params": {
    "children_story": {
      "speaker_1_voice": "请替换为儿童故事配置的tts模型对应的音色"
    }
  }
}
```

<a id="使用方式-6"></a>

<a id="15dd16236bv5e"></a>

#### 使用方式

在语音通话中说“打开故事模式”。

<a id="智能纪要"></a>

<a id="7a81de1544xz9"></a>

## 智能纪要

智能纪要Agent能够对用户提供的实时或离线录音进行智能总结分析。

本Agent可在多模态交互开发套件和通义听悟Agent中的[智能纪要](../application-user-guide/agent-development/application-gallery/official-application-tingwu-agent/tingwu-meeting.md)中使用。

<a id="设置方式-7"></a>

<a id="f214c4545ddew"></a>

### 设置方式

需要用户的端侧和后台服务侧配合进行完整的体验来使用，完整的集成参考：

-   [实时转写能力集成](realtime-tingwu-meeting-agent-integration-13caf4635d7f9e89.md)
-   [离线转写能力集成](fast-integrate-offline-tingwu-meeting-agent-c9061ca43c1cff3c.md)

# EndToEndRealTimeDialog - 语音实时对话

本接口通过 WebSocket 协议实现实时语音对话转写、意图识别、话术语音合成返回等功能，支持多种音频格式的输入输出，满足实时性与高兼容性需求。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/EndToEndRealTimeDialog)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/EndToEndRealTimeDialog)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

dianjin:EndToEndRealTimeDialog

none

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/ws/realtime/dialog HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

业务空间 Id

llm-xxxxx

asrModelId

string

否

语音识别模型 id。默认为 nls-base。目前支持 paraformer-realtime-v2、paraformer-realtime-8k-v2 等。

枚举值：

-   paraformer-realtime-v1：paraformer-realtime-v1。
-   nls-base：nls-base。

nls-base

ttsModelId

string

否

语音合成模型 id。默认为 nls-base。支持 cosyvoice-v2。

nls-base

inputFormat

string

否

输入音频格式，支持 pcm/wav/mp3

pcm

outputFormat

string

否

输出音频格式

wav

sampleRate

string

否

采样率

SAMPLE\_RATE\_16K

voiceCode

string

是

音色参数值，仅限于支持字/句级别时间戳。

longxiaochun\_v2

volume

integer

否

音量，范围是 0~100，可选，默认 50。

50

speechRate

integer

否

朗读语速。 ● 当 ttsModelId 为 nls-base 时：范围是-500~500，默认是 0。 ● 当 ttsModelId 为 cosyvoice-v2 时： 指定合成音频的语速，取值范围：0.5~2。 ○ 0.5：表示默认语速的 0.5 倍速。 ○ 1：表示默认语速。默认语速是指模型默认输出的合成语速，语速会因发音人不同而略有不同。约每秒钟 4 个字。 ○ 2：表示默认语速的 2 倍速。

0

pitchRate

integer

否

朗读语调。 ● 当 ttsModelId 为 nls-base 时： 范围是-500~500，默认是 0。 ● 当 ttsModelId 为 cosyvoice-v2 时：指定合成音频的语调，取值范围：0.5~2。

0

# [](#客户端请求消息)客户端请求消息

## [](#通用字段说明)通用字段说明

字段名

说明

type

消息类型

seq

消息序列号

timestamp

毫秒时间戳

## [](#starttranscription-开始实时转录)StartTranscription （开始实时转录）

### [](#作用开始实时转录并创建实时会话)作用：开始实时转录，并创建实时会话。

```json
type:StartTranscription
seq:1
timestamp:1719242591197

{
    "playCode": "c00aa8467a",   // 场景编码
    "metaData": {},   // 元数据，此处可添加一些 k-v 对，用于开场白占位等。如在场景管理中的开场白中设置了占位符${name}，此处可传入{"name": "张三"}。
    "selfDirected": true   // 是否开启自主问答（当意图识别为其它时，会使用模型自主回答的能力）
}
```

## [](#processtranscription发送音频数据)ProcessTranscription（发送音频数据）

### [](#作用上传一段音频数据)作用：上传一段音频数据

```json
type:ProcessTranscription
seq:1
timestamp:1719242591197
ack:required

{
	"dataSourceType": "customer",   // 数据源类型
	"data": [0,0,0,0,0]   // 二进制音频流
}
```

-   dataSourceType 标识数据来源（如“customer”, “service”）
    -   customer 表示客户音频数据
    -   service 表示运营商等三方提示音的音频数据
    -   请注意进行区分，可只发送客户的音频数据，该接口暂不处理来源为 service 的音频数据。

## [](#stoptranscription停止转录)StopTranscription（停止转录）

### [](#作用主动结束实时会话)作用：主动结束实时会话

```json
type:StopTranscription
seq:1
timestamp:1719242591197

{}
```

payload 为空

## 返回参数

名称

类型

描述

示例值

object

RealTimeDialogResp

requestId

string

请求 id

1C98B466-D6E0-5252-A60B-F345CBB33DDB

# [](#服务端返回推送消息)服务端返回（推送）消息

## [](#transcriptionstarted会话转录已开始)TranscriptionStarted（会话/转录已开始）

```json
type:TranscriptionStarted
seq:1
timestamp:1752922002409

{
    "sessionId": "1752922001S001nojxboa26z",  // 业务会话唯一标识
    "openingRemarks": "你好，请问你是李先生吗"  // 开场白文本
}
```

-   sessionId：业务会会话唯一标识
-   openingRemarks：开场白内容；文本内容。

## [](#transcriptionresultchanged转写文本变化asr-结果)TranscriptionResultChanged（转写文本变化「ASR 结果」）

```json
type:TranscriptionResultChanged 
seq:29 
timestamp:1754659632826 

{
  "content": "是的，你",
  "messageId":"5da6a7211fd54f7087f74f2f028308e7"
}
```

-   content：当前转写文本内容
-   messageId：消息唯一标识

## [](#sentenceend一句话转写完成流式返回客服回复的音频数据)SentenceEnd（一句话转写完成「流式返回客服回复的音频数据」）

```json
type:SentenceEnd 
seq: 3 
timestamp: 1754659629166

{
  "data": [73,68,51,4,0,0,0],    // 语音的二进制数据
  "messageId": "",    // 消息唯一标识
  "messageEnd": true   // 本轮消息结束标识
}
```

## [](#bizprocessing业务意图识别结果)BizProcessing（业务意图识别结果）

```json
type:BizProcessing 
seq: 3 
timestamp: 1754659629166

{
  "id": "175465963554371b6ffdea5eb446188fc366df451b23b",
  "choices": [
    {
      "index": 0,
      "finishReason": "stop",
      "delta": {
        "intentionCode": "1940679612569849856",
        "intentionScript": "您好，这里这边是 xxx”，我们看到您有一笔 x 万的预审额度，所以提醒您到咱们微信小程序或 APP 看一下呢。",
        "intentionName": "客户询问来电身份",
        "callTime": "819",
        "hangUpDialog": false,
        "interrupt": false
      }
    }
  ],
  "created": "1754659635543",
  "success": true
}
```

-   主要输出意图识别相关文本内容，输出字段描述请参考 API: [RealTimeDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-realtimedialog)

## [](#sentenceinterrupted句子中断需清理音频缓存)SentenceInterrupted（句子中断「需清理音频缓存」）

```json
type:SentenceInterrupted 
seq: 32 
timestamp: 1754659635543 

{}
```

-   body 内容为空 收到此消息需清空音频缓存、终止播放之前的音频内容，以实现打断效果。

## [](#transcriptionend转录结束会话建议结束智能体判断会话可结束)TranscriptionEnd（转录结束「会话建议结束：智能体判断会话可结束」）

```json
type:TranscriptionEnd 
seq: 367 
timestamp: 1754659669964 

{}
```

## [](#transcriptioncompleted转写完全结束可主动断开-websocket-连接)TranscriptionCompleted（转写完全结束，可主动断开 WebSocket 连接）

```json
type:TranscriptionCompleted
seq:3
timestamp:1752922030325

{}
```

## [](#状态码与错误处理)状态码与错误处理

若连接/发送消息出错，服务端返回标准格式 Error 消息：

```json
type:Error
seq:3
timestamp:1752922030325

{
  "code": "401",
  "message": "Token 无效或已过期"
}
```

常见错误码：

code

描述

400

请求参数错误

401

鉴权失败

500

服务内部出错

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "1C98B466-D6E0-5252-A60B-F345CBB33DDB"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-10-28

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/EndToEndRealTimeDialog?updateTime=2025-10-28#workbench-doc-change-demo)

## [](#交互流程)交互流程

![](data:image/svg+xml;utf8,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22us-ascii%22%20standalone%3D%22no%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20contentStyleType%3D%22text%2Fcss%22%20height%3D%22896px%22%20preserveAspectRatio%3D%22none%22%20style%3D%22width%3A462px%3Bheight%3A896px%3Bbackground%3A%23FFFFFF%3B%22%20version%3D%221.1%22%20viewBox%3D%220%200%20462%20896%22%20width%3D%22462px%22%20zoomAndPan%3D%22magnify%22%3E%3Cdefs%2F%3E%3Cg%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3Bstroke-dasharray%3A5.0%2C5.0%3B%22%20x1%3D%2233%22%20x2%3D%2233%22%20y1%3D%2236.2969%22%20y2%3D%22860.8828%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3Bstroke-dasharray%3A5.0%2C5.0%3B%22%20x1%3D%22354%22%20x2%3D%22354%22%20y1%3D%2236.2969%22%20y2%3D%22860.8828%22%2F%3E%3Crect%20fill%3D%22%23E2E2F0%22%20height%3D%2230.2969%22%20rx%3D%222.5%22%20ry%3D%222.5%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%20width%3D%2256%22%20x%3D%225%22%20y%3D%225%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2214%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2242%22%20x%3D%2212%22%20y%3D%2224.9951%22%3E%26%2323458%3B%26%2325143%3B%26%2331471%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23E2E2F0%22%20height%3D%2230.2969%22%20rx%3D%222.5%22%20ry%3D%222.5%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%20width%3D%2256%22%20x%3D%225%22%20y%3D%22859.8828%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2214%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2242%22%20x%3D%2212%22%20y%3D%22879.8779%22%3E%26%2323458%3B%26%2325143%3B%26%2331471%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23FFA500%22%20height%3D%2230.2969%22%20rx%3D%222.5%22%20ry%3D%222.5%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%20width%3D%2256%22%20x%3D%22326%22%20y%3D%225%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2214%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2242%22%20x%3D%22333%22%20y%3D%2224.9951%22%3E%26%2326381%3B%26%2321153%3B%26%2331471%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23FFA500%22%20height%3D%2230.2969%22%20rx%3D%222.5%22%20ry%3D%222.5%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%20width%3D%2256%22%20x%3D%22326%22%20y%3D%22859.8828%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2214%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2242%22%20x%3D%22333%22%20y%3D%22879.8779%22%3E%26%2326381%3B%26%2321153%3B%26%2331471%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%223%22%20style%3D%22stroke%3A%23EEEEEE%3Bstroke-width%3A1.0%3B%22%20width%3D%22455%22%20x%3D%220%22%20y%3D%2266.8633%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%2266.8633%22%20y2%3D%2266.8633%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%2269.8633%22%20y2%3D%2269.8633%22%2F%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%2223.1328%22%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A2.0%3B%22%20width%3D%22108%22%20x%3D%22173.5%22%20y%3D%2256.2969%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2289%22%20x%3D%22179.5%22%20y%3D%2272.3638%22%3E1.%20%26%2321457%3B%26%2336215%3B%26%2321644%3B%26%2330830%3B%26%2335748%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C117.1289%2C352%2C121.1289%2C342%2C125.1289%2C346%2C121.1289%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22121.1289%22%20y2%3D%22121.1289%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2240%22%20y%3D%22116.063%22%3E1%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22131%22%20x%3D%2253%22%20y%3D%22116.063%22%3E%26%2324314%3B%26%2331435%3B%20WebSocket%20%26%2336830%3B%26%2325509%3B%3C%2Ftext%3E%3Cpath%20d%3D%22M359%2C94.4297%20L359%2C134.4297%20L432%2C134.4297%20L432%2C104.4297%20L422%2C94.4297%20L359%2C94.4297%20%22%20fill%3D%22%23FEFFDD%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%2F%3E%3Cpath%20d%3D%22M422%2C94.4297%20L422%2C104.4297%20L432%2C104.4297%20L422%2C94.4297%20%22%20fill%3D%22%23FEFFDD%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2252%22%20x%3D%22365%22%20y%3D%22111.4966%22%3E%26%2327492%3B%26%2322788%3B%26%2330465%3B%26%2330053%3B%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2252%22%20x%3D%22365%22%20y%3D%22126.6294%22%3E%26%2325569%3B%26%2325163%3B%26%2330830%3B%26%2335748%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C156.8281%2C352%2C160.8281%2C342%2C164.8281%2C346%2C160.8281%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22160.8281%22%20y2%3D%22160.8281%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2240%22%20y%3D%22155.7622%22%3E2%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22166%22%20x%3D%2253%22%20y%3D%22155.7622%22%3E%26%2325351%3B%26%2320196%3B%26%2312304%3BStartTranscription%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C185.9609%2C34%2C189.9609%2C44%2C193.9609%2C40%2C189.9609%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22189.9609%22%20y2%3D%22189.9609%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2250%22%20y%3D%22184.895%22%3E3%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22182%22%20x%3D%2263%22%20y%3D%22184.895%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BTranscriptionStarted%26%2312305%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%223%22%20style%3D%22stroke%3A%23EEEEEE%3Bstroke-width%3A1.0%3B%22%20width%3D%22455%22%20x%3D%220%22%20y%3D%22218.5273%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%22218.5273%22%20y2%3D%22218.5273%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%22221.5273%22%20y2%3D%22221.5273%22%2F%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%2223.1328%22%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A2.0%3B%22%20width%3D%22108%22%20x%3D%22173.5%22%20y%3D%22207.9609%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2289%22%20x%3D%22179.5%22%20y%3D%22224.0278%22%3E2.%20%26%2321457%3B%26%2336865%3B%26%2321644%3B%26%2335782%3B%26%2321035%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C258.2266%2C352%2C262.2266%2C342%2C266.2266%2C346%2C262.2266%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22262.2266%22%20y2%3D%22262.2266%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2240%22%20y%3D%22257.1606%22%3E4%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22275%22%20x%3D%2253%22%20y%3D%22257.1606%22%3E%26%2325351%3B%26%2320196%3B%26%2312304%3BProcessTranscription%26%2312305%3B%26%2365288%3B%26%2321253%3B%26%2321547%3B%26%2338899%3B%26%2339057%3B%26%2327969%3B%26%2365289%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C287.3594%2C34%2C291.3594%2C44%2C295.3594%2C40%2C291.3594%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22291.3594%22%20y2%3D%22291.3594%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2250%22%20y%3D%22286.2935%22%3E5%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22230%22%20x%3D%2263%22%20y%3D%22286.2935%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BTranscriptionResultChanged%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C316.4922%2C34%2C320.4922%2C44%2C324.4922%2C40%2C320.4922%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22320.4922%22%20y2%3D%22320.4922%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2250%22%20y%3D%22315.4263%22%3E6%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22140%22%20x%3D%2263%22%20y%3D%22315.4263%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BBizProcessing%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C345.625%2C34%2C349.625%2C44%2C353.625%2C40%2C349.625%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22349.625%22%20y2%3D%22349.625%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2250%22%20y%3D%22344.5591%22%3E7%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22137%22%20x%3D%2263%22%20y%3D%22344.5591%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BSentenceEnd%26%2312305%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%223%22%20style%3D%22stroke%3A%23EEEEEE%3Bstroke-width%3A1.0%3B%22%20width%3D%22455%22%20x%3D%220%22%20y%3D%22378.1914%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%22378.1914%22%20y2%3D%22378.1914%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%22381.1914%22%20y2%3D%22381.1914%22%2F%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%2223.1328%22%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A2.0%3B%22%20width%3D%22108%22%20x%3D%22173.5%22%20y%3D%22367.625%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2289%22%20x%3D%22179.5%22%20y%3D%22383.6919%22%3E3.%20%26%2321457%3B%26%2336865%3B%26%2321644%3B%26%2325171%3B%26%2326029%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C417.8906%2C352%2C421.8906%2C342%2C425.8906%2C346%2C421.8906%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22421.8906%22%20y2%3D%22421.8906%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2240%22%20y%3D%22416.8247%22%3E8%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22275%22%20x%3D%2253%22%20y%3D%22416.8247%22%3E%26%2325351%3B%26%2320196%3B%26%2312304%3BProcessTranscription%26%2312305%3B%26%2365288%3B%26%2321253%3B%26%2321547%3B%26%2338899%3B%26%2339057%3B%26%2327969%3B%26%2365289%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C447.0234%2C34%2C451.0234%2C44%2C455.0234%2C40%2C451.0234%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22451.0234%22%20y2%3D%22451.0234%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%229%22%20x%3D%2250%22%20y%3D%22445.9575%22%3E9%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22230%22%20x%3D%2263%22%20y%3D%22445.9575%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BTranscriptionResultChanged%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C476.1563%2C34%2C480.1563%2C44%2C484.1563%2C40%2C480.1563%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22480.1563%22%20y2%3D%22480.1563%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22475.0903%22%3E10%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22140%22%20x%3D%2272%22%20y%3D%22475.0903%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BBizProcessing%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C523.4219%2C34%2C527.4219%2C44%2C531.4219%2C40%2C527.4219%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22527.4219%22%20y2%3D%22527.4219%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22522.356%22%3E11%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22184%22%20x%3D%2272%22%20y%3D%22522.356%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BSentenceInterrupted%26%2312305%3B%3C%2Ftext%3E%3Cpath%20d%3D%22M359%2C493.1563%20L359%2C548.1563%20L432%2C548.1563%20L432%2C503.1563%20L422%2C493.1563%20L359%2C493.1563%20%22%20fill%3D%22%23FEFFDD%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%2F%3E%3Cpath%20d%3D%22M422%2C493.1563%20L422%2C503.1563%20L432%2C503.1563%20L422%2C493.1563%20%22%20fill%3D%22%23FEFFDD%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2252%22%20x%3D%22365%22%20y%3D%22510.2231%22%3E%26%2325171%3B%26%2326029%3B%26%2320449%3B%26%2321495%3B%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2252%22%20x%3D%22365%22%20y%3D%22525.356%22%3E%26%2338656%3B%26%2335201%3B%26%2328165%3B%26%2331354%3B%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2252%22%20x%3D%22365%22%20y%3D%22540.4888%22%3E%26%2338899%3B%26%2339057%3B%26%2332531%3B%26%2323384%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C570.6875%2C34%2C574.6875%2C44%2C578.6875%2C40%2C574.6875%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22574.6875%22%20y2%3D%22574.6875%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22569.6216%22%3E12%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22137%22%20x%3D%2272%22%20y%3D%22569.6216%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BSentenceEnd%26%2312305%3B%3C%2Ftext%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%223%22%20style%3D%22stroke%3A%23EEEEEE%3Bstroke-width%3A1.0%3B%22%20width%3D%22455%22%20x%3D%220%22%20y%3D%22603.2539%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%22603.2539%22%20y2%3D%22603.2539%22%2F%3E%3Cline%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A1.0%3B%22%20x1%3D%220%22%20x2%3D%22455%22%20y1%3D%22606.2539%22%20y2%3D%22606.2539%22%2F%3E%3Crect%20fill%3D%22%23EEEEEE%22%20height%3D%2223.1328%22%20style%3D%22stroke%3A%23000000%3Bstroke-width%3A2.0%3B%22%20width%3D%22108%22%20x%3D%22173.5%22%20y%3D%22592.6875%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2289%22%20x%3D%22179.5%22%20y%3D%22608.7544%22%3E4.%20%26%2320572%3B%26%2327490%3B%26%2321644%3B%26%2323436%3B%26%2325104%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C642.9531%2C352%2C646.9531%2C342%2C650.9531%2C346%2C646.9531%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22646.9531%22%20y2%3D%22646.9531%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2240%22%20y%3D%22641.8872%22%3E13%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22275%22%20x%3D%2262%22%20y%3D%22641.8872%22%3E%26%2325351%3B%26%2320196%3B%26%2312304%3BProcessTranscription%26%2312305%3B%26%2365288%3B%26%2321253%3B%26%2321547%3B%26%2338899%3B%26%2339057%3B%26%2327969%3B%26%2365289%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C672.0859%2C34%2C676.0859%2C44%2C680.0859%2C40%2C676.0859%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22676.0859%22%20y2%3D%22676.0859%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22671.02%22%3E14%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22230%22%20x%3D%2272%22%20y%3D%22671.02%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BTranscriptionResultChanged%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C701.2188%2C34%2C705.2188%2C44%2C709.2188%2C40%2C705.2188%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22705.2188%22%20y2%3D%22705.2188%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22700.1528%22%3E15%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22140%22%20x%3D%2272%22%20y%3D%22700.1528%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BBizProcessing%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C740.918%2C34%2C744.918%2C44%2C748.918%2C40%2C744.918%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22744.918%22%20y2%3D%22744.918%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22739.8521%22%3E16%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22158%22%20x%3D%2272%22%20y%3D%22739.8521%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BTranscriptionEnd%26%2312305%3B%3C%2Ftext%3E%3Cpath%20d%3D%22M359%2C718.2188%20L359%2C758.2188%20L445%2C758.2188%20L445%2C728.2188%20L435%2C718.2188%20L359%2C718.2188%20%22%20fill%3D%22%23FEFFDD%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%2F%3E%3Cpath%20d%3D%22M435%2C718.2188%20L435%2C728.2188%20L445%2C728.2188%20L435%2C718.2188%20%22%20fill%3D%22%23FEFFDD%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A0.5%3B%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2251%22%20x%3D%22365%22%20y%3D%22735.2856%22%3ELLM%26%2321028%3B%26%2326029%3B%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2265%22%20x%3D%22365%22%20y%3D%22750.4185%22%3E%26%2320250%3B%26%2335805%3B%26%2321487%3B%26%2325346%3B%26%2326029%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C780.6172%2C352%2C784.6172%2C342%2C788.6172%2C346%2C784.6172%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22784.6172%22%20y2%3D%22784.6172%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2240%22%20y%3D%22779.5513%22%3E17%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22164%22%20x%3D%2262%22%20y%3D%22779.5513%22%3E%26%2325351%3B%26%2320196%3B%26%2312304%3BStopTranscription%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%2244%2C809.75%2C34%2C813.75%2C44%2C817.75%2C40%2C813.75%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2238%22%20x2%3D%22353%22%20y1%3D%22813.75%22%20y2%3D%22813.75%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2250%22%20y%3D%22808.6841%22%3E18%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22204%22%20x%3D%2272%22%20y%3D%22808.6841%22%3E%26%2320107%3B%26%2320214%3B%26%2312304%3BTranscriptionCompleted%26%2312305%3B%3C%2Ftext%3E%3Cpolygon%20fill%3D%22%23181818%22%20points%3D%22342%2C838.8828%2C352%2C842.8828%2C342%2C846.8828%2C346%2C842.8828%22%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%2F%3E%3Cline%20style%3D%22stroke%3A%23181818%3Bstroke-width%3A1.0%3B%22%20x1%3D%2233%22%20x2%3D%22348%22%20y1%3D%22842.8828%22%20y2%3D%22842.8828%22%2F%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20font-weight%3D%22bold%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%2218%22%20x%3D%2240%22%20y%3D%22837.8169%22%3E19%3C%2Ftext%3E%3Ctext%20fill%3D%22%23000000%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20lengthAdjust%3D%22spacing%22%20textLength%3D%22131%22%20x%3D%2262%22%20y%3D%22837.8169%22%3E%26%2320851%3B%26%2338381%3B%20WebSocket%20%26%2336830%3B%26%2325509%3B%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

## [](#java-sdk-demo)Java Sdk Demo

请注意：当前示例为通用 SDK，后续会有 API 专属 SDK。

### [](#添加依赖)添加依赖

```yaml
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>aliyun-gateway-pop</artifactId>
    <version>${version}</version> 
</dependency>
```

版本号请联系点金开发人员获取

### [](#代码示例)代码示例

```java
String WORKSPACE_ID = "xxx";

//构造身份提供器， 匿名调用可使用 AnonymousCredentialProvider
StaticCredentialProvider provider = StaticCredentialProvider.create(
    Credential.builder()
    .accessKeyId("xxx")
    .accessKeySecret("xxx")
    .build()
);

//构造 WebSocket 客户端
CommonWebSocketClient client = CommonWebSocketClient.builder()
    .credentialsProvider(provider)
    .overrideConfiguration(
        ClientOverrideConfiguration.create()
        .setProtocol("wss")
        .setEndpointOverride("dianjin.cn-beijing.aliyuncs.com") //设置产品域名
    ).build();

//构造握手请求
CommonRequest commonRequest = CommonRequest.builder()
            .product("Dianjin")
            .version("2024-06-28")
            .action("EndToEndRealTimeDialog")
            .path(String.format("/%s/ws/realtime/dialog", WORKSPACE_ID))
            .putQueryParameters("asrModelId", "paraformer-realtime-v1")
            .putQueryParameters("ttsModelId", "cosyvoice-v2")
            .putQueryParameters("voiceCode", "longxiaochun_v2")
            .putQueryParameters("speechRate", 1)
            .putQueryParameters("pitchRate", 1)
            .build();

//通过 CommonWebSocketClient 构造适配 awap 协议的专用子协议客户端或适配 general 协议的客户端
//这里的 WebSocketClient 其实可以理解为一个会话，其内部保存了连接状态，可以手动重连，使用完毕后需要主动 close
WebSocketClient session = client.awapClient(commonRequest);
WebSocketClient session = client.generalClient(commonRequest);

// 添加事件监听器
session.addEventListener(WebSocketEvent.CONNECTION_OPENED, event -> {
    ConnectionOpenedEvent openedEvent = (ConnectionOpenedEvent)event;
    //连接建立时打印会话信息，其中的 sessionId 即为握手请求的 RequestId，可用于链路诊断
    System.out.println("Connection established: " + openedEvent.getSessionInfo());
});
session.addEventListener(WebSocketEvent.CONNECTION_CLOSED, event -> {
    ConnectionClosedEvent closedEvent = (ConnectionClosedEvent)event;
    System.out.println("Connection closed: " + closedEvent.getReason());
});
session.addEventListener(WebSocketEvent.CONNECTION_ERROR, event -> {
    ConnectionErrorEvent errorEvent = (ConnectionErrorEvent)event;
    System.err.println("Connection error: " + errorEvent.getError());
});
session.addEventListener(WebSocketEvent.MESSAGE_SENT, event -> {
    MessageSentEvent sentEvent = (MessageSentEvent)event;
    System.out.println("Message sent: " + sentEvent.getMessageId());
});

//接收消息的逻辑通过添加 MESSAGE_RECEIVED 事件监听来实现
session.addEventListener(WebSocketEvent.MESSAGE_RECEIVED, event -> {
    MessageReceivedEvent receiveEvent = (MessageReceivedEvent)event;
    IncomingMessage message = (IncomingMessage)receiveEvent.getMessage();
    //对于 awap 协议，可以获取消息的 header，general 协议没有 header
    Map<String, String> awapHeaders = message.getHeaders();
    String type = awapHeaders.get("type");  //业务侧定义的消息类型
    String timestamp = awapHeaders.get("timestamp");  //服务端消息生成的时间
    String id = awapHeaders.get("id");  //消息唯一 id，可为空
    System.out.println("Receive message, type: " + type + ", receiveTime: " + receiveEvent.getTimestamp());
    
    ByteBuffer data = message.getData();
    byte[] bytes = new byte[data.remaining()];
    data.get(bytes);
    if ("json".equals(message.getFormat())) {  //这里的 format 有 json 和 binary 两种
        //可以根据 type 将 payload 反序列化为对应的对象结构
        System.out.println("Receive text payload: " + new String(bytes, StandardCharsets.UTF_8));
    } else {
        System.out.println("Receive binary payload，length: " + bytes.length);
    }
});

//发起握手，这里为了方便，直接用 CompletableFuture.join()同步等待响应
HandshakeResult result = session.connect().join();
if (!result.isSuccess()) {
    throw new RuntimeException("Connect fail", result.getError());
}

//发送文本消息
SendOptions sendOptions = SendOptions.builder()
    .format("string")	//文本消息 format=string
    .header("type", "StartTranscription")  //awap 协议的消息需要通过 header()方法设置消息类型，general 协议不需要
    .build();

String json = "{\"playCode\":\"xxx\", \"selfDirected\":true}";
SendResult sendResult = session.send(json, sendOptions).join();
if (sendResult.isSuccess()) {
    System.out.println("text message sent: " + sendResult.getMessageId());
} else {
    throw new RuntimeException("send message error", sendResult.getError());
}
```

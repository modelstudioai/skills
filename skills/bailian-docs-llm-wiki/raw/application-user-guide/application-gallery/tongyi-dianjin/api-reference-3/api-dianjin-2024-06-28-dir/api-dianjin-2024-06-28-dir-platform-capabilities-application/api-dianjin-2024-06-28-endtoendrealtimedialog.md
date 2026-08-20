# EndToEndRealTimeDialog - 语音实时对话

本接口通过 WebSocket 协议实现实时语音对话转写、意图识别、话术语音合成返回等功能，支持多种音频格式的输入输出，满足实时性与高兼容性需求。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.alibabacloud.com/api/DianJin/2024-06-28/EndToEndRealTimeDialog)

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

## 客户端请求消息

## 通用字段说明

字段名

说明

type

消息类型

seq

消息序列号

timestamp

毫秒时间戳

## StartTranscription （开始实时转录）

### 作用：开始实时转录，并创建实时会话。

```
type:StartTranscription
seq:1
timestamp:1719242591197

{
    "playCode": "c00aa8467a",   // 场景编码
    "metaData": {},   // 元数据，此处可添加一些 k-v 对，用于开场白占位等。如在场景管理中的开场白中设置了占位符${name}，此处可传入{"name": "张三"}。
    "selfDirected": true   // 是否开启自主问答（当意图识别为其它时，会使用模型自主回答的能力）
}
```

## ProcessTranscription（发送音频数据）

### 作用：上传一段音频数据

```
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

## StopTranscription（停止转录）

### 作用：主动结束实时会话

```
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

## 服务端返回（推送）消息

## TranscriptionStarted（会话/转录已开始）

```
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

## TranscriptionResultChanged（转写文本变化「ASR 结果」）

```
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

## SentenceEnd（一句话转写完成「流式返回客服回复的音频数据」）

```
type:SentenceEnd
seq: 3
timestamp: 1754659629166

{
  "data": [73,68,51,4,0,0,0],    // 语音的二进制数据
  "messageId": "",    // 消息唯一标识
  "messageEnd": true   // 本轮消息结束标识
}
```

## BizProcessing（业务意图识别结果）

```
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

-   主要输出意图识别相关文本内容，输出字段描述请参考 API: RealTimeDialog

## SentenceInterrupted（句子中断「需清理音频缓存」）

```
type:SentenceInterrupted
seq: 32
timestamp: 1754659635543

{}
```

-   body 内容为空 收到此消息需清空音频缓存、终止播放之前的音频内容，以实现打断效果。

## TranscriptionEnd（转录结束「会话建议结束：智能体判断会话可结束」）

```
type:TranscriptionEnd
seq: 367
timestamp: 1754659669964

{}
```

## TranscriptionCompleted（转写完全结束，可主动断开 WebSocket 连接）

```
type:TranscriptionCompleted
seq:3
timestamp:1752922030325

{}
```

## 状态码与错误处理

若连接/发送消息出错，服务端返回标准格式 Error 消息：

```
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

访问[错误中心](https://api.alibabacloud.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-10-28

新增 OpenAPI

[查看变更详情](https://api.alibabacloud.com/document/DianJin/2024-06-28/EndToEndRealTimeDialog?updateTime=2025-10-28#workbench-doc-change-demo)

## 交互流程

## Java Sdk Demo

请注意：当前示例为通用 SDK，后续会有 API 专属 SDK。

### 添加依赖

```
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>aliyun-gateway-pop</artifactId>
    <version>${version}</version>
</dependency>
```

版本号请联系点金开发人员获取

### 代码示例

```
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

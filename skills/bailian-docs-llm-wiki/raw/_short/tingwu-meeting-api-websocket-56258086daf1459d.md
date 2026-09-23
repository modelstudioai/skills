# 会议纪要实时音频转写交互协议（WebSocket）

本文介绍通过WebSocket进行会议纪要实时转写的方法。

本文介绍会议纪要实时转写WebSocket API。WebSocket协议延迟低、资源占用少，是首选接入方案。

WebSocket是一种支持全双工通信的网络协议。客户端和服务器通过一次握手建立持久连接，双方可以互相主动推送数据，因此在实时性和效率方面具有显著优势。

建议您先了解WebSocket的基本原理和技术细节，再参照本文进行开发。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

## 整体调用流程

请参考[实时会议](raw/_short/tingwu-meeting-api-usage-bc4c1ca718d0e73c.md)。

## 调用时序图

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8885290671/p1009193.png)

您必须遵循时序图中所展示的时序进行调用，否则会有运行失败的风险。

## WebSocket建联

对应时序图中过程1。

对于常用编程语言，有许多现成的WebSocket库和示例可供参考，例如：

-   Go：`gorilla/websocket`
-   PHP：`Ratchet`
-   Node.js：`ws`

### 建联请求头

```
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Upgrade: websocket
Connection: Upgrade
```

### WebSocket接入地址

```
wss://dashscope.aliyuncs.com/api-ws/v1/inference
```

## 向服务端发送指令

您可以向服务端发送指令，控制转写的开始和停止。

指令分为两种，run-task和finish-task，都需要以Text Frame方式发送的JSON格式的数据，具体协议如下：

### run-task指令

对应时序图中过程2，通知服务端开始一个转写任务。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.action

String

固定填写run-task。

header.task\_id

String

自定义16位随机字符串，排查问题使用，后续finish-task也应该使用这个task\_id。

header.streaming

String

固定填写duplex。

payload

Object

payload.model

String

固定填写tingwu-meeting-realtime。

payload.task\_group

String

固定填写aigc。

payload.task

String

固定填写multimodal-generation。

payload.function

String

固定填写generation。

payload.input

Object

payload.input.appId

String

填写会议纪要控制台中发布的应用id，可从控制台获取。

payload.input.directive

String

固定传start。

payload.input.dataId

String

请填写CreateTask中获取的dataId

run-task指令示例如下：

```
{
  "header": {
    "action": "run-task",
    "task_id": "f2E3zvK*******wp",
    "streaming": "duplex"
  },
  "payload": {
    "model": "tingwu-meeting-realtime",
    "task_group": "aigc",
    "task": "multimodal-generation",
    "function": "generation",
    "input": {
      "appId": "tw_YrN*******Cw",
      "dataId": "uTx*******bN",
      "directive": "start"
    }
  }
}
```

### finish-task

对应时序图中过程6，通知服务端音频已全部发送完成。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.action

String

固定填写finish-task。

header.task\_id

String

请填写run-task指令中填写的task\_id。

header.streaming

String

固定填写duplex。

payload

Object

payload.model

String

固定填写tingwu-meeting-realtime。

payload.task\_group

String

固定填写aigc。

payload.task

String

固定填写multimodal-generation。

payload.function

String

固定填写generation。

payload.input

Object

payload.input.directive

String

固定传stop。

finish-task指令示例如下：

```
{
  "header": {
    "action": "finish-task",
    "task_id": "f2E3zvK*******wp",
    "streaming": "duplex"
  },
  "payload": {
    "model": "tingwu-meeting-realtime",
    "task_group": "aigc",
    "task": "multimodal-generation",
    "function": "generation",
    "input": {
      "directive": "stop"
    }
  }
}
```

## 向服务端发送音频

将原始音频直接转为二进制流即可，无需额外处理。但需要注意：

-   上传的语音识别音频采样率必须是8000Hz或16000Hz，且与调用CreateTask时传入参数一致。
-   音频编码格式需要与调用CreateTask时传入参数一致。
-   支持的音频格式：pcm、opus、aac、speex、mp3。

## 接收服务端返回的事件

在指令或音频发送后，服务端会向您发送不同种类的事件，每个事件代表不同的处理阶段，请严格遵循时序图对不同事件做相应处理。

事件总共分为五种，分别是speech-listen事件、recognize-result事件、心跳事件、speech-end事件及task-failed事件。

### speech-listen事件

对应时序图中的过程3，speech-listen事件会在run-task指令后返回，代表服务端收到了您的转写指令，并完成相关初始化工作，您可以开始发送音频了。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.event

String

固定为result-generated。

header.task\_id

String

您在run-task指令中填写的task\_id。

payload

Object

payload.output

Object

payload.output.action

String

固定为speech-listen。

payload.output.dataId

String

您传入的dataId

speech-listen事件的示例如下：

```
{
  "header": {
    "event": "result-generated",
    "task_id": "f2E3zvK*******wp"
  },
  "payload": {
    "output": {
      "action": "speech-listen",
      "dataId": "Adb*******uY"
    }
  }
}
```

### recognize-result事件

对应时序图中的过程4，recognize-result事件会在您发送一段时间的音频后返回，也可能会在您发送finish-task指令后返回，代表当前服务端识别到的原文和译文结果。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.event

String

固定为result-generated。

header.task\_id

String

您在run-task指令中填写的task\_id。

payload

Object

payload.output

Object

payload.output.action

String

固定为recognize-result。

payload.output.transcription

Object

转写的原始结果。

payload.output.transcription.sentenceId

Integer

句子序号。

payload.output.transcription.time

Integer

当前已处理的音频时长。

payload.output.transcription.text

String

识别文本。

payload.output.transcription.words

Array\[Word\]

字时间戳信息。

payload.output.transcription.sentenceEnd

Boolean

true：当前文本已构成一句完整句子。

false：当前文本未构成完整句子，识别结果可能会更新。

payload.output.transcription.stashResult

Object

语音识别的暂存结果，是暂未完成断句的下一句话信息。您可以将stashResult结果和上面的text结果拼接以便后续处理

payload.output.transcription.stashResult.sentenceId

Integer

下一句话的句子ID

payload.output.transcription.stashResult.text

String

stash结果的ASR文本

payload.output.transcription.stashResult.words

Array\[Word\]

stash结果的词信息

payload.output.translations

Object

翻译结果

payload.output.translations\[targetLang\].sourceLang

String

原始语种

payload.output.translations\[targetLang\].targetLang

String

目标语种

payload.output.translations\[targetLang\].translateResult

Array\[Object\]

翻译句子结果

payload.output.translations\[targetLang\].translateResult\[i\].sentenceId

Integer

翻译句子编号，从0开始递增。

payload.output.translations\[targetLang\].translateResult\[i\].text

String

句子翻译结果

payload.output.translations\[targetLang\].translateResult\[i\].beginTime

Integer

翻译句子的开始时间，单位为毫秒，在翻译SentenceEnd识别结果时会返回。

payload.output.translations\[targetLang\].translateResult\[i\].endTime

Integer

翻译句子的结束时间，单位为毫秒，在翻译SentenceEnd识别结果时会返回。

payload.output.translations\[targetLang\].translateResult\[i\].partial

Boolean

为true时对应stash部分识别内容的翻译结果。

Word类型协议如下：

**字段**

**类型**

**说明**

beginTime

Integer

当前词在音频中的开始时间。

endTime

Integer

当前词在音频中的结束时间。

text

String

当前词的内容。

注意一次结果只会下发识别结果或翻译结果，不会同时包含识别结果和翻译结果。

recognize-result事件的示例如下：

##### 识别到句子开始

```
{
  "header": {
    "event":"result-generated",
    "task_id": "f2E3zvK*******w"
  },
  "payload": {
    "output": {
      "action": "recognize-result",
      "transcription": {
        "sentenceId": 1,
        "time": 10000
      }
    }
  }
}
```

##### 识别到句子中

```
{
  "header": {
    "event":"result-generated",
    "task_id": "f2E3zvK*******w"
  },
  "payload": {
    "output": {
      "action": "recognize-result",
      "transcription": {
        "sentenceId": 0,
        "sentenceEnd": false,
        "time": 2065,
        "text": "这是一句用来测试的",
        "words": [
          {
            "beginTime": 100,
            "endTime": 427,
            "text": "这"
          },
          {
            "beginTime": 427,
            "endTime": 755,
            "text": "是一"
          },
          {
            "beginTime": 755,
            "endTime": 1082,
            "text": "句"
          },
          {
            "beginTime": 1082,
            "endTime": 1410,
            "text": "用来"
          },
          {
            "beginTime": 1410,
            "endTime": 1737,
            "text": "测试"
          },
          {
            "beginTime": 1737,
            "endTime": 2065,
            "text": "的"
          }
        ]
      }
    }
  }
}
```

##### 识别到句子结束

```
{
  "header": {
    "event":"result-generated",
    "task_id": "f2E3zvK*******w"
  },
  "payload": {
    "output": {
      "action": "recognize-result",
      "transcription": {
        "sentenceId": 0,
        "time": 2720,
        "sentenceEnd": true,
        "text": "这是一句用来测试的文本。",
        "words": [
          {
            "beginTime": 100,
            "endTime": 427,
            "text": "这"
          },
          {
            "beginTime": 427,
            "endTime": 755,
            "text": "是一"
          },
          {
            "beginTime": 755,
            "endTime": 1082,
            "text": "句"
          },
          {
            "beginTime": 1082,
            "endTime": 1410,
            "text": "用来"
          },
          {
            "beginTime": 1410,
            "endTime": 1737,
            "text": "测试"
          },
          {
            "beginTime": 1737,
            "endTime": 2065,
            "text": "的"
          },
          {
            "beginTime": 2065,
            "endTime": 2392,
            "text": "文本"
          },
          {
            "beginTime": 2392,
            "endTime": 2720,
            "text": "。"
          }
        ],
        "stashResult": {
          "sentenceId": 1,
          "words": [
            {
              "beginTime": 2920,
              "text": "会",
              "endTime": 3030
            },
            {
              "beginTime": 3030,
              "text": "下雨",
              "endTime": 3230
            }
          ],
          "text": "会下雨"
        }
      }
    }
  }
}
```

##### 翻译结果

```
{
  "header": {
    "event":"result-generated",
    "task_id": "f2E3zvK*******w"
  },
  "payload": {
    "output": {
      "action": "recognize-result",
      "translations": {
        "en": {
          "sourceLang":"cn",
          "targetLang":"en",
          "translateResult":[
            {
              "text":"At that time.",
              "sentenceId":110,
              "beginTime":123000,
              "endTime":125000
            },
            {
              "text":"I am",
              "sentenceId":111,
              "partial":true
            }
          ]
        }
      }
    }
  }
}
```

### 心跳事件

对应时序图中的过程5。在长时间发送静音音频时，为保证下行链路不中断，服务端会发送心跳保活事件，心跳保活事件会在最后一次下发事件后30s后发送，服务端无需对心跳事件进行回复。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.event

String

固定为result-generated。

header.task\_id

String

您在run-task指令中填写的task\_id。

payload

Object

payload.output

Object

payload.output.action

String

固定为ping。

心跳事件的示例如下：

```
{
  "header": {
    "event": "result-generated",
    "task_id": "f2E3zvK*******wp"
  },
  "payload": {
    "output": {
      "action": "ping"
    }
  }
}
```

### speech-end事件

对应时序图中的过程7。speech-end事件代表本次实时转写的结果已全部发送完毕，之后您可以关闭WebSocket连接。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.event

String

固定为result-generated。

header.task\_id

String

您在run-task指令中填写的task\_id。

payload

Object

payload.output

Object

payload.output.action

String

固定为speech-end。

speech-end事件的示例如下：

```
{
  "header": {
    "event": "result-generated",
    "task_id": "f2E3zvK*******wp"
  },
  "payload": {
    "output": {
      "action": "speech-end"
    }
  }
}
```

### task-failed事件

若在任务过程中，由于客户端传参错误或服务端内部错误导致任务失败，服务端会返回给您task-failed事件，随即会中断WebSocket连接。

协议字段如下：

**字段**

**类型**

**说明**

header

Object

header.event

String

固定为result-generated。

header.task\_id

String

您在run-task指令中填写的task\_id。

payload

Object

payload.output

Object

payload.output.action

String

固定为task-failed。

payload.output.errorCode

String

错误码

payload.output.errorMessage

String

错误信息

task-failed事件的示例如下：

```
{
  "header": {
    "event": "result-generated",
    "task_id": "f2E3zvK*******wp"
  },
  "payload": {
    "output": {
      "action": "task-failed",
      "errorCode": "Agent.FrameSequenceIllegal",
      "errorMessage": "Agent Websocket Frame Sequence Illegal."
    }
  }
}
```

具体错误码及其含义，可以参考[错误码](raw/_short/tingwu-industrial-instruction-api-websocket-08c1283fedfe256b.md)。

## 会议暂停及恢复

WebSocket生命周期内，您可以随时通过发送finish-task指令暂停会议。

若客户端10s内无文本指令或二进制语音流发送，连接将自动断开。

单个会议dataId的有效期是24h，在此期间，您可以随时重新通过建立WebSocket并传入会议dataId恢复指定的会议。

## 代码示例

java

```
package nls.alibaba;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.codec.binary.Hex;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.security.SecureRandom;
import java.util.HashMap;
import java.util.Map;

import static java.lang.Thread.sleep;

public class TingWuMeetingApiUsage extends WebSocketClient {

  private final byte[] audioData;

  private final String taskId;

  private final ObjectMapper objectMapper = new ObjectMapper();

  private boolean audioSent = false;

  private static final int CHUNK_SIZE = 3200;

  private static final long SEND_INTERVAL_MS = 100; // 模拟流式发送间隔

  private static final String apiKey = "替换为您的api-key";

  public TingWuMeetingApiUsage(URI serverUri, String audioFilePath) throws IOException {
    super(serverUri, createHeaders());
    this.audioData = Files.readAllBytes(new File(audioFilePath).toPath());

    // 生成随机16位字符串
    SecureRandom random = new SecureRandom();
    byte[] taskIdBytes = new byte[8];
    random.nextBytes(taskIdBytes);
    this.taskId = Hex.encodeHexString(taskIdBytes);
  }

  private static Map<String, String> createHeaders() {
    Map<String, String> headers = new HashMap<>();
    headers.put("Authorization", "Bearer " + apiKey);
    headers.put("Upgrade", "websocket");
    headers.put("Connection", "Upgrade");
    return headers;
  }

  @Override
  public void onOpen(ServerHandshake serverHandshake) {
    System.out.println("WebSocket connected.");
    System.out.println("Task ID: " + taskId);

    // 构造 run-task 消息
    String runTaskMessage = "{\n" +
      "  \"header\": {\n" +
      "    \"action\": \"run-task\",\n" +
      "    \"task_id\": \"" + taskId + "\",\n" +
      "    \"streaming\": \"duplex\"\n" +
      "  },\n" +
      "  \"payload\": {\n" +
      "    \"model\": \"tingwu-meeting-realtime\",\n" +
      "    \"task_group\": \"aigc\",\n" +
      "    \"task\": \"multimodal-generation\",\n" +
      "    \"function\": \"generation\",\n" +
      "    \"input\": {\n" +
      "      \"appId\": \"替换为您的应用Id\",\n" +
      "      \"dataId\": \"替换为CreateTask中获取的dataId\",\n" +
      "      \"directive\": \"start\"\n" +
      "    }\n" +
      "  }\n" +
      "}";

    System.out.println("Sending run-task: " + runTaskMessage);
    send(runTaskMessage);
  }

  @Override
  public void onMessage(String message) {
    System.out.println("Received text message: " + message);

    try {
      JsonNode root = objectMapper.readTree(message);

            JsonNode header = root.get("header");
            JsonNode payload = root.get("payload");

            if (header != null) {
                String event = header.path("event").asText("");
                // 可以忽略此消息
                if ("task-started".equals(event)) {
                    return;
                }

                String action = payload.path("output").path("action").asText("");
                switch (action) {
                    case "speech-listen":
                        System.out.println("Received speech-listen event, sending full audio...");
                        sendAudioFile();
                        break;
                    case "task-failed":
                        String errorCode = payload.path("output").path("errorCode").asText("N/A");
                        String errorMsg = payload.path("output").path("errorMessage").asText("N/A");
                        System.out.println("Task failed: " + errorCode + " - " + errorMsg);
                        close();
                        break;
                    case "recognize-result":
                        JsonNode output = payload.get("output");
                        System.out.println("Recognition result: " + (output != null ? output.toString() : "N/A"));
                        break;
                    case "ping":
                        // 保活，可忽略
                        System.out.println("Received Ping action, do nothing...");
                        break;
                    case "speech-end":
                        System.out.println("Speech ended. Closing...");
                        close();
                        break;
                    default:
                        System.out.println("Unknown message received: " + message);
                        break;
                }
            } else {
                System.out.println("Unknown message format (no header): " + message);
            }

        } catch (JsonProcessingException e) {
            System.err.println("Invalid JSON received: " + e.getMessage());
            System.out.println("Raw message: " + message);
        }
    }

    @Override
    public void onClose(int code, String reason, boolean b) {
        System.out.println("WebSocket closed. Code: " + code + ", Reason: " + reason);
    }

    @Override
    public void onError(Exception ex) {
        System.err.println("WebSocket error: " + ex.getMessage());
        ex.printStackTrace();
    }

    private void sendAudioFile() {
        if (audioSent) {
            System.out.println("Audio already sent, skipping...");
            return;
        }
        audioSent = true;

        int offset = 0;
        while (offset < audioData.length) {
            int len = Math.min(CHUNK_SIZE, audioData.length - offset);
            byte[] chunk = new byte[len];
            System.arraycopy(audioData, offset, chunk, 0, len);
            try {
                send(chunk);
                offset += len;
                System.out.println("Sent chunk: " + offset + "/" + audioData.length);
                sleep(SEND_INTERVAL_MS);
            } catch (Exception e) {
                System.err.println("Send failed at offset " + offset);
                e.printStackTrace();
                close();
                return;
            }
        }
        System.out.println("Audio sent completely.");
        sendFinishTask();

    }

    // 发送 finish-task 消息
    private void sendFinishTask() {
        String finishTaskMessage = "{\n" +
                "  \"header\": {\n" +
                "    \"action\": \"finish-task\",\n" +
                "    \"task_id\": \"" + taskId + "\",\n" +
                "    \"streaming\": \"duplex\"\n" +
                "  },\n" +
                "  \"payload\": {\n" +
                "    \"model\": \"tingwu-meeting-realtime\",\n" +
                "    \"task_group\": \"aigc\",\n" +
                "    \"task\": \"multimodal-generation\",\n" +
                "    \"function\": \"generation\",\n" +
                "    \"input\": {\n" +
                "      \"directive\": \"stop\"\n" +
                "    }\n" +
                "  }\n" +
                "}";

        System.out.println("Sending finish-task: " + finishTaskMessage);
        send(finishTaskMessage);
    }

    public static void main(String[] args) {
        try {
            URI wsUri = new URI("wss://dashscope.aliyuncs.com/api-ws/v1/inference");
            String audioPath = "替换为您的音频路径";
            TingWuMeetingApiUsage client = new TingWuMeetingApiUsage(wsUri, audioPath);
            client.connect();
        } catch (Exception e) {
            System.err.println("Initialization error: " + e.getMessage());
            e.printStackTrace();
        }
    }

}
```

javascript

```
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const wsUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
const audioFilePath = path.resolve('请替换为你自己的音频文件路径');

// 创建WebSocket连接
console.log('开始连接WebSocket...');
const ws = new WebSocket(wsUrl, {
  headers: {
    'Authorization': 'Bearer ' + '请替换为您的api-key',
    'Upgrade': 'websocket',
    'Connection': 'Upgrade'
  }
});

// 生成随机16位taskId
ws.taskId = crypto.randomBytes(8).toString('hex');

ws.on('open', () => {
  console.log('WebSocket connected.' );
  console.log(ws.taskId);

  // 构造run-task消息
  const runTaskMessage = {
    header: {
      action: 'run-task',
      task_id: ws.taskId,
      streaming: 'duplex'
    },
    payload: {
      model: 'tingwu-meeting-realtime',
      task_group: 'aigc',
      task: "multimodal-generation",
      function: "generation",
      input: {
        appId: '请替换为您的应用Id',
        dataId: '替换为CreateTask中获取的dataId',
        directive: 'start'
      }
    }
  };

  console.log('发送run-task指令:', runTaskMessage);
  ws.send(JSON.stringify(runTaskMessage), { binary: false }, (err) => {
    if (err) {
      console.error('发送 run-task 失败:', err);
      return;
    }
    console.log(`任务ID ${ws.taskId}：已发送 run-task 指令`);
  });
});

// 处理服务端消息
ws.on('message', (data) => {
  let message;
  try {
    message = JSON.parse(data.toString());
  } catch (e) {
    console.warn('无法解析非JSON消息:', data);
    return;
  }
  console.log('解析后的 message:', message);

  // 处理不同事件
  let action;

  if (message.payload && message.payload.output && message.payload.output.action) {
    action = message.payload.output.action;
  }
  switch(action) {
    case 'speech-listen':
      console.log('收到 speech-listen 事件，开始发送音频数据, id:', message.payload.output.dataId);
      sendAudioFile(ws, audioFilePath);
      break;

    case 'recognize-result':
      console.log('识别结果:', message.payload.output);
      break;

    case 'ping':
      console.log('收到 ping 事件，无需处理');
      break;

    case 'speech-end':
      console.log('收到 speech-end 事件，关闭连接');
      ws.close();
      break;

    case 'task-failed':
      console.log('收到 task-failed 事件，错误为' + message.payload.output.errorCode + ' ' +
                  message.payload.output.errorMessage + '关闭连接');
      ws.close();
      break;

    default:
      console.log('收到未知事件:', message);
  }
});

let once = false;

// 发送音频文件
function sendAudioFile(socket, filePath) {
  if (once) {
    console.log('已经发送过音频文件，跳过');
    return;
  }
  once = true;

  const CHUNK_SIZE = 3200;
  let buffer;

  try {
    buffer = fs.readFileSync(filePath);
  } catch (err) {
    console.error(`读取音频文件失败: ${filePath}`, err);
    return;
  }

  let offset = 0;

  function sendChunk() {
    if (offset >= buffer.length) {
      console.log('音频文件发送完成，发送 finish-task');
      sendFinishTask(socket);
      return;
    }

    const end = Math.min(offset + CHUNK_SIZE, buffer.length);
        const chunk = buffer.slice(offset, end);

        socket.send(chunk, { binary: true }, (err) => {
            if (err) {
                console.error('发送音频数据失败:', err);
                return;
            }

            offset = end;
            console.log("sending chunk: ", offset)
            // 控制发送间隔（模拟流式传输）
            setTimeout(sendChunk, 100);
        });
    }

    sendChunk();
}

// 发送finish-task指令
function sendFinishTask(socket) {
    const finishTaskMessage = JSON.stringify({
        header: {
            action: 'finish-task',
            task_id: ws.taskId,
            streaming: 'duplex'
        },
        payload: {
            model: 'tingwu-meeting-realtime',
            task_group: 'aigc',
            task: "multimodal-generation",
            function: "generation",
            input: {
                directive: 'stop'
            },
        }
    });

    socket.send(finishTaskMessage, { binary: false }, (err) => {
        if (err) {
            console.error('发送 finish-task 失败:', err);
            return;
        }
        console.log('已发送 finish-task 指令');
    });
}

// 错误处理
ws.on('error', (err) => {
    console.error('WebSocket 错误:', err);
});

// 关闭连接处理
ws.on('close', () => {
    console.log('WebSocket 连接已关闭');
});
```

## 错误码

**错误码**

**错误信息**

**说明**

InvalidParameter

Invalid parameter. Please refer to the official documents.

参数错误，请检查您传入的参数。

Agent.FrameSequenceIllegal

Agent Websocket Frame Sequence Illegal.

调用指令时序不合法。

Agent.InputActionIllegal

Agent Input Action Illegal.

传入的指令action字段不合法。

Agent.InputAppIdIllegal

Agent Input appId illegal.

传入的应用Id字段不合法。

Agent.AppNotPublished

Agent App not published.

传入的应用Id尚未发布。

Agent.InputInvalidDataId

Agent Input invalid dataId.

传入的dataId不合法。

Agent.CustomTaskIdInvalid

The length of custom task id must be 16.

传入的taskId字段长度不合法，必须是16位字符串。

BIL.ServiceNotActivate

User hasn't activate service.

您尚未开通通义听悟Agent服务。

BIL.UserArrears

User is in arrears.

您目前处在欠费状态。

Agent.AppInfoNotExist

Agent App Info not exist.

传入的应用Id信息不存在，请先在控制台保存并发布应用配置信息。

ServerError

Server error.

服务端内部错误。

若错误码不在上述错误列表中，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

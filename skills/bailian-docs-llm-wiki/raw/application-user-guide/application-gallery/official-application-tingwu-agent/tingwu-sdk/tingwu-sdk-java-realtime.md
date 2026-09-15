# tingwu-sdk-java-realtime

本文介绍通义听悟 Java SDK的实时接口，帮助开发者快速调用通义听悟的实时服务。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)(版本号>=2.21.7)

## 接口说明

### TingWuRealtimeParam.java

参数配置类。以[工业生产指令转写交互协议（WebSocket）](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-industrial-instruction/tingwu-industrial-instruction-api/tingwu-industrial-instruction-api-websocket.md)为例，创建任务主要参数如下：

**名称**

**类型**

**必填**

**描述**

appId

string

是

应用id

sampleRate

int

否

音频采样率，只支持16000Hz。

format

string

是

设置待识别音频格式。支持的音频格式：pcm、wav、mp3、opus、speex、aac、amr。对于opus和speex格式的音频，需要ogg封装；对于wav格式的音频，需要pcm编码。

maxEndSilence

int

否

非必传，最大静音时长，单位ms，检测到超过此时长则会认为一句话结束，转写完成

terminology

string

否

纠正指令集id

#### 示例代码

```
TingWuRealtimeParam tingWuRealtimeParam = TingWuRealtimeParam.builder()
    .model("tingwu-industrial-instruction")
    .format("pcm")
    .sampleRate(16000)
    .terminology("terminology")
    .appId("your-app-id")
    .apiKey("your-api-key")
    .build();
```

### TingWuRealtime.java

-   听悟实时客户端接口

```
/**
   * tingwu real-time SDK.
   *
   * @param baseUrl Base URL
   */
public TingWuRealtime(String baseUrl)

**
   * Start tingwu real-time via sendAudioFrame API. The correct order of
   * calls is: first call, then repeatedly sendAudioFrame, and finally stop.
   *
   * @param param Configuration for tinwu real-time, including audio format,
   *     source language, target languages, etc.
   * @param TingWuRealtimeCallback ResultCallback
   */
public void call(
      TingWuRealtimeParam param, TingWuRealtimeCallback callback)

/**
   * Send one frame audio
   *
   * @param audioFrame One frame of binary audio The correct order of calls is: first call, then
   *     repeatedly sendAudioFrame, and finally stop.
   */
public void sendAudioFrame(ByteBuffer audioFrame)

/**
   * Stop tingwu real-time call session
   */
public void stop()
```

### TingWuRealtimeCallback

-   通过回调返回服务端事件和结果。

```
/**
 * Abstract class representing callbacks for multi-modal conversation events.
 *
 * author songsong.shao
 * date 2025/4/27
 */
public abstract class TingWuRealtimeCallback {

  /**
   * Called when a conversation starts with a specific dialog ID.
   */
  public abstract void onStarted(String taskId);

  /**
   * Called when a conversation stops with a specific dialog ID.
   */
  public abstract void onStopped(String taskId);

  /**
   * Called when an error occurs during a conversation.
   *
   * param errorCode The error code associated with the error.
   * param errorMsg The error message associated with the error.
   */
  public abstract void onError(String errorCode, String errorMsg);

  /**
   * Called when responding content is available in a specific dialog.
   *
   * param taskId The unique identifier for the dialog.
   * param content The content of the response as a JsonObject.
   */
  public abstract void onAiResult(String taskId, JsonObject content);

  /**
   * Called when speech content is available in a specific dialog.
   *
   * param taskId The unique identifier for the dialog.
   * param content The content of the speech as a JsonObject.
   */
  public abstract void onRecognizeResult(String taskId, JsonObject content);

  /**
   * Called when a request is accepted in a specific dialog.
   *
   * param taskId The unique identifier for the dialog.
   * param dataId for this task
   */
  public abstract void onSpeechListen(String taskId, String dataId);

  /** Called when the conversation closes. */
  public abstract void onClosed();
}
```

## 调用时序

通过听悟实时接口调用的时序如下，在建立连接之后，收到 SpeechListen 事件即可发送流式语音数据，服务端返回流式识别和纠错结果。

![截屏2025-09-05 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1394297571/p1004662.png)

## 响应结果说明

以[工业生产指令转写交互协议（WebSocket）](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-industrial-instruction/tingwu-industrial-instruction-api/tingwu-industrial-instruction-api-websocket.md)为例，在指令或音频发送后，服务端会向您发送不同种类的事件，每个事件代表不同的处理阶段，请严格遵循时序图对不同事件做相应处理。

事件总共分为四种，分别是speech-listen事件、recognize-result事件、ai-result事件及speech-end事件。

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

您本次转写的任务id，您可以通过该id向我们反馈问题，同时在账单中也可以通过该id查看对应任务的计费项。

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

payload.output.transcription.beginTime

Integer

当前句子已识别部分的第一个字在音频中的开始时间，单位ms。

payload.output.transcription.endTime

Integer

当前句子已识别部分的最后一个字在音频中的结束时间，单位ms。

payload.output.transcription.sentenceEnd

Boolean

当前句子是否已结束。

payload.output.transcription.text

String

当前句子已识别部分的内容。

payload.output.transcription.words

List\[Word\]

句子分词信息。

payload.output.translations

Object

转写的翻译结果。

payload.output.translations.sentenceEnd

Boolean

当前句子是否结束。

payload.output.translations.translations

Object

转写的翻译目标语种结果集合。

payload.output.translations.translations.zh

Object

目前只支持翻译成中文，所以只会有zh一个对象。

payload.output.translations.translations.zh.lang

String

固定为zh。

payload.output.translations.translations.zh.sentenceId

Integer

句子序号。

payload.output.translations.translations.zh.beginTime

Integer

当前句子已翻译部分的第一个字在音频中的开始时间，单位ms。

payload.output.translations.translations.zh.endTime

Integer

当前句子已翻译部分的最后一个字在音频中的结束时间，单位ms。

payload.output.translations.translations.zh.sentenceEnd

Boolean

当前句子是否已结束。

payload.output.translations.translations.zh.text

String

当前句子已翻译部分的内容。

payload.output.translations.translations.zh.words

List\[Word\]

已翻译句子分词信息。

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

recognize-result事件的示例如下：

```
{
  "header": {
    "event":"result-generated",
    "task_id": "f2E3zvK*******wp"
  },
  "payload": {
    "output": {
      "action": "recognize-result",
      "transcription": {
        "sentenceId": 0,
        "beginTime": 100,
        "endTime": 2720,
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
        ]
      },
      "translations": {
        "sentenceEnd": true,
        "translations": {
          "zh": {
            "sentenceId": 0,
            "beginTime": 100,
            "endTime": 2720,
            "text": "这是一句用来测试的文本。",
            "lang": "zh",
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
            "sentenceEnd": true
          }
        }
      }
    }
  }
}
```

### ai-result事件

对应时序图中的过程6。ai-result事件会在最后一条recognize-result事件后返回给您，代表工业指令转写结合指令集纠正后的最终结果。

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

固定为ai-result。

payload.output.aiResult

Object

payload.output.aiResult.correction

String

工业指令转写最终结果

ai-result事件的示例如下：

```
{
  "header": {
    "event": "result-generated",
    "task_id": "f2E3zvK*******wp"
  },
  "payload": {
    "output": {
      "action": "ai-result",
      "aiResult": {
        "correction": "右翼子板漆渣SQE。"
      }
    }
  }
}
```

### speech-end事件

对应时序图中的过程7。speech-end事件会在ai-result事件后发送给您，代表工业指令转写完全结束，之后您可以关闭WebSocket连接。

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
      "errorCode": "错误码",
      "errorMessage": "错误信息"
    }
  }
}
```

具体错误码及其含义，可以参考[错误码](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-industrial-instruction/tingwu-industrial-instruction-api/tingwu-industrial-instruction-api-websocket.md)。

### 错误码说明

**错误码**

**错误信息**

**说明**

InvalidParameter

Invalid parameter. Please refer to the official documents.

参数错误，请检查您传入的参数。

InvalidParameter

MaxEndSilence invalid, must between \[0. 6000\].

传入的maxEndSilence参数不合法。

InvalidParameter

Terminology not exist.

传入的指令集不存在。

InvalidParameter

SampleRate invalid.

传入的采样率参数不合法。

InvalidParameter

Audio format invalid.

传入的音频编码格式参数不合法。

InvalidParameter

Terminology invalid.

传入的指令集Id不合法。

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

Agent.CustomTaskIdInvalid

The length of custom task id must be 16.

传入的taskId字段长度不合法。

BIL.ServiceNotActivate

User hasn't activate service.

您尚未开通听悟Agent服务。

BIL.UserArrears

User is in arrears.

您目前处在欠费状态。

Agent.AppInfoNotExist

Agent App Info not exist.

传入的应用Id信息不存在，请先在控制台保存并发布应用配置信息。

ServerError

Server error.

服务端内部错误。

## 代码示例

以工业生产指令转写为例，调用 Java SDK 实现的示例如下：

```
package org.alibaba.speech.examples.speech_plus;

import com.alibaba.dashscope.multimodal.tingwu.TingWuRealtime;
import com.alibaba.dashscope.multimodal.tingwu.TingWuRealtimeCallback;
import com.alibaba.dashscope.multimodal.tingwu.TingWuRealtimeParam;
import com.google.gson.JsonObject;
import lombok.extern.slf4j.Slf4j;

import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.CountDownLatch;

@Slf4j
public class TingWuRealtimeUsage {

    private static CountDownLatch speechListenLatch = new CountDownLatch(1);
    private static boolean isStopped = false;

    public static TingWuRealtimeCallback tingWuRealtimeCallback = new TingWuRealtimeCallback() {

        @Override
        public void onStarted(String taskId) {
            log.debug("onStarted: {}", taskId);
        }

        @Override
        public void onStopped(String taskId) {
            log.debug("onStopped: {}", taskId);
            isStopped = true;
        }

        @Override
        public void onError(String errorCode, String errorMsg) {
            log.debug("onError: {}, {}", errorCode, errorMsg);
        }

        @Override
        public void onAiResult(String taskId, JsonObject content) {
            log.debug("onAiResult: {}, {}", taskId, content.toString());
        }

        @Override
        public void onRecognizeResult(String taskId, JsonObject content) {
            log.debug("onRecognizeResult: {}, {}", taskId, content.toString());
        }

        @Override
        public void onSpeechListen(String taskId, String dataId) {
            log.debug("onSpeechListen: {}", taskId);
            speechListenLatch.countDown();
        }

        @Override
        public void onClosed() {
            log.debug("onClosed");
        }
    };

    public static void main(String[] args) {
        TingWuRealtimeParam tingWuRealtimeParam = TingWuRealtimeParam.builder()
                .model("tingwu-industrial-instruction")
                .format("pcm")
                .sampleRate(16000)
                .terminology("your-terminology")
                .appId("your-app-id")
                .apiKey("your-api-key")
                .build();

        Path filePath = Paths.get("/path-to-your-file/test.pcm");
        String baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        TingWuRealtime tingWuRealtime = new TingWuRealtime(baseWebsocketApiUrl);
        tingWuRealtime.call(tingWuRealtimeParam, tingWuRealtimeCallback);

        try {
            // 等待 onSpeechListen 回调触发，设置超时时间为5秒
            if (!speechListenLatch.await(5, java.util.concurrent.TimeUnit.SECONDS)) {
                log.warn("onSpeechListen callback not received within 5 seconds");
            }
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        log.info("start to send audio....");

        // 发送音频
        try (FileInputStream fis = new FileInputStream(filePath.toFile())) {
            // chunk size set to 100 ms for 16KHz sample rate
            byte[] buffer = new byte[3200];
            int bytesRead;
            // Loop to read chunks of the file
            while ((bytesRead = fis.read(buffer)) != -1 && !isStopped) {
                ByteBuffer byteBuffer;
                if (bytesRead < buffer.length) {
                    byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
                } else {
                    byteBuffer = ByteBuffer.wrap(buffer);
                }
                // Send the ByteBuffer to the translation and recognition instance
                tingWuRealtime.sendAudioFrame(byteBuffer);
                Thread.sleep(100);
                buffer = new byte[3200];
            }
            if (!isStopped) {
                tingWuRealtime.stop();
            }
            Thread.sleep(1000 ); // wait for 10 seconds
            log.info("end test.");
            tingWuRealtime.getDuplexApi().close(1000, "bye");
        } catch (Exception e) {
            e.printStackTrace();
            tingWuRealtime.getDuplexApi().close(1000, "bye");
        }

        System.exit(0);
    }
}
```

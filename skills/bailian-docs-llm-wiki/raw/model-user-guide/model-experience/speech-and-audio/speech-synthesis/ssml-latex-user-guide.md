# SSML 与 LaTeX

使用 SSML 控制语速、音高、音量等声音特征，使用 LaTeX 朗读中文数学公式。本文介绍支持范围、调用示例及标签与符号参考。

<a id="功能介绍"></a>

<a id="feature-introduction"></a>

<a id="sl00_overview_h2"></a>

## 功能介绍

SSML 是基于 XML 的语音合成标记语言，可设置音色、语速、音高和音量等声音特征，控制停顿、指定发音与读法，并添加背景音乐和音效。CosyVoice 的 LaTeX 公式朗读功能可将文本中的数学公式转换为中文语音。

这两项功能可用于有声读物、客服信息播报、多语种发音和在线教育。各功能的适用模型、音色及接口见下文；模型选型请参见[语音合成](tts-model.md)。

<a id="使用限制"></a>

<a id="supported-scope"></a>

### 使用限制

<a id="sec-tabs"></a>

<a id="ssml"></a>

<a id="ssml-h4"></a>

#### SSML

<a id="sl01_constraint_h3"></a>

-   **支持模型：** qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash、qwen-audio-3.0-tts-plus、cosyvoice-v3.5-flash、cosyvoice-v3.5-plus、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2
    
-   **音色：** 仅复刻音色，以及[Qwen-Audio-TTS音色列表](tts-voice-list/qwen-audio-tts-voice-list.md)和[CosyVoice音色列表](tts-voice-list/cosyvoice-voice-list.md)中标注为支持 SSML 的系统音色可用。
    
-   **接口：**
    -   Java SDK（2.20.3 及以上版本）：支持非流式调用和单向流式调用
    -   Python SDK（2.0.1 及以上版本）：支持非流式调用和单向流式调用
    -   WebSocket API：需将参数 `enable_ssml` 设置为 `true`，且只允许发送一次 continue-task 事件
    -   HTTP API：需将参数 `enable_ssml` 设置为 `true`

<a id="latex"></a>

<a id="latex-h4"></a>

#### LaTeX

<a id="sl02_limit_h3"></a>

-   **支持模型：** cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2
    
-   **语种：**仅支持中文。
    
-   **内容：**公式必须在支持的标签与符号范围内。不支持 Markdown 数学公式代码块（例如标记为 `math` 的代码块）。分隔符内仅放公式，混入非公式文本可能导致朗读不准确。
    

<a id="使用方式"></a>

<a id="usage-and-examples"></a>

### 使用方式

<a id="sec-tabs-2"></a>

<a id="ssml-2"></a>

<a id="ssml-2-h4"></a>

#### SSML

<a id="sl01_ssml_h2"></a>

使用 SSML 时，请遵循以下规则：

-   所有文本必须放在 `<speak></speak>` 中。支持多个 `<speak>` 标签并列，不支持嵌套。
-   标签内的 XML 特殊字符需要转义：`"` → `&quot;`、`'` → `&apos;`、`&` → `&amp;`、`<` → `&lt;`、`>` → `&gt;`。

<a id="sl01_qs_h3"></a>

#### 快速开始

以下示例展示如何使用 SSML 控制语速进行语音合成。运行前，请完成以下准备工作：

1.  [获取与配置 API Key](../../../../model-api-reference/preparations/get-api-key.md)
2.  安装 DashScope SDK（Python 2.0.1 及以上版本，Java 2.20.3 及以上版本）。详情请参见[安装SDK](../../../../model-api-reference/preparations/install-sdk.md)。

> **重要**
>
> cosyvoice-v3.5-plus 和 cosyvoice-v3.5-flash 不提供系统音色。在本节 SSML 示例中使用这两个模型时，需先通过[音色复刻](voice-customization/voice-cloning-user-guide.md)创建复刻音色。

<a id="sec-tabs-3"></a>

<a id="java-sdk"></a>

<a id="java-sdk-h4"></a>

#### Java SDK

<a id="fig-code-group"></a>

<a id="fig-code-group-非流式调用-tab"></a>

非流式调用

<a id="code-code-group-非流式调用"></a>

```java
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

/**
 * SSML功能说明：
 *     1. 只有非流式调用和单向流式调用支持SSML功能
 * 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。
 */
public class Main {
    private static String model = "cosyvoice-v3-flash";
    private static String voice = "longanyang";

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }

    public static void streamAudioDataToSpeaker() {
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model)
                        .voice(voice)
                        .build();

        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        ByteBuffer audio = null;
        try {
            // 非流式调用，阻塞直至音频返回
            // 特殊字符需要进行转义
            audio = synthesizer.call("<speak rate=\"2\">我的语速比正常人快。</speak>");
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        if (audio != null) {
            // 将音频数据保存到本地文件“output.mp3”中
            File file = new File("output.mp3");
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(audio.array());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }
}
```

<a id="fig-code-group-单向流式调用-tab"></a>

单向流式调用

<a id="code-code-group-单向流式调用"></a>

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;

/**
 * SSML功能说明：
 *     1. 只有非流式调用和单向流式调用支持SSML功能
 * 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。
 */
public class Main {
    private static String model = "cosyvoice-v3-flash";
    private static String voice = "longanyang";

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.out.println("音频已保存到 output.mp3 文件中");
        System.exit(0);
    }

    public static void streamAudioDataToSpeaker() {
        CountDownLatch latch = new CountDownLatch(1);
        final FileOutputStream[] fileOutputStream = new FileOutputStream[1];

        try {
            fileOutputStream[0] = new FileOutputStream("output.mp3");
        } catch (IOException e) {
            System.err.println("无法创建输出文件: " + e.getMessage());
            return;
        }

        // 实现回调接口ResultCallback
        ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
            @Override
            public void onEvent(SpeechSynthesisResult result) {
                if (result.getAudioFrame() != null) {
                    // 将音频数据写入本地文件
                    try {
                        byte[] audioData = result.getAudioFrame().array();
                        fileOutputStream[0].write(audioData);
                        fileOutputStream[0].flush();
                    } catch (IOException e) {
                        System.err.println("写入音频数据失败: " + e.getMessage());
                    }
                }
            }

            @Override
            public void onComplete() {
                System.out.println("收到Complete，语音合成结束");
                closeFileOutputStream(fileOutputStream[0]);
                latch.countDown();
            }

            @Override
            public void onError(Exception e) {
                System.out.println("出现异常：" + e.toString());
                closeFileOutputStream(fileOutputStream[0]);
                latch.countDown();
            }
        };

        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model)
                        .voice(voice)
                        .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS)
                        .build();

        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);

        try {
            // 单向流式调用，立即返回null（实际结果通过回调接口异步传递），在回调接口的onEvent方法中实时获取二进制音频
            // 特殊字符需要进行转义
            synthesizer.call("<speak rate=\"2\">我的语速比正常人快。</speak>");
            // 等待合成完成
            latch.await();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束后关闭websocket连接
            try {
                synthesizer.getDuplexApi().close(1000, "bye");
            } catch (Exception e) {
                System.err.println("关闭WebSocket连接失败: " + e.getMessage());
            }

            // 确保文件流被关闭
            closeFileOutputStream(fileOutputStream[0]);
        }

        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    private static void closeFileOutputStream(FileOutputStream fileOutputStream) {
        try {
            if (fileOutputStream != null) {
                fileOutputStream.close();
            }
        } catch (IOException e) {
            System.err.println("关闭文件流失败: " + e.getMessage());
        }
    }
}
```

<a id="python-sdk"></a>

<a id="python-sdk-h4"></a>

#### Python SDK

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-非流式调用-tab"></a>

非流式调用

<a id="code-code-group-2-非流式调用"></a>

```python
# coding=utf-8
# SSML功能说明：
#     1. 只有非流式调用和单向流式调用支持SSML功能
# 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。

import os

import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "cosyvoice-v3-flash"
# 音色
voice = "longanyang"

# 非流式调用，阻塞直至音频返回
# 特殊字符需要进行转义
audio = client.audio.tts.synthesize(
    "<speak rate=\"2\">我的语速比正常人快。</speak>",
    model=model,
    voice=voice,
    enable_ssml=True)

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

<a id="fig-code-group-2-单向流式调用-tab"></a>

单向流式调用

<a id="code-code-group-2-单向流式调用"></a>

```python
# coding=utf-8
# SSML功能说明：
#     1. 只有非流式调用和单向流式调用支持SSML功能
# 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。

import os
from datetime import datetime

import dashscope

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "cosyvoice-v3-flash"
# 音色
voice = "longanyang"

# 单向流式调用，发送待合成文本，逐块实时获取二进制音频
# 特殊字符需要进行转义
with open("output.mp3", "wb") as f:
    for chunk in client.audio.tts.stream(
            "<speak rate=\"2\">我的语速比正常人快。</speak>",
            model=model,
            voice=voice,
            enable_ssml=True):
        print(get_timestamp() + " 二进制音频长度为：" + str(len(chunk)))
        # 将音频数据写入文件
        f.write(chunk)
print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
```

<a id="websocket-api"></a>

<a id="websocket-api-h4"></a>

#### WebSocket API

<a id="sec-tabs-4"></a>

<a id="java"></a>

<a id="java-h4"></a>

#### Java

Java 开发建议使用 Java DashScope SDK，详情请参见[Java SDK](../../../../_short/cosyvoice-websocket-sdk-java-a4920147be4869ef.md)。

以下是Java WebSocket的调用示例。在运行示例前，请确保已导入以下依赖：

-   `Java-WebSocket`
-   `jackson-databind`

建议使用 Maven 或 Gradle 管理依赖包，配置如下：

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-pom-xml-tab"></a>

pom.xml

<a id="code-code-group-3-pom-xml"></a>

```xml
<dependencies>
    <!-- WebSocket Client -->
    <dependency>
        <groupId>org.java-websocket</groupId>
        <artifactId>Java-WebSocket</artifactId>
        <version>1.5.3</version>
    </dependency>

    <!-- JSON Processing -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.13.0</version>
    </dependency>
</dependencies>
```

<a id="fig-code-group-3-build-gradle-tab"></a>

build.gradle

<a id="code-code-group-3-build-gradle"></a>

```groovy
// 省略其它代码
dependencies {
  // WebSocket Client
  implementation 'org.java-websocket:Java-WebSocket:1.5.3'
  // JSON Processing
  implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.0'
}
// 省略其它代码
```

Java代码如下：

<a id="code-block"></a>

```java
import com.fasterxml.jackson.databind.ObjectMapper;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.nio.ByteBuffer;
import java.util.*;

/**
 * SSML功能说明：
 *     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
 *     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
 * 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。
 */
public class TTSWebSocketClient extends WebSocketClient {
    private final String taskId = UUID.randomUUID().toString();
    private final String outputFile = "output_" + System.currentTimeMillis() + ".mp3";
    private boolean taskFinished = false;

    public TTSWebSocketClient(URI serverUri, Map<String, String> headers) {
        super(serverUri, headers);
    }

    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        System.out.println("连接成功");

        // 发送run-task指令
        // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
        String runTaskCommand = "{ \"header\": { \"action\": \"run-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"task_group\": \"audio\", \"task\": \"tts\", \"function\": \"SpeechSynthesizer\", \"model\": \"cosyvoice-v3-flash\", \"parameters\": { \"text_type\": \"PlainText\", \"voice\": \"longanyang\", \"format\": \"mp3\", \"sample_rate\": 22050, \"volume\": 50, \"rate\": 1, \"pitch\": 1, \"enable_ssml\": true }, \"input\": {} }}";
        send(runTaskCommand);
    }

    @Override
    public void onMessage(String message) {
        System.out.println("收到服务端返回的消息：" + message);
        try {
            // Parse JSON message
            Map<String, Object> messageMap = new ObjectMapper().readValue(message, Map.class);

            if (messageMap.containsKey("header")) {
                Map<String, Object> header = (Map<String, Object>) messageMap.get("header");

                if (header.containsKey("event")) {
                    String event = (String) header.get("event");

                    if ("task-started".equals(event)) {
                        System.out.println("收到服务端返回的task-started事件");

                        // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                        // 特殊字符需要进行转义
                        sendContinueTask("<speak rate=\\\"2\\\">我的语速比正常人快。</speak>");

                        // 发送finish-task指令
                        sendFinishTask();
                    } else if ("task-finished".equals(event)) {
                        System.out.println("收到服务端返回的task-finished事件");
                        taskFinished = true;
                        closeConnection();
                    } else if ("task-failed".equals(event)) {
                        System.out.println("任务失败：" + message);
                        closeConnection();
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("出现异常：" + e.getMessage());
        }
    }

    @Override
    public void onMessage(ByteBuffer message) {
        System.out.println("收到的二进制音频数据大小为：" + message.remaining());

        try (FileOutputStream fos = new FileOutputStream(outputFile, true)) {
            byte[] buffer = new byte[message.remaining()];
            message.get(buffer);
            fos.write(buffer);
            System.out.println("音频数据已写入本地文件" + outputFile + "中");
        } catch (IOException e) {
            System.err.println("音频数据写入本地文件失败：" + e.getMessage());
        }
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("连接关闭：" + reason + " (" + code + ")");
    }

    @Override
    public void onError(Exception ex) {
        System.err.println("报错：" + ex.getMessage());
        ex.printStackTrace();
    }

    private void sendContinueTask(String text) {
        String command = "{ \"header\": { \"action\": \"continue-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": { \"text\": \"" + text + "\" } }}";
        send(command);
    }

    private void sendFinishTask() {
        String command = "{ \"header\": { \"action\": \"finish-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": {} }}";
        send(command);
    }

    private void closeConnection() {
        if (!isClosed()) {
            close();
        }
    }

    public static void main(String[] args) {
        try {
            // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
            String apiKey = System.getenv("DASHSCOPE_API_KEY");
            if (apiKey == null || apiKey.isEmpty()) {
                System.err.println("请设置 DASHSCOPE_API_KEY 环境变量");
                return;
            }

            Map<String, String> headers = new HashMap<>();
            headers.put("Authorization", "bearer " + apiKey);
            // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
            TTSWebSocketClient client = new TTSWebSocketClient(new URI("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference/"), headers);

            client.connect();

            while (!client.isClosed() && !client.taskFinished) {
                Thread.sleep(1000);
            }
        } catch (Exception e) {
            System.err.println("连接WebSocket服务失败：" + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

<a id="python"></a>

<a id="python-h4"></a>

#### Python

Python 开发建议使用 Python DashScope SDK，详情请参见[Python SDK](../../../../_short/cosyvoice-websocket-sdk-python-47e109e34183e539.md#model-cosyvoice)。

以下是Python WebSocket的调用示例。在运行示例前，请确保通过如下方式导入依赖：

<a id="code-block-2"></a>

```bash
pip uninstall websocket-client
pip uninstall websocket
pip install websocket-client
```

> **重要**
>
> 运行示例代码的 Python 文件不能命名为 `websocket.py`，否则会报错（AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?）。

<a id="code-block-3"></a>

```python
# SSML功能说明：
#     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
#     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
# 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。

import websocket
import json
import uuid
import os
import time

class TTSClient:
    def __init__(self, api_key, uri):
        """
    初始化 TTSClient 实例

    参数:
        api_key (str): 鉴权用的 API Key
        uri (str): WebSocket 服务地址
    """
        self.api_key = api_key  # 替换为你的 API Key
        self.uri = uri  # 替换为你的 WebSocket 地址
        self.task_id = str(uuid.uuid4())  # 生成唯一任务 ID
        self.output_file = f"output_{int(time.time())}.mp3"  # 输出音频文件路径
        self.ws = None  # WebSocketApp 实例
        self.task_started = False  # 是否收到 task-started
        self.task_finished = False  # 是否收到 task-finished / task-failed

    def on_open(self, ws):
        """
    WebSocket 连接建立时回调函数
    发送 run-task 指令开启语音合成任务
    """
        print("WebSocket 已连接")

        # 构造 run-task 指令
        run_task_cmd = {
            "header": {
                "action": "run-task",
                "task_id": self.task_id,
                "streaming": "duplex"
            },
            "payload": {
                "task_group": "audio",
                "task": "tts",
                "function": "SpeechSynthesizer",
                "model": "cosyvoice-v3-flash",
                "parameters": {
                    "text_type": "PlainText",
                    "voice": "longanyang",
                    "format": "mp3",
                    "sample_rate": 22050,
                    "volume": 50,
                    "rate": 1,
                    "pitch": 1,
                    # 如果enable_ssml设为True，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                    "enable_ssml": True
                },
                "input": {}
            }
        }

        # 发送 run-task 指令
        ws.send(json.dumps(run_task_cmd))
        print("已发送 run-task 指令")

    def on_message(self, ws, message):
        """
    接收到消息时的回调函数
    区分文本和二进制消息处理
    """
        if isinstance(message, str):
            # 处理 JSON 文本消息
            try:
                msg_json = json.loads(message)
                print(f"收到 JSON 消息: {msg_json}")

                if "header" in msg_json:
                    header = msg_json["header"]

                    if "event" in header:
                        event = header["event"]

                        if event == "task-started":
                            print("任务已启动")
                            self.task_started = True

                            # 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                            # 特殊字符需要进行转义
                            self.send_continue_task("<speak rate=\"2\">我的语速比正常人快。</speak>")

                            # continue-task 发送完成后发送 finish-task
                            self.send_finish_task()

                        elif event == "task-finished":
                            print("任务已完成")
                            self.task_finished = True
                            self.close(ws)

                        elif event == "task-failed":
                            error_msg = msg_json.get("error_message", "未知错误")
                            print(f"任务失败: {error_msg}")
                            self.task_finished = True
                            self.close(ws)

            except json.JSONDecodeError as e:
                print(f"JSON 解析失败: {e}")
        else:
            # 处理二进制消息（音频数据）
            print(f"收到二进制消息，大小: {len(message)} 字节")
            with open(self.output_file, "ab") as f:
                f.write(message)
            print(f"已将音频数据写入本地文件{self.output_file}中")

    def on_error(self, ws, error):
        """发生错误时的回调"""
        print(f"WebSocket 出错: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭时的回调"""
        print(f"WebSocket 已关闭: {close_msg} ({close_status_code})")

    def send_continue_task(self, text):
        """发送 continue-task 指令，附带要合成的文本内容"""
        cmd = {
            "header": {
                "action": "continue-task",
                "task_id": self.task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {
                    "text": text
                }
            }
        }

        self.ws.send(json.dumps(cmd))
        print(f"已发送 continue-task 指令，文本内容: {text}")

    def send_finish_task(self):
        """发送 finish-task 指令，结束语音合成任务"""
        cmd = {
            "header": {
                "action": "finish-task",
                "task_id": self.task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            }
        }

        self.ws.send(json.dumps(cmd))
        print("已发送 finish-task 指令")

    def close(self, ws):
        """主动关闭连接"""
        if ws and ws.sock and ws.sock.connected:
            ws.close()
            print("已主动关闭连接")

    def run(self):
        """启动 WebSocket 客户端"""
        # 设置请求头部（鉴权）
        header = {
            "Authorization": f"bearer {self.api_key}",
            "X-DashScope-DataInspection": "enable"
        }

        # 创建 WebSocketApp 实例
        self.ws = websocket.WebSocketApp(
            self.uri,
            header=header,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        print("正在监听 WebSocket 消息...")
        self.ws.run_forever()  # 启动长连接监听

# 示例使用方式
if __name__ == "__main__":
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：API_KEY = "sk-xxx"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    SERVER_URI = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference/"

    client = TTSClient(API_KEY, SERVER_URI)
    client.run()
```

<a id="go"></a>

<a id="go-h4"></a>

#### Go

<a id="code-block-4"></a>

```go
// SSML功能说明：
//     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
//     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
// 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。

package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "strings"
    "time"

    "github.com/google/uuid"
    "github.com/gorilla/websocket"
)

const (
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    wsURL      = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference/"
    outputFile = "output.mp3"
)

func main() {
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey := "sk-xxx"
    apiKey := os.Getenv("DASHSCOPE_API_KEY")

    // 清空输出文件
    os.Remove(outputFile)
    os.Create(outputFile)

    // 连接WebSocket
    header := make(http.Header)
    header.Add("X-DashScope-DataInspection", "enable")
    header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))

    conn, resp, err := websocket.DefaultDialer.Dial(wsURL, header)
    if err != nil {
        if resp != nil {
            fmt.Printf("连接失败 HTTP状态码: %d\n", resp.StatusCode)
        }
        fmt.Println("连接失败:", err)
        return
    }
    defer conn.Close()

    // 生成任务ID
    taskID := uuid.New().String()
    fmt.Printf("生成任务ID: %s\n", taskID)

    // 发送run-task指令
    runTaskCmd := map[string]interface{}{
        "header": map[string]interface{}{
            "action":    "run-task",
            "task_id":   taskID,
            "streaming": "duplex",
        },
        "payload": map[string]interface{}{
            "task_group": "audio",
            "task":       "tts",
            "function":   "SpeechSynthesizer",
            "model":      "cosyvoice-v3-flash",
            "parameters": map[string]interface{}{
                "text_type":   "PlainText",
                "voice":       "longanyang",
                "format":      "mp3",
                "sample_rate": 22050,
                "volume":      50,
                "rate":        1,
                "pitch":       1,
                // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                "enable_ssml": true,
            },
            "input": map[string]interface{}{},
        },
    }

    runTaskJSON, _ := json.Marshal(runTaskCmd)
    fmt.Printf("发送run-task指令: %s\n", string(runTaskJSON))

    err = conn.WriteMessage(websocket.TextMessage, runTaskJSON)
    if err != nil {
        fmt.Println("发送run-task失败:", err)
        return
    }

    textSent := false

    // 处理消息
    for {
        messageType, message, err := conn.ReadMessage()
        if err != nil {
            fmt.Println("读取消息失败:", err)
            break
        }

        // 处理二进制消息
        if messageType == websocket.BinaryMessage {
            fmt.Printf("收到二进制消息，长度: %d\n", len(message))
            file, _ := os.OpenFile(outputFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
            file.Write(message)
            file.Close()
            continue
        }

        // 处理文本消息
        messageStr := string(message)
        fmt.Printf("收到文本消息: %s\n", strings.ReplaceAll(messageStr, "\n", ""))

        // 简单解析JSON获取event类型
        var msgMap map[string]interface{}
        if json.Unmarshal(message, &msgMap) == nil {
            if header, ok := msgMap["header"].(map[string]interface{}); ok {
                if event, ok := header["event"].(string); ok {
                    fmt.Printf("事件类型: %s\n", event)

                    switch event {
                    case "task-started":
                        fmt.Println("=== 收到task-started事件 ===")

                        if !textSent {
                            // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                            continueTaskCmd := map[string]interface{}{
                                "header": map[string]interface{}{
                                    "action":    "continue-task",
                                    "task_id":   taskID,
                                    "streaming": "duplex",
                                },
                                "payload": map[string]interface{}{
                                    "input": map[string]interface{}{
                                        // 特殊字符需要进行转义
                                        "text": "<speak rate=\"2\">我的语速比正常人快。</speak>",
                                    },
                                },
                            }

                            continueTaskJSON, _ := json.Marshal(continueTaskCmd)
                            fmt.Printf("发送continue-task指令: %s\n", string(continueTaskJSON))

                            err = conn.WriteMessage(websocket.TextMessage, continueTaskJSON)
                            if err != nil {
                                fmt.Println("发送continue-task失败:", err)
                                return
                            }

                            textSent = true

                            // 延迟发送finish-task
                            time.Sleep(500 * time.Millisecond)

                            // 发送finish-task指令
                            finishTaskCmd := map[string]interface{}{
                                "header": map[string]interface{}{
                                    "action":    "finish-task",
                                    "task_id":   taskID,
                                    "streaming": "duplex",
                                },
                                "payload": map[string]interface{}{
                                    "input": map[string]interface{}{},
                                },
                            }

                            finishTaskJSON, _ := json.Marshal(finishTaskCmd)
                            fmt.Printf("发送finish-task指令: %s\n", string(finishTaskJSON))

                            err = conn.WriteMessage(websocket.TextMessage, finishTaskJSON)
                            if err != nil {
                                fmt.Println("发送finish-task失败:", err)
                                return
                            }
                        }

                    case "task-finished":
                        fmt.Println("=== 任务完成 ===")
                        return

                    case "task-failed":
                        fmt.Println("=== 任务失败 ===")
                        if header["error_message"] != nil {
                            fmt.Printf("错误信息: %s\n", header["error_message"])
                        }
                        return

                    case "result-generated":
                        fmt.Println("收到result-generated事件")
                    }
                }
            }
        }
    }
}
```

<a id="c"></a>

<a id="c-h4"></a>

#### C#

<a id="code-block-5"></a>

```csharp
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

// SSML功能说明：
//     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
//     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
// 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。
class Program {
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：private static readonly string ApiKey = "sk-xxx"
    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    private const string WebSocketUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference/";
    // 输出文件路径
    private const string OutputFilePath = "output.mp3";

    // WebSocket客户端
    private static ClientWebSocket _webSocket = new ClientWebSocket();
    // 取消令牌源
    private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
    // 任务ID
    private static string? _taskId;
    // 任务是否已启动
    private static TaskCompletionSource<bool> _taskStartedTcs = new TaskCompletionSource<bool>();

    static async Task Main(string[] args) {
        try {
            // 清空输出文件
            ClearOutputFile(OutputFilePath);

            // 连接WebSocket服务
            await ConnectToWebSocketAsync(WebSocketUrl);

            // 启动接收消息的任务
            Task receiveTask = ReceiveMessagesAsync();

            // 发送run-task指令
            _taskId = GenerateTaskId();
            await SendRunTaskCommandAsync(_taskId);

            // 等待task-started事件
            await _taskStartedTcs.Task;

            // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
            // 特殊字符需要进行转义
            await SendContinueTaskCommandAsync("<speak rate=\"2\">我的语速比正常人快。</speak>");

            // 发送finish-task指令
            await SendFinishTaskCommandAsync(_taskId);

            // 等待接收任务完成
            await receiveTask;

            Console.WriteLine("任务完成，连接已关闭。");
        } catch (OperationCanceledException) {
            Console.WriteLine("任务被取消。");
        } catch (Exception ex) {
            Console.WriteLine($"发生错误：{ex.Message}");
        } finally {
            _cancellationTokenSource.Cancel();
            _webSocket.Dispose();
        }
    }

    private static void ClearOutputFile(string filePath) {
        if (File.Exists(filePath)) {
            File.WriteAllText(filePath, string.Empty);
            Console.WriteLine("输出文件已清空。");
        } else {
            Console.WriteLine("输出文件不存在，无需清空。");
        }
    }

    private static async Task ConnectToWebSocketAsync(string url) {
        var uri = new Uri(url);
        if (_webSocket.State == WebSocketState.Connecting || _webSocket.State == WebSocketState.Open) {
            return;
        }

        // 设置WebSocket连接的头部信息
        _webSocket.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
        _webSocket.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");

        try {
            await _webSocket.ConnectAsync(uri, _cancellationTokenSource.Token);
            Console.WriteLine("已成功连接到WebSocket服务。");
        } catch (OperationCanceledException) {
            Console.WriteLine("WebSocket连接被取消。");
        } catch (Exception ex) {
            Console.WriteLine($"WebSocket连接失败: {ex.Message}");
            throw;
        }
    }

    private static async Task SendRunTaskCommandAsync(string taskId) {
        var command = CreateCommand("run-task", taskId, "duplex", new {
            task_group = "audio",
            task = "tts",
            function = "SpeechSynthesizer",
            model = "cosyvoice-v3-flash",
            parameters = new
            {
                text_type = "PlainText",
                voice = "longanyang",
                format = "mp3",
                sample_rate = 22050,
                volume = 50,
                rate = 1,
                pitch = 1,
                // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                enable_ssml = true
            },
            input = new { }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("已发送run-task指令。");
    }

    private static async Task SendContinueTaskCommandAsync(string text) {
        if (_taskId == null) {
            throw new InvalidOperationException("任务ID未初始化。");
        }

        var command = CreateCommand("continue-task", _taskId, "duplex", new {
            input = new {
                text
            }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("已发送continue-task指令。");
    }

    private static async Task SendFinishTaskCommandAsync(string taskId) {
        var command = CreateCommand("finish-task", taskId, "duplex", new {
            input = new { }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("已发送finish-task指令。");
    }

    private static async Task SendJsonMessageAsync(string message) {
        var buffer = Encoding.UTF8.GetBytes(message);
        try {
            await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
        } catch (OperationCanceledException) {
            Console.WriteLine("消息发送被取消。");
        }
    }

    private static async Task ReceiveMessagesAsync() {
        while (_webSocket.State == WebSocketState.Open) {
            var response = await ReceiveMessageAsync();
            if (response != null) {
                var eventStr = response.RootElement.GetProperty("header").GetProperty("event").GetString();
                switch (eventStr) {
                    case "task-started":
                        Console.WriteLine("任务已启动。");
                        _taskStartedTcs.TrySetResult(true);
                        break;
                    case "task-finished":
                        Console.WriteLine("任务已完成。");
                        _cancellationTokenSource.Cancel();
                        break;
                    case "task-failed":
                        Console.WriteLine("任务失败：" + response.RootElement.GetProperty("header").GetProperty("error_message").GetString());
                        _cancellationTokenSource.Cancel();
                        break;
                    default:
                        // result-generated可在此处理
                        break;
                }
            }
        }
    }

    private static async Task<JsonDocument?> ReceiveMessageAsync() {
        var buffer = new byte[1024 * 4];
        var segment = new ArraySegment<byte>(buffer);

        try {
            WebSocketReceiveResult result = await _webSocket.ReceiveAsync(segment, _cancellationTokenSource.Token);

            if (result.MessageType == WebSocketMessageType.Close) {
                await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cancellationTokenSource.Token);
                return null;
            }

            if (result.MessageType == WebSocketMessageType.Binary) {
                // 处理二进制数据
                Console.WriteLine("接收到二进制数据...");

                // 将二进制数据保存到文件
                using (var fileStream = new FileStream(OutputFilePath, FileMode.Append)) {
                    fileStream.Write(buffer, 0, result.Count);
                }

                return null;
            }

            string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
            return JsonDocument.Parse(message);
        } catch (OperationCanceledException) {
            Console.WriteLine("消息接收被取消。");
            return null;
        }
    }

    private static string GenerateTaskId() {
        return Guid.NewGuid().ToString("N").Substring(0, 32);
    }

    private static string CreateCommand(string action, string taskId, string streaming, object payload) {
        var command = new {
            header = new {
                action,
                task_id = taskId,
                streaming
            },
            payload
        };

        return JsonSerializer.Serialize(command);
    }
}
```

<a id="php"></a>

<a id="php-h4"></a>

#### PHP

示例代码目录结构为：

my-php-project/

├── composer.json

├── vendor/

└── index.php

composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

<a id="code-block-6"></a>

```json
{
    "require": {
        "react/event-loop": "^1.3",
        "react/socket": "^1.11",
        "react/stream": "^1.2",
        "react/http": "^1.1",
        "ratchet/pawl": "^0.4"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

index.php内容如下：

<a id="code-block-7"></a>

```php
<!-- SSML功能说明： -->
<!--     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持 -->
<!--     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令 -->
<!--     3. 只有qwen-audio-3.0-tts-flash、qwen-audio-3.0-tts-plus、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色） -->

<?php

require __DIR__ . '/vendor/autoload.php';

use Ratchet\Client\Connector;
use React\EventLoop\Loop;
use React\Socket\Connector as SocketConnector;

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用百炼API Key将下行替换为：$api_key = "sk-xxx"
$api_key = getenv("DASHSCOPE_API_KEY");
// 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
$websocket_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference/'; // WebSocket服务器地址
$output_file = 'output.mp3'; // 输出文件路径

$loop = Loop::get();

if (file_exists($output_file)) {
    // 清空文件内容
    file_put_contents($output_file, '');
}

// 创建自定义的连接器
$socketConnector = new SocketConnector($loop, [
    'tcp' => [
        'bindto' => '0.0.0.0:0',
    ],
    'tls' => [
        'verify_peer' => false,
        'verify_peer_name' => false,
    ],
]);

$connector = new Connector($loop, $socketConnector);

$headers = [
    'Authorization' => 'bearer ' . $api_key,
    'X-DashScope-DataInspection' => 'enable'
];

$connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $output_file) {
    echo "连接到WebSocket服务器\n";

    // 生成任务ID
    $taskId = generateTaskId();

    // 发送 run-task 指令
    sendRunTaskMessage($conn, $taskId);

    // 定义发送 continue-task 指令的函数
    $sendContinueTask = function() use ($conn, $loop, $taskId) {
        // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
        $continueTaskMessage = json_encode([
            "header" => [
                "action" => "continue-task",
                "task_id" => $taskId,
                "streaming" => "duplex"
            ],
            "payload" => [
                "input" => [
                    // 特殊字符需要进行转义
                    "text" => "<speak rate=\"2\">我的语速比正常人快。</speak>"
                ]
            ]
        ]);
        $conn->send($continueTaskMessage);

        // 发送 finish-task 指令
        sendFinishTaskMessage($conn, $taskId);
    };

    // 标记是否收到 task-started 事件
    $taskStarted = false;

    // 监听消息
    $conn->on('message', function($msg) use ($conn, $sendContinueTask, $loop, &$taskStarted, $taskId, $output_file) {
        if ($msg->isBinary()) {
            // 写入二进制数据到本地文件
            file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
        } else {
            // 处理非二进制消息
            $response = json_decode($msg, true);

            if (isset($response['header']['event'])) {
                handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, $taskStarted);
            } else {
                echo "未知的消息格式\n";
            }
        }
    });

    // 监听连接关闭
    $conn->on('close', function($code = null, $reason = null) {
        echo "连接已关闭\n";
        if ($code !== null) {
            echo "关闭代码: " . $code . "\n";
        }
        if ($reason !== null) {
            echo "关闭原因：" . $reason . "\n";
        }
    });
}, function ($e) {
    echo "无法连接：{$e->getMessage()}\n";
});

$loop->run();

/**
 * 生成任务ID
 * @return string
 */
function generateTaskId(): string {
    return bin2hex(random_bytes(16));
}

/**
 * 发送 run-task 指令
 * @param $conn
 * @param $taskId
 */
function sendRunTaskMessage($conn, $taskId) {
    $runTaskMessage = json_encode([
        "header" => [
            "action" => "run-task",
            "task_id" => $taskId,
            "streaming" => "duplex"
        ],
        "payload" => [
            "task_group" => "audio",
            "task" => "tts",
            "function" => "SpeechSynthesizer",
            "model" => "cosyvoice-v3-flash",
            "parameters" => [
                "text_type" => "PlainText",
                "voice" => "longanyang",
                "format" => "mp3",
                "sample_rate" => 22050,
                "volume" => 50,
                "rate" => 1,
                "pitch" => 1,
                // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                "enable_ssml" => true
            ],
            "input" => (object) []
        ]
    ]);
    echo "准备发送run-task指令: " . $runTaskMessage . "\n";
    $conn->send($runTaskMessage);
    echo "run-task指令已发送\n";
}

/**
 * 读取音频文件
 * @param string $filePath
 * @return bool|string
 */
function readAudioFile(string $filePath) {
    $voiceData = file_get_contents($filePath);
    if ($voiceData === false) {
        echo "无法读取音频文件\n";
    }
    return $voiceData;
}

/**
 * 分割音频数据
 * @param string $data
 * @param int $chunkSize
 * @return array
 */
function splitAudioData(string $data, int $chunkSize): array {
    return str_split($data, $chunkSize);
}

/**
 * 发送 finish-task 指令
 * @param $conn
 * @param $taskId
 */
function sendFinishTaskMessage($conn, $taskId) {
    $finishTaskMessage = json_encode([
        "header" => [
            "action" => "finish-task",
            "task_id" => $taskId,
            "streaming" => "duplex"
        ],
        "payload" => [
            "input" => (object) []
        ]
    ]);
    echo "准备发送finish-task指令: " . $finishTaskMessage . "\n";
    $conn->send($finishTaskMessage);
    echo "finish-task指令已发送\n";
}

/**
 * 处理事件
 * @param $conn
 * @param $response
 * @param $sendContinueTask
 * @param $loop
 * @param $taskId
 * @param $taskStarted
 */
function handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, &$taskStarted) {
    switch ($response['header']['event']) {
        case 'task-started':
            echo "任务开始，发送continue-task指令...\n";
            $taskStarted = true;
            // 发送 continue-task 指令
            $sendContinueTask();
            break;
        case 'result-generated':
            // 忽略result-generated事件
            break;
        case 'task-finished':
            echo "任务完成\n";
            $conn->close();
            break;
        case 'task-failed':
            echo "任务失败\n";
            echo "错误代码：" . $response['header']['error_code'] . "\n";
            echo "错误信息：" . $response['header']['error_message'] . "\n";
            $conn->close();
            break;
        case 'error':
            echo "错误：" . $response['payload']['message'] . "\n";
            break;
        default:
            echo "未知事件：" . $response['header']['event'] . "\n";
            break;
    }

    // 如果任务已完成，关闭连接
    if ($response['header']['event'] == 'task-finished') {
        // 等待1秒以确保所有数据都已传输完毕
        $loop->addTimer(1, function() use ($conn) {
            $conn->close();
            echo "客户端关闭连接\n";
        });
    }

    // 如果没有收到 task-started 事件，关闭连接
    if (!$taskStarted && in_array($response['header']['event'], ['task-failed', 'error'])) {
        $conn->close();
    }
}
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

需安装相关依赖：

<a id="code-block-8"></a>

```bash
npm install ws
npm install uuid
```

示例代码如下：

<a id="code-block-9"></a>

```javascript
// SSML功能说明：
//     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
//     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
// 使用支持 SSML 的复刻音色或系统音色（如 cosyvoice-v3-flash 的 longanyang）；适用模型见本页使用限制。

import fs from 'fs';
import WebSocket from 'ws';
import { v4 as uuid } from 'uuid'; // 用于生成UUID

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用百炼API Key将下行替换为：const apiKey = "sk-xxx"
const apiKey = process.env.DASHSCOPE_API_KEY;
// 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
const url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference/';
// 输出文件路径
const outputFilePath = 'output.mp3';

// 清空输出文件
fs.writeFileSync(outputFilePath, '');

// 创建WebSocket客户端
const ws = new WebSocket(url, {
  headers: {
    Authorization: `bearer ${apiKey}`,
    'X-DashScope-DataInspection': 'enable'
  }
});

let taskStarted = false;
let taskId = uuid();

ws.on('open', () => {
  console.log('已连接到WebSocket服务器');

  // 发送run-task指令
  const runTaskMessage = JSON.stringify({
    header: {
      action: 'run-task',
      task_id: taskId,
      streaming: 'duplex'
    },
    payload: {
      task_group: 'audio',
      task: 'tts',
      function: 'SpeechSynthesizer',
      model: 'cosyvoice-v3-flash',
      parameters: {
        text_type: 'PlainText',
        voice: 'longanyang', // 音色
        format: 'mp3', // 音频格式
        sample_rate: 22050, // 采样率
        volume: 50, // 音量
        rate: 1, // 语速
        pitch: 1, // 音调
        enable_ssml: true // 是否开启SSML功能。如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
      },
      input: {}
    }
  });
  ws.send(runTaskMessage);
  console.log('已发送run-task消息');
});

const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
ws.on('message', (data, isBinary) => {
  if (isBinary) {
    // 写入二进制数据到文件
    fileStream.write(data);
  } else {
    const message = JSON.parse(data);

    switch (message.header.event) {
      case 'task-started':
        taskStarted = true;
        console.log('任务已开始');
        // 发送continue-task指令
        sendContinueTasks(ws);
        break;
      case 'task-finished':
        console.log('任务已完成');
        ws.close();
        fileStream.end(() => {
          console.log('文件流已关闭');
        });
        break;
      case 'task-failed':
        console.error('任务失败：', message.header.error_message);
        ws.close();
        fileStream.end(() => {
          console.log('文件流已关闭');
        });
        break;
      default:
        // 可以在这里处理result-generated
        break;
    }
  }
});

function sendContinueTasks(ws) {

  if (taskStarted) {
    // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
    const continueTaskMessage = JSON.stringify({
      header: {
        action: 'continue-task',
        task_id: taskId,
        streaming: 'duplex'
      },
      payload: {
        input: {
          // 特殊字符需要进行转义
          text: '<speak rate="2">我的语速比正常人快。</speak>'
        }
      }
    });
    ws.send(continueTaskMessage);

    // 发送finish-task指令
    const finishTaskMessage = JSON.stringify({
      header: {
        action: 'finish-task',
        task_id: taskId,
        streaming: 'duplex'
      },
      payload: {
        input: {}
      }
    });
    ws.send(finishTaskMessage);
  }
}

ws.on('close', () => {
  console.log('已断开与WebSocket服务器的连接');
});
```

<a id="http-api"></a>

<a id="http-api-h4"></a>

#### HTTP API

<a id="code-block-10"></a>

```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "<speak rate=\"2\">我的语速比正常人快。</speak>",
      "voice": "longanyang",
      "format": "mp3",
      "sample_rate": 24000,
      "enable_ssml": true
    }
}'
```

<a id="latex-2"></a>

<a id="latex-2-h4"></a>

#### LaTeX

<a id="sl02_latex_h2"></a>

<a id="sl02_usage_h3"></a>

#### 使用方法

将数学公式用分隔符包裹后，调用语音合成 API。

**支持的分隔符**（任选一种，效果相同）：

-   `$...$`
-   `$$...$$`
-   `\(...\)`
-   `\[...\]`

**示例输入：**

<a id="code-block-11"></a>

```text
这是一道分数：$\frac{1}{2}$。
```

上述分数朗读为“二分之一”。

包含多个运算符的公式也使用相同的分隔符，例如：

<a id="code-block-12"></a>

```text
这是一道一元二次方程的求根公式：$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$，请仔细计算。
```

在 JSON 和 Python、Java、JavaScript 等语言的普通字符串中，反斜杠 `\` 需要写为 `\\`。例如，公式中的 `\frac` 在普通字符串中写为 `\\frac`。

<a id="sl02_qs_h3"></a>

#### 快速开始

以下 Python 示例合成包含分数的中文文本，保存为 `output.mp3`。API Key 和 SDK 的准备方法见 SSML 快速开始。

<a id="code-block-13"></a>

```python
# coding=utf-8

import os

import dashscope

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

model = "cosyvoice-v3-flash"
voice = "longanyang"

# 公式中的反斜杠需要转义为 \\
audio = client.audio.tts.synthesize("这是一道分数：$\\frac{1}{2}$。", model=model, voice=voice)

with open('output.mp3', 'wb') as f:
    f.write(audio)
```

<a id="ssml-标签"></a>

<a id="sl01_tagref_h3"></a>

## SSML 标签

> **说明**
>
> 功能实现参考 [W3C SSML 1.0 规范](https://www.w3.org/TR/speech-synthesis/)，支持的标签以下文为准，并非全部标准标签。

<a id="speak-根节点"></a>

<a id="title-7k1-est-sl7"></a>

### `<speak>`：根节点

`<speak>` 是所有 SSML 标签的根节点。使用 SSML 功能时，文本内容必须包含在 `<speak></speak>` 标签之间。

<a id="code-block-14"></a>

```xml
<speak>需要使用SSML功能的文本</speak>
```

<a id="sec-tabs-5"></a>

<a id="属性"></a>

<a id="属性-h4"></a>

#### 属性

<table><thead><tr><th><p><strong>属性名称</strong></p></th><th><p><strong>属性类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p><code>voice</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>指定发音人（音色）。</p><p>该属性的优先级高于接口请求参数<code>voice</code>指定的发音人。</p><ul><li>取值范围：具体的音色，详情请参见<a href="tts-voice-list/cosyvoice-voice-list.md">CosyVoice 音色列表</a>。</li></ul></td></tr><tr><td><p><code>rate</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>指定语速。该属性的优先级高于接口请求参数<code>rate</code>指定的语速。</p><ul><li><p>取值范围：[0.5,2]之间的小数</p></li><li><p>默认值：1</p><ul><li>大于1表示加快语速</li><li>小于1表示减慢语速</li></ul></li></ul></td></tr><tr><td><p><code>pitch</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>指定音高（语调）。该属性的优先级高于接口请求参数<code>pitch</code>指定的音高。</p><ul><li><p>取值范围：[0.5,2]之间的小数</p></li><li><p>默认值：1</p><ul><li>大于1表示升高音高</li><li>小于1表示降低音高</li></ul></li></ul></td></tr><tr><td><p><code>volume</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>指定音量。该属性的优先级高于接口请求参数<code>volume</code>指定的音量。</p><ul><li><p>取值范围：[0,100]之间的整数</p></li><li><p>默认值：50</p><ul><li>大于50表示增大音量</li><li>小于50表示减小音量</li></ul></li></ul></td></tr><tr><td><p><code>effect</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>指定音效。</p><ul><li><p>取值范围：</p><ul><li>robot：机器人音效</li><li>lolita：萝莉音效</li><li>lowpass：低通音效</li><li>echo：回声音效</li><li>eq：均衡器（高级）</li><li>lpfilter：低通滤波器（高级）</li><li>hpfilter：高通滤波器（高级）</li></ul><div><div><p><strong>说明</strong></p><ul><li>eq、lpfilter 和 hpfilter 是高级音效类型，可通过<code>effectValue</code>参数自定义具体效果。</li><li>每个 SSML 标签仅支持配置一种音效，不允许同时设置多个 <code>effect</code> 属性。</li><li>启用音效功能会增加合成延时。</li></ul></div></div></li></ul></td></tr><tr><td><p><code>effectValue</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>用于进一步配置音效（<code>effect</code>参数）的具体效果，适用于 eq、lpfilter、hpfilter 三种高级音效类型。</p><ul><li><p>取值范围：</p><ul><li><p><code>eq</code>（均衡器）：系统默认支持8个频率等级，对应频率如下：</p><p>[“40 Hz”,“100 Hz”, “200 Hz”, “400 Hz”, “800 Hz”, “1600 Hz”, “4000 Hz”, “12000 Hz”]。</p><p>每个频段的带宽均为 1.0q。</p><p>通过 <code>effectValue</code> 参数指定每个频段的增益值：该参数为由 8 个整数组成的字符串，数值范围为 [-20, 20]，数字之间用空格分隔。数值为 <code>0</code> 表示不调整对应频率的增益。</p><p>例如：<code>effectValue=&quot;1 1 1 1 1 1 1 1&quot;</code></p></li><li><p><code>lpfilter</code>（低通滤波器）：指定低通滤波器的截止频率，取值为 (0, 目标采样率/2] 之间的整数。例如 effectValue=&quot;800&quot;。</p></li><li><p><code>hpfilter</code>（高通滤波器）：指定高通滤波器的截止频率，取值为 (0, 目标采样率/2] 之间的整数。例如 effectValue=&quot;1200&quot;。</p></li></ul></li></ul></td></tr><tr><td><p><code>bgm</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>为合成语音添加背景音乐。</p><p>音频文件需存储在阿里云 OSS 上，并可通过外网 URL 访问，上传方法请参见<a href="https://help.aliyun.com/zh/oss/user-guide/console-quick-start">上传文件</a>。私有文件可使用有效的签名 URL。URL 中的 XML 特殊字符须转义，例如将 <code>&amp;</code> 写为 <code>&amp;amp;</code>。</p><ul><li><p>音频要求：</p><p>背景音文件大小无上限，但文件越大下载耗时越长。如果合成语音的时长超过背景音时长，背景音将自动循环播放。</p><ul><li><p>采样率：16kHz</p></li><li><p>声道数：单声道</p></li><li><p>文件格式：WAV</p><p>若原始音频非 WAV 格式，可使用 <code>ffmpeg</code> 工具进行转换：</p><a id="code-block-15"></a><pre class="language-bash"><code>ffmpeg -i 输入音频 -acodec pcm_s16le -ac 1 -ar 16000 输出.wav
</code></pre></li><li><p>位深度：16位</p></li></ul></li></ul><div><div><p><strong>重要</strong>上传方应对上传音频的版权承担相应的法律责任。</p></div></div></td></tr><tr><td><p><code>backgroundMusicVolume</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>指定背景音乐的音量。需与<code>bgm</code>属性搭配使用。</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="示例-h4"></a>

#### 示例

**空属性**

<a id="code-block-16"></a>

```xml
<speak>
  需要调用SSML标签的文本
</speak>
```

**属性组合（空格分隔）**

<a id="code-block-17"></a>

```xml
<speak rate="1.5" pitch="0.8" volume="80">
  所以放在一起，我的声音是这样的。
</speak>
```

**voice**

<a id="code-block-18"></a>

```xml
<speak voice="longcheng_v2">
  我是男声。
</speak>
```

**rate**

<a id="code-block-19"></a>

```xml
<speak rate="2">
  我的语速比正常人快。
</speak>
```

**pitch**

<a id="code-block-20"></a>

```xml
<speak pitch="0.5">
  我的音高却比别人低。
</speak>
```

**volume**

<a id="code-block-21"></a>

```xml
<speak volume="80">
  我的音量也很大。
</speak>
```

**effect**

<a id="code-block-22"></a>

```xml
<speak effect="robot">
  你喜欢机器人瓦力吗？
</speak>
```

**effectValue**

<a id="code-block-23"></a>

```xml
<speak effect="eq" effectValue="1 -20 1 1 1 1 20 1">
  你喜欢机器人瓦力吗？
</speak>

<speak effect="lpfilter" effectValue="1200">
  你喜欢机器人瓦力吗？
</speak>

<speak effect="hpfilter" effectValue="1200">
  你喜欢机器人瓦力吗？
</speak>
```

**bgm**

<a id="code-block-24"></a>

```xml
<speak bgm="https://nls.alicdn.com/bgm/2.wav" backgroundMusicVolume="30" rate="0.8" volume="40">
  <break time="2s"/>
  阴崖老木苍苍烟
  <break time="700ms"/>
  雨声犹在竹林间
  <break time="700ms"/>
  绵蕝固知裨国计
  <break time="700ms"/>
  绵州风物总堪怜
  <break time="2s"/>
</speak>
```

<a id="标签关系"></a>

<a id="标签关系-h4"></a>

#### 标签关系

<speak> 标签可以包含文本和以下子标签：

-   `<break>`：控制停顿时间
-   `<sub>`：替换文本
-   `<phoneme>`：指定发音（拼音/音标）
-   `<soundEvent>`：插入一段外部声音（铃声、猫叫等）
-   `<say-as>`：设置文本的读法（数字、日期、电话号码等）

<a id="break-控制停顿"></a>

<a id="title-722-sn2-4x8"></a>

### `<break>`：控制停顿

在语音合成过程中插入一段静默停顿，模拟自然说话中的间歇。支持秒（s）和毫秒（ms）两种单位。

<a id="code-block-25"></a>

```xml
<!-- 空属性 -->
<break/>
<!-- 带time属性 -->
<break time="string"/>
```

<a id="sec-tabs-6"></a>

<a id="属性-2"></a>

<a id="属性-2-h4"></a>

#### 属性

<table><thead><tr><th><p><strong>属性名称</strong></p></th><th><p><strong>属性类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p><code>time</code></p></td><td><p>String</p></td><td><p>否</p></td><td><p>设置停顿时长，支持秒和毫秒两种单位（如 “2s” 或 “50ms”）。</p><ul><li><p>取值范围：</p><ul><li>以秒（s）为单位，取值范围为[1, 10]之间的整数</li><li>以毫秒（ms）为单位，取值范围为[50, 10000]之间的整数</li></ul></li></ul><p>连续使用多个 <code>&lt;break&gt;</code> 标签时，总停顿时长为各标签时间的累加值。如果总时长超过 10 秒，则仅保留前 10 秒。</p></td></tr></tbody></table>

不带属性的 `<break>` 默认停顿 1 秒。

<a id="示例-2"></a>

<a id="示例-2-h4"></a>

#### 示例

**time**

<a id="code-block-26"></a>

```xml
<speak>
  请闭上眼睛休息一下<break time="500ms"/>好了，请睁开眼睛。
</speak>
```

连续使用以下三个 `<break>` 标签时，设置的总停顿时长为 15 秒，实际仅保留 10 秒。

<a id="code-block-27"></a>

```xml
<speak>
  请闭上眼睛休息一下<break time="5s"/><break time="5s"/><break time="5s"/>好了，请睁开眼睛。
</speak>
```

<a id="标签关系-2"></a>

<a id="标签关系-2-h4"></a>

#### 标签关系

<break> 是自闭合标签，不能包含任何子标签。

<a id="sub-替换文本"></a>

<a id="title-4jk-q1t-jwz"></a>

### `<sub>`：替换文本

将指定文本替换为更适合朗读的内容。例如，将 “W3C” 朗读为 “网络协议标准”。

<a id="code-block-28"></a>

```xml
<sub alias="string"></sub>
```

<a id="sec-tabs-7"></a>

<a id="属性-3"></a>

<a id="属性-3-h4"></a>

#### 属性

| 属性名称 | 属性类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| `alias` | String | 是 | 指定用于替代原文本的朗读内容。 |

<a id="示例-3"></a>

<a id="示例-3-h4"></a>

#### 示例

**alias**

<a id="code-block-29"></a>

```xml
<speak>
  <sub alias="网络协议标准">W3C</sub>
</speak>
```

<a id="标签关系-3"></a>

<a id="标签关系-3-h4"></a>

#### 标签关系

<sub> 标签内只能包含纯文本。

<a id="phoneme-指定发音"></a>

<a id="title-m9h-7yc-48k"></a>

### `<phoneme>`：指定发音

精确控制文本的发音方式。中文可通过拼音指定读音，英文可使用 CMU 音标。适用于多音字消歧和外语发音等场景。

<a id="code-block-30"></a>

```xml
<phoneme alphabet="string" ph="string">文本</phoneme>
```

<a id="sec-tabs-8"></a>

<a id="属性-4"></a>

<a id="属性-4-h4"></a>

#### 属性

<table><thead><tr><th><p><strong>属性名称</strong></p></th><th><p><strong>属性类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p><code>alphabet</code></p></td><td><p>String</p></td><td><p>是</p></td><td><p>指定发音类型：拼音（对应中文）或音标（对应英文）。</p><p>取值范围：</p><ul><li>&quot;py&quot;：拼音</li><li>&quot;cmu&quot;：音标，参见<a href="http://www.speech.cs.cmu.edu/cgi-bin/cmudict">The CMU Pronouncing Dictionary</a></li></ul></td></tr><tr><td><p><code>ph</code></p></td><td><p>String</p></td><td><p>是</p></td><td><p>指定具体的拼音或音标。使用规则如下：</p><ul><li>多个汉字的拼音之间用空格分隔，拼音个数必须与汉字数量一致。</li><li>每个拼音由发音部分和音调组成，其中音调为 <code>1</code> 到 <code>5</code> 的整数，<code>5</code> 表示轻声。</li></ul></td></tr></tbody></table>

<a id="示例-4"></a>

<a id="示例-4-h4"></a>

#### 示例

**ph**

<a id="code-block-31"></a>

```xml
<speak>
  去<phoneme alphabet="py" ph="dian3 dang4 hang2">典当行</phoneme>把这个玩意<phoneme alphabet="py" ph="dang4 diao4">当掉</phoneme>
</speak>

<speak>
  How to spell <phoneme alphabet="cmu" ph="S AY N">sin</phoneme>?
</speak>
```

<a id="标签关系-4"></a>

<a id="标签关系-4-h4"></a>

#### 标签关系

<phoneme> 标签内只能包含纯文本。

<a id="soundevent-插入音效"></a>

<a id="title-al9-xs8-oer"></a>

### `<soundEvent>`：插入音效

在语音中的指定位置插入音效文件（如提示音、环境音等），增强语音表达的丰富性。

<a id="code-block-32"></a>

```xml
<soundEvent src="URL"/>
```

<a id="sec-tabs-9"></a>

<a id="属性-5"></a>

<a id="属性-5-h4"></a>

#### 属性

<table><thead><tr><th><p><strong>属性名称</strong></p></th><th><p><strong>属性类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p><code>src</code></p></td><td><p>String</p></td><td><p>是</p></td><td><p>指定外部音频文件的 URL。</p><p>音频文件需存储在阿里云 OSS 上，并可通过外网 URL 访问，上传方法请参见<a href="https://help.aliyun.com/zh/oss/user-guide/console-quick-start">上传文件</a>。私有文件可使用有效的签名 URL。URL 中的 XML 特殊字符须转义，例如将 <code>&amp;</code> 写为 <code>&amp;amp;</code>。</p><ul><li><p>音频要求：</p><ul><li><p>采样率：16kHz</p></li><li><p>声道数：单声道</p></li><li><p>文件格式：WAV</p><p>若原始音频非 WAV 格式，可使用 <code>ffmpeg</code> 工具进行转换：</p><a id="code-block-33"></a><pre class="language-bash"><code>ffmpeg -i 输入音频 -acodec pcm_s16le -ac 1 -ar 16000 输出.wav
</code></pre></li><li><p>文件大小：不超过2MB</p></li><li><p>位深度：16位</p></li></ul></li></ul><div><div><p><strong>重要</strong>上传方应对上传音频的版权承担相应的法律责任。</p></div></div></td></tr></tbody></table>

<a id="示例-5"></a>

<a id="示例-5-h4"></a>

#### 示例

**src**

<a id="code-block-34"></a>

```xml
<speak>
  一匹马受了惊吓<soundEvent src="https://nls.alicdn.com/sound-event/horse-neigh.wav"/>人们四散躲避
</speak>
```

<a id="标签关系-5"></a>

<a id="标签关系-5-h4"></a>

#### 标签关系

<soundEvent> 是自闭合标签，不能包含任何子标签。

<a id="say-as-设置读法"></a>

<a id="title-xt2-m52-1uk"></a>

### `<say-as>`：设置读法

指定文本的内容类型（如数字、日期、电话号码等），系统将按照对应类型的规范读法进行朗读。

<a id="code-block-35"></a>

```xml
<say-as interpret-as="string">文本</say-as>
```

<a id="sec-tabs-10"></a>

<a id="属性-6"></a>

<a id="属性-6-h4"></a>

#### 属性

<table><thead><tr><th><p><strong>属性名称</strong></p></th><th><p><strong>属性类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p><code>interpret-as</code></p></td><td><p>String</p></td><td><p>是</p></td><td><p>指定标签内文本的内容类型。</p><p>取值范围：</p><ul><li>cardinal：按整数或小数的标准读法朗读</li><li>digits：按数字逐个读出（如：123 → 一二三）</li><li>telephone：按电话号码的标准方式逐位读出</li><li>name：按人名的标准读法朗读</li><li>address：按地址的标准方式朗读</li><li>id：按标识符（如账户名、昵称）的标准方式朗读</li><li>characters：逐字符朗读标签内的文本</li><li>punctuation：将标签内的标点符号读出名称</li><li>date：按日期格式的标准读法朗读</li><li>time：按时间格式的标准方式朗读</li><li>currency：按货币金额的标准读法朗读</li><li>measure：按计量单位的标准方式朗读</li></ul></td></tr></tbody></table>

<a id="accordion-点击查看-say-as-支持范围"></a>

点击查看 say-as 支持范围

**cardinal**

<a id="sec-tabs-11"></a>

<a id="中文"></a>

<a id="中文-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>数字串</p></td><td><p>145</p></td><td><p>一百四十五</p></td><td rowspan="8"><p>整数输入范围：20位以内的正负整数，[-99999999999999999999,99999999999999999999]。 小数输入范围：对小数点后小数的位数没有特殊限制，建议不超过10位。</p></td></tr><tr><td><p>负号+数字串</p></td><td><p>-145</p></td><td><p>负一百四十五</p></td></tr><tr><td><p>以逗号分隔3位数字串</p></td><td><p>10,000</p></td><td><p>一万</p></td></tr><tr><td><p>负号+以逗号分隔3位数字串</p></td><td><p>-10,124</p></td><td><p>负一万一百二十四</p></td></tr><tr><td><p>数字串+小数点+2个零</p></td><td><p>10.00</p></td><td><p>十</p></td></tr><tr><td><p>负号+数字串+小数点+2个零</p></td><td><p>-110.00</p></td><td><p>负一百一十</p></td></tr><tr><td><p>数字串+小数点+数字串</p></td><td><p>79.090</p></td><td><p>七十九点零九零</p></td></tr><tr><td><p>负号+数字串+小数点+数字串</p></td><td><p>-79.001</p></td><td><p>负七十九点零零一</p></td></tr></tbody></table>

<a id="英文"></a>

<a id="英文-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>数字串</p></td><td><p>145</p></td><td><p>one hundred forty five</p></td><td rowspan="11"><p>整数输入范围：13位以内的正负整数，[-999999999999,999999999999]。</p><p>小数输入范围：对小数点后小数的位数没有特殊限制，建议不超过10位。</p></td></tr><tr><td><p>以零开头的数字串</p></td><td><p>0145</p></td><td><p>one hundred forty five</p></td></tr><tr><td><p>负号+数字串</p></td><td><p>-145</p></td><td><p>minus hundred forty five</p></td></tr><tr><td><p>以逗号分隔三位数字串</p></td><td><p>60,000</p></td><td><p>sixty thousand</p></td></tr><tr><td><p>负号+以逗号分隔三位数字串</p></td><td><p>-208,000</p></td><td><p>minus two hundred eight thousand</p></td></tr><tr><td><p>数字串+小数点+零</p></td><td><p>12.00</p></td><td><p>twelve</p></td></tr><tr><td><p>数字串+小数点+数字串</p></td><td><p>12.34</p></td><td><p>twelve point three four</p></td></tr><tr><td><p>以逗号分隔三位数字串+小数点+数字串</p></td><td><p>1,000.1</p></td><td><p>one thousand point one</p></td></tr><tr><td><p>负号+数字串+小数点+数字串</p></td><td><p>-12.34</p></td><td><p>minus twelve point three four</p></td></tr><tr><td><p>负号+以逗号分隔三位数字串+小数点+数字串</p></td><td><p>-1,000.1</p></td><td><p>minus one thousand point one</p></td></tr><tr><td><p>（以逗号分隔三位）数字串+连词符+（以逗号分隔三位）数字</p></td><td><p>1-1,000</p></td><td><p>one to one thousand</p></td></tr><tr><td rowspan="8"><p>其他默认读法</p></td><td><p>012.34</p></td><td><p>twelve point three four</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>1/2</p></td><td><p>one half</p></td></tr><tr><td><p>-3/4</p></td><td><p>minus three quarters</p></td></tr><tr><td><p>5.1/6</p></td><td><p>five point one over six</p></td></tr><tr><td><p>-3 1/2</p></td><td><p>minus three and a half</p></td></tr><tr><td><p>1,000.3^3</p></td><td><p>one thousand point three to the power of three</p></td></tr><tr><td><p>3e9.1</p></td><td><p>three times ten to the power of nine point one</p></td></tr><tr><td><p>23.10%</p></td><td><p>twenty three point one percent</p></td></tr></tbody></table>

**digits**

<a id="sec-tabs-12"></a>

<a id="中文-2"></a>

<a id="中文-2-h4"></a>

#### 中文

| 格式 | 示例 | 中文输出 | 说明 |
| --- | --- | --- | --- |
| 数字串 | 129090909 | 一二九零九零九零九 | 对数字串的长度没有特殊限制，建议不超过20位。 当数字串超过10位时，每个数字后插入停顿。 |

<a id="英文-2"></a>

<a id="英文-2-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>数字串</p></td><td><p>12034</p></td><td><p>one two zero three four</p></td><td rowspan="2"><p>对数字串的长度没有特殊限制，建议不超过20位。</p><p>当数字串以空格或连词符分组时，分组之间会插入逗号而产生适当停顿，支持最长5个分组。</p></td></tr><tr><td><p>数字串+空格或连词符+数字串+空格或连词符+数字串+空格或连词符+数字串</p></td><td><p>1-23-456 7890</p></td><td><p>one, two three, four five six, seven eight nine zero</p></td></tr></tbody></table>

**telephone**

<a id="sec-tabs-13"></a>

<a id="中文-3"></a>

<a id="中文-3-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="6"><p>座机号</p></td><td><p>4930286</p></td><td><p>四九三 零二八六</p></td><td rowspan="6"><p>支持7~8位座机号，支持空格和“-”作为分隔符。 其中，7位座机号支持“3-4”的数字分隔方式；8位座机号支持“4-4”的数字分隔方式。</p></td></tr><tr><td><p>493 0286</p></td><td><p>四九三 零二八六</p></td></tr><tr><td><p>493-0286</p></td><td><p>四九三 零二八六</p></td></tr><tr><td><p>62552560</p></td><td><p>六二五五 二五六零</p></td></tr><tr><td><p>6255 2560</p></td><td><p>六二五五 二五六零</p></td></tr><tr><td><p>6255-2560</p></td><td><p>六二五五 二五六零</p></td></tr><tr><td rowspan="4"><p>座机号+分机号</p></td><td><p>4930286-109</p></td><td><p>四九三 零二八六 转幺零九</p></td><td rowspan="4"><p>支持1~4位分机号。</p></td></tr><tr><td><p>4930286转109</p></td><td><p>四九三 零二八六 转幺零九</p></td></tr><tr><td><p>4930286分机109</p></td><td><p>四九三 零二八六 分机幺零九</p></td></tr><tr><td><p>4930286分机号109</p></td><td><p>四九三 零二八六 分机号幺零九</p></td></tr><tr><td rowspan="9"><p>区号+座机号</p></td><td><p>01062552560</p></td><td><p>零幺零 六二五五 二五六零</p></td><td rowspan="9"><p>支持区号：010、02x、03xx、04xx、05xx、07xx、08xx、09xx。</p></td></tr><tr><td><p>010 62552560</p></td><td><p>零幺零 六二五五 二五六零</p></td></tr><tr><td><p>010 6255 2560</p></td><td><p>零幺零 六二五五 二五六零</p></td></tr><tr><td><p>010 6255-2560</p></td><td><p>零幺零 六二五五 二五六零</p></td></tr><tr><td><p>010-62552560</p></td><td><p>零幺零 六二五五 二五六零</p></td></tr><tr><td><p>010-6255-2560</p></td><td><p>零幺零 六二五五 二五六零</p></td></tr><tr><td><p>(010)62552560</p></td><td><p>零幺零 六二五五 二五六零</p></td></tr><tr><td><p>03198907098</p></td><td><p>零三幺九 八九零 七零九八</p></td></tr><tr><td><p>0319-8907098</p></td><td><p>三幺九 八九零 七零九八</p></td></tr><tr><td rowspan="6"><p>区号+座机号+分机号</p></td><td><p>010 62552560-109</p></td><td><p>零幺零 六二五五 二五六零 转幺零九</p></td><td rowspan="6"><p>无</p></td></tr><tr><td><p>010-62552560-109</p></td><td><p>零幺零 六二五五 二五六零 转幺零九</p></td></tr><tr><td><p>(010)62552560-109</p></td><td><p>零幺零 六二五五 二五六零 转幺零九</p></td></tr><tr><td><p>(010)62552560转109</p></td><td><p>零幺零 六二五五 二五六零 转幺零九</p></td></tr><tr><td><p>(010)62552560分机109</p></td><td><p>零幺零 六二五五 二五六零 分机幺零九</p></td></tr><tr><td><p>(010)62552560分机号109</p></td><td><p>零幺零 六二五五 二五六零 分机号幺零九</p></td></tr><tr><td rowspan="5"><p>国家代码+区号+座机号</p></td><td><p>86-010-62791627</p></td><td><p>八六 零幺零 六二七九 幺六二七</p></td><td rowspan="5"><p>支持国家代码：86、 (86)、+86、(+86)、0086。并统一读为“八六”。</p></td></tr><tr><td><p>(86)10-62791627</p></td><td><p>八六 幺零 六二七九 幺六二七</p></td></tr><tr><td><p>+86-010-62791627</p></td><td><p>八六 零幺零 六二七九 幺六二七</p></td></tr><tr><td><p>0086-10-62791627</p></td><td><p>八六 幺零 六二七九 幺六二七</p></td></tr><tr><td><p>(+86)-10-6279 1627</p></td><td><p>八六 幺零 六二七九 幺六二七</p></td></tr><tr><td rowspan="5"><p>国家代码+区号+座机号+分机号</p></td><td><p>(86)21-58118818-207</p></td><td><p>八六 二幺 五八幺幺 八八幺八 转二零七</p></td><td rowspan="5"><p>无</p></td></tr><tr><td><p>(86)021-5811-8818-207</p></td><td><p>八六 零二幺 五八幺幺 八八幺八 转二零七</p></td></tr><tr><td><p>(86)021-58118818转207</p></td><td><p>八六 零二幺 五八幺幺 八八幺八 转二零七</p></td></tr><tr><td><p>(86)21-5811-8818分机207</p></td><td><p>八六 二幺 五八幺幺 八八幺八 分机二零七</p></td></tr><tr><td><p>+86-021-58118818分机号207</p></td><td><p>八六 零二幺 五八幺幺 八八幺八分机号二零七</p></td></tr><tr><td rowspan="3"><p>手机号</p></td><td><p>139 0000 5678</p></td><td><p>幺三九 零零零零 五六七八</p></td><td rowspan="3"><p>支持11位手机号，支持3-3-5、3-4-4两种数字分隔方式</p></td></tr><tr><td><p>139-000-05678</p></td><td><p>幺三九 零零零 零五六七八</p></td></tr><tr><td><p>139 000 05678</p></td><td><p>幺三九 零零零 零五六七八</p></td></tr><tr><td rowspan="4"><p>国家代码+手机号</p></td><td><p>+86-13900005678</p></td><td><p>八六 幺三九 零零零零 五六七八</p></td><td rowspan="4"><p>无</p></td></tr><tr><td><p>(+86)-139-0000-5678</p></td><td><p>八六 幺三九 零零零零 五六七八</p></td></tr><tr><td><p>+8613900005678</p></td><td><p>八六 幺三九 零零零零 五六七八</p></td></tr><tr><td><p>0086-139 000 05678</p></td><td><p>八六 幺三九 零零零 零五六七八</p></td></tr><tr><td rowspan="5"><p>服务号</p></td><td><p>123</p></td><td><p>幺二三</p></td><td rowspan="5"><p>支持常用的服务号。 支持以400/800开头的10位服务号，支持以“3-3-4”的数字分隔方式。 支持以12530/17951/12593开头的16位号码。</p></td></tr><tr><td><p>95678</p></td><td><p>九五六七八</p></td></tr><tr><td><p>4008110510</p></td><td><p>四零零 八幺幺 零五幺零</p></td></tr><tr><td><p>800-810-8888</p></td><td><p>八零零 八幺零 八八八八</p></td></tr><tr><td><p>1253013520638377</p></td><td><p>幺二五三零 幺三五 二零六三 八三七七</p></td></tr><tr><td><p>其他</p></td><td><p>(86)(21)9899-80800-0909</p></td><td><p>八六 二幺 九八九九 八零八零零 零九零九</p></td><td><p>支持“数字串+分隔符（左右括号、-）”方式。</p></td></tr></tbody></table>

<a id="英文-3"></a>

<a id="英文-3-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>数字串</p></td><td><p>12034</p></td><td><p>one two oh three four</p></td><td rowspan="4"><p>对数字串的长度没有特殊限制，建议不超过20位。当数字串以空格或连词符分组时，分组之间会插入逗号而产生适当停顿，支持最长5个分组。</p></td></tr><tr><td><p>数字串+空格或连词符+数字串+空格或连词符+数字串</p></td><td><p>1-23-456 7890</p></td><td><p>one, two three, four five six, seven eight nine oh</p></td></tr><tr><td><p>加号+数字串+空格或连词符+数字串</p></td><td><p>+43-211-0567</p></td><td><p>plus four three, two one one, oh five six seven</p></td></tr><tr><td><p>左括号+数字串+右括号+空格+数字串+空格或连词符+数字串</p></td><td><p>(21) 654-3210</p></td><td><p>(two one) six five four, three two one oh</p></td></tr></tbody></table>

**address**

<a id="sec-tabs-14"></a>

<a id="中文-4"></a>

<a id="中文-4-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="6"><p>常用地址格式</p></td><td><p>元和镇嘉元30-9</p></td><td><p>元和镇嘉元三十杠九</p></td><td rowspan="6"><p>支持常用地址格式。此处地址指标准的邮寄地址。</p></td></tr><tr><td><p>市台路388弄1107-1108号</p></td><td><p>市台路三八八弄幺幺零七杠幺幺零八号</p></td></tr><tr><td><p>华润二十四城六期锦云府3-1-3205</p></td><td><p>华润二十四城六期锦云府三杠一杠三二零五</p></td></tr><tr><td><p>圣华名都大厦2幢2006室</p></td><td><p>圣华名都大厦二幢二零零六室</p></td></tr><tr><td><p>五常街道庭院5幢4单元201</p></td><td><p>五常街道庭院五幢四单元二零幺</p></td></tr><tr><td><p>芙蓉江路150弄19号</p></td><td><p>芙蓉江路幺五零弄十九号</p></td></tr></tbody></table>

<a id="英文-4"></a>

<a id="英文-4-h4"></a>

#### 英文

英文文本不支持此类型。

**id**

<a id="sec-tabs-15"></a>

<a id="中文-5"></a>

<a id="中文-5-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>字符串</p></td><td><p>dell0101</p></td><td><p>D E L L 零 一 零 一</p></td><td rowspan="3"><p>大小写英文字符、阿拉伯数字0~9、下划线。 输出的空格表示每个字符之间插入停顿，即字符一个一个地读。</p></td></tr><tr><td><p>myid_1998</p></td><td><p>M Y I D 下划线 一 九 九 八</p></td></tr><tr><td><p>AiTest</p></td><td><p>A I T E S T</p></td></tr></tbody></table>

<a id="英文-5"></a>

<a id="英文-5-h4"></a>

#### 英文

英文文本中，此类型与 `characters` 的作用相同。

**characters**

<a id="sec-tabs-16"></a>

<a id="中文-6"></a>

<a id="中文-6-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="9"><p>字符串</p></td><td><p>ISBN 1-001-099098-1</p></td><td><p>I S B N 一 杠 零 零 一 杠 零 九 九 零 九 八 杠 一</p></td><td rowspan="9"><p>支持中文汉字、大小写英文字符、阿拉伯数字0~9以及部分全角和半角字符。 输出的空格表示每个字符之间插入停顿，即字符一个一个地读。标签内的文本如果包含XML的特殊字符，需要做字符转义。</p></td></tr><tr><td><p>x10b2345_u</p></td><td><p>x 一 零 b 二 三 四 五 下划线 u</p></td></tr><tr><td><p>v1.0.1</p></td><td><p>v 一 点 零 点 一</p></td></tr><tr><td><p>版本号2.0</p></td><td><p>版本号二 点 零</p></td></tr><tr><td><p>苏M MA000</p></td><td><p>苏M M A 零 零 零</p></td></tr><tr><td><p>空中客车A330</p></td><td><p>空中客车A 三 三 零</p></td></tr><tr><td><p>型号s01 s02和s03</p></td><td><p>型号s 零 一 s 零二 和s 零 三</p></td></tr><tr><td><p>空中客车A330</p></td><td><p>空中客车A 三 三 零</p></td></tr><tr><td><p>αβγ</p></td><td><p>阿尔法 贝塔 伽玛</p></td></tr></tbody></table>

<a id="英文-6"></a>

<a id="英文-6-h4"></a>

#### 英文

| 格式 | 示例 | 英文输出 | 说明 |
| --- | --- | --- | --- |
| 字符串 | \*b+3$.c-0'=α | asterisk B plus three dollar dot C dash zero apostrophe equals alpha | 支持中文汉字、大小写英文字符、阿拉伯数字0~9以及部分全角和半角字符。<br><br>输出的空格表示每个字符之间插入停顿，即字符一个一个地读。<br><br>标签内的文本如果包含XML的特殊字符，需要做字符转义。 |

**punctuation**

<a id="sec-tabs-17"></a>

<a id="中文-7"></a>

<a id="中文-7-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="7"><p>标点符号</p></td><td><p>…</p></td><td><p>省略号</p></td><td rowspan="7"><p>支持常见中英文标点。输出的空格表示每个字符之间插入停顿，即字符一个一个地读。 标签内的文本如果包含XML的特殊字符，需要做字符转义。</p></td></tr><tr><td><p>……</p></td><td><p>省略号</p></td></tr><tr><td><p>!&quot;#$%&amp;</p></td><td><p>叹号 双引号 井号 dollar 百分号 and</p></td></tr><tr><td><p>‘()*+</p></td><td><p>单引号 左括号 右括号 星号 加号</p></td></tr><tr><td><p>,-./:;</p></td><td><p>逗号 杠 点 斜杠 冒号 分号</p></td></tr><tr><td><p>&lt;=&gt;?@</p></td><td><p>小于 等号 大于 问号 at</p></td></tr><tr><td><p>[\]^_</p></td><td><p>左方括号 反斜线 右方括号 脱字符 下划线</p></td></tr></tbody></table>

<a id="英文-7"></a>

<a id="英文-7-h4"></a>

#### 英文

英文文本中，此类型与 `characters` 的作用相同。

**date**

<a id="sec-tabs-18"></a>

<a id="中文-8"></a>

<a id="中文-8-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="6"><p>xx年</p></td><td><p>71年</p></td><td><p>七一年</p></td><td rowspan="6"><p>支持2位和4位年份。其中： 2位年份支持60年~99年、00年~09年、10年~19年。 4位年份支持1000年~1999年、2000年~2099年。</p></td></tr><tr><td><p>04年</p></td><td><p>零四年</p></td></tr><tr><td><p>19年</p></td><td><p>一九年</p></td></tr><tr><td><p>1011年</p></td><td><p>一零一一年</p></td></tr><tr><td><p>1998年</p></td><td><p>一九九八年</p></td></tr><tr><td><p>2008年</p></td><td><p>二零零八年</p></td></tr><tr><td rowspan="4"><p>xx年xx月</p></td><td><p>98年4月</p></td><td><p>九八年四月</p></td><td rowspan="4"><p>当月份为1到9月时，支持开头带“0”和不带“0”两种写法。例如“1908年4月”和“1908年04月”。</p></td></tr><tr><td><p>1998年04月</p></td><td><p>一九九八年四月</p></td></tr><tr><td><p>08年8月</p></td><td><p>零八年八月</p></td></tr><tr><td><p>2008年8月</p></td><td><p>二零零八年八月</p></td></tr><tr><td rowspan="4"><p>xx年xx月xx日xx年xx月xx号</p></td><td><p>98年4月23日</p></td><td><p>九八年四月二十三日</p></td><td rowspan="4"><p>当日期为1到9日时，支持开头带“0”和不带“0”两种写法。例如“1908年4月8日”和“1908年04月08日”。</p></td></tr><tr><td><p>1998年04月23日</p></td><td><p>一九九八年四月二十三日</p></td></tr><tr><td><p>08年8月8号</p></td><td><p>零八年八月八号</p></td></tr><tr><td><p>2008年08月08号</p></td><td><p>二零零八年八月八号</p></td></tr><tr><td rowspan="4"><p>xx年xx月xx日xx年xx月xx号</p></td><td><p>98年4月23日</p></td><td><p>九八年四月二十三日</p></td><td rowspan="4"><p>当日期为1到9日时，支持开头带“0”和不“0”两种写法。例如“1908年4月8日”和“1908年04月08日”。</p></td></tr><tr><td><p>1998年04月23日</p></td><td><p>一九九八年四月二十三日</p></td></tr><tr><td><p>08年8月8号</p></td><td><p>零八年八月八号</p></td></tr><tr><td><p>2008年08月08号</p></td><td><p>二零零八年八月八号</p></td></tr><tr><td rowspan="2"><p>xx月xx号</p></td><td><p>3月20日</p></td><td><p>三月二十日</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>08月07号</p></td><td><p>八月七号</p></td></tr><tr><td rowspan="3"><p>年月缩写</p></td><td><p>2018/08</p></td><td><p>二零一八年八月</p></td><td rowspan="6"><p>支持“/”、“-”、“.”作为缩写的分隔符。</p></td></tr><tr><td><p>2018-08</p></td><td><p>二零一八年八月</p></td></tr><tr><td><p>2018.08</p></td><td><p>二零一八年八月</p></td></tr><tr><td rowspan="3"><p>年月日缩写</p></td><td><p>2018/08/08</p></td><td><p>二零一八年八月八日</p></td></tr><tr><td><p>2018-8-8</p></td><td><p>二零一八年八月八日</p></td></tr><tr><td><p>2018.08.08</p></td><td><p>二零一八年八月八日</p></td></tr><tr><td rowspan="2"><p>xx年xx月xx日~xx年xx月xx日xx年xx月xx号~xx年xx月xx号</p></td><td><p>04年9月1日~30日</p></td><td><p>零四年九月一日至三十日</p></td><td rowspan="10"><p>支持“~”、“-”作为“至”的缩写标志。</p></td></tr><tr><td><p>2004年09月01号-2008年06月08号</p></td><td><p>二零零四年九月一号至二零零八年六月八号</p></td></tr><tr><td rowspan="2"><p>xx年xx月xx日~xx日xx年xx月xx号~xx号</p></td><td><p>04年9月1日~30日</p></td><td><p>零四年九月一日至三十日</p></td></tr><tr><td><p>2004年09月01号-2008年06月08号</p></td><td><p>二零零四年九月一号至二零零八年六月八号</p></td></tr><tr><td rowspan="2"><p>xx年xx月~xx年xx月</p></td><td><p>01年04月~10年04月</p></td><td><p>零一年四月至一零年四月</p></td></tr><tr><td><p>2001年04月~2010年04月</p></td><td><p>二零零一年四月至二零一零年四月</p></td></tr><tr><td rowspan="2"><p>xx月xx日~xx月xx日xx月xx号~xx月xx号</p></td><td><p>10月1日~10月7日</p></td><td><p>十月一日至十月七日</p></td></tr><tr><td><p>10月01号~10月07号</p></td><td><p>十月一号至十月七号</p></td></tr><tr><td rowspan="2"><p>xx月xx日~xx日xx月xx号~xx号</p></td><td><p>10月1日~7日</p></td><td><p>十月一日至七日</p></td></tr><tr><td><p>10月01号~07号</p></td><td><p>十月一号至七号</p></td></tr><tr><td rowspan="2"><p>年月日缩写~年月日缩写</p></td><td><p>2018/03/03~2019/01/01</p></td><td><p>二零一八年三月三日至二零一九年一月一日</p></td><td rowspan="5"><p>支持“/”、“.”作为缩写的分隔符，支持“~”、“-”作为“至”的缩写标志。</p></td></tr><tr><td><p>1997.9.9~1998.9.9</p></td><td><p>一九九七年九月九日至一九九八年九月九日</p></td></tr><tr><td><p>月日缩写~月日缩写</p></td><td><p>10/20~10/31</p></td><td><p>十月二十日至十月三十一日</p></td></tr><tr><td rowspan="2"><p>xx~xx月xx月~xx月</p></td><td><p>1~10月</p></td><td><p>一至十月</p></td></tr><tr><td><p>1月~10月</p></td><td><p>一月至十月</p></td></tr><tr><td><p>月日年缩写</p></td><td><p>10/20/2018</p></td><td><p>二零一八年十月二十日</p></td><td><p>仅支持4位的年份，仅支持“/”作为日期的分隔符，仅支持“月/日/年”的书写方式。</p></td></tr></tbody></table>

<a id="英文-8"></a>

<a id="英文-8-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="6"><p>四位数字/两位数字或四位数字-两位数字</p></td><td><p>2000/01</p></td><td><p>two thousand, oh one</p></td><td rowspan="6"><p>跨年度。</p></td></tr><tr><td><p>1900-01</p></td><td><p>nineteen hundred, oh one</p></td></tr><tr><td><p>2001-02</p></td><td><p>twenty oh one, oh two</p></td></tr><tr><td><p>2019-20</p></td><td><p>twenty nineteen, twenty</p></td></tr><tr><td><p>1998-99</p></td><td><p>nineteen ninety eight, ninety nine</p></td></tr><tr><td><p>1999-00</p></td><td><p>nineteen ninety nine, oh oh</p></td></tr><tr><td rowspan="4"><p>以1或2开头的四位数字</p></td><td><p>2000</p></td><td><p>two thousand</p></td><td rowspan="4"><p>四位数字年份。</p></td></tr><tr><td><p>1900</p></td><td><p>nineteen hundred</p></td></tr><tr><td><p>1905</p></td><td><p>nineteen oh five</p></td></tr><tr><td><p>2021</p></td><td><p>twenty twenty one</p></td></tr><tr><td rowspan="3"><p>星期几-星期几</p><p>或</p><p>星期几~星期几</p><p>或</p><p>星期几&amp;星期几</p></td><td><p>mon-wed</p></td><td><p>monday to wednesday</p></td><td rowspan="3"><p>星期几的范围标签内的文本如果包含XML的特殊字符，需要做字符转义。</p></td></tr><tr><td><p>tue~fri</p></td><td><p>tuesday to friday</p></td></tr><tr><td><p>sat&amp;sun</p></td><td><p>saturday and sunday</p></td></tr><tr><td rowspan="3"><p>DD-DD MMM, YYYY</p><p>或</p><p>DD~DD MMM, YYYY</p><p>或</p><p>DD&amp;DD MMM, YYYY</p></td><td><p>19-20 Jan, 2000</p></td><td><p>the nineteen to the twentieth of january two thousand</p></td><td rowspan="3"><p>DD表示两位数字日期，MMM表示月份的三字母缩写或完整单词，YYYY表示以1或2开头的四位数字年份。</p></td></tr><tr><td><p>01 ~ 10 Jul, 2020</p></td><td><p>the first to the tenth of july twenty twenty</p></td></tr><tr><td><p>05&amp;06 Apr, 2009</p></td><td><p>the fifth and the sixth of april two thousand nine</p></td></tr><tr><td rowspan="3"><p>MMM DD-DD</p><p>或</p><p>MMM DD~DD</p><p>或</p><p>MMM DD&amp;DD</p></td><td><p>Feb 01 - 03</p></td><td><p>feburary the first to the third</p></td><td rowspan="3"><p>MMM表示月份的三字母缩写或完整单词，DD表示两位数字日期。</p></td></tr><tr><td><p>Aug 10~20</p></td><td><p>august the tenth to the twentieth</p></td></tr><tr><td><p>Dec 11&amp;12</p></td><td><p>december the eleventh and the twelfth</p></td></tr><tr><td rowspan="3"><p>MMM-MMM</p><p>或</p><p>MMM~MMM</p><p>或</p><p>MMM&amp;MMM</p></td><td><p>Jan-Jun</p></td><td><p>january to june</p></td><td rowspan="3"><p>MMM表示月份的三字母缩写或完整单词。</p></td></tr><tr><td><p>jul ~ dec</p></td><td><p>july to december</p></td></tr><tr><td><p>sep&amp;oct</p></td><td><p>september and october</p></td></tr><tr><td rowspan="2"><p>YYYY-YYYY</p><p>或</p><p>YYYY~YYYY</p></td><td><p>1990 - 2000</p></td><td><p>nineteen ninety to two thousand</p></td><td rowspan="2"><p>YYYY表示以1或2开头的四位数字年份。</p></td></tr><tr><td><p>2001~2021</p></td><td><p>two thousand one to twenty twenty one</p></td></tr><tr><td><p>WWW DD MMM YYYY</p></td><td><p>Sun 20 Nov 2011</p></td><td><p>sunday the twentieth of november twenty eleven</p></td><td rowspan="9"><p>WWW表示星期几的三字母缩写或完整单词，DD表示两位数字日期，MMM表示月份的三字母缩写或完整单词，MM表示两位数字月份（或三字母缩写或完整单词），YYYY表示以1或2开头的四位数字年份。</p></td></tr><tr><td><p>WWW DD MMM</p></td><td><p>Sun 20 Nov</p></td><td><p>sunday the twentieth of november</p></td></tr><tr><td><p>WWW MMM DD YYYY</p></td><td><p>Sun Nov 20 2011</p></td><td><p>sunday november the twentieth twenty eleven</p></td></tr><tr><td><p>WWW MMM DD</p></td><td><p>Sun Nov 20</p></td><td><p>sunday november the twentieth</p></td></tr><tr><td><p>WWW YYYY-MM-DD</p></td><td><p>Sat 2010-10-01</p></td><td><p>aturday october the first twenty ten</p></td></tr><tr><td><p>WWW YYYY/MM/DD</p></td><td><p>Sat 2010/10/01</p></td><td><p>saturday october the first twenty ten</p></td></tr><tr><td><p>WWW MM/DD/YYYY</p></td><td><p>Sun 11/20/2011</p></td><td><p>sunday november the twentieth twenty eleven</p></td></tr><tr><td><p>MM/DD/YYYY</p></td><td><p>11/20/2011</p></td><td><p>november the twentieth twenty eleven</p></td></tr><tr><td><p>YYYY</p></td><td><p>1998</p></td><td><p>nineteen ninety eight</p></td></tr><tr><td rowspan="12"><p>其他默认读法</p></td><td><p>10 Mar, 2001</p></td><td><p>the tenth of march two thousand one</p></td><td rowspan="12"><p>无</p></td></tr><tr><td><p>10 Mar</p></td><td><p>the tenth of march</p></td></tr><tr><td><p>Mar 2001</p></td><td><p>march two thousand one</p></td></tr><tr><td><p>Fri. 10/Mar/2001</p></td><td><p>friday the tenth of march two thousand one</p></td></tr><tr><td><p>Mar 10th, 2001</p></td><td><p>march the tenth two thousand one</p></td></tr><tr><td><p>Mar 10</p></td><td><p>march the tenth</p></td></tr><tr><td><p>2001/03/10</p></td><td><p>march the tenth two thousand one</p></td></tr><tr><td><p>2001-03-10</p></td><td><p>march the tenth two thousand one</p></td></tr><tr><td><p>2000s</p></td><td><p>two thousands</p></td></tr><tr><td><p>2010's</p></td><td><p>twenty tens</p></td></tr><tr><td><p>1900's</p></td><td><p>nineteen hundreds</p></td></tr><tr><td><p>1990s</p></td><td><p>nineteen nineties</p></td></tr></tbody></table>

**time**

<a id="sec-tabs-19"></a>

<a id="中文-9"></a>

<a id="中文-9-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>时刻</p></td><td><p>12:00</p></td><td><p>十二点</p></td><td rowspan="32"><p>支持常用时间和时间范围格式。</p></td></tr><tr><td><p>12:00:00点</p></td><td><p>十二点</p></td></tr><tr><td><p>10:20分</p></td><td><p>十点二十分</p></td></tr><tr><td><p>10:20:30</p></td><td><p>十点二十分三十秒</p></td></tr><tr><td><p>09:18:14</p></td><td><p>九点十八分十四秒</p></td></tr><tr><td rowspan="9"><p>时刻~时刻</p></td><td><p>11:00~12:00</p></td><td><p>十一点到十二点</p></td></tr><tr><td><p>09:00-14:00</p></td><td><p>九点到十四点</p></td></tr><tr><td><p>11:00~11:30</p></td><td><p>十一点到十一点三十分</p></td></tr><tr><td><p>11:00-12:18</p></td><td><p>十一点到十二点十八分</p></td></tr><tr><td><p>10:30~11:00</p></td><td><p>十点三十分到十一点</p></td></tr><tr><td><p>09:28-10:00</p></td><td><p>九点二十八分到十点</p></td></tr><tr><td><p>10:20~11:20</p></td><td><p>十点二十分到十一点二十分</p></td></tr><tr><td><p>06:00~08:00</p></td><td><p>六点到八点</p></td></tr><tr><td><p>上午10:20~下午13:30</p></td><td><p>上午十点二十分到下午十三点三十分</p></td></tr><tr><td rowspan="18"><p>时间缩写</p></td><td><p>5:00 am</p></td><td><p>凌晨五点整</p></td></tr><tr><td><p>5:30 am</p></td><td><p>凌晨五点半</p></td></tr><tr><td><p>5:20:12 am</p></td><td><p>凌晨五点二十分十二秒</p></td></tr><tr><td><p>7:00 am</p></td><td><p>上午七点整</p></td></tr><tr><td><p>7:30 AM</p></td><td><p>上午七点半</p></td></tr><tr><td><p>7:20:12 a.m.</p></td><td><p>上午七点二十分十二秒</p></td></tr><tr><td><p>07:08:12 A.M.</p></td><td><p>上午七点零八分十二秒</p></td></tr><tr><td><p>5:00 pm</p></td><td><p>下午五点整</p></td></tr><tr><td><p>5:30 PM</p></td><td><p>下午五点半</p></td></tr><tr><td><p>5:20:12 p.m.</p></td><td><p>下午五点二十分十二秒</p></td></tr><tr><td><p>05:09:12 P.M.</p></td><td><p>下午五点零九分十二秒</p></td></tr><tr><td><p>9:00 pm</p></td><td><p>晚上九点整</p></td></tr><tr><td><p>9:30 pm</p></td><td><p>晚上九点半</p></td></tr><tr><td><p>9:20:12 PM</p></td><td><p>晚上九点二十分十二秒</p></td></tr><tr><td><p>9:02:12 P.M.</p></td><td><p>晚上九点零二分十二秒</p></td></tr><tr><td><p>12:00 pm</p></td><td><p>中午十二点整</p></td></tr><tr><td><p>12:30 p.m.</p></td><td><p>中午十二点半</p></td></tr><tr><td><p>12:20:12 PM</p></td><td><p>中午十二点二十分十二秒</p></td></tr></tbody></table>

<a id="英文-9"></a>

<a id="英文-9-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>HH:MM AM或PM</p></td><td><p>09:00 AM</p></td><td><p>nine A M</p></td><td rowspan="5"><p>HH表示一或两位数字小时，MM表示两位数字分钟，AM/PM表示上/下午。</p></td></tr><tr><td><p>09:03 PM</p></td><td><p>nine oh three P M</p></td></tr><tr><td><p>09:13 p.m.</p></td><td><p>nine thirteen p m</p></td></tr><tr><td><p>HH:MM</p></td><td><p>21:00</p></td><td><p>twenty one hundred</p></td></tr><tr><td><p>HHMM</p></td><td><p>100</p></td><td><p>one oclock</p></td></tr><tr><td rowspan="3"><p>时刻-时刻</p></td><td><p>8:00 am - 05:30 pm</p></td><td><p>eight a m to five p m</p></td><td rowspan="3"><p>支持常见时间格式和范围。</p></td></tr><tr><td><p>7:05~10:15 AM</p></td><td><p>seven oh five to ten fifteen A M</p></td></tr><tr><td><p>09:00-13:00</p></td><td><p>nine oclock to thirteen hundred</p></td></tr></tbody></table>

**currency**

<a id="sec-tabs-20"></a>

<a id="中文-10"></a>

<a id="中文-10-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>数字+金额标识符</p></td><td><p>12.00 RMB</p></td><td><p>十二人民币</p></td><td rowspan="5"><p>支持AUD（澳元） 、CAD（加元）、 HKD（港币）、JPY（日元）、USD（美元）、CHF（瑞士法郎）、NOK（挪威克朗）、SEK（瑞典克朗）、GBP（英镑）、 RMB（人民币）、CNY（元）和EUR（欧元）。 支持的数字格式包括：整数、小数以及以逗号分隔的国际写法。</p></td></tr><tr><td><p>12.50 RMB</p></td><td><p>十二点五零人民币</p></td></tr><tr><td><p>12,000,000 RMB</p></td><td><p>一千二百万人民币</p></td></tr><tr><td><p>12,000,000.00 RMB</p></td><td><p>一千二百万人民币</p></td></tr><tr><td><p>12,000.35 RMB</p></td><td><p>一万两千点三五人民币</p></td></tr><tr><td rowspan="6"><p>金额标识符+数字</p></td><td><p>$12</p></td><td><p>十二美元</p></td><td rowspan="6"><p>支持 CAD（加元）、 $（美元）、Fr（法郎）、kr（丹麦克朗）、 £（英镑）、¥（元）和 €（欧元）。 支持的数字格式包括：整数、小数以及以逗号分隔的国际写法。</p></td></tr><tr><td><p>$12.00</p></td><td><p>十二美元</p></td></tr><tr><td><p>$12.12</p></td><td><p>二点一二美元</p></td></tr><tr><td><p>$12,000</p></td><td><p>一万两千美元</p></td></tr><tr><td><p>$12,000.00</p></td><td><p>一万两千美元</p></td></tr><tr><td><p>$12,000.99</p></td><td><p>一万两千点九九美元</p></td></tr><tr><td rowspan="8"><p>其他默认读法</p></td><td><p>1213</p></td><td><p>一千二百一十三</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>1213 KML</p></td><td><p>一千二百一十三K M L</p></td></tr><tr><td><p>1213.00 KML</p></td><td><p>一千二百一十三K M L</p></td></tr><tr><td><p>1213.9 KML</p></td><td><p>一千二百一十三点九K M L</p></td></tr><tr><td><p>1,000 KML</p></td><td><p>一千K M L</p></td></tr><tr><td><p>1,000.00 KML</p></td><td><p>一千K M L</p></td></tr><tr><td><p>1,000.98 KML</p></td><td><p>一千点九八K M L</p></td></tr><tr><td><p>12,000</p></td><td><p>一万两千</p></td></tr></tbody></table>

<a id="英文-10"></a>

<a id="英文-10-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="7"><p>数字+金额识别符</p></td><td><p>1.00 RMB</p></td><td><p>one yuan</p></td><td rowspan="7"><p>支持的数字格式：整数、小数以及以逗号分隔的国际写法。</p><p>支持的金额识别符：</p><p>CN¥ (yuan)</p><p>CNY (yuan)</p><p>RMB (yuan)</p><p>AUD (australian dollar)</p><p>CAD (canadian dollar)</p><p>CHF (swiss franc)</p><p>DKK (danish krone)</p><p>EUR (euro)</p><p>GBP (british pound)</p><p>HKD (Hong Kong(China) dollar)</p><p>JPY (japanese yen)</p><p>NOK (norwegian krone)</p><p>SEK (swedish krona)</p><p>SGD (singapore dollar)</p><p>USD (united states dollar)</p></td></tr><tr><td><p>2.02 CNY</p></td><td><p>two point zero two yuan</p></td></tr><tr><td><p>1,000.23 CN¥</p></td><td><p>one thousand point two three yuan</p></td></tr><tr><td><p>1.01 SGD</p></td><td><p>one singapore dollar and one cent</p></td></tr><tr><td><p>2.01 CAD</p></td><td><p>two canadian dollars and one cent</p></td></tr><tr><td><p>3.1 HKD</p></td><td><p>three hong kong dollars and ten cents</p></td></tr><tr><td><p>1,000.00 EUR</p></td><td><p>one thousand euros</p></td></tr><tr><td rowspan="6"><p>金额识别符+数字</p></td><td><p>US$ 1.00</p></td><td><p>one US dollar</p></td><td rowspan="6"><p>支持的数字格式：整数、小数以及以逗号分隔的国际写法。</p><p>支持的金额识别符：</p><p>US$ (US dollar)</p><p>CA$ (Canadian dollar)</p><p>AU$ (Australian dollar)</p><p>SG$ (Singapore dollar)</p><p>HK$ (Hong Kong dollar)</p><p>C$ (Canadian dollar)</p><p>A$ (Australian dollar)</p><p>$ (dollar)</p><p>£ (pound)</p><p>€ (euro)</p><p>CN¥ (yuan)</p><p>CNY (yuan)</p><p>RMB (yuan)</p><p>AUD (australian dollar)</p><p>CAD (canadian dollar)</p><p>CHF (swiss franc)</p><p>DKK (danish krone)</p><p>EUR (euro)</p><p>GBP (british pound)</p><p>HKD (Hong Kong(China) dollar)</p><p>JPY (japanese yen)</p><p>NOK (norwegian krone)</p><p>SEK (swedish krona)</p><p>SGD (singapore dollar)</p><p>USD (united states dollar)</p></td></tr><tr><td><p>$0.01</p></td><td><p>one cent</p></td></tr><tr><td><p>JPY 1.01</p></td><td><p>one japanese yen and one sen</p></td></tr><tr><td><p>£1.1</p></td><td><p>one pound and ten pence</p></td></tr><tr><td><p>€2.01</p></td><td><p>two euros and one cent</p></td></tr><tr><td><p>USD 1,000</p></td><td><p>one thousand united states dollars</p></td></tr><tr><td rowspan="2"><p>数字+量词+金额识别符</p><p>或</p><p>金额识别符+数字+量词</p></td><td><p>1.23 Tn RMB</p></td><td><p>one point two three trillion yuan</p></td><td rowspan="2"><p>支持的量词格式包括：</p><p>thousand</p><p>million</p><p>billion</p><p>trillion</p><p>Mil (million)</p><p>mil (million)</p><p>Bil (billion)</p><p>bil (billion)</p><p>MM (million)</p><p>Bn (billion)</p><p>bn (billion)</p><p>Tn (trillion)</p><p>tn (trillion)</p><p>K(thousand)</p><p>k (thousand)</p><p>M (million)</p><p>m (million)</p></td></tr><tr><td><p>$1.2 K</p></td><td><p>one point two thousand dollars</p></td></tr></tbody></table>

**measure**

<a id="sec-tabs-21"></a>

<a id="中文-11"></a>

<a id="中文-11-h4"></a>

#### 中文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>中文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="7"><p>数字+中文单位</p></td><td><p>2片</p></td><td><p>两片</p></td><td rowspan="21"><p>支持常见中文单位及单位缩写。</p></td></tr><tr><td><p>120公顷</p></td><td><p>一百二十公顷</p></td></tr><tr><td><p>100多毫克</p></td><td><p>一百多毫克</p></td></tr><tr><td><p>100来米</p></td><td><p>一百来米</p></td></tr><tr><td><p>100余人</p></td><td><p>一百余人</p></td></tr><tr><td><p>1厘米20毫米</p></td><td><p>一厘米二十毫米</p></td></tr><tr><td><p>120.00平方公里</p></td><td><p>一百二十平方公里</p></td></tr><tr><td rowspan="3"><p>数字+单位缩写</p></td><td><p>120.56 cm²</p></td><td><p>一百二十点五六平方厘米</p></td></tr><tr><td><p>120 ㎡ 56 cm²</p></td><td><p>一百二十平方米五十六平方厘米</p></td></tr><tr><td><p>100 m 12 cm 6 mm</p></td><td><p>一百米十二厘米六毫米</p></td></tr><tr><td rowspan="4"><p>范围</p></td><td><p>10~15 kg</p></td><td><p>十至十五千克</p></td></tr><tr><td><p>10.24~789.82亩</p></td><td><p>十点二四至七百八十九点八二亩</p></td></tr><tr><td><p>10米~15米</p></td><td><p>十米至十五米</p></td></tr><tr><td><p>10.24 cm~19.08 cm</p></td><td><p>十点二四厘米至十九点零八厘米</p></td></tr><tr><td rowspan="3"><p>数字+单位+&quot;/&quot;+单位</p></td><td><p>10元/斤</p></td><td><p>十元每斤</p></td></tr><tr><td><p>199~299元/件</p></td><td><p>一百九十九至二百九十九元每件</p></td></tr><tr><td><p>299.99元/g~399.99元/g</p></td><td><p>二百九十九点九九元每克至三百九十九点九九元每克</p></td></tr><tr><td rowspan="4"><p>其他默认读法</p></td><td><p>12扎</p></td><td><p>十二扎</p></td></tr><tr><td><p>30 rm</p></td><td><p>三十r m</p></td></tr><tr><td><p>4万万同胞</p></td><td><p>四万万同胞</p></td></tr><tr><td><p>12.897微克</p></td><td><p>十二点八九七微克</p></td></tr></tbody></table>

<a id="英文-11"></a>

<a id="英文-11-h4"></a>

#### 英文

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>示例</strong></p></th><th><p><strong>英文输出</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>数字+计量单位</p></td><td><p>1.0 kg</p></td><td><p>one kilogram</p></td><td rowspan="3"><p>支持的数字格式：整数、小数以及以逗号分隔的国际写法。</p><p>支持常见单位缩写。</p></td></tr><tr><td><p>1,234.01 km</p></td><td><p>one thousand two hundred thirty four point zero one kilometres.</p></td></tr><tr><td><p>计量单位</p></td><td><p>mm2</p></td><td><p>square millimetre</p></td></tr></tbody></table>

**常见符号**

| 符号 | 中文读法 | 英文读法 |
| --- | --- | --- |
| ! | 叹号 | exclamation mark |
| “ | 双引号 | double quote |
| # | 井号 | pound |
| $ | dollar | dollar |
| % | 百分号 | percent |
| & | and | and |
| ‘ | 单引号 | left quote |
| （ | 左括号 | left parenthesis |
| ） | 右括号 | right parenthesis |
| \* | 星 | asterisk |
| + | 加 | plus |
| , | 逗号 | comma |
| \- | 杠 | dash |
| . | 点 | dot |
| / | 斜杠 | slash |
| ： | 零冒号 | solon |
| ； | 分号 | semicolon |
| < | 小于 | less than |
| \= | 等号 | equals |
| \> | 大于 | greater than |
| ? | 问号 | question mark |
| @ | at | at |
| \[ | 左方括号 | left bracket |
| \\ | 反斜线 | back slash |
| \] | 右方括号 | right bracket |
| ^ | 脱字符 | caret |
| \_ | 下划线 | underscore |
| \` | 反引号 | back quote |
| { | 左花括号 | left brace |
| \| | 竖线 | vertical bar |
| } | 右花括号 | right brace |
| ~ | 波浪线 | tilde |
| ！ | 叹号 | exclamation mark |
| “ | 左双引号 | left double quote |
| ” | 右双引号 | right double qute |
| ‘ | 左单引号 | left quote |
| ’ | 右单引号 | right quote |
| （ | 左括号 | left parenthesis |
| ） | 右括号 | right parenthesis |
| ， | 逗号 | comma |
| 。 | 句号 | full stop |
| — | 杠 | em dash |
| ： | 冒号 | colon |
| ； | 分号 | semicolon |
| ？ | 问号 | question mark |
| 、 | 顿号 | enumeration comma |
| … | 省略号 | ellipsis |
| …… | 省略号 | ellipsis |
| 《 | 左书名号 | left guillemet |
| 》 | 右书名号 | right guillemet |
| ￥ | 人民币符号 | yuan |
| ≥ | 大于等于 | greater than or equal to |
| ≤ | 小于等于 | less than or equal to |
| ≠ | 不等于 | not equal |
| ≈ | 约等于 | approximately equal |
| ± | 加减 | plus or minus |
| × | 乘 | times |
| π | 派 | pi |
| Α | 阿尔法 | alpha |
| Β | 贝塔 | beta |
| Γ | 伽玛 | gamma |
| Δ | 德尔塔 | delta |
| Ε | 艾普西龙 | epsilon |
| Ζ | 捷塔 | zeta |
| Θ | 西塔 | theta |
| Ι | 艾欧塔 | iota |
| Κ | 喀帕 | kappa |
| ∧ | 拉姆达 | lambda |
| Μ | 缪 | mu |
| Ν | 拗 | nu |
| Ξ | 克西 | ksi |
| Ο | 欧麦克轮 | omicron |
| ∏ | 派 | pi |
| Ρ | 柔 | rho |
| ∑ | 西格玛 | sigma |
| Τ | 套 | tau |
| Υ | 宇普西龙 | upsilon |
| Φ | fai | phi |
| Χ | 器 | chi |
| Ψ | 普赛 | psi |
| Ω | 欧米伽 | omega |
| α | 阿尔法 | alpha |
| β | 贝塔 | beta |
| γ | 伽玛 | gamma |
| δ | 德尔塔 | delta |
| ε | 艾普西龙 | epsilon |
| ζ | 捷塔 | zeta |
| η | 依塔 | eta |
| θ | 西塔 | theta |
| ι | 艾欧塔 | iota |
| κ | 喀帕 | kappa |
| λ | 拉姆达 | lambda |
| μ | 缪 | mu |
| ν | 拗 | nu |
| ξ | 克西 | ksi |
| ο | 欧麦克轮 | omicron |
| π | 派 | pi |
| ρ | 柔 | rho |
| σ | 西格玛 | sigma |
| τ | 套 | tau |
| υ | 宇普西龙 | upsilon |
| φ | fai | phi |
| χ | 器 | chi |
| ψ | 普赛 | psi |
| ω | 欧米伽 | omega |

**常见计量单位**

<table><thead><tr><th><p><strong>格式</strong></p></th><th><p><strong>类别</strong></p></th><th><p><strong>中文示例</strong></p></th><th><p><strong>英文示例</strong></p></th></tr></thead><tbody><tr><td rowspan="8"><p>缩写</p></td><td><p>长度</p></td><td><p>nm（纳米）、μm（微米）、 mm（毫米）、cm（厘米）、m（米）、km（千米）、ft（英尺）、in（英寸）</p></td><td><p>nm (nanometre), μm (micrometre), mm (millimetre), cm (centimetre), m (metre), km (kilometre), ft (foot), in (inch)</p></td></tr><tr><td><p>面积</p></td><td><p>cm²（平方厘米）、㎡（平方米）、km²（平方千米）、SqFt（平方英尺）</p></td><td><p>cm² (square centimetre), ㎡ (square metre), km2 (square kilometre), SqFt (square foot)</p></td></tr><tr><td><p>体积</p></td><td><p>cm³（立方厘米）、m³（立方米）、km³（立方千米）、mL（毫升）、L（升）、gallon（加仑）</p></td><td><p>cm³ (cubic centimetre), m³ (cubic metre), km3 (cubic kilometre), mL (millilitre), L (millilitre), gal (gallon)</p></td></tr><tr><td><p>重量</p></td><td><p>μg（微克）、mg（毫克）、g（克）、kg（千克）</p></td><td><p>μg (microgram), mg (microgram), g (gram), kg (kilogram)</p></td></tr><tr><td><p>时间</p></td><td><p>min（分）、sec（秒）、ms（毫秒）</p></td><td><p>min (minute), sec (second), ms (millisecond)</p></td></tr><tr><td><p>电磁</p></td><td><p>μA（微安）、mA（毫安）、Ω（欧姆）、Hz（赫兹）、kHz（千赫兹）、MHz（兆赫兹）、GHz（吉赫兹）、V（伏）、kV（千伏）、kWh（千瓦时）</p></td><td><p>μA (microamp), mA (milliamp), Hz (hertz), kHz (kilohertz), MHz (megahertz), GHz (gigahertz), V (volt), kV (kilovolt), kWh (kilowatt hour)</p></td></tr><tr><td><p>声音</p></td><td><p>dB（分贝）</p></td><td><p>dB (decibel)</p></td></tr><tr><td><p>气压</p></td><td><p>Pa（帕）、kPa（千帕）、Mpa（兆帕）</p></td><td><p>Pa (pascal), kPa (kilopascal), MPa (megapascal)</p></td></tr><tr><td colspan="2"><p>其他常见单位</p></td><td><p>支持不限于上述类别的中文单位，例如“米”、“秒”、“美元”、“毫升每瓶”等。以及中文量词，例如“架”、“场”、“头”、“部”、“盆”等。</p></td><td><p>支持不限于上述类别的计量单位，例如 tsp (teaspoon), rpm (round per minute), KB (kilobyte), mmHg (milimetre of mercury) 等。</p></td></tr></tbody></table>

<a id="示例-6"></a>

<a id="示例-6-h4"></a>

#### 示例

**cardinal**

<a id="code-block-36"></a>

```xml
<speak>
  <say-as interpret-as="cardinal">12345</say-as>
</speak>
```

<a id="code-block-37"></a>

```xml
<speak>
  <say-as interpret-as="cardinal">10234</say-as>
</speak>
```

**digits**

<a id="code-block-38"></a>

```xml
<speak>
  <say-as interpret-as="digits">12345</say-as>
</speak>
```

<a id="code-block-39"></a>

```xml
<speak>
  <say-as interpret-as="digits">10234</say-as>
</speak>
```

**telephone**

<a id="code-block-40"></a>

```xml
<speak>
  <say-as interpret-as="telephone">12345</say-as>
</speak>
```

<a id="code-block-41"></a>

```xml
<speak>
  <say-as interpret-as="telephone">10234</say-as>
</speak>
```

**name**

<a id="code-block-42"></a>

```xml
<speak>
  她的曾用名是<say-as interpret-as="name">曾小凡</say-as>
</speak>
```

**address**

<a id="code-block-43"></a>

```xml
<speak>
  <say-as interpret-as="address">富路国际1号楼3单元304</say-as>
</speak>
```

**id**

<a id="code-block-44"></a>

```xml
<speak>
  <say-as interpret-as="id">myid_1998</say-as>
</speak>
```

**characters**

<a id="code-block-45"></a>

```xml
<speak>
  <say-as interpret-as="characters">希腊字母αβ</say-as>
</speak>
```

<a id="code-block-46"></a>

```xml
<speak>
  <say-as interpret-as="characters">*b+3.c$=α</say-as>
</speak>
```

**punctuation**

<a id="code-block-47"></a>

```xml
<speak>
  <say-as interpret-as="punctuation"> -./:;</say-as>
</speak>
```

**date**

<a id="code-block-48"></a>

```xml
<speak>
  <say-as interpret-as="date">1000-10-10</say-as>
</speak>
```

<a id="code-block-49"></a>

```xml
<speak>
  <say-as interpret-as="date">10-01-2020</say-as>
</speak>
```

**time**

<a id="code-block-50"></a>

```xml
<speak>
  <say-as interpret-as="time">5:00am</say-as>
</speak>
```

<a id="code-block-51"></a>

```xml
<speak>
  <say-as interpret-as="time">0500</say-as>
</speak>
```

**currency**

<a id="code-block-52"></a>

```xml
<speak>
  <say-as interpret-as="currency">13,000,000.00RMB</say-as>
</speak>
```

<a id="code-block-53"></a>

```xml
<speak>
  <say-as interpret-as="currency">$1,000.01</say-as>
</speak>
```

**measure**

<a id="code-block-54"></a>

```xml
<speak>
  <say-as interpret-as="measure">100m12cm6mm</say-as>
</speak>
```

<a id="code-block-55"></a>

```xml
<speak>
  <say-as interpret-as="measure">1,000.01kg</say-as>
</speak>
```

<a id="标签关系-6"></a>

<a id="标签关系-6-h4"></a>

#### 标签关系

`<say-as>` 标签可以包含文本。

<a id="latex-标签与符号"></a>

<a id="sl02_symbols_h3"></a>

## LaTeX 标签与符号

按类别查看支持的标签与符号。公式输入示例包含分隔符；读法列为中文示例。

<a id="基础数学"></a>

<a id="6f2aeae22c64c"></a>

### 基础数学

<table><thead><tr><th><p><strong>标签或符号</strong></p></th><th><p><strong>含义</strong></p></th><th><p><strong>公式内容示例</strong></p></th><th><p><strong>公式输入示例</strong></p></th><th><p><strong>示例读法</strong></p></th></tr></thead><tbody><tr><td><p><code>+</code></p></td><td><p>加</p></td><td><p><code>2 + 3 = 5</code></p></td><td><p><code>$2 + 3 = 5$</code></p></td><td><p>二加三等于五</p></td></tr><tr><td><p><code>-</code></p></td><td><p>减</p></td><td><p><code>3 - 2 = 1</code></p></td><td><p><code>$3 - 2 = 1$</code></p></td><td><p>三减二等于一</p></td></tr><tr><td rowspan="2"><p><code>\pm</code></p></td><td><p>加减</p></td><td rowspan="2"><p><code>\pm 1 \pm 2</code></p></td><td rowspan="2"><p><code>$\pm 1\pm 2$</code></p></td><td rowspan="2"><p>正负一加减二</p></td></tr><tr><td><p>正负</p></td></tr><tr><td><p><code>\times</code></p></td><td rowspan="3"><p>乘</p></td><td><p><code>2 \times 3 = 6</code></p></td><td><p><code>$2 \times 3 = 6$</code></p></td><td rowspan="3"><p>二乘三等于六</p></td></tr><tr><td><p><code>×</code></p></td><td><p><code>2 × 3 = 6</code></p></td><td><p><code>$$2 × 3 = 6$$</code></p></td></tr><tr><td><p><code>*</code></p></td><td><p><code>2 * 3 = 6</code></p></td><td><p><code>\(2 * 3 = 6\)</code></p></td></tr><tr><td><p><code>\div</code></p></td><td rowspan="3"><p>除</p></td><td><p><code>6\div2=3</code></p></td><td><p><code>\[6\div2=3\]</code></p></td><td rowspan="3"><p>六除二等于三</p></td></tr><tr><td><p><code>÷</code></p></td><td><p><code>6÷2=3</code></p></td><td><p><code>$6÷2=3$</code></p></td></tr><tr><td><p><code>/</code></p></td><td><p><code>6/2=3</code></p></td><td><p><code>$6/2=3$</code></p></td></tr><tr><td><p><code>=</code></p></td><td><p>等于</p></td><td><p><code>3+5=8</code></p></td><td><p><code>$3+5=8$</code></p></td><td><p>三加五等于八</p></td></tr><tr><td><p><code>&lt;</code></p></td><td><p>小于</p></td><td><p><code>1&lt; 2</code></p></td><td><p><code>$1&lt; 2$</code></p></td><td><p>一小于二</p></td></tr><tr><td><p><code>≤</code></p></td><td rowspan="6"><p>小于等于</p></td><td><p><code>3≤5</code></p></td><td><p><code>$3≤5$</code></p></td><td rowspan="6"><p>三小于等于五</p></td></tr><tr><td><p><code>&lt;=</code></p></td><td><p><code>3&lt;=5</code></p></td><td><p><code>$3&lt;=5$</code></p></td></tr><tr><td><p><code>\leq</code></p></td><td><p><code>3\leq5</code></p></td><td><p><code>$3\leq 5$</code></p></td></tr><tr><td><p><code>\le</code></p></td><td><p><code>3\le5</code></p></td><td><p><code>$3\le 5$</code></p></td></tr><tr><td><p><code>\leqq</code></p></td><td><p><code>3\leqq5</code></p></td><td><p><code>$3\leqq 5$</code></p></td></tr><tr><td><p><code>\leqslant</code></p></td><td><p><code>3\leqslant5</code></p></td><td><p><code>$3\leqslant 5$</code></p></td></tr><tr><td><p><code>&gt;</code></p></td><td><p>大于</p></td><td><p><code>2&gt;1</code></p></td><td><p><code>$2&gt;1$</code></p></td><td><p>二大于一</p></td></tr><tr><td><p><code>≥</code></p></td><td rowspan="6"><p>大于等于</p></td><td><p><code>5≥3</code></p></td><td><p><code>$5≥3$</code></p></td><td rowspan="6"><p>五大于等于三</p></td></tr><tr><td><p><code>&gt;=</code></p></td><td><p><code>5&gt;=3</code></p></td><td><p><code>$5&gt;=3$</code></p></td></tr><tr><td><p><code>\geq</code></p></td><td><p><code>5\geq3</code></p></td><td><p><code>$5\geq 3$</code></p></td></tr><tr><td><p><code>\ge</code></p></td><td><p><code>5\ge3</code></p></td><td><p><code>$5\ge 3$</code></p></td></tr><tr><td><p><code>\geqq</code></p></td><td><p><code>5\geqq3</code></p></td><td><p><code>$5\geqq 3$</code></p></td></tr><tr><td><p><code>\geqslant</code></p></td><td><p><code>5\geqslant3</code></p></td><td><p><code>$5\geqslant 3$</code></p></td></tr><tr><td><p><code>\frac</code></p></td><td><p>分数</p></td><td><p><code>2\frac3</code></p></td><td><p><code>$\frac {2}{3}$</code></p></td><td><p>三分之二</p></td></tr><tr><td><p><code>^</code></p></td><td><p>次方</p></td><td><p><code>2^1</code></p></td><td><p><code>$2^{1}$</code></p></td><td><p>二的一次方</p></td></tr><tr><td rowspan="2"><p><code>\sqrt</code></p></td><td rowspan="2"><p>开根</p></td><td><p><code>\sqrt{9} = 3</code></p></td><td><p><code>$\sqrt {9} = 3$</code></p></td><td><p>根号下九等于三</p></td></tr><tr><td><p><code>\sqrt[3]{8} = 2</code></p></td><td><p><code>$\sqrt[3]{8} = 2$</code></p></td><td><p>三次根号下八等于二</p></td></tr><tr><td><p><code>\%</code></p></td><td><p>百分比</p></td><td><p><code>5\%</code></p></td><td><p><code>$5\%$</code></p></td><td><p>百分之五</p></td></tr><tr><td><p><code>|</code></p></td><td rowspan="2"><p>绝对值</p></td><td><p><code>∣3∣=3</code></p></td><td><p><code>$|3| =3$</code></p></td><td><p>绝对值三的绝对值等于三</p></td></tr><tr><td><p><code>\vert</code></p></td><td><p><code>3\vert=3</code></p></td><td><p><code>$\vert 3\vert =3$</code></p></td><td><p>绝对值三绝对值等于三</p></td></tr><tr><td><p><code>\lg</code></p></td><td><p>对数</p></td><td><p><code>lg {10}</code></p></td><td><p><code>$\lg {10}$</code></p></td><td><p>log十</p></td></tr><tr><td><p><code>\log</code></p></td><td><p>对数</p></td><td><p><code>\log{5}</code></p></td><td><p><code>$\log{5}$</code></p></td><td><p>log五</p></td></tr><tr><td><p><code>\ln</code></p></td><td><p>自然对数</p></td><td><p><code>\lnX</code></p></td><td><p><code>$ln {10}$</code></p></td><td><p>LN十</p></td></tr><tr><td><p><code>!</code></p></td><td><p>阶乘</p></td><td><p><code>5!</code></p></td><td><p><code>$5!$</code></p></td><td><p>五的阶乘</p></td></tr><tr><td><p><code>()</code></p></td><td rowspan="2"><p>括号</p></td><td rowspan="2"><p><code>（2+1）</code></p></td><td><p><code>$(2+1)$</code></p></td><td><p>括号内二加一</p></td></tr><tr><td><p><code>\{ \}</code></p></td><td><p><code>$\{2+1\}$</code></p></td><td><p>大括号二加一反大括号</p></td></tr></tbody></table>

<a id="特殊数学符号"></a>

<a id="ee60f2d1ef0ms"></a>

### 特殊数学符号

<table><thead><tr><th><p><strong>标签或符号</strong></p></th><th><p><strong>含义</strong></p></th><th><p><strong>公式内容示例</strong></p></th><th><p><strong>公式输入示例</strong></p></th><th><p><strong>示例读法</strong></p></th></tr></thead><tbody><tr><td><p><code>\alpha</code></p></td><td rowspan="2"><p>alpha</p></td><td><p><code>\alpha</code></p></td><td><p><code>$\alpha$</code></p></td><td rowspan="2"><p>α</p></td></tr><tr><td><p><code>\Alpha</code></p></td><td><p><code>\Alpha</code></p></td><td><p><code>$\Alpha$</code></p></td></tr><tr><td><p><code>\beta</code></p></td><td rowspan="2"><p>beta</p></td><td><p><code>\beta</code></p></td><td><p><code>$\beta$</code></p></td><td rowspan="2"><p>β</p></td></tr><tr><td><p><code>\Beta</code></p></td><td><p><code>\Beta</code></p></td><td><p><code>$\Beta$</code></p></td></tr><tr><td><p><code>\gamma</code></p></td><td rowspan="2"><p>gamma</p></td><td><p><code>\gamma</code></p></td><td><p><code>$\gamma$</code></p></td><td rowspan="2"><p>γ</p></td></tr><tr><td><p><code>\Gamma</code></p></td><td><p><code>\Gamma</code></p></td><td><p><code>$\Gamma$</code></p></td></tr><tr><td><p><code>\delta</code></p></td><td rowspan="2"><p>delta</p></td><td><p><code>\delta</code></p></td><td><p><code>$\delta$</code></p></td><td rowspan="2"><p>Δ</p></td></tr><tr><td><p><code>\Delta</code></p></td><td><p><code>\Delta</code></p></td><td><p><code>$\Delta$</code></p></td></tr><tr><td><p><code>\infty</code></p></td><td><p>无穷大（中）</p></td><td><p><code>\infty</code></p></td><td><p><code>$\infty$</code></p></td><td rowspan="2"><p>无穷大</p></td></tr><tr><td><p><code>∞</code></p></td><td><p>infty （英）</p></td><td><p><code>∞</code></p></td><td><p><code>$∞$</code></p></td></tr></tbody></table>

<a id="几何"></a>

<a id="000b50814531q"></a>

### 几何

<table><thead><tr><th><p><strong>标签或符号</strong></p></th><th><p><strong>含义</strong></p></th><th><p><strong>公式内容示例</strong></p></th><th><p><strong>公式输入示例</strong></p></th><th><p><strong>示例读法</strong></p></th></tr></thead><tbody><tr><td><p><code>\pi</code></p></td><td><p>派</p></td><td><p><code>\pi=3.14159</code></p></td><td><p><code>$\pi =3.14159$</code></p></td><td><p>派等于三点一四一五九</p></td></tr><tr><td><p><code>\sin (sine)</code></p></td><td rowspan="6"><p>三角函数</p></td><td><p><code>\sin 30^\circ =\frac {1}{2}</code></p></td><td><p><code>$\sin 30^\circ =\frac {1}{2}$</code></p></td><td><p>sine三十度等于二分之一</p></td></tr><tr><td><p><code>\cos (cosine)</code></p></td><td><p><code>\cos 45^\circ =\frac {\sqrt {2}}{2}</code></p></td><td><p><code>$\cos 45^\circ =\frac {\sqrt {2}}{2}$</code></p></td><td><p>cosine四十五度等于二分之根号下二</p></td></tr><tr><td><p><code>\tan (tangent)</code></p></td><td><p><code>\tan 30^\circ =\frac {\sin 30^\circ}{\cos 30^\circ}</code></p></td><td><p><code>$\tan 30^\circ =\frac {\sin 30^\circ}{\cos 30^\circ}$</code></p></td><td><p>tangent三十度等于cosine三十度分之sine三十度</p></td></tr><tr><td><p><code>\csc (cosecant)</code></p></td><td><p><code>\csc A</code></p></td><td><p><code>$\csc A$</code></p></td><td><p>cosecant A</p></td></tr><tr><td><p><code>\sec (secant)</code></p></td><td><p><code>\sec A</code></p></td><td><p><code>$\sec A$</code></p></td><td><p>secant A</p></td></tr><tr><td><p><code>\cot (cotangent)</code></p></td><td><p><code>\cot A</code></p></td><td><p><code>$\cot A$</code></p></td><td><p>cotangent A</p></td></tr><tr><td><p><code>\angle</code></p></td><td rowspan="2"><p>角</p></td><td><p><code>\angle AB</code></p></td><td><p><code>$\angle AB$</code></p></td><td rowspan="2"><p>角A B</p></td></tr><tr><td><p><code>∠</code></p></td><td><p><code>∠AB</code></p></td><td><p><code>$∠AB$</code></p></td></tr><tr><td><p><code>^\circ</code></p></td><td><p>度</p></td><td><p><code>∠AB = 30^\circ</code></p></td><td><p><code>$∠AB = 30^\circ$</code></p></td><td><p>角A B 等于三十度</p></td></tr><tr><td><p><code>\odot</code></p></td><td><p>圆</p></td><td><p><code>\odot</code></p></td><td><p><code>$\odot$</code></p></td><td><p>圆</p></td></tr><tr><td><p><code>\overset\frown</code></p></td><td><p>弧</p></td><td><p><code>\overset\frown {BC}</code></p></td><td><p><code>$\overset\frown {BC}$</code></p></td><td><p>弧BC</p></td></tr><tr><td><p><code>\rm{Rt}</code></p></td><td rowspan="2"><p>直角</p></td><td><p><code>\because \rm{Rt}\triangle ABC</code></p></td><td><p><code>$\because \rm{Rt}\triangle ABC$</code></p></td><td><p>因为直角三角形ABC</p></td></tr><tr><td><p><code>\mathrm{Rt}</code></p></td><td><p><code>\therefore AB \perp BC</code></p></td><td><p><code>$\therefore AB \perp BC$</code></p></td><td><p>所以AB垂直于BC</p></td></tr><tr><td><p><code>\triangle</code></p></td><td rowspan="2"><p>三角形</p></td><td><p><code>\triangleABC</code></p></td><td><p><code>$\triangle ABC$</code></p></td><td rowspan="2"><p>三角形ABC</p></td></tr><tr><td><p><code>△</code></p></td><td><p><code>△ABC</code></p></td><td><p><code>$△ABC$</code></p></td></tr><tr><td><p><code>\parallelogram</code></p></td><td><p>平行四边形</p></td><td><p><code>\parallelogramABCD</code></p></td><td><p><code>$\parallelogram ABCD$</code></p></td><td><p>平行四边形ABCD</p></td></tr><tr><td><p><code>\perp</code></p></td><td rowspan="3"><p>垂直</p></td><td><p><code>AB \perp BC</code></p></td><td><p><code>$AB \perp BC$</code></p></td><td rowspan="3"><p>A B 垂直于 B C</p></td></tr><tr><td><p><code>\bot</code></p></td><td><p><code>AB \bot BC</code></p></td><td><p><code>$AB \bot BC$</code></p></td></tr><tr><td><p><code>⊥</code></p></td><td><p><code>AB ⊥ BC</code></p></td><td><p><code>$AB ⊥ BC$</code></p></td></tr><tr><td><p><code>\parallel</code></p></td><td><p>平行</p></td><td><p><code>A\parallel B</code></p></td><td><p><code>$A\parallel B$</code></p></td><td><p>A平行于B</p></td></tr><tr><td><p><code>\equalparallel</code></p></td><td><p>平行且相等于</p></td><td><p><code>A\equalparallel B</code></p></td><td><p><code>$A\equalparallel B$</code></p></td><td><p>A平行且相等于B</p></td></tr><tr><td><p><code>\cong</code></p></td><td><p>全等</p></td><td><p><code>△ABC\cong△DEF</code></p></td><td><p><code>$△ABC\cong△DEF$</code></p></td><td><p>三角形ABC全等于三角形DEF</p></td></tr></tbody></table>

<a id="条件"></a>

<a id="14e88dc484j2g"></a>

### 条件

<table><thead><tr><th><p><strong>标签或符号</strong></p></th><th><p><strong>含义</strong></p></th><th><p><strong>公式内容示例</strong></p></th><th><p><strong>公式输入示例</strong></p></th><th><p><strong>示例读法</strong></p></th></tr></thead><tbody><tr><td><p><code>\implies</code></p></td><td><p>推出</p></td><td><p><code>\implies 1+1=2</code></p></td><td><p><code>$\implies 1+1=2$</code></p></td><td><p>推出一加一等于二</p></td></tr><tr><td><p><code>\iff</code></p></td><td><p>等价</p></td><td><p><code>p\iffq</code></p></td><td><p><code>$p\iffq$</code></p></td><td><p>p等价q</p></td></tr><tr><td><p><code>\because</code></p></td><td><p>因为</p></td><td rowspan="2"><p><code>\because a = b \therefore b=a</code></p></td><td rowspan="2"><p><code>$\because a = b \therefore b=a$</code></p></td><td rowspan="2"><p>因为a等于b所以b等于a</p></td></tr><tr><td><p><code>\therefore</code></p></td><td><p>所以</p></td></tr></tbody></table>

<a id="单位"></a>

<a id="12804b45f1zl6"></a>

### 单位

单位须使用 `\unit`、`\quantity`、`\mathit`、`\mathrm` 或 `\rm` 包裹，例如 `\unit{cm}`。

| 标签或符号 | 含义 | 公式内容示例 | 公式输入示例 | 示例读法 |
| --- | --- | --- | --- | --- |
| `mm` | 毫米 | `5\quantity{mm}` | `$5\quantity{mm}$` | 五毫米 |
| `cm` | 厘米 | `5\quantity{cm}` | `$5\quantity{cm}$` | 五厘米 |
| `dm` | 分米 | `5\quantity{dm}` | `$5\quantity{dm}$` | 五分米 |
| `m` | 米 | `5\quantity{m}` | `$5\quantity{m}$` | 五米 |
| `km` | 千米 | `5\quantity{km}` | `$5\quantity{km}$` | 五千米 |
| `g` | 克 | `5\quantity{g}` | `$5\quantity{g}$` | 五克 |
| `kg` | 千克 | `5\quantity{kg}` | `$5\quantity{kg}$` | 五千克 |
| `t` | 吨 | `5\quantity{t}` | `$5\quantity{t}$` | 五吨 |
| `mm^2` | 平方毫米 | `5\quantity{mm^2}` | `$5\quantity{mm^2}$` | 五平方毫米 |
| `cm^2` | 平方厘米 | `5\quantity{cm^2}` | `$5\quantity{cm^2}$` | 五平方厘米 |
| `dm^2` | 平方分米 | `5\quantity{dm^2}` | `$5\quantity{dm^2}$` | 五平方分米 |
| `m^2` | 平方米 | `5\quantity{m^2}` | `$5\quantity{m^2}$` | 五平方米 |
| `km^2` | 平方千米 | `5\quantity{km^2}` | `$5\quantity{km^2}$` | 五平方千米 |
| `mm^3` | 立方毫米 | `5\quantity{mm^3}` | `$5\quantity{mm^3}$` | 五立方毫米 |
| `cm^3` | 立方厘米 | `5\quantity{cm^3}` | `$5\quantity{cm^3}$` | 五立方厘米 |
| `dm^3` | 立方分米 | `5\quantity{dm^3}` | `$5\quantity{dm^3}$` | 五立方分米 |
| `m^3` | 立方米 | `5\quantity{m^3}` | `$5\quantity{m^3}$` | 五立方米 |
| `km^3` | 立方千米 | `5\quantity{km^3}` | `$5\quantity{km^3}$` | 五立方千米 |
| `ml` | 毫升 | `5\quantity{ml}` | `$5\quantity{ml}$` | 五毫升 |
| `s` | 秒 | `5\quantity{s}` | `$5\quantity{s}$` | 五秒 |
| `min` | 分钟 | `5\quantity{min}` | `$5\quantity{min}$` | 五分 |
| `h` | 小时 | `5\quantity{h}` | `$5\quantity{h}$` | 五小时 |
| `km/h` | 千米每小时 | `5\quantity{km/h}` | `$5\quantity{km/h}$` | 五千米每小时 |
| `g/l` | 克每升 | `5\quantity{g/l}` | `$5\quantity{g/l}$` | 五克每升 |

<a id="常见问题"></a>

<a id="sl02_faq_h3"></a>

## 常见问题

<a id="公式没有被正确朗读-如何排查"></a>

<a id="sl02_faq1_h4"></a>

### 公式没有被正确朗读，如何排查？

1.  检查公式是否已用 `$...$`、`$$...$$`、`\(...\)` 或 `\[...\]` 包裹。
2.  检查公式是否包含不支持的标签或符号。
3.  检查请求字符串中的 `\` 是否已正确转义为 `\\`。

<a id="如何在代码中处理反斜杠"></a>

<a id="sl02_faq2_h4"></a>

### 如何在代码中处理反斜杠？

请参见[使用方法](ssml-latex-user-guide.md#sl02_usage_h3)中的转义说明。公式内容和代码字符串的写法不同，例如 `\frac` 在普通字符串中应写为 `\\frac`。

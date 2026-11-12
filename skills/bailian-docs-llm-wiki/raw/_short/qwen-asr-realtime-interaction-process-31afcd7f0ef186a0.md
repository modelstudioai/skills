# WebSocket 接入指南

Qwen-ASR-Realtime 实时语音识别服务通过 WebSocket 协议，接收实时音频流并实时转写。支持 VAD 模式 和 Manual 模式 交互流程。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md)，示例代码请参见[实时语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)。

## 接口地址

WebSocket URL 固定如下，通过查询参数 `model` 指定要调用的模型名称（将 `<model_name>` 替换为实际的模型）：

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

**重要**URL 必须使用 `wss://` 协议。Authorization 在请求头中设置（参见[请求头](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#b02603aacf7e9)），模型通过 URL 查询参数 `model` 指定。

## 请求头

请求头中需添加如下信息：

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为 `Bearer <your_api_key>`，将 `<your_api_key>` 替换为实际的 API Key。

user-agent

string

否

客户端标识，便于服务端追踪来源。

X-DashScope-WorkSpace

string

否

阿里云百炼[业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace)。

X-DashScope-DataInspection

string

否

是否启用数据合规检测功能。默认不传或设为`enable`。如非必要，请勿启用该参数。

**重要**Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。

## 交互流程

客户端事件和服务端事件的详细说明，请参见[客户端事件](raw/_short/qwen-asr-realtime-client-events-1496b1c0718012d4.md)和[服务端事件](raw/_short/qwen-asr-realtime-server-events-5dc40b9e8a313c98.md)。

支持两种交互模式：

-   **VAD 模式（默认）**：服务端自动检测语音的起点和终点（断句），适用于实时对话、会议记录等场景。
-   **Manual 模式**：由客户端控制断句，适用于客户端能明确判断语句边界的场景，如聊天软件中的发送语音。

该模型不返回转写文本的句级、字词级时间戳。VAD 事件中的语音起止时间用于描述语音活动边界，字段说明见对应事件。

### VAD 模式（默认）

`silence_duration_ms` 的服务端默认值为 `800`，对话、聊天等需要快速断句的场景可参考 `400`；`threshold` 的服务端默认值为 `0.2`。完整配置见[客户端事件](raw/_short/qwen-asr-realtime-client-events-1496b1c0718012d4.md)。

服务端自动检测语音的起点和终点（断句）。开发者只需持续发送音频流，服务端会在检测到一句话结束时自动返回最终识别结果。此模式适用于实时对话、会议记录等场景。

**启用方式：**配置客户端`session.update`事件的`session.turn_detection`参数。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9052835871/CAEQaxiBgICW9b6H3RkiIGM5MDgwMTNkMjBjMDRlNTNiOGZlODNjZGJhNDQ3NGJm5812623_20251022102739.334.svg)

-   客户端通过发送`input_audio_buffer.append`事件将音频追加到缓冲区。
    
-   服务端在检测到语音时返回`input_audio_buffer.speech_started`事件。
    
    **注意**：如果客户端尚未收到该事件，就直接发送`session.finish`结束会话，服务端会直接返回`session.finished`事件，随后客户端需主动断开连接。
    
-   客户端继续发送`input_audio_buffer.append`事件提交音频。
    
-   客户端在音频提交完后，发送`session.finish`事件通知服务端结束当前会话。
    
    **警告**在 VAD 模式下，推完音频后必须先发送`session.finish`事件再关闭连接。如果客户端直接关闭 WebSocket 连接而未发送该事件，服务端将丢弃当前 in\_progress item，`conversation.item.input_audio_transcription.completed` 等事件将不会到达。建议在调用 `ws.Close()` 之前，先发送 `{"type":"session.finish"}`，并等待收到`session.finished`事件后再关闭连接。
    
-   服务端在检测到语音结束时返回`input_audio_buffer.speech_stopped`事件。
    
-   服务端返回`input_audio_buffer.committed`事件。
    
-   服务端返回`conversation.item.created`事件。
    
-   服务端返回`conversation.item.input_audio_transcription.text`事件，其中包含语音识别实时结果。
    
-   服务端返回`conversation.item.input_audio_transcription.completed`事件，其中包含语音识别最终结果。
    
-   服务端返回`session.finished`事件，通知客户端识别结束，此时客户端需要主动断开连接。
    

### Manual 模式

由客户端控制断句。客户端需要发送完一整句话的音频后，再发送一个`input_audio_buffer.commit`事件来通知服务端。此模式适用于客户端能明确判断语句边界的场景，如聊天软件中的发送语音。

**启用方式：**将客户端`session.update`事件的`session.turn_detection`设为null。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9052835871/CAEQaxiBgMDUp8qH3RkiIGEyYTc0NTI1ZmQ1OTQ5NjliNWE0OTYwYTAwMDBlMjBm5812623_20251022102739.334.svg)

-   客户端通过发送`input_audio_buffer.append`事件将音频追加到缓冲区。
-   客户端通过发送`input_audio_buffer.commit`事件来提交输入音频缓冲区。 该提交会在对话中创建一个新的用户消息项。
-   客户端发送`session.finish`事件通知服务端结束当前会话。
-   服务端返回`input_audio_buffer.committed`事件进行响应。
-   服务端返回`conversation.item.input_audio_transcription.text`事件，其中包含语音识别实时结果。
-   服务端返回`conversation.item.input_audio_transcription.completed`事件，其中包含语音识别最终结果。
-   服务端返回`session.finished`事件，通知客户端识别结束，此时客户端需要主动断开连接。

## 调用示例

以下示例使用 qwen3-asr-flash-realtime。在[控制台获取 API Key 和 Base URL](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)，分别配置环境变量 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL`。

下载[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)并保存为 `asr_example.wav`。音频为 16 kHz、单声道、16-bit PCM 编码的 WAV 文件。

**说明**示例代码读取 `asr_example.pcm`（PCM16、16 kHz、单声道）。如仅有 MP3/WAV 等格式，可使用 ffmpeg 转换：

```
ffmpeg -i asr_example.wav -ar 16000 -ac 1 -f s16le asr_example.pcm
```

**说明**使用非 VAD（Manual）模式时，建议单次会话持续发送的音频时长累加不超过 60 秒。

#### Java

在运行示例前，请确保已安装Java-WebSocket依赖：

Maven

```
<dependency>
    <groupId>org.java-websocket</groupId>
    <artifactId>Java-WebSocket</artifactId>
    <version>1.5.6</version>
</dependency>
<dependency>
    <groupId>org.json</groupId>
    <artifactId>json</artifactId>
    <version>20240303</version>
</dependency>
```

Gradle

```
implementation 'org.java-websocket:Java-WebSocket:1.5.6'
implementation 'org.json:json:20240303'
```

```
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONObject;

import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.*;

public class QwenASRRealtimeClient {

    private static final Logger logger = Logger.getLogger(QwenASRRealtimeClient.class.getName());
    private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final String MODEL = "qwen3-asr-flash-realtime";

    // 控制是否使用 VAD 模式
    private static final boolean enableServerVad = true;

    private static final AtomicBoolean isRunning = new AtomicBoolean(true);
    private static WebSocketClient client;

    public static void main(String[] args) throws Exception {
        initLogger();

        String baseUrl = "wss://" + URI.create(System.getenv("DASHSCOPE_BASE_URL")).getHost() + "/api-ws/v1/realtime";
        String url = baseUrl + "?model=" + MODEL;
        logger.info("Connecting to server: " + url);

        client = new WebSocketClient(new URI(url)) {
            @Override
            public void onOpen(ServerHandshake handshake) {
                logger.info("Connected to server.");
                sendSessionUpdate();
            }

            @Override
            public void onMessage(String message) {
                try {
                    JSONObject data = new JSONObject(message);
                    String eventType = data.optString("type");

                    logger.info("Received event: " + data.toString(2));

                    // 最终识别结果在 transcription.completed 事件中
                    if ("conversation.item.input_audio_transcription.completed".equals(eventType)) {
                        logger.info("Final transcript: " + data.optString("transcript"));
                    }

                    // 收到结束事件 → 停止发送线程并关闭连接
                    if ("session.finished".equals(eventType)) {
                        logger.info("Closing WebSocket connection after session finished...");

                        isRunning.set(false); // 停止发送音频线程
                        if (this.isOpen()) {
                            this.close(1000, "ASR finished");
                        }
                    }
                } catch (Exception e) {
                    logger.severe("Failed to parse message: " + message);
                }
            }

            @Override
            public void onClose(int code, String reason, boolean remote) {
                logger.info("Connection closed: " + code + " - " + reason);
            }

            @Override
            public void onError(Exception ex) {
                logger.severe("Error: " + ex.getMessage());
            }
        };

        // 添加请求头
        client.addHeader("Authorization", "Bearer " + API_KEY);
        client.addHeader("OpenAI-Beta", "realtime=v1");

        client.connectBlocking(); // 阻塞直到连接建立

        // 替换为待识别的音频文件路径
        String localAudioPath = "asr_example.pcm";
        Thread audioThread = new Thread(() -> {
            try {
                sendAudio(localAudioPath);
            } catch (Exception e) {
                logger.severe("Audio sending thread error: " + e.getMessage());
            }
        });
        audioThread.start();
    }

    /** 会话更新事件（开启/关闭 VAD） */
    private static void sendSessionUpdate() {
        JSONObject eventNoVad = new JSONObject()
                .put("event_id", "event_123")
                .put("type", "session.update")
                .put("session", new JSONObject()
                        .put("modalities", new String[]{"text"})
                        .put("input_audio_format", "pcm")
                        .put("sample_rate", 16000)
                        // .put("input_audio_transcription", new JSONObject()
                        //         .put("language", "zh"))
                        .put("turn_detection", JSONObject.NULL) // 手动模式
                );

        JSONObject eventVad = new JSONObject()
                .put("event_id", "event_123")
                .put("type", "session.update")
                .put("session", new JSONObject()
                        .put("modalities", new String[]{"text"})
                        .put("input_audio_format", "pcm")
                        .put("sample_rate", 16000)
                        // .put("input_audio_transcription", new JSONObject()
                        //         .put("language", "zh"))
                        .put("turn_detection", new JSONObject()
                                .put("type", "server_vad")
                                .put("threshold", 0.2)
                                .put("silence_duration_ms", 400))
                );

        if (enableServerVad) {
            logger.info("Sending event (VAD):\n" + eventVad.toString(2));
            client.send(eventVad.toString());
        } else {
            logger.info("Sending event (Manual):\n" + eventNoVad.toString(2));
            client.send(eventNoVad.toString());
        }
    }

    /** 发送音频文件流 */
    private static void sendAudio(String localAudioPath) throws Exception {
        Thread.sleep(3000); // 等会话准备
        byte[] allBytes = Files.readAllBytes(Paths.get(localAudioPath));
        logger.info("文件读取开始");

        int offset = 0;
        while (isRunning.get() && offset < allBytes.length) {
            int chunkSize = Math.min(3200, allBytes.length - offset);
            byte[] chunk = new byte[chunkSize];
            System.arraycopy(allBytes, offset, chunk, 0, chunkSize);
            offset += chunkSize;

            if (client != null && client.isOpen()) {
                String encoded = Base64.getEncoder().encodeToString(chunk);
                JSONObject eventd = new JSONObject()
                        .put("event_id", "event_" + System.currentTimeMillis())
                        .put("type", "input_audio_buffer.append")
                        .put("audio", encoded);

                client.send(eventd.toString());
                logger.info("Sending audio event: " + eventd.getString("event_id"));
            } else {
                break; // 避免在断开后继续发送
            }

            Thread.sleep(100); // 模拟实时发送
        }

        logger.info("文件读取完毕");

        if (client != null && client.isOpen()) {
            // 非 VAD 模式下需要 commit
            if (!enableServerVad) {
                JSONObject commitEvent = new JSONObject()
                        .put("event_id", "event_789")
                        .put("type", "input_audio_buffer.commit");
                client.send(commitEvent.toString());
                logger.info("Sent commit event for manual mode.");
            }

            JSONObject finishEvent = new JSONObject()
                    .put("event_id", "event_987")
                    .put("type", "session.finish");
            client.send(finishEvent.toString());
            logger.info("Sent finish event.");
        }
    }

    /** 初始化日志 */
    private static void initLogger() {
        logger.setLevel(Level.ALL);
        Logger rootLogger = Logger.getLogger("");
        for (Handler h : rootLogger.getHandlers()) {
            rootLogger.removeHandler(h);
        }

        Handler consoleHandler = new ConsoleHandler();
        consoleHandler.setLevel(Level.ALL);
        consoleHandler.setFormatter(new SimpleFormatter());
        logger.addHandler(consoleHandler);
    }
}
```

#### Python

在运行示例前，请确保已使用以下命令安装依赖：

```
python -m pip install websocket-client
```

**说明**不要将示例文件命名为 `websocket.py`，以免与 `websocket` 模块重名，导致导入冲突。

```
# pip install websocket-client
import os
import time
import json
import threading
import base64
from urllib.parse import urlsplit
import websocket
import logging
import logging.handlers
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

API_KEY = os.environ["DASHSCOPE_API_KEY"]
QWEN_MODEL = "qwen3-asr-flash-realtime"
baseUrl = f"wss://{urlsplit(os.environ['DASHSCOPE_BASE_URL']).netloc}/api-ws/v1/realtime"
url = f"{baseUrl}?model={QWEN_MODEL}"
print(f"Connecting to server: {url}")

# 注意： 如果是非vad模式，建议持续发送的音频时长累加不超过60s
enableServerVad = True
is_running = True  # 增加运行标志位

headers = [
    "Authorization: Bearer " + API_KEY,
    "OpenAI-Beta: realtime=v1"
]

def init_logger():
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
    f_handler = logging.handlers.RotatingFileHandler(
        "omni_tester.log", maxBytes=100 * 1024 * 1024, backupCount=3
    )
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(f_handler)
    logger.addHandler(console)

def on_open(ws):
    logger.info("Connected to server.")

    # 会话更新事件
    event_manual = {
        "event_id": "event_123",
        "type": "session.update",
        "session": {
            "modalities": ["text"],
            "input_audio_format": "pcm",
            "sample_rate": 16000,
            # "input_audio_transcription": {
            #     # 语种标识，可选，如果有明确的语种信息，建议设置
            #     "language": "zh"
            # },
            "turn_detection": None
        }
    }
    event_vad = {
        "event_id": "event_123",
        "type": "session.update",
        "session": {
            "modalities": ["text"],
            "input_audio_format": "pcm",
            "sample_rate": 16000,
            # "input_audio_transcription": {
            #     "language": "zh"
            # },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.2,
                "silence_duration_ms": 400
            }
        }
    }
    if enableServerVad:
        logger.info(f"Sending event: {json.dumps(event_vad, indent=2)}")
        ws.send(json.dumps(event_vad))
    else:
        logger.info(f"Sending event: {json.dumps(event_manual, indent=2)}")
        ws.send(json.dumps(event_manual))

def on_message(ws, message):
    global is_running
    try:
        data = json.loads(message)
        logger.info(f"Received event: {json.dumps(data, ensure_ascii=False, indent=2)}")
        if data.get("type") == "conversation.item.input_audio_transcription.completed":
            logger.info(f"Final transcript: {data.get('transcript')}")
        elif data.get("type") == "session.finished":
            logger.info("Closing WebSocket connection after session finished...")
            is_running = False  # 停止音频发送线程
            ws.close()
    except json.JSONDecodeError:
        logger.error(f"Failed to parse message: {message}")

def on_error(ws, error):
    logger.error(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logger.info(f"Connection closed: {close_status_code} - {close_msg}")

def send_audio(ws, local_audio_path):
    time.sleep(3)  # 等待会话更新完成
    global is_running

    with open(local_audio_path, 'rb') as audio_file:
        logger.info(f"文件读取开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        while is_running:
            audio_data = audio_file.read(3200)  # ~0.1s PCM16/16kHz
            if not audio_data:
                logger.info(f"文件读取完毕: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
                if ws.sock and ws.sock.connected:
                    if not enableServerVad:
                        commit_event = {
                            "event_id": "event_789",
                            "type": "input_audio_buffer.commit"
                        }
                        ws.send(json.dumps(commit_event))
                    finish_event = {
                        "event_id": "event_987",
                        "type": "session.finish"
                    }
                    ws.send(json.dumps(finish_event))
                break

            if not ws.sock or not ws.sock.connected:
                logger.info("WebSocket已关闭，停止发送音频。")
                break

            encoded_data = base64.b64encode(audio_data).decode('utf-8')
            eventd = {
                "event_id": f"event_{int(time.time() * 1000)}",
                "type": "input_audio_buffer.append",
                "audio": encoded_data
            }
            ws.send(json.dumps(eventd))
            logger.info(f"Sending audio event: {eventd['event_id']}")
            time.sleep(0.1)  # 模拟实时采集

# 初始化日志
init_logger()
logger.info(f"Connecting to WebSocket server at {url}...")

local_audio_path = "asr_example.pcm"
ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

thread = threading.Thread(target=send_audio, args=(ws, local_audio_path))
thread.start()
ws.run_forever()
```

#### Go

新建 Go 示例目录后初始化模块并安装依赖：

```
go mod init asr-example
go get github.com/gorilla/websocket@v1.5.3
```

在运行示例前，请确保已安装相关依赖：

```
package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	neturl "net/url"
	"os"
	"time"

	"github.com/gorilla/websocket"
)

const (
	model           = "qwen3-asr-flash-realtime"
	audioFile       = "asr_example.pcm" // 替换为您的PCM音频文件路径
	enableServerVad = true                  // 控制是否使用 VAD 模式
)

// 服务端事件结构
type ServerEvent struct {
	Type       string `json:"type"`
	Transcript string `json:"transcript,omitempty"`
}

func main() {
	base, err := neturl.Parse(os.Getenv("DASHSCOPE_BASE_URL"))
	if err != nil {
		log.Fatal(err)
	}
	baseURL := "wss://" + base.Host + "/api-ws/v1/realtime"
	apiKey := os.Getenv("DASHSCOPE_API_KEY")

	url := baseURL + "?model=" + model
	log.Printf("Connecting to server: %s", url)

	conn, err := connect(url, apiKey)
	if err != nil {
		log.Fatal("连接WebSocket失败：", err)
	}
	defer conn.Close()

	// 启动接收消息的 goroutine
	sessionFinished := make(chan bool, 1)
	go receiveMessages(conn, sessionFinished)

	// 发送 session.update
	if err := sendSessionUpdate(conn); err != nil {
		log.Fatal("发送 session.update 失败：", err)
	}

	// 等待会话配置完成
	time.Sleep(3 * time.Second)

	// 发送音频流
	if err := sendAudioStream(conn); err != nil {
		log.Fatal("发送音频失败：", err)
	}

	// 等待 session.finished
	<-sessionFinished
}

// 建立 WebSocket 连接
func connect(url, apiKey string) (*websocket.Conn, error) {
	headers := http.Header{}
	headers.Set("Authorization", "Bearer "+apiKey)
	headers.Set("OpenAI-Beta", "realtime=v1")
	conn, _, err := websocket.DefaultDialer.Dial(url, headers)
	return conn, err
}

// 发送 session.update 事件
func sendSessionUpdate(conn *websocket.Conn) error {
	session := map[string]interface{}{
		"modalities":         []string{"text"},
		"input_audio_format": "pcm",
		"sample_rate":        16000,
		// "input_audio_transcription": map[string]interface{}{
		// 	"language": "zh",
		// },
	}
	if enableServerVad {
		session["turn_detection"] = map[string]interface{}{
			"type":                "server_vad",
			"threshold":           0.2,
			"silence_duration_ms": 400,
		}
	} else {
		session["turn_detection"] = nil
	}
	event := map[string]interface{}{
		"event_id": "event_123",
		"type":     "session.update",
		"session":  session,
	}
	payload, _ := json.Marshal(event)
	log.Printf("Sending session.update: %s", string(payload))
	return conn.WriteMessage(websocket.TextMessage, payload)
}

// 发送音频流（每100ms发送一个PCM chunk）
func sendAudioStream(conn *websocket.Conn) error {
	f, err := os.Open(audioFile)
	if err != nil {
		return err
	}
	defer f.Close()

	chunk := make([]byte, 3200) // 100ms @ 16kHz 16bit 单声道
	for {
		n, err := f.Read(chunk)
		if n > 0 {
			event := map[string]interface{}{
				"event_id": fmt.Sprintf("event_%d", time.Now().UnixMilli()),
				"type":     "input_audio_buffer.append",
				"audio":    base64.StdEncoding.EncodeToString(chunk[:n]),
			}
			payload, _ := json.Marshal(event)
			if err := conn.WriteMessage(websocket.TextMessage, payload); err != nil {
				return err
			}
			time.Sleep(100 * time.Millisecond)
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}
	}
	log.Println("音频流结束")
	if !enableServerVad {
		commitEvt := map[string]interface{}{
			"event_id": "event_789",
			"type":     "input_audio_buffer.commit",
		}
		payload, _ := json.Marshal(commitEvt)
		if err := conn.WriteMessage(websocket.TextMessage, payload); err != nil {
			return err
		}
	}
	finishEvt := map[string]interface{}{
		"event_id": "event_987",
		"type":     "session.finish",
	}
	payload, _ := json.Marshal(finishEvt)
	return conn.WriteMessage(websocket.TextMessage, payload)
}

// 接收并处理服务端事件
func receiveMessages(conn *websocket.Conn, sessionFinished chan<- bool) {
	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("读取消息错误：", err)
			sessionFinished <- true
			return
		}
		var evt ServerEvent
		if err := json.Unmarshal(msg, &evt); err != nil {
			log.Println("解析消息错误：", err)
			continue
		}
		log.Printf("Received event: %s", evt.Type)
		switch evt.Type {
		case "conversation.item.input_audio_transcription.completed":
			log.Printf("Final transcript: %s", evt.Transcript)
		case "session.finished":
			log.Println("Session finished")
			sessionFinished <- true
			return
		}
	}
}
```

#### Node.js

在运行示例前，请确保已使用以下命令安装依赖：

```
npm install ws
```
```
/**
 * Qwen-ASR Realtime WebSocket 客户端（Node.js版）
 * 功能：
 * - 支持 VAD 模式和 Manual 模式
 * - 发送 session.update 启动会话
 * - 持续发送音频块 input_audio_buffer.append
 * - 如果是Manual模式，需要发送 input_audio_buffer.commit
 * - 发送session.finish事件
 * - 收到 session.finished 事件后关闭连接
 */

import WebSocket from 'ws';
import fs from 'fs';

// ===== 配置 =====
const API_KEY = process.env.DASHSCOPE_API_KEY;
const MODEL = 'qwen3-asr-flash-realtime';
const enableServerVad = true; // true为VAD模式，false为Manual模式
const localAudioPath = 'asr_example.pcm'; // PCM16、16kHz音频文件路径

const baseUrl = `wss://${new URL(process.env.DASHSCOPE_BASE_URL).host}/api-ws/v1/realtime`;
const url = `${baseUrl}?model=${MODEL}`;

console.log(`Connecting to server: ${url}`);

// ===== 状态控制 =====
let isRunning = true;

// ===== 建立连接 =====
const ws = new WebSocket(url, {
    headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'OpenAI-Beta': 'realtime=v1'
    }
});

// ===== 事件绑定 =====
ws.on('open', () => {
    console.log('[WebSocket] Connected to server.');
    sendSessionUpdate();
    // 启动音频发送线程
    sendAudio(localAudioPath);
});

ws.on('message', (message) => {
    try {
        const data = JSON.parse(message);
        console.log('[Received Event]:', JSON.stringify(data, null, 2));

        // 最终识别结果在 transcription.completed 事件中
        if (data.type === 'conversation.item.input_audio_transcription.completed') {
            console.log(`[Final Transcript] ${data.transcript}`);
        }

        // 收到结束事件
        if (data.type === 'session.finished') {
            console.log('[Action] Closing WebSocket connection after session finished...');

            if (ws.readyState === WebSocket.OPEN) {
                ws.close(1000, 'ASR finished');
            }
        }
    } catch (e) {
        console.error('[Error] Failed to parse message:', message);
    }
});

ws.on('close', (code, reason) => {
    console.log(`[WebSocket] Connection closed: ${code} - ${reason}`);
});

ws.on('error', (err) => {
    console.error('[WebSocket Error]', err);
});

// ===== 会话更新 =====
function sendSessionUpdate() {
    const eventNoVad = {
        event_id: 'event_123',
        type: 'session.update',
        session: {
            modalities: ['text'],
            input_audio_format: 'pcm',
            sample_rate: 16000,
            // input_audio_transcription: {
            //     language: 'zh'
            // },
            turn_detection: null
        }
    };

    const eventVad = {
        event_id: 'event_123',
        type: 'session.update',
        session: {
            modalities: ['text'],
            input_audio_format: 'pcm',
            sample_rate: 16000,
            // input_audio_transcription: {
            //     language: 'zh'
            // },
            turn_detection: {
                type: 'server_vad',
                threshold: 0.2,
                silence_duration_ms: 400
            }
        }
    };

    if (enableServerVad) {
        console.log('[Send Event] VAD Mode:\n', JSON.stringify(eventVad, null, 2));
        ws.send(JSON.stringify(eventVad));
    } else {
        console.log('[Send Event] Manual Mode:\n', JSON.stringify(eventNoVad, null, 2));
        ws.send(JSON.stringify(eventNoVad));
    }
}

// ===== 发送音频文件流 =====
function sendAudio(audioPath) {
    setTimeout(() => {
        console.log(`[File Read Start] ${audioPath}`);
        const buffer = fs.readFileSync(audioPath);

        let offset = 0;
        const chunkSize = 3200; // 约0.1s的PCM16音频

        function sendChunk() {
            if (!isRunning) return;
            if (offset >= buffer.length) {
                isRunning = false; // 停止发送音频
                console.log('[File Read End]');
                if (ws.readyState === WebSocket.OPEN) {
                    if (!enableServerVad) {
                        const commitEvent = {
                            event_id: 'event_789',
                            type: 'input_audio_buffer.commit'
                        };
                        ws.send(JSON.stringify(commitEvent));
                        console.log('[Send Commit Event]');
                    }

                    const finishEvent = {
                        event_id: 'event_987',
                        type: 'session.finish'
                    };
                    ws.send(JSON.stringify(finishEvent));
                    console.log('[Send Finish Event]');
                }

                return;
            }

            if (ws.readyState !== WebSocket.OPEN) {
                console.log('[Stop] WebSocket is not open.');
                return;
            }

            const chunk = buffer.slice(offset, offset + chunkSize);
            offset += chunkSize;

            const encoded = chunk.toString('base64');
            const appendEvent = {
                event_id: `event_${Date.now()}`,
                type: 'input_audio_buffer.append',
                audio: encoded
            };

            ws.send(JSON.stringify(appendEvent));
            console.log(`[Send Audio Event] ${appendEvent.event_id}`);

            setTimeout(sendChunk, 100); // 模拟实时发送
        }

        sendChunk();
    }, 3000); // 等待会话配置完成
}
```

将代码保存为 `asr_example.mjs`，运行 `node asr_example.mjs`。

#### C#

将代码保存为 `Program.cs`，使用 .NET 控制台项目运行。

示例代码如下：

```
using System.Net.WebSockets;
using System.Text;
using System.Text.Json.Nodes;

class Program {
    private static ClientWebSocket _webSocket = new ClientWebSocket();
    private static CancellationTokenSource _cts = new CancellationTokenSource();
    private static bool _sessionFinished = false;
    private static bool _isRunning = true;

    // 控制是否使用 VAD 模式
    private const bool EnableServerVad = true;

    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
    private const string Model = "qwen3-asr-flash-realtime";
    private static readonly string BaseUrl = "wss://" + new Uri(Environment.GetEnvironmentVariable("DASHSCOPE_BASE_URL")!).Authority + "/api-ws/v1/realtime";
    private const string AudioFilePath = "asr_example.pcm"; // 替换为您的PCM音频文件路径

    static async Task Main(string[] args) {
        var url = $"{BaseUrl}?model={Model}";
        Console.WriteLine($"Connecting to server: {url}");

        // 设置鉴权 headers
        _webSocket.Options.SetRequestHeader("Authorization", $"Bearer {ApiKey}");
        _webSocket.Options.SetRequestHeader("OpenAI-Beta", "realtime=v1");

        await _webSocket.ConnectAsync(new Uri(url), _cts.Token);
        Console.WriteLine("Connected to server.");

        // 启动消息接收任务
        var receiveTask = ReceiveMessagesAsync();

        // 发送 session.update 配置
        await SendSessionUpdateAsync();

        // 发送音频流
        await SendAudioStreamAsync();

        // 等待 session.finished 事件
        while (!_sessionFinished && !_cts.IsCancellationRequested) {
            await Task.Delay(100);
        }

        if (_webSocket.State == WebSocketState.Open) {
            await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "ASR finished", _cts.Token);
        }
    }

    private static async Task SendAsync(string text) {
        var bytes = Encoding.UTF8.GetBytes(text);
        await _webSocket.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, _cts.Token);
    }

    // 发送 session.update 事件
    private static async Task SendSessionUpdateAsync() {
        var session = new JsonObject {
            ["modalities"] = new JsonArray { "text" },
            ["input_audio_format"] = "pcm",
            ["sample_rate"] = 16000,
            // ["input_audio_transcription"] = new JsonObject { ["language"] = "zh" }
        };
        if (EnableServerVad) {
            session["turn_detection"] = new JsonObject {
                ["type"] = "server_vad",
                ["threshold"] = 0.2,
                ["silence_duration_ms"] = 400
            };
        } else {
            session["turn_detection"] = null;
        }
        var payload = new JsonObject {
            ["event_id"] = "event_123",
            ["type"] = "session.update",
            ["session"] = session
        };
        Console.WriteLine($"Sending session.update: {payload.ToJsonString()}");
        await SendAsync(payload.ToJsonString());
    }

    // 发送音频流（每100ms发送一个PCM chunk）
    private static async Task SendAudioStreamAsync() {
        await Task.Delay(3000); // 等待会话配置完成
        const int chunkSize = 3200; // 100ms @ 16kHz 16bit 单声道
        using var fs = new FileStream(AudioFilePath, FileMode.Open, FileAccess.Read);
        var buffer = new byte[chunkSize];
        int read;
        while (_isRunning && (read = await fs.ReadAsync(buffer, 0, chunkSize)) > 0) {
            if (_webSocket.State != WebSocketState.Open) break;
            string b64 = Convert.ToBase64String(buffer, 0, read);
            var append = new JsonObject {
                ["event_id"] = $"event_{DateTimeOffset.Now.ToUnixTimeMilliseconds()}",
                ["type"] = "input_audio_buffer.append",
                ["audio"] = b64
            };
            await SendAsync(append.ToJsonString());
            await Task.Delay(100);
        }
        Console.WriteLine("File read end.");
        if (_webSocket.State == WebSocketState.Open) {
            if (!EnableServerVad) {
                var commit = new JsonObject {
                    ["event_id"] = "event_789",
                    ["type"] = "input_audio_buffer.commit"
                };
                await SendAsync(commit.ToJsonString());
            }
            var finish = new JsonObject {
                ["event_id"] = "event_987",
                ["type"] = "session.finish"
            };
            await SendAsync(finish.ToJsonString());
        }
    }

    // 接收并处理服务端事件
    private static async Task ReceiveMessagesAsync() {
        var buffer = new byte[16384];
        var sb = new StringBuilder();
        while (_webSocket.State == WebSocketState.Open && !_cts.IsCancellationRequested) {
            try {
                var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), _cts.Token);
                if (result.MessageType == WebSocketMessageType.Close) {
                    await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cts.Token);
                    break;
                }
                sb.Append(Encoding.UTF8.GetString(buffer, 0, result.Count));
                if (!result.EndOfMessage) continue;
                string text = sb.ToString();
                sb.Clear();
                var data = JsonNode.Parse(text);
                string? type = data?["type"]?.GetValue<string>();
                Console.WriteLine($"Received event: {type}");
                if (type == "conversation.item.input_audio_transcription.completed") {
                    Console.WriteLine($"Final transcript: {data!["transcript"]}");
                } else if (type == "session.finished") {
                    Console.WriteLine("Session finished, closing...");
                    _sessionFinished = true;
                    _isRunning = false;
                    break;
                }
            } catch (Exception ex) {
                Console.WriteLine($"Receive error: {ex.Message}");
                break;
            }
        }
    }
}
```

#### PHP

将依赖配置保存为 `composer.json`，执行 `composer install` 后运行 PHP 示例。

示例代码目录结构为：

my-php-project/

├── composer.json

├── vendor/

└── index.php

composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

```
{
    "require": {
        "react/event-loop": "^1.3",
        "react/socket": "^1.11",
        "ratchet/pawl": "^0.4"
    }
}
```

index.php内容如下：

```
<?php

require __DIR__ . '/vendor/autoload.php';

use Ratchet\Client\Connector;
use React\EventLoop\Loop;
use React\Socket\Connector as SocketConnector;

$api_key = getenv("DASHSCOPE_API_KEY");
$model = 'qwen3-asr-flash-realtime';
$base_url = 'wss://' . parse_url(getenv('DASHSCOPE_BASE_URL'), PHP_URL_HOST) . '/api-ws/v1/realtime';
$websocket_url = $base_url . '?model=' . $model;
$audio_file_path = 'asr_example.pcm'; // 替换为您的PCM音频文件路径

// 控制是否使用 VAD 模式
$enable_server_vad = true;

$loop = Loop::get();
$socketConnector = new SocketConnector($loop, [
    'tls' => ['verify_peer' => true, 'verify_peer_name' => true],
]);
$connector = new Connector($loop, $socketConnector);

$headers = [
    'Authorization' => 'Bearer ' . $api_key,
    'OpenAI-Beta' => 'realtime=v1',
];

$is_running = true;

$connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $audio_file_path, $enable_server_vad, &$is_running) {
    echo "连接到WebSocket服务器\n";

    // 监听服务端事件
    $conn->on('message', function($msg) use ($conn, &$is_running) {
        $event = json_decode($msg, true);
        if (!isset($event['type'])) {
            return;
        }
        echo "Received event: {$event['type']}\n";
        if ($event['type'] === 'conversation.item.input_audio_transcription.completed') {
            echo "Final transcript: {$event['transcript']}\n";
        } elseif ($event['type'] === 'session.finished') {
            echo "Session finished, closing...\n";
            $is_running = false;
            $conn->close();
        }
    });
    $conn->on('close', function() {
        echo "连接已关闭\n";
    });

    // 发送 session.update 事件
    sendSessionUpdate($conn, $enable_server_vad);

    // 等待会话配置完成后开始发送音频
    $loop->addTimer(3, function () use ($conn, $audio_file_path, $enable_server_vad, $loop, &$is_running) {
        sendAudioStream($conn, $audio_file_path, $enable_server_vad, $loop, $is_running);
    });
}, function ($e) {
    echo "无法连接：{$e->getMessage()}\n";
});

$loop->run();

// 发送 session.update 事件
function sendSessionUpdate($conn, $enable_server_vad) {
    $session = [
        'modalities' => ['text'],
        'input_audio_format' => 'pcm',
        'sample_rate' => 16000,
        // 'input_audio_transcription' => ['language' => 'zh'],
        'turn_detection' => $enable_server_vad ? [
            'type' => 'server_vad',
            'threshold' => 0.2,
            'silence_duration_ms' => 400,
        ] : null,
    ];
    $event = [
        'event_id' => 'event_123',
        'type' => 'session.update',
        'session' => $session,
    ];
    $conn->send(json_encode($event));
    echo "Sent session.update\n";
}

// 发送音频流（每100ms发送一个PCM chunk）
function sendAudioStream($conn, $audio_file_path, $enable_server_vad, $loop, &$is_running) {
    $fp = fopen($audio_file_path, 'rb');
    if (!$fp) {
        echo "无法打开音频文件\n";
        return;
    }
    $send_chunk = function() use ($conn, $fp, $enable_server_vad, $loop, &$send_chunk, &$is_running) {
        if (!$is_running) {
            fclose($fp);
            return;
        }
        $chunk = fread($fp, 3200); // 100ms @ 16kHz 16bit 单声道
        if ($chunk === false || strlen($chunk) === 0) {
            fclose($fp);
            echo "音频流结束\n";
            if (!$enable_server_vad) {
                $conn->send(json_encode([
                    'event_id' => 'event_789',
                    'type' => 'input_audio_buffer.commit',
                ]));
            }
            $conn->send(json_encode([
                'event_id' => 'event_987',
                'type' => 'session.finish',
            ]));
            return;
        }
        $append = [
            'event_id' => 'event_' . round(microtime(true) * 1000),
            'type' => 'input_audio_buffer.append',
            'audio' => base64_encode($chunk),
        ];
        $conn->send(json_encode($append));
        $loop->addTimer(0.1, $send_chunk);
    };
    $send_chunk();
}
```

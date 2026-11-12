# WebSocket 接入指南

本文介绍通过 WebSocket 连接访问 Qwen-Audio-ASR-Streaming 实时语音识别服务的接口地址、请求头和交互流程。

## 接口地址

WebSocket URL 固定如下：

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

## 请求头

请求头中需添加如下信息：

**参数**

**类型**

**是否必选**

**说明**

`Authorization`

`string`

是

鉴权令牌，格式为 `Bearer <your_api_key>`，将 `<your_api_key>` 替换为实际的 API Key。

`user-agent`

`string`

否

客户端标识，便于服务端追踪来源。

`X-DashScope-WorkSpace`

`string`

否

阿里云百炼[业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace)。

`X-DashScope-DataInspection`

`string`

否

是否启用数据合规检测功能。默认不传或设为`enable`。如非必要，请勿启用该参数。

**重要**Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。

## 交互流程

客户端事件和服务端事件的详细说明，请参见[客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md)和[服务端事件](raw/_short/qwen-audio-asr-streaming-server-events-4757090610f208c7.md)。

![WebSocket 语音识别交互时序](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7761245871/CAEQURiBgMCczta5pxkiIGY0N2Q2YjIwZTM1MTQyNTY4ZmFkY2MwN2JmOTllODFl4709861_20241015153444.149.svg)

按时间顺序，客户端与服务端的交互流程如下：

1.  建立连接：客户端与服务端建立 WebSocket 连接。
2.  开启任务：客户端发送 run-task 指令以开启任务，并接收服务端返回的 task-started 事件，标志着任务已成功开启，可以进行后续步骤。
3.  发送音频流：客户端开始发送二进制音频（须为单声道音频），并同时接收服务端持续返回的 result-generated 事件，该事件包含语音识别结果。
4.  通知服务端结束任务：客户端发送 finish-task 指令通知服务端结束任务，并继续接收服务端返回的 result-generated 事件。
5.  任务结束：客户端收到服务端返回的 task-finished 事件，标志着任务结束。
6.  关闭连接：客户端关闭 WebSocket 连接。

## 调用示例

以下示例使用 qwen-audio-3.1-asr-flash-streaming。在[控制台获取 API Key 和 Base URL](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)，分别配置环境变量 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL`。

下载[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)并保存为 `asr_example.wav`。音频为 16 kHz、单声道、16-bit PCM 编码的 WAV 文件。

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
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

public class FunASRRealtimeClient {

    private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final String URL = "wss://" + URI.create(System.getenv("DASHSCOPE_BASE_URL")).getHost() + "/api-ws/v1/inference";
    private static final String AUDIO_FILE = "asr_example.wav"; // 替换为您的音频文件路径
    private static final String MODEL = "qwen-audio-3.1-asr-flash-streaming";

    // 生成32位随机ID
    private static final String TASK_ID = UUID.randomUUID().toString().replace("-", "").substring(0, 32);

    private static final AtomicBoolean taskStarted = new AtomicBoolean(false);
    private static WebSocketClient client;

    public static void main(String[] args) throws Exception {
        client = new WebSocketClient(new URI(URL)) {
            @Override
            public void onOpen(ServerHandshake handshake) {
                System.out.println("连接到服务器");
                sendRunTask();
            }

            @Override
            public void onMessage(String data) {
                JSONObject message = new JSONObject(data);
                String event = message.getJSONObject("header").getString("event");
                switch (event) {
                    case "task-started":
                        System.out.println("任务开始");
                        taskStarted.set(true);
                        new Thread(FunASRRealtimeClient::sendAudioStream).start();
                        break;
                    case "result-generated":
                        JSONObject payload = message.getJSONObject("payload");
                        String text = payload.getJSONObject("output").getJSONObject("sentence").getString("text");
                        System.out.println("识别结果：" + text);
                        if (payload.has("usage")) {
                            System.out.println("任务音频时长（秒）：" + payload.getJSONObject("usage").get("duration"));
                        }
                        break;
                    case "task-finished":
                        System.out.println("任务完成");
                        close();
                        break;
                    case "task-failed":
                        String errMsg = message.getJSONObject("header").optString("error_message");
                        System.err.println("任务失败：" + errMsg);
                        close();
                        break;
                    default:
                        System.out.println("未知事件：" + event);
                }
            }

            @Override
            public void onClose(int code, String reason, boolean remote) {
                if (!taskStarted.get()) {
                    System.err.println("任务未启动，关闭连接");
                }
            }

            @Override
            public void onError(Exception ex) {
                System.err.println("WebSocket错误：" + ex.getMessage());
            }
        };
        client.addHeader("Authorization", "bearer " + API_KEY);
        client.connectBlocking();
    }

    // 发送run-task指令
    private static void sendRunTask() {
        JSONObject runTask = new JSONObject()
                .put("header", new JSONObject()
                        .put("action", "run-task")
                        .put("task_id", TASK_ID)
                        .put("streaming", "duplex"))
                .put("payload", new JSONObject()
                        .put("task_group", "audio")
                        .put("task", "asr")
                        .put("function", "recognition")
                        .put("model", MODEL)
                        .put("parameters", new JSONObject()
                                .put("sample_rate", 16000)
                                .put("format", "wav"))
                        .put("input", new JSONObject()));
        client.send(runTask.toString());
    }

    // 发送音频流（每100ms发送一个二进制chunk）
    private static void sendAudioStream() {
        int chunkSize = 3200; // 100ms @ 16kHz 16bit 单声道
        try {
            byte[] audio = Files.readAllBytes(Paths.get(AUDIO_FILE));
            int offset = 0;
            while (offset < audio.length) {
                int end = Math.min(offset + chunkSize, audio.length);
                byte[] chunk = new byte[end - offset];
                System.arraycopy(audio, offset, chunk, 0, end - offset);
                client.send(ByteBuffer.wrap(chunk));
                offset = end;
                Thread.sleep(100);
            }
            System.out.println("音频流结束");
            sendFinishTask();
        } catch (Exception e) {
            System.err.println("读取音频文件错误：" + e.getMessage());
            client.close();
        }
    }

    // 发送finish-task指令
    private static void sendFinishTask() {
        JSONObject finishTask = new JSONObject()
                .put("header", new JSONObject()
                        .put("action", "finish-task")
                        .put("task_id", TASK_ID)
                        .put("streaming", "duplex"))
                .put("payload", new JSONObject()
                        .put("input", new JSONObject()));
        client.send(finishTask.toString());
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
import json
import time
import uuid
import threading
from urllib.parse import urlsplit
import websocket

api_key = os.environ.get('DASHSCOPE_API_KEY')
url = f"wss://{urlsplit(os.environ['DASHSCOPE_BASE_URL']).netloc}/api-ws/v1/inference"  # WebSocket服务器地址
audio_file = 'asr_example.wav'  # 替换为您的音频文件路径

# 生成32位随机ID
TASK_ID = uuid.uuid4().hex[:32]

task_started = False  # 标记任务是否已启动

# 发送run-task指令
def send_run_task(ws):
    run_task_message = {
        'header': {
            'action': 'run-task',
            'task_id': TASK_ID,
            'streaming': 'duplex'
        },
        'payload': {
            'task_group': 'audio',
            'task': 'asr',
            'function': 'recognition',
            'model': 'qwen-audio-3.1-asr-flash-streaming',
            'parameters': {
                'sample_rate': 16000,
                'format': 'wav'
            },
            'input': {}
        }
    }
    ws.send(json.dumps(run_task_message))

# 发送finish-task指令
def send_finish_task(ws):
    finish_task_message = {
        'header': {
            'action': 'finish-task',
            'task_id': TASK_ID,
            'streaming': 'duplex'
        },
        'payload': {
            'input': {}
        }
    }
    ws.send(json.dumps(finish_task_message))

# 发送音频流（每100ms发送一个二进制chunk）
def send_audio_stream(ws):
    chunk_size = 3200  # 100ms @ 16kHz 16bit 单声道
    try:
        with open(audio_file, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)
                time.sleep(0.1)
        print('音频流结束')
        send_finish_task(ws)
    except Exception as e:
        print('读取音频文件错误：', e)
        ws.close()

# 连接打开时发送run-task指令
def on_open(ws):
    print('连接到服务器')
    send_run_task(ws)

# 接收消息处理
def on_message(ws, data):
    global task_started
    message = json.loads(data)
    event = message['header']['event']
    if event == 'task-started':
        print('任务开始')
        task_started = True
        threading.Thread(target=send_audio_stream, args=(ws,), daemon=True).start()
    elif event == 'result-generated':
        print('识别结果：', message['payload']['output']['sentence']['text'])
        if message['payload'].get('usage'):
            print('任务音频时长（秒）：', message['payload']['usage']['duration'])
    elif event == 'task-finished':
        print('任务完成')
        ws.close()
    elif event == 'task-failed':
        print('任务失败：', message['header'].get('error_message'))
        ws.close()
    else:
        print('未知事件：', event)

# 如果没有收到task-started事件，关闭连接
def on_close(ws, close_status_code, close_msg):
    if not task_started:
        print('任务未启动，关闭连接')

# 错误处理
def on_error(ws, error):
    print('WebSocket错误：', error)

if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        url,
        header={'Authorization': f'bearer {api_key}'},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
```

#### Go

新建 Go 示例目录后初始化模块并安装依赖：

```
go mod init asr-example
go get github.com/gorilla/websocket@v1.5.3 github.com/google/uuid@v1.6.0
```
```
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	neturl "net/url"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

const (
	audioFile = "asr_example.wav"                                   // 替换为您的音频文件路径
)

var dialer = websocket.DefaultDialer

func main() {
	apiKey := os.Getenv("DASHSCOPE_API_KEY")

	// 连接WebSocket服务
	conn, err := connectWebSocket(apiKey)
	if err != nil {
		log.Fatal("连接WebSocket失败：", err)
	}
	defer closeConnection(conn)

	// 启动一个goroutine来接收结果
	taskStarted := make(chan bool)
	taskDone := make(chan bool)
	startResultReceiver(conn, taskStarted, taskDone)

	// 发送run-task指令
	taskID, err := sendRunTaskCmd(conn)
	if err != nil {
		log.Fatal("发送run-task指令失败：", err)
	}

	// 等待task-started事件
	waitForTaskStarted(taskStarted)

	// 发送待识别音频文件流
	if err := sendAudioData(conn); err != nil {
		log.Fatal("发送音频失败：", err)
	}

	// 发送finish-task指令
	if err := sendFinishTaskCmd(conn, taskID); err != nil {
		log.Fatal("发送finish-task指令失败：", err)
	}

	// 等待任务完成或失败
	<-taskDone
}

// 定义结构体来表示JSON数据
type Header struct {
	Action       string                 `json:"action"`
	TaskID       string                 `json:"task_id"`
	Streaming    string                 `json:"streaming"`
	Event        string                 `json:"event"`
	ErrorCode    string                 `json:"error_code,omitempty"`
	ErrorMessage string                 `json:"error_message,omitempty"`
	Attributes   map[string]interface{} `json:"attributes"`
}

type Output struct {
	Sentence struct {
		BeginTime int64  `json:"begin_time"`
		EndTime   *int64 `json:"end_time"`
		Text      string `json:"text"`
		Words     []struct {
			BeginTime   int64  `json:"begin_time"`
			EndTime     *int64 `json:"end_time"`
			Text        string `json:"text"`
			Punctuation string `json:"punctuation"`
		} `json:"words"`
	} `json:"sentence"`
}

type Payload struct {
	TaskGroup  string `json:"task_group"`
	Task       string `json:"task"`
	Function   string `json:"function"`
	Model      string `json:"model"`
	Parameters Params `json:"parameters"`
	Input      Input  `json:"input"`
	Output     Output `json:"output,omitempty"`
	Usage      *struct {
		Duration int `json:"duration"`
	} `json:"usage,omitempty"`
}

type Params struct {
	Format                   string `json:"format"`
	SampleRate               int    `json:"sample_rate"`
	DisfluencyRemovalEnabled bool   `json:"disfluency_removal_enabled"`
}

type Input struct {
}

type Event struct {
	Header  Header  `json:"header"`
	Payload Payload `json:"payload"`
}

// 连接WebSocket服务
func connectWebSocket(apiKey string) (*websocket.Conn, error) {
	base, err := neturl.Parse(os.Getenv("DASHSCOPE_BASE_URL"))
	if err != nil {
		return nil, err
	}
	wsURL := "wss://" + base.Host + "/api-ws/v1/inference"
	header := make(http.Header)
	header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))
	conn, _, err := dialer.Dial(wsURL, header)
	return conn, err
}

// 启动一个goroutine异步接收WebSocket消息
func startResultReceiver(conn *websocket.Conn, taskStarted chan<- bool, taskDone chan<- bool) {
	go func() {
		for {
			_, message, err := conn.ReadMessage()
			if err != nil {
				log.Println("解析服务器消息失败：", err)
				return
			}
			var event Event
			err = json.Unmarshal(message, &event)
			if err != nil {
				log.Println("解析事件失败：", err)
				continue
			}
			if handleEvent(conn, event, taskStarted, taskDone) {
				return
			}
		}
	}()
}

// 发送run-task指令
func sendRunTaskCmd(conn *websocket.Conn) (string, error) {
	runTaskCmd, taskID, err := generateRunTaskCmd()
	if err != nil {
		return "", err
	}
	err = conn.WriteMessage(websocket.TextMessage, []byte(runTaskCmd))
	return taskID, err
}

// 生成run-task指令
func generateRunTaskCmd() (string, string, error) {
	taskID := uuid.New().String()
	runTaskCmd := Event{
		Header: Header{
			Action:    "run-task",
			TaskID:    taskID,
			Streaming: "duplex",
		},
		Payload: Payload{
			TaskGroup: "audio",
			Task:      "asr",
			Function:  "recognition",
			Model:     "qwen-audio-3.1-asr-flash-streaming",
			Parameters: Params{
				Format:     "wav",
				SampleRate: 16000,
			},
			Input: Input{},
		},
	}
	runTaskCmdJSON, err := json.Marshal(runTaskCmd)
	return string(runTaskCmdJSON), taskID, err
}

// 等待task-started事件
func waitForTaskStarted(taskStarted chan bool) {
	select {
	case <-taskStarted:
		fmt.Println("任务开启成功")
	case <-time.After(10 * time.Second):
		log.Fatal("等待task-started超时，任务开启失败")
	}
}

// 发送音频数据
func sendAudioData(conn *websocket.Conn) error {
	file, err := os.Open(audioFile)
	if err != nil {
		return err
	}
	defer file.Close()

	buf := make([]byte, 3200)
	for {
		n, err := file.Read(buf)
		if n == 0 {
			break
		}
		if err != nil && err != io.EOF {
			return err
		}
		err = conn.WriteMessage(websocket.BinaryMessage, buf[:n])
		if err != nil {
			return err
		}
		time.Sleep(100 * time.Millisecond)
	}
	return nil
}

// 发送finish-task指令
func sendFinishTaskCmd(conn *websocket.Conn, taskID string) error {
	finishTaskCmd, err := generateFinishTaskCmd(taskID)
	if err != nil {
		return err
	}
	err = conn.WriteMessage(websocket.TextMessage, []byte(finishTaskCmd))
	return err
}

// 生成finish-task指令
func generateFinishTaskCmd(taskID string) (string, error) {
	finishTaskCmd := Event{
		Header: Header{
			Action:    "finish-task",
			TaskID:    taskID,
			Streaming: "duplex",
		},
		Payload: Payload{
			Input: Input{},
		},
	}
	finishTaskCmdJSON, err := json.Marshal(finishTaskCmd)
	return string(finishTaskCmdJSON), err
}

// 处理事件
func handleEvent(conn *websocket.Conn, event Event, taskStarted chan<- bool, taskDone chan<- bool) bool {
	switch event.Header.Event {
	case "task-started":
		fmt.Println("收到task-started事件")
		taskStarted <- true
	case "result-generated":
		if event.Payload.Output.Sentence.Text != "" {
			fmt.Println("识别结果：", event.Payload.Output.Sentence.Text)
		}
		if event.Payload.Usage != nil {
			fmt.Println("任务音频时长（秒）：", event.Payload.Usage.Duration)
		}
	case "task-finished":
		fmt.Println("任务完成")
		taskDone <- true
		return true
	case "task-failed":
		handleTaskFailed(event, conn)
		taskDone <- true
		return true
	default:
		log.Printf("预料之外的事件：%v", event)
	}
	return false
}

// 处理任务失败事件
func handleTaskFailed(event Event, conn *websocket.Conn) {
	if event.Header.ErrorMessage != "" {
		log.Fatalf("任务失败：%s", event.Header.ErrorMessage)
	} else {
		log.Fatal("未知原因导致任务失败")
	}
}

// 关闭连接
func closeConnection(conn *websocket.Conn) {
	if conn != nil {
		conn.Close()
	}
}
```

#### Node.js

需安装相关依赖：

```
npm install ws@8 uuid@9
```

示例代码如下：

```
const fs = require('fs');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid'); // 用于生成UUID

const apiKey = process.env.DASHSCOPE_API_KEY;
const url = `wss://${new URL(process.env.DASHSCOPE_BASE_URL).host}/api-ws/v1/inference`; // WebSocket服务器地址
const audioFile = 'asr_example.wav'; // 替换为您的音频文件路径

// 生成32位随机ID
const TASK_ID = uuidv4().replace(/-/g, '').slice(0, 32);

// 创建WebSocket客户端
const ws = new WebSocket(url, {
  headers: {
    Authorization: `bearer ${apiKey}`
  }
});

let taskStarted = false; // 标记任务是否已启动

// 连接打开时发送run-task指令
ws.on('open', () => {
  console.log('连接到服务器');
  sendRunTask();
});

// 接收消息处理
ws.on('message', (data) => {
  const message = JSON.parse(data);
  switch (message.header.event) {
    case 'task-started':
      console.log('任务开始');
      taskStarted = true;
      sendAudioStream();
      break;
    case 'result-generated':
      console.log('识别结果：', message.payload.output.sentence.text);
      if (message.payload.usage) {
        console.log('任务音频时长（秒）：', message.payload.usage.duration);
      }
      break;
    case 'task-finished':
      console.log('任务完成');
      ws.close();
      break;
    case 'task-failed':
      console.error('任务失败：', message.header.error_message);
      ws.close();
      break;
    default:
      console.log('未知事件：', message.header.event);
  }
});

// 如果没有收到task-started事件，关闭连接
ws.on('close', () => {
  if (!taskStarted) {
    console.error('任务未启动，关闭连接');
  }
});

// 发送run-task指令
function sendRunTask() {
  const runTaskMessage = {
    header: {
      action: 'run-task',
      task_id: TASK_ID,
      streaming: 'duplex'
    },
    payload: {
      task_group: 'audio',
      task: 'asr',
      function: 'recognition',
      model: 'qwen-audio-3.1-asr-flash-streaming',
      parameters: {
        sample_rate: 16000,
        format: 'wav'
      },
      input: {}
    }
  };
  ws.send(JSON.stringify(runTaskMessage));
}

// 发送音频流
function sendAudioStream() {
  const audioStream = fs.createReadStream(audioFile);
  let chunkCount = 0;

  function sendNextChunk() {
    const chunk = audioStream.read();
    if (chunk) {
      ws.send(chunk);
      chunkCount++;
      setTimeout(sendNextChunk, 100); // 每100ms发送一次
    }
  }

  audioStream.on('readable', () => {
    sendNextChunk();
  });

  audioStream.on('end', () => {
    console.log('音频流结束');
    sendFinishTask();
  });

  audioStream.on('error', (err) => {
    console.error('读取音频文件错误：', err);
    ws.close();
  });
}

// 发送finish-task指令
function sendFinishTask() {
  const finishTaskMessage = {
    header: {
      action: 'finish-task',
      task_id: TASK_ID,
      streaming: 'duplex'
    },
    payload: {
      input: {}
    }
  };
  ws.send(JSON.stringify(finishTaskMessage));
}

// 错误处理
ws.on('error', (error) => {
  console.error('WebSocket错误：', error);
});
```

将代码保存为 `asr_example.cjs`，运行 `node asr_example.cjs`。

#### C#

将代码保存为 `Program.cs`，使用 .NET 控制台项目运行。

示例代码如下：

```
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

class Program {
    private static ClientWebSocket _webSocket = new ClientWebSocket();
    private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
    private static bool _taskStartedReceived = false;
    private static bool _taskFinishedReceived = false;
    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

    private static readonly string WebSocketUrl = "wss://" + new Uri(Environment.GetEnvironmentVariable("DASHSCOPE_BASE_URL")!).Authority + "/api-ws/v1/inference";
    // 替换为您的音频文件路径
    private const string AudioFilePath = "asr_example.wav";

    static async Task Main(string[] args) {
        // 建立WebSocket连接，配置headers进行鉴权
        _webSocket.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");

        await _webSocket.ConnectAsync(new Uri(WebSocketUrl), _cancellationTokenSource.Token);

        // 启动线程异步接收WebSocket消息
        var receiveTask = ReceiveMessagesAsync();

        // 发送run-task指令
        string _taskId = Guid.NewGuid().ToString("N"); // 生成32位随机ID
        var runTaskJson = GenerateRunTaskJson(_taskId);
        await SendAsync(runTaskJson);

        // 等待task-started事件
        while (!_taskStartedReceived) {
            await Task.Delay(100, _cancellationTokenSource.Token);
        }

        // 读取本地文件，向服务器发送待识别音频流
        await SendAudioStreamAsync(AudioFilePath);

        // 发送finish-task指令结束任务
        var finishTaskJson = GenerateFinishTaskJson(_taskId);
        await SendAsync(finishTaskJson);

        // 等待task-finished事件
        while (!_taskFinishedReceived && !_cancellationTokenSource.IsCancellationRequested) {
            try {
                await Task.Delay(100, _cancellationTokenSource.Token);
            } catch (OperationCanceledException) {
                // 任务已被取消，退出循环
                break;
            }
        }

        // 关闭连接
        if (!_cancellationTokenSource.IsCancellationRequested) {
            await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cancellationTokenSource.Token);
        }

        _cancellationTokenSource.Cancel();
        try {
            await receiveTask;
        } catch (OperationCanceledException) {
            // 忽略操作取消异常
        }
    }

    private static async Task ReceiveMessagesAsync() {
        try {
            while (_webSocket.State == WebSocketState.Open && !_cancellationTokenSource.IsCancellationRequested) {
                var message = await ReceiveMessageAsync(_cancellationTokenSource.Token);
                if (message != null) {
                    var eventValue = message["header"]?["event"]?.GetValue<string>();
                    switch (eventValue) {
                        case "task-started":
                            Console.WriteLine("任务开启成功");
                            _taskStartedReceived = true;
                            break;
                        case "result-generated":
                            Console.WriteLine($"识别结果：{message["payload"]?["output"]?["sentence"]?["text"]?.GetValue<string>()}");
                            if (message["payload"]?["usage"] != null && message["payload"]?["usage"]?["duration"] != null) {
                                Console.WriteLine($"任务音频时长（秒）：{message["payload"]?["usage"]?["duration"]?.GetValue<int>()}");
                            }
                            break;
                        case "task-finished":
                            Console.WriteLine("任务完成");
                            _taskFinishedReceived = true;
                            _cancellationTokenSource.Cancel();
                            break;
                        case "task-failed":
                            Console.WriteLine($"任务失败：{message["header"]?["error_message"]?.GetValue<string>()}");
                            _cancellationTokenSource.Cancel();
                            break;
                    }
                }
            }
        } catch (OperationCanceledException) {
            // 忽略操作取消异常
        }
    }

    private static async Task<JsonNode?> ReceiveMessageAsync(CancellationToken cancellationToken) {
        var buffer = new byte[1024 * 4];
        var segment = new ArraySegment<byte>(buffer);
        var sb = new StringBuilder();
        WebSocketReceiveResult result;
        // 循环接收并拼接分片，直到 EndOfMessage，避免长消息被截断导致 JSON 解析失败
        do {
            result = await _webSocket.ReceiveAsync(segment, cancellationToken);
            if (result.MessageType == WebSocketMessageType.Close) {
                await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", cancellationToken);
                return null;
            }
            sb.Append(Encoding.UTF8.GetString(buffer, 0, result.Count));
        } while (!result.EndOfMessage);

        return JsonNode.Parse(sb.ToString());
    }

    private static async Task SendAsync(string message) {
        var buffer = Encoding.UTF8.GetBytes(message);
        var segment = new ArraySegment<byte>(buffer);
        await _webSocket.SendAsync(segment, WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
    }

    private static async Task SendAudioStreamAsync(string filePath) {
        using (var audioStream = File.OpenRead(filePath)) {
            var buffer = new byte[3200]; // 每次发送100ms的音频数据
            int bytesRead;

            while ((bytesRead = await audioStream.ReadAsync(buffer, 0, buffer.Length)) > 0) {
                var segment = new ArraySegment<byte>(buffer, 0, bytesRead);
                await _webSocket.SendAsync(segment, WebSocketMessageType.Binary, true, _cancellationTokenSource.Token);
                await Task.Delay(100); // 间隔100ms
            }
        }
    }

    private static string GenerateRunTaskJson(string taskId) {
        var runTask = new JsonObject {
            ["header"] = new JsonObject {
                ["action"] = "run-task",
                ["task_id"] = taskId,
                ["streaming"] = "duplex"
            },
            ["payload"] = new JsonObject {
                ["task_group"] = "audio",
                ["task"] = "asr",
                ["function"] = "recognition",
                ["model"] = "qwen-audio-3.1-asr-flash-streaming",
                ["parameters"] = new JsonObject {
                    ["format"] = "wav",
                    ["sample_rate"] = 16000,
                },
                ["input"] = new JsonObject()
            }
        };
        return JsonSerializer.Serialize(runTask);
    }

    private static string GenerateFinishTaskJson(string taskId) {
        var finishTask = new JsonObject {
            ["header"] = new JsonObject {
                ["action"] = "finish-task",
                ["task_id"] = taskId,
                ["streaming"] = "duplex"
            },
            ["payload"] = new JsonObject {
                ["input"] = new JsonObject()
            }
        };
        return JsonSerializer.Serialize(finishTask);
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

```
<?php

require __DIR__ . '/vendor/autoload.php';

use Ratchet\Client\Connector;
use React\EventLoop\Loop;
use React\Socket\Connector as SocketConnector;
use Ratchet\rfc6455\Messaging\Frame;

$api_key = getenv("DASHSCOPE_API_KEY");
$websocket_url = 'wss://' . parse_url(getenv('DASHSCOPE_BASE_URL'), PHP_URL_HOST) . '/api-ws/v1/inference';
$audio_file_path = 'asr_example.wav'; // 替换为您的音频文件路径

$loop = Loop::get();

// 创建自定义的连接器
$socketConnector = new SocketConnector($loop, [
    'tcp' => [
        'bindto' => '0.0.0.0:0',
    ],
    'tls' => [
        'verify_peer' => true,
        'verify_peer_name' => true,
    ],
]);

$connector = new Connector($loop, $socketConnector);

$headers = [
    'Authorization' => 'bearer ' . $api_key
];

$connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $audio_file_path) {
    echo "连接到WebSocket服务器\n";

    // 启动异步接收WebSocket消息的线程
    $taskId = generateTaskId();
    $conn->on('message', function($msg) use ($conn, $loop, $audio_file_path, $taskId) {
        $response = json_decode($msg, true);

        if (isset($response['header']['event'])) {
            handleEvent($conn, $response, $loop, $audio_file_path, $taskId);
        } else {
            echo "未知的消息格式\n";
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

    // 生成任务ID

    // 发送 run-task 指令
    sendRunTaskMessage($conn, $taskId);

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
            "task" => "asr",
            "function" => "recognition",
            "model" => "qwen-audio-3.1-asr-flash-streaming",
            "parameters" => [
                "format" => "wav",
                "sample_rate" => 16000
            ],
            "input" => new stdClass()
        ]
    ]);
    echo "准备发送run-task指令：" . $runTaskMessage . "\n";
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
            "input" => new stdClass()
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
 * @param $loop
 * @param $audio_file_path
 */
function handleEvent($conn, $response, $loop, $audio_file_path, $taskId) {
    static $chunks;
    static $allChunksSent = false;

    switch ($response['header']['event']) {
        case 'task-started':
            echo "任务开始，发送音频数据...\n";
            // 读取音频文件
            $voiceData = readAudioFile($audio_file_path);
            if ($voiceData === false) {
                echo "无法读取音频文件\n";
                $conn->close();
                return;
            }

            // 分割音频数据
            $chunks = splitAudioData($voiceData, 3200);

            // 定义发送函数
            $sendChunk = function() use ($conn, &$chunks, $loop, &$sendChunk, &$allChunksSent, $taskId) {
                if (!empty($chunks)) {
                    $chunk = array_shift($chunks);
                    $binaryMsg = new Frame($chunk, true, Frame::OP_BINARY);
                    $conn->send($binaryMsg);
                    // 100ms后发送下一个片段
                    $loop->addTimer(0.1, $sendChunk);
                } else {
                    echo "所有数据块已发送\n";
                    $allChunksSent = true;

                    // 发送 finish-task 指令
                    sendFinishTaskMessage($conn, $taskId);
                }
            };

            // 开始发送音频数据
            $sendChunk();
            break;
        case 'result-generated':
            $result = $response['payload']['output']['sentence'];
            echo "识别结果：" . $result['text'] . "\n";
            if (isset($response['payload']['usage']['duration'])) {
                echo "任务音频时长（秒）：" . $response['payload']['usage']['duration'] . "\n";
            }
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

    // 如果所有数据已发送且任务已完成，关闭连接
    if ($allChunksSent && $response['header']['event'] == 'task-finished') {
        // 等待1秒以确保所有数据都已传输完毕
        $loop->addTimer(1, function() use ($conn) {
            $conn->close();
            echo "客户端关闭连接\n";
        });
    }
}
```

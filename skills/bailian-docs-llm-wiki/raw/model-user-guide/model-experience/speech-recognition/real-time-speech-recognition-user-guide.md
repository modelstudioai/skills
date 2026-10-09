# 实时语音识别

实时语音识别服务接收音频流并实时转写为带标点的文本，适用于直播字幕、在线会议、语音聊天、智能助手等场景。

## 概述

实现低延迟音频到文本转换。

-   支持普通话及粤语、四川话等多种方言的高精度语音识别
-   具备应对复杂声学环境的能力，支持自动语种检测与智能非人声过滤
-   支持惊讶、平静、愉快、悲伤、厌恶、愤怒、恐惧等多种情绪状态识别
-   支持热词定制，可提升特定词汇的识别准确率
-   支持上下文增强，通过配置上下文提高识别准确率
-   支持时间戳输出，生成结构化识别结果
-   灵活采样率与多种音频格式，适配不同录音环境

批量场景（会议转写、通话分析、字幕生成等）可使用[非实时语音识别](raw/model-user-guide/model-experience/speech-recognition/non-realtime-speech-recognition-user-guide.md)。各模型选型建议请参见[语音识别](raw/model-user-guide/model-experience/speech-recognition/asr-model.md)。

## 前提条件

-   已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并将其[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   如果通过 DashScope SDK 调用，需要[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

以下示例展示如何通过 DashScope SDK 快速调用实时语音识别服务。

#### Qwen-Audio-3.x-ASR-Flash-Streaming/ Fun-ASR -Realtime

AOQ 协议的适用场景、支持模型和接入方式，请参见[Realtime API 概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### 识别传入麦克风的语音

识别麦克风传入的语音并实时输出文本，实现"边说边出字"的效果。

#### Java

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;

import java.nio.ByteBuffer;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.submit(new RealtimeRecognitionTask());
        executorService.shutdown();
        executorService.awaitTermination(1, TimeUnit.MINUTES);
        System.exit(0);
    }
}

class RealtimeRecognitionTask implements Runnable {
    @Override
    public void run() {
        RecognitionParam param = RecognitionParam.builder()
                .model("qwen-audio-3.0-asr-flash-streaming")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .format("pcm")
                .sampleRate(16000)
                .build();
        Recognition recognizer = new Recognition();

        ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
            @Override
            public void onEvent(RecognitionResult result) {
                if (result.isSentenceEnd()) {
                    System.out.println("Final Result: " + result.getSentence().getText());
                } else {
                    System.out.println("Intermediate Result: " + result.getSentence().getText());
                }
            }

            @Override
            public void onComplete() {
                System.out.println("Recognition complete");
            }

            @Override
            public void onError(Exception e) {
                System.out.println("RecognitionCallback error: " + e.getMessage());
            }
        };
        try {
            recognizer.call(param, callback);
            // 创建音频格式
            AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
            // 根据格式匹配默认录音设备
            TargetDataLine targetDataLine =
                    AudioSystem.getTargetDataLine(audioFormat);
            targetDataLine.open(audioFormat);
            // 开始录音
            targetDataLine.start();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            long start = System.currentTimeMillis();
            // 录音50s并进行实时转写
            while (System.currentTimeMillis() - start < 50000) {
                int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
                if (read > 0) {
                    buffer.limit(read);
                    // 将录音音频数据发送给流式识别服务
                    recognizer.sendAudioFrame(buffer);
                    buffer = ByteBuffer.allocate(1024);
                    // 录音速率有限，防止cpu占用过高，休眠一小会儿
                    Thread.sleep(20);
                }
            }
            recognizer.stop();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 任务结束后关闭 Websocket 连接
            recognizer.getDuplexApi().close(1000, "bye");
        }

        System.out.println(
                "[Metric] requestId: "
                        + recognizer.getLastRequestId()
                        + ", first package delay ms: "
                        + recognizer.getFirstPackageDelay()
                        + ", last package delay ms: "
                        + recognizer.getLastPackageDelay());
    }
}
```

#### Python

运行Python示例前，需要通过`pip install pyaudio`命令安装第三方音频播放与采集套件。

```
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

import dashscope
import pyaudio
from dashscope.audio.asr import *

mic = None
stream = None

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

# Real-time speech recognition callback
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print('RecognitionCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    def on_close(self) -> None:
        global mic
        global stream
        print('RecognitionCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')  # recognition completed

    def on_error(self, message) -> None:
        print('RecognitionCallback task_id: ', message.request_id)
        print('RecognitionCallback error: ', message.message)
        # Stop and close the audio stream if it is running
        if 'stream' in globals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop recognition ...')
    # Stop recognition
    recognition.stop()
    print('Recognition stopped.')
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay(),
            recognition.get_last_package_delay(),
        ))
    # Forcefully exit the program
    sys.exit(0)

# main function
if __name__ == '__main__':
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

    # Create the recognition callback
    callback = Callback()

    # Call recognition service by async mode, you can customize the recognition parameters, like model, format,
    # sample_rate
    recognition = Recognition(
        model='qwen-audio-3.0-asr-flash-streaming',
        format=format_pcm,
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=sample_rate,
        # support 8000, 16000
        semantic_punctuation_enabled=False,
        callback=callback)

    # Start recognition
    recognition.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")
    # Create a keyboard listener until "Ctrl+C" is pressed

    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
        else:
            break

    recognition.stop()
```

#### 识别本地音频文件

识别本地音频文件并输出结果，适用于对话聊天、控制口令、语音输入法、语音搜索等较短的准实时场景。

Java

```
import com.alibaba.dashscope.api.GeneralApi;
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.base.HalfDuplexParamBase;
import com.alibaba.dashscope.common.GeneralListParam;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.protocol.GeneralServiceOption;
import com.alibaba.dashscope.protocol.HttpMethod;
import com.alibaba.dashscope.protocol.Protocol;
import com.alibaba.dashscope.protocol.StreamingMode;
import com.alibaba.dashscope.utils.Constants;

import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        // 实际应用中，该方法仅在程序最开始执行一次即可，不必多次执行该方法。
        warmUp();

        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.submit(new RealtimeRecognitionTask(Paths.get(System.getProperty("user.dir"), "{YOUR_AUDIO_FILE}")));
        executorService.shutdown();

        // wait for all tasks to complete
        executorService.awaitTermination(1, TimeUnit.MINUTES);
        System.exit(0);
    }

    public static void warmUp() {
        try {
            // Lightweight GET request to establish connection
            GeneralServiceOption warmupOption = GeneralServiceOption.builder()
                    .protocol(Protocol.HTTP)
                    .httpMethod(HttpMethod.GET)
                    .streamingMode(StreamingMode.OUT)
                    .path("assistants")
                    .build();

            warmupOption.setBaseHttpUrl(Constants.baseHttpApiUrl);
            GeneralApi<HalfDuplexParamBase> api = new GeneralApi<>();
            api.get(GeneralListParam.builder().limit(1L).build(), warmupOption);
        } catch (Exception e) {
            // Reset flag to allow retry if pre-warming failed
        }
    }
}

class RealtimeRecognitionTask implements Runnable {
    private Path filepath;

    public RealtimeRecognitionTask(Path filepath) {
        this.filepath = filepath;
    }

    @Override
    public void run() {
        RecognitionParam param = RecognitionParam.builder()
                .model("qwen-audio-3.1-asr-flash-streaming")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .format("wav")
                .sampleRate(16000)
                .build();
        Recognition recognizer = new Recognition();

        String threadName = Thread.currentThread().getName();

        ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
            @Override
            public void onEvent(RecognitionResult message) {
                if (message.isSentenceEnd()) {

                    System.out.println(TimeUtils.getTimestamp()+" "+
                            "[process " + threadName + "] Final Result:" + message.getSentence().getText());
                } else {
                    System.out.println(TimeUtils.getTimestamp()+" "+
                            "[process " + threadName + "] Intermediate Result: " + message.getSentence().getText());
                }
            }

            @Override
            public void onComplete() {
                System.out.println(TimeUtils.getTimestamp()+" "+"[" + threadName + "] Recognition complete");
            }

            @Override
            public void onError(Exception e) {
                System.out.println(TimeUtils.getTimestamp()+" "+
                        "[" + threadName + "] RecognitionCallback error: " + e.getMessage());
            }
        };

        try {
            recognizer.call(param, callback);
            // Please replace the path with your audio file path
            System.out.println(TimeUtils.getTimestamp()+" "+"[" + threadName + "] Input file_path is: " + this.filepath);
            // Read file and send audio by chunks
            FileInputStream fis = new FileInputStream(this.filepath.toFile());
            byte[] allData = new byte[fis.available()];
            int ret = fis.read(allData);
            fis.close();

            int sendFrameLength = 3200;
            for (int i = 0; i * sendFrameLength < allData.length; i ++) {
                int start = i * sendFrameLength;
                int end = Math.min(start + sendFrameLength, allData.length);
                ByteBuffer byteBuffer = ByteBuffer.wrap(allData, start, end - start);
                recognizer.sendAudioFrame(byteBuffer);
                Thread.sleep(100);
            }

            System.out.println(TimeUtils.getTimestamp()+" "+LocalDateTime.now());
            recognizer.stop();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 任务结束后关闭 Websocket 连接
            recognizer.getDuplexApi().close(1000, "bye");
        }

        System.out.println(
                "["
                        + threadName
                        + "][Metric] requestId: "
                        + recognizer.getLastRequestId()
                        + ", first package delay ms: "
                        + recognizer.getFirstPackageDelay()
                        + ", last package delay ms: "
                        + recognizer.getLastPackageDelay());
    }
}
```

Python

```
import os
import time
import dashscope
from dashscope.audio.asr import *

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

class Callback(RecognitionCallback):
    def on_complete(self) -> None:
        print(get_timestamp() + ' Recognition completed')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('Recognition task_id: ', result.request_id)
        print('Recognition error: ', result.message)
        exit(0)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print(get_timestamp() + ' RecognitionCallback text: ', sentence['text'])
        if RecognitionResult.is_sentence_end(sentence):
            print(get_timestamp() +
                  'RecognitionCallback sentence end, request_id:%s, usage:%s'
                  % (result.get_request_id(), result.get_usage(sentence)))

callback = Callback()

recognition = Recognition(model='qwen-audio-3.1-asr-flash-streaming',
                          format='wav',
                          sample_rate=16000,
                          callback=callback)

try:
    audio_data: bytes = None
    f = open("{YOUR_AUDIO_FILE}", 'rb')
    if os.path.getsize("{YOUR_AUDIO_FILE}"):
        # 一次性将文件数据全部读入buffer
        file_buffer = f.read()
        f.close()
        print("Start Recognition")
        recognition.start()

        # 从buffer中间隔3200字节发送一次
        buffer_size = len(file_buffer)
        offset = 0
        chunk_size = 3200

        while offset < buffer_size:
            # 计算本次要发送的数据块大小
            remaining_bytes = buffer_size - offset
            current_chunk_size = min(chunk_size, remaining_bytes)

            # 从buffer中提取当前数据块
            audio_data = file_buffer[offset:offset + current_chunk_size]

            # 发送音频数据帧
            recognition.send_audio_frame(audio_data)
            # 更新偏移量
            offset += current_chunk_size

            # 添加延迟模拟实时传输
            time.sleep(0.1)

        recognition.stop()
    else:
        raise Exception(
            'The supplied file was empty (zero bytes long)')
except Exception as e:
    raise e

print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
    ))
```

#### Paraformer

Paraformer示例代码和Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime相似，将model替换成Paraformer模型名即可。

## 进阶功能

### VAD 断句配置

VAD（Voice Activity Detection，语音活动检测）用于判定一段连续语音何时结束，从而触发"最终识别结果"事件。以下模型均默认启用服务端 VAD，但参数命名与可调粒度不同：

-   **Qwen-Audio-3.1-ASR-Flash-Streaming**：通过 `vad_model` 选择 VAD 模型，可选值为 `near_meeting_16k`（近场）和 `far_field_meeting_16k`（远场，默认值）。参数定义请参见[客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-1bae8548d2be6bc5.md)。
-   **Qwen-Audio-3.0-ASR-Flash-Streaming / Fun-ASR-Realtime / Paraformer**：通过 `max_sentence_silence`（VAD 断句静音阈值，毫秒）配置。当一段语音后的静音时长超过该阈值时，系统判定该句子已结束。
-   **Qwen3-ASR-Flash-Realtime**：通过 `session.turn_detection` 配置，含 `silence_duration_ms`（静音持续时长阈值，超过则判定 turn 结束，服务端默认 `800`，对话和聊天等需快速断句的场景推荐设为 `400`）与 `threshold`（VAD 检测灵敏度，服务端默认 `0.2`）。Qwen3-ASR-Flash-Realtime 还支持关闭 VAD 改用客户端 commit 控制断句的 Manual 模式，详见 [Qwen3-ASR-Flash-Realtime 交互模式](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#qwen-asr-flow-h2)。

参数名因协议而异（同一含义在 Qwen-Audio-3.0-ASR-Flash-Streaming / Fun-ASR-Realtime / Paraformer 中称 `max_sentence_silence`，在 Qwen3-ASR-Flash-Realtime 中称 `silence_duration_ms`）。完整字段定义请参见[API参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#c09d428f2crac)。

### 使用热词提升准确率

支持通过热词提升特定词汇（品牌名、人名、专有术语等）的识别准确率。

详细的热词配置方法和使用说明，请参见[提升识别准确率](raw/model-user-guide/model-experience/speech-recognition/improve-asr-accuracy.md)。

### 使用上下文增强提升准确率

支持上下文增强功能，可将对话历史或领域术语传入 ASR 模型，显著提升专有词汇的转写准确率。详细的使用方法和效果示例，请参见[上下文增强](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_enhance_h2)。

### 获取时间戳

Qwen-Audio-3.x-ASR-Flash-Streaming、Fun-ASR-Realtime 和 Paraformer 系列模型默认输出**句级**与**字级**两种粒度的时间戳，便于字幕对齐、关键词高亮、卡拉 OK 跟读等场景。**Qwen3-ASR-Flash-Realtime（qwen3-asr-flash-realtime）当前不返回时间戳信息**，如需时间戳请使用 Qwen-Audio-3.x-ASR-Flash-Streaming、Fun-ASR-Realtime 或 Paraformer。**Qwen ASR** 的录音文件转写模型 `qwen3-asr-flash-filetrans` 支持字级时间戳，详见[非实时语音识别](raw/model-user-guide/model-experience/speech-recognition/non-realtime-speech-recognition-user-guide.md)。

时间戳单位均为毫秒，分两个层级返回：

-   **句级**：`payload.output.sentence.begin_time` 与 `payload.output.sentence.end_time`，标识整句在音频中的起止时刻。中间结果中 `end_time` 可能为 `null`，待句子结束（`sentence_end = true`）时填充最终值。
-   **字级**：`payload.output.sentence.words` 数组，每个元素包含 `begin_time`、`end_time`、`text`（该字/词文本）以及 `punctuation`（该字后跟随的标点，无则为空串）。

返回结构示例（节选）：

```
{
  "payload": {
    "output": {
      "sentence": {
        "begin_time": 170,
        "end_time": 920,
        "text": "好，我知道了",
        "sentence_end": true,
        "words": [
          { "begin_time": 170, "end_time": 295, "text": "好", "punctuation": "，" },
          { "begin_time": 295, "end_time": 503, "text": "我", "punctuation": "" },
          { "begin_time": 503, "end_time": 711, "text": "知道", "punctuation": "" },
          { "begin_time": 711, "end_time": 920, "text": "了", "punctuation": "" }
        ]
      }
    }
  }
}
```

以上字段名以 WebSocket JSON 路径为准。不同 SDK 暴露上述字段的命名习惯不同（如字典 key、对象属性、getter 方法等），完整字段对照请参见各 SDK 的 API 参考。

完整字段定义请参见[API参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#c09d428f2crac)。

### 情感识别

**Qwen3-ASR-Flash-Realtime** 与 Paraformer 部分模型可在转写结果中附带说话人的情绪状态，但两者输出粒度与开启方式不同。

**Qwen3-ASR-Flash-Realtime（qwen3-asr-flash-realtime）**：固定开启，无需配置。在 `conversation.item.input_audio_transcription.text` 与 `conversation.item.input_audio_transcription.completed` 事件中均通过顶层 `emotion` 字段返回，取值为 7 类细粒度情绪：`surprised`（惊讶）、`neutral`（平静）、`happy`（愉快）、`sad`（悲伤）、`disgusted`（厌恶）、`angry`（愤怒）、`fearful`（恐惧）。

```
{
  "type": "conversation.item.input_audio_transcription.text",
  "emotion": "neutral",
  "text": "今天天气不错",
  "stash": ""
}
```

**Paraformer（paraformer-realtime-8k-v2）**：仅此一款 Paraformer 模型支持情感识别，结果通过 `payload.output.sentence.emo_tag` 与 `payload.output.sentence.emo_confidence` 返回，取值为 3 类极性：`positive`（正面，如开心、满意）、`negative`（负面，如愤怒、沉闷）、`neutral`（无明显情感），置信度范围 \[0.0, 1.0\]。

情感识别需同时满足以下条件才会输出：

-   模型为 `paraformer-realtime-8k-v2`。
-   语义断句关闭：`semantic_punctuation_enabled = false`（默认即为 false，无需特别设置）。
-   仅在 `sentence_end = true` 的句子结束事件中返回。

如不希望返回情感识别字段，可将 `semantic_punctuation_enabled` 设为 `true`，此时将启用语义断句、不再返回 `emo_tag` 与 `emo_confidence` 字段。

以上字段名以 WebSocket JSON 路径为准。不同 SDK 暴露上述字段的命名习惯不同（如字典 key、对象属性、getter 方法等），完整字段对照请参见各 SDK 的 API 参考。

完整字段定义、取值约束与示例请参见[API参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#c09d428f2crac)。

### 敏感词过滤

敏感词过滤可对识别结果中的敏感词执行替换或移除，适用于客服质检、内容合规、字幕审核等场景。

**支持范围：**仅Qwen-Audio-3.x-ASR-Flash-Streaming和Fun-ASR-Realtime。

**使用限制：**最多支持设置32个敏感词。

**默认行为：**未传入 `special_word_filter` 参数时，不会对敏感词进行过滤。

**如何配置：**`special_word_filter` 是 JSON 对象，包含三个子字段：

-   `filter_with_signed.word_list`：字符串数组，列出需要被替换为等长 `*` 的敏感词。例如 `["测试"]`，「帮我测试一下」会变成「帮我\*\*一下」。
-   `filter_with_empty.word_list`：字符串数组，列出需要从结果中完全移除的敏感词。例如 `["开始"]`，「比赛这就要开始了吗」会变成「比赛这就要了吗」。
-   `system_reserved_filter`：布尔值，默认 `false`。是否启用敏感词过滤功能。

配置示例：

```
{
  "special_word_filter": {
    "filter_with_signed": {
      "word_list": ["测试"]
    },
    "filter_with_empty": {
      "word_list": ["开始", "发生"]
    },
    "system_reserved_filter": true
  }
}
```

不同 SDK 暴露上述参数的命名习惯不同（如字典 key、对象属性、方法等），完整字段对照请参见 API参考。

### WebSocket 原始协议调用

以下示例展示如何通过 WebSocket 原始协议直连服务端，适用于不使用 DashScope SDK 的场景。此为最小可运行实现，WebSocket 协议请参见各模型的 [API参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#c09d428f2crac)。

点击查看 WebSocket 原始协议调用示例

#### Qwen-Audio-3.x-ASR-Flash-Streaming/ Fun-ASR-Realtime

#### Python

在运行示例前，请确保已使用以下命令安装依赖：

```
pip uninstall websocket-client
pip uninstall websocket
pip install websocket-client
```

请不要将示例代码文件命名为 `websocket.py`，这会与 websocket 库产生命名冲突，导致如下错误：`AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?`。

```
# pip install websocket-client
import os
import json
import time
import uuid
import threading
import websocket

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.environ.get('DASHSCOPE_API_KEY')
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'  # WebSocket服务器地址
audio_file = '{YOUR_AUDIO_FILE}'  # 替换为您的音频文件路径

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
            print('任务计费时长（秒）：', message['payload']['usage']['duration'])
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

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static final String API_KEY = "sk-xxx";
    private static final String API_KEY = System.getenv().getOrDefault("DASHSCOPE_API_KEY", "sk-xxx");
    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    private static final String URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
    private static final String AUDIO_FILE = "{YOUR_AUDIO_FILE}"; // 替换为您的音频文件路径
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
                            System.out.println("任务计费时长（秒）：" + payload.getJSONObject("usage").get("duration"));
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

#### Node.js

需安装相关依赖：

```
npm install ws
npm install uuid
```

示例代码如下：

```
const fs = require('fs');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid'); // 用于生成UUID

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：const apiKey = "sk-xxx"
const apiKey = process.env.DASHSCOPE_API_KEY;
// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
const url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
const audioFile = '{YOUR_AUDIO_FILE}'; // 替换为您的音频文件路径

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
        console.log('任务计费时长（秒）：', message.payload.usage.duration);
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

#### C#

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
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static readonly string ApiKey = "sk-xxx"
    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    private const string WebSocketUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
    // 替换为您的音频文件路径
    private const string AudioFilePath = "{YOUR_AUDIO_FILE}";

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
                                Console.WriteLine($"任务计费时长（秒）：{message["payload"]?["usage"]?["duration"]?.GetValue<int>()}");
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
            var buffer = new byte[1024]; // 每次发送100ms的音频数据
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

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$api_key = "sk-xxx"
$api_key = getenv("DASHSCOPE_API_KEY");
// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
$websocket_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference';
$audio_file_path = '{YOUR_AUDIO_FILE}'; // 替换为您的音频文件路径

$loop = Loop::get();

// 创建自定义的连接器
$socketConnector = new SocketConnector($loop, [
    'tcp' => [
        'bindto' => '0.0.0.0:0',
    ],
    // 警告：关闭 TLS 证书校验存在中间人攻击风险，仅限本地调试；生产环境务必将 verify_peer/verify_peer_name 设为 true
    'tls' => [
        'verify_peer' => false,
        'verify_peer_name' => false,
    ],
]);

$connector = new Connector($loop, $socketConnector);

$headers = [
    'Authorization' => 'bearer ' . $api_key
];

$connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $audio_file_path) {
    echo "连接到WebSocket服务器\n";

    // 启动异步接收WebSocket消息的线程
    $conn->on('message', function($msg) use ($conn, $loop, $audio_file_path) {
        $response = json_decode($msg, true);

        if (isset($response['header']['event'])) {
            handleEvent($conn, $response, $loop, $audio_file_path);
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
    $taskId = generateTaskId();

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
            "model" => "qwen-audio-3.0-asr-flash-streaming",
            "parameters" => [
                "format" => "wav",
                "sample_rate" => 16000
            ],
            "input" => []
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
            "input" => []
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
function handleEvent($conn, $response, $loop, $audio_file_path) {
    static $taskId;
    static $chunks;
    static $allChunksSent = false;

    if (is_null($taskId)) {
        $taskId = generateTaskId();
    }

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
            $chunks = splitAudioData($voiceData, 1024);

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
                echo "任务计费时长（秒）：" . $response['payload']['usage']['duration'] . "\n";
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

#### Go

```
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

const (
	// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
	wsURL     = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference" // WebSocket服务器地址
	audioFile = "{YOUR_AUDIO_FILE}"                                   // 替换为您的音频文件路径
)

var dialer = websocket.DefaultDialer

func main() {
	// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
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

	buf := make([]byte, 1024)
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
			fmt.Println("任务计费时长（秒）：", event.Payload.Usage.Duration)
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

#### Qwen3-ASR-Flash-Realtime

**说明**示例代码读取 `your_audio_file.pcm`（PCM16、16 kHz、单声道）。如仅有 MP3/WAV 等格式，可使用 ffmpeg 转换：

```
ffmpeg -i your_audio.mp3 -ar 16000 -ac 1 -f s16le your_audio_file.pcm
```

**说明**使用非 VAD（Manual）模式时，建议单次会话持续发送的音频时长累加不超过 60 秒。

#### Python

在运行示例前，请确保已使用以下命令安装依赖：

```
pip uninstall websocket-client
pip uninstall websocket
pip install websocket-client
```

请不要将示例代码文件命名为 `websocket.py`，这会与 websocket 库产生命名冲突，导致如下错误：`AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?`。

```
# pip install websocket-client
import os
import time
import json
import threading
import base64
import websocket
import logging
import logging.handlers
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：API_KEY="sk-xxx"
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-xxx")
QWEN_MODEL = "qwen3-asr-flash-realtime"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
baseUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
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

local_audio_path = "your_audio_file.pcm"
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

#### Java

在运行示例前，请确保已安装Java-WebSocket依赖：

Maven

```
<dependency>
    <groupId>org.java-websocket</groupId>
    <artifactId>Java-WebSocket</artifactId>
    <version>1.5.6</version>
</dependency>
```

Gradle

```
implementation 'org.java-websocket:Java-WebSocket:1.5.6'
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
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static final String API_KEY = "sk-xxx"
    private static final String API_KEY = System.getenv().getOrDefault("DASHSCOPE_API_KEY", "sk-xxx");
    private static final String MODEL = "qwen3-asr-flash-realtime";

    // 控制是否使用 VAD 模式
    private static final boolean enableServerVad = true;

    private static final AtomicBoolean isRunning = new AtomicBoolean(true);
    private static WebSocketClient client;

    public static void main(String[] args) throws Exception {
        initLogger();

        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        String baseUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime";
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
        String localAudioPath = "your_audio_file.pcm";
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
// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：const API_KEY = "sk-xxx"
const API_KEY = process.env.DASHSCOPE_API_KEY || 'sk-xxx';
const MODEL = 'qwen3-asr-flash-realtime';
const enableServerVad = true; // true为VAD模式，false为Manual模式
const localAudioPath = 'your_audio_file.pcm'; // PCM16、16kHz音频文件路径

// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
const baseUrl = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime';
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

#### C#

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

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static readonly string ApiKey = "sk-xxx"
    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
    private const string Model = "qwen3-asr-flash-realtime";
    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    private const string BaseUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime";
    private const string AudioFilePath = "your_audio_file.pcm"; // 替换为您的PCM音频文件路径

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

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$api_key = "sk-xxx"
$api_key = getenv("DASHSCOPE_API_KEY");
$model = 'qwen3-asr-flash-realtime';
// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
$base_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime';
$websocket_url = $base_url . '?model=' . $model;
$audio_file_path = 'your_audio_file.pcm'; // 替换为您的PCM音频文件路径

// 控制是否使用 VAD 模式
$enable_server_vad = true;

$loop = Loop::get();
$socketConnector = new SocketConnector($loop, [
    // 警告：关闭 TLS 证书校验存在中间人攻击风险，仅限本地调试；生产环境务必将 verify_peer/verify_peer_name 设为 true
    'tls' => ['verify_peer' => false, 'verify_peer_name' => false],
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

#### Go

在运行示例前，请确保已安装相关依赖：

```
go get github.com/gorilla/websocket
```
```
package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/websocket"
)

const (
	// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
	baseURL         = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
	model           = "qwen3-asr-flash-realtime"
	audioFile       = "your_audio_file.pcm" // 替换为您的PCM音频文件路径
	enableServerVad = true                  // 控制是否使用 VAD 模式
)

// 服务端事件结构
type ServerEvent struct {
	Type       string `json:"type"`
	Transcript string `json:"transcript,omitempty"`
}

func main() {
	// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
	// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
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

#### Paraformer

Paraformer示例代码和Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime相似，将model替换成Paraformer模型名即可。

## 应用于生产环境

### 连接复用（WebSocket）

Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime 和 Paraformer 的 WebSocket 连接支持复用：一个识别任务结束后，无需重新建立连接即可开启下一个任务。

**复用流程**：客户端发送 `finish-task`，服务端返回 `task-finished` 后，可重新发送 `run-task` 开启新任务。

**重要**

1.  必须等服务端返回 `task-finished` 事件后才可发起新任务。
2.  复用连接中的不同任务需要使用不同的 `task_id`。
3.  任务失败时服务端返回错误事件并关闭连接，该连接不可复用。
4.  任务结束后 60 秒无新任务，连接自动断开。

Qwen3-ASR-Flash-Realtime 采用会话模式，每次会话结束后需主动断开连接，不支持连接复用。

各模型事件说明请参见对应的[API参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#c09d428f2crac)。

### 高并发最佳实践

DashScope SDK 内置池化机制，可复用 WebSocket 连接和识别对象，避免频繁创建销毁带来的开销。

**重要**目前仅 Java SDK 支持此功能。

点击查看高并发最佳实践

#### 前提条件

-   [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   已安装符合版本要求的 DashScope SDK，建议[安装最新版](raw/model-api-reference/preparations/install-sdk.md)：Java SDK 版本≥2.16.9

Java SDK 通过内置的连接池和自定义的对象池协同工作，实现最佳性能：

-   **连接池**：SDK 内部集成的 OkHttp3 连接池，负责管理和复用底层的 WebSocket 连接，减少网络握手开销。此功能默认开启。
-   **对象池**：基于 `commons-pool2` 实现，用于维护一组已预先建立好连接的 `Recognition` 对象。从池中获取对象可消除连接建立的延迟，显著降低首包延迟。

#### 实现步骤

1.  添加依赖
    
    根据项目构建工具，在依赖配置文件中添加 dashscope-sdk-java 和 commons-pool2。
    
    以 Maven 和 Gradle 为例，配置如下：
    
    #### Maven
    
    1.  打开 Maven 项目的 `pom.xml` 文件。
    2.  在 `<dependencies>` 标签内添加以下依赖信息。
    
    ```
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <!-- 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
        <version>the-latest-version</version>
    </dependency>
    
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-pool2</artifactId>
        <!-- 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2 -->
        <version>the-latest-version</version>
    </dependency>
    ```
    
    1.  保存 `pom.xml` 文件。
    2.  使用 Maven 命令（如 `mvn clean install` 或 `mvn compile`）来更新项目依赖。
    
    #### Gradle
    
    1.  打开 Gradle 项目的 `build.gradle` 文件。
    2.  在 `dependencies` 块内添加以下依赖信息。
    
    ```
    dependencies {
        // 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    
        // 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2
        implementation group: 'org.apache.commons', name: 'commons-pool2', version: 'the-latest-version'
    }
    ```
    
    3.  保存 `build.gradle` 文件。
    4.  在命令行中，切换到项目根目录，执行以下 Gradle 命令来更新项目依赖。
    
    ```
    ./gradlew build --refresh-dependencies
    ```
    
    如果使用 Windows 系统，命令应为：
    
    ```
    gradlew build --refresh-dependencies
    ```
    
2.  配置连接池
    
    通过环境变量配置连接池关键参数：
    
    **环境变量**
    
    **描述**
    
    DASHSCOPE\_CONNECTION\_POOL\_SIZE
    
    连接池大小。
    
    推荐值：峰值并发数的 2 倍以上。
    
    默认值：32。
    
    DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS
    
    最大异步请求数。
    
    推荐值：与 `DASHSCOPE_CONNECTION_POOL_SIZE` 保持一致。
    
    默认值：32。
    
    DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS\_PER\_HOST
    
    单主机最大异步请求数。
    
    推荐值：与 `DASHSCOPE_CONNECTION_POOL_SIZE` 保持一致。
    
    默认值：32。
    
3.  配置对象池
    
    通过环境变量配置对象池大小：
    
    **环境变量**
    
    **描述**
    
    RECOGNITION\_OBJECTPOOL\_SIZE
    
    对象池大小。
    
    推荐值：峰值并发数的 1.5 至 2 倍。
    
    默认值：500。
    
    **重要**
    
    -   对象池的大小（`RECOGNITION_OBJECTPOOL_SIZE`）必须小于或等于连接池的大小（`DASHSCOPE_CONNECTION_POOL_SIZE`）。否则，当对象池请求对象时，若连接池已满，会导致调用线程阻塞。
    -   对象池大小不应超过账户的 QPS（每秒查询率）限制。
    
    通过如下代码创建对象池：
    

```
class RecognitionObjectPool {
    // ……完整示例请参见完整代码
    public static GenericObjectPool<Recognition> getInstance() {
        lock.lock();
        if (recognitionGenericObjectPool == null) {
            int objectPoolSize = getObjectivePoolSize();
            RecognitionObjectFactory recognitionObjectFactory =
                    new RecognitionObjectFactory();
            GenericObjectPoolConfig<Recognition> config =
                    new GenericObjectPoolConfig<>();
            config.setMaxTotal(objectPoolSize);
            config.setMaxIdle(objectPoolSize);
            config.setMinIdle(objectPoolSize);
            recognitionGenericObjectPool =
                    new GenericObjectPool<>(recognitionObjectFactory, config);
        }
        lock.unlock();
        return recognitionGenericObjectPool;
    }
}
```

4.  从对象池中获取 Recognition 对象
    
    未归还的对象数量超过对象池上限时，系统会额外创建新的 `Recognition` 对象。这类新对象需重新建立 WebSocket 连接，无法复用。
    

```
recognizer = RecognitionObjectPool.getInstance().borrowObject();
```

5.  进行语音识别
    
    调用 `Recognition` 对象的 call 或 streamCall 方法进行语音识别。
    
6.  归还 Recognition 对象
    
    语音识别任务结束后，归还 Recognition 对象以供复用。不要归还未完成任务或任务失败的对象。
    

```
RecognitionObjectPool.getInstance().returnObject(recognizer);
```

#### 完整代码

```
package org.alibaba.bailian.example.examples;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    public static void checkoutEnv(String envName, int defaultSize) {
        if (System.getenv(envName) != null) {
            System.out.println("[ENV CHECK]: " + envName + " "
                    + System.getenv(envName));
        } else {
            System.out.println("[ENV CHECK]: " + envName
                    + " Using Default which is " + defaultSize);
        }
    }

    public static void main(String[] args)
            throws NoApiKeyException, InterruptedException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
        checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);
        checkoutEnv(RecognitionObjectPool.RECOGNITION_OBJECTPOOL_SIZE_ENV,
                RecognitionObjectPool.DEFAULT_OBJECT_POOL_SIZE);

        int threadNums = 3;
        String currentDir = System.getProperty("user.dir");
        Path[] filePaths = {
                Paths.get(currentDir, "{YOUR_AUDIO_FILE}"),
                Paths.get(currentDir, "{YOUR_AUDIO_FILE}"),
                Paths.get(currentDir, "{YOUR_AUDIO_FILE}"),
        };
        ExecutorService executorService = Executors.newFixedThreadPool(threadNums);
        for (int i = 0; i < threadNums; i++) {
            executorService.submit(new RealtimeRecognizeTask(filePaths));
        }
        executorService.shutdown();
        executorService.awaitTermination(10, TimeUnit.MINUTES);
        System.exit(0);
    }
}

class RecognitionObjectFactory extends BasePooledObjectFactory<Recognition> {
    public RecognitionObjectFactory() {
        super();
    }

    @Override
    public Recognition create() throws Exception {
        return new Recognition();
    }

    @Override
    public PooledObject<Recognition> wrap(Recognition obj) {
        return new DefaultPooledObject<>(obj);
    }
}

class RecognitionObjectPool {
    public static GenericObjectPool<Recognition> recognitionGenericObjectPool;
    public static String RECOGNITION_OBJECTPOOL_SIZE_ENV =
            "RECOGNITION_OBJECTPOOL_SIZE";
    public static int DEFAULT_OBJECT_POOL_SIZE = 500;
    private static Lock lock = new java.util.concurrent.locks.ReentrantLock();

    public static int getObjectivePoolSize() {
        try {
            Integer n = Integer.parseInt(
                    System.getenv(RECOGNITION_OBJECTPOOL_SIZE_ENV));
            return n;
        } catch (NumberFormatException e) {
            return DEFAULT_OBJECT_POOL_SIZE;
        }
    }

    public static GenericObjectPool<Recognition> getInstance() {
        lock.lock();
        if (recognitionGenericObjectPool == null) {
            int objectPoolSize = getObjectivePoolSize();
            System.out.println("RECOGNITION_OBJECTPOOL_SIZE: "
                    + objectPoolSize);
            RecognitionObjectFactory recognitionObjectFactory =
                    new RecognitionObjectFactory();
            GenericObjectPoolConfig<Recognition> config =
                    new GenericObjectPoolConfig<>();
            config.setMaxTotal(objectPoolSize);
            config.setMaxIdle(objectPoolSize);
            config.setMinIdle(objectPoolSize);
            recognitionGenericObjectPool =
                    new GenericObjectPool<>(recognitionObjectFactory, config);
        }
        lock.unlock();
        return recognitionGenericObjectPool;
    }
}

class RealtimeRecognizeTask implements Runnable {
    private static final Object lock = new Object();
    private Path[] filePaths;

    public RealtimeRecognizeTask(Path[] filePaths) {
        this.filePaths = filePaths;
    }

    private static String getDashScopeApiKey() throws NoApiKeyException {
        String dashScopeApiKey = null;
        try {
            ApiKey apiKey = new ApiKey();
            dashScopeApiKey = ApiKey.getApiKey(null);
        } catch (NoApiKeyException e) {
            System.out.println("No API key found in environment.");
        }
        if (dashScopeApiKey == null) {
            dashScopeApiKey = "your-dashscope-apikey";
        }
        return dashScopeApiKey;
    }

    public void runCallback() {
        for (Path filePath : filePaths) {
            RecognitionParam param = null;
            try {
                param = RecognitionParam.builder()
                        .model("paraformer-realtime-v2")
                        .format("pcm")
                        .sampleRate(16000)
                        .apiKey(getDashScopeApiKey())
                        .build();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }

            Recognition recognizer = null;
            final boolean[] hasError = {false};
            try {
                recognizer = RecognitionObjectPool.getInstance().borrowObject();
                String threadName = Thread.currentThread().getName();

                ResultCallback<RecognitionResult> callback =
                        new ResultCallback<RecognitionResult>() {
                            @Override
                            public void onEvent(RecognitionResult message) {
                                synchronized (lock) {
                                    if (message.isSentenceEnd()) {
                                        System.out.println("[process " + threadName
                                                + "] Fix:" + message.getSentence().getText());
                                    } else {
                                        System.out.println("[process " + threadName
                                                + "] Result: " + message.getSentence().getText());
                                    }
                                }
                            }

                            @Override
                            public void onComplete() {
                                System.out.println("[" + threadName
                                        + "] Recognition complete");
                            }

                            @Override
                            public void onError(Exception e) {
                                System.out.println("[" + threadName
                                        + "] RecognitionCallback error: " + e.getMessage());
                                hasError[0] = true;
                            }
                        };
                System.out.println("[" + threadName
                        + "] Input file_path is: " + filePath);
                FileInputStream fis = null;
                try {
                    fis = new FileInputStream(filePath.toFile());
                } catch (Exception e) {
                    System.out.println("Error when loading file: " + filePath);
                    e.printStackTrace();
                }
                recognizer.call(param, callback);

                // chunk size set to 100 ms for 16KHz sample rate
                byte[] buffer = new byte[3200];
                int bytesRead;
                while ((bytesRead = fis.read(buffer)) != -1) {
                    ByteBuffer byteBuffer;
                    if (bytesRead < buffer.length) {
                        byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
                    } else {
                        byteBuffer = ByteBuffer.wrap(buffer);
                    }
                    recognizer.sendAudioFrame(byteBuffer);
                    Thread.sleep(100);
                    buffer = new byte[3200];
                }
                System.out.println("[" + threadName + "] send audio done");
                recognizer.stop();
                System.out.println("[" + threadName + "] asr task finished");
            } catch (Exception e) {
                e.printStackTrace();
                hasError[0] = true;
            }
            if (recognizer != null) {
                try {
                    if (hasError[0] == true) {
                        recognizer.getDuplexApi().close(1000, "bye");
                        RecognitionObjectPool.getInstance()
                                .invalidateObject(recognizer);
                    } else {
                        RecognitionObjectPool.getInstance()
                                .returnObject(recognizer);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    @Override
    public void run() {
        runCallback();
    }
}
```

#### 推荐配置

以下配置基于在指定规格的阿里云服务器上仅运行 Paraformer 实时语音识别服务的测试结果。其中单机并发数指的是同一时刻正在运行的 Paraformer 实时语音识别任务数（即工作线程数）。

**机器配置（阿里云）**

**单机最大并发数**

**对象池大小**

**连接池大小**

4核8GiB

100

500

2000

8核16GiB

200

500

2000

16核32GiB

400

500

2000

#### 资源管理与异常处理

-   **任务成功**：必须调用 `GenericObjectPool.returnObject()` 将 Recognition 对象归还到池中以便复用。
    
    **重要**不要归还未完成任务或任务失败的 Recognition 对象。
    
-   **任务失败**：当 SDK 内部或业务逻辑抛出异常导致任务中断时，必须执行以下两个操作：
    
    1.  主动关闭底层的 WebSocket 连接
    2.  从对象池中废弃该对象，防止被再次使用

```
// 关闭连接
recognizer.getDuplexApi().close(1000, "bye");
// 在对象池中废弃出现异常的 recognizer
RecognitionObjectPool.getInstance().invalidateObject(recognizer);
```

-   在服务出现 TaskFailed 报错时，不需要额外处理。

#### 调用预热与耗时统计

在对 DashScope Java SDK 进行并发调用延迟等性能评估时，建议在正式测试前执行充分的预热操作。

##### 连接复用机制

DashScope Java SDK 通过全局单例的连接池管理和复用 WebSocket 连接。该机制的工作特点如下：

-   **按需创建**：SDK 不会在服务启动时预创建 WebSocket 连接，而是在首次调用时按需建立。
    
-   **限时复用**：请求完成后，连接将在池中保留最多 60 秒以备复用。
    
    -   若 60 秒内有新请求，将复用现有连接，避免重复握手开销。
    -   若连接空闲超过 60 秒，将被自动关闭以释放资源。

##### 预热的重要性

在以下场景中，连接池中可能没有可复用的活跃连接，导致请求需要新建连接：

-   应用刚启动，尚未发起任何调用。
-   服务空闲时间超过 60 秒，池中连接已因超时而关闭。

在这些场景下，首次或初期请求会触发完整的 WebSocket 建连过程（包括 TCP 握手、TLS 加密协商和协议升级），其端到端延迟会显著高于后续复用连接的请求。

##### 推荐做法

在正式进行性能压测或延迟统计前，请遵循以下预热步骤：

1.  模拟正式测试的并发级别，提前发起一定数量的调用（例如，持续 1~2 分钟），以充分填充连接池。
2.  确认连接池已建立并维持足够的活跃连接后，再开始正式的性能数据采集。

### 提升识别效果

-   **选择匹配采样率的模型**：8kHz 电话音频直接使用 8kHz 模型，避免升采样到 16kHz 造成的信息失真。
-   **优化输入音频质量**：使用高质量麦克风，确保录音环境信噪比高、无回声。可在应用层集成降噪（如 RNNoise）、回声消除（AEC）等算法做预处理。

### 设置容错策略

-   **客户端重连**：客户端应实现断线自动重连机制，以应对网络抖动。Python SDK 参考实现如下：
    
    1.  捕获异常：在`Callback`类中实现`on_error`方法。当`dashscope` SDK遇到网络错误或其他问题时，会调用该方法。
    2.  状态通知：当`on_error`被触发时，设置重连信号。在Python中可以使用`threading.Event`，它是一种线程安全的信号标志。
    3.  重连循环：将主逻辑包裹在一个`for`循环中（例如重试3次）。当检测到重连信号后，当前轮次的识别会中断，清理资源，然后等待几秒钟，再次进入循环，创建一个全新的连接。
-   **设置心跳防止连接断开：**当需要与服务端保持长连接时，可将参数[heartbeat](raw/_short/paraformer-real-time-speech-recognition-python-s-145dc2b30661b050.md)设置为`true`，即使音频中长时间没有声音，与服务端的连接也不会中断。
    
-   **模型限流**：在调用模型接口时请注意模型的[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)规则。
    

## 支持的模型与地域

#### 华北2（北京）

调用以下模型时，请选择北京地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-3.1-ASR-Flash-Streaming：**qwen-audio-3.1-asr-flash-streaming
    
-   **Qwen-Audio-3.0-ASR-Flash-Streaming：**qwen-audio-3.0-asr-flash-streaming
    
-   **Fun-ASR-Realtime**：
    
    -   fun-asr-realtime（稳定版，当前等同fun-asr-realtime-2025-11-07）、fun-asr-realtime-2026-02-28（最新快照版）、fun-asr-realtime-2025-11-07（快照版）、fun-asr-realtime-2025-09-15（快照版）
    -   fun-asr-flash-8k-realtime（稳定版，当前等同fun-asr-flash-8k-realtime-2026-01-28）、fun-asr-flash-8k-realtime-2026-01-28
-   **Qwen3-ASR-Flash-Realtime**：qwen3-asr-flash-realtime（稳定版，当前等同qwen3-asr-flash-realtime-2025-10-27）、qwen3-asr-flash-realtime-2026-02-10（最新快照版）、qwen3-asr-flash-realtime-2025-10-27（快照版）
    
-   **Paraformer**：paraformer-realtime-v2、paraformer-realtime-v1、paraformer-realtime-8k-v2、paraformer-realtime-8k-v1
    

#### 新加坡

调用以下模型时，请选择新加坡地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-3.1-ASR-Flash-Streaming：**qwen-audio-3.1-asr-flash-streaming
-   **Qwen-Audio-3.0-ASR-Flash-Streaming：**qwen-audio-3.0-asr-flash-streaming
-   **Fun-ASR-Realtime**：fun-asr-realtime（稳定版，当前等同fun-asr-realtime-2025-11-07）、fun-asr-realtime-2025-11-07（快照版）
-   **Qwen3-ASR-Flash-Realtime**：qwen3-asr-flash-realtime（稳定版，当前等同qwen3-asr-flash-realtime-2025-10-27）、qwen3-asr-flash-realtime-2026-02-10（最新快照版）、qwen3-asr-flash-realtime-2025-10-27（快照版）

## API参考

通过 AOQ 接入的流程和示例，请参见[AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)。支持的模型及版本请参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。

-   [实时语音识别-Qwen-Audio-ASR-Streaming API参考](raw/_short/qwen-audio-asr-streaming-model-access-38a48d03960dfb9a.md)
-   [实时语音识别-Fun-ASR-Realtime API参考](raw/_short/fun-asr-realtime-model-access-3d1392d9c101b199.md)
-   [实时语音识别-Qwen3-ASR-Flash-Realtime API参考](raw/_short/qwen-asr-realtime-api-18aa3c2b3386c250.md)
-   [实时语音识别-Paraformer API参考](raw/_short/paraformer-real-time-speech-recognition-api-refe-79877d5c8ef469f7.md)

## 常见问题

### 实时语音识别支持哪些音频格式？

Qwen-Audio-3.x-ASR-Flash-Streaming、Fun-ASR-Realtime 和 Paraformer 模型支持 pcm、wav、mp3、opus、speex、aac、amr 格式。**Qwen3-ASR-Flash-Realtime 模型推荐使用 pcm 或 opus 格式**；其他格式（如 wav、aac、amr）虽然在 `session.update` 校验层会被接受，但服务端实际解码可能失败，请务必确认音频流为推荐格式后再发送。

### SDK 和 WebSocket API 有什么区别？该如何选择？

DashScope SDK 封装了 WebSocket 连接管理、鉴权、重连等细节，适合快速集成。WebSocket API 直连提供更细粒度的控制能力，适用于 SDK 未覆盖的编程语言或需要自定义连接管理的场景。推荐优先使用 SDK。

### 如何提升专有名词的识别准确率？

使用热词或上下文增强。详细的配置方法和使用说明，请参见[提升识别准确率](raw/model-user-guide/model-experience/speech-recognition/improve-asr-accuracy.md)。

### 连接经常断开怎么办？

建议实现客户端重连机制，并开启心跳参数（`heartbeat=true`）防止长时间无音频导致连接断开。详细的容错策略请参见[应用于生产环境](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt01_production_h2)。

## 模型应用上架及备案

参见[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

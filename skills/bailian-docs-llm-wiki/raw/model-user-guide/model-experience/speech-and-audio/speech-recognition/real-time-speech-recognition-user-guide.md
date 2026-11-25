# 实时语音识别

了解实时语音识别的模型特性、音频流调用方式和识别效果优化方法。

<a id="功能介绍"></a>

<a id="f5d833b6cdu29"></a>

## 功能介绍

实时语音识别支持持续输入音频、返回转写文本，适用于语音输入、会议记录和实时字幕等场景。

-   **多语言与方言**：支持自动语种检测，识别多种语言及中文方言，具体范围参见[语音识别概述](asr-model.md#asr_all02)。
-   **语音检测**：自动检测语音起止，并支持调整语音与噪音的判定阈值，适配不同拾音环境。
-   **文本处理**：支持标点预测，可保留方言表达，或通过文本润色整理口语中的语气词、重复和自我纠正。
-   **准确率优化**：使用热词辅助识别人名、品牌名等特定词汇，通过上下文补充对话信息。
-   **结构化结果**：返回句子识别结果及时间戳，供字幕展示、文本保存和音频定位使用。
-   **音频输入**：支持多种音频格式，可按模型支持范围选择采样率。

> **说明**
>
> 各模型支持的能力有所不同，请核对对应功能的适用范围。已有完整录音文件需要一次提交时，参见[非实时语音识别](non-realtime-speech-recognition-user-guide.md)。

| 使用场景 | 推荐模型 | 结果特点 |
| --- | --- | --- |
| 会议、课堂、字幕等持续转写 | [qwen-audio-3.1-asr-flash-streaming](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-streaming) | 返回中间结果与最终结果，适合边说边查看和更新文本。 |
| 语音输入法、语音消息等短段语音输入 | [qwen-audio-3.1-asr-flash-message](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-message) | 默认返回句子最终结果，可分别开启中间结果和文本润色。 |

<a id="开始使用"></a>

<a id="a1f78ed641n8r"></a>

<a id="rt02_prereq_h2"></a>

## 开始使用

[安装 DashScope SDK](../../../../model-api-reference/preparations/install-sdk.md)，在控制台[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)，并配置 `DASHSCOPE_API_KEY` 环境变量。

下载[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)，在运行目录中保存为 `asr_example.wav`。该音频为 16 kHz、单声道、16-bit PCM 编码的 WAV 文件。以下示例从文件分块发送音频，模拟实时输入，无需麦克风。

<a id="sec-tabs"></a>

<a id="qwen-audio-asr-streaming"></a>

<a id="qwen-audio-asr-streaming-h4"></a>

#### Qwen-Audio-ASR-Streaming

示例使用 qwen-audio-3.1-asr-flash-streaming，通过 DashScope SDK 持续发送音频，同时接收并打印中间结果和最终结果。音频输入结束后，等待剩余结果和任务完成，再关闭连接。

<a id="fig-code-group"></a>

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.atomic.AtomicReference;

public class Main {
    public static void main(String[] args) throws Exception {
        Constants.baseWebsocketApiUrl =
            "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        RecognitionParam param = RecognitionParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen-audio-3.1-asr-flash-streaming")
            .format("wav")
            .sampleRate(16000)
            .build();
        Recognition recognition = new Recognition();
        AtomicReference<Exception> failure = new AtomicReference<>();
        ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
            @Override
            public void onEvent(RecognitionResult result) {
                if (result.getSentence() != null && result.getSentence().getText() != null
                        && !result.getSentence().getText().isEmpty()) {
                    System.out.println(result.getSentence());
                }
            }
            @Override
            public void onComplete() {}
            @Override
            public void onError(Exception error) {
                failure.set(error);
            }
        };
        try {
            recognition.call(param, callback);
            try (InputStream audio = Files.newInputStream(Paths.get("asr_example.wav"))) {
                byte[] buffer = new byte[3200];
                int size;
                while ((size = audio.read(buffer)) != -1) {
                    recognition.sendAudioFrame(ByteBuffer.wrap(buffer, 0, size));
                    Thread.sleep(100);
                }
            }
            recognition.stop();
            if (failure.get() != null) throw failure.get();
        } finally {
            if (recognition.getDuplexApi() != null) {
                recognition.getDuplexApi().close(1000, "bye");
            }
        }
        System.exit(0);
    }
}
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
import os
import time
from concurrent.futures import ThreadPoolExecutor
import dashscope

client = dashscope.Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1",
)

def receive_results(recognition):
    for event in recognition.events():
        payload = event.get("payload") or {}
        sentence = (payload.get("output") or {}).get("sentence") or {}
        if sentence.get("text") and not sentence.get("heartbeat"):
            print(sentence)

with client.audio.asr.recognize(
    ws_url="wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    model="qwen-audio-3.1-asr-flash-streaming",
    format="wav",
    sample_rate=16000,
) as recognition:
    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_results, recognition)
        try:
            with open("asr_example.wav", "rb") as audio:
                while chunk := audio.read(3200):
                    recognition.send_audio_frame(chunk)
                    time.sleep(0.1)
            recognition.stop()
            receiver.result()
        finally:
            recognition.close()
```

<a id="qwen-audio-asr-message"></a>

<a id="qwen-audio-asr-message-h4"></a>

#### Qwen-Audio-ASR-Message

示例使用 qwen-audio-3.1-asr-flash-message，通过 DashScope SDK 持续发送音频，默认接收并打印句子的最终结果。音频输入结束后，等待剩余结果和任务完成，再关闭连接。

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-java-tab"></a>

Java

<a id="code-code-group-2-java"></a>

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.atomic.AtomicReference;

public class Main {
    public static void main(String[] args) throws Exception {
        Constants.baseWebsocketApiUrl =
            "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        RecognitionParam param = RecognitionParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen-audio-3.1-asr-flash-message")
            .format("wav")
            .sampleRate(16000)
            .build();
        Recognition recognition = new Recognition();
        AtomicReference<Exception> failure = new AtomicReference<>();
        ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
            @Override
            public void onEvent(RecognitionResult result) {
                if (result.getSentence() != null && result.getSentence().getText() != null
                        && !result.getSentence().getText().isEmpty()) {
                    System.out.println(result.getSentence());
                }
            }
            @Override
            public void onComplete() {}
            @Override
            public void onError(Exception error) {
                failure.set(error);
            }
        };
        try {
            recognition.call(param, callback);
            try (InputStream audio = Files.newInputStream(Paths.get("asr_example.wav"))) {
                byte[] buffer = new byte[3200];
                int size;
                while ((size = audio.read(buffer)) != -1) {
                    recognition.sendAudioFrame(ByteBuffer.wrap(buffer, 0, size));
                    Thread.sleep(100);
                }
            }
            recognition.stop();
            if (failure.get() != null) throw failure.get();
        } finally {
            if (recognition.getDuplexApi() != null) {
                recognition.getDuplexApi().close(1000, "bye");
            }
        }
        System.exit(0);
    }
}
```

<a id="fig-code-group-2-python-tab"></a>

Python

<a id="code-code-group-2-python"></a>

```python
import os
import time
from concurrent.futures import ThreadPoolExecutor
import dashscope

client = dashscope.Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1",
)

def receive_results(recognition):
    for event in recognition.events():
        payload = event.get("payload") or {}
        sentence = (payload.get("output") or {}).get("sentence") or {}
        if sentence.get("text") and not sentence.get("heartbeat"):
            print(sentence)

with client.audio.asr.recognize(
    ws_url="wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    model="qwen-audio-3.1-asr-flash-message",
    format="wav",
    sample_rate=16000,
) as recognition:
    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_results, recognition)
        try:
            with open("asr_example.wav", "rb") as audio:
                while chunk := audio.read(3200):
                    recognition.send_audio_frame(chunk)
                    time.sleep(0.1)
            recognition.stop()
            receiver.result()
        finally:
            recognition.close()
```

<a id="处理识别结果"></a>

<a id="results"></a>

<a id="rt03_message_h3"></a>

<a id="rt03_timestamp_h3"></a>

### 处理识别结果

-   **中间结果**：用于实时字幕或输入预览。同一句子的内容可能随识别过程修订，应更新该句的显示文本，避免将每次结果逐条拼接。
    
-   **最终结果**：一句话结束后，用最终结果替换该句的中间结果，再用于保存转写、生成字幕或后续业务处理。
    
    > **说明**
    >
    > Qwen-Audio-ASR-Message 默认仅返回最终结果；需要实时预览时，可开启 `intermediate_result_enabled`。
    
-   **时间戳**：将文字与音频位置对应，用于字幕对齐、关键词高亮或音频跳转。使用最终结果的句级、字词级时间戳，避免依赖尚未确定的中间结束时间；时间戳单位为毫秒。
    
    > **说明**
    >
    > Qwen3-ASR-Flash-Realtime 不返回转写文本的时间戳。
    

<a id="识别效果优化"></a>

<a id="rt03_advanced_h2"></a>

## 识别效果优化

通过调整断句、整理或保留口语表达，以及配置热词和上下文，可改善句子划分与文本可读性，提高特定词汇的识别准确率。

<a id="调整断句"></a>

<a id="rt03_vad_h3"></a>

### 调整断句

VAD（语音活动检测）根据语音后的静音判断一句话何时结束，进而触发最终识别结果。较短的静音阈值适合需要快速响应的语音交互；较长的阈值可容纳句内停顿，但会增加等待时间。可根据说话习惯和交互节奏调整。

<table><thead><tr><th><strong>模型</strong></th><th><strong>配置方式</strong></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.1-asr-flash-message</p></td><td><p>通过 <code>max_sentence_silence</code> 调整断句静音阈值。还可根据实际拾音方式，通过 <code>vad_model</code> 选择近场或远场 VAD 模型：</p><ul><li><p>近场（<code>near_meeting_16k</code>）：说话人与麦克风距离较近，例如使用耳麦的客服通话、手持手机的 App 语音输入。</p></li><li><p>远场（<code>far_field_meeting_16k</code>）：说话人与麦克风距离较远，例如智能音箱语音交互、会议室集中拾音和车载免提语音交互。</p></li></ul></td></tr><tr><td><p>qwen-audio-3.0-asr-flash-streaming、Fun-ASR-Realtime系列</p></td><td><p>通过 <code>max_sentence_silence</code> 调整断句静音阈值。</p></td></tr><tr><td><p>Paraformer</p></td><td><p>使用 VAD 断句时，通过 <code>max_sentence_silence</code> 调整静音阈值；也可通过 <code>semantic_punctuation_enabled</code> 改用语义断句。</p></td></tr><tr><td><p>Qwen3-ASR-Flash-Realtime</p></td><td><p>通过 <code>session.turn_detection</code> 中的 <code>silence_duration_ms</code> 调整断句静音阈值，通过 <code>threshold</code> 调整检测灵敏度；也支持关闭 VAD，由客户端提交音频来控制断句。</p></td></tr></tbody></table>

<a id="文本润色"></a>

<a id="polish"></a>

### 文本润色

语音输入中常包含语气词、重复和自我纠正。文本润色可整理这些表达，使转写文本更适合语音消息、输入法等场景。

qwen-audio-3.1-asr-flash-message 通过 `disfluency_removal_enabled` 控制润色。润色在最终结果中生效，界面应在句子结束时更新为润色后的文本。

<a id="保留方言表达"></a>

<a id="dialect"></a>

### 保留方言表达

识别方言时，可根据用途选择保留方言表达，或转写为普通话文本。例如，方言字幕需要保留原有表达，而面向更广泛读者的文字记录可能需要普通话文本。

qwen-audio-3.1-asr-flash-streaming 和 qwen-audio-3.1-asr-flash-message 通过 `keep_dialect` 控制是否保留方言表达；后者仅在最终结果中生效。

<a id="热词与上下文增强"></a>

<a id="rt03_hotword_h3"></a>

<a id="rt03_ctx_h3"></a>

<a id="rt04_faq_q3_h3"></a>

### 热词与上下文增强

热词用于辅助识别品牌名、人名、专有术语等特定词汇；上下文增强用于补充前几轮对话中的术语和背景。具体配置、支持范围和调优方法参见[提升识别准确率](improve-asr-accuracy.md)。

<a id="敏感词过滤"></a>

<a id="rt03_sensitive_h3"></a>

### 敏感词过滤

敏感词过滤可将识别结果中的指定词汇替换为等长的星号，或从文本中移除，便于处理需要屏蔽的字幕或转写内容。Qwen-Audio-ASR-Streaming 和 Fun-ASR-Realtime 支持通过 `special_word_filter` 配置过滤规则。

<a id="应用于生产环境"></a>

<a id="rt01_production_h2"></a>

<a id="rt03_ws_reuse_h3"></a>

<a id="rt03_hc_h3"></a>

<a id="rt04_faq_h2"></a>

<a id="rt04_faq_q4_h3"></a>

<a id="rt01_prod_improve_h3"></a>

<a id="rt01_prod_resilience_h3"></a>

<a id="rt03_hc_prereq_h4"></a>

<a id="rt03_hc_steps_h4"></a>

<a id="rt03_hc_fullcode_h4"></a>

<a id="rt03_hc_config_h4"></a>

<a id="rt03_hc_resource_h4"></a>

<a id="rt03_hc_warmup_h4"></a>

<a id="rt03_hc_warmup_reuse_h5"></a>

<a id="rt03_hc_warmup_why_h5"></a>

<a id="rt03_hc_warmup_howto_h5"></a>

## 应用于生产环境

将识别能力接入生产环境时，需要结合业务流量管理连接与并发，处理长静音、异常重试和资源释放。音频准备、任务与连接管理、Java 并发处理等实践及完整示例，参见[语音识别最佳实践](speech-recognition-best-practices.md)。

<a id="支持的模型与地域"></a>

<a id="4a43cc1bb7kxg"></a>

## 支持的模型与地域

<a id="sec-tabs-2"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Fun-ASR-Realtime**：
    
    -   fun-asr-realtime（稳定版）、fun-asr-realtime-2026-02-28（最新快照版）
    -   fun-asr-flash-8k-realtime（稳定版，当前等同fun-asr-flash-8k-realtime-2026-01-28）、fun-asr-flash-8k-realtime-2026-01-28
-   **Qwen-ASR-Realtime**：qwen3-asr-flash-realtime（稳定版）
    
-   **Paraformer**：paraformer-realtime-v2、paraformer-realtime-8k-v2
    

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
-   **Fun-ASR-Realtime**：fun-asr-realtime（稳定版）
-   **Qwen-ASR-Realtime**：qwen3-asr-flash-realtime（稳定版）

<a id="使用限制"></a>

<a id="usage-limits"></a>

<a id="rt04_faq_q1_h3"></a>

## 使用限制

实时音频须为单声道。按下表选择音频格式与采样率，并将 `format`、`sample_rate` 设置为实际音频对应的值。

| 模型 | 输入方式 | 音频格式 | 采样率 | 大小/时长 |
| --- | --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming | 二进制流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 任意 | 不限 |
| qwen-audio-3.1-asr-flash-message | 二进制流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 16 kHz | — |
| Fun-ASR-Realtime系列（fun-asr-realtime） | 二进制流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 任意 | 不限 |
| Fun-ASR-Flash-8K-Realtime系列（fun-asr-flash-8k-realtime） | 二进制流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 8 kHz | 不限 |
| qwen3-asr-flash-realtime | JSON 事件中的 Base64 音频 | `pcm`、`opus` | 8 kHz、16 kHz | 不限 |
| paraformer-realtime-v2 | 二进制流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 任意 | 不限 |
| paraformer-realtime-8k-v2 | 二进制流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 8 kHz | 不限 |

音频检查和格式转换参见[准备输入音频](speech-recognition-best-practices.md#audio)。

<a id="api-参考"></a>

<a id="c09d428f2crac"></a>

<a id="rt03_websocket_h3"></a>

<a id="rt03_emotion_h3"></a>

<a id="rt04_faq_q2_h3"></a>

## API 参考

需要低延迟传输、弱网对抗，以及回声消除和降噪能力的实时音频场景，可了解 AOQ 接入方案。协议选型、支持模型和接入方式参见 [Realtime API 概述](../../../../model-api-reference/realtime-api-directory/realtime-api-overview.md)。

-   [Qwen-Audio-ASR-Streaming](../../../../model-api-reference/realtime-api-directory/realtime-asr-model-apis/qwen-audio-asr-streaming-api.md)
-   [Qwen-Audio-ASR-Message](../../../../model-api-reference/realtime-api-directory/realtime-asr-model-apis/qwen-asr-message-api.md)
-   [Fun-ASR-Realtime](../../../../_short/fun-asr-real-time-speech-recognition-api-referen-c1b5c2ef9baf2fd3.md)
-   [Qwen3-ASR-Flash-Realtime](../../../../_short/qwen-asr-realtime-api-8ffee6ce35d13bb5.md)
-   [Paraformer](../../../../_short/paraformer-real-time-speech-recognition-api-refe-fcf57d84158b854c.md)

<a id="模型应用上架及备案"></a>

<a id="6e0358ac2bi17"></a>

## 模型应用上架及备案

参见[应用合规备案](../../../../_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

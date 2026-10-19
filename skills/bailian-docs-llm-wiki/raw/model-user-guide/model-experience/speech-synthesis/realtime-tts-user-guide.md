# 实时语音合成

了解实时语音合成的模型特性、流式调用方法和合成效果优化方式。

## 功能介绍

实时语音合成支持分段输入文本、逐段返回音频，适合将大模型生成的文本实时转换为语音。

-   **多语言与方言**：根据目标语言选择模型和音色，也可通过指令指定方言。参见[方言](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#tts_rt_dialect_h3)。
-   **表现力控制**：通过自然语言指令调整语速、情感等表达，或在文本中插入情感与富语言标签。参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)和[情感与富语言标签](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#rt_emtag_h3)。
-   **自定义音色**：通过[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)从音频样本创建音色，或通过[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)使用文字描述创建音色。
-   **精细控制与公式朗读**：使用 [SSML 与 LaTeX](raw/model-user-guide/model-experience/speech-synthesis/ssml-latex-user-guide.md)控制停顿、发音等效果，或将公式转换为语音。
-   **音频控制**：可调节语速、语调、音量和码率，输出 PCM、WAV、MP3、Opus 等主流音频格式，最高支持 48 kHz 采样率。具体取值与支持范围以对应 API 参数说明为准。

**说明**各模型及音色支持的能力有所不同，使用前请核对对应功能的支持范围。

需要通过 HTTP 一次提交完整文本时，请参见[非实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/non-realtime-tts-user-guide.md)。

## 开始使用

-   [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置到环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt) `DASHSCOPE_API_KEY`。使用与示例地域对应的 API Key。
-   使用业务空间专属域名时，将代码中的 `{WorkspaceId}` 替换为该地域的[业务空间 ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
-   [安装 DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)，选择 Python 或 Java 示例。

**说明**对延迟和弱网下音频传输稳定性要求较高的移动端应用，可使用 AOQ 协议。AOQ 的接入方式，以及 AOQ、WebRTC 和 WebSocket 的差异与模型支持范围，请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### Qwen-Audio-TTS（推荐）

以下使用北京地域的 `qwen-audio-3.1-tts-flash` 和系统音色 `longanhuan_v3.1`，分段发送文本并将返回音频保存为 `output.mp3`。

Python

```
import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback, AudioFormat

dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
dashscope.base_websocket_api_url = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"

with open("output.mp3", "wb") as audio:
    class Callback(ResultCallback):
        def on_data(self, data: bytes):
            audio.write(data)

        def on_error(self, message):
            print(f"Synthesis failed: {message}")

    synthesizer = SpeechSynthesizer(
        model="qwen-audio-3.1-tts-flash",
        voice="longanhuan_v3.1",
        format=AudioFormat.MP3_24000HZ_MONO_256KBPS,
        callback=Callback(),
    )
    for text in ["你好，欢迎使用阿里云百炼。", "文本可以分段发送，音频会逐段返回。"]:
        synthesizer.streaming_call(text)
    synthesizer.streaming_complete()
```

Java

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;

public class Main {
    public static void main(String[] args) throws Exception {
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        try (FileOutputStream audio = new FileOutputStream("output.mp3")) {
            SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-audio-3.1-tts-flash")
                .voice("longanhuan_v3.1")
                .format(SpeechSynthesisAudioFormat.MP3_24000HZ_MONO_256KBPS)
                .build();
            ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<>() {
                @Override
                public void onEvent(SpeechSynthesisResult result) {
                    ByteBuffer buffer = result.getAudioFrame();
                    if (buffer != null) {
                        byte[] bytes = new byte[buffer.remaining()];
                        buffer.get(bytes);
                        try { audio.write(bytes); }
                        catch (Exception e) { throw new RuntimeException(e); }
                    }
                }
                @Override
                public void onComplete() {}
                public void onError(Exception e) { e.printStackTrace(); }
            };
            SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
            try {
                for (String text : new String[]{"你好，欢迎使用阿里云百炼。", "文本可以分段发送，音频会逐段返回。"}) {
                    synthesizer.streamingCall(text);
                }
                synthesizer.streamingComplete(60000);
            } finally {
                synthesizer.getDuplexApi().close(1000, "done");
            }
        }
    }
}
```

#### CosyVoice

以下使用北京地域的 `cosyvoice-v3-flash` 和系统音色 `longanyang`，分段发送文本并将返回音频保存为 `output.mp3`。

Python

```
import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback, AudioFormat

dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
dashscope.base_websocket_api_url = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"

with open("output.mp3", "wb") as audio:
    class Callback(ResultCallback):
        def on_data(self, data: bytes):
            audio.write(data)

        def on_error(self, message):
            print(f"Synthesis failed: {message}")

    synthesizer = SpeechSynthesizer(
        model="cosyvoice-v3-flash",
        voice="longanyang",
        format=AudioFormat.MP3_24000HZ_MONO_256KBPS,
        callback=Callback(),
    )
    for text in ["你好，欢迎使用阿里云百炼。", "文本可以分段发送，音频会逐段返回。"]:
        synthesizer.streaming_call(text)
    synthesizer.streaming_complete()
```

Java

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;

public class Main {
    public static void main(String[] args) throws Exception {
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        try (FileOutputStream audio = new FileOutputStream("output.mp3")) {
            SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("cosyvoice-v3-flash")
                .voice("longanyang")
                .format(SpeechSynthesisAudioFormat.MP3_24000HZ_MONO_256KBPS)
                .build();
            ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<>() {
                @Override
                public void onEvent(SpeechSynthesisResult result) {
                    ByteBuffer buffer = result.getAudioFrame();
                    if (buffer != null) {
                        byte[] bytes = new byte[buffer.remaining()];
                        buffer.get(bytes);
                        try { audio.write(bytes); }
                        catch (Exception e) { throw new RuntimeException(e); }
                    }
                }
                @Override
                public void onComplete() {}
                public void onError(Exception e) { e.printStackTrace(); }
            };
            SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
            try {
                for (String text : new String[]{"你好，欢迎使用阿里云百炼。", "文本可以分段发送，音频会逐段返回。"}) {
                    synthesizer.streamingCall(text);
                }
                synthesizer.streamingComplete(60000);
            } finally {
                synthesizer.getDuplexApi().close(1000, "done");
            }
        }
    }
}
```

## 合成效果优化

### 语言与发音

根据需要控制的内容，选择对应方式：

**需求**

**使用方式**

指定合成语音的目标语言

使用 `language_hints` 指定整体合成语言，帮助模型按目标语言朗读数字、缩写和符号，改善小语种合成效果。

修正特定词语的发音或替换文本

使用 `hot_fix` 为指定词语标注拼音，或在合成前将词语替换为目标文本。适合统一修正专有名词等局部内容。

精细控制停顿、数字读法或字词发音

使用 SSML 标签标记需要控制的文本，按标签设置停顿、读法和发音等效果。

朗读数学公式

使用 CosyVoice 的 LaTeX 公式朗读功能，将支持的数学公式转换为中文语音。

参数适用模型和配置方法请参见 [Qwen-Audio-TTS API](raw/_short/qwen-audio-tts-client-events-81541f7ec0ef1c33.md)或 [CosyVoice API](raw/_short/cosyvoice-client-events-a63a525ab07e6693.md)；SSML 与 LaTeX 的适用模型、音色、接口及用法请参见 [SSML 与 LaTeX](raw/model-user-guide/model-experience/speech-synthesis/ssml-latex-user-guide.md)。

**说明**使用 SSML 时，需要一次提交完整的 SSML 文本，再逐段接收音频，不支持分段输入。

### 指令控制

通过 `instruction` 参数，用自然语言描述语速、情感或说话方式，控制合成语音的表现。

**说明**如需创建具有特定性别、年龄或音色特质的新音色，或参考声音描述的编写建议与示例，请参见[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)。

#### Qwen-Audio-TTS

`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash` 的系统音色、复刻音色和设计音色均支持在合成请求中通过 `instruction` 设置自然语言指令。

例如，将 `instruction` 设为以下内容，可放慢语速：

```
请用非常缓慢的语速说话，每个字都慢慢说。
```

#### CosyVoice

**说明**CosyVoice 的 `instruction` 长度不能超过 100 个字符。计数时，汉字（包括简体、繁体汉字、日文汉字和韩文汉字）按 2 个字符计算，其他字符（包括标点符号、字母、数字、假名和谚文）按 1 个字符计算。

**模型**

**可使用的音色**

**指令要求**

**指令文本语言**

`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`

复刻音色、设计音色

无系统音色。

自然语言指令。

中文、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语。

`cosyvoice-v3-plus`

系统音色

按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中的固定格式和内容填写。

复刻音色、设计音色不支持指令控制。

按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)指定的语言填写。

`cosyvoice-v3-flash`

系统音色

按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中的固定格式和内容填写。

中文。

复刻音色、设计音色

自然语言指令。

中文、英文、法语、德语、日语、韩语、俄语。

### 方言

通过方言功能，可将文本合成为河南话、四川话等中文方言语音。方言的选择方式取决于模型和音色类型。

#### Qwen-Audio-TTS

-   **系统音色**：从 [Qwen-Audio-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)中选择支持目标方言的音色。直接支持该方言的音色无需额外设置；支持方言指令的音色使用 `instruction` 指定。
-   **复刻音色**：通过 `instruction` 指定方言，例如 `请用河南话表达。`。

#### CosyVoice

-   **系统音色**：选择直接支持目标方言的音色，例如 `longshange_v3`；或选择支持方言指令的音色，例如 `longanhuan_v3`，按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)的格式填写指令。
-   **复刻音色**：使用支持指令控制的模型，通过 `instruction` 指定方言。
-   **设计音色**：暂不支持方言。

使用 CosyVoice 的 Python 开始使用示例时，将初始化与文本发送部分替换为以下内容，可使用 `longanhuan_v3` 输出河南话：

```
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="longanhuan_v3",
    instruction="请用河南话表达。",
    format=AudioFormat.MP3_24000HZ_MONO_256KBPS,
    callback=Callback(),
)
synthesizer.streaming_call("叫你去买盐，你买回来一袋面，这不是弄啥嘞吗！")
synthesizer.streaming_complete()
```

使用 Qwen3-TTS 时，请从 [Qwen3-TTS 音色列表](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list#0ad0bfdd635ar)中选择支持目标方言的音色。

### 情感与富语言标签

**说明**适用于 `qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash`。

情感与富语言标签可控制语音的情感和风格，并在指定位置加入笑声、叹息等拟声效果。将标签直接写入待合成文本 `text`，无需额外参数。

#### 使用示例

以下文本先使用兴奋语气，在指定位置插入笑声后继续合成正文：

```
[excited]今天的天气真不错！[laughing]我们一起出去玩吧！
```

以下文本在第二句切换为兴奋语气：

```
[serious]请注意安全事项。[excited]好了，现在让我们开始吧！
```

#### 支持标签

#### 控制类标签

控制类标签设置后续文本的情感或风格，直到出现下一个控制类标签；长句被自动切分时，作用范围以切分后的文本为界。

**标签**

**说明**

`[sad]`

悲伤

`[amazed]`

惊叹

`[deep and loud shouting]`

深沉大声呐喊

`[trembling]`

颤抖

`[angry]`

愤怒

`[excited]`

兴奋

`[sarcastic]`

讽刺

`[curious]`

好奇

`[like dracula]`

吸血鬼语气

`[bored]`

无聊

`[tired]`

疲倦

`[scornful]`

轻蔑

`[shouting]`

大喊

`[asmr]`

ASMR 轻声

`[panicked]`

惊慌

`[mischievously]`

调皮

`[empathetic]`

共情

`[whispers]`

低声耳语

`[reluctantly]`

不情愿

`[crying]`

哭泣

`[serious]`

严肃

`[very slowly]`

非常缓慢

`[very fast]`

非常快速

#### 富语言类标签

富语言类标签在当前位置插入拟声效果，不改变前后文本的情感风格。

**标签**

**说明**

`[gasp]`

倒吸气

`[sighing]`

叹息

`[clears throat]`

清嗓

`[giggles]`

咯咯笑

`[laughing]`

大笑

`[cough]`

咳嗽

`[snorts]`

哼声、嗤笑

## 应用于生产环境

### 取消任务

使用 Qwen-Audio-TTS 或 CosyVoice 模型时，如需中断当前轮次合成，可发送取消指令。服务端会结束当前任务并返回 `task-finished`。

**调用方式**

**版本要求**

**使用方法**

Python SDK

1.26.4 及以上版本

调用 `SpeechSynthesizer.streaming_cancel()`。

Java SDK

2.22.26 及以上版本

调用 `SpeechSynthesizer.streamingCancel()`。

WebSocket 原始协议

无需 SDK

发送 `finish-task` 事件，并在 `input` 中设置 `directive=cancel`。

### WebSocket 连接复用

同一 WebSocket 连接可顺序处理多轮合成，各模型系列开启下一轮的方式如下：

**模型系列**

**本轮结束信号**

**开启下一轮**

Qwen-Audio-TTS、CosyVoice

`task-finished`

必须使用新的 `task_id` 发送 `run-task`，再按该系列的流程发送文本。取消任务后也按此流程复用连接。

**说明**使用 Python SDK 调用 Qwen-Audio-TTS 或 CosyVoice 时，直接创建的 `SpeechSynthesizer` 会在任务结束或取消后关闭连接。需要复用连接时，从 `SpeechSynthesizerObjectPool` 借出对象。

Sambert

`task-finished`

必须使用新的 `task_id` 发送 `run-task`，并在该事件中携带本轮完整文本，无需发送 `continue-task` 或 `finish-task`。

Qwen3-TTS

`response.done`

在当前会话中继续发送 `input_text_buffer.append`。根据会话模式，由服务端触发合成或发送 `input_text_buffer.commit`；全部文本发送完毕后再发送 `session.finish` 结束会话。

SDK 对象池的配置与完整示例请参见[语音合成高并发最佳实践](raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)。Qwen3-TTS 的会话流程请参见 [WebSocket API](raw/_short/interactive-process-of-qwen-tts-realtime-synthes-3c96d28349bb779a.md)。

Qwen-Audio-TTS、CosyVoice、Sambert 任务结束后 60 秒内没有新任务时，连接会自动断开。连接已关闭或任务状态异常时，应重新建立连接。

### 模型限流

按对应模型的限流规则控制请求频率和并发数。限流条件、常见报错及处理方法请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 高并发最佳实践

通过对象池复用合成对象与连接，并按业务需求配置并发、预热和异常处理，具体请参见[语音合成高并发最佳实践](raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)。

## 支持模型

#### 华北2（北京）

使用该地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 和[接入域名](raw/model-user-guide/get-started-with-models/regions.md)调用以下模型：

-   **Qwen-Audio-TTS**：qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
-   **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2
-   **Qwen3-TTS**：qwen3-tts-flash-realtime
-   **Sambert**：sambert-zhinan-v1、sambert-zhiqi-v1、sambert-zhichu-v1、sambert-zhide-v1、sambert-zhijia-v1、sambert-zhiru-v1、sambert-zhiqian-v1、sambert-zhixiang-v1、sambert-zhiwei-v1、sambert-zhihao-v1、sambert-zhijing-v1、sambert-zhiming-v1、sambert-zhimo-v1、sambert-zhina-v1、sambert-zhishu-v1、sambert-zhistella-v1、sambert-zhiting-v1、sambert-zhixiao-v1、sambert-zhiya-v1、sambert-zhiye-v1、sambert-zhiying-v1、sambert-zhiyuan-v1、sambert-zhiyue-v1、sambert-zhigui-v1、sambert-zhishuo-v1、sambert-zhimiao-emo-v1、sambert-zhimao-v1、sambert-zhilun-v1、sambert-zhifei-v1、sambert-zhida-v1、sambert-camila-v1、sambert-perla-v1、sambert-indah-v1、sambert-clara-v1、sambert-hanna-v1、sambert-beth-v1、sambert-betty-v1、sambert-cally-v1、sambert-cindy-v1、sambert-eva-v1、sambert-donna-v1、sambert-brian-v1、sambert-waan-v1，请参见[Sambert模型列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi)

#### 新加坡

使用该地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 和[接入域名](raw/model-user-guide/get-started-with-models/regions.md)调用以下模型：

-   **Qwen-Audio-TTS**：qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
-   **CosyVoice**：cosyvoice-v3-plus、cosyvoice-v3-flash
-   **Qwen3-TTS**：qwen3-tts-flash-realtime

系统音色与试听分别参见 [Qwen-Audio-TTS](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)、[CosyVoice](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)、[Qwen3-TTS](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list#0ad0bfdd635ar) 和 [Sambert](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi) 音色列表。使用复刻或设计音色时，合成模型须与创建音色时指定的目标模型一致。

## API 参考

通过 AOQ 接入的流程和示例，请参见[AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)。支持的模型及版本请参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。

-   [实时语音合成-Qwen-Audio-TTS API参考](raw/_short/qwen-audio-tts-api-2a5997e924bff673.md)
-   [实时语音合成-CosyVoice API参考](raw/_short/cosyvoice-large-model-for-speech-synthesis-c25d07a9b3ba6047.md)
-   [实时语音合成-千问API参考](raw/_short/qwen-tts-realtime-api-reference-5bfb7590608ff1dc.md)
-   [实时语音合成-Sambert API参考](raw/_short/sambert-speech-synthesis-60d77f54e64567a1.md)

WebSocket 原始协议的完整调用示例见以下文档。

-   [Qwen-Audio-TTS WebSocket](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-websocket-api#ws-examples)
    
-   [CosyVoice WebSocket](https://help.aliyun.com/zh/model-studio/cosyvoice-websocket-api#ws-examples)
    
-   [Qwen3-TTS WebSocket](https://help.aliyun.com/zh/model-studio/interactive-process-of-qwen-tts-realtime-synthesis#ws-examples)
    
-   [Sambert WebSocket](https://help.aliyun.com/zh/model-studio/sambert-websocket-api#ws-examples)
    

## 常见问题

### 使用复刻音色生成的音频无声音如何排查？

确认 `voice` 为创建成功的音色 ID，创建音色时的 `target_model` 与合成时的 `model` 一致。音色状态、源音频要求及质量建议请参见[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)。

### 为什么语音合成的实际时长与 WAV 文件显示的时长不一致？

流式返回 WAV 时，文件头可能无法反映最终音频长度。如需准确的时长信息，可将 `format` 设为 `pcm`，接收完整音频后添加包含实际长度的 WAV 文件头。

### 为什么音频无法播放？

请按以下场景逐一排查：

1.  音频保存为完整文件（如 xx.mp3）的情况
    
    1.  音频格式一致性：请求参数中的音频格式须与文件后缀一致（如参数为 wav 则文件须为 .wav）。
    2.  播放器兼容性：确认播放器支持该音频的格式和采样率。
2.  流式播放音频的情况
    
    1.  将音频流保存为完整文件，尝试用播放器播放。如果文件无法播放，请参考场景 1 的排查方法。
    2.  如果文件可正常播放，则问题在流式播放实现。请确认播放器支持流式播放（如 ffmpeg、pyaudio、AudioFormat、MediaSource 等）。

### 为什么音频播放卡顿？

请按以下步骤逐一排查：

1.  检查文本发送速度：确保发送间隔合理，避免上段音频播完后下段文本尚未到达。
    
2.  检查回调函数性能：
    
    -   确认回调函数中无阻塞性业务逻辑。
    -   回调运行在 WebSocket 线程，阻塞会影响数据接收。建议将音频数据写入独立缓冲区，在其他线程中处理。
3.  检查网络稳定性：网络波动可能导致音频传输中断或延迟。
    

### 语音合成耗时较长是什么原因？

分段输入时，过长的文本发送间隔会增加合成总时长；首次调用还包含 WebSocket 建连开销。高并发场景下的预热与耗时统计，请参见[语音合成高并发最佳实践](https://help.aliyun.com/zh/model-studio/tts-high-concurrency-best-practices#warm-up)。

### 如何限制 API Key 仅用于语音合成服务（权限隔离）？

通过新建业务空间并仅授权特定模型，可限制 API Key 的使用范围。请参见[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

### 子业务空间的 API Key 能否调用 Qwen-Audio-TTS/CosyVoice 模型？

默认业务空间下，所有模型均可调用。

子业务空间下，需要为 API Key 对应的子业务空间进行[模型授权](https://help.aliyun.com/zh/model-studio/model-authentication-instructions)。请参见[子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

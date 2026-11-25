# Qwen-Audio-TTS Java SDK

使用 CosyVoice 时，请参见 [CosyVoice Java SDK](cosyvoice-websocket-sdk-java-a4920147be4869ef.md)。

<a id="前提条件"></a>

## 前提条件

-   [安装 Java SDK](../model-api-reference/preparations/install-sdk.md)
-   [获取并配置 API Key](../model-api-reference/preparations/get-api-key.md)

<a id="接口地址"></a>

<a id="model-qwen-audio-tts-h2-3r8w6k1j"></a>

<a id="shared-1"></a>

### 接口地址

<a id="model-cosyvoice-h2-3r8w6k1j"></a>

SDK的接口地址需在初始化前设置为下方地址（包含WorkspaceId）。如需切换到其他地域，请修改 `Constants.baseWebsocketApiUrl`为对应地域的URL。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<a id="快速开始"></a>

## 快速开始

示例使用北京。将代码中的 `{WorkspaceId}` 替换为实际的[业务空间 ID](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。运行后，音频保存到当前目录的 `output.mp3`。

<a id="code-block"></a>

```java
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class Main {
    // 模型
    private static String model = "qwen-audio-3.0-tts-flash";
    // 音色
    private static String voice = "longanhuan_v3.6";

    public static void streamAudioDataToSpeaker() {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();

        // 同步模式：禁用回调（第二个参数为null）
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        ByteBuffer audio = null;
        try {
            // 阻塞直至音频返回
            audio = synthesizer.call("今天天气怎么样？");
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        if (audio != null) {
            // 将音频数据保存到本地文件"output.mp3"中
            File file = new File("output.mp3");
            // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
            System.out.println(
                    "[Metric] requestId为："
                            + synthesizer.getLastRequestId()
                            + "首包延迟（毫秒）为："
                            + synthesizer.getFirstPackageDelay());
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(audio.array());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

<a id="qwen-audio-tts-cosyvoice"></a>

<a id="model-qwen-audio-tts-6bc2d05715bdk"></a>

<a id="示例代码"></a>

<a id="model-cosyvoice-6bc2d05715bdk"></a>

<a id="示例代码-2"></a>

### Qwen-Audio-TTS / CosyVoice

以下示例使用 Qwen-Audio-TTS。调用 CosyVoice 时，将 `model` 改为 `cosyvoice-v3-plus`，将 `voice` 改为 `longanyang`。

SDK提供了语音合成的关键接口，支持以下几种调用方式：

-   非流式调用：阻塞式，一次性发送完整文本，直接返回完整音频。适合短文本语音合成场景。
-   单向流式调用：非阻塞式，一次性发送完整文本，通过回调函数接收音频数据（可能分片）。适用于对实时性要求高的短文本语音合成场景。
-   双向流式调用：非阻塞式，可分多次发送文本片段，通过回调函数实时接收增量合成的音频流。适合实时性要求高的长文本语音合成场景。

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="sec-tabs-2"></a>

<a id="非流式调用"></a>

<a id="非流式调用-h4"></a>

#### 非流式调用

<a id="model-qwen-audio-tts-82d9324616ifx"></a>

<a id="model-cosyvoice-82d9324616ifx"></a>

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6892567871/CAEQURiBgIDHpsn4phkiIDQ0ZGE2OTk3NmY5NTRhNDVhZDQwNWE3ZGZiMzk4Yjk54709861_20241015153444.149.svg)

发送的文本长度不得超过20000字符。

> **重要**
>
> 每次调用`call`方法前，需要重新初始化`SpeechSynthesizer`实例。

<a id="code-block-2"></a>

```java
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class Main {
    // 模型
    private static String model = "qwen-audio-3.0-tts-flash";
    // 音色
    private static String voice = "longanhuan_v3.6";

    public static void streamAudioDataToSpeaker() {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();

        // 同步模式：禁用回调（第二个参数为null）
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        ByteBuffer audio = null;
        try {
            // 阻塞直至音频返回
            audio = synthesizer.call("今天天气怎么样？");
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        if (audio != null) {
            // 将音频数据保存到本地文件"output.mp3"中
            File file = new File("output.mp3");
            // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
            System.out.println(
                    "[Metric] requestId为："
                            + synthesizer.getLastRequestId()
                            + "首包延迟（毫秒）为："
                            + synthesizer.getFirstPackageDelay());
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(audio.array());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

<a id="单向流式调用"></a>

<a id="单向流式调用-h4"></a>

#### 单向流式调用

<a id="model-qwen-audio-tts-cc2a504f344s2"></a>

<a id="model-cosyvoice-cc2a504f344s2"></a>

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6892567871/CAEQVRiBgMCfo..hrBkiIGEyMjNkZjVlMWZiYzRhZDU4ZjEyZjdjMmMzYjM1YzMz4709861_20241015153444.149.svg)

发送的文本长度不得超过20000字符。

> **重要**
>
> 每次调用`call`方法前，需要重新初始化`SpeechSynthesizer`实例。

<a id="code-block-3"></a>

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.CountDownLatch;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    // 模型
    private static String model = "qwen-audio-3.0-tts-flash";
    // 音色
    private static String voice = "longanhuan_v3.6";

    public static void streamAudioDataToSpeaker() {
        CountDownLatch latch = new CountDownLatch(1);

        // 实现回调接口ResultCallback
        ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
            @Override
            public void onEvent(SpeechSynthesisResult result) {
                if (result.getAudioFrame() != null) {
                    // 此处实现保存音频数据到本地的逻辑
                    System.out.println(TimeUtils.getTimestamp() + " 收到音频");
                }
                // 获取输出信息，包含事件类型和原始文本
                if (result.getOutput() != null && result.getOutput().has("type")) {
                    System.out.println("事件类型: " + result.getOutput().get("type").getAsString()
                            + ", 原始文本: " + (result.getOutput().has("original_text") ? result.getOutput().get("original_text").getAsString() : ""));
                }
            }

            @Override
            public void onComplete() {
                System.out.println(TimeUtils.getTimestamp() + " 收到Complete，语音合成结束");
                latch.countDown();
            }

            @Override
            public void onError(Exception e) {
                System.out.println("出现异常：" + e.toString());
                latch.countDown();
            }
        };

        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();
        // 第二个参数"callback"传入回调即启用异步模式
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
        // 非阻塞调用，立即返回null（实际结果通过回调接口异步传递），在回调接口的onEvent方法中实时获取二进制音频
        try {
            synthesizer.call("今天天气怎么样？");
            // 等待合成完成
            latch.await();
            // 等待播放线程全部播放完
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束后关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

<a id="双向流式调用"></a>

<a id="双向流式调用-h4"></a>

#### 双向流式调用

<a id="model-qwen-audio-tts-ba023aacfbr84"></a>

<a id="model-cosyvoice-ba023aacfbr84"></a>

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6892567871/CAEQVRiBgICHxPGhrBkiIGE3ZTVmMzY0YzI3NzQxYTFiYWE2MmU2NTBhMDgzZGM14709861_20241015153444.149.svg)

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

-   流式输入时可多次调用`streamingCall`按顺序提交文本片段。服务端接收文本片段后自动进行分句：
    
    -   完整语句立即合成
    -   不完整语句缓存至完整后合成
    
    调用 `streamingComplete` 时，服务端会强制合成所有已接收但未处理的文本片段（包括未完成的句子）。
    
-   发送文本片段的间隔不得超过23秒，否则触发“request timeout after 23 seconds”异常。
    
    若无待发送文本，需及时调用 `streamingComplete`结束任务。
    
    > **重要**
    >
    > 请务必确保调用`streamingComplete`方法，否则可能会导致结尾部分的文本无法成功转换为语音。
    
    > 服务端强制设定23秒超时机制，客户端无法修改该配置。
    

<a id="code-block-4"></a>

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    private static String[] textArray = {"流式文本语音合成SDK，",
            "可以将输入的文本", "合成为语音二进制数据，", "相比于非流式语音合成，",
            "流式合成的优势在于实时性", "更强。用户在输入文本的同时",
            "可以听到接近同步的语音输出，", "极大地提升了交互体验，",
            "减少了用户等待时间。", "适用于调用大规模", "语言模型（LLM），以",
            "流式输入文本的方式", "进行语音合成的场景。"};
    private static String model = "qwen-audio-3.0-tts-flash"; // 模型
    private static String voice = "longanhuan_v3.6"; // 音色

    public static void streamAudioDataToSpeaker() {
        // 配置回调函数
        ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
            @Override
            public void onEvent(SpeechSynthesisResult result) {
                // System.out.println("收到消息: " + result);
                if (result.getAudioFrame() != null) {
                    // 此处实现处理音频数据的逻辑
                    System.out.println(TimeUtils.getTimestamp() + " 收到音频");
                }
            }

            @Override
            public void onComplete() {
                System.out.println(TimeUtils.getTimestamp() + " 收到Complete，语音合成结束");
            }

            @Override
            public void onError(Exception e) {
                System.out.println("出现异常：" + e.toString());
            }
        };

        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model)
                        .voice(voice)
                        .format(SpeechSynthesisAudioFormat
                                .PCM_22050HZ_MONO_16BIT) // 流式合成使用PCM或者MP3
                        .build();
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
        // 带Callback的call方法将不会阻塞当前线程
        try {
            for (String text : textArray) {
                // 发送文本片段，在回调接口的onEvent方法中实时获取二进制音频
                synthesizer.streamingCall(text);
            }
            // 等待结束流式语音合成
            synthesizer.streamingComplete();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }

        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

<a id="通过flowable调用"></a>

<a id="model-qwen-audio-tts-b0f81fef83ojo"></a>

<a id="通过flowable调用-2"></a>

<a id="model-cosyvoice-b0f81fef83ojo"></a>

#### 通过Flowable调用

Flowable是RxJava中表示响应式数据流的类型，支持背压。关于Flowable的使用，请参见[Flowable API详情](http://reactivex.io/RxJava/2.x/javadoc/)。

使用Flowable前需确保已集成RxJava库，并了解响应式编程基础概念。

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

<a id="sec-tabs-3"></a>

<a id="单向流式调用-2"></a>

<a id="单向流式调用-2-h4"></a>

#### 单向流式调用

以下示例展示了通过Flowable对象的`blockingForEach`接口，阻塞式地获取每次流式返回的`SpeechSynthesisResult`类型数据。

<a id="code-block-5"></a>

```java
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    private static String model = "qwen-audio-3.0-tts-flash"; // 模型
    private static String voice = "longanhuan_v3.6"; // 音色

    public static void streamAudioDataToSpeaker() throws NoApiKeyException {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        synthesizer.callAsFlowable("今天天气怎么样?").blockingForEach(result -> {
            if (result.getAudioFrame() != null) {
                // 此处实现处理音频数据的逻辑
                System.out.println(TimeUtils.getTimestamp() + " 收到音频");
            }
            // 获取输出信息，包含事件类型和原始文本
            if (result.getOutput() != null && result.getOutput().has("type")) {
                System.out.println("事件类型: " + result.getOutput().get("type").getAsString()
                        + ", 原始文本: " + (result.getOutput().has("original_text") ? result.getOutput().get("original_text").getAsString() : ""));
            }
        });
        // 任务结束关闭 WebSocket 连接
        synthesizer.getDuplexApi().close(1000, "bye");
        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) throws NoApiKeyException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

<a id="双向流式调用-2"></a>

<a id="双向流式调用-2-h4"></a>

#### 双向流式调用

以下示例展示了通过Flowable对象作为输入参数，输入文本流。并通过Flowable对象作为返回值，利用的`blockingForEach`接口，阻塞式地获取每次流式返回的`SpeechSynthesisResult`类型数据。

<a id="code-block-6"></a>

```java
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.BackpressureStrategy;
import io.reactivex.Flowable;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    private static String[] textArray = {"流式文本语音合成SDK，",
            "可以将输入的文本", "合成为语音二进制数据，", "相比于非流式语音合成，",
            "流式合成的优势在于实时性", "更强。用户在输入文本的同时",
            "可以听到接近同步的语音输出，", "极大地提升了交互体验，",
            "减少了用户等待时间。", "适用于调用大规模", "语言模型（LLM），以",
            "流式输入文本的方式", "进行语音合成的场景。"};
    private static String model = "qwen-audio-3.0-tts-flash";
    private static String voice = "longanhuan_v3.6";

    public static void streamAudioDataToSpeaker() throws NoApiKeyException {
        // 模拟流式输入
        Flowable<String> textSource = Flowable.create(emitter -> {
            new Thread(() -> {
                for (int i = 0; i < textArray.length; i++) {
                    emitter.onNext(textArray[i]);
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }
                emitter.onComplete();
            }).start();
        }, BackpressureStrategy.BUFFER);

        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        synthesizer.streamingCallAsFlowable(textSource).blockingForEach(result -> {
            if (result.getAudioFrame() != null) {
                // 此处实现播放音频的逻辑
                System.out.println(
                        TimeUtils.getTimestamp() +
                                " 二进制音频大小为：" + result.getAudioFrame().capacity());
            }
            // 获取输出信息，包含事件类型和原始文本
            if (result.getOutput() != null && result.getOutput().has("type")) {
                System.out.println("事件类型: " + result.getOutput().get("type").getAsString()
                        + ", 原始文本: " + (result.getOutput().has("original_text") ? result.getOutput().get("original_text").getAsString() : ""));
            }
        });
        synthesizer.getDuplexApi().close(1000, "bye");
        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) throws NoApiKeyException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

<a id="高并发调用"></a>

<a id="model-qwen-audio-tts-93d37d8ec4vw8"></a>

<a id="高并发调用-2"></a>

<a id="model-cosyvoice-93d37d8ec4vw8"></a>

#### 高并发调用

在DashScope Java SDK中，采用了OkHttp3的连接池技术，以减少重复建立连接的开销。详情请参见[高并发最佳实践](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#ug_hc_h3)。

<a id="请求参数"></a>

<a id="request-parameters"></a>

## 请求参数

<a id="qwen-audio-tts"></a>

### Qwen-Audio-TTS

<a id="speechsynthesisparam"></a>

<a id="model-qwen-audio-tts-h3-6m2k9p5r"></a>

#### SpeechSynthesisParam

**包路径**：`com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam`

**示例**：

<a id="code-block-7"></a>

```java
SpeechSynthesisParam param = SpeechSynthesisParam.builder()
    .model("qwen-audio-3.0-tts-flash") // 模型
    .voice("longanhuan_v3.6") // 音色
    .format(SpeechSynthesisAudioFormat.WAV_8000HZ_MONO_16BIT) // 音频编码格式、采样率
    .volume(50) // 音量，取值范围：[0, 100]
    .speechRate(1.0f) // 语速，取值范围：[0.5, 2]
    .pitchRate(1.0f) // 语调，取值范围：[0.5, 2]
    .build();
```

<a id="builder-方法"></a>

<a id="model-qwen-audio-tts-5a66d45053gnm"></a>

##### Builder 方法

<table><thead><tr><th><strong>方法</strong></th><th><strong>参数类型</strong></th><th><strong>必填</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>model(String)</code></td><td><code>String</code></td><td>是</td><td>模型名称。</td></tr><tr><td><code>voice(String)</code></td><td><code>String</code></td><td>是</td><td>语音合成所使用的音色。<ul><li><strong>系统音色</strong>：参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a></li><li><strong>复刻音色</strong>：通过声音复刻功能定制</li><li><strong>声音设计音色</strong>：通过声音设计功能定制</li></ul></td></tr><tr><td><code>format(SpeechSynthesisAudioFormat)</code></td><td><code>enum</code></td><td>否</td><td>音频编码格式及采样率。<p>默认值：SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS。</p><p>SpeechSynthesisAudioFormat包路径：<code>com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat</code>。</p></td></tr><tr><td><code>volume(int)</code></td><td><code>int</code></td><td>否</td><td>音量。<p>默认值：50。</p><p>取值范围：[0, 100]。</p></td></tr><tr><td><code>speechRate(float)</code></td><td><code>float</code></td><td>否</td><td>语速。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>pitchRate(float)</code></td><td><code>float</code></td><td>否</td><td>音调。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>enableWordTimestamp(boolean)</code></td><td><code>boolean</code></td><td>否</td><td>是否开启字级别时间戳。<p>默认值：false。</p><p>仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a>。</p></td></tr><tr><td><code>seed(int)</code></td><td><code>int</code></td><td>否</td><td>生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。<p>默认值0。</p><p>取值范围：[0, 65535]。</p><p>SDK版本低于2.21.7时，<code>seed</code>需要通过扩展参数进行设置。</p></td></tr><tr><td><code>languageHints(List&lt;String&gt;)</code></td><td><code>List&lt;String&gt;</code></td><td>否</td><td><div><div><p><strong>说明</strong>使用 qwen-audio-3.1-tts-flash 的多语种与方言音色时，可通过此参数指定语种或方言。具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md#qwen-tts31-language-hints">多语种与方言音色的设置方法</a>。</p></div></div><p>指定语音合成的目标语言，提升合成效果。</p><p>当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：</p><ul><li>数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”</li><li>符号朗读不准确，“@”读成“艾特”而非“at”</li><li>小语种合成效果差，合成不自然</li></ul><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li><p>zh：中文</p></li><li><p>en：英语</p></li><li><p>fr：法语</p></li><li><p>de：德语</p></li><li><p>ja：日语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>pt：葡萄牙语</p></li><li><p>th：泰语</p></li><li><p>id：印尼语</p></li><li><p>vi：越南语</p></li><li><p>es：西班牙语</p></li><li><p>it：意大利语</p></li><li><p>ms：马来西亚语</p></li><li><p>fil：菲律宾语</p></li><li><p>ar：阿拉伯语</p></li><li><p>other：其他语种（适用于 <code>qwen-audio-3.1-tts-flash</code>）</p><p>保加利亚语、荷兰语、匈牙利语、罗马尼亚语、丹麦语、克罗地亚语、希腊语、捷克语、挪威语、瑞典语、印地语、斯洛伐克语、芬兰语、乌尔都语、塞尔维亚语、墨西哥西班牙语、立陶宛语、拉脱维亚语、土耳其语、波斯语、希伯来语、蒙古语、斯洛文尼亚语、阿塞拜疆语、波兰语、加泰罗尼亚语、高棉语、巴西葡萄牙语、老挝语、格鲁吉亚语、南非荷兰语、尼泊尔语、白俄罗斯语、马拉雅拉姆语、卢森堡语、阿尔巴尼亚语、泰米尔语、僧伽罗语、泰卢固语、爱沙尼亚语、宿务语、波斯尼亚语、缅甸语、亚美尼亚语、拉丁语、冰岛语、马耳他语、斯瓦希里语、哈萨克语、塞舌尔克里奥尔语、乌克兰语。</p></li></ul></div></section><div><div><p><strong>说明</strong></p><ul><li>此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。</li><li>此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create">声音复刻API参考</a>。</li></ul></div></div></td></tr><tr><td><code>instruction(String)</code></td><td><code>String</code></td><td>否</td><td>设置指令，用于控制方言、情感或角色等合成效果。<p>使用说明请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#12884a10929p9">指令控制</a>。</p></td></tr><tr><td><code>hotFix(ParamHotFix)</code></td><td><code>ParamHotFix</code></td><td>否</td><td>文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。<p>参数介绍：</p><ul><li>pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。</li><li>replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。</li></ul><p>示例：</p><a id="code-block-8"></a><pre class="language-java"><code>List&lt;ParamHotFix.PronunciationItem&gt; pronunciationItems = new ArrayList&lt;&gt;();
pronunciationItems.add(new ParamHotFix.PronunciationItem(&quot;天气&quot;, &quot;tian1 qi4&quot;));

List&lt;ParamHotFix.ReplaceItem&gt; replaceItems = new ArrayList&lt;&gt;();
replaceItems.add(new ParamHotFix.ReplaceItem(&quot;今天&quot;, &quot;金天&quot;));

ParamHotFix paramHotFix = new ParamHotFix();
paramHotFix.setPronunciation(pronunciationItems);
paramHotFix.setReplace(replaceItems);

SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                        .model(&quot;qwen-audio-3.0-tts-flash&quot;) // 模型
                        .voice(&quot;longanhuan_v3.6&quot;) // 音色
                        .hotFix(paramHotFix)
                        .build();
</code></pre></td></tr><tr><td><code>parameter(String key, Object value)</code></td><td>String, Object</td><td>否</td><td>设置扩展参数。</td></tr><tr><td><code>parameters(Map&lt;String, Object&gt;)</code></td><td><code>Map</code></td><td>否</td><td>设置扩展参数。</td></tr></tbody></table>

<a id="扩展参数"></a>

<a id="model-qwen-audio-tts-8135356d13pvn"></a>

##### 扩展参数

通过 `parameter()` 或 `parameters()` 设置。

**示例**：

<a id="code-block-9"></a>

```java
SpeechSynthesisParam param = SpeechSynthesisParam.builder()
  .model("qwen-audio-3.0-tts-flash")
  .voice("longanhuan_v3.6")
  .parameter("bit_rate", 32)
  .build();
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bit_rate` | `integer` | 否 | 音频码率（kbps）。音频格式为mp3或opus时，支持通过`bit_rate`参数调整码率。<br><br>默认值：32。<br><br>取值范围：\[6, 510\]。 |
| `enable_markdown_filter` | `boolean` | 否 | 是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。<br><br>默认值：`false`。设为 `true` 启用。<br><br>通过 `parameter("enable_markdown_filter", true)` 启用。 |
| `enable_aigc_tag` | `boolean` | 否 | 是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。<br><br>默认值：false。 |
| `aigc_propagator` | `String` | 否 | 设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。<br><br>默认值：阿里云UID。 |
| `aigc_propagate_id` | `String` | 否 | 设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。<br><br>默认值：本次语音合成请求Request ID。 |

<a id="接口参考"></a>

<a id="通用参考"></a>

<a id="sdk-reference"></a>

## 接口参考

<a id="构造方法"></a>

<a id="model-qwen-audio-tts-h4-7k2m9p5r"></a>

<a id="shared-3"></a>

### 构造方法

<a id="model-cosyvoice-h4-7k2m9p5r"></a>

<a id="code-block-10"></a>

```java
public SpeechSynthesizer(SpeechSynthesisParam param, ResultCallback<SpeechSynthesisResult> callback)
```

**参数说明**：

-   `param`：语音合成参数，通过`SpeechSynthesisParam .builder()`构建
-   `callback`：回调函数，用于流式调用。非流式调用时传入null

<a id="call-非流式-单向流式合成"></a>

<a id="model-qwen-audio-tts-h4-cv-call"></a>

<a id="shared-5"></a>

### call() - 非流式/单向流式合成

<a id="model-cosyvoice-h4-cv-call"></a>

**方法签名**：

<a id="code-block-11"></a>

```java
public ByteBuffer call(String text)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | `String` | 是 | 待合成的文本，长度不得超过20000字符。 |

**返回值**：`ByteBuffer` 或 null。非流式调用时返回完整音频数据；单向流式调用时音频通过回调返回，此方法返回null。

<a id="streamingcall-双向流式合成"></a>

<a id="model-qwen-audio-tts-h4-cv-streaming"></a>

<a id="shared-7"></a>

### streamingCall() - 双向流式合成

<a id="model-cosyvoice-h4-cv-streaming"></a>

**方法签名**：

<a id="code-block-12"></a>

```java
public void streamingCall(String text)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | `String` | 是 | 待合成的文本，长度不得超过20000字符。可多次调用追加文本。 |

<a id="streamingcomplete-结束双向流式调用"></a>

<a id="model-qwen-audio-tts-h4-cv-sc-complete"></a>

<a id="shared-9"></a>

### streamingComplete() - 结束双向流式调用

<a id="model-cosyvoice-h4-cv-sc-complete"></a>

**方法签名**：

<a id="code-block-13"></a>

```java
public void streamingComplete()
```

结束双向流式调用，通知服务端所有文本已发送完毕。

<a id="callasflowable-单向流式合成-响应式"></a>

<a id="model-qwen-audio-tts-h4-cv-flowable"></a>

<a id="shared-11"></a>

### callAsFlowable() - 单向流式合成（响应式）

<a id="model-cosyvoice-h4-cv-flowable"></a>

**方法签名**：

<a id="code-block-14"></a>

```java
public Flowable<SpeechSynthesisResult> callAsFlowable(String text)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | `String` | 是 | 待合成的文本。 |

**返回值**：`Flowable< SpeechSynthesisResult >` 响应式流。

<a id="streamingcallasflowable-双向流式合成-响应式"></a>

<a id="model-qwen-audio-tts-h4-cv-sc-flowable"></a>

<a id="shared-13"></a>

### streamingCallAsFlowable() - 双向流式合成（响应式）

<a id="model-cosyvoice-h4-cv-sc-flowable"></a>

**方法签名**：

<a id="code-block-15"></a>

```java
public Flowable<SpeechSynthesisResult> streamingCallAsFlowable(Flowable<String> textStream)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `textStream` | `Flowable<String>` | 是 | 文本的响应式流。 |

**返回值**：`Flowable< SpeechSynthesisResult >` 响应式流。

<a id="getduplexapi-close-关闭websocket连接"></a>

<a id="model-qwen-audio-tts-h4-cv-close"></a>

<a id="shared-15"></a>

### getDuplexApi().close() - 关闭WebSocket连接

<a id="model-cosyvoice-h4-cv-close"></a>

**方法签名**：

<a id="code-block-16"></a>

```java
public boolean getDuplexApi().close(int code, String reason)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `code` | `int` | 是 | 关闭码。 |
| `reason` | `String` | 是 | 关闭原因。 |

**返回值**：`boolean`，是否成功关闭。

<a id="getlastrequestid-获取请求id"></a>

<a id="model-qwen-audio-tts-h4-cv-reqid"></a>

<a id="shared-17"></a>

### getLastRequestId() - 获取请求ID

<a id="model-cosyvoice-h4-cv-reqid"></a>

**方法签名**：

<a id="code-block-17"></a>

```java
public String getLastRequestId()
```

**返回值**：`String`，请求ID。

<a id="getfirstpackagedelay-获取首包延迟"></a>

<a id="model-qwen-audio-tts-h4-cv-delay"></a>

<a id="shared-19"></a>

### getFirstPackageDelay() - 获取首包延迟

<a id="model-cosyvoice-h4-cv-delay"></a>

**方法签名**：

<a id="code-block-18"></a>

```java
public long getFirstPackageDelay()
```

**返回值**：`long`，首包延迟（ms），从发送第一包到收到首包结果。

<a id="onevent-接收音频数据"></a>

<a id="model-qwen-audio-tts-h4-cb-onevent"></a>

<a id="shared-21"></a>

### onEvent() - 接收音频数据

<a id="model-cosyvoice-h4-cb-onevent"></a>

**方法签名**：

<a id="code-block-19"></a>

```java
public void onEvent(SpeechSynthesisResult result)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `result` | [SpeechSynthesisResult](#tts-h3-8k2m9p5r) | 是 | 接收到合成事件时触发，包含音频帧、时间戳信息和输出信息（事件类型、原始文本等）。 |

<a id="oncomplete-合成完成"></a>

<a id="model-qwen-audio-tts-h4-cb-oncomplete"></a>

<a id="shared-23"></a>

### onComplete() - 合成完成

<a id="model-cosyvoice-h4-cb-oncomplete"></a>

**方法签名**：

<a id="code-block-20"></a>

```java
public void onComplete()
```

语音合成完成时触发。

<a id="onerror-错误处理"></a>

<a id="model-qwen-audio-tts-h4-cb-onerror"></a>

<a id="shared-25"></a>

### onError() - 错误处理

<a id="model-cosyvoice-h4-cb-onerror"></a>

**方法签名**：

<a id="code-block-21"></a>

```java
public void onError(Exception e)
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `e` | `Exception` | 是 | 发生错误时触发，包含异常信息。 |

<a id="getaudioframe-获取音频数据帧"></a>

<a id="model-qwen-audio-tts-h4-result-getframe"></a>

<a id="shared-27"></a>

### getAudioFrame() - 获取音频数据帧

<a id="model-cosyvoice-h4-result-getframe"></a>

**方法签名**：

<a id="code-block-22"></a>

```java
public ByteBuffer getAudioFrame()
```

**返回值**：`ByteBuffer`，音频数据帧。

<a id="gettimestamp-获取时间戳信息"></a>

<a id="model-qwen-audio-tts-h4-result-getts"></a>

<a id="shared-29"></a>

### getTimestamp() - 获取时间戳信息

<a id="model-cosyvoice-h4-result-getts"></a>

**方法签名**：

<a id="code-block-23"></a>

```java
public Sentence getTimestamp()
```

**返回值**：`Sentence`，时间戳信息。

<a id="getoutput-获取输出信息"></a>

<a id="model-qwen-audio-tts-h4-result-getoutput"></a>

<a id="shared-31"></a>

### getOutput() - 获取输出信息

<a id="model-cosyvoice-h4-result-getoutput"></a>

**方法签名**：

<a id="code-block-24"></a>

```java
public JsonObject getOutput()
```

**返回值**：`com.google.gson.JsonObject`，合成事件的[输出信息](#model-qwen-audio-tts-h4-output-info)，包含事件类型和文本内容。需要SDK版本 >= 2.22.0。

<a id="getbegintime-获取句子开始时间"></a>

<a id="model-qwen-audio-tts-h5-sent-begin"></a>

<a id="shared-33"></a>

### getBeginTime() - 获取句子开始时间

<a id="model-cosyvoice-h5-sent-begin"></a>

**方法签名**：

<a id="code-block-25"></a>

```java
public int getBeginTime()
```

**返回值**：句子开始时间，单位为ms。

<a id="getendtime-获取句子结束时间"></a>

<a id="model-qwen-audio-tts-h5-sent-end"></a>

<a id="shared-35"></a>

### getEndTime() - 获取句子结束时间

<a id="model-cosyvoice-h5-sent-end"></a>

**方法签名**：

<a id="code-block-26"></a>

```java
public int getEndTime()
```

**返回值**：句子结束时间，单位为ms。

<a id="getwords-获取字级别时间戳"></a>

<a id="model-qwen-audio-tts-h5-sent-words"></a>

<a id="shared-37"></a>

### getWords() - 获取字级别时间戳

<a id="model-cosyvoice-h5-sent-words"></a>

**方法签名**：

<a id="code-block-27"></a>

```java
public List<Word> getWords()
```

**返回值**：[Word](#tts-h4-word-ts)的`List`集合，批量获取字级别时间戳信息，可能为空。

<a id="getbegintime-获取词开始时间"></a>

<a id="model-qwen-audio-tts-h5-word-begin"></a>

<a id="shared-39"></a>

### getBeginTime() - 获取词开始时间

<a id="model-cosyvoice-h5-word-begin"></a>

**方法签名**：

<a id="code-block-28"></a>

```java
public int getBeginTime()
```

**返回值**：词开始时间，单位为ms。

<a id="getendtime-获取词结束时间"></a>

<a id="model-qwen-audio-tts-h5-word-end"></a>

<a id="shared-41"></a>

### getEndTime() - 获取词结束时间

<a id="model-cosyvoice-h5-word-end"></a>

**方法签名**：

<a id="code-block-29"></a>

```java
public int getEndTime()
```

**返回值**：词结束时间，单位为ms。

<a id="gettext-获取文本信息"></a>

<a id="model-qwen-audio-tts-h5-word-text"></a>

<a id="shared-43"></a>

### getText() - 获取文本信息

<a id="model-cosyvoice-h5-word-text"></a>

**方法签名**：

<a id="code-block-30"></a>

```java
public String getText()
```

**返回值**：`String`，文本信息。

<a id="getphonemes-获取音素级别时间戳"></a>

<a id="model-qwen-audio-tts-h5-word-phonemes"></a>

<a id="shared-45"></a>

### getPhonemes() - 获取音素级别时间戳

<a id="model-cosyvoice-h5-word-phonemes"></a>

**方法签名**：

<a id="code-block-31"></a>

```java
public List<Phoneme> getPhonemes()
```

**返回值**：[Phoneme](#tts-h4-phoneme-ts)的`List`集合，批量获取音素级别时间戳信息，可能为空。

<a id="getbegintime-获取音素开始时间"></a>

<a id="model-qwen-audio-tts-h5-ph-begin"></a>

<a id="shared-47"></a>

### getBeginTime() - 获取音素开始时间

<a id="model-cosyvoice-h5-ph-begin"></a>

**方法签名**：

<a id="code-block-32"></a>

```java
public int getBeginTime()
```

**返回值**：音素开始时间，单位为ms。

<a id="getendtime-获取音素结束时间"></a>

<a id="model-qwen-audio-tts-h5-ph-end"></a>

<a id="shared-49"></a>

### getEndTime() - 获取音素结束时间

<a id="model-cosyvoice-h5-ph-end"></a>

**方法签名**：

<a id="code-block-33"></a>

```java
public int getEndTime()
```

**返回值**：音素结束时间，单位为ms。

<a id="gettext-获取文本信息-2"></a>

<a id="model-qwen-audio-tts-h5-ph-text"></a>

<a id="shared-51"></a>

### getText() - 获取文本信息

<a id="model-cosyvoice-h5-ph-text"></a>

**方法签名**：

<a id="code-block-34"></a>

```java
public String getText()
```

**返回值**：`String`，文本信息。

<a id="gettone-获取音调"></a>

<a id="model-qwen-audio-tts-h5-ph-tone"></a>

<a id="shared-53"></a>

### getTone() - 获取音调

<a id="model-cosyvoice-h5-ph-tone"></a>

**方法签名**：

<a id="code-block-35"></a>

```java
public int getTone()
```

**返回值**：音调。

-   英文中，0、1、2分别代表轻音、重音和次重音。
-   拼音中，1、2、3、4、5分别代表一声、二声、三声、四声和轻声。

<a id="输出信息-output"></a>

<a id="model-qwen-audio-tts-h4-output-info"></a>

<a id="shared-55"></a>

### 输出信息（`output`）

<a id="model-cosyvoice-h4-output-info"></a>

`getOutput()`返回`JsonObject`，封装了合成事件的输出信息。在`onEvent`回调或Flowable流中获取。包含以下字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `String` | 事件类型。取值：`sentence-begin`（句子开始，返回待合成的文本内容）、`sentence-synthesis`（标识音频数据块，表示当前正在合成音频）、`sentence-end`（句子结束，返回文本内容和字级别时间戳）。 |
| `original_text` | `String` | 当前句子的原始文本内容。在`sentence-begin`和`sentence-end`事件中返回。 |
| `sentence` | `JsonObject` | 句子信息，包含句子编号（`index`）和字级别时间戳（`words`）。在`sentence-end`事件中包含完整的字级别时间戳信息。 |

<a id="qwen-audio-tts-2"></a>

<a id="model-qwen-audio-tts"></a>

### Qwen-Audio-TTS

<a id="speechsynthesizer"></a>

<a id="model-qwen-audio-tts-h3-3k1w9m6p"></a>

#### SpeechSynthesizer

**包路径**：`com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer`

<a id="streamingcancel-取消双向流式调用"></a>

<a id="model-qwen-audio-tts-h4-cv-sc-cancel"></a>

##### streamingCancel() - 取消双向流式调用

**方法签名**：

<a id="code-block-36"></a>

```java
public void streamingCancel()
```

**说明**：取消当前轮次的双向流式语音合成任务。调用后，SDK 会立即结束当前任务。取消后可在当前连接上继续发起新的合成任务，无需重新初始化 `SpeechSynthesizer` 实例。

> **重要**
>
> **版本要求**：使用该功能需要 Java SDK 版本不低于 2.22.26。

<a id="resultcallback"></a>

<a id="model-qwen-audio-tts-h3-8m9k5p2r"></a>

#### ResultCallback

**包路径**：`com.alibaba.dashscope.common.ResultCallback`

<a id="speechsynthesisresult"></a>

<a id="model-qwen-audio-tts-h3-8k2m9p5r"></a>

<a id="tts-h3-8k2m9p5r"></a>

#### SpeechSynthesisResult

**包路径**：`com.alibaba.dashscope.audio.tts.SpeechSynthesisResult`

<a id="句子级别时间戳信息-sentence"></a>

<a id="model-qwen-audio-tts-h4-sentence-ts"></a>

##### 句子级别时间戳信息（`Sentence`）

`Sentence`封装了句子级别时间戳信息。

<a id="字级别时间戳信息-word"></a>

<a id="model-qwen-audio-tts-h4-word-ts"></a>

<a id="tts-h4-word-ts"></a>

##### 字级别时间戳信息（`Word`）

`Word`封装了字级别时间戳信息。

<a id="音素级别时间戳信息-phoneme"></a>

<a id="model-qwen-audio-tts-h4-phoneme-ts"></a>

<a id="tts-h4-phoneme-ts"></a>

##### 音素级别时间戳信息（`Phoneme`）

`Phoneme`封装了音素级别时间戳信息。

# Qwen-Audio-ASR-Streaming Java SDK

其他模型 — [Qwen-Audio-ASR-Message Java SDK](qwen-asr-message-websocket-sdk-java-4524c054fb74f217.md) · [Fun-ASR-Realtime Java SDK](fun-asr-realtime-websocket-sdk-java-ec987af1c2fd19d4.md)

使用 DashScope Java SDK 识别本地音频文件或麦克风输入。本文覆盖 Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Message 和 Fun-ASR-Realtime。

<a id="前提条件"></a>

<a id="通用参考"></a>

<a id="model-qwen-audio-asr-streaming-8a24f2ed09vr0"></a>

<a id="shared-1"></a>

## 前提条件

<a id="model-qwen-audio-asr-message-8a24f2ed09vr0"></a>

<a id="model-fun-asr-realtime-8a24f2ed09vr0"></a>

-   已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请配置API Key到环境变量，而非硬编码在代码中，防范因代码泄露导致的安全风险。
-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="接口地址"></a>

<a id="model-qwen-audio-asr-streaming-h2-3r8w6k1j"></a>

<a id="shared-4"></a>

### 接口地址

<a id="model-qwen-audio-asr-message-h2-3r8w6k1j"></a>

<a id="model-fun-asr-realtime-h2-3r8w6k1j"></a>

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

<a id="model-qwen-audio-asr-streaming-dd017b69c3byd"></a>

<a id="快速开始-2"></a>

<a id="model-qwen-audio-asr-message-dd017b69c3byd"></a>

<a id="快速开始-3"></a>

<a id="model-fun-asr-realtime-dd017b69c3byd"></a>

<a id="model-qwen-audio-asr-streaming-8341058094tc3"></a>

<a id="model-qwen-audio-asr-streaming-9d1e5f6852jr8"></a>

<a id="model-qwen-audio-asr-streaming-6734e006bc0gp"></a>

<a id="model-qwen-audio-asr-message-8341058094tc3"></a>

<a id="model-qwen-audio-asr-message-9d1e5f6852jr8"></a>

<a id="model-qwen-audio-asr-message-6734e006bc0gp"></a>

<a id="model-fun-asr-realtime-8341058094tc3"></a>

<a id="model-fun-asr-realtime-9d1e5f6852jr8"></a>

<a id="model-fun-asr-realtime-6734e006bc0gp"></a>

## 快速开始

将示例中的 `{WorkspaceId}` 换成实际的业务空间 ID，`{YOUR_AUDIO_FILE}` 换成本地 16 kHz WAV 文件路径。运行后，终端输出识别结果。

<a id="code-block"></a>

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        // 创建Recognition实例
        Recognition recognizer = new Recognition();
        // 创建RecognitionParam
        RecognitionParam param =
                RecognitionParam.builder()
                        .model("qwen-audio-3.1-asr-flash-streaming")
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .format("wav")
                        .sampleRate(16000)
                        .build();

        try {
            System.out.println("识别结果：" + recognizer.call(param, new File("{YOUR_AUDIO_FILE}")));
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 任务结束后关闭 WebSocket 连接
            recognizer.getDuplexApi().close(1000, "bye");
        }
        System.out.println(
                "[Metric] requestId: "
                        + recognizer.getLastRequestId()
                        + ", first package delay ms: "
                        + recognizer.getFirstPackageDelay()
                        + ", last package delay ms: "
                        + recognizer.getLastPackageDelay());
        System.exit(0);
    }
}
```

<a id="更多示例"></a>

### 更多示例

以下代码可共用。示例默认使用 Qwen-Audio-ASR-Streaming。调用其他模型时，按下表替换 `model`。

| 模型 | `model` 的值 |
| --- | --- |
| Qwen-Audio-ASR-Streaming | 非流式调用和基于回调的本地文件示例使用 `qwen-audio-3.1-asr-flash-streaming`。麦克风和 Flowable 示例使用 `qwen-audio-3.0-asr-flash-streaming`。 |
| Qwen-Audio-ASR-Message | `qwen-audio-3.1-asr-flash-message` |
| Fun-ASR-Realtime | `fun-asr-realtime` |

如需指定识别语言，请按对应模型的[请求参数](#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0)配置 `language_hints`。

`Recognition`提供了非流式调用和双向流式调用等接口。请根据实际需求选择合适的调用方式：

-   非流式调用：针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
-   双向流式调用：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

<a id="sec-tabs-2"></a>

<a id="非流式调用"></a>

<a id="非流式调用-h4"></a>

#### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

将示例中的 `{YOUR_AUDIO_FILE}` 替换为本地 WAV 文件的路径。运行后，程序会在终端打印完整的识别结果。

<a id="code-block-2"></a>

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        // 创建Recognition实例
        Recognition recognizer = new Recognition();
        // 创建RecognitionParam
        RecognitionParam param =
                RecognitionParam.builder()
                        .model("qwen-audio-3.1-asr-flash-streaming")
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .format("wav")
                        .sampleRate(16000)
                        .build();

        try {
            System.out.println("识别结果：" + recognizer.call(param, new File("{YOUR_AUDIO_FILE}")));
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 任务结束后关闭 WebSocket 连接
            recognizer.getDuplexApi().close(1000, "bye");
        }
        System.out.println(
                "[Metric] requestId: "
                        + recognizer.getLastRequestId()
                        + ", first package delay ms: "
                        + recognizer.getFirstPackageDelay()
                        + ", last package delay ms: "
                        + recognizer.getLastPackageDelay());
        System.exit(0);
    }
}
```

<a id="双向流式调用-基于回调"></a>

<a id="双向流式调用-基于回调-h4"></a>

#### 双向流式调用：基于回调

提交单个语音实时转写任务，通过实现回调接口的方式流式输出实时识别结果。

1.  启动流式语音识别
    
    实例化Recognition类，调用`call`方法绑定请求参数和回调接口（ResultCallback）并启动流式语音识别。
    
2.  流式传输
    
    循环调用Recognition类的`sendAudioFrame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。
    
    在发送音频数据的过程中，服务端会通过回调接口（ResultCallback）的`onEvent`方法，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用Recognition类的`stop`方法结束语音识别。
    
    该方法会阻塞当前线程，直到回调接口（ResultCallback）的`onComplete`或者`onError`回调触发后才会释放线程阻塞。
    

<a id="fig-code-group"></a>

<a id="fig-code-group-识别传入麦克风的语音-tab"></a>

识别传入麦克风的语音

<a id="code-code-group-识别传入麦克风的语音"></a>

```java
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

<a id="fig-code-group-识别本地语音文件-tab"></a>

识别本地语音文件

<a id="code-code-group-识别本地语音文件"></a>

```java
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

<a id="双向流式调用-基于flowable"></a>

<a id="双向流式调用-基于flowable-h4"></a>

#### 双向流式调用：基于Flowable

提交单个语音实时转写任务，通过实现工作流（Flowable）的方式流式输出实时识别结果。

Flowable 是 RxJava 中用于处理响应式数据流的类。关于Flowable的使用，请参见[Flowable API详情](https://reactivex.io/RxJava/2.x/javadoc/io/reactivex/Flowable.html)。

直接调用Recognition类的`streamCall`方法开始识别。

`streamCall`方法返回一个`Flowable<RecognitionResult>`实例，您可以调用`Flowable`实例的`blockingForEach`、`subscribe`等方法处理识别结果。识别结果封装在`RecognitionResult`中。

`streamCall`方法需要传入两个参数：

-   `RecognitionParam`实例（请求参数）：通过它可以设置语音识别所需的模型、采样率、音频格式等参数。
-   `Flowable<ByteBuffer>`实例：您需要创建一个`Flowable<ByteBuffer>`类型的实例，并在其中实现解析音频流的方法。

<a id="code-block-3"></a>

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.BackpressureStrategy;
import io.reactivex.Flowable;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;
import java.nio.ByteBuffer;

public class Main {
    public static void main(String[] args) throws NoApiKeyException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        // 创建一个Flowable<ByteBuffer>
        Flowable<ByteBuffer> audioSource =
                Flowable.create(
                        emitter -> {
                            new Thread(
                                    () -> {
                                        try {
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
                                                    emitter.onNext(buffer);
                                                    buffer = ByteBuffer.allocate(1024);
                                                    // 录音速率有限，防止cpu占用过高，休眠一小会儿
                                                    Thread.sleep(20);
                                                }
                                            }
                                            // 通知结束转写
                                            emitter.onComplete();
                                        } catch (Exception e) {
                                            emitter.onError(e);
                                        }
                                    })
                                    .start();
                        },
                        BackpressureStrategy.BUFFER);

        // 创建Recognizer
        Recognition recognizer = new Recognition();
        // 创建RecognitionParam，audioFrames参数中传入上面创建的Flowable<ByteBuffer>
        RecognitionParam param = RecognitionParam.builder()
                .model("qwen-audio-3.0-asr-flash-streaming")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .format("pcm")
                .sampleRate(16000)
                .build();

        // 流式调用接口
        recognizer
                .streamCall(param, audioSource)
                .blockingForEach(
                        result -> {
                            // Subscribe to the output result
                            if (result.isSentenceEnd()) {
                                System.out.println("Final Result: " + result.getSentence().getText());
                            } else {
                                System.out.println("Intermediate Result: " + result.getSentence().getText());
                            }
                        });
        // 任务结束后关闭 Websocket 连接
        recognizer.getDuplexApi().close(1000, "bye");
        System.out.println(
                "[Metric] requestId: "
                        + recognizer.getLastRequestId()
                        + ", first package delay ms: "
                        + recognizer.getFirstPackageDelay()
                        + ", last package delay ms: "
                        + recognizer.getLastPackageDelay());
        System.exit(0);
    }
}
```

<a id="高并发调用"></a>

<a id="model-qwen-audio-asr-streaming-ea8503736dlf7"></a>

<a id="高并发调用-2"></a>

<a id="model-qwen-audio-asr-message-ea8503736dlf7"></a>

<a id="高并发调用-3"></a>

<a id="model-fun-asr-realtime-ea8503736dlf7"></a>

### 高并发调用

在DashScope Java SDK中，采用了OkHttp3的连接池技术，以减少重复建立连接的开销。详情请参见[高并发最佳实践](../model-user-guide/model-experience/speech-and-audio/speech-recognition/speech-recognition-best-practices.md#java)。

<a id="请求参数"></a>

## 请求参数

<a id="qwen-audio-asr-streaming"></a>

<a id="model-qwen-audio-asr-streaming"></a>

<a id="model-qwen-audio-asr-streaming-d72d661a1brzp"></a>

### Qwen-Audio-ASR-Streaming

通过`RecognitionParam`的链式方法配置模型、采样率、音频格式等参数。配置完成的参数对象传入Recognition类的`call`/`streamCall`方法中使用。

<a id="code-block-4"></a>

```java
RecognitionParam param = RecognitionParam.builder()
  .model("qwen-audio-3.1-asr-flash-streaming")
  .format("pcm")
  .sampleRate(16000)
  //.parameter("language_hints", new String[]{"zh"})
  .build();
```

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>model</code></td><td><code>String</code></td><td>是</td><td>模型名称。</td></tr><tr><td><code>sampleRate</code></td><td><code>Integer</code></td><td>是</td><td><p>采样率（Hz），支持任意采样率。</p></td></tr><tr><td><code>format</code></td><td><code>String</code></td><td>是</td><td>音频格式。<p>取值范围：</p><ul><li><code>pcm</code></li><li><code>wav</code></li><li><code>mp3</code></li><li><code>opus</code></li><li><code>speex</code></li><li><code>aac</code></li><li><code>amr</code></li></ul><div><div><p><strong>重要</strong>opus/speex：必须使用Ogg封装；</p><p>wav：必须为PCM编码；</p><p>amr：仅支持AMR-NB类型。</p></div></div></td></tr><tr><td><code>keep_dialect</code></td><td><code>boolean</code></td><td>否</td><td>仅 <code>qwen-audio-3.1-asr-flash-streaming</code> 支持。默认 <code>false</code>，将方言转写为普通话；设为 <code>true</code> 时保留方言表达。通过 <code>.parameter(&quot;keep_dialect&quot;, value)</code> 设置。完整参数说明请参见<a href="qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md">客户端事件</a>。</td></tr><tr><td><code>vad_model</code></td><td><code>String</code></td><td>否</td><td>仅 <code>qwen-audio-3.1-asr-flash-streaming</code> 支持。可选 <code>near_meeting_16k</code>（近场）或 <code>far_field_meeting_16k</code>（远场，默认值）。通过 <code>.parameter(&quot;vad_model&quot;, value)</code> 设置。完整参数说明请参见<a href="qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md">客户端事件</a>。</td></tr><tr><td><code>vocabularyId</code></td><td><code>String</code></td><td>否</td><td>预编译热词列表 ID。<p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><code>vocabulary</code></td><td><code>Map&lt;String, Integer&gt;</code></td><td>否</td><td>即时热词。<p>以键值对形式传入，键为热词文本（<code>string</code>），值为热词权重（<code>integer</code>），无需预先创建热词列表。权重取值范围为 [1, 5] 或 50：取 [1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。</p><p>适用于临时性、会话级别的热词优化。</p><p>与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p><p><code>vocabulary</code>需要通过 <code>RecognitionParam</code> 实例的 <code>parameter</code> 方法或者 <code>parameters</code> 方法进行设置：</p><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-2-通过parameter设置"></a><pre class="language-java"><code>Map&lt;String, Integer&gt; vocab = new HashMap&lt;&gt;();
vocab.put(&quot;张三&quot;, 5);
vocab.put(&quot;李四&quot;, 5);

RecognitionParam param = RecognitionParam.builder()
        .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
        .format(&quot;pcm&quot;)
        .sampleRate(16000)
        .parameter(&quot;vocabulary&quot;, vocab)
        .build();
</code></pre></div><a id="fig-code-group-2-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-2-通过parameters设置"></a><pre class="language-java"><code>Map&lt;String, Integer&gt; vocab = new HashMap&lt;&gt;();
vocab.put(&quot;张三&quot;, 5);
vocab.put(&quot;李四&quot;, 5);

Map&lt;String, Object&gt; parameters = new HashMap&lt;&gt;();
parameters.put(&quot;vocabulary&quot;, vocab);

RecognitionParam param = RecognitionParam.builder()
        .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
        .format(&quot;pcm&quot;)
        .sampleRate(16000)
        .parameters(parameters)
        .build();
</code></pre></div></div></td></tr><tr><td><code>max_sentence_silence</code></td><td><code>Integer</code></td><td>否</td><td>VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。<p>默认值：800。</p><p>取值范围：[200, 6000]。</p><p><code>max_sentence_silence</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-3-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;max_sentence_silence&quot;, 800)
 .build();
</code></pre></div><a id="fig-code-group-3-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-3-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;max_sentence_silence&quot;, 800))
 .build();
</code></pre></div></div></td></tr><tr><td><code>multi_threshold_mode_enabled</code></td><td><code>boolean</code></td><td>否</td><td><p>是否启用多阈值模式。启用后可防止 VAD 断句切割过长。</p><p>默认值：false。</p><p><code>multi_threshold_mode_enabled</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-4-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;multi_threshold_mode_enabled&quot;, true)
 .build();
</code></pre></div><a id="fig-code-group-4-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-4-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;multi_threshold_mode_enabled&quot;, true))
 .build();
</code></pre></div></div></td></tr><tr><td><code>punctuation_prediction_enabled</code></td><td><code>boolean</code></td><td>否</td><td>设置是否在识别结果中自动添加标点：<ul><li>true（默认）：是，不支持修改。</li></ul><p><code>punctuation_prediction_enabled</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-5-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;punctuation_prediction_enabled&quot;, false)
 .build();
</code></pre></div><a id="fig-code-group-5-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-5-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;punctuation_prediction_enabled&quot;, false))
 .build();
</code></pre></div></div></td></tr><tr><td><code>heartbeat</code></td><td><code>boolean</code></td><td>否</td><td>是否启用心跳包。<p>默认值：false。</p><ul><li>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</li></ul><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p><div><div><p><strong>说明</strong>使用该字段时，SDK版本不能低于2.19.1。</p></div></div><p><code>heartbeat</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-6-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;heartbeat&quot;, true)
 .build();
</code></pre></div><a id="fig-code-group-6-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-6-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;heartbeat&quot;, true))
 .build();
</code></pre></div></div></td></tr><tr><td><code>language_hints</code></td><td><code>String[]</code></td><td>否</td><td>待识别音频语种。无默认值，不设置时模型自动识别。<p>最多支持设置 4 个值，超出时仅前 4 个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></div></section><p><code>language_hints</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-7-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;language_hints&quot;, new String[]{&quot;zh&quot;})
 .build();
</code></pre></div><a id="fig-code-group-7-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-7-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;language_hints&quot;, new String[]{&quot;zh&quot;}))
 .build();
</code></pre></div></div></td></tr><tr><td><code>speech_noise_threshold</code></td><td><code>float</code></td><td>否</td><td>语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。<p>取值范围：[-1.0, 1.0]。</p><p>取值说明：</p><ul><li>取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写</li><li>取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤</li></ul><p>此参数为高级配置参数，调整可能显著影响识别效果，建议：</p><ul><li>调整前充分测试验证效果</li><li>根据实际音频环境小幅度调整（建议步长 0.1）</li></ul><p><code>speech_noise_threshold</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-8-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;speech_noise_threshold&quot;, -0.5)
 .build();
</code></pre></div><a id="fig-code-group-8-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-8-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;speech_noise_threshold&quot;, -0.5))
 .build();
</code></pre></div></div></td></tr><tr><td><code>special_word_filter</code></td><td><code>String</code></td><td>否</td><td>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md#rt03_sensitive_h3">敏感词过滤</a>。<p><code>special_word_filter</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-9-通过parameter设置"></a><pre class="language-java"><code>// 1. 构建最外层对象
JSONObject root = new JSONObject();
root.put(&quot;system_reserved_filter&quot;, true);

// 2. 构建“从结果中完全移除”的配置
JSONObject root1 = new JSONObject();
JSONArray array1 = new JSONArray();
array1.put(&quot;开始&quot;);
array1.put(&quot;进行&quot;);
root1.put(&quot;word_list&quot;, array1);

// 3. 构建“替换为等长 *”的配置
JSONObject root2 = new JSONObject();
JSONArray array2 = new JSONArray();
array2.put(&quot;测试&quot;);
root2.put(&quot;word_list&quot;, array2);

// 4. 组装
root.put(&quot;filter_with_empty&quot;, root1);
root.put(&quot;filter_with_signed&quot;, root2);

RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;special_word_filter&quot;, root.toString())
 .build();
</code></pre></div><a id="fig-code-group-9-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-9-通过parameters设置"></a><pre class="language-java"><code>// 1. 构建最外层对象
JSONObject root = new JSONObject();
root.put(&quot;system_reserved_filter&quot;, true);

// 2. 构建“从结果中完全移除”的配置
JSONObject root1 = new JSONObject();
JSONArray array1 = new JSONArray();
array1.put(&quot;开始&quot;);
array1.put(&quot;进行&quot;);
root1.put(&quot;word_list&quot;, array1);

// 3. 构建“替换为等长 *”的配置
JSONObject root2 = new JSONObject();
JSONArray array2 = new JSONArray();
array2.put(&quot;测试&quot;);
root2.put(&quot;word_list&quot;, array2);

// 4. 组装
root.put(&quot;filter_with_empty&quot;, root1);
root.put(&quot;filter_with_signed&quot;, root2);

RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;special_word_filter&quot;, root.toString()))
 .build();
</code></pre></div></div></td></tr><tr><td><code>input</code></td><td><code>Map&lt;String, Object&gt;</code></td><td>否</td><td>输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md">提升识别准确率</a>。<p>Map 中需包含 <code>context</code> 键，值为 <code>List&lt;Map&lt;String, Object&gt;&gt;</code> 类型的消息数组，每条消息包含以下字段：</p><ul><li><code>role</code>（String，必选）：消息角色。<code>user</code> 表示前几轮用户语音的识别结果或领域相关的词表；<code>assistant</code> 表示前几轮大语言模型的回复内容。</li><li><code>content</code>（List&lt;Map&gt;，必选）：消息内容列表。每个元素包含 <code>type</code>（String，role 为 user 时填 <code>input_text</code>，role 为 assistant 时填 <code>text</code>）和 <code>text</code>（String，文本内容）。</li></ul><div><div><p><strong>重要</strong>上下文消息（<code>input_text</code> 和 <code>text</code> 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。</p></div></div><div><div><p><strong>重要</strong>携带上下文时，<code>context</code> 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 <code>user</code>（<code>input_text</code> 类型）必须在对应的 <code>assistant</code>（<code>text</code> 类型）之前。</p></div></div><div><div><p><strong>说明</strong>使用该字段时，SDK版本不能低于2.22.23。</p></div></div><p><code>input</code>通过<code>RecognitionParam</code>实例的<code>input</code>方法进行设置：</p><a id="code-block-5"></a><pre class="language-java"><code>// 1. 构建 input 结构体
Map&lt;String, Object&gt; userContent = new HashMap&lt;&gt;();
userContent.put(&quot;type&quot;, &quot;input_text&quot;);
userContent.put(&quot;text&quot;, &quot;你好啊&quot;);

Map&lt;String, Object&gt; assistantContent = new HashMap&lt;&gt;();
assistantContent.put(&quot;type&quot;, &quot;text&quot;);
assistantContent.put(&quot;text&quot;, &quot;你好啊，我是通义千问，有什么可以帮助你的？&quot;);

Map&lt;String, Object&gt; userMessage = new HashMap&lt;&gt;();
userMessage.put(&quot;role&quot;, &quot;user&quot;);
userMessage.put(&quot;content&quot;, Arrays.asList(userContent));

Map&lt;String, Object&gt; assistantMessage = new HashMap&lt;&gt;();
assistantMessage.put(&quot;role&quot;, &quot;assistant&quot;);
assistantMessage.put(&quot;content&quot;, Arrays.asList(assistantContent));

Map&lt;String, Object&gt; input = new HashMap&lt;&gt;();
input.put(&quot;context&quot;, Arrays.asList(userMessage, assistantMessage));

// 2. 通过 input 方法传入
RecognitionParam param = RecognitionParam.builder()
 .model(&quot;qwen-audio-3.1-asr-flash-streaming&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .input(input)
 .build();
</code></pre></td></tr><tr><td><code>apiKey</code></td><td><code>String</code></td><td>否</td><td>用户API Key。</td></tr></tbody></table>

<a id="接口参考"></a>

## 接口参考

<a id="qwen-audio-asr-streaming-与-fun-asr-realtime"></a>

<a id="通用参考-qwen-audio-asr-streaming-fun-asr-realtime"></a>

<a id="关键接口"></a>

<a id="model-qwen-audio-asr-streaming-8b0d2507910sx"></a>

<a id="关键接口-3"></a>

<a id="model-fun-asr-realtime-8b0d2507910sx"></a>

### Qwen-Audio-ASR-Streaming 与 Fun-ASR-Realtime

这两个系列共用以下会话、回调和识别结果接口。各模型支持的字段以本页「请求参数」为准。

<a id="recognition类"></a>

<a id="model-qwen-audio-asr-streaming-adcb5e9bddbyq"></a>

<a id="shared-7"></a>

#### `Recognition`类

<a id="model-fun-asr-realtime-adcb5e9bddbyq"></a>

`Recognition`通过`import com.alibaba.dashscope.audio.asr.recognition.Recognition;`方式引入。它的关键接口如下：

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-6"></a><pre class="language-java"><code>public void call(RecognitionParam param, final ResultCallback&lt;RecognitionResult&gt; callback)
</code></pre></td><td><ul><li><code>param</code>：请求参数</li><li><code>callback</code>：回调接口（ResultCallback）</li></ul></td><td>无</td><td>基于回调形式的流式实时识别，该方法不会阻塞当前线程。</td></tr><tr><td><a id="code-block-7"></a><pre class="language-java"><code>public String call(RecognitionParam param, File file)
</code></pre></td><td><ul><li><code>param</code>：请求参数</li><li><code>file</code>：待识别音频文件</li></ul></td><td>识别结果</td><td>基于本地文件的非流式调用，该方法会阻塞当前线程直到全部音频读完，该方法要求所识别文件具有可读权限。</td></tr><tr><td><a id="code-block-8"></a><pre class="language-java"><code>public Flowable&lt;RecognitionResult&gt; streamCall(RecognitionParam param, Flowable&lt;ByteBuffer&gt; audioFrame)
</code></pre></td><td><ul><li><code>param</code>：请求参数</li><li><code>audioFrame</code>：<code>Flowable&lt;ByteBuffer&gt;</code>实例</li></ul></td><td><code>Flowable&lt;RecognitionResult&gt;</code></td><td>基于Flowable的流式实时识别。</td></tr><tr><td><a id="code-block-9"></a><pre class="language-java"><code>public void sendAudioFrame(ByteBuffer audioFrame)
</code></pre></td><td><ul><li><code>audioFrame</code>：二进制音频流，为<code>ByteBuffer</code>类型</li></ul></td><td>无</td><td>推送音频，每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。<p>识别结果通过回调接口（ResultCallback）的onEvent方法获取。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-java"><code>public void stop()
</code></pre></td><td>无</td><td>无</td><td>停止实时识别。<p>该方法会阻塞当前线程，直到回调实例<code>ResultCallback</code>的<code>onComplete</code>或者<code>onError</code>被调用之后才会解除对当前线程的阻塞。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-java"><code>boolean getDuplexApi().close(int code, String reason)
</code></pre></td><td>code: WebSocket关闭码（Close Code）<p>reason：关闭原因</p><p>这两个参数可参考<a href="https://datatracker.ietf.org/doc/html/rfc6455#section-7.1.5">The WebSocket Protocol</a>文档进行配置</p></td><td>true</td><td>在任务结束后，无论是否出现异常都需要关闭WebSocket连接，避免造成连接泄漏。关于如何复用连接提升效率请参考<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/speech-recognition-best-practices.md#java">高并发最佳实践</a>。</td></tr><tr><td><a id="code-block-12"></a><pre class="language-java"><code>public String getLastRequestId()
</code></pre></td><td>无</td><td>requestId</td><td>获取当前任务的requestId，在调用<code>call</code>、<code>streamingCall</code>开始新任务之后可以使用。<div><div><p><strong>说明</strong>该方法自2.18.0版本及以后的SDK中才开始提供。</p></div></div></td></tr><tr><td><a id="code-block-13"></a><pre class="language-java"><code>public long getFirstPackageDelay()
</code></pre></td><td>无</td><td>首包延迟</td><td>获取首包延迟，从发送第一包音频到收到首包识别结果延迟，在任务完成后使用。<div><div><p><strong>说明</strong>该方法自2.18.0版本及以后的SDK中才开始提供。</p></div></div></td></tr><tr><td><a id="code-block-14"></a><pre class="language-java"><code>public long getLastPackageDelay()
</code></pre></td><td>无</td><td>尾包延迟</td><td>获得尾包延迟，发送<code>stop</code>指令到最后一包识别结果下发耗时，在任务完成后使用。<div><div><p><strong>说明</strong>该方法自2.18.0版本及以后的SDK中才开始提供。</p></div></div></td></tr></tbody></table>

<a id="回调接口-resultcallback"></a>

<a id="model-qwen-audio-asr-streaming-3639e1cb40mxi"></a>

<a id="shared-9"></a>

#### 回调接口（`ResultCallback`）

<a id="model-fun-asr-realtime-3639e1cb40mxi"></a>

双向流式调用时，服务端会通过回调的方式，将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

回调方法的实现，通过继承抽象类`ResultCallback`完成，继承该抽象类时，您可以指定泛型为`RecognitionResult`。`RecognitionResult`封装了服务器返回的数据结构。

由于Java支持连接复用，因此没有`onClose`和`onOpen`。

<a id="code-block-15"></a>

```java
ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
    @Override
    public void onEvent(RecognitionResult result) {
        System.out.println("RequestId为：" + result.getRequestId());
        // 在此实现处理语音识别结果的逻辑
    }

    @Override
    public void onComplete() {
        System.out.println("任务完成");
    }

    @Override
    public void onError(Exception e) {
        System.out.println("任务失败：" + e.getMessage());
    }
};
```

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-16"></a><pre class="language-java"><code>public void onEvent(RecognitionResult result)
</code></pre></td><td><code>result</code>：<a href="#model-qwen-audio-asr-streaming-11a082e1d9ijq">实时识别结果（RecognitionResult）</a></td><td>无</td><td>当服务有回复时会被回调。</td></tr><tr><td><a id="code-block-17"></a><pre class="language-java"><code>public void onComplete()
</code></pre></td><td>无</td><td>无</td><td>任务完成后该接口被回调。</td></tr><tr><td><a id="code-block-18"></a><pre class="language-java"><code>public void onError(Exception e)
</code></pre></td><td><code>e</code>：异常信息</td><td>无</td><td>发生异常时该接口被回调。</td></tr></tbody></table>

<a id="实时识别结果-recognitionresult"></a>

<a id="model-qwen-audio-asr-streaming-11a082e1d9ijq"></a>

<a id="shared-11"></a>

<a id="响应结果"></a>

<a id="model-qwen-audio-asr-streaming-60280ef1ec77f"></a>

<a id="响应结果-3"></a>

<a id="model-fun-asr-realtime-60280ef1ec77f"></a>

#### 实时识别结果（`RecognitionResult`）

<a id="model-fun-asr-realtime-11a082e1d9ijq"></a>

`RecognitionResult`代表一次实时识别的结果。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-19"></a><pre class="language-java"><code>public String getRequestId()
</code></pre></td><td>无</td><td>requestId</td><td>获取requestId。</td></tr><tr><td><a id="code-block-20"></a><pre class="language-java"><code>public boolean isSentenceEnd()
</code></pre></td><td>无</td><td>是否是完整句子，即产生断句</td><td>判断给定句子是否已经结束。</td></tr><tr><td><a id="code-block-21"></a><pre class="language-java"><code>public Sentence getSentence()
</code></pre></td><td>无</td><td><a href="#model-qwen-audio-asr-streaming-e3e502b072h3a">单句信息（Sentence）</a></td><td>获取单句信息，包括时间戳和文本信息等。</td></tr></tbody></table>

<a id="单句信息-sentence"></a>

<a id="model-qwen-audio-asr-streaming-e3e502b072h3a"></a>

<a id="shared-13"></a>

#### 单句信息（`Sentence`）

<a id="model-fun-asr-realtime-e3e502b072h3a"></a>

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-22"></a><pre class="language-java"><code>public Long getBeginTime()
</code></pre></td><td>无</td><td>句子开始时间，单位为ms</td><td>返回句子开始时间。</td></tr><tr><td><a id="code-block-23"></a><pre class="language-java"><code>public Long getEndTime()
</code></pre></td><td>无</td><td>句子结束时间，单位为ms</td><td>返回句子结束时间。</td></tr><tr><td><a id="code-block-24"></a><pre class="language-java"><code>public String getText()
</code></pre></td><td>无</td><td>识别文本</td><td>返回识别文本。</td></tr><tr><td><a id="code-block-25"></a><pre class="language-java"><code>public List&lt;Word&gt; getWords()
</code></pre></td><td>无</td><td><a href="#model-qwen-audio-asr-streaming-125fb5faa3y7t">字时间戳信息（Word）</a>的List集合</td><td>返回字时间戳信息。</td></tr></tbody></table>

<a id="字时间戳信息-word"></a>

<a id="model-qwen-audio-asr-streaming-125fb5faa3y7t"></a>

<a id="shared-15"></a>

#### 字时间戳信息（`Word`）

<a id="model-fun-asr-realtime-125fb5faa3y7t"></a>

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-26"></a><pre class="language-java"><code>public long getBeginTime()
</code></pre></td><td>无</td><td>字开始时间，单位为ms</td><td>返回字开始时间。</td></tr><tr><td><a id="code-block-27"></a><pre class="language-java"><code>public long getEndTime()
</code></pre></td><td>无</td><td>字结束时间，单位为ms</td><td>返回字结束时间。</td></tr><tr><td><a id="code-block-28"></a><pre class="language-java"><code>public String getText()
</code></pre></td><td>无</td><td>字</td><td>返回识别的字。</td></tr><tr><td><a id="code-block-29"></a><pre class="language-java"><code>public String getPunctuation()
</code></pre></td><td>无</td><td>标点</td><td>返回标点。</td></tr></tbody></table>

<a id="错误码"></a>

<a id="model-qwen-audio-asr-streaming-605d5ca873bnd"></a>

<a id="shared-17"></a>

## 错误码

<a id="model-qwen-audio-asr-message-605d5ca873bnd"></a>

<a id="model-fun-asr-realtime-605d5ca873bnd"></a>

如遇报错问题，请参见[错误码](../model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，可加入[语音 SDK 示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo)中列出的开发者群反馈问题，并提供Request ID，以便进一步排查问题。

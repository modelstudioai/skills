# Qwen-Audio-ASR-Message实时语音识别Java SDK

本文介绍Qwen-Audio-3.1-ASR-Flash-Message实时语音识别Java SDK的参数和接口细节。

## 前提条件

-   已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。请配置API Key到环境变量，而非硬编码在代码中，防范因代码泄露导致的安全风险。
-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

[Recognition类](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#adcb5e9bddbyq)提供了非流式调用和双向流式调用等接口。请根据实际需求选择合适的调用方式：

-   非流式调用：针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
-   双向流式调用：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

#### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

实例化Recognition类，调用`call`方法绑定请求参数和待识别文件，进行识别并最终获取识别结果。

```
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
                        .model("qwen-audio-3.1-asr-flash-message")
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
    

识别传入麦克风的语音

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
                .model("qwen-audio-3.1-asr-flash-message")
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

识别本地语音文件

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
                .model("qwen-audio-3.1-asr-flash-message")
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

#### 双向流式调用：基于Flowable

提交单个语音实时转写任务，通过实现工作流（Flowable）的方式流式输出实时识别结果。

Flowable 是 RxJava 中用于处理响应式数据流的类。关于Flowable的使用，请参见[Flowable API详情](https://reactivex.io/RxJava/2.x/javadoc/io/reactivex/Flowable.html)。

直接调用Recognition类的`streamCall`方法开始识别。

`streamCall`方法返回一个`Flowable<RecognitionResult>`实例，您可以调用`Flowable`实例的`blockingForEach`、`subscribe`等方法处理识别结果。识别结果封装在`RecognitionResult`中。

`streamCall`方法需要传入两个参数：

-   `RecognitionParam`实例（请求参数）：通过它可以设置语音识别所需的模型、采样率、音频格式等参数。
-   `Flowable<ByteBuffer>`实例：您需要创建一个`Flowable<ByteBuffer>`类型的实例，并在其中实现解析音频流的方法。

```
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
                .model("qwen-audio-3.1-asr-flash-message")
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

### 高并发调用

在DashScope Java SDK中，采用了OkHttp3的连接池技术，以减少重复建立连接的开销。详情请参见[高并发最佳实践](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_hc_h3)。

## 接口地址

SDK的接口地址需在初始化前设置为下方地址（包含WorkspaceId）。如需切换到其他地域，请修改 `Constants.baseWebsocketApiUrl`为对应地域的URL。

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

## 请求参数

通过`RecognitionParam`的链式方法配置模型、采样率、音频格式等参数。配置完成的参数对象传入[Recognition类](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#adcb5e9bddbyq)的`call`/`streamCall`方法中使用。

```
RecognitionParam param = RecognitionParam.builder()
  .model("qwen-audio-3.1-asr-flash-message")
  .format("pcm")
  .sampleRate(16000)
  .build();
```

**参数**

**类型**

**是否必须**

**说明**

`model`

`String`

是

模型名，设置为 `qwen-audio-3.1-asr-flash-message`。

`sampleRate`

`Integer`

是

采样率（Hz）。

仅支持 `16000` Hz。

`format`

`String`

是

音频格式。

取值范围：

-   `pcm`
-   `wav`
-   `mp3`
-   `opus`
-   `speex`
-   `aac`
-   `amr`

**重要**opus/speex：必须使用Ogg封装；

wav：必须为PCM编码；

amr：仅支持AMR-NB类型。

`disfluency_removal_enabled`

`boolean`

否

是否过滤语气词并对输出结果进行润色，默认值为 `false`。设置为 `true` 时启用。 通过 `.parameter("disfluency_removal_enabled", value)` 设置。

`intermediate_result_enabled`

`boolean`

否

是否返回流式中间结果，默认值为 `false`。设置为 `true` 时返回流式中间结果。 通过 `.parameter("intermediate_result_enabled", value)` 设置。

`keep_dialect`

`boolean`

否

默认 `false`，将方言转写为普通话；设为 `true` 时保留方言表达。通过 `.parameter("keep_dialect", value)` 设置。完整参数说明请参见[客户端事件](raw/_short/qwen-asr-message-client-events-0be34a3639cdd40b.md)。

`vad_model`

`String`

否

可选 `near_meeting_16k`（近场）或 `far_field_meeting_16k`（远场，默认值）。通过 `.parameter("vad_model", value)` 设置。完整参数说明请参见[客户端事件](raw/_short/qwen-asr-message-client-events-0be34a3639cdd40b.md)。

`vocabularyId`

`String`

否

预编译热词列表 ID。

需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。

适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。

使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

`vocabulary`

`Map<String, Integer>`

否

即时热词。

以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5\] 或 50：取 \[1, 5\] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。

适用于临时性、会话级别的热词优化。

与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。

`vocabulary`需要通过 `RecognitionParam` 实例的 `parameter` 方法或者 `parameters` 方法进行设置：

通过parameter设置

```
Map<String, Integer> vocab = new HashMap<>();
vocab.put("张三", 5);
vocab.put("李四", 5);

RecognitionParam param = RecognitionParam.builder()
        .model("qwen-audio-3.1-asr-flash-message")
        .format("pcm")
        .sampleRate(16000)
        .parameter("vocabulary", vocab)
        .build();
```

通过parameters设置

```
Map<String, Integer> vocab = new HashMap<>();
vocab.put("张三", 5);
vocab.put("李四", 5);

Map<String, Object> parameters = new HashMap<>();
parameters.put("vocabulary", vocab);

RecognitionParam param = RecognitionParam.builder()
        .model("qwen-audio-3.1-asr-flash-message")
        .format("pcm")
        .sampleRate(16000)
        .parameters(parameters)
        .build();
```

`max_sentence_silence`

`Integer`

否

VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

默认值：1300。

取值范围：\[200, 6000\]。

`max_sentence_silence`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .parameter("max_sentence_silence", 800)
 .build();
```

通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("max_sentence_silence", 800))
 .build();
```

`heartbeat`

`boolean`

否

是否启用心跳包。

默认值：false。

-   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
-   false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

**说明**使用该字段时，SDK版本不能低于2.19.1。

`heartbeat`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .parameter("heartbeat", true)
 .build();
```

通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("heartbeat", true))
 .build();
```

`speech_noise_threshold`

`float`

否

语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。

取值范围：\[-1.0, 1.0\]。

取值说明：

-   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
-   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤

此参数为高级配置参数，调整可能显著影响识别效果，建议：

-   调整前充分测试验证效果
-   根据实际音频环境小幅度调整（建议步长 0.1）

`speech_noise_threshold`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .parameter("speech_noise_threshold", -0.5)
 .build();
```

通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("speech_noise_threshold", -0.5))
 .build();
```

`input`

`Map<String, Object>`

否

输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见[提升识别准确率](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy)。

Map 中需包含 `context` 键，值为 `List<Map<String, Object>>` 类型的消息数组，每条消息包含以下字段：

-   `role`（String，必选）：消息角色。`user` 表示前几轮用户语音的识别结果或领域相关的词表；`assistant` 表示前几轮大语言模型的回复内容。
-   `content`（List<Map>，必选）：消息内容列表。每个元素包含 `type`（String，role 为 user 时填 `input_text`，role 为 assistant 时填 `text`）和 `text`（String，文本内容）。

**重要**上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。

**重要**携带上下文时，`context` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

**说明**使用该字段时，SDK版本不能低于2.22.23。

`input`通过`RecognitionParam`实例的`input`方法进行设置：

```
// 1. 构建 input 结构体
Map<String, Object> userContent = new HashMap<>();
userContent.put("type", "input_text");
userContent.put("text", "你好啊");

Map<String, Object> assistantContent = new HashMap<>();
assistantContent.put("type", "text");
assistantContent.put("text", "你好啊，我是通义千问，有什么可以帮助你的？");

Map<String, Object> userMessage = new HashMap<>();
userMessage.put("role", "user");
userMessage.put("content", Arrays.asList(userContent));

Map<String, Object> assistantMessage = new HashMap<>();
assistantMessage.put("role", "assistant");
assistantMessage.put("content", Arrays.asList(assistantContent));

Map<String, Object> input = new HashMap<>();
input.put("context", Arrays.asList(userMessage, assistantMessage));

// 2. 通过 input 方法传入
RecognitionParam param = RecognitionParam.builder()
 .model("qwen-audio-3.1-asr-flash-message")
 .format("pcm")
 .sampleRate(16000)
 .input(input)
 .build();
```

`apiKey`

`String`

否

用户API Key。

## 关键接口

### `Recognition`类

`Recognition`通过`import com.alibaba.dashscope.audio.asr.recognition.Recognition;`方式引入。它的关键接口如下：

**接口/方法**

**参数**

**返回值**

**描述**

```
public void call(RecognitionParam param, final ResultCallback<RecognitionResult> callback)
```

-   `param`：[请求参数](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#d72d661a1brzp)
-   `callback`：[回调接口（ResultCallback）](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#3639e1cb40mxi)

无

基于回调形式的流式实时识别，该方法不会阻塞当前线程。

```
public String call(RecognitionParam param, File file)
```

-   `param`：[请求参数](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#d72d661a1brzp)
-   `file`：待识别音频文件

识别结果

基于本地文件的非流式调用，该方法会阻塞当前线程直到全部音频读完，该方法要求所识别文件具有可读权限。

```
public Flowable<RecognitionResult> streamCall(RecognitionParam param, Flowable<ByteBuffer> audioFrame)
```

-   `param`：[请求参数](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#d72d661a1brzp)
-   `audioFrame`：`Flowable<ByteBuffer>`实例

`Flowable<RecognitionResult>`

基于Flowable的流式实时识别。

```
public void sendAudioFrame(ByteBuffer audioFrame)
```

-   `audioFrame`：二进制音频流，为`ByteBuffer`类型

无

推送音频，每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。

识别结果通过[回调接口（ResultCallback）](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#3639e1cb40mxi)的onEvent方法获取。

```
public void stop()
```

无

无

停止实时识别。

该方法会阻塞当前线程，直到回调实例`ResultCallback`的`onComplete`或者`onError`被调用之后才会解除对当前线程的阻塞。

```
boolean getDuplexApi().close(int code, String reason)
```

code: WebSocket关闭码（Close Code）

reason：关闭原因

这两个参数可参考[The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455#section-7.1.5)文档进行配置

true

在任务结束后，无论是否出现异常都需要关闭WebSocket连接，避免造成连接泄漏。关于如何复用连接提升效率请参考[高并发最佳实践](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_hc_h3)。

```
public String getLastRequestId()
```

无

requestId

获取当前任务的requestId，在调用`call`、`streamingCall`开始新任务之后可以使用。

**说明**该方法自2.18.0版本及以后的SDK中才开始提供。

```
public long getFirstPackageDelay()
```

无

首包延迟

获取首包延迟，从发送第一包音频到收到首包识别结果延迟，在任务完成后使用。

**说明**该方法自2.18.0版本及以后的SDK中才开始提供。

```
public long getLastPackageDelay()
```

无

尾包延迟

获得尾包延迟，发送`stop`指令到最后一包识别结果下发耗时，在任务完成后使用。

**说明**该方法自2.18.0版本及以后的SDK中才开始提供。

#### 更新对话上下文

调用 `updateContext` 在识别任务运行过程中更新对话上下文，用于辅助后续音频的识别。该方法要求 DashScope Java SDK 2.23.0 及以上版本。

```
public void updateContext(Map<String, Object> payloadInput)
```

-   **调用时机：**调用 `call(param, callback)` 启动流式识别后、调用 `stop` 前。
-   **参数：**`payloadInput` 为`Map<String, Object>`，传入 `continue-task` 事件的 `payload.input` 对象，包含 `context` 字段，不要额外包装 `payload` 或 `input` 层级。
-   **支持范围与参数约束：**请参见 [continue-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#h-continue-task)。

以下示例复用已启动的 `recognizer` 实例，Java 集合类型通过 `import java.util.*;` 导入。

```
Map<String, Object> userContent = new HashMap<>();
userContent.put("type", "input_text");
userContent.put("text", "这是第 1 轮语音识别测试");
Map<String, Object> userMessage = new HashMap<>();
userMessage.put("role", "user");
userMessage.put("content", Collections.singletonList(userContent));

Map<String, Object> assistantContent = new HashMap<>();
assistantContent.put("type", "text");
assistantContent.put("text", "好的，请开始第 1 轮测试");
Map<String, Object> assistantMessage = new HashMap<>();
assistantMessage.put("role", "assistant");
assistantMessage.put("content", Collections.singletonList(assistantContent));

Map<String, Object> payloadInput = new HashMap<>();
payloadInput.put("context", Arrays.asList(userMessage, assistantMessage));
recognizer.updateContext(payloadInput);
```

### 回调接口（`ResultCallback`）

[双向流式调用](raw/_short/qwen-asr-message-java-sdk-52d0c0e627247c00.md)时，服务端会通过回调的方式，将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

回调方法的实现，通过继承抽象类`ResultCallback`完成，继承该抽象类时，您可以指定泛型为`RecognitionResult`。`RecognitionResult`封装了服务器返回的数据结构。

由于Java支持连接复用，因此没有`onClose`和`onOpen`。

```
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

**接口/方法**

**参数**

**返回值**

**描述**

```
public void onEvent(RecognitionResult result)
```

`result`：[实时识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#11a082e1d9ijq)

无

当服务有回复时会被回调。

```
public void onComplete()
```

无

无

任务完成后该接口被回调。

```
public void onError(Exception e)
```

`e`：异常信息

无

发生异常时该接口被回调。

## 响应结果

### 实时识别结果（`RecognitionResult`）

`RecognitionResult`代表一次实时识别的结果。

**接口/方法**

**参数**

**返回值**

**描述**

```
public String getRequestId()
```

无

requestId

获取requestId。

```
public boolean isSentenceEnd()
```

无

是否是完整句子，即产生断句

判断给定句子是否已经结束。

```
public Sentence getSentence()
```

无

[单句信息（Sentence）](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#e3e502b072h3a)

获取单句信息，包括时间戳和文本信息等。

### 单句信息（`Sentence`）

**接口/方法**

**参数**

**返回值**

**描述**

```
public Long getBeginTime()
```

无

句子开始时间，单位为ms

返回句子开始时间。

```
public Long getEndTime()
```

无

句子结束时间，单位为ms

返回句子结束时间。

```
public String getText()
```

无

识别文本

返回识别文本。

```
public List<Word> getWords()
```

无

[字时间戳信息（Word）](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#125fb5faa3y7t)的List集合

返回字时间戳信息。

### 字时间戳信息（`Word`）

**接口/方法**

**参数**

**返回值**

**描述**

```
public long getBeginTime()
```

无

字开始时间，单位为ms

返回字开始时间。

```
public long getEndTime()
```

无

字结束时间，单位为ms

返回字结束时间。

```
public String getText()
```

无

字

返回识别的字。

```
public String getPunctuation()
```

无

标点

返回标点。

## 错误码

如遇报错问题，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，可加入[语音 SDK 示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo)中列出的开发者群反馈问题，并提供Request ID，以便进一步排查问题。

## 常见问题

### 功能特性

#### Q：在长时间静默的情况下，如何保持与服务端长连接？

将请求参数`heartbeat`设置为true，并持续向服务端发送静音音频。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

#### Q：如何将音频格式转换为满足要求的格式？

可使用[FFmpeg工具](https://ffmpeg.en.lo4d.com/download)，更多用法请参见FFmpeg官网。

```
# 基础转换命令（万能模板）
# -i，作用：输入文件路径，常用值示例：audio.wav
# -c:a，作用：音频编码器，常用值示例：aac, libmp3lame, pcm_s16le
# -b:a，作用：比特率（音质控制），常用值示例：192k, 320k
# -ar，作用：采样率，本模型设为16000
# -ac，作用：声道数，常用值示例：1(单声道), 2(立体声)
# -y，作用：覆盖已存在文件(无需值)
ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

# 例如：WAV → MP3（保持原始质量）
ffmpeg -i input.wav -c:a libmp3lame -q:a 0 -ar 16000 -ac 1 output.mp3
# 例如：MP3 → WAV（16bit PCM标准格式）
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 16000 -ac 1 output.wav
# 例如：M4A → AAC（提取/转换苹果音频）
ffmpeg -i input.m4a -c:a copy output.aac  # 仅用于源音频已为16000 Hz、单声道AAC的情况
ffmpeg -i input.m4a -c:a aac -b:a 64k -ar 16000 -ac 1 output.aac  # 重编码为16000 Hz单声道音频
# 例如：FLAC无损 → Opus（高压缩）
ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on -ar 16000 -ac 1 output.opus
```

#### Q：如何识别本地文件（录音文件）？

识别本地文件有两种方式：

-   直接传入本地文件路径：此种方式在最终识别结束后获取完整识别结果，不适合即时反馈的场景。
    
    参见[非流式调用](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#8341058094tc3)，在[Recognition类](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#adcb5e9bddbyq)的`call`方法中传入文件路径对录音文件直接进行识别。
    
-   将本地文件转成二进制流进行识别：此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。
    
    -   参见[双向流式调用：基于回调](raw/_short/qwen-asr-message-java-sdk-52d0c0e627247c00.md)，通过[Recognition类](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#adcb5e9bddbyq)的`sendAudioFrame`方法向服务端发送二进制流对其进行识别。
    -   参见[双向流式调用：基于Flowable](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#6734e006bc0gp)，通过[Recognition类](https://help.aliyun.com/zh/model-studio/qwen-asr-message-java-sdk#adcb5e9bddbyq)的`streamCall`方法向服务端发送二进制流对其进行识别。

### 故障排查

#### Q：无法识别语音（无识别结果）是什么原因？

1.  请检查请求参数中的音频格式（`format`）和采样率（`sampleRate`/`sample_rate`）设置是否正确且符合参数约束。以下为常见错误示例：
    
    -   音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 wav（参数设置错误）。
    -   音频采样率为 3600Hz，但请求参数 `sampleRate`/`sample_rate` 设置为 48000（参数设置错误）。
    
    可以使用[ffprobe](https://ffmpeg.org/ffprobe.html)工具获取音频的容器、编码、采样率、声道等信息：
    
    ```
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
    ```
    
2.  若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。

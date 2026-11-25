# Paraformer Java SDK

本文介绍Paraformer实时语音识别Java SDK的参数和接口细节。

<a id="819b16d82anlx"></a>

<a id="ef653d0bb7ol9"></a>

<a id="f7fe42677arpg"></a>

<a id="1ac8c3f01dd06"></a>

<a id="874eec6d83jkm"></a>

<a id="f0d00ff99cvjs"></a>

<a id="5add9e5334cwf"></a>

<a id="5d23a676caz62"></a>

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

<a id="前提条件"></a>

<a id="8a24f2ed09vr0"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="模型列表"></a>

<a id="1e173d999c1th"></a>

### 模型列表

<table><thead><tr><th></th><th><strong>paraformer-realtime-v2（推荐）</strong></th><th><strong>paraformer-realtime-8k-v2（推荐）</strong></th></tr></thead><tbody><tr><td><strong>适用场景</strong></td><td><p>直播、会议等场景</p></td><td><p>电话客服、语音信箱等 8kHz 音频的识别场景</p></td></tr><tr><td><strong>采样率</strong></td><td><p>任意</p></td><td><p>8kHz</p></td></tr><tr><td><strong>语种</strong></td><td><p>中文（包含中文普通话和各种方言）、英文、日语、韩语、德语、法语、俄语</p><p>支持的中文方言：上海话、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、江西话、宁夏话、山西话、陕西话、山东话、四川话、天津话、云南话、粤语</p></td><td><p>中文</p></td></tr><tr><td><strong>标点符号预测</strong></td><td><p>默认支持，无需配置</p></td><td><p>默认支持，无需配置</p></td></tr><tr><td><strong>逆文本正则化（ITN）</strong></td><td><p>默认支持，无需配置</p></td><td><p>默认支持，无需配置</p></td></tr><tr><td><strong>定制热词</strong></td><td><p>支持：参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a></p></td><td><p>支持：参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a></p></td></tr><tr><td><strong>指定待识别语种</strong></td><td><p>支持：通过<code>language_hints</code>参数指定</p></td><td><p>不支持</p></td></tr><tr><td><strong>情感识别</strong></td><td><p>不支持</p></td><td><a id="accordion-支持-点击查看使用方式"></a><section><p>支持：（点击查看使用方式）</p><div><p>情感识别遵循如下约束：</p><ul><li>仅限<code>paraformer-realtime-8k-v2</code>模型。</li><li>必须关闭语义断句（可通过<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp">请求参数</a><code>semantic_punctuation_enabled</code>控制）。语义断句默认为关闭状态。</li><li>只有在<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#11a082e1d9ijq">实时识别结果（RecognitionResult）</a>的<code>isSentenceEnd</code>方法返回结果为<code>true</code>时才显示情感识别结果。</li></ul><p>情感识别结果获取方式：调用<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#e3e502b072h3a">单句信息（Sentence）</a>的<code>getEmoTag</code>和<code>getEmoConfidence</code>方法分别获取当前句子的情感和情感置信度。</p></div></section></td></tr></tbody></table>

<a id="快速开始"></a>

<a id="dd017b69c3byd"></a>

## 快速开始

[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)提供了非流式调用和双向流式调用接口。请根据实际需求选择合适的调用方式：

-   非流式调用：针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
-   双向流式调用：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

<a id="非流式调用"></a>

<a id="8341058094tc3"></a>

### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5323116871/CAEQURiBgMDS0c2RpxkiIDNmYjBlMTE3ODQxYTQ3Nzk4MGMxNTc5MjY3OWVjZjlj4709861_20241015153444.149.svg)

实例化[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)，调用`call`方法绑定[请求参数](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp)和待识别文件，进行识别并最终获取识别结果。

<a id="accordion-点击查看完整示例"></a>

点击查看完整示例

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
                        // 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
                        // .apiKey("yourApikey")
                        .model("paraformer-realtime-v2")
                        .format("wav")
                        .sampleRate(16000)
                        // “language_hints”只支持paraformer-realtime-v2模型
                        .parameter("language_hints", new String[]{"zh", "en"})
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

<a id="9d1e5f6852jr8"></a>

### 双向流式调用：基于回调

提交单个语音实时转写任务，通过实现回调接口的方式流式输出实时识别结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5323116871/CAEQURiBgID1ooWUpxkiIDcyOTEyYjZiZmUxNzRkZjVhMTNhYmNkYjI2NzYzYTMy4709861_20241015153444.149.svg)

1.  启动流式语音识别
    
    实例化[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)，调用`call`方法绑定[请求参数](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp)和[回调接口（ResultCallback）](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#3639e1cb40mxi)并启动流式语音识别。
    
2.  流式传输
    
    循环调用[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)的`sendAudioFrame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。
    
    在发送音频数据的过程中，服务端会通过[回调接口（ResultCallback）](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#3639e1cb40mxi)的`onEvent`方法，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)的`stop`方法结束语音识别。
    
    该方法会阻塞当前线程，直到[回调接口（ResultCallback）](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#3639e1cb40mxi)的`onComplete`或者`onError`回调触发后才会释放线程阻塞。
    

<a id="accordion-点击查看完整示例-2"></a>

点击查看完整示例

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
                // 若没有将API Key配置到环境变量中，需将apiKey替换为自己的API Key
                // .apiKey("yourApikey")
                .model("paraformer-realtime-v2")
                .format("wav")
                .sampleRate(16000)
                // “language_hints”只支持paraformer-realtime-v2模型
                .parameter("language_hints", new String[]{"zh", "en"})
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
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.CountDownLatch;
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
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.submit(new RealtimeRecognitionTask(Paths.get(System.getProperty("user.dir"), "{YOUR_AUDIO_FILE}")));
        executorService.shutdown();

        // wait for all tasks to complete
        executorService.awaitTermination(1, TimeUnit.MINUTES);
        System.exit(0);
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
                // 若没有将API Key配置到环境变量中，需将apiKey替换为自己的API Key
                // .apiKey("yourApikey")
                .model("paraformer-realtime-v2")
                .format("wav")
                .sampleRate(16000)
                // “language_hints”只支持paraformer-realtime-v2模型
                .parameter("language_hints", new String[]{"zh", "en"})
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
            // chunk size set to 1 seconds for 16KHz sample rate
            byte[] buffer = new byte[3200];
            int bytesRead;
            // Loop to read chunks of the file
            while ((bytesRead = fis.read(buffer)) != -1) {
                ByteBuffer byteBuffer;
                // Handle the last chunk which might be smaller than the buffer size
                System.out.println(TimeUtils.getTimestamp()+" "+"[" + threadName + "] bytesRead: " + bytesRead);
                if (bytesRead < buffer.length) {
                    byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
                } else {
                    byteBuffer = ByteBuffer.wrap(buffer);
                }

                recognizer.sendAudioFrame(byteBuffer);
                buffer = new byte[3200];
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

<a id="6734e006bc0gp"></a>

### 双向流式调用：基于Flowable

提交单个语音实时转写任务，通过实现工作流（Flowable）的方式流式输出实时识别结果。

Flowable 是一个用于工作流和业务流程管理的开源框架，它基于 Apache 2.0 许可证发布。关于Flowable的使用，请参见[Flowable API详情](http://reactivex.io/RxJava/2.x/javadoc/)。

<a id="accordion-点击查看完整示例-3"></a>

点击查看完整示例

直接调用[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)的`streamCall`方法开始识别。

`streamCall`方法返回一个`Flowable<RecognitionResult>`实例，您可以调用`Flowable`实例的`blockingForEach`、`subscribe`等方法处理识别结果。识别结果封装在`RecognitionResult`中。

`streamCall`方法需要传入两个参数：

-   `RecognitionParam`实例（[请求参数](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp)）：通过它可以设置语音识别所需的模型、采样率、音频格式等参数。
-   `Flowable<ByteBuffer>`实例：您需要创建一个`Flowable<ByteBuffer>`类型的实例，并在其中实现解析音频流的方法。

<a id="code-block-2"></a>

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
                // 若没有将API Key配置到环境变量中，需将apiKey替换为自己的API Key
                // .apiKey("yourApikey")
                .model("paraformer-realtime-v2")
                .format("pcm")
                .sampleRate(16000)
                // “language_hints”只支持paraformer-realtime-v2模型
                .parameter("language_hints", new String[]{"zh", "en"})
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

<a id="ea8503736dlf7"></a>

### 高并发调用

在DashScope Java SDK中，采用了OkHttp3的连接池技术，以减少重复建立连接的开销。详情请参见[实时语音识别高并发场景](https://help.aliyun.com/zh/model-studio/paraformer-in-high-concurrency-scenarios)。

<a id="请求参数"></a>

<a id="d72d661a1brzp"></a>

## 请求参数

通过`RecognitionParam`的链式方法配置模型、采样率、音频格式等参数。配置完成的参数对象传入[Recognition类](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#adcb5e9bddbyq)的`call`/`streamCall`方法中使用。

<a id="accordion-点击查看示例"></a>

点击查看示例

<a id="code-block-3"></a>

```java
RecognitionParam param = RecognitionParam.builder()
  .model("paraformer-realtime-v2")
  .format("pcm")
  .sampleRate(16000)
  // “language_hints”只支持paraformer-realtime-v2模型
  .parameter("language_hints", new String[]{"zh", "en"})
  .build();
```

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>默认值</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>用于实时语音识别的模型。详情请参见<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#1e173d999c1th">模型列表</a>。</p></td></tr><tr><td><p>sampleRate</p></td><td><p>Integer</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>设置待识别音频采样率（单位Hz）。</p><p>因模型而异：</p><ul><li>paraformer-realtime-v2支持任意采样率。</li><li>paraformer-realtime-8k-v2仅支持8000Hz采样率。</li></ul></td></tr><tr><td><p>format</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>设置待识别音频格式。</p><p>支持的音频格式：pcm、wav、mp3、opus、speex、aac、amr。</p><div><div><p><strong>重要</strong>opus/speex：必须使用Ogg封装；</p><p>wav：必须为PCM编码；</p><p>amr：仅支持AMR-NB类型。</p></div></div></td></tr><tr><td><p>vocabularyId</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>否</p></td><td><p>设置热词ID，若未设置则不生效。v2及更高版本模型设置热词ID时使用该字段。</p><p>在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a>。</p></td></tr><tr><td><p>disfluencyRemovalEnabled</p></td><td><p>boolean</p></td><td><p>false</p></td><td><p>否</p></td><td><p>设置是否过滤语气词：</p><ul><li>true：过滤语气词</li><li>false（默认）：不过滤语气词</li></ul></td></tr><tr><td><p>language_hints</p></td><td><p>String[]</p></td><td><p>[&quot;zh&quot;, &quot;en&quot;]</p></td><td><p>否</p></td><td><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>目前支持的语言代码：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul><p>该参数仅对支持多语言的模型生效（参见<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#1e173d999c1th">模型列表</a>）。</p><div><div><p><strong>说明</strong><code>language_hints</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-2-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;language_hints&quot;, new String[]{&quot;zh&quot;, &quot;en&quot;})
 .build();
</code></pre></div><a id="fig-code-group-2-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-2-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;language_hints&quot;, new String[]{&quot;zh&quot;, &quot;en&quot;}))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>semantic_punctuation_enabled</p></td><td><p>boolean</p></td><td><p>false</p></td><td><p>否</p></td><td><p>设置是否开启语义断句，默认关闭。</p><ul><li>true：开启语义断句，关闭VAD（Voice Activity Detection，语音活动检测）断句。</li><li>false（默认）：开启VAD（Voice Activity Detection，语音活动检测）断句，关闭语义断句。</li></ul><p>语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。</p><p>通过调整<code>semantic_punctuation_enabled</code>参数，可以灵活切换语音识别的断句方式以适应不同场景需求。</p><p>该参数仅在模型为v2及更高版本时生效。</p><div><div><p><strong>说明</strong><code>semantic_punctuation_enabled</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-3-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;semantic_punctuation_enabled&quot;, true)
 .build();
</code></pre></div><a id="fig-code-group-3-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-3-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;semantic_punctuation_enabled&quot;, true))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>max_sentence_silence</p></td><td><p>Integer</p></td><td><p>800</p></td><td><p>否</p></td><td><p>设置VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。</p><p>当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。</p><p>参数范围为200ms至6000ms，默认值为800ms。</p><p>该参数仅在<code>semantic_punctuation_enabled</code>参数为false（VAD断句）且模型为v2及更高版本时生效。</p><div><div><p><strong>说明</strong><code>max_sentence_silence</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-4-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;max_sentence_silence&quot;, 800)
 .build();
</code></pre></div><a id="fig-code-group-4-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-4-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;max_sentence_silence&quot;, 800))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>multi_threshold_mode_enabled</p></td><td><p>boolean</p></td><td><p>false</p></td><td><p>否</p></td><td><p>该开关打开时（true）可以防止VAD断句切割过长。默认关闭。</p><p>该参数仅在<code>semantic_punctuation_enabled</code>参数为false（VAD断句）且模型为v2及更高版本时生效。</p><div><div><p><strong>说明</strong><code>multi_threshold_mode_enabled</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-5-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;multi_threshold_mode_enabled&quot;, true)
 .build();
</code></pre></div><a id="fig-code-group-5-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-5-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;multi_threshold_mode_enabled&quot;, true))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>punctuation_prediction_enabled</p></td><td><p>boolean</p></td><td><p>true</p></td><td><p>否</p></td><td><p>设置是否在识别结果中自动添加标点：</p><ul><li>true（默认）：是</li><li>false：否</li></ul><p>该参数仅在模型为v2及更高版本时生效。</p><div><div><p><strong>说明</strong><code>punctuation_prediction_enabled</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-6-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;punctuation_prediction_enabled&quot;, false)
 .build();
</code></pre></div><a id="fig-code-group-6-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-6-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;punctuation_prediction_enabled&quot;, false))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>heartbeat</p></td><td><p>boolean</p></td><td><p>false</p></td><td><p>否</p></td><td><p>当需要与服务端保持长连接时，可通过该开关进行控制：</p><ul><li><p>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</p></li><li><p>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</p><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p></li></ul><p>该参数仅在模型为v2及更高版本时生效。</p><div><div><p><strong>说明</strong>使用该字段时，SDK版本不能低于2.19.1。</p><p><code>heartbeat</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-7-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;heartbeat&quot;, true)
 .build();
</code></pre></div><a id="fig-code-group-7-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-7-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;heartbeat&quot;, true))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>inverse_text_normalization_enabled</p></td><td><p>boolean</p></td><td><p>true</p></td><td><p>否</p></td><td><p>设置是否开启ITN（Inverse Text Normalization，逆文本正则化）。</p><p>默认开启（true）。开启后，中文数字将转换为阿拉伯数字。</p><p>该参数仅在模型为v2及更高版本时生效。</p><div><div><p><strong>说明</strong><code>inverse_text_normalization_enabled</code>需要通过<code>RecognitionParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-8-通过parameter设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameter(&quot;inverse_text_normalization_enabled&quot;, false)
 .build();
</code></pre></div><a id="fig-code-group-8-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-8-通过parameters设置"></a><pre class="language-java"><code>RecognitionParam param = RecognitionParam.builder()
 .model(&quot;paraformer-realtime-v2&quot;)
 .format(&quot;pcm&quot;)
 .sampleRate(16000)
 .parameters(Collections.singletonMap(&quot;inverse_text_normalization_enabled&quot;, false))
 .build();
</code></pre></div></div></div></div></td></tr><tr><td><p>apiKey</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>否</p></td><td><p>用户API Key。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="8b0d2507910sx"></a>

<a id="关键接口"></a>

## 接口参考

<a id="recognition类"></a>

<a id="adcb5e9bddbyq"></a>

### `Recognition`类

`Recognition`通过“`import com.alibaba.dashscope.audio.asr.recognition.Recognition;`”方式引入。它的关键接口如下：

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-4"></a><pre class="language-java"><code>public void call(RecognitionParam param, final ResultCallback&lt;RecognitionResult&gt; callback)
</code></pre></td><td><ul><li><code>param</code>：<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp">请求参数</a></li><li><code>callback</code>：<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#3639e1cb40mxi">回调接口（ResultCallback）</a></li></ul></td><td><p>无</p></td><td><p>基于回调形式的流式实时识别，该方法不会阻塞当前线程。</p></td></tr><tr><td><a id="code-block-5"></a><pre class="language-java"><code>public String call(RecognitionParam param, File file)
</code></pre></td><td><ul><li><code>param</code>：<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp">请求参数</a></li><li><code>file</code>：待识别音频文件</li></ul></td><td><p>识别结果</p></td><td><p>基于本地文件的非流式调用，该方法会阻塞当前线程直到全部音频读完，该方法要求所识别文件具有可读权限。</p></td></tr><tr><td><a id="code-block-6"></a><pre class="language-java"><code>public Flowable&lt;RecognitionResult&gt; streamCall(RecognitionParam param, Flowable&lt;ByteBuffer&gt; audioFrame)
</code></pre></td><td><ul><li><code>param</code>：<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp">请求参数</a></li><li><code>audioFrame</code>：<code>Flowable&lt;ByteBuffer&gt;</code>实例</li></ul></td><td><p><code>Flowable&lt;RecognitionResult&gt;</code></p></td><td><p>基于Flowable的流式实时识别。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-java"><code>public void sendAudioFrame(ByteBuffer audioFrame)
</code></pre></td><td><ul><li><code>audioFrame</code>：二进制音频流，为<code>ByteBuffer</code>类型</li></ul></td><td><p>无</p></td><td><p>推送音频，每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。</p><p>识别结果通过<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#3639e1cb40mxi">回调接口（ResultCallback）</a>的onEvent方法获取。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-java"><code>public void stop()
</code></pre></td><td><p>无</p></td><td><p>无</p></td><td><p>停止实时识别。</p><p>该方法会阻塞当前线程，直到回调实例<code>ResultCallback</code>的<code>onComplete</code>或者<code>onError</code>被调用之后才会解除对当前线程的阻塞。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-java"><code>recognizer.getDuplexApi().close(int code, String reason)
</code></pre></td><td><p>code: WebSocket关闭码（Close Code）</p><p>reason：关闭原因</p><p>这两个参数可参考<a href="https://datatracker.ietf.org/doc/html/rfc6455#section-7.1.5">The WebSocket Protocol</a>文档进行配置</p></td><td><p>true</p></td><td><p>在任务结束后，无论是否出现异常都需要关闭WebSocket连接，避免造成连接泄漏。关于如何复用连接提升效率请参考<a href="https://help.aliyun.com/zh/model-studio/paraformer-in-high-concurrency-scenarios">实时语音识别高并发场景</a>。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-java"><code>public String getLastRequestId()
</code></pre></td><td><p>无</p></td><td><p>requestId</p></td><td><p>获取当前任务的requestId，在调用<code>call</code>、<code>streamingCall</code>开始新任务之后可以使用。</p><div><div><p><strong>说明</strong>该方法自2.18.0版本及以后的SDK中才开始提供。</p></div></div></td></tr><tr><td><a id="code-block-11"></a><pre class="language-java"><code>public long getFirstPackageDelay()
</code></pre></td><td><p>无</p></td><td><p>首包延迟</p></td><td><p>获取首包延迟，从发送第一包音频到收到首包识别结果延迟，在任务完成后使用。</p><div><div><p><strong>说明</strong>该方法自2.18.0版本及以后的SDK中才开始提供。</p></div></div></td></tr><tr><td><a id="code-block-12"></a><pre class="language-java"><code>public long getLastPackageDelay()
</code></pre></td><td><p>无</p></td><td><p>尾包延迟</p></td><td><p>获得尾包延迟，发送<code>stop</code>指令到最后一包识别结果下发耗时，在任务完成后使用。</p><div><div><p><strong>说明</strong>该方法自2.18.0版本及以后的SDK中才开始提供。</p></div></div></td></tr></tbody></table>

<a id="回调接口-resultcallback"></a>

<a id="3639e1cb40mxi"></a>

### 回调接口（`ResultCallback`）

[双向流式调用](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#9d1e5f6852jr8)时，服务端会通过回调的方式，将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

回调方法的实现，通过继承抽象类`ResultCallback`完成，继承该抽象类时，您可以指定泛型为`RecognitionResult`。`RecognitionResult`封装了服务器返回的数据结构。

由于Java支持连接复用，因此没有`onClose`和`onOpen`。

<a id="accordion-示例"></a>

示例

<a id="code-block-13"></a>

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

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-14"></a><pre class="language-java"><code>public void onEvent(RecognitionResult result)
</code></pre></td><td><p><code>result</code>：<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#11a082e1d9ijq">实时识别结果（RecognitionResult）</a></p></td><td><p>无</p></td><td><p>当服务有回复时会被回调。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-java"><code>public void onComplete()
</code></pre></td><td><p>无</p></td><td><p>无</p></td><td><p>任务完成后该接口被回调。</p></td></tr><tr><td><a id="code-block-16"></a><pre class="language-java"><code>public void onError(Exception e)
</code></pre></td><td><p><code>e</code>：异常信息</p></td><td><p>无</p></td><td><p>发生异常时该接口被回调。</p></td></tr></tbody></table>

<a id="响应结果"></a>

<a id="60280ef1ec77f"></a>

### 响应结果

<a id="实时识别结果-recognitionresult"></a>

<a id="11a082e1d9ijq"></a>

#### 实时识别结果（`RecognitionResult`）

`RecognitionResult`代表一次实时识别的结果。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-17"></a><pre class="language-java"><code>public String getRequestId()
</code></pre></td><td><p>无</p></td><td><p>requestId</p></td><td><p>获取requestId。</p></td></tr><tr><td><a id="code-block-18"></a><pre class="language-java"><code>public boolean isSentenceEnd()
</code></pre></td><td><p>无</p></td><td><p>是否是完整句子，即产生断句</p></td><td><p>判断给定句子是否已经结束。</p></td></tr><tr><td><a id="code-block-19"></a><pre class="language-java"><code>public Sentence getSentence()
</code></pre></td><td><p>无</p></td><td><p><a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#e3e502b072h3a">单句信息（Sentence）</a></p></td><td><p>获取单句信息，包括时间戳和文本信息等。</p></td></tr></tbody></table>

<a id="单句信息-sentence"></a>

<a id="e3e502b072h3a"></a>

#### 单句信息（`Sentence`）

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-20"></a><pre class="language-java"><code>public Long getBeginTime()
</code></pre></td><td><p>无</p></td><td><p>句子开始时间，单位为ms</p></td><td><p>返回句子开始时间。</p></td></tr><tr><td><a id="code-block-21"></a><pre class="language-java"><code>public Long getEndTime()
</code></pre></td><td><p>无</p></td><td><p>句子结束时间，单位为ms</p></td><td><p>返回句子结束时间。</p></td></tr><tr><td><a id="code-block-22"></a><pre class="language-java"><code>public String getText()
</code></pre></td><td><p>无</p></td><td><p>识别文本</p></td><td><p>返回识别文本。</p></td></tr><tr><td><a id="code-block-23"></a><pre class="language-java"><code>public List&lt;Word&gt; getWords()
</code></pre></td><td><p>无</p></td><td><p><a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#125fb5faa3y7t">字时间戳信息（Word）</a>的List集合</p></td><td><p>返回字时间戳信息。</p></td></tr><tr><td><a id="code-block-24"></a><pre class="language-java"><code>public String getEmoTag()
</code></pre></td><td><p>无</p></td><td><p>当前句子的情感</p></td><td><p>返回当前句子的情感：</p><ul><li>positive：正面情感，如开心、满意</li><li>negative：负面情感，如愤怒、沉闷</li><li>neutral：无明显情感</li></ul><p>情感识别遵循如下约束：</p><ul><li>仅限<code>paraformer-realtime-8k-v2</code>模型。</li><li>必须关闭语义断句（可通过<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp">请求参数</a><code>semantic_punctuation_enabled</code>控制）。语义断句默认为关闭状态。</li><li>只有在<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#11a082e1d9ijq">实时识别结果（RecognitionResult）</a>的<code>isSentenceEnd</code>方法返回结果为<code>true</code>时才显示情感识别结果。</li></ul></td></tr><tr><td><a id="code-block-25"></a><pre class="language-java"><code>public Double getEmoConfidence()
</code></pre></td><td><p>无</p></td><td><p>当前句子识别情感的置信度</p></td><td><p>返回当前句子识别情感的置信度，取值范围：[0.0,1.0]，值越大表示置信度越高。</p><p>情感识别遵循如下约束：</p><ul><li>仅限<code>paraformer-realtime-8k-v2</code>模型。</li><li>必须关闭语义断句（可通过<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#d72d661a1brzp">请求参数</a><code>semantic_punctuation_enabled</code>控制）。语义断句默认为关闭状态。</li><li>只有在<a href="paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md#11a082e1d9ijq">实时识别结果（RecognitionResult）</a>的<code>isSentenceEnd</code>方法返回结果为<code>true</code>时才显示情感识别结果。</li></ul></td></tr></tbody></table>

<a id="字时间戳信息-word"></a>

<a id="125fb5faa3y7t"></a>

#### 字时间戳信息（`Word`）

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-26"></a><pre class="language-java"><code>public long getBeginTime()
</code></pre></td><td><p>无</p></td><td><p>字开始时间，单位为ms</p></td><td><p>返回字开始时间。</p></td></tr><tr><td><a id="code-block-27"></a><pre class="language-java"><code>public long getEndTime()
</code></pre></td><td><p>无</p></td><td><p>字结束时间，单位为ms</p></td><td><p>返回字结束时间。</p></td></tr><tr><td><a id="code-block-28"></a><pre class="language-java"><code>public String getText()
</code></pre></td><td><p>无</p></td><td><p>字</p></td><td><p>返回识别的字。</p></td></tr><tr><td><a id="code-block-29"></a><pre class="language-java"><code>public String getPunctuation()
</code></pre></td><td><p>无</p></td><td><p>标点</p></td><td><p>返回标点。</p></td></tr></tbody></table>

<a id="更多示例"></a>

<a id="a197604bf2kyv"></a>

## 更多示例

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="错误码"></a>

<a id="605d5ca873bnd"></a>

## 错误码

如遇报错问题，请参见[错误码](../model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

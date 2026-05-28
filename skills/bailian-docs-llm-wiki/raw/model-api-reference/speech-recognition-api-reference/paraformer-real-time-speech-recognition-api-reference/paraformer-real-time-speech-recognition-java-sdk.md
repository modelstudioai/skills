# Paraformer实时语音识别Java SDK

本文介绍Paraformer实时语音识别Java SDK的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Gummy/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

**在线体验**：仅paraformer-realtime-v2、paraformer-realtime-8k-v2和paraformer-realtime-v1支持[在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/voice)。

## **前提条件**

-   已开通服务并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。
    
    **说明**
    
    当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。
    
    与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
    
    使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。
    
-   [安装最新版DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## **模型列表**

**paraformer-realtime-v2（推荐）**

**paraformer-realtime-8k-v2（推荐）**

**paraformer-realtime-v1**

**paraformer-realtime-8k-v1**

**适用场景**

直播、会议等场景

电话客服、语音信箱等 8kHz 音频的识别场景

直播、会议等场景

电话客服、语音信箱等 8kHz 音频的识别场景

**采样率**

任意

8kHz

16kHz

8kHz

**语种**

中文（包含中文普通话和各种方言）、英文、日语、韩语、德语、法语、俄语

支持的中文方言：上海话、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、江西话、宁夏话、山西话、陕西话、山东话、四川话、天津话、云南话、粤语

中文

中文

中文

**标点符号预测**

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

**逆文本正则化（ITN）**

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

**定制热词**

✅ 参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)

✅ 参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)

✅ 参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)

✅ 参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)

**指定待识别语种**

✅ 通过`language_hints`参数指定

❌

❌

❌

**情感识别**

❌

✅ （点击查看使用方式）

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](#d72d661a1brzp)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[实时识别结果（RecognitionResult）](#11a082e1d9ijq)的`isSentenceEnd`方法返回结果为`true`时才显示情感识别结果。
    

情感识别结果获取方式：调用[单句信息（Sentence）](#e3e502b072h3a)的`getEmoTag`和`getEmoConfidence`方法分别获取当前句子的情感和情感置信度。

❌

❌

## **快速开始**

[Recognition类](#adcb5e9bddbyq)提供了非流式调用和双向流式调用接口。请根据实际需求选择合适的调用方式：

-   非流式调用：针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
    
-   双向流式调用：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。
    

### **非流式调用**

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1013285771/CAEQURiBgMDS0c2RpxkiIDNmYjBlMTE3ODQxYTQ3Nzk4MGMxNTc5MjY3OWVjZjlj4709861_20241015153444.149.svg)

实例化[Recognition类](#adcb5e9bddbyq)，调用`call`方法绑定[请求参数](#d72d661a1brzp)和待识别文件，进行识别并最终获取识别结果。

点击查看完整示例

示例中用到的音频为：[asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250210/elouas/asr_example.wav)。

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;

import java.io.File;

public class Main {
    public static void main(String[] args) {
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
            System.out.println("识别结果：" + recognizer.call(param, new File("asr_example.wav")));
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

### **双向流式调用：基于回调**

提交单个语音实时转写任务，通过实现回调接口的方式流式输出实时识别结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1013285771/CAEQURiBgID1ooWUpxkiIDcyOTEyYjZiZmUxNzRkZjVhMTNhYmNkYjI2NzYzYTMy4709861_20241015153444.149.svg)

1.  启动流式语音识别
    
    实例化[Recognition类](#adcb5e9bddbyq)，调用`call`方法绑定[请求参数](#d72d661a1brzp)和[回调接口（ResultCallback）](#3639e1cb40mxi)并启动流式语音识别。
    
2.  流式传输
    
    循环调用[Recognition类](#adcb5e9bddbyq)的`sendAudioFrame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。
    
    在发送音频数据的过程中，服务端会通过[回调接口（ResultCallback）](#3639e1cb40mxi)的`onEvent`方法，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用[Recognition类](#adcb5e9bddbyq)的`stop`方法结束语音识别。
    
    该方法会阻塞当前线程，直到[回调接口（ResultCallback）](#3639e1cb40mxi)的`onComplete`或者`onError`回调触发后才会释放线程阻塞。
    

点击查看完整示例

## 识别传入麦克风的语音

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;

import java.nio.ByteBuffer;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Main {
    public static void main(String[] args) throws InterruptedException {
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

## 识别本地语音文件

示例中用到的音频为：[asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250210/oiydrd/asr_example.wav)。

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;

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
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.submit(new RealtimeRecognitionTask(Paths.get(System.getProperty("user.dir"), "asr_example.wav")));
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

### **双向流式调用：基于Flowable**

提交单个语音实时转写任务，通过实现工作流（Flowable）的方式流式输出实时识别结果。

Flowable 是一个用于工作流和业务流程管理的开源框架，它基于 Apache 2.0 许可证发布。关于Flowable的使用，请参见[Flowable API详情](http://reactivex.io/RxJava/2.x/javadoc/)。

**点击查看完整示例**

直接调用[Recognition类](#adcb5e9bddbyq)的`streamCall`方法开始识别。

`streamCall`方法返回一个`Flowable<RecognitionResult>`实例，您可以调用`Flowable`实例的`blockingForEach`、`subscribe`等方法处理识别结果。识别结果封装在`RecognitionResult`中。

`streamCall`方法需要传入两个参数：

-   `RecognitionParam`实例（[请求参数](#d72d661a1brzp)）：通过它可以设置语音识别所需的模型、采样率、音频格式等参数。
    
-   `Flowable<ByteBuffer>`实例：您需要创建一个`Flowable<ByteBuffer>`类型的实例，并在其中实现解析音频流的方法。
    

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.BackpressureStrategy;
import io.reactivex.Flowable;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;
import java.nio.ByteBuffer;

public class Main {
    public static void main(String[] args) throws NoApiKeyException {
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

### **高并发调用**

在DashScope Java SDK中，采用了OkHttp3的连接池技术，以减少重复建立连接的开销。详情请参见[实时语音识别高并发场景](https://help.aliyun.com/zh/model-studio/paraformer-in-high-concurrency-scenarios)。

## **请求参数**

通过`RecognitionParam`的链式方法配置模型、采样率、音频格式等参数。配置完成的参数对象传入[Recognition类](#adcb5e9bddbyq)的`call`/`streamCall`方法中使用。

**点击查看示例**

```
RecognitionParam param = RecognitionParam.builder()
  .model("paraformer-realtime-v2")
  .format("pcm")
  .sampleRate(16000)
  // “language_hints”只支持paraformer-realtime-v2模型
  .parameter("language_hints", new String[]{"zh", "en"})
  .build();
```

**参数**

**类型**

**默认值**

**是否必须**

**说明**

model

String

\-

是

用于实时语音识别的模型。详情请参见[模型列表](#1e173d999c1th)。

sampleRate

Integer

\-

是

设置待识别音频采样率（单位Hz）。

因模型而异：

-   paraformer-realtime-v2支持任意采样率。
    
-   paraformer-realtime-v1仅支持16000Hz采样。
    
-   paraformer-realtime-8k-v2仅支持8000Hz采样率。
    
-   paraformer-realtime-8k-v1仅支持8000Hz采样率。
    

format

String

\-

是

设置待识别音频格式。

支持的音频格式：pcm、wav、mp3、opus、speex、aac、amr。

**重要**

opus/speex：必须使用Ogg封装；

wav：必须为PCM编码；

amr：仅支持AMR-NB类型。

vocabularyId

String

\-

否

设置热词ID，若未设置则不生效。v2及更高版本模型设置热词ID时使用该字段。

在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。

phraseId

String

\-

否

设置热词ID，若未设置则不生效。v1系列模型设置热词ID时使用该字段。

在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)。

disfluencyRemovalEnabled

boolean

false

否

设置是否过滤语气词：

-   true：过滤语气词
    
-   false（默认）：不过滤语气词
    

language\_hints

String\[\]

\["zh", "en"\]

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。

目前支持的语言代码：

-   zh: 中文
    
-   en: 英文
    
-   ja: 日语
    
-   yue: 粤语
    
-   ko: 韩语
    
-   de：德语
    
-   fr：法语
    
-   ru：俄语
    

该参数仅对支持多语言的模型生效（参见[模型列表](#1e173d999c1th)）。

**说明**

`language_hints`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("language_hints", new String[]{"zh", "en"})
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("language_hints", new String[]{"zh", "en"}))
 .build();
```

semantic\_punctuation\_enabled

boolean

false

否

设置是否开启语义断句，默认关闭。

-   true：开启语义断句，关闭VAD（Voice Activity Detection，语音活动检测）断句。
    
-   false（默认）：开启VAD（Voice Activity Detection，语音活动检测）断句，关闭语义断句。
    

语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。

通过调整`semantic_punctuation_enabled`参数，可以灵活切换语音识别的断句方式以适应不同场景需求。

该参数仅在模型为v2及更高版本时生效。

**说明**

`semantic_punctuation_enabled`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("semantic_punctuation_enabled", true)
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("semantic_punctuation_enabled", true))
 .build();
```

max\_sentence\_silence

Integer

800

否

设置VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。

当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

参数范围为200ms至6000ms，默认值为800ms。

该参数仅在`semantic_punctuation_enabled`参数为false（VAD断句）且模型为v2及更高版本时生效。

**说明**

`max_sentence_silence`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("max_sentence_silence", 800)
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("max_sentence_silence", 800))
 .build();
```

multi\_threshold\_mode\_enabled

boolean

false

否

该开关打开时（true）可以防止VAD断句切割过长。默认关闭。

该参数仅在`semantic_punctuation_enabled`参数为false（VAD断句）且模型为v2及更高版本时生效。

**说明**

`multi_threshold_mode_enabled`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("multi_threshold_mode_enabled", true)
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("multi_threshold_mode_enabled", true))
 .build();
```

punctuation\_prediction\_enabled

boolean

true

否

设置是否在识别结果中自动添加标点：

-   true（默认）：是
    
-   false：否
    

该参数仅在模型为v2及更高版本时生效。

**说明**

`punctuation_prediction_enabled`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("punctuation_prediction_enabled", false)
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("punctuation_prediction_enabled", false))
 .build();
```

heartbeat

boolean

false

否

当需要与服务端保持长连接时，可通过该开关进行控制：

-   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
    
-   false（默认）：即使持续发送静音音频，连接也将在60秒后因超时而断开。
    
    静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。
    

该参数仅在模型为v2及更高版本时生效。

**说明**

使用该字段时，SDK版本不能低于2.19.1。

`heartbeat`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("heartbeat", true)
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("heartbeat", true))
 .build();
```

inverse\_text\_normalization\_enabled

boolean

true

否

设置是否开启ITN（Inverse Text Normalization，逆文本正则化）。

默认开启（true）。开启后，中文数字将转换为阿拉伯数字。

该参数仅在模型为v2及更高版本时生效。

**说明**

`inverse_text_normalization_enabled`需要通过`RecognitionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameter("inverse_text_normalization_enabled", false)
 .build();
```

## 通过parameters设置

```
RecognitionParam param = RecognitionParam.builder()
 .model("paraformer-realtime-v2")
 .format("pcm")
 .sampleRate(16000)
 .parameters(Collections.singletonMap("inverse_text_normalization_enabled", false))
 .build();
```

apiKey

String

\-

否

用户API Key。

## **关键接口**

### `Recognition`类

`Recognition`通过“`import com.alibaba.dashscope.audio.asr.recognition.Recognition;`”方式引入。它的关键接口如下：

**接口/方法**

**参数**

**返回值**

**描述**

```
public void call(RecognitionParam param, final ResultCallback<RecognitionResult> callback)
```

-   `param`：[请求参数](#d72d661a1brzp)
    
-   `callback`：[回调接口（ResultCallback）](#3639e1cb40mxi)
    

无

基于回调形式的流式实时识别，该方法不会阻塞当前线程。

```
public String call(RecognitionParam param, File file)
```

-   `param`：[请求参数](#d72d661a1brzp)
    
-   `file`：待识别音频文件
    

识别结果

基于本地文件的非流式调用，该方法会阻塞当前线程直到全部音频读完，该方法要求所识别文件具有可读权限。

```
public Flowable<RecognitionResult> streamCall(RecognitionParam param, Flowable<ByteBuffer> audioFrame)
```

-   `param`：[请求参数](#d72d661a1brzp)
    
-   `audioFrame`：`Flowable<ByteBuffer>`实例
    

`Flowable<RecognitionResult>`

基于Flowable的流式实时识别。

```
public void sendAudioFrame(ByteBuffer audioFrame)
```

-   `audioFrame`：二进制音频流，为`ByteBuffer`类型
    

无

推送音频，每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。

识别结果通过[回调接口（ResultCallback）](#3639e1cb40mxi)的onEvent方法获取。

```
public void stop()
```

无

无

停止实时识别。

该方法会阻塞当前线程，直到回调实例`ResultCallback`的`onComplete`或者`onError`被调用之后才会解除对当前线程的阻塞。

```
recognizer.getDuplexApi().close(int code, String reason)
```

code: WebSocket关闭码（Close Code）

reason：关闭原因

这两个参数可参考[The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455#section-7.1.5)文档进行配置

true

在任务结束后，无论是否出现异常都需要关闭WebSocket连接，避免造成连接泄漏。关于如何复用连接提升效率请参考[实时语音识别高并发场景](https://help.aliyun.com/zh/model-studio/paraformer-in-high-concurrency-scenarios)。

```
public String getLastRequestId()
```

无

requestId

获取当前任务的requestId，在调用`call`、`streamingCall`开始新任务之后可以使用。

**说明**

该方法自2.18.0版本及以后的SDK中才开始提供。

```
public long getFirstPackageDelay()
```

无

首包延迟

获取首包延迟，从发送第一包音频到收到首包识别结果延迟，在任务完成后使用。

**说明**

该方法自2.18.0版本及以后的SDK中才开始提供。

```
public long getLastPackageDelay()
```

无

尾包延迟

获得尾包延迟，发送`stop`指令到最后一包识别结果下发耗时，在任务完成后使用。

**说明**

该方法自2.18.0版本及以后的SDK中才开始提供。

### **回调接口（**`ResultCallback`）

[双向流式调用](#9d1e5f6852jr8)时，服务端会通过回调的方式，将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

回调方法的实现，通过继承抽象类`ResultCallback`完成，继承该抽象类时，您可以指定泛型为`RecognitionResult`。`RecognitionResult`封装了服务器返回的数据结构。

由于Java支持连接复用，因此没有`onClose`和`onOpen`。

**示例**

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

`result`：[实时识别结果（RecognitionResult）](#11a082e1d9ijq)

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

## **响应结果**

### **实时识别结果（**`**RecognitionResult**`**）**

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

[单句信息（Sentence）](#e3e502b072h3a)

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

[字时间戳信息（Word）](#125fb5faa3y7t)的List集合

返回字时间戳信息。

```
public String getEmoTag()
```

无

当前句子的情感

返回当前句子的情感：

-   positive：正面情感，如开心、满意
    
-   negative：负面情感，如愤怒、沉闷
    
-   neutral：无明显情感
    

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](#d72d661a1brzp)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[实时识别结果（RecognitionResult）](#11a082e1d9ijq)的`isSentenceEnd`方法返回结果为`true`时才显示情感识别结果。
    

```
public Double getEmoConfidence()
```

无

当前句子识别情感的置信度

返回当前句子识别情感的置信度，取值范围：\[0.0,1.0\]，值越大表示置信度越高。

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](#d72d661a1brzp)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[实时识别结果（RecognitionResult）](#11a082e1d9ijq)的`isSentenceEnd`方法返回结果为`true`时才显示情感识别结果。
    

### **字时间戳信息（**`**Word**`**）**

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

## **错误码**

如遇报错问题，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

## **更多示例**

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## **常见问题**

### **功能特性**

#### **Q：在长时间静默的情况下，如何保持与服务端长连接？**

将请求参数`heartbeat`设置为true，并持续向服务端发送静音音频。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

#### **Q：如何将音频格式转换为满足要求的格式？**

可使用[FFmpeg工具](https://ffmpeg.en.lo4d.com/download)，更多用法请参见FFmpeg官网。

```
# 基础转换命令（万能模板）
# -i，作用：输入文件路径，常用值示例：audio.wav
# -c:a，作用：音频编码器，常用值示例：aac, libmp3lame, pcm_s16le
# -b:a，作用：比特率（音质控制），常用值示例：192k, 320k
# -ar，作用：采样率，常用值示例：44100 (CD), 48000, 16000
# -ac，作用：声道数，常用值示例：1(单声道), 2(立体声)
# -y，作用：覆盖已存在文件(无需值)
ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

# 例如：WAV → MP3（保持原始质量）
ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
# 例如：MP3 → WAV（16bit PCM标准格式）
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
# 例如：M4A → AAC（提取/转换苹果音频）
ffmpeg -i input.m4a -c:a copy output.aac  # 直接提取不重编码
ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac  # 重编码提高质量
# 例如：FLAC无损 → Opus（高压缩）
ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
```

#### **Q：**是否支持查看每句话对应的时间范围？

支持。语音识别结果中会包含每句话的开始时间戳和结束时间戳，可通过它们确定每句话的时间范围。

#### **Q：如何识别本地文件（录音文件）？**

识别本地文件有两种方式：

-   直接传入本地文件路径：此种方式在最终识别结束后获取完整识别结果，不适合即时反馈的场景。
    
    参见[非流式调用](#8341058094tc3)，在[Recognition类](#adcb5e9bddbyq)的`call`方法中传入文件路径对录音文件直接进行识别。
    
-   将本地文件转成二进制流进行识别：此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。
    
    -   参见[双向流式调用：基于回调](#9d1e5f6852jr8)，通过[Recognition类](#adcb5e9bddbyq)的`sendAudioFrame`方法向服务端发送二进制流对其进行识别。
        
    -   参见[双向流式调用：基于Flowable](#6734e006bc0gp)，通过[Recognition类](#adcb5e9bddbyq)的`streamCall`方法向服务端发送二进制流对其进行识别。
        

### **故障排查**

#### **Q：无法识别语音（无识别结果）是什么原因？**

1.  请检查请求参数中的音频格式（`format`）和采样率（`sampleRate`/`sample_rate`）设置是否正确且符合参数约束。以下为常见错误示例：
    
    -   音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 mp3（参数设置错误）。
        
    -   音频采样率为 3600Hz，但请求参数 `sampleRate`/`sample_rate` 设置为 48000（参数设置错误）。
        
    
    可以使用[ffprobe](https://ffmpeg.org/ffprobe.html)工具获取音频的容器、编码、采样率、声道等信息：
    
    ```
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
    ```
    
2.  使用`paraformer-realtime-v2`模型时，请检查`language_hints`设置的语言是否与音频实际语言一致。
    
    例如：音频实际为中文，但`language_hints`设置为`en`（英文）。
    
3.  若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。

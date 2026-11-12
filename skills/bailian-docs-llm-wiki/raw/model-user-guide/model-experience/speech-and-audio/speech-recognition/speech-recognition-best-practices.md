# 语音识别最佳实践

介绍语音识别应用中的音频准备、连接复用、Java 并发处理、异步作业管理和异常处理方法。

## 准备输入音频

根据目标模型的[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)，检查输入的格式、采样率、声道和时长。

-   优先保证采集质量，减少背景噪声和回声。需要降噪或 AEC 时，使用同一组代表性标注音频比较处理前后的识别结果，再决定是否启用相应处理。
-   8 kHz 电话音频选择匹配的模型和采样率。
-   根据音频的语种和方言选择支持的模型。
-   专业名词识别不准时，可配置热词或上下文增强，使用方法参见[提升识别准确率](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md)。

音频检查与处理

#### 检查音频格式

使用 FFprobe 查看文件的容器格式、编码、采样率和声道数：

```
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.mp3
```

#### 转换编码与采样率

需要统一输入格式时，可使用 FFmpeg 转换。例如，将 MP3 转为 16 kHz、16-bit、单声道 WAV：

```
ffmpeg -i input.mp3 -ac 1 -ar 16000 -sample_fmt s16 output.wav
```

Java 对象池示例使用无 WAV 文件头的 PCM 数据，可按以下命令生成 `asr-example.pcm`：

```
ffmpeg -i input.mp3 -ac 1 -ar 16000 -c:a pcm_s16le -f s16le asr-example.pcm
```

#### 裁剪音频

例如，从 WAV 文件的第 1 分 30 秒起截取 2 分钟。`-c copy` 直接复制音频流，保留原编码和采样率：

```
ffmpeg -i long_audio.wav -ss 00:01:30 -t 00:02:00 -c copy output_clip.wav
```

#### 提取视频音轨

需要单独处理视频中的音频时，可提取音轨并转为 16 kHz、16-bit、单声道 WAV；输出格式按目标模型要求调整：

```
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le output.wav
```

### 选择文件输入方式

文件输入方式由所用接口决定。例如，Qwen-Audio-ASR-Flash 支持音频文件 URL 和 Base64 Data URI。本地音频可编码为 Base64 Data URI 后直接提交，编码方法和调用示例参见[Flash HTTP API](https://help.aliyun.com/zh/model-studio/fun-asr-flash-recorded-speech-recognition-http-api#h-fl-rq)。

通过 URL 提交文件时，确保识别服务能在任务处理期间下载音频，并检查访问权限、URL 有效期和公网可达性。

生产环境可将文件托管到 OSS 等稳定存储，再通过 URL 提交。批量处理时复用已上传的文件，减少重复上传。使用 SDK 的本地文件上传能力前，核对对应接口的上传限制；临时文件机制及适用条件请参见[获取临时文件 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

## 管理实时任务与连接

Qwen-Audio-ASR-Message、Qwen-Audio-ASR-Streaming、Fun-ASR-Realtime 和 Paraformer 的 `run-task` / `finish-task` 协议支持串行复用连接：

1.  发送 `run-task`，为本次任务生成唯一 `task_id`，等待 `task-started` 后发送音频。
2.  发送音频结束后，以相同 `task_id` 发送 `finish-task`。
3.  等待服务端返回 `task-finished`，确认当前任务已完成。
4.  在同一连接上使用新的 `task_id` 发起下一项任务；同一连接不并行运行多个任务。

Qwen3-ASR-Realtime 使用会话协议，会话结束后需主动断开连接；其接入和结束流程参见[Qwen3-ASR-Realtime 交互流程](raw/_short/qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md)。

### 处理空闲与失败连接

-   任务结束后约 60 秒没有新任务，连接会自动断开。长时间空闲后应重新建立连接。
-   任务失败、网络中断或协议异常后，主动关闭旧连接并重新创建识别对象；池化对象应废弃，不归还为可用对象。
-   应用退出或停止提供识别服务时，关闭对象池及其持有的连接。

### 处理任务中的长时间静音

任务运行期间需要持续发送静音音频时，按对应 API 配置 `heartbeat=true`，并持续发送符合编码要求的静音数据。任务结束后的空闲连接按上一节的规则管理。各模型的参数说明见以下文档。

[Message 客户端事件](raw/_short/qwen-asr-message-client-events-1721a061cc8750e6.md) ｜ [Streaming 客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md) ｜ [Fun-ASR 客户端事件](raw/_short/fun-asr-client-events-a037d05e99747fff.md) ｜ [Paraformer 客户端事件](raw/_short/paraformer-client-events-2ebe52755a401965.md)

## 配置 Java 并发处理

并发识别时，每个正在运行的任务独占一个 `Recognition` 对象，任务成功结束后再归还。以下示例基于 Commons Pool 2 自行管理识别对象，不需要为每次调用重新创建对象池。

### 添加依赖

先完成[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)和[安装 SDK](raw/model-api-reference/preparations/install-sdk.md)。本节完整示例要求 DashScope Java SDK 2.18.0 及以上。以下依赖配置使用 DashScope Java SDK 2.23.2、Commons Pool 2.12.0：

#### Maven

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>2.23.2</version>
</dependency>
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
    <version>2.12.0</version>
</dependency>
```

#### Gradle

```
dependencies {
    implementation 'com.alibaba:dashscope-sdk-java:2.23.2'
    implementation 'org.apache.commons:commons-pool2:2.12.0'
}
```

### 区分连接、对象和请求容量

以下三个 `DASHSCOPE_` 环境变量由 SDK 读取，需在进程启动前设置；`RECOGNITION_OBJECTPOOL_SIZE` 由本文示例代码读取。

**环境变量**

**默认值**

**作用**

`DASHSCOPE_CONNECTION_POOL_SIZE`

32

SDK 共享 OkHttp 客户端保留的空闲 HTTP 连接数。

`DASHSCOPE_MAXIMUM_ASYNC_REQUESTS`

32

SDK 异步请求的并发调度容量，超过容量的请求等待调度。

`DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST`

32

同一主机的异步请求调度容量。

`RECOGNITION_OBJECTPOOL_SIZE`

500

本文示例允许同时持有的识别对象总数，由 Commons Pool 的 `maxTotal` 控制。

**说明**并发数是同一时刻运行的任务数，RPS 是每秒请求数。按业务并发量配置工作线程数和对象池容量，并根据模型接口的[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)控制任务发起频率。

Paraformer 配置参考

以下为 Paraformer 实时识别应用的容量规划参考。单机并发表示同一时刻运行的识别任务数；服务器仅承载该识别应用。

-   HTTP 空闲连接容量可从峰值并发数的 2 倍以上开始调整。
-   异步请求调度容量、单主机调度容量可先取与该连接容量一致的值，再按实际排队情况调整。
-   识别对象池容量可从峰值并发数的 1.5～2 倍开始调整。本文示例的默认容量为 500，属于应用配置。

**阿里云服务器规格**

**任务并发参考**

**识别对象池容量**

**HTTP 空闲连接容量**

4 核 8 GiB

100

500

2000

8 核 16 GiB

200

500

2000

16 核 32 GiB

400

500

2000

**说明**以上配置适用于仅承载 Paraformer 实时识别应用的服务器。实际容量按音频发送速率、客户端资源和业务处理负载调整；模型接口的限流见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 实现识别对象池

对象池的完整生命周期如下。达到 `maxTotal` 且没有空闲对象时，本例的 `borrowObject` 等待对象归还；对象按需创建，并在发起识别请求时建立 WebSocket 连接。

1.  借用一个 `Recognition` 对象，启动识别并发送音频。
2.  发送结束指令并等待完成确认；异步调用同时检查错误回调。
3.  成功完成后调用 `returnObject`，让后续任务复用该对象。
4.  失败或中断时调用 `invalidateObject`；工厂的 `destroyObject` 主动关闭连接。
5.  所有任务结束后关闭对象池，释放空闲对象持有的连接。

将以下代码保存为 `RecognitionPoolExample.java`。准备 16 kHz、16-bit、单声道 PCM 文件 `asr-example.pcm`，配置 `DASHSCOPE_API_KEY`，并将代码中的业务空间和地址替换为对应地域的配置（参见[接入地址](raw/model-user-guide/get-started-with-models/regions.md)）。示例启动 3 个工作线程，处理 9 个识别任务。

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicReference;

public class RecognitionPoolExample {
    private static final int WORKERS = 3;
    private static final int TASKS = 9;
    private static final int COMPLETION_TIMEOUT_SECONDS = 60;

    public static void main(String[] args) {
        int exitCode = 0;
        try {
            run(args);
        } catch (Exception e) {
            e.printStackTrace();
            exitCode = 1;
        }
        // Exit this standalone example after all owned resources are closed.
        System.exit(exitCode);
    }

    private static void run(String[] args) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalArgumentException("Set DASHSCOPE_API_KEY first");
        }
        // Replace {WorkspaceId} with the workspace ID for the endpoint region.
        Constants.baseWebsocketApiUrl =
                "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        Path audio = Paths.get(args.length == 0 ? "asr-example.pcm" : args[0]);
        if (!Files.isReadable(audio)) {
            throw new IllegalArgumentException("Audio file is not readable: " + audio);
        }
        int capacity = Integer.parseInt(System.getenv().getOrDefault(
                "RECOGNITION_OBJECTPOOL_SIZE", "500"));
        if (capacity <= 0) {
            throw new IllegalArgumentException("Pool size must be positive");
        }
        GenericObjectPoolConfig<Recognition> config = new GenericObjectPoolConfig<>();
        config.setMaxTotal(capacity);
        config.setMaxIdle(capacity);
        config.setBlockWhenExhausted(true);
        config.setMinIdle(0);

        GenericObjectPool<Recognition> pool =
                new GenericObjectPool<>(new RecognitionFactory(), config);
        ExecutorService executor = Executors.newFixedThreadPool(WORKERS);
        ExecutorService completionExecutor = Executors.newFixedThreadPool(WORKERS);
        try {
            List<Callable<Void>> tasks = new ArrayList<>();
            for (int i = 0; i < TASKS; i++) {
                tasks.add(() -> {
                    recognize(pool, audio, apiKey, completionExecutor);
                    return null;
                });
            }
            // Wait for every task, then propagate any task failure.
            List<Future<Void>> results = executor.invokeAll(tasks);
            for (Future<Void> result : results) {
                result.get();
            }
        } finally {
            executor.shutdown();
            completionExecutor.shutdownNow();
            try {
                if (!executor.awaitTermination(1, TimeUnit.MINUTES)) {
                    executor.shutdownNow();
                }
                if (!completionExecutor.awaitTermination(1, TimeUnit.MINUTES)) {
                    completionExecutor.shutdownNow();
                }
            } finally {
                pool.close();
                System.out.printf("Pool closed: created=%d, destroyed=%d, active=%d, idle=%d%n",
                        pool.getCreatedCount(), pool.getDestroyedCount(),
                        pool.getNumActive(), pool.getNumIdle());
            }
        }
    }

    private static void recognize(GenericObjectPool<Recognition> pool,
                                  Path audio, String apiKey,
                                  ExecutorService completionExecutor) throws Exception {
        // Example timeout; adjust it to the application's queueing policy.
        Recognition recognizer = pool.borrowObject(Duration.ofSeconds(30));
        boolean reusable = false;
        AtomicReference<Exception> failure = new AtomicReference<>();
        CountDownLatch completed = new CountDownLatch(1);
        try (InputStream input = Files.newInputStream(audio)) {
            RecognitionParam param = RecognitionParam.builder()
                    .model("qwen-audio-3.1-asr-flash-streaming")
                    .apiKey(apiKey).format("pcm").sampleRate(16000).build();
            ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
                @Override
                public void onEvent(RecognitionResult result) {
                    if (result.isSentenceEnd() && result.getSentence() != null) {
                        System.out.println(result.getSentence().getText());
                    }
                }

                @Override
                public void onComplete() {
                    completed.countDown();
                }

                @Override
                public void onError(Exception error) {
                    failure.set(error);
                    completed.countDown();
                }
            };
            recognizer.call(param, callback);
            // 100 ms of PCM16 mono audio at 16 kHz is 3,200 bytes.
            byte[] buffer = new byte[3200];
            int count;
            while ((count = input.read(buffer)) != -1) {
                if (failure.get() != null) {
                    throw failure.get();
                }
                recognizer.sendAudioFrame(ByteBuffer.wrap(buffer, 0, count));
                Thread.sleep(100);
                buffer = new byte[3200];
            }
            // stop() blocks in the SDK, so apply the deadline to the stop call itself.
            long deadline = System.nanoTime()
                    + TimeUnit.SECONDS.toNanos(COMPLETION_TIMEOUT_SECONDS);
            Future<?> stopTask = completionExecutor.submit(recognizer::stop);
            try {
                stopTask.get(Math.max(0, deadline - System.nanoTime()), TimeUnit.NANOSECONDS);
                long remaining = Math.max(0, deadline - System.nanoTime());
                if (!completed.await(remaining, TimeUnit.NANOSECONDS)) {
                    throw new TimeoutException("Timed out waiting for task completion");
                }
            } finally {
                stopTask.cancel(true);
            }
            if (failure.get() != null) {
                throw failure.get();
            }
            reusable = true;
            System.out.printf("Completed: request_id=%s, first_packet_ms=%d, last_packet_ms=%d%n",
                    recognizer.getLastRequestId(), recognizer.getFirstPackageDelay(),
                    recognizer.getLastPackageDelay());
        } finally {
            if (reusable) {
                pool.returnObject(recognizer);
            } else {
                // destroyObject closes the connection before discarding the object.
                pool.invalidateObject(recognizer);
            }
        }
    }

    private static class RecognitionFactory extends BasePooledObjectFactory<Recognition> {
        @Override
        public Recognition create() {
            return new Recognition();
        }

        @Override
        public PooledObject<Recognition> wrap(Recognition recognizer) {
            return new DefaultPooledObject<>(recognizer);
        }

        @Override
        public void destroyObject(PooledObject<Recognition> object) {
            if (object.getObject().getDuplexApi() != null) {
                object.getObject().getDuplexApi().close(1000, "pool cleanup");
            }
        }
    }
}
```

代码中的对象借用等待上限为 30 秒，结束任务的等待上限为 60 秒，均为可调整的示例配置。实时采集场景需按允许的启动延迟设置等待上限，并限制排队任务数。更换音频来源时，保留结束确认、异常废弃和资源关闭流程。

### 预热与耗时统计

通过发起实际识别请求预热，建立后续任务可复用的 WebSocket 连接。

1.  按正式业务的并发级别提前发起调用，持续 1～2 分钟可作为起始参考，再按负载调整。
2.  确认已有可复用连接后，再采集正式延迟数据；冷启动和稳定运行的数据分别统计。
3.  业务空闲导致连接断开后，再次调用可能重新建连；重新进行性能统计前，按需预热。

可同时记录 SDK 返回的首包、尾包耗时，以及业务端的端到端耗时，并明确各自的起止点。排队、建连、音频发送和服务处理会影响不同指标，应分开观察。

## 管理异步转写作业

高并发批量转写优先通过回调接收任务完成通知，减少轮询请求。回调配置和事件格式参见[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。

收到完成通知后，使用 `data.task_id` 关联业务任务，并检查 `data.task_status`。任务成功且通知中未包含所需结果时，按[对应模型的 HTTP API](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#55d72db0d5jgx)查询任务结果，再[下载并保存转写文件](#results)。

### 控制提交、查询与上传频率

-   **任务提交**：根据目标模型的[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)控制提交频率。
-   **状态查询**：查询接口默认限流为 **20 QPS**，最高可扩容至 100 QPS（扩容请联系阿里云商务经理），按阿里云主账号（含其子账号）计算。使用主动轮询时，可从 2～5 秒的查询间隔开始，并按任务数量调整，确保总查询频率在限额内。查询、批量查询及取消任务的方法参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
-   **临时文件上传**：文件上传凭证接口限流为 **100 QPS**，按阿里云主账号 + 模型维度计算，不支持扩容。生产环境和高并发场景使用 OSS 等稳定存储；临时文件上传的使用方式及限制参见[获取临时文件 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

### 及时保存识别结果

收到任务成功状态后，应尽快下载并保存结果文件。以[Qwen-Audio-ASR-Filetrans HTTP API](raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)为例，`transcription_url` 有效期为 24 小时，需在到期前下载并持久保存结果文件。

-   返回 `results` 数组时，逐项检查 `subtask_status`，再下载成功文件的转写 JSON，保存业务需要的时间戳、说话人等字段。
-   保存任务与文件的对应关系及最终状态；结果下载失败时保留任务记录，并在有效期内重试下载。

## 处理异常与重试

先根据错误类型决定是否重试。记录请求 ID、任务 ID、模型、地域和失败阶段，便于区分输入问题、权限问题与临时服务异常。

**问题类型**

**处理方式**

输入文件或参数错误

检查 URL、编码、采样率、声道及参数范围，修正后再提交。

鉴权或接入配置错误

核对 API Key、业务空间及接入地址所属地域，按具体错误信息修正配置。

限流

降低请求频率或任务启动速率，按[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)处理，不立即循环重试。

网络超时、中断或临时服务端错误（5xx）

查询或下载失败时，采用有次数和总等待时限的退避重试。异步提交超时后，已取得 `task_id` 的任务先查询状态；未取得 `task_id` 时，按业务对重复处理和重复计费的容忍程度决定是否重新提交。

异步任务或文件处理失败

保留任务及文件级错误信息，先判断原因，再决定修正输入或重新提交。

重试采用指数退避并加入随机抖动，同时限制重试次数和总等待时间，例如最多重试 3 次，具体上限按业务时延预算调整。实时连接中断后关闭旧连接，以新任务 ID 重建任务；根据最后确认的最终结果记录音频位置，按业务需要重放应用缓存中的未确认片段，并按原始音频位置合并结果、去重。

## 相关文档

-   基础接入：[实时语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)、[非实时语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md)。
-   识别效果调优：[提升识别准确率](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md)。
-   异步作业：[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)、[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

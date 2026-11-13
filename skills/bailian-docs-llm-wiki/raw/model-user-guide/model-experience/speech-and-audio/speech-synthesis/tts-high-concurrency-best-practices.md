# 语音合成最佳实践

介绍语音合成的文本提交、音频处理、连接与并发资源管理，以及性能评估和问题诊断的最佳实践。

## 文本提交与任务控制

使用复刻音色或设计音色时，合成请求中的模型须与创建音色时指定的目标模型一致。音色创建要求请参见[音色复刻](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md)或[音色设计](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-design-user-guide.md)。

### 文本分段与发送时序

Qwen-Audio-TTS、CosyVoice 通过 WebSocket 接入时，收到 `task-started` 后再按顺序发送文本片段。服务端自动对文本分句：完整语句立即合成，不完整语句暂存，直到语句完整或收到 `finish-task` 时再合成。

分段输入时，过长的发送间隔会增加合成总时长；若上一段音频已经播完、下一段文本尚未到达，也会造成播放卡顿。单次文本长度、累计长度和发送间隔限制，请参见 [Qwen-Audio-TTS 客户端事件](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-client-events#h3continuetask)或 [CosyVoice 客户端事件](https://help.aliyun.com/zh/model-studio/cosyvoice-client-events#h3continuetask)。

**说明**使用 SSML 时，需要一次提交完整的 SSML 文本，不支持分段输入。支持的模型、音色和接口请参见 [SSML 与 LaTeX](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl01_constraint_h3)。

### 任务完成与取消

通过 WebSocket 原始协议调用 Qwen-Audio-TTS、CosyVoice 时，文本发送完毕后，发送 `finish-task` 通知服务端结束输入，并继续接收音频，直到收到 `task-finished`。不能省略结束通知，否则可能导致语音数据不完整。

需要中断当前轮次合成时，使用取消任务能力；服务端结束当前任务并返回 `task-finished`。各 SDK 与原始协议的使用方式及适用条件请参见[取消任务](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#rt_cancel_h3)。

## 音频接收与播放

### 音频接收与保存

Qwen-Audio-TTS、CosyVoice 的不同接入方式返回音频的形式不同：

-   **HTTP 非流式输出**：从 `output.audio.url` 获取完整音频文件。URL 有效期为 24 小时，需要及时下载保存；过期后可重新合成。
-   **HTTP SSE 流式输出**：`output.audio.data` 为 Base64 编码的音频片段，按接收顺序解码并追加到同一文件。返回字段请参见 [Qwen-Audio-TTS HTTP API](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-http-api#0e1c44902ea1e)和 [CosyVoice HTTP API](https://help.aliyun.com/zh/model-studio/cosyvoice-tts-http-api#0e1c44902ea1e)。
-   **WebSocket 原始协议**：通过 `binary` 通道接收音频，文本事件用于传递句子等信息。具体交互请参见 [Qwen-Audio-TTS WebSocket API](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-websocket-api#62149ca39bx2i)和 [CosyVoice WebSocket API](https://help.aliyun.com/zh/model-studio/cosyvoice-websocket-api#62149ca39bx2i)。

### 音频格式与播放器适配

保存完整音频文件时，请求中的音频格式应与文件后缀一致，并确认播放器支持对应的格式和采样率。流式播放异常时，可先将音频流保存为完整文件：若文件也无法播放，检查格式与播放器；若文件能正常播放，则检查播放实现是否支持流式音频，例如 ffmpeg、pyaudio、AudioFormat、MediaSource 等。

流式返回 WAV 时，文件头可能无法反映最终音频长度。如需准确的时长信息，可将 `format` 设为 `pcm`，接收完整音频后添加包含实际长度的 WAV 文件头。

### 回调与播放调度

实时合成的回调运行在 WebSocket 线程，阻塞性业务逻辑会影响音频数据接收。可将音频写入独立缓冲区，在其他线程中处理。播放卡顿时，还需检查文本发送速度和网络稳定性；网络波动可能导致音频传输中断或延迟。

## 连接与并发资源管理

### 连接复用与任务隔离

通过原始 WebSocket 协议调用 Qwen-Audio-TTS、CosyVoice 时，同一连接可顺序处理多轮合成。收到本轮 `task-finished` 后，必须使用新的 `task_id` 发送 `run-task`，再按该系列的流程发送文本；取消任务后也按此流程复用连接。

对于 Qwen-Audio-TTS、CosyVoice、Sambert，任务结束后空闲 60 秒会自动断开连接。长时间空闲后的调用应按重新建连的情况评估。

使用 Python SDK 的 `client.audio.tts.connect` 时，会话在任务结束或取消后默认关闭底层连接。需要复用连接时，可先通过 `client.ws_connection()` 创建共享连接，再以 `connection=` 传入会话；共享连接由调用方通过 `WsConnection.close` 关闭。

### 鉴权身份与隔离范围

API Key 仅在 WebSocket 建连握手时通过 `Authorization` 请求头进行鉴权，后续 `run-task` 消息不携带 API Key。连接复用期间，修改参数或全局配置中的 API Key 不会改变该连接的鉴权身份，可能导致身份、配额或计费归属与预期不一致。

#### Java SDK

Java 为不同 API Key 创建独立对象池，同一池始终使用相同的 API Key。Qwen-Audio-TTS/CosyVoice 每次借出对象后都应调用 `updateParamAndCallback`，但该方法不会为已有连接重新鉴权。

#### Python SDK

Python 应在创建池前设置 `dashscope.api_key`。池初始化时建立的连接沿用握手时的 API Key，`borrow_synthesizer` 不提供 API Key 参数。`SpeechSynthesizerObjectPool` 是进程内单例，多 API Key 应按进程隔离。

### 并发与资源规划

对象池通过保留合成对象及其 WebSocket 连接，减少反复创建对象、TCP/TLS 握手和协议升级的开销。支持的模型系列和 SDK 如下：

-   **Qwen-Audio-TTS、CosyVoice**：Python、Java 对象池。
-   **Sambert**：Java 对象池，Python SDK 未提供对应的对象池封装。

根据预期同时运行的任务数和服务器规格配置资源池。模型限流按主账号统计，RAM 用户、业务空间和 API Key 共享主账号的额度；各模型的调用频率和并发限制请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

对象池容量可从峰值并发数的 1.5～2 倍开始配置，并根据实际负载调整。 Python 池内对象全部借出后，仍可能创建额外对象；这些对象在使用时需要新建连接。

#### 服务器配置参考

以下为仅运行相应语音合成服务时的阿里云服务器参考配置。单机并发数指同一时刻运行的合成任务数，可根据实际负载调整配置。

表中的“连接池配置”同时作为 `DASHSCOPE_CONNECTION_POOL_SIZE`、`DASHSCOPE_MAXIMUM_ASYNC_REQUESTS` 和 `DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST` 的参考值，即三项均设为 2000；对象池容量使用对应示例的环境变量配置。

**系列**

**阿里云服务器规格**

**单机并发数**

**对象池容量**

**连接池配置**

CosyVoice

4 vCPU / 8 GiB

100

500

2000

CosyVoice

8 vCPU / 16 GiB

150

500

2000

CosyVoice

16 vCPU / 32 GiB

200

500

2000

Sambert

4 vCPU / 8 GiB

600

1200

2000

#### Java 资源池参数

SDK 环境变量应在 Java 进程启动前设置。下列前 3 项是 SDK 配置，后面的对象池容量变量由示例代码自定义：

**环境变量**

**默认值**

**说明**

`DASHSCOPE_CONNECTION_POOL_SIZE`

32

底层 OkHttp 空闲连接池的配置。

`DASHSCOPE_MAXIMUM_ASYNC_REQUESTS`

32

底层异步请求调度的最大请求数。

`DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST`

32

底层异步请求调度的单主机最大请求数。

`COSYVOICE_OBJECTPOOL_SIZE`

500

本文 Qwen-Audio-TTS/CosyVoice Java 示例的对象池容量，对应 `maxTotal` 和 `maxIdle`，不是 SDK 内置参数。

`SAMBERT_OBJECTPOOL_SIZE`

500

本文 Sambert Java 示例的对象池容量，对应 `maxTotal` 和 `maxIdle`，不是 SDK 内置参数。

本文 Java 示例将 `maxIdle` 和 `maxTotal` 设为相同值，减少闲置对象被销毁后再次创建的开销。销毁对象时应关闭其连接。达到 `maxTotal` 后，新的借用请求将等待可用对象。

### 对象生命周期

配置 API Key 和接入地址后，创建共享对象池，供业务任务借用。

#### Java SDK

1.  调用 `borrowObject` 借用对象。对于 Qwen-Audio-TTS/CosyVoice，每次借出后都需调用 `updateParamAndCallback(param, callback)` 设置本次任务的参数和回调。
2.  Qwen-Audio-TTS/CosyVoice 使用 `call` 或 `streamingCall` 执行合成。Sambert 使用 `call(param, callback)` 执行单向流式合成。
3.  任务正常完成后，调用 `returnObject` 归还对象；未完成或失败时，使用 `invalidateObject` 废弃对象，并由工厂关闭连接，不得直接归还。
4.  所有任务结束后，调用对象池的 `close()`，释放对象池资源。

Java 中，若 `maxIdle` 小于 `maxTotal`，对象归还时超出空闲容量的对象会被销毁。如果工厂的 `destroyObject` 没有关闭 WebSocket，连接可能在对象销毁后仍保持打开。

#### Python SDK

1.  调用 `borrow_synthesizer` 借用对象，传入模型、音色、格式和回调。
2.  调用 `call` 或 `streaming_call` 执行合成。
3.  任务正常完成后，调用 `return_synthesizer` 归还对象；未完成或失败时，调用对象的 `close()`，不得直接归还。
4.  所有任务结束后，调用 `shutdown()`，释放对象池资源。

客户端异常中断任务后，服务端可能仍认为上一轮任务正在执行。此时复用连接发送新的 `run-task` 会造成协议顺序错误（`Invalid action('run-task')! Please follow the protocol!`）。应关闭连接并废弃该对象，再新建连接执行后续任务。

频繁创建合成对象而未关闭旧连接，会使连接数持续增长，增加服务器资源开销。检查任务结束后是否正确归还对象，以及不再使用的连接是否关闭。

## 对象池调用示例

-   [获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)并配置 `DASHSCOPE_API_KEY`，使用与调用地域对应的 API Key。
-   将示例中的 `{WorkspaceId}` 替换为对应地域的业务空间 ID，并按地域设置 WebSocket 地址。

#### Java SDK

-   **Qwen-Audio-TTS、CosyVoice**：DashScope Java SDK 2.16.6 及以上版本。
-   **Sambert**：DashScope Java SDK 2.16.9 及以上版本。

Java 示例还需要 Apache Commons Pool 2，可通过 Maven 或 Gradle 配置依赖：

Maven

```
<dependencies>
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
</dependencies>
```

Gradle

```
dependencies {
    implementation 'com.alibaba:dashscope-sdk-java:2.23.2'
    implementation 'org.apache.commons:commons-pool2:2.12.0'
}
```

#### Python SDK

Qwen-Audio-TTS、CosyVoice 的对象池需要 DashScope Python SDK 2.0.1 及以上版本：

```
pip install "dashscope>=2.0.1"
```

#### Qwen-Audio-TTS/CosyVoice

以下示例使用 qwen-audio-3.1-tts-flash 和 `longanhuan_v3.1`，并发执行 3 次合成。使用 CosyVoice 时，可将模型和音色分别改为 cosyvoice-v3-flash 和 `longanyang`；其他模型选择与音色要求参见[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#4a43cc1bb7kxg)。

Java

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;
import java.time.Duration;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicReference;

public class PooledTts {
    static class Factory extends BasePooledObjectFactory<SpeechSynthesizer> {
        public SpeechSynthesizer create() { return new SpeechSynthesizer(); }
        public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer value) {
            return new DefaultPooledObject<>(value);
        }
        public void destroyObject(PooledObject<SpeechSynthesizer> value) {
            value.getObject().getDuplexApi().close(1000, "done");
        }
    }

    static void synthesize(GenericObjectPool<SpeechSynthesizer> pool, int index) throws Exception {
        SpeechSynthesizer synthesizer = pool.borrowObject();
        boolean successful = false;
        AtomicReference<Exception> error = new AtomicReference<>();
        try (FileOutputStream audio = new FileOutputStream("output_" + index + ".mp3")) {
            SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-audio-3.1-tts-flash")
                .voice("longanhuan_v3.1")
                .format(SpeechSynthesisAudioFormat.MP3_24000HZ_MONO_256KBPS)
                .build();
            synthesizer.updateParamAndCallback(param, new ResultCallback<SpeechSynthesisResult>() {
                public void onEvent(SpeechSynthesisResult result) {
                    ByteBuffer buffer = result.getAudioFrame();
                    if (buffer != null) {
                        byte[] bytes = new byte[buffer.remaining()];
                        buffer.get(bytes);
                        try { audio.write(bytes); }
                        catch (Exception e) { error.set(e); }
                    }
                }
                public void onComplete() {}
                public void onError(Exception e) { error.set(e); }
            });
            synthesizer.streamingCall("你好，欢迎使用阿里云百炼。");
            synthesizer.streamingComplete(60000);
            if (error.get() != null) { throw error.get(); }
            successful = true;
        } finally {
            if (successful) { pool.returnObject(synthesizer); }
            else { pool.invalidateObject(synthesizer); }
        }
    }

    public static void main(String[] args) throws Exception {
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        GenericObjectPoolConfig<SpeechSynthesizer> config = new GenericObjectPoolConfig<>();
        int poolSize = Integer.parseInt(System.getenv().getOrDefault("COSYVOICE_OBJECTPOOL_SIZE", "500"));
        config.setMaxTotal(poolSize);
        config.setMaxIdle(poolSize);
        config.setMaxWait(Duration.ofSeconds(60));
        ExecutorService executor = Executors.newFixedThreadPool(3);
        try (GenericObjectPool<SpeechSynthesizer> pool = new GenericObjectPool<>(new Factory(), config)) {
            java.util.List<Future<?>> futures = new java.util.ArrayList<>();
            for (int i = 0; i < 3; i++) {
                final int index = i;
                futures.add(executor.submit(() -> {
                    try { synthesize(pool, index); }
                    catch (Exception e) { throw new RuntimeException(e); }
                }));
            }
            for (Future<?> future : futures) { future.get(); }
        } finally {
            executor.shutdownNow();
        }
    }
}
```

Python

```
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizerObjectPool, ResultCallback, AudioFormat

dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
dashscope.base_websocket_api_url = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"
pool = SpeechSynthesizerObjectPool(max_size=3)

def synthesize(index):
    done = threading.Event()
    errors = []
    with open(f"output_{index}.mp3", "wb") as audio:
        class Callback(ResultCallback):
            def on_data(self, data: bytes):
                audio.write(data)

            def on_complete(self):
                done.set()

            def on_error(self, message):
                errors.append(message)
                done.set()

        synthesizer = pool.borrow_synthesizer(
            model="qwen-audio-3.1-tts-flash",
            voice="longanhuan_v3.1",
            format=AudioFormat.MP3_24000HZ_MONO_256KBPS,
            callback=Callback(),
        )
        successful = False
        try:
            synthesizer.streaming_call("你好，欢迎使用阿里云百炼。")
            synthesizer.streaming_complete(60000)
            if not done.wait(60):
                raise TimeoutError("Synthesis timed out")
            if errors:
                raise RuntimeError(errors[0])
            successful = True
        finally:
            if successful:
                pool.return_synthesizer(synthesizer)
            else:
                synthesizer.close()

try:
    with ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(synthesize, range(3)))
finally:
    pool.shutdown()
```

#### Sambert

以下示例共享一个对象池，并发执行 3 次单向流式合成，分别保存为 `sambert_0.mp3`、`sambert_1.mp3` 和 `sambert_2.mp3`。

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.io.FileOutputStream;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicReference;

public class PooledSambert {
    static class Factory extends BasePooledObjectFactory<SpeechSynthesizer> {
        @Override
        public SpeechSynthesizer create() { return new SpeechSynthesizer(); }

        @Override
        public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer value) {
            return new DefaultPooledObject<>(value);
        }

        @Override
        public void destroyObject(PooledObject<SpeechSynthesizer> value) {
            value.getObject().getSyncApi().close(1000, "done");
        }
    }

    static void synthesize(GenericObjectPool<SpeechSynthesizer> pool, int index, String text)
            throws Exception {
        SpeechSynthesizer synthesizer = pool.borrowObject();
        boolean successful = false;
        CountDownLatch finished = new CountDownLatch(1);
        AtomicReference<Exception> error = new AtomicReference<>();
        try (FileOutputStream audio = new FileOutputStream("sambert_" + index + ".mp3")) {
            SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("sambert-zhichu-v1")
                .text(text)
                .format(SpeechSynthesisAudioFormat.MP3)
                .enablePhonemeTimestamp(true)
                .enableWordTimestamp(true)
                .build();
            synthesizer.call(param, new ResultCallback<SpeechSynthesisResult>() {
                @Override
                public void onEvent(SpeechSynthesisResult result) {
                    if (result.getAudioFrame() != null) {
                        byte[] bytes = result.getAudioFrame().array();
                        try { audio.write(bytes); }
                        catch (Exception e) { error.compareAndSet(null, e); }
                    }
                }

                @Override
                public void onComplete() { finished.countDown(); }

                @Override
                public void onError(Exception e) {
                    error.compareAndSet(null, e);
                    finished.countDown();
                }
            });
            if (!finished.await(60, TimeUnit.SECONDS)) {
                throw new TimeoutException("Synthesis timed out");
            }
            if (error.get() != null) { throw error.get(); }
            successful = true;
        } finally {
            if (successful) { pool.returnObject(synthesizer); }
            else { pool.invalidateObject(synthesizer); }
        }
    }

    public static void main(String[] args) throws Exception {
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        int poolSize = Integer.parseInt(System.getenv().getOrDefault("SAMBERT_OBJECTPOOL_SIZE", "500"));
        GenericObjectPoolConfig<SpeechSynthesizer> config = new GenericObjectPoolConfig<>();
        config.setMaxTotal(poolSize);
        config.setMaxIdle(poolSize);
        config.setMaxWait(Duration.ofSeconds(60));
        ExecutorService executor = Executors.newFixedThreadPool(3);
        try (GenericObjectPool<SpeechSynthesizer> pool = new GenericObjectPool<>(new Factory(), config)) {
            String[] texts = {"床前明月光，疑似地上霜。", "举头望明月，低头思故乡。", "你好，欢迎使用阿里云百炼。"};
            List<Future<?>> futures = new ArrayList<>();
            for (int i = 0; i < texts.length; i++) {
                final int index = i;
                futures.add(executor.submit(() -> {
                    try { synthesize(pool, index, texts[index]); }
                    catch (Exception e) { throw new RuntimeException(e); }
                }));
            }
            Exception failure = null;
            for (Future<?> future : futures) {
                try { future.get(); }
                catch (ExecutionException e) { failure = e; }
            }
            if (failure != null) { throw failure; }
        } finally {
            executor.shutdownNow();
        }
    }
}
```

## 性能评估与问题诊断

连接预热与启动恢复

Python 对象池初始化时会建立连接；Java `GenericObjectPool` 按需创建对象，首次合成时才建立连接，因此 Java 连接预热需要实际执行合成请求。

服务启动或网络恢复后先执行预热调用，逐步提高并发。性能测试前，可按目标并发持续预热（例如 1～2 分钟），待连接稳定复用后再采集数据。 逐步提高并发可避免同时建立大量 WebSocket 连接造成阻塞。

延迟与实时率评估

首次调用包含 WebSocket 建连开销，应与复用连接后的首包延迟和任务总耗时分别统计。也可通过实时率（RTF，合成总耗时 / 音频时长）评估合成速度。

SDK 侧首包延迟包含建连和网络传输等耗时，不等同于纯模型推理耗时。Qwen-Audio-TTS/CosyVoice 的 Python 对象可通过 `get_first_package_delay()` 获取首包延迟，并通过 `get_last_request_id()` 获取请求 ID，用于关联请求日志。Java 对象通过 `getLastRequestId()` 获取请求 ID。

对象池借用等待与超时

Java 对象池达到 `maxTotal` 后，借用操作会等待可用对象。检查池容量、对象归还及连接关闭情况，避免任务因等待对象而增加耗时。

请求尖峰与限流

服务启动、网络中断或大量服务端错误后，集中重连可能使任务积压；连接恢复后，积压任务同时提交又会形成调用尖峰，并可能触发账号限流。

检查尖峰前是否出现网络异常或大量服务端错误，例如 `Requests rate limit exceeded, please try again later.`。 控制启动和恢复阶段的并发量。Java 可通过对象池的 `maxTotal` 限制同一池同时借出的对象数。

核对账号限流额度；需要提额时，按[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)中的流程申请。 根据实际负载调整服务器配置或增加机器数。

网络带宽与服务器负载

检查网络带宽是否达到上限，以及实际并发数是否过高，再根据业务负载调整并发量或服务器配置。

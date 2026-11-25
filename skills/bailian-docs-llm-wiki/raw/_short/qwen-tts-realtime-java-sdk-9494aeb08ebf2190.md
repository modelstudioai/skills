# Qwen-TTS-Realtime Java SDK

本文介绍 DashScope Java SDK 调用 Qwen-TTS-Realtime 系列模型时的关键接口与请求参数。

<a id="前提条件"></a>

<a id="8779ce97deiou"></a>

<a id="前期准备"></a>

## 前提条件

DashScope Java SDK 版本需要不低于2.22.7。

<a id="快速开始"></a>

<a id="3dc1a29b077gt"></a>

## 快速开始

<a id="fig-code-group"></a>

<a id="fig-code-group-server-commit模式-tab"></a>

server commit模式

<a id="code-code-group-server-commit模式"></a>

```java
import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.AudioSystem;
import java.io.*;
import java.util.Base64;
import java.util.Queue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class Main {
    static String[] textToSynthesize = {
            "对吧~我就特别喜欢这种超市",
            "尤其是过年的时候",
            "去逛超市",
            "就会觉得",
            "超级超级开心！",
            "想买好多好多的东西呢！"
    };
    public static QwenTtsRealtimeAudioFormat ttsFormat = QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT;

    // 实时PCM音频播放器类
    public static class RealtimePcmPlayer {
        private int sampleRate;
        private SourceDataLine line;
        private AudioFormat audioFormat;
        private Thread decoderThread;
        private Thread playerThread;
        private AtomicBoolean stopped = new AtomicBoolean(false);
        private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
        private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();
        private ByteArrayOutputStream totalAudioStream = new ByteArrayOutputStream();

        // 构造函数初始化音频格式和音频线路
        public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
            this.sampleRate = sampleRate;
            this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
            line = (SourceDataLine) AudioSystem.getLine(info);
            line.open(audioFormat);
            line.start();
            decoderThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (!stopped.get()) {
                        String b64Audio = b64AudioBuffer.poll();
                        if (b64Audio != null) {
                            byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                            RawAudioBuffer.add(rawAudio);
                            // 将音频数据写入 totalAudioStream
                            try {
                                totalAudioStream.write(rawAudio);
                            } catch (IOException e) {
                                throw new RuntimeException(e);
                            }
                        } else {
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }
                }
            });
            playerThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (!stopped.get()) {
                        byte[] rawAudio = RawAudioBuffer.poll();
                        if (rawAudio != null) {
                            try {
                                playChunk(rawAudio);
                            } catch (IOException e) {
                                throw new RuntimeException(e);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        } else {
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }
                }
            });
            decoderThread.start();
            playerThread.start();
        }

        // 播放一个音频块并阻塞直到播放完成
        private void playChunk(byte[] chunk) throws IOException, InterruptedException {
            if (chunk == null || chunk.length == 0) return;

            int bytesWritten = 0;
            while (bytesWritten < chunk.length) {
                bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
            }
            int audioLength = chunk.length / (this.sampleRate*2/1000);
            // 等待缓冲区中的音频播放完成
            Thread.sleep(audioLength - 10);
        }

        public void write(String b64Audio) {
            b64AudioBuffer.add(b64Audio);
        }

        public void cancel() {
            b64AudioBuffer.clear();
            RawAudioBuffer.clear();
        }

        public void waitForComplete() throws InterruptedException {
            while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                Thread.sleep(100);
            }
            line.drain();
        }

        public void shutdown() throws InterruptedException, IOException {
            stopped.set(true);
            decoderThread.join();
            playerThread.join();

            // 保存完整音频文件
            File file = new File("TotalAudio_"+ttsFormat.getSampleRate()+"."+ttsFormat.getFormat());
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(totalAudioStream.toByteArray());
            }

            if (line != null && line.isRunning()) {
                line.drain();
                line.close();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException, LineUnavailableException, IOException {
        QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                .model("qwen3-tts-flash-realtime")
                // 以下为华北2（北京）地域的配置。
                .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apikey(System.getenv("DASHSCOPE_API_KEY"))
                .build();
        AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));
        final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);

        // 创建实时音频播放器实例
        RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

        QwenTtsRealtime qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
            @Override
            public void onOpen() {
                // 连接建立时的处理
            }
            @Override
            public void onEvent(JsonObject message) {
                String type = message.get("type").getAsString();
                switch(type) {
                    case "session.created":
                        // 会话创建时的处理
                        if (message.has("session")) {
                            String eventId = message.get("event_id").getAsString();
                            String sessionId = message.get("session").getAsJsonObject().get("id").getAsString();
                            System.out.println("[onEvent] session.created, session_id: "
                                    + sessionId + ", event_id: " + eventId);
                        }
                        break;
                    case "response.audio.delta":
                        String recvAudioB64 = message.get("delta").getAsString();
                        // 实时播放音频
                        audioPlayer.write(recvAudioB64);
                        break;
                    case "response.done":
                        // 响应完成时的处理
                        break;
                    case "session.finished":
                        // 会话结束时的处理
                        completeLatch.get().countDown();
                    default:
                        break;
                }
            }
            @Override
            public void onClose(int code, String reason) {
                // 连接关闭时的处理
            }
        });
        qwenTtsRef.set(qwenTtsRealtime);
        try {
            qwenTtsRealtime.connect();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }
        QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                .voice("Cherry")
                .responseFormat(ttsFormat)
                .mode("server_commit")
                .build();
        qwenTtsRealtime.updateSession(config);
        for (String text:textToSynthesize) {
            qwenTtsRealtime.appendText(text);
            Thread.sleep(100);
        }
        qwenTtsRealtime.finish();
        completeLatch.get().await();
        qwenTtsRealtime.close();

        // 等待音频播放完成并关闭播放器
        audioPlayer.waitForComplete();
        audioPlayer.shutdown();
        System.exit(0);
    }
}
```

<a id="fig-code-group-commit模式-tab"></a>

commit模式

<a id="code-code-group-commit模式"></a>

```java
import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.AudioSystem;
import java.io.*;
import java.util.Base64;
import java.util.Queue;
import java.util.Scanner;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class Main {
    public static QwenTtsRealtimeAudioFormat ttsFormat = QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT;
    // 实时PCM音频播放器类
    public static class RealtimePcmPlayer {
        private int sampleRate;
        private SourceDataLine line;
        private AudioFormat audioFormat;
        private Thread decoderThread;
        private Thread playerThread;
        private AtomicBoolean stopped = new AtomicBoolean(false);
        private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
        private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();
        private ByteArrayOutputStream totalAudioStream = new ByteArrayOutputStream();

        // 构造函数初始化音频格式和音频线路
        public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
            this.sampleRate = sampleRate;
            this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
            line = (SourceDataLine) AudioSystem.getLine(info);
            line.open(audioFormat);
            line.start();
            decoderThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (!stopped.get()) {
                        String b64Audio = b64AudioBuffer.poll();
                        if (b64Audio != null) {
                            byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                            RawAudioBuffer.add(rawAudio);
                            // 将音频数据写入 totalAudioStream
                            try {
                                totalAudioStream.write(rawAudio);
                            } catch (IOException e) {
                                throw new RuntimeException(e);
                            }
                        } else {
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }
                }
            });
            playerThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (!stopped.get()) {
                        byte[] rawAudio = RawAudioBuffer.poll();
                        if (rawAudio != null) {
                            try {
                                playChunk(rawAudio);
                            } catch (IOException e) {
                                throw new RuntimeException(e);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        } else {
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }
                }
            });
            decoderThread.start();
            playerThread.start();
        }

        // 播放一个音频块并阻塞直到播放完成
        private void playChunk(byte[] chunk) throws IOException, InterruptedException {
            if (chunk == null || chunk.length == 0) return;

            int bytesWritten = 0;
            while (bytesWritten < chunk.length) {
                bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
            }
            int audioLength = chunk.length / (this.sampleRate*2/1000);
            // 等待缓冲区中的音频播放完成
            Thread.sleep(audioLength - 10);
        }

        public void write(String b64Audio) {
            b64AudioBuffer.add(b64Audio);
        }

        public void cancel() {
            b64AudioBuffer.clear();
            RawAudioBuffer.clear();
        }

        public void waitForComplete() throws InterruptedException {
            // 等待所有缓冲区中的音频数据播放完成
            while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                Thread.sleep(100);
            }
            // 等待音频线路播放完成
            line.drain();
        }

        public void shutdown() throws InterruptedException {
            stopped.set(true);
            decoderThread.join();
            playerThread.join();
            // 保存完整音频文件
            File file = new File("TotalAudio_"+ttsFormat.getSampleRate()+"."+ttsFormat.getFormat());
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(totalAudioStream.toByteArray());
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            if (line != null && line.isRunning()) {
                line.drain();
                line.close();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException, LineUnavailableException, FileNotFoundException {
        Scanner scanner = new Scanner(System.in);

        QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                .model("qwen3-tts-flash-realtime")
                // 以下为华北2（北京）地域的配置。
                .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apikey(System.getenv("DASHSCOPE_API_KEY"))
                .build();

        AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));

        // 创建实时播放器实例
        RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

        final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);
        QwenTtsRealtime qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
            //            File file = new File("result_24k.pcm");
//            FileOutputStream fos = new FileOutputStream(file);
            @Override
            public void onOpen() {
                System.out.println("connection opened");
                System.out.println("输入文本并按Enter发送，输入'quit'退出程序");
            }
            @Override
            public void onEvent(JsonObject message) {
                String type = message.get("type").getAsString();
                switch(type) {
                    case "session.created":
                        System.out.println("start session: " + message.get("session").getAsJsonObject().get("id").getAsString());
                        break;
                    case "response.audio.delta":
                        String recvAudioB64 = message.get("delta").getAsString();
                        byte[] rawAudio = Base64.getDecoder().decode(recvAudioB64);
                        //                            fos.write(rawAudio);
                        // 实时播放音频
                        audioPlayer.write(recvAudioB64);
                        break;
                    case "response.done":
                        System.out.println("response done");
                        // 等待音频播放完成
                        try {
                            audioPlayer.waitForComplete();
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        }
                        // 为下一次输入做准备
                        completeLatch.get().countDown();
                        break;
                    case "session.finished":
                        System.out.println("session finished");
                        if (qwenTtsRef.get() != null) {
                            System.out.println("[Metric] response: " + qwenTtsRef.get().getResponseId() +
                                    ", first audio delay: " + qwenTtsRef.get().getFirstAudioDelay() + " ms");
                        }
                        completeLatch.get().countDown();
                    default:
                        break;
                }
            }
            @Override
            public void onClose(int code, String reason) {
                System.out.println("connection closed code: " + code + ", reason: " + reason);
                try {
//                    fos.close();
                    // 等待播放完成并关闭播放器
                    audioPlayer.waitForComplete();
                    audioPlayer.shutdown();
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        qwenTtsRef.set(qwenTtsRealtime);
        try {
            qwenTtsRealtime.connect();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }
        QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                .voice("Cherry")
                .responseFormat(ttsFormat)
                .mode("commit")
                .build();
        qwenTtsRealtime.updateSession(config);

        // 循环读取用户输入
        while (true) {
            System.out.print("请输入要合成的文本: ");
            String text = scanner.nextLine();

            // 如果用户输入quit，则退出程序
            if ("quit".equalsIgnoreCase(text.trim())) {
                System.out.println("正在关闭连接...");
                qwenTtsRealtime.finish();
                completeLatch.get().await();
                break;
            }

            // 如果用户输入为空，跳过
            if (text.trim().isEmpty()) {
                continue;
            }

            // 重新初始化倒计时锁存器
            completeLatch.set(new CountDownLatch(1));

            // 发送文本
            qwenTtsRealtime.appendText(text);
            qwenTtsRealtime.commit();

            // 等待本次合成完成
            completeLatch.get().await();
        }

        // 清理资源
        audioPlayer.waitForComplete();
        audioPlayer.shutdown();
        scanner.close();
        System.exit(0);
    }
}
```

访问[github](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)下载更多示例代码。

<a id="请求参数"></a>

<a id="cb904fc48ck5u"></a>

## 请求参数

下述请求参数可以通过`QwenTtsRealtimeParam`对象的链式方法或setter配置、之后作为参数传入QwenTtsRealtime的构造方法完成配置。

| 参数 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| model | String | 是 | 模型名称。参见[支持的模型](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#4a43cc1bb7kxg)。 |
| url | String | 是 | 华北2（北京）地域：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`<br><br>新加坡地域：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime` |

下述请求参数可以通过`QwenTtsRealtimeConfig`对象的链式方法或setter配置、之后作为参数传入updateSession接口完成配置。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>voice</p></td><td><p>String</p></td><td><p>是</p></td><td><p>语音合成所使用的音色。参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-tts-voice-list.md">Qwen-TTS音色列表</a>。</p></td></tr><tr><td><p>languageType</p></td><td><p>String</p></td><td><p>否</p></td><td><div><p>指定合成音频的语种，默认为 <code>Auto</code>。</p><ul><li><p><code>Auto</code>：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。</p></li><li><p>指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 <code>Auto</code>。可选值包括：</p><ul><li><p><code>Chinese</code></p></li><li><p><code>English</code></p></li><li><p><code>German</code></p></li><li><p><code>Italian</code></p></li><li><p><code>Portuguese</code></p></li><li><p><code>Spanish</code></p></li><li><p><code>Japanese</code></p></li><li><p><code>Korean</code></p></li><li><p><code>French</code></p></li><li><p><code>Russian</code></p></li></ul></li></ul></div></td></tr><tr><td><p>mode</p></td><td><p>String</p></td><td><p>否</p></td><td><div><p>交互模式，可选值：</p><ul><li><p><code>server_commit</code>（默认）：服务端自动判断合成时机，平衡延迟与质量，推荐大多数场景使用</p></li><li><p><code>commit</code>：客户端手动触发合成，延迟最低，但需自行管理句子完整性</p></li></ul></div></td></tr><tr><td><p>format</p></td><td><p>String</p></td><td><p>否</p></td><td><div><p>模型输出音频的格式。</p><p>支持的格式：</p><ul><li><p><code>pcm</code>（默认）</p></li><li><p><code>wav</code></p></li><li><p><code>mp3</code></p></li><li><p><code>opus</code></p></li></ul></div></td></tr><tr><td><p>sampleRate</p></td><td><p>int</p></td><td><p>否</p></td><td><div><p>模型输出音频的采样率（Hz）。</p><p>支持的采样率：</p><ul><li><p>8000</p></li><li><p>16000</p></li><li><p>24000（默认）</p></li><li><p>48000</p></li></ul></div></td></tr><tr><td><p>speechRate</p></td><td><p>float</p></td><td><p>否</p></td><td><div><p>音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p>volume</p></td><td><p>int</p></td><td><p>否</p></td><td><div><p>音频的音量。</p><p>取值范围：[0, 100]。</p></div></td></tr><tr><td><p>pitchRate</p></td><td><p>float</p></td><td><p>否</p></td><td><div><p>合成音频的语调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p>bitRate</p></td><td><p>int</p></td><td><p>否</p></td><td><div><p>指定音频的<a href="https://opus-codec.org/">码率</a>（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（<code>response_format</code>）为<code>opus</code>时可用。</p><p>默认值：128。</p><p>取值范围：[6, 510]。</p></div></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="e580668d035j6"></a>

<a id="关键接口"></a>

## 接口参考

<a id="qwenttsrealtime类"></a>

<a id="37a6cc33a7jk8"></a>

### QwenTtsRealtime类

引入方法：

<a id="code-block"></a>

```java
import com.alibaba.dashscope.audio.qwen_tts_realtime.QwenTtsRealtime;
```

<table><thead><tr><th><strong>成员方法</strong></th><th><strong>方法签名</strong></th><th><strong>服务端响应事件（通过回调下发）</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>connect</p></td><td><a id="code-block-2"></a><pre class="language-java"><code>public void connect() throws NoApiKeyException, InterruptedException
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#05bb97c283l2n">session.created</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#58f078ab61di5">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。</p></td></tr><tr><td><p>updateSession</p></td><td><a id="code-block-3"></a><pre class="language-java"><code>public void updateSession(QwenTtsRealtimeConfig config)
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#58f078ab61di5">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。</p><p>在您建立链接，服务端会及时返回用于此会话的默认输出输入配置。如果您需要更新默认会话配置，我们也推荐您总是在建立链接后即刻调用此接口。</p><p>服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。</p></td></tr><tr><td><p>appendText</p></td><td><a id="code-block-4"></a><pre class="language-java"><code>public void appendText(String text)
</code></pre></td><td><p>无</p></td><td><p>将文本片段追加到云端输入文本缓冲区。 缓冲区是你可以写入并稍后提交的临时存储。</p><ul><li>&quot;server_commit&quot;模式下，服务器决定何时提交并合成文本缓冲区中的文本。</li><li>&quot;commit&quot;模式下，客户端需要主动通过commit触发语音合成。</li></ul></td></tr><tr><td><p>clearAppendedText</p></td><td><a id="code-block-5"></a><pre class="language-java"><code>public void clearAppendedText()
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#7a04edb8840o7">input_text_buffer.cleared</a></p><blockquote><p>清空服务端收到的文本</p></blockquote></td><td><p>删除当前云端缓冲区的文本。</p></td></tr><tr><td><p>commit</p></td><td><a id="code-block-6"></a><pre class="language-java"><code>public void commit()
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#76abc25665qt8">input_text_buffer.committed</a></p><blockquote><p>提交文本并触发语音合成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#efd58c096b3bv">response.output_item.added</a></p><blockquote><p>响应时有新的输出内容</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#141bec9bb11yi">response.content_part.added</a></p><blockquote><p>新的输出内容添加到assistant message 项</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#a2b95643bdvnl">response.audio.delta</a></p><blockquote><p>模型增量生成的音频</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#faa3f9bc106tj">response.audio.done</a></p><blockquote><p>完成音频生成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#5244e1dbc9vw6">response.content_part.done</a></p><blockquote><p>Assistant message 的音频内容流式输出完成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#a922404106vzd">response.output_item.done</a></p><blockquote><p>Assistant message 的整个输出项流式传输完成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#91f767e7440pc">response.done</a></p><blockquote><p>响应完成</p></blockquote></td><td><p>提交之前通过append添加到云端缓冲区的文本，并立刻合成所有文本。如果输入的文本缓冲区为空将产生错误。</p><ul><li>&quot;server_commit&quot;模式下，客户端不需要发送此事件，服务器会自动提交文本缓冲区。</li><li>&quot;commit&quot;模式下，客户端必须通过commit触发语音合成。</li></ul></td></tr><tr><td><p>finish</p></td><td><a id="code-block-7"></a><pre class="language-java"><code>public void finish()
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#ac332f7d78oxg">session.finished</a></p><blockquote><p>响应完成</p></blockquote></td><td><p>终止任务。</p></td></tr><tr><td><p>close</p></td><td><a id="code-block-8"></a><pre class="language-java"><code>public void close()
</code></pre></td><td><p>无</p></td><td><p>关闭连接。</p></td></tr><tr><td><p>getSessionId</p></td><td><a id="code-block-9"></a><pre class="language-java"><code>public String getSessionId()
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id。</p></td></tr><tr><td><p>getResponseId</p></td><td><a id="code-block-10"></a><pre class="language-java"><code>public String getResponseId()
</code></pre></td><td><p>无</p></td><td><p>获取最近一次response的response_id。</p></td></tr><tr><td><p>getFirstAudioDelay</p></td><td><a id="code-block-11"></a><pre class="language-java"><code>public long getFirstAudioDelay()
</code></pre></td><td><p>无</p></td><td><p>获取首包音频延迟。</p></td></tr></tbody></table>

<a id="回调接口-qwenttsrealtimecallback"></a>

<a id="7d80f97d4fgc3"></a>

### 回调接口（QwenTtsRealtimeCallback）

<table><thead><tr><th><p>方法</p></th><th><p>参数</p></th><th><p>返回值</p></th><th><p>描述</p></th></tr></thead><tbody><tr><td><a id="code-block-12"></a><pre class="language-java"><code>public void onOpen()
</code></pre></td><td><p>无</p></td><td><p>无</p></td><td><p>当和服务端建立连接完成后，该方法立刻被回调。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-java"><code>public abstract void onEvent(JsonObject message)
</code></pre></td><td><p>message：服务端响应事件。</p></td><td><p>无</p></td><td><p>包括对接口调用的回复响应和模型生成的文本和音频。具体可以参考：<a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md">服务端事件</a></p></td></tr><tr><td><a id="code-block-14"></a><pre class="language-java"><code>public abstract void onClose(int code, String reason)
</code></pre></td><td><p>code：关闭WebSocket的状态码。</p><p>reason：关闭WebSocket的关闭信息。</p></td><td><p>无</p></td><td><p>当服务已经关闭连接后进行回调。</p></td></tr></tbody></table>

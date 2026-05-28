# Java SDK

本文介绍 DashScope Java SDK 调用[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)时的关键接口与请求参数。

**用户指南**：关于模型介绍和选型建议请参见[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)或[语音合成-千问](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

## **前期准备**

DashScope Java SDK 版本需要不低于2.22.7。

## **快速开始**

## **server commit模式**

```
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
                // 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime
                .model("qwen3-tts-flash-realtime")
                // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
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
                // 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash-realtime
                // .instructions("")
                // .optimizeInstructions(true)
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

## **commit模式**

```
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
                // 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime
                .model("qwen3-tts-flash-realtime")
                // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
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
                // 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash-realtime
                // .instructions("")
                // .optimizeInstructions(true)
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

## **请求参数**

下述请求参数可以通过`QwenTtsRealtimeParam`对象的链式方法或setter配置、之后作为参数传入QwenTtsRealtime的构造方法完成配置。

**参数**

**类型**

**是否必须**

**说明**

model

String

是

模型名称。参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#d2ad2470a394c)。

url

String

是

中国内地：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`

国际：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`

下述请求参数可以通过`QwenTtsRealtimeConfig`对象的链式方法或setter配置、之后作为参数传入updateSession接口完成配置。

**参数**

**类型**

**是否必须**

**说明**

voice

String

是

语音合成所使用的音色。参见[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)。

支持系统音色和专属音色：

-   **系统音色**：仅限千问3-TTS-Instruct-Flash-Realtime、千问3-TTS-Flash-Realtime和千问-TTS-Realtime系列模型。音色效果请参见：[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)。
    
-   **专属音色**
    
    -   [声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)功能定制的音色：仅限千问3-TTS-VC-Realtime系列模型
        
    -   [声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)功能定制的音色：仅限千问3-TTS-VD-Realtime系列模型
        

languageType

String

否

指定合成音频的语种，默认为 `Auto`。

-   `Auto`：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。
    
-   指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 `Auto`。可选值包括：
    
    -   `Chinese`
        
    -   `English`
        
    -   `German`
        
    -   `Italian`
        
    -   `Portuguese`
        
    -   `Spanish`
        
    -   `Japanese`
        
    -   `Korean`
        
    -   `French`
        
    -   `Russian`
        

mode

String

否

交互模式，可选值：

-   `server_commit`（默认）：服务端自动判断合成时机，平衡延迟与质量，推荐大多数场景使用
    
-   `commit`：客户端手动触发合成，延迟最低，但需自行管理句子完整性
    

format

String

否

模型输出音频的格式。

支持的格式：

-   `pcm`（默认）
    
-   `wav`
    
-   `mp3`
    
-   `opus`
    

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）仅支持`pcm`。

sampleRate

int

否

模型输出音频的采样率（Hz）。

支持的采样率：

-   8000
    
-   16000
    
-   24000（默认）
    
-   48000
    

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）仅支持24000。

speechRate

float

否

音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

volume

int

否

音频的音量。

默认值：50。

取值范围：\[0, 100\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

pitchRate

float

否

合成音频的语调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

bitRate

int

否

指定音频的[码率](https://opus-codec.org/)（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（`response_format`）为`opus`时可用。

默认值：128。

取值范围：\[6, 510\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

instructions

String

否

设置指令，参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

默认值：无默认值，不设置不生效。

长度限制：长度不得超过 1600 Token。

支持语言：仅支持中文和英文。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

optimizeInstructions

boolean

否

是否对 `instructions` 进行优化，以提升语音合成的自然度和表现力。

默认值：false。

行为说明：当设置为 true 时，系统将对 `instructions` 的内容进行语义增强与重写，生成更适合语音合成的内部指令。

适用场景：推荐在追求高品质、精细化语音表达的场景下开启。

依赖关系：此参数依赖于 `instructions` 参数被设置。如果 `instructions` 为空，此参数不生效。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

## **关键接口**

### QwenTtsRealtime**类**

引入方法：

```
import com.alibaba.dashscope.audio.qwen_tts_realtime.QwenTtsRealtime;
```

**成员方法**

**方法签名**

**服务端响应事件（通过回调下发）**

**说明**

connect

```
public void connect() throws NoApiKeyException, InterruptedException
```

[session.created](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#05bb97c283l2n)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#58f078ab61di5)

> 会话配置已更新

和服务端创建连接。

updateSession

```
public void updateSession(QwenTtsRealtimeConfig config)
```

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#58f078ab61di5)

> 会话配置已更新

更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。

在您建立链接，服务端会及时返回用于此会话的默认输出输入配置。如果您需要更新默认会话配置，我们也推荐您总是在建立链接后即刻调用此接口。

服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。

appendText

```
public void appendText(String text)
```

无

将文本片段追加到云端输入文本缓冲区。 缓冲区是你可以写入并稍后提交的临时存储。

-   "server\_commit"模式下，服务器决定何时提交并合成文本缓冲区中的文本。
    
-   "commit"模式下，客户端需要主动通过commit触发语音合成。
    

clearAppendedText

```
public void clearAppendedText()
```

[input\_text\_buffer.cleared](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#7a04edb8840o7)

> 清空服务端收到的文本

删除当前云端缓冲区的文本。

commit

```
public void commit()
```

[input\_text\_buffer.committed](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#76abc25665qt8)

> 提交文本并触发语音合成

[response.output\_item.added](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#efd58c096b3bv)

> 响应时有新的输出内容

[response.content\_part.added](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#141bec9bb11yi)

> 新的输出内容添加到assistant message 项

[response.audio.delta](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#a2b95643bdvnl)

> 模型增量生成的音频

[response.audio.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#faa3f9bc106tj)

> 完成音频生成

[response.content\_part.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#5244e1dbc9vw6)

> Assistant message 的音频内容流式输出完成

[response.output\_item.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#a922404106vzd)

> Assistant message 的整个输出项流式传输完成

[response.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#91f767e7440pc)

> 响应完成

提交之前通过append添加到云端缓冲区的文本，并立刻合成所有文本。如果输入的文本缓冲区为空将产生错误。

-   "server\_commit"模式下，客户端不需要发送此事件，服务器会自动提交文本缓冲区。
    
-   "commit"模式下，客户端必须通过commit触发语音合成。
    

finish

```
public void finish()
```

[session.finished](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#ac332f7d78oxg)

> 响应完成

终止任务。

close

```
public void close()
```

无

关闭连接。

getSessionId

```
public String getSessionId()
```

无

获取当前任务的session\_id。

getResponseId

```
public String getResponseId()
```

无

获取最近一次response的response\_id。

getFirstAudioDelay

```
public long getFirstAudioDelay()
```

无

获取首包音频延迟。

### **回调接口（**QwenTtsRealtimeCallback**）**

方法

参数

返回值

描述

```
public void onOpen()
```

无

无

当和服务端建立连接完成后，该方法立刻被回调。

```
public abstract void onEvent(JsonObject message)
```

message：服务端响应事件。

无

包括对接口调用的回复响应和模型生成的文本和音频。具体可以参考：[服务端事件](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events)

```
public abstract void onClose(int code, String reason)
```

code：关闭WebSocket的状态码。

reason：关闭WebSocket的关闭信息。

无

当服务已经关闭连接后进行回调。

# 实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考

本文档介绍如何使用 DashScope Java SDK 调用实时音视频翻译（Qwen-LiveTranslate）模型。

## **前提条件**

1.  [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，确保DashScope SDK版本不低于2.22.5。
    
2.  [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
3.  了解[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)。
    

## **请求参数**

-   以下参数通过`OmniRealtimeParam`的链式方法设置。
    
    **点击查看示例代码**
    
    ```
    OmniRealtimeParam param = OmniRealtimeParam.builder()
            .model("qwen3.5-livetranslate-flash-realtime")
            // 以下为中国内地地域url，若使用国际版，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
            .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
            // 国际版和中国内地的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            // 若没有配置环境变量，请用百炼API Key将下行替换为：.apikey("sk-xxx")
            .apikey(System.getenv("DASHSCOPE_API_KEY"))
            .build();
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `model`
    
    `String`
    
    是
    
    指定要使用的模型名称，推荐使用`qwen3.5-livetranslate-flash-realtime`。
    
    > `qwen3-livetranslate-flash-realtime`为旧版模型。
    
    `url`
    
    `String`
    
    是
    
    实时翻译服务地址：
    
    -   中国内地：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
        
    -   国际：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`
        
    
    `apikey`
    
    `String`
    
    否
    
    设置API Key。
    
-   以下参数通过`OmniRealtimeConfig`的链式方法设置。
    
    **点击查看示例代码**
    
    ```
    // 设置翻译热词
    Map<String, Object> phrases = new HashMap<>();
    phrases.put("人工智能", "Artificial Intelligence");
    phrases.put("机器学习", "Machine Learning");
    
    OmniRealtimeConfig config = OmniRealtimeConfig.builder()
            .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
            .voice("Tina")
            .inputAudioFormat(OmniRealtimeAudioFormat.PCM_16000HZ_MONO_16BIT)
            .outputAudioFormat(OmniRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
            .InputAudioTranscription("qwen3-asr-flash-realtime")
            .translationConfig(OmniRealtimeTranslationParam.builder()
                    .language("en")
                    .corpus(OmniRealtimeTranslationParam.Corpus.builder()
                            .phrases(phrases)
                            .build())
                    .build())
            .build();
    
    conversation.updateSession(config);
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `modalities`
    
    `List<OmniRealtimeModality>`
    
    否
    
    模型输出模态。
    
    默认值：`[OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT]`。
    
    取值范围：
    
    -   `[OmniRealtimeModality.TEXT]`：仅输出文本
        
    -   `[OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT]`：输出文本和音频
        
    
    `voice`
    
    `String`
    
    否
    
    生成音频的音色。
    
    默认值：
    
    -   Qwen3.5-LiveTranslate-Flash-Realtime默认音色为： `Tina`
        
    -   Qwen3-LiveTranslate-Flash-Realtime默认音色为： `Cherry`
        
    
    可选值：参见[支持的音色](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#0a5bde7593gdk)。
    
    `inputAudioFormat`
    
    `OmniRealtimeAudioFormat`
    
    否
    
    输入音频格式。
    
    默认值：`OmniRealtimeAudioFormat.PCM_16000HZ_MONO_16BIT`。
    
    `outputAudioFormat`
    
    `OmniRealtimeAudioFormat`
    
    否
    
    输出音频格式。
    
    默认值：`OmniRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT`。
    
    `InputAudioTranscription`
    
    `String`
    
    否
    
    输入音频转录模型。如需输出原文转录，则必须设置此参数。
    
    可选值：`qwen3-asr-flash-realtime`。
    
    `translationConfig`
    
    `OmniRealtimeTranslationParam`
    
    否
    
    翻译相关配置。
    
-   以下参数通过OmniRealtimeTranslationParam的链式方法设置。
    
    **点击查看示例代码**
    
    ```
    // 设置翻译热词
    Map<String, Object> phrases = new HashMap<>();
    phrases.put("人工智能", "Artificial Intelligence");  // 源语言词: 目标语言翻译
    phrases.put("机器学习", "Machine Learning");
    
    OmniRealtimeTranslationParam translationParam = OmniRealtimeTranslationParam.builder()
            .language("en")  // 翻译目标语言代码
            .corpus(OmniRealtimeTranslationParam.Corpus.builder()
                    .phrases(phrases)
                    .build())
            .build();
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `language`
    
    `String`
    
    否
    
    翻译目标语言代码。
    
    默认值：`en`。
    
    可选值：参见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s)。
    
    `corpus`
    
    `OmniRealtimeTranslationParam.Corpus`
    
    否
    
    热词配置，用于提升特定词汇的翻译准确性。
    
    `corpus.phrases`
    
    `Map<String, Object>`
    
    否
    
    热词映射表。key 为源语言词汇，value 为目标语言对应翻译。
    
    示例：`{"人工智能": "Artificial Intelligence"}`
    

## **关键接口**

### **OmniRealtimeConversation类**

OmniRealtimeConversation通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeConversation;`方法引入。

**方法签名**

**服务端响应事件（通过回调下发）**

**说明**

```
public OmniRealtimeConversation(OmniRealtimeParam param, OmniRealtimeCallback callback)
```

无

构造方法。

```
public void connect() throws NoApiKeyException, InterruptedException
```

[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#2c04b24bc3wlo)

> 会话已创建

[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#4d6ed9dd62vmj)

> 会话配置已更新

和服务端创建连接。

```
public void updateSession(OmniRealtimeConfig config)
```

[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#4d6ed9dd62vmj)

> 会话配置已更新

用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注`OmniRealtimeConfig`中涉及的参数。

```
public void appendAudio(String audioBase64)
```

无

将Base64编码后的音频数据片段追加到云端输入音频缓冲区。服务端会自动检测语音起止并触发翻译。

```
public void endSession() throws InterruptedException
```

[session.finished](https://help.aliyun.com/zh/model-studio/live-translator-server-events#5369266402pgb)

> 服务端完成语音翻译，结束会话

通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音翻译。

```
public void close(int code, String reason)
```

无

终止任务，并关闭连接。

```
public String getSessionId()
```

无

获取当前任务的session\_id。

```
public String getResponseId()
```

无

获取最近一次response的response\_id。

```
public long getFirstTextDelay()
```

无

获取最近一次响应的首个文本延迟（毫秒）。

```
public long getFirstAudioDelay()
```

无

获取最近一次响应的首个音频延迟（毫秒）。

### **回调接口（OmniRealtimeCallback）**

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。

继承此类并实现相应方法以处理服务端事件。

通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeCallback;`引入。

**方法签名**

**参数**

**说明**

```
public void onOpen()
```

无

WebSocket连接成功建立时触发。

```
public abstract void onEvent(JsonObject message)
```

message：[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events)

收到服务端事件时触发。

```
public abstract void onClose(int code, String reason)
```

code：状态码

reason：WebSocket连接关闭时的日志信息

WebSocket连接关闭时触发。

## **完整示例**

以下示例展示如何从麦克风实时录音并进行翻译。

**麦克风实时翻译示例代码**

```
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;

import javax.sound.sampled.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * 实时音视频翻译模型麦克风示例
 */
public class Main {
    private static final int INPUT_CHUNK_SIZE = 3200;   // 100ms 的 16kHz 16bit 单声道音频
    private static final int OUTPUT_CHUNK_SIZE = 4800;  // 100ms 的 24kHz 16bit 单声道音频
    private static final AtomicBoolean running = new AtomicBoolean(true);
    private static SourceDataLine speaker;  // 扬声器

    public static void main(String[] args) throws InterruptedException {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("请设置环境变量 DASHSCOPE_API_KEY");
            System.exit(1);
        }

        // 创建连接参数
        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen3.5-livetranslate-flash-realtime")
                .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                .apikey(apiKey)
                .build();

        // 创建回调处理
        OmniRealtimeCallback callback = new OmniRealtimeCallback() {
            @Override
            public void onOpen() {
                System.out.println("[连接已建立]");
            }

            @Override
            public void onEvent(JsonObject message) {
                String type = message.get("type").getAsString();
                switch (type) {
                    case "input_audio_buffer.speech_started":
                        System.out.println("====== 检测到语音输入 ======");
                        break;
                    case "input_audio_buffer.speech_stopped":
                        System.out.println("====== 语音输入结束 ======");
                        break;
                    case "conversation.item.input_audio_transcription.completed":
                        String originalText = message.get("transcript").getAsString();
                        System.out.println("[原文] " + originalText);
                        break;
                    case "response.audio_transcript.done":
                        String translatedText = message.get("transcript").getAsString();
                        System.out.println("[翻译结果] " + translatedText);
                        break;
                    case "response.audio.delta":
                        // 解码并播放翻译后的音频
                        String audioB64 = message.get("delta").getAsString();
                        byte[] audioBytes = Base64.getDecoder().decode(audioB64);
                        if (speaker != null) {
                            speaker.write(audioBytes, 0, audioBytes.length);
                        }
                        break;
                    case "error":
                        JsonObject error = message.get("error").getAsJsonObject();
                        System.err.println("[错误] " + error.get("message").getAsString());
                        break;
                }
            }

            @Override
            public void onClose(int code, String reason) {
                System.out.println("[连接已关闭] code: " + code + ", reason: " + reason);
            }
        };

        // 创建会话
        OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, callback);

        try {
            // 初始化扬声器（用于播放翻译后的语音）
            AudioFormat speakerFormat = new AudioFormat(24000, 16, 1, true, false);
            DataLine.Info speakerInfo = new DataLine.Info(SourceDataLine.class, speakerFormat);
            speaker = (SourceDataLine) AudioSystem.getLine(speakerInfo);
            speaker.open(speakerFormat, OUTPUT_CHUNK_SIZE * 4);
            speaker.start();

            // 初始化麦克风（用于采集语音输入）
            AudioFormat micFormat = new AudioFormat(16000, 16, 1, true, false);
            DataLine.Info micInfo = new DataLine.Info(TargetDataLine.class, micFormat);
            if (!AudioSystem.isLineSupported(micInfo)) {
                System.err.println("麦克风不可用");
                System.exit(1);
            }
            TargetDataLine microphone = (TargetDataLine) AudioSystem.getLine(micInfo);
            microphone.open(micFormat);
            microphone.start();

            // 连接服务端
            conversation.connect();

            // 配置翻译参数
            Map<String, Object> phrases = new HashMap<>();
            phrases.put("人工智能", "Artificial Intelligence");
            phrases.put("机器学习", "Machine Learning");

            OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                    .voice("Tina")
                    .inputAudioFormat(OmniRealtimeAudioFormat.PCM_16000HZ_MONO_16BIT)
                    .outputAudioFormat(OmniRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
                    .InputAudioTranscription("qwen3-asr-flash-realtime")
                    .translationConfig(OmniRealtimeTranslationParam.builder()
                            .language("en")
                            .corpus(OmniRealtimeTranslationParam.Corpus.builder()
                                    .phrases(phrases)
                                    .build())
                            .build())
                    .build();

            conversation.updateSession(config);

            // 注册退出信号处理
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                System.out.println("\n[正在退出...]");
                running.set(false);
                microphone.stop();
                microphone.close();
                speaker.stop();
                speaker.close();
                conversation.close(1000, "用户停止");
            }));

            System.out.println("[开始实时翻译] 请对着麦克风说话，按 Ctrl+C 退出");

            // 持续采集麦克风音频并发送
            byte[] buffer = new byte[INPUT_CHUNK_SIZE];
            while (running.get()) {
                int bytesRead = microphone.read(buffer, 0, buffer.length);
                if (bytesRead > 0) {
                    conversation.appendAudio(Base64.getEncoder().encodeToString(buffer));
                }
            }

        } catch (NoApiKeyException e) {
            System.err.println("API Key 错误: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("发生异常: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

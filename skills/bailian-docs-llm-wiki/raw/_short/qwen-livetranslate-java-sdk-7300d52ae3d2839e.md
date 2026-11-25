# Qwen-LiveTranslate-Realtime Java SDK

本文档介绍如何使用 DashScope Java SDK 调用实时音视频翻译（Qwen-LiveTranslate-Realtime）模型。

连接与鉴权参见 [WebSocket 接入](livetranslate-realtime-websocket-access-c83c6ed44456849c.md)；事件字段与 JSON 示例参见[客户端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)和[服务端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)。

<a id="前提条件"></a>

<a id="lt002prereqh2"></a>

## 前提条件

1.  [安装SDK](../model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.22.5。
2.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。
3.  了解[实时语音/音视频翻译-千问](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `wss://dashscope.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `wss://dashscope-intl.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="快速开始"></a>

<a id="lt002exampleh2"></a>

<a id="完整示例"></a>

## 快速开始

以下示例展示如何从麦克风实时录音并进行翻译。

<a id="accordion-麦克风实时翻译示例代码"></a>

麦克风实时翻译示例代码

<a id="code-block"></a>

```java
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;

import javax.sound.sampled.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;
import com.alibaba.dashscope.utils.Constants;

/**
 * 实时音视频翻译模型麦克风示例
 */
public class Main {
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
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
                .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
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
                try {
                    conversation.endSession();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
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

<a id="请求参数"></a>

<a id="lt002paramsh2"></a>

## 请求参数

WebSocket`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`

WebSocket`wss://WorkspaceId.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`

-   以下参数通过`OmniRealtimeParam`的链式方法设置。
    
    <a id="accordion-点击查看示例代码"></a>
    
    点击查看示例代码
    
    <a id="code-block-2"></a>
    
    ```java
    OmniRealtimeParam param = OmniRealtimeParam.builder()
            .model("qwen3.5-livetranslate-flash-realtime")
            // 使用请求地址所选地域和业务空间的 API Key。
            .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
            // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            // 若没有配置环境变量，请用百炼API Key将下行替换为：.apikey("sk-xxx")
            .apikey(System.getenv("DASHSCOPE_API_KEY"))
            .build();
    ```
    
    | 参数 | 类型 | 是否必须 | 说明 |
    | --- | --- | --- | --- |
    | `model` | `String` | 是 | 指定要使用的模型名称，推荐使用`qwen3.5-livetranslate-flash-realtime`。 |
    | `url` | `String` | 是 | 实时翻译服务的 WebSocket 地址。见[请求参数](#lt002paramsh2)中的连接地址。 |
    | `apikey` | `String` | 否 | 设置API Key。 |
    
-   以下参数通过`OmniRealtimeConfig`的链式方法设置。
    
    <a id="accordion-点击查看示例代码-2"></a>
    
    点击查看示例代码
    
    <a id="code-block-3"></a>
    
    ```java
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
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>modalities</code></p></td><td><p><code>List&lt;OmniRealtimeModality&gt;</code></p></td><td><p>否</p></td><td><p>模型输出模态。</p><p>默认值：<code>[OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT]</code>。</p><p>取值范围：</p><ul><li><p><code>[OmniRealtimeModality.TEXT]</code>：仅输出文本</p></li><li><p><code>[OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT]</code>：输出文本和音频</p></li></ul></td></tr><tr><td><p><code>voice</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>生成音频的音色。</p><p>默认值：</p><ul><li><p>Qwen3.5-LiveTranslate-Flash-Realtime默认音色为： <code>Tina</code></p></li></ul><p>可选值：参见<a href="../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#0a5bde7593gdk">支持的音色</a>。</p></td></tr><tr><td><p><code>inputAudioFormat</code></p></td><td><p><code>OmniRealtimeAudioFormat</code></p></td><td><p>否</p></td><td><p>输入音频格式。</p><p>默认值：<code>OmniRealtimeAudioFormat.PCM_16000HZ_MONO_16BIT</code>。</p></td></tr><tr><td><p><code>outputAudioFormat</code></p></td><td><p><code>OmniRealtimeAudioFormat</code></p></td><td><p>否</p></td><td><p>输出音频格式。</p><p>默认值：<code>OmniRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT</code>。</p></td></tr><tr><td><p><code>InputAudioTranscription</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>输入音频转录模型。如需输出原文转录，则必须设置此参数。</p><p>可选值：<code>qwen3-asr-flash-realtime</code>。</p></td></tr><tr><td><p><code>translationConfig</code></p></td><td><p><code>OmniRealtimeTranslationParam</code></p></td><td><p>否</p></td><td><p>翻译相关配置。</p></td></tr><tr><td><p><code>enableTurnDetection</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用 VAD（语音活动检测）。</p><p>默认值：<code>true</code>，即启用 VAD 模式，服务端自动检测语音起止并自动触发翻译。</p><p>设为<code>false</code>可切换为 Manual 模式，由客户端通过<code>commit()</code>方法手动提交音频。详细参数说明参见<a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md">turn_detection object （可选） 语音活动检测（VAD，Voice Activity Detection）配置，用于控制语音起止的检测方式： 设为配置对象（默认值）：启用 VAD 模式。服务端自动检测语音起止，自动提交音频缓冲区并触发翻译响应，客户端无需发送input_audio_buffer.commit事件。 设为null：启用 Manual 模式。由客户端通过input_audio_buffer.commit事件手动提交音频缓冲区，服务端收到后自动开始生成翻译响应。 属性 type string （可选） VAD 类型，固定为server_vad。 threshold float （可选） VAD 检测灵敏度。值越低，越容易将微弱声音（包括背景噪音）识别为语音；值越高，需要更清晰、音量更大的语音才能触发。 取值范围：[-1.0, 1.0]，默认值为 0.2。 silence_duration_ms integer （可选） 语音结束后需保持静音的最短时长（毫秒）。超过该时长后判定语音结束，服务端自动提交音频缓冲区并触发翻译响应。 取值范围：[200, 6000]，默认值为 1000。</a>。</p></td></tr></tbody></table>
    
    **扩展会话参数**
    
    部分会话参数没有对应的 SDK 配置方法，可以通过 `OmniRealtimeConfig.builder().parameters(Map)` 传入。Map 中的键会直接写入 `session`。例如，开启实时声音复刻时，先构造以下参数：
    
    <a id="code-block-4"></a>
    
    ```java
    Map<String, Object> options = new HashMap<>();
    options.put("frequency", "once");
    
    Map<String, Object> parameters = new HashMap<>();
    parameters.put("enable_voice_clone", true);
    parameters.put("voice_clone_options", options);
    ```
    
    在已有配置构建链中，将音色设为 `.voice("default")`，并加入 `.parameters(parameters)`。保留原有语种和音频设置，构建后调用 `conversation.updateSession(config)`。复刻频率与音色的搭配见[声音复刻](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#8q75hr4eu55j0)。
    
-   以下参数通过OmniRealtimeTranslationParam的链式方法设置。
    
    <a id="accordion-点击查看示例代码-3"></a>
    
    点击查看示例代码
    
    <a id="code-block-5"></a>
    
    ```java
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
    
    | 参数 | 类型 | 是否必须 | 说明 |
    | --- | --- | --- | --- |
    | `language` | `String` | 否 | 翻译目标语言代码。<br><br>默认值：`en`。<br><br>可选值：参见[支持的语种](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#4ffd192226f0s)。 |
    | `corpus` | `OmniRealtimeTranslationParam.Corpus` | 否 | 热词配置，用于提升特定词汇的翻译准确性。 |
    | `corpus.phrases` | `Map<String, Object>` | 否 | 热词映射表。key 为源语言词汇，value 为目标语言对应翻译。<br><br>示例：`{"人工智能": "Artificial Intelligence"}` |
    

<a id="接口参考"></a>

<a id="lt002interfacesh2"></a>

<a id="关键接口"></a>

## 接口参考

<a id="omnirealtimeconversation类"></a>

<a id="lt002conversationh3"></a>

### OmniRealtimeConversation类

OmniRealtimeConversation通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeConversation;`方法引入。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>服务端响应事件（通过回调下发）</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-6"></a><pre class="language-java"><code>public OmniRealtimeConversation(OmniRealtimeParam param, OmniRealtimeCallback callback)
</code></pre></td><td><p>无</p></td><td><p>构造方法。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-java"><code>public void connect() throws NoApiKeyException, InterruptedException
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-java"><code>public void updateSession(OmniRealtimeConfig config)
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注<code>OmniRealtimeConfig</code>中涉及的参数。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-java"><code>public void appendAudio(String audioBase64)
</code></pre></td><td><p>无</p></td><td><p>将Base64编码后的音频数据片段追加到云端输入音频缓冲区。服务端会自动检测语音起止并触发翻译。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-java"><code>public void commit()
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md#ltcommitted001h2">input_audio_buffer.committed</a></p><blockquote><p>输入音频缓冲区已提交</p></blockquote></td><td><p>Manual 模式下，提交之前通过<code>appendAudio</code>方法追加到云端缓冲区的音频，服务端收到后自动开始生成翻译响应。VAD 模式下无需调用此方法，服务端会自动提交。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-java"><code>public void clearAppendedAudio()
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md#ltcleared001h2">input_audio_buffer.cleared</a></p><blockquote><p>输入音频缓冲区已清空</p></blockquote></td><td><p>清空当前云端缓冲区中尚未提交的音频数据。</p></td></tr><tr><td><a id="code-block-12"></a><pre class="language-java"><code>public void endSession() throws InterruptedException
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md#5369266402pgb">session.finished</a></p><blockquote><p>服务端完成语音翻译，结束会话</p></blockquote></td><td><p>通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音翻译。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-java"><code>public void close(int code, String reason)
</code></pre></td><td><p>无</p></td><td><p>终止任务，并关闭连接。</p></td></tr><tr><td><a id="code-block-14"></a><pre class="language-java"><code>public String getSessionId()
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-java"><code>public String getResponseId()
</code></pre></td><td><p>无</p></td><td><p>获取最近一次response的response_id。</p></td></tr><tr><td><a id="code-block-16"></a><pre class="language-java"><code>public long getFirstTextDelay()
</code></pre></td><td><p>无</p></td><td><p>获取最近一次响应的首个文本延迟（毫秒）。</p></td></tr><tr><td><a id="code-block-17"></a><pre class="language-java"><code>public long getFirstAudioDelay()
</code></pre></td><td><p>无</p></td><td><p>获取最近一次响应的首个音频延迟（毫秒）。</p></td></tr></tbody></table>

<a id="回调接口-omnirealtimecallback"></a>

<a id="lt002callback"></a>

### 回调接口（OmniRealtimeCallback）

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。

继承此类并实现相应方法以处理服务端事件。

通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeCallback;`引入。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>参数</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-18"></a><pre class="language-java"><code>public void onOpen()
</code></pre></td><td><p>无</p></td><td><p>WebSocket连接成功建立时触发。</p></td></tr><tr><td><a id="code-block-19"></a><pre class="language-java"><code>public abstract void onEvent(JsonObject message)
</code></pre></td><td><p>message：<a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p></td><td><p>收到服务端事件时触发。</p></td></tr><tr><td><a id="code-block-20"></a><pre class="language-java"><code>public abstract void onClose(int code, String reason)
</code></pre></td><td><p>code：状态码</p><p>reason：WebSocket连接关闭时的日志信息</p></td><td><p>WebSocket连接关闭时触发。</p></td></tr></tbody></table>

![](data:image/png;base64,)

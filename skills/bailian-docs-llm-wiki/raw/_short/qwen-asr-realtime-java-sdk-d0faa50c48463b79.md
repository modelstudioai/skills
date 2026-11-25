# Qwen-ASR-Realtime Java SDK

本文档介绍如何使用 DashScope Java SDK 调用实时语音识别（Qwen-ASR-Realtime）模型。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="前提条件"></a>

<a id="b0c7b4e349rvj"></a>

## 前提条件

1.  [安装SDK](../model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.22.5。
2.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。
3.  了解[WebSocket API](qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md)。

<a id="快速开始"></a>

<a id="qwen-asr-complete-example"></a>

<a id="完整示例"></a>

## 快速开始

> **说明**
>
> 示例代码读取 `your_audio_file.pcm`（PCM16、16 kHz、单声道）。如仅有 MP3/WAV 等格式，可使用 ffmpeg 转换：
>
> <a id="code-block"></a>
>
> ```bash
> ffmpeg -i your_audio.mp3 -ar 16000 -ac 1 -f s16le your_audio_file.pcm
> ```

<a id="code-block-2"></a>

```java
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.sound.sampled.LineUnavailableException;
import java.io.File;
import java.io.FileInputStream;
import java.util.Base64;
import java.util.Collections;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

public class Qwen3AsrRealtimeUsage {
    private static final Logger log = LoggerFactory.getLogger(Qwen3AsrRealtimeUsage.class);
    private static final int AUDIO_CHUNK_SIZE = 1024; // Audio chunk size in bytes
    private static final int SLEEP_INTERVAL_MS = 30;  // Sleep interval in milliseconds

    public static void main(String[] args) throws InterruptedException, LineUnavailableException {
        CountDownLatch finishLatch = new CountDownLatch(1);

        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen3-asr-flash-realtime")
                // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
                .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apikey("sk-xxx")
                .apikey(System.getenv("DASHSCOPE_API_KEY"))
                .build();

        OmniRealtimeConversation conversation = null;
        final AtomicReference<OmniRealtimeConversation> conversationRef = new AtomicReference<>(null);
        conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
            @Override
            public void onOpen() {
                System.out.println("connection opened");
            }
            @Override
            public void onEvent(JsonObject message) {
                String type = message.get("type").getAsString();
                switch(type) {
                    case "session.created":
                        System.out.println("start session: " + message.get("session").getAsJsonObject().get("id").getAsString());
                        break;
                    case "conversation.item.input_audio_transcription.completed":
                        System.out.println("transcription: " + message.get("transcript").getAsString());
                        finishLatch.countDown();
                        break;
                    case "input_audio_buffer.speech_started":
                        System.out.println("======VAD Speech Start======");
                        break;
                    case "input_audio_buffer.speech_stopped":
                        System.out.println("======VAD Speech Stop======");
                        break;
                    case "conversation.item.input_audio_transcription.text":
                        System.out.println("transcription: " + message.get("text").getAsString() + message.get("stash").getAsString());
                        break;
                    default:
                        break;
                }
            }
            @Override
            public void onClose(int code, String reason) {
                System.out.println("connection closed code: " + code + ", reason: " + reason);
            }
        });
        conversationRef.set(conversation);
        try {
            conversation.connect();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }

        OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
        transcriptionParam.setLanguage("zh");
        transcriptionParam.setInputAudioFormat("pcm");
        transcriptionParam.setInputSampleRate(16000);

        OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                .modalities(Collections.singletonList(OmniRealtimeModality.TEXT))
                .transcriptionConfig(transcriptionParam)
                .build();
        conversation.updateSession(config);

        String filePath = "your_audio_file.pcm";
        File audioFile = new File(filePath);
        if (!audioFile.exists()) {
            log.error("Audio file not found: {}", filePath);
            return;
        }

        try (FileInputStream audioInputStream = new FileInputStream(audioFile)) {
            byte[] audioBuffer = new byte[AUDIO_CHUNK_SIZE];
            int bytesRead;
            int totalBytesRead = 0;

            log.info("Starting to send audio data from: {}", filePath);

            // Read and send audio data in chunks
            while ((bytesRead = audioInputStream.read(audioBuffer)) != -1) {
                totalBytesRead += bytesRead;
                byte[] chunk = new byte[bytesRead];
                System.arraycopy(audioBuffer, 0, chunk, 0, bytesRead);
                String audioB64 = Base64.getEncoder().encodeToString(chunk);
                // Send audio chunk to conversation
                conversation.appendAudio(audioB64);

                // Add small delay to simulate real-time audio streaming
                Thread.sleep(SLEEP_INTERVAL_MS);
            }

            log.info("Finished sending audio data. Total bytes sent: {}", totalBytesRead);

        } catch (Exception e) {
            log.error("Error sending audio from file: {}", filePath, e);
        }

        //send session.finish and wait for finish and close
        conversation.endSession();
        log.info("task finished");

        System.exit(0);
    }
}
```

<a id="请求参数"></a>

<a id="e80d6aab34svh"></a>

## 请求参数

-   以下参数通过`OmniRealtimeParam`的链式方法设置。
    
    <a id="accordion-点击查看示例代码"></a>
    
    点击查看示例代码
    
    <a id="code-block-3"></a>
    
    ```java
    OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3-asr-flash-realtime")
                    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
                    .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                    // 若没有配置环境变量，请用百炼API Key将下行替换为：.apikey("sk-xxx")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    .build();
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>model</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>指定要使用的<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md">模型</a>名称。</p></td></tr><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>语音识别服务地址：</p><ul><li><p>华北2（北京）地域：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime</code>。调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></li><li><p>新加坡地域：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime</code>。调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p></li></ul></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>设置API Key。</p></td></tr></tbody></table>
    
-   以下参数通过`OmniRealtimeConfig`的链式方法设置。
    
    <a id="accordion-点击查看示例代码-2"></a>
    
    点击查看示例代码
    
    <a id="code-block-4"></a>
    
    ```java
    OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
            transcriptionParam.setLanguage("zh");
            transcriptionParam.setInputSampleRate(16000);
            transcriptionParam.setInputAudioFormat("pcm");
    
    OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                    .modalities(Collections.singletonList(OmniRealtimeModality.TEXT))
                    .enableTurnDetection( true)
                    .turnDetectionType("server_vad")
                    .turnDetectionThreshold(0.0f)
                    .turnDetectionSilenceDurationMs(400)
                    .transcriptionConfig(transcriptionParam)
                    .build();
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>modalities</code></p></td><td><p><code>List&lt;OmniRealtimeModality&gt;</code></p></td><td><p>是</p></td><td><p>模型输出模态，固定为<code>[OmniRealtimeModality.TEXT]</code>。</p></td></tr><tr><td><p><code>enableTurnDetection</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启服务端语音活动检测（VAD）。关闭后，需手动调用<code>commit()</code>方法触发识别。</p><p>默认值：<code>true</code>。</p><p>取值范围：</p><ul><li><p><code>true</code>：开启</p></li><li><p><code>false</code>：关闭</p></li></ul></td></tr><tr><td><p><code>turnDetectionType</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>服务端VAD类型，固定为 <code>server_vad</code>。</p></td></tr><tr><td><p><code>turnDetectionThreshold</code></p></td><td><p><code>float</code></p></td><td><p>否</p></td><td><div><p>VAD检测阈值。推荐将该值设为<code>0.0</code>。</p><p>默认值：<code>0.5</code>。</p><p>取值范围：<code>[-1, 1]</code>。</p><p>较低的阈值会提高 VAD 的灵敏度，可能将背景噪音误判为语音。较高的阈值则降低灵敏度，有助于在嘈杂环境中减少误触发。</p></div></td></tr><tr><td><p><code>turnDetectionSilenceDurationMs</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><div><p>VAD断句检测阈值（ms）。静音持续时长超过该阈值将被认为是语句结束。推荐将该值设为<code>400</code>。</p><p>默认值：<code>800</code>。</p><p>取值范围：<code>[200, 6000]</code>。</p><p>较低的值（如 300ms）可使模型更快响应，但可能导致在自然停顿处发生不合理的断句。较高的值（如 1200ms）可更好地处理长句内的停顿，但会增加整体响应延迟。</p></div></td></tr><tr><td><p><code>transcriptionConfig</code></p></td><td><p><code>OmniRealtimeTranscriptionParam</code></p></td><td><p>否</p></td><td><p>语音识别相关配置。</p></td></tr></tbody></table>
    
-   以下参数通过`OmniRealtimeTranscriptionParam`的`setter`方法设置。
    
    <a id="accordion-点击查看示例代码-3"></a>
    
    点击查看示例代码
    
    <a id="code-block-5"></a>
    
    ```java
    OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
            transcriptionParam.setLanguage("zh");
            transcriptionParam.setInputSampleRate(16000);
            transcriptionParam.setInputAudioFormat("pcm");
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>language</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音频源语言。</p><ul><li><p>zh：中文（普通话、四川话、闽南语、吴语）</p></li><li><p>yue：粤语</p></li><li><p>en：英文</p></li><li><p>ja：日语</p></li><li><p>de：德语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>fr：法语</p></li><li><p>pt：葡萄牙语</p></li><li><p>ar：阿拉伯语</p></li><li><p>it：意大利语</p></li><li><p>es：西班牙语</p></li><li><p>hi：印地语</p></li><li><p>id：印尼语</p></li><li><p>th：泰语</p></li><li><p>tr：土耳其语</p></li><li><p>uk：乌克兰语</p></li><li><p>vi：越南语</p></li><li><p>cs：捷克语</p></li><li><p>da：丹麦语</p></li><li><p>fil：菲律宾语</p></li><li><p>fi：芬兰语</p></li><li><p>is：冰岛语</p></li><li><p>ms：马来语</p></li><li><p>no：挪威语</p></li><li><p>pl：波兰语</p></li><li><p>sv：瑞典语</p></li></ul></div></td></tr><tr><td><p><code>inputSampleRate</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><div><p>音频采样率（Hz）。支持<code>16000</code>和<code>8000</code>。</p><p>默认值：<code>16000</code>。</p><p>设置为 <code>8000</code> 时，服务端会先升采样到16000Hz再进行识别，可能引入微小延迟。建议仅在源音频为8000Hz（如电话线路）时使用。</p></div></td></tr><tr><td><p><code>inputAudioFormat</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音频格式。支持<code>pcm</code>和<code>opus</code>。</p><p>默认值：<code>pcm</code>。</p></div></td></tr></tbody></table>
    

<a id="接口参考"></a>

<a id="08096516dauq0"></a>

<a id="关键接口"></a>

## 接口参考

<a id="omnirealtimeconversation类"></a>

<a id="4c4810ff87ofz"></a>

### OmniRealtimeConversation类

OmniRealtimeConversation通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeConversation;`方法引入。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>服务端响应事件（通过回调下发）</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-6"></a><pre class="language-java"><code>public OmniRealtimeConversation(OmniRealtimeParam param, OmniRealtimeCallback callback)
</code></pre></td><td><p>无</p></td><td><p>构造方法。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-java"><code>public void connect() throws NoApiKeyException, InterruptedException
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#2c04b24bc3wlo">session.created</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#4d6ed9dd62vmj">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-java"><code>public void updateSession(OmniRealtimeConfig config)
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#4d6ed9dd62vmj">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注<a href="qwen-asr-realtime-java-sdk-d0faa50c48463b79.md">请求参数</a>中的涉及到的参数。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-java"><code>public void appendAudio(String audioBase64)
</code></pre></td><td><p>无</p></td><td><p>将Base64编码后的音频数据片段追加到云端输入音频缓冲区。</p><ul><li><a href="qwen-asr-realtime-java-sdk-d0faa50c48463b79.md">请求参数</a><code>enableTurnDetection</code>设为<code>true</code>，音频缓冲区用于检测语音，服务端决定何时提交。</li><li><a href="qwen-asr-realtime-java-sdk-d0faa50c48463b79.md">请求参数</a><code>enableTurnDetection</code>设为<code>false</code>，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。</li></ul></td></tr><tr><td><a id="code-block-10"></a><pre class="language-java"><code>public void commit()
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#1108a3764an0e">input_audio_buffer.committed</a></p><blockquote><p>服务端收到提交的音频</p></blockquote></td><td><p>提交之前通过append添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。</p><p><strong>禁用场景：</strong><a href="qwen-asr-realtime-java-sdk-d0faa50c48463b79.md">请求参数</a><code>enableTurnDetection</code>设为<code>true</code>时。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-java"><code>public void endSession() throws InterruptedException
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#6eaa77339djdv">session.finished</a></p><blockquote><p>服务端完成语音识别，结束会话</p></blockquote></td><td><p>通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音识别。</p><p><strong>调用时机</strong>：</p><ul><li><a href="qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md#9b49887720jcw">VAD 模式（默认）</a>下，发送完音频后调用该方法</li><li><a href="qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md#ee09a3493fsuc">Manual 模式</a>下，调用commit方法之后调用该方法</li></ul><p><code>endSessionAsync</code> 是 <code>endSession</code> 的异步版本，两者功能完全相同。</p></td></tr><tr><td><a id="code-block-12"></a><pre class="language-java"><code>public void close()
</code></pre></td><td><p>无</p></td><td><p>终止任务，并关闭连接。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-java"><code>public String getSessionId()
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id。</p></td></tr><tr><td><a id="code-block-14"></a><pre class="language-java"><code>public String getResponseId()
</code></pre></td><td><p>无</p></td><td><p>获取最近一次response的response_id。</p></td></tr></tbody></table>

<a id="回调接口-omnirealtimecallback"></a>

<a id="9d08669109iwx"></a>

### 回调接口（OmniRealtimeCallback）

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。

继承此类并实现相应方法以处理服务端事件。

通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeCallback;`引入。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>参数</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-15"></a><pre class="language-java"><code>public void onOpen()
</code></pre></td><td><p>无</p></td><td><p>WebSocket连接成功建立时触发。</p></td></tr><tr><td><a id="code-block-16"></a><pre class="language-java"><code>public abstract void onEvent(JsonObject message)
</code></pre></td><td><p>message：<a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md">服务端事件</a></p></td><td><p>收到服务端事件时触发。</p></td></tr><tr><td><a id="code-block-17"></a><pre class="language-java"><code>public abstract void onClose(int code, String reason)
</code></pre></td><td><p>code：状态码</p><p>reason：WebSocket连接关闭时的日志信息</p></td><td><p>WebSocket连接关闭时触发。</p></td></tr></tbody></table>

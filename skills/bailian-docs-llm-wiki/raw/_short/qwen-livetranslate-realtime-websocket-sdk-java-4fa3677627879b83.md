# Qwen-LiveTranslate-Realtime Java SDK

本文档介绍如何使用 DashScope Java SDK 调用实时音视频翻译（Qwen-LiveTranslate-Realtime）模型。

## 前提条件

1.  [安装SDK](raw/model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.22.5。
2.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
3.  了解[实时语音/音视频翻译-千问](raw/model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `wss://dashscope.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `wss://dashscope-intl.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

## 快速开始

以下示例展示如何从麦克风实时录音并进行翻译。

麦克风实时翻译示例代码

```
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

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/qwen-livetranslate-java-sdk#lt002paramsh2)
-   [接口参考](https://help.aliyun.com/zh/model-studio/qwen-livetranslate-java-sdk#lt002interfacesh2)

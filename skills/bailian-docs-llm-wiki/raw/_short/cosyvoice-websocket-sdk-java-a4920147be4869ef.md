# CosyVoice Java SDK

## 前提条件

-   [安装 Java SDK](raw/model-api-reference/preparations/install-sdk.md)
-   [获取并配置 API Key](raw/model-api-reference/preparations/get-api-key.md)

## 快速开始

示例使用北京。将代码中的 `{WorkspaceId}` 替换为实际的[业务空间 ID](raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。运行后，音频保存到当前目录的 `output.mp3`。

```
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class Main {
    // 模型
    private static String model = "cosyvoice-v3-plus";
    // 音色
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();

        // 同步模式：禁用回调（第二个参数为null）
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        ByteBuffer audio = null;
        try {
            // 阻塞直至音频返回
            audio = synthesizer.call("今天天气怎么样？");
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        if (audio != null) {
            // 将音频数据保存到本地文件"output.mp3"中
            File file = new File("output.mp3");
            // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
            System.out.println(
                    "[Metric] requestId为："
                            + synthesizer.getLastRequestId()
                            + "首包延迟（毫秒）为："
                            + synthesizer.getFirstPackageDelay());
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(audio.array());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

## 更多示例与参考

-   [流式合成示例](https://help.aliyun.com/zh/model-studio/realtime-websocket-java-sdk-qwen-audio-tts-cosyvoice#model-cosyvoice-6bc2d05715bdk)
-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-java-sdk-qwen-audio-tts-cosyvoice#model-cosyvoice-h3-6m2k9p5r)
-   [接口参考](https://help.aliyun.com/zh/model-studio/realtime-websocket-java-sdk-qwen-audio-tts-cosyvoice#model-cosyvoice-h4-7k2m9p5r)

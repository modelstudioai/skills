# Qwen-Audio-ASR-Message Java SDK

## 前提条件

-   已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。请配置API Key到环境变量，而非硬编码在代码中，防范因代码泄露导致的安全风险。
-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

将示例中的 `{WorkspaceId}` 换成实际的业务空间 ID，`{YOUR_AUDIO_FILE}` 换成本地 16 kHz WAV 文件路径。运行后，终端输出识别结果。

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        // 创建Recognition实例
        Recognition recognizer = new Recognition();
        // 创建RecognitionParam
        RecognitionParam param =
                RecognitionParam.builder()
                        .model("qwen-audio-3.1-asr-flash-message")
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .format("wav")
                        .sampleRate(16000)
                        .build();

        try {
            System.out.println("识别结果：" + recognizer.call(param, new File("{YOUR_AUDIO_FILE}")));
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

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-java-sdk-qwen-audio-asr-fun-asr#model-qwen-audio-asr-message)
-   [接口参考](raw/_short/realtime-websocket-java-sdk-qwen-audio-asr-fun-a-40ad2b10386e472d.md)

# Omni 声音复刻用户指南

使用参考音频创建 Omni 复刻音色，并在实时或非实时全模态调用中使用；包含完整示例、音频要求、配额和计费。

**用户指南**：关于模型介绍和选型建议请参见[实时（Qwen-Omni-Realtime）](raw/model-user-guide/model-experience/omni-modal/realtime.md)或[非实时（Qwen-Omni）](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)。

**重要**本文档专用于千问Omni和千问Omni-Realtime声音复刻接口；若您使用的是语音合成模型，请参见[声音复刻用户指南](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

请求参数、响应和错误说明见[声音复刻 API 参考](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning)。

## 音频要求

高质量的输入音频是获得优质复刻效果的基础。

**项目**

**要求**

**支持格式**

WAV (16bit)、MP3、M4A

**音频时长**

推荐10~20秒，最长不得超过60秒

**文件大小**

＜ 10 MB

**采样率**

≥ 24 kHz

**声道**

单声道

**内容**

音频必须包含至少3秒连续清晰朗读（无背景音），其余部分仅允许短暂停顿（≤2秒）；整段音频应避免背景音乐、噪音或其他人声，确保核心朗读内容质量；请使用正常说话音频作为输入，不要上传歌曲或唱歌音频，以确保复刻效果准确和可用

**语言**

中文（zh）、英文（en）、德语（de）、意大利语（it）、葡萄牙语（pt）、西班牙语（es）、日语（ja）、韩语（ko）、法语（fr）、俄语（ru）、泰语（th）、印尼语（id）、阿拉伯语（ar）、捷克语（cs）、丹麦语（da）、荷兰语（nl）、芬兰语（fi）、希伯来语（he）、印地语（hi）、冰岛语（is）、马来语（ms）、挪威语（no）、波斯语（fa）、波兰语（pl）、瑞典语（sv）、他加禄语（tl）、土耳其语（tr）、乌尔都语（ur）、越南语（vi）

中文方言：东北话（Dongbei）、陕西话（Shannxi）、四川话（Sichuan）、河南话（Henan）、长沙话（Changsha）、天津话（Tianjin）、杭州话（Hangzhou）、辽宁话（Liaoning）、沈阳话（Shenyang）、鞍山话（Anshan）

## 快速开始：复刻与使用音色

先创建音色，再调用模型使用音色：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2365984871/CAEQbxiBgICd6_Do8BkiIDM3NjYwZDQxMGIyMTQzMDdhOGMyY2YwNWFhMmM2NjVi5899512_20251120114927.389.svg)

### 1\. 工作流程

声音复刻与模型调用是紧密关联的两个独立步骤，遵循“先创建，后使用”的流程：

1.  创建音色
    
    调用[创建音色](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#1eaa57d82did9)接口，上传一段音频。系统会分析该音频，创建一个专属的复刻音色。**此步骤必须指定**`target_model`**，声明创建的音色将由哪个全模态模型驱动。**
    
    若已有创建好的音色（调用[查询音色列表](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#401d33226330i)接口查看），可跳过这一步直接进行下一步。
    
2.  使用音色进行对话
    
    调用 Omni 接口（实时或非实时），传入上一步获得的音色。**此步骤指定的全模态模型必须和上一步的**`target_model`**一致。**
    

### 2\. 模型配置与准备工作

选择合适的模型并完成准备工作。

#### 模型配置

声音复刻时需要指定以下两个模型：

-   声音复刻模型：qwen-voice-enrollment
    
-   驱动音色的全模态模型：
    
    -   qwen3.8-omni-flash-realtime
    -   qwen3.5-omni-plus-realtime
    -   qwen3.5-omni-flash-realtime
    -   qwen3.5-omni-plus
    -   qwen3.5-omni-flash

#### 准备工作

1.  **获取API Key**：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，为安全起见，推荐将API Key配置到环境变量。
2.  获取并配置 API Host
    
    从控制台[获取API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)并填入下方，本文其他可编辑地址会同步更新。
    
    {WorkspaceId}.cn-beijing.maas.aliyuncs.com
    
3.  **安装SDK**：确保已[安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。
4.  **准备待复刻音频**：音频需符合[音频要求](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#fe3daa6c3f7jw)。

### 3\. 端到端示例

以下示例演示了如何在对话中使用声音复刻生成的专属音色，实现与原音高度相似的输出效果。

-   **关键原则**：声音复刻时，`target_model`（驱动音色的全模态模型）必须与后续调用 Omni 接口时指定的模型一致，否则会合成失败。
-   示例使用本地音频文件 `voice.mp3` 进行声音复刻，运行代码时，请注意替换。

#### 实时

适用于千问Omni-Realtime系列模型，更多说明请参见[实时（Qwen-Omni-Realtime）](raw/model-user-guide/model-experience/omni-modal/realtime.md)。

Python

```
# 依赖：dashscope >= 1.26.5，pyaudio
import os
import requests
import base64
import pathlib
import time
import pyaudio
from dashscope.audio.qwen_omni import MultiModality, OmniRealtimeCallback, OmniRealtimeConversation
import dashscope

# ======= 常量配置 =======
DEFAULT_TARGET_MODEL = "qwen3.8-omni-flash-realtime"  # 声音复刻、实时对话要使用相同的模型
DEFAULT_PREFERRED_NAME = "guanyu"
DEFAULT_AUDIO_MIME_TYPE = "audio/mpeg"
VOICE_FILE_PATH = "voice.mp3"  # 用于声音复刻的本地音频文件的相对路径

def create_voice(file_path: str,
                 url: str,
                 target_model: str = DEFAULT_TARGET_MODEL,
                 preferred_name: str = DEFAULT_PREFERRED_NAME,
                 audio_mime_type: str = DEFAULT_AUDIO_MIME_TYPE) -> str:
    """
    创建音色，并返回 voice 参数
    """
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    file_path_obj = pathlib.Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:{audio_mime_type};base64,{base64_str}"
    payload = {
        "model": "qwen-voice-enrollment",
        "parameters": {"voice_clone_mode": "normal"},
        "input": {
            "action": "create",
            "target_model": target_model,
            "preferred_name": preferred_name,
            "audio": {"data": data_uri}
        }
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"创建 voice 失败: {resp.status_code}, {resp.text}")

    try:
        return resp.json()["output"]["voice"]
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"解析 voice 响应失败: {e}")

class SimpleCallback(OmniRealtimeCallback):
    def __init__(self, pya):
        self.pya = pya
        self.out = None
    def on_open(self):
        self.out = self.pya.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )
    def on_event(self, response):
        if response['type'] == 'response.audio.delta':
            self.out.write(base64.b64decode(response['delta']))
        elif response['type'] == 'conversation.item.input_audio_transcription.completed':
            print(f"[User] {response['transcript']}")
        elif response['type'] == 'response.audio_transcript.done':
            print(f"[LLM] {response['transcript']}")

if __name__ == '__main__':
    # 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # 默认示例为华北2（北京），请使用业务空间对应的 API Host 和同地域的 API Key。
    base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com"
    ws_url = base_url.replace("https://", "wss://") + "/api-ws/v1/realtime"

    # 1. 声音复刻：创建专属音色
    voice = create_voice(VOICE_FILE_PATH, url=f"{base_url}/api/v1/services/audio/tts/customization")
    print(f"声音复刻完成，音色: {voice}")

    # 2. 使用复刻音色进行实时对话
    pya = pyaudio.PyAudio()
    callback = SimpleCallback(pya)
    conv = OmniRealtimeConversation(model=DEFAULT_TARGET_MODEL, callback=callback, url=ws_url)
    conv.connect()
    conv.update_session(
        output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
        voice=voice  # 使用复刻生成的专属音色
    )
    mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    print("对话已开始，对着麦克风说话 (Ctrl+C 退出)...")
    try:
        while True:
            audio_data = mic.read(3200, exception_on_overflow=False)
            conv.append_audio(base64.b64encode(audio_data).decode())
            time.sleep(0.01)
    except KeyboardInterrupt:
        conv.close()
        mic.close()
        callback.out.close()
        pya.terminate()
        print("\n对话结束")
```

Java

```
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import javax.sound.sampled.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.ByteBuffer;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class Main {
    // ===== 常量定义 =====
    // 声音复刻、实时对话要使用相同的模型
    private static final String TARGET_MODEL = "qwen3.8-omni-flash-realtime";
    private static final String PREFERRED_NAME = "guanyu";
    // 用于声音复刻的本地音频文件的相对路径
    private static final String AUDIO_FILE = "voice.mp3";
    private static final String AUDIO_MIME_TYPE = "audio/mpeg";
    // 默认示例为华北2（北京），请使用业务空间对应的 API Host 和同地域的 API Key。
    private static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com";

    // 生成 data URI
    public static String toDataUrl(String filePath) throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
    }

    // 调用 API 创建 voice
    public static String createVoice() throws Exception {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        String jsonPayload =
                "{"
                        + "\"model\": \"qwen-voice-enrollment\","
                        + "\"parameters\": {\"voice_clone_mode\": \"normal\"},"
                        + "\"input\": {"
                        +     "\"action\": \"create\","
                        +     "\"target_model\": \"" + TARGET_MODEL + "\","
                        +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                        +     "\"audio\": {"
                        +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                        +     "}"
                        + "}"
                        + "}";

        String url = BASE_URL + "/api/v1/services/audio/tts/customization";
        HttpURLConnection con = (HttpURLConnection) new URL(url).openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Authorization", "Bearer " + apiKey);
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);

        try (OutputStream os = con.getOutputStream()) {
            os.write(jsonPayload.getBytes(StandardCharsets.UTF_8));
        }

        int status = con.getResponseCode();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(),
                        StandardCharsets.UTF_8))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            if (status == 200) {
                JsonObject jsonObj = new Gson().fromJson(response.toString(), JsonObject.class);
                return jsonObj.getAsJsonObject("output").get("voice").getAsString();
            }
            throw new IOException("创建语音失败: " + status + " - " + response);
        }
    }

    // 简单的音频播放器
    static class SimpleAudioPlayer {
        private final SourceDataLine line;
        private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
        private final Thread playerThread;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);

        public SimpleAudioPlayer() throws LineUnavailableException {
            AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
            line = AudioSystem.getSourceDataLine(format);
            line.open(format);
            line.start();
            playerThread = new Thread(() -> {
                while (!shouldStop.get()) {
                    byte[] audio = audioQueue.poll();
                    if (audio != null) {
                        line.write(audio, 0, audio.length);
                    } else {
                        try { Thread.sleep(10); } catch (InterruptedException ignored) {}
                    }
                }
            }, "AudioPlayer");
            playerThread.start();
        }

        public void play(String base64Audio) {
            audioQueue.add(Base64.getDecoder().decode(base64Audio));
        }

        public void close() {
            shouldStop.set(true);
            try { playerThread.join(1000); } catch (InterruptedException ignored) {}
            line.drain();
            line.close();
        }
    }

    public static void main(String[] args) {
        try {
            // 1. 声音复刻：创建专属音色
            String voice = createVoice();
            System.out.println("声音复刻完成，音色: " + voice);

            // 2. 使用复刻音色进行实时对话
            SimpleAudioPlayer player = new SimpleAudioPlayer();
            AtomicBoolean shouldStop = new AtomicBoolean(false);

            OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model(TARGET_MODEL)
                    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                    // 若没有配置环境变量，请用百炼API Key将下行替换为：.apikey("sk-xxx")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    .url(BASE_URL.replace("https://", "wss://") + "/api-ws/v1/realtime")
                    .build();

            OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                @Override public void onOpen() { System.out.println("连接已建立"); }
                @Override public void onClose(int code, String reason) {
                    System.out.println("连接已关闭 (" + code + "): " + reason);
                    shouldStop.set(true);
                }
                @Override public void onEvent(JsonObject event) {
                    String type = event.get("type").getAsString();
                    if ("response.audio.delta".equals(type)) {
                        player.play(event.get("delta").getAsString());
                    } else if ("conversation.item.input_audio_transcription.completed".equals(type)) {
                        System.out.println("[User] " + event.get("transcript").getAsString());
                    } else if ("response.audio_transcript.done".equals(type)) {
                        System.out.println("[LLM] " + event.get("transcript").getAsString());
                    }
                }
            });

            conversation.connect();
            conversation.updateSession(OmniRealtimeConfig.builder()
                    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                    .voice(voice)  // 使用复刻生成的专属音色
                    .enableTurnDetection(true)
                    .enableInputAudioTranscription(true)
                    .build()
            );

            System.out.println("对话已开始，对着麦克风说话 (Ctrl+C 退出)...");
            AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
            TargetDataLine mic = AudioSystem.getTargetDataLine(format);
            mic.open(format);
            mic.start();

            ByteBuffer buffer = ByteBuffer.allocate(3200);
            while (!shouldStop.get()) {
                int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
                if (bytesRead > 0) {
                    conversation.appendAudio(Base64.getEncoder().encodeToString(buffer.array()));
                }
                Thread.sleep(20);
            }

            conversation.close(1000, "正常结束");
            player.close();
            mic.close();
            System.out.println("\n对话结束");
        } catch (NoApiKeyException e) {
            System.err.println("未找到API KEY: 请设置环境变量 DASHSCOPE_API_KEY");
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.exit(0);
    }
}
```

#### 非实时

适用于千问Omni系列模型，更多说明请参见[非实时（Qwen-Omni）](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)。

Python

```
# 依赖：dashscope >= 1.23.9，soundfile，numpy
import os
import requests
import base64
import pathlib
import numpy as np
import soundfile as sf
import dashscope

# ======= 常量配置 =======
DEFAULT_TARGET_MODEL = "qwen3.5-omni-plus"  # 声音复刻、非实时对话要使用相同的模型
DEFAULT_PREFERRED_NAME = "guanyu"
DEFAULT_AUDIO_MIME_TYPE = "audio/mpeg"
VOICE_FILE_PATH = "voice.mp3"  # 用于声音复刻的本地音频文件的相对路径

def create_voice(file_path: str,
                 target_model: str = DEFAULT_TARGET_MODEL,
                 preferred_name: str = DEFAULT_PREFERRED_NAME,
                 audio_mime_type: str = DEFAULT_AUDIO_MIME_TYPE) -> str:
    """
    创建音色，并返回 voice 参数
    """
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    file_path_obj = pathlib.Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:{audio_mime_type};base64,{base64_str}"

    url = dashscope.base_http_api_url + "/services/audio/tts/customization"
    payload = {
        "model": "qwen-voice-enrollment",
        "input": {
            "action": "create",
            "target_model": target_model,
            "preferred_name": preferred_name,
            "audio": {"data": data_uri}
        }
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"创建 voice 失败: {resp.status_code}, {resp.text}")

    try:
        return resp.json()["output"]["voice"]
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"解析 voice 响应失败: {e}")

if __name__ == '__main__':
    # 默认示例为华北2（北京），请使用业务空间对应的 API Host 和同地域的 API Key。
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

    # 1. 声音复刻：创建专属音色
    voice = create_voice(VOICE_FILE_PATH)
    print(f"声音复刻完成，音色: {voice}")

    # 2. 使用复刻音色进行非实时对话
    messages = [{"role": "user", "content": [{"text": "你好，请做一段自我介绍"}]}]

    response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model=DEFAULT_TARGET_MODEL,
        messages=messages,
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "wav"},  # 使用复刻生成的专属音色
        stream=True
    )

    print("模型回复：")
    audio_base64_string = ""
    for r in response:
        try:
            content = r.output.choices[0].message.content
            for item in content:
                if isinstance(item, dict):
                    if "audio" in item:
                        audio_base64_string += item["audio"].get("data", "")
                    elif "text" in item:
                        print(item["text"], end="")
        except Exception:
            pass

    if audio_base64_string:
        wav_bytes = base64.b64decode(audio_base64_string)
        audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
        sf.write("audio_cloned.wav", audio_np, samplerate=24000)
        print("\n音频文件已保存至：audio_cloned.wav")
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class Main {
    // ===== 常量定义 =====
    // 声音复刻、非实时对话要使用相同的模型
    private static final String TARGET_MODEL = "qwen3.5-omni-plus";
    private static final String PREFERRED_NAME = "guanyu";
    // 用于声音复刻的本地音频文件的相对路径
    private static final String AUDIO_FILE = "voice.mp3";
    private static final String AUDIO_MIME_TYPE = "audio/mpeg";
    // 默认示例为华北2（北京），请使用业务空间对应的 API Host 和同地域的 API Key。
    private static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com";

    // 将 PCM 数据写入标准 WAV 文件
    public static void writeWav(String path, byte[] pcmData, int sampleRate) throws IOException {
        int channels = 1, bitsPerSample = 16;
        int byteRate = sampleRate * channels * bitsPerSample / 8;
        int blockAlign = channels * bitsPerSample / 8;
        ByteBuffer header = ByteBuffer.allocate(44).order(ByteOrder.LITTLE_ENDIAN);
        header.put("RIFF".getBytes()); header.putInt(36 + pcmData.length);
        header.put("WAVE".getBytes()); header.put("fmt ".getBytes());
        header.putInt(16); header.putShort((short) 1); header.putShort((short) channels);
        header.putInt(sampleRate); header.putInt(byteRate);
        header.putShort((short) blockAlign); header.putShort((short) bitsPerSample);
        header.put("data".getBytes()); header.putInt(pcmData.length);
        try (FileOutputStream fos = new FileOutputStream(path)) {
            fos.write(header.array());
            fos.write(pcmData);
        }
    }

    // 生成 data URI
    public static String toDataUrl(String filePath) throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
    }

    // 调用 API 创建 voice
    public static String createVoice() throws Exception {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        String jsonPayload =
                "{"
                        + "\"model\": \"qwen-voice-enrollment\","
                        + "\"input\": {"
                        +     "\"action\": \"create\","
                        +     "\"target_model\": \"" + TARGET_MODEL + "\","
                        +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                        +     "\"audio\": {"
                        +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                        +     "}"
                        + "}"
                        + "}";

        String url = BASE_URL + "/api/v1/services/audio/tts/customization";
        HttpURLConnection con = (HttpURLConnection) new URL(url).openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Authorization", "Bearer " + apiKey);
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);

        try (OutputStream os = con.getOutputStream()) {
            os.write(jsonPayload.getBytes(StandardCharsets.UTF_8));
        }

        int status = con.getResponseCode();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(),
                        StandardCharsets.UTF_8))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            if (status == 200) {
                JsonObject jsonObj = new Gson().fromJson(response.toString(), JsonObject.class);
                return jsonObj.getAsJsonObject("output").get("voice").getAsString();
            }
            throw new IOException("创建语音失败: " + status + " - " + response);
        }
    }

    public static void main(String[] args) {
        try {
            // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
            String apiKey = System.getenv("DASHSCOPE_API_KEY");

            // 1. 声音复刻：创建专属音色
            String voice = createVoice();
            System.out.println("声音复刻完成，音色: " + voice);

            // 2. 使用复刻音色进行非实时对话（OpenAI 兼容接口）
            String requestBody = "{"
                    + "\"model\": \"" + TARGET_MODEL + "\","
                    + "\"messages\": [{\"role\": \"user\", \"content\": \"你好，请做一段自我介绍\"}],"
                    + "\"modalities\": [\"text\", \"audio\"],"
                    + "\"audio\": {\"voice\": \"" + voice + "\", \"format\": \"wav\"},"
                    + "\"stream\": true,"
                    + "\"stream_options\": {\"include_usage\": true}"
                    + "}";

            String url = BASE_URL + "/compatible-mode/v1/chat/completions";
            HttpURLConnection con = (HttpURLConnection) new URL(url).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            try (OutputStream os = con.getOutputStream()) {
                os.write(requestBody.getBytes(StandardCharsets.UTF_8));
            }

            // 3. 解析流式 SSE 响应
            StringBuilder audioBase64 = new StringBuilder();
            System.out.println("模型回复：");

            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(con.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = br.readLine()) != null) {
                    if (!line.startsWith("data: ") || line.equals("data: [DONE]")) continue;
                    String json = line.substring(6);
                    JsonObject chunk = new Gson().fromJson(json, JsonObject.class);
                    if (!chunk.has("choices") || chunk.getAsJsonArray("choices").size() == 0) continue;

                    JsonObject delta = chunk.getAsJsonArray("choices").get(0)
                            .getAsJsonObject().getAsJsonObject("delta");
                    if (delta.has("content") && !delta.get("content").isJsonNull()) {
                        System.out.print(delta.get("content").getAsString());
                    }
                    if (delta.has("audio") && !delta.get("audio").isJsonNull()) {
                        JsonObject audio = delta.getAsJsonObject("audio");
                        if (audio.has("data")) {
                            audioBase64.append(audio.get("data").getAsString());
                        }
                    }
                }
            }

            // 4. 保存音频文件（API 返回原始 PCM 数据，需添加 WAV 头）
            if (audioBase64.length() > 0) {
                byte[] pcmBytes = Base64.getDecoder().decode(audioBase64.toString());
                writeWav("audio_cloned.wav", pcmBytes, 24000);
                System.out.println("\n音频文件已保存至：audio_cloned.wav");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 对话使用

如何使用声音复刻生成的专属音色进行对话，请参见[快速开始：复刻与使用音色](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#bb60d81324wsu)。

## 音色配额与自动清理规则

-   **总数限制**：1000个音色/账号
    
    > 当前接口不提供音色数量查询功能，可通过调用[查询音色列表](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#401d33226330i)接口自行统计音色数目
    
-   **自动清理**：若单个音色在过去一年内未被用于任何模型调用请求，系统将自动将其删除
    

## 计费说明

声音复刻和模型调用分开计费：

-   声音复刻：[创建音色](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#1eaa57d82did9)按0.01 元/个计费，创建失败不计费
    
    **说明**免费额度说明（仅中国站北京地域和国际站新加坡地域有免费额度）：
    
    -   阿里云百炼开通后90天内，可享1000次免费音色创建机会。
    -   创建失败不占用免费次数。
    -   删除音色不会恢复免费次数。
    -   免费额度用完或超出 90 天有效期后，创建音色将按0.01 元/个的价格计费。
    
-   使用复刻生成的专属音色进行对话：按模型调用的 token 用量计费，详情请参见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)
    

## 版权与合法性

您需对所提供声音的所有权及合法使用权负责，请注意阅读[服务协议](https://terms.alicdn.com/legal-agreement/terms/b_platform_service_agreement/20240229113512917/20240229113512917.html)。

## 录音操作指南

### 录音设备

推荐使用具备降噪功能的麦克风，或在安静环境下使用手机近距离录音，以保证音源纯净。

### 录音环境

#### 场地

-   建议在 10 平方米以内的小型封闭空间录音。
-   优先选择配有吸音材料（如吸音棉、地毯、窗帘）的房间。
-   避免空旷大厅、会议室、教室等高混响场所。

#### 噪音控制

-   室外噪音：关闭门窗，避免交通、施工等干扰。
-   室内噪音：关闭空调、风扇、日光灯镇流器等设备；可通过手机录制环境音并放大播放，识别潜在噪音源。

#### 混响控制

-   混响会导致声音模糊、清晰度下降。
-   减少光滑表面反射：拉上窗帘、打开衣柜门、铺放衣物或床单覆盖桌面/柜面。
-   利用不规则物体（如书架、软包家具）实现声波漫反射。

### 录音文案

-   文案内容灵活，建议与目标应用场景一致（例如，若用于客服场景，文案应为客服对话风格），但必须确保不包含任何敏感或非法词汇（如政治、色情、暴力相关内容），否则会导致复刻失败。
-   避免短句（如“你好”、“是的”），应使用完整句子。
-   保持语义连贯，朗读时避免频繁停顿（建议至少连续 3 秒无中断）。
-   可带入目标情绪（如亲切、严肃），但需避免过度夸张的戏剧化朗读，保持语调自然。

### 操作建议

以普通卧室为例：

1.  关闭门窗，隔绝外部噪音。
2.  关闭空调、电扇等电器。
3.  拉上窗帘，减少玻璃反射。
4.  在桌面铺放衣物或毛毯，降低桌面反射。
5.  提前熟悉文案，设定角色语气，自然演绎。
6.  与录音设备保持约 10 厘米距离，避免喷麦或信号过弱。

## 错误信息

如遇报错问题，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

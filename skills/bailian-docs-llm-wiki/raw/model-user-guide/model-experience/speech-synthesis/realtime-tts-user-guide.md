# 实时语音合成

实时语音合成将文本实时转换为自然语音，支持流式输入与输出，具备声音复刻、声音设计及精细化音频控制能力，适用于语音助手、有声读物、智能客服等场景。

## 概述

实现低延迟文本到语音转换。

-   支持流式输入与输出，首包延迟低
-   可调节语速、语调、音量与码率，实现精细的语音效果控制
-   兼容主流音频格式（PCM、WAV、MP3、Opus），最高支持 48kHz 采样率输出
-   支持[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)，可通过自然语言指令控制语音表现力
-   支持[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)与[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)音色定制
-   支持[情感与富语言标签](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#rt_emtag_h3)，可在文本中嵌入标签控制情感表达或插入拟声效果

批量场景（有声读物、课件配音等）可使用[非实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/non-realtime-tts-user-guide.md)。各模型选型建议请参见[语音合成](raw/model-user-guide/model-experience/speech-synthesis/tts-model.md)。

**说明**Sambert 为早期语音合成模型，新项目建议优先使用 CosyVoice 或 Qwen-Audio-TTS，可获得更好的合成效果和更丰富的功能支持。

## 前提条件

-   已[配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并将其[设置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   如果通过 DashScope SDK 调用，需要[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。
-   如果通过 AOQ 协议接入 CosyVoice 系列模型，需要下载并集成 AOQ 客户端 SDK，详见[AOQ SDK 简介](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)。

## 快速开始

以下是各模型的语音合成示例。更多示例和参数说明请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### Qwen-Audio-TTS

以下示例演示如何使用系统音色进行语音合成。

如需使用[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)功能，请通过 `instruction` 参数设置指令。

Python

```
# coding=utf-8

import os
import dashscope
from dashscope.audio.tts_v2 import *

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

# 模型
# qwen-audio-3.0-tts-flash/qwen-audio-3.0-tts-plus：使用longanhuan_v3.6等音色。
# 不同语言选择对应音色
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("今天天气怎么样？")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

Java

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
    // qwen-audio-3.0-tts-flash/qwen-audio-3.0-tts-plus：使用longanhuan_v3.6等音色。
    // 每个音色支持的语言不同，合成日语、韩语等非中文语言时，需选择支持对应语言的音色。详见音色列表。
    private static String model = "qwen-audio-3.0-tts-flash";
    // 音色
    private static String voice = "longanhuan_v3.6";

    public static void streamAudioDataToSpeaker() {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
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
            // 注意：getFirstPackageDelay() 需要 dashscope-sdk-java 2.18.0 及以上版本
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

#### CosyVoice

该模型除 WebSocket 协议外，还支持通过 AOQ 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见[模型/应用支持力度](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。

**重要**`cosyvoice-v3.5-plus` 和 `cosyvoice-v3.5-flash` 仅在北京地域可用，且仅支持声音设计和声音复刻场景（无系统音色）。使用前需先通过[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)或[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)创建音色，然后在代码中将 `voice` 设为音色 ID、`model` 设为对应模型名称。

以下示例演示如何使用系统音色（参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)）进行语音合成。

如需使用[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)功能，请通过 `instruction` 参数设置指令。

Python

```
# coding=utf-8

import os
import dashscope
from dashscope.audio.tts_v2 import *

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

# 模型
# 不同模型版本需要使用对应版本的音色：
# cosyvoice-v3-flash/cosyvoice-v3-plus：使用longanyang等音色。
# cosyvoice-v2：使用longxiaochun_v2等音色。
# 不同语言选择对应音色
model = "cosyvoice-v3-flash"
# 音色
voice = "longanyang"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("今天天气怎么样？")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

Java

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
    // 不同模型版本需要使用对应版本的音色：
    // cosyvoice-v3-flash/cosyvoice-v3-plus：使用longanyang等音色。
    // cosyvoice-v2：使用longxiaochun_v2等音色。
    // 每个音色支持的语言不同，合成日语、韩语等非中文语言时，需选择支持对应语言的音色。详见CosyVoice音色列表。
    private static String model = "cosyvoice-v3-flash";
    // 音色
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
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
            // 注意：getFirstPackageDelay() 需要 dashscope-sdk-java 2.18.0 及以上版本
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

## 进阶功能

### 指令控制

指令控制通过自然语言描述控制语音的音调、语速、情感和音色特点，无需调整复杂的音频参数。

**各模型指令规格**：

#### Qwen-Audio-TTS

**支持的模型**：`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`

系统音色和声音复刻音色：均可输入任意指令。

#### CosyVoice

**支持的模型**：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`

不同模型对指令的格式要求不同：

-   `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`：
    
    -   声音复刻/设计音色：可输入任意指令。
    -   系统音色：v3.5不支持系统音色。
-   `cosyvoice-v3-plus`：
    
    -   声音复刻/设计音色：不支持指令控制。
    -   系统音色：指令必须使用固定格式和内容，参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。
-   `cosyvoice-v3-flash`：
    
    -   声音复刻/设计音色：可输入任意指令。
    -   系统音色：指令必须使用固定格式和内容，参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。

**使用方式**：通过 `instruction` 参数指定指令内容。

**指令文本支持的语言**：

-   `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`：
    
    -   声音复刻/设计音色：中文、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语。
    -   系统音色：v3.5不支持系统音色。
-   `cosyvoice-v3-plus`：
    
    -   声音复刻/设计音色：中文、英文、法语、德语、日语、韩语、俄语。
    -   系统音色：指令必须使用固定格式和内容，参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。
-   `cosyvoice-v3-flash`：
    
    -   声音复刻/设计音色：中文、英文、法语、德语、日语、韩语、俄语。
    -   系统音色：中文。

**指令文本长度限制**：不超过 100 字符。汉字（包括简体/繁体汉字、日文汉字和韩文汉字）按 2 个字符计算，其他字符（如标点符号、字母、数字、日韩文假名/谚文等）按 1 个字符计算。

#### Qwen-TTS

**支持的模型**：仅支持Qwen3-TTS-Instruct-Flash-Realtime系列模型。

**使用方式**：通过 `instructions` 参数指定指令内容。

**指令文本支持的语言**：仅支持中文和英文。

**指令文本长度限制**：不超过 1600 Token。

**适用场景**：

-   有声书和广播剧配音
-   广告和宣传片配音
-   游戏角色和动画配音
-   情感化的智能语音助手
-   纪录片和新闻播报

**如何编写高质量的声音描述**：

-   **核心原则**：
    
    1.  **具体而非模糊**：使用描绘声音特质的词语，如“低沉”、“清脆”、“语速偏快”，避免“好听”、“普通”等主观或模糊的表述。
    2.  **多维而非单一**：好的描述通常涵盖多个维度（如性别、年龄、情感等）。仅写“女声”过于宽泛，难以生成有特色的音色。
    3.  **客观而非主观**：聚焦声音的物理和感知特征。例如，用”音调偏高，带有活力“代替”我最喜欢的声音”。
    4.  **原创而非模仿**：描述声音的特质，而非要求模仿特定人物（如名人、演员）。模型不支持模仿，且可能涉及版权风险。
    5.  **简洁而非冗余**：确保每个词都有明确作用，避免重复的同义词或无意义的修饰。
-   **描述维度参考**：
    
    建议组合以下维度描述声音，维度越丰富，生成效果越精准。
    

**维度**

**描述示例**

性别

男性、女性、中性

年龄

儿童（5-12 岁）、青少年（13-18 岁）、青年（19-35 岁）、中年（36-55 岁）、老年（55 岁以上）

音调

高音、中音、低音、偏高、偏低

语速

快速、中速、缓慢、偏快、偏慢

情感

开朗、沉稳、温柔、严肃、活泼、冷静、治愈

特点

有磁性、清脆、沙哑、圆润、甜美、浑厚、有力

用途

新闻播报、广告配音、有声书、动画角色、语音助手、纪录片解说

-   **示例**：
    
    -   标准播音风格：吐字清晰精准，字正腔圆
    -   年轻活泼的女性声音，语速较快，带有明显的上扬语调，适合介绍时尚产品
    -   沉稳的中年男性，语速缓慢，音色低沉有磁性，适合朗读新闻或纪录片解说
    -   温柔知性的女性，30 岁左右，语调平和，适合有声书朗读
    -   可爱的儿童声音，大约 8 岁女孩，说话略带稚气，适合动画角色配音

### 方言

本节介绍如何让模型用**中文方言**（如河南话、四川话、粤语等）输出语音。不同模型和音色类型的设置方式不同。

**各模型方言设置方式**：

#### Qwen-Audio-TTS

-   **系统音色**：在[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)中选择以下任一种音色：
    
    -   支持方言的系统音色，无需额外设置即可输出对应方言。
    -   支持[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)且可指定方言的音色，通过指令文本指定方言。
-   **声音复刻音色**：通过[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)功能设置，例如指令文本写 `请用河南话表达`。
    

**具体支持哪些方言**：参见[Qwen-Audio-TTS](https://help.aliyun.com/zh/model-studio/tts-model#qat_all01)中各模型“支持的语言”。

#### CosyVoice

-   **系统音色**：在[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中选择以下任一种音色：
    
    -   支持方言的系统音色（例如 `longshange_v3`），无需额外设置即可输出对应方言。
    -   支持[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)且可指定方言的音色（例如 `longanhuan_v3`），通过指令文本指定方言。
-   **声音复刻音色**：通过[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)功能设置，例如指令文本写 `请用河南话表达`。
    
-   **声音设计音色**：暂不支持方言。
    

**具体支持哪些方言**：参见[CosyVoice](https://help.aliyun.com/zh/model-studio/tts-model#tts08_cosy02)中各模型“支持的语言”。

**示例**：以 `cosyvoice-v3-flash` + `longanhuan_v3` 音色，通过指令文本 `"请用河南话表达。"` 输出河南话语音。

```
# coding=utf-8

import os
import dashscope
from dashscope.audio.tts_v2 import *

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

# 模型
# 不同模型版本需要使用对应版本的音色：
# cosyvoice-v3-flash/cosyvoice-v3-plus：使用longanyang等音色。
# cosyvoice-v2：使用longxiaochun_v2等音色。
# 不同语言选择对应音色
model = "cosyvoice-v3-flash"
# 音色
voice = "longanhuan_v3"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice, instruction="请用河南话表达。")
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("叫你去买盐，你买回来一袋面，这不是弄啥嘞吗！")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

#### Qwen-TTS

-   **系统音色**：使用支持方言的系统音色，参见[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)中的 Qwen-TTS音色列表。
-   **声音复刻音色**：不支持方言。
-   **声音设计音色**：不支持方言。

**具体支持哪些方言**：参见[Qwen3-TTS](https://help.aliyun.com/zh/model-studio/tts-model#tts08_q3tts02)中各模型“支持的语言”。

### 情感与富语言标签

Qwen-Audio-TTS 系列模型支持在待合成文本（`text` 参数）中直接嵌入情感与富语言标签，用于控制语音的情感表达或在指定位置插入拟声效果（如笑声、叹息等），无需调整复杂的音频参数即可生成更具表现力的语音。

**重要****支持的模型**：仅 `qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash`。

**限制**：仅支持单向流式模式。

**控制类标签**

控制类标签用于设定语音的情感或风格。将标签写在文本中，标签会作用于其后的所有文本，直到遇到下一个控制类标签，或因句子较长被自动切分为止。

**标签**

**说明**

`[sad]`

悲伤

`[amazed]`

惊叹

`[deep and loud shouting]`

深沉大声呐喊

`[trembling]`

颤抖

`[angry]`

愤怒

`[excited]`

兴奋

`[sarcastic]`

讽刺

`[curious]`

好奇

`[like dracula]`

德古拉风格（低沉、阴森）

`[bored]`

无聊

`[tired]`

疲惫

`[scornful]`

轻蔑

`[shouting]`

大喊

`[asmr]`

ASMR 轻柔耳语

`[panicked]`

恐慌

`[mischievously]`

调皮

`[empathetic]`

共情

`[whispers]`

耳语

`[reluctantly]`

不情愿

`[crying]`

哭泣

`[serious]`

严肃

`[very slowly]`

非常缓慢地说话

`[very fast]`

非常快速地说话

**富语言类标签**

富语言类标签用于在文本的当前位置插入一段拟声效果，不影响前后文本的情感风格。

**标签**

**说明**

`[gasp]`

倒吸一口气

`[sighing]`

叹息

`[clears throat]`

清嗓

`[giggles]`

咯咯笑

`[laughing]`

大笑

`[cough]`

咳嗽

`[snorts]`

哼声、嗤笑

**使用示例**

以下示例展示如何在 `text` 参数中组合使用控制类标签和富语言类标签：

`[excited]今天的天气真不错！[laughing]我们一起出去玩吧！`

上述文本中，`[excited]` 是控制类标签，作用于其后的所有文本，使语音带有兴奋的情感；`[laughing]` 是富语言类标签，在该位置插入一段笑声效果后继续合成后续文本。

您也可以在同一段文本中切换不同情感：

`[serious]请注意安全事项。[excited]好了，现在让我们开始吧！`

其中 `[serious]` 控制第一句为严肃语气，`[excited]` 从第二句起切换为兴奋语气。

### 取消任务

在实时语音合成过程中，如果需要中断当前轮次合成，可以发送取消指令。取消后服务端会立即结束当前任务并返回结束事件，您可在当前 WebSocket 连接上继续发起新的合成任务，无需重新建立连接。

**使用方式**：

-   **Python SDK**：1.26.4 及以上版本，调用 `SpeechSynthesizer.streaming_cancel()`。
-   **Java SDK**：2.22.26 及以上版本，调用 `SpeechSynthesizer.streamingCancel()`。
-   **WebSocket 原始协议**：发送 `finish-task` 事件，并在 `input` 中设置 `directive=cancel`。

**重要****模型限制**：

-   华北2（北京）地域：Qwen-Audio-TTS 系列模型的所有模型都支持该功能；CosyVoice 系列模型仅 v2 及以上版本支持该功能。
-   新加坡地域：Qwen-Audio-TTS 系列模型的所有模型都支持该功能；CosyVoice 系列模型不支持该功能。

### WebSocket 原始协议调用

以下示例展示如何通过 WebSocket 原始协议直连服务端，适用于不使用 DashScope SDK 的场景。此为最小可运行实现，WebSocket 协议请参见各模型的 API 参考。

点击查看 WebSocket 原始协议调用示例

#### Qwen-Audio-TTS/CosyVoice

Qwen-Audio-TTS 和 CosyVoice 使用相同的 WebSocket 协议，只需替换 `model` 和 `voice` 参数。以下示例以 `qwen-audio-3.0-tts-flash` 为例，使用 CosyVoice 时将 model 替换为 `cosyvoice-v3-flash` 等，voice 替换为对应音色即可。

#### Go

```
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

const (
	// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
	wsURL      = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"
	outputFile = "output.mp3"
)

func main() {
	// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
	// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
	apiKey := os.Getenv("DASHSCOPE_API_KEY")

	// 清空输出文件
	os.Remove(outputFile)
	os.Create(outputFile)

	// 连接WebSocket
	header := make(http.Header)
	header.Add("X-DashScope-DataInspection", "enable")
	header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))

	conn, resp, err := websocket.DefaultDialer.Dial(wsURL, header)
	if err != nil {
		if resp != nil {
			fmt.Printf("连接失败 HTTP状态码: %d\n", resp.StatusCode)
		}
		fmt.Println("连接失败:", err)
		return
	}
	defer conn.Close()

	// 生成任务ID
	taskID := uuid.New().String()
	fmt.Printf("生成任务ID: %s\n", taskID)

	// 发送run-task事件
	runTaskCmd := map[string]interface{}{
		"header": map[string]interface{}{
			"action":    "run-task",
			"task_id":   taskID,
			"streaming": "duplex",
		},
		"payload": map[string]interface{}{
			"task_group": "audio",
			"task":       "tts",
			"function":   "SpeechSynthesizer",
			"model":      "qwen-audio-3.0-tts-flash",
			"parameters": map[string]interface{}{
				"text_type":   "PlainText",
				"voice":       "longanhuan_v3.6",
				"format":      "mp3",
				"sample_rate": 22050,
				"volume":      50,
				"rate":        1,
				"pitch":       1,
				// 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
				"enable_ssml": false,
			},
			"input": map[string]interface{}{},
		},
	}

	runTaskJSON, _ := json.Marshal(runTaskCmd)
	fmt.Printf("发送run-task事件: %s\n", string(runTaskJSON))

	err = conn.WriteMessage(websocket.TextMessage, runTaskJSON)
	if err != nil {
		fmt.Println("发送run-task失败:", err)
		return
	}

	textSent := false

	// 处理消息
	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("读取消息失败:", err)
			break
		}

		// 处理二进制消息
		if messageType == websocket.BinaryMessage {
			fmt.Printf("收到二进制消息，长度: %d\n", len(message))
			file, _ := os.OpenFile(outputFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
			file.Write(message)
			file.Close()
			continue
		}

		// 处理文本消息
		messageStr := string(message)
		fmt.Printf("收到文本消息: %s\n", strings.ReplaceAll(messageStr, "\n", ""))

		// 简单解析JSON获取event类型
		var msgMap map[string]interface{}
		if json.Unmarshal(message, &msgMap) == nil {
			if header, ok := msgMap["header"].(map[string]interface{}); ok {
				if event, ok := header["event"].(string); ok {
					fmt.Printf("事件类型: %s\n", event)

					switch event {
					case "task-started":
						fmt.Println("=== 收到task-started事件 ===")

						if !textSent {
							// 发送continue-task事件

							texts := []string{"床前明月光，疑是地上霜。", "举头望明月，低头思故乡。"}

							for _, text := range texts {
								continueTaskCmd := map[string]interface{}{
									"header": map[string]interface{}{
										"action":    "continue-task",
										"task_id":   taskID,
										"streaming": "duplex",
									},
									"payload": map[string]interface{}{
										"input": map[string]interface{}{
											"text": text,
										},
									},
								}

								continueTaskJSON, _ := json.Marshal(continueTaskCmd)
								fmt.Printf("发送continue-task事件: %s\n", string(continueTaskJSON))

								err = conn.WriteMessage(websocket.TextMessage, continueTaskJSON)
								if err != nil {
									fmt.Println("发送continue-task失败:", err)
									return
								}
							}

							textSent = true

							// 延迟发送finish-task
							time.Sleep(500 * time.Millisecond)

							// 发送finish-task事件
							finishTaskCmd := map[string]interface{}{
								"header": map[string]interface{}{
									"action":    "finish-task",
									"task_id":   taskID,
									"streaming": "duplex",
								},
								"payload": map[string]interface{}{
									"input": map[string]interface{}{},
								},
							}

							finishTaskJSON, _ := json.Marshal(finishTaskCmd)
							fmt.Printf("发送finish-task事件: %s\n", string(finishTaskJSON))

							err = conn.WriteMessage(websocket.TextMessage, finishTaskJSON)
							if err != nil {
								fmt.Println("发送finish-task失败:", err)
								return
							}
						}

					case "task-finished":
						fmt.Println("=== 任务完成 ===")
						return

					case "task-failed":
						fmt.Println("=== 任务失败 ===")
						if header["error_message"] != nil {
							fmt.Printf("错误信息: %s\n", header["error_message"])
						}
						return

					case "result-generated":
						fmt.Println("收到result-generated事件")
					}
				}
			}
		}
	}
}
```

#### C#

```
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

class Program {
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static readonly string ApiKey = "sk-xxx"
    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    private const string WebSocketUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
    // 输出文件路径
    private const string OutputFilePath = "output.mp3";

    // WebSocket客户端
    private static ClientWebSocket _webSocket = new ClientWebSocket();
    // 取消令牌源
    private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
    // 任务ID
    private static string? _taskId;
    // 任务是否已启动
    private static TaskCompletionSource<bool> _taskStartedTcs = new TaskCompletionSource<bool>();

    static async Task Main(string[] args) {
        try {
            // 清空输出文件
            ClearOutputFile(OutputFilePath);

            // 连接WebSocket服务
            await ConnectToWebSocketAsync(WebSocketUrl);

            // 启动接收消息的任务
            Task receiveTask = ReceiveMessagesAsync();

            // 发送run-task事件
            _taskId = GenerateTaskId();
            await SendRunTaskCommandAsync(_taskId);

            // 等待task-started事件
            await _taskStartedTcs.Task;

            // 持续发送continue-task事件
            string[] texts = {
                "床前明月光",
                "疑是地上霜",
                "举头望明月",
                "低头思故乡"
            };
            foreach (string text in texts) {
                await SendContinueTaskCommandAsync(text);
            }

            // 发送finish-task事件
            await SendFinishTaskCommandAsync(_taskId);

            // 等待接收任务完成
            await receiveTask;

            Console.WriteLine("任务完成，连接已关闭。");
        } catch (OperationCanceledException) {
            Console.WriteLine("任务被取消。");
        } catch (Exception ex) {
            Console.WriteLine($"发生错误：{ex.Message}");
        } finally {
            _cancellationTokenSource.Cancel();
            _webSocket.Dispose();
        }
    }

    private static void ClearOutputFile(string filePath) {
        if (File.Exists(filePath)) {
            File.WriteAllText(filePath, string.Empty);
            Console.WriteLine("输出文件已清空。");
        } else {
            Console.WriteLine("输出文件不存在，无需清空。");
        }
    }

    private static async Task ConnectToWebSocketAsync(string url) {
        var uri = new Uri(url);
        if (_webSocket.State == WebSocketState.Connecting || _webSocket.State == WebSocketState.Open) {
            return;
        }

        // 设置WebSocket连接的头部信息
        _webSocket.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
        _webSocket.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");

        try {
            await _webSocket.ConnectAsync(uri, _cancellationTokenSource.Token);
            Console.WriteLine("已成功连接到WebSocket服务。");
        } catch (OperationCanceledException) {
            Console.WriteLine("WebSocket连接被取消。");
        } catch (Exception ex) {
            Console.WriteLine($"WebSocket连接失败: {ex.Message}");
            throw;
        }
    }

    private static async Task SendRunTaskCommandAsync(string taskId) {
        var command = CreateCommand("run-task", taskId, "duplex", new {
            task_group = "audio",
            task = "tts",
            function = "SpeechSynthesizer",
            model = "qwen-audio-3.0-tts-flash",
            parameters = new
            {
                text_type = "PlainText",
                voice = "longanhuan_v3.6",
                format = "mp3",
                sample_rate = 22050,
                volume = 50,
                rate = 1,
                pitch = 1,
                // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                enable_ssml = false
            },
            input = new { }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("已发送run-task事件。");
    }

    private static async Task SendContinueTaskCommandAsync(string text) {
        if (_taskId == null) {
            throw new InvalidOperationException("任务ID未初始化。");
        }

        var command = CreateCommand("continue-task", _taskId, "duplex", new {
            input = new {
                text
            }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("已发送continue-task事件。");
    }

    private static async Task SendFinishTaskCommandAsync(string taskId) {
        var command = CreateCommand("finish-task", taskId, "duplex", new {
            input = new { }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("已发送finish-task事件。");
    }

    private static async Task SendJsonMessageAsync(string message) {
        var buffer = Encoding.UTF8.GetBytes(message);
        try {
            await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
        } catch (OperationCanceledException) {
            Console.WriteLine("消息发送被取消。");
        }
    }

    private static async Task ReceiveMessagesAsync() {
        while (_webSocket.State == WebSocketState.Open) {
            var response = await ReceiveMessageAsync();
            if (response != null) {
                var eventStr = response.RootElement.GetProperty("header").GetProperty("event").GetString();
                switch (eventStr) {
                    case "task-started":
                        Console.WriteLine("任务已启动。");
                        _taskStartedTcs.TrySetResult(true);
                        break;
                    case "task-finished":
                        Console.WriteLine("任务已完成。");
                        _cancellationTokenSource.Cancel();
                        break;
                    case "task-failed":
                        Console.WriteLine("任务失败：" + response.RootElement.GetProperty("header").GetProperty("error_message").GetString());
                        _cancellationTokenSource.Cancel();
                        break;
                    default:
                        // result-generated可在此处理
                        break;
                }
            }
        }
    }

    private static async Task<JsonDocument?> ReceiveMessageAsync() {
        var buffer = new byte[1024 * 4];
        var segment = new ArraySegment<byte>(buffer);

        try {
            WebSocketReceiveResult result = await _webSocket.ReceiveAsync(segment, _cancellationTokenSource.Token);

            if (result.MessageType == WebSocketMessageType.Close) {
                await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cancellationTokenSource.Token);
                return null;
            }

            if (result.MessageType == WebSocketMessageType.Binary) {
                // 处理二进制数据
                Console.WriteLine("接收到二进制数据...");

                // 将二进制数据保存到文件
                using (var fileStream = new FileStream(OutputFilePath, FileMode.Append)) {
                    fileStream.Write(buffer, 0, result.Count);
                }

                return null;
            }

            string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
            return JsonDocument.Parse(message);
        } catch (OperationCanceledException) {
            Console.WriteLine("消息接收被取消。");
            return null;
        }
    }

    private static string GenerateTaskId() {
        return Guid.NewGuid().ToString("N").Substring(0, 32);
    }

    private static string CreateCommand(string action, string taskId, string streaming, object payload) {
        var command = new {
            header = new {
                action,
                task_id = taskId,
                streaming
            },
            payload
        };

        return JsonSerializer.Serialize(command);
    }
}
```

#### PHP

示例代码目录结构为：

my-php-project/

├── composer.json

├── vendor/

└── index.php

composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

```
{
    "require": {
        "react/event-loop": "^1.3",
        "react/socket": "^1.11",
        "react/stream": "^1.2",
        "react/http": "^1.1",
        "ratchet/pawl": "^0.4"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

index.php内容如下：

```
<?php

require __DIR__ . '/vendor/autoload.php';

use Ratchet\Client\Connector;
use React\EventLoop\Loop;
use React\Socket\Connector as SocketConnector;

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$api_key = "sk-xxx"
$api_key = getenv("DASHSCOPE_API_KEY");
// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
$websocket_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
$output_file = 'output.mp3'; // 输出文件路径

$loop = Loop::get();

if (file_exists($output_file)) {
    // 清空文件内容
    file_put_contents($output_file, '');
}

// 创建自定义的连接器
$socketConnector = new SocketConnector($loop, [
    'tcp' => [
        'bindto' => '0.0.0.0:0',
    ],
    // 警告：关闭 TLS 证书校验存在中间人攻击风险，仅限本地调试；生产环境务必将 verify_peer/verify_peer_name 设为 true
    'tls' => [
        'verify_peer' => false,
        'verify_peer_name' => false,
    ],
]);

$connector = new Connector($loop, $socketConnector);

$headers = [
    'Authorization' => 'bearer ' . $api_key,
    'X-DashScope-DataInspection' => 'enable'
];

$connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $output_file) {
    echo "连接到WebSocket服务器\n";

    // 生成任务ID
    $taskId = generateTaskId();

    // 发送 run-task 事件
    sendRunTaskMessage($conn, $taskId);

    // 定义发送 continue-task 事件的函数
    $sendContinueTask = function() use ($conn, $loop, $taskId) {
        // 待发送的文本
        $texts = ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"];
        $continueTaskCount = 0;
        foreach ($texts as $text) {
            $continueTaskMessage = json_encode([
                "header" => [
                    "action" => "continue-task",
                    "task_id" => $taskId,
                    "streaming" => "duplex"
                ],
                "payload" => [
                    "input" => [
                        "text" => $text
                    ]
                ]
            ]);
            echo "准备发送continue-task事件: " . $continueTaskMessage . "\n";
            $conn->send($continueTaskMessage);
            $continueTaskCount++;
        }
        echo "发送的continue-task事件个数为：" . $continueTaskCount . "\n";

        // 发送 finish-task 事件
        sendFinishTaskMessage($conn, $taskId);
    };

    // 标记是否收到 task-started 事件
    $taskStarted = false;

    // 监听消息
    $conn->on('message', function($msg) use ($conn, $sendContinueTask, $loop, &$taskStarted, $taskId, $output_file) {
        if ($msg->isBinary()) {
            // 写入二进制数据到本地文件
            file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
        } else {
            // 处理非二进制消息
            $response = json_decode($msg, true);

            if (isset($response['header']['event'])) {
                handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, $taskStarted);
            } else {
                echo "未知的消息格式\n";
            }
        }
    });

    // 监听连接关闭
    $conn->on('close', function($code = null, $reason = null) {
        echo "连接已关闭\n";
        if ($code !== null) {
            echo "关闭代码: " . $code . "\n";
        }
        if ($reason !== null) {
            echo "关闭原因：" . $reason . "\n";
        }
    });
}, function ($e) {
    echo "无法连接：{$e->getMessage()}\n";
});

$loop->run();

/**
 * 生成任务ID
 * @return string
 */
function generateTaskId(): string {
    return bin2hex(random_bytes(16));
}

/**
 * 发送 run-task 事件
 * @param $conn
 * @param $taskId
 */
function sendRunTaskMessage($conn, $taskId) {
    $runTaskMessage = json_encode([
        "header" => [
            "action" => "run-task",
            "task_id" => $taskId,
            "streaming" => "duplex"
        ],
        "payload" => [
            "task_group" => "audio",
            "task" => "tts",
            "function" => "SpeechSynthesizer",
            "model" => "qwen-audio-3.0-tts-flash",
            "parameters" => [
                "text_type" => "PlainText",
                "voice" => "longanhuan_v3.6",
                "format" => "mp3",
                "sample_rate" => 22050,
                "volume" => 50,
                "rate" => 1,
                "pitch" => 1,
                // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                "enable_ssml" => false
            ],
            "input" => (object) []
        ]
    ]);
    echo "准备发送run-task事件: " . $runTaskMessage . "\n";
    $conn->send($runTaskMessage);
    echo "run-task事件已发送\n";
}

/**
 * 读取音频文件
 * @param string $filePath
 * @return bool|string
 */
function readAudioFile(string $filePath) {
    $voiceData = file_get_contents($filePath);
    if ($voiceData === false) {
        echo "无法读取音频文件\n";
    }
    return $voiceData;
}

/**
 * 分割音频数据
 * @param string $data
 * @param int $chunkSize
 * @return array
 */
function splitAudioData(string $data, int $chunkSize): array {
    return str_split($data, $chunkSize);
}

/**
 * 发送 finish-task 事件
 * @param $conn
 * @param $taskId
 */
function sendFinishTaskMessage($conn, $taskId) {
    $finishTaskMessage = json_encode([
        "header" => [
            "action" => "finish-task",
            "task_id" => $taskId,
            "streaming" => "duplex"
        ],
        "payload" => [
            "input" => (object) []
        ]
    ]);
    echo "准备发送finish-task事件: " . $finishTaskMessage . "\n";
    $conn->send($finishTaskMessage);
    echo "finish-task事件已发送\n";
}

/**
 * 处理事件
 * @param $conn
 * @param $response
 * @param $sendContinueTask
 * @param $loop
 * @param $taskId
 * @param $taskStarted
 */
function handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, &$taskStarted) {
    switch ($response['header']['event']) {
        case 'task-started':
            echo "任务开始，发送continue-task事件...\n";
            $taskStarted = true;
            // 发送 continue-task 事件
            $sendContinueTask();
            break;
        case 'result-generated':
            // 收到result-generated事件
            break;
        case 'task-finished':
            echo "任务完成\n";
            $conn->close();
            break;
        case 'task-failed':
            echo "任务失败\n";
            echo "错误代码：" . $response['header']['error_code'] . "\n";
            echo "错误信息：" . $response['header']['error_message'] . "\n";
            $conn->close();
            break;
        case 'error':
            echo "错误：" . $response['payload']['message'] . "\n";
            break;
        default:
            echo "未知事件：" . $response['header']['event'] . "\n";
            break;
    }

    // 如果任务已完成，关闭连接
    if ($response['header']['event'] == 'task-finished') {
        // 等待1秒以确保所有数据都已传输完毕
        $loop->addTimer(1, function() use ($conn) {
            $conn->close();
            echo "客户端关闭连接\n";
        });
    }

    // 如果没有收到 task-started 事件，关闭连接
    if (!$taskStarted && in_array($response['header']['event'], ['task-failed', 'error'])) {
        $conn->close();
    }
}
```

#### Node.js

需安装相关依赖：

```
npm install ws
npm install uuid
```

示例代码如下：

```
const WebSocket = require('ws');
const fs = require('fs');
const uuid = require('uuid').v4;

// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：const apiKey = "sk-xxx"
const apiKey = process.env.DASHSCOPE_API_KEY;
// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
const url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference';
// 输出文件路径
const outputFilePath = 'output.mp3';

// 清空输出文件
fs.writeFileSync(outputFilePath, '');

// 创建WebSocket客户端
const ws = new WebSocket(url, {
  headers: {
    Authorization: `bearer ${apiKey}`,
    'X-DashScope-DataInspection': 'enable'
  }
});

let taskStarted = false;
let taskId = uuid();

ws.on('open', () => {
  console.log('已连接到WebSocket服务器');

  // 发送run-task事件
  const runTaskMessage = JSON.stringify({
    header: {
      action: 'run-task',
      task_id: taskId,
      streaming: 'duplex'
    },
    payload: {
      task_group: 'audio',
      task: 'tts',
      function: 'SpeechSynthesizer',
      model: 'qwen-audio-3.0-tts-flash',
      parameters: {
        text_type: 'PlainText',
        voice: 'longanhuan_v3.6', // 音色
        format: 'mp3', // 音频格式
        sample_rate: 22050, // 采样率
        volume: 50, // 音量
        rate: 1, // 语速
        pitch: 1, // 音调
        enable_ssml: false // 是否开启SSML功能。如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
      },
      input: {}
    }
  });
  ws.send(runTaskMessage);
  console.log('已发送run-task消息');
});

const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
ws.on('message', (data, isBinary) => {
  if (isBinary) {
    // 写入二进制数据到文件
    fileStream.write(data);
  } else {
    const message = JSON.parse(data);

    switch (message.header.event) {
      case 'task-started':
        taskStarted = true;
        console.log('任务已开始');
        // 发送continue-task事件
        sendContinueTasks(ws);
        break;
      case 'task-finished':
        console.log('任务已完成');
        ws.close();
        fileStream.end(() => {
          console.log('文件流已关闭');
        });
        break;
      case 'task-failed':
        console.error('任务失败：', message.header.error_message);
        ws.close();
        fileStream.end(() => {
          console.log('文件流已关闭');
        });
        break;
      default:
        // 可以在这里处理result-generated
        break;
    }
  }
});

function sendContinueTasks(ws) {
  const texts = [
    '床前明月光，',
    '疑是地上霜。',
    '举头望明月，',
    '低头思故乡。'
  ];

  texts.forEach((text, index) => {
    setTimeout(() => {
      if (taskStarted) {
        const continueTaskMessage = JSON.stringify({
          header: {
            action: 'continue-task',
            task_id: taskId,
            streaming: 'duplex'
          },
          payload: {
            input: {
              text: text
            }
          }
        });
        ws.send(continueTaskMessage);
        console.log(`已发送continue-task，文本：${text}`);
      }
    }, index * 1000); // 每隔1秒发送一次
  });

  // 发送finish-task事件
  setTimeout(() => {
    if (taskStarted) {
      const finishTaskMessage = JSON.stringify({
        header: {
          action: 'finish-task',
          task_id: taskId,
          streaming: 'duplex'
        },
        payload: {
          input: {}
        }
      });
      ws.send(finishTaskMessage);
      console.log('已发送finish-task');
    }
  }, texts.length * 1000 + 1000); // 在所有continue-task事件发送完毕后1秒发送
}

ws.on('close', () => {
  console.log('已断开与WebSocket服务器的连接');
});
```

#### Java

建议使用 Java DashScope SDK 进行开发，请参见[Qwen-Audio-TTS Java SDK](raw/_short/qwen-audio-tts-java-sdk-a8824c674989f110.md) / [CosyVoice Java SDK](raw/_short/cosyvoice-java-sdk-4cad5c0351587943.md)。

以下是 Java WebSocket 直连示例，运行前请导入以下依赖：

-   `Java-WebSocket`
-   `jackson-databind`

推荐使用Maven或Gradle管理依赖包，其配置如下：

pom.xml

```
<dependencies>
    <!-- WebSocket Client -->
    <dependency>
        <groupId>org.java-websocket</groupId>
        <artifactId>Java-WebSocket</artifactId>
        <version>1.5.3</version>
    </dependency>

    <!-- JSON Processing -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.13.0</version>
    </dependency>
</dependencies>
```

build.gradle

```
// 省略其它代码
dependencies {
  // WebSocket Client
  implementation 'org.java-websocket:Java-WebSocket:1.5.3'
  // JSON Processing
  implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.0'
}
// 省略其它代码
```

Java代码如下：

```
import com.fasterxml.jackson.databind.ObjectMapper;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.nio.ByteBuffer;
import java.util.*;

public class TTSWebSocketClient extends WebSocketClient {
    private final String taskId = UUID.randomUUID().toString();
    private final String outputFile = "output_" + System.currentTimeMillis() + ".mp3";
    private boolean taskFinished = false;

    public TTSWebSocketClient(URI serverUri, Map<String, String> headers) {
        super(serverUri, headers);
    }

    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        System.out.println("连接成功");

        // 发送run-task事件
        // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
        String runTaskCommand = "{ \"header\": { \"action\": \"run-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"task_group\": \"audio\", \"task\": \"tts\", \"function\": \"SpeechSynthesizer\", \"model\": \"qwen-audio-3.0-tts-flash\", \"parameters\": { \"text_type\": \"PlainText\", \"voice\": \"longanhuan_v3.6\", \"format\": \"mp3\", \"sample_rate\": 22050, \"volume\": 50, \"rate\": 1, \"pitch\": 1, \"enable_ssml\": false }, \"input\": {} }}";
        send(runTaskCommand);
    }

    @Override
    public void onMessage(String message) {
        System.out.println("收到服务端返回的消息：" + message);
        try {
            // Parse JSON message
            Map<String, Object> messageMap = new ObjectMapper().readValue(message, Map.class);

            if (messageMap.containsKey("header")) {
                Map<String, Object> header = (Map<String, Object>) messageMap.get("header");

                if (header.containsKey("event")) {
                    String event = (String) header.get("event");

                    if ("task-started".equals(event)) {
                        System.out.println("收到服务端返回的task-started事件");

                        List<String> texts = Arrays.asList(
                                "床前明月光，疑是地上霜",
                                "举头望明月，低头思故乡"
                        );

                        for (String text : texts) {
                            // 发送continue-task事件
                            sendContinueTask(text);
                        }

                        // 发送finish-task事件
                        sendFinishTask();
                    } else if ("task-finished".equals(event)) {
                        System.out.println("收到服务端返回的task-finished事件");
                        taskFinished = true;
                        closeConnection();
                    } else if ("task-failed".equals(event)) {
                        System.out.println("任务失败：" + message);
                        closeConnection();
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("出现异常：" + e.getMessage());
        }
    }

    @Override
    public void onMessage(ByteBuffer message) {
        System.out.println("收到的二进制音频数据大小为：" + message.remaining());

        try (FileOutputStream fos = new FileOutputStream(outputFile, true)) {
            byte[] buffer = new byte[message.remaining()];
            message.get(buffer);
            fos.write(buffer);
            System.out.println("音频数据已写入本地文件" + outputFile + "中");
        } catch (IOException e) {
            System.err.println("音频数据写入本地文件失败：" + e.getMessage());
        }
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("连接关闭：" + reason + " (" + code + ")");
    }

    @Override
    public void onError(Exception ex) {
        System.err.println("报错：" + ex.getMessage());
        ex.printStackTrace();
    }

    private void sendContinueTask(String text) {
        String command = "{ \"header\": { \"action\": \"continue-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": { \"text\": \"" + text + "\" } }}";
        send(command);
    }

    private void sendFinishTask() {
        String command = "{ \"header\": { \"action\": \"finish-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": {} }}";
        send(command);
    }

    private void closeConnection() {
        if (!isClosed()) {
            close();
        }
    }

    public static void main(String[] args) {
        try {
            // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：String apiKey = "sk-xxx"
            String apiKey = System.getenv("DASHSCOPE_API_KEY");
            if (apiKey == null || apiKey.isEmpty()) {
                System.err.println("请设置 DASHSCOPE_API_KEY 环境变量");
                return;
            }

            Map<String, String> headers = new HashMap<>();
            headers.put("Authorization", "bearer " + apiKey);
            // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
            TTSWebSocketClient client = new TTSWebSocketClient(new URI("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"), headers);

            client.connect();

            while (!client.isClosed() && !client.taskFinished) {
                Thread.sleep(1000);
            }
        } catch (Exception e) {
            System.err.println("连接WebSocket服务失败：" + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

#### Python

建议使用 Python DashScope SDK 进行开发，请参见[Qwen-Audio-TTS Python SDK](raw/_short/qwen-audio-tts-python-sdk-33fc56a178dfcd65.md) / [CosyVoice Python SDK](raw/_short/cosyvoice-python-sdk-c20dfd31499fc83c.md)。

以下是 Python WebSocket 直连示例，运行前请导入以下依赖：

```
pip uninstall websocket-client
pip uninstall websocket
pip install websocket-client
```

**重要**请不要将运行示例代码的Python文件命名为“websocket.py”，否则会报错（AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?）。

```
import websocket
import json
import uuid
import os
import time

class TTSClient:
    def __init__(self, api_key, uri):
        """
    初始化 TTSClient 实例

    参数:
        api_key (str): 鉴权用的 API Key
        uri (str): WebSocket 服务地址
    """
        self.api_key = api_key  # 替换为你的 API Key
        self.uri = uri  # 替换为你的 WebSocket 地址
        self.task_id = str(uuid.uuid4())  # 生成唯一任务 ID
        self.output_file = f"output_{int(time.time())}.mp3"  # 输出音频文件路径
        self.ws = None  # WebSocketApp 实例
        self.task_started = False  # 是否收到 task-started
        self.task_finished = False  # 是否收到 task-finished / task-failed

    def on_open(self, ws):
        """
    WebSocket 连接建立时回调函数
    发送 run-task 事件开启语音合成任务
    """
        print("WebSocket 已连接")

        # 构造 run-task 事件
        run_task_cmd = {
            "header": {
                "action": "run-task",
                "task_id": self.task_id,
                "streaming": "duplex"
            },
            "payload": {
                "task_group": "audio",
                "task": "tts",
                "function": "SpeechSynthesizer",
                "model": "qwen-audio-3.0-tts-flash",
                "parameters": {
                    "text_type": "PlainText",
                    "voice": "longanhuan_v3.6",
                    "format": "mp3",
                    "sample_rate": 22050,
                    "volume": 50,
                    "rate": 1,
                    "pitch": 1,
                    # 如果enable_ssml设为True，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                    "enable_ssml": False
                },
                "input": {}
            }
        }

        # 发送 run-task 事件
        ws.send(json.dumps(run_task_cmd))
        print("已发送 run-task 事件")

    def on_message(self, ws, message):
        """
    接收到消息时的回调函数
    区分文本和二进制消息处理
    """
        if isinstance(message, str):
            # 处理 JSON 文本消息
            try:
                msg_json = json.loads(message)
                print(f"收到 JSON 消息: {msg_json}")

                if "header" in msg_json:
                    header = msg_json["header"]

                    if "event" in header:
                        event = header["event"]

                        if event == "task-started":
                            print("任务已启动")
                            self.task_started = True

                            # 发送 continue-task 事件
                            texts = [
                                "床前明月光，疑是地上霜",
                                "举头望明月，低头思故乡"
                            ]

                            for text in texts:
                                self.send_continue_task(text)

                            # 所有 continue-task 发送完成后发送 finish-task
                            self.send_finish_task()

                        elif event == "task-finished":
                            print("任务已完成")
                            self.task_finished = True
                            self.close(ws)

                        elif event == "task-failed":
                            error_msg = msg_json.get("error_message", "未知错误")
                            print(f"任务失败: {error_msg}")
                            self.task_finished = True
                            self.close(ws)

            except json.JSONDecodeError as e:
                print(f"JSON 解析失败: {e}")
        else:
            # 处理二进制消息（音频数据）
            print(f"收到二进制消息，大小: {len(message)} 字节")
            with open(self.output_file, "ab") as f:
                f.write(message)
            print(f"已将音频数据写入本地文件{self.output_file}中")

    def on_error(self, ws, error):
        """发生错误时的回调"""
        print(f"WebSocket 出错: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭时的回调"""
        print(f"WebSocket 已关闭: {close_msg} ({close_status_code})")

    def send_continue_task(self, text):
        """发送 continue-task 事件，附带要合成的文本内容"""
        cmd = {
            "header": {
                "action": "continue-task",
                "task_id": self.task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {
                    "text": text
                }
            }
        }

        self.ws.send(json.dumps(cmd))
        print(f"已发送 continue-task 事件，文本内容: {text}")

    def send_finish_task(self):
        """发送 finish-task 事件，结束语音合成任务"""
        cmd = {
            "header": {
                "action": "finish-task",
                "task_id": self.task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            }
        }

        self.ws.send(json.dumps(cmd))
        print("已发送 finish-task 事件")

    def close(self, ws):
        """主动关闭连接"""
        if ws and ws.sock and ws.sock.connected:
            ws.close()
            print("已主动关闭连接")

    def run(self):
        """启动 WebSocket 客户端"""
        # 设置请求头部（鉴权）
        header = {
            "Authorization": f"bearer {self.api_key}",
            "X-DashScope-DataInspection": "enable"
        }

        # 创建 WebSocketApp 实例
        self.ws = websocket.WebSocketApp(
            self.uri,
            header=header,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        print("正在监听 WebSocket 消息...")
        self.ws.run_forever()  # 启动长连接监听

# 示例使用方式
if __name__ == "__main__":
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：API_KEY = "sk-xxx"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    SERVER_URI = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"  # 替换为你的 WebSocket 地址

    client = TTSClient(API_KEY, SERVER_URI)
    client.run()
```

#### Qwen-TTS

1.  **创建客户端**
    
    #### Python
    
    在本地新建 Python 文件，命名为`tts_realtime_client.py`并复制以下代码到文件中：
    
    ```
    # -- coding: utf-8 --
    
    import asyncio
    import websockets
    import json
    import base64
    import time
    from typing import Optional, Callable, Dict, Any
    from enum import Enum
    
    class SessionMode(Enum):
        SERVER_COMMIT = "server_commit"
        COMMIT = "commit"
    
    class TTSRealtimeClient:
        """
        与 TTS Realtime API 交互的客户端。
    
        该类提供了连接 TTS Realtime API、发送文本数据、获取音频输出以及管理 WebSocket 连接的相关方法。
    
        属性说明:
            base_url (str):
                Realtime API 的基础地址。
            api_key (str):
                用于身份验证的 API Key。
            voice (str):
                服务端合成语音所使用的声音。
            mode (SessionMode):
                会话模式，可选 server_commit 或 commit。
            audio_callback (Callable[[bytes], None]):
                接收音频数据的回调函数。
            language_type(str)
                合成的语音的语种，可选值Chinese、English、German、Italian、Portuguese、Spanish、Japanese、Korean、French、Russian、Auto
        """
    
        def __init__(
                self,
                base_url: str,
                api_key: str,
                voice: str = "Cherry",
                mode: SessionMode = SessionMode.SERVER_COMMIT,
                audio_callback: Optional[Callable[[bytes], None]] = None,
            language_type: str = "Auto"):
            self.base_url = base_url
            self.api_key = api_key
            self.voice = voice
            self.mode = mode
            self.ws = None
            self.audio_callback = audio_callback
            self.language_type = language_type
    
            # 当前回复状态
            self._current_response_id = None
            self._current_item_id = None
            self._is_responding = False
            self._response_done_future = None
    
        async def connect(self) -> None:
            """与 TTS Realtime API 建立 WebSocket 连接。"""
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
    
            self.ws = await websockets.connect(self.base_url, additional_headers=headers)
    
            # 设置默认会话配置
            await self.update_session({
                "mode": self.mode.value,
                "voice": self.voice,
                # 如需使用指令控制功能，请取消下方注释，并在server_commit.py或commit.py中将model替换为qwen3-tts-instruct-flash-realtime
                # "instructions": "语速较快，带有明显的上扬语调，适合介绍时尚产品。",
                # "optimize_instructions": true
                "language_type": self.language_type,
                "response_format": "pcm",
                "sample_rate": 24000
            })
    
        async def send_event(self, event) -> None:
            """发送事件到服务器。"""
            event['event_id'] = "event_" + str(int(time.time() * 1000))
            print(f"发送事件: type={event['type']}, event_id={event['event_id']}")
            await self.ws.send(json.dumps(event))
    
        async def update_session(self, config: Dict[str, Any]) -> None:
            """更新会话配置。"""
            event = {
                "type": "session.update",
                "session": config
            }
            print("更新会话配置: ", event)
            await self.send_event(event)
    
        async def append_text(self, text: str) -> None:
            """向 API 发送文本数据。"""
            event = {
                "type": "input_text_buffer.append",
                "text": text
            }
            await self.send_event(event)
    
        async def commit_text_buffer(self) -> None:
            """提交文本缓冲区以触发处理。"""
            event = {
                "type": "input_text_buffer.commit"
            }
            await self.send_event(event)
    
        async def clear_text_buffer(self) -> None:
            """清除文本缓冲区。"""
            event = {
                "type": "input_text_buffer.clear"
            }
            await self.send_event(event)
    
        async def finish_session(self) -> None:
            """结束会话。"""
            event = {
                "type": "session.finish"
            }
            await self.send_event(event)
    
        async def wait_for_response_done(self):
            """等待 response.done 事件"""
            if self._response_done_future:
                await self._response_done_future
    
        async def handle_messages(self) -> None:
            """处理来自服务器的消息。"""
            try:
                async for message in self.ws:
                    event = json.loads(message)
                    event_type = event.get("type")
    
                    if event_type != "response.audio.delta":
                        print(f"收到事件: {event_type}")
    
                    if event_type == "error":
                        print("错误: ", event.get('error', {}))
                        continue
                    elif event_type == "session.created":
                        print("会话创建，ID: ", event.get('session', {}).get('id'))
                    elif event_type == "session.updated":
                        print("会话更新，ID: ", event.get('session', {}).get('id'))
                    elif event_type == "input_text_buffer.committed":
                        print("文本缓冲区已提交，项目ID: ", event.get('item_id'))
                    elif event_type == "input_text_buffer.cleared":
                        print("文本缓冲区已清除")
                    elif event_type == "response.created":
                        self._current_response_id = event.get("response", {}).get("id")
                        self._is_responding = True
                        # 创建新的 future 来等待 response.done
                        self._response_done_future = asyncio.Future()
                        print("响应已创建，ID: ", self._current_response_id)
                    elif event_type == "response.output_item.added":
                        self._current_item_id = event.get("item", {}).get("id")
                        print("输出项已添加，ID: ", self._current_item_id)
                    # 处理音频增量
                    elif event_type == "response.audio.delta" and self.audio_callback:
                        audio_bytes = base64.b64decode(event.get("delta", ""))
                        self.audio_callback(audio_bytes)
                    elif event_type == "response.audio.done":
                        print("音频生成完成")
                    elif event_type == "response.done":
                        self._is_responding = False
                        self._current_response_id = None
                        self._current_item_id = None
                        # 标记 future 完成
                        if self._response_done_future and not self._response_done_future.done():
                            self._response_done_future.set_result(True)
                        print("响应完成")
                    elif event_type == "session.finished":
                        print("会话已结束")
    
            except websockets.exceptions.ConnectionClosed:
                print("连接已关闭")
            except Exception as e:
                print("消息处理出错: ", str(e))
    
        async def close(self) -> None:
            """关闭 WebSocket 连接。"""
            if self.ws:
                await self.ws.close()
    ```
    
    #### Java
    
    在本地新建 Java 文件，命名为`TTSRealtimeClient.java`并复制以下代码到文件中：
    
    ```
    import com.google.gson.Gson;
    import com.google.gson.JsonObject;
    import org.java_websocket.client.WebSocketClient;
    import org.java_websocket.handshake.ServerHandshake;
    
    import java.net.URI;
    import java.util.Base64;
    import java.util.HashMap;
    import java.util.Map;
    import java.util.concurrent.CountDownLatch;
    import java.util.function.Consumer;
    
    /**
     * 与 TTS Realtime API 交互的客户端。
     *
     * 该类提供了连接 TTS Realtime API、发送文本数据、获取音频输出以及管理 WebSocket 连接的相关方法。
     */
    public class TTSRealtimeClient {
    
        public enum SessionMode {
            SERVER_COMMIT("server_commit"),
            COMMIT("commit");
            private final String value;
            SessionMode(String value) { this.value = value; }
            public String getValue() { return value; }
        }
    
        /**
         * 音频回调接口
         */
        public interface AudioCallback {
            void onAudio(byte[] audioData);
        }
    
        private final String baseUrl;
        private final String apiKey;
        private final String voice;
        private final SessionMode mode;
        private final String languageType;
        private final AudioCallback audioCallback;
        private final Gson gson = new Gson();
    
        private WebSocketClient ws;
        private CountDownLatch responseDoneLatch;
        private CountDownLatch sessionFinishedLatch;
    
        public TTSRealtimeClient(String baseUrl, String apiKey, String voice,
                                 SessionMode mode, AudioCallback audioCallback,
                                 String languageType) {
            this.baseUrl = baseUrl;
            this.apiKey = apiKey;
            this.voice = voice;
            this.mode = mode;
            this.audioCallback = audioCallback;
            this.languageType = languageType;
        }
    
        public TTSRealtimeClient(String baseUrl, String apiKey, String voice,
                                 SessionMode mode, AudioCallback audioCallback) {
            this(baseUrl, apiKey, voice, mode, audioCallback, "Auto");
        }
    
        /**
         * 与 TTS Realtime API 建立 WebSocket 连接。
         */
        public void connect() throws Exception {
            Map<String, String> headers = new HashMap<>();
            headers.put("Authorization", "Bearer " + apiKey);
    
            responseDoneLatch = new CountDownLatch(0);
            sessionFinishedLatch = new CountDownLatch(1);
    
            ws = new WebSocketClient(new URI(baseUrl), headers) {
                @Override
                public void onOpen(ServerHandshake handshake) {
                    System.out.println("WebSocket 连接已建立");
                    // 发送默认会话配置
                    JsonObject session = new JsonObject();
                    session.addProperty("mode", mode.getValue());
                    session.addProperty("voice", TTSRealtimeClient.this.voice);
                    // 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash-realtime
                    // session.addProperty("instructions", "语速较快，带有明显的上扬语调，适合介绍时尚产品。");
                    // session.addProperty("optimize_instructions", true);
                    session.addProperty("language_type", languageType);
                    session.addProperty("response_format", "pcm");
                    session.addProperty("sample_rate", 24000);
                    updateSession(session);
                }
    
                @Override
                public void onMessage(String message) {
                    JsonObject event = gson.fromJson(message, JsonObject.class);
                    String eventType = event.has("type") ? event.get("type").getAsString() : "";
    
                    if (!"response.audio.delta".equals(eventType)) {
                        System.out.println("收到事件: " + eventType);
                    }
    
                    switch (eventType) {
                        case "error":
                            System.err.println("错误: " + event.get("error"));
                            break;
                        case "session.created":
                            System.out.println("会话创建，ID: " +
                                event.getAsJsonObject("session").get("id").getAsString());
                            break;
                        case "session.updated":
                            System.out.println("会话更新，ID: " +
                                event.getAsJsonObject("session").get("id").getAsString());
                            break;
                        case "input_text_buffer.committed":
                            System.out.println("文本缓冲区已提交，项目ID: " + event.get("item_id"));
                            break;
                        case "input_text_buffer.cleared":
                            System.out.println("文本缓冲区已清除");
                            break;
                        case "response.created":
                            System.out.println("响应已创建，ID: " +
                                event.getAsJsonObject("response").get("id").getAsString());
                            responseDoneLatch = new CountDownLatch(1);
                            break;
                        case "response.output_item.added":
                            System.out.println("输出项已添加，ID: " +
                                event.getAsJsonObject("item").get("id").getAsString());
                            break;
                        case "response.audio.delta":
                            if (audioCallback != null) {
                                byte[] audioBytes = Base64.getDecoder().decode(
                                    event.get("delta").getAsString());
                                audioCallback.onAudio(audioBytes);
                            }
                            break;
                        case "response.audio.done":
                            System.out.println("音频生成完成");
                            break;
                        case "response.done":
                            System.out.println("响应完成");
                            responseDoneLatch.countDown();
                            break;
                        case "session.finished":
                            System.out.println("会话已结束");
                            sessionFinishedLatch.countDown();
                            break;
                    }
                }
    
                @Override
                public void onClose(int code, String reason, boolean remote) {
                    System.out.println("连接已关闭: " + reason);
                }
    
                @Override
                public void onError(Exception ex) {
                    System.err.println("WebSocket 错误: " + ex.getMessage());
                }
            };
            ws.connectBlocking();
        }
    
        /**
         * 发送事件到服务器。
         */
        public void sendEvent(JsonObject event) {
            String eventId = "event_" + System.currentTimeMillis();
            event.addProperty("event_id", eventId);
            System.out.println("发送事件: type=" + event.get("type").getAsString()
                + ", event_id=" + eventId);
            ws.send(gson.toJson(event));
        }
    
        /**
         * 更新会话配置。
         */
        public void updateSession(JsonObject config) {
            JsonObject event = new JsonObject();
            event.addProperty("type", "session.update");
            event.add("session", config);
            System.out.println("更新会话配置: " + event);
            sendEvent(event);
        }
    
        /**
         * 向 API 发送文本数据。
         */
        public void appendText(String text) {
            JsonObject event = new JsonObject();
            event.addProperty("type", "input_text_buffer.append");
            event.addProperty("text", text);
            sendEvent(event);
        }
    
        /**
         * 提交文本缓冲区以触发处理。
         */
        public void commitTextBuffer() {
            JsonObject event = new JsonObject();
            event.addProperty("type", "input_text_buffer.commit");
            sendEvent(event);
        }
    
        /**
         * 清除文本缓冲区。
         */
        public void clearTextBuffer() {
            JsonObject event = new JsonObject();
            event.addProperty("type", "input_text_buffer.clear");
            sendEvent(event);
        }
    
        /**
         * 结束会话。
         */
        public void finishSession() {
            JsonObject event = new JsonObject();
            event.addProperty("type", "session.finish");
            sendEvent(event);
        }
    
        /**
         * 等待 response.done 事件。
         */
        public void waitForResponseDone() throws InterruptedException {
            responseDoneLatch.await();
        }
    
        /**
         * 等待 session.finished 事件。
         */
        public void waitForSessionFinished() throws InterruptedException {
            sessionFinishedLatch.await();
        }
    
        /**
         * 关闭 WebSocket 连接。
         */
        public void close() {
            if (ws != null) {
                ws.close();
            }
        }
    }
    ```
    
2.  **选择语音合成模式**
    
    Realtime API支持以下两种模式：
    
    -   **server\_commit 模式**
        
        服务端智能判断文本分段与合成时机，客户端只需发送文本。适合低延迟场景（如 GPS 导航）。
        
    -   **commit 模式**
        
        客户端将文本添加至缓冲区后主动触发合成。适合精细控制断句的场景（如新闻播报）。
        
    
    #### server\_commit 模式
    
    #### Python
    
    在`tts_realtime_client.py`的同级目录下新建另一个 Python 文件，命名为`server_commit.py`，并将以下代码复制进文件中：
    
    ```
    import os
    import asyncio
    import logging
    import wave
    from tts_realtime_client import TTSRealtimeClient, SessionMode
    import pyaudio
    
    # QwenTTS 服务配置
    # 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime，并在tts_realtime_client.py中取消instructions的注释
    # 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime
    URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：API_KEY="sk-xxx"
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    
    if not API_KEY:
        raise ValueError("Please set DASHSCOPE_API_KEY environment variable")
    
    # 收集音频数据
    _audio_chunks = []
    # 实时播放相关
    _AUDIO_SAMPLE_RATE = 24000
    _audio_pyaudio = pyaudio.PyAudio()
    _audio_stream = None  # 将在运行时打开
    
    def _audio_callback(audio_bytes: bytes):
        """TTSRealtimeClient 音频回调: 实时播放并缓存"""
        global _audio_stream
        if _audio_stream is not None:
            try:
                _audio_stream.write(audio_bytes)
            except Exception as exc:
                logging.error(f"PyAudio playback error: {exc}")
        _audio_chunks.append(audio_bytes)
        logging.info(f"Received audio chunk: {len(audio_bytes)} bytes")
    
    def _save_audio_to_file(filename: str = "output.wav", sample_rate: int = 24000) -> bool:
        """将收集到的音频数据保存为 WAV 文件"""
        if not _audio_chunks:
            logging.warning("No audio data to save")
            return False
    
        try:
            audio_data = b"".join(_audio_chunks)
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)  # 单声道
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            logging.info(f"Audio saved to: {filename}")
            return True
        except Exception as exc:
            logging.error(f"Failed to save audio: {exc}")
            return False
    
    async def _produce_text(client: TTSRealtimeClient):
        """向服务器发送文本片段"""
        text_fragments = [
            "阿里云的大模型服务平台阿里云百炼是一站式的大模型开发及应用构建平台。",
            "不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。",
            "您可以通过简单的界面操作，在5分钟内开发出一款大模型应用，",
            "或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。",
        ]
    
        logging.info("Sending text fragments…")
        for text in text_fragments:
            logging.info(f"Sending fragment: {text}")
            await client.append_text(text)
            await asyncio.sleep(0.1)  # 片段间稍作延时
    
        # 等待服务器完成内部处理后结束会话
        await asyncio.sleep(1.0)
        await client.finish_session()
    
    async def _run_demo():
        """运行完整 Demo"""
        global _audio_stream
        # 打开 PyAudio 输出流
        _audio_stream = _audio_pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=_AUDIO_SAMPLE_RATE,
            output=True,
            frames_per_buffer=1024
        )
    
        client = TTSRealtimeClient(
            base_url=URL,
            api_key=API_KEY,
            voice="Cherry",
            mode=SessionMode.SERVER_COMMIT,
            audio_callback=_audio_callback
        )
    
        # 建立连接
        await client.connect()
    
        # 并行执行消息处理与文本发送
        consumer_task = asyncio.create_task(client.handle_messages())
        producer_task = asyncio.create_task(_produce_text(client))
    
        await producer_task  # 等待文本发送完成
    
        # 等待 response.done
        await client.wait_for_response_done()
    
        # 关闭连接并取消消费者任务
        await client.close()
        consumer_task.cancel()
    
        # 关闭音频流
        if _audio_stream is not None:
            _audio_stream.stop_stream()
            _audio_stream.close()
        _audio_pyaudio.terminate()
    
        # 保存音频数据
        os.makedirs("outputs", exist_ok=True)
        _save_audio_to_file(os.path.join("outputs", "qwen_tts_output.wav"))
    
    def main():
        """同步入口"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Starting QwenTTS Realtime Client demo…")
        asyncio.run(_run_demo())
    
    if __name__ == "__main__":
        main()
    ```
    
    运行`server_commit.py`，即可听到 Realtime API实时生成的音频。
    
    #### Java
    
    在`TTSRealtimeClient.java`的同级目录下新建另一个 Java 文件，命名为`ServerCommit.java`，并将以下代码复制进文件中：
    
    ```
    import javax.sound.sampled.*;
    import java.io.*;
    import java.util.ArrayList;
    import java.util.List;
    import java.util.concurrent.ConcurrentLinkedQueue;
    import java.util.concurrent.atomic.AtomicBoolean;
    
    public class ServerCommit {
        // 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime
        private static final String URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime";
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static final String API_KEY = "sk-xxx";
        private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
        private static final int SAMPLE_RATE = 24000;
    
        // 音频数据缓存
        private static final List<byte[]> audioChunks = new ArrayList<>();
        // 实时播放队列
        private static final ConcurrentLinkedQueue<byte[]> playbackQueue = new ConcurrentLinkedQueue<>();
        private static final AtomicBoolean playing = new AtomicBoolean(true);
    
        public static void main(String[] args) throws Exception {
            if (API_KEY == null || API_KEY.isEmpty()) {
                throw new IllegalStateException("请设置 DASHSCOPE_API_KEY 环境变量");
            }
    
            // 初始化音频播放
            AudioFormat format = new AudioFormat(SAMPLE_RATE, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
            SourceDataLine audioLine = (SourceDataLine) AudioSystem.getLine(info);
            audioLine.open(format);
            audioLine.start();
    
            // 启动播放线程
            Thread playerThread = new Thread(() -> {
                while (playing.get() || !playbackQueue.isEmpty()) {
                    byte[] chunk = playbackQueue.poll();
                    if (chunk != null) {
                        audioLine.write(chunk, 0, chunk.length);
                    } else {
                        try { Thread.sleep(10); } catch (InterruptedException ignored) {}
                    }
                }
            });
            playerThread.start();
    
            // 创建 TTS 客户端
            // 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime，并在TTSRealtimeClient.java中取消instructions的注释
            TTSRealtimeClient client = new TTSRealtimeClient(
                URL, API_KEY, "Cherry",
                TTSRealtimeClient.SessionMode.SERVER_COMMIT,
                audioData -> {
                    playbackQueue.add(audioData);
                    audioChunks.add(audioData);
                    System.out.println("收到音频数据: " + audioData.length + " bytes");
                }
            );
    
            client.connect();
    
            // 发送文本片段
            String[] textFragments = {
                "阿里云的大模型服务平台阿里云百炼是一站式的大模型开发及应用构建平台。",
                "不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。",
                "您可以通过简单的界面操作，在5分钟内开发出一款大模型应用，",
                "或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。"
            };
    
            System.out.println("开始发送文本...");
            for (String text : textFragments) {
                System.out.println("发送片段: " + text);
                client.appendText(text);
                Thread.sleep(100);
            }
    
            Thread.sleep(1000);
            client.finishSession();
    
            // 等待响应完成
            client.waitForResponseDone();
            client.waitForSessionFinished();
            client.close();
    
            // 等待播放完成
            playing.set(false);
            playerThread.join();
            audioLine.drain();
            audioLine.close();
    
            // 保存音频文件
            saveWav("output.wav");
            System.out.println("完成");
        }
    
        private static void saveWav(String filename) throws IOException {
            if (audioChunks.isEmpty()) {
                System.out.println("没有音频数据可保存");
                return;
            }
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            for (byte[] chunk : audioChunks) {
                bos.write(chunk);
            }
            byte[] allAudio = bos.toByteArray();
            AudioFormat format = new AudioFormat(SAMPLE_RATE, 16, 1, true, false);
            AudioInputStream ais = new AudioInputStream(
                new ByteArrayInputStream(allAudio), format, allAudio.length / 2);
            new File("outputs").mkdirs();
            AudioSystem.write(ais, AudioFileFormat.Type.WAVE,
                new File("outputs/" + filename));
            System.out.println("音频已保存到: outputs/" + filename);
        }
    }
    ```
    
    编译并运行`ServerCommit.java`，即可听到 Realtime API实时生成的音频。
    
    #### commit 模式
    
    #### Python
    
    在`tts_realtime_client.py`的同级目录下新建另一个 Python 文件，命名为`commit.py`，并将以下代码复制进文件中：
    
    ```
    import os
    import asyncio
    import logging
    import wave
    from tts_realtime_client import TTSRealtimeClient, SessionMode
    import pyaudio
    
    # QwenTTS 服务配置
    # 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime，并在tts_realtime_client.py中取消instructions的注释
    # 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime
    URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：API_KEY="sk-xxx"
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    
    if not API_KEY:
        raise ValueError("Please set DASHSCOPE_API_KEY environment variable")
    
    # 收集音频数据
    _audio_chunks = []
    _AUDIO_SAMPLE_RATE = 24000
    _audio_pyaudio = pyaudio.PyAudio()
    _audio_stream = None
    
    def _audio_callback(audio_bytes: bytes):
        """TTSRealtimeClient 音频回调: 实时播放并缓存"""
        global _audio_stream
        if _audio_stream is not None:
            try:
                _audio_stream.write(audio_bytes)
            except Exception as exc:
                logging.error(f"PyAudio playback error: {exc}")
        _audio_chunks.append(audio_bytes)
        logging.info(f"Received audio chunk: {len(audio_bytes)} bytes")
    
    def _save_audio_to_file(filename: str = "output.wav", sample_rate: int = 24000) -> bool:
        """将收集到的音频数据保存为 WAV 文件"""
        if not _audio_chunks:
            logging.warning("No audio data to save")
            return False
    
        try:
            audio_data = b"".join(_audio_chunks)
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)  # 单声道
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            logging.info(f"Audio saved to: {filename}")
            return True
        except Exception as exc:
            logging.error(f"Failed to save audio: {exc}")
            return False
    
    async def _user_input_loop(client: TTSRealtimeClient):
        """持续获取用户输入并发送文本，当用户输入空文本时发送commit事件并结束本次会话"""
        print("请输入文本（直接按Enter发送commit事件并结束本次会话，按Ctrl+C或Ctrl+D结束整个程序）：")
    
        while True:
            try:
                user_text = input("> ")
                if not user_text:  # 用户输入为空
                    # 空输入视为一次对话的结束: 提交缓冲区 -> 结束会话 -> 跳出循环
                    logging.info("空输入，发送 commit 事件并结束本次会话")
                    await client.commit_text_buffer()
                    # 适当等待服务器处理 commit，防止过早结束会话导致丢失音频
                    await asyncio.sleep(0.3)
                    await client.finish_session()
                    break  # 直接退出用户输入循环，无需再次回车
                else:
                    logging.info(f"发送文本: {user_text}")
                    await client.append_text(user_text)
    
            except EOFError:  # 用户按下Ctrl+D
                break
            except KeyboardInterrupt:  # 用户按下Ctrl+C
                break
    
        # 结束会话
        logging.info("结束会话...")
    async def _run_demo():
        """运行完整 Demo"""
        global _audio_stream
        # 打开 PyAudio 输出流
        _audio_stream = _audio_pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=_AUDIO_SAMPLE_RATE,
            output=True,
            frames_per_buffer=1024
        )
    
        client = TTSRealtimeClient(
            base_url=URL,
            api_key=API_KEY,
            voice="Cherry",
            mode=SessionMode.COMMIT,  # 修改为COMMIT模式
            audio_callback=_audio_callback
        )
    
        # 建立连接
        await client.connect()
    
        # 并行执行消息处理与用户输入
        consumer_task = asyncio.create_task(client.handle_messages())
        producer_task = asyncio.create_task(_user_input_loop(client))
    
        await producer_task  # 等待用户输入完成
    
        # 等待 response.done
        await client.wait_for_response_done()
    
        # 关闭连接并取消消费者任务
        await client.close()
        consumer_task.cancel()
    
        # 关闭音频流
        if _audio_stream is not None:
            _audio_stream.stop_stream()
            _audio_stream.close()
        _audio_pyaudio.terminate()
    
        # 保存音频数据
        os.makedirs("outputs", exist_ok=True)
        _save_audio_to_file(os.path.join("outputs", "qwen_tts_output.wav"))
    
    def main():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Starting QwenTTS Realtime Client demo…")
        asyncio.run(_run_demo())
    
    if __name__ == "__main__":
        main()
    ```
    
    运行`commit.py`，可多次输入要合成的文本。在未输入文本的情况下单击 Enter 键，将从扬声器听到 Realtime API返回的音频。
    
    #### Java
    
    在`TTSRealtimeClient.java`的同级目录下新建另一个 Java 文件，命名为`Commit.java`，并将以下代码复制进文件中：
    
    ```
    import javax.sound.sampled.*;
    import java.io.*;
    import java.util.ArrayList;
    import java.util.List;
    import java.util.Scanner;
    import java.util.concurrent.ConcurrentLinkedQueue;
    import java.util.concurrent.atomic.AtomicBoolean;
    
    public class Commit {
        // 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime
        private static final String URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime";
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：private static final String API_KEY = "sk-xxx";
        private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
        private static final int SAMPLE_RATE = 24000;
    
        private static final List<byte[]> audioChunks = new ArrayList<>();
        private static final ConcurrentLinkedQueue<byte[]> playbackQueue = new ConcurrentLinkedQueue<>();
        private static final AtomicBoolean playing = new AtomicBoolean(true);
    
        public static void main(String[] args) throws Exception {
            if (API_KEY == null || API_KEY.isEmpty()) {
                throw new IllegalStateException("请设置 DASHSCOPE_API_KEY 环境变量");
            }
    
            // 初始化音频播放
            AudioFormat format = new AudioFormat(SAMPLE_RATE, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
            SourceDataLine audioLine = (SourceDataLine) AudioSystem.getLine(info);
            audioLine.open(format);
            audioLine.start();
    
            // 启动播放线程
            Thread playerThread = new Thread(() -> {
                while (playing.get() || !playbackQueue.isEmpty()) {
                    byte[] chunk = playbackQueue.poll();
                    if (chunk != null) {
                        audioLine.write(chunk, 0, chunk.length);
                    } else {
                        try { Thread.sleep(10); } catch (InterruptedException ignored) {}
                    }
                }
            });
            playerThread.start();
    
            // 创建 TTS 客户端（commit 模式）
            // 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime，并在TTSRealtimeClient.java中取消instructions的注释
            TTSRealtimeClient client = new TTSRealtimeClient(
                URL, API_KEY, "Cherry",
                TTSRealtimeClient.SessionMode.COMMIT,
                audioData -> {
                    playbackQueue.add(audioData);
                    audioChunks.add(audioData);
                    System.out.println("收到音频数据: " + audioData.length + " bytes");
                }
            );
    
            client.connect();
    
            // 交互式输入
            System.out.println("请输入文本（直接按Enter发送commit事件并结束本次会话，按Ctrl+D结束程序）：");
            Scanner scanner = new Scanner(System.in);
            while (true) {
                System.out.print("> ");
                if (!scanner.hasNextLine()) {
                    client.finishSession();
                    break;
                }
                String userText = scanner.nextLine();
                if (userText.isEmpty()) {
                    // 空输入：提交缓冲区并结束会话
                    System.out.println("空输入，发送 commit 事件并结束本次会话");
                    client.commitTextBuffer();
                    Thread.sleep(300);
                    client.finishSession();
                    break;
                } else {
                    System.out.println("发送文本: " + userText);
                    client.appendText(userText);
                }
            }
            scanner.close();
    
            // 等待响应完成
            client.waitForResponseDone();
            client.waitForSessionFinished();
            client.close();
    
            // 等待播放完成
            playing.set(false);
            playerThread.join();
            audioLine.drain();
            audioLine.close();
    
            // 保存音频文件
            saveWav("output.wav");
            System.out.println("完成");
        }
    
        private static void saveWav(String filename) throws IOException {
            if (audioChunks.isEmpty()) {
                System.out.println("没有音频数据可保存");
                return;
            }
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            for (byte[] chunk : audioChunks) {
                bos.write(chunk);
            }
            byte[] allAudio = bos.toByteArray();
            AudioFormat format = new AudioFormat(SAMPLE_RATE, 16, 1, true, false);
            AudioInputStream ais = new AudioInputStream(
                new ByteArrayInputStream(allAudio), format, allAudio.length / 2);
            new File("outputs").mkdirs();
            AudioSystem.write(ais, AudioFileFormat.Type.WAVE,
                new File("outputs/" + filename));
            System.out.println("音频已保存到: outputs/" + filename);
        }
    }
    ```
    
    编译并运行`Commit.java`，可多次输入要合成的文本。在未输入文本的情况下单击 Enter 键，将从扬声器听到 Realtime API返回的音频。
    

#### Sambert

#### Go

```
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

const (
	wsURL      = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference" // WebSocket服务器地址
	outputFile = "output.mp3"                                        // 输出文件路径
)

func main() {
	// 若没有将API Key配置到环境变量，可将下行替换为：apiKey := "your_api_key"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")

	// 检查并清空输出文件
	if err := clearOutputFile(outputFile); err != nil {
		fmt.Println("清空输出文件失败：", err)
		return
	}

	// 连接WebSocket服务
	conn, err := connectWebSocket(apiKey)
	if err != nil {
		fmt.Println("连接WebSocket失败：", err)
		return
	}
	defer closeConnection(conn)

	// 创建一个通道用于接收任务完成的通知
	done := make(chan struct{})

	// 启动异步接收消息的goroutine
	go receiveMessage(conn, done)

	// 发送run-task指令
	if err := sendRunTaskMsg(conn); err != nil {
		fmt.Println("发送run-task指令失败：", err)
		return
	}

	// 等待任务完成或超时
	select {
	case <-done:
		fmt.Println("任务结束")
	case <-time.After(5 * time.Minute):
		fmt.Println("任务超时")
	}
}

// 定义消息结构体
type Message struct {
	Header  Header  `json:"header"`
	Payload Payload `json:"payload"`
}

// 定义头部信息
type Header struct {
	Action       string                 `json:"action,omitempty"`
	TaskID       string                 `json:"task_id"`
	Streaming    string                 `json:"streaming,omitempty"`
	Event        string                 `json:"event,omitempty"`
	ErrorCode    string                 `json:"error_code,omitempty"`
	ErrorMessage string                 `json:"error_message,omitempty"`
	Attributes   map[string]interface{} `json:"attributes"`
}

// 定义负载信息
type Payload struct {
	Model      string     `json:"model,omitempty"`
	TaskGroup  string     `json:"task_group,omitempty"`
	Task       string     `json:"task,omitempty"`
	Function   string     `json:"function,omitempty"`
	Input      Input      `json:"input,omitempty"`
	Parameters Parameters `json:"parameters,omitempty"`
	Output     Output     `json:"output,omitempty"`
	Usage      Usage      `json:"usage,omitempty"`
}

// 定义输入信息
type Input struct {
	Text string `json:"text"`
}

// 定义参数信息
type Parameters struct {
	TextType                string  `json:"text_type"`
	Format                  string  `json:"format"`
	SampleRate              int     `json:"sample_rate"`
	Volume                  int     `json:"volume"`
	Rate                    float64 `json:"rate"`
	Pitch                   float64 `json:"pitch"`
	WordTimestampEnabled    bool    `json:"word_timestamp_enabled"`
	PhonemeTimestampEnabled bool    `json:"phoneme_timestamp_enabled"`
}

// 定义输出信息
type Output struct {
	Sentence Sentence `json:"sentence"`
}

// 定义句子信息
type Sentence struct {
	BeginTime int    `json:"begin_time"`
	EndTime   int    `json:"end_time"`
	Words     []Word `json:"words"`
}

// 定义单词信息
type Word struct {
	Text      string    `json:"text"`
	BeginTime int       `json:"begin_time"`
	EndTime   int       `json:"end_time"`
	Phonemes  []Phoneme `json:"phonemes"`
}

// 定义音素信息
type Phoneme struct {
	BeginTime int    `json:"begin_time"`
	EndTime   int    `json:"end_time"`
	Text      string `json:"text"`
	Tone      int    `json:"tone"`
}

// 定义使用信息
type Usage struct {
	Characters int `json:"characters"`
}

func receiveMessage(conn *websocket.Conn, done chan struct{}) {
	for {
		msgType, message, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("解析服务器消息失败：", err)
			close(done)
			break
		}

		if msgType == websocket.BinaryMessage {
			// 处理二进制音频流
			if err := writeBinaryDataToFile(message, outputFile); err != nil {
				fmt.Println("写入二进制数据失败：", err)
				close(done)
				break
			}
			fmt.Println("音频片段已写入本地文件")
		} else {
			// 处理文本消息
			var msg Message
			if err := json.Unmarshal(message, &msg); err != nil {
				fmt.Println("解析事件失败：", err)
				continue
			}
			if handleMessage(conn, msg, done) {
				break
			}
		}
	}
}

func handleMessage(conn *websocket.Conn, msg Message, done chan struct{}) bool {
	switch msg.Header.Event {
	case "task-started":
		fmt.Println("任务已启动")

	case "result-generated":
	// 如需获取附加消息，可在此处添加相应代码

	case "task-finished":
		fmt.Println("任务已完成")
		close(done)
		return true

	case "task-failed":
		if msg.Header.ErrorMessage != "" {
			fmt.Printf("任务失败：%s\n", msg.Header.ErrorMessage)
		} else {
			fmt.Println("未知原因导致任务失败")
		}
		close(done)
		return true

	default:
		fmt.Printf("预料之外的事件：%v\n", msg)
		close(done)
	}

	return false
}

func sendRunTaskMsg(conn *websocket.Conn) error {
	runTaskMsg, err := generateRunTaskMsg()
	if err != nil {
		return err
	}
	if err := conn.WriteMessage(websocket.TextMessage, []byte(runTaskMsg)); err != nil {
		return err
	}
	return nil
}

func generateRunTaskMsg() (string, error) {
	runTaskMessage := Message{
		Header: Header{
			Action:    "run-task",
			TaskID:    uuid.New().String(),
			Streaming: "out",
		},
		Payload: Payload{
			Model:     "sambert-zhichu-v1",
			TaskGroup: "audio",
			Task:      "tts",
			Function:  "SpeechSynthesizer",
			Input: Input{
				Text: "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
			},
			Parameters: Parameters{
				TextType:                "PlainText",
				Format:                  "mp3",
				SampleRate:              16000,
				Volume:                  50,
				Rate:                    1.0,
				Pitch:                   1.0,
				WordTimestampEnabled:    true,
				PhonemeTimestampEnabled: true,
			},
		},
	}

	runTaskMsgJSON, err := json.Marshal(runTaskMessage)
	return string(runTaskMsgJSON), err
}

func connectWebSocket(apiKey string) (*websocket.Conn, error) {
	header := make(http.Header)
	header.Add("X-DashScope-DataInspection", "enable")
	header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))
	conn, _, err := websocket.DefaultDialer.Dial(wsURL, header)
	if err != nil {
		fmt.Println("连接WebSocket失败：", err)
		return nil, err
	}
	return conn, nil
}

func writeBinaryDataToFile(data []byte, filePath string) error {
	file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer file.Close()
	_, err = file.Write(data)
	return err
}

func closeConnection(conn *websocket.Conn) {
	if conn != nil {
		conn.Close()
	}
}

func clearOutputFile(filePath string) error {
	file, err := os.OpenFile(filePath, os.O_TRUNC|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	file.Close()
	return nil
}
```

#### C#

示例代码如下：

```
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

class Program {
    // 若没有将API Key配置到环境变量，可将下行替换为：private const string ApiKey="your_api_key"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

    private const string WebSocketUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"; // WebSocket服务器地址
    private const string OutputFilePath = "output.mp3"; // 输出文件路径

    static async Task Main(string[] args) {
        var ws = new ClientWebSocket();
        try {
            // 1. 连接WebSocket服务，鉴权
            await ConnectWithAuth(ws, WebSocketUrl);

            // 2. 启动接收消息的线程
            var receiveTask = ReceiveMessages(ws);

            // 3. 发送run-task指令
            string textToSynthesize = "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。";
            string taskId = GenerateTaskId();
            await SendRunTaskCommand(ws, textToSynthesize, taskId);

            // 4. 等待接收任务完成
            await receiveTask;
        } catch (Exception ex) {
            Console.WriteLine($"错误：{ex.Message}");
        } finally {
            if (ws.State == WebSocketState.Open) {
                await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, "关闭连接", CancellationToken.None);
            }
        }
    }

    private static async Task ConnectWithAuth(ClientWebSocket ws, string url) {
        var uri = new Uri(url);
        ws.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
        ws.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");
        await ws.ConnectAsync(uri, CancellationToken.None);
        Console.WriteLine("已连接到WebSocket服务器。");
    }

    private static string GenerateTaskId() {
        return Guid.NewGuid().ToString("N");
    }

    private static async Task SendRunTaskCommand(ClientWebSocket ws, string text, string taskId) {
        var command = CreateRunTaskCommand(text, taskId);
        var buffer = Encoding.UTF8.GetBytes(command);
        await ws.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, CancellationToken.None);
        Console.WriteLine("已发送run-task指令。");
    }

    private static string CreateRunTaskCommand(string text, string taskId) {
        var command = new {
            header = new {
                action = "run-task",
                task_id = taskId,
                streaming = "out"
            },
            payload = new {
                model = "sambert-zhichu-v1",
                task_group = "audio",
                task = "tts",
                function = "SpeechSynthesizer",
                input = new {
                    text = text
                },
                parameters = new {
                    text_type = "PlainText",
                    format = "mp3",
                    sample_rate = 16000,
                    volume = 50,
                    rate = 1,
                    pitch = 1,
                    word_timestamp_enabled = true,
                    phoneme_timestamp_enabled = true
                }
            }
        };
        return JsonSerializer.Serialize(command);
    }

    private static async Task ReceiveMessages(ClientWebSocket ws) {
        var buffer = new byte[1024 * 4];
        var fs = new FileStream(OutputFilePath, FileMode.Create, FileAccess.Write);
        bool taskStarted = false;
        bool taskFinished = false;

        while (ws.State == WebSocketState.Open && !taskFinished) {
            var result = await ws.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);

            switch (result.MessageType) {
                case WebSocketMessageType.Text:
                    var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    var jsonMessage = JsonSerializer.Deserialize<JsonElement>(message);

                    ProcessTextMessage(jsonMessage, ref taskStarted, ref taskFinished);
                    break;
                case WebSocketMessageType.Binary:
                    if (taskStarted) {
                        await fs.WriteAsync(buffer, 0, result.Count);
                        Console.WriteLine("收到音频数据。");
                    }
                    break;
                case WebSocketMessageType.Close:
                    Console.WriteLine("服务器关闭了连接。");
                    taskFinished = true;
                    break;
            }
        }
        fs.Close();
    }

    private static void ProcessTextMessage(JsonElement jsonMessage, ref bool taskStarted, ref bool taskFinished) {
        if (jsonMessage.TryGetProperty("header", out JsonElement header) && header.TryGetProperty("event", out JsonElement eventToken)) {
            var eventType = eventToken.GetString();
            switch (eventType) {
                case "task-started":
                    taskStarted = true;
                    Console.WriteLine("任务开始。");
                    break;
                case "result-generated":
                    // 如需获取附加消息，可在此处添加相应代码
                    break;
                case "task-finished":
                    taskFinished = true;
                    Console.WriteLine("任务完成。");
                    break;
                case "task-failed":
                    taskFinished = true;
                    Console.WriteLine("任务失败。");
                    break;
            }
        }
    }
}
```

#### PHP

示例代码目录结构为：

my-php-project/

├── composer.json

├── vendor/

└── index.php

composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

```
{
    "require": {
        "react/event-loop": "^1.3",
        "react/socket": "^1.11",
        "react/stream": "^1.2",
        "react/http": "^1.1",
        "ratchet/pawl": "^0.4"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

index.php内容如下：

```
<?php

require 'vendor/autoload.php';

use Ratchet\Client\Connector;
use React\EventLoop\Loop;
use React\Socket\Connector as SocketConnector;

# 若没有将API Key配置到环境变量，可将下行替换为：$api_key="your_api_key"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$websocket_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
$output_file = 'output.mp3'; // 输出文件路径

$loop = Loop::get();

if (file_exists($output_file)) {
    // 清空文件内容
    file_put_contents($output_file, '');
    echo "文件已清空\n";
}

// 创建自定义的连接器
$socketConnector = new SocketConnector($loop, [
    'tcp' => [
        'bindto' => '0.0.0.0:0',
    ],
    // 警告：关闭 TLS 证书校验存在中间人攻击风险，仅限本地调试；生产环境务必将 verify_peer/verify_peer_name 设为 true
    'tls' => [
        'verify_peer' => false,
        'verify_peer_name' => false,
    ],
]);

$connector = new Connector($loop, $socketConnector);

$headers = [
    'Authorization' => 'bearer ' . $api_key,
    'X-DashScope-DataInspection' => 'enable'
];

// 连接WebSocket服务
$connector($websocket_url, [], $headers)
    ->then(function ($conn) use ($output_file) {
        echo "连接成功\n";

        // 异步接收WebSocket消息
        $conn->on('message', function ($msg) use ($conn, $output_file) {
            if ($msg->isBinary()) {
                // 写入二进制数据到本地文件
                file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
                echo "二进制数据写入文件\n";
            } else {
                $data = json_decode($msg, true);
                switch ($data['header']['event']) {
                    case 'task-started':
                        echo "任务开始\n";
                        break;
                    case 'result-generated':
                        // 如需获取附加消息，可在此处添加相应代码
                        break;
                    case 'task-finished':
                        echo "任务完成\n";
                        $conn->close();
                        break;
                    case 'task-failed':
                        echo "任务失败：" . $data['header']['error_message'] . "\n";
                        $conn->close();
                        break;
                    default:
                        echo "未知事件：" . $msg . "\n";
                }
            }
        });

        // 监听连接关闭
        $conn->on('close', function($code = null, $reason = null) {
            echo "连接已关闭\n";
            if ($code !== null) {
                echo "关闭代码：" . $code . "\n";
            }
            if ($reason !== null) {
                echo "关闭原因：" . $reason . "\n";
            }
        });

        // 发送run-task指令
        $conn->send(json_encode([
            'header' => [
                'action' => 'run-task',
                'task_id' => bin2hex(random_bytes(16)),
                'streaming' => 'out'
            ],
            'payload' => [
                'model' => 'sambert-zhichu-v1',
                'task_group' => 'audio',
                'task' => 'tts',
                'function' => 'SpeechSynthesizer',
                'input' => [
                    'text' => '床前明月光，疑是地上霜。举头望明月，低头思故乡。'
                ],
                'parameters' => [
                    'text_type' => 'PlainText',
                    'format' => 'mp3',
                    'sample_rate' => 16000,
                    'volume' => 50,
                    'rate' => 1,
                    'pitch' => 1,
                    'word_timestamp_enabled' => true,
                    'phoneme_timestamp_enabled' => true
                ]
            ]
        ]));
        echo "run-task指令已发送\n";
    }, function (Exception $e) {
        echo "连接失败：{$e->getMessage()}\n";
        file_put_contents('error.log', $e->getMessage() . "\n", FILE_APPEND);
    });

$loop->run();
```

#### Node.js

需安装相关依赖：

```
npm install ws
npm install uuid
```

示例代码如下：

```
const WebSocket = require('ws');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

// 若没有将API Key配置到环境变量，可将下行替换为：apiKey = 'your_api_key'。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
const apiKey = process.env.DASHSCOPE_API_KEY;
const wsUrl = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
const outputFilePath = 'output.mp3'; // 替换为您的音频文件路径

async function main() {
  await checkAndClearOutputFile(outputFilePath);
  createWebSocketConnection();
}

const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
function createWebSocketConnection() {
  const ws = new WebSocket(wsUrl, {
    headers: {
      Authorization: `bearer ${apiKey}`,
      'X-DashScope-DataInspection': 'enable'
    }
  });

  ws.on('open', () => {
    console.log('已连接到WebSocket服务器');
    sendRunTaskMessage(ws);
  });

  ws.on('message', (data, isBinary) => handleWebSocketMessage(data, isBinary, ws));
  ws.on('error', (error) => console.error('WebSocket错误:', error));
  ws.on('close', () => console.log('WebSocket连接已关闭'));

  return ws;
}

function sendRunTaskMessage(ws) {
  const taskId = uuidv4();
  const runTaskMessage = {
    header: {
      action: 'run-task',
      task_id: taskId,
      streaming: 'out'
    },
    payload: {
      model: 'sambert-zhichu-v1',
      task_group: 'audio',
      task: 'tts',
      function: 'SpeechSynthesizer',
      input: {
        text: '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。'
      },
      parameters: {
        text_type: 'PlainText',
        format: 'mp3',
        sample_rate: 16000,
        volume: 50,
        rate: 1,
        pitch: 1,
        word_timestamp_enabled: true,
        phoneme_timestamp_enabled: true
      }
    }
  };
  ws.send(JSON.stringify(runTaskMessage));
  console.log('run-task指令已发送');
}

function handleWebSocketMessage(data, isBinary, ws) {
  if (isBinary) {
    fileStream.write(data);
  } else {
    const message = JSON.parse(data);
    handleWebSocketEvent(message, ws);
  }
}

function handleWebSocketEvent(message, ws) {
  switch (message.header.event) {
    case 'task-started':
      console.log('任务已启动');
      break;
    case 'result-generated':
      console.log('结果已生成');
      break;
    case 'task-finished':
      console.log('任务已完成');
      ws.close();
      fileStream.end(() => {
        console.log('文件流已关闭');
      });
      break;
    case 'task-failed':
      console.error('任务失败：', message.header.error_message);
      ws.close();
      fileStream.end(() => {
        console.log('文件流已关闭');
      });
      break;
    default:
      console.log('未知事件：', message.header.event);
  }
}

function checkAndClearOutputFile(filePath) {
  return new Promise((resolve, reject) => {
    fs.access(filePath, fs.F_OK, (err) => {
      if (!err) {
        fs.truncate(filePath, 0, (truncateErr) => {
          if (truncateErr) return reject(truncateErr);
          console.log('文件已清空');
          resolve();
        });
      } else {
        fs.open(filePath, 'w', (openErr) => {
          if (openErr) return reject(openErr);
          console.log('文件已创建');
          resolve();
        });
      }
    });
  });
}

main().catch(console.error);
```

## 应用于生产环境

### 连接复用（WebSocket）

WebSocket 连接支持复用：一个合成任务结束后，无需重新建立连接即可开启下一个任务。

**复用流程**：

-   **Qwen-Audio-TTS** / **CosyVoice/ Sambert**：客户端发送 `finish-task`，服务端返回 `task-finished` 后，可重新发送 `run-task` 开启新任务。
-   **Qwen-TTS**：客户端发送 `session.finish`，服务端返回 `session.finished` 后，可建立新会话开启下一个任务。

**取消任务后复用**：对于 Qwen-Audio-TTS / CosyVoice，如果使用 `cancel` 指令取消当前任务，服务端返回 `task-finished` 后，同样可以在当前连接上重新发送 `run-task` 开启新任务。详情请参见[取消任务](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#rt_cancel_h3)。

**重要**

1.  必须等服务端返回结束事件（`task-finished` 或 `session.finished`）后才可发起新任务。
2.  Qwen-Audio-TTS、CosyVoice 和 Sambert 在复用连接中的不同任务需要使用不同的 `task_id`。
3.  任务失败时服务端返回错误事件并关闭连接，该连接不可复用。
4.  任务结束后 60 秒无新任务，连接自动断开。

各模型事件说明请参见对应的[API参考](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#e52d8b91d3qsk)。

### 模型限流

模型调用受限流规则约束，超出限制时服务端返回 `Requests rate limit exceeded, please try again later.` 报错，需降低调用频率或并发数后重试。

各模型的限流条件请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 高并发最佳实践

DashScope SDK 内置池化机制，可复用 WebSocket 连接和合成对象，避免频繁创建销毁带来的开销。

点击查看高并发最佳实践

#### Qwen-Audio-TTS/CosyVoice

Qwen-Audio-TTS 和 CosyVoice 使用相同的 SDK 接口，以下示例同样适用于 Qwen-Audio-TTS 系列模型，只需替换 `model` 和 `voice` 参数。

#### 前提条件

-   [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
    
-   已安装符合版本要求的DashScope SDK，建议[安装最新版](raw/model-api-reference/preparations/install-sdk.md)：
    
    -   Python SDK：版本≥1.25.2
    -   Java SDK：版本≥2.16.6

#### Python SDK

Python SDK 通过 `SpeechSynthesizerObjectPool` 管理和复用 `SpeechSynthesizer` 对象。

对象池在初始化时即创建指定数量的 `SpeechSynthesizer` 实例并建立 WebSocket 连接，获取对象时可直接发起请求，降低首包延迟。归还后连接保持活跃，等待下次复用。

#### 实现步骤

1.  安装依赖：安装DashScope依赖（`pip install -U dashscope`）
    
2.  创建并配置对象池
    
    对象池大小推荐设为峰值并发数的 1.5~2 倍，且不应超过账户的 QPS 限制。
    
    创建全局单例对象池（初始化时建立连接，有一定耗时）：
    

```
from dashscope.audio.tts_v2 import SpeechSynthesizerObjectPool

connectionPool = SpeechSynthesizerObjectPool(max_size=20)
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
```

**重要**

-   在对象池场景中，`SpeechSynthesizerObjectPool`在初始化时即按当前全局`dashscope.api_key`与服务端建立 WebSocket 连接。apiKey 仅在 WebSocket 建连握手时写入`Authorization`请求头用于鉴权，后续任务消息（如`run-task`）本身不携带 apiKey。**池创建后修改**`dashscope.api_key`**不会影响池内已建连接**——`borrow_synthesizer`取出的对象（包括归还后再次复用的对象）仍使用握手时的 apiKey，新值会被静默忽略，可能导致身份、配额或计费归属与预期不一致。注意：`borrow_synthesizer`也不支持通过参数指定 apiKey。
-   如确需使用多个不同的 API Key，请为每个 API Key 维护**独立的**`SpeechSynthesizerObjectPool`**实例**。

3.  从对象池中获取`SpeechSynthesizer`对象
    
    如果当前未归还的对象数已超过池容量，系统会额外创建新对象。
    
    此类对象需重新建立连接，不具备复用效果。
    

```
speech_synthesizer = connectionPool.borrow_synthesizer(
    model='cosyvoice-v3-flash',
    voice='longanyang',
    seed=12382,
    callback=synthesizer_callback
)
```

4.  进行语音合成
    
    调用`SpeechSynthesizer`对象的call或streaming\_call方法进行语音合成。
    
5.  归还`SpeechSynthesizer`对象
    
    任务结束后归还对象以供复用。
    
    不要归还未完成任务或任务失败的对象。
    

```
connectionPool.return_synthesizer(speech_synthesizer)
```

##### 完整代码

**重要**复制使用前请注意：`SpeechSynthesizerObjectPool`在初始化时即按当前全局`dashscope.api_key`与服务端建立 WebSocket 连接并完成鉴权；**池创建后再修改**`dashscope.api_key`**不会影响池内已建连接**，新值会被静默忽略。多 API Key 场景请为每个 API Key 维护独立的池实例。详见上文重要说明。

```
# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import time
import threading

import dashscope
from dashscope.audio.tts_v2 import *

USE_CONNECTION_POOL = True
text_to_synthesize = [
    '第一句、欢迎使用阿里巴巴语音合成服务。',
    '第二句、欢迎使用阿里巴巴语音合成服务。',
    '第三句、欢迎使用阿里巴巴语音合成服务。',
]
connectionPool = None

def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually

def synthesis_text_to_speech_and_play_by_streaming_mode(text, task_id):
    global USE_CONNECTION_POOL, connectionPool
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''

    complete_event = threading.Event()

    # Define a callback to handle the result

    class Callback(ResultCallback):
        def on_open(self):
            # when using object pool, on_open will be called after task start
            self.file = open(f'result_{task_id}.mp3', 'wb')
            print(f'[task_{task_id}] start')

        def on_complete(self):
            print(f'[task_{task_id}] speech synthesis task complete successfully.')
            complete_event.set()

        def on_error(self, message: str):
            print(f'[task_{task_id}] speech synthesis task failed, {message}')

        def on_close(self):
            # when using object pool, on_close will be called after task finished
            print(f'[task_{task_id}] finished')

        def on_event(self, message):
            # print(f'recv speech synthsis message {message}')
            pass

        def on_data(self, data: bytes) -> None:
            # send to player
            # save audio to file
            self.file.write(data)

    # Call the speech synthesizer callback
    synthesizer_callback = Callback()

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    if USE_CONNECTION_POOL:
        speech_synthesizer = connectionPool.borrow_synthesizer(
            model='cosyvoice-v3-flash',
            voice='longanyang',
            seed=12382,
            callback=synthesizer_callback
        )
    else:
        speech_synthesizer = SpeechSynthesizer(model='cosyvoice-v3-flash',
                                               voice='longanyang',
                                               seed=12382,
                                               callback=synthesizer_callback)
    try:
        speech_synthesizer.call(text)
    except Exception as e:
        print(f'[task_{task_id}] speech synthesis task failed, {e}')
        if USE_CONNECTION_POOL:
            # close the synthesizer connection manually if task failed when using connection pool.
            speech_synthesizer.close()
        return

    print('[task_{}] Synthesized text: {}'.format(task_id, text))
    complete_event.wait()
    print('[task_{}][Metric] requestId: {}, first package delay ms: {}'.format(
        task_id,
        speech_synthesizer.get_last_request_id(),
        speech_synthesizer.get_first_package_delay()))
    if USE_CONNECTION_POOL:
        connectionPool.return_synthesizer(speech_synthesizer)

# main function
if __name__ == '__main__':
    # 必须先设置 dashscope.api_key 和 base_websocket_api_url，再创建 SpeechSynthesizerObjectPool。
    # 池在初始化时即按当前全局 dashscope.api_key 建立 WebSocket 连接，
    # 池创建后再修改 dashscope.api_key 不会影响池内已建连接。
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'
    init_dashscope_api_key()

    if USE_CONNECTION_POOL:
        print('creating connection pool')
        start_time = time.time() * 1000
        connectionPool = SpeechSynthesizerObjectPool(max_size=3)
        end_time = time.time() * 1000
        print('connection pool created, cost: {} ms'.format(end_time - start_time))

    task_thread_list = []
    for task_id in range(3):
        thread = threading.Thread(
            target=synthesis_text_to_speech_and_play_by_streaming_mode,
            args=(text_to_synthesize[task_id], task_id))
        task_thread_list.append(thread)

    for task_thread in task_thread_list:
        task_thread.start()

    for task_thread in task_thread_list:
        task_thread.join()

    if USE_CONNECTION_POOL:
        connectionPool.shutdown()
```

#### 资源管理与异常处理

-   任务成功：当语音合成任务正常完成时，必须调用 `connectionPool.return_synthesizer(speech_synthesizer)` 将 `SpeechSynthesizer` 对象归还到池中，以便复用。
    
    **重要**不要归还未完成任务或任务失败的`SpeechSynthesizer`对象。
    
-   任务失败：当 SDK 内部或业务逻辑抛出异常导致任务中断时，主动关闭底层的 WebSocket 连接：`speech_synthesizer.close()`
    
-   在所有语音合成任务完成后，要通过如下方式关闭对象池：`connectionPool.shutdown()`。
    
-   在服务出现TaskFailed报错时，不需要额外处理。
    

#### Java SDK

Java SDK通过内置的连接池和自定义的对象池协同工作，实现最佳性能。

-   连接池：SDK 内部集成的 OkHttp3 连接池，负责管理和复用底层的 WebSocket 连接，减少网络握手开销。此功能默认开启。
-   对象池：基于 `commons-pool2` 实现，用于维护一组已预先建立好连接的 `SpeechSynthesizer` 对象。从池中获取对象可消除连接建立的延迟，显著降低首包延迟。

#### 实现步骤

1.  添加依赖
    
    根据项目构建工具，在依赖配置文件中添加 dashscope-sdk-java 和 commons-pool2。
    
    以Maven和Gradle为例，配置如下：
    
    #### Maven
    
    1.  打开Maven项目的`pom.xml`文件。
    2.  在`<dependencies>`标签内添加以下依赖信息。
    
    ```
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <!-- 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
        <version>the-latest-version</version>
    </dependency>
    
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-pool2</artifactId>
        <!-- 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2 -->
        <version>the-latest-version</version>
    </dependency>
    ```
    
    1.  保存`pom.xml`文件。
    2.  使用Maven命令（如`mvn clean install`或`mvn compile`）来更新项目依赖
    
    #### Gradle
    
    1.  打开Gradle项目的`build.gradle`文件。
    2.  在`dependencies`块内添加以下依赖信息。
    
    ```
    dependencies {
        // 请将 'the-latest-version' 替换为2.16.6及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    
        // 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2
        implementation group: 'org.apache.commons', name: 'commons-pool2', version: 'the-latest-version'
    }
    ```
    
    3.  保存`build.gradle`文件。
    4.  在命令行中，切换到项目根目录，执行以下Gradle命令来更新项目依赖。
    
    ```
    ./gradlew build --refresh-dependencies
    ```
    
    或者，如果使用Windows系统，命令应为：
    
    ```
    gradlew build --refresh-dependencies
    ```
    
2.  配置连接池
    
    通过环境变量配置连接池关键参数：
    

**环境变量**

**描述**

DASHSCOPE\_CONNECTION\_POOL\_SIZE

连接池大小。

推荐值：峰值并发数的 2 倍以上。

默认值：32。

DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS

最大异步请求数。

推荐值：与 `DASHSCOPE_CONNECTION_POOL_SIZE` 保持一致。

默认值：32。

DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS\_PER\_HOST

单主机最大异步请求数。

推荐值：与 `DASHSCOPE_CONNECTION_POOL_SIZE` 保持一致。

默认值：32。

3.  配置对象池
    
    通过环境变量配置对象池大小：
    

**环境变量**

**描述**

COSYVOICE\_OBJECTPOOL\_SIZE

对象池大小。

推荐值：峰值并发数的 1.5 至 2 倍。

默认值：500。

**重要**

-   对象池的大小（`COSYVOICE_OBJECTPOOL_SIZE`）必须小于或等于连接池的大小（`DASHSCOPE_CONNECTION_POOL_SIZE`）。否则，当对象池请求对象时，若连接池已满，会导致调用线程阻塞，等待可用连接。
-   对象池大小不应超过账户的 QPS（每秒查询率）限制。

通过如下代码创建对象池：

```
class CosyvoiceObjectPool {
    // 。。。这里省略其它代码，完整示例请参见完整代码
    public static GenericObjectPool<SpeechSynthesizer> getInstance() {
        lock.lock();
        if (synthesizerPool == null) {
            // 您可以在这里设置对象池的大小。或在环境变量COSYVOICE_OBJECTPOOL_SIZE中设置。
            // 建议设置为服务器最大并发连接数的1.5到2倍。
            int objectPoolSize = getObjectivePoolSize();
            SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                    new SpeechSynthesizerObjectFactory();
            GenericObjectPoolConfig<SpeechSynthesizer> config =
                    new GenericObjectPoolConfig<>();
            config.setMaxTotal(objectPoolSize);
            config.setMaxIdle(objectPoolSize);
            config.setMinIdle(objectPoolSize);
            synthesizerPool =
                    new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
        }
        lock.unlock();
        return synthesizerPool;
    }
}
```

4.  从对象池中获取`SpeechSynthesizer`对象
    
    如果当前未归还的对象数量已超过对象池的最大容量，系统会额外创建一个新的`SpeechSynthesizer`对象。
    
    此类新创建的对象需要重新进行初始化并建立 WebSocket 连接，无法利用对象池的既有连接资源，因此不具备复用效果。
    

```
synthesizer = CosyvoiceObjectPool.getInstance().borrowObject();
```

5.  进行语音合成
    
    从对象池借出`SpeechSynthesizer`对象后，需先调用`updateParamAndCallback(param, callback)`关联本次任务的参数与回调，再调用`streamingCall`或`call`方法进行语音合成。
    
    **重要**
    
    -   在对象池场景中，`updateParamAndCallback`会被**多次调用**（每次借出对象时都需调用一次，用于切换该次任务的回调和任务级参数，如`voice`、`format`等）。**多次调用时传入的**`apiKey`**必须始终相同**。`updateParamAndCallback`只更新当前`SpeechSynthesizer`实例的本地字段，不会重建底层 WebSocket 连接；而 SDK 仅在 WebSocket 建连握手时将`apiKey`写入`Authorization`请求头用于鉴权，后续任务消息（如`run-task`）本身不携带`apiKey`。因此只要复用的连接未断开，传入新的`apiKey`不会被发送到服务端，请求实际仍会使用连接首次握手时的`apiKey`，可能导致身份、配额或计费归属与预期不一致。
    -   如确需使用多个不同的 API Key，请为每个 API Key 维护**独立的对象池实例**。
    
6.  归还`SpeechSynthesizer`对象
    
    语音合成任务结束后，归还`SpeechSynthesizer`对象，以便后续任务可以复用该对象。
    
    不要归还未完成任务或任务失败的对象。
    

```
CosyvoiceObjectPool.getInstance().returnObject(synthesizer);
```

##### 完整代码

**重要**复制使用前请注意：对象池场景下多次调用`updateParamAndCallback`时传入的 apiKey**必须始终相同**——SDK 不会更新已建立连接的 apiKey，传入不同的 apiKey 不会生效。多 API Key 场景请为每个 API Key 维护独立的对象池实例。详见上文重要说明。

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.time.LocalDateTime;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;

/**
 * 您需要在项目中引入org.apache.commons.pool2和DashScope相关的包。
 *
 * DashScope SDK 2.16.6及后续版本针对高并发场景进行了优化，
 * DashScope SDK 2.16.6之前的版本不推荐在高并发场景下使用。
 *
 *
 * 在对TTS服务进行高并发调用之前，
 * 请通过以下环境变量配置连接池的相关参数。
 *
 * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS
 * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST
 * DASHSCOPE_CONNECTION_POOL_SIZE
 *
 */

class SpeechSynthesizerObjectFactory
        extends BasePooledObjectFactory<SpeechSynthesizer> {
    public SpeechSynthesizerObjectFactory() {
        super();
    }
    @Override
    public SpeechSynthesizer create() throws Exception {
        return new SpeechSynthesizer();
    }

    @Override
    public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
        return new DefaultPooledObject<>(obj);
    }
}

class CosyvoiceObjectPool {
    public static GenericObjectPool<SpeechSynthesizer> synthesizerPool;
    public static String COSYVOICE_OBJECTPOOL_SIZE_ENV = "COSYVOICE_OBJECTPOOL_SIZE";
    public static int DEFAULT_OBJECT_POOL_SIZE = 500;
    private static Lock lock = new java.util.concurrent.locks.ReentrantLock();
    public static int getObjectivePoolSize() {
        try {
            Integer n = Integer.parseInt(System.getenv(COSYVOICE_OBJECTPOOL_SIZE_ENV));
            System.out.println("Using Object Pool Size In Env: "+ n);
            return n;
        } catch (NumberFormatException e) {
            System.out.println("Using Default Object Pool Size: "+ DEFAULT_OBJECT_POOL_SIZE);
            return DEFAULT_OBJECT_POOL_SIZE;
        }
    }
    public static GenericObjectPool<SpeechSynthesizer> getInstance() {
        lock.lock();
        if (synthesizerPool == null) {
            // 您可以在这里设置对象池的大小。或在环境变量COSYVOICE_OBJECTPOOL_SIZE中设置。
            // 建议设置为服务器最大并发连接数的1.5到2倍。
            int objectPoolSize = getObjectivePoolSize();
            SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                    new SpeechSynthesizerObjectFactory();
            GenericObjectPoolConfig<SpeechSynthesizer> config =
                    new GenericObjectPoolConfig<>();
            config.setMaxTotal(objectPoolSize);
            config.setMaxIdle(objectPoolSize);
            config.setMinIdle(objectPoolSize);
            synthesizerPool =
                    new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
        }
        lock.unlock();
        return synthesizerPool;
    }
}

class SynthesizeTaskWithCallback implements Runnable {
    String[] textArray;
    String requestId;
    long timeCost;
    public SynthesizeTaskWithCallback(String[] textArray) {
        this.textArray = textArray;
    }
    @Override
    public void run() {
        SpeechSynthesizer synthesizer = null;
        long startTime = System.currentTimeMillis();
        // if recv onError
        final boolean[] hasError = {false};
        try {
            class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
                ReactCallback() {}

                @Override
                public void onEvent(SpeechSynthesisResult message) {
                    if (message.getAudioFrame() != null) {
                        try {
                            byte[] bytesArray = message.getAudioFrame().array();
                            System.out.println("收到音频，音频文件流length为：" + bytesArray.length);
                        } catch (Exception e) {
                            throw new RuntimeException(e);
                        }
                    }
                }

                @Override
                public void onComplete() {}

                @Override
                public void onError(Exception e) {
                    System.out.println(e.getMessage());
                    e.printStackTrace();
                    hasError[0] = true;
                }
            }

            SpeechSynthesisParam param =
                    SpeechSynthesisParam.builder()
                            .model("cosyvoice-v3-flash")
                            .voice("longanyang")
                            // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                            // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                            .format(SpeechSynthesisAudioFormat
                                    .MP3_22050HZ_MONO_256KBPS) // 流式合成使用PCM或者MP3
                            .build();

            try {
                synthesizer = CosyvoiceObjectPool.getInstance().borrowObject();
                // 注意：对象池场景下，多次调用 updateParamAndCallback 时传入的 apiKey 必须始终相同；SDK 不会更新已建立连接的 apiKey，传入不同的 apiKey 不会生效。详见上文“进行语音合成”步骤的重要说明。
                synthesizer.updateParamAndCallback(param, new ReactCallback());
                for (String text : textArray) {
                    synthesizer.streamingCall(text);
                }
                Thread.sleep(20);
                synthesizer.streamingComplete(60000);
                requestId = synthesizer.getLastRequestId();
            } catch (Exception e) {
                System.out.println("Exception e: " + e.toString());
                hasError[0] = true;
            }
        } catch (Exception e) {
            hasError[0] = true;
            throw new RuntimeException(e);
        }
        if (synthesizer != null) {
            try {
                if (hasError[0] == true) {
                    // 如果出现异常，则关闭连接并在对象池中禁用该对象。
                    synthesizer.getDuplexApi().close(1000, "bye");
                    CosyvoiceObjectPool.getInstance().invalidateObject(synthesizer);
                } else {
                    // 如果任务正常结束，则归还对象。
                    CosyvoiceObjectPool.getInstance().returnObject(synthesizer);
                }
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
            long endTime = System.currentTimeMillis();
            timeCost = endTime - startTime;
            System.out.println("[线程 " + Thread.currentThread() + "] 语音合成任务结束。耗时 " + timeCost + " ms, RequestId " + requestId);
        }
    }
}

@Slf4j
public class SynthesizeTextToSpeechWithCallbackConcurrently {
    public static void checkoutEnv(String envName, int defaultSize) {
        if (System.getenv(envName) != null) {
            System.out.println("[ENV CHECK]: " + envName + " "
                    + System.getenv(envName));
        } else {
            System.out.println("[ENV CHECK]: " + envName
                    + " Using Default which is " + defaultSize);
        }
    }

    public static void main(String[] args)
            throws InterruptedException, NoApiKeyException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        // Check for connection pool env
        checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);
        checkoutEnv(CosyvoiceObjectPool.COSYVOICE_OBJECTPOOL_SIZE_ENV, CosyvoiceObjectPool.DEFAULT_OBJECT_POOL_SIZE);

        int runTimes = 3;
        // Create the pool of SpeechSynthesis objects
        ExecutorService executorService = Executors.newFixedThreadPool(runTimes);

        for (int i = 0; i < runTimes; i++) {
            // Record the task submission time
            LocalDateTime submissionTime = LocalDateTime.now();
            executorService.submit(new SynthesizeTaskWithCallback(new String[] {
                    "床前明月光，", "疑似地上霜。", "举头望明月，", "低头思故乡。"}));
        }

        // Shut down the ExecutorService and wait for all tasks to complete
        executorService.shutdown();
        executorService.awaitTermination(1, TimeUnit.MINUTES);
        System.exit(0);
    }
}
```

#### 推荐配置

以下配置基于在指定规格的阿里云服务器上仅运行 CosyVoice 语音合成服务的测试结果。过高的并发数可能导致任务处理延迟。

其中单机并发数指的是同一时刻正在运行的CosyVoice语音合成任务数，也可以理解为工作线程数。

**机器配置（阿里云）**

**单机最大并发数**

**对象池大小**

**连接池大小**

4核8GiB

100

500

2000

8核16GiB

150

500

2000

16核32GiB

200

500

2000

#### 资源管理与异常处理

-   任务成功：当语音合成任务正常完成时，必须调用GenericObjectPool的returnObject方法将`SpeechSynthesizer`对象归还到池中，以便复用。
    
    在当前代码中，对应`CosyvoiceObjectPool.getInstance().returnObject(synthesizer)`
    
    **重要**不要归还未完成任务或任务失败的`SpeechSynthesizer`对象。
    
-   任务失败：当 SDK 内部或业务逻辑抛出异常导致任务中断时，必须执行以下两个操作：
    
    1.  主动关闭底层的 WebSocket 连接
    2.  从对象池中废弃该对象，防止被再次使用

```
// 在当前代码中对应如下内容
// 关闭连接
synthesizer.getDuplexApi().close(1000, "bye");
// 在对象池中废弃出现异常的synthesizer
CosyvoiceObjectPool.getInstance().invalidateObject(synthesizer);
```

-   在服务出现TaskFailed报错时，不需要额外处理。

#### 调用预热与耗时统计说明

在对 DashScope Java SDK 进行并发调用延迟等性能评估时，建议先执行充分的预热操作，确保测量结果反映稳定状态下的真实性能，避免初始连接耗时导致数据偏差。

##### 连接复用机制

DashScope Java SDK 通过全局单例的连接池高效管理和复用 WebSocket 连接，旨在减少频繁建连和断连的开销，提升高并发场景下的处理能力。

该机制的工作特点如下：

-   **按需创建**：SDK 不会在服务启动时预创建 WebSocket 连接，而是在首次调用时按需建立。
    
-   **限时复用**：请求完成后，连接将在池中保留最多 60 秒以备复用。
    
    -   若 60 秒内有新请求，将复用现有连接，避免重复握手开销。
    -   若连接空闲超过 60 秒，将被自动关闭以释放资源。

##### 预热的重要性

在以下场景中，连接池中可能没有可复用的活跃连接，导致请求需要新建连接：

-   应用刚启动，尚未发起任何调用。
-   服务空闲时间超过 60 秒，池中连接已因超时而关闭。

在这些场景下，首次请求需完成 WebSocket 建连（TCP 握手、TLS 协商、协议升级），延迟显著高于后续复用连接的请求。若未预热，性能测试结果会因包含建连耗时而产生偏差。

##### SDK侧延迟与实际首包延迟的区别

SDK侧打印的首包延迟（如通过 `get_first_package_delay()` 获取的值）包含了 WebSocket 建联和网络传输等耗时，并不等同于模型服务的实际首包延迟。

实际首包延迟是指从服务端收到 `run-task` 指令到返回第一个 `result-generated` 事件的时间间隔，该值可通过服务端日志查看。

在高并发场景下，由于大量连接的建立和资源调度，SDK侧打印的延迟数值可能显著高于服务端的实际首包延迟。如果观察到 SDK 报告的首包延迟较高，建议：

-   对比服务端日志中的首包延迟（从 `run-task` 到首个 `result-generated`），确认模型推理性能是否正常。
-   使用上述对象池或连接池机制进行预热，消除 WebSocket 建连开销，使 SDK 侧打印的延迟更接近实际首包延迟。

##### 推荐做法

为获取可靠的性能数据，在正式进行性能压测或延迟统计前，请遵循以下预热步骤：

1.  模拟正式测试的并发级别，提前发起一定数量的调用（例如，持续 1-2 分钟），以充分填充连接池。
2.  确认连接池已建立并维持足够的活跃连接后，再开始正式的性能数据采集。

通过合理的预热，可使 SDK 连接池进入稳定复用状态，从而测量出更具代表性的延迟指标，真实反映服务在线上平稳运行时的性能。

#### Java SDK常见异常

异常 1、 业务流量平稳，但是服务器 TCP 连接数持续上升

**出错原因：****类型一：**

每一个 SDK 对象创建时都会申请一个连接。如果没有使用对象池，每一次任务结束后对象都被析构。此时这一个连接将进入无引用状态，需要等待 61s 秒后服务端报错连接超时才会真正断开，这会导致这个连接在 61 秒内不可复用。

在高并发场景下，新的任务在发现没有可复用连接时会创建新连接，会造成如下后果：

1.  连接数持续上升。
2.  由于连接数过多，服务器资源不足，服务器卡顿。
3.  连接池被打满、新任务由于启动时需要等待可用连接而阻塞。

**类型二：**

对象池配置的MaxIdle小于MaxTotal，导致在对象闲置时，超过MaxIdle的对象被销毁，从而造成连接泄漏。泄漏的连接需要等待61秒超时后断连，同类型一造成连接数持续上升。

**解决方法**：

对于类型一，使用对象池解决。

对于类型二，检查对象池配置参数，设置MaxIdle和MaxTotal相等，关闭对象池自动销毁策略解决。

异常 2、任务耗时比正常调用多 60 秒

同“**异常 1**”，连接池已经达到最大连接限制，新的任务需要等待无引用状态的连接 61 秒触发超时后才可以获得连接。

异常 3、服务启动时任务慢，之后慢慢恢复正常

**出错原因**：

在高并发调用时，同一个对象会复用同一个WebSocket连接，因此WebSocket连接只会在服务启动时创建。需要注意的是，任务启动阶段如果立刻开始较高并发调用，同时创建过多的WebSocket连接会导致阻塞。

**解决方法**：

启动服务后逐步提升并发量，或增加预热任务。

异常 4、服务端报错 Invalid action('run-task')! Please follow the protocol!

**出错原因**：

这是由于出现了客户端报错后，服务端不知道客户端出错，连接处于任务中状态。此时连接和对象被复用并开启下一个任务，导致流程错误，下一个任务失败。

**解决方法**：

在抛出异常后主动关闭 WebSocket 连接后归还对象池。

异常 5、业务流量平稳，调用量出现异常尖刺

**出错原因**：

同时创建过多 WebSocket 连接导致阻塞，但业务流量持续打进来，导致任务短时间积压，并且在阻塞后所有积压任务立刻调用。这会造成调用量尖刺，并且有可能造成瞬时超过账号的并发数限制导致部分任务失败、服务器卡顿等。

这种瞬间创建过多 WebSocket 的情况多发生于：

-   服务启动阶段
-   网络出现异常，大量 WebSocket 连接同时中断重连
-   某一时刻出现大量服务端报错，导致大量 WebSocket 重连。常见报错如并发数超过账号限制（“Requests rate limit exceeded, please try again later.”）。

**解决方法**：

1.  检查网络情况。
2.  排查尖刺前是否出现大量其他服务端报错。
3.  提高账号并发限制。
4.  调小对象池和连接池大小，通过对象池上限限制最大并发数。
5.  提升服务器配置或扩充机器数。

异常 6、随着并发数提升，所有任务都变慢

**解决方法**：

1.  检查是否已经达到网络带宽上限。
2.  检查实际并发数是否已经过高。

#### Sambert

Sambert仅Java SDK内置了池化机制，Python SDK暂不支持。

#### 前提条件

-   [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   已安装符合版本要求的DashScope Java SDK，建议[安装最新版](raw/model-api-reference/preparations/install-sdk.md)，SDK版本需≥2.16.6

#### 推荐配置

连接池和对象池不是越多越好，过少或过多都会导致程序运行变慢。建议根据服务器实际规格配置。

在服务器上只运行Sambert语音合成服务的情况下，进行测试后得到了如下推荐配置供参考：

**常见机器配置（阿里云）**

**单机最大并发数**

**对象池大小**

**连接池大小**

4核8GiB

600

1200

2000

> 单机并发数指的是同一时刻正在运行的Sambert语音合成任务的数量，也可以理解为工作线程数。

**重要**在高并发调用时，同一个对象会复用同一个WebSocket连接，因此WebSocket连接只会在服务启动时创建。

同时创建过多的 WebSocket 连接会导致阻塞，启动服务时应逐步提高单机并发数。

#### 可配置参数

##### 连接池

DashScope Java SDK使用了OkHttp3提供的连接池来复用WebSocket连接，从而减少频繁创建WebSocket连接的耗时和资源开销。

连接池是DashScope SDK默认开启的优化项，需要根据使用场景配置连接池大小。

请在运行Java服务前，通过环境变量的方式提前按需配置好连接池的相关参数。连接池配置参数如下：

DASHSCOPE\_CONNECTION\_POOL\_SIZE

配置连接池大小。默认值为32。

推荐配置为峰值并发数的2倍以上。

DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS

配置最大异步请求数。默认值为32。

推荐配置为和连接池大小一致。

更多信息参见[参考文档](https://javadoc.io/static/com.squareup.okhttp3/okhttp/3.14.9/okhttp3/Dispatcher.html#setMaxRequests-int-)。

DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS\_PER\_HOST

配置单host最大异步请求数。默认值为32。

推荐配置为和连接池大小一致。

更多信息参见[参考文档](https://javadoc.io/static/com.squareup.okhttp3/okhttp/3.14.9/okhttp3/Dispatcher.html#setMaxRequestsPerHost-int-)。

##### 对象池

推荐使用对象池的方式来复用`SpeechSynthesizer`对象，这样可以进一步降低反复创建和销毁对象带来的内存和时间开销。

请在运行 Java 服务前，通过环境变量或代码的方式提前按需配置好对象池的大小。对象池配置参数如下：

SAMBERT\_OBJECTPOOL\_SIZE

对象池大小。

推荐配置为峰值并发数的1.5~2倍。

对象池大小需要小于或等于连接池大小，否则会出现对象等待连接的情况，导致调用阻塞。

关于如何配置环境变量，可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

#### 示例代码

以下为使用资源池的示例代码。其中，对象池为全局单例对象。

-   每个主账号默认每秒可提交3个Sambert语音合成任务。
    
    如需开通更高QPS请[联系我们](https://smartservice.console.aliyun.com/service/create-ticket)。
    

需要在项目中引入DashScope和org.apache.commons.pool2相关的包，DashScope要求版本号>=2.16.9。

以Maven和Gradle为例，配置如下：

#### Maven

1.  打开Maven项目的`pom.xml`文件。
2.  在`<dependencies>`标签内添加以下依赖信息。

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <!-- 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
    <version>the-latest-version</version>
</dependency>

<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
    <!-- 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2 -->
    <version>the-latest-version</version>
</dependency>
```

1.  保存`pom.xml`文件。
2.  使用Maven命令（如`mvn clean install`或`mvn compile`）来更新项目依赖

#### Gradle

1.  打开Gradle项目的`build.gradle`文件。
2.  在`dependencies`块内添加以下依赖信息。

```
dependencies {
    // 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'

    // 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2
    implementation group: 'org.apache.commons', name: 'commons-pool2', version: 'the-latest-version'
}
```

3.  保存`build.gradle`文件。
4.  在命令行中，切换到项目根目录，执行以下Gradle命令来更新项目依赖。

```
./gradlew build --refresh-dependencies
```

或者，如果使用Windows系统，命令应为：

```
gradlew build --refresh-dependencies
```

**说明**如果项目中没有Gradle Wrapper文件（`gradlew`或`gradlew.bat`），可以：

-   使用已安装的Gradle直接运行`gradle build --refresh-dependencies`
-   或先运行`gradle wrapper`生成wrapper文件，然后再运行上述命令

-   示例代码中，不同的线程通过等待随机时间来避免同时创建过多的WebSocket连接。

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import com.alibaba.dashscope.utils.Constants;

/**
 * Before making high-concurrency calls to the TTS service,
 * please configure the connection pool size through following environment
 * variables.
 *
 * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS=2000
 * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST=2000
 * DASHSCOPE_CONNECTION_POOL_SIZE=2000
 *
 * The default is 32, and it is recommended to set it to 2 times the maximum
 * concurrent connections of a single server.
 */

@Slf4j
public class SynthesizeTextToSpeechUsingSambertConcurrently {
    public static void checkoutEnv(String envName, int defaultSize) {
        if (System.getenv(envName) != null) {
            System.out.println("[ENV CHECK]: " + envName + " "
                    + System.getenv(envName));
        } else {
            System.out.println("[ENV CHECK]: " + envName
                    + " Using Default which is " + defaultSize);
        }
    }

    public static void main(String[] args)
            throws InterruptedException, NoApiKeyException {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";

        // Check for connection pool env
        checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
        checkoutEnv(SambertObjectPool.SAMBERT_OBJECTPOOL_SIZE_ENV, SambertObjectPool.DEFAULT_CONNECTION_POOL_SIZE);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);

        // Record task start time
        int runTimes = 1;

        // Create the pool of SpeechSynthesis objects
        ExecutorService executorService = Executors.newFixedThreadPool(runTimes);

        for (int i = 0; i < runTimes; i++) {
            executorService.submit(new SynthesizeTask(new String[]{
                    "床前明月光，",
                    "疑似地上霜。",
                    "举头望明月，",
                    "低头思故乡。"
            }));
        }

        // Shut down the ExecutorService and wait for all tasks to complete
        executorService.shutdown();
        executorService.awaitTermination(1, TimeUnit.MINUTES);
        System.exit(0);
    }
}

class SpeechSynthesizerObjectFactory
        extends BasePooledObjectFactory<SpeechSynthesizer> {
    public SpeechSynthesizerObjectFactory() {
        super();
    }
    @Override
    public SpeechSynthesizer create() throws Exception {
        return new SpeechSynthesizer();
    }

    @Override
    public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
        return new DefaultPooledObject<>(obj);
    }
}

class SambertObjectPool {
    public static GenericObjectPool<SpeechSynthesizer> synthesizerPool;
    public static String SAMBERT_OBJECTPOOL_SIZE_ENV = "SAMBERT_OBJECTPOOL_SIZE";
    public static int DEFAULT_CONNECTION_POOL_SIZE = 500;
    private static Lock lock = new java.util.concurrent.locks.ReentrantLock();
    public static int getObjectivePoolSize() {
        try {
            Integer n = Integer.parseInt(System.getenv(SAMBERT_OBJECTPOOL_SIZE_ENV));
            return n;
        } catch (NumberFormatException e) {
            return DEFAULT_CONNECTION_POOL_SIZE;
        }
    }
    public static GenericObjectPool<SpeechSynthesizer> getInstance() {
        lock.lock();
        if (synthesizerPool == null) {
            // You can set the object pool size here. or in environment variable
            // SAMBERT_OBJECTPOOL_SIZE It is recommended to set it to 1.5 to 2 times
            // your server's maximum concurrent connections.
            int objectPoolSize = getObjectivePoolSize();
            SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                    new SpeechSynthesizerObjectFactory();
            GenericObjectPoolConfig<SpeechSynthesizer> config =
                    new GenericObjectPoolConfig<>();
            config.setMaxTotal(objectPoolSize);
            config.setMaxIdle(objectPoolSize);
            config.setMinIdle(objectPoolSize);
            synthesizerPool =
                    new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
        }
        lock.unlock();
        return synthesizerPool;
    }
}

class SynthesizeTask implements Runnable {
    String[] textList;
    String requestId;
    long timeCost;
    public SynthesizeTask(String[] textList) {
        this.textList = textList;
    }
    @Override
    public void run() {
        // sleep random time before start task, avoid creating too much websocket at the same time.
        Random random = new Random();
        try {
            Thread.sleep(random.nextInt(30*1000));
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        for (String text:textList) {
            SpeechSynthesizer synthesizer = null;
            long startTime = System.currentTimeMillis();

            try {
                CountDownLatch latch = new CountDownLatch(1);
                class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
                    ReactCallback() {}

                    @Override
                    public void onEvent(SpeechSynthesisResult message) {
                        if (message.getAudioFrame() != null) {
                            try {
                                byte[] bytesArray = message.getAudioFrame().array();
                            } catch (Exception e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }

                    @Override
                    public void onComplete() {
                        latch.countDown();
                    }

                    @Override
                    public void onError(Exception e) {
                        System.out.println(e.getMessage());
                        e.printStackTrace();
                        latch.countDown();
                    }
                }

                SpeechSynthesisParam param =
                        SpeechSynthesisParam.builder()
                                .model("sambert-zhichu-v1")
                                .format(SpeechSynthesisAudioFormat.MP3) // 使用PCM或者MP3
                                .text(text)
                                .enablePhonemeTimestamp(true)
                                .enableWordTimestamp(true)
                                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                .build();

                try {
                    synthesizer = SambertObjectPool.getInstance().borrowObject();
                    synthesizer.call(param, new ReactCallback());
                    try {
                        latch.await();
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    requestId = synthesizer.getLastRequestId();
                } catch (Exception e) {
                    System.out.println("Exception e: " + e.toString());
                    synthesizer.getSyncApi().close(1000, "bye");
                }
            } catch (Exception e) {
                throw new RuntimeException(e);
            } finally {
                if (synthesizer != null) {
                    try {
                        // Return the SpeechSynthesizer object to the pool
                        SambertObjectPool.getInstance().returnObject(synthesizer);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
            long endTime = System.currentTimeMillis();
            timeCost = endTime - startTime;
            System.out.println("[线程" + Thread.currentThread() + "] 语音合成任务:(" + text + ")结束。耗时" + timeCost + "ms, RequestId" + requestId);
        }
    }
}
```

##### 异常处理

-   在服务出现TaskFailed报错时，不需要额外处理。
    
-   如果在语音合成中途，客户端出现错误（如SDK内部异常或业务逻辑异常）导致语音合成任务未完成，则需要主动关闭连接。
    
    关闭连接方法如下：
    

```
// 将下面这段代码放在try-catch块中
synthesizer.getSyncApi().close(1000, "bye");
```

#### 常见异常

异常 1、 业务流量平稳，但是服务器 TCP 连接数持续上升

**出错原因：****类型一：**

每一个 SDK 对象创建时都会申请一个连接。如果没有使用对象池，每一次任务结束后对象都被析构。此时这一个连接将进入无引用状态，需要等待 61s 秒后服务端报错连接超时才会真正断开，这会导致这个连接在 61 秒内不可复用。

在高并发场景下，新的任务在发现没有可复用连接时会创建新连接，会造成如下后果：

1.  连接数持续上升。
2.  由于连接数过多，服务器资源不足，服务器卡顿。
3.  连接池被打满、新任务由于启动时需要等待可用连接而阻塞。

**类型二：**

对象池配置的MaxIdle小于MaxTotal，导致在对象闲置时，超过MaxIdle的对象被销毁，从而造成连接泄漏。泄漏的连接需要等待61秒超时后断连，同类型一造成连接数持续上升。

**解决方法**：

对于类型一，使用对象池解决。

对于类型二，检查对象池配置参数，设置MaxIdle和MaxTotal相等，关闭对象池自动销毁策略解决。

异常 2、任务耗时比正常调用多 60 秒

同“**异常 1**”，连接池已经达到最大连接限制，新的任务需要等待无引用状态的连接 61 秒触发超时后才可以获得连接。

异常 3、服务启动时任务慢，之后慢慢恢复正常

**出错原因**：

在高并发调用时，同一个对象会复用同一个WebSocket连接，因此WebSocket连接只会在服务启动时创建。需要注意的是，任务启动阶段如果立刻开始较高并发调用，同时创建过多的WebSocket连接会导致阻塞。

**解决方法**：

启动服务后逐步提升并发量，或增加预热任务。

异常 4、服务端报错 Invalid action('run-task')! Please follow the protocol!

**出错原因**：

这是由于出现了客户端报错后，服务端不知道客户端出错，连接处于任务中状态。此时连接和对象被复用并开启下一个任务，导致流程错误，下一个任务失败。

**解决方法**：

在抛出异常后主动关闭 WebSocket 连接后归还对象池。

异常 5、业务流量平稳，调用量出现异常尖刺

**出错原因**：

同时创建过多 WebSocket 连接导致阻塞，但业务流量持续打进来，导致任务短时间积压，并且在阻塞后所有积压任务立刻调用。这会造成调用量尖刺，并且有可能造成瞬时超过账号的并发数限制导致部分任务失败、服务器卡顿等。

这种瞬间创建过多 WebSocket 的情况多发生于：

-   服务启动阶段
-   网络出现异常，大量 WebSocket 连接同时中断重连
-   某一时刻出现大量服务端报错，导致大量 WebSocket 重连。常见报错如并发数超过账号限制（“Requests rate limit exceeded, please try again later.”）。

**解决方法**：

1.  检查网络情况。
2.  排查尖刺前是否出现大量其他服务端报错。
3.  提高账号并发限制。
4.  调小对象池和连接池大小，通过对象池上限限制最大并发数。
5.  提升服务器配置或扩充机器数。

异常 6、随着并发数提升，所有任务都变慢

**解决方法**：

1.  检查是否已经达到网络带宽上限。
2.  检查实际并发数是否已经过高。

## 支持的模型与地域

#### 华北2（北京）

调用以下模型时，请选择北京地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-TTS：**qwen-audio-3.0-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash
    
-   **CosyVoice：**cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2、cosyvoice-v1
    
-   **Qwen-TTS**：
    
    -   **Qwen3-TTS-Instruct-Flash-Realtime**：qwen3-tts-instruct-flash-realtime（稳定版，当前等同qwen3-tts-instruct-flash-realtime-2026-01-22）、qwen3-tts-instruct-flash-realtime-2026-01-22（最新快照版）
    -   **Qwen3-TTS-VD-Realtime：**qwen3-tts-vd-realtime-2026-01-15（最新快照版）、qwen3-tts-vd-realtime-2025-12-16（快照版）
    -   **Qwen3-TTS-VC-Realtime：**qwen3-tts-vc-realtime-2026-01-15（最新快照版）、qwen3-tts-vc-realtime-2025-11-27（快照版）
    -   **Qwen3-TTS-Flash-Realtime：**qwen3-tts-flash-realtime（稳定版，当前等同qwen3-tts-flash-realtime-2025-11-27）、qwen3-tts-flash-realtime-2025-11-27（最新快照版）、qwen3-tts-flash-realtime-2025-09-18（快照版）
    -   **Qwen-TTS-Realtime：**qwen-tts-realtime（稳定版，当前等同qwen-tts-realtime-2025-07-15）、qwen-tts-realtime-latest（最新版，当前等同qwen-tts-realtime-2025-07-15）、qwen-tts-realtime-2025-07-15（快照版）
-   **Sambert：**sambert-zhinan-v1、sambert-zhiqi-v1、sambert-zhichu-v1、sambert-zhide-v1、sambert-zhijia-v1、sambert-zhiru-v1、sambert-zhiqian-v1、sambert-zhixiang-v1、sambert-zhiwei-v1、sambert-zhihao-v1、sambert-zhijing-v1、sambert-zhiming-v1、sambert-zhimo-v1、sambert-zhina-v1、sambert-zhishu-v1、sambert-zhistella-v1、sambert-zhiting-v1、sambert-zhixiao-v1、sambert-zhiya-v1、sambert-zhiye-v1、sambert-zhiying-v1、sambert-zhiyuan-v1、sambert-zhiyue-v1、sambert-zhigui-v1、sambert-zhishuo-v1、sambert-zhimiao-emo-v1、sambert-zhimao-v1、sambert-zhilun-v1、sambert-zhifei-v1、sambert-zhida-v1、sambert-camila-v1、sambert-perla-v1、sambert-indah-v1、sambert-clara-v1、sambert-hanna-v1、sambert-beth-v1、sambert-betty-v1、sambert-cally-v1、sambert-cindy-v1、sambert-eva-v1、sambert-donna-v1、sambert-brian-v1、sambert-waan-v1，请参见[Sambert模型列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi)
    

#### 新加坡

调用以下模型时，请选择新加坡地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-TTS**：qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
    
-   **CosyVoice**：cosyvoice-v3-plus、cosyvoice-v3-flash
    
-   **Qwen-TTS**：
    
    -   **Qwen3-TTS-Instruct-Flash-Realtime**：qwen3-tts-instruct-flash-realtime（稳定版，当前等同qwen3-tts-instruct-flash-realtime-2026-01-22）、qwen3-tts-instruct-flash-realtime-2026-01-22（最新快照版）
    -   **Qwen3-TTS-VD-Realtime：**qwen3-tts-vd-realtime-2026-01-15（最新快照版）、qwen3-tts-vd-realtime-2025-12-16（快照版）
    -   **Qwen3-TTS-VC-Realtime：**qwen3-tts-vc-realtime-2026-01-15（最新快照版）、qwen3-tts-vc-realtime-2025-11-27（快照版）
    -   **Qwen3-TTS-Flash-Realtime：**qwen3-tts-flash-realtime（稳定版，当前等同qwen3-tts-flash-realtime-2025-11-27）、qwen3-tts-flash-realtime-2025-11-27（最新快照版）、qwen3-tts-flash-realtime-2025-09-18（快照版）

## 支持的音色

不同模型支持的音色不同。将请求参数 `voice` 设为音色列表中 **voice参数** 列的值即可。

-   [Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)
-   [CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)
-   [Qwen-TTS音色列表](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list#0ad0bfdd635ar)
-   [Sambert音色列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi)

## API参考

通过 AOQ 接入的流程和示例，请参见[AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)。支持的模型及版本请参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。

-   [实时语音合成-Qwen-Audio-TTS API参考](raw/_short/qwen-audio-tts-api-2a5997e924bff673.md) / [实时语音合成-CosyVoice API参考](raw/_short/cosyvoice-large-model-for-speech-synthesis-c25d07a9b3ba6047.md)
-   [实时语音合成-千问API参考](raw/_short/qwen-tts-realtime-api-reference-5bfb7590608ff1dc.md)
-   [实时语音合成-Sambert API参考](raw/_short/sambert-speech-synthesis-60d77f54e64567a1.md)

## 常见问题

### Q：语音合成发音错误怎么办？多音字如何控制发音？

-   将多音字替换为同音的其他汉字，快速解决发音问题。
-   使用 SSML 标记语言控制发音：Sambert 和 CosyVoice 均支持 SSML。

### Q：使用复刻音色生成的音频无声音如何排查？

1.  **确认音色状态**
    
    调用[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)接口，确认音色的 `status` 是否为 `OK`。
    
2.  **检查模型版本一致性**
    
    确保复刻音色时使用的 `target_model` 参数与语音合成时的 `model` 参数完全一致。例如：
    
    -   复刻时使用 `cosyvoice-v3-plus`
    -   合成时也必须使用 `cosyvoice-v3-plus`
3.  **验证源音频质量**
    
    检查复刻音色时使用的源音频是否符合[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)：
    
    -   音频时长：10-20秒
    -   音质清晰
    -   无背景噪音
4.  **检查请求参数**
    
    确认语音合成请求中的 `voice` 参数已设置为复刻音色的 ID。
    

### Q：声音复刻后合成效果不稳定或语音不完整怎么办？

如果复刻音色后合成的语音出现以下问题：

-   语音播放不完整，只读出部分文字
-   合成效果不稳定，时好时坏
-   语音中包含异常停顿或静音段

**可能原因**：源音频质量不符合要求。

**解决方案**：请检查源音频是否符合[录音操作指南](https://help.aliyun.com/zh/model-studio/recording-guide)中的音频要求，建议按照录音指南重新录制。

### Q：为什么语音合成的实际时长与 WAV 文件显示的时长不一致？

语音合成采用流式机制，边合成边返回数据，因此保存的 WAV 文件头中的时长是预估值，存在一定误差。如需精确时长，可将 format 设置为 pcm，待获取完整合成结果后自行添加 WAV 文件头信息。

### Q：为什么音频无法播放？

请按以下场景逐一排查：

1.  音频保存为完整文件（如 xx.mp3）的情况
    
    1.  音频格式一致性：请求参数中的音频格式须与文件后缀一致（如参数为 wav 则文件须为 .wav）。
    2.  播放器兼容性：确认播放器支持该音频的格式和采样率。
2.  流式播放音频的情况
    
    1.  将音频流保存为完整文件，尝试用播放器播放。如果文件无法播放，请参考场景 1 的排查方法。
    2.  如果文件可正常播放，则问题在流式播放实现。请确认播放器支持流式播放（如 ffmpeg、pyaudio、AudioFormat、MediaSource 等）。

### Q：为什么音频播放卡顿？

请按以下步骤逐一排查：

1.  检查文本发送速度：确保发送间隔合理，避免上段音频播完后下段文本尚未到达。
    
2.  检查回调函数性能：
    
    -   确认回调函数中无阻塞性业务逻辑。
    -   回调运行在 WebSocket 线程，阻塞会影响数据接收。建议将音频数据写入独立缓冲区，在其他线程中处理。
3.  检查网络稳定性：网络波动可能导致音频传输中断或延迟。
    

### Q：语音合成耗时较长是什么原因？

请按以下步骤排查：

1.  检查输入间隔
    
    如果是流式合成，确认文本发送间隔是否过长，过长会导致合成总时长增加。
    
2.  分析性能指标
    
    -   首包延迟：正常约 500ms。
    -   RTF（实时率 = 合成总耗时 / 音频时长）：正常应小于 1.0。

### Q：合成的音频中读出了文本里的特殊符号怎么办？

Qwen-TTS 系列模型可能将文本中的部分特殊符号（如 Markdown 加粗标记 \*\*）合成为语音。可通过以下方式处理：

1.  调用前对文本进行预处理，去除特殊符号。
2.  改用 CosyVoice 模型。

### Q：如何限制 API Key 仅用于语音合成服务（权限隔离）？

通过新建业务空间并仅授权特定模型，可限制 API Key 的使用范围。请参见[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

### Q：子业务空间的 API Key 能否调用 Qwen-Audio-TTS/CosyVoice 模型？

默认业务空间下，所有模型均可调用。

子业务空间下，需要为 API Key 对应的子业务空间进行[模型授权](https://help.aliyun.com/zh/model-studio/model-authentication-instructions)。请参见[子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

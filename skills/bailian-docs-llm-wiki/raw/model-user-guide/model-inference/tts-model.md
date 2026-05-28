# 语音合成

选择适合语音合成、声音复刻和声音设计场景的模型。

## 标准语音合成还是自定义音色？

语音合成模型可将文本转换为自然语音。首先确定您需要使用内置音色还是自定义音色：

**标准语音合成**

**自定义音色**

音色来源

模型内置音色库，选择即用

从音频样本复刻，或用文字描述创建

上手成本

无需额外配置，选择模型和音色即可合成

需提供音频样本或文字描述来创建音色

适用场景

智能客服、有声阅读、内容播报、电商直播

品牌专属音色、虚拟主播、游戏角色配音

推荐模型

`cosyvoice-v3-plus`、`MiniMax/speech-2.8-hd`

`cosyvoice-v3.5-plus`（声音复刻+声音设计）、`MiniMax/speech-2.8-hd`（声音复刻）

-   **使用标准语音合成**：当内置音色库能满足需求，希望快速上手、无需额外配置时。
    
-   **使用自定义音色**：当需要品牌专属声音、复刻特定人物音色，或创建全新角色音色时。
    

## 声音复刻还是声音设计？

如果选择自定义音色，有两种方式创建：

**声音复刻（Voice Cloning）**

**声音设计（Voice Design）**

输入方式

提供一段音频样本

用文字描述期望的音色（如"温暖的低音女声"）

效果

合成语音与原始说话人高度相似

根据描述从零生成全新音色

适用场景

品牌代言人/主播音色复用、虚拟主播、个性化语音助手

品牌音色定制（无录音素材）、游戏/动画角色配音、创意内容制作

推荐模型

`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`MiniMax/speech-2.8-hd`

`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`

音色管理服务

`voice-enrollment`（注册和管理音色）

`voice-enrollment`（注册和管理音色）

-   **使用声音复刻**：当已有目标人物的录音素材，希望在合成中还原该音色时。
    
-   **使用声音设计**：当没有录音素材，希望根据文字描述从零创建全新音色时。
    

## WebSocket还是HTTP？

-   **WebSocket**：双向流式通信，支持流式输入和流式输出，音频边合成边返回，延迟最低。适用于智能客服、语音助手、呼叫中心等实时交互场景。
    
-   **HTTP**：发送完整文本，支持流式返回音频（逐段输出）。适用于有声阅读、音频内容制作等场景。
    

CosyVoice 系列模型使用同一模型名称同时支持 WebSocket 和 HTTP 两种接入方式；Qwen 系列模型通过模型名称区分，带 `-realtime` 后缀的为 WebSocket 接入，不带后缀的为 HTTP 接入。

CosyVoice 和 Qwen 系列的 WebSocket 模型支持通过 DashScope SDK（Java、Python）接入。CosyVoice 的 WebSocket 模型还支持Android、iOS SDK接入。其他模型需根据对应的 WebSocket 或 HTTP 协议直接调用。

选择 WebSocket 接入请参考**实时语音合成**，选择 HTTP 接入请参考**非实时语音合成**。

## 指令控制

用自然语言描述期望的表达方式，可按请求动态控制语速、情绪和风格。例如“用温柔的语气，语速稍慢”或“用激动的播报风格”。适用于情感化内容制作、专业播报、有声读物等需要丰富表现力的场景。

支持指令控制的模型：CosyVoice 系列（`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`）和 Qwen-TTS 系列（`qwen3-tts-instruct-flash-realtime`、`qwen3-tts-instruct-flash`）。详细使用方式请参见[实时语音合成 > 指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#d815caea76zx8)。

## 推荐模型

以下为各场景下最推荐的模型，可前往模型广场查看详情。

**模型**

**系列**

**API**

**声音复刻**

**声音设计**

**指令控制**

`cosyvoice-v3.5-plus`

CosyVoice

WebSocket / HTTP

支持

支持

支持

`cosyvoice-v3-plus`

CosyVoice

WebSocket / HTTP

支持

支持

不支持

`MiniMax/speech-2.8-hd`

MiniMax

HTTP

支持

不支持

不支持

## 所有模型

### CosyVoice

部分 CosyVoice 模型支持 SSML 标记和 LaTeX 公式朗读。

**模型**

**API**

**声音复刻**

**声音设计**

**指令控制**

`cosyvoice-v3.5-plus`

WebSocket / HTTP

支持

支持

支持

`cosyvoice-v3.5-flash`

WebSocket / HTTP

支持

支持

支持

`cosyvoice-v3-plus`

WebSocket / HTTP

支持

支持

不支持

`cosyvoice-v3-flash`

WebSocket / HTTP

支持

支持

支持

`cosyvoice-v2`

WebSocket / HTTP

支持

不支持

不支持

`cosyvoice-v1`

WebSocket

支持

不支持

不支持

### Qwen3-TTS

**模型**

**API**

**声音复刻**

**声音设计**

**指令控制**

`qwen3-tts-flash`

HTTP

不支持

不支持

不支持

`qwen3-tts-flash-2025-11-27`

HTTP

不支持

不支持

不支持

`qwen3-tts-flash-2025-09-18`

HTTP

不支持

不支持

不支持

`qwen3-tts-flash-realtime`

WebSocket

不支持

不支持

不支持

`qwen3-tts-flash-realtime-2025-11-27`

WebSocket

不支持

不支持

不支持

`qwen3-tts-flash-realtime-2025-09-18`

WebSocket

不支持

不支持

不支持

`qwen3-tts-instruct-flash`

HTTP

不支持

不支持

支持

`qwen3-tts-instruct-flash-2026-01-26`

HTTP

不支持

不支持

支持

`qwen3-tts-instruct-flash-realtime`

WebSocket

不支持

不支持

支持

`qwen3-tts-instruct-flash-realtime-2026-01-22`

WebSocket

不支持

不支持

支持

`qwen3-tts-vc-2026-01-22`

HTTP

支持

不支持

不支持

`qwen3-tts-vc-realtime-2026-01-15`

WebSocket

支持

不支持

不支持

`qwen3-tts-vc-realtime-2025-11-27`

WebSocket

支持

不支持

不支持

`qwen3-tts-vd-2026-01-26`

HTTP

不支持

支持

不支持

`qwen3-tts-vd-realtime-2026-01-15`

WebSocket

不支持

支持

不支持

`qwen3-tts-vd-realtime-2025-12-16`

WebSocket

不支持

支持

不支持

### MiniMax

**模型**

**API**

**声音复刻**

**声音设计**

**指令控制**

`MiniMax/speech-2.8-hd`

HTTP

支持

不支持

不支持

`MiniMax/speech-02-hd`

HTTP

支持

不支持

不支持

`MiniMax/speech-2.8-turbo`

HTTP

支持

不支持

不支持

`MiniMax/speech-02-turbo`

HTTP

支持

不支持

不支持

### Qwen-TTS（旧版，按 Token 计费）

以下为按 Token 计费的旧版 Qwen-TTS 模型。若您已迁移到 Qwen3-TTS，可优先使用前文推荐的模型。

**模型**

**API**

**说明**

`qwen-tts`

HTTP

非流式合成，按 Token 计费

`qwen-tts-latest`

HTTP

非流式合成，按 Token 计费

`qwen-tts-2025-05-22`

HTTP

快照版本，按 Token 计费

`qwen-tts-2025-04-10`

HTTP

快照版本，按 Token 计费

`qwen-tts-realtime`

WebSocket

流式合成，按 Token 计费

`qwen-tts-realtime-latest`

WebSocket

流式合成，按 Token 计费

`qwen-tts-realtime-2025-07-15`

WebSocket

快照版本，流式合成，按 Token 计费

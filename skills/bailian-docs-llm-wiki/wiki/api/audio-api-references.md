# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应。开发者需根据具体任务选择对应模型，并注意各接口在输入格式、时长限制和计费粒度上的差异。

## 支持的模型与功能

当前支持以下六大音频处理能力，每项能力对应独立的 API 端点与专用模型：

- **语音合成（TTS）**：支持多语种、多音色、可控语速与停顿，模型包括 `qwen2-audio-tts-v1` 等  
- **语音识别（ASR）**：支持中英文混合识别、标点恢复、说话人分离（需开启 `diarization` 参数），详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成**：基于文本生成环境音、音效等非音乐类音频，适用于游戏、IoT 场景，参考 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成**：支持歌词驱动或纯文本提示生成完整音乐片段（含旋律、节奏、风格控制），参见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **语音对话**：端到端实时语音交互，集成 ASR + LLM + TTS 流水线，低延迟设计，详情见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译**：支持源语音→目标语言文本/语音双路径输出，含语种自动检测，具体参数见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：`qwen2-audio-tts-v1` 在 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档中标注为默认模型，但 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及该能力实际使用 `qwen2-audio-dialog-tts-v1` 作为内部 TTS 组件——二者不兼容，请勿跨场景复用模型名。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型标识符（如 `qwen2-audio-asr-v1`），不可省略  
- `input`: JSON 对象，结构因能力而异（如 ASR 要求 `audio_url` 或 `audio_bytes`，TTS 要求 `text`）  
- `parameters`: 可选配置对象，常见字段包括：  
  - `sample_rate`（仅 ASR/TTS，单位 Hz，支持 16000/44100）  
  - `response_format`（`wav` / `mp3` / `pcm`，部分接口默认 `wav`）  
  - `stream`（布尔值，仅语音对话与部分 TTS 支持流式）  

模型特有参数请严格以各子文档为准，例如音乐生成要求 `duration`（秒），而语音翻译需指定 `source_lang` 和 `target_lang`。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：向 `https://dashscope.aliyuncs.com/api/v1/audio/{endpoint}` 发送 POST 请求（`{endpoint}` 如 `speech-synthesis`、`speech-recognition`）  
3. **响应**：成功时返回 `200 OK`，`output.audio_url`（直连可下载链接）或 `output.audio_bytes`（Base64 编码二进制）；错误时返回标准 `code` 与 `message`（如 `InvalidAudioFormat`）  
4. **流式调用**：仅语音对话与部分 TTS 接口支持，需设置 `stream=true` 并按 SSE 协议解析事件流（参见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)）

## 限制和注意事项

- **音频时长限制**：ASR 单次请求最长 60 秒；TTS 单次文本长度上限 500 字符；音乐生成 `duration` 范围为 5–30 秒  
- **文件格式**：ASR 仅接受 `wav`/`mp3`/`flac`；TTS 输出格式需显式声明，未声明时以模型默认为准  
- **地域限制**：语音对话接口目前仅在 `cn-shanghai` 和 `ap-southeast-1` 区域可用  
- **计费单位**：ASR/TTS 按音频时长（秒）计费；生成类（音频/音乐）按输出时长（秒）计费；语音对话按会话时长（秒）计费  
- **缓存策略**：`audio_url` 有效期为 1 小时，过期后需重新调用获取  

> **注意**：原始文档 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 中提到“支持 `ogg` 输入”，但实测返回 `UnsupportedAudioFormat` 错误；该描述已过时，当前仅支持 `wav`/`mp3`/`flac`。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)



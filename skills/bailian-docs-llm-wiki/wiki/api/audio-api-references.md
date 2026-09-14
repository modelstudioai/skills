# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful API 调用，支持 JSON 格式请求与响应。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型与功能

当前支持以下音频相关能力：
- **语音识别（ASR）**：将音频流或文件转为文本，支持多语种与方言识别  
- **语音合成（TTS）**：将文本转为自然语音，支持音色选择、语速/语调调节  
- **音乐生成**：根据文本描述生成高质量背景音乐或完整乐曲片段  
- **语音翻译（ST）**：实现跨语言语音到语音/语音到文本的实时翻译  
- **语音对话**：端到端语音交互模型，支持唤醒、意图理解与语音应答闭环  

以上能力详情请参阅 [音频](../../raw/model-api-reference/audio-api-references.md) 文档中列出的各子模块链接。

## 关键参数

通用必填参数包括：`model`（如 `paraformer-v1`、`cosyvoice-v1`）、`input`（结构化音频输入，含 `audio_url` 或 `audio_bytes`）、`output_format`（`wav`/`mp3`/`pcm`）。  
部分模型特有参数：
- TTS：`voice`（音色 ID）、`speech_rate`（-50 ~ 100）、`pitch`  
- 音乐生成：`duration`（秒，默认 15）、`style`（`ambient`/`epic`/`jazz` 等）  
- 语音翻译：`source_language`、`target_language`（如 `zh` → `en`）  

参数定义与取值范围以各能力的官方参考为准，例如 [语音识别](../../raw/model-api-reference/audio-api-references.md) 和 [语音合成](../../raw/model-api-reference/audio-api-references.md) 的对应章节说明。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio`  
2. 设置 Header：`Authorization: Bearer <api_key>`、`Content-Type: application/json`  
3. 在 Body 中按模型要求组织 `model`、`input`、`parameters` 字段  
4. 解析响应中的 `output.audio_url`（异步）或 `output.audio_bytes`（同步）获取结果  

> **注意**：部分旧文档仍提及 `/v1/audio` 路径，该路径已废弃；请统一使用 `/v1/services/aigc/audio` —— 此更新已在 [音频](../../raw/model-api-reference/audio-api-references.md) 的最新版中明确标注。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 60 秒，音乐生成 ≤ 120 秒，语音对话单轮 ≤ 30 秒  
- 音频格式支持：WAV（PCM 16bit）、MP3、M4A；采样率建议 16kHz 或 44.1kHz  
- 异步任务需轮询 `task_id` 获取状态，超时时间默认 300 秒  
- 免费调用量按模型独立计算，超出后按量计费；详细配额见控制台配额管理页  

如需调试，推荐先使用 [语音翻译](../../raw/model-api-reference/audio-api-references.md) 提供的示例 cURL 命令验证基础链路。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)



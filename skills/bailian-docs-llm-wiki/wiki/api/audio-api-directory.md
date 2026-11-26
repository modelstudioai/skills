# audio api directory

audio api directory 是百炼平台提供的非实时音视频处理能力的统一入口，涵盖语音识别、语音合成、音频打标、音频生成及音视频翻译等核心功能。所有 API 均采用标准 HTTP 接口设计，支持 JSON 请求与响应，适用于离线批量处理场景。开发者需通过 API Key 认证，并遵循各子服务的输入格式与计费规则。

## 支持的模型/功能

当前目录下包含以下五类非实时音视频处理能力：
- **语音识别（ASR）**：支持多语种、高精度转写，适用于会议记录、字幕生成等场景；详见 [语音识别](audio-api-directory/speech-recognition-api-reference.md)  
- **语音合成（TTS）**：提供多种音色与语速调节能力，输出 WAV/MP3 格式音频；参考 [语音合成](audio-api-directory/speech-synthesis-api-reference.md)  
- **音频打标（Audio Captioning）**：对音频内容进行语义级描述与标签提取，基于 Qwen-Audio 模型；具体参数见 [音频打标](audio-api-directory/qwen-audio-asr-captioner-http-api.md)  
- **音频生成（Audio Generation）**：支持文本到音频（T2A）生成，含背景音与语音混合能力；详情参阅 [音频生成](audio-api-directory/audio-generation-api.md)  
- **音视频翻译（LiveTranslate Flash）**：面向音视频文件的跨语言翻译（如中→英字幕+配音），非实时流式处理；说明见 [音视频翻译](audio-api-directory/qwen3-livetranslate-flash-api.md)

> **注意**：`qwen3-livetranslate-flash-api.md` 文档标题含 “LiveTranslate”，但其实际为**非实时批处理接口**，与实时流式翻译服务无关；该命名易引发误解，建议以 [音视频翻译](audio-api-directory/qwen3-livetranslate-flash-api.md) 正文描述为准。

## 关键参数

通用请求头需包含 `Authorization: Bearer <api_key>`；各接口共用以下关键参数：
- `file`: `multipart/form-data` 上传的音频/视频文件（支持 MP3、WAV、MP4、MOV 等，单文件 ≤ 100 MB）  
- `language`: 源语言代码（如 `zh`, `en`, `ja`），ASR 和翻译类接口必需；TTS 接口则指定目标语言  
- `response_format`: 可选 `json`（默认）或 `srt`（仅 ASR/TTS 支持）  
- `model`: 显式指定模型 ID（如 `qwen-audio-asr-v1`, `qwen-tts-v2`），部分接口可省略（使用默认模型）  
- `prompt`: 音频生成与打标接口支持上下文提示词，长度 ≤ 200 字符  

详细字段定义请查阅 [概述](audio-api-directory/audio-api-references.md) 中的通用规范说明。

## 使用方式

1. 构造 POST 请求，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`（`<service_name>` 如 `asr`, `tts`, `captioning`）  
2. 设置 `Content-Type: multipart/form-data`，按需传入 `file` 及其他表单字段  
3. 解析返回的 `200 OK` 响应体，其中 `output.result` 为结构化结果（如文本、SRT 字符串、音频 URL 等）  
4. 异步任务（如长音频处理）将返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}` 获取最终结果  

完整调用示例与错误码说明见 [概述](audio-api-directory/audio-api-references.md)。

## 限制和注意事项

- 单次请求最大文件体积为 100 MB；超限需分片或压缩后重试  
- 音频时长上限：ASR/TTS ≤ 2 小时，音频生成 ≤ 30 秒，打标与翻译 ≤ 1 小时  
- 所有接口均不支持实时流式输入（即 chunked transfer encoding），必须上传完整文件  
- `qwen-audio-asr-captioner-http-api.md` 中提及的“支持视频帧采样”功能**尚未上线**，当前仅接受音频输入；该信息已过时，请以 [音频打标](audio-api-directory/qwen-audio-asr-captioner-http-api.md) 最新版本为准  
- 错误响应中 `code` 字段为平台级错误码（如 `InvalidParameter`），`message` 为用户可读提示；业务级失败（如语音质量不足）会返回 `200 OK` 但 `output.status = "failed"`，需检查 `output.error` 字段  

如遇模型不可用或参数校验异常，建议优先核对 [概述](audio-api-directory/audio-api-references.md) 中的兼容性矩阵与版本说明。

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)



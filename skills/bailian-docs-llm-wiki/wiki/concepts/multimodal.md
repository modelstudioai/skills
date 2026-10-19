# 多模态支持

多模态支持是指百炼平台模型和服务对**文本、图像、音频、视频等多种模态数据的联合理解与生成能力**，涵盖多模态输入（如图文混合提问、语音+文本指令）、多模态输出（如文本+语音响应、图文并茂结果）以及跨模态推理（如看图说话、文档内容语音播报）等核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

多模态支持不是单一功能，而是贯穿平台多个层级的架构能力，按使用场景可分为三类：

- **原生模型调用（`/v1/chat/completions` 等标准接口）**  
  适用于通义千问 VL 系列（如 `qwen-vl-plus`、`qwen2-vl-7b-instruct`）等视觉语言模型。用户通过 `messages` 数组中 `content` 字段传入结构化多模态内容：  
  ```json
  {
    "role": "user",
    "content": [
      {"type": "text", "text": "这张图里有什么动物？"},
      {"type": "image_url", "image_url": {"url": "https://xxx.jpg"}}
    ]
  }
  ```
  > ✅ 支持图像 URL（公网可访问）、Base64 编码或 `asset_id`（见下文资产中心集成）；不支持视频/音频直传。

- **应用调用（Application Call）**  
  新版智能体（Agent 2.0）和工作流支持更灵活的多模态输入协议：  
  - DashScope 原生 API：通过 `image_list`（数组，含 `url` 或 `base64`）或 `file_list`（PDF/DOCX/MP3 等）传入；  
  - OpenAI 兼容 Responses API：在 `input` 字段中使用消息数组，支持 `{"type":"image_url","image_url":{"url":"..."}}` 和 `{"type":"file_url","file_url":{"url":"..."}}`；  
  > ✅ 文件自动解析为文本/语音转写后送入模型；图像支持高分辨率理解（需模型支持）；文件大小单个 ≤ 50 MB。

- **[实时交互](realtime.md)（Omni Realtime API）**  
  面向低延迟音视频场景，支持端到端流式多模态 I/O：  
  - 输入：PCM/WAV 音频流（单/双/四通道）、文本消息、视频帧（实验性）；  
  - 输出：纯文本、文本+合成语音（TTS），音频格式可选 `pcm`/`wav`，采样率最高 48 kHz；  
  - 控制：通过 `session.update` 设置 `modalities: ["text", "audio"]`、`audio.input.format`、`audio.output.voice` 等参数。  
  > ✅ 语音活动检测（VAD）、语义轮次控制、工具调用与多模态输出可同时启用。

- **生成类任务（文生图/文生视频）**  
  虽属“单向生成”，但本质是文本→图像/视频的跨模态映射：  
  - 文生图（`qwen-image-3.0-pro`、`wan2.7-t2i`）：`prompt` + `negative_prompt` 驱动；  
  - 图生视频（`wan2.7-i2v`）：`input.first_frame` 可传 `asset_id` 或 URL；  
  - 文档转视频：先解析 PDF/DOCX（多模态输入），再生成分镜脚本与画面（多模态输出）。  
  > ✅ 资产中心 `asset_id` 可在所有支持图像/视频输入的 API 中复用，避免重复上传。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 说明 | 是否必需 | 示例值 |
|------|--------|------|------|----------|--------|
| **标准模型调用** | `content`（数组元素） | object | 消息内单个模态项 | 是（多模态时） | `{"type":"image_url","image_url":{"url":"https://x.jpg"}}` |
| **Application Call（DashScope）** | `image_list` | array | 图像列表（URL/Base64） | 否 | `[{"url":"https://x.jpg"}]` |
| | `file_list` | array | 文件列表（URL/Base64） | 否 | `[{"url":"https://x.pdf","name":"report.pdf"}]` |
| **Application Call（Responses）** | `input`（消息数组） | array | 同标准接口，支持 `type: "image_url"` / `"file_url"` | 是（多模态时） | `[{"type":"text","text":"分析此表"},{"type":"image_url","image_url":{"url":"..."}}]` |
| **Omni Realtime** | `modalities` | array | 输出模态组合 | 是 | `["text", "audio"]` |
| | `audio.input.format` | object | 音频输入格式 | 是（启用音频输入时） | `{"type":"pcm","sample_rate":16000}` |
| | `audio.output.voice` | string | 合成音色 | 否（有默认值） | `"longanlingxin"` |
| **通用（资产复用）** | `asset_id` | string | 平台资产唯一 ID | 否（替代 URL/Base64） | `"as-abc123xyz"` |

> ⚠️ 注意：  
> - 所有图像/文件 URL 必须公网可访问，或使用 `asset_id`（推荐用于生产环境，提升稳定性与性能）；  
> - 多模态请求受模型上下文长度限制（如 `qwen-vl-plus` 总 token ≤ 8192），图像会编码为 token 占用显著空间；  
> - 实时 API 的音频输入需严格匹配 `audio.input.format` 规范（如 `s16le`、`interleaved`），否则连接中断。

## 面向开发者，简洁实用

- ✅ **首选 `asset_id`**：图像/视频/文档优先上传至[资产中心](asset-center-page.md)，后续 API 调用直接传 `"asset_id": "as-xxx"` —— 避免超时、节省带宽、支持 OSS 自动转存。  
- ✅ **验证模型能力**：调用前查模型文档（如 `qwen-vl-plus` 支持图文问答，`qwen-audio-3.1-asr-flash-streaming` 仅支持语音识别），勿假设通用支持。  
- ✅ **实时场景用 WebSocket/AOQ**：语音对话、会议纪要等强交互需求，必须使用 `omni-realtime-api`，标准 REST 接口无法满足低延迟要求。  
- ✅ **错误快速定位**：  
  - `400 Bad Request` → 检查 `content` 结构是否符合多模态 schema（类型字段、嵌套层级）；  
  - `404 Not Found` → 确认模型 ID 正确且地域可用（如 `qwen3.8-omni-flash-realtime` 仅限华北2）；  
  - 音频无声 → 核对 `audio.output.format` 与播放器兼容性（推荐 `wav` + `24000Hz`）。  
- 🚫 **不支持的组合**：  
  - 标准 `/v1/chat/completions` 接口不支持音频/视频输入；  
  - `enable_search` 与 `tools` 在 Omni Realtime 中互斥；  
  - `asset_id` 仅适用于图片/视频/文档，不可用于音频直传（音频需走 Realtime 流式）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [use cases](../guides/use-cases.md)
- [asset center page](../guides/asset-center-page.md)



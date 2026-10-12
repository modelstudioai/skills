# 多模态

多模态是指模型能够同时理解、生成或跨模态关联两种及以上类型的数据（如文本、图像、音频、视频等），实现更接近人类感知与推理能力的智能交互。在百炼平台中，多模态不是单一能力，而是贯穿模型选型、API 设计、资产管理和实时交互的一类核心能力范式。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：多模态能力由特定模型原生支持，例如 `qwen-vl`（图文理解）、`qwen-audio`（语音理解与生成）、`qwen3.8-omni-flash`（全模态统一建模）、`qwen3.8-omni-flash-realtime`（实时音视频流处理）。调用时需选择对应模型 ID，并在 `input` 中结构化传入多类型数据（如 `image_url` + `audio_url` + 文本 `messages`）。

- **API 接口适配**：
  - 标准 `/v1/chat/completions` 接口支持图文混合输入（如 `{"role": "user", "content": [{"type": "text", "text": "描述这张图"}, {"type": "image_url", "image_url": "https://..."}]}`），兼容 OpenAI 多模态格式；
  - 实时多模态 API（`/omni/realtime`）基于 WebSocket，支持按事件类型（`input.text` / `input.image` / `input.audio`）动态注入不同模态数据，实现低延迟、上下文连贯的跨模态交互。

- **资产中心集成**：图像与视频生成结果（如 `qwen-image-3.0-pro`、`wan2.7-t2v` 输出）自动沉淀为可管理资产，通过 `asset_id` 在后续请求中复用（替代 URL 或 base64），实现模态间高效引用与版本控制；注意：音频资产当前**不支持**资产中心托管。

- **应用构建**：零代码模板（如「智能客服对话流」）可自动启用多模态模型，当用户上传图片或发送语音时，系统自动路由至 `qwen-audio` 或 `qwen-vl` 等模型处理，开发者无需修改逻辑即可获得多模态响应能力。

- **Prompt 工程**：多模态任务需协同设计提示词——图文任务中，文本描述应聚焦图像语义（如“图中人物是否佩戴安全帽？”），避免冗余视觉细节；音视频任务中，建议将音频转录文本与关键帧描述共同作为上下文输入，提升理解鲁棒性。

## 关键参数和配置

- **`model`**：必须显式指定多模态模型 ID（如 `qwen-vl`, `qwen-audio-3.1-asr-flash-streaming`, `qwen3.8-omni-flash-realtime`），不可混用纯文本模型（如 `qwen3.7-plus`）。
- **`input` 结构**：
  - 图文混合：使用 OpenAI 兼容的 `content` 数组，含 `{"type": "text", "text": "..."}` 和 `{"type": "image_url", "image_url": "..."}`（支持 HTTPS URL 或 base64 编码）；
  - 音频输入：标准接口中传 `{"audio_url": "..."}`；实时接口中通过 `input.audio` 事件分块推送 PCM/Opus 数据；
  - 视频输入：目前仅 `wan2.7-i2v`/`wan2.7-r2v` 等视频模型支持 `video_url` 字段，单文件 ≤ 500 MB。
- **`asset_id`**：在支持资产复用的接口中（如万相系列、Wan2.7 视频模型），优先使用 `{"asset_id": "xxx"}` 替代原始 URL，降低带宽开销并规避过期风险。
- **实时会话配置**（WebSocket）：
  - 连接 URL 必须携带 `stream=true`；
  - 首条 `session.update` 消息中需声明 `input_audio_format`（如 `"pcm-16000"`）和 `output_audio_format`（如 `"mp3"`）；
  - 图像上传限单图 ≤ 10 MB，需通过 `input.image` 事件发送。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `curl` 调用 `/v1/chat/completions`，`model=qwen-vl`，`input` 包含一张公开图片 URL 和问题文本，5 分钟内完成图文问答测试。
- ✅ **生产推荐**：图文/音视频混合任务优先选用 `qwen3.8-omni-flash-realtime`（实时）或 `qwen3.8-omni-flash`（离线批处理）；纯图像生成用 `qwen-image-3.0-pro`；纯语音识别用 `qwen-audio-3.1-asr-flash-streaming`。
- ⚠️ **避坑提示**：
  - 多模态模型**不支持** `function calling`（工具调用），若需插件能力，请拆分为纯文本子任务调用其他模型；
  - `stream=true` 时，标准接口返回 `delta` 流，但**不保证多模态 token 的原子性**（如图像 token 可能被截断），关键业务建议关闭流式或做服务端聚合；
  - 所有 `image_url`/`audio_url` 必须可公网访问（或已预上传至百炼资产中心），内网地址、临时签名 URL（未设置长时效）将导致加载失败；
  - 实时 API 的 `input.audio` 数据块必须严格匹配 `input_audio_format` 的采样率与位深，否则连接立即中断。

> 提示：最新多模态模型列表与地域支持情况，请始终以 [模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market) 控制台实时展示为准，勿依赖静态文档中的模型 ID 示例。

## 关联主题页

- [start using](../guides/start-using.md)
- [get started with models](../guides/get-started-with-models.md)
- [asset center page](../guides/asset-center-page.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [use cases](../guides/use-cases.md)



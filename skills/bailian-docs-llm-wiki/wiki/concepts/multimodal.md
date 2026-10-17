# 多模态

多模态（Multimodal）指模型能够同时理解、生成或关联两种及以上类型的数据模态（如文本、图像、音频、视频、3D结构等），并在此基础上完成跨模态推理、转换与交互的能力。在百炼平台中，多模态不是单一模型的标签，而是一类能力范式，覆盖从专用单向理解（如图文问答）到全模态联合生成（如音视频+文本协同输出）的完整技术谱系。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型选型层面**：多模态能力由特定模型提供，需显式选择对应标识符。例如：
  - `qwen3.7-vl-plus`、`qwen2.5-vl`：支持图像+文本输入，用于图文理解、OCR、视觉问答；
  - `qwen3.8-omni-flash`：支持文本、图像、音频、视频任意组合输入，具备全模态感知与响应能力；
  - `qwen-audio`：专注语音+文本联合建模，支持ASR、TTS、语音指令理解（仅 DashScope 协议）；
  - `qwen-image-*` 系列：面向图像生成任务，接受文本提示（T2I）或图像+文本（I2I），属生成型多模态；
  - `happyoyster`（世界模型）：融合传感器信号、动作指令、环境观测等多源异构输入，实现具身推理。

- **API 调用层面**：输入数据结构需按模态类型组织：
  - 文本+图像混合输入（如 VL 模型）：在 `messages` 中使用 `content` 数组，内含 `text` 和 `image_url`/`image_data` 类型元素；
  - 音视频输入（如 Omni 模型）：通过 `input.media` 字段传入多个 `{"type": "audio_url", "url": "..."}` 或 `{"type": "video_url", "url": "..."}` 对象；
  - 图像生成类 API（如 `/images/generations`）：`prompt` 为文本，`image` 字段为 Base64 或 URL，构成 T2I/I2I 双模态输入；
  - 视频生成类 API：必须携带 `X-DashScope-Async: enable`，`input` 中 `media` 数组可混合 `image_url`、`video_url`、`audio_url`，体现多模态驱动特性。

- **功能集成层面**：多模态能力常作为基础能力被上层功能复用：
  - 工具调用（`tools`）中，“文搜图”“图搜图”依赖视觉嵌入与文本嵌入的跨模态对齐；
  - 知识库搜索（`file_search`）自动解析 PDF 中的文本+图表+公式，实现文档级多模态理解；
  - 全模态 Agent 可根据用户上传的截图+语音留言+文字补充，统一生成操作建议或代码。

## 关键参数和配置

- **`model`（必填）**：决定多模态能力边界。务必选用明确标注多模态支持的模型 ID（如 `qwen3.7-vl-plus`），纯文本模型（如 `qwen3.7-plus`）无法处理图像/音频输入，将返回 400 错误。
- **`input` 结构（依模型而异）**：
  - VL/OMNI 模型：推荐使用 `messages` 格式，每个 `content` 项为对象数组，支持 `{"type":"text","text":"..."}` 和 `{"type":"image_url","image_url":"..."}` 混合；
  - 图像生成模型：使用 `prompt` + `image`（I2I）或仅 `prompt`（T2I）；
  - 视频/音频模型：必须通过 `input.media` 提交多模态资源，`type` 值须为 `image_url`/`video_url`/`audio_url`/`text` 之一。
- **`parameters.max_tokens`（输出约束）**：控制生成结果的 token 上限，**不影响输入模态数据大小**；图像分辨率、视频时长、音频采样率等由模型自身能力与服务端限制（如图像长边 ≤1536px）共同决定。
- **`stream`（流式支持）**：目前仅部分文本+图像理解模型（如 `qwen3.7-vl-plus`）支持流式响应；视频、3D、全模态生成类模型**不支持流式**，必须等待异步任务完成。
- **地域与域名强绑定**：多模态模型（尤其视频、音频类）对地域敏感，必须确保 API Key、WorkspaceId、Endpoint URL 三者地域一致（如 `cn-beijing`），否则请求失败。

## 面向开发者，简洁实用

- ✅ **快速验证**：在控制台「模型体验」页选择 `qwen3.7-vl-plus`，上传一张图+输入“图中有什么？请用中文描述”，5 秒内获得图文理解结果。
- ✅ **生产接入**：优先选用 `qwen3.8-omni-flash`（全模态）或 `qwen3.7-vl-plus`（图文专用），搭配业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），避免使用 DashScope 兼容域名。
- ⚠️ **避坑提示**：
  - 不要对 `qwen3.7-plus` 传入 `image_url` —— 它只认文本；
  - 调用 `qwen-audio` 时，必须用 DashScope SDK 或原生 HTTP，OpenAI 兼容协议不支持；
  - 视频生成必须带 `X-DashScope-Async: enable` 请求头，漏掉直接报错；
  - 所有媒体 URL 必须公网可访问、HTTPS、无鉴权，临时本地文件需先上传至 OSS 并生成公开 URL。
- 📦 **SDK 推荐**：使用 `dashscope` Python SDK v1.20.0+，其 `MultiModalInput` 工具类可自动组装多模态 `content` 数组，减少格式错误。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [model experience](../guides/model-experience.md)



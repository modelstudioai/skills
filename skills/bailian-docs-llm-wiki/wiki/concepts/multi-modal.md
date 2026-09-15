# 多模态支持

多模态支持是百炼平台的核心能力之一，指系统能够统一理解、生成和协同处理文本、图像、音频、视频、3D 等多种模态数据，并在单次推理或工作流中实现跨模态对齐与联合决策。该能力不依赖用户自行拼接多个单模态模型，而是由原生多模态大模型（如 Qwen-VL、Qwen-Omni、Tripo）或平台级编排机制提供端到端支持。

## 在百炼平台的不同场景中，这个概念如何使用

多模态支持贯穿百炼的三大使用层级，按抽象程度由低到高：

- **模型调用层**：直接调用专用多模态模型 API。例如：
  - 图像生成：使用 `qwen-vl-plus` 或 `wanx` 模型，通过 `/v1/images/generations` 接口传入图文混合 [prompt](../guides/prompt.md)；
  - 视频生成：使用 `wan2.7-t2v` 或 `happyhorse-t2v`，在 `input` 中指定 `prompt`（文）、`img_url`（图）或 `ref_video_url`（视频）；
  - 3D 生成：使用 `Tripo/Tripo-H3.1`，支持 `input.prompt`（文生3D）、`input.image`（单图生3D）或 `input.images`（四视角图生3D）；
  - 音频处理：ASR/TTS/Music Generation 各自独立 endpoint，但共享统一认证与参数范式；
  - 实时多模态交互：通过 `qwen3.5-omni-plus-realtime` WebSocket 连接，同时接收语音输入（`input_audio_buffer.append`）并返回文本+音频流（`response.text.delta` + `response.audio.delta`）。

- **智能体应用层（Agent）**：在零代码/低代码构建的智能体中启用多模态增强能力：
  - 关联含图片/音视频的知识库后，在“检索配置”中开启 **多模态回复增强**，使模型能结合知识库中的图表、截图、示意图等视觉内容生成更准确的回答；
  - Agent 2.0 支持将 OCR 提取的图文、ASR 转写的语音内容自动注入上下文，作为工具调用的输入依据；
  - [长期记忆](long-term-memory.md) 2.0 支持存储和语义检索图文混合历史片段，实现跨会话的多模态上下文延续。

- **工作流编排层（Workflow）**：通过可视化节点串联不同模态能力，例如：
  - “语音输入 → ASR 转文字 → LLM 理解 → 调用图像生成模型 → 返回图文响应”；
  - “用户上传产品图 → 调用万相图生视频 → 生成带商品展示的短视频 → 同步生成字幕（ASR）与配音（TTS）”。

> ✅ 关键提示：并非所有模型都支持全部模态。例如 `qwen-max` 和 `qwq-plus` 为纯文本模型，不支持图像/音频输入；`QwQ` 系列在 Agent 1.0 中明确不支持音视频交互。务必根据场景选择标注为 **多模态（Multimodal）** 或 **全模态（Omni）** 的模型。

## 关键参数和配置

多模态能力的启用与行为控制主要通过以下参数实现（按调用方式分类）：

### 通用参数（所有多模态 API 共享）
| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 必填，必须为多模态模型 ID | `"qwen-vl-plus"`, `"qwen3.5-omni-plus-realtime"`, `"Tripo/Tripo-H3.1"` |
| `X-DashScope-Async: enable` | 异步任务类 API（视频、3D、部分音频）强制要求 | `"enable"` |
| `Authorization: Bearer <api_key>` | 所有 API 均需有效 API Key，且须与模型地域一致 | — |

### 模态特异性参数
| 场景 | 参数名 | 作用 | 注意事项 |
|------|--------|------|----------|
| **图像生成** | `prompt`（支持中英文混写）、`size`（如 `"1024x1024"`）、`quality`（`"hd"`） | 控制图文生成质量与规格 | 千问系列不支持 `quality`；可灵仅支持固定 `size` |
| **视频生成** | `input.prompt` / `input.img_url` / `input.video_url` / `input.audio_url` | 指定输入模态源 | 必须严格匹配模型能力（如数字人驱动需 `image_url` + `audio_url`） |
| **3D 生成** | `input.prompt` / `input.image` / `input.images`（长度为 4 的数组） | 三选一，互斥 | 多图必须按「前/左/后/右」顺序；空视角用 `{}` 占位 |
| **实时 Omni** | `modalities: ["text", "audio"]`、`voice: "Tina"`、`audio.output.format: {type: "wav", sample_rate: 16000}` | 控制输出模态、音色与格式 | `semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持 |
| **智能体应用** | 控制台中开启 **多模态回复增强** 开关 | 启用知识库图文内容参与回答生成 | 仅当关联的知识库已成功解析图片/音视频时生效 |

### 配置要点
- **地域一致性**：多模态模型（尤其视频、3D、实时 Omni）对地域强敏感。例如 Tripo 仅支持华北2（北京），Omni Realtime 必须使用对应地域的 WebSocket endpoint。
- **输入资源要求**：图片需公网可访问 URL 或 Base64；音视频文件需符合格式（MP4/WAV）、尺寸（宽高 ≥400px）、大小（≤10MB–200MB）限制；所有 URL 必须可被百炼服务直连。
- **权限开通**：部分模型（如 `kling`、`emo-detect-v1`、`qwen-voice-enrollment`）需在控制台单独开通，否则调用返回 `403 Forbidden`。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 OpenAI SDK 调用 `qwen-vl-plus`，`messages` 中传入含 `image_url` 的 user message，5 分钟内验证图文理解；
- ✅ **生产推荐**：优先选用 `qwen3.5-omni-plus-realtime`（实时交互）、`qwen-vl-plus-latest`（图文问答）、`wan2.7-t2v`（视频生成）、`Tripo/Tripo-H3.1`（高精度 3D）——这些是当前功能最全、稳定性最高的多模态主力模型；
- ✅ **避坑指南**：
  - 不要混用地域：API Key、WorkspaceId、Endpoint、模型列表必须同属一个地域（如 `cn-beijing`）；
  - 不要硬编码快照模型：避免使用 `qwen-vl-plus-2025-01-25`，改用稳定版 `qwen-vl-plus-latest`；
  - 不要忽略异步轮询：视频/3D/部分音频任务必须轮询 `task_id`，同步调用将报错；
  - 不要跳过前置检测：EMO/LivePortrait 等人像模型需先调用 `detect` 接口校验人脸合规性；
- ✅ **调试技巧**：在智能体应用调试面板中，开启“显示检索片段”，可直观查看图文知识库是否被正确召回并送入模型上下文。

## 关联主题页

- [start using](../guides/start-using.md)
- [get started with models](../guides/get-started-with-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [audio api references](../api/audio-api-references.md)
- [omni realtime api](../api/omni-realtime-api.md)



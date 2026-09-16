# 多模态能力

多模态能力指百炼平台支持同时处理、理解与生成多种类型数据（如文本、图像、视频、音频、3D 网格等）并实现跨模态协同的能力。它不是单一模型，而是平台级能力抽象，体现为统一的 API 设计范式、一致的参数结构、共享的异步任务框架及面向开发者的多模态输入/输出语义表达。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中以**任务驱动、模型可插拔、输入可组合**的方式落地，覆盖五大核心场景：

- **图像生成与编辑**：支持文生图（T2I）、图生图（I2I）、多图参考生成（如 `qwen-image-3.0-pro` 支持 1–3 张参考图）、图像翻译（图文+语言对）、局部重绘（mask+[prompt](../guides/prompt.md)+image）。输入可混合文本提示词（`prompt`）与图像 URL/Base64（`image_url` / `image`），部分模型还接受结构化 `messages` 数组（如图文交错对话式编辑）。

- **视频生成与驱动**：涵盖文生视频、首帧/首尾帧生视频、参考视频风格迁移、数字人驱动（需图像+音频联合输入）、口型同步（`audio_url` + `image_url`）。所有视频 API 均强制异步，且 `input` 字段明确支持多源组合（如 `{"prompt": "...", "image_url": "...", "audio_url": "..."}`），体现强跨模态耦合特性。

- **3D 模型生成**：支持纯文本（`input.prompt`）、单张图像（`input.image`）或四视角图像组（`input.images`，前/左/后/右）三种互斥但语义等价的输入方式，底层统一映射为几何重建任务。`parameters` 中 `pbr` 与 `texture` 的协同控制，也体现了对“视觉表征（贴图）”与“几何结构（网格）”两类模态的解耦管理。

- **音频处理**：虽以单模态接口为主（如 ASR/TTS 各自独立），但在语音对话（`voice-conversation`）和语音翻译场景中，已显式要求音视频协同——例如对话需唤醒词检测（音频）→ 语义理解（文本）→ 语音响应（音频）闭环；语音翻译则隐含“语音→文本→文本→语音”的跨模态链路（当前输出限文本，但架构预留扩展性）。

- **统一模型体验层（Model Experience）**：通过 `/v1/models/{model}/invoke` 接口抽象出通用多模态调用范式。`input` 字段支持灵活嵌套：  
  ```json
  {
    "input": {
      "prompt": "请将这张图转为线稿，并用中文描述细节",
      "images": ["https://...", "https://..."],
      "audio": "https://..."
    }
  }
  ```  
  模型如 `qwen-vl-plus`（视觉语言）、`wanx-video`（视频理解）、`tripo-3d`（图像→3D）均遵循此结构，开发者无需切换协议即可复用鉴权、错误处理与结果解析逻辑。

> ✅ 关键共识：**“多模态”在百炼中不等于“多输入”，而强调“模态语义可识别、可组合、可联合推理”**。例如 `kling/kling-v3-omni-image-generation` 支持“文+图+图”输入并生成分镜组图，其 `input` 中 `prompt` 与两张 `image_url` 具有明确角色分工（主图+参考图），而非简单拼接。

## 关键参数和配置

多模态能力的实现依赖以下通用参数机制，开发者需重点关注：

| 参数 | 位置 | 类型 | 说明 | 典型取值示例 |
|------|------|------|------|--------------|
| `model` | 请求体（必填） | string | 指定具体多模态模型，决定输入/输出模态类型与能力边界 | `"qwen-vl-plus"`, `"wan2.7-videoedit"`, `"Tripo/Tripo-H3.1"` |
| `input` | 请求体（必填） | object | **多模态输入载体**，结构由 `model` 决定，支持字段混用 | `{ "prompt": "...", "image_url": "...", "audio_url": "..." }` |
| `parameters` | 请求体（可选） | object | 控制生成质量、格式、资源消耗等，部分参数跨模态通用 | `{"size": "1024*1024", "n": 2, "style": "anime"}` |
| `X-DashScope-Async: enable` | 请求头（**关键！**） | header | **所有耗时型多模态任务（视频、3D、复杂图像编辑）的强制开关**；缺失将报错 `"current user api does not support synchronous calls"` | `"enable"` |
| `stream` | 请求体（可选） | boolean | 启用流式响应（仅部分多模态模型支持，如 `qwen-vl-plus` 的图文理解流式 token 输出） | `true` |

⚠️ 注意事项：
- **输入互斥性**：同一请求中，`prompt` / `image_url` / `images` / `video_url` / `audio_url` 等字段通常互斥或有明确组合规则（如视频编辑必须含 `video_url` + `prompt`），违反将返回 `InvalidParameter`。
- **地域强绑定**：多模态模型（尤其视频、3D）常限定地域（如 `Tripo` 仅华北2），`model`、API Key、Endpoint 必须三者同地域，否则调用失败。
- **URL 安全要求**：所有 `*_url` 字段必须为 HTTPS 公网可访问地址，内网、带鉴权 Header 或临时签名过期的链接均无效。

## 面向开发者，简洁实用

- **起步建议**：优先使用 `model experience` 统一接口（`/v1/models/{model}/invoke`），它自动适配多模态参数规范，避免记忆各垂直 API 的路径差异。
- **调试技巧**：对多图/多模态输入，先用单模态（如纯 `prompt`）验证模型可用性，再逐步叠加 `image_url` 等字段；利用 `parameters.size` 或 `parameters.n` 快速缩小问题范围。
- **生产注意**：视频、3D、高分辨率图像生成必须启用 `X-DashScope-Async: enable` 并实现轮询逻辑；轮询间隔 ≥15 秒，任务 ID 有效期 24 小时，结果 URL 有效期仅 2 小时（务必及时下载）。
- **避坑清单**：
  - ❌ 不要混用旧版路径（如 `/api/v1/services/aigc/image2video/video-synthesis`）与新版 `wan2.7+` 模型；
  - ❌ 不要在 `Tripo` 请求中传入 `prompt` 和 `image` 同时存在；
  - ❌ 不要忽略 `parameters` 中的硬性约束（如 `qwen-image-3.0-pro` 要求 `size` 总像素在 `512*512` 至 `2048*2048` 之间）；
  - ✅ 推荐使用 Python SDK 的 `MultiModalConversation.call()` 封装，自动处理 `messages` 数组格式与 Base64 编码。

多模态能力是百炼平台的核心差异化优势——它让开发者能用一套思维、一种协议、一个 SDK，无缝调度文本、视觉、音视频与 3D 的智能能力。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [audio api references](../api/audio-api-references.md)
- [model experience](../guides/model-experience.md)



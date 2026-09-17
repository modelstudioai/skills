# 多模态

多模态是指模型能够同时理解、生成或协同处理两种及以上类型的数据（如文本、图像、音频、视频、3D 结构等），并建立跨模态语义关联的能力。在百炼平台中，多模态不是单一模型类别，而是一组具备跨模态输入/输出能力的模型能力集合，覆盖从图文理解、文生图/图生图，到音视频端到端处理、3D 生成等全栈场景。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中按**输入模态组合**和**输出目标类型**解耦为多个独立服务，开发者需根据任务选择对应 API 和模型：

- **图文理解与生成（Text + Image）**  
  使用 `qwen-vl-max`、`qwen3-vl-plus`、`QVQ` 等 VL（Vision-Language）模型，通过 `messages` 中嵌入 `image_url` 或 Base64 图像数据实现图文问答、描述生成、视觉推理等。  
  ✅ 支持：`Generation.call()` 接口（DashScope SDK）、OpenAI 兼容 `/chat/completions`  
  ❌ 不支持：纯文本模型（如 `qwen-plus`）若含 `image_url` 将触发 `InvalidParameter` 错误  

- **文生图 / 图生图（Text → Image / Image → Image）**  
  调用专用图像生成 API（`/v1/images/generations`），使用 `wanx-v1`、`kling-v2`、`zimage-v1` 等模型。输入为 `prompt`（文本）或 `image_url`（图像），不走通用 `messages` 流程。  
  ✅ 支持：`size`、`n`、`seed` 等图像专属参数  
  ❌ 不支持：`messages` 格式；`image_base64` 必须为合法 Base64 字符串（无 `data:image/...;base64,` 前缀）  

- **音视频理解与生成（Text + Audio/Video）**  
  - *端到端音视频理解*：使用 `qwen3.8-omni-flash`（支持音频+视频 URL 输入）或 `qwen3.5-omni-realtime`（实时 WebSocket 流式语音交互）；  
  - *语音识别（ASR）/合成（TTS）*：调用 `/v1/asr` 或 `/v1/tts` 独立接口，非多模态模型，但常作为多模态 pipeline 的前置/后置组件；  
  - *图生视频/文生视频*：使用 `/v1/videos/generations`，传 `input.prompt` + `input.image_url`（可选）+ `input.audio_url`（仅 `MiniMax`/人像驱动）。  

- **3D 生成（Text/Image → 3D）**  
  使用 Tripo 模型（`Tripo/Tripo-H3.1`），通过 `/v1/services/aigc/video-generation/3d-generation` 异步 API，支持文生3D、单图生3D、四视图生3D。输入为 `prompt` 或 `image_url` 数组，输出为 GLB/PBR 模型 URL。  

- **实时多模态对话（Text + Audio + Tool）**  
  通过 `qwen-omni-*realtime` WebSocket 接口，支持语音输入（`input_audio_buffer.append`）、文本输入（`input_text`）、工具调用（`tool_use`）与混合输出（`["text", "audio"]`），实现端到端低延迟交互。

> ⚠️ 关键约束：所有多模态调用均需严格匹配模型协议——Qwen-Audio 仅支持 DashScope 原生协议；QwQ/QVQ 模型不接受 `system` 消息；`qwen3.5-omni-realtime` 系列不可修改 `temperature` 等采样参数（`turbo` 系列完全锁定）。

## 关键参数和配置

| 场景 | 关键参数 | 说明 | 示例值 |
|--------|----------|------|--------|
| **图文理解（VL 模型）** | `messages[].content` | 必须为数组，含 `text` 和/或 `image_url` 对象 | `[{"type": "text", "text": "图中有什么？"}, {"type": "image_url", "image_url": "https://xxx.jpg"}]` |
| | `model` | 严格使用 VL 模型 ID | `"qwen3-vl-plus"` |
| **文生图/图生图** | `prompt` | UTF-8 文本，长度 ≤512（万相为1024） | `"青花瓷风格的猫，水墨背景"` |
| | `image_url` | 公网可访问 HTTPS 链接（JPG/PNG，≤10MB） | `"https://example.com/input.png"` |
| | `size` | `WxH` 格式，依模型支持范围而定 | `"1024x1024"` |
| **音视频理解（Omni）** | `input.audio_url` / `input.video_url` | 公网可访问，MP4/WAV/MP3，≤100MB | `"https://xxx.mp4"` |
| | `modalities`（Realtime） | 输出模态组合 | `["text", "audio"]` |
| | `voice`（Realtime） | 音色名称或复刻 ID | `"Cherry"` 或 `"voice_abc123"` |
| **3D 生成** | `input.prompt` / `input.image` / `input.images` | 三者互斥，不可共存 | `{ "prompt": "简约风陶瓷杯" }` |
| | `geometry_quality` | 仅 `Tripo-H3.1` 支持 | `"ultra"` |
| | `pbr`, `texture` | 控制是否生成材质与贴图 | `true`, `false` |

> 💡 提示：所有多模态请求必须使用**业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），且地域强绑定（如 Tripo 仅支持华北2）；API Key 需提前开通对应模型权限，免费试用额度不通用（例：`wanx-v1` 可试用，`kling-v2` 需后付费）。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 DashScope CLI 运行 `dashscope api call --model qwen3-vl-plus --messages '[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":"https://xxx.jpg"}]}]'`  
- ✅ **错误排查**：遇到 `InvalidParameter`，优先检查 `model` 是否为 VL 模型、`messages` 是否含非法字段（如 `system`）、`image_url` 是否可公开访问  
- ✅ **性能优化**：图文理解类请求建议压缩图像至 1024px 短边；视频生成类任务启用异步回调替代高频轮询（`X-DashScope-Async: enable`）  
- ❌ **禁止操作**：不要在非 VL 模型请求中混入图像；不要在图像生成 API 中使用 `messages`；不要跨地域复用 Workspace ID  
- 📦 **SDK 推荐**：Python 开发首选 `dashscope>=1.27.3`（内置 SDK Expert 自动补全多模态参数）；实时语音场景必用 `dashscope>=1.32.0`（WebSocket 支持完整）  

多模态是百炼平台的核心差异化能力，其价值在于“按需组合”——开发者无需自建 pipeline，直接调用原子化 API 即可构建图文分析、AIGC 创作、虚拟人交互等复杂应用。

## 关联主题页

- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [audio api references](../api/audio-api-references.md)
- [omni realtime api](../api/omni-realtime-api.md)



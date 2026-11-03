# 多模态

多模态（Multimodal）指模型能够同时理解、生成或关联两种及以上类型的数据模态（如文本、图像、音频、视频等），并在此基础上完成跨模态推理、转换或交互任务。在百炼平台中，多模态不是单一能力，而是贯穿模型设计、API 接口与应用场景的系统性架构特征。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用大模型调用（OpenAI 兼容 API / DashScope SDK）**：  
  `qwen3.8-omni-flash`、`qwen3.7-plus`、`qwen3.8-max` 等旗舰模型原生支持**图文混合输入**（如用户消息中同时包含 `text` 字符串和 `image_url` 或 Base64 图像数据），输出为结构化文本（支持 JSON 格式）、工具调用或思考链。适用于文档解析、商品识别、教育问答等视觉增强型对话场景。

- **实时音视频交互（Omni Realtime API）**：  
  `qwen3.8-omni-flash-realtime` 等模型提供端到端**流式多模态会话能力**：支持 PCM/WAV 音频 + Base64 图像 + H.264 视频（Qwen3.8+）同步输入，实时输出流式文本（`text.delta`）与流式音频（`audio.delta`），并内置语音活动检测（VAD）、自动打断、ASR 转录等感知层能力。典型用于智能座舱、远程医疗问诊、双语会议实时翻译等低延迟交互场景。

- **图像/视频生成（Image & Video Generation API）**：  
  多模态体现为**跨模态条件控制**：文生图（T2I）、图生图（I2I）、首帧/首尾帧生视频、参考视频编辑等均要求模型联合理解文本语义与视觉内容。例如 `wan3.0-video` 和 `qwen-image-3.0-pro` 支持 `input.messages.content` 中混合 `text` 提示词与多个 `image` URL，实现“用文字描述风格 + 用图片定义构图”的精准生成。

- **3D 生成（3D Generation API）**：  
  `Tripo/Tripo-H3.1` 等模型将文本提示（`prompt`）或单/多张参考图（`image` / `images`）作为输入，直接生成三维网格或 Gaussian Splatting 表示——这是典型的**文本→3D** 或 **2D图像→3D** 跨模态映射，属于生成式多模态的高阶形态。

> ⚠️ 注意：并非所有“支持图像/音频”的模型都具备真正多模态能力。例如部分语音模型仅支持 ASR（音频→文本）或 TTS（文本→音频），属单向模态转换；而百炼标注为“全模态”或“Omni”的模型（如 `qwen3.8-omni-*` 系列），才具备统一编码器下的联合感知与生成能力。

## 关键参数和配置

| 场景 | 参数名 | 说明 | 实际取值示例 |
|------|--------|------|--------------|
| **通用多模态模型（OpenAI 兼容）** | `messages.content` | 必须为数组，支持混合 `text` 和 `image_url` / `image`（Base64）对象 | `[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]` |
| **Omni Realtime API** | `modalities` | 指定服务端返回的模态组合 | `["text","audio"]`（不可仅设 `["audio"]`） |
| | `session.video.input.representation_compact` | 启用视频输入支持（Qwen3.8+） | `true` |
| | `audio.input.format.type` / `.sample_rate` | 输入音频格式与采样率（Qwen3.8 仅支持 `pcm` + `16000`） | `{"type":"pcm","sample_rate":16000}` |
| **图像/视频生成 API** | `input.messages.content`（图像） | 图像生成类接口统一输入结构 | `[{"type":"text","text":"赛博朋克风格的咖啡馆"},{"type":"image_url","image_url":"https://..."}]` |
| | `input`（视频） | 视频生成接口中，根据任务类型选择字段：`prompt`、`img_url`、`first_frame_url`、`reference_media` 等 | `{"first_frame_url":"https://...", "prompt":"让机器人动起来"}` |
| **3D 生成 API** | `input.prompt` / `input.image` / `input.images` | 三者互斥，决定输入模态来源 | `"一只陶瓷质感的机械猫"` 或 `{"image":"data:image/jpeg;base64,..."} ` |

- 所有涉及图像/视频/音频的输入，**必须使用 Base64 编码（`data:image/...;base64,...`）或公网可访问的 HTTPS URL**；本地文件路径无效。
- 多模态输入长度受模型上下文窗口限制：图文混合时，图像 token 占比显著高于文本（具体换算见各模型文档），建议优先使用紧凑格式（如 WebP）并控制单次输入图像数量（通常 ≤4 张）。
- 实时 API 中，`enable_search` 与 `tools` 参数互斥，二者均需在多模态理解基础上触发，但不可同时启用。

## 面向开发者，简洁实用

- ✅ **选型原则**：  
  - 做图文问答/报告分析 → 用 `qwen3.8-omni-flash`（OpenAI 兼容）  
  - 做语音助手/视频会议 → 用 `qwen3.8-omni-flash-realtime`（WebSocket）  
  - 做 AI 设计/营销素材 → 用 `qwen-image-3.0-pro` 或 `wan3.0-video-generation`（专用生成 API）  
  - 做数字人/3D 应用 → 用 `Tripo/Tripo-H3.1`（异步 3D 生成）

- ✅ **调试技巧**：  
  - 图像无法识别？检查 `content` 是否为合法数组、`image_url.url` 是否可公开访问、Base64 是否缺少 `data:` 前缀。  
  - 实时 API 连接失败？确认 WebSocket Endpoint 域名含 WorkspaceId，且 `modalities` 至少含 `"text"`。  
  - 视频生成报错 “invalid input format”？验证 `input` 结构是否匹配所选模型类型（T2V/I2V/V2V），勿混用字段。

- ✅ **避坑提醒**：  
  - `qwen3.8-flash` 是纯文本模型，**不支持图像输入**；名称含 `omni` 或 `realtime` 才代表多模态能力。  
  - OpenAI 兼容 API 的 `stream=true` 对多模态模型非强制，但 `qwen-audio-3.1-realtime-plus` 等实时模型**必须开启流式**。  
  - 所有生成类 API（图像/视频/3D）均为**异步调用**，需轮询 `task_id`，不可等待同步响应。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)



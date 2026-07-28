# 多模态

多模态（Multimodal）指模型能够同时理解或生成文本、图像、音频、视频等多种信息模态的能力。在百炼平台上，多模态贯穿于实时交互、内容生成、向量检索与模型选型等多个产品线，是构建语音助手、视频创作、跨模态搜索等应用的基础能力。

## 在百炼平台的主要使用场景

### 实时多模态交互（Realtime / Omni）

- **Qwen-Omni-Realtime API**：基于 WebSocket 的实时多模态对话接口，支持音频、图像（视频帧）与文本的流式输入输出，输出模态通过 `modalities` 配置为 `["text"]` 或 `["text","audio"]`（默认）。适用于语音助手、音视频客服、实时同传等场景。
- **Realtime API 接入方案**：提供 WebSocket、WebRTC、AOQ（AI over QUIC）三种传输协议。服务端集成选 WebSocket；浏览器端选 WebRTC；移动端原生、弱网环境选 AOQ（内置回声消除、降噪与弱网对抗）。
- 代表模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`，以及多模态开发套件 `multimodal-dialog`。

### 多模态内容生成（视频生成）

视频生成 API 统一采用异步任务模式（创建任务 → 轮询结果），多个模型家族支持多模态输入：

- **万相 wan2.7**：图生视频支持文本/图像/音频/视频多模态输入；参考生视频（`wan2.7-r2v`）以图片/视频/音频为参考，保持角色形象与音色一致。
- **数字人/对口型**：`wan2.2-s2v`（图片 + 音频生成说话视频）、`pixverse-lipsync`（音频或 TTS 文本驱动对口型）等，均属于跨模态驱动生成。

### 多模态向量（Multimodal Embedding）

将文本、图片、视频映射到同一语义空间，支持跨模态检索、相似度计算与聚类：

- 端点：`POST .../services/embeddings/multimodal-embedding/multimodal-embedding`，输入为 `input.contents` 数组，元素支持 `text`、`image`（URL 或 Base64）、`video`（仅 URL）。
- 支持**独立向量**（每个输入各生成一个向量）与**融合向量**（`qwen3-vl-embedding` 通过 `parameters.enable_fusion=true` 开启；`qwen2.5-vl-embedding` 仅支持融合向量）。
- 代表模型：`qwen3-vl-embedding`、`multimodal-embedding-v1`、`tongyi-embedding-vision-*` 系列。

### 多模态理解与文件输入

- 视觉理解首选 `qwen3.7-plus`：1M 上下文、单图最高 1600 万像素、视频最长 2 小时 / 2GB。图片 Token 消耗约 `h x w / (32 x 32) + 2`。
- 需要文件输入的多模态理解、文档解析等能力，需先通过文件管理 API 上传文件获取文件标识，再在模型调用中引用（"先上传、再引用、后清理"）。
- 全模态选型：首选 `qwen3.5-omni-plus`，低成本可选 `qwen3-omni-flash`。

## 关键参数与限制

| 参数/限制 | 说明 |
| --- | --- |
| `modalities` | Realtime 会话的输出模态，`["text"]` 或 `["text","audio"]` |
| 音频格式 | Omni Realtime 输入仅 16 kHz PCM，输出仅 24 kHz PCM |
| 图像输入 | Realtime 场景 JPG/JPEG，建议 480p/720p，Base64 后 ≤256KB，约 1 张/秒，且须在发送过音频后再发图像 |
| `enable_fusion` | 多模态向量是否生成融合向量（`qwen3-vl-embedding`） |
| `fps` / `max_video_frames` | 多模态向量视频抽帧控制 |
| 内容条数 | 如 `qwen3-vl-embedding` 单次内容元素 ≤20、图片 ≤10 张、视频 ≤1 个 |

## 开发者建议

- **实时对话**选 Omni Realtime 系列并按端侧环境选协议；**离线理解**选视觉理解模型 + 文件管理 API；**跨模态检索**选多模态 Embedding。
- 多模态调用的计费和[限流](rate-limit.md)通常按模态分别计量（如图片按像素折算 Token），集成前先确认目标模型支持的模态组合与输入规格。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [video generation api](../api/video-generation-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [file management api](../api/file-management-api.md)
- [realtime api user guide](../guides/realtime-api-user-guide.md)
- [model experience](../guides/model-experience.md)



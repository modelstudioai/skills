# 多模态能力

多模态能力指模型同时理解或生成文本、图像、音频、视频、3D 等多种模态内容的能力。在百炼平台上，它既体现为「输入多模态」（如图文混合输入、音视频实时对话），也体现为「输出多模态」（如文生图、文生视频、语音合成、3D 资产生成）。

## 在百炼平台的主要场景

百炼按模态与任务把能力拆分到多个方向，开发者可按需组合：

- **实时音视频对话**：Qwen-Omni-Realtime 系列通过 WebSocket 提供低延迟的语音输入/输出、图像输入、语音活动检测（VAD）、工具调用与联网搜索，适用于智能客服、语音助手等实时交互场景。
- **图像生成与编辑**：覆盖文生图、图生图、局部重绘、扩图、背景生成、虚拟模特、AI 试衣、创意海报等，涉及千问 Qwen-Image、万相 Wan/Wanx、Z-Image、可灵 Kling、Vidu 等模型家族。
- **视频生成与编辑**：聚合万相 Wan、HappyHorse、PixVerse、Vidu、可灵 Kling 及人像驱动模型，支持文生视频、图生视频（首帧/首尾帧/续写）、参考生视频、视频编辑与数字人。
- **3D 资产生成**：基于 Tripo 模型支持文生 3D、单图生 3D、多图生 3D，产出带 PBR 材质或无贴图的 GLB 模型。
- **视觉理解与 OCR**：以 Qwen 旗舰多模态模型理解图像与长视频（最长约 2 小时），并提供专优的 OCR/文档提取能力。
- **语音合成 / 识别 / 语音转语音**：TTS、ASR、声音复刻/设计、S2S 实时对话与同传翻译，以及音乐生成。

## 输入与协议

- **实时流式（WebSocket）**：延迟最低，适合实时交互。Omni-Realtime 通过 `input_audio_buffer.append`（PCM 音频，Base64）、`input_image_buffer.append`（JPG/JPEG，Base64）等事件送入多模态素材，`session.update` 的 `modalities` 控制输出模态（`["text"]` 或 `["text","audio"]`）。
- **HTTP 同步**：新一代图像模型（如 `wan2.6-image`、`wan2.7-image`、`z-image-turbo`）支持一次请求返回结果，路径为 `.../aigc/multimodal-generation/generation`，请求体用 `messages` 结构，`content` 内混排 `text` 与 `image`。
- **HTTP 异步**：图像、视频、3D 生成等耗时任务（约 1-5 分钟）统一采用「创建任务拿 `task_id` → 轮询查询」两步流程，创建时必须携带请求头 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。`task_id` 有效期 24 小时，切勿重复创建，轮询即可。

## 关键参数与配置

不同模态的请求体大多由 `model`、`input`、`parameters` 三部分组成：

- **实时对话**（`session.update`）：`modalities`、`voice`（音色，因模型而异）、`input_audio_format` / `output_audio_format`（仅 `pcm`，输入 16kHz、输出 24kHz）、`turn_detection.type`（`server_vad` / `semantic_vad`）及 `threshold`、`silence_duration_ms` 等。
- **图像生成**：`input.prompt` / `negative_prompt`（或新协议 `messages`），图像编辑用 `images` / `image_url` / `mask_image_url`；`parameters` 含 `size`（如 `1024*1024`、`1K`/`2K`/`4K`）、`n`、`aspect_ratio`、`watermark`、`prompt_extend` 等。
- **视频生成**：`input.prompt` 描述画面镜头，`input.media` 承载 `first_frame` / `last_frame` / `reference_image` / `video` 等素材；`parameters` 含 `resolution`（`480P`/`720P`/`1080P`）、`duration`、`ratio` 等。
- **3D 生成**：`prompt`、`image`、`images` 三者互斥；`parameters` 含 `texture_quality`、`geometry_quality`、`pbr`、`texture`。

## 注意事项

- **地域隔离**：模型、Endpoint URL 与 API Key 必须属于同一地域，华北2（北京）、新加坡、美国（弗吉尼亚）等地域各自独立、不可混用；部分能力（如 Tripo 3D、Fun-Music）仅在特定地域可用。推荐迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得更好性能与稳定性。
- **产物有效期**：图像结果 URL 有效期 24 小时，3D 模型下载链接仅 2 小时，务必及时下载。
- **计费**：图像等仅对成功生成的输出计费，输入与失败任务不计费；具体计费、上下文窗口等实时参数以模型广场为准。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [model experience](../guides/model-experience.md)



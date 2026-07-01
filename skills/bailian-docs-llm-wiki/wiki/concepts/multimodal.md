# 多模态

多模态（Multimodal）是指模型同时处理和生成多种信息形态（如文本、图像、音频、视频、3D）的能力。在百炼平台中，多模态贯穿从输入理解到内容生成的各类 API 和模型服务。

## 在百炼平台中的应用场景

### 实时多模态交互（Omni Realtime）

Qwen-Omni-Realtime 系列模型通过 WebSocket 长连接实现低延迟的语音、视频、图像实时对话。支持 VAD 自动检测与 Manual 手动控制两种交互模式，适用于语音助手、客服、同声传译等场景。代表模型包括 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`。

### 图像生成与编辑

百炼提供通义千问、万相、Z-Image、可灵等多个图像生成模型族，覆盖文生图、图像编辑、局部重绘、涂鸦作画等能力。推荐使用 `wan2.7-image-pro` 进行全功能图像生成与编辑，支持文字渲染、品牌色控制和多图生成。

### 视频生成与编辑

支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑等任务。万相2.7 和 HappyHorse 1.1 系列支持文本、图像、音频、视频等多模态输入，可保持角色形象与音色一致性。所有视频生成接口采用[异步调用](async-invocation.md)模式。

### 视觉理解

Qwen3.7/3.6/3.5 系列视觉理解模型支持图像分析、视频理解和 OCR，最长支持 2 小时视频输入，每张图像最高 1600 万像素。

### 3D 模型生成

基于 Tripo 模型实现文生 3D、单图生 3D 和多图生 3D，产出 GLB 格式的 PBR 材质模型，适用于游戏、AR 和影视场景。

### 模型调优

百炼支持对视觉理解（Qwen-VL 系列）、图像生成（wan2.7-image）、视频生成（wan2.5/2.2）和语音合成（CosyVoice）等多模态模型进行微调，开发者可用自有数据定制特定场景的生成效果。

## 关键参数与配置

| 参数/配置 | 场景 | 说明 |
|-----------|------|------|
| `modalities` | Omni Realtime | 指定会话支持的模态类型（audio、video、text） |
| `turn_detection.type` | Omni Realtime | 交互模式：`server_vad`（自动检测）/ `semantic_vad` / `null`（手动） |
| `X-DashScope-Async: enable` | 视频/3D 生成 | 异步任务必须携带此请求头 |
| `size` / `resolution` | 图像/视频生成 | 输出分辨率控制，各模型支持的尺寸集合不同 |
| `prompt` + `image`/`video` | 视觉理解/编辑 | 同时传入文本指令与视觉输入实现多模态理解或编辑 |

## 开发建议

1. **模型选型**：文本+视觉理解优先选 `qwen3.7-plus`；实时语音交互选 Omni Realtime 系列；图像生成选 `wan2.7-image-pro`；视频生成选 HappyHorse 1.1 或 wan2.7 系列。
2. **协议选择**：图像/视频/3D 生成多为异步任务，需通过 task_id 轮询结果；实时交互使用 WebSocket 长连接。
3. **地域一致性**：模型、Endpoint URL、[API Key](api-key.md) 必须属于同一地域，跨地域调用会失败。
4. **内容安全**：所有多模态接口内置内容安全审核，违规输入会被拒绝。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [model experience](../guides/model-experience.md)
- [fine tuning](../guides/fine-tuning.md)
- [3d generation](../api/3d-generation.md)



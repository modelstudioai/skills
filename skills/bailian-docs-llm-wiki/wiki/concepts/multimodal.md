# 多模态

多模态是指模型同时处理和生成文本、图像、音频、视频、3D 等多种信息形态的能力。百炼平台围绕多模态提供了从理解到生成的完整模型矩阵和 API 体系，开发者可按业务场景灵活组合不同模态的能力。

## 多模态能力矩阵

百炼平台的多模态能力按输入/输出模态可分为以下几类：

| 能力方向 | 输入模态 | 输出模态 | 代表模型/接口 |
|---------|---------|---------|-------------|
| 视觉理解 | 图像/视频 + 文本 | 文本 | qwen3.7-plus（支持图像分析、最长 2 小时视频理解） |
| 实时多模态交互 | 语音/视频/图像 | 语音 + 文本 | Qwen-Omni-Realtime 系列 |
| 图像生成与编辑 | 文本/图像 | 图像 | 万相 2.7、Z-Image、千问-文生图 |
| 视频生成与编辑 | 文本/图像/音频/视频 | 视频 | 万相 2.7、HappyHorse、PixVerse、Vidu、可灵 |
| 3D 模型生成 | 文本/图像 | GLB 模型 | Tripo-H3.1、Tripo-P1.0 |
| 语音合成 | 文本 | 音频 | CosyVoice、MiniMax-speech |
| 数字人/人像动画 | 图像 + 音频 | 视频 | wan2.2-s2v、AnimateAnyone、EMO |

## 实时多模态交互

Qwen-Omni-Realtime 系列通过 WebSocket 长连接实现低延迟的语音、视频、图像实时对话，是百炼平台最具代表性的多模态能力之一。

**核心模型**：
- `qwen3.5-omni-realtime`：最新版本，支持语义 VAD、联网搜索、静默超时主动引导
- `qwen3-omni-flash-realtime`：支持回复风格控制
- `qwen-omni-turbo-realtime`：轻量版，部分参数不可调

**交互模式**：
- **VAD 模式**（默认）：服务端自动检测语音起止，适合自然对话。关键参数包括 `threshold`（灵敏度，默认 0.5）、`silence_duration_ms`（静音判定，默认 800ms）、`idle_timeout_ms`（静默超时，5000-30000ms）
- **Manual 模式**：客户端显式控制音频提交与响应触发，适合按下即说场景

**接入地址**：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`（北京），新加坡使用[业务空间](workspace.md)专属域名。

## 图像生成与编辑

百炼提供多层次的图像多模态能力：

- **通用文生图**：万相 2.7（推荐）、Z-Image、千问-文生图，支持中文语义、多尺寸、风格控制
- **图像编辑**：万相-通用图像编辑 2.5/2.7，支持按自然语言指令局部修改
- **创意工具**：虚拟模特、AI 试衣、创意海报、图像背景生成等垂类接口

调用协议分两种：OpenAI 兼容模式（同步）和 DashScope 原生异步模式（提交任务 → 轮询结果）。

## 视频生成

视频生成全部采用异步调用模式，统一流程为创建任务后轮询 `task_id` 获取结果，处理时间通常 1-5 分钟。

**主要能力**：文生视频、图生视频（首帧/首尾帧）、参考生视频（保持角色一致性）、视频编辑、动作迁移、数字人。万相 2.7 是当前推荐版本，支持多模态输入（文本、图像、音频、视频混合）和多镜头叙事。

## 3D 生成

基于 Tripo 模型，支持文生 3D、单图生 3D、多图生 3D，输出 GLB 格式 PBR 材质模型。同样采用异步调用，建议轮询间隔 15 秒。仅限华北2（北京）地域。

## 关键开发要点

1. **协议选择**：实时交互走 WebSocket；图像/视频/3D 生成多为异步 REST（`X-DashScope-Async: enable`）；部分图像接口支持 OpenAI 兼容同步调用
2. **鉴权统一**：所有接口使用 `Authorization: Bearer <API_KEY>`，[API Key](api-key.md) 在百炼控制台获取
3. **图片传输**：输入支持公网 URL 或 Base64，输出为临时 URL（需及时下载）
4. **Prompt 技巧**：不同模态的 Prompt 设计有各自最佳实践——文生图侧重「主体 + 场景 + 风格」，文生视频增加「运动 + 运镜」，万相 2.7 还支持多镜头分镜描述
5. **地域限制**：3D 生成、部分第三方视频模型（PixVerse、Vidu、可灵）仅限北京地域

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [use cases](../guides/use-cases.md)
- [3d generation](../api/3d-generation.md)



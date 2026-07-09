# model experience

百炼平台模型体验中心提供覆盖文本、视觉、语音、视频、图片、3D、音乐及向量检索等全模态的模型能力。开发者可根据应用场景，从模型广场选择合适的模型，通过 OpenAI 兼容 API 或专用协议快速接入。

## 文本生成

文本生成是最基础的模型能力，覆盖聊天机器人、Agent 开发、内容生成、文档处理等场景。详细选型指南参见[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

### 推荐模型

| 模型 ID | 上下文 | 思考模式 | Function Calling | 内置工具 | 结构化输出 |
|---------|--------|---------|-----------------|---------|-----------|
| `qwen3.7-max` | 1M | 支持 | 支持 | 支持 | 不支持 |
| `qwen3.7-plus` | 1M | 支持 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 支持 | 支持 | 支持 | 支持 |
| `deepseek-v4-pro` | 1M | 支持 | 支持 | 不支持 | 不支持 |
| `deepseek-v4-flash` | 1M | 支持 | 支持 | 不支持 | 不支持 |

### 选型建议

- **Agent/编程**：`qwen3.7-plus`（能力与成本均衡，完整工具调用，1M 上下文）
- **最强推理**：`qwen3.7-max`
- **低成本**：`qwen3.6-flash`（效果接近旗舰，价格更低）
- **代码专用**：`qwen3-coder-plus`（1M 上下文，支持思考模式）

### 关键功能

- **思考模式**：通过 `enable_thinking` 参数开启逐步推理，所有 Qwen3 及以上模型支持
- **Function Calling**：所有通用模型均支持自定义工具调用
- **内置工具**：联网搜索、代码解释器、网页抓取等（仅部分模型支持）
- **结构化输出**：获取有效 JSON 返回
- **批量推理**：大量请求且对延迟要求不高时可降低成本

## 视觉理解

支持图像分析、视频理解、OCR 等场景。详细信息参见[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

### 推荐模型

| 模型 ID | 上下文 | 最大视频时长 | 最大图片数 | Function Calling |
|---------|--------|------------|-----------|-----------------|
| `qwen3.7-plus` | 1M | 2小时 | 2048 | 支持 |
| `qwen3.6-flash` | 1M | 2小时 | 256 | 支持 |
| `qwen3.5-omni-plus` | 64k | 1小时 | 2048 | 支持 |

### 关键参数

- **图像分辨率**：大多数模型支持每张图片最高 1600 万像素
- **[Token](../concepts/token.md) 计算**：每张图片 [Token](../concepts/token.md) 数 = `h x w / (32 x 32) + 2`
- **OCR**：`qwen3.5-ocr` 专为文档、表格、手写内容文字提取而优化

## 视频生成与编辑

覆盖文生视频、图生视频、参考生视频、视频编辑和角色动画等场景。详细信息参见[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

### 推荐模型

| 模型 ID | 场景 | 最大分辨率 | 最大时长 |
|---------|------|-----------|---------|
| `happyhorse-1.1-t2v` | 文生视频（有声） | 1080P | 3-15秒 |
| `happyhorse-1.1-i2v` | 首帧生视频 | 1080P | 3-15秒 |
| `happyhorse-1.1-r2v` | 参考生视频 | 1080P | 3-15秒 |
| `wan2.7-t2v-2026-06-12` | 文生视频（自定义音频） | 1080P | 2-15秒 |
| `wan2.7-i2v-2026-04-25` | 首尾帧生视频 | 1080P | 2-15秒 |
| `happyhorse-1.0-video-edit` | 视频编辑 | 1080P | 3-15秒 |

### 使用要点

- HappyHorse 1.1 系列默认生成有声视频，支持 1080P
- 首尾帧生视频可通过串联多片段构建长视频
- 角色动画使用 `wan2.2-animate-move`（动作迁移）和 `wan2.2-animate-mix`（人物替换）

## 图片生成与编辑

覆盖文生图、图片编辑、角色一致性多图生成等场景。详细信息参见[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

### 推荐模型

| 模型 ID | 场景 | 编辑 | 最大分辨率 |
|---------|------|------|-----------|
| `wan2.7-image-pro` | 文字渲染、品牌色、角色一致性 | 支持 | 4096x4096 |
| `z-image-turbo` | 快速生成、写实人像 | 不支持 | 2048x2048 |
| `qwen-image-2.0-pro` | 负向提示词、最多6张变体 | 支持 | 2048x2048 |

### 选型建议

- 默认选 `wan2.7-image-pro`：集成文字渲染、品牌色、编辑等功能
- 速度优先选 `z-image-turbo`：生成速度快 10 倍，价格约 1/5
- 需要负向提示词选 `qwen-image-2.0-pro`

## 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D 三种模式。详细信息参见[Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

| 模型名称 | 产物最高面数 | 速度 | 适用场景 |
|---------|------------|------|---------|
| `Tripo/Tripo-H3.1` | 200 万面 | 较慢 | 影视级渲染、高精度数字资产 |
| `Tripo/Tripo-P1.0` | 2 万面 | 更快 | 快速预览、游戏/AR 场景 |

> **注意**：Tripo 模型仅适用于华北2（北京）地域，必须使用该地域的 API Key。

### 关键参数

- `texture_quality`：`standard`（默认标清）/ `detailed`（高清贴图）
- `geometry_quality`：`standard`（默认 150 万面）/ `ultra`（200 万面），仅 Tripo-H3.1 支持
- 产物为 GLB 格式，可直接导入 Blender、Unity

## 语音合成（TTS）

覆盖标准合成、声音复刻、声音设计和指令控制等场景。详细信息参见[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。

### 推荐模型

| 模型 ID | 接入方式 | 声音复刻 | 声音设计 | 指令控制 |
|---------|---------|---------|---------|---------|
| `cosyvoice-v3.5-plus` | WebSocket / HTTP | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | WebSocket / HTTP | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | HTTP | 支持 | 不支持 | 不支持 |

### 选型维度

- **标准合成**（内置音色）：`cosyvoice-v3-plus` 或 `MiniMax/speech-2.8-hd`
- **自定义音色**：`cosyvoice-v3.5-plus`（声音复刻 + 声音设计）
- **低延迟实时**：WebSocket 接入（音频边合成边返回）
- **指令控制**：通过自然语言动态控制语速、情绪和风格

## 语音转语音（S2S）

端到端语音交互，无需 ASR + LLM + TTS 三段拼接，延迟更低。详细信息参见[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

### 推荐模型

| 场景 | 推荐模型 | 接口 |
|------|---------|------|
| 语音助手/客服对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译/直播翻译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音/播客翻译 | `qwen3-livetranslate-flash` | HTTP |

### S2S vs Pipeline 选型

- **S2S**：低延迟、端到端音频感知、通过系统提示词选择预设音色
- **Pipeline（ASR + LLM + TTS）**：支持声音克隆/设计，可分别选择最优组件

## 语音识别（ASR）

覆盖实时语音识别和录音文件转写场景。详细信息参见[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

### 推荐模型

| 模型 ID | 模式 | 精度增强 | 说话人分离 | 情感识别 |
|---------|------|---------|-----------|---------|
| `fun-asr-realtime` | 实时 | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | 热词 | 支持 | 不支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | Prompt 上下文 | 不支持 | 支持 |
| `qwen3-asr-flash-realtime` | 实时 | 不支持 | 不支持 | 支持 |

### 选型维度

- **实时 vs 非实时**：实时基于 WebSocket 流式，非实时基于 HTTP 提交文件
- **专业术语处理**：Prompt 上下文注入（Qwen3.5-Omni）或热词表（Fun-ASR）
- **说话人分离**：仅 Fun-ASR 系列非实时模型支持

## 音乐生成

Fun-Music 支持通过提示词或自定义歌词生成完整歌曲或纯音乐。详细信息参见[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

| 模型 ID | [prompt](prompt.md) | lyrics | 纯音乐 | 性别选择 |
|---------|--------|--------|--------|---------|
| `fun-music-v1` | 与 lyrics 至少传一个 | 与 [prompt](prompt.md) 至少传一个 | 支持 | 支持 |
| `fun-music-preview` | 必选 | 可选 | 支持 | 不支持 |

> **注意**：Fun-Music 目前处于邀测阶段，仅在华北2（北京）地域可用。

## 向量与重排序

覆盖语义搜索、RAG 检索、跨模态匹配和重排序场景。详细信息参见[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

### 推荐模型

| 模型 ID | 类型 | 向量维度 | 最大 [Token](../concepts/token.md) |
|---------|------|---------|-----------|
| `text-embedding-v4` | 文本 Embedding | 64~2048（默认 1024） | 8,192 |
| `qwen3-vl-embedding` | 多模态 Embedding | 256~2560（默认 2560） | 32,000 |
| `qwen3-rerank` | 文本重排序 | - | 4,000/条 |
| `qwen3-vl-rerank` | 多模态重排序 | - | 8,000/条 |

### 选型建议

- **纯文本搜索/RAG**：`text-embedding-v4`（速度快、维度灵活）
- **图文混合检索**：`qwen3-vl-embedding`（融合向量 + 独立向量）
- **跨模态搜索**：`tongyi-embedding-vision-plus`（独立向量，文搜图/图搜图）
- **重排序提升精度**：在 Embedding 检索后使用 `qwen3-rerank` 对 Top-N 重排

## 全模态（Omni）

Qwen3.5-Omni 系列同时理解文本、音频、图片和视频，并输出文本和语音。详细信息参见[全模态](../../raw/model-user-guide/model-experience/omni.md)。

### 使用场景

| 场景 | 推荐模型 | 接口 |
|------|---------|------|
| 实时语音/视频对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 音视频内容分析 | `qwen3.5-omni-plus` | HTTP |
| 轻量分析（支持思考模式） | `qwen3-omni-flash` | HTTP |
| 实时语音翻译（60种语言） | `qwen3.5-livetranslate-flash-realtime` | WebSocket |

### 附带能力

- **Function Calling**：Qwen3.5-Omni（WebSocket + HTTP）、Qwen3-Omni-Flash（仅 HTTP）
- **联网搜索**：仅 Qwen3.5-Omni 支持（与 Function Calling 不可同时开启）
- **思考模式**：Qwen3-Omni-Flash HTTP 模式支持（思考模式下不生成语音）
- **声音复刻**：Qwen3.5-Omni Plus/Flash 均支持

## 通用注意事项

- 所有模型通过 DashScope API 接入，主要端点为 `dashscope.aliyuncs.com`
- 旧版模型（Qwen2.x、Wan2.1 等）仍可使用但不再作为首选推荐，新项目建议使用最新系列
- 部分模型有地域限制（如 Tripo 仅限北京、Fun-Music 仅限北京）
- 异步任务（视频生成、3D 生成等）建议轮询间隔 15 秒，或配置回调通知
- 模型的详细定价和限流信息请前往模型广场查看

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)



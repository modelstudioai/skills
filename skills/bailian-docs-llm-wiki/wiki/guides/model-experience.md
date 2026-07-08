# model experience

百炼平台模型体验中心提供覆盖文本、视觉、音频、视频、图片、3D、向量等全模态的模型服务。开发者可通过模型广场快速试用和接入各类模型，支持 OpenAI 兼容 API、WebSocket 实时流式、HTTP 异步任务等多种调用方式。本文按模态分类梳理各场景的推荐模型、核心能力与关键参数，帮助开发者快速选型。

## 文本生成

文本生成是最常用的模型能力，覆盖聊天机器人、内容生成、摘要总结、AI 编程、Agent 开发等场景。详细信息参见[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

### 推荐模型

- `qwen3.7-max`：旗舰推理模型，1M 上下文，最强推理能力，成本较高。
- `qwen3.7-plus`：能力与成本均衡的首选，1M 上下文，完整工具调用和内置工具支持。
- `qwen3.6-flash`：效果接近旗舰、成本更低，1M 上下文，适合确认效果后降本。
- `deepseek-v4-pro` / `deepseek-v4-flash`：第三方模型，1M 上下文，支持思考模式和 Function Calling。

### 核心能力

| 能力 | 说明 |
|------|------|
| 思考模式 | 通过 `enable_thinking` 参数开启，所有 Qwen3 及以上模型均支持 |
| Function Calling | 自定义工具调用，所有通用模型均支持 |
| 内置工具 | 联网搜索、代码解释器、网页抓取等，无需额外配置 |
| 结构化输出 | 获取有效 JSON 返回 |
| 批量推理 | 大量请求且对延迟要求不高时降低成本 |

### 闭源模型迁移参考

| 能力档位 | 闭源代表 | 百炼推荐 |
|----------|----------|----------|
| 高能力 | GPT-5.5、Claude Opus 4.7 | `qwen3.7-max` |
| 平衡 | GPT-5.4、Claude Sonnet 4.6 | `qwen3.7-plus`、`deepseek-v4-pro` |
| 轻量低成本 | GPT-5.4-mini、Claude Haiku 4.5 | `qwen3.6-flash`、`deepseek-v4-flash` |

## 视觉理解

视觉理解模型支持图像分析、视频理解、OCR 等场景。推荐从 `qwen3.7-plus` 开始，它支持 1M 上下文、最长 2 小时视频、每张图片最高 1600 万像素。详细信息参见[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

### 关键参数

- **图像分辨率**：大多数模型支持每张图片最高 1600 万像素，[Token](../concepts/token.md) 计算公式为 `h x w / (32 x 32) + 2`。
- **视频支持**：`qwen3.7-plus`、`qwen3.6-flash` 等支持最长 2 小时 / 2GB 视频输入。
- **OCR**：`qwen3.5-ocr` 专为文档、表格、手写内容优化。

### 推荐模型

| 模型 | 上下文 | 最大视频时长 | Function Calling | 结构化输出 |
|------|--------|-------------|------------------|-----------|
| `qwen3.7-plus` | 1M | 2 小时 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 2 小时 | 支持 | 支持 |
| `qwen3.5-ocr` | -- | -- | -- | -- |

## 视频生成与编辑

视频生成模型支持文生视频、图生视频、参考生视频、视频编辑和角色动画等场景。详细信息参见[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

### 推荐模型

| 场景 | 推荐模型 | 最大分辨率 | 最大时长 |
|------|----------|-----------|----------|
| 文生视频 | `happyhorse-1.1-t2v` | 1080P | 3-15 秒 |
| 首帧生视频 | `happyhorse-1.1-i2v` | 1080P | 3-15 秒 |
| 首尾帧生视频 | `wan2.7-i2v-2026-04-25` | 1080P | 2-15 秒 |
| 参考生视频 | `happyhorse-1.1-r2v` | 1080P | 3-15 秒 |
| 视频编辑 | `happyhorse-1.0-video-edit` | 1080P | 3-15 秒 |
| 动作迁移 | `wan2.2-animate-move` | 720P | 2-30 秒 |

如需传入自定义音频文件，推荐使用 `wan2.7-t2v-2026-06-12`（文生视频）或 `wan2.7-i2v-2026-04-25`（图生视频）。首尾帧模型可串联多个片段实现长视频叙事。

## 图片生成与编辑

图片生成模型支持文生图、图片编辑、文字渲染、角色一致性多图生成等场景。详细信息参见[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

### 推荐模型

| 模型 | 场景 | 文生图 | 编辑 | 最大分辨率 |
|------|------|--------|------|-----------|
| `wan2.7-image-pro` | 文字渲染、品牌色、角色一致性 | 支持 | 支持 | 4096x4096 |
| `z-image-turbo` | 快速生成、低成本、写实人像 | 支持 | 不支持 | 2048x2048 |
| `qwen-image-2.0-pro` | 负向提示词、最多 6 张变体 | 支持 | 支持 | 2048x2048 |

- `z-image-turbo` 生成速度快 10 倍、价格约为 `wan2.7-image-pro` 的 1/5，适合只需生成不需编辑的场景。
- 需要负向提示词时使用 `qwen-image-2.0-pro`。

## 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D 三种模式。详细信息参见[Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

### 模型选型

| 模型 | 最高面数 | 速度 | 适用场景 |
|------|---------|------|----------|
| `Tripo/Tripo-H3.1` | 200 万面 | 较慢 | 影视级渲染、高精度数字资产 |
| `Tripo/Tripo-P1.0` | 2 万面 | 更快 | 快速预览、游戏/AR、实时应用 |

> **注意**：Tripo 3D 模型生成仅适用于华北2（北京）地域，必须使用该地域的 [API Key](../concepts/api-key.md)。

### 使用方式

调用为异步任务模式：先 POST 创建任务获取 `task_id`，再轮询 GET 获取结果。轮询间隔建议 15 秒。输出产物为 GLB 格式的 3D 模型文件，可直接导入 Blender、Unity 等工具。通过 `texture_quality` 参数控制贴图质量（`standard` / `detailed`），`Tripo-H3.1` 还支持 `geometry_quality` 控制几何精度。

## 语音合成

语音合成模型将文本转换为自然语音，支持标准合成、声音复刻和声音设计。详细信息参见[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。

### 推荐模型

| 模型 | 接入方式 | 声音复刻 | 声音设计 | 指令控制 |
|------|---------|---------|---------|---------|
| `cosyvoice-v3.5-plus` | WebSocket / HTTP | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | WebSocket / HTTP | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | HTTP | 支持 | 不支持 | 不支持 |

### 关键决策

- **WebSocket vs HTTP**：WebSocket 支持流式输入输出、延迟最低，适合实时对话；HTTP 适合有声阅读等非实时场景。
- **声音复刻**：已有目标人物录音时使用，合成语音与原始说话人高度相似。
- **声音设计**：无录音素材时使用，通过文字描述创建全新音色。
- **指令控制**：用自然语言动态控制语速、情绪和风格，CosyVoice 系列和 Qwen3-TTS-Instruct 系列支持。

## 语音转语音（S2S）

S2S 模型支持语音对话、语音翻译、同声传译等"语音输入到语音输出"场景。详细信息参见[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

### S2S vs Pipeline

| 维度 | S2S 单模型 | Pipeline（ASR + LLM + TTS） |
|------|-----------|---------------------------|
| 延迟 | 低（单模型流式处理） | 较高（3 阶段串行） |
| 音频理解 | 端到端，能感知语调和情绪 | 先转文本，音频细微信息丢失 |
| 音色定制 | 预设音色 | 支持声音克隆和声音设计 |

### 按场景选模型

| 场景 | 推荐模型 | API |
|------|---------|-----|
| 语音助手/客服对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译/直播翻译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音/播客翻译 | `qwen3-livetranslate-flash` | HTTP |

翻译语言覆盖方面，Qwen3.5-Livetranslate 支持 60 种语言，Qwen3.5-Omni 支持 29 种输出语言，Qwen3-Omni-Flash 支持 11 种。

## 语音识别（ASR）

语音识别模型支持实时语音识别和录音文件转写。详细信息参见[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

### 推荐模型

| 模型 | 模式 | 精度增强 | 情感识别 | 说话人分离 |
|------|------|---------|---------|-----------|
| `fun-asr-realtime` | 实时 | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | 热词 | 不支持 | 支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | Prompt 上下文 | 支持 | 不支持 |
| `qwen3.5-omni-plus` | 非实时 | Prompt 上下文 | 支持 | 不支持 |

### 选型要点

- **热词 vs Prompt 上下文**：热词适合稳定术语表（Fun-ASR），Prompt 上下文无需预配置、模型自适应（Qwen3.5-Omni）。
- **说话人分离**：仅 Fun-ASR 非实时模型支持。
- **情感识别**：Qwen-ASR 和 Qwen3.5-Omni 系列支持。

## 音乐生成

Fun-Music 模型支持通过提示词或自定义歌词生成完整歌曲或纯音乐。详细信息参见[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

| 模型 | 特点 |
|------|------|
| `fun-music-v1` | 支持 `prompt` 和 `lyrics`（至少传一个），支持性别选择 |
| `fun-music-preview` | `prompt` 必选，`lyrics` 可选，不支持性别选择 |

> **注意**：Fun-Music 目前处于邀测阶段，需在模型广场申请开通，且仅在华北2（北京）地域可用。

支持 MP3 和 WAV 两种输出格式，可通过 `is_instrumental=true` 生成纯音乐。

## 向量与重排序

向量和重排序模型支持语义搜索、RAG 检索、跨模态匹配等场景。详细信息参见[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

### 推荐模型

| 模型 | 类型 | 维度 | 最大 [Token](../concepts/token.md) | 场景 |
|------|------|------|-----------|------|
| `text-embedding-v4` | 文本 Embedding | 64~2048 | 8,192 | 文本搜索、RAG、聚类 |
| `qwen3-vl-embedding` | [多模态](../concepts/multimodal.md) Embedding | 256~2560 | 32,000 | 图文混合检索 |
| `qwen3-rerank` | 重排序 | - | 4,000/条 | 文本搜索结果重排序 |
| `qwen3-vl-rerank` | 重排序 | - | 8,000/条 | [多模态](../concepts/multimodal.md)搜索结果重排序 |

维度选择建议：大规模搜索选 256 或 512 维，通用场景选 1024 维（默认），高精度需求选 1536 或 2048 维。

## 全模态

全模态模型能同时理解文本、音频、图片和视频，并输出文本和语音。详细信息参见[全模态](../../raw/model-user-guide/model-experience/omni.md)。

### 三大系列

| 系列 | 定位 | 输入 |
|------|------|------|
| Qwen3.5-Omni | 旗舰，能力最全，支持 Function Calling 和联网搜索 | 文本、音频、图片、视频 |
| Qwen3-Omni-Flash | 轻量低成本，支持思考模式 | 文本、音频、图片、视频 |
| Qwen3.5-Livetranslate | 专业翻译，60 种语言，约 3 秒延迟 | 音频 |

### 按场景选型

| 场景 | 推荐模型 |
|------|---------|
| 实时语音/视频对话 | `qwen3.5-omni-plus-realtime`（WebSocket） |
| 音视频内容分析 | `qwen3.5-omni-plus`（HTTP） |
| 轻量音视频分析 | `qwen3-omni-flash`（HTTP） |
| 实时语音翻译 | `qwen3.5-livetranslate-flash-realtime`（WebSocket） |
| 声音复刻 | `qwen3.5-omni-plus`（HTTP / WebSocket） |

> **注意**：联网搜索与 Function Calling 不可同时开启。Qwen3-Omni-Flash 的思考模式下不支持生成语音。

## 限制和注意事项

- 各模型的上下文窗口、输入限制和计费信息请前往模型广场查看。
- 部分模型和功能存在地域限制（如 Tripo 仅限北京、Fun-Music 仅限北京）。
- 旧版模型（如 Qwen2.5 系列、Wan 2.1 系列等）不再作为首选推荐，新项目建议使用最新版本。
- 第三方模型（DeepSeek、GLM、MiniMax、Kimi 等）的功能支持范围与 Qwen 系列有差异，选型时需对照功能矩阵确认。

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




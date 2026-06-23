# model inference

百炼平台提供覆盖文本、图像、视觉、音视频、3D、音乐、语音及向量/重排序等全模态的模型推理能力，开发者通过 DashScope/[OpenAI 兼容接口](../concepts/openai-compatible.md)调用。本文汇总各模态的选型建议、关键参数与使用方式，更多模型细节可前往模型广场查看。

## 模型能力总览

| 模态 | 推荐起步模型 | 典型场景 |
| --- | --- | --- |
| 文本生成 | `qwen3.7-plus` | 聊天、代码、智能体、文档处理 |
| 视觉理解 | `qwen3.7-plus` | 图像/视频分析、OCR |
| 图片生成与编辑 | `wan2.7-image-pro` | 文生图、图片编辑 |
| 全模态 | `qwen3.5-omni-plus-realtime` | 实时语音/视频对话、内容审核 |
| 语音转语音（S2S） | `qwen3.5-omni-plus-realtime` | 语音助手、同声传译 |
| 音乐生成 | `fun-music-v1` | [prompt](prompt.md) 或歌词生成音乐 |
| 3D 生成 | Tripo 系列 | 文生3D、单图/多图生3D |
| 向量与重排序 | `text-embedding-v4` | 语义搜索、RAG 检索 |

## 文本生成

文本生成模型适用于智能体、聊天机器人、文档处理等场景，推荐从 `qwen3.7-plus` 起步，它能力与成本均衡，拥有 100 万上下文窗口和完整的内置工具支持；如需最强推理能力可选用 `qwen3.7-max`，如需降低成本可改用 `qwen3.6-flash`。详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

从闭源模型迁移时，可按下表对位选型：

| 能力档 | 闭源代表 | 百炼推荐 |
| --- | --- | --- |
| 高能力 | GPT-5.5、Claude Opus 4.7、Gemini 3.1 Pro | `qwen3.7-max` |
| 平衡 | GPT-5.4、Claude Sonnet 4.6、Gemini 3 Pro | `qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.2` |
| 轻量低成本 | GPT-5.4-mini、Claude Haiku 4.5、Gemini 3.1 Flash | `qwen3.6-flash`、`deepseek-v4-flash`、`MiniMax-M2.5` |

### 关键参数与能力

- **上下文窗口**：`qwen3.7-plus` / `qwen3.6-flash` / `deepseek-v4-pro` 等均为 1M（约 70 万汉字）。长文档或大型代码库选 1M；常规任务 128k-256k 足够。
- **思考模式**：通过 `enable_thinking` 参数开启（Responses API 使用 `reasoning.effort` 控制开关与深度），适用于多步数学计算、代码调试、架构规划等场景，所有 Qwen3 及以上模型均支持。
- **Function Calling 与内置工具**：所有通用模型均支持 Function Calling；内置工具（联网搜索、代码解释器、网页抓取等）仅部分模型支持。
- **结构化输出**：返回有效 JSON，例如从文本中提取姓名和地址。
- **批量推理**：大量请求且对延迟要求不高时使用，可降低请求成本，`qwen3.7-plus` / `qwen3.6-flash` 等支持。

## 视觉理解

视觉理解模型覆盖图像分析、视频理解、OCR 等场景。推荐从 `qwen3.7-plus` 起步，支持 1M 上下文、最长 2 小时视频、Function Calling 与内置工具；场景稳定后可尝试 `qwen3.6-flash` 降低成本。详见 [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

- **图像分辨率**：多数模型支持每张图片最高 1600 万像素，Token 数计算公式为 `h × w / (32 × 32) + 2`，更高分辨率会消耗更多 Token。
- **视频支持**：`qwen3.7-plus` / `qwen3.6-plus` / `qwen3.6-flash` / `qwen3.5-plus` / `qwen3.5-flash` 最长 2 小时 / 2GB；`qwen3-vl-plus` / `qwen3-vl-flash` 最长 1 小时 / 2GB。
- **结构化输出**：Qwen3.7、Qwen3.6、Qwen3.5 和 Qwen3-VL 系列在非思考模式下支持，例如从照片中提取商品信息。
- **OCR 与文档提取**：`qwen-vl-ocr` 针对文档、表格、试卷和手写内容优化；通用图片文字提取可用 `qwen3.7-plus` 或 `qwen3.6-flash`。

## 图片生成与编辑

图片生成与编辑推荐 `wan2.7-image-pro`，它在一个模型中集成了文字渲染、品牌色控制、角色一致性多图生成以及图片编辑功能，文生图最高 4096×4096、图片编辑最高 2048×2048。详见 [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

### 按场景选型

- `z-image-turbo`：仅需生成图片（不需要编辑）、速度或成本优先（生成速度快 10 倍、价格约 1/5）、写实人像和产品照片。最大输出 1 张，2048×2048。
- `qwen-image-2.0-pro`：需要负向提示词排除特定元素、需要单次生成最多 6 张变体。支持文生图与编辑，2048×2048。
- `wan2.7-image-pro`：功能最全，文生图最高 4096×4096、编辑最高 2048×2048，单次最多 4 张（连续 12 张）。

> **注意**：Legacy `wanx2.1-imageedit` 仅支持北京地域，不支持文生图。

## 全模态

全模态模型同时理解文本、音频、图片和视频，并输出文本和语音。当前提供三个模型系列：**Qwen3.5-Omni**（旗舰，能力最全）、**Qwen3-Omni-Flash**（轻量、成本低、支持深度推理）、**Qwen3.5-Livetranslate**（专业翻译，开箱即用）。

### 按场景选型

| 场景 | 推荐模型 | API |
| --- | --- | --- |
| 实时语音/视频对话（语音助手、智能客服） | Qwen3.5-Omni Realtime | WebSocket |
| 音视频内容分析（视频审核、会议纪要、字幕） | Qwen3.5-Omni | HTTP |
| 轻量音视频分析（单次输入限 150 秒，支持思考模式，仅输出文本） | Qwen3-Omni-Flash | HTTP |
| 实时语音翻译（约 3 秒延迟，60 种语言） | Qwen3.5-Livetranslate | WebSocket |
| 音视频文件翻译（视频配音、播客翻译） | Qwen3-Livetranslate | HTTP |
| 声音复刻（用参考音色生成语音回复） | Qwen3.5-Omni Plus / Flash | HTTP / WebSocket |

Qwen3.5-Omni 内容分析支持音频最长 3 小时、视频最长 1 小时。支持 Function Calling：Qwen3.5-Omni（WebSocket + HTTP）、Qwen3-Omni-Flash（仅 HTTP）。联网搜索仅 Qwen3.5-Omni 支持，且与 Function Calling 不可同时开启。详见 [全模态](../../raw/model-user-guide/model-inference/omni.md)。

### 翻译语言覆盖

- Qwen3.5-Livetranslate：60 种语言（29 种音频+文本，31 种仅文本）。
- Qwen3-Livetranslate：18 种语言 + 5 种中文方言。
- Qwen3.5-Omni：29 种输出语言 + 7 种中文方言，支持联网搜索与术语注入。
- Qwen3-Omni-Flash：11 种输出语言 + 8 种中文方言，成本更低。

> **注意**：快速搭建翻译应用推荐 Livetranslate；最高质量和最广语言覆盖推荐 Qwen3.5-Omni；成本敏感场景推荐 Qwen3-Omni-Flash。

## 语音转语音（S2S）

“语音输入 → 语音输出”场景有两种构建方式：

| 路线 | 延迟 | 音频理解 | 音色定制 |
| --- | --- | --- | --- |
| S2S（单模型） | 低，单模型流式处理 | 端到端，能感知语调、情绪并做出回应 | 通过系统提示词选择预设音色 |
| Pipeline（ASR + LLM + TTS） | 较高，3 阶段串行 | 先转文本再处理，细微信息可能丢失 | 声音克隆、声音设计（CosyVoice） |

- **使用 S2S**：交互式对话、低延迟和音频感知的回复是关键需求时。
- **使用 Pipeline**：需要自定义音色，或需为每个阶段分别选择最优 ASR、LLM、TTS 时（ASR 见语音识别、LLM 见文本生成、TTS 见语音合成）。

### 实时还是文件模式

- **实时（WebSocket）**：语音助手、呼叫中心、同声传译等，模型名称中包含 `-realtime`。
- **文件模式（HTTP）**：用延迟换更好效果，适用于视频配音、播客翻译、离线内容处理，附带 Function Calling、联网搜索、思考模式、视频上下文等能力。

### S2S 单模型的附带能力

- **Function Calling**：Qwen3.5 Omni（WebSocket 与 HTTP）或 Qwen3 Omni（HTTP），实时模型和 Livetranslate 不支持。
- **联网搜索**：Qwen3.5 Omni（HTTP 和 WebSocket）的 Plus 与 Flash 系列，Qwen3-Omni-Flash 和 Livetranslate 不支持。
- **思考模式**：Qwen3 Omni（HTTP），回答质量优先于延迟，思考模式下不支持生成语音。

详见 [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)。

## 音乐生成

使用 `fun-music-v1` 模型生成音乐，支持两种输入方式：

- **[prompt](prompt.md) 生成**：传入自然语言描述，如“夏日清新民谣，木吉他与口琴伴奏，轻快节奏”。
- **歌词生成**：传入 `lyrics` 参数，模型根据歌词谱曲并演唱。标准歌词结构应包含 `[intro]`（前奏）、`[verse]`（主歌）、`[chorus]`（副歌）等标签。

流式模式（请求头加 `X-DashScope-SSE: enable`）支持边生成边返回音频数据。注意流式与非流式的字符数限制不同：

- 非流式：`lyrics` 中文 5~350 字符 / 英文 5~2000 字符，`prompt` 1~2000 字符。
- 流式：`lyrics` 中文 300~350 字 / 英文 200~250 词，`prompt` 5~1000 个中文汉字或英文单词。

调用端点为 `https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation`，需配置 `DASHSCOPE_API_KEY`。

## 3D 模型生成

通过 Tripo 模型支持三种生成模式：文生3D、单图生3D、多图生3D。调用采用异步任务模式，需先创建任务获取任务 ID，再轮询任务状态获取 3D 文件产物。

> **注意**：Tripo 3D 模型**仅适用于“中国内地（北京）”地域**，且必须使用该地域的 API Key，调用前需在控制台开通 Tripo 模型服务。

详见 [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)。

## 向量与重排序

向量与重排序模型适用于语义搜索、RAG（[检索增强生成](../concepts/rag.md)）检索、跨模态匹配和重排序场景。

### 文本 Embedding

纯文本搜索、RAG 或聚类推荐 `text-embedding-v4`；如需迁移已有的 v3 索引可使用 `text-embedding-v3`（维度兼容）。维度选择建议：

- 大规模搜索且存储空间有限：256 或 512 维。
- 通用场景：1024 维（默认，平衡效果好）。
- 对检索精度要求高：1536 或 2048 维。

### 多模态 Embedding

跨模态检索（文本搜图片、文本搜视频）时，根据需求选择融合向量或独立向量。

详见 [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)。

## 通用使用方式

1. 在控制台开通对应模型服务并获取 API Key。
2. 将 API Key 配置到环境变量（如 `DASHSCOPE_API_KEY`）。
3. 通过 DashScope 接口调用：文本/视觉模型走 [OpenAI 兼容接口](../concepts/openai-compatible.md)；图片、音乐、3D 等走各自专用端点；实时音视频走 WebSocket。
4. 异步任务类接口（如 3D、音乐流式）需创建任务并轮询或接收 SSE 流式数据。

## 限制与注意事项

- 部分模型仅支持特定地域，如 Legacy `wanx2.1-imageedit` 仅北京、Tripo 仅北京。
- 旧版模型（如 Qwen2.5-VL、`qwen-omni-turbo`）不再更新，新项目建议使用 Qwen3.6 / Qwen3.5 系列。
- 思考模式下 S2S 模型不生成语音；联网搜索与 Function Calling 不可同时开启。
- 各模型的具体上下文长度、最大输出、图片/视频数等参数请前往模型广场查看，参数会随快照版本更新。
- 模型名称带日期后缀（如 `qwen3.7-plus-2026-05-26`）为快照版本，行为固定；不带后缀的为 latest 版本，会随平台更新而变化。

## 来源文档

- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)



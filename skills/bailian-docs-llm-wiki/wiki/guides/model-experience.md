# model experience

百炼平台按模态和场景组织了一整套可直接调用的模型能力：文本生成、视觉理解、图片/视频/3D 生成、语音合成与识别、语音转语音、全模态、音乐生成，以及向量与重排序。本页汇总各场景的推荐模型、关键参数和选型要点，帮助开发者快速定位到合适的模型；模型的实时上下文窗口、计费等详细参数请以模型广场为准。

## 文本生成

通用文本场景（聊天机器人、内容生成、摘要、文档处理、办公任务）推荐从 `qwen3.7-plus` 起步——能力与成本均衡，具备 1M 上下文、Function Calling 和内置工具；效果确认后可切到 `qwen3.6-flash` 降本，功能与上下文一致；需要最强推理时用 `qwen3.7-max`。超长文档（多合同审阅、大规模文献）可用 `qwen-long`（10M 上下文）。AI 编程 / Agent 开发推荐 `qwen3.7-plus`（工具调用完整、1M 上下文适合大代码库）。

关键能力：

- **思考模式**：通过 `enable_thinking` 参数开启（Responses API 用 `reasoning.effort` 控制开关与深度），所有 Qwen3 及以上模型均支持，多为混合模式可按请求切换。
- **Function Calling**：所有通用模型均支持自定义工具调用；**内置工具**（联网搜索、代码解释器、网页抓取）免复杂配置。
- **结构化输出**：可强制返回有效 JSON，适合信息抽取。
- **批量推理**：适合大量、低时延要求的请求以降本。

详细的模型对位（从 GPT / Claude / Gemini 迁移）与完整模型清单见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 视觉理解与 OCR

图像 / 视频理解推荐 `qwen3.7-plus`（1M 上下文、最长 2 小时视频、Function Calling + 内置工具），稳定后可降本到 `qwen3.6-flash`。要点见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)：

- **图像分辨率**：多数模型支持每张最高 1600 万像素，Token 数按 `h x w / (32 x 32) + 2` 计算。
- **视频支持**：`qwen3.7-plus` / `qwen3.6-plus` / `qwen3.6-flash` / `qwen3.5-plus` / `qwen3.5-flash` 最长 2 小时 / 2GB；`qwen3-vl-plus` / `qwen3-vl-flash` 最长 1 小时。
- **OCR / 文档提取**：`qwen3.5-ocr` 针对文档、表格、试卷、手写内容优化；通用图片文字提取也可用旗舰模型。

## 图片生成与编辑

见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。推荐 `wan2.7-image-pro`，集成文字渲染、品牌色控制、角色一致性多图生成和图片编辑（文生图最高 4096x4096，编辑最高 2048x2048，支持最多 9 张输入图参考）。仅需生图且追求速度/成本时用 `z-image-turbo`（约快 10 倍、价格约 1/5，写实人像与产品照）；需要负向提示词或单次最多 6 张变体时用 `qwen-image-2.0-pro`（生成和编辑同一模型 ID）。

## 视频生成与编辑

见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)，按子场景选型：

- **文生视频**：`happyhorse-1.1-t2v`（1080P、单片段最长 15 秒、有声）；需传入自定义音频文件用 `wan2.7-t2v-2026-06-12`。
- **图生视频**：首帧生视频用 `happyhorse-1.1-i2v`；首尾帧串联长视频用 `wan2.7-i2v-2026-04-25`。
- **参考生视频**：`happyhorse-1.1-r2v`（保持角色一致性）；需自定义音色或视频参考主体用 `wan2.7-r2v-2026-06-12`。
- **视频编辑 / 角色动画**：编辑用 `happyhorse-1.0-video-edit`，特效/运镜复刻用 `wan2.7-videoedit`；动作迁移用 `wan2.2-animate-move`，人物替换用 `wan2.2-animate-mix`（均支持 wan-std / wan-pro 两种模式）。

## Tripo 3D 模型生成

支持文生 3D、单图生 3D、多图生 3D 三种模式，通过 `input` 中互斥的 `prompt` / `image` / `images` 字段区分。`Tripo/Tripo-H3.1` 面向高精度（最高 200 万面，较慢），`Tripo/Tripo-P1.0` 面向快速预览（最高 2 万面，更快）。贴图质量用 `parameters.texture_quality`（`standard` / `detailed`）控制，几何精度用 `parameters.geometry_quality`（仅 H3.1 支持，`standard` 最高 150 万面 / `ultra` 最高 200 万面）。调用为异步任务，需轮询任务状态（`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`），建议间隔 15 秒。

> **注意**：Tripo 3D 生成仅适用于**华北2（北京）**地域，且必须使用该地域的 API Key。

## 语音合成（TTS）

见 [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。先确定内置音色还是自定义音色：标准合成推荐 `qwen-audio-3.0-tts-plus` / `MiniMax/speech-2.8-hd`；自定义音色分**声音复刻**（提供音频样本，用 `qwen-audio-3.0-tts-flash` / `MiniMax/speech-2.8-hd`）和**声音设计**（用文字描述音色，用 `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash`），音色统一由 `voice-enrollment` 服务注册管理。接入方式上，WebSocket 双向流式延迟最低（实时交互），HTTP 适合有声阅读等；Qwen 系列以 `-realtime` 后缀区分 WebSocket / HTTP。指令控制可用自然语言动态调节语速、情绪和风格。

## 语音识别（ASR）

见 [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)，按维度选型：

- **实时 vs 非实时**：实时（WebSocket）用 `fun-asr-realtime` 或 `qwen3.5-omni-plus-realtime`；非实时文件转写（HTTP）用 `fun-asr` 或 `qwen3.5-omni-plus`。
- **专业术语**：Prompt 上下文注入（Qwen3.5-Omni，无需预配置）或热词表（Fun-ASR，适合稳定术语列表）。
- **说话人分离**：仅 Fun-ASR 非实时模型（`fun-asr`、`fun-asr-mtl`）支持。
- **情感识别**：Qwen-ASR 与 Qwen3.5-Omni 系列支持，推荐 `qwen3-asr-flash-realtime` / `qwen3-asr-flash-filetrans`。

Paraformer 为较早一代模型，新业务建议迁移到 Fun-ASR 或 Qwen-ASR。

## 语音转语音（S2S）与全模态

构建语音应用可选 **S2S 单模型**（延迟低、端到端感知语调情绪）或 **Pipeline（ASR + LLM + TTS）**（可自定义音色、各阶段独立选优）。S2S 路线推荐：语音助手/客服用 `qwen3.5-omni-plus-realtime`，成本敏感用 `qwen3.5-omni-flash-realtime`，同传/直播翻译用 `qwen3.5-livetranslate-flash-realtime`，视频配音/播客翻译用 `qwen3-livetranslate-flash`。全模态（同时理解文本/音频/图片/视频）三大系列为 Qwen3.5-Omni（旗舰）、Qwen3-Omni-Flash（轻量、支持思考模式）、Qwen3.5-Livetranslate（专业翻译，开箱即用，60 种语言）。

> **注意**：Function Calling 与联网搜索能力在不同接入模式下差异较大——例如 `qwen3-omni-flash` 在 HTTP 模式支持 Function Calling 和思考模式，但其 WebSocket（`-realtime`）版本均不支持；联网搜索仅 Qwen3.5-Omni（HTTP / WebSocket）支持，且联网搜索与 Function Calling 不可同时开启；思考模式下不输出语音。选型前务必核对目标模型的具体接入模式。

## 音乐生成

Fun-Music 是端到端音乐生成模型，通过 `prompt` 描述风格/场景/情绪自动作词谱曲，或通过 `lyrics` 提供自定义歌词，用 `gender` 选男女声（仅 `fun-music-v1`），`is_instrumental=true` 生成纯音乐（此时 `lyrics` / `gender` 被忽略），`format` 指定 mp3 / wav 输出。

> **注意**：Fun-Music 处于邀测阶段，需在模型广场申请开通，且服务仅在**华北2（北京）**地域可用。

## 向量与重排序

见 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。纯文本搜索 / RAG / 聚类推荐 `text-embedding-v4`（维度 64~2048，默认 1024，最大 8192 Token；迁移旧索引可用 `text-embedding-v3`）；跨模态检索用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）。重排序用于 Embedding 检索后对 Top-N 结果精排：纯文本用 `qwen3-rerank`（100+ 语言、最多 500 文档），多模态用 `qwen3-vl-rerank`（文本/图片/视频混排）。

## 选型与使用注意事项

- 旧版模型（如旧版 Qwen、Paraformer、`qwen-omni-turbo`、`qwen-tts` 等）不再作为首选，新项目建议使用各系列最新版本。
- 上下文窗口、计费、地域可用性等以模型广场实时信息为准；本页面数据可能滞后。
- 图片/视频/3D/音乐等生成类模型多为异步任务，需按文档轮询或配置回调。

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



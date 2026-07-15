# model experience

百炼平台按模态与任务把模型体验拆分为文本生成、视觉理解、图像/视频/3D 生成、语音合成/识别、语音转语音、音乐生成、向量与重排序以及全模态等多个方向。本页汇总各方向的推荐模型、关键参数、接入方式与常见约束，帮助开发者快速完成选型；具体计费、上下文窗口等实时参数以模型广场为准。

## 文本生成

文本类任务的通用首选是 `qwen3.7-plus`（1M 上下文、Function Calling、内置工具、结构化输出俱全），成本敏感时切换到效果接近的 `qwen3.6-flash`，需要最强推理时用 `qwen3.7-max`；处理超长文档（多合同、大规模文献）时用上下文达 10M 的 `qwen-long`。关键能力开关包括：

- 思考模式：通过 `enable_thinking` 开启（Responses API 用 `reasoning.effort` 控制），Qwen3 及以上多为混合模式，可按请求切换。
- Function Calling：所有通用模型支持；内置工具（联网搜索、代码解释器、网页抓取）免复杂配置。
- 结构化输出与批量推理：分别用于稳定 JSON 返回和高吞吐、低延迟要求不高的场景。

从闭源模型迁移时可按能力档对位选型，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

> **注意**：文档中的模型 ID（如 `qwen3.7-max`、`glm-5.2`、`deepseek-v4-pro`）版本较新，且标注"旧版模型"建议新项目使用 Qwen3.6/Qwen3.5 系列，实际可用模型与版本请以模型广场为准。

## 视觉理解与 OCR

图像/视频理解同样推荐从 `qwen3.7-plus` 起步（1M 上下文、最长 2 小时视频、最大单图 1600 万像素）。要点：

- 图像 Token 估算：`h x w / (32 x 32) + 2`，分辨率越高消耗越大。
- 视频时长：`qwen3.7-plus` / `qwen3.6-plus` / `qwen3.6-flash` / `qwen3.5-plus` / `qwen3.5-flash` 支持最长 2 小时 / 2GB。
- OCR/文档提取用专优的 `qwen3.5-ocr`，通用图片文字提取也可用旗舰模型。

细节参见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 图像与视频、3D 生成

- **文生图 / 图片编辑**：首选 `wan2.7-image-pro`（文字渲染、品牌色、角色一致性、多图编辑；文生图最高 4096x4096，编辑最高 2048x2048）。追求速度与低成本用 `z-image-turbo`；需要负向提示词或最多 6 张变体用 `qwen-image-2.0-pro`。见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。
- **视频生成 / 编辑**：文生视频与首帧生视频推荐 `happyhorse-1.1-t2v` / `happyhorse-1.1-i2v`（1080P、3-15 秒、有声）；需要自定义音频或首尾帧串联长视频用 `wan2.7-*` 系列；角色动画用 `wan2.2-animate-move` / `wan2.2-animate-mix`（pro/std 两档）。
- **3D 生成**：通过 Tripo 模型支持文生/单图/多图三种模式，`prompt`、`image`、`images` 三字段互斥；快速预览用 `Tripo/Tripo-P1.0`，高精度用 `Tripo/Tripo-H3.1`（几何精度 `geometry_quality` 最高 200 万面）。

> **注意**：Tripo 3D 生成为异步任务，仅在"中国内地（北京）"地域可用，需使用该地域 API Key；产物 `pbr_model_url` / `rendered_image_url` 有效期仅 2 小时，务必及时下载。轮询建议间隔 15 秒。

## 语音合成、识别与语音对话

语音方向需先确定接入协议与音色来源：

- **接入方式**：WebSocket 双向流式、延迟最低，适合实时交互；HTTP 发送完整文本、支持流式返回，适合离线内容制作。Qwen-Audio-TTS/CosyVoice 用同一模型名同时支持两种协议，Qwen 系列用 `-realtime` 后缀区分。
- **语音合成**：标准合成用 `qwen-audio-3.0-tts-plus` / `MiniMax/speech-2.8-hd`；自定义音色分声音复刻（提供音频样本）与声音设计（文字描述音色），声音设计推荐 `cosyvoice-v3.5-plus`，音色注册统一用 `voice-enrollment`。指令控制可用自然语言动态调节语速、情绪、风格。
- **语音识别**：从实时/非实时、专业术语、说话人分离、情感识别四个维度选型。实时用 `fun-asr-realtime` 或 `qwen3.5-omni-plus-realtime`，非实时用 `fun-asr`（支持说话人分离）；情感识别用 Qwen-ASR 系列。详见 [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。
- **语音转语音**：S2S 单模型（Omni / Livetranslate）延迟低、端到端感知语调情绪；Pipeline（ASR+LLM+TTS）更灵活、可自定义音色。实时对话用 `qwen3.5-omni-plus-realtime`，同传翻译用 `qwen3.5-livetranslate-flash-realtime`。
- **音乐生成**：Fun-Music 通过 `prompt` 或 `lyrics` 生成完整歌曲，`is_instrumental=true` 生成纯音乐，`gender` 选男女声（仅 `fun-music-v1`）。

> **注意**：Fun-Music 处于邀测阶段，需在模型广场申请开通，且仅华北2（北京）地域可用；其请求端点为业务空间维度（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`），需替换 `{WorkspaceId}`。

## 向量与重排序

RAG / 语义搜索场景：纯文本 Embedding 首选 `text-embedding-v4`（维度 64~2048，默认 1024，最大 8192 Token），迁移旧索引可用 `text-embedding-v3`；跨模态检索用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）。重排序用 `qwen3-rerank`（纯文本、100+ 语言、最多 500 文档）或 `qwen3-vl-rerank`（多模态）。维度选择建议：存储受限选 256/512，通用选 1024，高精度选 1536/2048。

## 全模态

需要同时理解文本、音频、图片、视频并输出文本/语音时，用全模态模型：旗舰 `qwen3.5-omni-plus`（能力最全，支持联网搜索、Function Calling、音频最长 3 小时/视频最长 1 小时）、轻量 `qwen3-omni-flash`（成本低、支持思考模式但思考模式下不输出语音）、专业翻译 `qwen3.5-livetranslate-flash`（60 种语言、约 3 秒延迟、开箱即用）。

> **注意**：不同文档对同一模型的能力标注存在差异——例如 `qwen3-omni-flash-realtime`（WebSocket）在多数表格中不支持 Function Calling/联网搜索，而 HTTP 版 `qwen3-omni-flash` 支持 Function Calling 与思考模式；联网搜索与 Function Calling 不可同时开启。以对应模型的用户指南和 API 文档为最终依据。

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



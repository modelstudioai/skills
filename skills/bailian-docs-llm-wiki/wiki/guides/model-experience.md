# model experience

本页是百炼平台各模态模型选型的总览，覆盖文本生成、视觉理解、图片/视频生成与编辑、3D 生成、语音合成/识别/转语音、音乐生成、向量与重排序、全模态共 11 类能力。面向开发者提供"按场景选模型"的决策路径、关键参数与限制，并给出从 GPT/Claude/Gemini/Sora/ElevenLabs 等闭源服务迁移到百炼的对位建议。

## 能力总览与首选模型

| 能力方向 | 首选模型 | 备选/低成本 |
| --- | --- | --- |
| 文本生成 / Agent 开发 | `qwen3.7-plus` | `qwen3.7-flash`、`qwen3.7-max`（最强推理） |
| 视觉理解（图像/视频/OCR） | `qwen3.7-plus` | `qwen3.7-flash`、`qwen3.5-ocr`（文档提取） |
| 视频生成与编辑 | `happyhorse-1.1-t2v` / `happyhorse-1.1-i2v` | `wan2.7-*` 系列（自定义音频、首尾帧） |
| 图片生成与编辑 | `wan2.7-image-pro` | `z-image-turbo`（快 10 倍、约 1/5 价格）、`qwen-image-2.0-pro` |
| 3D 生成 | `Tripo/Tripo-P1.0`（快速验证） | `Tripo/Tripo-H3.1`（高精度，最高 200 万面） |
| 语音合成（TTS） | `qwen-audio-3.0-tts-plus` | `cosyvoice-v3.5-plus`（声音设计）、`MiniMax/speech-2.8-hd` |
| 语音转语音（S2S） | `qwen-audio-3.0-realtime-plus` | `qwen-audio-3.0-realtime-flash`、`qwen3.5-livetranslate-flash-realtime`（同传） |
| 语音识别（ASR） | `fun-asr-realtime` / `fun-asr` | `qwen3.5-omni-plus`（Prompt 上下文、多语种） |
| 音乐生成 | `fun-music-v1` | `fun-music-preview` |
| 向量与重排序 | `text-embedding-v4`、`qwen3-rerank` | `qwen3-vl-embedding`（[多模态](../concepts/multimodal.md)）、`gte-rerank-v2` |
| 全模态 | `qwen3.5-omni-plus` | `qwen3-omni-flash`（低成本、支持思考模式） |

## 文本生成

详见[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

- **通用场景**（聊天机器人、内容生成、办公文档处理）：`qwen3.7-plus`，能力与成本均衡，1M 上下文（约 70 万汉字），支持思考模式、Function Calling、内置工具和结构化输出。效果确认后可换 `qwen3.7-flash` 降低成本。
- **AI 编程 / Agent 开发**：推荐 `qwen3.7-plus`；最强推理选 `qwen3.8-max-preview`（仅 Token Plan 可用）或 `qwen3.7-max`。
- **超长文档**：`qwen-long`，上下文达 10M Token，但不支持思考模式和 Function Calling。
- **关键参数**：`enable_thinking` 开启思考模式（Responses API 用 `reasoning.effort`），所有 Qwen3 及以上模型支持；结构化输出可获得有效 JSON；批量推理可降低大量低时效请求的成本。
- 三方模型（`deepseek-v4-pro`、`glm-5.2`、`MiniMax-M3`、`kimi-k2.7-code` 等）均支持 Function Calling，但普遍不支持内置工具。

> **注意**：`qwen3.7-max` 在文本生成文档的推荐模型表中标注"结构化输出不支持"，选型时如需 JSON 输出请优先使用 `qwen3.7-plus` / `qwen3.7-flash`。

## 视觉理解

详见[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

- 首选 `qwen3.7-plus`：1M 上下文、单图最高 1600 万像素、视频最长 2 小时 / 2GB、最多 2048 张图片。
- Token 消耗：每张图片约 `h x w / (32 x 32) + 2` 个 Token。
- OCR 与文档提取：`qwen3.5-ocr`（文档、表格、试卷、手写内容专用）。
- 内置工具（联网搜索、代码执行）仅限 `qwen3.7-max-2026-06-08`、`qwen3.7/3.6/3.5` 的 plus 与 flash 版本；结构化输出仅在**非思考模式**下支持。

## 图片与视频生成

- **文生图/图片编辑**：`wan2.7-image-pro` 集成文字渲染、品牌色控制、角色一致性多图生成与编辑，文生图最高 4096x4096、编辑最高 2048x2048。仅需生成且追求速度/成本选 `z-image-turbo`；需要负向提示词或单次最多 6 张变体选 Qwen Image 系列（`qwen-image-3.0-pro` 邀测中）。
- **文生视频**：`happyhorse-1.1-t2v`（有声、1080P、3-15 秒）；需传入自定义音频用 `wan2.7-t2v-2026-06-12`。
- **图生视频**：首帧用 `happyhorse-1.1-i2v`；首尾帧串联长视频用 `wan2.7-i2v-2026-04-25`。
- **参考生视频**：`happyhorse-1.1-r2v`；需视频参考主体或自定义音色用 `wan2.7-r2v-2026-06-12`。
- **视频编辑与角色动画**：`happyhorse-1.0-video-edit` / `wan2.7-videoedit`（特效/运镜复刻）；动作迁移 `wan2.2-animate-move`，人物替换 `wan2.2-animate-mix`（均有 wan-std / wan-pro 两种模式）。

## 3D 与音乐生成（仅北京地域）

- **Tripo 3D**：文生/单图生/多图生 3D，异步任务接口（创建任务 → 轮询 `task_id`，建议间隔 15 秒，24 小时有效）。`input` 中 `prompt` / `image` / `images` 三字段互斥。贴图质量用 `texture_quality`（standard/detailed）控制；几何精度 `geometry_quality`（ultra 最高 200 万面）仅 `Tripo/Tripo-H3.1` 支持。详见 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **Fun-Music**：`prompt`（描述风格）或 `lyrics`（自定义歌词）二选一或组合，`is_instrumental=true` 生成纯音乐（此时 lyrics/gender 被忽略），`gender` 仅 `fun-music-v1` 支持，输出 MP3/WAV。**邀测中**，需在模型广场申请开通。

> **注意**：Tripo 与 Fun-Music 均仅在华北2（北京）地域可用，且必须使用该地域的 API Key。

## 语音能力

### 语音合成（TTS）

先决定内置音色（标准合成，`qwen-audio-3.0-tts-plus`、`MiniMax/speech-2.8-hd`）还是自定义音色；自定义再分**声音复刻**（有音频样本，`qwen-audio-3.0-tts-plus/flash`）与**声音设计**（文字描述音色，`cosyvoice-v3.5-plus/flash`），音色统一通过 `voice-enrollment` 服务管理。实时交互用 WebSocket（流式输入输出、延迟最低），内容制作用 HTTP。Qwen-Audio-TTS / CosyVoice / Qwen3-TTS-Instruct 系列支持指令控制（自然语言控制语速、情绪、风格）。

### 语音识别（ASR）

按四个维度选型：实时（`fun-asr-realtime`）还是非实时（`fun-asr`，最长 12 小时 / 2GB）；专业术语用热词（Fun-ASR）还是 Prompt 上下文注入（`qwen3.5-omni-plus`）；说话人分离仅 Fun-ASR 非实时模型（`fun-asr`、`fun-asr-mtl`）支持；情感识别用 Qwen-ASR（`qwen3-asr-flash-realtime` / `qwen3-asr-flash-filetrans`）。Paraformer 为较早一代模型，建议迁移。

### 语音转语音（S2S）

两条路线：**S2S 单模型**（低延迟、端到端感知语调情绪）与 **Pipeline（ASR + LLM + TTS）**（可自定义音色、逐组件选优）。S2S 路线中：对话选 `qwen-audio-3.0-realtime-plus`（支持语义 VAD 与 Function Calling），同传选 `qwen3.5-livetranslate-flash-realtime`（60 种语言），文件翻译选 `qwen3-livetranslate-flash`。文件（HTTP）模式支持 Function Calling、联网搜索、思考模式等附带能力；实时（WebSocket）模式下 Omni 系列不支持 Function Calling，思考模式下不生成语音。详见[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

## 向量与重排序

- **文本 Embedding**：`text-embedding-v4`，维度 64~2048（默认 1024）；大规模检索省存储选 256/512，高精度选 1536/2048；已有 v3 索引可继续用 `text-embedding-v3`。
- **[多模态](../concepts/multimodal.md) Embedding**：图文混合检索（融合向量）用 `qwen3-vl-embedding`；跨模态搜索（独立向量）用 `tongyi-embedding-vision-plus`。纯文本数据仍建议 `text-embedding-v4`。
- **重排序**：RAG 的 Top-N 精排用 `qwen3-rerank`（100+ 语言，最多 500 文档）；[多模态](../concepts/multimodal.md)排序用 `qwen3-vl-rerank`。

## 全模态

`qwen3.5-omni-plus`（旗舰）可同时理解文本、音频、图片、视频并输出文本和语音：音频最长 3 小时、视频最长 1 小时，支持 Function Calling、联网搜索（二者不可同时开启）、声音复刻。`qwen3-omni-flash` 成本更低、支持思考模式（仅 HTTP、仅文本输出、单次输入限 150 秒）。翻译场景：快速搭建选 Qwen3.5-Livetranslate（60 种语言、约 3 秒延迟），最高质量选 Qwen3.5-Omni（29 种输出语言），成本敏感选 Qwen3-Omni-Flash（11 种输出语言）。

> **注意**：关于粤语翻译，[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)文档标注 Qwen3.5-Livetranslate 对粤语为"仅文本"，而全模态文档同一表格写作"支持 仅文本"，实际应以"仅输出文本、不输出语音"理解。

## 通用限制与注意事项

- 模型的上下文、计费等详细参数以模型广场（北京/新加坡/美国/法兰克福各地域）实时数据为准。
- 快照版本（如 `qwen3.7-plus-2026-05-26`）适合版本回归和稳定性需求；主模型 ID 会随升级更新行为。
- 各文档中的"旧版模型"（Qwen3、Qwen2.5-Omni、Wan2.1、Paraformer、按 [Token 计费](../concepts/token-billing.md)的旧版 Qwen-TTS 等）不再作为首选推荐，新项目应使用文中的推荐系列。
- `qwen3.8-max-preview` 等部分模型仅对 Token Plan 用户开放。

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



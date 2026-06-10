# model inference

百炼平台提供覆盖文本、图像、音频、视频、3D 等多种模态的推理模型，统一通过 DashScope API 调用。本文按模态汇总各场景的推荐模型、关键参数与限制，帮助开发者快速选型。

## 选型总览

| 场景 | 推荐入口 |
| --- | --- |
| 文本对话 / Agent / 代码 | `qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash` |
| 图像 / 视频理解、OCR | `qwen3.7-plus`、`qwen3.6-flash`、`qwen-vl-ocr` |
| 文生图 / 图片编辑 | `wan2.7-image-pro`、`qwen-image-2.0-pro` |
| 文 / 图生视频、视频编辑 | `happyhorse-1.0-t2v`、`wan2.7-i2v-2026-04-25` |
| 文 / 图生 3D 模型 | `Tripo/Tripo-P1.0`、`Tripo/Tripo-H3.1` |
| 语音合成（TTS） / 声音复刻 | `cosyvoice-v3.5-plus`、`MiniMax/speech-2.8-hd` |
| 语音识别（ASR） | `fun-asr-realtime`、`fun-asr`、`qwen3-asr-flash-realtime` |
| 语音转语音（S2S）/ 翻译 | `qwen3.5-omni-plus-realtime`、`qwen3.5-livetranslate-flash-realtime` |
| 全模态（音频 + 视频 + 文本） | `qwen3.5-omni-plus`、`qwen3-omni-flash` |
| 音乐生成 | `fun-music-v1` |
| 向量 Embedding / Rerank | `text-embedding-v4`、`qwen3-rerank` |

## 文本生成

聊天机器人、Agent、文档处理、代码生成等场景。推荐从 `qwen3.7-plus`（1M 上下文，内置工具、Function Calling、结构化输出、批量推理全支持）起步，确认效果后降级到 `qwen3.6-flash` 降本；最强推理用 `qwen3.7-max`（不支持结构化输出 / 批量调用）。

- **思考模式**：所有 Qwen3 及以上模型均支持，通过 `enable_thinking` 或 Responses API 的 `reasoning.effort` 控制。
- **Function Calling**：所有通用模型均支持；**内置工具**（联网搜索、代码解释器）仅部分模型支持（`qwen3.7-plus` / `qwen3.6-plus` / `qwen3.6-flash` 等）。
- **上下文窗口**：100 万 Token ≈ 70 万汉字 / 10 本小说。
- **第三方模型**：`deepseek-v4-pro/flash`、`glm-5.1`、`kimi-k2.6`、`MiniMax-M2.5`、`mimo-v2.5-pro` 等可选。
- **专用模型**：翻译 `qwen-mt-*`、超长上下文 `qwen-long`（10M）、代码 `qwen3-coder-*`。

详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

## 视觉理解

图像分析、视频理解、OCR、结构化输出等。推荐 `qwen3.7-plus`（1M 上下文、最长 2 小时视频、2048 张图、64 视频、Function Calling + 内置工具 + 结构化输出全支持）。降本选 `qwen3.6-flash`。

- **图像分辨率**：大多数模型支持每图最高 1600 万像素；Token 计算 `h × w / (32 × 32) + 2`。
- **视频支持**：最长 2 小时 / 2GB（`qwen3.7-plus`、`qwen3.6-*`、`qwen3.5-*`）；最长 1 小时（`qwen3-vl-*`、`qwen3.5-omni-*`）。
- **OCR 专用**：`qwen-vl-ocr` 针对文档、表格、试卷、手写。
- **结构化输出**：Qwen3.7 / 3.6 / 3.5 / 3-VL 系列在非思考模式下支持。

详见 [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

## 图片生成与编辑

- **文生图推荐**：`wan2.7-image-pro`（最高 4096×4096，支持文字渲染、品牌色、角色一致性多图、编辑）；快速低成本选 `z-image-turbo`（快 10 倍、价格 1/5，但不支持编辑）。
- **需要负向提示词 / 6 张变体**：`qwen-image-2.0-pro`（最多 6 张变体，2048×2048）。
- **图片编辑**：`wan2.7-image-pro`（最多 9 张参考图、边界框交互、角色一致性多图）。
- **版本策略**：Wan 系列按 2.7 → 2.6 → 2.5 → 2.2 → 2.1 迭代；Qwen-Image 按 2.0-pro / 2.0 / max / plus 分级。

详见 [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

## 视频生成与编辑

所有模型支持 720P / 1080P 输出，单片段最长 15 秒（动画类最长 30 秒）。

| 场景 | 推荐模型 |
| --- | --- |
| 文生视频（默认） | `happyhorse-1.0-t2v`（有声，3–15 秒） |
| 文生视频（自定义音频） | `wan2.7-t2v-2026-04-25` |
| 首帧生视频 | `happyhorse-1.0-i2v` / `wan2.7-i2v-2026-04-25` |
| 首尾帧拼接长视频 | `wan2.7-i2v-2026-04-25` |
| 参考图 / 角色一致性 | `happyhorse-1.0-r2v` / `wan2.7-r2v` |
| 视频编辑 | `happyhorse-1.0-video-edit` / `wan2.7-videoedit`（特效 / 运镜复刻） |
| 动作迁移到静态人物 | `wan2.2-animate-move`（wan-pro / wan-std 两档） |
| 视频中替换人物 | `wan2.2-animate-mix` |

> **注意**：HappyHorse 1.0 与 Wan 2.7 系列在国内外部署模式均可用；Wan 2.6 的 `-us` 后缀模型仅适用于美国部署模式。

## 3D 模型生成（Tripo）

通过 `Tripo/Tripo-P1.0`（2 万面，快速预览 / 游戏 / AR）或 `Tripo/Tripo-H3.1`（200 万面，影视级）生成 3D 资产。

- **三种输入模式**（`prompt` / `image` / `images` 互斥）：
  - 文生 3D：`{"prompt": "..."}`
  - 单图生 3D：`{"image": "<url>"}`，JPEG/PNG，20~6000 px，≤ 20MB
  - 多图生 3D（2~4 张多角度）：`{"images": [...]}`，还原度更高
- **贴图质量**：`parameters.texture_quality = "standard" | "detailed"`；设 `texture: false, pbr: false` 返回无贴图基础模型。
- **几何精度**：仅 `Tripo-H3.1` 支持 `geometry_quality = "standard" | "ultra"`（最高 200 万面）。
- **调用方式**：[异步任务](../concepts/async-task.md)，先创建任务拿 `task_id`，再轮询（建议 15 秒间隔）或回调；`task_id` 查询有效期 24 小时。
- **地域限制**：仅中国内地（北京）地域可用。

## 语音合成（TTS）

- **标准 TTS**（内置音色）：`cosyvoice-v3-plus`、`MiniMax/speech-2.8-hd`。
- **声音复刻**（用音频样本还原音色）：`cosyvoice-v3.5-plus`、`MiniMax/speech-2.8-hd`。
- **声音设计**（用文字描述从零创建音色）：`cosyvoice-v3.5-plus / flash`。
- **指令控制**（自然语言描述语速 / 情绪 / 风格）：`cosyvoice-v3.5-plus / flash`、`cosyvoice-v3-flash`、`qwen3-tts-instruct-flash*`。
- **接入方式**：CosyVoice 与 Qwen3-TTS 的 `-realtime` 后缀为 WebSocket，其它为 HTTP；Qwen3-TTS 还有专用的 `-vc`（复刻）和 `-vd`（设计）系列。
- **语言覆盖**：CosyVoice v3.5 声音复刻支持 21+ 语言 + 17 种中文方言；Qwen3-TTS 系统音色覆盖中 / 英 / 日 / 韩 / 法 / 德 / 俄等 10+ 语言。

> **注意**：旧版 `qwen-tts*` 按 Token 计费，新业务建议优先用 Qwen3-TTS 或 CosyVoice v3.5。

详见 [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)。

## 语音识别（ASR）

从 4 个维度选型：实时 / 非实时、专业术语、说话人分离、情感识别。

| 需求 | 推荐模型 |
| --- | --- |
| 实时 + 热词 + 方言 | `fun-asr-realtime`（WebSocket，无时长限制） |
| 非实时 + 热词 + 说话人分离 | `fun-asr`（HTTP，12 小时 / 2GB） |
| 实时 + Prompt 上下文 + 情感识别 | `qwen3.5-omni-plus-realtime`（2 小时） |
| 非实时 + Prompt + 情感识别 | `qwen3.5-omni-plus`（3 小时 / 2GB） |
| 实时 + 情感识别（专用 ASR） | `qwen3-asr-flash-realtime` |
| 非实时 + 情感识别（文件转写） | `qwen3-asr-flash-filetrans` |

- **专业术语处理**：① Prompt 上下文注入（Qwen3.5-Omni，无需预配置，每次请求延迟更高）；② 热词（Fun-ASR，适合稳定术语表）。
- **说话人分离**：仅 `fun-asr` / `fun-asr-mtl` 支持。
- **8kHz 电话场景**：`fun-asr-flash-8k-realtime`、`paraformer-realtime-8k-v2/v1`。
- **多语种**：Fun-ASR 主版本覆盖 40+ 语言；Qwen-ASR 覆盖 29 语言。

## 语音转语音（S2S）

构建「语音输入 → 语音输出」应用的两条路线：

- **S2S 单模型**：低延迟，端到端感知语调情绪，通过系统提示词选预设音色。
- **Pipeline（ASR + LLM + TTS）**：更高延迟，但可分别选最优组件，支持声音克隆 / 设计。

| 场景 | 推荐模型 | API |
| --- | --- | --- |
| 语音助手 / 客服对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译 / 直播翻译 | `qwen3.5-livetranslate-flash-realtime`（60 语言） | WebSocket |
| 视频配音 / 播客翻译 | `qwen3-livetranslate-flash`（18 语言） | HTTP |
| 视频分析 + 思考模式 | `qwen3-omni-flash` | HTTP |

- **翻译语言覆盖**：Qwen3.5-Livetranslate（60 语言，29 种语音 + 文本输出）> Qwen3.5-Omni（29 语言）> Qwen3-Omni-Flash（11 语言）。
- **附带能力**（仅 S2S 单模型路线）：Function Calling / 联网搜索（Qwen3.5-Omni）；思考模式（仅 `qwen3-omni-flash` HTTP，且不支持同时生成语音）。

## 全模态

同时理解文本 / 音频 / 图片 / 视频，输出文本和语音。

| 场景 | 推荐模型 |
| --- | --- |
| 实时语音 / 视频对话 | `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime` |
| 音视频内容分析（≤ 3h 音频 / 1h 视频） | `qwen3.5-omni-plus` / `qwen3.5-omni-flash` |
| 轻量分析 + 深度推理（思考模式） | `qwen3-omni-flash`（仅 HTTP） |
| 实时翻译（60 语言） | `qwen3.5-livetranslate-flash-realtime` |
| 音视频文件翻译 | `qwen3-livetranslate-flash` |

- **Function Calling**：Qwen3.5-Omni（WebSocket + HTTP）、Qwen3-Omni-Flash（仅 HTTP）。
- **联网搜索**：仅 Qwen3.5-Omni（与 Function Calling 互斥）。
- **旧版模型**（`qwen-omni-turbo` 等）仅中 / 英文，新业务建议迁移到 Qwen3.5-Omni。

## 音乐生成

`fun-music-v1` / `fun-music-preview` 支持根据提示词自动作词作曲，或传入自定义歌词谱曲，输出男 / 女声演唱的中文或英文歌曲（MP3 / WAV）。

- `prompt`：描述风格场景，模型自动创作歌词。
- `lyrics`：自定义歌词（非流式：中 5–350 / 英 5–2000 字符；流式：中 300–350 字 / 英 200–250 词）。
- 同时传入 `lyrics` 和 `prompt` 时仅 `lyrics` 生效。
- [流式输出](../concepts/streaming-output.md)需带 `X-DashScope-SSE: enable` 请求头。
- **地域限制**：目前仅中国内地（北京）地域可用，需申请开通。

## 向量与重排序（Embedding / Rerank）

用于语义搜索、RAG 检索、跨模态匹配。

- **文本 Embedding**：`text-embedding-v4`（默认 1024 维，可 64–2048；最大 8192 Token）；`text-embedding-v3` 仅用于已有 v3 索引迁移（维度 512 / 1024 兼容）。
- **多模态 Embedding**：
  - 融合向量（图文混合检索）：`qwen3-vl-embedding`（256–2560 维）、`qwen2.5-vl-embedding`（512–1024 维）。
  - 独立向量（跨模态搜索，文搜图 / 图搜图）：`tongyi-embedding-vision-plus/flash`（64–1152 / 768 维）。
- **Rerank**：
  - 纯文本：`qwen3-rerank`（100+ 语言，4000 Token / 条）。
  - 多模态：`qwen3-vl-rerank`（文本 + 图 + 视频混合，8000 Token / 条）。
  - 旧版：`gte-rerank-v2`（4000 Token / 条）。

## 通用注意事项

- **API Key**：所有模型调用需通过 `DASHSCOPE_API_KEY` 环境变量配置；Tripo / 音乐生成 仅中国内地（北京）地域可用。
- **接入协议**：实时流式一般用 WebSocket（模型名含 `-realtime`），非实时文件处理用 HTTP；CosyVoice / Qwen-TTS 同名模型同时支持两种协议。
- **[异步任务](../concepts/async-task.md)**：3D 生成、部分视频生成使用[异步任务](../concepts/async-task.md)接口，需轮询 `task_id` 或配置回调。
- **版本策略**：带日期后缀（如 `-2026-04-25`）为快照版本，适合版本锁定；不带后缀为主版本，会持续迭代。
- **迁移提示**：旧版 Qwen2.5 / Qwen3 / Qwen3-VL / Paraformer / Qwen-Omni-Turbo / Qwen-TTS 仍可用，但新业务建议优先使用 Qwen3.5 / Qwen3.6 / Qwen3.7 系列以获得更完整的功能支持与更优性价比。

## 来源文档

- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)



# model experience

百炼平台提供覆盖文本、视觉、视频、图像、3D、语音合成、语音识别、语音转语音、音乐、向量/重排序及全模态理解等十余类大模型能力。本文按模态梳理各场景下的推荐模型、关键参数与使用方式，供开发者在选型与接入时快速定位。

## 模型能力总览

| 模态 | 推荐入口模型 | 主要接入方式 |
| --- | --- | --- |
| 文本生成 | `qwen3.7-plus` / `qwen3.7-max` / `qwen3.6-flash` | OpenAI 兼容 / Responses API |
| 视觉理解 | `qwen3.7-plus` / `qwen3.6-flash` / `qwen-vl-ocr` | [多模态](../concepts/multimodal.md)消息接口 |
| 视频生成与编辑 | `happyhorse-1.1-t2v` / `wan2.7-i2v-2026-04-25` | 异步任务（DashScope） |
| 图片生成与编辑 | `wan2.7-image-pro` / `z-image-turbo` / `qwen-image-2.0-pro` | 异步任务 |
| 3D 模型生成 | `Tripo/Tripo-P1.0` / `Tripo/Tripo-H3.1` | 异步任务（仅北京地域） |
| 语音合成（TTS） | `cosyvoice-v3.5-plus` / `qwen3-tts-instruct-flash` | WebSocket / HTTP |
| 语音转语音（S2S） | `qwen3.5-omni-plus-realtime` / `qwen3.5-livetranslate-flash-realtime` | WebSocket / HTTP |
| 语音识别（ASR） | `fun-asr-realtime` / `qwen3.5-omni-plus-realtime` | WebSocket / HTTP |
| 音乐生成 | `fun-music-v1` | HTTP（邀测，仅北京） |
| 向量与重排序 | `text-embedding-v4` / `qwen3-rerank` / `qwen3-vl-embedding` | HTTP |
| 全模态 | `qwen3.5-omni-plus` / `qwen3.5-livetranslate-flash-realtime` | WebSocket / HTTP |

## 文本生成

适用于 AI 智能体、聊天机器人、内容生成、文档处理等场景。推荐 `qwen3.7-plus`——能力与成本均衡，1M 上下文、完整工具调用与内置工具；效果稳定后可用 `qwen3.6-flash` 降本；需要最强推理选 `qwen3.7-max`。详细模型矩阵与历史快照见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

关键能力与参数：

- **思考模式**：通过 `enable_thinking` 开启（Responses API 用 `reasoning.effort` 控制深度）。Qwen3 及以上支持，多数为混合模式，可按请求切换。
- **Function Calling 与内置工具**：自定义工具全系列通用模型支持；内置工具（联网搜索、代码解释器、网页抓取）仅部分模型支持，例如 `qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`mimo-v2.5-pro`。
- **结构化输出**：非思考模式下返回合法 JSON，用于字段抽取。
- **批量推理**：低延迟要求的批量场景可降本。

从闭源模型迁移可按能力档对位：高能力档对应 `qwen3.7-max`，平衡档对应 `qwen3.7-plus` / `deepseek-v4-pro` / `glm-5.2`，轻量低成本档对应 `qwen3.6-flash` / `deepseek-v4-flash` / `MiniMax-M2.5`。

> **注意**：第三方模型（如 `deepseek-v4-pro`、`kimi-k2.7-code`、`MiniMax-M2.5`、`mimo-v2.5-pro`）不支持内置工具与结构化输出，迁移时需评估能力差异。

## 视觉理解

适用于图像分析、视频理解、OCR 等场景。推荐从 `qwen3.7-plus` 入手，支持 1M 上下文、最长 2 小时视频、Function Calling 与内置工具；降本用 `qwen3.6-flash`。`qwen-vl-ocr` 专为文档/表格/试卷/手写文字提取优化。详见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

关键限制：

- 单张图片最高 1600 万像素；[Token](../concepts/token.md) 计算公式 `h × w / (32 × 32) + 2`，分辨率越高消耗越大。
- 视频时长上限因模型而异：`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash` 支持 2 小时 / 2GB；`qwen3-vl-plus`、`qwen3-vl-flash` 与 `qwen3.5-omni-plus` 系列为 1 小时 / 2GB。
- 结构化输出仅在非思考模式下支持。
- 内置工具仅限 `qwen3.7-max-2026-06-08`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash`。

## 视频生成与编辑

异步任务模式，支持文生视频、图生视频、参考生视频、视频编辑、角色动画等。推荐入口见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

- **文生视频**：`happyhorse-1.1-t2v`（有声、1080P、3–15 秒）。需自定义音频文件用 `wan2.7-t2v-2026-04-25`。
- **图生视频**：首帧用 `happyhorse-1.1-i2v`；首尾帧、视频续写用 `wan2.7-i2v-2026-04-25`（可将上一片段末帧作为下一片段首帧串联长视频）。
- **参考生视频**：`happyhorse-1.1-r2v` 保持角色一致性；需音频定义音色或视频参考主体用 `wan2.7-r2v`。
- **视频编辑**：风格/元素替换用 `happyhorse-1.0-video-edit`；特效/运镜复刻用 `wan2.7-videoedit`。
- **角色动画**：动作迁移用 `wan2.2-animate-move`（pro 接近实拍、std 更快更省）；视频中替换人物用 `wan2.2-animate-mix`。两者均支持 wan-pro / wan-std 两种模式。

输出规格：HappyHorse 系列为 720P/1080P、3–15 秒、24fps、MP4；Wan 2.7 系列为 720P/1080P、2–15 秒（编辑/参考 2–10 秒）、30fps、MP4。Wan 2.2 动画为 720P、2–30 秒、15/25fps。

## 图片生成与编辑

- **文生图**：`wan2.7-image-pro` 集成文字渲染、品牌色控制、角色一致性多图生成与编辑，文生图最高 4096×4096、编辑最高 2048×2048。仅生成且追求速度/成本选 `z-image-turbo`（速度快约 10 倍、价格约 1/5）。需要负向提示词或单次最多 6 张变体选 `qwen-image-2.0-pro`。
- **图片编辑**：`wan2.7-image-pro` 支持多图参考（最多 9 张输入）、边界框交互式编辑、角色一致性多图生成。需负向提示词编辑用 `qwen-image-2.0-pro`（生成与编辑同一模型 ID）。

详见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。最大输出数：Wan 标准模式 4 张（连续 12 张）、`z-image-turbo` 1 张、`qwen-image-2.0-pro` 6 张。

## 3D 模型生成（Tripo）

通过异步任务调用 Tripo 模型，支持文生 3D、单图生 3D、多图生 3D 三种模式。详见 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

- **重要**：仅适用于"中国内地（北京）"地域，必须使用该地域的 [API Key](../concepts/api-key.md)。
- 调用流程：`POST /api/v1/services/aigc/video-generation/3d-generation`（带 `X-DashScope-Async: enable`）获取 `task_id` → 轮询 `GET /api/v1/tasks/{task_id}` 取结果。任务状态 `PENDING → RUNNING → SUCCEEDED/FAILED`，建议轮询间隔 15 秒，`task_id` 查询有效期 24 小时。
- 模式区分：`input.prompt`（文生）、`input.image`（单图）、`input.images`（2–4 张多角度）三字段互斥。
- 贴图质量 `parameters.texture_quality`：`standard`（默认标清）/`detailed`（高清）。需无贴图模型时同时设置 `texture=false` 与 `pbr=false`，返回 `base_model_url`。
- 几何精度 `parameters.geometry_quality`：仅 `Tripo/Tripo-H3.1` 支持，`standard`（≤150 万面）/`ultra`（≤200 万面）。
- 选型：不确定时先用 `Tripo/Tripo-P1.0`（2 万面、更快）快速验证，再用 `Tripo/Tripo-H3.1`（200 万面、较慢）生成高精度版本。产物 `pbr_model_url` / `base_model_url` 有效期 2 小时。
- 图片要求：JPEG/PNG，宽高 20–6000 像素（建议 >256），不超过 20MB。

## 语音合成（TTS）

详见 [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。先确定内置音色还是自定义音色：

- **标准语音合成**：内置音色库即选即用，推荐 `cosyvoice-v3-plus`、`MiniMax/speech-2.8-hd`。
- **自定义音色**：声音复刻（提供音频样本）与声音设计（文字描述音色）均推荐 `cosyvoice-v3.5-plus`；`MiniMax/speech-2.8-hd` 仅支持声音复刻。

接入方式：

- **WebSocket**：双向流式，延迟最低，适合智能客服、语音助手、呼叫中心。CosyVoice 同一模型名同时支持 WS 与 HTTP；Qwen-TTS 用 `-realtime` 后缀区分 WS 接入。
- **HTTP**：发送完整文本，支持流式返回音频，适合有声阅读、内容制作。

指令控制：用自然语言动态控制语速、情绪、风格（如"用温柔的语气，语速稍慢"）。支持模型：CosyVoice 系列（`cosyvoice-v3.5-plus/flash`、`cosyvoice-v3-flash`）与 Qwen-TTS-Instruct 系列（`qwen3-tts-instruct-flash` 及其 `-realtime` 版本）。`cosyvoice-v3.5-plus/flash` 的复刻音色支持中文方言（普通话、粤语、东北话、闽南话等 16 种）及英、法、德、日、韩、俄、葡、泰、印尼、越南语；声音设计音色仅支持中英。

## 语音转语音（S2S）

面向"语音输入 → 语音输出"场景。与 Pipeline（ASR+LLM+TTS 串行）相比，S2S 单模型流式处理延迟更低、能端到端感知语调情绪，但音色定制能力弱（仅预设音色）。详见 [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

按场景选模型：

- 语音助手/客服对话：`qwen3.5-omni-plus-realtime`（WS）；成本敏感用 `qwen3.5-omni-flash-realtime`。
- 同声传译/直播翻译：`qwen3.5-livetranslate-flash-realtime`（WS，60 种语言）。
- 视频配音/播客翻译：`qwen3-livetranslate-flash`（HTTP，18 种语言 + 5 种中文方言，约 3 秒延迟）。
- 视频分析/批量打标（需思考模式）：`qwen3-omni-flash`（HTTP）。

附带能力：Function Calling（Qwen3.5-Omni WS+HTTP、Qwen3-Omni 仅 HTTP；realtime 与 Livetranslate 不支持）、联网搜索（仅 Qwen3.5-Omni，含 Plus/Flash）、思考模式（Qwen3-Omni HTTP，思考下不生成语音）。联网搜索与 Function Calling 不可同时开启。

> **注意**：实时模型（`*-realtime`）和 Livetranslate 模型不支持 Function Calling；Qwen3-Omni-Flash 与 Livetranslate 不支持联网搜索。

## 语音识别（ASR）

详见 [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。选型四维度：

- **实时 vs 非实时**：实时基于 WebSocket 流式，非实时基于 HTTP 提交文件。实时推荐 `fun-asr-realtime`（热词、方言）或 `qwen3.5-omni-plus-realtime`（Prompt 上下文、多语种）；非实时推荐 `fun-asr`（热词、说话人分离）或 `qwen3.5-omni-plus`（Prompt 上下文）。
- **专业术语**：Prompt 上下文注入（`qwen3.5-omni-plus(-realtime)`，自适应但延迟高）或热词（`fun-asr(-realtime)`，适合稳定术语列表）。Qwen3.5-Omni 非传统 ASR，而是能理解音频的 LLM。
- **说话人分离**：仅 Fun-ASR 非实时模型（`fun-asr`、`fun-asr-mtl`）支持。
- **情感识别**：Qwen-ASR 与 Qwen3.5-Omni 支持，推荐 `qwen3-asr-flash-realtime`（实时）或 `qwen3-asr-flash-filetrans`（非实时）。

音频规格：非实时模型多支持 12 小时 / 2GB（`fun-asr-flash-2026-06-15` 为 5 分钟 / 2GB，`qwen3.5-omni-plus` 为 3 小时 / 2GB，`qwen3-asr-flash` 为 5 分钟 / 10MB）；实时模型无时长限制（`qwen3.5-omni-plus-realtime` 限 2 小时）。Paraformer 为早期模型，建议迁移到 Fun-ASR 或 Qwen-ASR。

## 音乐生成（fun-music）

百聆音乐大模型，根据提示词或歌词生成完整男/女声演唱的中英文歌曲。详见 [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

- **重要**：处于邀测阶段，需在模型广场申请开通；仅在华北2（北京）地域可用。
- 模型：`fun-music-preview`、`fun-music-v1`。歌词与提示词语言：中文、英文。
- 接口：`POST /api/v1/services/audio/music/generation`。参数 `prompt`（描述风格场景，模型自动创作歌词）与 `lyrics`（自定义歌词）二选一，同时提供时仅 `lyrics` 生效；`gender` 取 `male`/`female`。输出 MP3/WAV。
- 流式：请求头加 `X-DashScope-SSE: enable`，边生成边返回。字符数限制：非流式 `lyrics` 中文 5–350 / 英文 5–2000，`prompt` 1–2000；流式 `lyrics` 中文 300–350 / 英文 200–250 词，`prompt` 5–1000。

## 向量与重排序

详见 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

- **文本 Embedding**：推荐 `text-embedding-v4`（64–2048 维，默认 1024，最大 8192 [Token](../concepts/token.md)）。迁移已有 v3 索引用 `text-embedding-v3`（512–1024 维，与 v3 兼容）。维度选择：大规模+存储受限选 256/512；通用选 1024；高精度选 1536/2048。
- **[多模态](../concepts/multimodal.md) Embedding**：图文混合检索（融合向量）用 `qwen3-vl-embedding`（256–2560 维，默认 2560，最大 32000 [Token](../concepts/token.md)）或 `qwen2.5-vl-embedding`（仅融合向量）；跨模态搜索（文搜图/图搜图，独立向量）用 `tongyi-embedding-vision-plus`（仅独立向量）或其 flash 版本（注重成本）。
- **重排序**：纯文本用 `qwen3-rerank`（100+ 语言，最多 500 文档，4000 Token/条）；[多模态](../concepts/multimodal.md)用 `qwen3-vl-rerank`（文本/图片/视频混合，8000 Token/条）。另有 `gte-rerank-v2` 用于文本语义检索。

## 全模态

详见 [全模态](../../raw/model-user-guide/model-experience/omni.md)。三个系列：Qwen3.5-Omni（旗舰，能力最全）、Qwen3-Omni-Flash（轻量、成本低、支持深度推理仅输出文本）、Qwen3.5-Livetranslate（专业翻译、开箱即用）。

按场景：

- 实时语音/视频对话（WS）：`qwen3.5-omni-plus-realtime`。
- 音视频内容分析（HTTP）：`qwen3.5-omni-plus`（音频最长 3 小时、视频最长 1 小时）。
- 轻量音视频分析（HTTP，单次输入 ≤150 秒，支持思考模式，仅文本）：`qwen3-omni-flash`。
- 实时语音翻译（WS，约 3 秒延迟，60 种语言）：`qwen3.5-livetranslate-flash-realtime`。
- 音视频文件翻译（HTTP）：`qwen3-livetranslate-flash`。
- 声音复刻（参考音频生成回复）：`qwen3.5-omni-plus/flash`（HTTP/WS）。

能力：Function Calling（Qwen3.5-Omni WS+HTTP、Qwen3-Omni-Flash 仅 HTTP）、联网搜索（仅 Qwen3.5-Omni，与 Function Calling 互斥）。翻译语言覆盖：Qwen3.5-Omni 支持 113 种输入语言/方言、29 种输出语言 + 7 种中文方言；Qwen3.5-Livetranslate 支持 60 种语言（29 种音频+文本、31 种仅文本）；Qwen3-Omni-Flash 支持 11 种输出语言 + 8 种中文方言；旧版 `qwen-omni-turbo` 仅支持中英。

## 通用接入与限制

- **地域**：多数模型支持中国内地、新加坡、美国、法兰克福；3D 生成（Tripo）与音乐生成（fun-music）仅在华北2（北京）可用，且必须使用对应地域的 [API Key](../concepts/api-key.md)。
- **异步任务**：视频/图片/3D/音乐生成均为异步，通过 `X-DashScope-Async: enable` 创建任务后轮询结果；部分产物 URL（如 3D 的 `pbr_model_url`）有效期仅 2 小时，需及时下载。
- **实时 vs 文件**：语音类能力普遍区分实时（WebSocket，`-realtime` 后缀，流式低延迟）与非实时（HTTP，整段提交，可换取更好效果）。
- **版本管理**：文本/视觉等系列提供带日期的历史快照版本，供需要锁定特定版本的场景使用；新项目应优先使用当代主线版本。
- **[计费](../concepts/billing.md)**：旧版 Qwen-TTS（`qwen-tts` 等）按 Token [计费](../concepts/billing.md)；音乐生成、3D 生成等邀测/地域受限服务需先开通。
- **SDK**：Fun-ASR、CosyVoice 等支持 DashScope Java/Python SDK，CosyVoice 与 Fun-ASR 还支持 Android/iOS SDK；其他模型按对应 WebSocket/HTTP 协议直接调用。

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




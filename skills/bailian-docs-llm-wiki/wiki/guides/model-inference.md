# model inference

百炼平台的模型推理覆盖文本、视觉、图片生成、视频生成、语音、全模态、3D 和向量重排等场景，每个场景按"先选维度（实时/非实时、模态、能力）、再看模型"的方式选型。本页汇总各类推理模型的核心选型逻辑、关键参数与共有能力，方便快速定位到对应的子领域文档。

## 按模态/场景选型

### 文本生成（LLM）

适用于聊天机器人、智能体、内容生成、文档处理、代码与长上下文场景。

- 旗舰能力：`qwen3.7-max`（1M 上下文，最强推理），平衡首选 `qwen3.7-plus`，低成本选 `qwen3.6-flash`，三者均支持 1M 上下文与完整的思考模式、Function Calling、内置工具、结构化输出、批量调用。
- 第三方对位：`deepseek-v4-pro`、`deepseek-v4-flash`（1M 上下文）、`glm-5.1`（198k）、`kimi-k2.6`（256k）、`MiniMax-M2.5`（192k）、`mimo-v2.5-pro`（1M）。
- 闭源模型对位推荐：GPT-5.5 / Claude Opus 4.7 / Gemini 3.1 Pro → `qwen3.7-max`；GPT-5.4 / Claude Sonnet 4.6 / Gemini 3 Pro → `qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.1`；轻量档 → `qwen3.6-flash`、`deepseek-v4-flash`、`MiniMax-M2.5`。
- 思考模式通过 `enable_thinking` 开启（Responses API 走 `reasoning.effort`），Qwen3 及以上系列均支持，多数为混合模式，可按请求切换。

详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

### 视觉理解（图像/视频/OCR）

适用于图像分析、视频理解、OCR、表格/手写提取等。

- 通用旗舰 `qwen3.7-plus`：1M 上下文，单图最高 1600 万像素，视频最长 2 小时 / 2GB，最多 2048 张图、64 个视频，支持 Function Calling、内置工具、结构化输出。
- 低成本：`qwen3.6-flash`（同上下文与功能，最多 256 图）。
- OCR 专用：`qwen-vl-ocr`（文档、表格、试卷、手写）；通用 OCR 也可用 `qwen3.6-plus / flash`。
- 视频时长上限存在差异：Qwen3.7/3.6/3.5 系列 2 小时；Qwen3-VL 与 Qwen3.5-Omni 系列 1 小时。
- 图片 Token 计算公式：`h * w / (32 * 32) + 2`。

详见 [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

### 图片生成与编辑

- 文生图与图片编辑首选 `wan2.7-image-pro`：文字渲染、品牌色控制、角色一致性多图、最多 9 张参考图与边界框交互式编辑，文生图最高 4096x4096，编辑最高 2048x2048。
- 极速/低成本写实场景 → `z-image-turbo`（仅生成，不支持编辑）；需要负向提示词或一次最多 6 张变体 → `qwen-image-2.0-pro`。
- Legacy `wanx2.1-imageedit` 仅在北京地域可用。

详见 [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

### 视频生成与编辑

涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、角色动画/替换等模式。

- 文生视频首选 `happyhorse-1.0-t2v`（有声、1080P、3-15 秒）；需要自定义音频文件用 `wan2.7-t2v-2026-04-25`。
- 首帧生视频首选 `happyhorse-1.0-i2v`；首尾帧串联长视频用 `wan2.7-i2v-2026-04-25`。
- 参考生视频 `happyhorse-1.0-r2v` / `wan2.7-r2v`；视频编辑 `happyhorse-1.0-video-edit` 或 `wan2.7-videoedit`（特效复刻、运镜复刻）。
- 角色动画：`wan2.2-animate-move`（动作迁移）、`wan2.2-animate-mix`（视频中替换人物），均提供 wan-std / wan-pro 两种模式（pro 更接近实拍、std 更快更便宜）。

详见 [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)。

### 语音合成（TTS）

按"内置音色 vs 自定义音色"和"WebSocket vs HTTP"两个维度选型。

- 标准合成首选 `cosyvoice-v3-plus`、`MiniMax/speech-2.8-hd`。
- 自定义音色：声音复刻（提供音频样本）首选 `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash` / `MiniMax/speech-2.8-hd`；声音设计（文字描述）仅 `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash` 支持。
- 实时低延迟选 WebSocket；CosyVoice 同一模型名同时支持 WebSocket 与 HTTP；Qwen 系列以 `-realtime` 后缀区分。
- 指令控制（语速、情绪、风格、方言）：CosyVoice v3.5/v3-flash 与 Qwen3-TTS-Instruct-Flash 系列支持。

详见 [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)。

### 语音识别（ASR）

按实时/非实时、是否需要专业术语、说话人分离、情感识别 4 个维度逐项确认。

- 实时：`fun-asr-realtime`（热词、多方言）或 `qwen3.5-omni-plus-realtime`（Prompt 上下文注入、情感识别）。
- 非实时：`fun-asr`（热词、说话人分离，文件 ≤12 小时 / 2GB）或 `qwen3.5-omni-plus`（Prompt 上下文、情感识别，文件 ≤3 小时 / 2GB）。
- 情感识别：Qwen-ASR 与 Qwen3.5-Omni 系列在转写同时返回情感标注，实时推荐 `qwen3-asr-flash-realtime`，非实时 `qwen3-asr-flash-filetrans`。
- 说话人分离：仅 Fun-ASR 系列的非实时模型（`fun-asr`、`fun-asr-mtl`）支持，启用时建议音频 ≤2 小时。
- 旧版 Paraformer / Gummy / SenseVoice 建议迁移到 Fun-ASR 或 Qwen-ASR。

详见 [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)。

### 语音转语音（S2S）与全模态

"语音输入 → 语音输出"场景可选**单模型 S2S**（端到端，低延迟，能感知语调情绪）或 **Pipeline（ASR + LLM + TTS）**（可自定义音色、可分别选型）。

- 实时对话：`qwen3.5-omni-plus-realtime`（旗舰）或 `qwen3.5-omni-flash-realtime`（成本敏感）。
- 同传/直播翻译：`qwen3.5-livetranslate-flash-realtime`（60 种语言，约 3 秒延迟）；视频/播客翻译 `qwen3-livetranslate-flash`（HTTP）。
- 视频分析/批量打标（需思考模式）：`qwen3-omni-flash`（HTTP）。
- S2S 单模型路线附带能力（Pipeline 路线需由 LLM 组件分别支持）：Function Calling（Qwen3.5-Omni 全量、Qwen3-Omni-Flash 仅 HTTP）、联网搜索（仅 Qwen3.5-Omni）、思考模式（仅 Qwen3-Omni HTTP）。

详见 [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md) 与 [全模态](../../raw/model-user-guide/model-inference/omni.md)。

> **注意**：S2S 与 全模态两份文档列出的"粤语翻译支持"存在描述差异——"语音转语音"标注 Qwen3.5-Livetranslate 对粤语"仅文本"输出，而"全模态"在同一列显示"支持 仅文本"。功能本质一致（不输出语音），以"仅文本"理解为准。

> **注意**：Qwen3-Omni-Flash 的思考模式仅在 HTTP（非实时）下可用，且**思考模式下不会生成语音**，需要语音响应时必须关闭思考模式。

### 音乐生成

百聆 Fun-Music（`fun-music-v1` / `fun-music-preview`）通过 `prompt`（描述风格/场景，模型自动写词）或 `lyrics`（自定义歌词）生成男/女声中英文歌曲，支持 MP3 / WAV、流式与非[流式输出](../concepts/streaming.md)。

- `lyrics` 与 `prompt` 至少传一个；同时传时 `lyrics` 生效，`prompt` 被忽略。
- 字符数限制因流式模式而异：非流式 `lyrics` 中文 5~350 / 英文 5~2000、`prompt` 1~2000；流式 `lyrics` 中文 300~350 / 英文 200~250 词、`prompt` 5~1000 词。
- 启用流式需在请求头加 `X-DashScope-SSE: enable`。
- 仅支持中英文歌词；严禁抄袭已发表作品。

详见 [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)。

> **注意**：Fun-Music 处于**邀测阶段**，需在模型广场申请开通，且仅在**中国内地（北京）**地域可用。

### 3D 模型生成

Tripo 系列通过 `prompt`（文生 3D）、`image`（单图生 3D）或 `images`（多图生 3D，2~4 张多角度）三种互斥模式生成 GLB 格式 3D 模型。

- `Tripo/Tripo-P1.0`：最高 2 万面，速度更快，适合快速预览、游戏/AR、实时应用。
- `Tripo/Tripo-H3.1`：最高 200 万面（`geometry_quality=ultra`），速度较慢，适合影视级渲染、高精度数字资产。
- 贴图质量 `parameters.texture_quality`：`standard`（默认）/ `detailed`；同时设置 `texture: false` 和 `pbr: false` 则返回无贴图基础模型。
- 任务异步执行（`X-DashScope-Async: enable`），建议 15 秒间隔轮询。返回的 `pbr_model_url` / `base_model_url` / `rendered_image_url` **有效期 2 小时**。

详见 [Tripo 3D 模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)。

> **注意**：Tripo 3D 仅在**中国内地（北京）**地域可用，且必须使用该地域签发的 API Key。

### 向量（Embedding）与重排序（Rerank）

用于语义搜索、RAG、跨模态匹配。

- 纯文本：`text-embedding-v4`（64~2048 维，默认 1024，8192 Token）；迁移旧索引用 `text-embedding-v3`（512~1024 维）。
- 多模态融合向量（图文一个向量）：`qwen3-vl-embedding`（256~2560 维）、`qwen2.5-vl-embedding`（512~2048 维，仅融合向量）。
- 跨模态独立向量（文搜图、图搜图）：`tongyi-embedding-vision-plus` / `flash` 系列。
- 重排序：纯文本 `qwen3-rerank`（100+ 语言、最多 500 文档）、多模态 `qwen3-vl-rerank`（文/图/视频混合）、`gte-rerank-v2`（文本 RAG）。
- 维度选择经验：大规模搜索且存储受限选 256/512；通用 1024；高精度 1536/2048。

详见 [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)。

## 共通能力速查

| 能力 | 含义 | 主要支持范围 |
| --- | --- | --- |
| Function Calling | 自定义工具，由模型决定调用 | Qwen3 系列全量 LLM、视觉 LLM；Omni（HTTP / 部分 WebSocket） |
| 内置工具 | 无需配置即可联网搜索、代码执行等 | `qwen3.7-*`、`qwen3.6-plus/flash`、`qwen3.5-plus/flash` 及部分视觉模型 |
| 思考模式 | 显式推理，回答质量优先 | Qwen3 及以上 LLM；Qwen3-Omni-Flash（仅 HTTP） |
| 结构化输出 | 强约束 JSON 返回 | Qwen3 系列文本与视觉非思考模式 |
| 批量推理 | 离线大批量、低成本 | `qwen3.7-max/plus`、`qwen3.6-plus/flash`、`qwen3.5-plus/flash`、`qwen-long` 等 |
| WebSocket vs HTTP | 实时双向流 vs 文件/单次请求 | TTS、ASR、S2S、Omni、Livetranslate 各系列均有对应接入方式 |

## 限制与注意事项

- **地域限制**：Tripo 3D 与 Fun-Music 仅在中国内地（北京）地域可用；Legacy `wanx2.1-imageedit` 同样仅限北京。其它海外节点的模型清单见各子文档中的"模型广场"区域链接。
- **版本快照与稳定性**：所有"latest/主版本"模型会持续更新，需要稳定行为的生产场景请固定具体日期快照（如 `qwen3.7-plus-2026-05-26`），但批量推理通常只在主线版本生效。
- **输出/资源有效期**：Tripo 输出 URL 有效期 2 小时；Fun-Music 音频 URL 有效期 24 小时；ASR [异步任务](../concepts/async-task.md)结果 24 小时；请及时下载保存。
- **互斥参数**：Tripo 的 `prompt`/`image`/`images` 三者互斥；Fun-Music 同时传 `lyrics` 与 `prompt` 时 `prompt` 被忽略；S2S 联网搜索与 Function Calling 不可同时开启。
- **旧版迁移建议**：文本生成与视觉理解的 Qwen2.5、Qwen3-VL、QVQ、Qwen-Omni-Turbo 等不再首选推荐，新项目建议直接使用 Qwen3.5 / Qwen3.6 / Qwen3.7 系列；ASR 推荐从 Paraformer / Gummy / SenseVoice 迁移到 Fun-ASR 或 Qwen-ASR。
- **Token / 像素消耗**：视觉模型按 `h * w / (32 * 32) + 2` 计算每图 Token，高分辨率显著增加成本；文本模型的"思考预算"会单独计费，长上下文需评估总 Token。
- **接入 SDK 覆盖**：CosyVoice / Fun-ASR 的 WebSocket 模型额外支持 Android、iOS SDK；其它模型多走 DashScope Java / Python SDK 或直接调 WebSocket / HTTP 协议。

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




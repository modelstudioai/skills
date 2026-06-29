# 模型选型

模型选型是指在百炼平台提供的自研千问与第三方大模型矩阵中，按业务场景、能力档位、成本与延迟需求匹配最合适的模型，并选定对应地域、接入域名与调用方式的过程。选型结果直接决定效果、吞吐、合规性与单位成本。

## 选型总体思路

1. **先定场景**：明确任务是文本生成、视觉理解、视频/图像/3D 生成、语音、向量检索，还是 RAG、调优、深度研究等专用领域。
2. **再定能力档**：在同类模型中按「高能力档 / 平衡档 / 轻量低成本档」对位选择，效果稳定后再用低档降本。
3. **最后定接入**：根据合规与并发要求选择地域、服务部署范围与接入域名，并确认调用协议（OpenAI 兼容 / DashScope SDK / WebSocket / 异步任务）。

## 文本生成场景选型

对话、抽取、改写、Agent 等文本任务推荐从 `qwen3.7-plus` 入手——能力、速度与成本均衡，支持 1M 上下文、完整 Function Calling 与内置工具；需要最强推理选 `qwen3.7-max`；快速响应的简单任务用 `qwen3.6-flash` 降本。

从闭源或第三方模型迁移时按能力档对位：

| 能力档 | 千问 | 第三方对位 |
| --- | --- | --- |
| 高能力档 | `qwen3.7-max` | — |
| 平衡档 | `qwen3.7-plus` | `deepseek-v4-pro` / `glm-5.2` |
| 轻量低成本档 | `qwen3.6-flash` | `deepseek-v4-flash` / `MiniMax-M2.5` |

> 注意：第三方模型（`deepseek-v4-pro`、`kimi-k2.7-code`、`MiniMax-M2.5`、`mimo-v2.5-pro` 等）通常不支持内置工具与结构化输出，迁移时需评估能力差异。

## [多模态](multimodal.md)场景选型

| 模态 | 推荐入口 | 备选 / 降本 |
| --- | --- | --- |
| 视觉理解 / OCR | `qwen3.7-plus`（1M 上下文、2h 视频） | `qwen3.6-flash` 降本；`qwen-vl-ocr` 专做文档/表格/手写提取 |
| 图像生成 | `wan2.7-image-pro` / `qwen-image-2.0-pro` | `z-image-turbo` |
| 视频生成 | `happyhorse-1.1-t2v`（有声 1080P） | `wan2.7-t2v/i2v/r2v` 系列（自定义音频、首尾帧、角色一致性） |
| 3D 生成 | `Tripo/Tripo-H3.1` / `Tripo/Tripo-P1.0` | 仅北京地域，异步任务 |
| 语音合成（TTS） | `cosyvoice-v3.5-plus` | `qwen3-tts-instruct-flash` |
| 语音识别（ASR） | `fun-asr-realtime` | `qwen3.5-omni-plus-realtime` |
| 语音转语音 / 全模态 | `qwen3.5-omni-plus-realtime` | `qwen3.5-livetranslate-flash-realtime` |
| 音乐生成 | `fun-music-v1` | 邀测，仅北京 |
| 向量与重排序 | `text-embedding-v4` / `qwen3-rerank` | `qwen3-vl-embedding`（[多模态](multimodal.md)向量） |

视频、图像、3D、音乐等生成类模型统一走异步任务模式；语音类多走 WebSocket / HTTP；向量与重排序走 HTTP。

## 专用领域模型选型

除通用对话模型外，百炼提供面向特定任务的专用模型，选型时需关注地域与协议差异：

- **法律**：`farui-plus`，法律咨询/文书生成，DashScope SDK。
- **意图理解**：`tongyi-intent-detect-v3`，同时输出意图与[函数调用](function-calling.md)信息。
- **深度研究**：`qwen-deep-research`，两阶段（反问确认 + 深入研究），**仅 Python DashScope SDK、仅华北2（北京）**，不支持 OpenAI 兼容接口。
- **翻译**：`qwen-mt-plus`，支持术语干预、翻译记忆、领域提示。
- **OCR 与结构化抽取**：`qwen3.5-ocr`，可设 `min_pixels` / `max_pixels` 控制图像分辨率与 token 消耗。
- **界面交互**：`gui-plus-2026-02-26`，通过 `computer_use` 工具操控桌面 GUI，仅北京。

## 选型时的关键参数与能力差异

- **思考模式**：通过 `enable_thinking` 开启（Responses API 用 `reasoning.effort` 控制深度），Qwen3 及以上支持，多为可按请求切换的混合模式。
- **Function Calling 与内置工具**：自定义工具全系列通用模型支持；内置工具（联网搜索、代码解释器、网页抓取）仅部分模型支持，如 `qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`mimo-v2.5-pro`。
- **结构化输出**：非思考模式下返回合法 JSON，用于字段抽取；第三方模型多不支持。
- **上下文与[多模态](multimodal.md)限制**：视觉模型单张图片最高 1600 万像素，token 计算 `h × w / (32 × 32) + 2`；视频时长上限因模型而异（2 小时 / 2GB 或 1 小时 / 2GB）。
- **[流式输出](streaming-output.md)**：`stream` 参数控制；`qwen-deep-research` 反问阶段必须设为 `true`。

## 地域、部署范围与接入域名

地域决定接入点与数据存储位置，服务部署范围决定推理执行位置，接入域名决定并发承载与隔离性。三者共同影响可选模型与稳定性。

- **地域**：华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）。各地域模型列表、API Key、接入域名独立，**不能跨地域混用**。
- **服务部署范围**：无合规需求选「全球」（资源池更大）；有合规需求选特定地理边界（中国内地/美国/欧盟/日本/国际）。北京、新加坡各仅支持一种范围，无需选择。
- **接入域名**：生产环境推荐专属域名 `{WorkspaceId}.{region}.maas.aliyuncs.com`（99.9% SLA、超时 3600 秒、支持 HTTP/SSE/WebSocket/WebRTC）；共享域名 `dashscope.aliyuncs.com` 兼容存量；试用域名仅用于快速体验。
- **模型后缀**：美国地域使用带 `-us` 后缀的模型名（如 `qwen-plus-us`）可限定美国境内推理，不带后缀默认全球推理。

## 选型实践建议

- 先在控制台「模型体验」中迭代 Prompt，效果稳定后再固化到代码；切换模型后应回归测试。
- 穷尽 Prompt 工程与 RAG 方案后再投入模型调优（SFT/CPT/DPO），性价比最高。
- 低延迟批量场景可使用批量推理降本；遇 429 限流时用指数退避 + 客户端令牌桶平滑流量。
- 切换模型前关注上下文长度、[函数调用](function-calling.md)、[流式输出](streaming-output.md)、[计费](billing.md)方式与地域支持的差异。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [get started with models](../guides/get-started-with-models.md)
- [use cases](../guides/use-cases.md)
- [more models](../api/more-models.md)



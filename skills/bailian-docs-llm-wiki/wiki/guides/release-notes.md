# release notes

百炼平台的 release notes 由两条主线组成：一是**平台功能更新**（计费调整、API 变更、新模块上线、下线公告等），二是**模型上下架与更新**（新模型上架、快照版本发布、价格调整、模型下线）。本页汇总两类动态的查阅入口、近期重要变更和开发者需要关注的迁移事项。

## 平台功能更新

平台功能动态按年月组织，每条记录包含日期、功能模块、功能点和说明。完整时间线见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。页面顶部还维护一组**公告通知**，涉及降价、免费额度调整、资源包活动和模型下线机制等，计费相关问题建议优先查阅该区域。

### 近期重点功能（2026 年）

| 模块 | 变更 | 说明 |
| --- | --- | --- |
| 智能体托管 | Managed Agent 商业化 / 智能体托管运行时 API 上线 | 平台托管会话与工具执行；2026-07 起商业化计费 |
| 知识库 RAG | 知识检索服务、知识问答服务上线 | 支持多知识库联合检索与混合排序；检索调用可投递 SLS 日志 |
| 记忆库 | Memory 2.0 上线并商业化 | 自动提取记忆片段与用户画像，多应用可共享同一记忆库 |
| Responses API | 新增[异步调用](../concepts/async-invocation.md) | 通过 `background=true` 提交长耗时任务并轮询结果 |
| API 鉴权 | 临时 [API Key](../concepts/api-key.md) 文档上线 | 不可信环境下避免永久 [API Key](../concepts/api-key.md) 泄露 |
| 模型部署 | PTU 新增长输入与前缀缓存 | 预置吞吐部署支持长输入与前缀缓存能力 |
| 接入工具 | 新增 Codex、Kilo CLI 等客户端接入 | 支持 [Token](../concepts/token.md) Plan / Coding Plan / 按量计费三种方式 |
| 模型调优 | 强化学习（RL）训练（邀约制）、图像/视频/VL 模型类型支持 | 调优支持的模型类型持续扩展 |
| 模型评测 | 排行榜（Leaderboard）与综合评测 | 支持 BLEU_4、ROUGE 等评分方法，多模型横向对比 |
| 计费 | 团队版共享用量包、Coding Plan Pro 首月特惠 | 跨坐席共享 Credits 弹性用量包可抵扣超额用量 |

2026 年 7 月还有多条**下线/退市类公告**：企业知识库（旧）下线、部分老旧模型及长尾模型下线、析言 GBI 商品退市、qwen-turbo 资源包启动退市等，详见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)的公告与功能动态区。

### 模型调优与部署能力演进（2025 年）

- 2025-10：新增**按模型单元（MU）的部署方式**（按时间计费），可灵活调整模型性能、成本可预测。
- 2025-10：千问3-VL-8B-Instruct / Thinking 支持 SFT 调优（全参微调与 LoRA）和调优后部署。
- 2025-09：千问 3（32B/14B/8B）与千问 2.5（72B/32B/14B/8B）支持 **DPO 偏好训练**，通过负反馈降低幻觉。
- 2025-08：千问2.5-VL（72B/32B/7B）支持调优并部署。
- 2025-07：新增**免费额度用完即停**功能，额度耗尽后调用返回错误码 `AllocationQuota.FreeTierOnly`，避免产生额外费用。

## 模型上下架与更新

模型上架记录按地域组织（当前主要为华北2-北京），每条包含模型类型、时间、模型规格（model id）和功能说明。完整清单见[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)；**模型下线**规则及清单参考官方"模型下线机制说明"文档。

### 近期上架的代表性模型（2026 年）

- **文本/推理**：`qwen3.7-flash`（[多模态](../concepts/multimodal.md)理解与 Agent 能力全面提升）、`qwen3.7-max` / `qwen3.7-max-2026-06-08`（新增视觉模态）、`qwen3.7-plus`（[多模态](../concepts/multimodal.md)交互混合智能体）、`qwen3.6-flash`、`qwen3.6-27b`、`qwen3.6-max-preview`（仅纯文本输入、默认思考模式）。
- **第三方直供**：`kimi/kimi-k3`（2.8 万亿参数、100 万 token 上下文）、`kimi/kimi-k2.7-code` 及其 highspeed 版本（速度提升 5~6 倍）、`deepseek-v4-pro` / `deepseek-v4-flash`（阿里直供）、`vanchin/deepseek-v4-pro`（快手万擎直供）、`ZHIPU/GLM-5.1`、`stepfun/step-3.7-flash`、`xiaomi/mimo-v2.5-pro`。
- **图像生成**：`qwen-image-3.0-pro`（邀测，长文本输入与密集排版）、`qwen-image-2.0-pro-2026-06-22`（文字渲染增强，支持最长 1k token 指令）。
- **视频生成/编辑**：万相 2.7 系列（`wan2.7-t2v` / `wan2.7-i2v` / `wan2.7-r2v` / `wan2.7-videoedit`）、HappyHorse 1.0/1.1 系列（支持有声视频，3~15 秒、720P/1080P）、爱诗 C1/V6 系列、Vidu 系列。
- **语音/音频**：`qwen-audio-3.0-realtime-plus/flash`（端到端实时语音对话）、`qwen-audio-3.0-tts-plus/flash`（语音合成）、`fun-asr`（30 语种、七大方言）、`fun-music-v1`（音乐生成）。
- **其他**：`qwen3.5-ocr`（128K 上下文文字提取）、`qwen3.5-livetranslate-flash-realtime`（60 语种识别、29 语种实时翻译）、Tripo 3D 生成、pixverse 视频对口型/动作模仿/超清。

### 价格调整示例

`deepseek-v4-pro` 自 2026-04-29 起 `cached_token` 单价调整为 **1 元/百万 token**，标准 `input_token` 单价不变（上下文缓存计费）。更多降价公告见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)顶部的公告通知区。

## 使用方式与注意事项

- **如何跟进变更**：功能动态按月归档，模型上架按地域列表维护；接入前建议核对所用模型的 model id 是否为最新快照版本（如 `qwen3.7-max-2026-06-08` 与稳定别名 `qwen3.7-max` 并存）。
- **下线风险**：平台会定期下线老旧/长尾模型并发布延期下线通知，生产环境应关注公告通知区与"模型下线机制说明"，避免依赖即将退市的模型或资源包（如 qwen-turbo 资源包已启动退市）。
- **计费变更**：降价、资源包退市、商业化（记忆库、Managed Agent）等公告直接影响账单，升级集成前先核对最新计费规则。
- **思考模式差异**：部分新模型默认开启思考模式或仅支持思考模式（如 `qwen3.7-max`、`kimi/kimi-k2.7-code`），调用参数需按对应模型文档配置。

> **注意**：[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)中华北2（北京）地域的 `wan2.7-t2v-2026-06-12` 快照条目日期标注为 2026-07-01，与相邻条目（2026-04-26 的 `wan2.7-t2v-2026-04-25`）在时间排序上不一致，引用该快照版本日期时请以官方页面为准。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)





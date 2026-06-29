# release notes

本页汇总阿里云百炼模型平台的发布动态，包含模型上下架与更新、平台功能更新、[计费](../concepts/billing.md)调整等内容。开发者可据此了解新增模型规格、调优/部署能力、API 接口与 SDK、观测与评测能力等最新进展，便于选型与对接。详细条目以官方 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 与 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 为准。

## 模型上下架

百炼持续上架新模型规格并按规则下线旧版本，下线规则参见模型下线机制说明。近期重点上架模型（华北2-北京、中国内地部署范围）：

- **推理模型**
  - `qwen3.7-max` / `qwen3.7-max-2026-05-20`：Qwen Max 新一代旗舰，仅纯文本输入，默认开启思考模式，支持显式缓存，编程、办公与生产力、长周期自主执行表现突出。
  - `qwen3.7-plus` / `qwen3.7-plus-2026-05-26`：在文本能力基础上全面升级视觉-语言能力，可读取屏幕并操作 GUI、基于视觉参考生成代码、端到端导航移动应用。
  - `qwen3.6-max-preview` / `qwen3.6-plus` / `qwen3.6-flash` / `qwen3.6-35b-a3b`：Qwen3.6 系列，Coding 与 Agent 执行能力提升，Flash 系列为原生视觉语言模型，空间智能、物体定位与检测增强。
  - `deepseek-v4-pro` / `deepseek-v4-flash`（阿里直供）、`vanchin/deepseek-v4-pro`（快手万擎直供）、`stepfun/step-3.7-flash`、`xiaomi/mimo-v2.5-pro`、`ZHIPU/glm-5.1` / `ZHIPU/glm-5`、`kimi/kimi-k2.7-code` / `kimi/kimi-k2.7-code-highspeed` 等第三方模型陆续上架。
- **文生文与视觉理解**：`kimi/kimi-k2.6`、`qwen3.5-ocr`（文字提取，128K 上下文，多轮对话，覆盖多种国内外卡证）。
- **图像生成与编辑**：`qwen-image-2.0-pro-2026-06-22`（融合图片生成与编辑，文字渲染增强，支持最长 1k token 指令）、`wan2.7-image-pro` / `wan2.7-image`（文生图、组图、图像编辑、交互式编辑，Pro 支持 4K）。
- **视频生成**：万相 2.7（t2v/i2v/r2v/videoedit）、HappyHorse 1.0/1.1（有声视频，3~15 秒、720P/1080P）、爱诗 PixVerse V6/C1（文生/图生/首尾帧/参考生视频）、Vidu ViduQ2/Q3 系列、Tripo 3D 生成等。
- **全模态与音视频**：`qwen3.5-omni-plus` / `qwen3.5-omni-flash`（113 种语言识别、36 种语言音频生成，3 小时音频/1 小时视频输入）、`qwen3.5-livetranslate-flash-realtime`（多语言音视频实时翻译）、`fun-asr`（方言、30 语种、古诗词优化）、`fun-music-v1`（音乐生成）。

模型下线规则与清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。第三方直供模型（如 `vanchin/`、`stepfun/`、`xiaomi/`、`ZHIPU/` 前缀）与阿里直供同名模型（如 `deepseek-v4-pro`）在[计费](../concepts/billing.md)、可用区与稳定性策略上可能不同，选型时请以控制台模型市场为准。

## 平台功能更新

[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 按月发布功能动态，覆盖模型调优、部署、评测、API、应用、SDK、观测等模块。重点能力如下。

### 模型调优与部署

- 模型调优支持文本生成、视觉理解（VL）、图像生成（Wan/Wanx）、视频生成（万相）等多种模型类型；新增 0 代码安全合规强化训练流程、强化学习训练（RL，邀约制）。
- SFT 支持全参微调与 LoRA 高效微调；DPO 偏好训练覆盖千问 3-32B/14B/8B、千问 2.5-72B/32B/14B/8B。
- 模型部署新增按模型单元（MU）时长[计费](../concepts/billing.md)与按调用量计费两种方式，预置 `qwen-flash`/`qwen-plus` 等模型可一键部署；模型压缩模块上线，使用量化算法将全精度微调模型转为低精度版本以降低部署成本。
- 模型导入功能国际站上线（OSS 导入 LoRA 微调模型），并新增模型导入 API 目录。

### 模型 API 与应用调用

- 文本生成 API 入口聚合 OpenAI Responses 与 Anthropic Messages 两类兼容接口；Responses API 新增异步调用（`background=true` 提交长耗时任务并轮询）。
- 异步任务支持事件总线 EventBridge HTTP 回调与 RocketMQ 主动推送，无需轮询。
- 新版智能体应用 DashScope API 首发，支持单轮/多轮、流式、文件问答、视觉理解。
- 应用组件新增 Prompt 工程 API、数据连接 `ListCategory` / `ChangeParseSetting` 接口；知识库 Retrieve 接口新增排序模型选项与指令干预模式。
- 新增生成临时 API Key 文档，用于不可信环境下避免永久 API Key 泄露。

### 应用与 SDK

- [多模态](../concepts/multimodal.md)交互开发套件陆续上线服务端 Java SDK、移动端 Android SDK、Android/iOS Lite SDK、Linux C++ SDK、RTOS C SDK（含 License 模式）。
- 通义听悟 Agent 新增工业生产指令转写 WebSocket 协议与特惠 ASR 资源包。
- 通义[多模态](../concepts/multimodal.md)翻译 API 与网页翻译 JSSDK 上线，覆盖文本/图片/文档/网页翻译。
- UI 设计器上线（集成魔笔低代码，可视化拖放构建网页 UI）；记忆库 Memory 2.0 上线（自动提取记忆片段与用户画像，多应用共享）；联网检索 Agent 官方应用上线；官方 MCP 服务上线；Spring AI Alibaba 调用百炼应用文档上线。

### 评测与观测

- 模型评测新增排行榜（Leaderboard）与综合评测，支持 BLEU_4、ROUGE 等评分方法；新增多种评估器（字符串匹配、文本相似度、模型分类、模型打分、人工分类）。
- 模型观测支持查看推理日志、告警与通知、高级监控模式（分钟级低延时刷新、4xx/5xx 失败细分）。
- 知识库 RAG 新增日志与监控，检索调用全量投递至 SLS 日志服务。
- 模型用量新增免费额度与用量统计看板。

## 计费调整

近一年计费调整主要方向为降价与转计费：

- `qwen-max` 输入价格降低 88%、输出价格降低 84%（实时调用输入 0.0024 元/千 Token，输出 0.0096 元/千 Token）。
- `qwen2.5-14b-instruct` / `qwen2.5-7b-instruct` 降价 50%；`qwen2.5-3b-instruct`、`qwen-vl-72b-instruct` 由免费体验转为计费。
- 千问 VL 系列模型降价，降幅最高 85%。
- DeepSeek 系列部分模型由免费体验转为计费；`deepseek-v4-pro` 的 `cached_token` 单价调整为 1 元/百万 token，标准 `input_token` 单价不变。
- 上下文缓存（Context Cache）降价通知发布；当前支持 `qwen-plus` 等模型。

> **注意**：免费额度有效期与新人免费额度策略存在调整，启用「免费额度用完即停」后额度耗尽将返回 `AllocationQuota.FreeTierOnly` 错误；最新计费请以百炼控制台模型市场为准。

## 关键参数与限制

- **上下文长度**：`qwen3.5-ocr` 128K；`glm-5.1` 200K，最大输出 128K Token；全模态 `qwen3.5-omni` 可处理 3 小时音频 / 1 小时视频输入。
- **思考模式**：`qwen3.7-max`、`qwen3.6-max-preview` 默认开启思考模式；`kimi/kimi-k2.7-code` 仅支持思考模式；`qwen3.7-max-preview` / `qwen3.7-max-2026-05-17` 仅支持思考模式且仅纯文本。
- **[多模态](../concepts/multimodal.md)限制**：`qwen3.6-max-preview`、`qwen3.7-max-preview` / `qwen3.7-max-2026-05-17` 不支持图像与视频输入。
- **视频生成规格**：HappyHorse 1.1 支持 3~15 秒、720P/1080P 有声视频；万相 2.7 文生视频支持分辨率档位与宽高比自定义。
- **部署计费**：模型单元（MU）部署提供可调性能、固定成本、高稳定性；按调用量计费支持部署 qwen2.5-7B/14B/32B/72B、qwen2-7B 调优后模型。

> **注意**：模型规格名带日期快照（如 `qwen3.7-max-2026-05-20`、`qwen-image-2.0-pro-2026-06-22`）与不带日期的别名通常能力一致，快照版本用于锁定特定时间点的模型行为；不同快照间能力可能存在差异（如 `qwen3.7-max-2026-06-08` 较 5 月 20 日快照新增视觉模态）。

## 使用建议

- 选型优先参考 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中最新上架条目与控制台模型市场，避免使用已下线版本。
- 长耗时任务使用 Responses API 异步调用或异步任务 + EventBridge 回调，减少轮询开销。
- 不可信环境调用使用临时 API Key；生产环境配合模型观测的告警与高级监控进行故障定位。
- 调优后模型可通过模型压缩降低部署成本，再以模型单元或按调用量方式部署。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)



# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台级调整等关键更新，面向开发者提供可操作的版本演进信息。所有变更均以实际生效时间为准，建议通过控制台监控、API 响应头或事件总线（EventBridge）主动订阅变更通知。模型生命周期管理（含下线与替代）遵循统一机制，需特别关注通知窗口与兼容性过渡期。

## 支持的模型/功能

- **新模型上架**：2026年7月起密集发布多模态与垂直场景模型，包括 `qwen3.8-omni-flash-realtime`（实时全模态）、`decision-model-preview`（结构化决策）、`qwen-mt-uni`（全模态翻译）、`happyoyster-1.0-adventure`（世界模型）等；图像生成类新增 `qwen-image-3.0-pro` 与 `vidu/viduq3-drama_reference2video`；语音方向上线 `qwen-audio-3.0-realtime-plus` 与 `qwen-audio-3.0-tts-plus` 等差异化版本。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块升级**：
  - 知识库 RAG 新增「知识检索服务」与「知识问答服务」（2026年6月23日），支持多知识库联合检索与混合排序；
  - 智能体托管运行时 API 上线（2026年6月29日），提供会话与工具执行的平台级托管能力；
  - 模型评测新增排行榜（Leaderboard）与多种评估器（字符串匹配、模型打分、人工分类等），覆盖 BLEU_4、ROUGE 等指标（2025年12月15日 & 2026年6月9日）；
  - 数据连接模块上线（2026年6月10日），支持 MySQL/语雀/OSS 等数据源接入；
  - Responses API 新增[异步调用](../concepts/asynchronous-invocation.md)模式（`background=true`），适用于长耗时任务（2026年6月1日）。

> **注意**：文档2中“2025年11月6日 模型观测 支持查看模型推理日志”条目内容不完整（原文截断为“支持查”），其功能细节与可用性请以[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)最新版为准。

## 关键参数

- **模型标识规范**：
  - 快照模型（如 `qwen-max-2025-01-25`、`qwen3.8-max-2026-09-02`）带日期后缀，适用短期稳定需求；
  - 主线模型（如 `qwen3.8-max`、`glm-5.3`）代表系列核心版本，持续迭代但无固定日期标识。
- **上下文与输出限制**：
  - 多数旗舰模型（`qwen3.8-max`、`stepfun/step-5-preview`、`ZHIPU/GLM-5.3`）支持 **1M [Token](../concepts/token.md) 输入上下文**；
  - 输出长度上限因模型而异：`qwen3.8-flash` 支持 128K，`deepseek-v4.1-flash` 支持 384K；
  - 视频生成类模型（如 `wan3.0-video-prime`）最长支持 **30秒视频生成**。
- **计费与部署单元**：
  - 模型部署新增按「模型单元（MU）时长」计费模式（2026年1月23日），适用于 `qwen-flash`/`qwen-plus` 等预置模型；
  - PTU 部署支持长输入与前缀缓存（2026年6月15日），影响吞吐与延迟表现。

## 使用方式

- **模型切换与迁移**：
  - 下线模型用户需在通知期（快照模型30天，主线模型3个月）内完成替代模型测试与切换，参考 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 中的「操作建议」；
  - 新模型可通过控制台「模型广场」或 API `ListModels` 接口获取，ID 格式统一为 `<provider>/<model-id>`（如 `ZHIPU/GLM-5.3`）。
- **功能调用**：
  - 新增服务（如知识检索、智能体托管）需调用对应模块独立 API，路径见各功能详情链接（如 `rag-knowledge-retrieval.md`）；
  - 异步任务推荐使用事件总线（EventBridge）HTTP 回调或 RocketMQ 推送，避免轮询（2026年4月23日）；
  - 临时 API Key 生成用于不可信环境，降低密钥泄露风险（2026年6月3日）。

## 限制和注意事项

- **模型下线影响**：
  - 自下线通知发布日起，QPM/TPM 将逐步缩减至默认限流值（参见 [默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)），但接口仍可用；
  - 正式下线后，**已创建的应用将无法返回推理结果**，且禁止新建调优/部署任务（部分模型调优功能可能延续至下线后，以下线通知为准）；
  - 控制台功能（模型广场、体验中心）与官方文档同步下线，不再维护。
- **兼容性风险**：
  - `qwen-turbo` 资源包已启动退市（2026年6月28日），存量资源包到期后不可续购；
  - 企业知识库（旧）已于2026年7月16日下线，需迁移至新版知识库 RAG 服务；
  - `qwen-audio-3.0-asr-flash-*` 系列模型（2026年7月30日）取代旧版 ASR 模型，旧 ID（如 `qwen-audio-2.x`）不再接受新请求。
- **地域与协议**：
  - 新增美国、德国、日本地域接入（2026年6月12日），需显式指定 `region_id`；
  - Qwen3.8-Flash 等新模型兼容 OpenAI Responses 与 Anthropic Messages 接口分类（2026年5月15日），但部分高级能力（如 Function Calling）需启用对应 flag。

> **注意**：文档1与文档3对“快照模型”的定义存在表述差异——文档1强调“模型名称带有具体日期标识”，而文档3中 `qwen3.8-max-0902` 被明确标注为快照版本，但其别名 `qwen3.8-max-2026-09-02` 才符合日期格式。实践中请以模型 ID 是否含标准日期后缀（`YYYY-MM-DD`）为唯一判断依据，避免依赖别名。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)



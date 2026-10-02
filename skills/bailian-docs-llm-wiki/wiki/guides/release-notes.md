# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可落地的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。本文档不包含营销性描述，仅聚焦技术影响面与接入注意事项。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：  
  - 多模态旗舰：`qwen3.8-omni-flash`（全模态输入/输出）、`stepfun/step-5-preview`（1M上下文+MoE架构）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s推理速度）；  
  - 实时交互：`qwen-audio-3.1-realtime-plus`（双工语音+8系统音色）、`qwen3.8-omni-flash-realtime`（WebSocket/WebRTC/AOQ接入）；  
  - 专业场景：`qwen-mt-uni`（跨模态文档翻译）、`happyoyster-1.0-adventure`（开放式世界模型）、`decision-model-preview`（结构化决策）。  
  完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

- **平台功能升级**：  
  - 2026年6月起，知识库RAG新增「联合检索与混合排序」及「知识问答服务」；  
  - 2026年6月上线「智能体托管运行时API」，支持平台托管会话与工具执行；  
  - 2026年5月起，模型调优支持图像生成、视频生成、视觉理解（VL）三类新模型类型；  
  - 2026年4月起，多模态交互开发套件覆盖 Android/iOS Lite SDK、Linux C++ SDK 及 RTOS C SDK。

> **注意**：文档2中 `kimi/kimi-k3` 出现两次（2026-07-17 和 2026-08-19），但参数描述一致（2.8万亿参数、100万上下文），属重复录入；文档3中 `qwen3.7-max-2026-06-08` 在文档2中被列为快照模型，而文档1定义快照模型需含日期标识（如 `qwen-max-2025-01-25`），此处命名规范不一致，建议以控制台显示ID为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`stepfun/step-5-preview`）统一支持 **1M [Token](../concepts/token.md)** 上下文；  
- **输出长度**：`deepseek-v4.1-flash` 支持 384K 输出，`ZHIPU/GLM-5.3-FlashX` 支持 128K 输出；  
- **多模态能力**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持图像/视频/文件输入；  
- **推理性能**：`GLM-5.2-Fast-Preview` 输出 TPS 较标准版提升 1.5–2 倍；`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别；  
- **部署粒度**：自2026年1月起，模型部署API支持按「模型单元（MU）时长」计费，详见 [模型部署快速入门](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

## 使用方式

- **模型调用**：  
  - 新增模型默认兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/messages`）协议；  
  - 实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket 协议，参考 [实时语音对话接入文档](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-audio-realtime.md)；  
  - 多模态翻译模型（如 `qwen-mt-uni`）支持同步/异步两种调用方式，异步任务结果通过事件总线 HTTP 回调或 RocketMQ 主动推送（无需轮询）。

- **平台功能接入**：  
  - 知识库RAG服务需调用 `/v1/knowledge_base/retrieve`（检索）与 `/v1/knowledge_base/qa`（问答）接口；  
  - 智能体托管运行时 API 文档位于 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)；  
  - 模型导入支持从 OSS 导入 LoRA 微调模型，API 文档见 [模型导入 API](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。

## 限制和注意事项

- **模型下线机制**：  
  - 快照模型（含日期标识）下线前 **30天** 通知，主线模型下线前 **3个月** 通知；  
  - 自通知发布日起逐步缩减 QPM/TPM，正式下线后：① 推理服务完全不可用；② 新建调优/部署禁止；③ 控制台功能与文档同步移除；  
  - 已部署/训练的模型不受影响，但无法再发起新调优任务。详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

- **功能兼容性**：  
  - 2026年7月16日「企业知识库（旧）」已下线，存量用户需迁移至新版知识库；  
  - `qwen-turbo` 资源包已于2026年6月28日启动退市，不再接受新购；  
  - 2026年6月12日起，美国、德国、日本地域开放服务，但部分模型（如 `vidu/viduq3-*`）暂未在国际站全量部署，调用前需确认地域支持。

- **其他重要约束**：  
  - 短信/邮件/站内信通知仅触达近3个月有调用记录的用户；  
  - 异步任务回调需自行配置事件总线目标（HTTP Endpoint 或 RocketMQ Topic）；  
  - 使用临时 API Key 时，有效期最长为24小时，适用于不可信环境（如前端直连），详见 [获取临时认证令牌](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效时间为准，建议通过控制台通知中心、API 响应头（如 `X-Bailian-Release-Date`）及文档更新时间戳交叉验证。模型生命周期管理遵循统一的下线机制，新功能上线与旧功能淘汰同步推进。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：  
  - 多模态旗舰：`qwen3.8-omni-flash`（全模态输入/输出）、`stepfun/step-5-preview`（1M上下文+MoE架构）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s推理速度）；  
  - 实时交互：`qwen-audio-3.1-realtime-plus`（双工语音+8系统音色）、`qwen3.8-omni-flash-realtime`（WebSocket/WebRTC/AOQ接入）；  
  - 专业场景：`qwen-mt-uni`（跨模态翻译，支持PDF/Word/PPT等文件输入）、`happyoyster-1.0-adventure`（开放式世界模型）。  
  详细列表见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

- **平台功能扩展**：  
  - 2026年6月起，知识库RAG模块上线联合检索与混合排序（`rag-knowledge-retrieval`）、知识问答服务（`rag-knowledge-qa`）；  
  - 2026年5月起，模型调优支持强化学习（RL，邀约制）、视频生成模型（万相系列）及视觉理解（VL）模型类型；  
  - 2026年8月起，平台新增模型升级通知机制，用户可通过控制台实时感知模型能力变更。

> **注意**：文档2中 `kimi/kimi-k3` 出现两次（2026-08-19 和 2026-07-17），但参数描述完全一致（2.8万亿参数、100万token上下文），属重复条目；实际以首次发布日期（2026-07-17）为准，后续条目为冗余记录。

## 关键参数

- **模型上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`stepfun/step-5-preview`）统一支持 **1M [Token](../concepts/token.md)** 上下文，部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 128K；  
- **输出长度**：`deepseek-v4.1-flash` 支持 384K 输出，`ZHIPU/GLM-5.3-FlashX` 支持 128K 输出；  
- **多模态能力**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持图像/视频/文件输入；  
- **推理性能**：`GLM-5.2-Fast-Preview` 输出 TPS 较标准版提升 1.5–2 倍，`qwen-audio-3.0-tts-flash` 专为低延迟实时合成优化。

## 使用方式

- **模型调用**：  
  - 新增模型直接通过标准 API 接口调用（如 `/v1/chat/completions`），兼容 OpenAI 与 Anthropic 协议；  
  - 多模态输入需按 `multipart/form-data` 格式提交文本 + 文件（参考 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中各模型的“功能说明”字段）；  
  - 实时语音类模型（如 `qwen-audio-3.0-realtime-flash`）必须使用 WebSocket 协议，详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 2026年7月14日条目。

- **平台功能集成**：  
  - 知识库RAG服务通过 `POST /v1/knowledge/retrieve` 和 `POST /v1/knowledge/qa` 调用；  
  - 智能体托管运行时（Managed Agent）需调用专属 API（见 `raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md`）；  
  - 异步任务支持 HTTP 回调或 RocketMQ 推送（2026年4月23日上线），避免轮询。

## 限制和注意事项

- **模型下线规则**：  
  - 快照模型（含日期标识，如 `qwen-max-2025-01-25`）下线前 **30天** 通知，主线模型下线前 **3个月** 通知；  
  - 下线通知仅触达近3个月有调用记录的用户（短信/邮件/站内信），官网公告为唯一权威来源；  
  - 自通知发布日起逐步限流（QPM/TPM缩减），正式下线后推理、新调优/部署全部终止——已部署模型不受影响。详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

- **功能弃用与迁移**：  
  - 2026年7月16日，**企业知识库（旧）正式下线**，需迁移至新版知识库RAG服务；  
  - 2026年6月28日，`qwen-turbo` 资源包启动退市，存量资源包到期后不可续购；  
  - 2026年7月13日网关变更后，旧版 API 域名（`dashscope.aliyuncs.com`）将逐步停用，须切换至业务空间专属域名（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 6月29日条目）。

- **其他重要约束**：  
  - 模型调优的 RL 训练当前为邀约制，未开放自助申请；  
  - `qwen-mt-uni` 的异步调用模式仅支持文件类输入（PDF/Word等），文本直传不触发异步流程；  
  - `qwen3.8-omni-flash-realtime` 不支持 Function Calling，需改用 `qwen3.8-omni-flash`。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



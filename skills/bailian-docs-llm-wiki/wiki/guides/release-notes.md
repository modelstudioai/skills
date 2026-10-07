# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。模型生命周期管理（含下线与上架）与平台能力更新遵循独立但协同的节奏，需分别关注。

## 支持的模型/功能

- **新模型上线**：2026年9月起密集发布多模态与垂直场景模型，包括 `qwen3.8-omni-flash-realtime`（实时全模态）、`decision-model-preview`（结构化决策）、`qwen-mt-uni`（多模态翻译）、`happyoyster-1.0-adventure`（世界模型）等；图像生成类新增 `qwen-image-2.1-pro`，视频生成类新增 `kling/kling-v3-turbo-video-generation` 与 `wan3.0-video-prime`。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块扩展**：2026年6月起全面增强 RAG 能力，上线知识检索服务、知识问答服务；7月上线 Managed Agent 商业化支持；8月新增模型升级通知机制；9月起支持多模态输入统一处理（如 `qwen3.8-omni-flash` 同时接受文本、图片、音频、视频）。
- **SDK 与接入工具**：已支持 Linux C++、Android/iOS Lite、RTOS C 等多端 SDK；2026年6月新增 Codex 客户端接入；Spring AI Alibaba 集成文档已上线，覆盖智能体与工作流调用。

> **注意**：文档2中多次出现 `kimi-k3`（2026-09-17）与 `kimi/kimi-k3`（2026-07-17）两个条目，模型ID格式不一致（带斜杠 vs 不带），且发布时间不同。实际调用应以控制台模型列表或 API 返回的 `model_id` 字段为准，避免硬编码路径。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`stepfun/step-5-preview`、`glm-5.3`）均支持 **1M [Token](../concepts/token.md)** 上下文；部分 Flash 类模型（如 `qwen3.8-flash`）在保持该能力的同时优化吞吐。
- **输出长度**：`ZHIPU/GLM-5.3-Flash` 支持 128K 输出，`deepseek-v4.1-flash` 支持 384K 输出，`qwen3.8-2.4t-a95b` 支持 100 万 [Token](../concepts/token.md) 上下文与高精度长输出。
- **多模态能力**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持图像/视频/文件输入；`qwen3.7-text-embedding-flash` 支持 128K 长文本与 Sparse Embedding。
- **性能指标**：`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别；`qwen-audio-3.0-tts-flash` 专为低延迟交互优化；`deepseek-v4-flash-0731` 推理速度达 180–260 tokens/s。

## 使用方式

- **模型调用**：所有新模型均兼容 OpenAI Messages API 与 Anthropic Messages 协议（见 [模型 - API](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 2026年5月15日更新）；异步任务可通过 `background=true` 参数提交，并支持 EventBridge HTTP 回调或 RocketMQ 主动推送（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **部署与调优**：预置模型（如 `qwen-flash`）支持 API 直接部署；模型调优已覆盖文本生成、视觉理解（VL）、图像生成（Wan/Wanx）、视频生成（Wan）四类模型类型（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 2026年1月与5月条目）。
- **配套服务**：知识库 RAG 可通过 `/v1/rag/retrieve` 与 `/v1/rag/qa` 接口调用；记忆库 Memory 2.0 支持跨应用共享；多模态翻译 `qwen-mt-uni` 同时支持同步与异步调用。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）提前30天下线通知，主线模型提前3个月通知；通知仅触达近3个月有调用记录的用户。下线后，API 推理立即失效，新调优与新部署禁止，但已部署模型不受影响。详情请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **地域与接入限制**：2026年6月12日起新增美国、德国、日本地域支持，但部分模型（如 `qwen-audio-*` 系列）当前仅限中国内地（华北2）调用，国际站需确认模型可用性。
- **功能兼容性**：企业知识库（旧）已于2026年7月16日下线，须迁移至新版知识库；`qwen-turbo` 资源包于2026年6月28日启动退市；`fun-asr-flash-2026-06-15` 等 ASR 模型虽支持30语种，但古诗词识别仅限中文，非中文语种无此优化。
- **计费变更**：上下文缓存、GLM-5.2 Fast mode 等服务已降价（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 公告列表）；[Token](../concepts/token.md) Plan 团队版自2026年5月8日起支持 SSO/钉钉登录与席位用量监控。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



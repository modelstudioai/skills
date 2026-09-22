# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。本文档不包含营销性描述，仅聚焦技术影响与接入要点。

## 支持的模型/功能

- **新增模型（2026年8月起）**：`stepfun/step-5-preview`（1M上下文、稀疏MoE）、`qwen3.8-omni-flash-realtime`（实时音视频+WebSocket/WebRTC）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s推理速度）、`deepseek-v4.1-flash`（552B MoE，KV Cache压缩至HBM 1/4）、`kimi-k3`（2.8T参数，开源3T级模型）等，详见[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **新增能力模块**：2026年6月上线智能体托管运行时 API（[了解详情](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；2026年6月23日上线知识检索与知识问答双服务（[了解详情](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)）；2026年5月31日开放强化学习（RL）训练（邀约制）。
- **多模态专项支持**：2026年7月起，`qwen3.7-flash`、`qwen3.8-flash` 等系列全面强化视觉理解与Agent执行能力；`qwen-mt-uni` 支持文档/PDF/图片/音频混合输入的端到端翻译；`vidu/viduq3-ad_reference2video` 提供广告级切镜与直出音效。

> **注意**：文档2中 `kimi/kimi-k3` 出现两次（2026-07-17 和 2026-09-17），但模型ID、参数量、上下文窗口等核心描述完全一致，属重复录入，以首次发布日期（2026-07-17）为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`kimi-k3`）统一支持 **1,000,000 [Token](../concepts/token.md)**；部分轻量模型（如 `qwen-audio-3.1-realtime-plus`）为 262,144 [Token](../concepts/token.md)。
- **输出长度**：`GLM-5.3-FlashX` / `deepseek-v4.1-flash` 支持 **128K–384K 输出**；`qwen3.8-2.4t-a95b` 在 GPQA Diamond 等基准达 92.6 分。
- **推理性能**：`GLM-5.2-Fast-Preview` TPS 较标准版提升 1.5–2 倍；`deepseek-v4-flash-0731` 输出速度约 180–260 tokens/s；`qwen-audio-3.0-tts-flash` 专为低延迟交互优化。
- **多模态输入**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持文本/图像/音频/视频混合输入。

## 使用方式

- **模型调用**：所有新模型均兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/messages`）协议；实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket 或 WebRTC 接入。
- **功能启用**：
  - 新增 Responses API 异步调用：在请求参数中添加 `background=true`，轮询 `/v1/async/{task_id}` 获取结果（2026年6月1日上线）；
  - 智能体托管运行时：通过 `POST /v1/agents/{agent_id}/runs` 启动托管会话（2026年6月29日上线）；
  - 多模态翻译：同步调用 `/api/v1/multimodal/translate`，异步任务返回 `task_id`（2026年5月26日上线）。
- **部署与调优**：预置模型（如 `qwen-flash`）支持 API 直接部署（2026年1月23日）；模型调优已覆盖文本生成、视觉理解（VL）、图像生成、视频生成四类模型（2026年1月22日、5月28日、5月21日）。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）下线前 **30天** 通知，主线模型（如 `qwen3.8-max`）下线前 **3个月** 通知；通知后逐步限流，正式下线后推理、调优、部署全部停止（[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与接入限制**：2026年6月12日新增美国、德国、日本地域支持，但部分模型（如 `happyoyster-1.0-adventure`）当前仅限华北2（北京）可用。
- **功能兼容性**：
  - 企业知识库（旧）已于 2026年7月16日下线，需迁移至新版知识库（[了解详情](../../raw/model-user-guide/release-notes/model-release-notes.md)）；
  - `qwen-turbo` 资源包于 2026年6月28日启动退市，存量资源包到期后不可续购；
  - 部分老旧长尾模型（如 `qwen-turbo` 衍生型号）已在 2026年7月9日下线（[部分老旧长尾模型下线通知](https://www.aliyun.com/notice/118427)）。
- > **注意**：文档3中“2026年6月12日新增美国、德国、日本地域”与文档2中所有新模型发布记录均未注明地域限制，但文档3明确指出“新增地域与部署范围”，因此默认新模型**不自动全球可用**，需确认模型详情页的「支持地域」字段。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



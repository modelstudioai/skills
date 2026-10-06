# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台通知中心与[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)页面主动跟踪影响范围。本文档不包含营销性描述，仅聚焦技术可用性、接口兼容性与迁移路径。

## 支持的模型/功能

- **新增模型（2026年7–10月）**：涵盖多模态理解与生成、实时语音交互、决策推理、世界建模等方向，例如 `qwen3.8-omni-flash-realtime`（实时全模态）、`decision-model-preview`（结构化决策）、`happyoyster-1.0-adventure`（开放式世界模型）、`qwen-mt-uni`（多模态翻译）。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块上线**：包括知识检索服务、知识问答服务、智能体托管运行时 API、多模态交互开发套件（Android/iOS/Linux C++/RTOS SDK）、[Prompt 工程](../concepts/prompt.md) API、记忆库 Memory 2.0、Managed Agent 商业化支持等。
- **模型调优能力扩展**：自2026年1月起支持视频生成（万相系列）、视觉理解（VL）、图像生成（Wan/Wanx）三类新模型类型；5月新增强化学习（RL）训练（邀约制）与 0 代码安全合规强化流程。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`stepfun/step-5-preview`、`kimi-k3`）统一支持 **1M [Token](../concepts/token.md)** 上下文；部分 Flash 系列模型（如 `qwen3.8-flash`）在保持该能力的同时优化吞吐与延迟。
- **输出长度**：`ZHIPU/GLM-5.3-Flash` 支持 128K 输出，`deepseek-v4.1-flash` 支持 384K 输出，`qwen3.8-2.4t-a95b` 支持 100 万 [Token](../concepts/token.md) 上下文与高激活参数密度。
- **多模态输入支持**：`qwen3.8-omni-flash`、`GLM-5.3-FlashX`、`deepseek-v4.1-flash` 均原生支持文本、图像、音频、视频混合输入；`qwen-mt-uni` 自动识别并处理 PDF/Word/PPT/Excel/HTML/Markdown/TXT/图片/音频等 8 类模态。
- **推理性能指标**：`glm-5.2-fast-preview` 输出 TPS 较标准版提升 1.5–2 倍；`deepseek-v4-flash-0731` 激活参数仅 13B，主打高并发轻量化场景；`qwen-audio-3.0-tts-flash` 专为低延迟实时合成优化。

> **注意**：文档2中 `kimi/kimi-k3` 出现两次（2026-09-17 和 2026-07-17），但参数描述完全一致（2.8 万亿参数、100 万 token 上下文、KDA 架构），属重复录入，以首次发布日期（2026-07-17）为准；文档2末尾 `kimi-k2.7-code` 描述截断（“思”字结尾），应为笔误，完整能力请以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中其他 kimi-k2.7 系列条目为参考。

## 使用方式

- **模型调用**：所有新模型均兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/messages`）协议；实时语音模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket 或 WebRTC 接入；异步任务（如多模态翻译、长视频生成）支持 `background=true` 参数提交并轮询结果。
- **平台功能接入**：
  - 知识检索/问答服务通过 `/v1/knowledge_retrieval` 和 `/v1/knowledge_qa` 接口调用；
  - 智能体托管运行时 API 文档位于 [raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)；
  - [Prompt 工程](../concepts/prompt.md)模块提供模板管理 API，详见 [raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)。
- **部署与调优**：预置模型（如 `qwen-flash`）可通过 API 直接部署，支持按模型单元（MU）时长计费；微调任务支持 LoRA 导入（国际站已上线）、强化学习（邀约制）及安全合规零代码强化。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）下线前 **30 天**通知，主线模型（如 `qwen3.8-max`）下线前 **3 个月**通知；通知仅触达近 3 个月有调用记录的用户。下线后，API 推理、新调优/部署立即失效，但已部署模型不受影响。详情见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **功能兼容性风险**：
  - 企业知识库（旧）已于 2026-07-16 下线，需迁移至新版知识库服务；
  - `qwen-turbo` 资源包于 2026-06-28 启动退市，存量资源包到期后不可续订；
  - 部分老旧长尾模型（2026-07-09 通知）及部分老旧模型（2026-07-10 通知）已进入下线流程，具体清单以官网公告为准。
- **地域与协议限制**：新增美国、德国、日本地域支持（2026-06-12），但部分模型（如 `qwen-audio-3.0-realtime-plus`）当前仅限华北2（北京）可用；WebSocket 接入需配置 TLS 1.2+ 与指定域名，不支持 HTTP 明文。
- **计费变更**：上下文缓存、GLM-5.2 Fast mode 等服务存在阶段性降价（参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中公告链接），但 `qwen-turbo` 资源包退市与 `qwen3-Coder-Plus` 限时优惠等活动具有明确有效期，需及时关注通知时效。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



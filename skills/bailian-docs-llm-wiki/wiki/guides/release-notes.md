# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可落地的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。本文档不包含营销性描述，仅聚焦技术可用性、接口行为与约束条件。

## 支持的模型/功能

- **新上线模型（2026年7–9月）**：包括 `qwen3.8-omni-flash-realtime`（实时全模态）、`stepfun/step-5-preview`（Agentic 旗舰基座）、`decision-model-preview`（结构化决策）、`happyoyster-1.0-adventure`（开放式世界模型）等，覆盖文本生成、视觉理解、实时语音、视频生成、多模态翻译等场景。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块新增**：2026年6月起，平台陆续上线知识检索服务、知识问答服务、智能体托管运行时 API、Skill 能力包、数据连接模块（支持 MySQL/语雀/OSS）、多模态交互开发套件（含 Android/iOS/Linux C++/RTOS SDK）等核心能力；7月起支持 Responses API 异步调用（`background=true`）、API Key 加密存储与业务空间专属域名升级。
- **模型调优扩展**：自2026年1月起支持视频生成、视觉理解（VL）、图像生成模型类型调优；5月新增强化学习（RL）训练（邀约制）与 0 代码安全合规强化流程。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`glm-5.3`、`kimi-k3`）统一支持 **1M Token** 上下文；部分 Flash 系列（如 `qwen3.8-flash`）在保持该能力的同时优化吞吐。
- **输出长度**：`deepseek-v4.1-flash` 支持最大 **384K 输出**，`ZHIPU/GLM-5.3-FlashX` 支持 **128K 输出**，`qwen-mt-uni` 支持异步调用返回文件下载链接。
- **推理性能**：`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别；`glm-5.2-fast-preview` 输出 TPS 达标准版 1.5–2 倍；`kimi-k2.7-code-highspeed` 编程场景下输出速度约 180–260 Token/s。
- **多模态输入**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 等均原生支持文本、图像、音频、视频混合输入。

## 使用方式

- **模型调用**：所有新模型均兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/messages`）协议；实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket 或 WebRTC 接入；多模态翻译模型（如 `qwen-mt-uni`）支持同步/异步两种调用模式。
- **平台功能接入**：
  - 知识库 RAG 服务通过 `/v1/knowledge_retrieval` 和 `/v1/knowledge_qa` 接口调用；
  - 智能体托管运行时 API 文档见 [raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)；
  - 数据连接模块配置需通过控制台「数据连接」入口或调用 `ListCategory` / `ChangeParseSetting` 等 API。
- **模型部署与调优**：预置模型（如 `qwen-flash`）可通过 API 直接部署，支持按模型单元（MU）时长计费；微调任务需指定模型类型（`text-generation` / `image-generation` / `video-generation` / `vl`），并遵循对应文档指引。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）下线前 **30天** 发布通知，主线模型（如 `qwen3.8-max`）提前 **3个月** 通知；通知仅触达近3个月有调用记录的用户。下线后，模型推理、新调优/新部署立即停止，但已部署实例不受影响。详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- > **注意**：文档2中列出的 `kimi/kimi-k3`（2026-07-17）与 `kimi-k3`（2026-08-19）为同一模型，但文档2未明确其是否为快照或主线版本，而文档1规定快照模型必须带日期标识。此处存在表述模糊，建议以控制台模型详情页标注为准，避免误判下线周期。
- > **注意**：文档3中“6月12日 新增美国、德国、日本地域”与文档2中“2026-09-21 `stepfun/step-5-preview` 华北2（北京）上架”存在地域覆盖矛盾——新模型未必默认全地域可用。实际调用前请确认目标 Region 是否已开放该模型，参考 [raw/model-user-guide/get-started-with-models/regions.md](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **功能兼容性**：企业知识库（旧）已于2026年7月16日下线，迁移至新版知识库需适配新 API；`qwen-turbo` 资源包已于6月28日启动退市，存量资源包到期后不可续购；Managed Agent 自7月16日起进入商业化阶段，免费额度不再覆盖其运行时调用。
- **限流策略**：待下线模型自通知发布日起逐步缩减 QPM/TPM，先恢复至[默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)再递减；新模型上线初期可能受灰度流量控制，建议通过 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 观察实际 QPM。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



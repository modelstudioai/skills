# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台级更新等关键信息，面向开发者提供可操作的版本演进视图。内容涵盖新增模型能力、API 行为变更、计费与限流策略调整，以及已知约束。所有变更均以实际生效日期为准，建议通过控制台监控与文档联动验证兼容性。

## 支持的模型/功能

- **新模型上架**：2026年7月起密集发布多模态与垂直场景模型，包括 `qwen3.8-omni-flash`（全模态输入/文本输出）、`qwen-audio-3.0-realtime-plus`（实时双工语音）、`qwen-mt-uni`（跨模态统一翻译）、`decision-model-preview`（结构化决策）等；图像生成类新增 `qwen-image-3.0-pro` 与 `viduq3-drama_reference2video`；视频生成类覆盖 `wan3.0-video-prime`、`pixverse/pixverse-motioncontrol` 等细分能力模型。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块扩展**：
  - 2026年6月上线知识检索服务与知识问答服务，支持多知识库联合检索与混合排序；
  - 2026年6月新增 Skill 能力包，支持智能体添加官方或自定义技能；
  - 2026年5月起模型调优支持图像生成、视觉理解、视频生成三类新模型类型；
  - 2026年3月起记忆库升级为 Memory 2.0，支持[长期记忆](../concepts/memory.md)提取与多应用共享；
  - 2026年2月上线官方 MCP 服务，支持平台内集成与第三方接入（如 Amap Maps）。

> **注意**：文档2中“2026年6月29日”条目提及“智能体托管运行时上线”，但其链接指向 `raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md`；而文档3未提及相关托管能力变更。开发者应以该 API 文档为准，而非仅依赖功能列表日期。

## 关键参数

- **上下文窗口**：主流旗舰模型（如 `qwen3.8-max`、`stepfun/step-5-preview`、`glm-5.3`）均支持 **1M [Token](../concepts/token.md)** 上下文；部分 Flash 类模型（如 `qwen3.8-flash`）在保持同等能力下优化吞吐与延迟。
- **输出长度**：`GLM-5.3-FlashX` 支持 128K 输出，`deepseek-v4.1-flash` 支持 384K 输出。
- **推理性能**：`GLM-5.2-Fast-Preview` 输出 TPS 达标准版 1.5～2 倍；`kimi-k2.7-code-highspeed` 编程场景下输出速度约 180–260 [Token](../concepts/token.md)/s。
- **多模态输入支持**：`qwen3.8-omni-flash`、`ZHIPU/GLM-5.3-Flash`、`vanchin/deepseek-v4.1-flash` 等明确声明原生支持图像、视频、文件输入。

## 使用方式

- **模型调用**：文本生成类模型统一接入 OpenAI Responses / Anthropic Messages 接口分类（见文档2“2025年5月15日”条目）；异步任务可通过事件总线 HTTP 回调或 RocketMQ 主动推送完成事件，避免轮询（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **部署与调优**：PTU 部署支持长输入与前缀缓存（2026年6月15日上线）；模型导入功能国际站已支持从 OSS 导入 LoRA 微调模型（2026年6月5日）；模型压缩模块可用于量化微调模型以降低部署成本（2026年5月25日）。
- **SDK 与客户端**：多模态交互开发套件已提供 Linux C++、Android/iOS Lite、RTOS C 等 SDK；Kilo CLI 支持 [Token](../concepts/token.md) Plan/Coding Plan/按量计费三种接入方式（2026年2月22日）。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）下线前30天通知，主线模型下线前提前3个月通知；通知后逐步缩减 QPM/TPM，正式下线后推理、新调优与新部署即刻终止（[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与部署范围**：2026年6月12日起新增美国、德国、日本地域支持，需在创建资源时显式指定（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **兼容性风险**：`qwen-turbo` 资源包已于2026年6月28日启动退市；企业知识库（旧）于2026年7月16日下线，需迁移至新版知识库 RAG 服务。
- **权限与安全**：API Key 加密存储与业务空间专属推理域名已升级（2026年6月29日）；临时 API Key 生成能力上线，适用于不可信环境（2026年6月3日），推荐替代永久 Key 的直接暴露。

> **注意**：文档2中“2026年10月24日”条目截断为“模型部署 新增按模型单”，无后续说明；该条目内容不完整，实际功能请以 [模型部署快速入门](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) 为准。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)



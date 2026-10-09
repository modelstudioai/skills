# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台级调整等关键变更信息，面向开发者提供可落地的操作依据。所有变更均以实际生效时间为准，建议通过控制台监控、API 响应或文档链接及时同步最新能力与约束。变更通知遵循分级机制：核心模型/功能变更通过多通道主动推送，次要更新则集中归档于本页。

## 支持的模型/功能

- **新模型上架**：2026年7月起密集发布多模态与垂直场景模型，包括 `qwen3.8-omni-flash`（全模态输入/输出）、`qwen-audio-3.0-realtime-plus`（实时双工语音）、`qwen-mt-uni`（跨模态统一翻译）、`decision-model-preview`（结构化决策）等；图像生成新增 `qwen-image-3.0-pro` 与 `viduq3-drama_reference2video` 等专业子模型；视频生成覆盖 `wan3.0-video-prime`、`pixverse/pixverse-motioncontrol` 等细分能力模型。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块升级**：
  - 智能体托管：6月29日上线托管运行时 API，支持会话与工具执行全生命周期托管；
  - 知识库 RAG：6月23日上线知识检索与知识问答服务，支持多知识库联合检索与混合排序；
  - 模型评测：6月9日新增排行榜与综合评测能力，支持 BLEU_4 等评分方法；
  - 多模态交互：4月起陆续上线 Android/iOS Lite SDK、Linux C++ SDK 及 RTOS C SDK；
  - API 层：6月1日 Responses API 新增异步调用（`background=true`），5月11日发布新版 DashScope 智能体应用 API。
- **平台机制更新**：3月20日上线 Memory 2.0 [长期记忆](../concepts/memory.md)能力；7月16日下线“企业知识库（旧）”；7月21日启动记忆库商业化。

> **注意**：文档2中“6月12日 新增地域与部署范围”提及美国、德国、日本地域，但文档3未列出对应地域的模型可用性清单；实际调用前请确认目标地域是否已同步支持所需模型，可通过 [regions.md](../../raw/model-user-guide/get-started-with-models/regions.md) 核验。

## 关键参数

- **上下文窗口**：主流旗舰模型（如 `qwen3.8-max`、`stepfun/step-5-preview`、`glm-5.3`）统一支持 **1M [Token](../concepts/token.md)** 上下文；`qwen3.7-text-embedding-flash` 支持最长 **128K** 输入；`qwen-audio-3.1-realtime-plus` 为 **262,144 [Token](../concepts/token.md)**。
- **输出长度**：`ZHIPU/GLM-5.3-Flash` 最大输出 **128K**；`deepseek-v4.1-flash` 达 **384K**；`qwen3.8-2.4t-a95b` 未明确限制，但基准测试中支持长程任务端到端交付。
- **推理性能**：`GLM-5.2-Fast-Preview` 输出 TPS 为标准版 1.5～2 倍；`deepseek-v4-flash-0731` 推理速度约 180 [Token](../concepts/token.md)/s（中位数输入）；`qwen-audio-3.0-tts-flash` 专为低延迟实时合成优化。
- **计费单元**：1月23日起模型部署 API 新增按**模型单元（MU）时长**计费模式；6月30日团队版新增共享 Credits 弹性用量包。

## 使用方式

- **模型调用**：所有新模型均通过标准推理 API（如 `/v1/chat/completions`）接入，兼容 OpenAI 与 Anthropic 协议（见文档2中“5月15日 文本生成 API 入口聚合四类接口”）；多模态模型需按 `input` 字段规范传入 base64 或 URL；异步任务通过 `background=true` 提交并轮询，或配置事件总线 HTTP 回调（见 [异步任务支持事件总线 HTTP 回调与 RocketMQ](https://help.aliyun.com/zh/model-studio/async-task-api#f9e4c6c88c6ho)）。
- **功能启用**：新功能（如知识检索服务、[Prompt 工程](../concepts/prompt.md) API、Managed Agent 托管运行时）需在控制台开通对应权限，并参考对应文档初始化 SDK 或调用 API；例如知识检索服务需先创建知识库实例，再调用 `/v1/knowledge_retrieval` 接口。
- **模型迁移**：当模型进入下线流程时，需主动切换至替代模型。操作路径为：登录控制台 → 进入 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 筛选待下线模型 → 测试替代模型效果 → 更新应用配置。详细机制参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

## 限制和注意事项

- **模型下线时效性**：快照模型（如 `qwen-max-2025-01-25`）下线前 **30天** 发布通知，主线模型为 **3个月**；通知后即开始限流（QPM/TPM 逐步缩减），正式下线后推理、新调优/部署全部停止。已部署模型不受影响，但无法新建调优任务（[原文标题](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与模型不一致风险**：部分新模型（如 `qwen3.8-omni-flash-realtime`）仅在特定地域（如华北2）首发，国际站或新开放地域可能存在延迟；调用前务必核对 [regions.md](../../raw/model-user-guide/get-started-with-models/regions.md) 与模型文档中的地域支持声明。
- **功能兼容性边界**：
  - “企业知识库（旧）”已于7月16日下线，存量应用需迁移至新版知识库 RAG 服务；
  - `qwen-turbo` 资源包于6月28日启动退市，不再接受新购，但已购资源包仍可使用至有效期结束；
  - 记忆库 Memory 2.0（3月20日上线）与旧版记忆库不兼容，迁移需重建记忆库实例。
- **安全与合规**：5月4日上线的“0 代码安全合规强化”仅适用于文本生成模型调优，图像/视频生成模型暂不支持该能力；所有模型调用须遵守 [默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 规则，扩容申请需单独审批。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)



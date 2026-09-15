# release notes

百炼平台的 Release Notes 汇总了模型、API、功能模块及计费策略等维度的最新动态，涵盖新增模型上线、老旧模型下线、核心能力升级与关键参数变更。所有变更均面向开发者提供可编程接口支持，并同步更新控制台与文档。建议开发者定期查阅本页，并结合 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 主动评估兼容性影响。

## 支持的模型/功能

- **新增模型（2026年7–9月）**：覆盖文本生成、视觉理解、视频/图片生成、语音识别（ASR）、语音合成（TTS）、实时语音对话、多模态翻译等全模态类型。代表性模型包括 `qwen3.8-max`（2.4T MoE旗舰）、`ZHIPU/GLM-5.3`（320B原生多模态）、`kimi-k3`（2.8T开源旗舰）、`qwen-audio-3.0-asr-flash-streaming`（支持七大方言+古诗词优化）、`vidu/viduq3-ad_reference2video`（广告专用视频生成）等。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块扩展**：
  - 知识库 RAG 新增联合检索与混合排序（[知识检索服务上线](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)）、日志投递至 SLS；
  - 智能体托管运行时 API 上线，支持平台托管会话与工具执行；
  - Skill 能力包上线，支持添加官方或自定义技能；
  - 数据连接模块上线，支持 MySQL/语雀/OSS 等数据源；
  - 多模态交互开发套件提供 Java SDK（服务端）、Android/iOS Lite SDK、RTOS C SDK 及 Linux C++ SDK；
  - 通义多模态翻译 API 上线，覆盖文本/图片/文档/网页翻译。

> **注意**：文档1中“6月23日 知识库RAG”条目链接指向 `codex.md`，但实际应为 `rag-knowledge-retrieval.md` —— 此为原文笔误，正确路径以 [知识检索服务上线](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) 为准。

## 关键参数

- **[模型部署](../concepts/model-deployment.md)计费模式**：新增按模型单元（MU）时长计费，适用于 `qwen-flash`/`qwen-plus` 等预置模型，支持灵活调整性能与成本平衡（见 [模型部署-快速入门](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）。
- **异步任务机制**：Responses API 支持 `background=true` 异步提交；事件总线（EventBridge）支持 HTTP 回调与 RocketMQ 主动推送，替代轮询（见 [异步任务API](https://help.aliyun.com/zh/model-studio/async-task-api#f9e4c6c88c6ho)）。
- **上下文与输出限制**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`kimi-k3`）统一支持 **1M 上下文窗口** 与 **最高 128K–384K 输出长度**；`qwen3.8-flash` 等 Flash 系列侧重高吞吐低延迟，适合 RAG 和批量文案场景。
- **Token Plan 配额管理**：团队版新增共享 Credits 弹性用量包，支持跨坐席抵扣超额用量（见 [Token Plan 概览](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）。

## 使用方式

- **模型调用**：通过 DashScope API 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（如 `/v1/chat/completions`）调用，需指定 `model` 参数（如 `"qwen3.8-flash"`）；多模态模型需按规范构造 `messages` 中的 `image_url` 或 `audio_url` 字段。
- **[模型部署](../concepts/model-deployment.md)**：使用 PTU 部署支持长输入与前缀缓存（见 [PTU 长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)）；国际站已支持从 OSS 导入 LoRA 微调模型。
- **智能体与应用集成**：
  - 新版 DashScope 智能体 API 支持单轮/多轮、流式、文件问答、视觉理解；
  - Spring AI Alibaba 框架提供百炼智能体/工作流调用示例；
  - UI 设计器支持可视化拖放构建网页应用。
- **临时凭证**：在不可信环境推荐使用临时 API Key，避免永久密钥泄露（见 [获取临时认证令牌](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)）。

## 限制和注意事项

- **模型下线策略**：快照模型（如 `qwen-max-2025-01-25`）提前30天下线通知，主线模型提前3个月通知；下线后推理服务立即终止，已有部署/调优任务不受影响，但不可新建（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与接入限制**：新增美国、德国、日本地域部署，但部分模型（如 `qwen-audio-3.0-realtime-plus`）当前仅限中国内地可用，调用前需确认地域支持。
- **兼容性风险**：
  - `qwen-turbo` 资源包已启动退市（6月28日），不建议新购；
  - 企业知识库（旧）已于7月16日下线，需迁移至新版知识库；
  - `glm-5.2-fast-preview` 为预览版，不承诺 SLA，生产环境请使用正式版 `glm-5.2` 或 `glm-5.3`。
- **安全与合规**：模型调优新增 0 代码安全合规强化流程，但用户仍需自行确保训练数据符合《生成式人工智能服务管理暂行办法》要求。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)



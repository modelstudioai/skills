# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台级调整等关键更新，面向开发者提供可落地的版本演进信息。内容涵盖新增模型能力、API 行为变更、计费与部署模式升级、以及模型生命周期管理规则。所有变更均以实际生效日期为准，建议开发者定期查阅并及时适配。

## 支持的模型/功能

- **新模型上架**：2026年6月起密集发布多模态与垂直场景模型，包括 `qwen3.8-flash`（原生百万上下文多模态模型）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s 高速推理）、`qwen-mt-uni`（全模态翻译统一接口）、`kling/kling-v3-turbo-video-generation`（极速文生视频）等；视觉理解类新增 `qwen3.5-ocr`，语音类新增 `qwen-audio-3.0-asr-flash-streaming`（支持7大方言+30语种实时ASR）[原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块扩展**：
  - 知识库 RAG 新增「知识检索服务」与「知识问答服务」，支持多知识库联合检索与混合排序 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)；
  - 模型调优新增强化学习训练（RL）、图像/视频/视觉理解（VL）模型类型支持；
  - 智能体托管运行时 API 上线，支持平台托管会话与工具执行；
  - 多模态交互开发套件覆盖 Android/iOS Lite SDK、Linux C++ SDK、RTOS C SDK 及 JSSDK；
  - 记忆库升级至 Memory 2.0，支持[长期记忆](../concepts/memory.md)提取与多应用共享。

> **注意**：文档2中“2026年6月15日”条目提及“PTU 长输入与缓存”能力，但文档3未在对应时间点列出该能力所依赖的新模型；实际使用需以控制台模型详情页或 [PTU 长输入与缓存](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md) 文档为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`deepseek-v4.1-flash`）普遍支持 **1M Token** 输入，部分模型（如 `qwen3.8-2.4t-a95b`）明确标注支持 100 万 Token。
- **输出长度**：`GLM-5.3-FlashX` 支持 128K 输出，`deepseek-v4.1-flash` 支持 384K 输出。
- **推理性能**：`GLM-5.3-FlashX` 达 200 tokens/s；`kimi-k2.7-code-highspeed` 输出速度约 180–260 tokens/s；`qwen-audio-3.0-realtime-flash` 强调低延迟端到端响应。
- **模型单元（MU）计费**：自2026年1月起，模型部署 API 新增按模型单元时长计费模式，适用于 `qwen-flash`/`qwen-plus` 等预置模型 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 使用方式

- **API 调用**：
  - 文本生成 API 入口已聚合 OpenAI Responses 与 Anthropic Messages 接口分类；
  - Responses API 新增异步调用（`background=true`），适用于长耗时任务；
  - 新增生成临时 API Key 文档，用于不可信环境规避永久密钥泄露风险；
  - 异步任务支持通过事件总线 EventBridge 主动推送完成事件，替代轮询。
- **模型部署**：支持预置模型一键部署（含 `qwen-flash`/`qwen-plus`），亦可通过模型导入 API 导入 LoRA 微调模型（国际站已上线）。
- **模型调优**：支持文本生成、视觉理解（VL）、图像生成（Wan/Wanx）、视频生成（Wan）四类模型类型；强化学习训练当前为邀约制。
- **SDK 接入**：多模态交互开发套件提供 Android/iOS Lite、Linux C++、RTOS C、JSSDK 等多端支持；Kilo CLI 支持 Token Plan/Coding Plan/按量三种接入方式。

## 限制和注意事项

- **模型下线机制**：
  - 快照模型（如 `qwen-max-2025-01-25`）下线前 **30天** 发布通知；
  - 主线模型下线前 **3个月** 发布通知；
  - 自通知发布日起逐步缩减 QPM/TPM，正式下线后停止推理服务，且不再支持新调优与新部署（已训练/部署模型不受影响）[原文标题](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **地域与服务范围**：2026年6月12日起新增美国、德国、日本地域部署，调用需指定对应 endpoint。
- **兼容性说明**：
  - `qwen3.8-flash` 兼容 OpenAI 与 Anthropic 主流协议，但 `qwen3.8-omni-flash` 明确支持 Function Calling、联网搜索与上下文缓存，而 `qwen3.8-2.4t-a95b` 未提及其对 Function Calling 的支持，实际调用前请验证；
  - 文档2中“2026年7月16日”企业知识库（旧）下线通知与文档3无直接关联，但开发者需确认当前知识库服务是否已迁移至新版 RAG 架构。
- **免费额度**：2025年12月22日起上线免费额度与用量统计看板，集中展示各模型剩余额度及调用量，但额度有效期受 [新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment) 约束。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)



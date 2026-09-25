# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可落地的版本演进信息。所有变更均以实际生效时间为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。本文档不包含营销性描述，仅聚焦技术可用性、接口行为与约束条件。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：  
  - 多模态旗舰：`qwen3.8-omni-flash`（支持文本/图/音/视输入）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s，1M上下文）、`vanchin/deepseek-v4.1-flash`（原生多模态，384K输出）；  
  - 实时交互：`qwen-audio-3.1-realtime-plus`（双工语音+Function Calling）、`qwen3.8-omni-flash-realtime`（WebSocket/WebRTC/AOQ接入）；  
  - 专业场景：`qwen-mt-uni`（跨模态文档/图片/音频翻译）、`happyoyster-1.0-adventure`（开放式世界模型）、`decision-model-preview`（结构化决策）。  
  详细列表见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

- **平台级功能上线**：  
  - 2026年6月起，知识库RAG服务正式提供「知识检索」与「知识问答」双服务接口；  
  - 2026年6月29日，智能体托管运行时 API 上线，支持平台托管会话与工具执行；  
  - 2026年5月11日，新版智能体应用 DashScope API 首发，支持单轮/多轮、流式、文件问答与视觉理解；  
  - 2026年3月20日，[记忆](../concepts/memory.md)库 Memory 2.0 上线，支持长期[记忆](../concepts/memory.md)自动提取与多应用共享。

> **注意**：文档2中 `kimi/kimi-k3` 出现两次（2026-09-17 和 2026-07-17），但参数描述完全一致（2.8万亿参数、100万token上下文），属重复条目；文档3中未提及该模型，应以文档2中首次发布时间（2026-07-17）为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`deepseek-v4.1-flash`）统一支持 **1M [Token](../concepts/token.md)** 上下文，部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 128K；  
- **输出长度**：`deepseek-v4.1-flash` 最大输出 384K，`ZHIPU/GLM-5.3-FlashX` 为 128K，`qwen3.8-omni-flash` 未明确上限，需以实际调用响应为准；  
- **多模态能力**：`qwen3.8-omni-flash`、`GLM-5.3-FlashX`、`deepseek-v4.1-flash` 均声明“原生支持图像、视频与文件输入”，但文档2未说明是否支持音频输入——此能力在 `qwen3.8-omni-flash-realtime` 中明确列出，故非实时模型的音频输入支持需单独验证；  
- **推理性能**：`ZHIPU/GLM-5.3-FlashX` 标称 200 tokens/s，`kimi-k2.7-code-highspeed` 为 180–260 tokens/s，`qwen-audio-3.0-tts-flash` 侧重低延迟而非吞吐，具体数值未公开。

## 使用方式

- **模型调用**：所有新模型均兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/messages`）协议，无需修改客户端核心逻辑；  
- **异步任务**：Responses API 自2026年6月1日起支持 `background=true` 参数提交长耗时任务，结果通过轮询或事件总线（EventBridge HTTP回调/RocketMQ）获取；  
- **部署与调优**：  
  - 模型部署支持按模型单元（MU）时长计费（2026年1月23日上线）；  
  - 调优支持新增类型包括视觉理解（VL）、图像生成（Wan/Wanx）、视频生成（万相系列）及强化学习（RL，邀约制）；  
- **SDK接入**：多模态交互开发套件已提供 Linux C++、Android/iOS Lite、RTOS C、Java 等 SDK，详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 限制和注意事项

- **模型下线机制**：  
  - 快照模型（如 `qwen-max-2025-01-25`）下线前30天通知，主线模型（如 `qwen3.8-max`）提前3个月通知；  
  - 下线通知发布后即开始限流（QPM/TPM逐步缩减），正式下线后推理服务终止，且**不再支持新调优与新部署**（已训练/部署模型不受影响）；  
  - 具体下线清单与时间请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。  

- **地域与协议限制**：  
  - 2026年6月12日起新增美国、德国、日本地域，但部分模型（如 `qwen-mt-uni`）当前仅限华北2（北京）调用；  
  - `qwen-audio-3.1-realtime-plus` 仅支持 WebSocket/WebRTC/AOQ 接入，不兼容传统 RESTful 长连接。  

- **功能兼容性**：  
  - 企业知识库（旧）已于2026年7月16日下线，存量用户需迁移至新版知识库；  
  - `qwen-turbo` 资源包自2026年6月28日起启动退市，新购用户不可用；  
  - 文档3中「2026年7月10日部分老旧模型下线通知」与文档1中「2026年10月10日将下线」存在时间差，应以文档1的官方下线日程表为准，文档3仅为前置通告。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



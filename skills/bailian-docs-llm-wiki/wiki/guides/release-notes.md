# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可落地的操作依据。所有变更均遵循明确的时间节点与通知机制，核心模型生命周期（上架、升级、下线）和平台能力演进（API、部署、评测、RAG 等）均在此同步。开发者应定期查阅本页，并结合[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)评估服务连续性。

## 支持的模型/功能

- **新上线模型（2026年重点）**：涵盖多模态理解与生成全栈能力，包括 `qwen3.8-max`（2.4T MoE 旗舰）、`qwen-audio-3.1-realtime-flash`（实时双工语音）、`Tripo/Tripo-AutoRig`（AI 自动绑骨）、`qwen-mt-uni`（全模态翻译）、`happyoyster-1.0-adventure`（开放式世界模型）等；新增模型均支持 1M 上下文、多档思考深度及 Function Calling。
- **模型类型标识**：正式版模型提供系列名（如 `qwen-max`）、日期后缀（如 `qwen-max-2025-01-25`）和 `-latest` 别名三种形态；预览版模型 ID 含 `preview`/`beta`/`experimental` 标识或文档明确标注，更新快、可能快速下线。
- **平台级功能扩展**：
  - RAG：知识检索与问答服务（2026-06-23）、多知识库联合检索与混合排序；
  - 部署：PTU 长输入与前缀缓存（2026-06-15）、新增美国/德国/日本地域（2026-06-12）；
  - 调优：强化学习训练（邀约制，2026-05-31）、支持图像/视频/视觉理解模型微调（2026-05/01）；
  - API：Responses API 异步调用（2026-06-01）、新版 DashScope Agent API（2026-05-11）、Spring AI Alibaba 集成文档（2026-06-01）；
  - SDK：Linux C++ / Android / iOS Lite / RTOS C 多端多模态 SDK 全面覆盖（2026-02 至 04 月）。

> **注意**：文档 2 中列出的 `kimi/kimi-k3`（2026-07-17）与 `kimi-k3`（2026-08-19）参数描述存在不一致（前者称“2.8 万亿参数”，后者称“全球首个开源的 3 万亿级别模型”），实际以控制台模型详情页或 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 中发布的权威规格为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`deepseek-v4.1-flash`、`glm-5.3`）统一支持 **1,000,000 [Token](../concepts/token.md)** 输入；
- **输出长度**：`deepseek-v4.1-flash` 系列支持最大 **384K [Token](../concepts/token.md)** 输出；`GLM-5.3-FlashX` 支持 **128K**；
- **推理速度**：`qwen-audio-3.0-realtime-flash` 与 `qwen-audio-3.1-realtime-flash` 侧重低延迟双工交互；`GLM-5.3-FlashX` 达 **200 tokens/s**；`MiniMax-M3.1-Flash` 约 **170 tokens/s**；
- **架构特性**：`qwen3.8-2.4t-a95b`（2.4T MoE，激活 ~95B）、`deepseek-v4-pro-0813`（1.6T MoE，激活 49B）、`stepfun/step-5-preview`（600B MoE，激活 27B）；
- **多模态能力**：`qwen3.8-omni-flash`、`qwen3.8-omni-flash-realtime`、`xiaomi/mimo-v2.6-pro-ultraspeed` 均原生支持文本/图片/音频/视频输入。

## 使用方式

- **模型调用**：通过标准 REST API（兼容 OpenAI Anthropic 协议）或 SDK（Java/Android/iOS/C++/RTOS）接入；实时语音类模型需使用 WebSocket/WebRTC/AOQ 协议；
- **新功能启用**：
  - 异步任务：在 Responses API 请求中添加 `background=true` 参数（2026-06-01 起）；
  - 记忆库 2.0：自动提取对话记忆并支持跨应用共享（2026-03-20）；
  - 知识库检索：`Retrieve` 接口支持指定排序模型与指令干预模式（2026-02-05）；
- **资源管理**：
  - [Token](../concepts/token.md) Plan 团队版支持跨坐席共享 Credits 弹性用量包（2026-06-30）；
  - 新增生成临时 API Key 文档，用于不可信环境安全调用（2026-06-03）；
- **模型切换**：下线模型迁移需参考[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)中的替代模型建议，并在模型监控页面验证调用情况。

## 限制和注意事项

- **模型下线节奏**：
  - 正式版模型：启动下线后 **3 个月**停止服务（EoS），期间逐步缩减 QPM/TPM 并停止新购（EoM）；
  - 预览版模型：启动下线后仅 **14 天**即停止服务，无 EoM 阶段；
  - 所有下线通知均不晚于 EoS 前 3 个月（正式版）或 14 天（预览版）发布。
- **功能兼容性**：
  - `qwen-turbo` 资源包已于 2026-06-28 启动退市（见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）；
  - 企业知识库（旧）已于 2026-07-16 下线，需迁移至新版知识库；
  - 部分老旧长尾模型下线通知（2026-07-09）与部分老旧模型下线通知（2026-07-10）存在重叠，具体清单以官网公告为准。
- **关键风险提示**：
  > **注意**：文档 3 中“7月6日 部分老旧模型延期下线通知”与文档 1 中“2026年10月10日已下线”列表存在时间矛盾——文档 1 明确将 2026-10-10 列为“已下线”，而文档 3 的延期通知发生在 2026-07-06，逻辑上无法覆盖该日期。请以[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)中“下线模型列表”及对应官网公告（如 [https://www.aliyun.com/notice/118177](https://www.aliyun.com/notice/118177)）为最终依据。
- **其他限制**：预览版模型不承诺 SLA，不适用于生产环境；所有模型限流默认值参见[默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；模型压缩、RL 训练等功能当前为邀约制或受限开放。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、服务策略变更等关键更新，面向开发者提供可落地的版本演进信息。所有变更均以生产环境生效时间为准，建议通过控制台「模型监控」和「通知中心」主动订阅变更。模型生命周期管理（如上下线）与平台能力升级（如 API、部署、评测）遵循独立但协同的发布节奏。

## 支持的模型/功能

- **新增模型**：2026年9–10月集中上线多类模型，包括实时语音对话模型 `qwen-audio-3.1-realtime-flash`、3D生成全栈能力（如 `Tripo/Tripo-SmartSegmentation`、`Tripo/Tripo-AutoRig`）、多模态翻译模型 `qwen-mt-uni`、世界模型 `happyoyster-1.0-adventure` 及决策模型 `decision-model-preview`。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **模型类型覆盖**：当前支持文本生成、视觉理解、语音识别（ASR）、语音合成（TTS）、视频生成、3D生成、多模态翻译、排序（rerank）、文本向量（embedding）、决策推理、世界建模等11类任务模型。
- **平台功能扩展**：2026年6月起全面支持知识库 RAG 的联合检索与问答服务；7月上线 Managed Agent 商业化运行时；8月新增模型升级通知机制；9月起支持 WebSocket、WebRTC 和 AOQ 多协议接入实时全模态模型（如 `qwen3.8-omni-flash-realtime`）。

> **注意**：文档 2 中列出的 `qwen-audio-3.1-tts-next` 定义为“不再局限于传统 TTS 的单一语音合成”，而文档 3 的 2026年9月功能动态中未提及该模型的配套 SDK 或 API 支持，实际集成前请以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中最新 API 文档为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`MiniMax-M3.1-Flash`、`ZHIPU/GLM-5.3-FlashX`）统一支持 **1M Token** 上下文；部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 128K；语音/视频模型上下文按帧或 Token 等效折算（如 `qwen-audio-3.1-realtime-flash` 为 262,144 Token）。
- **输出长度**：`deepseek-v4.1-flash-1017`、`qwen3.8-max` 等旗舰模型最大输出达 **384K Token**；`GLM-5.3-FlashX` 为 128K；TTS/ASR 类模型以音频时长（秒）或转写文本长度为约束。
- **性能指标**：`qwen3.8-flash` 推理吞吐达约 170 tokens/s；`ZHIPU/GLM-5.3-FlashX` 达 200 tokens/s；`qwen-audio-3.1-asr-flash-streaming` 强调低延迟流式识别，端到端延迟 <300ms（典型场景）。

## 使用方式

- **模型调用**：所有正式版模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`）与 Anthropic Messages 协议；实时语音、3D、视频等专用模型需使用对应领域 API（如 `/v1/audio/realtime`、`/v1/3d/segment`），具体参见各模型文档页。
- **部署与接入**：
  - 预置模型可通过控制台一键部署，或调用 [模型部署 API](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)；
  - 自定义模型支持 OSS 导入 LoRA 微调结果（[模型导入功能国际站上线](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)）；
  - 多模态交互支持 Android/iOS/Lite/RTOS/C++/Java 全端 SDK（见文档 3 2026年2–4月条目）。
- **通知与监控**：启用模型升级/下线通知需在控制台「账号设置 > 通知偏好」中开启邮件/站内信；用量与调用日志可通过 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 实时查看。

## 限制和注意事项

- **模型生命周期**：正式版模型下线遵循「启动下线 → 停止新购（EoM）→ 停止服务（EoS）」三阶段流程，其中 EoS 不晚于启动下线后 **3 个月**；预览版模型 EoS 不晚于启动下线后 **14 天**。详情请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **兼容性风险**：`-latest` 别名（如 `qwen-max-latest`）指向最新正式版，但不保证 ABI 兼容；生产环境强烈建议使用带日期后缀的固定版本（如 `qwen-max-2025-01-25`）。
- **地域与协议限制**：2026年6月起新增美国、德国、日本地域接入，但部分模型（如 `Tripo/*`、`kling/*`）暂未在全部地域部署；WebSocket 接入仅适用于 `qwen3.8-omni-flash-realtime` 等明确标注「realtime」的模型。
- **资源包与计费**：`qwen-turbo` 资源包已于 2026年6月28日启动退市（见文档 3），存量资源包到期后不可续购；企业知识库（旧）已于 2026年7月16日下线，需迁移至新版知识库服务。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。模型生命周期管理（含下线与上架）与平台能力升级遵循独立但协同的发布节奏。

## 支持的模型/功能

- **新模型上架**：2026年7–9月集中上线[多模态](../concepts/multi-modal.md)旗舰模型，包括 `qwen3.8-max`（2.4T MoE）、`deepseek-v4.1-flash`（552B MoE）、`ZHIPU/GLM-5.3-Flash`（320B原生[多模态](../concepts/multi-modal.md)）、`kimi-k3`（2.8T开源旗舰）及 `vidu/viduq3-drama_reference2video` 等垂直场景视频模型；语音方向新增 `qwen-audio-3.0-asr-flash-streaming`（实时ASR）与 `qwen-audio-3.0-tts-plus`（高表现力TTS）。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **平台功能扩展**：2026年6月起全面支持[多模态](../concepts/multi-modal.md)交互开发套件（Linux C++/Android/iOS Lite SDK）、智能体托管运行时 API、知识检索与问答服务、Prompt 工程 API、异步 Responses API（`background=true`）、以及模型压缩模块（量化部署）。详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **模型调优能力增强**：自2026年5月起支持图像生成、视频生成、视觉理解（VL）三类模型的定制训练；2026年5月31日上线强化学习（RL）训练（邀约制），2026年5月4日新增0代码安全合规强化流程。

## 关键参数

- **模型上下文窗口**：主流新模型（如 `qwen3.8-max`、`glm-5.3`、`kimi-k3`）统一支持 **1M token** 上下文；部分 Flash 类模型（如 `qwen3.8-flash`）在保持该能力的同时优化吞吐与延迟。
- **输出长度**：`qwen3.8-max`、`ZHIPU/GLM-5.3-Flash` 等支持 **384K 最大输出 token**；`pixverse/pixverse-v6-r2v` 支持 **15秒视频生成**；`wan3.0-video-prime` 支持 **30秒视频**。
- **多模态能力**：`qwen3.8-flash`、`ZHIPU/GLM-5.3-Flash`、`kimi-k3` 均为原生多模态模型，支持图像/视频/文件输入与跨模态推理；`qwen3.7-ocr` 专精文档解析与关键信息提取。
- **语音模型参数**：`qwen-audio-3.0-asr-flash-streaming` 支持30语种+七大方言+古诗词识别；`qwen-audio-3.0-tts-plus` 提供细粒度情绪/语速/音量控制标签。

## 使用方式

- **模型调用**：通过标准 OpenAI 或 Anthropic 兼容接口（如 `/v1/chat/completions`）调用，`qwen3.8-flash` 等模型已明确声明兼容性；视频/图片/语音类模型使用专属 API 路径（如 `/v1/video/generation`）。
- **平台功能接入**：
  - 新增功能（如知识检索、Managed Agent）需调用对应 API（见 [application-api-reference](../../raw/application-api-reference/) 目录）；
  - SDK 接入参考各语言文档（如 [multimodal-sdk-android](../../raw/application-user-guide/application-gallery/multimodal-products/multimodal-sdk/multimodal-sdk-android.md)）；
  - [异步任务](../concepts/asynchronous-task.md)推荐使用 EventBridge HTTP 回调替代轮询（[异步任务支持事件总线](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **模型迁移**：快照模型（如 `qwen-max-2025-01-25`）下线前30天通知，主线模型（如 `qwen3.7-max`）提前3个月通知；切换前务必在 [模型监控](https://bailian.console.aliyun.com/model/telemetry) 中验证替代模型效果。详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

## 限制和注意事项

- > **注意**：文档2中 `kimi/kimi-k3` 与 `kimi-k3` 出现两次（2026-08-19 和 2026-07-17），但模型ID写法不一致（带斜杠 vs 不带），实际应以控制台或API返回的 `model_id` 字段为准，避免硬编码路径。
- > **注意**：文档3中“6月12日 新增地域与部署范围”注明支持美国、德国、日本，但文档2所列新模型（如 `deepseek-v4.1-flash`）未声明地域可用性；调用前需确认目标地域是否已同步上线该模型，否则将返回 `ModelNotAvailableInRegion` 错误。
- **下线影响**：自下线通知发布日起，QPM/TPM 将逐步缩减至默认限流值；正式下线后，**已创建的应用若仍调用该模型将直接失败**，且无法新建调优/部署任务（已训练部署的模型实例不受影响）。
- **功能兼容性**：`qwen-turbo` 资源包已于2026年6月28日启动退市（[qwen-turbo 资源包启动退市通知](../../raw/model-user-guide/release-notes/model-release-notes.md)），请迁移到 `qwen-flash` 或 `qwen-plus` 等现行模型。
- **计费变更**：2026年6月30日起团队版支持共享 Credits 用量包；2026年7月14日 `GLM-5.2 Fast mode` 降价；2026年8月4日上线模型升级通知机制——所有价格与配额调整均以官网公告为准。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



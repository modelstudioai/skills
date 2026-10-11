# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效时间为准，建议通过控制台通知中心、API 响应头（如 `X-Bailian-Release-Date`）及文档更新时间戳交叉验证。模型生命周期管理与平台能力升级同步推进，需特别关注下线窗口期与替代方案兼容性。

## 支持的模型/功能

- **新模型上架**：2026年9月起密集发布多模态旗舰模型，包括 `qwen3.8-omni-flash-realtime`（实时全模态）、`ZHIPU/GLM-5.3-FlashX`（1M上下文+多模态输入）、`deepseek-v4.1-flash`（原生视觉理解+384K输出）等；图像生成领域新增 `qwen-image-2.1-turbo` 和 `vidu/viduq3-ad_reference2video`（广告专用）；视频生成覆盖 `wan3.0-video-prime`（高速版）与 `pixverse/pixverse-lipsync`（精准对口型）等细分能力模型。完整清单见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **平台功能扩展**：2026年6月起全面支持多模态翻译 API（含 PDF/Word/PPT 等文档解析）、知识检索服务（多知识库联合检索）、智能体托管运行时（会话与工具执行托管）、以及 Responses API 异步调用（`background=true` 参数启用）。模型调优能力持续增强，已支持图像生成、视频生成、视觉理解（VL）三类模型的定制训练，详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **SDK 与接入工具**：新增 Codex 客户端、Spring AI Alibaba 集成文档、Linux C++ / Android/iOS Lite 多模态 SDK，并于2026年6月上线 RTOS C SDK License 模式，覆盖嵌入式半托管场景。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`glm-5.3`、`kimi-k3`）统一支持 **1M Token** 上下文；部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 **128K** 输入长度。
- **输出能力**：`qwen3.8-max` 最大输出 **384K Token**；`ZHIPU/GLM-5.3-FlashX` 支持 **128K 输出**；语音合成模型 `qwen-audio-3.0-tts-plus` 提供细粒度情绪/语速/音量控制标签。
- **性能指标**：`deepseek-v4-flash-0731` 推理延迟低至毫秒级，TPS 较前代提升 2–3 倍；`glm-5.2-fast-preview` 输出速度达标准版 **1.5–2 倍**；`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别，端到端时延 <500ms。
- **多模态支持**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持文本、图像、音频、视频混合输入；`qwen-mt-uni` 自动识别输入模态并完成版面还原与语音克隆。

## 使用方式

- **模型调用**：通过标准 REST API（兼容 OpenAI Anthropic 协议）或 DashScope SDK 调用；新模型默认启用 `thinking_mode`（深度思考）与 `function_calling`，需在请求 payload 中显式声明 `tool_choice`。
- **异步任务**：长耗时任务（如视频生成、大文件翻译）须使用 Responses API 的 `background=true` 模式提交，轮询 `/v1/tasks/{task_id}` 获取结果；事件总线（EventBridge）支持 HTTP 回调与 RocketMQ 主动推送，避免轮询开销。
- **模型迁移**：快照模型（如 `qwen-max-2025-01-25`）下线前30天、主线模型下线前3个月启动限流（QPM/TPM 逐步缩减），期间仍可正常调用；切换前务必在 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 页面验证替代模型效果，参考 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 执行灰度迁移。
- **部署与调优**：预置模型可通过 API 直接部署（支持按模型单元 MU 计费）；微调任务需指定 `model_type`（如 `image_generation`、`video_generation`），调优后模型支持量化压缩（降低 HBM/SSD 占用）。

## 限制和注意事项

- > **注意**：文档2中 `kimi/kimi-k3` 出现两次（2026-07-17 与 2026-09-17），但参数描述完全一致（2.8万亿参数、100万上下文），属重复条目，以首次发布时间（2026-07-17）为准，后续条目为冗余记录。
- > **注意**：文档2列出 `qwen3.8-2.4t-a95b`（2026-08-12）为“开源版本”，但文档3未提及该模型开源状态，且百炼平台不提供模型权重下载；实际仅开放 API 调用，非真正开源。
- **下线模型不可逆**：自正式下线日起，模型推理、新调优/新部署全部终止；已部署模型不受影响，但无法创建新实例。历史下线批次（如2025年7月30日、2024年4月22日）未发布专项公告，需依赖控制台通知与文档归档核查。
- **功能兼容性风险**：`企业知识库（旧）` 已于2026年7月16日下线，其 API（`/v1/knowledge_base/old/*`）同步失效；新知识库 RAG 服务需使用 `/v1/knowledge_base/retrieve` 等新版接口，旧集成需重构。
- **地域限制**：新增美国、德国、日本地域部署（2026-06-12），但部分模型（如 `qwen-mt-image-2.0`）暂未开放海外地域调用，调用前需确认 `region_id` 有效性。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



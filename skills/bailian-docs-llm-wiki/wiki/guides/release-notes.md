# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、API 变更及关键运营策略调整。所有变更均面向开发者设计，聚焦可用性、兼容性与可迁移性。模型生命周期管理（含上架、快照发布、下线）与平台能力演进（如[异步调用](../concepts/asynchronous-invocation.md)、托管运行时、多模态 SDK）是当前核心演进方向。

## 支持的模型/功能

- **新模型上架**：2026年7–9月密集上线多模态与垂直场景模型，包括 `qwen3.8-max`（2.4T MoE，100万上下文）、`qwen-mt-uni`（跨模态翻译）、`kling/kling-v3-turbo-video-generation`（极速视频生成）、`happyoyster-1.0-adventure`（开放式世界模型）等。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **模型类型扩展**：支持图像生成（`vidu/vidu-image-pro_reference2image`）、视频生成（`wan3.0-video-prime`）、语音实时对话（`qwen-audio-3.0-realtime-plus`）、OCR（`qwen3.5-ocr`）、文本向量（`qwen3.7-text-embedding-flash`）等全栈能力。
- **平台功能新增**：
  - [异步调用](../concepts/asynchronous-invocation.md)：Responses API 支持 `background=true` 提交长耗时任务（2026-06-01）；
  - 托管运行时：智能体托管运行时 API 上线，平台统一管理会话与工具执行（2026-06-29）；
  - 多模态 SDK：Linux C++、Android/iOS Lite、RTOS C 等多端 SDK 全面覆盖（2026-02 至 04 月）；
  - RAG 增强：知识检索服务与知识问答服务上线，支持多知识库联合检索与混合排序（2026-06-23）。

> **注意**：文档2中多次出现 `kimi/kimi-k3` 与 `kimi-k3` 两种命名（如2026-08-19与2026-07-17），但模型ID在API调用中必须使用带斜杠的规范格式 `kimi/kimi-k3`；实际调用请以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中表格列示为准。

## 关键参数

- **上下文长度**：主流旗舰模型（如 `qwen3.8-max`、`glm-5.3`、`kimi-k3`）均支持 **1,000,000 token** 上下文；部分Flash模型（如 `qwen3.7-flash`）亦原生支持百万级。
- **输出能力**：视频模型支持最长30秒生成（`wan3.0-video`）、4K超分（`pixverse/pixverse-upscale`）；语音模型区分 `realtime-plus`（高质）与 `realtime-flash`（低延迟）双版本。
- **调用协议兼容性**：`qwen3.8-flash` 等模型兼容 OpenAI Messages 与 Anthropic Messages 协议（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 2026-05-15 条目）。
- **限流基准**：模型QPM/TPM默认值参见 [默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)，下线模型将按通知节奏逐步缩减配额。

## 使用方式

- **模型调用**：通过 `/v1/chat/completions`（OpenAI兼容）或 `/v1/messages`（Anthropic兼容）等标准API入口，传入 `model` 参数（如 `"model": "qwen3.8-max"`）；
- **异步任务**：在请求中添加 `background=true`，获取 `task_id` 后轮询 `/v1/tasks/{task_id}` 或配置 EventBridge HTTP 回调（2026-04-23）；
- **模型部署**：支持预置模型一键部署（2026-01-23），计费模式新增按模型单元（MU）时长计费；
- **调优与压缩**：视觉理解、视频生成、图像生成模型均已开放调优（2026-01 至 05 月），并新增模型压缩模块降低部署成本（2026-05-25）。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）提前30天下线通知，主线模型提前3个月通知；自通知发布日起即开始限流，正式下线后推理、新调优/部署全部停止（[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与接入**：2026-06-12起新增美国、德国、日本地域部署，需在请求Header中显式指定 `X-DashScope-Region`（参见 [regions.md](../../raw/model-user-guide/get-started-with-models/regions.md)）。
- **兼容性风险**：
  - `qwen-audio-3.0-realtime-plus` 与 `qwen-audio-3.0-realtime-flash` 接口协议相同但性能目标不同，不可互换使用；
  - `qwen3.7-max-2026-05-20` 与 `qwen3.7-max-2026-06-08` 为不同快照，后者新增视觉模态能力，旧快照无此能力；
  - 文档3中提及“企业知识库（旧）下线通知”（2026-07-16），新知识库RAG服务已全面替代，旧接口将于下线日完全不可用。

> **注意**：文档2末尾存在截断（`qwen3.5-livetranslate-flash-realtime` 后内容不全），该模型完整ID及能力描述请以控制台或最新版 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 为准。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



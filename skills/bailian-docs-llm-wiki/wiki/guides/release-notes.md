# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可落地的版本演进信息。所有变更均以实际生效时间为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。本文档不包含营销性描述，仅聚焦技术可用性、接口兼容性与操作约束。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：`qwen3.8-omni-flash-realtime`（实时全模态）、`stepfun/step-5-preview`（Agentic 旗舰基座）、`qwen-mt-uni`（多模态翻译）、`happyoyster-1.0-adventure`（开放式世界模型）、`kling/kling-v3-turbo-video-generation`（极速视频生成）。完整列表见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块上线**：知识检索服务与知识问答服务（2026-06-23）、智能体托管运行时 API（2026-06-29）、Responses API 异步调用（2026-06-01）、多模态交互开发套件 Android/iOS Lite SDK（2026-02-06）。
- **模型调优能力扩展**：自 2026 年 1 月起支持视觉理解（VL）、视频生成（如 Wan 系列）、图像生成模型类型；2026 年 5 月新增强化学习（RL）训练（邀约制）和 0 代码安全合规强化流程。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`glm-5.3`、`stepfun/step-5-preview`）统一支持 **1M [Token](../concepts/token.md)** 上下文；部分 Flash 型号（如 `qwen3.8-flash`）在保持该能力的同时优化吞吐。
- **输出长度**：`deepseek-v4.1-flash` 支持最大 **384K 输出**，`ZHIPU/GLM-5.3-FlashX` 支持 **128K 输出**。
- **多模态输入**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 等均原生支持文本、图像、音频、视频混合输入。
- **推理性能**：`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别；`glm-5.2-fast-preview` 输出 TPS 较标准版提升 1.5–2 倍；`kimi-k2.7-code-highspeed` 编程场景下可达 260 [Token](../concepts/token.md)/s。

> **注意**：文档 2 中 `kimi/kimi-k3` 出现两次（2026-07-17 和 2026-08-19），但 2026-08-19 条目标注为“全球首个开源的 3 万亿级别模型”，而 2026-07-17 条目未提开源属性；实际发布状态请以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中最新条目为准。

## 使用方式

- **模型调用**：通过 `/v1/chat/completions`（OpenAI 兼容）或 `/v1/messages`（Anthropic 兼容）接口调用；多模态模型需按规范构造 `content` 数组（含 `text`/`image_url`/`audio_url` 等 type 字段）。
- **异步任务**：对长耗时请求（如视频生成、大文件翻译），使用 `background=true` 参数提交至 Responses API，并轮询 `GET /v1/async_tasks/{task_id}` 获取结果；亦可配置事件总线 HTTP 回调或 RocketMQ 主动推送（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **模型部署与调优**：预置模型可通过 API 直接部署（支持按模型单元 MU 计费）；微调任务需指定 `model_type`（如 `vl`、`video-generation`、`image-generation`），详见各模型类型调优指南。
- **通知订阅**：短信/邮件/站内信仅推送给近 3 个月有对应模型调用记录的用户；官网公告为全量覆盖渠道。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）下线前 **30 天**通知，主线模型下线前 **3 个月**通知；下线后已创建的应用将无法返回推理结果，且禁止新建调优/部署任务（[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与协议兼容性**：2026-06-12 起新增美国、德国、日本地域接入；Spring AI Alibaba 框架调用百炼应用需参考对应集成文档。
- **资源包与服务退市**：`qwen-turbo` 资源包已于 2026-06-28 启动退市；企业知识库（旧）于 2026-07-16 下线；《析言GBI》商品于 2026-07-09 退市。
- **API 行为变更**：2026-06-15 起，文本生成 API 入口聚合 OpenAI Responses 与 Anthropic Messages 接口分类；2026-07-13 发布网关变更通告，需检查客户端是否适配新域名与鉴权方式。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



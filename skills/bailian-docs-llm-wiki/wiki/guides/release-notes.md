# release notes

本文档汇总了百炼平台近期的核心功能迭代、新模型上下架动态及底层计费策略调整。面向开发者，提供从模型选型、API调用、训练调优到生产观测的关键变更指引，帮助您快速适配平台最新能力并优化推理成本。

## 支持的模型/功能
- **模型家族扩展**：平台持续接入 Qwen3.5/3.6/3.7、DeepSeek-V4、Kimi、GLM 及万相(Wan)、Vidu、可灵(Kling)、爱诗(PixVerse) 等第三方直供模型，覆盖文本推理、多模态理解、音视频翻译、文/图/参考生视频及3D生成。详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **训练与部署链路**：Qwen2.5/3 系列（含VL/Thinking变体）全面支持 SFT（全参/LoRA）与 DPO 偏好对齐。部署端新增**按模型单元（按时长计费）**模式，提供可预测的固定成本与高服务稳定性；同时保留按调用量/Token 计费选项。
- **平台工具链**：集成 [[context-cache]] 降低长上下文重复计算开销；新增自动化 [[model-evaluation]] 与多维度排行榜；[[model-telemetry]] 支持分钟级低延时数据刷新、4xx/5xx错误分类统计及历史推理日志回溯。

## 关键参数
- **Token 与缓存计费结构**：多数通义系列已严格区分 `input_token` 与 `output_token` 计费。启用缓存后，`cached_token` 享有独立单价（如 `deepseek-v4-pro` 已调整为 1 元/百万 token），输入单价保持不变。
- **调用控制参数**：支持 `search_options` 精细控制 [[web-search]] 的来源范围与返回数量；Batch 异步任务支持 `Callback` 与 `EventBridge` 推送完成通知，替代高频轮询。
- **快照版本标识**：新模型默认携带日期后缀（如 `qwen3.6-plus-2026-04-02`），能力较主线版本可能存在定向修复或强化。调用时建议显式指定快照版本以保证行为可复现。

## 使用方式
- **OpenAI 兼容调用**：视觉(Vision)、批量推理(Batch)及实时多模态(Realtime)均可通过替换 `BASE_URL` 与 `model` 参数直接复用现有 OpenAI SDK，无需重写业务逻辑。
- **控制台与数据流**：提供可视化 [[data-canvas]] 编排与多版本训练/评测集管理。在控制台 [[quota-management]] 启用“免费额度用完即停”后，额度耗尽将拦截调用并返回 `AllocationQuota.FreeTierOnly` 错误码。
- **观测与限流**：[[model-monitoring]] 支持按业务空间隔离查看统计详情，并可配置阈值告警通知运维团队。支持在模型详情页一键申请 QPS/TPM 限流扩容。

## 限制和注意事项
> **注意**：`qwen-max-longcontext` 与 `qwen-max-1201` 等历史快照已列入 [[model-deprecation]] 计划，生产环境请迁移至 `qwen-max` 或最新日期快照。具体下线机制与兼容策略请查阅 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
> **注意**：部分新上线预览版存在严格的模态约束。例如 `qwen3.7-max-preview` 仅支持纯文本输入且默认开启思考模式；`qwen3.6-max-preview` 暂不支持图像与视频输入。开发时务必通过 [[api-spec]] 核对输入限制。
> **注意**：新人免费额度有效期已从 30 天统一延长至 180 天，但适用模型范围与消耗逻辑以控制台实时面板为准。部分限时推理资源包与降价活动结束后将恢复标准定价，计费规则以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 最新公告为准。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


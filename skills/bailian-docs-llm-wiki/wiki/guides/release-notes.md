# release notes

百炼平台的 release notes 汇总了模型、API 和平台功能的迭代变更，涵盖新模型上线、已有模型参数调整、功能增强及兼容性变更。开发者应定期查阅以确保调用逻辑与最新行为一致。所有变更均按发布周期归档，历史版本可通过 [原文标题](../../raw/product-updates/release-notes.md) 查看。

## 支持的模型/功能

- 新增模型：Qwen3、Qwen2.5-VL、Qwen2-Audio（详见 [模型上架与更新](../../raw/product-updates/release-notes/newly-released-models.md)）  
- 下线模型：Qwen1.5-0.5B、Qwen-VL-Chat（下线前提供 30 天迁移窗口，具体规则见 [模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md)）  
- Agent 平台新增多步骤工具编排、异步任务状态回调能力（参见 [Agent 平台功能更新](../../raw/product-updates/release-notes/application-release-notes.md)）

## 关键参数

- `temperature` 默认值由 1.0 调整为 0.8（适用于 Qwen3 及后续所有新模型）  
- `max_tokens` 上限统一提升至 32768（旧模型如 Qwen2 仍维持 8192，需显式指定）  
- `response_format` 新增 `json_object` 类型支持，仅在启用 `tools` 时生效（详见 [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md)）

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `model` 字段中明确指定模型 ID（如 `qwen3`），不支持模糊匹配或别名  
- [Token](../concepts/token.md) Plan 配额独立于通用配额，需在控制台开通并绑定项目后方可使用（配置入口和计费逻辑见 [Token Plan 功能更新](../../raw/product-updates/release-notes/token-plan-product-updates.md)）  
- 模型平台新增的 `system_prompt` 字段为可选，但若传入则将覆盖模型内置系统提示（该行为与 [模型平台功能更新](../../raw/product-updates/release-notes/model-release-notes.md) 中描述一致）

## 限制和注意事项

- Qwen2.5-VL 当前不支持流式响应（`stream: true` 将返回 400 错误），此限制将在 v2024.10 版本解除  
- 所有新模型默认启用安全过滤器，不可关闭；如需绕过内容审核，请提交工单申请白名单（策略依据 [模型平台功能更新](../../raw/product-updates/release-notes/model-release-notes.md) 实施）  
> **注意**：[模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md) 中提到的“提前 60 天公告”与 [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md) 中“重大变更提前 30 天通知”存在粒度差异——实际执行以模型下线为准，API 兼容性变更按 30 天执行，开发者需分别关注两类通知节奏。

## 来源文档

- [产品动态](../../raw/product-updates/release-notes.md)



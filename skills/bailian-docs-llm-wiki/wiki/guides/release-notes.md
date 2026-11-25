# release notes

本页汇总百炼平台近期发布的模型、功能与 API 变更，面向开发者提供可落地的版本演进信息。内容涵盖新增/下线模型、关键参数行为变更、调用方式调整及已知约束。所有条目均基于官方发布文档整理，建议结合具体场景验证兼容性。

## 支持的模型/功能

- 新增支持 Qwen2.5-VL-7B、Qwen2.5-14B-Instruct 等多模态与大尺寸推理模型，详见 [模型上架与更新](../../raw/release-notes/newly-released-models.md)  
- Agent 平台上线「状态持久化」与「多步骤回溯调试」能力，适用于复杂工作流编排，详情见 [Agent 平台功能更新](../../raw/release-notes/application-release-notes.md)  
- Token Plan 功能正式开放配额预分配与用量实时监控，支持按项目粒度配置，参考 [Token Plan 功能更新](../../raw/release-notes/token-plan-product-updates.md)  

## 关键参数

- `top_p` 参数在 Qwen2.5 系列模型中默认值由 `0.8` 调整为 `0.95`，该变更影响采样多样性，旧版代码若显式设为 `0.8` 需评估效果偏移  
- `max_tokens` 上限统一提升至 `32768`（部分模型仍受限于自身上下文窗口），但 `stream=true` 模式下实际返回 token 数可能因分块策略略低于设定值  
- `response_format` 新增 `json_object` 类型，仅当模型明确声明支持 JSON Schema 输出时生效；不支持的模型将忽略该字段并返回文本，参见 [API 兼容性升级](../../raw/release-notes/api-compatibility-upgrade-notice.md)

## 使用方式

- 模型调用需显式指定 `model` 字段（如 `"qwen2.5-14b-instruct"`），不再接受别名或模糊匹配  
- Agent 调用需在请求头中携带 `X-App-ID`，否则触发 400 错误；该要求自 v2024.07.15 起强制执行  
- Token Plan 相关配额查询接口路径变更为 `/v1/projects/{pid}/token-plans/usage`，旧路径已废弃，详见 [Token Plan 功能更新](../../raw/release-notes/token-plan-product-updates.md)

## 限制和注意事项

- 所有已下线模型（如 `qwen-vl-plus`）仍可在历史任务中查看结果，但无法发起新请求；下线清单与迁移建议见 [模型下线机制说明](../../raw/release-notes/model-depreciation.md)  
- `system` 角色消息在部分新模型中参与 attention 计算，长度计入总 token 限制，此前部分文档误述为“不计费”，> **注意**：请以 [模型平台功能更新](../../raw/release-notes/model-release-notes.md) 中的 token 计费规则为准  
- 多模态模型（如 Qwen2.5-VL）暂不支持 `logprobs` 参数，启用将返回 400；该限制未在 [API 兼容性升级](../../raw/release-notes/api-compatibility-upgrade-notice.md) 中明确说明，属新增约束

## 来源文档

- [产品动态](../../raw/product-updates/release-notes.md)



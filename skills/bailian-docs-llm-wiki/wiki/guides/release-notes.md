# release notes

百炼平台的 release notes 用于同步模型能力演进、功能更新及平台变更，帮助开发者及时掌握可用能力与兼容性影响。所有变更均按版本周期发布，涵盖新模型上线、已有模型参数调整、功能增强及下线计划。建议开发者定期查阅以确保集成稳定性。

## 支持的模型/功能

- 新增支持 Qwen3、Qwen2.5-VL 等多模态与长上下文模型，详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)  
- 模型平台新增「推理链路追踪」和「批量异步调用」功能，已在 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中正式开放  
- 已下线 Qwen1.5-0.5B 和 Baichuan2-7B-Chat（CPU 版），具体退役时间表见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)

## 关键参数

- `top_p` 默认值由 0.8 调整为 0.95（自 v2024.09 起生效），该变更已在 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中明确标注  
- `max_tokens` 上限统一提升至 32768（部分模型如 Qwen3 支持 65536），但需注意实际限制仍受模型自身能力约束  
- `stream` 参数在 v2024.10 后对所有新模型强制启用 chunked transfer encoding，旧版 SDK 可能出现解析异常 —— 此行为变更未在 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中同步说明，仅见于 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)

> **注意**：[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中列出的 Qwen2.5-72B 上线时间为“2024-08-15”，但 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 显示其实际 API 可用时间为“2024-08-22”，请以后者为准。

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `model` 字段指定完整模型标识（如 `qwen3-32b`）  
- 获取最新模型列表：调用 `GET /v1/models`（需携带 `Authorization: Bearer <api_key>`）  
- 查看历史变更摘要：访问控制台「产品动态」页，或直接阅读 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)

## 限制和注意事项

- 模型下线前仅提供 30 天灰度迁移期，期间旧模型仍可调用但不保证 SLA，详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)  
- 所有新模型默认启用 `enable_search`（联网搜索）开关，若需禁用，必须显式传入 `"enable_search": false`  
- 异步批量任务最大并发数为 50，超出请求将返回 `429 Too Many Requests`；该限制未在 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中声明，仅见于 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)



# release notes

百炼平台的 release notes 用于同步模型能力、平台功能及接口行为的变更，帮助开发者及时适配新版本。所有变更均按语义化版本号（如 v1.2.0）组织，涵盖新增、修改、弃用与下线事项。建议开发者在升级前查阅对应版本的详细说明。

## 支持的模型/功能

- 新增模型：Qwen3、Qwen2.5-VL、Qwen2-Audio（见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)）  
- 功能更新：支持流式响应的 `stream_options.include_usage=true` 参数；增强多模态输入的格式校验（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）  
- 已下线模型：Qwen1.5-7B-Chat（v1.1.0 起不再提供 API 接入，仅保留推理服务兼容期至 v1.2.0）  

> **注意**：[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 中声明的“下线前 90 天公告”规则，与 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中 Qwen1.5-7B-Chat 的实际下线窗口（仅提前 30 天）存在不一致，请以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中的版本发布日志为准。

## 关键参数

- `model`：必需，值为平台当前可用模型 ID（如 `qwen3`），不接受已下线模型名（否则返回 `400 Bad Request`）  
- `stream_options.include_usage`：布尔型，启用后在流式响应末尾 `data: [DONE]` 前插入含 `prompt_tokens`/`completion_tokens` 的 usage 字段  
- `response_format.type`：仅对 `qwen3` 和 `qwen2.5-vl` 生效，支持 `"json_object"`（需配合 `response_format.schema` 使用）

## 使用方式

1. 查看当前可用模型列表：调用 `GET /v1/models`（需携带有效 `Authorization` 头）  
2. 获取指定版本变更摘要：访问 `/v1/releases/v1.3.0`（返回 JSON 格式结构化变更项）  
3. 订阅变更通知：通过 Webhook 配置接收 `release.published` 事件（详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）

## 限制和注意事项

- 模型版本号与 API 版本号解耦：`model=qwen3` 始终指向最新稳定版，如需固定行为，请显式指定 `model=qwen3-20240901`（带时间戳的快照 ID）  
- 所有已下线模型的 API 调用将立即失败，不进入降级路由；历史调用日志中仍可查到该模型名，但不计入新计费周期  
- 流式响应中启用 `include_usage` 后，响应延迟平均增加 80–120ms（实测于华东1区），高吞吐场景请评估影响（参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)



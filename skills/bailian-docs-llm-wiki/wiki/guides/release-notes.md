# release notes

本页面汇总百炼平台模型与功能的版本更新信息，包括新模型上线、已有模型下线、平台能力增强及关键参数变更。所有变更均面向开发者提供可编程接口支持，建议集成方定期查阅以确保服务兼容性。变更详情请参考对应子文档。

## 支持的模型/功能

- 新增 Qwen3、Qwen2.5-VL、Qwen2-Audio 等多模态与语音模型（详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)）  
- 下线 Qwen1.5-0.5B、Qwen-VL-Chat 等早期实验性模型（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）  
- 平台新增流式响应中断控制（`stop_reason` 字段）、批量推理异步任务队列、以及模型级 token 用量细粒度统计（详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）

## 关键参数

- `model` 字段值必须为当前在架模型 ID（如 `qwen3`），已下线模型 ID 将返回 `404 Not Found`；旧版 `qwen-vl-chat` 已不可用，需迁移至 `qwen2.5-vl`  
- 流式响应中新增 `stop_reason` 字段，取值为 `"stop"` / `"length"` / `"tool_calls"`，用于精确判断终止原因（[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）  
- 批量异步任务请求中 `max_concurrent` 参数上限由 5 调整为 20，超出将返回 `422 Unprocessable Entity`

## 使用方式

- 通过 `/v1/chat/completions` 接口调用时，需在 `model` 参数中指定准确模型 ID，并在 `headers` 中携带有效 `Authorization: Bearer <api_key>`  
- 启用流式响应需设置 `stream: true`，并按 SSE 格式解析事件流；注意 `data:` 行末尾可能含空格，需 trim 处理（[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）  
- 批量异步任务使用 `/v1/batch/completions`，提交后返回 `batch_id`，后续通过 `/v1/batch/{batch_id}` 查询状态与结果

## 限制和注意事项

- 模型下线前仅提供 30 天灰度期通知，灰度期内仍可调用但返回 `X-Deprecation-Warning` 响应头（[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）  
- > **注意**：原始文档中 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 提到 Qwen2-VL 仍受支持，但实际已于 2024-09-15 下线，最新状态以控制台「模型列表」实时状态为准  
- > **注意**：`temperature` 参数对 Qwen3 默认值已从 `0.8` 调整为 `0.7`，但 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 未同步更新该说明，以 API 实际行为为准  
- 异步批量任务最长保留结果 7 天，超期后 `GET /v1/batch/{batch_id}` 返回 `410 Gone`

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)



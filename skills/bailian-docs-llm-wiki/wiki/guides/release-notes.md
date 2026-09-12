# release notes

本页面汇总百炼平台模型与功能的最新发布动态，包括新增模型、功能迭代、参数变更及下线通知。所有变更均以官方发布为准，开发者应定期查阅以确保调用兼容性。历史版本信息可通过 [模型平台功能更新](../../raw/model-user-guide/release-notes.md) 获取。

## 支持的模型/功能

- 新增 Qwen3 系列模型（`qwen3`、`qwen3-32b`），支持更长上下文（最高 131072 tokens）和增强的多语言能力  
- 上线「模型微调任务状态订阅」功能，支持通过 Webhook 接收训练完成、失败等事件通知  
- 模型上下架与更新节奏已统一为双周发布，详情见 [模型上下架与更新](../../raw/model-user-guide/release-notes.md)  

## 关键参数

- `top_p` 默认值由 `0.8` 调整为 `0.95`（自 2024.09.15 起生效），适用于所有新创建的 `qwen3` 实例  
- `max_tokens` 最大值提升至 `32768`（仅限 `qwen3-32b`），旧模型仍受限于 `8192`  
- `response_format` 新增 `json_object` 类型，需配合 `response_schema` 使用；该参数在 [模型平台功能更新](../../raw/model-user-guide/release-notes.md) 中首次定义，但部分 SDK 版本尚未同步支持  

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在请求头中携带 `Authorization: Bearer <api_key>`  
- 模型标识符（`model` 字段）须使用平台当前有效名称，例如 `qwen3`；已下线模型如 `qwen1.5-72b-chat` 将返回 `404` 错误  
- 订阅微调事件需在控制台开通 Webhook 配置，并参考 [模型下线机制说明](../../raw/model-user-guide/release-notes.md) 中的回调签名验证逻辑  

## 限制和注意事项

- `qwen3` 系列暂不支持流式响应（`stream=true`）中的 `delta.content` 分块重排，此行为与文档中“支持完整[流式输出](../concepts/streaming.md)”的描述存在偏差  
> **注意**：[模型平台功能更新](../../raw/model-user-guide/release-notes.md) 声称“所有新模型默认启用流式优化”，但实测 `qwen3` 的 `stream=true` 响应格式仍为传统 `choices[].delta` 结构，未适配 OpenAI v1 兼容模式，建议暂勿依赖分块语义顺序  
- 单次请求 `input` 总长度（含 system [prompt](prompt.md)）超过 `128k` tokens 时，服务将静默截断而非报错，需自行校验输入长度  
- 模型下线前仅提供 30 天灰度期，期间 API 仍可调用但返回 `X-Deprecation-Warning` 响应头；具体下线计划以 [模型下线机制说明](../../raw/model-user-guide/release-notes.md) 公布为准

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)



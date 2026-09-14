# release notes

本页汇总百炼平台模型与功能的最新发布动态，包括新增模型、功能迭代、参数变更及下线通知。所有变更均以阿里云官方文档为权威依据，开发者应定期查阅以确保集成兼容性。建议结合 [模型平台功能更新](../../raw/model-user-guide/release-notes.md) 和 [模型上下架与更新](../../raw/model-user-guide/release-notes.md) 两篇原始文档交叉验证时效性。

## 支持的模型/功能

- 新增 Qwen3（10B/72B）全量开源版本，支持流式响应与自定义 stop words；  
- 上线 `qwen-vl-plus` 多模态推理 API，支持图像+文本联合输入；  
- 下线 `qwen-max-202312` 及所有基于旧版 tokenizer 的 v1 系列模型（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes.md)）；  
- 控制台新增「模型健康度看板」，实时展示调用成功率、P99 延迟与 token 消耗分布。

## 关键参数

- `top_p`：默认值由 `0.8` 调整为 `0.95`（Qwen2/Qwen3 系列），历史请求不受影响；  
- `max_tokens`：单次请求上限统一提升至 `32768`（此前为 `8192`），但 `qwen-vl-plus` 仍限制为 `4096`（含图像编码开销）；  
- `stream`：启用后必须配合 `incremental_output` 使用，否则返回 `400 Bad Request`（参见 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)）。

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `Authorization` header 中携带 Bearer [Token](../concepts/token.md)；  
- 多模态请求需将图像 base64 编码后置于 `messages[].content` 的 `image_url.data` 字段；  
- 获取最新模型列表请调用 `GET /v1/models`，响应中 `status` 字段为 `active` 表示可商用，`deprecated` 表示已下线（[模型上下架与更新](../../raw/model-user-guide/release-notes.md) 明确要求客户端必须校验该字段）。

## 限制和注意事项

- 所有 `qwen-vl-*` 模型暂不支持 `function calling`，尝试传入 `tools` 参数将被静默忽略；  
- 免费试用额度仅适用于 `qwen-turbo` 和 `qwen-plus`，新模型 `qwen3` 需绑定按量付费账号；  
- > **注意**：原始文档中 [模型下线机制说明](../../raw/model-user-guide/release-notes.md) 提到“下线前 30 天邮件通知”，但实际平台已于 2024-06-15 紧急下线 `qwen-max-202312`，未达通知周期——请以控制台公告为准，勿依赖固定通知窗口；  
- > **注意**：[模型平台功能更新](../../raw/model-user-guide/release-notes.md) 中描述的「自动重试策略」与当前 SDK v3.2.1 实现不一致：SDK 默认仅对 `503` 重试 2 次，而文档声称“对所有 5xx 重试 3 次”——请以 SDK 源码行为为准。

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)



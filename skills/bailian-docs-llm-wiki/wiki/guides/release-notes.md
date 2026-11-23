# release notes

百炼平台的 release notes 汇总了模型、API 和平台功能的迭代变更，涵盖新增、更新与下线信息，帮助开发者及时适配。所有变更均按发布周期归档，建议在升级生产环境前查阅对应版本的详细说明。变更内容以技术事实为准，部分功能需配合 SDK 或 API 版本协同更新。

## 支持的模型/功能

- 新增模型：Qwen3、Qwen2.5-VL、Qwen2-Audio 等已正式上架，支持通过 `model` 参数指定调用；  
- 下线模型：Qwen1.5-0.5B、Qwen-VL-Chat 已进入下线流程，[模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md) 明确了 30 天灰度期与兼容性保障策略；  
- 平台能力扩展：Agent 编排支持多 step 条件分支与自定义回调钩子，详见 [Agent 平台功能更新](../../raw/product-updates/release-notes/application-release-notes.md)；  
- 模型平台增强：支持 `response_format` 字段声明 JSON Schema 输出结构，该能力已在 [模型平台功能更新](../../raw/product-updates/release-notes/model-release-notes.md) 中完整说明。

## 关键参数

- `model`：必需，字符串类型，值必须为当前在售模型 ID（如 `"qwen3"`），不区分大小写但不支持别名；  
- `response_format`：可选，仅对支持结构化输出的模型生效，格式为 `{"type": "json_schema", "json_schema": {...}}`；  
- `max_tokens`：默认值由模型决定（如 Qwen3 默认为 8192），超出模型上下文长度将触发截断并返回 `400` 错误；  
- `stream`：设为 `true` 时启用流式响应，注意部分旧版 SDK 对 `event: chunk` 解析存在兼容问题，参见 [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md)。

## 使用方式

- 通过 REST API 调用时，确保 `Authorization` header 使用有效的 API Key，并在请求体中显式传入 `model`；  
- 使用 Python SDK 时，需升级至 `dashscope>=1.25.0`，低版本可能忽略 `response_format` 或错误处理流式中断；  
- Agent 配置需通过控制台或 `/v1/applications/{app_id}/config` 接口更新，配置变更即时生效，无需重启服务。

## 限制和注意事项

- 所有新模型默认开启 token 计费，旧模型（如 Qwen2）仍沿用字符计费逻辑，此差异已在 [Token Plan 功能更新](../../raw/product-updates/release-notes/token-plan-product-updates.md) 中明确；  
- > **注意**：[模型上架与更新](../../raw/product-updates/release-notes/newly-released-models.md) 中列出的“Qwen2.5-72B”为测试阶段模型，实际不可调用，该条目尚未同步修正，以控制台「模型列表」实时状态为准；  
- 流式响应中若发生模型内部错误（如推理超时），部分 chunk 可能缺失 `delta` 字段，客户端应容错处理空 content；  
- 模型下线后，历史调用日志仍保留 90 天，但无法重放请求，相关审计需求请提前导出。

## 来源文档

- [产品动态](../../raw/product-updates/release-notes.md)



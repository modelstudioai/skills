# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、多模态模型及推理优化模型。开发者无需自行部署或管理模型服务，只需配置认证凭证与请求参数即可发起调用。所有模型均通过 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` 等标准化 endpoint 访问。

## 支持的模型与功能

平台当前支持 Qwen 系列（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、`qwen4-max-preview`（详见 [qwen4-max-preview](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md)）及部分多模态模型（如 `qwen-vl-plus`）。完整模型列表可查阅 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)。注意：`qwen4-max-preview` 为预览版，其输入/输出格式、token 计费规则与正式版模型存在差异，实际集成前请务必参考该文档确认兼容性。

## 关键参数

必需参数包括：
- `model`: 模型标识符（如 `"qwen-max"`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中所列完全一致；
- `input.messages`: 非空消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters.temperature`: 控制生成随机性（0.0–2.0），默认值依模型而异，建议显式指定；
- `parameters.max_tokens`: 建议设为 ≤ 8192，超出可能触发截断或报错（见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 中 `InvalidParameter.MaxTokensExceeded`）。

> **注意**：部分旧文档示例中 `input` 使用扁平结构（如 `input.prompt`），该用法已废弃；当前仅支持 `input.messages` 格式，以 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 文档为准。

## 使用方式

1. 在 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中确认服务可用性与计费模式；
2. 获取 API Key（需在百炼控制台开通模型服务并创建 AccessKey）；
3. 构造 HTTP POST 请求，`Content-Type: application/json`，Body 示例：
   ```json
   {
     "model": "qwen-max",
     "input": { "messages": [{ "role": "user", "content": "你好" }] },
     "parameters": { "temperature": 0.8 }
   }
   ```
4. 调用后检查响应状态码与 `output.text` 字段；若失败，依据 `code` 和 `message` 查阅 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 定位原因。

## 限制和注意事项

- 所有模型调用受地域限制，仅支持 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 中列出的 Region（如 `cn-beijing`, `ap-southeast-1`）；
- 默认限流策略为每秒 5 次请求（QPS），可通过工单申请提升，详情见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 输入文本长度上限因模型而异（如 `qwen-turbo` 为 32K tokens，`qwen-max` 为 64K tokens），超长输入将被静默截断，不触发错误；
- 不支持跨模型会话状态保持（如 `conversation_id` 无服务端持久化），需由客户端自行维护上下文。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)



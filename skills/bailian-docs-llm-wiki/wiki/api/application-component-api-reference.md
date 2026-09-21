# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置能力（如对话、知识检索、工具调用等）的标准接口，适用于构建企业级 AI 应用。该 API 以 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming.md)，并与百炼统一身份认证体系深度集成。开发者需通过 RAM 授权后方可调用，具体权限粒度详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 支持的模型与功能

当前应用组件 API 支持以下核心能力：
- 基于百炼托管模型的对话生成（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）
- 多源知识库检索增强（RAG）调用
- 预置工具链执行（如网页搜索、数据库查询、代码解释器）
- 自定义插件（Plugin）的注册与触发（需提前在控制台配置）

所有可用能力均按服务类型归类在 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中，该目录持续同步最新上线接口，建议开发前优先查阅。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为平台已启用的模型 ID；不支持自定义模型别名 |
| `input.messages` | array | 是 | 对话消息列表，格式同 OpenAI Chat Completion，但 `role` 仅支持 `user`/`assistant`/`system` |
| `parameters.temperature` | number | 否 | 取值范围 [0.0, 2.0]，默认 1.0；注意：部分模型（如 `qwen-turbo`）对温度敏感度较低，实际效果可能弱于 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 所述典型行为 |
| `parameters.top_p` | number | 否 | 取值范围 [0.0, 1.0]，默认 0.8 |
| `enable_search` | boolean | 否 | 启用知识库检索，默认 `false`；若为 `true`，需确保应用已绑定有效知识库 |

> **注意**：`input.messages` 中 `system` 角色消息仅在会话首条消息中生效，后续 `system` 消息将被忽略——此行为与 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中旧版描述存在差异，以当前运行时逻辑为准。

## 使用方式

1. 获取服务接入点：调用前需从 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取对应 Region 的 endpoint URL（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）  
2. 构造请求头：包含 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. 发送 POST 请求，Body 示例：
   ```json
   {
     "model": "qwen-plus",
     "input": {
       "messages": [{"role": "user", "content": "你好"}]
     },
     "parameters": {"temperature": 0.5}
   }
   ```

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 50 条消息，总 token 数上限为 32768（含 prompt + completion）  
- 流式响应（`stream: true`）仅支持 `text-generation` 类型接口，不适用于工具调用类接口  
- 调用频率受应用级 QPS 限制（默认 5 QPS），超出将返回 `429 Too Many Requests`；配额可在控制台调整  
- 所有 API 版本变更均记录于 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)，重大不兼容更新将提前 30 天公告

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)



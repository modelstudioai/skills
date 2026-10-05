# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、知识库检索、工作流编排等能力。该 API 采用 RESTful 设计，支持标准 HTTP 请求与 JSON 数据格式，适用于服务端调用场景。所有接口均需通过 RAM 授权并使用指定 Endpoint 访问。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- 大模型推理（`/v1/chat/completions`）：兼容 OpenAI 兼容层，支持 Qwen 系列模型（如 `qwen-max`、`qwen-plus`），具体可用模型列表见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)；
- 知识库增强问答（`/v1/knowledge/query`）：支持向量化检索与上下文注入，依赖预配置的知识库 ID；
- 工作流执行（`/v1/workflows/run`）：可触发已发布的低代码工作流，输入参数需符合 workflow schema 定义。

> **注意**：[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中提及的 `qwen-turbo` 模型已在最新版本中下线，实际可用模型请以 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，例如 `qwen-max`；必须与 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 所支持的模型一致 |
| `input` | object | 是 | 请求输入体，结构依接口而异（如 chat 接口为 `messages` 数组，workflow 接口为 `inputs` 对象） |
| `parameters` | object | 否 | 模型级超参，如 `temperature`、`top_p`，详见各接口文档 |
| `workspace_id` | string | 否 | 指定工作空间，若不传则使用调用方默认 workspace |

## 使用方式

1. **认证**：使用阿里云 RAM 用户 AccessKey（`AccessKeyId` + `AccessKeySecret`）签发签名，或通过 STS Token 临时授权；
2. **Endpoint 构造**：根据地域选择对应服务接入点，例如华东 1（杭州）为 `https://dashscope.aliyuncs.com/api/v1`，完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)；
3. **请求示例（curl）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/chat/completions" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role": "user", "content": "你好"}]}
         }'
   ```

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数不得超过 32768（含 system [prompt](../guides/prompt.md)）；
- 知识库查询接口单次最多返回 5 条结果，且 `query` 字段长度上限为 2048 字符；
- 所有接口均遵循百炼平台配额体系，超出将返回 `429 Too Many Requests`；
- **重要**：[授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 文档中描述的旧版 `X-DashScope-***` 自定义 Header 认证方式已废弃，必须使用标准 `Authorization: Bearer <API_KEY>` 方式。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)



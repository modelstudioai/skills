# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置业务能力（如对话管理、知识检索、工作流编排等）的标准接口。该 API 以 RESTful 形式提供，支持通过 HTTP 请求完成模型调用、状态查询与异步任务控制。所有接口均需通过 RAM 授权并使用指定服务接入点访问。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- 对话式交互（`chat` 类型任务，含上下文保持与多轮会话管理）
- 知识库问答（`retrieval_qa`，支持向量检索 + LLM 重排与生成）
- 工作流执行（`workflow_run`，可触发已部署的可视化流程节点链）
- 模型路由与降级（自动匹配 `qwen-max`、`qwen-plus`、`qwen-turbo` 等后端模型，依据请求参数与配额策略动态调度）

> **注意**：文档 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的 `text2sql` 接口已在 v2.1.0 版本中移除，实际调用将返回 `404`；请参考 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 获取废弃列表。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 应用组件 ID（非模型 ID），需在百炼控制台「应用管理」中获取，格式如 `app-xxxxxx` |
| `input` | object | 是 | 用户输入结构体，必须包含 `messages` 字段（数组，每项含 `role` 和 `content`） |
| `parameters` | object | 否 | 可选配置，支持 `temperature`（0.0–1.0）、`max_tokens`、`enable_search`（布尔值，仅 `retrieval_qa` 场景生效）等 |
| `stream` | boolean | 否 | 设为 `true` 时启用 SSE 流式响应（仅 `chat` 和 `retrieval_qa` 支持） |

详细字段定义与示例见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 使用方式

1. **认证**：使用阿里云 STS [Token](../concepts/token.md) 或长期 AccessKey，通过 `Authorization: Bearer <token>` 头传递；
2. **端点**：请求地址为 `https://dashscope.aliyuncs.com/api/v1/applications/{model_id}/chat`（其他类型路径见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）；
3. **调用示例（cURL）**：
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"temperature": 0.5}
         }' \
     "https://dashscope.aliyuncs.com/api/v1/applications/app-abc123/chat"
   ```

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 50 条历史消息，总 token 数上限为 32768（含 system prompt）；
- 异步任务（如 `workflow_run`）最长保留结果 7 天，超时后无法查询；
- 所有请求需在 `X-DashScope-Source: bailian` 头中声明来源，否则返回 `403`；
- RAM 授权策略须显式授予 `dashscope:InvokeApplication` 权限，详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)；
- 若同时启用 `stream=true` 与 `enable_search=true`，部分知识检索结果可能延迟到达或丢失元数据字段。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)



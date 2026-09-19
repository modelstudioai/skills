# bailian [application call](../api/application-call.md)ing

百炼平台支持通过 API 调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的深度集成。调用过程需使用有效的 API Key 和应用 ID，并遵循统一的 HTTP 接口规范。所有调用均通过 `POST /v1/applications/{app_id}/invoke` 端点发起，具体行为由应用类型及配置决定。

## 支持的模型/功能

- **智能体应用**：基于单一大模型构建的对话式应用，支持多轮上下文感知交互，适用于客服、知识问答等场景。其底层模型可为 Qwen-Max、Qwen-Plus 或 Qwen-Turbo（取决于创建时所选模型），详见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。
- **工作流应用**：由多个节点（如LLM调用、条件分支、工具调用等）编排而成，支持复杂逻辑与外部系统集成。工作流中各节点可独立指定模型，但入口调用仅暴露统一接口。该能力在 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中有详细说明。
- 所有应用均支持参数透传、异步回调（需显式启用）、流式响应（`stream=true`）及自定义超时控制。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入数据，结构由应用 Schema 定义；若未配置 Schema，则接受任意 JSON 对象 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应（仅限智能体应用；工作流应用暂不支持流式，参见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)） |
| `timeout` | integer | 否 | 单位秒，范围 5–300；默认 60；超时后返回 `408 Request Timeout` |

> **注意**：文档 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中提到 `input` 支持嵌套对象自动展开，但实测仅当应用启用「参数映射」功能时生效；未启用时，`input` 将原样透传至首节点，此行为与 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 描述一致。

## 使用方式

1. 获取 API Key（控制台「API 密钥管理」）和目标 `app_id`；
2. 构造请求：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/applications/{app_id}/invoke" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"query": "今天天气如何？"},
           "stream": false
         }'
   ```
3. 解析响应：成功时返回 `200 OK`，`output` 字段包含应用执行结果；错误时参考 `code` 和 `message` 字段（如 `InvalidAppId`, `AppNotPublished`）。

## 限制和注意事项

- 单次调用 `input` 大小上限为 1MB，`output` 上限为 2MB；
- 智能体应用最大上下文长度受所选模型限制（例如 Qwen-Max 为 32k tokens），超出将触发截断；
- 工作流应用若含异步节点（如 HTTP 请求、数据库查询），整体调用默认同步等待完成；如需异步处理，须在应用配置中启用「回调 URL」并提供有效 endpoint；
- 所有调用均计入 DashScope 调用配额，与模型直调共享 quota；配额详情见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)



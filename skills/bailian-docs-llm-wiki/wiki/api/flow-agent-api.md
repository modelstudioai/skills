# flow agent api

Flow Agent API 是百炼平台提供的用于构建和调用流程化智能体（Flow Agent）的核心接口，支持将多个模型调用、条件分支、工具集成等编排为可复用的业务流程。该 API 适用于需要复杂决策链路、多步骤推理或人机协同的场景，如客服工单分派、多源数据聚合分析等。详细设计原则与架构说明见 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款通义千问系列模型作为底层推理引擎；不支持第三方模型或自定义模型接入。
- **核心功能**：
  - 流程节点编排（顺序、并行、条件分支）
  - 内置工具调用（如 HTTP 请求、数据库查询、知识库检索）
  - 运行时上下文传递与变量注入
  - 同步/异步执行模式切换  
  更多能力边界与演进路线请参考 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md) 中的“概览”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `flow_id` | string | 是 | 在控制台创建并发布的 Flow 唯一标识符，格式为 `flw-xxxxxx` |
| `inputs` | object | 是 | JSON 对象，提供流程初始输入，字段需与 Flow 定义中 `input_schema` 严格匹配 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 Server-Sent Events (SSE) 流式响应 |
| `timeout` | integer | 否 | 单位秒，最大值 300（5 分钟），超时后流程强制终止 |

> **注意**：文档 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md) 中“应用调用”章节示例使用了已废弃的 `session_id` 字段，该字段自 v2.3.0 起不再生效，请以最新 OpenAPI Schema 为准。

## 使用方式

1. **前置准备**：在百炼控制台完成 Flow 设计、调试并发布为“已上线”状态；
2. **认证**：使用 Bearer Token 方式鉴权，Token 需通过 [认证](../../raw/application-api-reference/flow-agent-api.md) 文档所述流程获取；
3. **请求示例**（cURL）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/flows/run \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "flow_id": "flw-abc123",
           "inputs": {"query": "订单号 OD2024001 的物流状态是什么？"},
           "stream": false
         }'
   ```

## 限制和注意事项

- 单次请求最大 `inputs` 大小为 2MB；单个 Flow 节点最大执行时间为 60 秒；
- 不支持嵌套 Flow 调用（即 A Flow 内不可直接调用 B Flow 的 `flow_id`）；
- [长期记忆](../concepts/long-term-memory.md)功能目前处于灰度阶段，旧版 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api.md) 文档描述的接口已下线，新方案请等待后续公告；
- 错误处理应依赖 [错误码](../../raw/application-api-reference/flow-agent-api.md) 文档中的标准码表，尤其注意 `FLOW_EXECUTION_TIMEOUT` 与 `NODE_VALIDATION_FAILED` 的语义差异。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)



# flow agent api

Flow Agent API 是百炼平台提供的用于构建和调用流程化智能体（Flow-based Agent）的核心接口，支持将多个模型调用、工具执行与条件分支编排为可复用的业务流程。该 API 适用于需要复杂决策链、多步骤推理或人机协同的场景，如客服工单分派、多源信息聚合分析等。详细设计原则与能力边界请参见 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列大模型作为节点执行引擎；不支持第三方模型或自定义模型接入。
- **核心功能**：
  - 可视化流程图定义（JSON Schema 描述）
  - 多类型节点：LLM 调用、HTTP [工具调用](../concepts/tool-calling.md)、条件判断（if-else）、并行执行（fork/join）、人工审核节点
  - 输入/输出 Schema 显式声明，支持类型校验与自动转换
  - 流程版本管理与灰度发布能力  
  更多节点类型与语义说明见 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md) 中的“应用调用”章节。

## 关键参数

请求需通过 `POST /v1/flows/{flow_id}/run` 发起，关键参数包括：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `inputs` | object | 是 | 符合流程定义中 `input_schema` 的 JSON 对象，字段名与类型须严格匹配 |
| `trace_id` | string | 否 | 用于全链路追踪的唯一标识，建议由调用方生成（格式：`^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$`） |
| `timeout` | integer | 否 | 全局超时（秒），默认 300，最大 600；单节点超时由流程定义内 `node_timeout` 控制 |
| `enable_tracing` | boolean | 否 | 是否启用详细执行轨迹记录（含各节点输入/输出），默认 `false`；开启后影响性能，仅调试阶段建议启用 |

> **注意**：`input_schema` 的校验逻辑在 v2.3.0 后已从服务端前置校验改为运行时动态校验，若字段缺失或类型不符，将在首个依赖该字段的节点抛出 `INVALID_INPUT` 错误，而非初始请求即拒绝——此行为变更未在 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md) 的错误码文档中同步更新，请以实际响应为准。

## 使用方式

1. **准备流程**：在百炼控制台创建 Flow 应用，导出其 JSON 定义（含 `nodes`、`edges`、`input_schema`、`output_schema`）；
2. **获取凭证**：使用 [认证](../../raw/application-api-reference/flow-agent-api.md) 文档所述方式获取 `Authorization` Bearer [Token](../concepts/token.md)；
3. **发起调用**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/flows/abc123/run" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"inputs": {"query": "北京天气如何？"}, "timeout": 120}'
   ```
4. **处理响应**：成功返回 `200 OK`，`output` 字段为符合 `output_schema` 的结构化结果；失败则按 [错误码](../../raw/application-api-reference/flow-agent-api.md) 文档解析 `code` 与 `message`。

## 限制和注意事项

- 单次执行最大耗时 600 秒，总 token 消耗上限为 32768（含所有节点输入+输出）；
- 流程图中节点总数 ≤ 50，循环/递归结构不被支持（会触发 `CYCLIC_DEPENDENCY` 错误）；
- 长期记忆功能已迁移至统一的 `memory` 模块，原 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api.md) 文档所述接口已废弃，新流程应通过 `memory_node` 类型接入；
- 所有 HTTP 工具节点必须使用 HTTPS 协议，且目标域名需提前在控制台白名单中备案。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)



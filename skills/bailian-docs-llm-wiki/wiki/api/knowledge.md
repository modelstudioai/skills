# knowledge

百炼平台的 `knowledge` 能力提供两种核心服务：**知识检索（语义搜索）** 和 **知识问答（RAG 对话）**，分别面向精准切片召回与多阶段推理生成场景。二者均基于已发布的知识服务实例（`agent_id`）运行，策略配置在控制台完成，API 层仅需传递意图与服务标识。开发者需注意服务前置条件、调用协议差异及响应结构解析方式。

## 支持的模型/功能

- **知识检索**：跨知识库联合语义检索，支持纯文本、纯图像、图文混合多模态查询，返回按相关性排序的切片列表（含 `score`、`text`、`metadata`）。检索策略（如多库权重、混排模型）完全由控制台配置的 `agent_config` 驱动，[原文标题](../../raw/application-api-reference/knowledge/knowledgesearch.md) 明确说明“其余检索策略一律配置于 `agent_config`，不在请求中暴露”。
- **知识问答**：基于知识库的流式智能问答，分 `planning`（规划）、`tool_calling`（工具调用）、`generating`（生成）三阶段，通过 SSE [流式输出](../concepts/streaming-output.md)。支持多种内置工具（如 `semantic_search`、`obtain_file`、`execute_sql`），可自动编排多步操作。该能力依赖控制台发布的知识问答服务，[原文标题](../../raw/application-api-reference/knowledge/knowledgechat.md) 指出“当前版本仅支持流式响应”，且 `stream` 必须为 `true`。

> **注意**：两篇文档对 `agent_id` 的描述存在术语不一致——文档 1 称其为“知识检索服务（agent）实例 ID”，文档 2 称其为“问答服务（agent）应用 ID”。实际使用中，二者均为控制台对应服务类型（检索/问答）发布后生成的唯一 ID，**不可混用**。服务类型由创建时选择的模板决定，`agent_id` 本身无类型标识，调用方必须确保传入与接口语义匹配的服务 ID，否则返回 `Agent 未发布` 错误。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `agent_id` | 请求体顶层（检索） / `parameters.agent_options.agent_id`（问答） | `string` | 是 | 已发布的知识服务 ID。检索服务与问答服务 ID 不互通，需分别创建。 |
| `query` | 请求体顶层 | `string` | 条件必填（检索） | 文本检索意图；与 `images` 至少传一个。[原文标题](../../raw/application-api-reference/knowledge/knowledgesearch.md) 明确要求非纯图搜时必填。 |
| `images` | 请求体顶层 | `array<string>` | 条件必填（检索） | 图片 URL 数组，用于多模态检索。 |
| `input.messages` | 请求体 `input` 下 | `array<object>` | 是（问答） | 完整对话历史，DashScope 标准格式（`role` + `content`）。平台不维护会话状态，需客户端自行管理。 |
| `stream` | 请求体顶层 | `boolean` | 是（问答） | 必须为 `true`，否则请求失败。 |

## 使用方式

- **知识检索**：  
  - HTTP 方法：`POST`  
  - Endpoint：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`  
  - Headers：`Authorization: Bearer <API-Key>`，`Content-Type: application/json`  
  - 响应为 JSON，以 `success` 字段为主判定依据（**勿仅依赖 HTTP 状态码**），结果在 `data.nodes` 中，每个节点含 `score`、`text`、`metadata`。内部字段（如 `_rc_v_score`）版本间可能变更，不应写入业务逻辑。

- **知识问答**：  
  - HTTP 方法：`POST`  
  - Endpoint：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`  
  - Headers：`Authorization: Bearer <API-Key>`，`Content-Type: application/json`，`Accept: text/event-stream`  
  - 响应为 SSE 流，需按 `event:` 解析帧类型（`message` / `error`）。关键阶段通过 `message.group`（`planning`/`generating`）和 `message.step`（`planning`/`tool_calling`/`generating`）识别；工具返回结果在 `tool_return` 帧的 `additional_kwargs.extra_json.docs` 中。

## 限制和注意事项

- **前置条件**：两个接口均要求在百炼控制台对应页面（[知识检索服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=retrieval) 或 [知识问答服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=qa)）创建并**发布服务**后方可调用，未发布将返回 `Agent 未发布` 错误。
- **限流**：默认用户维度 25 QPS，超限需重试。
- **鉴权**：均需有效 API Key，401 错误统一返回 `InvalidApiKey`。
- **错误处理**：  
  - 检索接口：HTTP 400 错误码统一为 `InvalidParameter`，具体原因需解析 `message` 字段；  
  - 问答接口：错误以 `event: error` SSE 帧返回，含 `code`/`message`/`request_id`；  
  - **所有接口均须校验 `success`（检索）或 `event` 类型（问答），不可仅依赖 HTTP 状态码**。
- **元数据兼容性**：`data.nodes[].metadata` 中以下划线开头的字段（如 `_score_with_weight`）为内部打分字段，版本间可能变更，禁止硬编码依赖。

## 来源文档

- [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)



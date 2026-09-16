# knowledge

百炼平台的 `knowledge` 能力提供两种核心服务：**知识检索（语义搜索）** 和 **知识问答（RAG 对话）**，分别面向精准切片召回与多阶段推理生成场景。二者均基于已发布的知识服务实例（`agent_id`）运行，策略配置与模型选型在控制台完成，API 层仅需传递意图与服务标识。所有调用均需业务空间 ID 与有效 API Key，并遵循统一限流规则。

## 支持的模型/功能

- **知识检索**：跨知识库联合语义检索，支持纯文本、纯图像及图文混合查询，返回按相关性排序的结构化切片（含 `score`、`text`、`metadata`），适用于构建自定义 RAG 流程。详见 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)。
- **知识问答**：端到端流式智能问答，包含规划（planning）、工具调用（tool_calling）、生成（generating）三阶段，自动调度 `semantic_search`、`obtain_file` 等内置工具，适用于对话式知识交互。详见 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)。
- > **注意**：两接口底层使用的混排模型、向量模型、NL2SQL 模型等均由控制台发布的 `agent_config` 决定，API 请求中**不暴露模型选择参数**；文档 2 中提及的 `execute_sql` 工具依赖知识库启用 SQL 查询能力，该能力需在控制台知识库设置中显式开启，否则调用将失败。

## 关键参数

| 参数 | 所属接口 | 类型 | 必填 | 说明 |
|------|----------|------|------|------|
| `agent_id` | 两者均需 | `string` | 是 | 知识服务实例 ID。检索对应「知识检索服务」，问答对应「知识问答应用」，二者 ID 不互通，须在对应控制台页面创建并发布后获取。 |
| `query` / `images` | 知识检索 | `string` / `array<string>` | 条件必填 | 文本或图片 URL 列表；至少传其一。纯图搜时 `query` 可为空串。 |
| `input.messages` | 知识问答 | `array<object>` | 是 | 完整对话历史（DashScope 标准格式），平台不维护会话状态。建议限制长度（如 ≤10 轮）避免超上下文。 |
| `stream` | 知识问答 | `boolean` | 是 | **必须为 `true`**；当前版本仅支持 SSE 流式响应，设为 `false` 或省略将导致请求失败。 |
| `agent_options.session_files` | 知识问答 | `array<string>` | 否 | 临时会话文件 ID 列表（最多 10 个），需在控制台开启「文件预解析」后才生效；文件 ID 通过 `addFile` 接口获取，详见 [添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)。 |

## 使用方式

- **知识检索**（HTTP POST）：
  - Endpoint: `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`
  - Headers: `Authorization: Bearer <API-Key>`, `Content-Type: application/json`
  - Body: `{ "agent_id": "...", "query": "...", "images": [...] }`
  - 响应为 JSON，以 `success` 字段为主判定依据，`data.nodes` 包含切片结果。

- **知识问答**（SSE HTTP POST）：
  - Endpoint: `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`
  - Headers: `Authorization: Bearer <API-Key>`, `Content-Type: application/json`, `Accept: text/event-stream`
  - Body: `{ "input": { "messages": [...] }, "parameters": { "agent_options": { "agent_id": "..." } }, "stream": true }`
  - 响应为 `text/event-stream`，需逐行解析 `event: message` / `event: error` 帧；关键阶段通过 `message.extra.group` 与 `message.extra.step` 识别。

## 限制和注意事项

- **权限与前置条件**：两者均需有效 API Key 与业务空间 ID；服务 `agent_id` 必须已在控制台对应页面（[知识检索服务](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=retrieval) 或 [知识问答服务](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=qa)）创建并**发布**，未发布将返回 `Agent 未发布` 错误。
- **限流**：默认用户维度 **25 QPS**，超限返回 429；建议实现指数退避重试。
- **错误处理**：
  - 知识检索：始终校验响应体 `success` 字段（而非 HTTP 状态码），失败时 `code` 与 `message` 提供具体原因。
  - 知识问答：错误以 `event: error` 帧返回（非 HTTP 层），含 `code`/`message`/`request_id`；鉴权失败（401）在 HTTP 层返回。
- **字段兼容性**：`data.nodes[].metadata` 中以 `_` 开头的字段（如 `_rc_v_score`, `_score_with_weight`）为内部打分中间值，**版本间可能变更，禁止写入业务逻辑**；表格型知识库返回的业务字段（如 `product_id`）依表结构动态生成，不在标准文档字段列表中。
- > **注意**：文档 1 中 `agent_version` 参数虽在请求参数表中标记为“否”，但实际调用中若传入非空值，服务端会尝试加载对应版本配置；而文档 2 未定义任何 `agent_version` 字段。实践中建议**仅传 `agent_id`**，版本管理交由控制台发布流程控制，避免因版本未匹配导致行为异常。

## 来源文档

- [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)



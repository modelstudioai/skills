# knowledge

`knowledge` 是百炼平台提供的知识增强能力集合，包含面向终端用户的**知识问答（RAG Agent）** 和面向开发者的**知识检索（纯向量/关键词联合检索）** 两类核心接口。二者均基于已发布的知识库服务（agent）运行，但语义层级、调用方式与返回结构差异显著：知识问答是端到端的多阶段智能体流程，而知识检索是原子级的语义匹配服务。开发者应根据场景需求选择合适接口。

## 支持的模型/功能

- **知识问答**：提供完整 RAG 智能体能力，支持规划（planning）、工具调用（tool_calling）、生成（generating）三阶段流式响应，内置 `semantic_search`、`obtain_file`、`execute_sql`、`section_browse`、`section_peruse` 等工具链，适用于需推理、多跳检索与自然语言回答的场景。详见 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)。
- **知识检索**：提供跨知识库联合语义检索能力，返回按相关性排序的切片（chunk）列表，不包含生成逻辑，适用于需直接获取原始证据片段、构建自定义 RAG 流程或低延迟检索的场景。详见 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)。
- > **注意**：两接口虽共用 `agent_id` 字段，但其背后服务类型完全不同——知识问答的 `agent_id` 对应控制台「知识问答」服务页创建的实例，知识检索的 `agent_id` 对应「知识检索」服务页创建的实例。混用将导致 `AgentApp.NotFound` 错误。

## 关键参数

| 参数 | 所属接口 | 必填 | 说明 |
|------|----------|------|------|
| `agent_id` | 两者均需 | 是 | 知识服务实例 ID。**必须与服务类型严格匹配**：问答服务 ID 仅用于 `/api/v2/apps/knowledge/chat`；检索服务 ID 仅用于 `/api/v1/indices/knowledge/search`。 |
| `input.messages` | 知识问答 | 是 | DashScope 标准消息数组，含 `role`（`user`/`assistant`）与 `content`（文本或 `[{"type":"text","text":"..."},{"type":"image_url","image_url":{"url":"..."}}]`）。 |
| `query` / `images` | 知识检索 | 条件必填 | 文本查询字符串或图片 URL 数组（至少传其一）。纯图搜时 `query` 可为空串；非图搜场景下 `query` 必须非空。 |
| `stream` | 知识问答 | 是 | 必须为 `true`；当前版本**仅支持流式响应**，设为 `false` 或省略将导致请求失败。知识检索接口不支持流式。 |
| `parameters.agent_options.session_files` | 知识问答 | 否 | 会话级临时文件 ID 列表（最多 10 个），需在控制台开启「文件预解析」后才生效。文件 ID 通过 `addFile` 接口获取，详见 [添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)。 |

## 使用方式

- **Base URL**：统一为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID。
- **认证**：`Authorization: Bearer <API-Key>`，API Key 需在控制台 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/api-key) 获取。
- **知识问答调用**：
  - Endpoint：`POST /api/v2/apps/knowledge/chat`
  - Header：必须包含 `Accept: text/event-stream`
  - Body：`input`（含 `messages`）、`parameters`（含 `agent_options.agent_id`）、`stream: true`
- **知识检索调用**：
  - Endpoint：`POST /api/v1/indices/knowledge/search`
  - Header：无特殊 `Accept` 要求
  - Body：`agent_id`、`query`（或 `images`）、可选 `agent_version`
- **前置条件**：两个接口均要求对应的知识服务（问答或检索）已在控制台 [知识库服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list) 创建并**发布**，否则返回 `AgentApp.NotFound`。

## 限制和注意事项

- **限流**：默认用户维度 25 QPS，超限返回 HTTP 429，需退避重试。
- **上下文管理**：知识问答接口**不保存对话状态**，每次请求必须传入完整 `messages` 历史（建议限制为最近 10 轮以内），响应不返回 `session_id`。
- **错误处理**：
  - 知识问答：HTTP 层错误（如 401）表示鉴权失败；SSE 流中 `event: error` 帧携带业务错误（如 `AgentApp.NotFound`），需解析 `data:` 内容。
  - 知识检索：**必须校验响应体中的 `success` 字段**（布尔值），而非仅依赖 HTTP 状态码；失败时 `message` 字段提供具体原因。
- > **注意**：知识问答接口的 `usage` 字段（`input_tokens`/`output_tokens` 等）**仅出现在 `tool_calling` 和 `generation_end` 等边界帧中**，普通流式文本片段不携带该字段，不可用于实时 token 统计。

## 来源文档

- [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)
- [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)



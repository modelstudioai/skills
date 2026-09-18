# knowledge

百炼平台的 `knowledge` 能力提供两种核心服务：**知识检索（语义搜索）** 和 **知识问答（RAG 对话）**，分别面向精准切片召回与多阶段推理生成场景。二者均基于已发布的知识库服务（`agent_id`）运行，策略配置在控制台完成，API 层仅需传入意图与服务标识。所有调用均需有效的 API Key 与业务空间上下文。

## 支持的模型/功能

- **知识检索**：跨知识库联合语义检索，支持纯文本、纯图像及图文混合查询，返回按相关性排序的切片列表（含 `score`、`text`、`metadata`）。检索策略（如多库权重、混排模型）完全由控制台发布的 `agent_config` 决定，[知识检索 (raw/application-api-reference/knowledge/knowledgesearch.md)](../../raw/application-api-reference/knowledge/knowledgesearch.md) 中明确说明“其余检索策略一律配置于 `agent_config`，不在请求中暴露”。
- **知识问答**：基于知识库的流式对话接口，执行三阶段 RAG 流程（规划 → 工具调用 → 生成），支持 `semantic_search`、`obtain_file`、`execute_sql` 等内置工具调用，并可串联使用。该能力依赖控制台发布的知识问答服务，[知识问答 (raw/application-api-reference/knowledge/knowledgechat.md)](../../raw/application-api-reference/knowledge/knowledgechat.md) 强调“当前版本仅支持流式响应”，且 `stream` 必须为 `true`。

> **注意**：两文档对 `agent_id` 的描述存在术语差异——文档 1 称其为“知识检索服务（agent）实例 ID”，文档 2 称其为“问答服务（agent）应用 ID”。实际使用中，二者均为控制台对应服务类型（检索/问答）发布后生成的唯一 ID，不可混用。请严格依据服务创建页面（[知识检索服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=retrieval) 或 [知识问答服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=qa)）获取对应 ID。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `agent_id` | string | 是 | 服务 ID，对应控制台发布的知识检索或问答服务实例。**不可跨类型复用**。 | 两文档均强制要求 |
| `query` | string | 条件必填 | 文本检索意图；与 `images` 至少传一个；非纯图搜时必填。 | [知识检索 (raw/application-api-reference/knowledge/knowledgesearch.md)](../../raw/application-api-reference/knowledge/knowledgesearch.md) |
| `images` | array<string> | 条件必填 | 图片 URL 数组（公网可访问）；支持多模态检索。 | 同上 |
| `input.messages` | array<object> | 是（问答） | DashScope 标准消息格式，含 `role`（`user`/`assistant`）与 `content`（支持文本或多模态数组）。 | [知识问答 (raw/application-api-reference/knowledge/knowledgechat.md)](../../raw/application-api-reference/knowledge/knowledgechat.md) |
| `stream` | boolean | 是（问答） | 必须为 `true`；不支持非流式调用。 | 同上 |

> **注意**：知识检索接口不支持 `stream` 参数；知识问答接口**不接受** `query`/`images` 等检索直连参数，所有意图必须封装在 `input.messages` 中。

## 使用方式

- **知识检索**：  
  `POST /api/v1/indices/knowledge/search`，`Content-Type: application/json`，`Authorization: Bearer <API-Key>`。  
  请求体仅含 `agent_id`、`query`、`images`（三者至少提供有效意图）。示例见 [知识检索 (raw/application-api-reference/knowledge/knowledgesearch.md)](../../raw/application-api-reference/knowledge/knowledgesearch.md)。

- **知识问答**：  
  `POST /api/v2/apps/knowledge/chat`，`Content-Type: application/json`，`Accept: text/event-stream`，`Authorization: Bearer <API-Key>`。  
  请求体为三层结构：`input`（含 `messages`）、`parameters`（含 `agent_options.agent_id`）、`stream: true`。必须处理 SSE 流式响应，解析 `event: message` 与 `event: error` 帧。示例见 [知识问答 (raw/application-api-reference/knowledge/knowledgechat.md)](../../raw/application-api-reference/knowledge/knowledgechat.md)。

## 限制和注意事项

- **权限与前置条件**：两者均需有效 API Key 及业务空间 ID；服务必须**先在控制台创建并发布**，否则返回 `Agent 未发布` 错误。
- **限流**：默认用户维度 25 QPS，超限需重试。
- **响应校验**：  
  - 知识检索：**必须校验 `success` 字段**（而非 HTTP 状态码），失败时 `request_id` 用于排查。  
  - 知识问答：错误以 `event: error` 帧返回（含 `code`/`message`/`request_id`），HTTP 401 仅用于鉴权失败。
- **元数据稳定性**：`data.nodes[].metadata` 中以下划线 `_` 开头的字段（如 `_score`, `_rc_v_score`）为内部打分字段，**版本间可能变更，禁止写入业务逻辑**。
- **上下文管理**：知识问答不维护会话状态，`messages` 需传入完整历史，建议限制轮次（如 ≤10）避免超上下文窗口。
- **文件处理**：临时文件上传需在控制台开启“文件预解析”，并通过 `addFile` 接口获取 `file_id` 后，再通过 `parameters.agent_options.session_files` 传入。

## 来源文档

- [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)



# knowledge

百炼平台的 `knowledge` 能力提供两种核心服务：**知识检索（语义搜索）** 和 **知识问答（RAG 对话）**，分别面向精准切片召回与多阶段推理生成场景。二者均基于已发布的知识服务实例（`agent_id`）运行，策略配置与模型选型在控制台完成，API 层仅需传递意图与服务标识。所有调用均需业务空间 ID 与有效 API Key，并遵循统一限流规则。

## 支持的模型/功能

- **知识检索**：跨知识库联合语义检索，支持纯文本、纯图像及图文混合查询，返回按相关性排序的结构化切片（含 `score`、`text`、`metadata`），适用于构建自定义 RAG 流程。详见 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)。
- **知识问答**：端到端流式智能体对话，自动执行规划 → 工具调用（如 `semantic_search`、`obtain_file`）→ 生成三阶段，支持多轮上下文、临时文件注入与多模态输入。详见 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)。
- > **注意**：两接口底层共享同一套知识库索引与向量模型，但检索策略（如混排模型、权重配置）仅在知识检索服务中可配置；知识问答服务不暴露检索策略参数，其工具调用行为由平台自动决策，开发者不可干预。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | 请求体顶层（检索） / `parameters.agent_options.agent_id`（问答） | 是 | 已发布的知识服务实例 ID。检索服务 ID 来自 [知识检索服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=retrieval)，问答服务 ID 来自 [知识问答服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=qa)。 |
| `query` / `images` | 请求体顶层（检索） | 条件必填 | 文本或图片意图，至少传一个。纯图搜时 `query` 可为空串；非纯图搜时 `query` 必填。参见 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)。 |
| `input.messages` | 请求体 `input` 下（问答） | 是 | 完整对话历史，DashScope 标准格式。平台不维护会话状态，需客户端自行管理并截断（建议 ≤10 轮）。 |
| `stream` | 请求体顶层（问答） | 是 | 必须为 `true`，当前版本仅支持流式响应；设为 `false` 或省略将导致请求失败。 |

## 使用方式

- **知识检索**：`POST /api/v1/indices/knowledge/search`，HTTP REST 同步调用，返回完整 JSON 响应。Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，需携带 `Authorization: Bearer <API-Key>` 与 `Content-Type: application/json`。[知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md) 提供了完整的 cURL 与 Python 示例。
- **知识问答**：`POST /api/v2/apps/knowledge/chat`，HTTP REST + SSE 流式调用，`Accept: text/event-stream` 必须声明。响应为 `event: message` / `event: error` 分帧流，需逐行解析。[知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md) 包含详细帧结构与 Python 流式处理示例。
- 两者均要求前置在控制台创建并**发布**对应服务，未发布时返回 `Agent 未发布` 错误；服务配置（如知识库选择、路由规则、混排模型）均在控制台完成，API 不透出。

## 限制和注意事项

- **限流**：默认用户维度 25 QPS，超限返回 HTTP 429，需退避重试。
- **鉴权**：始终校验响应中的 `success` 字段（检索）或 `event: error` 帧（问答），**不可仅依赖 HTTP 状态码**；`401 InvalidApiKey` 表示密钥无效或缺失。
- **字段稳定性**：`data.nodes[].metadata` 中以 `_` 开头的字段（如 `_score_with_weight`, `_rc_v_score`）为内部打分中间值，版本间可能变更，**禁止写入业务逻辑**。
- **问答流式约束**：`stream: true` 为强制要求；`messages` 需包含完整历史，且 `content` 支持多模态数组（如 `[{"type":"text","text":"..."},{"type":"image_url","image_url":{"url":"..."}}]`）。
- > **注意**：文档 1 中 `agent_version` 为可选参数，但文档 2 未提及该字段；当前问答接口不支持指定 `agent_version`，版本控制完全由服务发布行为决定，调用方只需传 `agent_id`。

## 来源文档

- [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)



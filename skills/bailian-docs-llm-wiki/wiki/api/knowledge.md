# knowledge

知识检索与问答功能提供基于向量语义的跨知识库联合检索与端到端智能问答能力，适用于构建 RAG 应用。该能力通过 DashScope 应用网关统一暴露 HTTP REST 接口，与底层 OpenAPI（如 `CreateIndex`、`Retrieve`）在调用方式、鉴权机制和路由层级上存在明确区分。所有接口均需使用业务空间 ID 拼接 Base URL 并携带 API Key 进行 Bearer 鉴权。

## 支持的模型/功能

- **知识检索**：支持跨多个知识库执行联合语义检索，返回按相关性排序的文本切片，适用于预检、召回等场景。详见 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。
- **知识问答（Knowledge Chat）**：支持流式多阶段推理（规划 → 工具调用 → 生成），自动协调知识检索与大模型生成，输出结构化响应。该能力封装了 RAG 全链路逻辑，开发者无需自行编排检索+LLM调用流程，具体行为参见 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)。
- 注意：该能力**不依赖用户显式指定模型名称**，底层模型由平台根据知识库配置与请求上下文动态调度；当前不开放模型切换开关，与 [知识库管理文档](../../raw/application-user-guide/knowledge-base/overview.md) 中提及的“自定义 LLM”描述存在不一致 —— 后者指知识库创建时的 embedding 模型配置，而非问答阶段的生成模型。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_ids` | string[] | 是 | 目标知识库 ID 列表，最多支持 10 个；空数组或缺失将导致 400 错误 |
| `query` | string | 是 | 用户原始查询文本，长度 ≤ 2048 字符 |
| `top_k` | integer | 否 | 检索阶段返回切片数，默认 5，取值范围 1–20 |
| `stream` | boolean | 否 | 是否启用 SSE 流式响应，默认 `false`；仅对 `/api/v2/apps/knowledge/chat` 生效 |

> **注意**：`top_k` 作用于检索阶段，不影响问答生成长度；生成阶段的 `max_tokens` 等参数**不可控**，由服务端统一管理，与 [知识检索与问答](../../raw/application-api-reference/knowledge.md) 中“支持自定义生成参数”的旧版描述矛盾，以当前接口实际行为为准。

## 使用方式

1. **构造 Base URL**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 需从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
2. **设置请求头**：`Authorization: Bearer <API-Key>`，API Key 须从 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 创建并复制；
3. **发送请求**：
   - 检索：`POST /api/v1/indices/knowledge/search`，Body 为 JSON，含 `knowledge_ids` 和 `query`；
   - 问答：`POST /api/v2/apps/knowledge/chat`，Body 同上，可选加 `"stream": true`；
4. 响应格式遵循标准 HTTP 状态码，错误详情见 [知识检索与问答](../../raw/application-api-reference/knowledge.md) 的“错误码”章节。

## 限制和注意事项

- **限流策略**：默认按用户维度限流 25 QPS，超限返回 `429 Too Many Requests`，需客户端实现退避重试；
- **知识库状态要求**：所有 `knowledge_ids` 对应的知识库必须处于 `ACTIVE` 状态，否则请求失败；
- **字符限制**：`query` 超过 2048 字符将被截断并返回 400，不支持分块提交；
- **调试建议**：首次集成时，建议先用非流式问答接口验证知识库召回效果，再启用 `stream=true`；流式响应中各阶段事件类型（`plan`/`tool_call`/`content`）定义见 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)



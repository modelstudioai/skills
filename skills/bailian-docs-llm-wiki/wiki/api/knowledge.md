# knowledge

百炼平台的 `knowledge` 能力提供两种核心服务：面向开发者直接调用的**知识检索（semantic search）**，以及面向对话场景的**知识问答（RAG-based chat）**。二者均基于已发布的知识库服务（`agent_id`）运行，策略配置与模型选型在控制台完成，API 层仅需传递意图和基础参数。所有调用均需有效 API Key 与业务空间上下文。

## 支持的模型/功能

- **知识检索**：跨知识库联合语义检索，支持纯文本、纯图像及[多模态](../concepts/multi-modal.md)混合查询，返回结构化切片列表（含相关性分数、元数据、[多模态](../concepts/multi-modal.md)资源 URL）。检索策略（如多库权重、混排模型、知识路由）完全在控制台 [知识检索服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=retrieval) 配置并发布，API 不暴露策略参数 —— 详见 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)。
- **知识问答**：基于知识库的流式智能问答，采用三阶段执行模型（规划 → 工具调用 → 生成），支持自动选择 `semantic_search`、`obtain_file`、`execute_sql` 等工具，并返回结构化检索结果（`docs` 数组）或全文内容。工具调用逻辑与返回格式由平台统一管理 —— 详见 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)。
- > **注意**：两接口底层均依赖同一套知识库索引与向量模型，但**不支持在 API 请求中动态指定模型名称或版本**；模型选型、rerank 模型、embedding 模型等均由控制台发布的 `agent_config` 决定，API 仅通过 `agent_id` 绑定配置。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `agent_id` | 请求体顶层（检索） / `parameters.agent_options.agent_id`（问答） | `string` | 是 | 已发布的知识服务 ID。检索服务与问答服务 ID 不互通，须分别创建 —— 参考 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md) 和 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md) 文档。 |
| `query` | 请求体顶层 | `string` | 条件必填（检索） | 文本检索意图。与 `images` 至少传其一；非纯图搜时必填。 |
| `images` | 请求体顶层 | `array<string>` | 条件必填（检索） | 图片 URL 数组（公网可访问），支持多图联合检索。 |
| `input.messages` | `input` 对象内 | `array<object>` | 是（问答） | 完整对话历史，DashScope 标准格式。平台不维护会话状态，必须显式传入全部轮次。 |
| `stream` | 请求体顶层 | `boolean` | 是（问答） | **必须为 `true`**；当前版本仅支持 SSE 流式响应，设为 `false` 或省略将导致请求失败。 |

## 使用方式

- **知识检索**（HTTP POST）：
  - Endpoint：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`
  - Headers：`Authorization: Bearer <API-Key>`, `Content-Type: application/json`
  - Body 示例：
    ```json
    {
      "agent_id": "aid-xxxxxxxxxxxxxxxx",
      "query": "推荐一件适合秋冬的运动夹克",
      "images": []
    }
    ```
- **知识问答**（SSE HTTP POST）：
  - Endpoint：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`
  - Headers：`Authorization: Bearer <API-Key>`, `Content-Type: application/json`, `Accept: text/event-stream`
  - Body 示例：
    ```json
    {
      "input": {
        "messages": [{"role": "user", "content": "什么是百炼知识库？"}]
      },
      "parameters": {
        "agent_options": { "agent_id": "aid-xxxxxxxxxxxxxxxx" }
      },
      "stream": true
    }
    ```
- 两接口均要求 `workspaceId` 从控制台业务空间获取，且 API Key 需具备对应空间权限 —— 具体配置路径见 [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md) 和 [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md) 的“权限要求”章节。

## 限制和注意事项

- **限流**：默认用户维度 25 QPS，超限返回 `429 Too Many Requests`，需客户端重试。
- **错误处理**：
  - 知识检索：**必须校验响应体 `success` 字段**（而非 HTTP 状态码），失败时 `message` 提供具体原因。
  - 知识问答：错误以 `event: error` SSE 帧返回（含 `code`/`message`/`request_id`），HTTP 层仅对鉴权失败（`401`）等极少数情况返回状态码。
- **字段稳定性**：
  - 响应中以 `_` 开头的字段（如 `_score`, `_rc_v_score`, `_knowledge_type`）为内部打分或元数据字段，**版本间可能变更，禁止写入业务逻辑**。
  - 表格型知识库返回的业务字段（如 `product_id`）由用户表结构决定，不在标准文档定义范围内。
- > **注意**：知识问答接口的 `parameters.agent_options.session_files` 仅在控制台开启“文件预解析”后生效，且文件 ID 必须通过 `addFile` 接口注册 —— 该能力依赖 [添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md) 文档所述流程，未启用时传入无效。

## 来源文档

- [知识检索](../../raw/application-api-reference/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/knowledge/knowledgechat.md)



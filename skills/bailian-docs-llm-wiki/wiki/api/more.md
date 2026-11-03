# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务关联角色管理、临时认证机制与高级知识库检索控制等关键基础设施功能。这些能力不直接暴露为独立模型或 API，而是支撑工作流编排、安全存储、RAG 精准检索及可观测性等核心场景的底层依赖。开发者需按需启用并理解其权限边界与生命周期约束。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下功能模块提供必要支撑：

- **服务关联角色（SLR）**：自动创建并托管跨云服务访问权限，支撑[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)调用函数计算（FC）、[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)导入 OSS 数据、[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)对接 ADB-PG 与 OSS、[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)集成 OpenTelemetry 等场景。
- **临时 API Key**：用于不可信前端环境的安全鉴权，避免永久密钥泄露，适用于浏览器、移动 App 等客户端直连调用。
- **知识库 SearchFilters**：在 `Retrieve` 接口上提供结构化过滤能力，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 检索精度，尤其适用于员工信息表等结构化数据场景。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒（默认 60） |
| SearchFilters（OpenAPI） | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为平铺 key-value Map | 子分组内字段默认 `AND`；支持 `_operator: "OR"` |
| SearchFilters（RAG API / Spring AI SDK） | `_operator`, `_conditions` | string, array | 否 | 支持嵌套条件与多条件 OR，如 `{ "_operator": "OR", "_conditions": [{ "field": "val" }, { "field": { "like": "%x%" } }] }` | `_operator` 可为 `"AND"` 或 `"OR"`（大小写不敏感） |

> **注意**：OpenAPI Retrieve 的 `searchFilters` 不支持嵌套 `_conditions`；若传入嵌套结构，请求可能成功但**实际不生效**，结果未按预期过滤 —— 详见 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) 文档中“语法说明”章节。

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间）时，百炼自动为您创建所需 SLR。角色名称与策略均预置，权限最小化且不可修改。详情请参阅 [服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)。
- **生成临时 API Key**：通过后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，可选 `expire_in_seconds` 查询参数。响应返回 `token` 与 `expires_at`（UNIX 时间戳）。该能力在 [生成临时API Key](raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 中有完整示例。
- **使用 SearchFilters**：在调用 `Retrieve` 接口时，将过滤条件以 JSON 数组形式赋值给 `searchFilters` 字段。注意根据调用方式（OpenAPI / RAG API / Spring AI SDK）选择对应语法：OpenAPI 仅支持平铺 Map；RAG API 与 Spring AI SDK 支持 `_conditions` 嵌套与 `_operator` 控制逻辑关系。

## 限制和注意事项

- **服务关联角色不可手动删除**：部分 SLR（如 `AliyunServiceRoleForSFMAccessingMNS`）明确声明“请勿修改、删除，或将其授予除服务关联角色之外的任何 RAM 身份”。其他 SLR 删除前必须先解除所有依赖（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止数据导入任务），否则功能立即中断。
- **临时 API Key 无法主动撤销**：其生命周期完全由 `expire_in_seconds` 决定，到期自动失效，不支持手动吊销或提前删除。
- **SearchFilters 字段类型强约束**：单值/多值查询仅支持 `string` 或数值（`long`/`double`）；范围查询（`gt`/`gte` 等）仅支持数值；模糊查询（`like`）仅支持 `string`；标签查询仅限文档/音视频类知识库。字段名必须与知识库 Schema 中定义的字段严格一致。
- **地域隔离**：临时 API Key 的生成 Endpoint 与所用永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将返回 `InvalidApiKey` 错误 —— 此限制在 [生成临时API Key](raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 中已强调。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



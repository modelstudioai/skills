# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大类功能。它不构成独立服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心场景的底层基础设施。开发者需根据具体使用场景按需启用对应能力，并严格遵循权限最小化原则配置服务关联角色或临时凭证。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供关键支撑能力：

- **服务集成**：通过服务关联角色（SLR）实现与 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等云服务的安全对接，支撑[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)、[流程编排](https://help.aliyun.com/zh/model-studio/what-is-process-orchestration-old)、[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)、[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)、[创建和使用知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)等场景 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **安全调用**：提供生成临时 API Key 的能力，用于在浏览器、移动 App 等不可信前端环境安全调用后端模型服务 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **精准检索**：支持在知识库 `Retrieve` 接口请求中传入 `searchFilters`，对语义检索结果进行结构化过滤，提升 RAG 效果 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMAccessFC` 权限范围（仅 `fc:ListFunctions` 和 `fc:InvokeFunction`）与实际工作流中函数节点可能需要的 `fc:GetFunction`、`fc:CreateFunction` 等管理类操作存在潜在不一致；生产环境应以控制台实际策略绑定为准，必要时通过自定义策略补充。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| 知识库检索 | `searchFilters` | Array of Object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND 关系），子分组内字段默认 AND，可设 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| 知识库检索（RAG API） | `_conditions` | Array of Object | 否 | 子分组内嵌套条件数组，支持同一字段多条件（如 `eq` + `like`） | `[{"department": "Corporate"}, {"department": {"like": "%Research%"}}]` |

## 使用方式

- **服务关联角色**：首次在控制台启用对应功能（如添加函数计算节点、导入 OSS 数据、配置 ADB-PG 安全存储）时，系统自动创建所需 SLR；无需手动调用 API。角色名称与策略已预置，详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久AK>` 的 POST 请求，可选 `?expire_in_seconds=N` 查询参数。响应返回 `token`（临时密钥）和 `expires_at`（Unix 时间戳）。
- **SearchFilters**：
  - OpenAPI Retrieve（`bailian.cn-beijing.aliyuncs.com/{WorkspaceId}/index/retrieve`）：`searchFilters` 为平铺 Map 数组，支持 `_operator` 控制子分组内逻辑，**不支持嵌套 `_conditions`**。
  - RAG API / Spring AI Alibaba SDK（`{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`）：支持 `_conditions` 嵌套及 `like`/`eq`/`gte` 等丰富操作符，推荐用于复杂过滤场景。

## 限制和注意事项

- **服务关联角色**：
  - 删除 SLR 前必须先解除所有依赖该角色的功能（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止数据导入任务），否则对应功能将立即失效 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止手动修改或删除，因其由平台内部托管。
- **临时 API Key**：
  - 临时 Key 继承生成它的永久 AK 的**全部权限**（含模型访问、知识库读写等），务必确保源 AK 权限最小化。
  - 无法主动撤销，仅能等待过期；最长 TTL 为 1800 秒（30 分钟）。
- **SearchFilters**：
  - OpenAPI SDK 的 `SearchFilters` 字段类型为 `Map<String, String>`，若传入嵌套 JSON 或重复字段名，将被静默忽略或导致未预期行为，**必须使用平铺结构**。
  - 字段名必须与知识库 Schema 中定义的字段完全一致（区分大小写），且仅支持已开启“参与检索”的字段。
  - 标签（Tag）查询仅适用于文档搜索、音视频搜索类知识库，不适用于数据表类知识库。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



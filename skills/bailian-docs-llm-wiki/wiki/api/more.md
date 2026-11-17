# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不构成独立服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心功能的底层基础设施。开发者需根据具体使用场景（如调用函数计算、访问 OSS 数据、过滤 RAG 检索结果）按需启用对应能力，并严格遵循权限最小化与生命周期管理原则。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下关键功能提供支撑能力：

- **服务集成**：通过服务关联角色（SLR）实现与 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等云服务的安全对接，支撑[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)、[流程编排](https://help.aliyun.com/zh/model-studio/what-is-process-orchestration-old)、[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)、[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)、[创建和使用知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)等场景；  
- **安全认证**：提供临时 API Key 生成能力，用于在不可信前端环境（如浏览器、移动 App）中安全调用模型服务；  
- **高级检索**：支持 `searchFilters` 参数，在知识库 `Retrieve` 接口调用中对语义检索结果进行结构化过滤，提升 RAG 精准度，尤其适用于员工信息表等结构化数据场景 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列举的 `AliyunServiceRoleForSFMAccessFC` 权限范围（仅 `fc:ListFunctions` 和 `fc:InvokeFunction`）与实际工作流节点所需能力可能存在收敛偏差——例如异步回调、日志拉取等运维操作可能依赖额外权限，建议结合[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)最新实践验证。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| 知识库检索 | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为子分组（Map 或含 `_operator`/`_conditions` 的对象） | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| 知识库检索（RAG API） | `_operator` | string | 否 | 子分组内条件逻辑，支持 `"AND"`（默认）、`"OR"` | `"OR"` |
| 知识库检索（RAG API） | `_conditions` | array of object | 否 | 支持嵌套多条件（如 `like`、`gte`/`lte`），仅 RAG API 与 Spring AI SDK 支持 | `[{"department": "Corporate"}, {"department": {"like": "%Research%"}}]` |

## 使用方式

- **服务关联角色**：首次开通对应功能（如函数计算节点、OSS 数据导入）时，系统自动创建 SLR；无需手动调用 API。角色名称与策略已固化，详见 [服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)；  
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，可选传入 `expire_in_seconds` 查询参数；  
- **SearchFilters**：在 `Retrieve` 请求体中添加 `searchFilters` 字段。语法因调用方式而异：  
  - OpenAPI（`bailian.cn-beijing.aliyuncs.com/{WorkspaceId}/index/retrieve`）：仅支持平铺 Map，不支持 `_conditions` 嵌套；  
  - RAG API（`{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`）与 Spring AI Alibaba SDK：支持 `_operator` 和 `_conditions`，可表达复杂逻辑 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色**：  
  - 删除 SLR 将导致对应功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后无法创建/调用函数计算节点），且删除前必须清理所有依赖资源（如已发布的应用、进行中的导入任务、已配置的连接）；  
  - 所有 SLR 均由百炼平台定义，**禁止手动修改其策略或授予非 SLR 身份**（如 `AliyunServiceRoleForSFMAccessingMNS` 明确禁止授予其他 RAM 身份）；  
- **临时 API Key**：  
  - 继承父 Key 全部权限（含模型/知识库访问限制），**不可降权**；  
  - 不可手动删除，仅能等待自动过期；  
- **SearchFilters**：  
  - OpenAPI SDK 不支持同一字段多条件 OR（如 `{"age": {"gte": 25, "lte": 35}}` 有效，但 `{"age": {"gte": 25}}` 和 `{"age": {"lte": 35}}` 分属不同子分组时将被解释为 AND）；  
  - 字段名必须与知识库 Schema 中定义的字段名**完全一致且大小写敏感**；  
  - 标签（Tag）查询仅适用于文档搜索、音视频搜索类知识库，不适用于数据查询类知识库。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



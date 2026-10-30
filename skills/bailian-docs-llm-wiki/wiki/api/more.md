# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大类功能。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、可观测性集成等关键场景的底层基础设施。开发者需根据具体使用场景（如调用函数计算、访问OSS数据、生成临时凭证或过滤RAG结果）选择对应能力并配置相应权限或参数。

## 支持的模型/功能

`more` 本身**不提供模型**，而是为以下平台功能提供支撑能力：

- **服务关联角色（SLR）**：支撑工作流应用调用函数计算（FC）、数据管理接入OSS/MNS、安全存储空间连接ADB-PG、用量监控对接OpenTelemetry/SLS/CMS、内容安全审核、DTS数据同步、模型调优访问CPFS/OSS等 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时API Key**：为前端/移动端等不可信环境提供短期、可管控的访问凭证，用于调用模型服务或知识库API [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters**：在知识库 `Retrieve` 接口请求中嵌入结构化过滤条件，实现对语义检索结果的字段级精准筛选（如按姓名、岗位、年龄范围等过滤），显著提升RAG召回质量 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档1中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失完整JSON），实际策略应以RAM控制台或最新版帮助文档为准；其他SLR策略均完整给出，可直接参考。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时API Key | `expire_in_seconds` | Integer | 否 | 指定临时[Token](../concepts/token.md)有效期（TTL） | `[1, 1800]` 秒（默认60秒） |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为一个Key-Value Map（支持 `_operator: "OR"`） | 单层Map，不支持 `_conditions` 嵌套 |
| SearchFilters（RAG API / Spring AI SDK） | `search_filters` | Array of Object | 否 | 过滤条件数组，支持 `_operator` + `_conditions` 嵌套结构 | 支持 `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like` 等操作符 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、配置OSS数据源）时，系统自动创建SLR；无需手动调用API。角色名称与权限策略已固化，详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口调用，需在Header中携带 `Authorization: Bearer <永久API Key>`，支持地域Endpoint切换（北京/新加坡/弗吉尼亚/中国香港）。
- **SearchFilters**：
  - OpenAPI Retrieve：在 `RetrieveRequest.search_filters` 中传入平铺Map数组（如 `[{"姓名": "张三"}, {"岗位": "技术员"}]`）；
  - RAG API 或 Spring AI SDK：支持更复杂语法，例如 `{"_operator": "OR", "_conditions": [{"部门": "Corporate"}, {"部门": {"like": "%Research%"}}]}`。

## 限制和注意事项

- **SLR删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流中所有函数计算节点无法调用）。删除前必须先解除依赖（如删除节点、断开OSS/ADB连接、停止导入任务）。
- **临时API Key不可撤销**：生成后无法主动删除或禁用，仅能等待过期；其权限严格继承自签发用的永久API Key，**切勿在客户端硬编码永久Key生成临时[Token](../concepts/token.md)**。
- **SearchFilters兼容性差异**：
  - OpenAPI SDK 仅支持平铺Map，**不支持 `_conditions` 嵌套**；若误传嵌套结构，请求可能成功但过滤逻辑不生效；
  - RAG API 和 Spring AI SDK 支持完整语法，包括同一字段多条件OR（如 `{"department": {"like": "%A%"}, "department": {"like": "%B%"}}` 需置于同一 `_conditions` 数组内）。
- **权限最小化原则**：SLR策略已按功能最小化设计（如 `AliyunServiceRoleForSFMDataHubOSSImport` 仅允许读取带特定Bucket Tag的OSS资源），但开发者仍需定期审计RAM角色策略，避免过度授权。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



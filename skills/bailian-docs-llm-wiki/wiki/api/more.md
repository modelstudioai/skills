# more

`more` 是百炼平台为高级用例提供的扩展能力集合，涵盖服务权限治理、安全凭证分发与知识库精准检索三大方向。它不构成独立 API 服务，而是以配套机制形式支撑工作流、数据接入、RAG 等核心场景的合规性与可控性。开发者需结合具体功能上下文（如知识库检索、函数计算节点调用）按需启用。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下关键功能提供底层支持：

- **服务关联角色（SLR）**：支撑百炼与外部云服务的受控交互，包括函数计算（FC）、OSS、ADB-PG、MNS、SLS、CMS、内容安全等。例如，`AliyunServiceRoleForSFMAccessFC` 使工作流应用能安全调用用户 FC 函数 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；`AliyunServiceRoleForSFMDataHubOSSImport` 支持数据管理模块从带标签的 OSS Bucket 导入数据。
- **临时 API Key 生成**：为不可信前端环境（如浏览器、App）提供短期凭证，避免永久密钥泄露，适用于所有支持 `Authorization: Bearer <token>` 的百炼 API [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口上实现结构化过滤，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 结果相关性，尤其适用于员工信息表、制度文档等结构化知识库 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForAccessOSS` 的权限描述（允许 `PutObject`/`DeleteObject`）与文档 3 中知识库检索场景的只读需求存在粒度不匹配。实际使用中，该角色应仅在“安全存储空间”启用写入时才需完整权限；若仅用于知识库元数据读取（如 `ListObjects`），建议通过 RAM 自定义策略最小化授权。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 有效期（秒） | `[1, 1800]`，默认 `60` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为平铺 Key-Value Map | 子分组内字段默认 `AND`；设 `_operator: "OR"` 可切换逻辑 |
| SearchFilters（RAG API / Spring AI） | `_conditions` | Array of Object | 否 | 嵌套条件数组，支持同一字段多条件（如 `eq` + `like`） | 需配合 `_operator` 使用 |

## 使用方式

- **服务关联角色**：首次开通对应功能（如添加 FC 节点、配置 OSS 数据源）时由系统自动创建，无需手动调用 API。角色名称与用途严格绑定，详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档中的表格。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。地域 Endpoint 需与生成该 API Key 的地域一致（北京/新加坡/弗吉尼亚/中国香港）。
- **SearchFilters**：
  - OpenAPI Retrieve：直接在 `RetrieveRequest.search_filters` 字段传入 JSON 数组（如 `[{"姓名": "张三"}, {"岗位": "技术员"}]`）。
  - RAG API 或 Spring AI SDK：使用嵌套 `_conditions` 结构（如 `{"_operator": "OR", "_conditions": [{"department": "Corporate"}, {"document_type": {"like": "%Policy%"}}]}`）。

## 限制和注意事项

- **服务关联角色删除风险**：删除任一 SLR 均将导致其关联功能立即失效（如删 `AliyunServiceRoleForSFMAccessFC` → 工作流无法调用 FC）。删除前必须先解除所有依赖资源（如删除函数节点、断开 OSS/ADB 连接），否则操作被拒绝 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，不支持主动吊销或刷新。敏感场景应严格控制 `expire_in_seconds` 时长。
- **SearchFilters 兼容性差异**：
  - OpenAPI SDK **不支持** `_conditions` 嵌套，传入将被忽略；同一字段多条件需拆分为多个子分组（AND 语义）或改用 RAG API。
  - RAG API 和 Spring AI SDK 支持完整语法，但 `_operator` 作用域仅限其所在 `_conditions` 数组，数组间仍为 AND。
- **权限继承**：临时 API Key 完全继承源 API Key 的权限边界（含模型白名单、知识库访问控制），无额外限制能力。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、安全凭证分发、知识库高级检索等关键功能。它不构成独立服务，而是支撑工作流编排、数据接入、模型监控、RAG 等核心场景的底层基础设施。开发者需根据具体使用场景（如调用函数计算、导入 OSS 数据、过滤检索结果）按需启用对应能力，并严格遵循权限最小化与生命周期管理原则。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下平台功能提供必要支撑：

- **服务关联角色（SLR）**：自动创建并托管跨云服务访问权限，支撑工作流应用调用函数计算（FC）、知识库对接 ADB-PG、OSS 数据导入、MNS 消息监听、OpenTelemetry 监控上报等。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）提供短期有效的认证凭据，避免永久密钥泄露风险。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精准筛选，显著提升 RAG 输出相关性，尤其适用于结构化数据表（如员工信息表）场景。详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中将 `AliyunServiceRoleForSFMAccessADB` 的应用场景描述为“[创建和使用知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)和[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)”，但文档 3 的前置步骤明确要求知识库需配置为“数据查询”类型并依赖 ADB-PG 向量引擎；而标准 RAG 知识库（非数据查询型）通常不强制依赖该 SLR。实际使用中，仅当知识库类型为“数据查询”且后端存储为 ADB-PG 时，才需此角色。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 临时 [Token](../concepts/token.md) 有效期（秒） | `[1, 1800]`，默认 `60` |
| SearchFilters（OpenAPI） | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为 key-value 映射 | 子分组内字段默认 `AND`；支持 `_operator: "OR"` |
| SearchFilters（RAG API / Spring AI） | `_operator`, `_conditions` | string, array | 否 | 支持同一字段多条件 OR（如 `{"department": {"like": "%Research%"}}`）及嵌套逻辑 | `_operator` 可为 `"AND"` 或 `"OR"` |

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用对应功能（如在工作流中添加 FC 节点、在数据管理中配置 OSS 导入源、在安全存储空间中绑定 ADB-PG 实例）时，百炼自动为您创建所需 SLR。角色名称与策略均已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档中明确定义。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口调用，需在请求头 `Authorization: Bearer <permanent_api_key>` 中携带有效永久密钥。各地域 Endpoint 不同，新加坡、北京、弗吉尼亚、中国香港需分别使用对应域名。
- **SearchFilters**：
  - OpenAPI Retrieve：直接在 `RetrieveRequest.search_filters` 字段传入平铺 Map 数组（如 `[{"姓名": "张三"}, {"岗位": "技术员"}]`），**不支持嵌套 `_conditions`**。
  - RAG API / Spring AI SDK：支持完整语法，包括 `_operator` 和 `_conditions` 数组，可表达复杂逻辑（如 `{"_operator": "OR", "_conditions": [{"部门": "Corporate"}, {"部门": {"like": "%Research%"}}]}`）。详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的 FC 节点无法调用）。删除前必须先解除所有业务依赖（如删除 FC 节点、断开 OSS/ADB-PG 连接、停止数据导入任务），否则操作将被拒绝。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持手动删除或提前吊销**。请严格控制 TTL 时长，避免在高敏感场景设置过长有效期。
- **SearchFilters 兼容性差异**：OpenAPI SDK 的 `search_filters` 字段仅接受平铺 Map，若传入含 `_conditions` 的嵌套结构，请求可能成功但**过滤逻辑不生效**。务必根据所用接口（OpenAPI vs RAG API）选择对应语法。
- **权限继承与最小化**：临时 API Key 继承其父密钥的全部权限（含模型、知识库访问限制），请勿使用高权限主账号密钥生成前端 [Token](../concepts/token.md)。子账号使用知识库 API 前，须确保已授予 `AliyunBailianDataFullAccess` 策略并加入目标业务空间。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



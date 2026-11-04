# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制等关键功能。它不构成独立服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心场景的底层基础设施。开发者需根据具体使用场景按需启用并正确配置相关组件。

## 支持的模型/功能

`more` 本身不提供模型，但为以下功能提供必要支撑：

- **服务关联角色（SLR）**：自动创建并管理百炼访问其他阿里云服务所需的最小权限角色，如函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry 等。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用 FC 函数；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 访问 OSS 与 ADB-PG 实例；[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)依赖 `AliyunServiceRoleForSFMTelemetry` 接入 OpenTelemetry。  
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）的安全鉴权方案，通过后端调用 `/api/v1/tokens` 接口签发短期有效凭证。  
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精准筛选，显著提升 RAG 场景下结构化数据的召回准确率。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 的说明称“本策略由大模型服务平台百炼定义并使用，请勿修改、删除”，但其他 SLR（如 `AliyunServiceRoleForSFMAccessFC`）均明确允许用户在满足前提条件下删除。该表述存在一致性风险，实际操作应以各角色章节的「删除服务关联角色」子节为准，而非通用声明。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围 | 来源 |
|------|--------|------|------|-----------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 临时 Token 有效期（TTL） | `[1, 1800]` 秒（默认 60） | [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| SearchFilters（OpenAPI） | `_operator` | String | 同一子分组内多字段逻辑关系 | `"AND"`（默认）、`"OR"` | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| SearchFilters（RAG API / Spring AI） | `_conditions` | Array | 支持嵌套的多条件数组，可混合等值、模糊、范围查询 | 见语法说明 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| SearchFilters（通用） | 字段值 | String / Number / Array / Object | 支持单值、多值（JSON 数组字符串）、`{"like": "..."}`、`{"gte": x, "lte": y}` 等格式 | 依字段 Schema 而定 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

## 使用方式

- **服务关联角色**：首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间）时，系统自动创建 SLR。无需手动调用 API，但需确保主账号或具备 `ram:CreateServiceLinkedRole` 权限的 RAM 用户执行开通操作。  
- **临时 API Key**：后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久AK>` 的 POST 请求，可选传 `expire_in_seconds`。响应返回 `token` 与 `expires_at`（UNIX 时间戳）。  
- **SearchFilters**：在 `Retrieve` 请求体中以 JSON 数组形式传入 `searchFilters` 字段。**必须注意调用方式与语法的严格匹配**：  
  - OpenAPI SDK（`bailian20231229`）仅支持平铺 Map，不支持 `_conditions` 嵌套；  
  - RAG API 与 Spring AI Alibaba SDK 支持完整嵌套语法（`_operator` + `_conditions`）；  
  - 同一字段多条件 OR 查询在 OpenAPI 中需通过 `_operator: "OR"` 并列字段实现，在 RAG API 中需放入 `_conditions` 数组。

## 限制和注意事项

- **服务关联角色**：  
  - 删除 SLR 前**必须**解除其依赖功能（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止数据导入任务），否则对应功能将立即失效；  
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止用户删除（见文档 1），而其他 SLR 均提供删除指引，此差异需特别关注；  
  - 所有 SLR 均绑定特定服务主体（如 `fc.sfm.aliyuncs.com`），不可复用或手动附加至其他服务。  
- **临时 API Key**：  
  - 无法提前撤销，仅能等待自然过期；  
  - 权限完全继承自签发所用的永久 API Key，**切勿使用高权限 AK 签发前端可用 Token**；  
  - 各地域 Endpoint 独立（北京、新加坡、弗吉尼亚、中国香港），密钥不互通。  
- **SearchFilters**：  
  - OpenAPI SDK 不支持同一字段多个独立条件（如 `{"age": {"gt": 25}}` 和 `{"age": {"lt": 35}}` 需合并为 `{"age": {"gt": 25, "lt": 35}}` 或使用 RAG API）；  
  - 字段名必须与知识库 Schema 中定义的字段名**完全一致**（区分大小写）；  
  - 多值查询需传入 JSON 字符串（如 `json.dumps(["张三", "李四"])`），而非原生数组。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



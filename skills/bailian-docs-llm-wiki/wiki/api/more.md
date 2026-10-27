# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖临时凭证管理、服务关联角色（SLR）授权、以及知识库检索增强等功能。这些能力不直接参与模型推理主流程，但对安全调用、跨云资源集成和精准语义检索至关重要。开发者需根据具体场景选择启用，并严格遵循权限最小化原则。

## 支持的模型/功能

- **临时 API Key 生成**：用于在浏览器、移动端等不可信环境安全调用模型服务，避免永久密钥泄露。该能力本身不绑定特定模型，而是为所有支持 `Authorization: Bearer <token>` 的百炼 API 提供鉴权支撑 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色（SLR）**：百炼通过预定义 SLR 访问其他阿里云服务（如 FC、OSS、ADB-PG、MNS、SLS 等），支撑工作流[函数调用](../concepts/function-calling.md)、OSS 数据导入、安全存储空间、知识库向量化、用量监控等核心功能 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行后置精确筛选，显著提升结构化数据（如员工表、制度文档）的召回准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}` 和完整 `Statement`），实际策略应以 RAM 控制台或最新版 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档为准。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 示例值 |
|------|--------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters（OpenAPI） | `searchFilters` | array of object | 平铺 Map 形式子分组，支持 `_operator: "OR"`，**不支持嵌套 `_conditions`** | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API / Spring AI SDK） | `search_filters` | array of object | 支持 `_operator` + `_conditions` 嵌套，支持同一字段多条件（如 `eq` + `like`） | `[{"_operator":"OR","_conditions":[{"department":"Corporate"},{"department":{"like":"%Research%"}}]}]` |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。地域 Endpoint 需与生成所用永久 Key 一致（北京/新加坡/弗吉尼亚/中国香港）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色**：首次开通对应功能（如函数计算节点、OSS 导入）时由系统自动创建；手动删除前必须先解除所有依赖（如删除工作流中的 FC 节点、断开安全存储空间的 OSS 连接）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **SearchFilters**：在 `Retrieve` 请求体中添加 `searchFilters` 字段。**务必注意调用方式差异**：OpenAPI SDK 仅接受平铺 Map；RAG API 和 Spring AI SDK 支持嵌套 `_conditions`。错误使用嵌套结构将导致过滤失效 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 3 中“同一字段的多条件 OR 查询（OpenAPI Retrieve）”示例代码使用了 `_operator: "OR"` 与字段并列的写法，但明确指出 OpenAPI SDK **不支持嵌套 `_conditions`**；而后续 RAG API 示例则正确使用了 `_conditions` 数组。开发者必须严格匹配所选 SDK 的语法规范，混用将导致过滤逻辑未生效。

## 限制和注意事项

- **临时 API Key**：继承父 Key 全部权限，无法做细粒度权限降级；生命周期固定，到期自动失效，**不可手动删除**；各地域 Key 不互通 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色**：删除 SLR 将导致依赖功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用 FC 函数）；部分 SLR（如 `AliyunServiceRoleForSFMAccessingMNS`）明确禁止手动修改或删除。  
- **SearchFilters**：仅作用于 `Retrieve` 接口返回的 `nodes` 列表，不影响语义相似度计算过程；字段名必须与知识库 Schema 中定义的字段名**完全一致（大小写敏感）**；多值查询需对数组 `json.dumps` 后作为字符串传入（OpenAPI 方式）。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



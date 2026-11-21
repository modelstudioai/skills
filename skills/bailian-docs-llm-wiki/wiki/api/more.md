# more

`more` 是百炼平台为开发者提供的扩展能力集合，涵盖服务权限管理、知识库高级检索控制、临时认证机制等关键功能。这些能力不直接参与模型推理主流程，但对构建安全、可控、可观察的企业级 AI 应用至关重要。本文档面向开发者，聚焦其技术实现细节与集成约束。

## 支持的模型/功能

`more` 并非模型名称或推理能力，而是百炼平台中一组支撑性功能模块的统称，主要包括：

- **服务关联角色（SLR）管理**：用于授予百炼访问其他阿里云服务（如 FC、OSS、ADB-PG、MNS、SLS 等）所需的最小权限。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算资源；[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)使用 `AliyunServiceRoleForSFMDataHubOSSImport` 导入 OSS 数据；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)通过 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 访问受控的 OSS 与 ADB-PG 实例。完整列表详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

- **知识库高级检索过滤（SearchFilters）**：在调用 `Retrieve` 接口时，通过结构化 `searchFilters` 字段对语义检索结果进行后置过滤，支持单值、多值、范围、模糊及标签查询，显著提升结构化数据场景下的召回精度。该能力适用于 OpenAPI、RAG API 及 Spring AI Alibaba SDK 等多种调用方式。

- **临时 API Key 生成**：为在不可信前端环境（如浏览器、移动 App）中安全调用模型服务而设计，后端服务可基于永久 API Key 动态签发带 TTL 的短期凭证，避免长期密钥泄露风险。

> **注意**：文档 1 中将 `AliyunServiceRoleForSFMTelemetry` 关联至“用量监控与性能分析”，但其策略定义在文档末尾被截断，权限内容不完整；实际部署前请以 RAM 控制台中该策略的最新版本为准。

## 关键参数

- **SearchFilters**：  
  - 类型：`Array<Object>`，每个 Object 为一个子分组（AND 语义）。  
  - 子分组内支持 `_operator: "AND" | "OR"`（默认 AND）；RAG API/Spring AI 支持嵌套 `_conditions` 实现同一字段多条件 OR。  
  - 字段值支持：字符串（`"field": "value"`）、数值范围（`"field": {"gte": 20, "lte": 30}`）、模糊匹配（`"field": {"like": "%Research%"}`）、多值数组（需 JSON 序列化为字符串，如 `"field": "[\"A\",\"B\"]"`）。  
  - 详见 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

- **临时 API Key 请求参数**：  
  - `expire_in_seconds`：TTL，整数，取值范围 `[1, 1800]` 秒，默认 `60`。  
  - `Authorization: Bearer <permanent_api_key>`：必须使用永久 API Key 签发，临时 Token 继承其全部权限。  
  - 地域 Endpoint 需与永久 API Key 所属地域一致（北京、新加坡、弗吉尼亚、中国香港），详见 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 使用方式

- **服务关联角色**：系统在首次启用对应功能（如创建函数计算节点、配置 OSS 数据源）时自动创建，无需手动申请。开发者需确保目标云服务（如 FC、OSS Bucket）已按文档要求打上指定 Tag（如 `bailian-datahub-access: read`），否则权限校验失败。

- **SearchFilters**：  
  - OpenAPI：在 `RetrieveRequest.search_filters` 中传入平铺 Map 数组，不支持 `_conditions` 嵌套。  
  - RAG API / Spring AI Alibaba：支持完整语法，包括 `_operator` 和 `_conditions`，推荐用于复杂过滤逻辑。  
  - 必须前置完成：子账号需具备 `AliyunBailianDataFullAccess` 权限并加入对应业务空间；知识库字段需已配置为可检索类型。

- **临时 API Key**：  
  - 后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization` 头的 POST 请求。  
  - 将响应中的 `token` 字段值作为 `Authorization: Bearer <temp_token>` 用于后续模型调用（如 `/api/v1/services/aigc/text-generation/generation`）。  
  - 过期时间由 `expires_at` 返回，客户端应缓存并在失效前重新签发。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能（如工作流中函数计算节点）完全不可用。删除前必须先解除所有业务绑定（如删除函数节点、断开 OSS/ADB-PG 连接），否则操作被拒绝。详情见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

- **SearchFilters 兼容性差异**：OpenAPI Retrieve 不支持同一字段多条件 OR（如 `{"age": {"gte": 20, "lte": 30}}` 与 `{"age": {"eq": 25}}` 并存），仅能通过 RAG API 或 Spring AI Alibaba 实现。若误在 OpenAPI 中传入嵌套 `_conditions`，请求虽可能成功，但过滤逻辑将被忽略。

- **临时 API Key 不可撤销**：生命周期由 `expire_in_seconds` 决定，到期自动失效，**无法手动删除或提前吊销**。敏感场景应严格控制 TTL 时长，并避免在前端持久化存储。

- **权限继承原则**：临时 API Key 的权限范围完全等同于签发它的永久 API Key。若永久 Key 仅授权访问特定知识库，则临时 Key 也无法访问其他知识库；反之，若永久 Key 权限过大，临时 Key 即构成越权风险。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)



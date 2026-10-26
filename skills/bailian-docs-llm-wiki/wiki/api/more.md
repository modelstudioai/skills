# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全凭证分发、知识库高级检索等关键功能。这些能力不直接参与模型推理，但为应用构建、数据治理与系统集成提供基础设施支撑。开发者需根据具体场景按需启用，并严格遵循最小权限原则配置关联资源。

## 支持的模型/功能

`more` 不对应具体模型，而是支撑以下核心功能模块：

- **服务关联角色（SLR）**：为百炼子系统（如工作流、数据管理、安全存储空间、模型监控等）自动申请并托管对其他云服务的访问权限，例如函数计算（FC）、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry 和内容安全服务。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、移动 App）提供短期有效的认证凭据，避免永久密钥泄露风险。
- **知识库 SearchFilters**：在 `Retrieve` 接口调用中嵌入结构化过滤条件，实现语义检索结果的精准裁剪，尤其适用于结构化数据（如员工信息表、制度文档库）。该能力深度集成于 OpenAPI、RAG API 及 Spring AI Alibaba SDK 中，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失完整 JSON），实际策略应以控制台或最新版 RAM 策略文档为准；同时，`AliyunServiceRoleForSFMAccessingMNS` 的说明强调“请勿修改、删除”，与其他 SLR 的可删性描述存在策略差异，需按实际业务依赖谨慎操作。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 指定临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒（默认 60 秒） |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为平铺 Key-Value Map | 子分组内字段默认 `AND`；支持 `_operator: "OR"` 控制同组逻辑 |
| SearchFilters（RAG API / Spring AI） | `search_filters._operator` | String | 否 | 控制 `_conditions` 数组内条件关系 | `"AND"`（默认）、`"OR"` |
| SearchFilters（RAG API / Spring AI） | `search_filters._conditions` | Array of Object | 否 | 支持嵌套条件，允许多个同名字段（如多条件 OR） | 支持 `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like` 等操作符 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建首个工作流中的 FC 节点、配置首个 OSS 数据源）时，系统自动创建所需 SLR；无需手动调用 API。角色名称与权限策略已固化，不可自定义。
- **生成临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <PERMANENT_API_KEY>` 的 POST 请求，可选传入 `expire_in_seconds` 查询参数。响应返回 `token`（字符串）与 `expires_at`（UNIX 时间戳）。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **使用 SearchFilters**：
  - OpenAPI Retrieve：`searchFilters` 为平铺 Map 数组，不支持嵌套 `_conditions`；同一字段多值需序列化为 JSON 字符串（如 `{"姓名": "[\"张三\",\"李四\"]"}`）。
  - RAG API 或 Spring AI SDK：支持完整嵌套语法，推荐使用 `_conditions` 数组表达复杂逻辑（如 `{"department": {"like": "%Research%"}}`）。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中 FC 节点无法调用）。删除前必须先解除所有业务依赖（如删除 FC 节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作将被拒绝。
- **临时 API Key 不可撤销**：[Token](../concepts/token.md) 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，并确保后端服务妥善保管永久 API Key。
- **SearchFilters 兼容性差异**：
  - OpenAPI SDK 仅接受平铺结构，传入 `_conditions` 将被忽略，可能导致过滤失效；
  - RAG API 与 Spring AI SDK 支持全部高级语法（`_conditions`, `like`, 范围查询等），但要求知识库字段类型与查询操作符严格匹配（如 `age: {"gte": 25, "lte": 35}` 要求 `age` 字段为 `double` 类型）。
- **权限继承**：临时 API Key 完全继承生成者永久 Key 的权限范围，包括模型访问白名单、知识库读写权限等，**不会缩小权限边界**。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



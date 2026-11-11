# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、安全鉴权机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、可观测性集成等关键场景的底层基础设施。开发者需结合具体功能文档按需启用和配置。

## 支持的模型/功能

`more` 本身**不对应具体模型**，而是为以下核心功能提供必要支撑：

- **服务关联角色（SLR）管理**：为百炼各子系统访问外部云资源（如 FC、OSS、ADB-PG、MNS、SLS 等）提供最小权限委托机制。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 访问 OSS 与 ADB-PG [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）的安全调用方案，通过后端服务签发短期有效凭证，避免永久密钥泄露。
- **知识库 SearchFilters**：在 `Retrieve` 接口上提供结构化过滤能力，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 检索精度，尤其适用于员工信息表等结构化数据场景 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 的说明称其“请勿修改、删除”，但其他 SLR（如 `AliyunServiceRoleForSFMAccessFC`）均明确允许删除并给出前置条件。该矛盾表明 MNS 角色可能被设计为平台强依赖项，实际操作前应确认当前业务是否已启用 OSS 变更自动同步功能。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 平铺 Map 结构，子分组间 AND，同组内默认 AND，可设 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API / Spring AI） | `search_filters._conditions` | Array of Object | 否 | 支持嵌套条件，同一字段可多条件组合（如 `eq` + `like`） | `[{"_operator": "OR", "_conditions": [{"department": "Corporate"}, {"department": {"like": "%Research%"}}]}]` |

## 使用方式

- **服务关联角色**：首次开通对应功能（如函数计算节点、OSS 数据导入）时由百炼**自动创建**，无需手动申请。角色策略已预置，不可修改。查看路径：[RAM 控制台 > 角色管理](https://ram.console.aliyun.com/) [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，传入 `expire_in_seconds` 查询参数。响应返回 `token`（字符串）与 `expires_at`（Unix 时间戳）。
- **SearchFilters**：
  - OpenAPI Retrieve：使用 `bailian20231229.RetrieveRequest.search_filters` 字段，仅支持平铺结构（不支持 `_conditions` 嵌套）。
  - RAG API 或 Spring AI SDK：使用 `search_filters` 字段，支持 `_operator` 和 `_conditions` 嵌套，实现复杂逻辑组合。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能**立即失效**。例如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中函数计算节点将无法调用；删除 `AliyunServiceRoleForAccessOSS` 前必须先断开安全存储空间中的所有 OSS 连接。
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。
- **SearchFilters 兼容性差异**：
  - OpenAPI SDK 不支持 `_conditions` 嵌套，若误传将静默忽略嵌套逻辑，导致过滤失效；
  - 同一字段的多条件 OR 查询（如 `部门 = A OR 部门 LIKE "%B%"`）**仅 RAG API / Spring AI 支持**，OpenAPI 仅支持单值或数组形式的多值等值匹配；
  - 所有 `searchFilters` 字段名必须与知识库 Schema 中定义的字段名**严格一致**（区分大小写），且字段需已配置为“可检索”。
- **地域隔离**：临时 API Key 的 Endpoint 与生成所用的永久 API Key 地域强绑定（北京/新加坡/弗吉尼亚/中国香港），跨地域请求将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



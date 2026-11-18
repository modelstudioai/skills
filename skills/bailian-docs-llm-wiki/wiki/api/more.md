# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、安全鉴权机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、可观测性集成等关键场景的底层基础设施。开发者需结合具体功能文档按需启用和配置。

## 支持的模型/功能

`more` 本身**不对应具体模型**，而是为以下核心功能提供必要支撑：

- **服务关联角色（SLR）管理**：为百炼各子系统访问外部云资源（如 FC、OSS、ADB-PG、MNS、SLS 等）提供最小权限委托机制。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 访问 OSS 与 ADB-PG [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）的安全调用方案，通过后端服务签发短期有效凭证，避免永久密钥泄露。
- **知识库 SearchFilters**：在 `Retrieve` 接口上提供结构化过滤能力，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 检索精度，尤其适用于结构化数据表（如员工信息表）[知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 的说明称“请勿修改、删除”，但其他 SLR（如 `AliyunServiceRoleForSFMAccessFC`）均明确允许删除并给出前置条件。该矛盾表明 `MNS` 角色可能被设计为强绑定型，实际操作前应以控制台提示或最新控制台行为为准。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | Token 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| SearchFilters（OpenAPI） | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为平铺 key-value Map | 子分组内默认 `AND`；支持 `_operator: "OR"` 控制同组字段关系 |
| SearchFilters（RAG API / Spring AI） | `search_filters._conditions` | array of object | 否 | 嵌套条件数组，支持同一字段多条件（如 `eq` + `like`） | 需配合 `_operator: "OR"` 或 `"AND"` 使用 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、配置 OSS 数据源）时由百炼自动创建，无需手动调用 API。角色策略已预置，不可自定义修改。查看与管理请前往 [RAM 控制台](https://ram.console.aliyun.com/) 的角色管理页。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer <permanent_api_key>`，可选 `expire_in_seconds` 查询参数 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters**：
  - OpenAPI Retrieve：`searchFilters` 字段传入 JSON 数组，如 `[{"姓名": "张三"}, {"岗位": "技术员"}]`；
  - RAG API / Spring AI SDK：使用嵌套 `_conditions` 结构，如 `[{"_operator": "OR", "_conditions": [{"department": "Corporate"}, {"department": {"like": "%Research%"}}]}]`。

## 限制和注意事项

- **服务关联角色**：
  - 删除任一 SLR 将导致其关联功能立即失效（如删除 `AliyunServiceRoleForSFMAccessFC` → 工作流无法调用 FC），且必须先清理所有依赖资源（如已发布的函数节点、OSS 导入任务、ADB 连接等）；
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止手动删除或修改，违反可能导致数据同步中断；
  - 所有 SLR 均绑定特定服务域名（如 `datahub.sfm.aliyuncs.com`），不可跨服务复用。
- **临时 API Key**：
  - 不可手动撤销，仅能等待过期；
  - 权限完全继承自签发它的永久 API Key，包括模型白名单、知识库访问限制等；
  - 各地域 endpoint 独立（北京/新加坡/弗吉尼亚/香港），密钥不可跨地域使用。
- **SearchFilters**：
  - OpenAPI SDK 仅支持平铺 Map，**不支持嵌套 `_conditions`**；若误传嵌套结构，请求可能成功但过滤逻辑不生效；
  - 字段名必须与知识库 Schema 中定义的字段名严格一致（区分大小写）；
  - 多值查询需将数组序列化为 JSON 字符串（如 `{"姓名": "[\"张三\",\"李四\"]"}`），而非原生数组。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



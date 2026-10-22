# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、知识库高级检索控制、以及安全的临时凭证分发等关键功能。这些能力不直接暴露为独立模型或服务，而是作为底层支撑机制，用于增强工作流编排、RAG 应用、数据连接与可观测性等核心场景的安全性与灵活性。开发者需结合具体使用场景按需启用和配置。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但支撑以下关键功能模块：

- **服务关联角色（SLR）**：为百炼各功能模块自动申请最小必要云资源访问权限，例如函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry 等。不同功能依赖不同 SLR，如 `AliyunServiceRoleForSFMAccessFC` 支撑[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)调用 FC 节点，`AliyunServiceRoleForSFMDataHubOSSImport` 支撑[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)导入 OSS 数据 [原文标题](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精准筛选，适用于结构化知识库（如员工信息表），显著提升 RAG 结果相关性 [原文标题](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **临时 API Key 生成**：通过后端服务调用 `/api/v1/tokens` 接口，基于长期 API Key 签发短期、可配置 TTL 的临时凭证，适用于前端直连等不可信环境，避免永久密钥泄露风险 [原文标题](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 的权限说明末尾 JSON 截断（`"Statement": [` 后无闭合），实际策略内容应以控制台或最新版 RAM 策略文档为准；该问题已在[原文标题](../../raw/application-api-reference/more/bailian-service-linked-role.md)中存在，属原始文档缺陷。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| **临时 API Key** | `expire_in_seconds` | integer | 否 | 临时 Token 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| **SearchFilters（OpenAPI）** | `searchFilters` | array of object | 否 | 过滤子分组数组；每个子分组为平铺 key-value Map；支持 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| **SearchFilters（RAG API / Spring AI）** | `_conditions` | array of object | 否 | 嵌套条件数组，支持同一字段多条件（如 `like`, `eq`, `gte`）及 `_operator: "OR"` | `[{"_operator": "OR", "_conditions": [{"department": "Corporate"}, {"department": {"like": "%Research%"}}]}]` |

## 使用方式

- **服务关联角色**：无需手动创建。当首次在控制台启用对应功能（如添加 FC 节点、配置 OSS 数据源、开启安全存储空间）时，系统自动创建所需 SLR。开发者需确保主账号或具备 `AliyunRAMFullAccess` 权限的子账号执行开通操作。
- **SearchFilters**：
  - OpenAPI `Retrieve`：将 `searchFilters` 字段作为 JSON 数组嵌入请求体，仅支持平铺结构，不支持 `_conditions` 嵌套 [原文标题](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
  - RAG API 或 Spring AI Alibaba SDK：使用完整嵌套语法（含 `_conditions` 和 `_operator`），详见各 SDK 文档。
- **临时 API Key**：
  1. 后端服务使用长期 `DASHSCOPE_API_KEY` 调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800`；
  2. 解析响应获取 `token` 字段；
  3. 前端或客户端使用该 `st-***` Token 替代长期 Key 发起模型或知识库请求。

## 限制和注意事项

- **服务关联角色**：
  - 删除 SLR 前必须先解除所有依赖该角色的功能（如删除 FC 节点、断开 OSS/ADB-PG 连接、停止 MNS 订阅等），否则对应功能将立即失效；
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止手动修改或删除（见文档 1），因其由平台严格管控；
  - 所有 SLR 均绑定特定服务主体（如 `fc.sfm.aliyuncs.com`），不可复用于其他服务。
- **SearchFilters**：
  - OpenAPI SDK 的 `SearchFilters` 字段类型为 `Map<String, String>`，若传入嵌套结构（如 `_conditions`），请求虽可能成功，但**不会生效**，结果未过滤；
  - 字段名必须与知识库 Schema 中定义的字段完全一致（区分大小写），且仅支持已配置为“参与检索”的字段；
  - 多值查询需对数组值调用 `json.dumps()`（Python）或等效序列化，否则被识别为字符串。
- **临时 API Key**：
  - 无法提前撤销或删除，仅能等待过期；
  - 继承签发者 API Key 的全部权限（包括模型白名单、知识库访问策略等），请勿用高权限 Key 签发低信任环境使用的临时 Token；
  - 各地域（北京、新加坡、弗吉尼亚、中国香港）Endpoint 独立，API Key 不互通，需按目标地域调用对应 Endpoint。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)



# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不直接提供模型推理能力，而是为工作流编排、知识库精准检索、跨云服务集成等关键场景提供底层支撑。开发者需结合具体业务需求，按需启用对应功能并严格遵循权限最小化原则。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是支撑以下核心功能模块：

- **服务关联角色（SLR）**：为百炼各子系统访问外部云资源（如 FC、OSS、ADB-PG、MNS、SLS 等）提供托管式权限委托。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)调用函数计算节点依赖 `AliyunServiceRoleForSFMAccessFC`；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)对接 ADB-PG 依赖 `AliyunServiceRoleForSFMAccessADB`；[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)导入 OSS 数据依赖 `AliyunServiceRoleForSFMDataHubOSSImport` [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、移动 App）中安全调用百炼 API，避免永久密钥泄露。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤，显著提升 RAG 场景下结构化数据的召回准确率 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的策略定义被截断（末尾缺失 `}` 和完整权限项），实际使用时请以控制台或最新版 RAM 策略为准。该问题已在 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中明确标注。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 有效期（秒），范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | Array of Object | 否 | 过滤规则数组，每个元素为一个子分组（AND 语义），支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gt`, `gte`, `lt`, `lte`, `eq`, `neq` | Number/String | 否 | 字段比较操作符，仅限数值字段支持区间操作 | `{"年龄": {"gte": 25, "lt": 30}}` |
| SearchFilters（模糊查询） | `like` | String | 否 | 字符串模糊匹配，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API。角色名称与权限策略已预置，不可修改 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口生成，需在请求 Header 中携带主账号的永久 `Authorization: Bearer <DASHSCOPE_API_KEY>`。生成后直接用于后续模型或知识库 API 调用。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，格式为 JSON 数组。各子分组内字段值支持原生类型（字符串/数字）、JSON 对象（用于范围/模糊）或 JSON 字符串（用于多值/标签）。详见 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的完整代码示例。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的函数计算节点无法调用）。删除前必须先解除所有业务依赖（如删除节点、断开数据源连接），否则操作将被拒绝。
- **临时 API Key 不可撤销**：生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持手动删除或禁用**。应严格控制 TTL 时长，避免长期有效。
- **SearchFilters 兼容性**：仅适用于知识库 `Retrieve` 接口（非 `Chat` 或 `Embedding`）；仅对已启用“结构化字段索引”的知识库生效（如数据查询型知识库）；标签（Tag）查询仅支持文档/音视频类知识库。
- **权限继承**：临时 API Key 继承签发它的永久 API Key 的全部权限（含模型、知识库、业务空间范围限制），不支持降权。
- **地域隔离**：API Key、Endpoint、业务空间均按地域隔离，北京、新加坡、弗吉尼亚、中国香港等地域的密钥不可混用。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



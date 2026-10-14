# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务关联角色管理、临时认证机制和高级知识库检索控制等关键功能。这些能力面向开发者提供细粒度权限控制、安全调用保障与精准语义过滤支持，是构建生产级 AI 应用的基础设施组件。所有功能均需通过 API 或控制台显式启用，并依赖对应云资源的访问授权。

## 支持的模型/功能

`more` 不直接对应特定模型，而是为以下核心功能提供底层支撑：

- **服务关联角色（SLR）**：自动创建并托管跨服务访问权限，支撑工作流应用调用函数计算（FC）、数据管理接入 OSS/MNS、安全存储空间连接 ADB-PG、模型监控对接 SLS/CMS、用量分析集成 OpenTelemetry 等场景。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：为不可信前端环境（如浏览器、移动 App）提供短期有效的认证凭证，避免永久密钥泄露风险。
- **知识库 `SearchFilters`**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级、范围级、模糊级或标签级二次筛选，显著提升 RAG 结果相关性。

> **注意**：文档 3 中 Python 示例代码末尾存在截断（`json.du`），且 `tag_query()` 方法内 `json.du` 明显为 `json.dumps` 的拼写错误。实际使用时请以 SDK 最新文档和 `alibabacloud_bailian20231229` 官方包行为为准。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 指定临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒（默认 60 秒） |
| `SearchFilters` | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为一个子分组（AND 关系） | 子分组内支持 `_operator: "AND"`（默认）或 `"OR"`；字段支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like` 等操作符 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加 FC 节点、配置 OSS 数据源）时由系统自动创建，无需手动申请。角色策略已预置，禁止修改。详情参见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，可选传入 `expire_in_seconds` 查询参数。响应返回 `token` 和 `expires_at`（UNIX 时间戳）。
- **`SearchFilters`**：在 `RetrieveRequest` 请求体中添加 `searchFilters` 字段，格式为 JSON 数组。例如：`{"searchFilters": [{"姓名": "张三"}, {"岗位": "技术员"}]}` 表示同时满足“姓名=张三”且“岗位=技术员”。完整语法与多类型查询示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致其关联功能完全失效（如工作流无法调用 FC）。删除前必须先解除所有业务绑定（如删除函数节点、断开 OSS/ADB 连接等），否则操作被拒绝。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中各角色的“删除服务关联角色”章节。
- **临时 API Key 不可撤销**：生成后仅能等待自然过期，不支持主动吊销或提前失效。务必严格控制其 TTL 时长与使用范围。
- **`SearchFilters` 依赖知识库字段定义**：仅对在知识库索引配置中明确声明为“参与检索”的字段生效；未索引字段无法用于过滤。多值查询需确保字段类型为纯字符串或纯数值数组；范围查询仅支持 `long`/`double` 类型字段。
- **地域隔离**：临时 API Key 的 Endpoint 与生成所用的永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



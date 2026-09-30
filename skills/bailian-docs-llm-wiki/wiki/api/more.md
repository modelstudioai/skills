# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务关联角色管理、临时认证机制与高级知识库检索控制等功能。它不构成独立服务，而是支撑工作流编排、安全存储、知识库 RAG、可观测性等核心场景的关键基础设施。开发者需根据具体使用场景按需启用对应能力，并严格遵循权限最小化原则配置服务关联角色。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下关键功能提供底层支持：

- **服务关联角色（SLR）**：自动创建并托管跨云服务访问权限，支撑工作流调用函数计算（FC）、OSS 数据导入、ADB-PG 向量库接入、MNS 消息监听、OpenTelemetry/SLS/CMS 监控数据采集等。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）安全调用后端模型服务，避免永久密钥泄露。该能力继承源 API Key 的全部权限范围。
- **知识库 `searchFilters` 高级过滤**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精准筛选（如单值、多值、范围、模糊、标签查询），显著提升 RAG 结果相关性。详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}` 及后续内容），完整策略请以控制台实际策略或 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档最新版本为准。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `expire_in_seconds` | integer | 临时 API Key 有效期，取值范围 `[1, 1800]` 秒，默认 `60` 秒。 | [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| `searchFilters` | array of object | 知识库 `Retrieve` 请求中的过滤条件数组，每个元素为一个子分组（AND 语义），支持单值、多值、范围（`gte`/`lte` 等）、模糊（`like`）及标签（`tags`）查询。 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| `indexId` | string | `searchFilters` 所作用的知识库唯一标识符，需与 `Retrieve` 请求中一致。 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

## 使用方式

- **服务关联角色**：首次在控制台启用对应功能（如函数计算节点、OSS 导入、ADB-PG 连接）时，系统自动创建 SLR；无需手动调用 API。角色名称与权限策略已预定义，不可修改。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在 `Authorization` Header 中携带有效的永久 `DASHSCOPE_API_KEY`，并在 Query 参数中指定 `expire_in_seconds`。响应返回 `token` 和 `expires_at`（UNIX 时间戳）。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **`searchFilters`**：在调用 `Retrieve` 接口时，将过滤条件作为 JSON 数组赋值给 `searchFilters` 字段。例如：`{"searchFilters": [{"姓名": "张三"}, {"岗位": "技术员"}]}`。各子分组内支持嵌套复杂查询（如 `{"年龄": {"gte": 20, "lte": 30}}`）。完整语法与代码示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将导致其关联功能（如工作流中 FC 节点）完全失效。删除前必须先解除所有依赖（如删除应用、断开 OSS/ADB 连接、停止数据导入任务）。操作路径：RAM 控制台 > 角色管理 > 服务关联角色。
- **临时 API Key 不可撤销**：临时 Token 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，避免过度授权。
- **`searchFilters` 字段类型约束**：范围查询（`gt`/`gte`/`lt`/`lte`）仅支持数值类型（`long`/`double`）；模糊查询（`like`）和标签查询（`tags`）仅支持字符串类型；多值查询需确保数组元素类型一致（全为 string 或全为 number）。字段类型需与知识库索引配置严格匹配。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



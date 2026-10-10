# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大类功能。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、跨云服务集成及客户端安全调用等关键场景。开发者需结合具体业务需求，按需启用对应能力并严格遵循权限最小化原则。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是为以下核心功能提供底层支撑：

- **服务关联角色（SLR）**：支持工作流应用调用函数计算（FC）、知识库对接 ADB-PG、OSS 数据导入、MNS 消息监听、OpenTelemetry 监控上报等跨服务操作，详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露；
- **知识库 `searchFilters` 高级过滤**：在 `Retrieve` 接口请求中对语义检索结果进行结构化字段级过滤，显著提升 RAG 场景下结果相关性，尤其适用于员工信息表、产品目录等结构化数据源。

> **注意**：文档 3 中“标签（Tag）查询”说明“多个标签之间是或（OR）的关系”，但其示例代码 `tag_query2()` 的结构暗示支持多组标签分组（AND 语义），而文档未明确说明分组内多标签是否为 OR 或 AND。实际行为应以 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 文档最新运行时表现为准。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `expire_in_seconds` | Integer | 临时 API Key 有效期，取值范围 `[1, 1800]`（秒），默认 `60` | [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| `searchFilters` | Array of Object | 检索过滤条件数组，每个元素为一个子分组（Key-Value 对），子分组间为 AND 逻辑 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| `like` | String | 模糊查询字段值，支持 `%` 通配符（如 `"技%员"`） | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| `gte` / `lte` | Number | 范围查询的下界与上界，仅支持数值类型字段 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

## 使用方式

- **服务关联角色**：首次启用对应功能（如函数计算节点、OSS 导入、ADB-PG 知识库）时，系统自动创建 SLR；无需手动调用 API，但需确保 RAM 权限允许创建服务关联角色；
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口调用，需在请求头 `Authorization: Bearer <permanent_api_key>` 中携带有效永久密钥，并可选传入 `expire_in_seconds` 查询参数；
- **`searchFilters`**：在 `RetrieveRequest` 请求体中作为顶层字段传入，格式为 `{"searchFilters": [{"字段名": "值"}, {"字段名": {"eq": "值"}}]}`，支持单值、多值、范围、模糊及标签查询，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- 服务关联角色**不可手动删除**，除非满足前置清理条件（如删除所有依赖该角色的工作流节点、断开 OSS/ADB 连接、停止 MNS 订阅等），否则删除将导致对应功能完全失效；
- 临时 API Key **无法提前撤销**，仅能等待自然过期（最长 1800 秒），因此 `expire_in_seconds` 应按实际会话周期谨慎设置；
- `searchFilters` 仅作用于 `Retrieve` 接口返回的 `nodes` 列表，**不影响语义召回阶段**，即仍需保证原始知识库索引已正确配置相关字段为可检索属性；
- 所有 SLR 均绑定特定服务主体（如 `fc.sfm.aliyuncs.com`），**禁止修改策略或将其授予非服务关联角色身份**，否则将破坏百炼平台服务自治性；
- 子账号使用 `searchFilters` 前，必须已获得 `AliyunBailianDataFullAccess` 权限并加入目标业务空间，主账号无此限制。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



# more

`more` 是百炼平台为高级集成与安全治理场景提供的扩展能力集合，涵盖临时凭证生成、服务关联角色（SLR）授权、知识库精细化检索等关键功能。这些能力不直接参与模型推理，而是支撑应用安全调用、跨云资源协同及结构化数据精准召回，适用于对权限隔离、合规性与检索精度有明确要求的生产环境。

## 支持的模型/功能

- **临时 API Key 生成**：面向浏览器、移动端等不可信前端环境，通过后端服务签发短期有效凭证，避免永久密钥泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)  
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于安全访问 FC、OSS、ADB-PG、MNS、SLS 等阿里云服务，覆盖工作流编排、知识库接入、安全存储、监控分析等核心场景 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升语义检索结果的相关性与准确性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)

> **注意**：文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}` 和完整 `Statement`），实际使用请以控制台或最新 SDK 返回的策略为准；完整策略定义应参考 [用量监控与性能分析](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md) 文档中引用的 OpenTelemetry 集成说明。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围/示例 |
|------|--------|------|------|----------------|
| 临时 API Key | `expire_in_seconds` | integer | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60`；示例：`?expire_in_seconds=1800` |
| SearchFilters | `searchFilters` | array of object | 检索过滤条件数组，每个对象为一个子分组（AND 语义） | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters | 字段值（单值） | string / number | 直接匹配字段值 | `"张三"`、`25` |
| SearchFilters | 字段值（范围） | JSON object | 使用 `gte`/`lte`/`gt`/`lt`/`eq`/`neq` 属性 | `{"age": "{\"gte\": 20, \"lte\": 30}\"}`（需 JSON 字符串化） |
| SearchFilters | 字段值（模糊） | JSON object | 使用 `like` 属性 | `{"position": "{\"like\": \"技%员\"}\"}` |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 POST 请求，携带 `Authorization: Bearer <永久APIKey>`，可选 `expire_in_seconds` 查询参数。响应返回 `token`（如 `st-****`）和 `expires_at`（UNIX 时间戳）。各地域 Endpoint 不同，需按实际部署区域选择（北京、新加坡、弗吉尼亚、中国香港）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)  
- **服务关联角色**：首次启用对应功能（如函数计算节点、OSS 数据导入、ADB-PG 知识库）时，系统自动创建 SLR；无需手动创建，但删除前须解除所有依赖（如删除工作流中的 FC 节点、断开安全存储空间的 OSS 连接）  
- **SearchFilters**：在 `RetrieveRequest` 请求体中添加 `searchFilters` 字段，其值为 JSON 数组；各子分组内支持混合查询类型（如 `{"姓名": "张三", "年龄": "{\"gte\": 20}"}`）；SDK 调用需对嵌套 JSON 值做 `json.dumps()` 序列化（见 Python 示例）[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)

## 限制和注意事项

- 临时 API Key **不可手动删除**，仅能等待自然过期；其权限严格继承自签发所用的永久 API Key，包括模型访问白名单与知识库范围限制  
- 所有服务关联角色均含 `ram:DeleteServiceLinkedRole` 权限，但**仅当满足前置清理条件后才允许删除**；误删将导致对应功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后无法调用函数计算节点）  
- `SearchFilters` 仅作用于知识库 `Retrieve` 接口，**不适用于 `ChatCompletion` 或其他模型 API**；字段名必须与知识库索引时定义的元数据字段名完全一致（区分大小写）；多值查询需传入 JSON 字符串格式的数组（如 `"[\"张三\",\"李四\"]"`）  
- 各 SLR 的权限策略中均包含 `Condition` 字段（如 `oss:BucketTag/bailian-datahub-access`），要求目标云资源（如 OSS Bucket）已配置指定 Tag，否则访问将被拒绝；此约束在文档 2 的策略示例中明确体现，但未在前置步骤中强调，开发者需主动检查资源 Tag 配置 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



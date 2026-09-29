# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不构成独立 API 服务，而是支撑工作流编排、知识库精准检索、可观测性集成等关键场景的底层基础设施。开发者需按需启用对应能力，并严格遵循最小权限原则配置关联资源。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下核心功能提供必要支撑：

- **服务关联角色（SLR）**：自动创建并绑定云资源访问权限，支撑工作流调用函数计算（FC）、OSS 数据导入、ADB-PG 向量库接入、MNS 消息监听、OpenTelemetry/SLS/CMS 监控数据采集等 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用模型 API，避免永久密钥泄露。
- **知识库 `searchFilters` 高级检索**：在 `Retrieve` 接口请求中传入结构化过滤条件，实现对语义检索结果的字段级精确过滤，显著提升 RAG 场景下结构化数据的召回准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的策略定义被截断（末尾缺失 `}`），且未列出完整权限；实际部署应以控制台或 RAM 策略详情页显示的完整 JSON 为准。该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中标记为待修复。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 设置 Token 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| `searchFilters` | `searchFilters` | Array of Object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | 子分组内支持单值、多值、范围（`gte`/`lte` 等）、模糊（`like`）、标签（`tags`）查询 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如发布含 FC 节点的工作流、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API，但需确保主账号具备 `ram:CreateServiceLinkedRole` 权限。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，可选传 `expire_in_seconds` 查询参数 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **`searchFilters`**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，格式为 `[{ "field1": "value1" }, { "field2": { "gte": 20, "lte": 30 } }]`；需确保知识库字段已正确映射为可检索类型（如 `string`, `double`）。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全失效（如工作流无法调用 FC），且删除前必须先解除所有业务绑定（如删除函数节点、断开 OSS/ADB 连接）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：Token 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**；应严格控制 TTL 时长，并避免在日志中打印 `token` 值。
- **`searchFilters` 语法约束**：
  - 子分组间为强制 `AND` 逻辑，不可修改；
  - 多值查询需使用 `json.dumps(["val1","val2"])` 编码为字符串（见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 示例）；
  - 模糊查询 `like` 值中 `%` 为通配符，`%abc%` 表示包含 `abc`，`abc%` 表示前缀匹配。
- **地域隔离**：临时 API Key 的 Endpoint 与生成所用永久 Key 的地域强绑定（北京/新加坡/弗吉尼亚/中国香港），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



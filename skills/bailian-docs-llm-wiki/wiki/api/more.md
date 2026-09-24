# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务关联角色管理、临时认证机制、知识库高级检索等关键功能模块。这些能力不直接参与模型推理，但为工作流编排、安全合规、数据治理和前端集成等场景提供必要支撑。开发者需根据具体使用场景按需启用并配置对应权限或参数。

## 支持的模型/功能

`more` 本身不对应具体模型，而是支撑以下核心功能：
- **服务关联角色（SLR）**：为百炼子系统（如工作流、知识库、安全存储、用量监控等）自动申请对其他云服务（FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）的最小化访问权限。例如，`AliyunServiceRoleForSFMAccessFC` 支持函数计算节点调用，`AliyunServiceRoleForSFMAccessADB` 支持向 ADB-PG 写入向量数据 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在不可信客户端（如浏览器、App）中安全调用后端模型服务，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精准过滤，显著提升 RAG 结果相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `log:List*` 后续内容及完整 JSON），实际策略请以控制台或最新版 RAM 策略文档为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中明确标注。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围 |
|------|--------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | Integer | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒（默认 60 秒） |
| SearchFilters | `searchFilters` | Array of Object | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | 子分组内支持单值（`"字段": "值"`）、多值（`"字段": ["值1","值2"]`）、范围（`"字段": {"gte": 10, "lte": 20}`）、模糊（`"字段": {"like": "张%"}`）、标签（`"tags": ["A大学","学生会主席"]`） |

## 使用方式

- **服务关联角色**：首次启用对应功能（如发布含 FC 节点的工作流、配置 OSS 数据源至安全存储空间）时，系统自动创建 SLR；无需手动调用 API，但需确保主账号具备 `ram:CreateServiceLinkedRole` 权限。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口生成，需在请求 Header 中携带由永久 API Key 构造的 `Authorization: Bearer <DASHSCOPE_API_KEY>`；生成后将 `token` 值用于后续模型调用（如 `Authorization: Bearer st-****`）。
- **SearchFilters**：在调用知识库 `Retrieve` 接口的请求体中，与 `query`、`indexId` 同级传入 `searchFilters` 字段，格式为 JSON 数组；各语言 SDK（如 Python/Java）均支持构造该结构 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全失效（如工作流无法调用 FC），且删除前必须先解除所有业务绑定（如删除函数计算节点、断开 OSS/ADB 连接）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：[Token](../concepts/token.md) 一旦生成即无法主动吊销，仅能等待过期；务必严格控制 `expire_in_seconds` 时长，生产环境建议 ≤ 300 秒。
- **SearchFilters 字段约束**：过滤字段必须已在知识库索引配置中声明为“可过滤字段”（Filterable），且类型需匹配（如数值字段不可用字符串值过滤）；多值查询需显式使用 `json.dumps` 序列化（见 Python 示例）[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚/中国香港），跨地域调用将返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



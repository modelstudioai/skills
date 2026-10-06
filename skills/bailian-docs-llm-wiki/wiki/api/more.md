# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制和高级检索控制等关键功能。它不构成独立服务，而是支撑工作流编排、知识库检索、模型监控、数据接入等核心场景的底层基础设施。开发者需根据具体使用场景按需配置对应能力，并严格遵循最小权限原则。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供必要支撑：
- **服务关联角色（SLR）**：为百炼与外部云服务（如 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）的安全集成提供托管式权限委托。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 访问 ADB-PG 向量库；[用量监控与性能分析](raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)依赖 `AliyunServiceRoleForSFMTelemetry` 接入 OpenTelemetry 实例。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、移动 App）提供短期凭证分发能力，避免永久密钥泄露风险。
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口调用中对语义检索结果进行结构化后过滤，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 场景下结果相关性。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `log:Get*` 后续权限及完整 JSON 结构），实际策略应以控制台或最新 SDK 返回为准。请参考 [用量监控与性能分析](raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md) 文档确认完整权限集。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 约束 |
|------|--------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 指定临时 [Token](../concepts/token.md) 有效期（秒） | 必须在 `[1, 1800]` 范围内，默认 `60` |
| SearchFilters | `searchFilters` | Array of Object | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | 子分组内支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like` 及 `tags` 字段；字段类型需与知识库索引定义一致 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源、启用 ADB-PG 安全存储）时，系统自动创建 SLR；无需手动调用 API。角色名称、策略及删除约束详见 [服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口生成，需在请求头 `Authorization: Bearer $DASHSCOPE_API_KEY` 中携带有效永久密钥。各地域 Endpoint 不同，需严格匹配（如北京：`bailian.cn-beijing.aliyuncs.com`）。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段。例如：`{"searchFilters": [{"姓名": "张三"}, {"岗位": "技术员"}]}`。完整语法与代码示例见 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR 将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流中所有函数计算节点无法调用）。删除前必须先解除所有业务依赖（如断开连接、删除节点、停止任务），否则操作将被拒绝。
- **临时 API Key 不可撤销**：[Token](../concepts/token.md) 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，避免过度宽松。
- **SearchFilters 字段一致性要求**：过滤字段名（如 `"姓名"`）必须与知识库索引时定义的字段名**完全一致**（含大小写、空格），且字段类型（string/double/long）需匹配，否则过滤无效或返回错误。
- **地域隔离**：API Key、Endpoint、业务空间均按地域隔离。新加坡地域生成的临时 [Token](../concepts/token.md) 不能用于北京地域的 `Retrieve` 请求，反之亦然。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



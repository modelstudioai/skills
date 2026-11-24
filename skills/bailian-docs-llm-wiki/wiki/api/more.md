# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、安全认证机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、可观测性集成等关键场景的底层基础设施。开发者需结合具体功能模块（如知识库、工作流、监控）按需启用和配置。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是为以下核心功能提供必要支撑：

- **服务关联角色（SLR）**：为百炼各功能模块访问外部云资源（如 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、DTS、内容安全）提供最小权限委托。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 访问 OSS 与 ADB-PG；[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)依赖 `AliyunServiceRoleForSFMTelemetry` 接入 OpenTelemetry。详情见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在不可信前端环境（如浏览器、移动 App）中安全调用模型服务，避免永久密钥泄露。该能力由 `/api/v1/tokens` 接口提供，属于认证授权体系的补充机制。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行二次精筛，显著提升结构化数据（如员工信息表）的召回精度。该能力适用于 OpenAPI、RAG API 及 Spring AI Alibaba SDK 等多种调用方式。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 的说明提到“本策略……请勿修改、删除”，但其他 SLR（如 `AliyunServiceRoleForSFMAccessFC`）均明确允许删除并给出前置条件。此表述存在矛盾，实际操作应以各角色章节的**具体删除警告**为准，而非统一禁止。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 平铺 Map 数组，子分组间为 AND；同一子分组内字段默认 AND，可设 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API / Spring AI） | `search_filters` | Array of Object | 否 | 支持嵌套 `_conditions` 和 `_operator`，支持 `like`、`gte`/`lte` 等操作符 | `[{"_operator":"OR","_conditions":[{"部门":"Corporate"},{"部门":{"like":"%Research%"}}]}]` |

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间）时，系统自动创建所需 SLR。角色权限已预置，**禁止手动修改其关联策略**。查看与管理请前往 [RAM 控制台 > 角色管理](https://ram.console.aliyun.com/)。
- **生成临时 API Key**：通过后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer $DASHSCOPE_API_KEY` 的 POST 请求，并可选传入 `expire_in_seconds` 查询参数。响应返回 `token`（临时密钥）与 `expires_at`（UNIX 时间戳）。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **使用 SearchFilters**：在调用知识库 `Retrieve` 接口时，将过滤条件作为 `searchFilters`（OpenAPI）或 `search_filters`（RAG API）字段嵌入 JSON 请求体。需确保知识库已启用对应字段的索引，并遵循各调用方式的语法约束（如 OpenAPI 不支持嵌套 `_conditions`）。完整示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR 将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后无法调用函数计算节点）。删除前**必须**满足文档中列出的前置条件（如清空相关任务、断开连接、重新发布流程），否则操作将失败或引发不可逆中断。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持手动删除或禁用**。务必严格控制其 TTL 时长与分发范围。
- **SearchFilters 兼容性差异**：
  - OpenAPI `searchFilters` 仅支持平铺 Map，不支持 `_conditions` 嵌套；若错误传入嵌套结构，请求可能成功但过滤逻辑不生效。
  - RAG API 与 Spring AI SDK 支持完整表达式（`like`, `gte`, `OR` 多条件等），但需确保知识库 Schema 中字段类型匹配（如 `age` 字段为 `double` 才支持 `gte`）。
- **权限最小化原则**：所有 SLR 均按功能粒度授予最小必要权限（如 `AliyunServiceRoleForSFMDataHubOSSImport` 仅允许读取带特定 Bucket Tag 的 OSS 资源）。切勿复用或扩权。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



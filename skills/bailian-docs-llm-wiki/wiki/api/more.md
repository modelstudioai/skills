# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制和高级检索控制三大方向。它不构成独立 API 服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心功能的底层基础设施。开发者需根据具体使用场景（如调用函数计算、访问 OSS、过滤知识库结果）按需启用对应能力，并严格遵循权限最小化原则配置服务关联角色或临时凭证。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下关键功能提供必要支撑：

- **服务集成与资源访问**：通过预置的服务关联角色（SLR），支持工作流应用调用函数计算（FC）、知识库/安全存储空间访问 OSS 和 ADB-PG、数据管理对接 OSS/MNS/DTS、用量监控对接 OpenTelemetry/SLS/CMS 等。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **安全凭证分发**：提供生成临时 API Key 的能力，用于在不可信前端环境（如浏览器、App）中安全调用模型服务，避免永久密钥泄露。
- **知识库精准检索**：通过 `searchFilters` 参数，在 `Retrieve` 接口请求中对语义检索结果进行结构化过滤，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 场景下的结果相关性。详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失 `log:Get*` 后续权限及完整 JSON 结构），实际策略应以控制台或最新版 RAM 策略文档为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中体现。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `expire_in_seconds` | 请求 URL 查询参数 | Integer | 临时 API Key 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| `searchFilters` | `RetrieveRequest` 请求体字段 | Array of Object | 检索过滤条件数组，每个对象为一个子分组（AND 语义），支持 `{"字段名": "值"}`（单值）、`{"字段名": "[\"v1\",\"v2\"]"}`（多值）、`{"字段名": "{\"gte\":20,\"lte\":27}\"}`（范围）、`{"字段名": "{\"like\":\"技%员\"}\"}`（模糊）等格式 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |

## 使用方式

- **服务关联角色**：首次在控制台启用对应功能（如添加 FC 节点、配置 OSS 数据源）时，系统自动创建所需 SLR；无需手动调用 API。角色名称、权限策略及删除约束详见各角色章节。
- **生成临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久APIKey>` 的 POST 请求，可选传入 `expire_in_seconds`。响应返回 `token`（临时密钥）和 `expires_at`（Unix 时间戳）。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **使用 SearchFilters**：在调用知识库 `Retrieve` 接口时，于请求体中设置 `searchFilters` 字段。需确保知识库已正确配置字段类型（如 `年龄` 为 `double`），且调用方具备对应业务空间的数据访问权限（如子账号需绑定 `AliyunBailianDataFullAccess` 策略）。详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色不可手动创建或修改**：所有 SLR 均由百炼平台自动创建并绑定固定策略，用户仅可删除（需满足前置条件）。
- **删除 SLR 有强依赖约束**：例如删除 `AliyunServiceRoleForSFMAccessFC` 前，必须先删除所有已发布工作流/流程中的 FC 节点并重新发布；删除 `AliyunServiceRoleForAccessOSS` 前，必须先在安全存储空间中断开所有 OSS 连接。违反约束将导致删除失败。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持手动删除或禁用**。
- **SearchFilters 字段类型必须匹配**：若知识库中 `年龄` 字段定义为 `string`，则不能对其使用 `gte`/`lte` 范围查询，否则过滤无效或报错。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（如北京、新加坡），跨地域调用将失败。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



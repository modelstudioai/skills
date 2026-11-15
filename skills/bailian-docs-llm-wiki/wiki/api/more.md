# more

`more` 是百炼平台中一组面向高级集成与安全治理能力的扩展功能集合，涵盖临时凭证管理、服务关联角色（SLR）授权、以及知识库语义检索增强等核心能力。这些功能不直接参与模型推理，但为可信调用、跨云资源协同和精准检索提供关键支撑。开发者需根据具体场景选择对应能力，并严格遵循权限最小化原则。

## 支持的模型/功能

- **临时 API Key 生成**：用于浏览器、移动端等不可信环境的安全调用，避免永久密钥泄露。该能力本身不绑定特定模型，而是为所有支持 `Authorization: Bearer <token>` 的百炼 API 提供短期访问凭证 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于安全访问外部云服务（如 FC、OSS、ADB-PG、MNS、SLS 等）。不同功能模块依赖不同 SLR，例如 `AliyunServiceRoleForSFMAccessFC` 支持工作流中的函数计算节点调用，`AliyunServiceRoleForSFMAccessADB` 支持知识库对接 ADB-PG 向量库 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **知识库 SearchFilters**：专用于 `Retrieve` 接口的结构化过滤能力，支持在语义检索结果基础上按字段值、范围、模糊匹配等条件二次筛选，显著提升 RAG 场景下结果相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的策略定义在原文末尾被截断（JSON 不完整），实际使用时请以 RAM 控制台中该角色绑定的最新系统策略 `AliyunServiceRolePolicyForSFMTelemetry` 为准，避免因权限缺失导致用量监控上报失败。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters（OpenAPI） | `searchFilters` | array of object | 否 | 平铺 Map 数组，子分组内字段默认 `AND`，支持 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API / Spring AI） | `_operator`, `_conditions` | string, array | 否 | 支持嵌套条件与多条件 `OR`，同一字段可多次出现 | `[{"_operator":"OR","_conditions":[{"部门":"Corporate"},{"部门":{"like":"%Research%"}}]}]` |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。地域 Endpoint 需与生成所用 API Key 一致（北京/新加坡/弗吉尼亚/中国香港），详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色**：首次启用对应功能（如工作流中添加 FC 节点、安全存储空间配置 ADB-PG）时由百炼自动创建；删除前必须先解除所有依赖资源（如删除函数计算节点、断开 OSS 连接），否则将导致功能异常 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **SearchFilters**：在 `Retrieve` 请求体中传入 `searchFilters` 字段。**务必注意调用方式差异**：OpenAPI SDK 仅支持平铺 Map，不支持 `_conditions` 嵌套；RAG API 和 Spring AI Alibaba SDK 支持完整嵌套语法。错误混用会导致过滤失效 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- 临时 API Key **不可手动删除**，到期后自动失效；其权限完全继承自签发用的永久 API Key，**切勿授予超出必要范围的权限**。  
- 所有服务关联角色均受 RAM 权限管控，**禁止手动修改其策略内容或将其授予非百炼服务主体**；删除角色前未清理依赖资源将导致对应功能永久中断。  
- SearchFilters 对字段类型敏感：单值/多值查询要求字段为 `string` 或数值类型；范围查询（`gt`/`lte`）仅支持数值；模糊查询（`like`）仅支持 `string`。字段名必须与知识库 Schema 中定义的**精确一致（含大小写）**。  
- > **注意**：文档 3 中“前置步骤”要求子账号需具备 `AliyunBailianDataFullAccess` 策略，但该策略在最新版权限模型中已拆分为更细粒度策略（如 `AliyunBailianKnowledgeBaseReadOnlyAccess`）。建议优先使用最小权限策略，并通过业务空间授权控制数据范围，避免过度授权风险。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



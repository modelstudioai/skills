# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全访问控制、知识库高级检索等关键功能模块。它不直接提供模型推理能力，而是为模型应用、数据治理和可观测性提供底层支撑。开发者需结合具体场景按需启用相关能力，并严格遵循最小权限原则配置服务关联角色与临时凭证。

## 支持的模型/功能

`more` 本身不是模型，而是支撑以下核心功能的基础设施：

- **服务关联角色（SLR）**：为百炼各子系统（如工作流、知识库、安全存储、用量监控等）自动申请并托管对其他云服务的最小化访问权限，例如 `AliyunServiceRoleForSFMAccessFC` 用于函数计算节点调用，`AliyunServiceRoleForSFMAccessADB` 用于向 ADB-PG 写入向量数据 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App），通过后端服务调用 `/api/v1/tokens` 接口签发短期有效的访问令牌，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤，显著提升 RAG 场景下结构化数据的召回准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `log:List*` 后续内容及完整 JSON 结构），实际策略应以控制台或最新版 RAM 策略文档为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中体现。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | [Token](../concepts/token.md) 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| SearchFilters | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为一个子分组（AND 语义），支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | Number/String | 否 | 字段比较操作符，需嵌套在字段对象内 | `{"年龄": {"gte": 20, "lte": 30}}` |
| SearchFilters（模糊查询） | `like` | String | 否 | 模糊匹配值，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、配置 OSS 数据源）时由百炼自动创建；无需手动调用 API，但需确保 RAM 权限允许创建 SLR。角色详情与删除操作请参考 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key**：后端服务使用永久 `DASHSCOPE_API_KEY` 向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer <key>` 头；响应返回 `token` 和 `expires_at`（UNIX 时间戳）。[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 提供了完整 cURL 示例与错误处理说明。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接添加 `searchFilters` 字段，格式为 JSON 数组；各子分组内字段值支持字符串、数值、JSON 对象（如范围/模糊查询）；多值查询需将数组 `json.dumps` 后作为字符串传入（见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 的 Python 示例）。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全失效（如工作流无法调用 FC），且删除前必须先清理所有关联资源（已发布的应用、OSS 导入任务、ADB 连接等）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 严格控制，到期自动失效，**不支持手动删除或提前吊销**；务必严格限制 TTL 时长，并确保后端服务具备安全的密钥分发逻辑 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **SearchFilters 兼容性约束**：仅适用于知识库 `Retrieve` 接口；过滤字段必须已在知识库索引配置中声明为可检索字段；标签（Tag）查询仅支持文档搜索、音视频搜索类知识库；子分组间固定为 AND 逻辑，不可修改 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。  
- **权限继承风险**：临时 API Key 继承签发所用永久密钥的全部权限（含模型、知识库访问限制），若永久密钥权限过大，可能导致临时 [Token](../concepts/token.md) 越权；建议为临时 [Token](../concepts/token.md) 签发专门创建最小权限的子账号密钥。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



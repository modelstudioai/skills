# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全访问控制、知识库高级检索等关键功能模块。它不直接提供模型推理能力，而是为模型应用、数据治理和可观测性提供底层支撑。开发者需结合具体场景按需启用相关能力，并严格遵循最小权限原则配置服务关联角色与临时凭证。

## 支持的模型/功能

`more` 本身不是模型，而是支撑以下核心功能的基础设施：

- **服务关联角色（SLR）**：为百炼各子系统（如工作流、知识库、安全存储、用量监控等）自动申请并托管对其他云服务的最小化访问权限，例如 `AliyunServiceRoleForSFMAccessFC` 用于函数计算节点调用，`AliyunServiceRoleForSFMAccessADB` 用于向 ADB-PG 写入向量数据 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App），通过后端服务调用 `/api/v1/tokens` 接口签发短期有效的访问令牌，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确/范围/模糊过滤，显著提升 RAG 场景下结构化数据的召回精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `log:List*` 后续内容及完整 JSON 结构），实际策略应以 RAM 控制台或最新版 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档为准。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `expire_in_seconds` | Query String | Integer | 临时 API Key 有效期，单位秒，取值范围 `[1, 1800]` | `?expire_in_seconds=1800` |
| `searchFilters` | Request Body (JSON) | Array of Objects | 知识库检索过滤条件数组，每个对象为一个 AND 分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `token` | Response Body | String | 生成的临时 API Key，前缀为 `st-` | `st-abc123...` |
| `expires_at` | Response Body | Number | 临时 [Token](../concepts/token.md) 过期时间（UNIX 时间戳，秒） | `1744080369` |

## 使用方式

1. **服务关联角色**：首次启用对应功能（如创建函数计算节点、导入 OSS 数据、配置安全存储空间）时，系统自动创建所需 SLR；无需手动调用 API，但需确保 RAM 权限允许创建 SLR。  
2. **生成临时 API Key**：  
   - 后端服务使用已配置的永久 `DASHSCOPE_API_KEY` 发起 POST 请求：  
     ```bash
     curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
       -H "Authorization: Bearer $DASHSCOPE_API_KEY"
     ```  
   - 将响应中的 `token` 值传递给前端，前端在后续模型请求中使用该 `token` 替代永久密钥。  
3. **SearchFilters 检索**：  
   - 在 `RetrieveRequest` 请求体中添加 `searchFilters` 字段；  
   - 每个分组内支持 `eq`/`neq`（等值）、`gt`/`gte`/`lt`/`lte`（范围）、`like`（模糊）、`tags`（标签）等操作符；  
   - 多个分组间为隐式 `AND` 关系，不可更改 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色不可手动删除**：若删除 `AliyunServiceRoleForSFMAccessingMNS` 等角色，将导致依赖功能（如 OSS 变更自动同步）完全失效，且文档明确警告“请勿修改、删除” [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 无法主动撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，不支持手动删除或禁用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **SearchFilters 字段类型强约束**：范围查询（`gt`/`lte`）仅支持 `long` 或 `double` 类型字段；模糊查询（`like`）仅支持 `string` 类型；多值查询数组内元素必须同类型（全为字符串或全为数值） [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。  
- **权限继承风险**：临时 API Key 继承生成它的永久密钥的全部权限（含模型/知识库访问限制），务必确保生成服务使用的永久密钥权限最小化 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



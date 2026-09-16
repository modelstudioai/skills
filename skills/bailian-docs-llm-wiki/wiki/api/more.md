# more

`more` 是百炼平台为高级用例提供的扩展能力集合，涵盖知识库检索增强、服务权限委托、客户端安全鉴权等关键场景。它不构成独立服务，而是分散在多个核心组件（如知识库 Retrieve、工作流、数据管理、模型调用）中的可选增强模块。开发者需根据具体功能需求按需启用和配置，所有能力均依赖主账号或已授权子账号的合法访问权限。

## 支持的模型/功能

`more` 本身不对应特定模型，而是为以下功能提供支撑能力：
- **知识库语义检索增强**：通过 `searchFilters` 对 `Retrieve` 接口返回结果进行结构化字段过滤，显著提升结构化数据（如员工表、产品目录）的检索精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **服务间资源访问委托**：通过预置的[服务关联角色（SLR）](../../raw/application-api-reference/more/bailian-service-linked-role.md)，使百炼能安全调用 FC、OSS、ADB-PG、MNS 等阿里云服务资源；
- **不可信环境安全调用**：支持后端服务生成带 TTL 的临时 API Key，用于浏览器或移动端等无法保护密钥的场景，避免永久密钥泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMAccessingMNS` 的权限说明存在截断（末尾 JSON 不完整），且其“禁止修改/删除”的警告与其他 SLR 的通用删除流程矛盾。实际操作应以 RAM 控制台最新策略定义及 [服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles) 官方文档为准。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `searchFilters`（知识库检索） | `searchFilters` | `array[object]` | 否 | 每个 object 为一个 AND 分组；支持单值（`{"字段": "值"}`）、多值（`{"字段": "[\"v1\",\"v2\"]"}`）、范围（`{"字段": "{\"gte\":20,\"lte\":30}\"}`）、模糊（`{"字段": "{\"like\":\"%关键词%\"}"}`）、标签（`{"tags": "[\"tag1\",\"tag2\"]"}`）查询 |
| 临时 API Key | `expire_in_seconds` | `integer` | 否 | TTL，取值范围 `[1, 1800]`，默认 `60` 秒 |
| 临时 API Key | `Authorization: Bearer <permanent_key>` | HTTP Header | 是 | 必须使用永久 API Key 签发，临时 Key 继承其全部权限 |

## 使用方式

- **知识库过滤**：在 `RetrieveRequest` 中直接设置 `searchFilters` 字段，无需额外开通；确保知识库字段已正确映射为可检索类型（如 `string`, `long`, `double`）；
- **服务关联角色**：首次使用对应功能（如工作流中添加 FC 节点、安全存储空间绑定 OSS）时，系统自动创建 SLR；无需手动创建，但需确保主账号或子账号具备 `AliyunBailianDataFullAccess` 等必要权限 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization` 头的 POST 请求，响应中提取 `token` 字段用于后续模型调用；各地域 Endpoint 不同，需严格匹配 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 限制和注意事项

- `searchFilters` 子分组间固定为 AND 逻辑，不支持 OR 或 NOT；模糊查询仅支持 `like`，不支持正则；
- 所有服务关联角色均需谨慎删除：删除 `AliyunServiceRoleForSFMAccessFC` 将导致工作流函数计算节点失效；删除 `AliyunServiceRoleForSFMDataHubOSSImport` 前必须终止所有 OSS 导入任务；
- 临时 API Key 无法主动撤销，仅能等待过期；其权限完全继承自签发用的永久 API Key，若永久 Key 权限过大，临时 Key 也具备同等风险；
- `searchFilters` 的字段名必须与知识库索引时定义的字段名**完全一致（含大小写）**，否则过滤无效；
- 文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（`"log:Get*", "log:List*", "log:Query*"` 后无闭合），完整策略请以 RAM 控制台实际策略内容为准。

## 来源文档

- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)



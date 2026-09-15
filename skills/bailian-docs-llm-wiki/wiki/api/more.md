# more

`more` 是百炼平台为高级场景提供的扩展能力集合，涵盖临时凭证管理、知识库检索增强、云服务权限委托等关键功能。它不构成独立 API 服务，而是分散在应用层、数据层与基础设施层的配套机制，面向需要细粒度控制、安全隔离或跨云集成的开发者场景。所有功能均需配合主账号/子账号权限体系与业务空间上下文使用。

## 支持的模型/功能

`more` 不对应具体模型，而是支撑以下三类核心功能：

- **临时身份凭证**：为前端/移动端等不可信环境生成短期有效的 API Key，避免永久密钥泄露风险，详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级后过滤，提升 RAG 精准度，适用于结构化数据知识库。
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于安全访问 FC、OSS、ADB-PG、MNS、OpenTelemetry 等外部云资源，实现免 AK 的受控集成。

> **注意**：文档 3 中 `AliyunServiceRoleForSFMAccessingMNS` 的权限说明在末尾被截断（缺少 `log:Query*` 后续内容及完整 JSON 结构），实际策略应以 RAM 控制台中该角色绑定的 `AliyunServiceRolePolicyForSFMTelemetry` 策略为准。请勿依赖该文档片段定义权限边界。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 示例值 |
|------|--------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 每个 object 为一个 AND 分组；支持单值、多值、范围（`gte`/`lte`）、模糊（`like`）、标签（`tags`）查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SLR 权限 | — | — | 无运行时参数，由百炼在首次开通对应功能时自动创建，权限策略不可手动修改 | — |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <PERMANENT_KEY>` 的 POST 请求，URL 可附加 `?expire_in_seconds=N`。地域 Endpoint 需与永久 Key 所属地域一致（北京/新加坡/弗吉尼亚/中国香港），详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段（非 query string），字段名须与知识库索引时定义的元数据字段名严格一致，大小写敏感。完整示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **服务关联角色**：无需主动调用 API。当您在控制台首次启用对应功能（如“工作流应用中添加函数计算节点”、“安全存储空间绑定 OSS Bucket”）时，百炼会自动创建所需 SLR。删除前必须先解除所有依赖该角色的功能配置（如删除函数计算节点、断开 OSS 连接等）。

## 限制和注意事项

- 临时 API Key **不可手动删除**，仅能等待自动过期；其权限完全继承自签发它的永久 API Key，包括模型访问白名单与知识库权限。
- SearchFilters **仅作用于 `Retrieve` 接口**，不适用于 `ChatCompletion` 或 `Embedding` 等模型推理接口；多值查询需通过 `json.dumps(["val1","val2"])` 序列化为字符串传递，且数组元素类型必须统一（全 string 或全 number）。
- 服务关联角色 **禁止手动修改策略内容**，否则可能导致功能异常；删除 SLR 前未清理依赖将导致对应功能永久不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后无法再创建函数计算节点）。
- > **注意**：文档 2 中 `multi_query()` 示例代码存在严重缺陷：`retrieve_request.search_filters = [{"姓名": json.dumps(names)}]` 将整个数组序列化为字符串，但服务端期望的是原生 JSON 数组。正确写法应为 `{"姓名": ["张三", "李四"]}`（无需 `json.dumps`）。该错误已在 SDK v2023-12-29+ 版本修复，旧版 SDK 用户需自行修正。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)



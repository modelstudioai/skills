# more

`more` 是百炼平台中一组面向高级集成与安全治理能力的扩展功能集合，涵盖临时凭证分发、服务权限委托和结构化检索增强等核心能力。这些功能不直接参与模型推理，而是为应用构建提供基础设施级支持，适用于需要细粒度权限控制、跨云服务协同或高精度知识召回的生产场景。开发者应根据具体集成需求选择启用对应子能力。

## 支持的模型/功能

`more` 本身不是模型，而是平台级能力模块，当前包含以下三类关键功能：

- **临时 API Key 生成**：为前端/移动端等不可信环境提供短期、可审计的访问凭证，避免永久密钥泄露风险。该能力由后端服务调用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 接口实现。
- **服务关联角色（SLR）管理**：百炼通过预定义的 RAM 服务关联角色，安全地访问用户授权的其他阿里云资源（如 FC、OSS、ADB-PG、MNS 等）。所有 SLR 均按功能场景自动创建与绑定，详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档。
- **知识库 SearchFilters 检索过滤**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精准筛选，显著提升 RAG 场景下结构化数据（如员工表、产品目录）的召回准确率。该能力在 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中详细说明。

> **注意**：文档 2 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失 `}` 和完整 `Statement`），实际策略应以控制台或最新 SDK 返回为准；请勿直接复制粘贴该片段用于自定义策略配置。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤子分组列表，每个子分组为 key-value 对或带操作符的对象（如 `{"年龄": {"gte": 20, "lte": 27}}`） | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gt`, `gte`, `lt`, `lte`, `eq`, `neq` | number/string | 否 | 字段比较操作符，仅支持数值型字段（`gt`/`gte`/`lt`/`lte`）或字符串/数值（`eq`/`neq`） | `{"年龄": {"gte": 25}}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 字符串模糊匹配，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在请求头 `Authorization: Bearer <PERMANENT_API_KEY>` 中携带具备权限的永久密钥。地域 Endpoint 需与密钥所在地域一致（如北京地域使用 `dashscope.aliyuncs.com`，新加坡地域同理），详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **服务关联角色**：无需手动创建。当您在控制台首次启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间）时，百炼自动为您创建并绑定 SLR。角色删除需先解除所有依赖资源（如删除工作流中的 FC 节点、断开 OSS 连接），再通过 RAM 控制台操作。
- **SearchFilters**：作为 `RetrieveRequest` 的字段传入 SDK 或 HTTP 请求体，**必须配合已启用“数据查询”类型的知识库使用**。字段名须与知识库索引时定义的元数据字段完全一致（区分大小写），且字段类型需匹配查询操作（如 `age` 字段为 `double` 才支持 `gte`）。完整示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- 临时 API Key **不可手动撤销**，仅能等待自然过期；其权限严格继承自签发所用的永久 API Key，包括模型访问白名单与知识库权限。
- 所有服务关联角色均受 RAM 权限模型约束：**主账号可查看/管理全部 SLR；子账号仅能管理其所属业务空间内触发创建的角色**。删除 SLR 前务必确认无活跃依赖（如运行中工作流、未完成的数据同步任务），否则将导致功能中断。
- SearchFilters 仅作用于 `Retrieve` 接口，**不改变知识库底层向量索引结构，也不影响 `ChatCompletion` 等模型接口**。多值查询需显式使用 `json.dumps(["val1","val2"])` 编码；标签（Tag）查询仅支持文档/音视频类知识库，且多个标签间为 OR 关系。
- > **注意**：文档 3 的 Python 示例代码中 `multi_query()` 方法将 `names` 数组 `json.dumps` 后赋值给字段，但实际 SDK（如 `alibabacloud_bailian20231229` v1.0.10+）已支持原生 list 类型传参，推荐直接传 `["张三", "李四"]`，避免双重序列化导致解析失败。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



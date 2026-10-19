# more

`more` 是百炼平台中一组面向高级场景的扩展能力集合，涵盖临时凭证管理、知识库检索增强、云服务权限委托等关键功能。这些能力不直接参与模型推理主流程，但为安全调用、精准检索和系统集成提供必要支撑。开发者需根据具体场景按需启用，并严格遵循各功能的权限与生命周期约束。

## 支持的模型/功能

`more` 不对应具体模型，而是提供三类基础设施级功能：

- **临时 API Key 生成**：用于在浏览器、移动端等不可信环境安全调用模型服务，避免永久密钥泄露（详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)）；
- **知识库 `SearchFilters`**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级、范围级、模糊级等多维度精筛，显著提升 RAG 结果相关性（详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)）；
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于授权访问 FC、OSS、ADB-PG、MNS 等外部云服务资源，支撑工作流、数据导入、安全存储、监控等核心功能（详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)）。

> **注意**：文档 2 中提及的 `SearchFilters` 在 OpenAPI SDK 与 RAG API 两种调用路径下语法不一致（如 `_conditions` 嵌套支持、`_operator` 作用域），且 OpenAPI SDK 明确声明“传入嵌套结构时……不会按嵌套条件过滤”。实际开发中应严格按目标接口类型选择对应语法，不可混用。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`；默认 `60` | `1800` |
| `SearchFilters`（OpenAPI） | `search_filters` | array of object | 否 | 每个 object 为一个 AND 分组；分组内字段默认 AND，可设 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `SearchFilters`（RAG API） | `search_filters.[].\_conditions` | array of object | 否 | 支持同一字段多条件（如 `eq` + `like`）、嵌套 OR/AND；仅 RAG API 支持 | `[{"_operator": "OR", "_conditions": [{"department": "Corporate"}, {"department": {"like": "%Research%"}}]}]` |
| SLR 删除前提 | — | — | — | 非参数，但为强制操作约束：删除前必须解除所有依赖该 SLR 的资源绑定（如函数计算节点、OSS 连接、ADB-PG 实例等） | — |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer <永久APIKey>` 及可选 `expire_in_seconds` 查询参数。响应返回 `token`（字符串）与 `expires_at`（UNIX 时间戳）。地域 Endpoint 需与永久 API Key 所属地域一致（北京、新加坡、弗吉尼亚、中国香港），详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
  
- **`SearchFilters`**：
  - OpenAPI 调用：通过 SDK 的 `retrieve_request.search_filters` 字段传入数组，每个元素为平铺 key-value 对或含 `_operator` 的对象；
  - RAG API 调用：在 JSON 请求体的 `search_filters` 数组中使用 `_conditions` 嵌套结构，支持更复杂的逻辑组合；
  - 所有字段名须与知识库 Schema 中定义的字段名完全一致（区分大小写），且仅支持已配置为“可检索”的字段。

- **服务关联角色**：无需手动创建。当首次启用对应功能（如发布含 FC 节点的工作流、配置 OSS 数据源、启用安全存储空间等）时，百炼自动创建所需 SLR。角色名称及策略权限详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)，删除前必须完成前置解绑。

## 限制和注意事项

- **临时 API Key**：继承生成者 API Key 的全部权限（含模型/知识库访问限制）；无法手动撤销，仅能等待自然过期；不同地域 API Key 不互通，需确保请求 Endpoint 与密钥地域匹配。
  
- **`SearchFilters`**：
  - OpenAPI SDK 不支持 `_conditions` 嵌套，若误传将导致过滤失效；
  - 单值查询字段类型仅限 `string` 或数值（`long`/`double`）；多值查询要求数组内元素类型统一；
  - 模糊查询（`like`）仅支持 `string` 字段，且 `%` 为唯一通配符；
  > **注意**：文档 2 中 Python 示例代码存在截断（末尾 `to_di` 未闭合），实际使用时需参考完整 SDK 文档补全 `to_dict()` 实现或直接构造字典。

- **服务关联角色**：
  - SLR 由百炼服务主体（`sfm.aliyuncs.com` 等）拥有，用户无权修改其策略；
  - 删除 SLR 将导致依赖该角色的所有功能立即中断（如工作流无法调用 FC、安全存储空间无法读写 OSS），必须严格按文档要求完成前置清理；
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止用户修改或删除，违反可能导致数据同步异常。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)



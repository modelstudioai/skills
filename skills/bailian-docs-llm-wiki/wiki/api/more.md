# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务关联角色管理、临时认证机制与高级知识库检索控制等功能。它不构成独立服务，而是支撑工作流编排、安全存储、知识库 RAG、监控分析等核心场景的底层基础设施。开发者需根据具体功能需求，按文档指引配置权限、调用接口或设置参数。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下关键功能提供必要支撑：

- **服务关联角色（SLR）**：自动创建并托管跨云服务访问权限，支撑工作流调用函数计算（FC）、OSS 数据导入、ADB-PG 向量库接入、MNS 消息监听、OpenTelemetry/SLS/CMS 监控数据采集等。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）的安全鉴权方案，用于临时授权模型调用或知识库访问。
- **知识库 `searchFilters` 高级过滤**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，实现对语义检索结果的精准裁剪，尤其适用于结构化表格数据（如员工信息表）。该能力直接作用于知识库检索链路，提升 RAG 输出相关性。

> **注意**：文档 3 中 `tag_query2()` 示例代码在末尾被截断（`retrieve_request.search_filters = [` 后无闭合），且未定义 `tag1`/`tag2` 的实际使用逻辑；完整实现请以 SDK 最新版本及 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 文档为准。

## 关键参数

| 参数名 | 所属功能 | 类型 | 说明 | 取值范围 |
|--------|----------|------|------|-----------|
| `expire_in_seconds` | 临时 API Key | Integer | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒（默认 60 秒） |
| `searchFilters` | 知识库 Retrieve | Array of Objects | 检索后过滤条件数组，每个对象为一个 AND 分组 | 支持单值、多值、范围（`gte`/`lte` 等）、模糊（`like`）、标签（`tags`）查询；字段类型需与知识库 Schema 严格匹配 |

## 使用方式

- **服务关联角色**：无需手动创建。当首次启用对应功能（如在工作流中添加 FC 节点、在安全存储空间中绑定 OSS Bucket）时，百炼自动创建所需 SLR。角色名称与策略权限已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中明确列出，开发者可通过 RAM 控制台查看与审计。
- **生成临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需携带主账号或子账号的永久 `DASHSCOPE_API_KEY`（Bearer 认证）。示例：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
- **使用 `searchFilters`**：在 `RetrieveRequest` 请求体中传入 `searchFilters` 字段。例如精确匹配姓名与岗位：
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中叫张三的员工",
    "searchFilters": [
      {"姓名": "张三"},
      {"岗位": "技术员"}
    ]
  }
  ```
  完整语法与多语言示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用 FC 函数）。删除前必须先解除所有业务依赖（如删除函数计算节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作将被拒绝。
- **临时 API Key 权限继承**：临时 [Token](../concepts/token.md) 继承签发它的永久 API Key 的全部权限（含模型、知识库、业务空间粒度的访问控制），**不支持降权**。敏感场景应使用最小权限原则创建专用永久 Key。
- **`searchFilters` 兼容性约束**：
  - 仅适用于知识库类型为「数据查询」且数据源为结构化表格（如 Excel/CSV）的索引；
  - 字段名、数据类型（string/long/double）必须与知识库 Schema 定义完全一致，否则过滤无效或返回错误；
  - 标签（`tags`）查询仅支持文档搜索、音视频搜索类知识库，不适用于数据查询类知识库（文档 3 中 `tag_query2()` 示例未体现此限制，需特别注意）。
- **地域隔离**：API Key、Endpoint、业务空间均按地域隔离（北京、新加坡、弗吉尼亚、中国香港），跨地域调用需使用对应地域的凭证与 Endpoint。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



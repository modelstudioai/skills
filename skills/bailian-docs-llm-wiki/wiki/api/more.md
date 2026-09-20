# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级知识库检索控制三大方向。它不构成独立 API 服务，而是以服务关联角色（SLR）、临时凭证生成和语义检索增强参数等形式，支撑工作流编排、数据接入、监控分析、知识库精准召回等关键场景。开发者需按需启用对应能力，并严格遵循权限最小化与生命周期管理原则。

## 支持的模型/功能

`more` 本身不提供模型，但为以下核心功能提供底层支持：

- **服务集成与资源访问**：通过预置服务关联角色（SLR），使百炼能安全调用外部云服务，包括函数计算（FC）、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全及 DTS 等。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用 FC 函数；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 访问 ADB-PG 向量库。
- **临时身份认证**：提供 `/api/v1/tokens` 接口，支持后端服务基于永久 API Key 签发带 TTL 的临时 API Key（`st-***`），适用于前端或移动 App 等不可信环境。
- **知识库精准检索**：在 `Retrieve` 接口（见 [知识库的Retrieve接口](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)）中支持 `searchFilters` 参数，实现结构化字段过滤（如 `{"姓名": "张三"}`），显著提升 RAG 结果相关性。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `expire_in_seconds` | integer | 临时 API Key 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| `searchFilters` | array of object | 检索过滤条件数组，每个对象为一个 AND 分组，支持单值、多值、范围（`gte`/`lte`）、模糊（`like`）及标签查询 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| `indexId` | string | 必填，知识库索引 ID，用于 `Retrieve` 请求 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

> **注意**：文档 3 中 Python 示例代码存在截断（末尾 `tag_query2()` 方法未闭合），且 `multi_query` 和 `wildcard_query` 示例中错误地使用 `json.dumps()` 封装字符串或对象作为字段值（如 `"姓名": json.dumps(names)`）。正确用法应为原生 JSON 结构，SDK 会自动序列化；手动 `dumps` 易导致双层转义。实际请求体应为 `{"姓名": ["张三", "李四"]}` 或 `{"岗位": {"like": "技%员"}}`，而非字符串形式。

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加 FC 节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动申请。角色策略已固化，不可修改。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer <permanent_api_key>` 及可选 `expire_in_seconds` 查询参数。响应返回 `token` 与 `expires_at`（UNIX 时间戳）。
- **SearchFilters**：在 `RetrieveRequest` 中设置 `search_filters` 字段，传入符合语法的过滤数组。例如：
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中姓名为张三的员工",
    "searchFilters": [
      {"姓名": "张三"},
      {"岗位": "技术员", "年龄": {"gte": 20, "lte": 30}}
    ]
  }
  ```
  > 注意：`searchFilters` 仅对已启用「结构化字段索引」的知识库生效，且字段类型需与查询方式匹配（如 `age` 字段必须为 `double` 才支持 `gte`）。

## 限制和注意事项

- **SLR 删除风险高**：删除任一服务关联角色将导致其关联功能完全失效（如删 `AliyunServiceRoleForSFMAccessFC` → 工作流无法调用 FC）。删除前必须先解除所有依赖（如删除函数节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作被拒绝。
- **临时 API Key 不可撤销**：一旦签发，只能等待过期（最长 30 分钟），无法主动吊销。务必确保签发服务自身安全，并严格限制 `expire_in_seconds`。
- **SearchFilters 兼容性约束**：仅适用于知识库类型为「数据查询」且字段已配置为索引的场景；不支持纯文本知识库。多值查询要求字段值为数组类型，模糊查询仅限字符串字段。
- **地域隔离**：临时 API Key 的签发 Endpoint 与永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将返回 `InvalidApiKey` 错误 —— 此限制在 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档中明确强调，但未在 SLR 或 SearchFilters 文档中体现，属能力边界差异。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



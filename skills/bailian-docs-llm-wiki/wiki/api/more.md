# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、跨云服务集成及可信调用等关键场景。开发者需结合具体功能按需启用，并严格遵循最小权限原则配置相关资源。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是为以下核心功能提供底层支撑：

- **服务关联角色（SLR）**：自动创建并管理百炼访问其他阿里云服务所需的权限角色，如函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry 等。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用 FC 函数；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 连接 ADB-PG 向量库。  
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）提供短期凭证，避免永久密钥泄露风险。该能力由 `/api/v1/tokens` 接口提供，详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，实现对语义检索结果的二次精筛，显著提升 RAG 场景下结构化数据（如员工表、产品目录）的召回准确率，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略描述被截断（末尾缺失 `log:Get*` 后续内容及完整 JSON 结构），实际策略应以控制台或最新版 RAM 策略文档为准。请勿直接复制使用该不完整策略定义。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 指定 Token 有效期（TTL） | `[1, 1800]` 秒（默认 60 秒） |
| SearchFilters | `searchFilters` | Array of Object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | 子分组内支持单值（`"字段": "值"`）、多值（`"字段": ["值1","值2"]`）、范围（`"字段": {"gte": 20, "lte": 30}`）、模糊（`"字段": {"like": "技%员"}`）、标签（`"tags": ["A大学","学生会主席"]`）等格式 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加 FC 节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API。角色名称与策略已预置，开发者只需确保目标云资源（如 OSS Bucket、ADB 实例）已正确打标（如 `bailian-safe-workspace-oss-access: ReadAndWrite`）。  
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在 `Authorization` Header 中携带有效的永久 API Key（`Bearer $DASHSCOPE_API_KEY`），并可选传入 `expire_in_seconds` 查询参数。响应返回 `token` 与 `expires_at`（UNIX 时间戳）。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，格式为 JSON 数组。例如：  
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中姓名为张三的员工",
    "searchFilters": [{"姓名": "张三"}, {"岗位": "技术员"}]
  }
  ```

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的 FC 节点无法调用）。删除前必须先解除所有业务依赖（如删除 FC 节点、断开 OSS/ADB 连接），否则操作将被拒绝。详情见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 不可撤销**：Token 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，避免过度宽松。  
- **SearchFilters 兼容性**：仅适用于知识库类型为“数据查询”的结构化知识库；对文档类知识库效果有限。字段名必须与知识库索引时定义的列名**完全一致（区分大小写）**，且字段类型需匹配（如 `年龄` 字段为 `double` 类型，不可用于 `like` 模糊查询）。  
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



# more

`more` 是百炼平台中一组面向高级用例与扩展能力的工具集合，涵盖临时凭证生成、知识库检索增强、服务权限委托等关键能力。它不构成独立 API 服务，而是分散在应用层、RAG、安全治理等模块中的补充机制，用于解决不可信环境调用、精准语义过滤、跨云资源协同等典型工程问题。开发者需结合具体场景按需选用，并注意各能力的权限继承性与生命周期约束。

## 支持的模型/功能

`more` 不绑定特定模型，而是提供以下三类基础设施级功能：

- **临时 API Key 生成**：为浏览器、移动端等不可信客户端提供短期、可撤回的访问令牌，避免永久密钥泄露风险。该能力适用于所有支持 `Authorization: Bearer <token>` 鉴权的百炼 API（如 `/api/v1/tokens`、`/api/v1/chat/completions` 等）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行二次精筛，支持单值、多值、范围、模糊及标签查询，显著提升结构化数据（如员工表、制度文档）的召回精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于授权访问 FC、OSS、ADB-PG、MNS、OpenTelemetry 等阿里云其他服务，支撑工作流[函数调用](../concepts/function-calling.md)、OSS 数据导入、安全存储空间、用量监控等核心功能 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

> **注意**：文档 2 中提及的 `SearchFilters` 语法在 OpenAPI Retrieve（`bailian.cn-beijing.aliyuncs.com/{WorkspaceId}/index/retrieve`）与 RAG API（`{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`）间存在不兼容设计：前者仅支持平铺 Map 和 `_operator: "OR"`，不支持 `_conditions` 嵌套；后者明确支持 `_conditions` 数组。若混用 SDK 或手动构造请求体，可能导致过滤失效。请严格按目标接口类型选择语法。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=300` |
| SearchFilters（OpenAPI） | `searchFilters` | array of object | 否 | 每个 object 为一个 AND 分组；分组内字段默认 AND，设 `_operator: "OR"` 变为 OR | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API） | `search_filters` | array of object | 否 | 支持 `_conditions` 嵌套，`_operator` 控制 `_conditions` 内部逻辑 | `[{"_operator":"OR","_conditions":[{"部门":"Corporate"},{"部门":{"like":"%Research%"}}]}]` |
| SLR 删除前提 | — | — | — | 非参数，但为强制操作约束：删除前须清空依赖资源（如函数计算节点、OSS 导入任务、ADB-PG 连接等） | 见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 各小节“删除服务关联角色”说明 |

## 使用方式

- **临时 API Key**：  
  后端服务调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800`，携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。响应返回 `token`（如 `st-****`）与 `expires_at`（UNIX 时间戳）。前端将该 `token` 用于后续模型或知识库 API 请求的 `Authorization` 头。地域 Endpoint 需与生成 Key 的地域一致（北京/新加坡/弗吉尼亚/中国香港）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

- **SearchFilters**：  
  在 `Retrieve` 请求体中添加 `searchFilters`（OpenAPI）或 `search_filters`（RAG API）字段。例如：
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中姓名为张三的员工",
    "searchFilters": [{"姓名": "张三"}]
  }
  ```
  注意：OpenAPI SDK（如 Java Tea）要求 `searchFilters` 为 `List<Map<String, Object>>`，且字段名不可重复；RAG API 或 Spring AI Alibaba SDK 支持更灵活的嵌套结构 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

- **服务关联角色**：  
  无需手动创建。当首次启用对应功能（如在工作流中添加函数计算节点、在数据管理中配置 OSS 导入）时，百炼自动创建 SLR。角色名称与权限策略已预定义，不可修改。如需删除，必须先解除所有依赖（见各 SLR 小节“删除服务关联角色”警告），再通过 RAM 控制台操作 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

## 限制和注意事项

- **临时 API Key**：  
  - 继承生成者 API Key 的全部权限（含模型访问、知识库读写等），无细粒度权限控制。  
  - 无法手动撤销，仅能等待过期（最长 1800 秒）。  
  - 各地域密钥隔离，跨地域调用会失败。

- **SearchFilters**：  
  - OpenAPI Retrieve 不支持同一字段的多值 OR 查询（如 `{"age": [25, 30]}`），仅支持单值或字符串数组（需 `json.dumps` 序列化后传入）。  
  - 模糊查询（`like`）仅限字符串字段；范围查询（`gt`, `gte` 等）仅限数值字段。  
  - 子账号需具备 `AliyunBailianDataFullAccess` 策略并加入业务空间，否则 `Retrieve` 调用将鉴权失败。

- **服务关联角色**：  
  - SLR 由百炼专属服务主体（如 `datahub.sfm.aliyuncs.com`）扮演，不可被其他服务复用。  
  - 删除 SLR 将导致对应功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用任何 FC 函数），且恢复需重新触发功能开通流程。  
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止用户修改或删除，因其为平台核心同步机制所必需。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)



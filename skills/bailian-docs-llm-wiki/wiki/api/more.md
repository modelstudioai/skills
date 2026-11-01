# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖临时凭证管理、服务关联角色（SLR）授权、以及知识库检索增强等关键功能。这些能力不直接暴露在基础模型调用链路中，但对构建安全、可治理、可扩展的企业级 AI 应用至关重要。开发者需根据具体场景（如前端直连、多云资源集成、结构化知识过滤）按需启用和配置。

## 支持的模型/功能

- **临时 API Key 生成**：为浏览器、移动端等不可信环境提供短期、权限继承的访问凭证，适用于模型推理、知识库检索等所有支持 `Authorization: Bearer <token>` 的 API [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于安全访问外部云服务（如 FC、OSS、ADB-PG、MNS、OpenTelemetry 等），支撑工作流[函数调用](../concepts/function-calling.md)、OSS 数据导入、安全存储空间、用量监控等核心功能 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升语义检索结果的相关性，尤其适用于结构化数据表（如员工信息、产品目录）[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失闭合大括号），实际策略定义请以 RAM 控制台或最新版控制台文档为准；其功能描述与 [用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) 一致，属有效能力。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围/示例 |
|------|--------|------|------|----------------|
| 临时 API Key | `expire_in_seconds` | Integer | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60`；示例：`?expire_in_seconds=1800` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 平铺式过滤子分组数组，每个子分组内字段默认 `AND`，支持 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]`；`[{"_operator": "OR", "doc_name": "A", "title": "B"}]` |
| SearchFilters（RAG API / Spring AI） | `_conditions` | Array of Object | 嵌套条件数组，配合 `_operator` 实现同一字段多条件（如 `like` + `eq`） | `[{"department": "Corporate"}, {"department": {"like": "%Research%"}}]` |

## 使用方式

- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 调用，需在请求头携带 `Authorization: Bearer $DASHSCOPE_API_KEY`（永久密钥）。地域 Endpoint 需与永久 API Key 所属地域一致（北京/新加坡/弗吉尼亚/中国香港）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色**：首次启用对应功能（如添加 FC 节点、配置 OSS 安全存储）时由百炼自动创建，无需手动操作；删除前必须先解除所有依赖（如删除工作流中的 FC 节点、断开 OSS 连接）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **SearchFilters**：在 `Retrieve` 请求体中直接传入 `searchFilters` 字段。**注意调用方式差异**：  
  - OpenAPI SDK 仅支持平铺 Map，不支持 `_conditions` 嵌套；  
  - RAG API 和 Spring AI Alibaba SDK 支持完整嵌套语法（`_operator` + `_conditions`）[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **临时 API Key**：  
  - 继承生成者永久 API Key 的全部权限（含模型访问、知识库读写等），**不可降权**；  
  - 无法手动删除，到期自动失效；  
  - 各地域 API Key 不互通，Endpoint 必须匹配密钥所在地域。  
- **服务关联角色**：  
  - 删除 SLR 将导致对应功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用 FC 函数）；  
  - 部分角色（如 `AliyunServiceRoleForSFMAccessingMNS`）明确禁止手动修改或删除。  
- **SearchFilters**：  
  - OpenAPI 方式不支持同一字段多个独立条件（如 `{"age": 25, "age": 30}` 会覆盖）；需用 RAG API 或 Spring AI SDK 的 `_conditions` 实现；  
  - 字段名必须与知识库 Schema 中定义的字段名**严格一致**（区分大小写）；  
  - 模糊查询（`like`）仅支持字符串类型字段。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



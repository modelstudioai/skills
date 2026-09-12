# data connection overview

数据连接是百炼平台中用于安全、高效地将外部数据源接入模型应用的关键基础设施，支持在推理、RAG、Agent 等场景中动态读取结构化与非结构化数据。它通过统一的连接管理、凭证隔离和权限控制机制，降低数据接入复杂度，同时保障敏感信息不泄露。该能力深度集成于百炼控制台与 SDK，适用于开发者构建生产级数据增强型 AI 应用。

## 支持的模型/功能

- 支持在 **RAG 检索节点**、**自定义函数（Function Calling）** 和 **Agent 工作流中的 Data Source 节点** 中直接调用已配置的数据连接；
- 兼容主流数据源类型：MySQL、PostgreSQL、SQL Server、Oracle、MongoDB、Elasticsearch、阿里云 Tablestore、OSS（CSV/JSON/Parquet 文件）、以及通过 JDBC 协议接入的任意关系型数据库；
- 支持自动元数据发现（如表结构、字段注释）、SQL 查询预检、以及基于列级别的动态过滤（需配合 [原文标题](../../raw/application-user-guide/data-connection-overview.md) 中定义的参数模板）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `type` | string | 是 | 数据源类型，如 `"mysql"`、`"oss"`、`"elasticsearch"`；必须与 [原文标题](../../raw/application-user-guide/data-connection-overview.md) 所列枚举值严格一致 |
| `connection_id` | string | 是 | 平台分配的唯一连接标识，可在控制台「数据连接」列表中获取 |
| `query` | string / object | 否 | SQL 查询语句（关系型）或 DSL/路径表达式（NoSQL/OSS）；若为对象格式，需符合 [原文标题](../../raw/application-user-guide/data-connection-overview.md) 中定义的 `query_template` 结构 |
| `timeout_ms` | number | 否 | 默认 10000（10 秒），超时后返回错误，不可设为 0 |

> **注意**：文档中曾提及支持 `redis` 类型，但当前 SDK v3.2.0+ 及控制台 v2.8.0 已移除此类型，实际调用将返回 `400 Unsupported type`；请以最新控制台可选类型下拉列表为准。

## 使用方式

1. **配置连接**：在控制台「数据连接」页面创建并测试连接，确保网络可达性与权限正确（如 VPC 内网访问、RAM 授权等）；
2. **引用连接**：在 RAG 检索节点或 Agent Data Source 节点中，选择已启用的 `connection_id`，并填写 `query`（支持 Jinja2 模板变量，如 `{{ input.query }}`）；
3. **调试验证**：使用节点内置的「试运行」功能执行查询，检查返回数据结构是否符合下游模型输入要求；
4. **代码调用（SDK）**：通过 `DataConnectionClient.invoke()` 方法传入参数对象，详见 [原文标题](../../raw/application-user-guide/data-connection-overview.md) 中的示例代码节。

## 限制和注意事项

- 单次查询返回结果默认最多 1000 行（`limit` 参数可显式覆盖，但最大不超过 5000）；
- OSS 连接仅支持公共读或 RAM 授权的私有 Bucket，不支持临时 STS [Token](../concepts/token.md) 动态鉴权（该能力计划 Q4 上线，当前需预置长期 AccessKey）；
- 所有查询均在服务端执行，原始 SQL/DLS 不会透出至前端或日志（审计日志除外），但 `query` 字段若含硬编码敏感值（如 `WHERE api_key = 'xxx'`），仍构成安全风险；
- 连接配置变更（如密码更新）后，**已有工作流不会自动热加载**，需手动触发节点重部署或重启 Agent 实例。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview.md)



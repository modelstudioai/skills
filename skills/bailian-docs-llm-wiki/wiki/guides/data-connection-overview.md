# data connection overview

数据连接（Data Connection）是百炼平台提供的核心能力之一，用于在模型应用中安全、高效地接入外部结构化数据源（如 MySQL、PostgreSQL、SQL Server 等），支撑 RAG、动态知识检索、SQL 生成等场景。它通过统一的连接管理、凭证隔离与查询沙箱机制，降低数据接入复杂度并保障运行时安全性。该能力深度集成于百炼应用构建流程，支持可视化配置与 API 调用两种接入路径。

## 支持的模型/功能

- 支持在 **RAG 应用** 中作为知识库数据源（需配合向量化或原生 SQL 检索模式）；  
- 支持在 **自定义工作流（Workflow）节点** 中直接执行参数化 SQL 查询，并将结果注入后续节点；  
- 支持与 [百炼 SQL Agent](../../raw/application-user-guide/sql-agent-overview.md) 协同，实现自然语言到可执行 SQL 的端到端闭环；  
- 当前仅支持关系型数据库（MySQL 5.7+/8.0、PostgreSQL 10+、SQL Server 2016+），不支持 NoSQL 或文件类数据源。  
> **注意**：[原文标题](../../raw/application-user-guide/data-connection-overview.md) 中提及的“支持 Oracle”尚未上线，实际控制台及 SDK v3.2.0 中暂未开放 Oracle 驱动选项，请以 [原文标题](../../raw/sdk-reference/python-sdk-data-connection.md) 的 `supported_databases` 列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `host` | string | 是 | 数据库主机地址（支持域名或 IP） |
| `port` | integer | 否 | 默认值依数据库类型而定（MySQL: 3306, PostgreSQL: 5432） |
| `database` | string | 是 | 目标数据库名（schema 名） |
| `username` | string | 是 | 连接用户名（建议使用最小权限账号） |
| `password` | string | 是 | 密码（平台自动加密存储，不透出明文） |
| `ssl_mode` | string | 否 | 可选 `disable` / `require` / `verify-ca`；生产环境强烈建议启用（参见 [原文标题](../../raw/application-user-guide/data-connection-security.md)） |

## 使用方式

1. **控制台配置**：进入「应用 > 数据连接」页面，点击「新建连接」，填写参数并测试连通性；  
2. **API 调用**：调用 `POST /v1/data_connections` 接口，传入 JSON 格式参数（详见 `data_connection_create_request` Schema）；  
3. **工作流中引用**：在 Workflow 节点配置中选择「Database Query」类型，下拉选择已创建的数据连接，并编写带 `{}` 占位符的参数化 SQL（如 `SELECT * FROM users WHERE status = '{status}'`）。

## 限制和注意事项

- 单个连接最大并发查询数为 10，超限请求将被拒绝（返回 HTTP 429）；  
- 查询语句执行超时默认为 30 秒，不可修改（避免长事务阻塞资源）；  
- 不支持跨库 JOIN（如 `SELECT * FROM db1.table1 JOIN db2.table2`），所有表必须属于同一 `database`；  
- 密码字段不支持环境变量注入，必须通过平台 UI 或 API 显式传入密文（即使使用 Secret Manager，也需先解密后传入）；  
- 删除数据连接后，所有依赖该连接的 RAG 知识库与 Workflow 节点将立即失效，需手动更新配置。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview.md)



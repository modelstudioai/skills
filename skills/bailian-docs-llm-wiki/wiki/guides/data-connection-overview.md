# data connection overview

数据连接（Data Connection）是百炼平台中用于安全、可控地将外部数据源接入模型应用的关键基础设施。它支持在不暴露原始凭证的前提下，为大模型应用提供结构化/非结构化数据的实时或批量访问能力。开发者可通过统一配置界面管理连接，并在[提示词工程](../concepts/prompt-engineering.md)、RAG 或[函数调用](../concepts/function-calling.md)等场景中引用已注册的数据源。

## 支持的模型/功能

- 支持在 RAG 应用中作为知识库数据源（如 MySQL、PostgreSQL、Elasticsearch、OSS 等）；
- 支持在[函数调用](../concepts/function-calling.md)（Function Calling）中作为后端服务代理，将 LLM 请求自动转换为 SQL 查询或 API 调用；
- 当前**不支持**直接用于训练微调任务的数据输入，仅面向推理阶段的数据接入；该限制详见 [数据连接](../../raw/application-user-guide/data-connection-overview.md)。

## 关键参数

- `type`：数据源类型，必须为预定义枚举值（如 `mysql`, `postgresql`, `oss`, `elasticsearch`），大小写敏感；
- `connection_id`：平台分配的唯一标识，创建后不可修改，用于在 Prompt 或 Function Schema 中引用；
- `auth_mode`：认证方式，支持 `ak_sk`（AccessKey）、`ram_role`（角色扮演）和 `oauth2`（部分 SaaS 服务），其中 `ak_sk` 模式需通过密钥管理服务（KMS）加密存储，详情见 [数据连接](../../raw/application-user-guide/data-connection-overview.md)；
- `timeout_ms`：默认 30000（30 秒），超时后返回 `ConnectionTimeoutError`，不可设为 0 或负数。

## 使用方式

1. 在控制台「数据连接」页面完成配置并测试连通性；
2. 在 RAG 应用中，于知识库配置页选择已启用的 `connection_id`；
3. 在 Function Calling 场景中，在函数定义的 `parameters.schema` 中声明 `"type": "data_connection"`，并指定 `connection_id` 字段；
4. 所有调用均经平台网关鉴权与审计，原始凭证**永不透出**至用户模型代码或日志，具体实现机制参见 [数据连接](../../raw/application-user-guide/data-connection-overview.md)。

## 限制和注意事项

- 单账号最多创建 50 个数据连接实例；
- OSS 类型连接仅支持 `bucket` + `prefix` 粒度授权，不支持单文件级 ACL 控制；
- > **注意**：文档中提及“支持 MongoDB 连接”为历史遗留描述，当前版本（v2.3.0+）已移除该类型支持，实际可用列表以控制台下拉菜单为准；
- 同一 `connection_id` 不可跨工作空间复用，迁移需重新创建；
- 所有连接默认启用 TLS 加密，禁用明文传输（包括 MySQL 的 `skip-ssl` 参数被强制覆盖）。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview.md)



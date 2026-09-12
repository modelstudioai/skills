# data connection overview

数据连接（Data Connection）是百炼平台中用于安全、可控地将外部数据源接入模型应用的关键基础设施，支持在推理、RAG、Agent 等场景中动态访问结构化与半结构化数据。它通过统一认证、连接池管理与查询沙箱机制，隔离用户数据与平台运行时环境。所有数据连接均需显式授权且不持久化原始数据至百炼服务端。

## 支持的模型/功能

- **适用模型**：当前仅支持在 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen2.5-*` 系列模型的 RAG 检索增强与 Agent 工具调用中使用；不支持直接用于 `qwen-vl` 或 `qwen-audio` 等[多模态](../concepts/multi-modal.md)模型的原生输入。  
- **核心功能**：  
  - SQL 查询执行（MySQL、PostgreSQL、Oracle、SQL Server、达梦、OceanBase）  
  - CSV/Excel 文件直连（通过上传后生成临时连接）  
  - API 数据源接入（需提供 OpenAPI 3.0 Schema，经 [原文标题](../../raw/application-user-guide/data-connection-overview.md) 校验）  
  > **注意**：文档 [原文标题](../../raw/application-user-guide/data-connection-overview.md) 中提及“支持 MongoDB”，但当前 v3.2.1 平台版本实际未开放该驱动，该描述已过时，请以控制台可选数据源列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `type` | string | 是 | 数据源类型，取值为 `mysql` / `postgresql` / `sqlserver` / `oracle` / `dm` / `oceanbase` / `csv` / `excel` / `openapi` |
| `connection_uri` | string | 条件必填 | 标准 JDBC URI（如 `jdbc:mysql://host:3306/db?user=xxx&password=xxx`），`csv`/`excel` 类型时为 OSS URL 或 base64 编码内容 |
| `query_timeout_ms` | integer | 否 | 默认 10000（10 秒），最大 60000；超时后终止查询并返回错误 |
| `max_rows` | integer | 否 | 单次查询结果最大行数，默认 1000，上限 5000；超过部分被截断 |

## 使用方式

1. **创建连接**：通过控制台「数据连接」页面填写参数，或调用 `/v1/data_connections` POST 接口（需 `data_connection:Create` 权限）；  
2. **绑定到应用**：在 RAG 知识库配置或 Agent 工具定义中，通过 `data_connection_id` 引用已创建连接；  
3. **运行时调用**：模型在生成过程中自动触发查询，结果经结构化解析后注入上下文；详细协议见 [原文标题](../../raw/application-user-guide/data-connection-overview.md)。

## 限制和注意事项

- 单个账号最多创建 50 个数据连接，每个连接最多关联 10 个应用；  
- 所有 SQL 查询默认启用只读模式（`SET SESSION TRANSACTION READ ONLY`），禁止 `INSERT`/`UPDATE`/`DROP` 等写操作；  
- CSV/Excel 文件大小上限为 50 MB，且仅支持 UTF-8 编码；若含 BOM 头，需手动去除，否则解析失败；  
- 连接凭证（如密码）不会明文返回 API 响应，且控制台仅显示掩码后的 `***`；  
- 不支持跨 VPC 直连，若数据源位于私有网络，必须通过 [阿里云 DataWorks 数据集成网关](https://help.aliyun.com/zh/dataworks/user-guide/data-integration-gateway) 或部署白名单代理中转。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview.md)




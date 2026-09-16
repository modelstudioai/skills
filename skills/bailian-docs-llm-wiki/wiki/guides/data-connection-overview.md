# data connection overview

数据连接（Data Connection）是百炼平台中用于将外部数据源接入模型推理流程的核心机制，支持在提示词中动态注入结构化或非结构化数据。它不改变模型本身，而是通过运行时数据绑定增强上下文相关性，适用于 RAG、动态知识注入等场景。该能力依赖于平台统一的数据接入网关与安全凭证管理模块。

## 支持的模型/功能

- 当前仅支持 **Qwen 系列大模型**（含 Qwen1.5、Qwen2、Qwen2.5 及 Qwen3）在 `chat` 模式下使用数据连接；其他模型（如 Baichuan、GLM）暂不支持，调用将返回 `400 UnsupportedModel` 错误。  
- 支持两类数据源：  
  - **结构化数据**：MySQL、PostgreSQL、SQL Server、Oracle（需通过 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 配置 JDBC 连接）；  
  - **非结构化数据**：OSS/BOS/S3 对象存储中的文本、PDF、Markdown 文件（解析后作为上下文片段注入）。  
- 功能上支持 `query`（SQL 查询结果注入）、`search`（向量检索结果注入）和 `fetch`（按 ID 或路径直取原始内容）三种数据获取模式。

## 关键参数

在 API 请求体中需通过 `data_connection` 字段声明，结构如下：

```json
{
  "data_connection": {
    "type": "sql", // 或 "vector"、"object"
    "id": "dc-abc123", // 已配置的数据连接 ID
    "query": "SELECT title, content FROM docs WHERE category = ?",
    "params": ["faq"]
  }
}
```

- `id` 必填，对应控制台中创建的数据连接唯一标识；  
- `query` 仅对 `type: "sql"` 有效，支持位置参数（`?`）；`type: "vector"` 时需改用 `query_text` 字段；  
- 最大上下文注入长度受模型 `max_context_length` 限制，实际可用长度 = 模型上下文上限 − 提示词长度 − 系统预留开销（约 200 token）。

## 使用方式

1. **前置配置**：在控制台「数据连接」页面新建连接，填写数据库连接串或对象存储凭证，并测试连通性；详情见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
2. **API 调用**：在 `/v1/chat/completions` 请求中携带 `data_connection` 字段（不可与 `tools` 并存）；  
3. **调试验证**：使用 `debug: true` 参数可返回注入的原始数据片段（含截断标记），便于排查字段映射或编码问题；参考 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中的调试章节。  
> **注意**：文档中提及“支持 CSV 本地上传作为数据源”，但该功能已于 v3.2.0 下线，当前仅支持已注册的远程数据连接，详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的版本变更说明。

## 限制和注意事项

- 单次请求最多绑定 **1 个数据连接**；多源需求需在 SQL 层或向量库中预先关联；  
- SQL 查询结果自动转为 JSON 数组，字段名区分大小写，且不支持嵌套查询或存储过程；  
- 向量检索默认 Top-K=3，不可配置；若需更高精度，须调整向量库索引参数并重新导入数据；  
- 所有数据连接操作均受项目级 IAM 权限控制，`data_connection:use` 权限为必需项；  
- 敏感字段（如密码、token）禁止硬编码在 `query` 中，必须通过 `params` 传入，否则触发审计拦截。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview.md)



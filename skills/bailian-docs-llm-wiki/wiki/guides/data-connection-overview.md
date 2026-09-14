# data connection overview

数据连接是百炼平台中用于安全、高效地将外部数据源接入模型应用的关键基础设施，支持在推理、RAG、Agent 等场景中动态读取结构化与非结构化数据。它通过统一的连接管理、凭证隔离和权限控制机制，降低数据接入复杂度，同时保障敏感信息不泄露。该能力深度集成于百炼控制台与 SDK，适用于开发者构建生产级数据增强型 AI 应用。

## 支持的模型/功能

- 支持在 **RAG 检索节点**、**自定义函数（Function Calling）** 和 **Agent 工作流中的 Data Source 节点** 中调用已配置的数据连接；
- 兼容主流数据源类型：MySQL、PostgreSQL、SQL Server、Oracle、Doris、StarRocks、Elasticsearch、MongoDB、OSS（含 CSV/JSON/Parquet 文件）、以及通过 JDBC 协议接入的任意关系型数据库；
- 支持字段级权限映射与查询结果自动 Schema 推断，无需手动定义表结构。  
  > **注意**：[数据连接](../../raw/application-user-guide/data-connection-overview.md) 文档中未明确列出 StarRocks 和 Doris 支持，但当前控制台实际已提供对应连接器类型，以控制台最新选项为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `connection_id` | string | 是 | 平台分配的唯一连接标识，创建后不可修改；需在 API 请求体或工作流节点配置中显式传入 |
| `query` | string | 否（RAG 场景下可选） | SQL 查询语句或文件路径（如 `oss://bucket-name/path/to/file.json`），支持参数占位符 `{{input.xxx}}` |
| `timeout_ms` | integer | 否 | 默认 10000（10 秒），超时后返回 `ConnectionTimeoutError` |

## 使用方式

1. **控制台配置**：进入「数据连接」页面 → 点击「新建连接」→ 选择数据源类型 → 填写网络可达的 endpoint、认证凭据（推荐使用密钥管理服务 KMS 加密存储）→ 测试连通性并保存；  
2. **API 调用**：在 `POST /v1/applications/{app_id}/runs` 的 `nodes` 配置中，为 `type: "data_source"` 节点指定 `connection_id` 与 `query`；  
3. **SDK 示例（Python）**：  
   ```python
   from alibabacloud_bailian20231229 import models as bailian_models
   node = bailian_models.RunNode(
       type="data_source",
       config={"connection_id": "conn-xxx", "query": "SELECT * FROM users WHERE id = {{input.user_id}}"}
   )
   ```  
   更多细节请参考 [数据连接](../../raw/application-user-guide/data-connection-overview.md) 的完整操作流程。

## 限制和注意事项

- 单个连接最大并发请求数为 50，超出将触发限流（HTTP 429）；
- OSS 连接仅支持公共读或授权 RAM 角色访问的 Bucket，不支持临时 STS [Token](../concepts/token.md) 动态鉴权（该限制已在 [数据连接](../../raw/application-user-guide/data-connection-overview.md) 中隐含说明，但未明确标注）；
- 所有查询执行均在服务端沙箱内完成，禁止执行 `INSERT`/`UPDATE`/`DROP` 等写操作，违反将直接拒绝请求；
- 连接凭据更新后，已缓存的旧连接实例不会自动刷新，需重启相关应用或手动清除运行时缓存。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview.md)



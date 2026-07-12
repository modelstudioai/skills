# data connection overview

数据连接是阿里云百炼平台管理外部数据源的统一入口。通过创建数据连接器，百炼应用可以安全地访问企业数据库、文档系统和对象存储中的数据，并在对话中实时查询和引用这些数据。详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 连接器类型

数据连接器按数据的存储和访问方式分为两大类：

- **平台托管**：数据导入并存储在百炼平台（或自有 OSS）。
  - **文件**：管理非结构化文档（PDF、Word、Markdown 等）。
  - **表格**：导入并查询结构化表格数据（CSV、Excel 等）。
- **流处理**：数据保留在原数据源，实时访问。
  - **MySQL / PostgreSQL / PolarDB-X 2.0**：连接对应数据库，支持执行 SQL 查询（仅 DMS 导入方式支持）。
  - **语雀**：访问语雀文档和知识库（仅公网版本）。
  - **OSS**：访问对象存储中的文件。

各类型的适用场景与存储方式详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的连接器类型表。

## 前置条件

- **账号权限**：主账号或具有数据连接管理权限的 RAM 用户；RAM 用户需先获得主账号授权。
- **数据源准备**（按连接器类型）：
  - 文件/表格：准备好待上传文档/表格，或已创建 OSS Bucket。
  - MySQL：已有 MySQL 实例（RDS 或自建），网络可达（公网或私网）。
  - PostgreSQL：账号具备高权限（Superuser 或 REPLICATION），且 `wal_level` 设置为 `logical`；自建实例还需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问。
  - PolarDB-X 2.0：已有阿里云 PolarDB-X 2.0 实例且所在地域支持私网访问；DMS 导入方式需先在 DMS 录入实例。
  - 语雀：已有公网版语雀知识库并获取访问 Token。
  - OSS：已创建 Bucket 并开通向量检索服务。

## 数据库连接器关键差异

| 差异项 | MySQL | PostgreSQL | PolarDB-X 2.0 |
| --- | --- | --- | --- |
| 默认端口 | 3306 | 5432 | 自动获取 |
| 额外必填字段 | 无 | dbName（数据库名称） | 无 |
| 连通性检测服务 | EventBridge | DTS | DTS |
| 网络类型 | 公网 / 私网 | 公网 / 私网 | 仅私网 |
| 特殊配置 | 无 | `wal_level=logical` | 需 SLR 授权（DTS、PolarDB-X，DMS 方式加 DMS 角色） |

三类流处理数据库连接器均支持两种数据来源配置：**创建自定义数据源**（手动配置连接信息）与**从 DMS 导入数据源**（导入 DMS 中已有数据源）。数据库用户须具备读取权限，配置后可点击检测验证连通性。完整字段说明见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的各连接器配置章节。

> **注意**：仅通过**从 DMS 导入数据源**方式创建的 MySQL / PostgreSQL / PolarDB-X 2.0 连接器支持执行 SQL 查询；通过**创建自定义数据源**方式添加的连接器不支持直接执行 SQL。

## 创建连接器

1. 在[数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)页面点击**创建连接器**。
2. 选择连接器类型，填写**连接器名称**和**描述**（描述会用于指导应用调用的准确度，建议写明数据内容和用途）。
3. 按类型填写存储位置或数据源信息，必要时执行连通性检测。
4. 点击**确认**完成创建。

存储位置选择要点：

- **文件连接器**：平台存储限时免费（最多 200,000 个文件、1 TB）；或使用自有 OSS，需为 Bucket 添加 `bailian-connector-access` 标签（值 `ReadAndWrite`）。
- **表格连接器**：平台存储提供 1 TB 免费额度，用尽后转按量付费；自有 OSS 同样需上述标签。
- **OSS 连接器**：从下拉列表选择 Bucket，需添加 `bailian-datahub-access` 标签（值 `read`）。

## 导入数据

- **导入文件**：进入文件连接器详情页，在**类目**下选择或新建类目后导入。平台暂不支持直接导入 JSON、CSV、YAML，需先转换为 XLSX/XLS。可选择**默认设置**或**自定义设置**解析（电子文档解析、文档智能解析、大模型文档解析、Qwen VL 解析、音视频解析等，具体能力取决于文件类型）。可为文件配置**标签**，API 调用时通过 `tags` 参数筛选以提升检索效率。
- **导入表格**：进入表格连接器详情页，在**数据表管理**下选择或新建数据表。支持**直接上传 Excel**（自动识别表头）或**自定义表头**。数据表结构（列名、描述、类型）一旦确定不可修改，且上传文件的列数与列名必须与表结构一一对应，否则导入失败。

## 限制和注意事项

- 数据库连接器执行 SQL 的限制见上文注意框（仅 DMS 导入方式支持）。
- **OSS 连接器**：使用需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)，否则无法使用 `searchOSSFile` / `searchOSSFileByFileName` 工具；不支持归档/冷归档/深度冷归档类型的 Bucket；支持内容加密与私有 Bucket；开启 Referer 防盗链时需将 `*.console.aliyun.com` 加入白名单。
- **文件导入**：文件作为独立副本存储在平台免费空间（当前无容量限制），仅支持查看最近 **90** 天内导入的文件（超期不可查看但不删除），且仅供当前业务空间使用。请求高峰期解析可能耗时数小时甚至偶现超时，需耐心等待或重试。
- **语雀连接器**：仅支持公网版本语雀，需提供有效的 Tenant access token。

以上流程、字段和限制的完整细节，请以原文 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 为准。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)




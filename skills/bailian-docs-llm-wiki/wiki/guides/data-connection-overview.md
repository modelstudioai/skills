# data connection overview

数据连接是阿里云百炼平台管理外部数据源的统一入口。通过创建数据连接器，百炼应用可以安全地访问企业数据库、文档系统和对象存储中的数据，在对话中实时查询和引用这些数据。本文汇总了所有连接器类型的创建方式、前置条件和数据导入流程，详见[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 连接器类型

数据连接器按数据的存储和访问方式分为**平台托管**和**流处理**两大类：

### 平台托管

| 连接器类型 | 数据存储方式 | 适用场景 |
|-----------|-------------|---------|
| 文件 | 百炼平台或自有 OSS | 上传和管理非结构化文档（PDF、Word、Markdown 等） |
| 表格 | 百炼平台或自有 OSS | 导入和查询结构化表格数据（CSV、Excel 等） |

### 流处理

| 连接器类型 | 数据存储方式 | 适用场景 |
|-----------|-------------|---------|
| MySQL | 数据保留在原数据库，实时访问 | 连接 MySQL 数据库，执行 SQL 查询（仅 DMS 导入方式支持） |
| PostgreSQL | 数据保留在原数据库，实时访问 | 连接 PostgreSQL 数据库，执行 SQL 查询（仅 DMS 导入方式支持） |
| PolarDB-X 2.0 | 数据保留在原数据库，实时访问 | 连接阿里云 PolarDB-X 2.0 分布式数据库（仅 DMS 导入方式支持执行 SQL） |
| 语雀 | 数据保留在语雀，实时访问 | 访问语雀文档和知识库 |
| OSS | 数据保留在 OSS，实时访问 | 访问对象存储中的文件 |

## 前置条件

创建连接器前需确保：

- **账号权限**：主账号或具有数据连接管理权限的 RAM 用户。
- **数据源准备**（按连接器类型）：
  - **文件/表格**：准备好文档或表格文件，或已创建 OSS Bucket。
  - **MySQL**：已有 MySQL 实例（阿里云 RDS 或自建），网络可达。
  - **PostgreSQL**：已有 PostgreSQL 实例，且 `wal_level` 参数设置为 `logical`。
  - **PolarDB-X 2.0**：已有阿里云 PolarDB-X 2.0 实例，实例所在地域支持私网访问。
  - **语雀**：已有语雀知识库（仅支持公网版本），并获取个人访问 Token。
  - **OSS**：已创建 OSS Bucket 并开通向量检索服务。

## 创建连接器

访问百炼控制台的[数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)页面，点击**创建连接器**后选择类型。以下是各类型的关键配置差异，完整步骤请参阅[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

### 文件连接器

- 填写名称和描述（描述会影响应用调用准确度）。
- 存储位置选择：
  - **平台存储**：最大 100,000 个文件，1 TB 额度，限时免费。
  - **自有 OSS**：需在 Bucket 上添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`）。

### 表格连接器

- 填写名称和描述。
- 存储位置选择：
  - **平台存储**：1 TB 免费额度，超出后按量付费。
  - **自有 OSS**：同样需要 `bailian-connector-access` 标签。

### MySQL 连接器

- 数据来源方式：
  - **创建自定义数据源**：手动配置连接信息（支持阿里云 RDS MySQL 或自建 MySQL）。
  - **从 DMS 导入数据源**：快速导入 DMS 中已有的数据源（首次使用需完成 SLR 授权）。
- 网络类型：支持公网（需配置白名单）和私网。
- 关键配置：数据库地址、端口（默认 3306）、用户名、密码。

> **注意**：仅通过 DMS 导入方式创建的 MySQL 连接器支持执行 SQL 查询，自定义数据源方式不支持。

### PostgreSQL 连接器

- 需额外填写 `dbName`（数据库名称）。
- 数据库账号需具有 Superuser 或 REPLICATION 权限。
- 自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问。
- 连通性检测使用 DTS 服务（不同于 MySQL 使用 EventBridge）。

### PolarDB-X 2.0 连接器

- 仅支持**私网**连接，不支持公网。
- 仅支持阿里云 PolarDB-X 2.0 实例，不支持自建数据库。
- 首次使用需完成 DTS 和 PolarDB-X 服务管理角色的 SLR 授权。

### 语雀连接器

- 仅支持公网版本语雀。
- 需通过语雀开放 API 获取 Tenant access token。

### OSS 连接器

- 目标 Bucket 需添加 `bailian-datahub-access` 标签（值为 `read`）。
- 需开通向量检索服务，否则 `searchOSSFile` 和 `searchOSSFileByFileName` 工具不可用。
- 不支持归档、冷归档或深度冷归档存储类型的 Bucket。

## 数据库连接器差异对比

| 差异项 | MySQL | PostgreSQL | PolarDB-X 2.0 |
|-------|-------|------------|----------------|
| 默认端口 | 3306 | 5432 | 自动获取 |
| 额外必填字段 | 无 | dbName | 无 |
| 连通性检测服务 | EventBridge | DTS | EventBridge |
| 网络类型 | 公网/私网 | 公网/私网 | 仅私网 |
| 支持自建数据库 | 是 | 是 | 否 |
| 特殊配置 | 无 | `wal_level` 设为 `logical` | SLR 授权 DTS + PolarDB-X |

## 导入数据

### 导入文件

通过文件连接器的**详情**页面导入，支持按类目管理文件。关键步骤：

1. 选择或新建类目。
2. 点击**导入数据** > **本地上传**。
3. 选择解析方式：
   - **电子文档解析**：基础解析，不支持插图和图表。
   - **文档智能解析**：支持提取插图文本并生成摘要。
   - **大模型文档解析**：支持对插图和图表内容进行问答。
   - **Qwen VL 解析**：仅支持图片格式，可自定义识别 Prompt。
   - **音视频解析**：语音识别 + 视频帧提取 + 剧情解析。
4. 可选配置标签（API 调用时可通过 `tags` 参数筛选）。

> **注意**：平台不支持直接导入 JSON、CSV、YAML 格式文件，需先转换为 XLSX 或 XLS 格式。导入的文件仅支持查看最近 90 天内的记录。

### 导入表格

通过表格连接器的**详情**页面导入，支持两种方式创建数据表：

- **直接上传 Excel**：自动识别表头并创建数据表结构。
- **自定义表头**：手动配置列名、描述和类型。

> **注意**：数据表结构一旦确定无法修改。上传文件的表结构必须与数据表定义完全一致（列数、列名一一对应），否则导入失败。若字段类型为 `image_url`，需确保链接公开可访问。

## 限制和注意事项

- 所有流处理类连接器（MySQL、PostgreSQL、PolarDB-X 2.0）仅在通过 DMS 导入方式创建时才支持执行 SQL 查询。
- OSS 连接器不支持归档类存储，使用防盗链的 Bucket 需将 `*.console.aliyun.com` 加入白名单。
- 文件连接器的平台存储上限为 100,000 个文件 / 1 TB。
- PostgreSQL 连接器对数据库权限要求较高，需 Superuser 或 REPLICATION 权限。
- PolarDB-X 2.0 连接器仅支持私网，无法通过公网访问。
- 更多细节请参阅原始文档[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)



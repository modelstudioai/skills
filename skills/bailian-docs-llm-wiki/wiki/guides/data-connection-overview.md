# data connection overview

数据连接是阿里云百炼平台管理外部数据源的统一入口。通过创建数据连接器，百炼应用可以安全访问企业数据库、文档系统和对象存储中的数据，并在对话中实时查询和引用。数据连接器分为**平台托管**（文件、表格）和**流处理**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）两大类，覆盖结构化与非结构化数据场景。

## 连接器类型

根据[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)文档，连接器按数据存储和访问方式分为两类：

### 平台托管类型

| 连接器类型 | 数据存储方式 | 适用场景 |
|-----------|-------------|---------|
| 文件 | 百炼平台或自有 OSS | 上传和管理非结构化文档（PDF、Word、Markdown 等） |
| 表格 | 百炼平台或自有 OSS | 导入和查询结构化表格数据（CSV、Excel 等） |

### 流处理类型

| 连接器类型 | 数据存储方式 | 适用场景 |
|-----------|-------------|---------|
| MySQL | 数据保留在原数据库，实时访问 | 连接 MySQL 数据库，执行 SQL 查询（仅 DMS 导入方式） |
| PostgreSQL | 数据保留在原数据库，实时访问 | 连接 PostgreSQL 数据库，执行 SQL 查询（仅 DMS 导入方式） |
| PolarDB-X 2.0 | 数据保留在原数据库，实时访问 | 连接阿里云 PolarDB-X 2.0 分布式数据库 |
| 语雀 | 数据保留在语雀，实时访问 | 访问语雀文档和知识库（仅公网版本） |
| OSS | 数据保留在 OSS，实时访问 | 访问对象存储中的文件 |

## 前置条件

创建数据连接器前需确保：

- **账号权限**：主账号或具有数据连接管理权限的 RAM 用户（RAM 用户需主账号授权）
- **数据源准备**：
  - 文件/表格：已准备上传文件或已创建 OSS Bucket
  - MySQL：已有 RDS 或自建实例，网络可达
  - PostgreSQL：已有实例，且 `wal_level` 设置为 `logical`
  - PolarDB-X 2.0：已有实例，所在地域支持私网访问
  - 语雀：已有知识库（公网版本）并获取个人访问 [Token](../concepts/token.md)
  - OSS：已创建 Bucket 并开通向量检索服务

## 创建连接器

访问[数据连接页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，点击**创建连接器**，选择类型后按向导完成配置。

### 文件连接器

填写连接器名称和描述，选择存储位置：

- **平台存储**：最大 100,000 个文件，1 TB 存储额度（限时免费）
- **自有 OSS**：需完成授权，目标 Bucket 添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`）

### 表格连接器

配置方式与文件连接器类似，平台存储提供 1 TB 免费额度，超出后按量付费。

### MySQL 连接器

支持两种数据来源配置方式：

- **创建自定义数据源**：手动配置连接信息（阿里云 RDS MySQL 或自建 MySQL）
- **从 DMS 导入数据源**：快速导入已有 DMS 数据源（首次需完成 SLR 授权）

网络类型支持公网和私网。公网连接需将指定 IP 段加入数据库白名单。

> **注意**：仅通过 DMS 导入方式创建的 MySQL 连接器支持执行 SQL 查询，自定义数据源方式不支持直接执行 SQL。

### PostgreSQL 连接器

参照[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)文档，PostgreSQL 连接器有额外的前置要求：

- 数据库账号必须具有高权限（Superuser 或 REPLICATION 权限）
- `wal_level` 参数需设置为 `logical`
- 自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问

连通性检测使用 DTS（数据传输服务），而非 MySQL 连接器使用的 EventBridge。

### PolarDB-X 2.0 连接器

与 MySQL 连接器的主要差异：

- **网络类型**：仅支持私网，不支持公网
- **数据源**：仅支持阿里云 PolarDB-X 2.0 实例，不支持自建数据库
- **SLR 授权**：首次使用需授权 DTS 和 PolarDB-X 服务管理角色

### 语雀连接器

仅支持公网版本语雀。需获取 Tenant access token 并通过连接检测验证有效性。

### OSS 连接器

选择要连接的 Bucket，目标 Bucket 需添加 `bailian-datahub-access` 标签（值为 `read`）。使用 OSS 连接器需开通向量检索服务，否则无法使用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具。

> **注意**：不支持归档、冷归档或深度冷归档存储类型的 Bucket。如需使用开启 Referer 防盗链的 Bucket，须将 `*.console.aliyun.com` 添加到白名单 Referer 中。

## 数据导入

### 文件导入

进入文件连接器详情页，选择或新建类目后导入数据。支持多种解析方式：

| 解析方式 | 说明 |
|---------|------|
| 电子文档解析 | 基础解析，不支持文件中的插图与图表 |
| 文档智能解析 | 识别图中文本并生成摘要，参与知识库检索 |
| 大模型文档解析 | 支持用户对文件中插图和图表内容进行提问 |
| Qwen VL 解析 | 仅支持图片格式，可通过 Prompt 指定识别内容 |
| 音视频解析 | 语音识别 + 视频帧提取 + 剧情解析（可选） |

导入的文件作为独立副本存储在平台免费空间中，仅支持查看最近 90 天内导入的文件。

### 表格导入

进入表格连接器详情页，支持两种方式创建数据表：

- **直接上传 Excel**：自动识别表头创建数据表结构
- **自定义表头**：手动配置列名、描述和类型

> **注意**：数据表结构（列名、描述和类型）一旦确定无法修改。上传文件的列数和列名必须与数据表结构完全一致。

## 关键限制

根据[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)文档，使用数据连接时需注意以下限制：

- 流处理类连接器（MySQL/PostgreSQL/PolarDB-X 2.0）仅 DMS 导入方式支持执行 SQL 查询
- 文件连接器平台存储限时免费，上限 100,000 文件 / 1 TB
- 不支持直接导入 JSON、CSV、YAML 格式文件到文件连接器（需先转换为 XLSX/XLS）
- OSS 连接器不支持归档类存储的 Bucket
- 语雀连接器仅支持公网版本
- PolarDB-X 2.0 连接器仅支持私网连接

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)



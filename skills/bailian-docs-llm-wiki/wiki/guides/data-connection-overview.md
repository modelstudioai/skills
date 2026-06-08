# data connection overview

数据连接是阿里云百炼平台管理外部数据源的统一入口。通过创建数据连接器，百炼应用可以安全地访问企业数据库、文档系统和对象存储中的数据，在对话中实时查询和引用这些数据。平台提供平台托管和流处理两大类共 7 种连接器类型，覆盖非结构化文档、结构化表格和实时数据库查询等场景。

## 连接器类型

数据连接器按数据存储和访问方式分为两大类（详见[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)）：

### 平台托管类

| 连接器类型 | 数据存储方式 | 适用场景 |
|-----------|-------------|---------|
| 文件 | 百炼平台或自有 OSS | 上传和管理非结构化文档（PDF、Word、Markdown 等） |
| 表格 | 百炼平台或自有 OSS | 导入和查询结构化表格数据（CSV、Excel 等） |

### 流处理类

| 连接器类型 | 数据存储方式 | 适用场景 |
|-----------|-------------|---------|
| MySQL | 数据保留在原数据库 | 连接 MySQL 数据库，执行 SQL 查询（仅 DMS 导入方式支持） |
| PostgreSQL | 数据保留在原数据库 | 连接 PostgreSQL 数据库，执行 SQL 查询（仅 DMS 导入方式支持） |
| PolarDB-X 2.0 | 数据保留在原数据库 | 连接阿里云 PolarDB-X 2.0 分布式数据库 |
| 语雀 | 数据保留在语雀 | 访问语雀文档和知识库（仅支持公网版本） |
| OSS | 数据保留在 OSS | 访问对象存储中的文件 |

> **注意**：流处理类连接器中，MySQL、PostgreSQL 和 PolarDB-X 2.0 仅通过"从 DMS 导入数据源"方式创建时才支持执行 SQL 查询，"创建自定义数据源"方式不支持直接执行 SQL。

## 前置条件

创建连接器前需满足：

- **账号权限**：主账号或具有数据连接管理权限的 RAM 用户
- **数据源准备**（按连接器类型）：
  - 文件/表格：已准备文件或已创建 OSS Bucket
  - MySQL：已有 MySQL 实例（RDS 或自建），网络可达
  - PostgreSQL：已有实例且 `wal_level` 设置为 `logical`
  - PolarDB-X 2.0：已有阿里云 PolarDB-X 2.0 实例，所在地域支持私网访问
  - 语雀：已有语雀知识库（公网版本），已获取个人访问 Token
  - OSS：已创建 Bucket 并开通向量检索服务

## 创建连接器

访问百炼控制台的[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)页面，选择连接器类型并填写配置。

### 文件/表格连接器

1. 填写连接器名称和描述（描述会影响应用调用准确度）
2. 选择存储位置：
   - **平台存储**：文件连接器提供最大 100,000 个文件、1 TB 额度（限时免费）；表格连接器提供 1 TB 免费额度
   - **自有 OSS**：需为目标 Bucket 添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`）

### MySQL 连接器

支持两种数据来源配置：

- **创建自定义数据源**：手动配置连接信息（支持阿里云 RDS MySQL 和自建 MySQL）
- **从 DMS 导入数据源**：快速导入已有 DMS 数据源（需完成 EventBridge、RDS、DMS 三个 SLR 授权）

网络类型支持公网（需配置白名单）和私网。关键配置项包括数据库地址、端口（默认 3306）、用户名和密码。

### PostgreSQL 连接器

与 MySQL 的主要差异：

| 差异项 | MySQL | PostgreSQL |
|-------|-------|------------|
| 默认端口 | 3306 | 5432 |
| 额外必填字段 | 无 | dbName（数据库名称） |
| 连通性检测服务 | EventBridge | DTS |
| 特殊配置要求 | 无 | `wal_level` 设为 `logical` |

PostgreSQL 账号需具有 Superuser 或 REPLICATION 权限。自建实例还需在 `pg_hba.conf` 中允许 `100.64.0.0/16` 网段访问。

### PolarDB-X 2.0 连接器

与 MySQL 连接器的差异：仅支持私网连接、仅支持阿里云 PolarDB-X 2.0 实例（不支持自建）、首次使用需完成 DTS 与 PolarDB-X 服务管理角色的 SLR 授权。

### 语雀连接器

填写连接器名称后，需从语雀开放 API 获取 Tenant access token 并填入连接信息区域，通过连接检测验证 Token 有效性。

### OSS 连接器

选择要连接的 OSS Bucket，需为 Bucket 添加 `bailian-datahub-access` 标签（值为 `read`）。使用前需开通向量检索服务。不支持归档、冷归档或深度冷归档存储类型的 Bucket。

## 导入数据

### 导入文件

进入文件连接器详情页，选择类目后点击"导入数据"。支持多种解析方式（参考[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)获取详细说明）：

- **电子文档解析**：不支持解析插图与图表
- **文档智能解析**：可识别插图文本并生成摘要
- **大模型文档解析**：支持对插图和图表内容提问
- **Qwen VL 解析**：仅支持图片格式，可自定义 Prompt
- **音视频解析**：语音识别 + 视频帧提取 + 剧情解析

> **注意**：平台不支持直接导入 JSON、CSV、YAML 格式文件，需先转换为 XLSX 或 XLS 格式。

可选操作：为文件配置标签，通过 API 调用时可在 `tags` 参数中指定标签以提高检索效率。

### 导入表格

进入表格连接器详情页，选择或新建数据表。支持"直接上传 Excel"（自动识别表头）和"自定义表头"两种方式。

关键限制：
- 数据表结构（列名、描述、类型）一旦确定无法修改
- 上传文件的列数和列名必须与数据表结构完全一致
- `image_url` 类型字段需确保链接公开可访问，用于生成图片向量索引

## 限制与注意事项

- 文件连接器导入的文件仅支持查看最近 90 天内的记录（超期不可查看但不会被删除）
- 导入的文件作为独立副本存储，与原始数据无关联
- OSS 连接器不支持归档类存储；如启用 Referer 防盗链需将 `*.console.aliyun.com` 加入白名单
- 流处理类连接器的 SQL 执行能力仅限 DMS 导入方式创建的连接器
- PolarDB-X 2.0 连接器仅支持私网连接

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)



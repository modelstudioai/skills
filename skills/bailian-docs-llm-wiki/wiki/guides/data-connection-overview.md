# data connection overview

数据连接是阿里云百炼平台管理外部数据源的统一入口。通过创建数据连接器，应用可以安全访问企业数据库、文档系统和对象存储中的数据，在对话中实时查询和引用这些数据。详见[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 连接器类型

数据连接器按数据存储和访问方式分为两大类，详见下表：

| 类别 | 连接器类型 | 数据存储方式 | 适用场景 |
| --- | --- | --- | --- |
| 平台托管 | 文件 | 平台或自有 OSS | 上传和管理非结构化文档（PDF、Word、Markdown 等） |
| 平台托管 | 表格 | 平台或自有 OSS | 导入和查询结构化表格数据（CSV、Excel 等） |
| 流处理 | MySQL | 原数据库实时访问 | 连接 MySQL 数据库 |
| 流处理 | PostgreSQL | 原数据库实时访问 | 连接 PostgreSQL 数据库 |
| 流处理 | PolarDB-X 2.0 | 原数据库实时访问 | 连接阿里云 PolarDB-X 2.0 分布式数据库 |
| 流处理 | 语雀 | 语雀中实时访问 | 访问语雀文档和[知识库](../concepts/knowledge-base.md) |
| 流处理 | OSS | OSS 中实时访问 | 访问对象存储中的文件 |

> **注意**：流处理类（MySQL、PostgreSQL、PolarDB-X 2.0）的连接器，仅通过**从 DMS 导入数据源**方式创建的实例才支持执行 SQL 查询；通过**创建自定义数据源**方式添加的实例不支持直接执行 SQL。参见[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 前置条件

- **账号权限**：主账号或具有数据连接管理权限的 RAM 用户，RAM 用户需主账号授权后才能使用。
- **数据源准备**：
  - 文件/表格连接器：准备好上传的文件，或已创建 OSS Bucket。
  - MySQL 连接器：已有 RDS 或自建实例，并保证网络可达。
  - PostgreSQL 连接器：已有实例，且 `wal_level` 参数已设置为 `logical`。
  - PolarDB-X 2.0 连接器：已有阿里云 PolarDB-X 2.0 实例，且实例所在地域支持[私网访问](../concepts/vpc-private-access.md)。
  - 语雀连接器：已有语雀[知识库](../concepts/knowledge-base.md)（仅支持公网版本），并获取了个人访问 [Token](../concepts/token.md)。
  - OSS 连接器：已创建 OSS Bucket，并开通了向量检索服务。

## 创建连接器

在[数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)页面单击右上角**创建连接器**，选择类型并填写信息。

### 文件连接器

填写名称和描述（描述会用于指导应用调用准确度），选择存储位置：

- **平台存储**：提供最大 100,000 个文件、1 TB 额度，限时免费。
- **自有 OSS**：首次需按提示授权；目标 Bucket 需添加标签 `bailian-connector-access=ReadAndWrite`。

### 表格连接器

填写名称和描述后选择存储位置。平台存储提供 1 TB 免费额度，超额自动转按量付费；使用自有 OSS 的要求与文件连接器一致。

### MySQL 连接器

配置数据来源：

- **创建自定义数据源**：手动配置，支持阿里云 RDS MySQL（地址和端口按实例 ID 自动获取）或自建 MySQL（手动填写地址和端口）。
- **从 DMS 导入数据源**：首次需完成 EventBridge、RDS、DMS 三个服务关联角色授权。

网络类型可选**公网**（需将指定 IP 段加入白名单）或**私网**（需选择所属地域，更安全）。必填数据库用户名与密码，可选**开始检测**验证连通性。

### PostgreSQL 连接器

要求账号具备高权限（Superuser 或 REPLICATION），实例 `wal_level` 设为 `logical`；自建实例还需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问。默认端口 5432，必填 dbName、用户名、密码；连通性检测使用 DTS。

| 差异项 | MySQL | PostgreSQL |
| --- | --- | --- |
| 默认端口 | 3306 | 5432 |
| 额外必填字段 | 无 | dbName |
| 连通性检测 | EventBridge | DTS |
| 特殊配置 | 无 | `wal_level` 设为 `logical` |

### PolarDB-X 2.0 连接器

仅支持**私网**且仅支持阿里云 PolarDB-X 2.0 实例，不支持自建。首次使用需显式同意 DTS 与 PolarDB-X 两个服务管理角色的授权（DMS 方式还需 DMS 角色）。其余流程与 MySQL 类似。

### 语雀连接器

获取[语雀开放 API](https://www.yuque.com/yuque/developer/api)的 Tenant access token 并填入，单击**连接检测**验证 [Token](../concepts/token.md) 有效性。仅支持公网版本语雀。

### OSS 连接器

在**存储 Bucket 选择**下拉列表中选择要连接的 Bucket。目标 Bucket 需添加标签 `bailian-datahub-access=read`，并开通向量检索服务。不支持归档、冷归档或深度冷归档存储类型；支持内容加密和私有 Bucket；如需使用开启 Referer 防盗链的 Bucket，须将 `*.console.aliyun.com` 添加到白名单。

## 导入数据

### 导入文件

进入文件连接器**详情**，在类目下点击**导入数据**选择本地上传，选择解析方式：

- **电子文档解析**：不支持解析插图与图表。
- **文档智能解析**：识别并提取插图文本，生成摘要，参与检索。
- **大模型文档解析**：支持对文件插图和图表提问，需配合选择模型。
- **Qwen VL 解析**：仅支持图片格式，可自选千问 VL 模型并传入 Prompt。
- **音视频解析**：语音识别、视频帧提取、剧情解析按时间轴结构化对齐。

> 平台不支持直接导入 JSON、CSV、YAML 格式文件，需转换为 XLSX 或 XLS 后再导入。

可为文件配置标签，便于 API 调用时通过 `tags` 参数筛选。导入在高峰时段可能耗时数小时，仅支持查看最近 90 天内导入的文件，超出时间范围不可查看但不会删除。

### 导入表格

进入表格连接器**详情**，在数据表管理下新建数据表，可选**直接上传 Excel**（自动识别表头）或**自定义表头**（列名、类型必填，描述选填）。

> **重要**：数据表结构一旦确定无法修改；上传文件结构必须与表结构完全一致；建议在"描述"中提供清晰的自然语言说明，便于模型理解字段含义。详见[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 限制和注意事项

- 文件/表格使用自有 OSS 时，必须添加对应标签（文件/表格为 `bailian-connector-access=ReadAndWrite`，OSS 连接器为 `bailian-datahub-access=read`）。
- 流处理类连接器执行 SQL 查询仅限 DMS 导入方式。
- PolarDB-X 2.0 不支持公网、不支持自建实例。
- OSS 连接器不支持归档类存储，使用 searchOSSFile/searchOSSFileByFileName 工具需开通向量检索服务。
- 导入文件仅保留 90 天可查看期，且仅供当前[业务空间](../concepts/workspace.md)用户使用。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)





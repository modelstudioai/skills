# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可配置的数据接入入口。通过创建不同类型的连接器，开发者可将企业自有数据库、文档系统、对象存储等数据源接入百炼，支撑知识库构建、实时SQL查询、多模态文件解析等场景。所有连接器均基于最小权限原则设计，支持平台托管与流处理两类访问模式。

## 支持的模型/功能

数据连接器按数据访问方式分为两大类：

- **平台托管类**：适用于非结构化与结构化静态数据，包括  
  - **文件连接器**：支持 PDF、Word、Markdown、PPTX、Excel（.xlsx/.xls）、图像、音视频等格式，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行智能解析；支持电子文档解析、文档智能解析、大模型文档解析（含 Qwen-VL）及音视频解析等模式。  
  - **表格连接器**：支持 CSV（需转为 XLSX/XLS 后导入）、Excel（.xlsx/.xls），支持 `image_url` 字段类型以生成图片向量索引，用于以图搜图等场景。

- **流处理类**：适用于实时、动态数据源，支持 SQL 查询（**仅限通过 DMS 导入数据源方式创建的连接器**），包括  
  - **MySQL / PostgreSQL / PolarDB-X 2.0 连接器**：直连数据库执行 SELECT 查询，不落库；其中 PostgreSQL 要求 `wal_level=logical`，PolarDB-X 2.0 仅支持私网接入。  
  - **语雀连接器**：对接语雀开放 API（需 Tenant Access Token），仅支持公网版语雀。  
  - **OSS 连接器**：读取 OSS Bucket 中的文件，依赖[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)启用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具；目标 Bucket 需打 `bailian-datahub-access: read` 标签。

> **注意**：原始文档中多次强调“仅通过 DMS 导入数据源方式支持执行 SQL 查询”，但[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)未明确说明该限制是否适用于所有流处理连接器的全部能力（如元数据发现、表结构同步）。实际开发中请以控制台创建流程中的选项为准，避免依赖自定义数据源方式实现 SQL 执行。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；**描述直接影响智能体调用准确度**，建议明确数据内容与业务用途。 |
| **文件/表格** | 存储位置（平台存储 / 自有 OSS） | 平台存储提供限时免费额度（文件连接器：200,000 文件 + 1 TB；表格连接器：1 TB 免费）；自有 OSS 需授权并打 `bailian-connector-access: ReadAndWrite` 标签。 |
| **MySQL/PostgreSQL/PolarDB-X** | 网络类型、数据库地址/端口/用户名/密码、dbName（PostgreSQL 必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 2.0 **仅支持私网**；PostgreSQL 需提前配置 `wal_level=logical` 及 `pg_hba.conf` 白名单（100.64.0.0/16）。 |
| **语雀/OSS** | Tenant Access Token（语雀）、Bucket 名称（OSS） | 语雀 Token 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 需开通向量检索服务，且**不支持归档/冷归档/深度冷归档存储类型**。 |

## 使用方式

1. **创建连接器**：进入 [数据连接控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，单击「创建连接器」，按向导选择类型并填写参数。  
2. **验证连通性**：MySQL 使用 EventBridge 检测，PostgreSQL 使用 DTS 检测，语雀/OSS 提供一键检测按钮。  
3. **导入数据**：  
   - 文件连接器：在详情页 → 「导入数据」→ 选择类目 → 本地上传 → 配置解析方式与标签 → 确认。  
   - 表格连接器：在详情页 → 「数据表管理」→ 新建或选择数据表 → 上传 XLSX/XLS 文件（必须含表头）→ 配置字段类型（`image_url` 字段需确保 URL 公开可访问）。  
   > 注意：JSON/CSV/YAML 文件需先转换为 XLSX/XLS 格式，否则导入失败 —— 此限制在[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中被反复强调。  
4. **在应用中调用**：连接器创建并完成数据导入后，可在知识库配置、Agent 工具调用或 API 请求中直接引用（如通过 `tags` 参数过滤文件，或使用 `searchOSSFile` 工具）。

## 限制和注意事项

- **权限要求**：主账号或已获 RAM 授权的用户方可操作；首次使用自有 OSS 或 DMS 数据源时，需完成 SLR 角色授权（如 `AliyunServiceRoleForSFMConnectorAccessDTS`）。  
- **地域与网络**：PolarDB-X 2.0 连接器仅支持私网，且实例需与百炼服务同地域；MySQL/PostgreSQL 公网连接需将百炼指定 IP 段加入数据库白名单。  
- **数据时效性**：平台托管类连接器（文件/表格）导入后生成独立副本，**与原始数据无关联**；流处理类连接器（MySQL/PostgreSQL/OSS/语雀）始终读取源端最新数据。  
- **生命周期管理**：文件连接器仅支持查看最近 **90 天内导入的文件**（超期不可见但不删除）；每个业务空间最多创建 **500 个类目**（文件）或 **不限数量数据表**（表格），类目扩容需提交工单。  
- **兼容性限制**：  
  - 不支持归档类 OSS 存储类型；  
  - 语雀连接器**仅支持公网版**，不支持企业私有部署版；  
  - 大模型文档解析与 Qwen-VL 解析需对应模型能力支持，具体参见[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中关于解析方式的说明。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)



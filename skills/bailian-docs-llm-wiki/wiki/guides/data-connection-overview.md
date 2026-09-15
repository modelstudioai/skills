# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入入口。通过创建不同类型的数据连接器，开发者可将企业自有数据库、文档系统、对象存储等异构数据源接入百炼，支撑知识库构建、RAG 检索及智能体实时数据查询等场景。所有连接器均遵循最小权限原则，支持细粒度网络控制与访问审计。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入至百炼平台或用户自有 OSS，经解析后构建向量索引，供 RAG 场景使用；支持文档智能解析、大模型文档解析（含图表理解）、音视频多模态解析等 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：数据保留在源端，应用通过 SQL 查询（仅 DMS 导入方式支持）或 API 调用（如语雀、OSS）实时获取结果，适用于对数据新鲜度要求高的场景。  
> **注意**：MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器中，**仅通过“从 DMS 导入数据源”方式创建的实例支持执行 SQL 查询**；“创建自定义数据源”方式仅支持元数据同步，不支持运行时 SQL 执行 —— 此限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中多次强调，但部分旧版文档未明确区分，开发者务必以该文档为准。

## 关键参数

| 参数类别       | 关键字段/配置项                                                                 | 说明                                                                 |
|----------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------|
| **通用**       | 连接器名称、描述                                                                 | 描述建议明确数据内容与用途，直接影响智能体调用准确率                 |
| **文件/表格**  | 存储位置（平台存储 / 自有 OSS）、类目（文件）或数据表结构（表格）                | 平台存储限时免费（文件）或按量计费（表格）；OSS 需添加 `bailian-connector-access` 标签 |
| **MySQL**      | 数据库地址/端口（自动填充或手动输入）、用户名/密码、网络类型（公网/私网）       | 公网需配置白名单；私网需指定地域；DMS 导入方式支持 SQL，自定义方式不支持 |
| **PostgreSQL** | `wal_level=logical`、`listen_addresses`（自建需放行 `100.64.0.0/16`）、dbName 必填 | 高权限账号（Superuser 或 REPLICATION）为必需前置条件                  |
| **PolarDB-X**  | 仅支持私网、SLR 授权（`AliyunServiceRoleForSFMConnectorAccessDTS` 等）           | 不支持自建库；DMS 导入方式需额外授权 DMS 角色                        |
| **语雀/OSS**   | Tenant access token（语雀）、Bucket 名称 + `bailian-datahub-access` 标签（OSS） | 语雀仅支持公网版；OSS 不支持归档/冷归档存储类型                      |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 控制台 → 单击「创建连接器」→ 选择类型 → 填写基础信息与连接参数 → 完成 SLR 授权（如需）→ 执行连通性检测（EventBridge/DTS/[Token](../concepts/token.md) 验证）→ 确认创建。  
2. **导入数据**（仅平台托管型）：  
   - **文件**：进入连接器详情页 → 新建/选择类目 → 「导入数据」→ 本地上传 PDF/Word/Excel 等 → 选择解析方式（推荐「大模型文档解析」以支持图表理解）→ 可选配置标签 → 提交。  
   - **表格**：进入连接器详情页 → 新建/选择数据表 → 上传 XLSX/XLS（必须含表头）→ 结构校验通过后导入；**注意**：表结构一旦确定不可修改，且 `image_url` 字段需指向公开可访问 URL 才能生成图片向量索引 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
3. **在应用中调用**：  
   - 平台托管型：绑定至知识库后，由 RAG 流程自动检索；  
   - 流处理型：通过 `searchMySQL`、`searchPostgreSQL`、`searchYuqueDoc` 等内置工具在智能体工作流中调用，或通过 API 直接发起查询。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天导入记录（不可见但未删除）；文件连接器最多支持 200,000 个文件 / 1 TB（限时免费），表格连接器平台存储额度用尽后转为按量付费。  
- **格式限制**：当前**不支持直接导入 JSON/CSV/YAML 文件**，须转换为 XLSX/XLS（表格）或 PDF/Word（文件）后再上传 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **网络与权限**：  
  - MySQL 公网连接需将百炼服务 IP 段加入 RDS 白名单；  
  - PostgreSQL 自建实例需显式配置 `pg_hba.conf` 放行 `100.64.0.0/16`；  
  - OSS Bucket 若开启 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单。  
- **功能边界**：  
  - 所有流处理型连接器（MySQL/PostgreSQL/PolarDB-X）的 SQL 执行能力**严格依赖 DMS 导入方式**，自定义方式仅同步元数据；  
  - OSS 连接器启用 `searchOSSFile` 等工具前，**必须开通 OSS 向量检索服务**，否则调用失败。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)



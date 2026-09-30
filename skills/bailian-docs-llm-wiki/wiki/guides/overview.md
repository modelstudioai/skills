# overview

阿里云百炼 Connector 是一个面向智能体（Agent）的 MCP（Model Context Protocol）服务框架，用于安全、标准化地连接企业内外部系统（如文件存储、数据库、SaaS 应用等），将业务系统能力封装为可被大模型调用的工具。它不复制或索引原始数据，而是按需实时访问，兼顾数据新鲜度与权限隔离。

## 支持的模型/功能

Connector 本身不提供大模型推理能力，而是作为**工具编排与协议网关**，支持以下核心功能：

- **多源系统接入**：覆盖平台托管（文件、表格）、阿里云服务（OSS、MaxCompute）、关系型数据库（MySQL/PostgreSQL/PolarDB-X 2.0）、SaaS 应用（Salesforce、语雀、钉钉系列、腾讯文档、云效、邮箱）等 [共 15+ 类 App](raw/application-user-guide/overview/apps-guide/apps-overview.md)。
- **MCP 协议统一出口**：所有已连接 App 的工具通过单一 MCP 地址暴露，客户端只需配置一次即可发现并调用全部可用能力。
- **智能体驱动的工具选择**：工具由 App 类型自动生成（如文件连接器固定生成“搜索文件”和“获取文件”），参数与行为不可手动增删，智能体根据用户提问与连接器描述自动决策调用逻辑。
- **两类数据访问模式**：
  - *平台托管*：文件/表格连接器将数据副本存入百炼平台（限时免费，额度见[配额与限制](raw/application-user-guide/overview/reference-overview/limits.md)）；
  - *原系统直连*：OSS、数据库、Salesforce 等保持数据在源系统，Connector 仅转发请求。

> **注意**：文档 19 中 Salesforce 部分描述“Salesforce on Alibaba Cloud MCP 服务不会预先复制、切片或索引 Salesforce 业务数据”，与文档 2 中“Connector 不拉取、不切片、不建索引”一致；但文档 11 明确指出文件连接器“文件上传后由平台解析成可检索的格式”，说明其对非结构化文档做了内容解析（非向量索引），此为特例，非通用行为。

## 关键参数

- **`workspaceId`**：业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于构造 MCP 地址和资源隔离，必须与连接器所属空间一致。
- **`DASHSCOPE_API_KEY`**：用于 MCP 请求头鉴权（`Authorization: Bearer <key>`），需具备对应业务空间权限。
- **连接器元数据**：
  - `连接器名称`（必填，≤64 字符）：唯一标识同一 App 下的多个实例（如 `订单库-生产`）。
  - `连接器描述`（选填）：**直接影响智能体调用准确性**，需明确数据内容与用途（如“2024Q3产品手册，供回答功能咨询”），而非泛称“文档”。
- **App 特定凭证**：
  - OAuth 2.0 类（Salesforce、MaxCompute、语雀）：依赖身份验证配置中的 `Client ID`/`Client Secret` 或 `API Key`；
  - 钉钉系列：需完整 `StreamableHttp URL`（含 `?key=` 参数）；
  - 邮箱类：需邮箱地址 + 第三方授权码（非登录密码）；
  - OSS/数据库：依赖服务关联角色或 DMS 数据源配置。

## 使用方式

1. **准备环境**：开通百炼、创建业务空间、获取 `workspaceId` 和 `DASHSCOPE_API_KEY`。
2. **判断接入路径**：  
   - 若 App 卡片连接对话框中**仅有“选择身份验证配置”下拉框**，则需先创建配置（如 [Salesforce](raw/application-user-guide/overview/apps-guide/salesforce.md)、[语雀](raw/application-user-guide/overview/apps-guide/yuque.md)）；  
   - 其余 App（如文件、OSS、钉钉）可直接填写凭证完成连接。
3. **创建连接器**：在 Apps 页面选择目标 App → 填写名称/描述/凭证 → 确认。连接成功后，工具自动出现在 App 详情页的“可用的工具”区域。
4. **配置 MCP 客户端**：在 Qoder 等客户端中添加 MCP 服务器，URL 格式为 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，并注入 `DASHSCOPE_API_KEY`。
5. **发起调用**：客户端通过自然语言提问，智能体自动匹配工具、填充参数并执行。

## 限制和注意事项

- **配额约束**：平台托管存储限 200,000 文件 / 1 TB（[配额与限制](raw/application-user-guide/overview/reference-overview/limits.md)），类目上限 500 个/空间，单文件标签最多 100 个。
- **格式限制**：文件/表格连接器**不支持直接导入 JSON/CSV/YAML**，需先转换为 XLSX/XLS 或 PDF/Word。
- **凭证安全**：API Key、授权码、OAuth 密钥均为高危凭证，严禁明文提交至代码仓库或聊天工具；建议使用环境变量注入客户端配置。
- **连接生命周期**：凭证过期（如 Token 失效、OAuth 应用停用）会导致连接状态变为“已过期”，需重建身份验证配置及连接；删除连接**不可恢复**，且会立即中断依赖它的智能体任务。
- **迁移截止**：旧版数据连接需在 **2026 年 9 月 30 日前**完成迁移，逾期入口关闭，须手动重建（[数据连接迁移](raw/application-user-guide/overview/reference-overview/migration.md)）。
- **费用提示**：平台托管存储限时免费；但 OSS 连接器读取数据会产生 OSS 下行流量费，需单独计费。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)



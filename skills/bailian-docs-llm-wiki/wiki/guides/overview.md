# overview

阿里云百炼 Connector 是一个面向企业级数据源的统一接入平台，通过 MCP 协议将各类外部系统（如文件存储、数据库、SaaS 应用）的能力封装为可被智能体调用的工具。它不复制或索引原始数据，而是按需实时访问，兼顾安全性与数据新鲜度。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与协议网关**，将外部系统能力标准化为 MCP 工具供下游 Agent（如 Qoder、千问办公）调用。支持的 App 类型分为四类：

- **平台托管型**：无需外部凭证，数据上传至百炼平台存储（限时免费，上限 200,000 文件 / 1 TB）。包括 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)（PDF/Word/Markdown）、[表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)（XLSX/XLS），均自动生成固定工具（如“搜索文件”“获取表结构”）。
- **阿里云服务型**：通过服务关联角色授权访问，如 [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)（实时读取 Bucket）、[数据库](../../raw/application-user-guide/overview/apps-guide/database.md)（MySQL/PostgreSQL/PolarDB-X，需 DMS 录入）。
- **SaaS 集成型**：分三种身份验证路径：
  - **OAuth 2.0**：[Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)、[MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)（后者无需填凭证）、[云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)、[腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)；
  - **API Key**：仅 [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)，需会员 Token；
  - **MCP 接入地址**：6 个 [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)（文档/表格/AI 表格/待办/日历/机器人消息），地址含密钥，需从钉钉 AI 应用市场单独获取；
- **邮件协议型**：[QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md) 与 [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)，使用 IMAP/SMTP 授权码。

> **注意**：文档 17 中 Salesforce 的 OAuth 配置步骤与文档 6 存在细节差异——文档 6 明确要求 Callback URL 必须为 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`，而文档 17 未强调该 URL 的**完全一致性**（如末尾斜杠、协议大小写），实际部署中必须严格匹配，否则回调校验失败。

## 关键参数

- **业务空间 ID**（`workspaceId`）：MCP 地址的核心变量，格式如 `llm-xxxxxxxxxxxx`，决定客户端可访问的数据范围。
- **DashScope API Key**：用于 MCP 请求头 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，敏感凭证，禁止明文硬编码。
- **连接器名称/描述**：名称（≤64 字符）用于区分同类型连接；**描述非可选字段**，直接影响智能体工具选择准确率，需明确说明内容与用途（如“2024Q3产品手册，用于回答功能咨询”）。
- **身份验证凭证**：依 App 而异，包括 Salesforce 的 Client ID/Secret、语雀的 Token、钉钉的完整 MCP URL（含 `?key=`）、邮箱的授权码等。
- **类目与标签**：文件/表格连接器通过类目组织数据，单业务空间最多 500 个类目；单文件最多 100 个标签，总长 ≤700 字符，用于检索前过滤。

## 使用方式

1. **准备环境**：开通百炼、创建业务空间、获取 DashScope API Key、确认目标 App 的前置条件（如语雀会员、OSS Bucket 标签、DMS 数据源录入）。
2. **建立连接**：
   - 对需身份验证配置的 App（Salesforce/MaxCompute/语雀），先在 **身份验证配置** 页面创建配置，再在 App 连接对话框中选用；
   - 对直接连接的 App（文件/表格/OSS/数据库），在连接对话框填写名称、描述及对应凭证（如 Bucket 名、数据库地址）；
   - 对钉钉/云效/腾讯文档，按指引获取地址或完成弹窗授权。
3. **配置 MCP 客户端**：在 Qoder 等客户端中配置 MCP Server，URL 为 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，注入 API Key。
4. **调用工具**：客户端自动发现并调用工具，例如自然语言提问“找计费相关的 PDF”，触发文件连接器的“搜索文件”工具。

## 限制和注意事项

- **配额限制**：平台托管存储限 200,000 文件 / 1 TB；文件仅显示最近 90 天导入记录；类目上限 500 个（可工单扩容）；JSON/CSV/YAML 不支持直传，需转 XLSX/XLS。
- **安全约束**：API Key、钉钉 URL、邮箱授权码、语雀 Token 均属高危凭证，严禁提交至代码仓库或聊天工具；建议使用环境变量注入客户端配置。
- **连接管理**：连接器类型创建后不可更改；删除连接不可逆，且会立即中断依赖它的智能体任务；状态为“已过期”时需重建连接（非仅更新凭证）。
- **费用提示**：平台托管存储限时免费；但 OSS 下行流量、大模型解析、智能体调用模型等按各自计费规则单独收费。
- **迁移截止**：旧版数据连接一键迁移入口将于 **2026 年 9 月 30 日关闭**，逾期需手动重建，详见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)



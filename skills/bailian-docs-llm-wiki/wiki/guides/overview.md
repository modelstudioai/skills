# overview

Connector 是阿里云百炼平台提供的企业级数据连接中枢，用于将各类外部系统（如 SaaS 应用、数据库、对象存储、文档平台等）安全接入智能体工作流。它通过统一的 MCP 协议对外暴露工具能力，无需为每个系统单独开发集成代码。核心设计围绕「App → 身份验证配置 → 连接器 → 工具」四层抽象展开，兼顾安全性、复用性与开发者体验。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与数据访问中间件**，支持以下类型系统的连接与能力封装：

- **SaaS 应用**：Salesforce on Alibaba Cloud（OAuth 2.0）、语雀（API Key）、钉钉系列（MCP 接入地址）、云效、腾讯文档（授权窗口）、网易邮箱、QQ邮箱（IMAP/SMTP 授权码）；
- **数据库**：MySQL、PostgreSQL、PolarDB-X 2.0（通过 DMS 导入数据源）；
- **对象存储**：OSS（基于服务关联角色）；
- **平台托管数据**：文件连接器（PDF/Word/Markdown）、表格连接器（XLSX/XLS）；
- **大数据平台**：MaxCompute（OAuth 2.0，免填凭证）。

所有连接成功后，Connector 自动为对应 App 生成标准化工具（如 `搜索文件`、`获取表结构`、`列出代码库`），工具入参与出参在 App 详情页的「可用的工具」区域可查。工具调用时实时访问原系统，不预建索引或副本（知识库除外）[原文标题](../../raw/application-user-guide/overview/concepts.md)。

> **注意**：文档 18 中 Salesforce 的 OAuth 配置说明要求 Callback URL 必须严格匹配 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`，而文档 4 中同字段描述为 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback` —— 二者路径一致，但文档 18 强调“协议、域名、路径或末尾字符不一致均导致失败”，该强调性说明未见于文档 4，建议以文档 18 的严格校验要求为准。

## 关键参数

不同连接方式涉及的关键参数如下：

| 连接类型 | 必填参数 | 说明 |
|----------|----------|------|
| **需身份验证配置的 App**（Salesforce、MaxCompute、语雀） | `配置名称`（可选）、App 专属凭证（如 `组织域名`+`Client ID`+`Client Secret` 或 `API Key`） | 凭证由 App 决定，不可选；配置名称用于区分同一 App 下多个配置 [原文标题](../../raw/application-user-guide/overview/auth-guide/create-config.md) |
| **直接连接的 App**（文件/表格/OSS/数据库） | `连接器名称`（必填，≤64 字符）、`连接器描述`（可选，影响智能体工具选择准确度） | OSS 需额外完成服务关联角色授权并确保 Bucket 带标签 `bailian-datahub-access=read` [原文标题](../../raw/application-user-guide/overview/apps-guide/oss.md) |
| **钉钉系列** | `MCP 接入地址（含密钥）`（完整 URL，含 `?key=`） | 地址从钉钉 AI 应用服务市场获取，不可共用 [原文标题](../../raw/application-user-guide/overview/apps-guide/dingtalk.md) |
| **邮箱类**（QQ/网易） | `邮箱地址`、`授权码`（非登录密码） | 授权码仅显示一次，泄露需立即重置 [原文标题](../../raw/application-user-guide/overview/apps-guide/qq-mail.md) |

## 使用方式

标准流程分三步：

1. **判断前置条件**：单击 App 卡片「连接」，若对话框仅含「选择身份验证配置」下拉框，则需先创建配置（Salesforce、MaxCompute、语雀）；否则直接填写对话框字段（文件、OSS、钉钉等）；
2. **创建连接器**：
   - 对需配置的 App：进入「身份验证配置」→「创建」→ 选 App → 填凭证 → 完成；再回到 App 连接对话框选择该配置；
   - 对其他 App：在连接对话框中填完字段（如连接器名称、OSS Bucket、邮箱地址等）→ 点「确认」或「提交」；
3. **接入客户端**：使用 MCP 地址 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，配合 DashScope API Key 鉴权，即可在 Qoder 等兼容客户端中发现并调用所有已连接 App 的工具。

首次上手推荐用「文件连接器」，因其无需外部凭证且流程最简 [原文标题](../../raw/application-user-guide/overview/quickstart.md)。

## 限制和注意事项

- **配额限制**：平台托管存储（文件/表格连接器）上限为 200,000 个文件 + 1 TB 容量，限时免费；类目数上限 500 个/业务空间；单个文件标签最多 100 个，总长 ≤700 字符；仅支持查看最近 90 天内导入的文件 [原文标题](../../raw/application-user-guide/overview/reference-overview/limits.md)；
- **凭证安全**：API Key、授权码、MCP 接入地址中的 `key` 参数均为敏感凭证，禁止明文存入代码仓库或聊天工具；泄露后需立即在来源系统（语雀、邮箱、钉钉市场）作废并重建配置；
- **连接生命周期**：删除连接器不影响其依赖的身份验证配置；OAuth 应用被删除将导致所有关联连接立即中断且无法恢复；[Token](../concepts/token.md) 过期或密钥轮转后，连接状态变为「已过期」，需新建配置并重建连接；
- **格式与兼容性**：不支持直接导入 JSON/CSV/YAML 文件，需先转换为 XLSX/XLS；扫描件解析效果差时，可在导入时启用自定义解析设置；
- **费用提示**：OSS 连接器实时读取会产生 OSS 下行流量费，与 Connector 平台用量分开计费；大模型解析或智能体调用按对应模型规则计费。

## 来源文档

- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)



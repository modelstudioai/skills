# overview

Connector 是阿里云百炼平台提供的企业数据连接中枢，通过统一的 MCP 协议将各类业务系统（如数据库、SaaS 应用、对象存储等）的能力暴露给智能体与客户端。它不拉取、不索引原始数据，而是按需实时调用，确保数据时效性与权限一致性。核心设计围绕 App（系统类型）、身份验证配置（凭证蓝图）、连接器（实例）、工具（能力单元）和 MCP（服务协议）五层展开，支持开发者快速集成并安全复用。

## 支持的模型/功能

Connector 本身不提供模型，而是作为**工具编排与数据接入层**，支持以下功能类别：

- **平台托管型**：文件连接器、表格连接器——上传 PDF/Word/XLSX 等副本至百炼平台，自动生成 `搜索文件`、`获取文件`、`获取表结构` 等工具；详见[文件连接器](raw/application-user-guide/overview/apps-guide/file.md)。
- **云服务直连型**：OSS、MySQL、PostgreSQL、PolarDB-X 2.0——实时访问原系统，不产生副本；其中数据库依赖 DMS 统一管理数据源。
- **SaaS OAuth 型**：Salesforce on Alibaba Cloud、MaxCompute、语雀——需先创建身份验证配置；Salesforce 使用 OAuth 2.0，语雀使用 API Key；详见[身份验证概览](raw/application-user-guide/overview/auth-guide/auth-overview.md)。
- **MCP 接入型**：钉钉系列（文档/表格/待办等）、腾讯文档、云效——通过对方签发的 MCP URL 或授权窗口完成对接，无需本地凭证。
- **邮件协议型**：QQ邮箱、网易邮箱——使用邮箱地址 + IMAP/SMTP 授权码连接。

> **注意**：文档 10（Apps 目录）中将 MaxCompute 归类为“需要身份验证配置的 App”，但文档 21 明确指出其 OAuth 配置“无需填写任何凭证”，且文档 6 补充说明 MaxCompute 是“唯一不需要填任何凭证的 OAuth 2.0 配置”。该处表述存在冗余，实际操作中可跳过凭证填写步骤。

## 关键参数

- **MCP 地址**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，业务空间级，新增/删除连接器后客户端刷新即可同步工具列表。
- **认证头**：`Authorization: Bearer ${DASHSCOPE_API_KEY}`，API Key 需在百炼控制台 **API-KEY** 页面创建，属敏感凭证，禁止明文写入配置文件。
- **连接器名称**：必填，最多 64 字符，用于区分同类连接，建议体现用途与环境（如 `订单库-生产`）。
- **连接器描述**：非必填，但直接影响智能体调用准确性，应明确说明数据内容与适用场景（如“产品手册与发布说明，供回答产品功能问题时引用”）。
- **身份验证配置字段**：由 App 决定，Salesforce 需 `组织域名`、`Client ID`、`Client Secret`；语雀仅需 `API Key`（即语雀 [Token](../concepts/token.md)）；MaxCompute 无必填字段。

## 使用方式

1. **前置准备**：开通百炼服务、创建业务空间、获取 `workspaceId` 与 DashScope API Key；RAM 用户需主账号预先授权。
2. **判断接入路径**：单击 Apps 页面任一卡片的 **连接**，若对话框仅含“选择身份验证配置”下拉框，则需先建配置（见[创建身份验证配置](raw/application-user-guide/overview/auth-guide/create-config.md)）；否则直接填连接信息。
3. **创建连接器**：
   - 平台托管型（文件/表格）：填名称、描述，选“使用平台存储”；
   - SaaS/OAuth 型（Salesforce/语雀）：先建身份验证配置，再在连接时选用；
   - MCP 接入型（钉钉/腾讯文档）：粘贴完整含 `key=` 的 MCP URL，或完成授权弹窗；
   - 数据库型：从 DMS 导入已录入的数据源。
4. **验证与调用**：进入 App 详情页 → **可用的工具** 查看入参；在支持 MCP 的客户端（如 Qoder）中配置 MCP 服务器，发起自然语言提问触发工具调用。

## 限制和注意事项

- **配额限制**：平台托管存储限 200,000 个文件 / 1 TB，类目上限 500 个/业务空间，单个文件标签最多 100 个；文件仅支持查看最近 90 天内导入的记录。
- **格式限制**：不支持直接导入 JSON、CSV、YAML，需先转为 XLSX/XLS；扫描件建议启用自定义解析设置。
- **安全约束**：
  - API Key、OAuth Client Secret、语雀 [Token](../concepts/token.md)、邮箱授权码均为高危凭证，禁止截图、明文提交、共享至代码仓库；
  - OSS 连接需 Bucket 打标 `bailian-datahub-access=read`，否则无法出现在下拉列表；
  - 删除连接器不可逆，且会立即中断依赖它的智能体任务。
- **费用提示**：平台托管存储限时免费；OSS 连接器调用会产生 OSS 下行流量费；大模型解析与调用按对应模型计费。
- **迁移提醒**：旧版数据连接一键迁移入口将于 2026 年 9 月 30 日关闭，逾期需手动重建。

## 来源文档

- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)



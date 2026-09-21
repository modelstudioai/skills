# overview

Connector 是阿里云百炼平台提供的企业数据连接中枢，通过统一的 MCP 协议将各类外部系统（如文件、数据库、SaaS 应用）的能力暴露给智能体与客户端。它不拉取、不索引原始数据，而是按需实时调用目标系统 API，确保数据新鲜度与权限一致性。核心设计围绕 App（系统类型）、身份验证配置（凭证模板）、连接器（实例）、工具（能力单元）和 MCP（服务入口）五层展开。

## 支持的模型/功能

Connector 本身不提供模型，而是为大模型智能体提供结构化工具调用能力。其功能由所连接的 App 类型决定，当前支持以下几类：

- **平台托管类**：文件连接器（PDF/Word/Markdown）、表格连接器（XLSX/XLS），数据上传至平台存储，自动生成 `搜索文件`/`获取文件` 或 `获取表结构` 工具；详见[文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。
- **阿里云服务类**：OSS（对象存储）、MaxCompute（大数据计算）、MySQL/PostgreSQL/PolarDB-X 2.0（数据库），数据保留在原系统，通过服务关联角色或 DMS 接入，实时读取；其中 MaxCompute 无需填写凭证，仅需 OAuth 授权，见[MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)。
- **第三方 SaaS 类**：语雀（API Key）、Salesforce on Alibaba Cloud（OAuth 2.0）、钉钉系列（MCP 接入地址）、云效/腾讯文档（授权窗口），均通过标准协议完成身份认证与能力封装；例如钉钉系列需从[钉钉 AI 应用服务市场](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)获取含密钥的 StreamableHttp URL。
- **邮箱类**：QQ邮箱、网易邮箱，使用 IMAP/SMTP 授权码连接，凭证加密存储。

> **注意**：文档 17 中 Salesforce 的 OAuth 配置说明要求 Callback URL 必须严格匹配 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`，而文档 7 中同名文档给出的 Callback URL 缺少末尾斜杠（`/`），以文档 17 为准。

## 关键参数

所有连接器共用基础字段，App 特定参数由类型决定：

- **连接器名称**（必填，≤64 字符）：用于区分同一 App 下的多个实例，建议体现环境与用途（如 `订单库-生产`）。
- **连接器描述**（选填）：直接影响智能体工具选择准确率，需明确数据内容与适用场景（如“产品手册与发布说明，供回答产品功能问题时引用”）。
- **身份验证配置**（部分 App 必填）：Salesforce、MaxCompute、语雀三类 App 必须预先创建，见[身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)；其余 App（如文件、OSS、数据库）在连接对话框中直接填写凭证或选择数据源。
- **MCP 配置参数**（客户端侧）：
  - `url`: `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`
  - `headers.Authorization`: `Bearer ${DASHSCOPE_API_KEY}`

## 使用方式

完整流程分四步：

1. **准备前置条件**：确认阿里云账号已开通百炼、拥有业务空间 ID 与 DashScope API Key；RAM 用户需主账号提前授权。
2. **创建连接**：
   - 若 App 需身份验证配置（Salesforce/MaxCompute/语雀），先在 **身份验证配置** 页面创建（如语雀只需粘贴 Token）；
   - 在 **Apps** 页面选择目标 App，按提示填写连接信息（如文件连接器填名称与描述，OSS 选 Bucket 并完成 SLR 授权）。
3. **验证工具**：进入 App 详情页，在 **可用的工具** 区域查看自动生成的工具及其入参（如 `搜索文件` 需 `keyWord`，`获取表结构` 可传 `fuzzyTableName`）。
4. **接入客户端**：将 MCP 地址与 API Key 配置到支持 MCP 的客户端（如 Qoder），重启后即可调用工具。首次调用建议用自然语言提问，如“帮我在产品文档里找一下和计费相关的文件”。

## 限制和注意事项

- **配额限制**：平台托管存储（文件/表格连接器）上限为 200,000 个文件、1 TB，且仅支持查看最近 90 天内导入的文件；类目上限 500 个/业务空间；单个文件标签最多 100 个，总长度 ≤700 字符；详见[配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)。
- **格式限制**：文件连接器不支持直接导入 JSON/CSV/YAML；表格连接器仅支持 XLSX/XLS，不支持 CSV/JSON/YAML。
- **安全注意事项**：
  - API Key、OAuth Client Secret、钉钉 MCP URL 中的 `key`、邮箱授权码均为敏感凭证，禁止明文提交至代码仓库或聊天工具；
  - 语雀 Token 建议按用途单独生成，避免使用管理员账号；钉钉接入地址泄露后需在钉钉市场重置服务。
- **状态管理**：连接器状态为“已过期”时，需更新身份验证配置中的凭证并重建连接；删除连接不可撤销，且会立即中断依赖它的智能体与客户端调用。
- **迁移截止**：旧版数据连接的一键迁移入口将于 2026 年 9 月 30 日关闭，逾期需手动重建。

## 来源文档

- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)



# overview

阿里云百炼 Connector 是一个企业级数据连接平台，用于将各类外部系统（如文件存储、数据库、SaaS 应用等）安全接入大模型智能体，使其能实时调用原系统能力。它通过 MCP 协议统一对外暴露工具，无需数据迁移或索引构建，强调权限继承与实时访问。核心设计围绕 App、身份验证配置、连接器、工具四层抽象展开，支持快速验证与规模化管理。

## 支持的模型/功能

Connector 本身不提供模型，而是为智能体提供**工具调用能力**，覆盖以下三类数据源：

- **平台托管型**：文件连接器（PDF/Word/Markdown）、表格连接器（XLSX/XLS），数据上传至百炼平台解析并托管，适用于非结构化与轻量结构化数据。二者共享 [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md) 中定义的 200,000 文件 / 1 TB 存储额度。
- **原系统直连型**：OSS、MySQL、PostgreSQL、PolarDB-X 2.0、Salesforce on Alibaba Cloud、MaxCompute、语雀、钉钉系列、云效、腾讯文档、QQ邮箱、网易邮箱等。数据保留在原系统，Connector 仅在调用时实时访问，不产生副本。例如，[OSS 连接器](../../raw/application-user-guide/overview/apps-guide/oss.md) 通过服务关联角色授权访问 Bucket；[Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md) 通过 OAuth 2.0 授权后调用其 MCP 服务。
- **特殊接入型**：钉钉系列、云效、腾讯文档等通过独立授权窗口完成连接，无需用户准备凭证，适合快速上手。

所有 App 均按类型自动生成标准化工具（如“搜索文件”“获取表结构”“列出代码库”），数量与参数不可手动增删，详见各 App 文档。

## 关键参数

- **`workspaceId`**：业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于构造 MCP 地址 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，决定客户端可访问的数据范围。
- **`DASHSCOPE_API_KEY`**：用于 MCP 请求头 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，必须有效且未过期；RAM 用户需主账号预先授权才能使用 [快速开始](../../raw/application-user-guide/overview/quickstart.md) 中的流程。
- **连接器名称与描述**：名称（≤64 字符，必填）用于区分同类连接；描述（非必填）直接影响智能体工具选择准确度，应明确写明数据内容与用途，而非泛称。
- **身份验证凭证**：依 App 而异——OAuth 2.0 类（Salesforce、MaxCompute）需 Client ID/Secret 或 Scope；API Key 类（语雀）需 [Token](../concepts/token.md)；邮箱类需邮箱地址+授权码；钉钉类需完整含 `key=` 参数的 MCP 接入地址。

> **注意**：文档 18（Salesforce）中要求 Callback URL 为 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`，而文档 5（OAuth 2.0 配置）中同样引用该地址，但文档 1 的快速开始示例 MCP 地址路径为 `/api/v2/connector/mcp`。此处版本号 `v1`（OAuth 回调）与 `v2`（MCP 服务）属不同接口，无矛盾。

## 使用方式

1. **前置准备**：开通百炼服务、创建业务空间、获取 `workspaceId` 和 DashScope API Key；确认目标 App 是否需先建[身份验证配置](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)（如 Salesforce、语雀、MaxCompute）。
2. **创建连接**：
   - 若需身份验证配置：先在控制台 **身份验证配置** 页面创建（如为语雀填入 [Token](../concepts/token.md)），再在 App 连接对话框中选择该配置；
   - 若无需配置：直接在 App 连接对话框填写名称、描述等（如文件连接器），或粘贴凭证（如钉钉 MCP 地址、邮箱授权码）。
3. **导入数据（仅平台托管型）**：对文件/表格连接器，在类目下上传文件，等待平台解析完成。
4. **MCP 客户端接入**：将 MCP 地址与 API Key 配置到支持 MCP 的客户端（如 Qoder），重启后即可发现并调用所有已连接 App 的工具。
5. **调用验证**：在客户端用自然语言提问（如“找产品文档里计费相关的文件”），触发对应工具调用。

## 限制和注意事项

- **存储与配额**：平台托管存储（文件/表格连接器）有硬性上限（200,000 文件 / 1 TB），超出需提交工单扩容；类目数上限 500 个/业务空间；单个文件标签最多 100 个，总长 ≤700 字符 [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)。
- **格式限制**：文件连接器不支持 JSON/CSV/YAML 直接导入；表格连接器仅支持 XLSX/XLS，不支持 CSV/JSON/YAML [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。
- **凭证安全与轮转**：API Key、[Token](../concepts/token.md)、授权码、MCP 接入地址均属敏感凭证，严禁明文提交至代码仓库或聊天工具；轮转时需新建身份验证配置并重建连接，切勿在对方系统直接删除仍在使用的 OAuth 应用（会导致所有连接立即中断）。
- **连接器不可变性**：连接器创建后类型不可更改（如文件连接器不能转为 OSS 连接器），只能新建；删除连接器不可恢复，且会立即导致依赖它的智能体和客户端工具失效。
- **旧版迁移截止**：旧版数据连接的一键迁移入口将于 2026 年 9 月 30 日关闭，逾期需手动重建，成本显著增加 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
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
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)



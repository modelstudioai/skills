# overview

阿里云百炼 Connector 是统一管理外部数据源并对外提供 MCP 服务的平台，支持将企业各类系统（如文件、数据库、SaaS 应用）安全接入智能体。它不拉取或索引原始数据，而是在工具调用时实时访问原系统，确保数据时效性与权限一致性。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**能力编排与协议网关**，将外部系统的能力封装为标准化 MCP 工具供智能体调用。支持的 App 类型按连接方式分为三类：

- **直接连接型**：无需身份验证配置，连接对话框内一次性填写完成。包括 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)、[表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)、OSS、MySQL、PostgreSQL、PolarDB-X 2.0 等。
- **身份验证配置型**：需预先创建配置复用凭证。当前包括 Salesforce on Alibaba Cloud（OAuth 2.0）、MaxCompute（OAuth 2.0）、语雀（API Key）——详见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/overview.md)。
- **授权窗口型**：无前置凭证准备，单击连接后跳转至目标系统完成 OAuth 授权。包括云效、腾讯文档、钉钉系列（6 个 App）等。

> **注意**：文档 28 中旧版数据连接说明“文件/表格连接器支持‘使用自有OSS存储’”，但新版 Connector 的 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md) 和 [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md) 均明确指出“存储位置目前只有‘使用平台存储’一个选项”，且配额说明（文档 25）也仅针对平台托管存储。OSS 存储路径已由独立的 OSS 连接器承担，二者逻辑分离，旧版描述已过时。

## 关键参数

所有连接器共用以下核心字段（除钉钉、邮箱、授权窗口型 App 外）：
- `连接器名称`（必填，≤64 字符）：用于区分同类连接，建议体现用途与环境（如 `产品手册-生产`）。
- `连接器描述`（非必填，但强烈推荐）：影响智能体调用决策准确率，需写明数据内容与适用场景（如“2024 年客户合同模板，用于回答签约流程问题”）。

App 特定参数依类型而异：
- 文件/表格连接器：仅需选择“使用平台存储”（文档 11、12）；
- OSS 连接器：需完成服务关联角色授权，并确保 Bucket 带有 `bailian-datahub-access=read` 标签（文档 20）；
- 数据库连接器：依赖 DMS 录入的数据源，需从 DMS 列表中选择实例（文档 21）；
- 钉钉系列：仅需粘贴含 `?key=` 的完整 MCP 接入地址（文档 14）；
- 邮箱类：仅需填写邮箱地址与授权码（文档 15、16）。

## 使用方式

1. **创建连接**：在 Apps 页面选择目标 App → 按类型完成配置（直接填写、选身份验证配置或跳转授权）→ 确认创建。
2. **验证工具**：进入 App 详情页，在“可用的工具”区域查看自动生成的工具及其入参（如文件连接器固定生成“搜索文件”和“获取文件”）。
3. **配置 MCP 客户端**：在支持 MCP 的客户端（如 Qoder）中配置统一地址：
   ```json
   {
     "mcpServers": {
       "bailian-connector-mcp": {
         "type": "http",
         "url": "https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp",
         "headers": { "Authorization": "Bearer ${DASHSCOPE_API_KEY}" }
       }
     }
   }
   ```
   替换 `${workspaceId}`（业务空间 ID）和 `${DASHSCOPE_API_KEY}`（DashScope API Key），API Key 应通过环境变量注入以避免明文泄露（文档 1）。
4. **发起调用**：客户端自动发现工具，智能体根据自然语言提问自主选择工具并传参。

## 限制和注意事项

- **存储配额**：文件/表格连接器共享平台托管存储，上限为 **200,000 个文件 + 1 TB 容量**，限时免费；超出需提交工单扩容（文档 25）。
- **类目与标签**：单业务空间最多 500 个类目；单文件最多 100 个标签，全部标签总长 ≤700 字符（文档 25）。
- **格式限制**：不支持直接导入 JSON、CSV、YAML；需先转换为 XLSX/XLS 再通过表格连接器导入（文档 11、12、26）。
- **凭证安全**：API Key、授权码、MCP 接入地址均含敏感信息，禁止明文存于配置文件或代码仓库；泄露后须立即在源系统作废并重建连接（文档 7、14、15、16）。
- **状态维护**：连接状态为“已过期”时，需更新身份验证配置中的凭证并重建连接（文档 8）；删除连接不可逆，且会立即中断依赖它的智能体与工作流（文档 8）。
- **迁移截止**：旧版数据连接需在 **2026 年 9 月 30 日前**完成迁移，逾期将关闭一键入口，需手动重建（文档 23、24）。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/overview.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/overview.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [参考](../../raw/application-user-guide/overview/overview.md)
- [数据连接迁移](../../raw/application-user-guide/overview/overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/overview/faq.md)
- [旧版数据连接](../../raw/application-user-guide/overview/data-connection-overview.md)
- [数据连接](../../raw/application-user-guide/overview/data-connection-overview/data-connection.md)



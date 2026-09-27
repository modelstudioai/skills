# overview

阿里云百炼 Connector 是一个面向企业级系统的统一连接平台，支持通过 MCP 协议将各类外部数据源与业务系统（如文件、数据库、SaaS 应用等）安全接入智能体。它不拉取或索引原始数据，而是在工具调用时实时访问原系统，兼顾数据新鲜度与权限隔离。核心设计围绕 App、身份验证配置、连接器、工具和 MCP 五层抽象展开，开发者可快速建立连接并集成至任意兼容 MCP 的客户端。

## 支持的模型/功能

Connector 本身不提供大模型推理能力，而是作为**工具编排与系统集成层**，将外部系统的能力封装为标准 MCP 工具供智能体调用。其功能覆盖三类数据源：

- **平台托管型**：如 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md) 和 [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)，上传非结构化/结构化文档副本至百炼平台存储（限时免费，额度见[配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)），自动生成 `搜索文件`/`获取文件` 或 `获取表结构` 等工具；
- **实时访问型**：如 [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)、[数据库](../../raw/application-user-guide/overview/apps-guide/database.md)、[Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)、[MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)，数据保留在原系统，Connector 通过服务角色或 OAuth 实时读取，工具能力由目标系统接口决定；
- **授权窗口型**：如 [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)、[云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)，无需预置凭证，单击连接后弹出第三方授权页完成 OAuth 流程。

> **注意**：文档 19 中 Salesforce 的 OAuth Scopes 描述为 `api`/`web`/`refresh_token, offline_access`，而文档 6 明确要求 `offline_access` 必须与 `refresh_token` 同时启用；若仅填 `refresh_token` 而未勾选 `offline_access`，可能导致令牌刷新失败。请以文档 6 的完整三项为准。

## 关键参数

所有连接均依赖以下关键参数，需在控制台或客户端配置中准确填写：

- `workspaceId`：业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于路由 MCP 请求并隔离资源，必须与创建连接器的空间一致；
- `DASHSCOPE_API_KEY`：DashScope API Key，用于 MCP 鉴权，需在请求头中以 `Bearer ${DASHSCOPE_API_KEY}` 格式传递；
- `connection name`：连接器名称（最多 64 字符），用于区分同一 App 下的多个实例，建议体现环境与用途（如 `订单库-生产`）；
- `connection description`：连接器描述（非必填但强烈推荐），直接影响智能体调用决策，应明确说明数据内容与适用场景（例如“产品手册与发布说明，供回答产品功能问题时引用”）；
- `MCP URL`：固定格式 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，路径必须为 `/api/v2/connector/mcp`（文档 1 明确指出返回 404 的常见原因是路径错误）。

## 使用方式

1. **前置准备**：开通百炼服务，创建业务空间，获取 `workspaceId` 和 DashScope API Key；
2. **选择 App 并判断认证模式**：进入 **Apps** 页面，单击目标 App 卡片。若连接对话框仅含“选择身份验证配置”下拉框，则需先创建配置（如 [Salesforce](../../raw/application-user-guide/overview/apps-guide/salesforce.md)、[语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)）；否则直接填写连接信息（如 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)、[QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)）；
3. **创建连接器**：按向导填写名称、描述等通用字段，以及 App 特定字段（如 OSS 的 Bucket 选择、钉钉的 MCP 接入地址）；
4. **配置 MCP 客户端**：在 Qoder 等客户端中添加 MCP 服务器，填入上述 `MCP URL` 和 `API Key`；
5. **发起调用**：客户端自动发现工具，智能体根据用户提问选择并调用（如自然语言“找计费相关的文件”，触发 `搜索文件` 工具）。

## 限制和注意事项

- **存储限制**：平台托管存储（文件/表格连接器）上限为 200,000 个文件 + 1 TB，且仅支持查看最近 90 天内导入的文件（[配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)）；
- **格式限制**：不支持直接导入 JSON、CSV、YAML 文件，需先转换为 XLSX/XLS（文档 11、12、26 均强调此限制）；
- **凭证安全**：API Key、OAuth Client Secret、邮箱授权码等敏感凭证严禁明文保存于配置文件或代码仓库；优先使用客户端环境变量注入（文档 1 提示）；
- **连接器不可变性**：创建后无法修改类型（如文件连接器不能转为数据库连接器），只能新建；
- **迁移截止**：旧版数据连接的一键迁移入口将于 2026 年 9 月 30 日关闭，逾期需手动重建（[数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)）；
- **费用提示**：OSS 连接器调用会产生 OSS 下行流量费，与 Connector 用量分开计费（文档 20、25）。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
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
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)



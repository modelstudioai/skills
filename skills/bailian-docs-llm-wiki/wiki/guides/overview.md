# overview

阿里云百炼 Connector 是一个面向企业级 AI 应用的数据连接平台，通过统一 MCP 协议将各类业务系统（如文件、数据库、SaaS 应用）的能力封装为可被智能体调用的工具。它不复制或索引原始数据，而是按需实时访问，兼顾数据新鲜度与权限隔离。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与协议网关**，支持以下能力类型：

- **平台托管型 App**：文件连接器、表格连接器 —— 数据上传至百炼平台存储，由平台解析并提供结构化访问能力；[文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)生成 `搜索文件` 和 `获取文件` 工具；[表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)生成 `获取表结构` 工具。
- **原系统直连型 App**：OSS、MySQL、PostgreSQL、PolarDB-X 2.0、语雀、Salesforce on Alibaba Cloud、MaxCompute、云效、腾讯文档、钉钉系列、QQ邮箱、网易邮箱 —— 数据保留在源系统，Connector 仅代理调用，权限与时效性由源系统保障。
- **协议统一接入**：所有已连接 App 的工具均通过标准 MCP 接口暴露，客户端只需配置一次 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp` 地址即可发现并调用全部工具。

> **注意**：文档 19 中 Salesforce 配置说明存在不完整字段（末尾截断：“8. 复…”），实际配置需参考 [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md) 获取完整 Client Secret 流程。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspaceId` | 业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于路由 MCP 请求和资源隔离 | 必填，从百炼控制台获取，见[快速开始](../../raw/application-user-guide/overview/quickstart.md) |
| `DASHSCOPE_API_KEY` | DashScope API Key，用于 MCP 请求鉴权 | 必填，需在百炼控制台 API-KEY 页面创建，见[快速开始](../../raw/application-user-guide/overview/quickstart.md) |
| `keyWord` / `fileId` / `tableId` 等 | 各 App 自动生成工具的入参，由 Connector 根据 App 类型固定定义 | 不可自定义，详见各 App 文档，如[文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md) |
| 连接器名称 & 描述 | 名称（≤64 字符）用于区分实例；描述影响智能体工具选择准确率，需写明内容与用途 | 建议具体化，避免“连接器1”等模糊命名 |

## 使用方式

1. **前置准备**：开通百炼服务、创建业务空间、获取 `workspaceId` 和 `DASHSCOPE_API_KEY`；
2. **判断连接模式**：单击 Apps 卡片 → 若连接对话框仅含“选择身份验证配置”下拉框，则需先建配置（如 Salesforce、语雀、MaxCompute）；否则直接填写凭证（如文件、OSS、数据库）；
3. **创建连接**：
   - 需配置类目的 App（文件、表格）：先建类目，再导入数据；
   - OAuth 类 App（云效、腾讯文档）：新开窗口授权；
   - 钉钉/邮箱类 App：粘贴含密钥的完整 MCP 地址或授权码；
4. **MCP 客户端接入**：在 Qoder 等客户端中配置 MCP Server，替换 `workspaceId` 和 `API_KEY`；
5. **调用验证**：自然语言提问（如“找计费相关文件”），客户端自动路由至对应工具。

## 限制和注意事项

- **配额限制**：平台托管存储限 200,000 文件 + 1 TB，类目上限 500 个，单文件标签 ≤100 个且总长 ≤700 字符；文件仅可查看最近 90 天内导入的记录（见[配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)）；
- **格式限制**：JSON/CSV/YAML 不支持直接导入，须转为 XLSX/XLS 后通过表格连接器处理；
- **安全要求**：
  - API Key、授权码、MCP 地址中的 `key` 参数均为敏感凭证，禁止明文提交至代码仓库或聊天工具；
  - OSS Bucket 必须打标签 `bailian-datahub-access=read` 才可被识别；
- **迁移截止**：旧版数据连接一键迁移入口将于 **2026 年 9 月 30 日关闭**，逾期需手动重建（见[数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)）；
- **状态管理**：连接状态为“已过期”时，需更新身份验证配置凭证并重建连接，删除连接不会影响其复用的身份验证配置。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)



# overview

阿里云百炼 Connector 是一个面向企业级 AI 应用的数据连接平台，支持将各类业务系统（如文件存储、数据库、SaaS 应用等）以标准化 MCP 工具形式接入智能体与客户端。它不复制或索引原始数据，而是在调用时实时访问源系统，兼顾数据新鲜度与权限一致性。

## 支持的模型/功能

Connector 本身不提供大模型推理能力，而是作为**工具编排与协议网关层**，将外部系统的能力封装为符合 [MCP](../../raw/application-user-guide/overview/concepts.md) 规范的工具供智能体调用。其核心功能包括：

- **多源连接**：覆盖三类数据源：
  - *平台托管*：文件连接器、表格连接器（上传副本，解析后提供检索）；
  - *云服务直连*：OSS、MySQL、PostgreSQL、PolarDB-X 2.0（实时访问，不存副本）；
  - *SaaS 集成*：语雀、Salesforce on Alibaba Cloud、MaxCompute、钉钉系列、云效、腾讯文档、邮箱等（通过 OAuth、API Key 或 MCP 接入地址授权）。
- **自动工具生成**：每个连接器创建后，Connector 根据 App 类型自动生成固定工具集（如文件连接器生成 `搜索文件` 和 `获取文件`），无需手动配置，详见[各 App 的说明](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。
- **统一 MCP 暴露**：所有已连接 App 的工具通过单个 MCP 地址聚合暴露，客户端只需配置一次即可发现并调用全部工具。

> **注意**：文档 11（文件连接器）与文档 23（常见问题）均指出“搜索文件”仅按**文件标题关键词匹配**，不支持正文语义检索；若需内容归纳，应配合知识库使用——这与文档 2 中“和知识库的区别”所述一致，无矛盾。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `workspaceId` | 业务空间 ID，形如 `llm-xxxxxxxxxxxx`，用于路由 MCP 请求 | 必填，从百炼控制台获取；见[快速开始](../../raw/application-user-guide/overview/quickstart.md) |
| `DASHSCOPE_API_KEY` | DashScope API Key，用于 MCP 请求鉴权 | 必填，需在控制台 API-KEY 页面创建；见[快速开始](../../raw/application-user-guide/overview/quickstart.md) |
| 连接器名称 | 最多 64 字符，用于区分同一 App 下的多个连接 | 必填，创建后可修改；见[连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md) |
| 连接器描述 | 非必填，但强烈建议写明数据内容与用途（如“产品手册与发布说明，供回答产品功能问题时引用”） | 描述直接影响智能体选择工具的准确度；见[核心概念](../../raw/application-user-guide/overview/concepts.md) |

## 使用方式

1. **前置准备**：开通百炼服务、创建业务空间、获取 `workspaceId` 与 `DASHSCOPE_API_KEY`。
2. **判断连接类型**：进入 Apps 页面，单击目标 App 的 **连接**：
   - 若对话框仅有“选择身份验证配置”下拉框 → 需先创建配置（如 Salesforce、语雀）；
   - 若对话框含连接器名称/描述等字段 → 直接填写（如文件、OSS、钉钉）；
   - 若弹出独立授权窗口 → 直接登录授权（如云效、腾讯文档）。
3. **创建连接器**：按向导完成凭证填写或授权（OAuth 2.0、API Key、MCP 地址等），确认后连接即生效。
4. **配置 MCP 客户端**：在 Qoder 等客户端中添加 MCP 服务器，URL 格式为 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，并注入 `Authorization: Bearer ${DASHSCOPE_API_KEY}`。
5. **调用工具**：客户端自动同步工具列表，智能体根据自然语言请求自主选择并调用对应工具。

## 限制和注意事项

- **配额限制**：平台托管存储（文件/表格连接器）上限为 **200,000 个文件 + 1 TB**，且仅支持查看最近 90 天内导入的文件；类目数上限 500 个/业务空间（见[配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)）。
- **格式限制**：JSON、CSV、YAML 文件**不支持直接导入**，需先转换为 XLSX/XLS 再通过表格连接器处理（见[文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md) 和 [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)）。
- **凭证安全**：API Key、授权码、MCP 接入地址（含 `key=` 参数）均为敏感凭证，严禁明文提交至代码仓库或聊天工具；推荐使用环境变量注入客户端配置（见[快速开始](../../raw/application-user-guide/overview/quickstart.md)）。
- **连接器不可变性**：连接器类型（如文件→OSS）创建后不可修改，只能新建；删除连接器不可恢复，且会立即中断依赖它的智能体与工作流（见[连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)）。
- **旧版迁移截止**：一键迁移旧版数据连接的入口将于 **2026 年 9 月 30 日关闭**，逾期需手动重建（见[数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)）。

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
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)



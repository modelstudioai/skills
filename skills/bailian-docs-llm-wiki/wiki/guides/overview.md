# overview

阿里云百炼 Connector 是统一管理企业外部数据源的平台，通过 MCP 协议将各类系统（如文件、数据库、SaaS 应用）的能力封装为可被智能体调用的工具。它不复制或索引原始数据，而是按需实时访问，兼顾数据新鲜度与安全隔离。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与路由层**，支持以下三类数据源接入：

- **平台托管型**：文件连接器、表格连接器。数据上传至百炼平台存储（限时免费，额度见[配额与限制](raw/application-user-guide/overview/overview/limits.md)），适用于非结构化文档（PDF/Word/Markdown）和结构化表格（XLSX/XLS）。  
- **流处理型（实时访问）**：MySQL、PostgreSQL、PolarDB-X 2.0、OSS、语雀、钉钉系列、云效、Salesforce on Alibaba Cloud、MaxCompute。数据保留在原系统，Connector 仅在调用时发起请求，支持读写操作（如钉钉文档、待办；Salesforce 记录查询）。  
- **MCP 统一暴露**：所有已连接 App 的工具均通过一个业务空间级 MCP 地址对外提供，客户端无需为每个 App 单独配置。详见[快速开始](raw/application-user-guide/overview/quickstart.md)中的配置示例。

> **注意**：文档 23 中旧版“数据连接”页面仍提及“使用自有OSS存储”选项，但新版 Connector 的文件/表格连接器**仅支持“使用平台存储”**（见文档 9 和文档 10），OSS 作为独立 App（文档 15）或批量导入来源存在，二者逻辑分离，不可混用。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间 ID，形如 `llm-xxxxxxxxxxxx`，用于构造 MCP 地址和资源隔离 | 必填，控制台可查 |
| `DASHSCOPE_API_KEY` | 用于 MCP 请求鉴权的 Bearer [Token](../concepts/token.md) | 敏感凭证，禁止明文硬编码；建议通过环境变量注入（见[快速开始](raw/application-user-guide/overview/quickstart.md)） |
| 连接器名称 | 同一 App 下区分多个连接的标识 | 最多 64 字符，创建后可修改（见[连接的账户](raw/application-user-guide/overview/overview/connected-accounts.md)） |
| 连接器描述 | 影响智能体调用决策的关键元信息 | 建议具体说明内容与用途（如“产品手册与发布说明，供回答计费问题”），非摆设 |

## 使用方式

1. **准备前置条件**：开通百炼、获取 `workspaceId` 和 `DASHSCOPE_API_KEY`、确认目标 App 所需凭证（如语雀 API Key、Salesforce OAuth 配置、钉钉 MCP 接入地址）。  
2. **创建连接**：  
   - *无需身份验证配置的 App*（如文件、表格、钉钉、云效）：直接在 Apps 页面点击“连接”，填写名称/描述等基础字段即可。  
   - *需身份验证配置的 App*（如语雀、Salesforce、MaxCompute）：先在“身份验证配置”页面创建配置（见[创建身份验证配置](raw/application-user-guide/overview/overview/create-config.md)），再于连接对话框中选择该配置。  
3. **配置客户端**：将 MCP 地址 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp` 与 API Key 注入客户端（如 Qoder）的 MCP 配置文件。  
4. **调用工具**：客户端自动发现并列出所有已连接 App 的工具，智能体根据用户提问自主选择调用（如“搜索文件”、“获取表结构”）。

## 限制和注意事项

- **存储限制**：平台托管存储上限为 **200,000 个文件 + 1 TB 容量**（见[配额与限制](raw/application-user-guide/overview/overview/limits.md)），超限需提交工单扩容。  
- **文件时效性**：仅支持查看最近 **90 天内导入的文件**，过期文件不再展示（但未删除）。  
- **格式限制**：不支持直接导入 JSON/CSV/YAML（见文档 9、10、22），须先转换为 XLSX/XLS 或通过数据库/OSS 连接器接入。  
- **凭证安全**：API Key、MCP 接入地址（含 `key=` 参数）、OAuth Client Secret 均为敏感凭证，严禁泄露至代码仓库、聊天工具或工单（见[API Key 配置](raw/application-user-guide/overview/overview/api-key.md)及[钉钉系列](raw/application-user-guide/overview/overview/dingtalk.md)）。  
- **连接不可变**：连接器类型（如文件 → MySQL）创建后不可修改，只能新建（见文档 5、19）。  
- **迁移截止**：旧版数据连接需在 **2026 年 9 月 30 日前完成迁移**，否则需手动重建（见[数据连接迁移](raw/application-user-guide/overview/overview/migration.md)）。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/overview/create-config.md)
- [身份验证概览](../../raw/application-user-guide/overview/overview.md)
- [连接的账户](../../raw/application-user-guide/overview/overview/connected-accounts.md)
- [API Key 配置](../../raw/application-user-guide/overview/overview/api-key.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/overview/oauth.md)
- [Apps 目录](../../raw/application-user-guide/overview/overview.md)
- [文件连接器](../../raw/application-user-guide/overview/overview/file.md)
- [表格连接器](../../raw/application-user-guide/overview/overview/table.md)
- [语雀](../../raw/application-user-guide/overview/overview/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/overview/dingtalk.md)
- [云效](../../raw/application-user-guide/overview/overview/yunxiao.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/overview/salesforce.md)
- [OSS](../../raw/application-user-guide/overview/overview/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/overview/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/overview/database.md)
- [参考](../../raw/application-user-guide/overview/overview.md)
- [配额与限制](../../raw/application-user-guide/overview/overview/limits.md)
- [数据连接迁移](../../raw/application-user-guide/overview/overview/migration.md)
- [旧版数据连接](../../raw/application-user-guide/overview/data-connection-overview.md)
- [常见问题](../../raw/application-user-guide/overview/overview/faq.md)
- [数据连接](../../raw/application-user-guide/overview/data-connection-overview/data-connection.md)



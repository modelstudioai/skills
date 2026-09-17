# overview

阿里云百炼 Connector 是统一管理企业外部数据源的平台能力，通过 MCP 协议将各类系统（如文件、数据库、SaaS 应用）的能力封装为工具，供智能体按需调用。它不拉取、不建索引，而是实时访问原系统，兼顾数据新鲜度与权限继承性。核心设计围绕 App → 连接器 → 工具三层抽象，支持快速接入与规模化管理。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与协议网关**，将外部系统能力标准化暴露给下游智能体（如 Qwen、Qoder）。其功能覆盖三类数据源：

- **平台托管型**：文件连接器、表格连接器——上传非结构化/结构化文档至平台存储，自动生成 `搜索文件`/`获取文件`/`获取表结构` 等工具；  
- **实时访问型**：OSS、数据库（MySQL/PostgreSQL/PolarDB-X 2.0）、语雀、Salesforce on Alibaba Cloud、MaxCompute、云效、钉钉系列——数据保留在原系统，调用时实时读取；  
- **协议桥接型**：所有连接器最终统一通过 MCP 协议对外提供服务，地址格式为 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，客户端只需配置一次即可发现全部已连接 App 的工具。

> **注意**：文档 21（旧版数据连接）中提到“使用自有OSS存储”时要求标签为 `bailian-connector-access=read`，而文档 15（OSS）和文档 19（常见问题）明确要求标签为 `bailian-datahub-access=read`。实际生效的是后者，[OSS](../../raw/application-user-guide/overview/overview/oss.md) 和 [常见问题](../../raw/application-user-guide/overview/overview/faq.md) 中的描述为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间 ID，形如 `llm-xxxxxxxxxxxx`，用于路由 MCP 请求 | 必填，跨空间不可见 |
| `DASHSCOPE_API_KEY` | 用于 MCP 鉴权的 Bearer [Token](../concepts/token.md) | 敏感凭证，需加密存储，避免明文泄露 |
| 连接器名称 | 区分同类连接的标识 | 最多 64 字符，创建后可修改 |
| 连接器描述 | 影响智能体调用决策的关键元信息 | 建议写明内容与用途，如“产品手册与发布说明，供回答计费问题” |
| 类目 | 文件/表格的组织单位 | 每业务空间最多 500 个，支持多级嵌套 |

## 使用方式

1. **准备前置条件**：开通百炼服务、创建业务空间、获取 DashScope API Key；  
2. **创建连接器**：  
   - 直连型（文件、表格、OSS、钉钉、云效）：在 Apps 页面单击对应卡片 → 填写名称/描述 → 完成授权或配置；  
   - 需身份验证型（语雀、Salesforce、MaxCompute）：先在[身份验证配置](../../raw/application-user-guide/overview/overview/create-config.md)页面创建配置（API Key 或 OAuth 2.0），再在连接对话框中选择；  
3. **导入数据（仅平台托管型）**：文件/表格连接器需上传数据后工具才可检索；  
4. **配置 MCP 客户端**：将 MCP 地址与 API Key 注入客户端（如 Qoder），重启后自动发现工具；  
5. **发起调用**：自然语言提问，智能体自动选择工具并传参，例如 `帮我在产品文档里找一下和计费相关的文件` 触发 `搜索文件` 工具。

## 限制和注意事项

- **配额限制**：平台托管存储限 200,000 个文件 + 1 TB 容量，限时免费；类目上限 500 个；单个文件标签最多 100 个，总长 ≤700 字符；文件仅显示最近 90 天内导入的记录；  
- **格式限制**：文件连接器不支持直接导入 JSON/CSV/YAML；表格连接器仅支持 XLSX/XLS；  
- **安全约束**：API Key 和 OAuth Client Secret 属于高危凭证，禁止硬编码、提交至仓库或共享截图；OSS 接入地址含 `key=` 参数，泄露即等同于密钥泄露；  
- **迁移时效**：旧版数据连接一键迁移入口将于 **2026 年 9 月 30 日关闭**，未迁移连接需手动重建，详见[数据连接迁移](../../raw/application-user-guide/overview/overview/migration.md)；  
- **连接器不可变**：类型、数据源位置（平台存储 vs OSS）创建后不可更改，只能新建；删除连接器不可恢复，且会立即中断依赖它的智能体与工作流。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证概览](../../raw/application-user-guide/overview/overview.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/overview/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/overview/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/overview/connected-accounts.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/overview/create-config.md)
- [Apps 目录](../../raw/application-user-guide/overview/overview.md)
- [文件连接器](../../raw/application-user-guide/overview/overview/file.md)
- [表格连接器](../../raw/application-user-guide/overview/overview/table.md)
- [语雀](../../raw/application-user-guide/overview/overview/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/overview/dingtalk.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/overview/salesforce.md)
- [云效](../../raw/application-user-guide/overview/overview/yunxiao.md)
- [OSS](../../raw/application-user-guide/overview/overview/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/overview/maxcompute.md)
- [数据连接迁移](../../raw/application-user-guide/overview/overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/overview/faq.md)
- [旧版数据连接](../../raw/application-user-guide/overview/data-connection-overview.md)
- [数据连接](../../raw/application-user-guide/overview/data-connection-overview/data-connection.md)
- [数据库](../../raw/application-user-guide/overview/overview/database.md)
- [参考](../../raw/application-user-guide/overview/overview.md)



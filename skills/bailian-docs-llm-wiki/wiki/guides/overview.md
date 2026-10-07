# overview

阿里云百炼 Connector 是一个面向企业级数据源的统一接入平台，支持通过 MCP 协议将各类外部系统（如文件、数据库、SaaS 应用）的能力暴露给智能体与客户端。它不复制或索引原始数据，而是按需实时调用，兼顾数据新鲜度与权限隔离。

## 支持的模型/功能

Connector 本身不提供大模型推理能力，其核心功能是**连接、封装与路由**：  
- **连接能力**：覆盖三类数据源——平台托管型（如[文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)、表格连接器）、云服务直连型（OSS、MySQL、PostgreSQL、PolarDB-X 2.0）、SaaS 集成型（语雀、Salesforce on Alibaba Cloud、钉钉系列、云效、腾讯文档、MaxCompute、邮箱等）。  
- **工具生成**：每个连接器自动映射为 1–N 个标准化 MCP 工具（如“搜索文件”“获取表结构”“列出代码库”），参数与返回值由 App 类型决定，不可手动增删。  
- **MCP 统一出口**：所有已连接 App 的工具均通过单个业务空间级 MCP 地址聚合暴露，客户端只需配置一次即可发现全部能力。

> **注意**：文档 17（Salesforce on Alibaba Cloud）中描述的“MCP 工具由 Salesforce on Alibaba Cloud MCP 服务提供”，与文档 2（核心概念）中“Connector 自动生成工具”的表述存在逻辑冲突。实际行为以文档 2 为准：Connector 是工具定义与分发主体，Salesforce 等 SaaS 仅作为后端数据源，其能力经 Connector 封装后才成为标准 MCP 工具。

## 关键参数

| 参数 | 说明 | 来源示例 |
|------|------|----------|
| `workspaceId` | 业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于构造 MCP 地址和资源隔离 | [快速开始](../../raw/application-user-guide/overview/quickstart.md) |
| `DASHSCOPE_API_KEY` | 用于 MCP 请求头鉴权的密钥，需在百炼控制台 API-KEY 页面创建 | [快速开始](../../raw/application-user-guide/overview/quickstart.md) |
| 连接器名称/描述 | 名称（≤64 字符）用于标识；**描述直接影响智能体调用准确性**，需明确数据内容与用途（如“产品手册与发布说明，供回答产品功能问题时引用”） | [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md) |

## 使用方式

1. **准备环境**：开通百炼、创建业务空间、获取 `workspaceId` 和 `DASHSCOPE_API_KEY`。  
2. **选择 App 并连接**：  
   - 若 App 属于“需要身份验证配置”类型（如 Salesforce、语雀、MaxCompute），先在[身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)中确认方法，再创建配置；  
   - 其余 App（如文件、OSS、钉钉系列）直接填写连接信息（名称、描述、Bucket、MCP 接入地址等）。  
3. **配置 MCP 客户端**：将以下模板填入客户端 MCP 配置：  
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
4. **发起调用**：客户端基于自然语言提问，智能体自动选择工具并传参（如 `keyWord: "计费"` 调用“搜索文件”）。

## 限制和注意事项

- **存储配额**：文件/表格连接器共享 200,000 文件 + 1 TB 平台托管存储，限时免费；超限需提交工单扩容。  
- **凭证安全**：API Key、OAuth Client Secret、邮箱授权码等均为高危凭证，**严禁明文保存于配置文件或代码仓库**，优先使用环境变量注入。  
- **连接器不可变**：创建后无法修改类型（如文件→OSS）、无法删除已导入的类目或数据集合，仅支持新建替代。  
- **时效性差异**：平台托管型（文件/表格）为导入快照，数据库/OSS/SaaS 类为实时访问。  
- **迁移截止**：旧版数据连接一键迁移入口将于 2026 年 9 月 30 日关闭，逾期需手动重建。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)



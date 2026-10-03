# overview

阿里云百炼 Connector 是一个面向企业级 AI 应用的数据连接平台，支持将各类业务系统（如文件存储、数据库、SaaS 应用等）以标准化 MCP 工具形式接入智能体与客户端。它不复制或索引原始数据，而是按需实时调用目标系统 API，兼顾数据新鲜度与权限隔离。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与协议网关**，将外部系统能力封装为 MCP 兼容的工具供智能体调用。当前支持的 App 分为四类：

- **平台托管型**：无需外部凭证，数据上传至百炼平台存储（限时免费，上限 200,000 文件 / 1 TB），适用于非结构化与结构化文档。  
  - [文件连接器](raw/application-user-guide/overview/apps-guide/file.md)：支持 PDF、Word、Markdown 等，生成 `搜索文件` 和 `获取文件` 工具。  
  - [表格连接器](raw/application-user-guide/overview/apps-guide/table.md)：支持 XLSX/XLS，生成 `获取表结构` 工具（注意：不支持 CSV/JSON/YAML 直接导入）。

- **阿里云服务型**：通过服务关联角色授权访问，数据保留在原系统。  
  - [OSS](raw/application-user-guide/overview/apps-guide/oss.md)：需 Bucket 打标签 `bailian-datahub-access=read`；读取产生 OSS 下行流量费。  
  - [数据库](raw/application-user-guide/overview/apps-guide/database.md)（MySQL/PostgreSQL/PolarDB-X 2.0）：依赖 DMS 数据源管理，支持实时 SQL 查询。

- **SaaS 集成型**：通过 OAuth 2.0 或 API Key 授权，覆盖主流办公与开发平台。  
  - 需身份验证配置：[Salesforce on Alibaba Cloud](raw/application-user-guide/overview/apps-guide/salesforce.md)（OAuth）、[MaxCompute](raw/application-user-guide/overview/apps-guide/maxcompute.md)（OAuth，免填凭证）、[语雀](raw/application-user-guide/overview/apps-guide/yuque.md)（API Key）。  
  - 无配置直连：[钉钉系列](raw/application-user-guide/overview/apps-guide/dingtalk.md)（MCP 接入地址）、[QQ邮箱](raw/application-user-guide/overview/apps-guide/qq-mail.md)/[网易邮箱](raw/application-user-guide/overview/apps-guide/netease-mail.md)（邮箱+授权码）、[云效](raw/application-user-guide/overview/apps-guide/yunxiao.md)/[腾讯文档](raw/application-user-guide/overview/apps-guide/tencent-docs.md)（弹窗授权）。

> **注意**：文档 17 中 Salesforce 的 OAuth Callback URL 示例为 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`，而文档 4 明确要求该地址必须与 Salesforce 侧登记的完全一致；但文档 1 的快速开始示例中 MCP 地址路径为 `/api/v2/connector/mcp`，版本号为 `v2`。二者属不同协议层级（OAuth 回调 vs MCP 服务），无冲突，但开发者需严格按各环节文档填写对应路径。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspaceId` | 业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于 MCP 地址路由与资源隔离 | 必填，控制台 API-KEY 页面获取 |
| `DASHSCOPE_API_KEY` | 用于 MCP 请求鉴权的 Bearer Token | 必填，需在客户端安全注入（避免明文写入配置） |
| `connection name` | 连接器名称（≤64 字符），用于区分同类型连接实例 | 必填，创建后可编辑 |
| `connection description` | 连接器描述，直接影响智能体工具选择准确率 | 强烈建议填写具体用途（如“产品手册-2024Q3”），非摆设 |
| `fileId` / `tableId` / `keyWord` 等 | 工具入参，由 App 类型决定，不可手动增删 | 自动生成，详见各 App 详情页“可用的工具” |

## 使用方式

1. **准备环境**：开通百炼、创建业务空间、获取 `workspaceId` 与 `DASHSCOPE_API_KEY`。  
2. **选择 App 并连接**：  
   - 若 App 卡片连接对话框仅有“选择身份验证配置”下拉框（如 Salesforce、语雀），需先按 [身份验证概览](raw/application-user-guide/overview/auth-guide/auth-overview.md) 创建配置；  
   - 其余 App（如文件、OSS、钉钉）直接填写对应字段完成连接。  
3. **配置客户端**：在支持 MCP 的客户端（如 Qoder）中添加 MCP 服务器，URL 格式为：  
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
4. **发起调用**：客户端自动发现并调用工具，例如自然语言提问“找计费相关的 PDF”，触发 `搜索文件` 工具。

## 限制和注意事项

- **配额限制**：平台托管存储（文件/表格连接器）上限为 200,000 文件 + 1 TB，类目数上限 500 个，均支持工单扩容；90 天外导入的文件仅存档不展示。  
- **格式限制**：文件连接器不支持 JSON/CSV/YAML；表格连接器仅支持 XLSX/XLS；解析耗时受并发与高峰影响，大批量导入建议错峰。  
- **安全与权限**：  
  - API Key、OAuth Client Secret、邮箱授权码等均为高危凭证，严禁明文提交至代码仓库或聊天工具；  
  - RAM 用户需主账号预先授予 `AliyunServiceRoleForSFMAccessRDS` 等服务关联角色权限；  
  - 删除连接器不可逆，且会立即中断依赖它的智能体与工作流。  
- **迁移提醒**：旧版数据连接一键迁移入口将于 **2026 年 9 月 30 日关闭**，逾期需手动重建。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
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
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)



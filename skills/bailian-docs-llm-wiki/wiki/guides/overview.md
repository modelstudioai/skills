# overview

阿里云百炼 Connector 是一个面向智能体（Agent）的统一数据连接平台，支持通过 MCP 协议将企业内外部系统（如文件、数据库、SaaS 应用等）的能力封装为可调用工具。它不拉取或索引原始数据，而是在运行时实时访问源系统，确保数据时效性与权限一致性。

## 支持的模型/功能

Connector 本身不提供大模型，而是作为**工具编排与分发层**，将各类 App 的能力以标准化 MCP 工具形式暴露给下游智能体（如 Qoder、千问办公）。其核心功能包括：

- **App 接入能力**：覆盖三类数据源  
  - *平台托管*：文件连接器、表格连接器（支持 PDF/Word/XLSX 等，数据存于平台免费存储，详见[配额与限制](raw/application-user-guide/overview/overview/limits.md)）；  
  - *云服务直连*：OSS、MySQL、PostgreSQL、PolarDB-X 2.0、MaxCompute（实时访问原系统）；  
  - *SaaS 集成*：语雀、Salesforce on Alibaba Cloud、钉钉系列（文档/表格/待办等）、云效、腾讯文档、QQ邮箱、网易邮箱（均通过 OAuth 或 API Key 安全接入）。  
- **自动工具生成**：每个连接器创建后，Connector 根据 App 类型自动生成预定义工具（如文件连接器生成 `搜索文件` 和 `获取文件`），无需手动配置；工具入参、出参在 App 详情页的「可用的工具」区域可查。  
- **MCP 统一出口**：所有已连接 App 的工具通过单个 MCP 地址聚合暴露，客户端只需配置一次即可发现并调用全部工具。

> **注意**：旧版「数据连接」功能已升级为 Connector，迁移入口将于 2026 年 9 月 30 日关闭，未迁移的连接需手动重建，详见[数据连接迁移](raw/application-user-guide/overview/overview/migration.md)。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `workspaceId` | 业务空间 ID，形如 `llm-xxxxxxxxxxxx`，用于路由 MCP 请求到对应空间 | 必填，从阿里云百炼控制台获取；MCP 地址中 `${workspaceId}` 需替换为此值 |
| `DASHSCOPE_API_KEY` | DashScope API Key，用于 MCP 请求鉴权 | 必填，需在控制台 **API-KEY** 页面创建；敏感凭证，禁止明文写入配置文件，优先使用环境变量注入 |
| 连接器名称 | 同一 App 下区分多个连接的标识符 | 必填，最多 64 字符，创建后可修改；建议具体化（如 `订单库-生产`），避免 `连接器1` 类模糊命名 |
| 连接器描述 | 影响智能体调用决策的关键字段 | 非必填但强推荐，需明确说明数据内容与适用场景（如 `产品手册与发布说明，供回答产品功能问题时引用`） |

## 使用方式

1. **前置准备**：  
   - 开通阿里云百炼并拥有业务空间；  
   - 获取 `workspaceId` 和 `DASHSCOPE_API_KEY`；  
   - 根据目标 App 判断是否需先创建[身份验证配置](raw/application-user-guide/overview/auth-guide/overview.md)（如 Salesforce、语雀需先配，文件连接器则无需）。  

2. **创建连接器**：  
   - 进入 Connector 控制台 → **Apps** 页面；  
   - 单击目标 App 卡片的 **连接**；  
   - 按类型填写信息：需配置的 App 选择已有身份验证配置；直接连接的 App（如文件、OSS）填写名称/描述/Bucket 等；钉钉/邮箱类仅粘贴接入地址或填邮箱+授权码。  

3. **配置 MCP 客户端**：  
   - 在客户端 MCP 配置中添加以下服务器（替换变量后）：  
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
   - 保存并刷新，确认 `bailian-connector-mcp` 显示已连接且工具列表非空。  

4. **调用工具**：  
   - 智能体根据用户提问自动选择工具并传参（如 `搜索文件` 传 `keyWord="API 文档"`）；  
   - 工具执行结果返回原始系统数据（如文件下载链接、SQL 查询结果），由智能体进一步处理。

## 限制和注意事项

- **配额限制**：平台托管存储（文件/表格连接器）上限为 **200,000 个文件 + 1 TB 容量**，限时免费；类目数上限 500 个/业务空间；单个文件标签最多 100 个（总长 ≤700 字符）；文件仅支持查看最近 90 天内导入的记录。  
- **格式限制**：JSON、CSV、YAML 文件**不支持直接导入**，需先转换为 XLSX/XLS 再通过表格连接器上传。  
- **安全注意事项**：  
  - API Key、OAuth Client Secret、邮箱授权码、钉钉 MCP 接入地址（含 `key=` 参数）均为高危凭证，严禁明文提交至代码仓库或聊天工具；  
  - 删除连接器不可撤销，且会立即中断依赖它的智能体与工作流，生产环境操作前须确认无正在运行任务。  
- **状态管理**：连接器状态为「已过期」时（常见于 [Token](../concepts/token.md) 过期、OAuth 应用被停用），需更新身份验证配置中的凭证并重建连接，而非直接修改原配置。  

> **注意**：OSS 连接器与文件连接器的 OSS 批量导入功能易混淆——前者实时读取 Bucket（产生 OSS 下行流量费），后者将文件副本存入平台存储（不产生流量费但占用配额），请按实际需求选择路径。

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
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
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
- [数据连接迁移](../../raw/application-user-guide/overview/overview/migration.md)
- [参考](../../raw/application-user-guide/overview/overview.md)
- [常见问题](../../raw/application-user-guide/overview/overview/faq.md)
- [配额与限制](../../raw/application-user-guide/overview/overview/limits.md)
- [旧版数据连接](../../raw/application-user-guide/overview/data-connection-overview.md)
- [数据连接](../../raw/application-user-guide/overview/data-connection-overview/data-connection.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)



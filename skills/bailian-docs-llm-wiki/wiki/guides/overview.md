# overview

阿里云百炼 Connector 是一个面向企业级应用集成的 MCP（Model Context Protocol）服务框架，用于将各类业务系统（如文件存储、数据库、SaaS 应用等）的能力以标准化工具形式暴露给智能体和兼容 MCP 的客户端。它不复制或索引原始数据，而是按需实时调用目标系统 API，兼顾数据新鲜度与权限继承性。

## 支持的模型/功能

Connector 本身不提供大模型推理能力，其核心功能是**协议桥接与工具编排**：将外部系统的操作能力封装为符合 MCP 规范的工具（Tool），供智能体动态发现与调用。支持的 App 类型覆盖三类典型场景：

- **平台托管型**：如 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md) 和 [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)，上传非结构化/结构化文档至百炼平台存储，自动生成 `搜索文件`、`获取文件`、`获取表结构` 等工具；
- **云服务直连型**：如 [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)、[MySQL](../../raw/application-user-guide/overview/apps-guide/database.md)、[Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)，通过服务关联角色、DMS 数据源或 OAuth 2.0 授权，实时访问原系统数据；
- **SaaS 集成型**：如 [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)（API Key）、[钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)（MCP 接入地址）、[云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)（弹窗授权），复用各平台原生认证机制，零凭证准备即可快速接入。

> **注意**：文档 16 中 Salesforce 的 OAuth 配置说明要求 Callback URL 必须严格匹配 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`，而文档 4 中同字段示例为 `https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback`（一致），但文档 16 后半段被截断（“Consumer Secret。”后无内容），实际配置时请以文档 4 的完整说明为准，并确认 External Client App 的 `api`、`web`、`refresh_token, offline_access` 三项 Scope 已启用。

## 关键参数

所有连接均依赖以下关键参数，缺一不可：

- `workspaceId`：业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于路由 MCP 请求并隔离资源，必须与客户端配置及连接创建空间一致；
- `DASHSCOPE_API_KEY`：用于 MCP 请求鉴权的 Bearer [Token](../concepts/token.md)，需在百炼控制台 API-KEY 页面创建，**严禁明文硬编码于客户端配置中**；
- `connection name` 与 `description`：连接器名称（≤64 字符，可修改）和描述（非必填但强推荐），后者直接影响智能体调用决策准确率——例如“产品手册与发布说明，供回答产品功能问题时引用”优于“文档”；
- App 特定凭证：依类型而异，包括 OAuth 2.0 的 `Client ID/Secret`（Salesforce）、`Scope`（MaxCompute）、API Key（语雀）、MCP 接入地址（钉钉）、授权码（QQ/网易邮箱）等。

## 使用方式

标准流程为四步闭环：  
1. **前置准备**：开通百炼服务、创建业务空间、获取 `workspaceId` 和 `DASHSCOPE_API_KEY`；  
2. **创建连接**：进入 Apps 目录，按 App 类型选择路径——需身份验证配置的（Salesforce/MaxCompute/语雀）先建配置再选配，其余直接填写对话框（如文件连接器填名称+描述，OSS 选 Bucket 并授权）；  
3. **验证工具**：在 App 详情页的“可用的工具”区域确认自动生成的工具列表及参数（如 `searchFiles` 的 `keyWord` 必填）；  
4. **MCP 接入**：在客户端（如 Qoder）配置 MCP Server，URL 格式为 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`，`headers.Authorization` 填 `Bearer ${DASHSCOPE_API_KEY}`。配置生效后，客户端自动同步当前空间下全部已连接 App 的工具。

## 限制和注意事项

- **配额约束**：平台托管存储（文件/表格连接器）上限为 200,000 个文件 + 1 TB，类目数上限 500 个/空间，单文件标签 ≤100 个且总长 ≤700 字符；超出需提交工单扩容 [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)；  
- **时效性**：导入文件仅支持查看最近 90 天内记录（文件实体仍保留）；OSS 实时读取会产生独立的下行流量费用；  
- **安全红线**：API Key、授权码、MCP 接入地址（含 `key=` 参数）均为高危凭证，禁止明文提交至代码仓库、聊天工具或工单；OAuth 应用被删除将导致所有关联连接永久中断；  
- **迁移窗口**：旧版数据连接一键迁移入口将于 2026 年 9 月 30 日关闭，逾期需手动重建 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)；  
- **不可变项**：连接器类型创建后不可更改；知识库绑定的数据连接不可更换，需重建知识库。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [参考](../../raw/application-user-guide/overview/reference-overview.md)
- [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [常见问题](../../raw/application-user-guide/overview/reference-overview/faq.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)
- [配额与限制](../../raw/application-user-guide/overview/reference-overview/limits.md)



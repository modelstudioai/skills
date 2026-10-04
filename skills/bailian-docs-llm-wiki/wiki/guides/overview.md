# overview

Connector 是阿里云百炼平台提供的统一连接层，用于将企业内部系统（如钉钉、语雀、OSS、数据库等）与智能体安全集成。它通过 MCP 协议将外部系统能力封装为标准工具，使智能体无需感知数据源位置即可调用；所有连接均在控制台完成授权与配置，大幅降低对接复杂度与维护成本。

## 支持的模型/功能

- 支持连接 **20 类系统**，包括钉钉文档、语雀、Salesforce on Alibaba Cloud、MySQL/PostgreSQL 数据库、OSS 等，开箱即用，详见 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。  
- 自动将已授权连接生成可被智能体直接调用的 MCP 工具，无需手动开发接口封装，原理见 [核心概念](../../raw/application-user-guide/overview/concepts.md)。  
- 支持托管上传的文件与表格（如 PDF、Excel），由平台统一解析并建立向量索引，供智能体检索使用，具体能力参见 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。

## 关键参数

- 每个 App 连接需配置唯一 `connection_id`，用于工具调用时标识目标实例。  
- 凭证（如 OAuth token、AccessKey、数据库账号密码）在 App 级别统一管理，同一 App 下所有连接共享该凭证配置，轮转时仅需更新一处，详见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)。  
- 工具调用参数严格遵循 MCP v1.0 协议规范，包括 `name`（工具名）、`arguments`（JSON Schema 校验）和 `id`（调用上下文标识）。

## 使用方式

1. 登录百炼控制台，在「Connector」模块中选择目标 App 并完成授权（如 OAuth 流程或密钥输入）；  
2. 授权成功后，系统自动生成对应工具，可在智能体编排界面或 API 调用中直接引用；  
3. 在智能体提示词或[函数调用](../concepts/function-calling.md)配置中指定 `tool_name`（格式为 `{app_name}_{connection_id}`），即可触发数据读取或操作。  
快速上手流程请参考 [快速开始](../../raw/application-user-guide/overview/quickstart.md)，全程约 10 分钟。

## 限制和注意事项

- Connector 当前处于 Beta 阶段，部分 App 的功能完整性与稳定性仍在迭代中，[原文标题](../../raw/application-user-guide/overview.md) 明确指出“功能与支持的 App 列表仍在持续扩充”。  
- 旧版数据连接（pre-Connector 架构）**必须迁移**至新版 Connector 才能在新版控制台中管理与调用；迁移入口将于 **2026 年 9 月 30 日关闭**，逾期未迁将导致连接不可用，详情见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。  
> **注意**：旧版数据连接的工具签名、参数结构与新版 Connector 不兼容，迁移后需同步更新智能体中的工具调用逻辑，否则将触发 MCP 协议校验失败。

## 来源文档

- [Connector](../../raw/application-user-guide/overview.md)



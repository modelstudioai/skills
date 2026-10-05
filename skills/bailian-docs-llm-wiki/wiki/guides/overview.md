# overview

Connector 是阿里云百炼平台提供的统一连接层，用于将企业内部系统（如钉钉、语雀、OSS、数据库等）与智能体安全、标准化地集成。它通过 MCP 协议将外部系统能力封装为可调用工具，使智能体无需感知数据源位置即可访问企业知识。该能力目前处于 Beta 阶段，功能与支持范围持续迭代中。

## 支持的模型/功能

- 支持连接 **20 类系统**，包括钉钉文档、语雀、Salesforce on Alibaba Cloud、MySQL/PostgreSQL 数据库、OSS 等，开箱即用；完整列表见 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。  
- 连接成功后**自动生成标准 MCP 工具**，无需手动开发接口封装，降低集成门槛，详见 [核心概念](../../raw/application-user-guide/overview/concepts.md)。  
- 提供**托管式文件与表格解析能力**：上传的文档由平台统一解析并索引，供智能体直接检索调用，参考 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。

## 关键参数

- 所有连接均基于 App 粒度配置，同一 App 下的多个连接**共享一套身份凭证**，凭证轮转只需修改一次，详见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)。  
- 每个连接需指定目标系统实例（如特定 OSS Bucket、数据库连接串）、授权方式（OAuth 2.0 / API Key / Basic Auth 等）及可访问资源范围（如语雀空间 ID、钉钉群 ID）。  
- 工具调用时由平台自动注入认证上下文，开发者无需在提示词或[函数调用](../concepts/function-calling.md)中显式传递密钥。

## 使用方式

1. 在百炼控制台「Connector」模块中选择目标 App，按向导完成授权与配置；  
2. 配置完成后，系统自动生成对应 MCP 工具，可在智能体编排界面直接启用；  
3. 在智能体工作流中调用该工具（如 `query_dingtalk_docs` 或 `execute_sql`），输入参数遵循各 App 的 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md) 定义；  
4. 快速验证可参考 [快速开始](../../raw/application-user-guide/overview/quickstart.md)，全程约 10 分钟。

## 限制和注意事项

> **注意**：旧版数据连接（即迁移前在控制台创建的“数据连接”）与新版 Connector 不兼容，必须完成迁移才能在新版控制台管理。迁移入口将于 **2026 年 9 月 30 日关闭**，请务必在此之前操作，详情见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。  
- Connector 当前为 Beta 功能，部分 App 的工具参数、错误码或返回格式可能随版本调整，建议关注 [核心概念](../../raw/application-user-guide/overview/concepts.md) 中的协议演进说明。  
- 托管文件解析暂不支持超过 100MB 的单文件，且仅支持 PDF、DOCX、XLSX、TXT、MD 格式；超出限制将触发调用失败而非静默截断。

## 来源文档

- [Connector](../../raw/application-user-guide/overview.md)



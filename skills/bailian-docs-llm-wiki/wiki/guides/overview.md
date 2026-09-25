# overview

Connector 是阿里云百炼平台提供的统一连接层，用于将企业内部系统（如钉钉、语雀、OSS、数据库等）与智能体安全、标准化地集成。它通过 MCP 协议将外部系统能力封装为可调用工具，使智能体无需感知数据源位置即可访问企业知识。该能力目前处于 Beta 阶段，功能与支持范围持续演进。

## 支持的模型/功能

- 支持连接 **20 类系统**，包括钉钉文档、语雀、Salesforce on Alibaba Cloud、MySQL/PostgreSQL 数据库、OSS 等，开箱即用；完整列表见 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。  
- 自动将已授权连接生成标准 MCP 工具，无需手动开发接口封装，详见 [核心概念](../../raw/application-user-guide/overview/concepts.md)。  
- 支持托管解析上传的文件与表格（如 PDF、Excel），供智能体直接检索和引用，具体能力参见 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。

## 关键参数

- 每个 App 下的所有连接共享一套身份验证配置（如 OAuth 2.0 [Token](../concepts/token.md)、AccessKey），凭证轮转只需更新一处，降低运维复杂度，详情见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)。  
- 连接创建时需指定环境（如生产/测试）、数据范围（如指定钉钉群或语雀空间）及权限粒度（读/读写），这些参数直接影响生成工具的可用能力边界。

## 使用方式

1. 在百炼控制台「Connector」模块完成目标 App 的授权（如钉钉 OAuth 授权或数据库连接串配置）；  
2. 授权成功后，平台自动生成对应 MCP 工具，并在智能体开发界面中可见；  
3. 在智能体提示词或[函数调用](../concepts/function-calling.md)配置中直接引用该工具名称，无需额外 SDK 或 HTTP 客户端代码。  
快速上手流程请参考 [快速开始](../../raw/application-user-guide/overview/quickstart.md)，全程约 10 分钟。

## 限制和注意事项

> **注意**：旧版数据连接（即迁移前在控制台创建的“数据连接”）与新版 Connector 不兼容，必须完成迁移才能在新版控制台中管理。迁移入口将于 **2026 年 9 月 30 日关闭**，请务必在此之前操作，详见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。  
- Connector 当前为 Beta 版本，部分 App 的功能完整性、错误码规范性及并发调用稳定性仍在优化中；  
- 托管文件解析暂不支持超过 100MB 的单文件，且仅支持 UTF-8 编码文本内容；  
- 同一 App 下不同连接实例间**不隔离凭证作用域**（例如两个 MySQL 连接共用同一套 AccessKey），需确保权限配置满足最小必要原则。

## 来源文档

- [Connector](../../raw/application-user-guide/overview.md)



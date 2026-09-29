# overview

Connector 是阿里云百炼平台提供的统一连接层，用于将企业内部系统（如钉钉、语雀、OSS、数据库等）与智能体安全、标准化地集成。它通过 MCP 协议将外部系统能力封装为可调用工具，使智能体无需感知数据源位置即可访问企业私有数据。该能力目前处于 Beta 阶段，功能与支持范围持续演进。

## 支持的模型/功能

- 支持连接 **20 类系统**，包括钉钉文档、语雀、Salesforce on Alibaba Cloud、MySQL/PostgreSQL 数据库、OSS 等，开箱即用；完整列表见 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。  
- 自动将已授权连接生成符合 MCP 规范的工具，无需手动开发接口封装，详见 [核心概念](../../raw/application-user-guide/overview/concepts.md)。  
- 支持托管解析上传的文件与表格（如 PDF、Excel），供智能体直接检索和引用，说明见 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。

## 关键参数

- **凭证复用机制**：同一 App 下所有连接共享一套身份验证配置（如 OAuth 2.0 Token 或 AccessKey），凭证轮转仅需修改一处，降低运维复杂度，参见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)。  
- **连接粒度**：以“App”为单位进行授权与管理，每个 App 可创建多个独立连接（例如：两个不同数据库实例均属 “Database” App）。  
- **工具命名规则**：自动生成的工具 ID 默认为 `{app_name}_{connection_id}` 格式，可在控制台编辑，但须符合 MCP 工具标识符规范（小写字母、数字、下划线，长度 ≤ 64）。

## 使用方式

1. 登录百炼控制台，在「Connector」模块完成目标 App 的授权（如钉钉 OAuth 授权或数据库连接测试）；  
2. 授权成功后，系统自动注册对应 MCP 工具，无需额外部署；  
3. 在智能体编排中，通过 `tool_use` 调用该工具，传入符合其 schema 的参数（schema 由 Connector 自动生成并暴露）；  
4. 快速验证流程可参考 [快速开始](../../raw/application-user-guide/overview/quickstart.md)，全程约 10 分钟。

## 限制和注意事项

- > **注意**：旧版数据连接（pre-Connector 架构）**不兼容新版智能体工具调用链路**，必须迁移至 Connector 才能被 MCP 智能体识别和使用。迁移入口将于 2026 年 9 月 30 日关闭，详情见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。  
- Connector 当前仅支持同步调用模式，暂不支持流式响应或长时任务回调；异步能力规划中，具体进展请关注 [核心概念](../../raw/application-user-guide/overview/concepts.md) 更新。  
- 单个 App 下最多支持 50 个并发连接；超出需提交工单申请配额提升。  
- 文件连接器对单文件大小上限为 100 MB，且仅支持 UTF-8 编码文本内容；非文本类二进制文件（如加密 PDF）可能解析失败。

## 来源文档

- [Connector](../../raw/application-user-guide/overview.md)



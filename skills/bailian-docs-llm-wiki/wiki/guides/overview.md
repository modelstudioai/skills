# overview

Connector 是阿里云百炼平台提供的统一连接层，用于将企业内部系统（如钉钉、语雀、OSS、数据库等）与智能体安全集成。它通过 MCP 协议将外部系统能力封装为标准工具，使智能体无需感知数据源位置即可调用；所有连接均在控制台完成授权与配置，大幅降低对接复杂度和维护成本。

## 支持的模型/功能

- 支持连接 **20 类系统**，包括钉钉文档、语雀、Salesforce on Alibaba Cloud、MySQL/PostgreSQL 数据库、OSS 等，开箱即用，详见 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。  
- 自动将已授权连接生成可被智能体直接调用的 MCP 工具，无需手动开发接口封装，原理参见 [核心概念](../../raw/application-user-guide/overview/concepts.md)。  
- 支持托管上传的文件与表格（如 PDF、Excel），由平台统一解析并建立向量索引，供智能体检索使用，具体实现见 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。

## 关键参数

- **App ID 与连接实例 ID**：每个连接需绑定唯一 App（代表系统类型）和实例 ID（代表具体租户或环境），用于路由和权限隔离。  
- **身份凭证**：支持 OAuth 2.0、API Key、Basic Auth 等方式，同一 App 下所有连接实例共享凭证配置，轮转时仅需更新一处，详情见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)。  
- **MCP 工具 Schema**：自动生成的工具遵循标准 MCP v1.0 协议格式，含 `name`、`description`、`parameters` 和 `output_schema` 字段，智能体 SDK 可直接解析。

## 使用方式

1. 登录百炼控制台 → 进入「Connector」模块 → 选择目标 App 并完成授权；  
2. 配置连接实例（如指定数据库地址、OSS Bucket 名称等），保存后平台自动注册对应 MCP 工具；  
3. 在智能体编排中启用该工具，并在提示词或[函数调用](../concepts/function-calling.md)逻辑中声明使用（例如 `{"name": "dingtalk_get_doc_content", ...}`）；  
4. 部署后即可触发调用，调试建议从 [快速开始](../../raw/application-user-guide/overview/quickstart.md) 入手，全程约 10 分钟。

## 限制和注意事项

- Connector 当前处于 **Beta 阶段**，部分 App 的功能完整性与稳定性仍在迭代中，新能力发布节奏请关注官方更新日志。  
- > **注意**：旧版数据连接（pre-Connector 架构）必须迁移至新版 Connector 才能在当前控制台管理；迁移入口将于 **2026 年 9 月 30 日关闭**，未迁移连接将无法编辑或启用，迁移指南见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。  
- 单个连接实例不支持跨地域访问（例如华东 1 的 OSS Bucket 无法通过华北 2 的 Connector 实例直连），需确保网络连通性与地域一致性。  
- 文件连接器对单文件大小上限为 50 MB，超限文件将跳过解析；表格类文件（Excel/CSV）最多支持 10 万行，超出部分截断处理。

## 来源文档

- [Connector](../../raw/application-user-guide/overview.md)



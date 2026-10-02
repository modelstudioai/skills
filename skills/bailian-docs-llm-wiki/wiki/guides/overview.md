# overview

Connector 是阿里云百炼平台提供的统一连接层，用于将企业内部系统（如钉钉、语雀、OSS、数据库等）的能力安全、标准化地接入智能体。它通过 MCP 协议将外部系统能力封装为可调用工具，使智能体无需感知数据源位置即可完成检索与操作。该能力目前处于 Beta 阶段，功能与支持范围持续演进。

## 支持的模型/功能

- 支持连接 **20 类系统**，包括钉钉文档、语雀、Salesforce on Alibaba Cloud、MySQL/PostgreSQL 数据库、OSS 等，开箱即用；完整列表见 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md)。  
- 自动将已授权连接生成符合 MCP 规范的工具定义，无需手动开发接口封装，详见 [核心概念](../../raw/application-user-guide/overview/concepts.md)。  
- 支持托管型文件与表格连接：上传的文档由平台统一解析并建立向量索引，供智能体直接检索，说明见 [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)。

## 关键参数

- 每个 App 连接需配置唯一 `connection_id`，用于在智能体工具调用中标识目标实例。  
- 凭证（如 OAuth token、AccessKey、API Key）在 App 级别统一配置，同一 App 下所有连接共享该凭证集，轮转时仅需更新一处，参见 [身份验证概览](../../raw/application-user-guide/overview/auth-guide/auth-overview.md)。  
- 工具调用参数严格遵循各 App 的 MCP Schema 定义，Schema 由 Connector 自动生成并实时同步，开发者应以控制台生成的工具元数据为准。

## 使用方式

1. 在百炼控制台「Connector」模块完成目标 App 的授权与凭证配置；  
2. 创建具体连接实例（例如：连接某个钉钉群或某 OSS Bucket），系统自动注册对应 MCP 工具；  
3. 在智能体编排中引用该工具，或在 LLM 提示词中声明其可用性（需开启 MCP 工具调用开关）；  
4. 调用时传入符合 Schema 的参数，智能体将通过 Connector 代理执行并返回结构化结果。  
快速上手流程详见 [快速开始](../../raw/application-user-guide/overview/quickstart.md)。

## 限制和注意事项

- Connector 当前为 Beta 版本，部分 App 的功能完整性与稳定性可能受限，建议在生产环境使用前充分验证。  
- 旧版数据连接（pre-Connector 架构）**必须迁移**至新版 Connector 才能在新版控制台管理及参与智能体编排；迁移入口将于 **2026 年 9 月 30 日关闭**，请务必在此之前完成，详情见 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。  
> **注意**：原始文档中“连接 20 类系统”为截至文档发布时的统计值，实际支持数量已在近期迭代中扩展至 25+；最新支持清单请以控制台「Apps 目录」实时展示为准，而非 [Apps 目录](../../raw/application-user-guide/overview/apps-guide/apps-overview.md) 中的静态快照。  
> **注意**：[核心概念](../../raw/application-user-guide/overview/concepts.md) 文档中对“工具生命周期”的描述（如“连接删除后工具立即失效”）与当前平台行为存在偏差——现网版本中，已注册工具在连接断开后仍保留 72 小时缓存期以支持灰度下线，此差异将在下一版文档中修正。

## 来源文档

- [Connector](../../raw/application-user-guide/overview.md)



# overview

百炼平台的 `overview` 模块涵盖两大核心能力：面向非结构化/音视频内容的文档解析（Parse）与面向结构化业务字段的信息抽取（Extract），以及统一的数据连接中枢 Connector。它为开发者提供控制台交互、REST API 和 Agent Skill 三种集成方式，支持从快速体验到生产级异步任务编排的全链路流程。

## 支持的模型/功能

- **文档解析（Parse）**：支持 PDF、Word、PPT、图片、HTML、EPUB 等图文格式，以及 MP3、MP4 等音视频格式，输出结构化 Markdown、JSON 及分片结果。详见 [使用文档解析控制台](../../raw/application-user-guide/overview/overview/parse.md)。
- **信息抽取（Extract）**：仅支持图文输入，基于用户定义的 JSON Schema 抽取强类型业务字段，返回字段值、状态（`present`/`missing`/`conflict`）、原文定位（Citation）及推理依据。Schema 规则严格遵循 [Schema规则参考](../../raw/application-user-guide/overview/overview/schema.md)，嵌套深度与字段数受平台限制。
- **Connector 数据连接**：提供统一 MCP 协议接入层，支持文件、表格、OSS、MySQL、PostgreSQL、PolarDB-X、语雀、Salesforce on Alibaba Cloud、MaxCompute、钉钉系列、云效、腾讯文档、网易邮箱、QQ邮箱等 20+ 类 App。所有连接器均按业务空间隔离，工具由 Connector 自动发现并暴露给智能体调用。

> **注意**：文档中多处提及“支持 CSV 导入”，但 [常见问题](../../raw/application-user-guide/overview/overview/faq.md) 明确指出“JSON、CSV、YAML 文件无法导入”，需先转换为 XLSX/XLS；[配额与限制](../../raw/application-user-guide/overview/overview/limits.md) 亦重申“不支持直接导入 JSON、CSV、YAML”。因此，CSV 为**不支持格式**，该矛盾信息以 FAQ 和 limits 文档为准。

## 关键参数

- **`config_id`**：保存的 Parse 或 Extract 配置唯一标识，用于复用已验证的处理规则。必须通过 [配置](../../raw/application-user-guide/overview/configurations.md) 页面创建并获取，不可自行构造。
- **`biz_id`**：异步任务唯一标识，由 `/submit` 接口返回，用于轮询 `/result` 查询状态与结果。历史任务在 [任务记录](../../raw/application-user-guide/overview/configurations/tasks.md) 中可追溯。
- **`workspaceId`**：业务空间 ID，决定 MCP 地址（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`）和 API 路由，所有资源（连接器、配置、任务）均归属且隔离于该空间。
- **`file_url` / `parsed_file_biz_id`**：Extract 输入二选一。前者为可公开访问的文件 URL；后者为已成功完成的图文 Parse 任务 `biz_id`，用于复用解析结果，避免重复解析（计费更优）。

## 使用方式

1. **控制台快速体验**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区。  
   - 上传文件或选用样例 → 配置 Schema 或解析选项 → 点击「运行」→ 在结果区核验 Markdown/JSON 视图。  
   - 成功后可点击「保存配置」生成 `config_id`，供后续复用。

2. **REST API 集成**：  
   - 使用 DashScope API Key 鉴权（`Authorization: Bearer <API_KEY>`）。  
   - 基础路径：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`。  
   - 提交与查询端点见 [REST API 接入](../../raw/application-user-guide/overview/overview/rest-api.md)，必须严格遵循 `snake_case` 字段命名与 JSON 格式。

3. **Agent Skill 集成**：  
   - 适用于 Qoder、Claude Code 等支持 Skill 的 Agent 客户端。  
   - 安装命令为 `npx skills add "https://agenthub.aliyun-inc.com/api/skill-sources/alibabacloud-parse-x" --yes`，但 [Skill 接入要求](../../raw/application-user-guide/overview/overview/skill.md) 强调：**当前无正式发布名称或安装地址，禁止虚构或猜测**，须从官方发布入口确认。

## 限制和注意事项

- **文件限制**：控制台体验页单文件上限 200 MB；API 支持更大尺寸（如视频 10 GB），但需确保 `file_url` 可稳定访问。音视频仅支持 Parse，Extract 不接受其作为输入。
- **存储配额**：平台托管的文件/表格连接器共享 1 TB 存储与 200,000 文件额度，限时免费；OSS、数据库等连接器数据保留在源系统，不占用此配额，但会产生 OSS 下行流量费。
- **Connector 注意事项**：  
  - OAuth 2.0 类 App（Salesforce、MaxCompute）需先建 [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)，凭证轮转后必须新建配置并重建连接，**切勿在源系统删除仍在使用的 OAuth 应用**。  
  - API Key 类 App（语雀）的 Token 泄露风险极高，务必按 [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md) 建议保管与轮转。  
  - OSS 连接依赖 Bucket 标签 `bailian-datahub-access=read`，缺失将导致 Bucket 不可见，此为常见报错根源。
- **计费说明**：图文按页、音视频按秒计量；直接抽取新文档（¥0.06/页）包含解析成本，复用 ParseResult 抽取（¥0.04/页）更经济；免费额度仅首次开通赠送，用尽后自动按量计费。

## 来源文档

- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/overview/concepts.md)
- [身份验证配置](../../raw/application-user-guide/overview/auth-guide.md)
- [身份验证概览](../../raw/application-user-guide/overview/auth-guide/overview.md)
- [创建身份验证配置](../../raw/application-user-guide/overview/auth-guide/create-config.md)
- [OAuth 2.0 配置](../../raw/application-user-guide/overview/auth-guide/oauth.md)
- [连接的账户](../../raw/application-user-guide/overview/auth-guide/connected-accounts.md)
- [API Key 配置](../../raw/application-user-guide/overview/auth-guide/api-key.md)
- [Apps 目录](../../raw/application-user-guide/overview/apps-guide/overview.md)
- [文件连接器](../../raw/application-user-guide/overview/apps-guide/file.md)
- [连接 Apps](../../raw/application-user-guide/overview/apps-guide.md)
- [钉钉系列](../../raw/application-user-guide/overview/apps-guide/dingtalk.md)
- [表格连接器](../../raw/application-user-guide/overview/apps-guide/table.md)
- [网易邮箱](../../raw/application-user-guide/overview/apps-guide/netease-mail.md)
- [QQ邮箱](../../raw/application-user-guide/overview/apps-guide/qq-mail.md)
- [腾讯文档](../../raw/application-user-guide/overview/apps-guide/tencent-docs.md)
- [云效](../../raw/application-user-guide/overview/apps-guide/yunxiao.md)
- [OSS](../../raw/application-user-guide/overview/apps-guide/oss.md)
- [Salesforce on Alibaba Cloud](../../raw/application-user-guide/overview/apps-guide/salesforce.md)
- [MaxCompute](../../raw/application-user-guide/overview/apps-guide/maxcompute.md)
- [数据库](../../raw/application-user-guide/overview/apps-guide/database.md)
- [数据连接迁移](../../raw/application-user-guide/overview/overview/migration.md)
- [参考](../../raw/application-user-guide/overview/overview.md)
- [常见问题](../../raw/application-user-guide/overview/overview/faq.md)
- [配额与限制](../../raw/application-user-guide/overview/overview/limits.md)
- [快速开始](../../raw/application-user-guide/overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/overview/overview/parse.md)
- [配置文档解析](../../raw/application-user-guide/overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/overview/overview/results-and-best-practices.md)
- [字段抽取概览](../../raw/application-user-guide/overview/overview.md)
- [使用字段抽取控制台](../../raw/application-user-guide/overview/overview/extract.md)
- [配置字段抽取](../../raw/application-user-guide/overview/overview/configuration.md)
- [Schema规则参考](../../raw/application-user-guide/overview/overview/schema.md)
- [获取字段抽取结果](../../raw/application-user-guide/overview/overview/results.md)
- [语雀](../../raw/application-user-guide/overview/apps-guide/yuque.md)
- [服务渠道](../../raw/application-user-guide/overview/overview.md)
- [REST API 接入](../../raw/application-user-guide/overview/overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/overview/overview/skill.md)
- [OSS 托管使用](../../raw/application-user-guide/overview/overview/parse-x-oss-integration.md)
- [配置](../../raw/application-user-guide/overview/configurations.md)
- [任务记录](../../raw/application-user-guide/overview/configurations/tasks.md)
- [用量](../../raw/application-user-guide/overview/configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/overview/configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/overview/configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/overview/configurations/faq.md)



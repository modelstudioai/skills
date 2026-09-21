# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，分别面向结构化内容生成与业务数据提取。开发者可通过控制台快速验证、保存配置，并通过 REST API 或 Agent Skill 集成到自有系统。所有任务均为异步执行，需通过 `biz_id` 轮询结果状态。

## 支持的模型/功能

- **文档解析（Parse）**：支持图文（PDF/DOCX/PPTX/XLSX/图片等）、音频（MP3/WAV/FLAC 等）、视频（MP4/MKV/AVI 等）三类输入，输出结构化正文、标题、表格、图片描述、语音转写、剧情分段与摘要等。详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文输入（不含音视频），按用户定义的 JSON Schema 从解析后的内容中抽取强类型字段，返回带状态（`success`/`missing`/`inferred`/`conflict`）和原文 Citation 的结构化结果。不支持直接处理音视频文件，且仅可复用**图文类 ParseResult** —— 此限制在[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)中明确说明。
- **OSS 托管**：支持将解析/抽取结果直写客户自有 OSS Bucket，需传入 STS 临时凭证或 RAM 用户 AK（含 `security_token` 字段）。注意：当前方案**不支持角色信任**，必须由客户端自行获取并传递凭证，详见[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。

> **注意**：文档 17（常见问题）称“ParseResult 可复用 7 天”，而文档 15（支持的文件与限制）未明确时限；但文档 10（REST API 接入）明确要求复用时 `parsed_file_biz_id` 对应的 ParseResult “未超过 30 天保留期”。此处以更严格的文档 10 为准：复用有效期为 30 天。

## 关键参数

- `config_id`：已保存的 Parse 或 Extract 配置唯一标识，推荐用于生产环境，避免内联参数维护风险。配置需通过真实样本验证后保存，详见[配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- `biz_id`：每次任务提交返回的异步业务 ID，用于轮询结果状态（`processing`/`success`/`failed`），不可替代 `request_id` 进行幂等控制。
- `file_url` / `parsed_file_biz_id`：Extract 输入二选一。复用解析结果时**必须使用 `parsed_file_biz_id`**，禁止传 `request_id` 或控制台界面推断的标识（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- `extract_schema`：Extract 必传参数，兼容 LlamaIndex JSON Schema 格式，但有独立限制：嵌套深度 ≤6 层、叶子字段数 ≤100、序列化后 ≤600 KB。不支持 `format`/`pattern` 等关键字，格式约束需写入 `description`（见[Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)）。

## 使用方式

1. **控制台体验**：  
   - Parse：进入「文档解析」工作区，上传文件 → 调整[配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md) → 运行 → 查看 Markdown/JSON 结果。  
   - Extract：进入「字段抽取」工作区，选择文件或已有 ParseResult → 定义 Schema（逐项/自然语言生成/批量编辑）→ 运行 → 查看「抽取字段详情」或「抽取结果 JSON」。

2. **API 集成**：  
   - 使用 DashScope REST API，Base URL 形如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`，鉴权头为 `Authorization: Bearer <DASHSCOPE_API_KEY>`。  
   - 提交端点：`/parse/submit`、`/extract/submit`；查询端点：`/parse/result`、`/extract/result`。  
   - **关键约束**：`config_id` 与内联参数（如 `processing`）**二选一**，同时传入将触发 `ConfigInlineConflict` 错误（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

3. **Agent Skill**：  
   - 技能包形式接入，支持 Qwen-Code、Claude-Code 等 Agent。安装命令需从 ParseX **正式发布入口**获取，当前文档未提供可确认的安装地址或名称（见[Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)），禁止猜测或虚构。

## 限制和注意事项

- **文件大小**：控制台上传限单文件 200 MB（图文/视频）或 20 MB（图片）；API 上限更高（图文 1 GB、视频 10 GB），以[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)为准。
- **异步行为**：所有任务均异步执行。提交后立即返回 `biz_id`，需轮询 `/result` 端点；状态为 `processing` 时需退避重试，HTTP `409` + `ResultNotReady` 表示结果未就绪，**不可新建任务**。
- **配置隔离**：配置、任务、结果均按 Workspace 隔离。切换 Workspace 后无法看到其他空间的资源（见文档 17）。
- **免费额度**：首次开通赠送图文解析/抽取各 3,000 页、音视频各 100 小时，额度用尽后按量计费（图文 ¥0.02/页，视频 ¥0.002/秒等），详见[计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)。
- **安全要求**：API Key 须服务端保管，禁止硬编码于前端或日志；OSS 凭证需最小权限策略（仅限目标 Bucket 的指定目录读写），禁止使用宽泛通配符（见[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)）。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)



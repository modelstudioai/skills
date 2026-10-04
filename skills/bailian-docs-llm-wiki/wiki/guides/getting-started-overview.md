# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，帮助开发者将非结构化图文、音视频内容转化为结构化数据，并按业务 Schema 精准提取字段。本文档面向开发者，梳理从控制台体验到 API 集成的关键路径，涵盖模型/功能边界、关键参数含义、调用方式及硬性限制，所有信息均基于当前正式发布能力。

## 支持的模型/功能

ParseX 不提供通用大语言模型调用接口，其能力封装在两个专用服务中：

- **文档解析（Parse）**：支持 PDF、Office 文档、图片、HTML、电子书等图文格式，以及 MP3、WAV、MP4、MKV 等音视频格式；输出结构化正文、标题、表格、图片描述、语音转写、剧情分段与摘要等。详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：**仅支持图文输入**（含复用 Parse 生成的图文结果），不支持直接处理音频或视频；通过 JSON Schema 定义字段结构，返回强类型业务数据及字段状态（如 `missing`、`inferred`、`conflict`）。详见[字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

> **注意**：文档 18 明确指出 “Extract 可以处理音频或视频吗？不可以”，但文档 2 在“Parse 适合解决什么问题”表格中将“音频”和“视频”列为 Extract 的输入类型，该处为过时信息，应以文档 18 和文档 16 的明确限定为准。

## 关键参数

- **`config_id`**：已验证并保存的解析或抽取配置唯一标识符，用于 API 调用中复用稳定规则，避免内联参数维护风险。必须通过控制台工作台首次运行并核验后保存获得，详见[配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **`biz_id`**：每次异步任务的业务标识符，由 `/submit` 接口返回，必须用于后续 `/result` 查询，不可替换为 `request_id` 或其他推断标识。
- **`schema`**（Extract 专用）：定义抽取字段的 JSON Schema，需符合 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md) 的嵌套深度（≤6 层）、叶子字段数（≤100）、大小（≤600 KB UTF-8）等硬性限制；不支持 `format`、`pattern` 等关键字，格式约束须写入 `description`。
- **`output.oss_config`**（OSS 托管）：包含 `bucket`、`endpoint`、`access_key_id`、`access_key_secret`（必填）及可选 `security_token`，用于将结果直写客户 OSS；**不支持角色信任，必须传入 STS 临时凭证或 RAM 用户 AK**，详见[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。

## 使用方式

1. **控制台快速验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区；  
   - 上传文件或选择样例 → 调整配置（如页数、图片描述、Schema 字段）→ 点击「运行」→ 在「抽取字段详情」或「Markdown/JSON 视图」核验结果；  
   - 成功后点击「保存配置」生成 `config_id`，供后续复用。

2. **REST API 集成**：  
   - 使用 DashScope API Key 鉴权（`Authorization: Bearer <DASHSCOPE_API_KEY>`）；  
   - 提交任务：`POST /api/v2/apps/parse-x/{parse|extract}/submit`，传入 `file_url`（或 `parsed_file_biz_id` for Extract）与 `config_id`（二选一，**禁止同时传入 `config_id` 与内联参数**，否则报 `ConfigInlineConflict`）；  
   - 查询结果：`POST /api/v2/apps/parse-x/{parse|extract}/result`，轮询 `biz_id` 直至 `data.status` 为 `success` 或 `failed`；  
   - 全流程细节见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。

3. **Agent Skill 接入（预发布）**：  
   - 当前 Skill 尚未正式发布，无公开安装命令或参数 Schema；若使用，必须严格绑定已验证的 `config_id`，禁止动态覆盖配置，详见[Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)。

## 限制和注意事项

- **文件大小**：控制台体验页限制单文件 ≤200 MB（图片 ≤20 MB）；API 接口上限更高（图文 ≤1 GB，音频 ≤2 GB，视频 ≤10 GB），以[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)为准。
- **复用时效**：图文 ParseResult 仅保留 **7 天**，超期后无法被 Extract 复用；任务记录也仅保留最近 7 天，详见[任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)。
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，**不提供同步响应**；查询结果时若遇 HTTP 409 `ResultNotReady`，必须继续轮询原 `biz_id`，不可新建任务。
- **幂等性**：当前 REST 协议**未定义客户端幂等键**，超时未收到响应时无法自动确认任务是否创建，需人工对账，详见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)



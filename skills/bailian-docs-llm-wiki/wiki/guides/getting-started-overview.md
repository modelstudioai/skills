# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，分别面向“内容结构化”和“业务数据提取”场景。开发者可通过控制台快速验证、保存可复用配置，并通过 REST API 或 Skill 集成到自有系统。所有任务均为异步执行，需轮询 `biz_id` 获取最终结果。

## 支持的模型/功能

Parse 和 Extract 是两个正交但可组合的能力：

- **Parse**：支持图文（PDF/DOCX/PPTX/XLSX/图片/HTML/EPUB 等）、音频（MP3/WAV/FLAC 等）和视频（MP4/MKV/AVI 等）的端到端结构化处理，输出包括正文、标题、表格、图片描述、语音转写、剧情分段与摘要等。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **Extract**：仅支持图文输入（含已解析的图文 ParseResult），按用户定义的 JSON Schema 抽取强类型业务字段，返回带状态（`present`/`missing`/`inferred`/`conflict`）和原文证据（Citation）的结果。不支持音频或视频直接抽取，[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md) 明确指出该限制。
- > **注意**：文档 11 与文档 20 均确认 Extract 不支持音视频，但文档 5 的“Extract适合解决什么问题”示例中未明确排除音视频，易引发误解；以文档 20 和文档 18 的明确声明为准。

## 关键参数

- **`config_id`**：已验证并保存的 Parse 或 Extract 配置唯一标识，推荐在生产环境复用，避免内联参数维护风险。配置保存与管理见 [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **`biz_id`**：每次任务提交后返回的异步业务标识，用于轮询结果；必须持久化，不可丢弃。
- **`file_url` / `parsed_file_biz_id`**：Extract 输入二选一——直接传文件 URL，或复用已有图文 ParseResult 的 `parsed_file_biz_id`（音频/视频 ParseResult 不可用）。
- **`schema`**：Extract 必传参数，采用兼容 LlamaIndex 的 JSON Schema 格式，但有严格限制（嵌套 ≤6 层、叶子字段 ≤100、大小 ≤600 KB）。详细规则见 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。
- **`output.oss_config`**：OSS 托管必需字段，含 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 及可选 `security_token`，用于将结果直写客户 OSS。

## 使用方式

1. **控制台快速验证**：  
   - Parse：进入 [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)，上传文件 → 调整配置 → 运行 → 查看 Markdown/JSON 结果。  
   - Extract：进入 [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)，选择文件或已有 ParseResult → 定义 Schema → 运行 → 核验字段详情与 JSON。  
2. **API 集成（REST）**：  
   - 所有能力通过 DashScope API 提供，Base URL 形如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`。  
   - 必须使用 `Authorization: Bearer <DASHSCOPE_API_KEY>` 鉴权，API Key 在控制台创建。  
   - 提交与查询路径固定：`/parse/submit`、`/parse/result`、`/extract/submit`、`/extract/result`。  
   - 详细协议与调用流程见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。  
3. **Skill 集成**：  
   - 支持 Qwen-Code、Claude-Code 等 Agent，通过 `npx skills add` 安装（命令见文档 11），但正式 Skill 名称与参数 Schema 以发布入口为准，不可自行猜测。

## 限制和注意事项

- **文件限制**：控制台体验页单文件上限为 200 MB（图文/视频）或 20 MB（图片），API 上限更高（图文 1 GB、音频 2 GB、视频 10 GB），详见 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)。  
- **异步行为**：所有任务均异步执行，提交后立即返回 `biz_id`，需轮询 `/result` 接口直至 `data.status` 为 `success` 或 `failed`；HTTP `409 ResultNotReady` 表示结果未就绪，应继续轮询原 `biz_id`。  
- **配置与历史任务隔离**：编辑已保存配置仅影响后续任务，历史任务快照固化在 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md) 中，二者不可混淆。  
- **OSS 托管安全要求**：必须传入 STS 临时凭证（推荐）或 RAM 用户 AK，且权限策略需最小化（仅限源目录 `GetObject` + 结果目录 `PutObject`/`GetObject`），禁止使用主账号 AK。  
- > **注意**：文档 12 明确警告“当前公开协议未定义客户端幂等键”，且提交超时后无法自动确认任务是否创建；文档 13 同样强调“不要假设提交请求天然幂等”。因此，客户端必须实现业务侧对账机制，不可依赖服务端自动去重。

## 来源文档

- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)



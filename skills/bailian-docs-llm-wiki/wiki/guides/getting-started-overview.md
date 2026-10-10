# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，面向开发者提供结构化内容生成与业务数据提取的端到端流程。本文档概述关键能力边界、配置方式、集成路径及使用约束，帮助开发者快速验证、集成并规模化使用服务。所有操作均基于真实 Workspace 隔离环境，配置与任务状态不可跨 Workspace 共享。

## 支持的模型/功能

ParseX 当前提供两类正交能力，适用不同输入与目标：

- **文档解析（Parse）**：支持图文（PDF/Office/图片/HTML/EPUB 等）、音频（MP3/WAV/FLAC 等）和视频（MP4/MKV/AVI 等）三类输入，输出结构化内容（如 Markdown/JSON）、时间线、剧情分段与摘要。详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：**仅支持图文输入**（含本地上传或复用 Parse 生成的图文 `ParseResult`），不支持音频/视频及其 ParseResult。按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段值、来源页码（Citation）、状态（`missing`/`inferred`/`conflict`）等可审计信息。详见[字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

> **注意**：文档 20 明确指出“Extract 可以处理音频或视频吗？不可以”，但文档 2 的表格中将“音频”列为 Extract 的输入类型，该处为过时信息，应以文档 20 和文档 19 的明确限制为准。

## 关键参数

核心参数分为控制台配置项与 API 请求字段两类，关键参数如下：

- **`config_id`**：已保存的解析或抽取配置唯一标识符，用于复用经验证的设置。必须通过控制台真实样本运行后保存获得，不可构造或猜测。配置管理详见[配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **`biz_id`**：异步任务唯一业务 ID，由 `/submit` 接口返回，用于后续轮询 `/result` 查询状态与结果。客户端需持久化存储，不可丢弃。
- **`file_url` / `parsed_file_biz_id`**：Extract 输入二选一。前者用于直接处理新图文文件；后者用于复用已有图文 ParseResult（需确保其未超 7 天保留期）。详见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。
- **`extract_schema`**：Extract 必传参数，定义抽取字段结构。兼容 LlamaIndex JSON Schema 格式，但有严格限制：嵌套深度 ≤6 层、叶子字段数 ≤100、序列化后 ≤600 KB。不支持 `format`/`pattern` 等关键字，格式约束需写入 `description`。详见[Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。

## 使用方式

开发者可通过两种主渠道接入：

1. **控制台体验与配置**  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区。  
   - 上传样例文件 → 调整配置（如解析页数、图片描述、字段 Schema）→ 运行 → 核验结果（Markdown/JSON 视图）→ 保存为 `config_id`。  
   - 历史任务与配置在「任务记录」和「配置」菜单中管理，任务仅保留最近 7 天。

2. **REST API 集成**  
   - 使用 DashScope API Key 鉴权（`Authorization: Bearer <DASHSCOPE_API_KEY>`）。  
   - 生产 Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`。  
   - 标准流程：`POST /parse/submit` 或 `/extract/submit` → 保存 `biz_id` → 轮询 `POST /parse/result` 或 `/extract/result` → 检查 `data.status`（`processing`/`success`/`failed`）。  
   - **重要**：API 协议已定稿，但生产 Base URL 尚未公开确认，正式发布前勿使用占位符或预发地址。详见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。

## 限制和注意事项

- **文件大小限制**：控制台体验页单文件上限为 200 MB（图文/文本/网页/电子书）、20 MB（图片）、200 MB（音频）、200 MB（视频）；API 上限更高（如图文 1 GB、视频 10 GB），具体见[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)。
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，无即时结果。客户端需轮询，且必须使用退避策略，避免高频查询。
- **配置与任务快照**：历史任务固定使用提交时的配置快照，编辑现有 `config_id` 仅影响后续新任务，不影响已运行任务。配置快照可在「任务记录」中查看。
- **OSS 托管安全要求**：若启用 OSS 结果落库，必须传入客户自有 STS 临时凭证（或 RAM 用户 AK），服务端不托管凭证。凭证权限须最小化（仅限源目录 `GetObject` + 结果目录 `PutObject`/`GetObject`）。
- **计费计量**：Parse 按图文页数、音视频秒数计费；Extract 按抽取页数计费（新文档直抽含解析，复用 ParseResult 单独计抽）。首次开通赠送额度，用尽后按量计费。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)



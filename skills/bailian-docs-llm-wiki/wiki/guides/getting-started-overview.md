# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，面向开发者提供控制台快速验证、配置复用、REST API 集成及 Agent Skill 封装等多渠道接入方式。本文档概述关键能力边界、参数规范、调用流程及硬性限制，帮助开发者在 5 分钟内完成首次任务提交与结果核验。

## 支持的模型/功能

ParseX 不提供通用大模型调用接口，而是封装了面向结构化内容生成与业务字段提取的专用能力：

- **文档解析（Parse）**：支持图文（PDF/Office/图片/HTML/EPUB 等）、音频（MP3/WAV/FLAC 等）、视频（MP4/MKV/AVI 等）三类输入，输出结构化正文、标题、表格、图片描述、语音转录、剧情分段与摘要等。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文输入（含已解析的图文 ParseResult），按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段值、来源页码（Citation）、状态（`missing`/`inferred`/`conflict`/`success`）。不支持音频或视频直接抽取，[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md) 明确指出该限制。
- **能力隔离**：Parse 与 Extract 严格分离，Extract 复用 ParseResult 时仅接受**图文类**解析结果；音频/视频 ParseResult 不可用于 Extract，此为硬性约束。

> **注意**：文档 11 和文档 12 均提及 REST API 入口为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`，但文档 14 的 OSS 托管说明中给出的预发地址为 `pre-maas.aliyuncs.com`，且正式 Base URL 在文档 12 中被明确标注为“尚未公开确认”。开发者应以控制台实际提供的生产端点为准，不可依赖文档中未确认的占位符地址。

## 关键参数

所有能力均围绕 `config_id` 与 `biz_id` 两个核心标识构建可复用、可追踪的工作流：

- **`config_id`**：通过控制台保存的不可变配置 ID，用于复用已验证的 Parse 解析设置或 Extract 字段 Schema。必须与能力类型匹配（Parse 配置不可用于 Extract），且调用时**禁止同时传入 `config_id` 与内联参数**，否则触发 `ConfigInlineConflict` 错误（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **`biz_id`**：每次任务提交后返回的异步业务任务 ID，用于轮询结果。客户端必须持久化该 ID 并在 `/result` 接口查询中精确复用，不可替换或推断。
- **Schema 规则**：Extract 的 `schema` 参数需符合兼容 LlamaIndex 的 JSON Schema 格式，但有独立限制：嵌套深度 ≤6 层、叶子字段数 ≤100、序列化后 ≤600 KB。不支持 `format`/`pattern` 等关键字，格式约束须写入 `description` 字段（见 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)）。
- **OSS 托管凭证**：若启用 OSS 结果直写，必须在请求中显式传入 STS 临时凭证（`access_key_id`/`access_key_secret`/`security_token`）或 RAM 用户 AK，服务端**不支持角色信任链自动获取**（见 [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)）。

## 使用方式

标准流程为「控制台验证 → 保存配置 → API 集成」三步：

1. **控制台快速验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区；  
   - 上传样例文件，调整配置（如 Parse 的图片描述开关、Extract 的字段 Schema），运行并核对 Markdown/JSON 结果；  
   - 通过 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md) 查看历史任务快照与状态。

2. **保存可复用配置**：  
   - 在工作台点击「保存配置」，填写名称后生成 `config_id`；  
   - 后续任务可直接引用该 ID，避免参数重复维护（见 [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)）。

3. **REST API 集成**：  
   - 使用 DashScope API Key 鉴权，调用 `/parse/submit` 或 `/extract/submit` 提交任务；  
   - 从响应中提取 `biz_id`，轮询 `/parse/result` 或 `/extract/result` 直至 `data.status` 为 `success`；  
   - 生产 Base URL 尚未公开，当前不可硬编码（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

## 限制和注意事项

- **文件大小限制**：控制台体验页单文件上限为 200 MB（文档 1），而 API 支持更大尺寸（图文 1 GB、音频 2 GB、视频 10 GB），具体以 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md) 为准。
- **异步行为约束**：所有任务均为异步，提交后立即返回 `biz_id`，无同步响应。轮询时需处理 `processing` 状态并采用退避策略；HTTP `409 ResultNotReady` 表示结果未就绪，**必须重用原 `biz_id` 查询，不可新建任务**（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **数据生命周期**：图文 ParseResult 仅保留 7 天，超期后无法被 Extract 复用（见 [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)）；任务记录同样仅保留最近 7 天。
- **Workspace 隔离**：配置、任务、用量均按 Workspace 隔离，切换 Workspace 后无法访问其他空间资源（见 [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)）。
- **幂等性缺失**：当前协议未定义客户端幂等键，提交超时后无法自动确认任务是否创建，需人工对账（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)



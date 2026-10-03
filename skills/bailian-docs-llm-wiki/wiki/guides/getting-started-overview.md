# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，面向开发者提供控制台快速验证、REST API 生产集成及 Agent Skill 封装三种使用路径。本文档概述关键能力边界、配置要点、调用方式及硬性限制，帮助开发者在 5 分钟内完成首次任务提交与结果核验。

## 支持的模型/功能

ParseX 不提供通用大模型调用接口，而是封装了针对多模态文档理解的专用处理链路：

- **Parse（文档解析）**：支持图文（PDF/Office/图片/HTML/EPUB 等）、音频（MP3/WAV/FLAC 等）、视频（MP4/MKV/AVI 等）三类输入，输出结构化内容（Markdown/JSON）、时间线、剧情分段与摘要。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **Extract（字段抽取）**：仅支持图文输入（含已解析的图文 ParseResult），按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段值、来源页码（Citation）、状态（`missing`/`inferred`/`conflict`/`success`）。不支持音频/视频直接抽取，[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md) 明确说明此限制。
- **功能隔离**：Parse 与 Extract 能力严格分离，Extract 复用 ParseResult 时仅接受图文类结果（音频/视频 ParseResult 不可复用），该约束在 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md) 中明确定义。

> **注意**：文档 19 中提到的 Agent Skill 安装命令（如 `npx skills add ...`）属于预发布规划内容，当前无正式发布入口与可验证的 Skill 包；实际集成应以 REST API 为准，避免依赖未上线的技能包。

## 关键参数

所有能力均围绕 `config_id` 与 `biz_id` 两个核心标识构建可复用、可追踪的工作流：

- **`config_id`**：通过控制台保存的不可变配置 ID，用于复用已验证的 Parse 解析设置或 Extract 字段 Schema。必须与能力类型匹配（Parse 配置不可用于 Extract 请求），且调用时禁止同时传入 `config_id` 与内联参数，否则触发 `ConfigInlineConflict` 错误（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **`biz_id`**：每次任务提交后返回的异步业务任务 ID，用于轮询结果状态（`processing`/`success`/`failed`）。客户端需持久化该 ID 并用于后续 `/result` 查询，不可自行构造或替换。
- **Schema 规则**：Extract 的 `schema` 参数必须为兼容 LlamaIndex 的 JSON Schema，但嵌套深度 ≤6、叶子字段数 ≤100、序列化后 ≤600 KB；不支持 `format`/`pattern` 等关键字，格式约束须写入 `description` 字段（见 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)）。

## 使用方式

开发者可通过三种路径接入，推荐按验证→集成→封装顺序推进：

1. **控制台快速验证**  
   登录 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，依次进入「文档解析」或「字段抽取」工作区，上传样例文件 → 调整配置 → 运行 → 核验结果（Markdown/JSON 视图对照原文）。配置保存后生成 `config_id`，用于后续 API 调用。

2. **REST API 生产集成**  
   使用 DashScope API Key 鉴权，调用以下定稿端点：  
   - Parse：`POST /parse/submit`（提交）、`POST /parse/result`（查询）  
   - Extract：`POST /extract/submit`（提交）、`POST /extract/result`（查询）  
   所有请求需携带 `Authorization: Bearer YOUR_API_KEY`，参数使用 `snake_case`，响应中提取 `biz_id` 并轮询。生产 Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`（见 [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)）。

3. **OSS 托管（可选）**  
   对数据合规有要求的场景，可在请求中传入 `output.oss_config`，指定客户自有 OSS Bucket 及 STS 临时凭证，使解析/抽取结果直写客户存储，避免结果落于服务侧（见 [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)）。

## 限制和注意事项

- **文件大小限制**：控制台体验页单文件上限为 200 MB（文档/文本/网页/电子书）或 20 MB（图片），而 API 接口支持更大尺寸（文档 1 GB、音频 2 GB、视频 10 GB），具体以 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md) 为准。
- **时效性约束**：图文 ParseResult 仅保留 7 天，超期后无法被 Extract 复用；任务记录也仅保留最近 7 天，历史任务需及时归档（见 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)）。
- **异步行为**：所有任务均为异步执行，提交后立即返回 `biz_id`，结果需轮询获取。HTTP `409 ResultNotReady` 表示结果未就绪，客户端应继续查询同一 `biz_id`，而非重复提交（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **免费额度**：新账号赠送一次性额度（图文解析 3,000 页、字段抽取 3,000 页、视频/音频各 100 小时），额度用尽后按量计费；直接抽取新文档费用（¥0.06/页）已包含解析成本，无需额外支付解析费（见 [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)）。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)



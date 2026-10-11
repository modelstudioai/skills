# getting started [overview](overview.md)

ParseX 是面向开发者的一站式文档智能处理平台，提供文档解析（Parse）与字段抽取（Extract）两大核心能力。本文档概述快速上手的关键路径：从控制台体验、配置管理到 API 集成，覆盖模型支持范围、关键参数含义、调用方式及生产级限制。所有操作均基于真实样本验证和可复用配置，确保结果稳定、可追溯、可审计。

## 支持的模型/功能

ParseX 提供两类正交能力，适用不同阶段的处理需求：

- **文档解析（Parse）**：将 PDF、Office 文档、图片、音频、视频等多模态输入转换为结构化内容。支持图文（含表格、图片描述、坐标）、音频（语音转录+说话人分离）和视频（剧情分段、摘要、抽帧理解）。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文输入（含已解析的 ParseResult），按用户定义的 JSON Schema 严格抽取业务字段，并返回字段值、来源页码（Citation）、状态（`missing`/`inferred`/`conflict`/`success`）。不支持音频/视频直接抽取，[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md) 明确说明此限制。

> **注意**：文档 18 与文档 20 均指出 Extract 仅支持图文，但文档 7 的“Extract适合解决什么问题”示例中未明确排除音视频；实际能力以文档 18 和文档 20 的权威声明为准，此处以文档 20 为准。

## 关键参数

核心参数围绕**能力选择**、**输入指定**和**配置复用**展开，避免重复定义：

- `config_id`：唯一标识已保存的 Parse 或 Extract 配置。**强烈推荐生产环境使用**，而非内联参数，以保障规则一致性与可维护性。配置需通过真实样本验证后保存，详见 [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- `biz_id`：每次异步任务的业务唯一标识，由 `/submit` 接口返回，用于后续轮询 `/result`。与 `request_id`（单次 HTTP 请求 ID）分离，不可互换。
- `file_url`（Parse/Extract 直接处理）或 `parsed_file_biz_id`（Extract 复用解析结果）：输入来源必须明确。复用 ParseResult 时，该 ID 必须来自已完成、类型为图文、且未超 7 天保留期的任务（见 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)）。
- `output.oss_config`（OSS 托管）：若需结果直写客户 OSS，必须传入 STS 临时凭证（`access_key_id`/`access_key_secret`/`security_token`）及 Bucket 信息。**不支持角色信任，凭证需客户端自行获取并传入**，详见 [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。

## 使用方式

遵循“验证→保存→复用”三步法，兼顾控制台快速验证与 API 稳定集成：

1. **控制台体验**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区。  
   - 上传样例文件 → 调整配置（如解析页数、字段 Schema）→ 运行 → 核验 Markdown/JSON 结果 → 逐字段对照原文（见 [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md) 和 [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)）。  
   - 成功后点击「保存配置」，获得 `config_id`。

2. **API 集成**：  
   - 使用 REST API（非 DashScope 通用接口），Base URL 为 `https://{workspace}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`。  
   - 认证：`Authorization: Bearer <DASHSCOPE_API_KEY>`（API Key 在控制台创建）。  
   - 调用流程：`POST /parse/submit` 或 `/extract/submit` → 保存响应中的 `biz_id` → 轮询 `POST /parse/result` 或 `/extract/result` → 检查 `data.status`（`processing`/`success`/`failed`）。  
   - **严禁同时传 `config_id` 与内联参数**，否则触发 `ConfigInlineConflict` 错误（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

3. **Skill 接入（实验性）**：  
   - 当前 Skill 为预发布状态，无官方安装命令或 Schema。正式使用前，必须从 ParseX 正式发布入口确认 Skill 名称、版本及权限，且 Skill 必须绑定 `config_id`，不得动态覆盖配置（见 [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)）。

## 限制和注意事项

- **文件大小**：控制台体验页限制为单文件 ≤200 MB（图文/视频）或 ≤20 MB（图片）；API 支持更大文件（图文 ≤1 GB，视频 ≤10 GB），以 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md) 为准。
- **Schema 限制**：Extract 的 `schema` 参数有严格约束：嵌套深度 ≤6 层、叶子字段数 ≤100、序列化后 ≤600 KB。不支持 `format`/`pattern` 等 JSON Schema 关键字，格式要求须写入 `description`（见 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)）。
- **异步行为**：所有任务均为异步。提交后立即返回 `biz_id`，结果需轮询查询；HTTP `409 ResultNotReady` 表示结果未就绪，应继续轮询原 `biz_id`，**不可重复提交**（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **数据隔离**：文件、配置、任务、用量均按 Workspace 隔离。切换 Workspace 后无法看到其他空间的资源（见 [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)）。
- **免费额度**：首次开通赠送图文解析/抽取各 3,000 页、音视频各 100 小时，额度一次性发放，用尽后按量计费（见 [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)）。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)



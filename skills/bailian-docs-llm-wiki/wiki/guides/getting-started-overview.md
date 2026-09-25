# getting started [overview](overview.md)

ParseX 是面向开发者的一站式文档理解平台，提供文档解析（Parse）与字段抽取（Extract）两大核心能力。本文档概述快速上手的关键路径：从控制台体验、配置管理到 API 集成，覆盖图文、音频、视频等多模态输入的结构化处理流程。所有操作均基于异步任务模型，强调配置复用、结果可验证与生产级集成可靠性。

## 支持的模型/功能

ParseX 不提供通用大模型调用接口，而是封装了针对文档理解场景深度优化的专用模型能力，分为两类：

- **文档解析（Parse）**：支持 PDF、Office 文档、图片、HTML、电子书、MP3/WAV 等音频及 MP4/MKV 等视频，输出结构化内容（如正文、标题、表格、图片描述、语音转录、剧情分段与摘要）。详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文类输入（含已解析的图文 ParseResult），按用户定义的 JSON Schema 抽取强类型业务字段（如合同编号、发票金额、报告期间），并返回字段值、来源页码（Citation）、状态（`missing`/`inferred`/`conflict`）等可审计信息。详见[字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

> **注意**：文档 19 明确指出“Extract 不能处理音频或视频”，而文档 2 的表格中曾将 Extract 列为“音频”“视频”的支持能力，该处为过时信息，应以文档 19 和文档 18 的明确限制为准。

## 关键参数

核心参数围绕任务定义、输入源与输出控制展开，需在控制台或 API 中显式指定：

- **`config_id`**：已保存的解析或抽取配置唯一标识，用于复用经验证的设置。必须通过[配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)流程创建，不可动态生成。
- **`biz_id`**：每次任务提交后返回的业务任务 ID，用于异步轮询结果（如调用 `/parse/result` 或 `/extract/result`）。与 `request_id`（API 请求级标识）分离，是结果追踪的唯一依据。
- **`file_url` / `parsed_file_biz_id`**：Extract 任务的输入源二选一。前者用于直接处理新文件；后者用于复用已有图文 ParseResult（需确保其未超 7 天保留期，见[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)）。
- **`schema`**：Extract 的必传参数，定义字段结构。严格遵循文档 9 的 JSON Schema 规则（如嵌套 ≤6 层、叶子字段 ≤100 个），不支持 `format`/`pattern` 等关键字，格式约束须写入 `description`。
- **`output.oss_config`**：OSS 托管必需参数，包含 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 及可选 `security_token`，用于将结果直写客户 OSS（见[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)）。

## 使用方式

推荐按“控制台验证 → 配置固化 → API 集成”三阶段演进：

1. **控制台验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区。  
   - 上传样例文件，调整配置（如解析页数、图片描述、字段 Schema），运行并核对 Markdown/JSON 结果与原文一致性（参考[获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)和[获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)）。  
   - 通过「保存配置」生成 `config_id`，确保后续调用行为可复现。

2. **配置固化**：  
   - 在左侧导航栏进入「配置」，管理已保存的 Parse/Extract 配置。编辑仅影响后续任务，历史任务快照可在「任务记录」中查看（见[任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)）。

3. **API 集成**：  
   - 使用 DashScope REST API（Base URL: `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`），携带 `Authorization: Bearer <DASHSCOPE_API_KEY>`。  
   - 提交任务（`/parse/submit` 或 `/extract/submit`）后，持久化 `biz_id` 并轮询 `/parse/result` 或 `/extract/result`，直至 `data.status` 为 `success` 或 `failed`。  
   - 生产环境必须使用 OSS 托管或服务端安全存储结果，禁止前端暴露 API Key（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

## 限制和注意事项

- **文件大小**：控制台体验页限制单文件 ≤200 MB（图片 ≤20 MB）；API 支持更大尺寸（文档 ≤1 GB，音频 ≤2 GB，视频 ≤10 GB），详见[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)。
- **异步模型**：所有任务均为异步，提交后立即返回 `biz_id`，无即时结果。客户端需实现带退避策略的轮询，避免高频请求（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **配置冲突**：API 调用中严禁同时传入 `config_id` 与内联参数（如 `processing` 或 `schema`），否则触发 `ConfigInlineConflict` 错误。规则变更必须新建配置并更新 `config_id`。
- **数据隔离**：文件、配置、任务、结果均按 Workspace 隔离。切换 Workspace 后无法访问其他空间资源（见[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)）。
- **免费额度**：首次开通赠送图文解析 3,000 页、字段抽取 3,000 页、音视频各 100 小时，用尽后按量计费（见[计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)）。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
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
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)



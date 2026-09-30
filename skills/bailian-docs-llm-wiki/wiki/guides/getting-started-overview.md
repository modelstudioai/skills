# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，面向开发者提供结构化内容生成与业务数据提取服务。本文档概述其支持模型/功能边界、关键参数定义、集成方式选择及生产环境必须关注的限制与注意事项，帮助开发者快速建立端到端集成路径。所有能力均通过异步任务模型交付，需配合 `biz_id` 轮询获取最终结果。

## 支持的模型/功能

ParseX 不提供通用大语言模型调用接口，而是封装了针对多模态文档理解的专用处理模型，分为两类能力：

- **文档解析（Parse）**：支持图文（PDF/Office/图片/HTML/EPUB等）、音频（MP3/WAV/FLAC等）、视频（MP4/MKV等）三类输入，输出结构化内容（如 Markdown/JSON）、时间线、剧情分段与摘要。详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文输入（含本地上传或复用 Parse 生成的图文 `ParseResult`），按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段值、状态（`missing`/`inferred`/`conflict`/`success`）及原文 Citation。**不支持音频、视频及其 ParseResult 复用**，该限制在[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)中明确强调。

> **注意**：文档 10 和文档 11 均提及 Agent Skill 接入，但文档 12 明确指出“当前可用资料未提供可公开确认的 Skill 正式名称、发布地址、安装命令……本页不虚构可安装的 Skill”，且所有 Skill 必须绑定已验证的 `config_id`，不可动态覆盖配置。因此，Skill 尚未进入稳定可用阶段，生产集成应以 REST API 为准。

## 关键参数

核心参数围绕任务提交、配置复用与结果控制展开：

- **`config_id`**：保存的解析或抽取配置唯一标识，用于复用已验证的设置。必须与能力类型（Parse/Extract）匹配，且属于当前 Workspace。使用时禁止同时传入内联参数（如 `processing` 或 `schema`），否则触发 `ConfigInlineConflict` 错误（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **`biz_id`**：每次任务提交返回的异步业务 ID，用于轮询结果。客户端必须持久化该值，不可丢弃或替换。
- **`schema`（Extract 专用）**：必传 JSON Schema，定义字段名、类型（`string`/`integer`/`number`/`boolean`/`object`/`array`）、嵌套结构及说明。最大嵌套深度为 6 层，叶子字段数 ≤ 100，序列化后 UTF-8 ≤ 600 KB（见[Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)）。不支持 `format`、`pattern` 等校验关键字，格式约束需写入 `description`。
- **`output.oss_config`（OSS 托管）**：启用客户自有 OSS 存储时必填，包含 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 及可选 `security_token`（STS 临时凭证）。**不支持角色信任，必须由客户端主动传入有效凭证**（见[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)）。

## 使用方式

开发者可通过两种正式渠道接入：

- **REST API（推荐）**：面向后端服务与工作流编排，使用 DashScope 鉴权（`Authorization: Bearer <DASHSCOPE_API_KEY>`）。Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`。完整流程为：① 提交 `/parse/submit` 或 `/extract/submit` → ② 保存响应中的 `biz_id` → ③ 轮询 `/parse/result` 或 `/extract/result` 直至 `data.status` 为 `success` 或 `failed`。轮询需实现退避策略，避免高频请求（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。
- **控制台体验与配置管理**：用于快速验证、调试与配置沉淀。所有能力均需先在控制台完成样本运行、结果核验，再通过「保存配置」生成 `config_id`，该 ID 是 API 集成的稳定基础。配置保存后，历史任务仍保留快照，编辑配置不影响已运行任务（见[配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)）。

## 限制和注意事项

- **文件大小与格式**：控制台体验页单文件上限为 200 MB（文档/图片/音频/视频均适用），而 API 支持更大体积（如视频 10 GB）。Extract 仅支持图文格式，明确不支持音频/视频（见[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)）。
- **异步任务生命周期**：ParseResult 默认保留 7 天，超期后无法被 Extract 复用；任务记录仅保留最近 7 天，需及时归档关键 `biz_id`（见[任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)）。
- **计量与免费额度**：图文按页计费（解析 ¥0.02/页，抽取 ¥0.04–¥0.06/页），音视频按秒计费。首次开通赠送 3,000 页图文解析/抽取额度、100 小时音视频解析额度，**额度不按月重置，用尽即按量计费**（见[计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)）。
- **安全性要求**：API Key 必须安全存储于服务端或密钥管理系统，严禁硬编码于前端、日志或仓库中；OSS 凭证同理，需动态获取并确保 STS Token 有效期覆盖任务周期。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
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
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)



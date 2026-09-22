# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两大核心能力，支持将图文、音频、视频等多模态材料转换为结构化结果，供下游 Agent 应用直接消费。本文档面向开发者，梳理从控制台体验到 API 集成的完整起点路径，涵盖能力边界、关键参数、使用方式及硬性约束，帮助快速建立可复用、可验证、可生产的处理流程。

## 支持的模型/功能

ParseX 不提供通用大模型调用接口，而是封装了两类专用模型服务：

- **文档解析（Parse）**：支持 PDF、Office 文档、图片、HTML、EPUB 等图文格式，以及 MP3、WAV、MP4、MKV 等音视频格式；输出结构化正文、表格、图片描述、时间线、剧情分段与摘要等。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文输入（含已解析的 ParseResult），按用户定义的 JSON Schema 抽取强类型业务字段（如合同编号、发票金额、报告期间），并返回字段值、来源页码（Citation）、状态（`missing`/`inferred`/`conflict`）等元信息。不支持音频或视频直接抽取，详见 [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

> **注意**：文档 20 明确指出 “Extract 可以处理音频或视频吗？不可以”，但文档 5 的表格中“您手中的材料”一栏将“音频”“视频”列为 Extract 的输入类型，该处为过时信息，应以文档 20 和文档 18 的明确限制为准。

## 关键参数

所有能力均围绕两个核心参数组织：

- **`config_id`**：通过控制台保存的不可变配置标识符，用于复用已验证的 Parse 解析设置或 Extract Schema。生产环境强烈推荐使用 `config_id` 而非内联参数，避免配置漂移。详见 [保存与复用配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **`biz_id`**：每次任务提交后返回的异步业务标识符，用于轮询结果状态（`processing`/`success`/`failed`）。客户端必须持久化该 ID 并用于后续 `/result` 查询，不可丢弃或替换。详见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。

Extract 还依赖 **`extract_schema`** 参数（JSON Schema 格式），其规则严格受限：嵌套深度 ≤6 层、叶子字段数 ≤100、序列化后 UTF-8 ≤600 KB，且仅支持 `type`/`description`/`properties`/`required`/`enum`/`default` 等关键字，`format`、`pattern` 等 LlamaIndex 常用关键字被忽略。详细限制见 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。

## 使用方式

### 控制台快速验证（推荐起点）
1. 登录 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」；
2. 上传样例文件（控制台单文件上限：图文/音频/视频 ≤200 MB，图片 ≤20 MB）；
3. 配置参数（Parse：调整页眉页脚、坐标、人声分离等；Extract：定义 Schema 或用自然语言生成）；
4. 点击「运行」，在结果区切换 Markdown/JSON 视图核验，并对照原文逐项检查标题、表格、图片描述或时间片段；
5. 验证通过后，点击「保存配置」生成 `config_id`，供后续复用。

### API 集成（生产部署）
- 使用 DashScope REST API，基础地址为 `https://{workspace}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`；
- 认证方式为 `Authorization: Bearer <DASHSCOPE_API_KEY>`，API Key 必须安全存储于服务端；
- 提交任务（`/parse/submit` 或 `/extract/submit`）后，立即保存响应中的 `request_id` 和 `data.biz_id`；
- 轮询 `/parse/result` 或 `/extract/result`，依据 `data.status` 判断终态，成功后读取 `data.result`；
- **严禁**同时传入 `config_id` 与内联参数（如 `processing` 或 `schema`），否则触发 `ConfigInlineConflict` 错误。

### 其他渠道
- **OSS 托管**：需客户自行准备 STS 临时凭证（或 RAM 用户 AK），在请求中通过 `output.oss_config` 字段传入 `bucket`/`endpoint`/`access_key_id`/`access_key_secret`/`security_token`，实现结果直写客户 OSS。详见 [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。
- **Agent Skill**：当前无公开可安装的正式 Skill，所有 Skill 接入必须基于 ParseX 官方发布入口，且必须绑定已验证的 `config_id`，禁止动态覆盖配置。详见 [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)。

## 限制和注意事项

- **文件限制**：API 端单文件上限高于控制台（图文/文本 ≤1 GB，音频 ≤2 GB，视频 ≤10 GB），但控制台体验页严格限制为 200 MB（文档 6、文档 18）。音视频仅支持 Parse，Extract 仅支持图文。
- **异步行为**：所有任务均为异步，提交后不返回结果，必须轮询 `biz_id`。HTTP `409 ResultNotReady` 表示结果未就绪，应继续查询原 `biz_id`，而非重试提交。
- **配置与历史任务隔离**：编辑已保存配置仅影响后续任务，历史任务始终使用提交时的“配置快照”，可在 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md) 中查看。
- **ParseResult 复用时效**：图文 ParseResult 仅保留 7 天，超期后 Extract 无法复用，需重新解析。
- **免费额度**：首次开通赠送图文解析 3,000 页、字段抽取 3,000 页、视频/音频各 100 小时，额度用尽后按量计费（图文解析 ¥0.02/页，视频 ¥0.002/秒，音频 ¥0.00035/秒）。

## 来源文档

- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)



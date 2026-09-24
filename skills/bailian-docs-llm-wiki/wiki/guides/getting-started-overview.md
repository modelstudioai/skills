# getting started [overview](overview.md)

ParseX 提供面向开发者的一站式文档智能处理能力，涵盖图文/音视频解析（Parse）与结构化字段抽取（Extract）两大核心功能。本文档概述其支持能力、关键参数、使用方式及限制，帮助开发者快速集成并规避常见陷阱。所有操作均基于异步任务模型，需通过 `biz_id` 轮询结果，不支持同步返回。

## 支持的模型/功能

ParseX 当前提供两类原子能力，**严格按输入类型隔离**：
- **文档解析（Parse）**：支持 PDF、Office 文档、图片、HTML、EPUB 等图文格式，以及 MP3、MP4、AVI 等音视频格式；输出结构化内容（Markdown/JSON）、位置坐标、图片描述、剧情分段与摘要等 [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)。
- **字段抽取（Extract）**：**仅支持图文输入**（含复用 Parse 生成的图文 `ParseResult`），不支持音频/视频或其解析结果；按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段状态（`missing`/`inferred`/`conflict`）与原文 Citation [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

> **注意**：文档 16 明确指出 Extract “不支持音频和视频”，而文档 5 的示例中提及“从合同中提取……”未限定输入类型，易引发误解；以文档 16 和文档 18 的明确声明为准。

## 关键参数

- **`config_id`**：已验证并保存的配置唯一标识，用于复用 Parse 解析设置或 Extract 字段 Schema。推荐在生产环境优先使用，避免内联参数维护风险 [保存与复用配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **`biz_id`**：每次任务提交返回的异步业务 ID，是轮询结果的唯一凭证；必须持久化存储，不可丢弃 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。
- **`schema`（Extract 专用）**：必传 JSON Schema，定义字段名、类型（`string`/`number`/`object`/`array` 等）、嵌套结构与说明。需满足嵌套深度 ≤6、叶子字段数 ≤100、序列化后 ≤600 KB 等硬性限制 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。
- **`output.oss_config`（OSS 托管）**：当需将结果直写客户 OSS 时，必须传入 STS 临时凭证（`access_key_id`/`access_key_secret`/`security_token`）、Bucket 名与 Endpoint；**不支持角色信任，凭证需由客户端自行获取并随请求传入** [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。

## 使用方式

1. **控制台体验**：登录 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，通过「文档解析」或「字段抽取」工作区上传文件、配置参数、运行并核验结果；所有操作均可保存为 `config_id` 复用 [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)。
2. **REST API 集成**：使用 DashScope API Key 鉴权，调用 `/parse/submit` 或 `/extract/submit` 提交任务，再用 `/parse/result` 或 `/extract/result` 轮询 `biz_id` 状态；**必须实现带退避的轮询逻辑，不可假设同步响应** [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。
3. **Agent Skill 封装**：Skill 应封装“选择输入 → 引用 `config_id` → 触发任务 → 轮询 → 返回结果”流程，**禁止动态拼接未验证的内联参数或绕过 Workspace 隔离**；当前 Skill 尚无公开安装命令，需从官方发布入口确认 [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)。

## 限制和注意事项

- **文件大小**：控制台上传限单文件 200 MB（图文/视频）或 20 MB（图片）；API 接口上限更高（图文 1 GB、视频 10 GB），以 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md) 为准。
- **异步时效**：所有任务均为异步，提交后立即返回 `biz_id`，结果需轮询；任务记录仅保留最近 7 天，ParseResult 复用期为 7 天 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)。
- **配置与任务快照**：编辑配置仅影响后续任务，历史任务始终使用提交时的配置快照；务必在任务详情页查看「配置快照」以复现问题 [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **安全红线**：API Key 必须服务端保管，禁止暴露于前端或日志；OSS 凭证需最小权限授权，禁止使用主账号 AK；Skill 不得将自然语言指令当作可信配置来源 [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)



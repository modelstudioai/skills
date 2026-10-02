# getting started [overview](overview.md)

ParseX 提供面向开发者的一站式文档智能处理能力，涵盖图文/音视频解析（Parse）与结构化字段抽取（Extract）两大核心功能。本文档概述其能力边界、关键配置项、集成方式及使用约束，帮助开发者快速验证、集成并规模化部署。所有功能均通过异步任务模型提供，需结合控制台体验与 REST API 实现生产级接入。

## 支持的模型/功能

ParseX 当前提供两类正交能力：

- **文档解析（Parse）**：支持 PDF、Office 文档、图片、HTML、EPUB 等图文格式，以及 MP3、WAV、MP4、MKV 等音视频格式，输出结构化内容（如 Markdown/JSON）、时间线、剧情分段与摘要。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：仅支持图文输入（含复用 Parse 生成的图文解析结果），按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段值、来源页码（Citation）、状态（`missing`/`conflict`/`inferred`）等可审计信息。不支持音频或视频直接抽取，[常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md) 明确说明此限制。

> **注意**：文档 11 和文档 20 均提及 Agent Skill 接入，但文档 20 明确警告“当前可用资料未提供可公开确认的 Skill 正式名称、发布地址、安装命令”，且所有 Skill 行为必须绑定已验证的 `config_id`；而文档 11 给出的 `npx skills add` 命令缺乏版本与发布方校验依据。因此，**Skill 尚未正式发布，不可用于生产环境，应以 REST API 或控制台为唯一可信接入路径**。

## 关键参数

| 参数类别 | 关键参数 | 说明 | 来源参考 |
|----------|----------|------|----------|
| **通用标识** | `biz_id` | 异步任务唯一业务 ID，用于轮询结果；`request_id` 仅用于单次请求排错 | [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md) |
| **配置复用** | `config_id` | 已保存的 Parse 或 Extract 配置 ID；API 调用时与内联参数二选一，**同时传入将触发 `ConfigInlineConflict` 错误** | [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md) |
| **输入指定** | `file_url` / `parsed_file_biz_id` | Extract 必须二选一：新文件用 `file_url`，复用解析结果则用 `parsed_file_biz_id`（非 `request_id`） | [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md) |
| **Schema 定义** | `extract_schema` | Extract 必传 JSON Schema，兼容 LlamaIndex 格式但有独立限制：嵌套深度 ≤6、叶子字段数 ≤100、大小 ≤600 KB；不支持 `format`/`pattern` 等关键字 | [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md) |
| **OSS 托管** | `output.oss_config` | 含 `bucket`/`endpoint`/`access_key_id`/`access_key_secret`/`security_token`；**不支持角色信任，必须传入 STS 临时凭证或 RAM 用户 AK** | [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md) |

## 使用方式

1. **控制台快速验证**  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区。  
   - 上传样例文件 → 调整配置（如 Parse 的图片描述、Extract 的 Schema）→ 点击「运行」→ 在「抽取字段详情」或「解析段落结果」中核验。  
   - 成功后点击「保存配置」生成 `config_id`，供后续 API 复用（见 [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)）。

2. **REST API 集成**  
   - 使用 DashScope API Key 鉴权（`Authorization: Bearer <DASHSCOPE_API_KEY>`）。  
   - 提交任务：`POST /parse/submit` 或 `POST /extract/submit`，传入 `file_url`（或 `parsed_file_biz_id`）与 `config_id`。  
   - 轮询结果：用响应中的 `biz_id` 调用 `POST /parse/result` 或 `POST /extract/result`，直至 `data.status` 为 `success` 或 `failed`。  
   - **注意**：生产 Base URL 尚未公开，预发地址不可用于生产（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

3. **OSS 托管（合规场景）**  
   - 为客户 OSS Bucket 创建最小权限策略（仅限目标目录的 `oss:GetObject`/`oss:PutObject`）。  
   - 通过 STS `AssumeRole` 获取临时凭证，填入 `output.oss_config` 字段。服务端将结果直写客户 OSS，避免数据出域。

## 限制和注意事项

- **文件限制**：控制台单文件上限为 200 MB（图文/音频/视频均同），API 上限更高（图文 1 GB、视频 10 GB），详见 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)。  
- **复用约束**：Extract 仅能复用**图文类** ParseResult，且保留期为 7 天；音视频 ParseResult 不可用于 Extract。  
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，**无同步响应**；客户端需轮询，且需实现退避策略避免高频查询。  
- **幂等性**：当前协议**未定义幂等键**，超时未收到响应时无法自动确认任务是否创建，需人工对账（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。  
- **Workspace 隔离**：配置、任务、结果均按 Workspace 隔离，切换 Workspace 后无法看到其他空间资源（见 [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)）。

## 来源文档

- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)



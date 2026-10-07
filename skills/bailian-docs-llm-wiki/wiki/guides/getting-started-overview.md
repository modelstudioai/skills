# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，帮助开发者将非结构化图文、音视频内容转化为结构化数据，并按业务 Schema 精准提取关键字段。本文档面向开发者，梳理从控制台体验到 API 集成的关键路径，涵盖模型/功能边界、核心参数含义、调用方式及硬性约束，所有信息均基于当前正式发布能力。

## 支持的模型/功能

ParseX 不提供通用大模型 API，而是封装了面向特定任务的专用处理模型：

- **文档解析（Parse）**：支持 PDF、Office 文档、扫描图片、HTML、EPUB 等图文格式，以及 MP3、WAV、MP4、MKV 等音视频格式；输出结构化正文、标题、表格、图片描述、语音转录、剧情分段与摘要等。详见 [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **字段抽取（Extract）**：**仅支持图文输入**（含复用 Parse 生成的图文结果），不支持音频/视频直接抽取；基于用户定义的 JSON Schema，从解析后的内容中提取强类型字段，并返回字段值、来源页码（Citation）、状态（`success`/`missing`/`inferred`/`conflict`）。详见 [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。
- > **注意**：文档 20 明确指出“Extract 当前仅支持图文文件”，而文档 17 的表格中 Extract 行对“音频”“视频”列为“不支持”，但文档 6 示例提到“从培训视频中提取”，该表述与事实不符，应以文档 17 和 20 为准。

## 关键参数

| 参数 | 作用 | 说明 |
|------|------|------|
| `config_id` | 复用已验证的配置 | 必须通过控制台保存获得，用于 REST API 中避免重复维护内联参数；[保存与复用配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md) 是配置生命周期管理的核心入口。 |
| `biz_id` | 异步任务唯一标识 | 提交任务后由服务返回，用于轮询结果；与 `request_id`（单次 API 请求 ID）分离，不可互换。 |
| `schema`（Extract） | 定义抽取字段结构 | 必传 JSON Schema，兼容 LlamaIndex 格式但有独立限制：嵌套深度 ≤6 层、叶子字段数 ≤100、序列化后 ≤600 KB；不支持 `format`/`pattern` 等关键字，需将约束写入 `description`。详见 [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。 |
| `output.oss_config` | OSS 托管结果写入配置 | 包含 `bucket`、`endpoint`、`access_key_id`、`access_key_secret`（`security_token` 可选），用于将结果直写客户 OSS；**不支持角色信任，必须传入 STS 临时凭证或 RAM 用户 AK**。详见 [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。 |

## 使用方式

1. **控制台快速验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区；  
   - 上传样例文件 → 调整配置（如解析页数、图片描述、字段 Schema）→ 点击运行 → 在「抽取字段详情」或「JSON」视图核验结果；  
   - 成功后点击「保存配置」生成 `config_id`，供后续复用。

2. **REST API 集成**：  
   - 使用 DashScope API Key 鉴权（`Authorization: Bearer <DASHSCOPE_API_KEY>`）；  
   - 提交端点：`POST /parse/submit` 或 `POST /extract/submit`；  
   - 查询端点：`POST /parse/result` 或 `POST /extract/result`，轮询 `biz_id` 直至 `data.status` 为 `success` 或 `failed`；  
   - **严禁同时传入 `config_id` 与对应内联参数**，否则触发 `ConfigInlineConflict` 错误（见 [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

3. **Skill 接入（预发布）**：  
   - 当前 Skill 尚未正式发布，无可用安装命令；正式发布后，Skill 应绑定已验证的 `config_id`，而非动态拼接参数（见 [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)）。

## 限制和注意事项

- **文件大小**：控制台体验页限制单文件 ≤200 MB（图文/视频）或 ≤20 MB（图片）；API 支持更大尺寸（图文 ≤1 GB，视频 ≤10 GB），以实际接口响应为准。
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，需轮询查询结果；HTTP `409 ResultNotReady` 表示结果未就绪，应继续轮询原 `biz_id`，**不可重复提交**。
- **复用边界**：  
  - 图文 ParseResult 可复用于 Extract，保留期为 **7 天**；  
  - 音频/视频 ParseResult **不可用于 Extract**；  
  - 历史任务始终使用提交时的配置快照，编辑配置不影响已运行任务（见 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)）。
- **计费计量**：  
  - 图文按“页”计费（PDF/PPT 按实际页数，Word/文本按 2000 字符折算 1 页）；  
  - 音视频按“秒”计费；  
  - 直接抽取新文档（¥0.06/页）包含解析费用，复用 ParseResult 抽取（¥0.04/页）不重复计费（见 [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)）。

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
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)



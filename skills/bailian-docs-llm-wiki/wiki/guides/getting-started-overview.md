# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，面向开发者提供结构化内容生成与业务数据提取服务。本文档概述其支持范围、关键配置项、集成方式及使用约束，帮助开发者快速评估适用性并启动集成。所有能力均通过异步任务模型提供，需结合控制台验证与 API 集成分阶段落地。

## 支持的模型/功能

Parse 和 Extract 是两个正交但可协同的能力：

- **Parse**：支持图文（PDF/Office/图片/HTML/电子书）、音频（MP3/WAV 等）、视频（MP4/MKV 等）三类输入，输出结构化内容（如 Markdown/JSON 格式的正文、表格、图片描述、语音转写、剧情分段与摘要）。详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。
- **Extract**：**仅支持图文输入**（含本地文件或已解析的图文 ParseResult），不支持音频/视频；按用户定义的 JSON Schema 抽取强类型业务字段，并返回字段值、状态（`missing`/`inferred`/`conflict`/`success`）及原文 Citation。详见[字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

> **注意**：文档 19 明确指出“Extract 可以处理音频或视频吗？不可以”，而文档 20 的表格中 Extract 行对“音频”“视频”列为空（即不支持），但文档 1 的表格曾模糊列出“音频”“视频”在“Parse 适合解决什么问题”下，易引发误解。此处以文档 19 和文档 20 的明确否定为准。

## 关键参数

- **`config_id`**：已保存的 Parse 或 Extract 配置唯一标识，用于 API 复用稳定规则。必须通过控制台真实样本验证后保存获得，不可凭空构造。配置管理见[配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)。
- **`biz_id`**：每次任务提交返回的业务任务 ID，用于异步轮询结果；与 `request_id`（单次 API 请求 ID）分离，是结果查询的必需凭证。
- **Schema（Extract 专用）**：必须为兼容 LlamaIndex 的 JSON Schema 格式，但有严格限制：嵌套深度 ≤ 6 层、叶子字段数 ≤ 100、序列化后 UTF-8 ≤ 600 KB；不支持 `format`/`pattern` 等关键字，格式约束须写入 `description`。详见[Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。
- **OSS 托管参数（可选）**：若启用客户 OSS 结果落库，需在 `output.oss_config` 中传入 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 及可选 `security_token`（STS 凭证），且权限策略须最小化授权。详见[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)。

## 使用方式

1. **控制台快速验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区；  
   - 上传样例文件 → 调整配置（如 Parse 的页眉页脚、图片描述；Extract 的字段名/类型/说明）→ 提交运行 → 对照原文核验结果（Markdown 视图阅读、JSON 视图检查结构）；  
   - 成功后点击「保存配置」生成 `config_id`，供后续复用。

2. **API 集成（生产环境）**：  
   - 使用 DashScope REST API，Base URL 形如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`；  
   - 鉴权：`Authorization: Bearer <DASHSCOPE_API_KEY>`（API Key 须服务端安全保管）；  
   - 异步流程：`POST /parse/submit` 或 `POST /extract/submit` → 保存响应中的 `biz_id` → 轮询 `POST /parse/result` 或 `POST /extract/result` 直至 `data.status` 为 `success` 或 `failed`；  
   - **严禁同时传 `config_id` 与内联参数**，否则触发 `ConfigInlineConflict` 错误（见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)）。

3. **Skill 接入（实验性）**：  
   - 当前 Skill 尚未正式发布，无公开安装命令或契约定义；若使用，必须绑定已验证的 `config_id`，禁止动态覆盖配置（见[Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)）。

## 限制和注意事项

- **文件限制**：控制台上传单文件上限为 200 MB（图文/音频/视频均同），API 支持更大尺寸（图文 1 GB、图片 20 MB、音频 2 GB、视频 10 GB）；但音频/视频 ParseResult **不可用于 Extract**（文档 19、20 明确）。
- **复用时效**：图文 ParseResult 仅保留 **7 天**，超期后 Extract 无法复用（文档 19）；任务记录也仅保留最近 7 天（文档 16）。
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，**不返回结果**；轮询时需处理 `processing` 状态并采用退避策略，避免高频请求（文档 11）。
- **计费计量**：  
  - Parse：图文按处理页数（PDF/扫描件按实际页；Word/文本按 2000 字符折算 1 页），音视频按秒；  
  - Extract：新文档直接抽取（¥0.06/页，含解析）；复用 ParseResult 抽取（¥0.04/页）；  
  - 免费额度为一次性赠送（图文/抽取各 3000 页，音视频各 100 小时），用尽后自动按量计费（文档 18）。
- **Workspace 隔离**：配置、任务、结果均按 Workspace 隔离，切换 Workspace 后无法看到其他空间的资源（文档 19）。

## 来源文档

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
- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)



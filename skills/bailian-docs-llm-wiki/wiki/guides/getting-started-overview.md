# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两类核心能力，分别面向内容结构化与业务数据提取场景。开发者可通过控制台快速验证、保存配置，并通过 REST API 或 Skill 集成到自有系统。本文档梳理关键能力边界、参数规范、调用路径及硬性约束，帮助开发者在 5 分钟内完成首次可用任务。

## 支持的模型/功能

Parse 和 Extract 是两个正交能力，**不可混用**：  
- **Parse** 支持图文（PDF/Office/图片/HTML/电子书）、音频（MP3/WAV 等）、视频（MP4/MKV 等）三类输入，输出结构化内容（如 Markdown/JSON）、时间线、剧情分段与摘要；详见[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)。  
- **Extract** **仅支持图文输入**（含本地上传或复用 Parse 生成的图文 `ParseResult`），不支持音频/视频；它按用户定义的 JSON Schema 抽取强类型字段，并返回字段值、状态（`missing`/`inferred`/`conflict`）与原文来源页码；详见[字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。  
> **注意**：文档 19 明确指出 “Extract 当前仅支持图文文件，也只能复用图文 ParseResult”，但文档 20 的表格中将 “有效的图文 ParseResult” 列为 Extract 的输入类型，而未标注“仅限图文”。该表述存在歧义，实际限制以文档 19 为准——**音频/视频 ParseResult 不可用于 Extract**。

## 关键参数

- **`config_id`**：已保存的配置唯一标识，用于复用经验证的 Parse 解析设置或 Extract 字段 Schema。必须与能力类型匹配（Parse 配置不可用于 Extract 调用）。  
- **`biz_id`**：异步任务唯一业务 ID，由 `submit` 接口返回，用于后续轮询 `result` 接口获取最终结果；见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。  
- **`schema`**（Extract 必填）：定义抽取字段的 JSON Schema，需严格满足嵌套深度 ≤6、叶子字段数 ≤100、序列化后 ≤600 KB 等限制；不支持 `format`/`pattern` 等关键字，格式约束须写入 `description`；详见[Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)。  
- **`output.oss_config`**（可选）：启用 OSS 托管时必填，包含 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 及可选 `security_token`；凭证需由客户自行获取并传入，服务端不代为生成。

## 使用方式

1. **控制台快速验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区；  
   - 上传样例文件 → 调整配置（如 Parse 的“图片描述”开关、Extract 的字段 Schema）→ 点击「运行」→ 核验结果（Markdown 视图适合阅读，JSON 视图适合检查结构）；  
   - 成功后点击「保存配置」生成 `config_id`，供后续 API 复用。  

2. **REST API 集成**：  
   - 使用 DashScope API Key 鉴权（`Authorization: Bearer <DASHSCOPE_API_KEY>`）；  
   - 调用 `/parse/submit` 或 `/extract/submit` 提交任务，传入 `file_url`（或 `parsed_file_biz_id` for Extract）与 `config_id`；  
   - 用返回的 `biz_id` 轮询 `/parse/result` 或 `/extract/result`，直至 `data.status` 为 `success`；  
   - 注意：**`config_id` 与内联参数不可共存**，否则触发 `ConfigInlineConflict` 错误；见[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)。  

3. **Skill 集成（Beta）**：  
   - 仅支持已发布官方 Skill，需通过 `npx skills add` 安装；  
   - Skill 必须绑定已验证的 `config_id`，**不得动态覆盖配置**；  
   - 当前无公开可安装 Skill 名称，切勿根据文档标题猜测安装命令；详见[Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)。

## 限制和注意事项

- **文件大小**：控制台上传单文件上限为 200 MB（图文/音频/视频均适用），但 API 支持更大尺寸（图文 1 GB、音频 2 GB、视频 10 GB）；见[支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)。  
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，**不返回结果**；必须轮询 `result` 接口获取最终状态，`processing` 状态需退避重试。  
- **复用时效**：图文 `ParseResult` 仅保留 **7 天**，超期后无法被 Extract 复用；音频/视频 ParseResult 不可用于 Extract。  
- **计量计费**：Parse 按页（图文）或秒（音视频）计费；Extract 按页计费，且“新文档直接抽取”单价已含解析费用；免费额度为一次性赠送，用尽即按量计费；见[计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)。  
> **注意**：文档 15 称“当前只会保存最近7天的历史任务”，而文档 19 称“当前可复用的图文 ParseResult 保留 7天”，二者口径一致；但文档 12 的 REST API 文档未明确提及此保留期，开发者需以文档 19 为准，在业务逻辑中强制设置 7 天过期策略。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)



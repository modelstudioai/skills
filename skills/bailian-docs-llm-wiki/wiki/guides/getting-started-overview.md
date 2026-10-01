# getting started [overview](overview.md)

ParseX 提供文档解析（Parse）与字段抽取（Extract）两大核心能力，分别面向内容结构化与业务数据提取。本文档为开发者提供统一的入门概览，涵盖能力边界、关键配置、调用方式及生产约束，所有说明均基于当前已定稿的协议与控制台行为，不包含预发布或实验性功能。

## 支持的模型/功能

Parse 和 Extract 是两个正交能力，**不可混用**：  
- **Parse** 支持图文（PDF/DOCX/PPTX/图片等）、音频（MP3/WAV 等）、视频（MP4/MKV 等）三类输入，输出结构化内容（如 Markdown、JSON、剧情分段、帧图等），是 Extract 的前置依赖；[文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md) 详细说明了各类材料的适用场景与结果组织方式。  
- **Extract** 仅支持图文输入（含本地上传或复用 Parse 生成的图文 `ParseResult`），不支持音频/视频及其 ParseResult；它按用户定义的 JSON Schema 抽取强类型字段，并返回字段值、状态（`missing`/`inferred`/`conflict`）、原文证据（Citation）等可审计信息；[字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md) 明确其解决的是“合同编号、票据金额、报告指标”等结构化业务数据提取问题。  
> **注意**：文档 19 中称“Extract 可复用图文 ParseResult”，但文档 17 明确限定“音频或视频 ParseResult 不能用于 Extract”。二者一致，无矛盾；需注意 Extract 仅接受**图文类** ParseResult，且该结果须在 7 天保留期内（见 [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)）。

## 关键参数

- **`config_id`**：已验证并保存的配置唯一标识，用于 REST API 调用中复用 Parse 解析设置或 Extract Schema。必须与能力类型匹配（Parse 配置不可用于 Extract），且仅在当前 Workspace 有效；[保存与复用配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md) 规定了其创建、测试与引用流程。  
- **`biz_id`**：每次异步任务的业务标识，由 `/submit` 接口返回，用于后续 `/result` 查询；客户端必须持久化该 ID 并轮询，不可丢弃或替换。  
- **Schema 定义**：Extract 的必传参数，采用兼容 LlamaIndex 的 JSON Schema 格式，但有严格限制（嵌套 ≤6 层、叶子字段 ≤100、大小 ≤600 KB）；不支持 `format`/`pattern` 等关键字，格式约束需写入 `description`；[Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md) 是唯一权威规范。  
- **OSS 托管参数**（可选）：通过 `output.oss_config` 传入客户自有 OSS 的 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 及（可选）`security_token`，实现结果直写客户存储；该方案要求客户自行管理 STS 凭证生命周期，[OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md) 详述了权限策略与异常排查。

## 使用方式

1. **控制台快速验证**：  
   - 进入 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，选择「文档解析」或「字段抽取」工作区；  
   - 上传文件或选择样例 → 调整配置（如页数范围、字段 Schema）→ 点击「运行文档解析」或「运行字段抽取」→ 在结果区切换 Markdown/JSON 视图核验；  
   - 成功后点击「保存配置」生成 `config_id`，供 API 复用；[快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md) 给出了完整操作流。  

2. **REST API 集成**：  
   - 使用 DashScope API Key 鉴权，Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x`；  
   - 调用 `/parse/submit` 或 `/extract/submit` 提交任务，必须传 `config_id` 或内联参数（二者互斥，同时传将触发 `ConfigInlineConflict` 错误）；  
   - 用返回的 `biz_id` 轮询 `/parse/result` 或 `/extract/result`，直到 `data.status` 为 `success` 或 `failed`；[REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md) 定义了完整协议与错误处理策略。  

3. **Agent Skill（预发布）**：  
   - Skill 尚未正式发布，当前无官方安装命令或参数 Schema；任何非 ParseX 正式发布入口提供的 Skill 均不可信；[Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md) 强调 Skill 必须绑定 `config_id`，禁止动态覆盖配置。

## 限制和注意事项

- **文件限制**：控制台体验页单文件上限为 200 MB（图文/视频）或 20 MB（图片），API 上限更高（图文 1 GB、视频 10 GB）；具体以 [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md) 为准。  
- **异步行为**：所有任务均为异步，提交后立即返回 `biz_id`，结果需轮询获取；HTTP `409 ResultNotReady` 表示结果未就绪，应继续查询同一 `biz_id`，而非重提任务。  
- **幂等性缺失**：当前协议**未定义幂等键**，客户端无法自动确认超时请求是否已提交；若提交超时，需人工对账，不可盲目重试。  
- **Workspace 隔离**：配置、任务、用量均按 Workspace 隔离；切换 Workspace 后原资源不可见，务必确认当前环境。  
- **免费额度**：首次开通赠送图文解析/字段抽取各 3,000 页、音视频各 100 小时；额度用尽后按量计费（图文解析 ¥0.02/页，字段抽取 ¥0.04–¥0.06/页），详见 [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/getting-started-overview/quickstart.md)
- [配置文档解析](../../raw/application-user-guide/getting-started-overview/overview/configuration.md)
- [使用文档解析控制台](../../raw/application-user-guide/getting-started-overview/overview/playground-parse.md)
- [获取文档解析结果](../../raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)
- [字段抽取概览](../../raw/application-user-guide/getting-started-overview/extract-overview.md)
- [使用字段抽取控制台](../../raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)
- [配置字段抽取](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)
- [获取字段抽取结果](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)
- [Schema规则参考](../../raw/application-user-guide/getting-started-overview/extract-overview/extract-schema.md)
- [REST API 接入](../../raw/application-user-guide/getting-started-overview/integration-overview/rest-api.md)
- [服务渠道](../../raw/application-user-guide/getting-started-overview/integration-overview.md)
- [Skill 接入要求](../../raw/application-user-guide/getting-started-overview/integration-overview/integration-skill.md)
- [OSS 托管使用](../../raw/application-user-guide/getting-started-overview/integration-overview/parse-x-oss-integration.md)
- [任务记录](../../raw/application-user-guide/getting-started-overview/settings-configurations/tasks.md)
- [配置](../../raw/application-user-guide/getting-started-overview/settings-configurations.md)
- [用量](../../raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)
- [支持的文件与限制](../../raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)
- [计量与计费](../../raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)
- [常见问题](../../raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)
- [文档解析概览](../../raw/application-user-guide/getting-started-overview/overview.md)



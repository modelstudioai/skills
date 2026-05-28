---
name: bailian-docs-llm-wiki
description: >-
  阿里云百炼平台技术文档知识库（LLM Wiki）。当用户查询百炼模型列表、API 参数、错误码、
  应用开发（智能体/RAG/知识库/记忆/插件）、模型对比与定价、SDK/OpenAI 兼容接口、
  多模态能力（语音/图片/视频）、Token 计费等百炼相关问题时激活。
  包含 models 结构化模型市场数据（含 contextWindow/QPM/价格/sample code）、
  wiki 合成层（主题页/概念页/对比页）和 raw 原始文档层；
  模型规格类问题先查 models/index.md，文档类问题先查 wiki/index.md。
---

# 百炼文档知识库

> 阿里云百炼平台的完整技术文档知识库，涵盖模型使用、应用开发、API 参考等内容。

## 何时使用

当用户涉及以下场景时激活此 Skill：

- 查询百炼平台的模型列表、模型参数、调用方式（含具体模型的 contextWindow、QPM、定价、sample code 等结构化字段 → 查 `models/`）
- 查阅百炼 API 参数、请求/响应格式、错误码
- 了解百炼应用开发（智能体、RAG、知识库、记忆、插件等）
- 选择模型、比较模型能力、了解模型定价与限流
- 使用百炼 SDK / OpenAI 兼容接口
- 语音识别、语音合成、图片生成、视频生成等多模态能力
- Token Plan、计费、免费额度等商务问题

## 何时**不要**使用

下面这些场景与百炼文档无关，**不要激活**本 Skill：

- 询问 OpenAI / Anthropic / Google 等其他厂商的 API、模型或定价
- 通用编程问题、框架问题（React、Vue、Spring 等）
- `bl` CLI 命令本身的用法（那是 `bailian-cli` skill 的职责）
- 与百炼无关的阿里云产品（OSS、ECS、RDS 等）

## 文档层级

### 1. Wiki 层（合成层） — `wiki/`

由 LLM 自动合成的结构化 Wiki，包含三类页面：

- **主题页**：按功能领域聚合的综合文档（`wiki/guides/*.md`、`wiki/api/*.md`）
- **概念页**：跨主题的横切概念（`wiki/concepts/*.md`，如 RAG、流式输出、Function Calling 等）
- **对比页**：同类方案的结构化对比分析（`wiki/comparisons/*.md`，含对比表格）

**优先查阅 `wiki/index.md`，它是全部 wiki 页面的索引入口。**

每篇主题页末尾都有 `## 来源文档` 段落，列出对应的 raw 原文路径，可用于追溯和深度阅读。

### 2. Models 层（模型市场结构化数据） — `models/`

直接从百炼 console 网关 `listFoundationModels` 抓取的**结构化模型元数据**，
对应「模型广场」页面。涉及具体模型的能力、上下文长度、QPM 限流、定价、
官方 sample code 等问题时，优先查这里，比 wiki 更新更准。

**三层产物，单一数据源**（`families.jsonl` / `models.jsonl` 是机器查询入口，`index.md` 是 `families.jsonl` 的人类可读视图）：

- `models/index.md` — 按主能力分桶的家族索引（中文标签 + 模型代码 + 链接到明细 JSON），适合「概览扫一眼」
- `models/families.jsonl` — **每行一个家族**，含 `slug` / `name` / `description` / `primaryCapability` /
  `capabilities`（家族下所有 item 的并集）/ `providers` / `itemCount` / `maxContextWindow` / 轻量 `items[]`
  摘要（每个 item 只含 `model` / `name` / `contextWindow` / `capabilities` / `openSource`）/ `detailPath`。
  适合按家族筛选，例如：
  - 列出推理类家族：`jq -c 'select(.primaryCapability=="Reasoning") | {slug,name,itemCount}' families.jsonl`
  - 找包含某个 provider 的家族：`grep '"moonshot-ai"' families.jsonl | jq -c .slug`
- `models/models.jsonl` — **每行一个主干模型**（跨家族扁平），含 `model` / `family` / `capabilities` /
  `features` / `contextWindow` / `maxInputTokens` / `maxOutputTokens` / `prices`（精简）/ `qpmInfo`（精简）/
  `docUrl` / `detailPath`。适合跨家族批量查询，例如：
  - 列出所有 contextWindow ≥ 1M 的模型：`jq -c 'select(.contextWindow>=1000000)' models.jsonl`
  - 找支持 function-calling 的文本模型：`grep '"function-calling"' models.jsonl | jq -c '{model,family,contextWindow}'`

两份 JSONL 的 **join 字段**：`models.jsonl[].family == families.jsonl[].slug`。命中后按 `detailPath` 打开 `groups/<slug>.json` 取完整字段（`samples`、`predictConfig`）。
- `models/groups/<slug>.json` — 单个模型家族（如 `qwen3-max`、`deepseek`、`wan-image-to-video`）的完整明细：
  - 家族层：`name`、`description`
  - `items[]`：该家族下所有**主干模型版本**（剔除了带日期后缀的快照），已经过裁剪
    （丢弃了 `permissions` / `activationStatus` / `quota` / `scope` / `tags` / `license` /
    `serviceSites` / `modelInfo` 等与模型能力无关的账号/UI 字段），保留：
    `model`（API 调用名）、`modelAlias`、`contextWindow`、`maxInputTokens`、`maxOutputTokens`、
    `capabilities`、`features`、`provider`、`docUrl`、`prices`、`qpmInfo`、
    `samples`（**调用示例**，扁平化结构：`samples.<sdk>.<api>.{curl,python,nodejs,java,docUrl}`，
    例如 `samples.openai.completionsAPI.python` 直接是代码字符串）、
    `predictConfig`（**模型调用入参定义**：从 `getPredictParamConfig` 网关获取，
    含 `system`/`temperature`/`top_p`/`enable_search`/`enable_thinking` 等参数的
    `name`/`key`/`default`/`tip`/`range`，与百炼 Playground 对齐）
- `models/meta.json` — 增量爬取的指纹缓存，**不要给用户引用**

> 数据通过 `pnpm --filter bailian-docs-llm-wiki run crawl:models` 刷新。

#### 能力代码（capability）映射

`index.md` 的章节标题与 `items[].capabilities[]` 用的是英文短代码，
对应中文含义如下：

| 代码                       | 中文标签       |
| -------------------------- | -------------- |
| `TG`                       | 文本生成       |
| `Reasoning`                | 推理           |
| `VU`                       | 视觉理解       |
| `IG`                       | 图像生成       |
| `VG`                       | 视频生成       |
| `TTS`                      | 语音合成       |
| `ASR`                      | 语音识别       |
| `Realtime-ASR`             | 实时语音识别   |
| `Realtime-Text-to-Speech`  | 实时语音合成   |
| `Realtime-Audio-Translate` | 实时音频翻译   |
| `Realtime-Omni`            | 实时全模态     |
| `Multimodal-Omni`          | 全模态         |
| `ME`                       | 多模态嵌入     |
| `TR`                       | 翻译           |
| `3D-generation`            | 3D 生成        |

一个模型常常带多个 capability，`index.md` 中按 `capabilities[0]`（主能力）归类，
查找时按中文标签即可定位章节。

### 3. Raw 层（原始层） — `raw/`

从 help.aliyun.com 爬取的原始文档，按分类存放：

- `raw/model-user-guide/` — 模型使用指南
- `raw/application-user-guide/` — 应用使用指南
- `raw/model-api-reference/` — 模型 API 参考
- `raw/application-api-reference/` — 应用 API 参考

当 wiki / models 层信息不足时，从 raw 层获取完整原文。

## 强约束

- **回答必须基于 `wiki/` 或 `raw/` 下的实际文件内容**，不得凭印象编造 API、参数名、错误码或定价数字。
- **引用时附带相对路径**（如 `wiki/api/qwen-api.md`），方便用户验证。
- 如果在 `wiki-metadata.json` 中查到某页面 `qualityScore <= 2`，直接绕过 wiki 该页，回退到 `raw/` 原文回答。

## 查阅流程

1. **模型规格类问题先查 models**：
   - **具体某个模型**的能力、上下文、QPM、价格、官方示例代码 → 看 `index.md` 定位家族 → 打开 `groups/<slug>.json`
   - **跨家族筛选模型**（如「上下文 ≥ 1M 的模型」「支持 function-calling 的推理模型」）→ grep `models.jsonl`
   - **按家族维度筛选**（如「有哪些纯推理家族」「moonshot 旗下都有哪些家族」）→ grep `families.jsonl`
   - 命中后按 `detailPath` 打开对应 `groups/<slug>.json` 取 `samples` / `predictConfig` 等完整字段
2. **概念/使用方式查 wiki 索引**：读取 `wiki/index.md` 找到对应的主题页、概念页或对比页
3. **概念/对比优先**：跨领域问题或方案选型问题，优先看 `wiki/concepts/*` 与 `wiki/comparisons/*`
4. **回溯 raw 原文**：从主题页末尾的 `## 来源文档` 列表点进 `raw/.../*.md` 看完整细节
5. **全文索引**：`llms.txt` 含完整目录树；`llms-full.txt` 含全文拼接，可用 grep
6. **特定参数/错误码**：直接在 `raw/` 下用 grep

## 快速定位映射

| 关键词                                | 推荐入口路径                                             |
| ------------------------------------- | -------------------------------------------------------- |
| 某模型的 contextWindow / 价格 / QPM / sample code / 入参定义 | `models/groups/<slug>.json`（从 `models/index.md` 找 slug） |
| **跨家族筛选模型**：按 contextWindow / capability / feature / price 批量查找 | `models/models.jsonl`（`grep` / `jq` 一行一模型） |
| **按家族筛选**：按 primaryCapability / providers / itemCount / maxContextWindow 找家族 | `models/families.jsonl`（一行一家族，含 items[] 摘要） |
| 模型家族总览 / 按能力分桶浏览         | `models/index.md`                                        |
| 模型列表 / Qwen / DeepSeek            | `wiki/guides/more-about-models.md`                       |
| 文本对话 / Chat Completion  | `wiki/api/text-generation-api-reference.md`              |
| 语音合成 / TTS              | `wiki/api/speech-synthesis-api-reference.md`             |
| 语音识别 / ASR              | `wiki/api/speech-recognition-api-reference.md`           |
| 图片生成 / 图片编辑         | `wiki/api/image-generation-api-reference.md`             |
| 视频生成                    | `wiki/api/video-generation-api-reference.md`             |
| 多模态 / Omni               | `wiki/api/multimodal-api-reference.md`                   |
| Function Calling / 工具调用 | `wiki/concepts/function-calling.md`                      |
| RAG / 知识库                | `wiki/concepts/rag.md` + `wiki/guides/knowledge-base.md` |
| 智能体 / 应用调用           | `wiki/guides/application-call.md`                        |
| OpenAI 兼容                 | `wiki/concepts/openai-compatibility.md`                  |
| Token / 计费 / 限流         | `wiki/guides/billing-and-rate-limit.md`                  |

> 实际文件名以 `wiki/index.md` 为准；上表若有出入应回到索引页查找。

## 注意事项

- 文档持续更新，如遇矛盾以 `models/` > `raw/` > `wiki/` 的顺序为准
  （`models/` 直接拉自 console 网关，最新；`raw/` 是源站爬取；`wiki/` 是 LLM 合成可能滞后）
- `metadata.json` 记录每篇 raw 文档的最后修改时间
- `wiki-metadata.json` 记录每个 wiki 页面的合成 hash、时间戳、可选的 `qualityScore`
- `wiki/eval-report.md` 是最近一次评测报告（结构问题、断链、长度异常等）
- `wiki/` 目录可能尚未生成（需运行 `pnpm --filter bailian-docs-llm-wiki run synthesize`）

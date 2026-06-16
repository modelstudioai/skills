# [more](more.md) models

百炼平台除通用大语言模型外，还提供多种专用模型的 API，覆盖机器翻译、深度研究、OCR 文字提取、文本排序、意图理解和法律等垂直场景。这些模型均可通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope API 调用，开发者可根据业务需求选择合适的模型快速集成。本文汇总了这些专用模型的核心能力、关键参数和调用方式。

## 模型总览

| 模型 | 模型名称 | 核心能力 | 接口协议 |
|------|---------|---------|---------|
| Qwen-MT | qwen-mt-plus / qwen-mt-turbo | 机器翻译，支持术语干预、翻译记忆、领域提示 | OpenAI 兼容 / DashScope |
| Qwen-Deep-Research | qwen-deep-research | 深入研究，自动搜索、分析并生成研究报告 | 仅 DashScope（Python SDK） |
| Qwen-OCR | qwen3.5-ocr 等 | 图片文字提取与结构化识别 | OpenAI 兼容 / DashScope |
| 文本排序 | qwen3-rerank / qwen3-vl-rerank / gte-rerank-v2 | 文档相关性排序，提升检索精度 | HTTP / DashScope SDK |
| 意图理解 | tongyi-intent-detect-v3 | 百毫秒级意图识别与工具选择 | OpenAI 兼容 / DashScope |
| 通义法睿 | farui-plus | 法律咨询、文书生成、案情分析 | DashScope SDK |

## Qwen-MT 翻译模型

Qwen-MT 提供高质量机器翻译能力，通过 `translation_options` 参数控制翻译行为。详细参数说明参见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。

**关键参数：**

- `source_lang` / `target_lang`：源语言和目标语言，`source_lang` 支持设为 `auto` 自动检测
- `terms`：术语干预列表，指定专业术语的翻译方式
- `tm_list`：翻译记忆列表，提供参考翻译对以提升一致性
- `domains`：领域提示，指导模型按特定领域风格翻译

**调用方式：** 通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，将翻译参数放入 `extra_body`（Python）或请求体顶层（curl）的 `translation_options` 字段。

**多地域支持：** 北京、新加坡、美国（弗吉尼亚）三个地域，各地域使用不同的 `base_url` 和 API Key。

## Qwen-Deep-Research 深入研究模型

Qwen-Deep-Research 采用两阶段调用模式：第一步模型反问确认研究方向，第二步根据用户回复进行深入研究并生成报告。详细流程和响应结构参见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

> **注意**：该模型仅支持华北2（北京）地域，且当前仅支持 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。

**关键参数：**

- `output_format`：控制报告详细程度，`model_detailed_report`（默认，约 6000 Token）或 `model_summary_report`（约 1500-2000 Token）

**响应阶段：** 流式响应包含 `ResearchPlanning`（研究规划）、`WebResearch`（网络搜索）、`KeepAlive`（连接保持）、`answer`（回答）四个阶段，通过 `phase` 字段区分。

## Qwen-OCR 文字提取模型

Qwen-OCR 对图片进行文字提取和结构化识别，支持自定义 Prompt 指定提取格式。调用方式与视觉模型类似，通过 `image_url` 传入图片。详细参数参见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

**关键参数：**

- `min_pixels` / `max_pixels`：控制输入图像的像素阈值，影响识别精度
- `text`：自定义 Prompt，不传则使用默认提取模式

**多地域支持：** 北京、新加坡、美国（弗吉尼亚）三个地域可用。

## 文本排序模型

文本排序模型对召回文档进行二次精准排序，提升检索应用的准确率。详细的模型对比和 API 规范参见 [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)。

> **注意**：gte-rerank 模型将于 2026 年 05 月 30 日下线，推荐使用 qwen3-rerank 模型替代。

**模型选择：**

| 模型 | 最大文档数 | 单条最大 Token | 特色 |
|------|-----------|---------------|------|
| qwen3-rerank | 500 | 4,000 | 纯文本排序，支持 100+ 语种 |
| qwen3-vl-rerank | 文本 100 / 图片 40 / 视频 4 | 8,000 | 多模态排序，支持图片和视频 |
| gte-rerank-v2 | — | — | 50+ 语种（即将下线） |

**关键参数：**

- `query`：查询内容，qwen3-vl-rerank 支持文本或图片查询
- `documents`：待排序文档列表，qwen3-vl-rerank 支持文本、图片、视频混合
- `top_n`：返回前 N 个最相关文档
- `instruct`：自定义排序策略说明（仅 qwen3-rerank 和 qwen3-vl-rerank）

> **注意**：qwen3-rerank 使用的 API 端点 (`/compatible-api/v1/reranks`) 与 qwen3-vl-rerank / gte-rerank-v2 使用的端点 (`/api/v1/services/rerank/text-rerank/text-rerank`) 不同，请求体和响应格式也有差异。

## 意图理解模型

tongyi-intent-detect-v3 能在百毫秒级时间内解析用户意图并选择合适的工具。详细的 System Message 设置方式参见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

**三种使用模式：**

1. **意图 + 函数调用**：在 System Message 中加入工具描述和 `Response in INTENT_MODE.`，模型返回包含 `<tags>`、`<tool_call>`、`<content>` 的结构化响应
2. **仅意图分类**：在 System Message 中提供意图标签列表和 `Just reply with the chosen tag.`
3. **仅函数调用**：标准 Function Calling 模式

**提速技巧：** 用单个大写字母代替意图名称，使模型输出始终为一个 Token，可显著优化响应时间。

**计费：** 输入 0.4 元/百万 Token，输出 1 元/百万 Token，新用户有 100 万 Token 免费额度（90 天有效）。

## 通义法睿法律模型

farui-plus 是基于千问训练的法律行业大模型，支持法律咨询、文书生成、争议焦点识别等场景，上下文长度 12K Token。详细的调用示例参见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

**使用方式：** 通过 DashScope SDK（Python / Java）调用，支持单轮对话、多轮对话和[流式输出](../concepts/streaming-output.md)。调用方式与通用大模型一致，将 `model` 参数设为 `farui-plus` 即可。

**计费：** 输入 20 元/百万 Token（仅列出输入成本）。

## 通用调用前提

所有模型调用前需要：

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并 [配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
2. 如使用 SDK，需先 [安装对应 SDK](https://help.aliyun.com/zh/model-studio/install-sdk)
3. 不同地域使用不同的 API Key 和 `base_url`，注意区分

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)



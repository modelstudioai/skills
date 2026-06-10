# [more](more.md) models

本页汇总百炼平台中三类“非通用聊天”补充模型 API：用于检索召回二次精排的**文本/多模态排序模型**、用于路由与[函数调用](../concepts/function-calling.md)的**意图理解模型**、以及面向法律垂直行业的**通义法睿大模型**。它们各自有独立的接入端点与参数结构，开发者按业务场景选用即可。

## 支持的模型一览

| 类别 | 模型 | 上下文 / 输入限制 | 主要用途 | 详细文档 |
| --- | --- | --- | --- | --- |
| 排序 | `qwen3-rerank` | 单条 ≤ 4,000 Token；单次 ≤ 500 文档；总输入 ≤ 30,000 Token | 文本语义检索、RAG | [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md) |
| 排序 | `qwen3-vl-rerank` | 单条 ≤ 8,000 Token；单次 ≤ 100 文本 / 40 图片 / 4 视频；总输入 ≤ 120,000 Token | 跨模态搜索、图像聚类、图片检索 | [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md) |
| 排序 | `gte-rerank-v2` | 单条 ≤ 4,000 Token；总输入 ≤ 30,000 Token | 通用文本精排（50+ 语种） | [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md) |
| 意图 | `tongyi-intent-detect-v3` | 上下文 8,192 Token；最大输出 1,024 Token | 意图识别、[函数调用](../concepts/function-calling.md)路由 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| 法律 | `farui-plus` | 上下文 12k Token；最大输出 2k Token | 法律咨询、文书生成、争议焦点识别 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |

> **注意**：根据 [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md) 中的公告，`gte-rerank` 将于 **2026-05-30 下线**，新接入请改用 `qwen3-rerank`。`gte-rerank-v2` 暂不受影响。

## 一、文本 / 多模态排序模型

排序模型用于在“召回 → 精排”两阶段检索流水线中，对召回结果做二次精排，把与 Query 最相关的文档顶到前面。

### 接入端点

不同模型走不同接口（详见 [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)）：

- `qwen3-rerank` → `POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`（OpenAI 兼容风格，参数 **扁平化**，不需要 `input`/`parameters` 嵌套）
- `qwen3-vl-rerank` / `gte-rerank-v2` → `POST https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`（DashScope 原生风格，参数走 `input` + `parameters` 嵌套）

> **注意**：同一份代码不能在两个端点间直接复用，请求体结构与响应字段位置都不同（例如 `qwen3-rerank` 的 `results` 在响应顶层，其它两个模型在 `output.results` 下）。

### 关键参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 必填，取上表中的模型名 |
| `query` | string / object | 必填。`qwen3-vl-rerank` 支持 `{"text": ...}` 或 `{"image": ...}` 两种模态对象 |
| `documents` | array | 必填。`qwen3-vl-rerank` 元素可为 `{"text"/"image"/"video": ...}`；视频只支持 URL，图片支持 URL 或 `data:image/{format};base64,{data}` |
| `top_n` | int | 可选，返回前 N 条；超过总数则返回全部 |
| `return_documents` | bool | 可选，是否回传文档原文。仅 `gte-rerank-v2` 和 `qwen3-vl-rerank` 支持；`qwen3-rerank` 不支持 |
| `instruct` | string | 可选，自定义排序任务指令（如问答检索 vs. 语义相似度）。仅 `qwen3-rerank` / `qwen3-vl-rerank` 生效，建议英文撰写 |
| `fps` | float | 可选，视频抽帧比例 0–1，默认 1.0。仅 `qwen3-vl-rerank` |

### 限制与注意

- 单条 Query / Document 超过 Token 上限会被**截断**后再计算，可能导致排序结果不准。
- 总输入 Token 计算公式：`Query Tokens × Document 数量 + Document Tokens 总和`，不得超过模型的“请求最大输入 Token”。
- `relevance_score` 取值 0.0–1.0，**只是本次请求内的相对分数**，不能跨请求比较。
- 多模态文档的图片支持 JPEG/PNG/WEBP/BMP/TIFF/ICO/DIB/ICNS/SGI，视频仅支持 MP4/AVI/MOV。

## 二、意图理解模型 `tongyi-intent-detect-v3`

意图理解模型可在百毫秒级内解析用户意图并选择工具，常用于路由层（替代“先让通用大模型识别意图”的高成本写法）。

### 三种工作模式（由 System Message 决定）

依据 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)，通过不同的 System Message 模板切换：

1. **同时输出意图与[函数调用](../concepts/function-calling.md)**：System Message 末尾加 `Response in INTENT_MODE.`，并把工具 JSON Schema 列表注入 System。响应是 `<tags>...</tags><tool_call>...</tool_call><content>...</content>` 三段式文本，需要用正则解析（文档给出了 `parse_text` 参考实现）。
2. **只输出意图标签**：System Message 提供 `{"意图key": "意图描述"}` 字典，要求 `Just reply with the chosen tag.`，模型只返回选中的 key。
3. **只输出[函数调用](../concepts/function-calling.md)信息**：与模式 1 类似但只回工具调用部分。

### 调用方式

- **OpenAI 兼容**：`base_url=https://dashscope.aliyuncs.com/compatible-mode/v1`，使用 `client.chat.completions.create(model="tongyi-intent-detect-v3", ...)`。
- **DashScope 原生**：`dashscope.Generation.call(model="tongyi-intent-detect-v3", messages=..., result_format="message")`。

### 性能优化技巧

为压缩响应延迟，可以把意图标签**用单大写字母（A/B/C/...）指代**，模型输出会被压缩为 1 个 Token，显著降低响应时间。这一技巧仅对“只输出意图标签”模式有效。

### 配额与计费

`tongyi-intent-detect-v3` 上下文 8,192 Token、最大输入 8,192、最大输出 1,024；输入 0.4 元/百万 Token、输出 1 元/百万 Token；开通后 90 天内享 100 万 Token 免费额度。

## 三、通义法睿大模型 `farui-plus`

通义法睿是基于千问、用法律行业数据继续训练的垂直大模型，覆盖法律咨询、推理法律适用、推荐裁判类案、辅助案情分析、生成法律文书、检索法律知识、合同条款审查等场景。

### 接入方式

仅通过 DashScope SDK 调用（参见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)），支持 Python 与 Java：

- **单轮对话**：`dashscope.Generation.call(model="farui-plus", messages=..., result_format="message")`。
- **多轮对话**：把上一轮 `assistant` 响应追加进 `messages` 列表继续 `call`。
- **[流式输出](../concepts/streaming.md)**：Python 设 `stream=True, incremental_output=True`；Java 使用 `gen.streamCall(param)`。

> **注意**：DashScope Java SDK 中 `Generation` 等请求对象**不是线程安全**的，复用时需自行加锁或及时关闭，避免并发问题。

### 关键参数与限制

- 上下文 12k Token，最大输入 12k、最大输出 2k。
- 输出成本 20 元/百万 Token（文档未单列输入成本，按输出价计费部分以官方计费页为准）。
- 限流规则参见百炼平台“限流”页面，未在 API 文档中单列。

## 通用约定

无论使用哪一类模型，都需要先完成两步前置：

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量 `DASHSCOPE_API_KEY`。
2. SDK 调用前安装对应语言的 DashScope SDK（Python / Java）。

所有失败响应都通过顶层 `code` + `message` 指明出错原因，详细错误码与限流规则统一参考百炼平台“错误码”与“限流”文档。

## 来源文档

- [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)







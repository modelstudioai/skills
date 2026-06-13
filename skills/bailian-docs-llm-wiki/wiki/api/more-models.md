# [more](more.md) models

百炼平台除了主流的通义千问系列大语言模型外，还提供多个面向特定场景的专用模型，包括机器翻译（Qwen-MT）、深度研究（Qwen-Deep-Research）、文本/多模态排序（qwen3-rerank / qwen3-vl-rerank）、意图理解（tongyi-intent-detect）以及法律领域（通义法睿）。这些模型均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope API 调用，开发者可根据业务场景按需选用。

## 模型一览

| 模型 | 用途 | 调用接口 | 关键限制 |
|------|------|----------|----------|
| qwen-mt-turbo / qwen-mt-plus | 机器翻译，支持术语干预、翻译记忆、领域提示 | OpenAI 兼容 | 通过 `translation_options` 传递翻译参数 |
| qwen-deep-research | 深度研究，两阶段（反问确认 + 深入研究） | DashScope（仅 Python SDK） | 仅支持华北2（北京）地域 |
| qwen3-rerank | 文本语义排序，RAG 场景 | HTTP / DashScope SDK | 最大 500 条文档，单条 4,000 Token |
| qwen3-vl-rerank | 多模态排序（文本+图片+视频） | HTTP / DashScope SDK | 文本 100 条、图片 40 条、视频 4 条 |
| gte-rerank-v2 | 文本排序（多语种） | HTTP / DashScope SDK | 已计划下线，推荐迁移到 qwen3-rerank |
| tongyi-intent-detect-v3 | 百毫秒级意图识别 + 工具选择 | OpenAI 兼容 / DashScope | 上下文 8,192 Token，输出 1,024 Token |
| farui-plus | 法律咨询、文书生成、案情分析 | DashScope SDK | 上下文 12k Token，输出 2k Token |

## Qwen-MT 翻译模型

Qwen-MT 通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，核心参数放在 `extra_body.translation_options` 中。详细参数说明参见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。

### 基本调用

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
    extra_body={
        "translation_options": {
            "source_lang": "Chinese",
            "target_lang": "English"
        }
    }
)
```

### 高级功能

- **术语干预**：在 `translation_options.terms` 中指定源语言词汇与目标译文的映射列表，确保专业术语翻译一致性。
- **翻译记忆**：通过 `translation_options.tm_list` 提供历史翻译对照，提升同领域文档翻译质量。
- **领域提示**：通过 `translation_options.domains` 传入领域描述文本，引导模型采用特定领域的翻译风格。

### 多地域支持

Qwen-MT 支持北京、新加坡、美国（弗吉尼亚）三个地域，不同地域使用不同的 `base_url` 和 API Key：

| 地域 | base_url |
|------|----------|
| 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

## Qwen-Deep-Research 深度研究

Qwen-Deep-Research 采用两阶段调用流程，详细 API 参数参见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

### 调用流程

1. **第一步（反问确认）**：发送研究主题，模型返回澄清式问题帮助聚焦方向。
2. **第二步（深入研究）**：将第一步的模型回复作为 `assistant` 消息，加上用户回答，发起正式研究请求。

```python
import dashscope

# 第一步
messages = [{"role": "user", "content": "研究一下人工智能在教育中的应用"}]
responses = dashscope.Generation.call(
    model="qwen-deep-research", messages=messages, stream=True
)

# 收集反问内容后进入第二步
messages.append({"role": "assistant", "content": step1_content})
messages.append({"role": "user", "content": "我主要关注个性化学习方面"})
responses = dashscope.Generation.call(
    model="qwen-deep-research", messages=messages
)
```

### 响应阶段

流式响应中通过 `phase` 字段标识当前阶段：

- `ResearchPlanning` -- 研究规划
- `WebResearch` -- 网络搜索（包含搜索查询和引用来源）
- `KeepAlive` -- 连接保持
- `answer` -- 最终回答（包含 `references` 引用列表）

可通过 `output_format` 参数控制报告详细程度：`model_detailed_report`（约 6,000 Token）或 `model_summary_report`（约 1,500-2,000 Token）。

> **注意**：该模型仅支持华北2（北京）地域，且当前仅支持 Python DashScope SDK，不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。

## 文本排序模型

排序模型（Rerank）用于对检索召回的文档进行二次精排，提升 RAG 等应用的准确率。详细参数参见 [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)。

### 接口差异

不同模型使用不同的 API 端点：

- **qwen3-rerank**：`POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`，请求体中 `query`、`documents` 与 `model` 同级。
- **qwen3-vl-rerank / gte-rerank-v2**：`POST https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`，使用嵌套的 `input` 和 `parameters` 结构。

### 基本调用（qwen3-rerank）

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-rerank",
    "query": "什么是文本排序模型",
    "documents": [
      "文本排序模型广泛用于搜索引擎和推荐系统中",
      "量子计算是计算科学的一个前沿领域",
      "预训练语言模型的发展给文本排序模型带来了新的进展"
    ],
    "top_n": 2
  }'
```

### 多模态排序（qwen3-vl-rerank）

qwen3-vl-rerank 支持文本、图片、视频三种模态的混合排序。查询可以是文本或图片，文档可以是文本、图片（URL 或 Base64）或视频（仅 URL）。通过 `fps` 参数控制视频抽帧密度。

### 自定义排序策略

通过 `instruct` 参数可指定排序任务类型：

- 问答检索（默认）：`"Given a web search query, retrieve relevant passages that answer the query."`
- 语义相似度：`"Retrieve semantically similar text."`

> **注意**：gte-rerank 模型已计划下线，建议迁移到 qwen3-rerank。`relevance_score` 为当前请求内的相对分数，不可跨请求比较。

## 意图理解模型

tongyi-intent-detect-v3 能在百毫秒级延迟内完成意图识别和工具选择，适用于需要快速响应的对话系统。详细参数与用法参见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

### 三种工作模式

1. **意图 + 函数调用**：在 System Message 中添加工具定义并附加 `Response in INTENT_MODE.`，模型返回 `<tags>`、`<tool_call>`、`<content>` 三段结构。
2. **仅意图分类**：在 System Message 中提供意图标签字典，模型直接返回匹配的标签名。
3. **仅函数调用**：标准 function calling 模式。

### 响应解析

意图+函数调用模式的响应需要用正则解析：

```python
import re, json

def parse_text(text):
    tags = re.search(r'<tags>(.*?)</tags>', text, re.DOTALL)
    tool_call = re.search(r'<tool_call>(.*?)</tool_call>', text, re.DOTALL)
    content = re.search(r'<content>(.*?)</content>', text, re.DOTALL)
    return {
        "tags": tags.group(1).strip() if tags else "",
        "tool_call": json.loads(tool_call.group(1).strip()) if tool_call else [],
        "content": content.group(1).strip() if content else ""
    }
```

### 性能优化

将意图分类标签用单个大写字母（A、B、C...）代替完整名称，可使模型始终返回单个 Token，进一步降低响应延迟。

## 通义法睿法律模型

farui-plus 是基于千问、经法律行业数据专门训练的法律大模型，支持法律咨询、起诉书/合同生成、案情分析等场景。详细用法参见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

### 调用方式

通义法睿通过 DashScope SDK 调用（Python / Java），支持单轮对话、多轮对话和[流式输出](../concepts/streaming.md)：

```python
import dashscope

response = dashscope.Generation.call(
    model="farui-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}
    ],
    result_format="message"
)
```

### 计费

输入成本 20 元/百万 Token，上下文长度 12k Token，最大输出 2k Token。

## 通用注意事项

- 所有模型调用前需 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量 `DASHSCOPE_API_KEY`。
- 不同地域的 API Key 不通用，需分别申请。
- 模型限流条件参见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)，错误码参见 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。
- SDK 调用时参数命名与 HTTP 接口基本一致，但结构有所封装（如 HTTP 使用嵌套的 `input`/`parameters`，SDK 使用扁平参数），开发时注意区分。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)




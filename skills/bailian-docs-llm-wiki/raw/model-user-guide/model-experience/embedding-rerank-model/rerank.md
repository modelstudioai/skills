# 重排序

检索系统优先保证速度，因此结果的精确度可能不够理想。重排序模型对检索到的文档重新打分，将最相关的结果排在前面，显著提升搜索精度。

> **说明**
>
> **重排序最能发挥价值的场景：**当初始检索返回 20-100+ 个相关度参差不齐的候选结果时，重排序的精度提升最为显著。如果检索已返回高度相关的结果（如精确关键词匹配），则重排序的价值较小。典型的 RAG 流程：先通过 Embedding 检索 50-100 个候选结果，再通过重排序筛选 Top 5-10，最后传入大语言模型。

<a id="前提条件"></a>

<a id="rr05a2b3c4d5e"></a>

## 前提条件

请先[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需使用 SDK，请[安装SDK](../../../model-api-reference/preparations/install-sdk.md)。

<a id="重排序文档"></a>

<a id="rr08a2b3c4d5e"></a>

## 重排序文档

将查询和候选文档列表传给 API，模型将按相关性对文档进行排序后返回。

<a id="文本重排序-qwen3-rerank"></a>

<a id="rr526txt02"></a>

### 文本重排序（qwen3-rerank）

<a id="sec-tabs"></a>

<a id="openai-兼容"></a>

<a id="openai-兼容-h4"></a>

#### OpenAI 兼容

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1",
)

results = client.post(
  "/reranks",
  body={
    "model": "qwen3-rerank",
    "query": "什么是重排序模型",
    "documents": [
      "重排序模型广泛应用于搜索引擎和推荐系统，按相关性对候选文本进行排序",
      "量子计算是计算科学的前沿领域",
      "预训练语言模型的发展为重排序模型带来了新的进展"
    ],
    "top_n": 2
  },
  cast_to=object
)

print(results)
```

<a id="fig-code-group-javascript-tab"></a>

javascript

<a id="code-code-group-javascript"></a>

```javascript
const OpenAI = require("openai");

const openai = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1",
});

async function rerank() {
  const results = await openai.post("/reranks", {
    body: {
      model: "qwen3-rerank",
      query: "什么是重排序模型",
      documents: [
        "重排序模型广泛应用于搜索引擎和推荐系统，按相关性对候选文本进行排序",
        "量子计算是计算科学的前沿领域",
        "预训练语言模型的发展为重排序模型带来了新的进展",
      ],
      top_n: 2,
    },
  });

  console.log(JSON.stringify(results, null, 2));
}

rerank();
```

<a id="fig-code-group-bash-tab"></a>

bash

<a id="code-code-group-bash"></a>

```bash
curl --request POST \
  --url https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen3-rerank",
    "query": "什么是重排序模型",
    "documents": [
      "重排序模型广泛应用于搜索引擎和推荐系统，按相关性对候选文本进行排序",
      "量子计算是计算科学的前沿领域",
      "预训练语言模型的发展为重排序模型带来了新的进展"
    ],
    "top_n": 2
}'
```

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

python

<a id="code-code-group-2-python"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
  # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
  # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  workspace="{WorkspaceId}",
  region="cn-beijing",
)

resp = client.rerank.create(
  model="qwen3-rerank",
  query="什么是重排序模型",
  documents=[
    "重排序模型广泛应用于搜索引擎和推荐系统，按相关性对候选文本进行排序",
    "量子计算是计算科学的前沿领域",
    "预训练语言模型的发展为重排序模型带来了新的进展"
  ],
  top_n=2,
  return_documents=True
)

print(resp)
```

<a id="fig-code-group-2-bash-tab"></a>

bash

<a id="code-code-group-2-bash"></a>

```bash
curl --request POST \
  --url https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen3-rerank",
    "input": {
      "query": "什么是重排序模型",
      "documents": [
        "重排序模型广泛应用于搜索引擎和推荐系统，按相关性对候选文本进行排序",
        "量子计算是计算科学的前沿领域",
        "预训练语言模型的发展为重排序模型带来了新的进展"
      ]
    },
    "parameters": {
      "top_n": 2,
      "return_documents": true
    }
}'
```

<a id="多模态重排序-qwen3-vl-rerank"></a>

<a id="rr526vl02"></a>

### 多模态重排序（qwen3-vl-rerank）

`qwen3-vl-rerank` 支持文本、图片和视频的混合排序。查询可以是文本或图片，文档可以包含文本、图片和视频。

> **说明**
>
> 多模态重排序需要使用 DashScope SDK 或 API，不支持 OpenAI 兼容接口。

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-python-tab"></a>

Python

<a id="code-code-group-3-python"></a>

```python
import os
import dashscope
import json

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
  # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
  # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  workspace="{WorkspaceId}",
  region="cn-beijing",
)

resp = client.rerank.create(
  model="qwen3-vl-rerank",
  query={"text": "什么是文本排序模型"},
  documents=[
    {"text": "文本排序模型广泛用于搜索引擎和推荐系统中"},
    {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
    {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"}
  ],
  top_n=2,
  return_documents=True
)

print(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
```

<a id="fig-code-group-3-curl-tab"></a>

curl

<a id="code-code-group-3-curl"></a>

```bash
curl --request POST \
  --url https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen3-vl-rerank",
    "input": {
      "query": {"text": "什么是文本排序模型"},
      "documents": [
        {"text": "文本排序模型广泛用于搜索引擎和推荐系统中"},
        {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
        {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"}
      ]
    },
    "parameters": {
      "return_documents": true,
      "top_n": 2,
      "fps": 1.0
    }
}'
```

<a id="核心功能"></a>

<a id="rr23a2b3c4d5e"></a>

## 核心功能

<a id="使用指令提升排序效果-instruct"></a>

<a id="rr25a2b3c4d5e"></a>

### 使用指令提升排序效果（instruct）

`instruct` 参数可以引导模型使用不同的排序策略。请使用英文编写指令。

-   **问答检索（默认）**：`"Given a web search query, retrieve relevant passages that answer the query."`
    
    侧重于寻找答案。对于查询"如何预防感冒？"，"勤洗手可预防感冒"的分数会高于"感冒是一种常见病"（主题相关但未回答问题）。
    
-   **语义相似度**：`"Retrieve semantically similar text."`
    
    侧重于语义等价，不受措辞影响。例如："如何修改密码？"可匹配"忘记密码怎么办？"（FAQ 场景）。
    

未设置时，模型默认使用问答检索策略。

<a id="fig-code-group-4"></a>

<a id="fig-code-group-4-openai-兼容-tab"></a>

OpenAI 兼容

<a id="code-code-group-4-openai-兼容"></a>

```bash
curl --request POST \
  --url https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen3-rerank",
    "query": "如何修改密码？",
    "documents": [
      "点击设置 > 安全 > 修改密码即可更新凭据",
      "忘记密码怎么办？",
      "我们的平台支持双因素认证"
    ],
    "instruct": "Retrieve semantically similar text."
}'
```

<a id="fig-code-group-4-dashscope-tab"></a>

DashScope

<a id="code-code-group-4-dashscope"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
  # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
  # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  workspace="{WorkspaceId}",
  region="cn-beijing",
)

resp = client.rerank.create(
  model="qwen3-rerank",
  query="如何修改密码？",
  documents=[
    "点击设置 > 安全 > 修改密码即可更新凭据",
    "忘记密码怎么办？",
    "我们的平台支持双因素认证"
  ],
  instruct="Retrieve semantically similar text."
)

print(resp)
```

<a id="返回前-n-个结果-top-n"></a>

<a id="rr43a2b3c4d5e"></a>

### 返回前 N 个结果（top\_n）

使用 `top_n` 仅返回排名最高的文档。如未设置，则返回按相关性排序的所有文档。如果 `top_n` 超过文档总数，则返回所有文档。

<a id="模型概览"></a>

<a id="rr46a2b3c4d5e"></a>

## 模型概览

> **重要**
>
> gte-rerank模型将于2026年05月30日下线，推荐使用qwen3-rerank模型替代。详情请参见[官网公告](https://www.aliyun.com/notice/118217)。

| 模型 | 最大文档数 | 单条最大 Token 数 | 单次请求最大 Token 数 | 支持语言 | 适用场景 |
| --- | --- | --- | --- | --- | --- |
| qwen3.7-text-rerank | 500 | 30,000 | 120,000（建议） | 201 种主流语种与方言：中文、英文、西班牙语、法语等 | 语义文本搜索、RAG 应用 |
| qwen3-vl-rerank | 文本：100<br><br>图片：40<br><br>视频：4 | 8,000 | 120,000 | 中文、英文、日语、韩语等 33 种语言 | 多模态搜索结果重排序（文本、图片、视频） |
| qwen3-rerank | 500 | 4,000 | 120,000 | 100+ 语言：中文、英文、西班牙语、法语等 | 语义文本搜索、RAG 应用 |
| gte-rerank-v2 | 500 | 4,000 | 30,000 | 50+ 语言：中文、英文、日语、韩语、泰语等 | 语义文本搜索、RAG 应用 |

**关键术语：**

-   **单条最大 Token 数**：单条查询或文档的最大 Token 数。单条查询或文档的输入超过该限制时，API 会返回 HTTP 400 错误，不会截断输入内容。
-   **单次请求最大文档数**：单次请求允许的最大文档数量。对于 qwen3-vl-rerank 模型，该限制会根据文档类型（文本、图片、视频、混合模态）的不同而有所差异。
-   **单次请求最大 Token 数**：计算公式为 `查询 Token 数 x 文档数量 + 所有文档 Token 总数`，该值不能超过单次请求上限。

<a id="api-参考"></a>

<a id="rr91a2b3c4d5e"></a>

## API 参考

参见[排序模型（Rerank）](../../../model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

<a id="错误码"></a>

<a id="rr94a2b3c4d5e"></a>

## 错误码

如果调用失败，请参见[错误码](../../../model-api-reference/preparations/error-code.md)。

<a id="限流"></a>

<a id="rr97a2b3c4d5e"></a>

## 限流

请参见[限流](../../get-started-with-models/rate-limit.md)。

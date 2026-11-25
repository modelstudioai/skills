# 知识检索

大模型无法回答私有领域问题。知识检索工具可从知识库中检索内容并提供给大模型，使其生成更准确、专业的回答。

<a id="前提条件"></a>

<a id="w4x6y8z0a2b3c"></a>

## 前提条件

1.  已[获取与配置 API Key](../../../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
2.  已创建知识库并获取知识库 ID。可通过以下方式创建知识库：
    
    -   **控制台创建**：在[百炼控制台](https://bailian.console.aliyun.com/rag/knowledge)的知识库页面创建知识库。详细步骤请参考[创建和使用知识库](../../../../application-user-guide/knowledge-base/rag-knowledge-base.md)。
        
    -   **API 创建**：通过阿里云百炼 SDK 调用 API 创建知识库。详细步骤请参考[知识库API指南](../../../../application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
        
        > 通过 API 创建知识库前，需要先在[百炼控制台](https://bailian.console.aliyun.com/settings/workspace)获取业务空间 ID（workspace\_id）。仅支持两类知识库：文档搜索和数据查询；适用于基础文档问答，不支持图文并茂回复。
        
    
    知识库 ID 可在[百炼控制台](https://bailian.console.aliyun.com/rag/knowledge)的知识库详情页中查看。
    

<a id="使用方式"></a>

<a id="b3c5d7e9f1g2h"></a>

## 使用方式

知识检索功能通过 Responses API 调用。在 `tools` 参数中添加 `file_search` 工具，并通过 `vector_store_ids` 参数指定要检索的知识库 ID。

> 使用前需先[创建和使用知识库](../../../../application-user-guide/knowledge-base/rag-knowledge-base.md)并获取知识库 ID。当前 `vector_store_ids` 仅支持传入一个知识库 ID。

<a id="code-block"></a>

```python
# 此处省略依赖导入与创建客户端步骤，完整可运行代码请参见下文「快速开始」
response = client.responses.create(
    model="qwen3.8-max",
    input="介绍一下阿里云百炼X1手机",
    tools=[
        {
            "type": "file_search",
            # 替换为您的知识库 ID，当前仅支持一个
            "vector_store_ids": ["your_knowledge_base_id"]
        }
    ]
)

print(response.output_text)
```

<a id="支持的模型"></a>

<a id="k2l4m6n8o0p1q"></a>

## 支持的模型

-   千问Max：qwen4-max、Qwen3.8-Max系列、Qwen3.7-Max系列
-   千问Plus：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列
-   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列
-   Qwen3.8开源系列
-   Qwen3.6开源系列（qwen3.6-27b除外）
-   Qwen3.5开源系列

仅支持通过 Responses API 调用。

<a id="快速开始"></a>

<a id="v9w1x3y5z7a8b"></a>

## 快速开始

运行以下代码，通过 Responses API 调用知识检索工具，在指定的知识库中检索相关内容并生成回答。

> 请将示例代码中的 `vector_store_ids` 替换为您实际的知识库 ID。

> **警告**
>
> 请确保传入有效的知识库 ID。如果传入空数组或无效的知识库 ID，知识检索工具将不会生效，模型会直接使用自身知识回答，且不会返回错误提示。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.responses.create(
    model="qwen3.8-max",
    input="介绍一下阿里云百炼X1手机",
    tools=[
        {
            "type": "file_search",
            # 替换为您的知识库 ID，当前仅支持一个
            "vector_store_ids": ["your_knowledge_base_id"]
        }
    ]
)

print("[模型回复]")
print(response.output_text)
print(f"\n[Token 用量] 输入: {response.usage.input_tokens}, 输出: {response.usage.output_tokens}, 合计: {response.usage.total_tokens}")
```

<a id="fig-code-group-javascript-tab"></a>

javascript

<a id="code-code-group-javascript"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.create({
        model: "qwen3.8-max",
        input: "介绍一下阿里云百炼X1手机",
        tools: [
            {
                type: "file_search",
                // 替换为您的知识库 ID，当前仅支持一个
                vector_store_ids: ["your_knowledge_base_id"]
            }
        ]
    });

    console.log("[模型回复]");
    console.log(response.output_text);

    const usage = response.usage;
    console.log(`\n[Token 用量] 输入: ${usage.input_tokens}, 输出: ${usage.output_tokens}, 合计: ${usage.total_tokens}`);
}

main();
```

<a id="fig-code-group-bash-tab"></a>

bash

<a id="code-code-group-bash"></a>

```bash
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "介绍一下阿里云百炼X1手机",
    "tools": [
        {
            "type": "file_search",
            "vector_store_ids": ["your_knowledge_base_id"]
        }
    ]
}'
```

运行以上代码可获取如下回复：

<a id="code-block-2"></a>

```text
[模型回复]
根据知识库中的内容，该产品要点包括以下几个方面：

1. **核心功能**：产品提供了...
2. **适用场景**：适用于...
3. **技术特性**：基于...

...

[Token 用量] 输入: 1568, 输出: 1724, 合计: 3292
```

<a id="流式输出"></a>

<a id="k4l6m8n0o2p3q"></a>

## 流式输出

知识检索工具需要在知识库中进行语义搜索，可能需要一定的处理时间，建议启用流式输出，实时获取中间过程输出结果。

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

python

<a id="code-code-group-2-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

stream = client.responses.create(
    model="qwen3.8-max",
    input="介绍一下阿里云百炼X1手机",
    tools=[
        {
            "type": "file_search",
            # 替换为您的知识库 ID，当前仅支持一个
            "vector_store_ids": ["your_knowledge_base_id"]
        }
    ],
    stream=True
)

for event in stream:
    # 模型回复开始
    if event.type == "response.content_part.added":
        print("[模型回复]")
    # 流式打印模型回复
    elif event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    # 响应完成，打印 Token 用量
    elif event.type == "response.completed":
        usage = event.response.usage
        print(f"\n\n[Token 用量] 输入: {usage.input_tokens}, 输出: {usage.output_tokens}, 合计: {usage.total_tokens}")
```

<a id="fig-code-group-2-javascript-tab"></a>

javascript

<a id="code-code-group-2-javascript"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const stream = await openai.responses.create({
        model: "qwen3.8-max",
        input: "介绍一下阿里云百炼X1手机",
        tools: [
            {
                type: "file_search",
                // 替换为您的知识库 ID，当前仅支持一个
                vector_store_ids: ["your_knowledge_base_id"]
            }
        ],
        stream: true
    });

    for await (const event of stream) {
        // 模型回复开始
        if (event.type === "response.content_part.added") {
            console.log("[模型回复]");
        }
        // 流式打印模型回复
        else if (event.type === "response.output_text.delta") {
            process.stdout.write(event.delta);
        }
        // 响应完成，打印 Token 用量
        else if (event.type === "response.completed") {
            const usage = event.response.usage;
            console.log(`\n\n[Token 用量] 输入: ${usage.input_tokens}, 输出: ${usage.output_tokens}, 合计: ${usage.total_tokens}`);
        }
    }
}

main();
```

<a id="fig-code-group-2-bash-tab"></a>

bash

<a id="code-code-group-2-bash"></a>

```bash
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "介绍一下阿里云百炼X1手机",
    "tools": [
        {
            "type": "file_search",
            "vector_store_ids": ["your_knowledge_base_id"]
        }
    ],
    "stream": true
}'
```

<a id="参数说明"></a>

<a id="v5w7x9y1z3a4b"></a>

## 参数说明

`file_search` 工具支持以下参数：

<table><thead><tr><th><strong>参数</strong></th><th><strong>必填</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>type</code></p></td><td><p>是</p></td><td><p>固定为 <code>&quot;file_search&quot;</code>。</p></td></tr><tr><td><p><code>vector_store_ids</code></p></td><td><p>是</p></td><td><p>知识库 ID 列表。当前仅支持传入<strong>一个</strong>知识库 ID。知识库 ID 可在<a href="https://bailian.console.aliyun.com/rag/knowledge">百炼控制台</a>的知识库详情页查看，也可通过 API 创建知识库时获取。</p><blockquote><p>请确保传入有效的知识库 ID。如果传入空数组或无效的知识库 ID，知识检索工具将不会生效，模型会直接使用自身知识回答，且不会返回错误提示。</p></blockquote></td></tr></tbody></table>

<a id="计费说明"></a>

<a id="c8d0e2f4g6h7i"></a>

## 计费说明

计费涉及以下方面：

-   **模型调用费用**：知识库检索到的内容会拼接到提示词中，增加模型的输入 Token，按照模型的标准价格计费。价格详情请参考百炼控制台。
-   **工具调用费用**：参见[知识库计费说明](../../../../application-user-guide/agent-billing/billing-for-knowledge-base.md)。

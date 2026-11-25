# PDF理解

PDF理解功能使模型能够解析PDF文档中的文字与图片，通过 Chat Completions、Responses API、DashScope 或 Anthropic 兼容接口进行分析。

<a id="支持的模型"></a>

<a id="pdf-models-h2"></a>

## 支持的模型

qwen4-max、qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash、qwen3.8-27b

qwen3.8-27b 仅支持在北京地域通过 Chat Completions 或 DashScope 调用 PDF 理解。

<a id="快速开始"></a>

<a id="pdf-quickstart-h2"></a>

## 快速开始

运行以下代码，向模型传入PDF文件。

> 需要已[获取与配置 API Key](../../../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="sec-tabs"></a>

<a id="openai-兼容"></a>

<a id="openai-兼容-h4"></a>

#### OpenAI 兼容

<a id="sec-tabs-2"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="pdf-quickstart-oai-python-code-h3"></a>

### 示例代码

<a id="code-block"></a>

```python
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen4-max",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "file",
                    "file": {
                        "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                    }
                },
                {
                    "type": "text",
                    "text": "总结一下这个PDF文档的内容"
                }
            ]
        }
    ],
    stream=True,
    stream_options={"include_usage": True},
    # 需要开启该参数才会在 usage 中返回 x_tools.pdf_page_parser.count（PDF解析页数）
    extra_body={"include_tool_usage": True}
)

for chunk in completion:
    if not chunk.choices:
        print(f"\nUsage: {chunk.usage}")
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "content") and delta.content:
        print(delta.content, end="", flush=True)
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="pdf-quickstart-oai-nodejs-code-h3"></a>

### 示例代码

<a id="code-block-2"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

async function main() {
    const stream = await openai.chat.completions.create({
        model: 'qwen4-max',
        messages: [
            {
                role: 'user',
                content: [
                    {
                        type: 'file',
                        file: {
                            file_url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf'
                        }
                    },
                    {
                        type: 'text',
                        text: '总结一下这个PDF文档的内容'
                    }
                ]
            }
        ],
        stream: true,
        stream_options: { include_usage: true },
        // 需要开启该参数才会在 usage 中返回 x_tools.pdf_page_parser.count（PDF解析页数）
        include_tool_usage: true
    });

    for await (const chunk of stream) {
        if (!chunk.choices?.length) {
            console.log('\nUsage:', chunk.usage);
            continue;
        }
        const delta = chunk.choices[0].delta;
        if (delta.content) {
            process.stdout.write(delta.content);
        }
    }
}

main();
```

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="pdf-quickstart-oai-curl-code-h3"></a>

### 示例代码

<a id="code-block-3"></a>

```bash
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen4-max",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "file",
                    "file": {
                        "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                    }
                },
                {
                    "type": "text",
                    "text": "总结一下这个PDF文档的内容"
                }
            ]
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "include_tool_usage": true
}'
```

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="sec-tabs-3"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

<a id="pdf-quickstart-dashscope-python-code-h3"></a>

### 示例代码

<a id="code-block-4"></a>

```python
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {
                "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
            },
            {
                "text": "总结一下这个PDF文档的内容"
            }
        ]
    }
]

completion = MultiModalConversation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen4-max",
    messages=messages,
    stream=True,
    incremental_output=True
)

for chunk in completion:
    message = chunk.output.choices[0].message
    if message.content:
        print(message.content[0]["text"], end="", flush=True)
```

<a id="http-2"></a>

<a id="http-2-h4"></a>

#### HTTP

<a id="pdf-quickstart-dashscope-curl-code-h3"></a>

### 示例代码

<a id="code-block-5"></a>

```bash
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen4-max",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                    },
                    {
                        "text": "总结一下这个PDF文档的内容"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

<a id="responses-api"></a>

<a id="responses-api-h4"></a>

#### Responses API

Responses API 支持通过 `input_file.file_url` 传入 PDF。qwen3.8-27b 不支持此方式。

以下示例使用北京地域的业务空间专属域名；请替换 `{WorkspaceId}`，并按所选地域及部署范围配置对应的 API Key 和域名，详见[接入信息](../../../get-started-with-models/regions.md)。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    timeout=300.0,
)

response = client.responses.create(
    model="qwen3.8-flash",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_file", "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"},
            {"type": "input_text", "text": "总结这个PDF文档的内容。"},
        ],
    }],
    extra_body={"include_tool_usage": True},
)

print(response.output_text)
```

<a id="fig-code-group-http-tab"></a>

HTTP

<a id="code-code-group-http"></a>

```bash
curl 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-flash",
    "input": [{
      "role": "user",
      "content": [
        {"type": "input_file", "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"},
        {"type": "input_text", "text": "总结这个PDF文档的内容。"}
      ]
    }],
    "include_tool_usage": true
  }'
```

<a id="anthropic"></a>

<a id="anthropic-h4"></a>

#### Anthropic

qwen3.8-max、qwen3.8-flash 及 qwen4 系列模型支持通过 Anthropic 兼容 Messages API 直接传入 PDF 文件 URL。在 `messages[].content` 中使用 `type: "document"` 内容块，将 `source.type` 设置为 `url`，并在 `source.url` 中指定 PDF 文件 URL。

<a id="code-block-6"></a>

```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages' \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $DASHSCOPE_API_KEY" \
  --data '{
    "model": "qwen3.8-max",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [
        {
          "type": "document",
          "source": {
            "type": "url",
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
          }
        },
        {"type": "text", "text": "总结一下这个PDF文档的内容"}
      ]
    }]
  }'
```

完整参数说明见 [Anthropic兼容-Messages](../../../../model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

<a id="使用base64输入"></a>

<a id="pdf-base64-h2"></a>

## 使用Base64输入

如果无法提供文件的URL地址，也可以将PDF文件以Base64编码字符串的形式传入。使用 `file_data` 时，`filename` 字段为必填项。

> **说明**
>
> Base64 编码会使数据体积增大约 1/3，例如 150MB 的文件编码后约 200MB，会超出请求体大小上限。大文件请改用 URL 方式传入。

<a id="sec-tabs-4"></a>

<a id="chat-completions-dashscope"></a>

<a id="chat-completions-dashscope-h4"></a>

#### Chat Completions / DashScope

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-openai-兼容-tab"></a>

OpenAI 兼容

<a id="code-code-group-2-openai-兼容"></a>

```python
import base64
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 读取并编码PDF文件
with open("report.pdf", "rb") as f:
    pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

completion = client.chat.completions.create(
    model="qwen4-max",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "file",
                    "file": {
                        "file_data": f"data:application/pdf;base64,{pdf_base64}",
                        "filename": "report.pdf"
                    }
                },
                {
                    "type": "text",
                    "text": "这份报告的核心结论是什么？"
                }
            ]
        }
    ]
)

print(completion.choices[0].message.content)
```

<a id="fig-code-group-2-dashscope-tab"></a>

DashScope

<a id="code-code-group-2-dashscope"></a>

```python
import base64
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 读取并编码PDF文件
with open("report.pdf", "rb") as f:
    pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

messages = [
    {
        "role": "user",
        "content": [
            {
                "file_data": f"data:application/pdf;base64,{pdf_base64}",
                "filename": "report.pdf"
            },
            {
                "text": "这份报告的核心结论是什么？"
            }
        ]
    }
]

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen4-max",
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

<a id="anthropic-2"></a>

<a id="anthropic-2-h4"></a>

#### Anthropic

Anthropic 兼容接口支持 Base64 PDF 输入；qwen3.8-max、qwen3.8-flash 及 qwen4 系列还支持通过 `document.source.type="url"` 传入 PDF 文件 URL。

Anthropic 兼容接口支持通过 `document.source` 传入 Base64 PDF。下载[示例 PDF](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf)并保存为 `report.pdf`，或替换为自己的 PDF 文件。Python 示例需要安装 `anthropic` SDK。

以下示例使用北京地域的业务空间专属域名；请替换 `{WorkspaceId}`，并按所选地域及部署范围配置对应的 API Key 和域名，详见[接入信息](../../../get-started-with-models/regions.md)。

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-python-tab"></a>

Python

<a id="code-code-group-3-python"></a>

```python
import os
import base64
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
    timeout=300.0,
)

with open("report.pdf", "rb") as file:
    pdf_base64 = base64.b64encode(file.read()).decode("utf-8")

response = client.messages.create(
    model="qwen3.8-flash",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_base64,
                },
            },
            {"type": "text", "text": "总结这个PDF文档的内容。"},
        ],
    }],
    extra_body={"include_tool_usage": True},
)

for block in response.content:
    if block.type == "text":
        print(block.text)
```

<a id="fig-code-group-3-http-tab"></a>

HTTP

<a id="code-code-group-3-http"></a>

```bash
PDF_BASE64=$(base64 < report.pdf | tr -d '\n')
curl 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<EOF
{
  "model": "qwen3.8-flash",
  "max_tokens": 1024,
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf",
          "data": "$PDF_BASE64"
        }
      },
      {"type": "text", "text": "总结这个PDF文档的内容。"}
    ]
  }],
  "include_tool_usage": true
}
EOF
```

<a id="请求参数"></a>

<a id="pdf-request-params-h2"></a>

## 请求参数

以下参数表适用于 Chat Completions。Responses API 使用 `type: "input_file"` 和 `file_url`；Anthropic 兼容接口使用 `type: "document"`，URL 输入在 `source` 中设置 `type: "url"` 和 `url`，Base64 输入设置 `type: "base64"`、`media_type: "application/pdf"` 和 `data`（不含 Data URI 前缀的 Base64 字符串）。URL 输入支持 qwen3.8-max、qwen3.8-flash 及 qwen4 系列模型。DashScope 使用 `content` 数组中包含 `file_url` 或 `file_data` 的元素传入文件。

> **说明**
>
> 协议中 URL 部分仅支持字符串输入，不支持 list（数组）形式。

**OpenAI兼容协议格式：**

<table><thead><tr><th><p>参数</p></th><th><p>类型</p></th><th><p>是否必填</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><p>file_url</p></td><td><p>string</p></td><td rowspan="2"><p>二选一必填</p></td><td><p>指定PDF文件的下载地址，和 <code>file_data</code> 二选一必填。</p></td></tr><tr><td><p>file_data</p></td><td><p>string</p></td><td><p>Base64格式的PDF文件输入，格式为 <code>data:application/pdf;base64,xxx</code>，和 <code>file_url</code> 二选一必填。</p></td></tr><tr><td><p>filename</p></td><td><p>string</p></td><td><p>条件必填</p></td><td><p>文件名，使用 <code>file_data</code> 作为入参时必填。</p></td></tr><tr><td><p>file_format</p></td><td><p>string</p></td><td><p>否</p></td><td><p>文件格式，可选参数，当前仅支持 <code>pdf</code>，默认 <code>pdf</code>。</p></td></tr></tbody></table>

<a id="限制说明"></a>

<a id="pdf-limits-h2"></a>

## 限制说明

| 项目 | 限制 |
| --- | --- |
| 单文件大小限制 | 150MB |
| 单文档页数限制 | 256页 |

> **说明**
>
> PDF解析可能比普通文本请求耗时更长，首包超时时间最长为300秒，建议使用流式输出方式实时获取结果，避免长时间等待。

<a id="计费说明"></a>

<a id="pdf-billing-h2"></a>

## 计费说明

计费涉及以下方面：

-   **模型调用费用**：PDF文件解析出的文字与图片会计入模型的输入Token，按照模型的标准输入价格计费。
-   **文档解析费用**：按PDF文档解析的页数计费，各地域单价不同：华北2（北京）0.02元/页，新加坡0.024元/页。全球部署模式：0.02 元/页。

各模型的输入输出单价请参见[模型调用计费](../../../test-1/model-pricing.md)。

<a id="查看pdf解析页数"></a>

<a id="pdf-page-count-h3"></a>

### 查看PDF解析页数

`qwen4-max` 的 Responses API 使用响应顶层 `tool_usage`，各工具的 `num_requests` 为计费次数，`pdf_page_parser.num_requests` 为解析页数。Qwen3.8 的 Responses 示例仍使用 `usage.x_tools`。

Chat Completions 与 Responses API (Qwen3.8) 可在请求体顶层传入 `include_tool_usage: true`，从 `usage.x_tools.pdf_page_parser.count` 查看解析页数；DashScope 从 `usage.plugins.pdf_page_parser.count` 查看。Anthropic 兼容接口返回的解析页数位于响应顶层 `x_tools.pdf_page_parser.count`。解析计数未返回时，不表示本次未产生解析费用。

<a id="fig-code-group-4"></a>

<a id="fig-code-group-4-openai-兼容-tab"></a>

OpenAI 兼容

<a id="code-code-group-4-openai-兼容"></a>

```json
// 需在请求体顶层传入 "include_tool_usage": true 后才会返回。
// OpenAI Python SDK 请通过 extra_body={"include_tool_usage": True} 传入，
// 直接使用 HTTP/curl 时放在请求体顶层，不要嵌套到 extra_body 或 stream_options。
{
    "usage": {
        "x_tools": {
            "pdf_page_parser": {
                "count": 10,
                "strategy": "normal"
            }
        }
    }
}
```

<a id="fig-code-group-4-dashscope-tab"></a>

DashScope

<a id="code-code-group-4-dashscope"></a>

```json
// 默认返回，无需额外参数。
{
    "usage": {
        "plugins": {
            "pdf_page_parser": {
                "count": 10,
                "strategy": "normal"
            }
        }
    }
}
```

<a id="fig-code-group-4-anthropic-tab"></a>

Anthropic

<a id="code-code-group-4-anthropic"></a>

```json
{
    "x_tools": {
        "pdf_page_parser": {
            "count": 10,
            "strategy": "normal"
        }
    }
}
```

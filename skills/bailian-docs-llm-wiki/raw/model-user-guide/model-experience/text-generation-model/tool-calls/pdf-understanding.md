# PDF理解

PDF理解功能使模型能够解析PDF文档中的文字与图片，通过 Chat Completions、Responses API、DashScope 或 Anthropic 兼容接口进行分析。

## 支持的模型

qwen4-max-preview（[仅 Token Plan](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)）、qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash、qwen3.8-27b

qwen3.8-27b 仅支持在北京地域通过 Chat Completions 或 DashScope 调用 PDF 理解。

## 快速开始

运行以下代码，向模型传入PDF文件。

> 需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

#### OpenAI 兼容

#### Python

### 示例代码

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
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

#### Node.js

### 示例代码

```
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
        model: 'qwen3.8-max',
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

#### HTTP

### 示例代码

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
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

#### DashScope

#### Python

### 示例代码

```
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
    model="qwen3.8-max",
    messages=messages,
    stream=True,
    incremental_output=True
)

for chunk in completion:
    message = chunk.output.choices[0].message
    if message.content:
        print(message.content[0]["text"], end="", flush=True)
```

#### HTTP

### 示例代码

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
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

#### Responses API

Responses API 支持通过 `input_file.file_url` 传入 PDF。qwen3.8-27b 不支持此方式。

以下示例使用北京地域的业务空间专属域名；请替换 `{WorkspaceId}`，并按所选地域及部署范围配置对应的 API Key 和域名，详见[接入信息](raw/model-user-guide/get-started-with-models/regions.md)。

Python

```
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

HTTP

```
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

## 使用Base64输入

如果无法提供文件的URL地址，也可以将PDF文件以Base64编码字符串的形式传入。使用 `file_data` 时，`filename` 字段为必填项。

**说明**Base64 编码会使数据体积增大约 1/3，例如 150MB 的文件编码后约 200MB，会超出请求体大小上限。大文件请改用 URL 方式传入。

#### Chat Completions / DashScope

OpenAI 兼容

```
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
    model="qwen3.8-max",
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

DashScope

```
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
    model="qwen3.8-max",
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

#### Anthropic

Anthropic 兼容接口目前仅支持 Base64 PDF 输入，不支持 `document.source.type="url"`。

Anthropic 兼容接口支持通过 `document.source` 传入 Base64 PDF。下载[示例 PDF](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf)并保存为 `report.pdf`，或替换为自己的 PDF 文件。Python 示例需要安装 `anthropic` SDK。

以下示例使用北京地域的业务空间专属域名；请替换 `{WorkspaceId}`，并按所选地域及部署范围配置对应的 API Key 和域名，详见[接入信息](raw/model-user-guide/get-started-with-models/regions.md)。

Python

```
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

HTTP

```
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

## 请求参数

以下参数表适用于 Chat Completions。Responses API 使用 `type: "input_file"` 和 `file_url`；Anthropic 兼容接口使用 `type: "document"`，并在 `source` 中设置 `type: "base64"`、`media_type: "application/pdf"` 和 `data`（不含 Data URI 前缀的 Base64 字符串）。 DashScope 使用 `content` 数组中包含 `file_url` 或 `file_data` 的元素传入文件。

**说明**协议中 URL 部分仅支持字符串输入，不支持 list（数组）形式。

**OpenAI兼容协议格式：**

参数

类型

是否必填

说明

file\_url

string

二选一必填

指定PDF文件的下载地址，和 `file_data` 二选一必填。

file\_data

string

Base64格式的PDF文件输入，格式为 `data:application/pdf;base64,xxx`，和 `file_url` 二选一必填。

filename

string

条件必填

文件名，使用 `file_data` 作为入参时必填。

file\_format

string

否

文件格式，可选参数，当前仅支持 `pdf`，默认 `pdf`。

## 限制说明

项目

限制

单文件大小限制

150MB

单文档页数限制

256页

**说明**PDF解析可能比普通文本请求耗时更长，首包超时时间最长为300秒，建议使用流式输出方式实时获取结果，避免长时间等待。

## 计费说明

计费涉及以下方面：

-   **模型调用费用**：PDF文件解析出的文字与图片会计入模型的输入Token，按照模型的标准输入价格计费。
-   **文档解析费用**：按PDF文档解析的页数计费，各地域单价不同：华北2（北京）0.02元/页，新加坡0.024元/页。全球部署模式：0.02 元/页。

各模型的输入输出单价请参见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。

### 查看PDF解析页数

Chat Completions 与 Responses API 可在请求体顶层传入 `include_tool_usage: true`，从 `usage.x_tools.pdf_page_parser.count` 查看解析页数；DashScope 从 `usage.plugins.pdf_page_parser.count` 查看。Anthropic 兼容接口返回的解析页数位于响应顶层 `x_tools.pdf_page_parser.count`。解析计数未返回时，不表示本次未产生解析费用。

OpenAI 兼容

```
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

DashScope

```
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

Anthropic

```
{
    "x_tools": {
        "pdf_page_parser": {
            "count": 10,
            "strategy": "normal"
        }
    }
}
```

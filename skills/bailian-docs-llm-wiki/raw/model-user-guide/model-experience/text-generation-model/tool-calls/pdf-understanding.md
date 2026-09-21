# PDF理解

PDF理解功能使模型能够解析并理解PDF文档，提取文档中的文字与图片内容进行分析。您可以通过 OpenAI 兼容的 Chat Completions 接口或 DashScope 接口，以 URL 或 Base64 编码方式传入 PDF 文件。

> 当前 PDF 理解功能支持华北2（北京）与新加坡地域调用（其中 qwen3.8-27b 仅在华北2（北京）地域支持 PDF 理解，新加坡地域暂不支持）。暂不支持通过 Responses API 调用——使用 Responses API 传入 PDF 时，请求会返回 HTTP 200，但文件不会传递给模型。

## 支持的模型

qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash、qwen3.8-27b

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

## 使用Base64输入

如果无法提供文件的URL地址，也可以将PDF文件以Base64编码字符串的形式传入。使用 `file_data` 时，`filename` 字段为必填项。

**说明**Base64 编码会使数据体积增大约 1/3，例如 150MB 的文件编码后约 200MB，会超出请求体大小上限。大文件请改用 URL 方式传入。

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

## 请求参数

文件输入通过content数组中的元素指定，OpenAI兼容协议使用 `type: "file"` 类型，DashScope协议使用包含 `file_url`/`file_data` 的元素。

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
-   **文档解析费用**：按PDF文档解析的页数计费，各地域单价不同：华北2（北京）0.02元/页，新加坡0.024元/页。

各模型的输入输出单价请参见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。

### 查看PDF解析页数

如需在响应中查看本次请求的 PDF 解析页数，可通过 `usage` 字段中的 `pdf_page_parser.count` 获取，两种协议的行为略有不同：

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

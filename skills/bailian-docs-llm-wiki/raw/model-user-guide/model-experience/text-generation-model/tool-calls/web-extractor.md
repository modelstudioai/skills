# 网页抓取

大模型无法直接获取网页数据。网页抓取工具可以访问指定 URL 并提取内容，为大模型提供所需信息。

## 使用方式

网页抓取功能支持四种调用方式，启用参数有所不同：

#### OpenAI 兼容-Responses API

要启用网页抓取功能，您需要在 `tools` 参数中同时添加 `web_search`（联网搜索）和 `web_extractor`（网页抓取）工具。

> 当使用 qwen3-max-2026-01-23 时，需要启用 `enable_thinking` 参数以开启思考模式。

> 为获得最佳回复效果，尤其是在解决数学计算、数据分析类问题时，建议同时开启 `code_interpreter` 工具。这将允许模型在需要时调用代码解释器，提高结果的准确性。

```
# 导入依赖与创建客户端...
response = client.responses.create(
    model="qwen3.8-max",
    input="请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
    tools=[
        # 开启网页抓取必须同时开启联网搜索工具
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    extra_body={
      # 必须开启思考模式
      "enable_thinking": True
    }
)

print(response.output_text)
```

#### OpenAI 兼容-Chat Completions API

通过 `enable_search` 参数启用联网搜索，并将 `search_strategy` 设置为 `agent_max` 以启用网页抓取功能。同时需要启用 `enable_thinking` 参数开启思考模式。

> 不支持非流式输出。

```
# 导入依赖与创建客户端...
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"}],
    extra_body={
        "enable_thinking": True,
        "enable_search": True,
        "search_options": {"search_strategy": "agent_max"}
    },
    stream=True
)
```

#### DashScope

通过 `enable_search` 参数启用联网搜索，并将 `search_strategy` 设置为 `agent_max` 以启用网页抓取功能。同时需要启用 `enable_thinking` 参数开启思考模式。

> 不支持非流式输出。

```
from dashscope import Generation

response = Generation.call(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"}],
    enable_search=True,
    search_options={"search_strategy": "agent_max"},
    enable_thinking=True,
    result_format="message",
    stream=True,
    incremental_output=True
)
```

#### Anthropic 兼容

在 `tools` 参数中添加 Anthropic 服务端的网页抓取工具（`name` 为 `web_fetch`）即可启用网页抓取，并且必须同时添加联网搜索工具（`name` 为 `web_search`）。请求地址为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic`。

> 该方式面向 Claude Code 等 Anthropic 官方客户端。在客户端中直接用自然语言提问即可触发网页抓取，无需额外配置。

> 使用 Anthropic SDK 或 HTTP 直接调用时，需在 `system` 中传入客户端标识 `x-anthropic-billing-header: cc_entrypoint=cli;`，否则网页抓取不生效。

> **关于工具版本号**：`type` 中的日期后缀（例如 `web_fetch_20250910`、`web_search_20250305`）由 Anthropic 官方客户端的版本决定，客户端升级后可能改用其他日期的版本号。百炼按工具类别识别这两个工具，不校验具体的日期后缀，因此无需将 `type` 固定为某一版本，与客户端实际发送的值保持一致即可。

> 只添加网页抓取工具而未添加联网搜索工具时，请求返回 `InvalidParameter` 错误：`The web_extractor tool must be executed with web_search tool.`

```
# 导入依赖与创建客户端...
message = client.messages.create(
    model="qwen3.8-max",
    max_tokens=4096,
    # 传入客户端标识
    system=[{"type": "text", "text": "x-anthropic-billing-header: cc_entrypoint=cli;"}],
    messages=[{"role": "user", "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"}],
    tools=[
        # 开启网页抓取必须同时开启联网搜索工具
        # type 中的日期后缀由客户端版本决定，此处以 Claude Code 当前使用的版本为例
        {"type": "web_search_20250305", "name": "web_search", "max_uses": 5},
        {"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5}
    ]
)
```

抓取过程通过 `server_tool_use`（抓取请求）和 `web_fetch_tool_result`（抓取结果）内容块返回，抓取次数记录在 `usage.server_tool_use.web_fetch_requests` 中。

## 支持的模型

### 推荐模型

#### Responses API

千问Max：Qwen3.8-Max系列、Qwen3.7-Max系列

千问Plus：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列

DeepSeek：deepseek-v4-flash、deepseek-v4-flash-0731

Qwen3.8开源系列

#### Chat Completions API / DashScope

-   千问Max（思考模式）：Qwen3-Max系列
-   千问Plus：Qwen3.5-Plus系列

### 其他模型

以下模型也支持此工具调用，但效果不如推荐模型。仅支持通过Responses API调用。

-   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列
-   Qwen3.6开源系列（qwen3.6-27b除外）
-   Qwen3.5开源系列

## 快速开始

运行以下代码，通过 Responses API 调用网页抓取工具，自动总结一篇技术文档。

> 需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.responses.create(
    model="qwen3.8-max",
    input="请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
    tools=[
        {
            "type": "web_search"
        },
        {
            "type": "web_extractor"
        },
        {
            "type": "code_interpreter"
        }
    ],
    extra_body = {
        "enable_thinking": True
    }
)
# 取消以下注释查看中间过程输出
# print(response.output)
print("="*20+"回复内容"+"="*20)
print(response.output_text)
# 打印工具调用次数
usage = response.usage
print("="*20+"工具调用次数"+"="*20)
if hasattr(usage, 'x_tools') and usage.x_tools:
    print(f"\n网页抓取运行次数: {usage.x_tools.get('web_extractor', {}).get('count', 0)}")
```

javascript

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.create({
        model: "qwen3.8-max",
        input: "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
        tools: [
            { type: "web_search" },
            { type: "web_extractor" },
            { type: "code_interpreter" }
        ],
        enable_thinking: true
    });

    console.log("====================回复内容====================");
    console.log(response.output_text);

    // 打印工具调用次数
    console.log("====================工具调用次数====================");
    if (response.usage && response.usage.x_tools) {
        console.log(`网页抓取次数: ${response.usage.x_tools.web_extractor?.count || 0}`);
        console.log(`联网搜索次数: ${response.usage.x_tools.web_search?.count || 0}`);
    }
    // 取消以下注释查看中间过程的输出
    // console.log(JSON.stringify(response.output[0], null, 2));
}

main();
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
    "tools": [
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    "enable_thinking": true
}'
```

运行以上代码可获取如下回复：

```
====================回复内容====================
根据阿里云百炼官方文档，我为您总结了**代码解释器**功能的核心内容：

## 一、功能定位

...

> **文档来源**：阿里云百炼官方文档 - [Qwen代码解释器](https://help.aliyun.com/zh/model-studio/qwen-code-interpreter) 与 [Assistant API代码解释器](https://help.aliyun.com/zh/model-studio/code-interpreter)（更新时间：2025年12月）
====================工具调用次数====================

网页抓取运行次数: 1
```

## 流式输出

网页抓取耗时较长，建议启用流式输出，实时获取中间过程输出结果。

> 建议优先使用Responses API，以获取工具的中间执行状态。

#### OpenAI 兼容-Responses API

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

stream = client.responses.create(
    model="qwen3.8-max",
    input="请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
    tools=[
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    stream=True,
    extra_body={"enable_thinking": True}
)

reasoning_started = False
output_started = False

for chunk in stream:
    # 打印思考过程
    if chunk.type == 'response.reasoning_summary_text.delta':
        if not reasoning_started:
            print("="*20 + "思考过程" + "="*20)
            reasoning_started = True
        print(chunk.delta, end='', flush=True)
    # 打印工具调用完成
    elif chunk.type == 'response.output_item.done':
        if hasattr(chunk, 'item') and hasattr(chunk.item, 'type'):
            if chunk.item.type == 'web_extractor_call':
                print("\n" + "="*20 + "工具调用" + "="*20)
                print(chunk.item.goal)
                print(chunk.item.output)
            elif chunk.item.type == 'reasoning':
                reasoning_started = False
    # 打印回复内容
    elif chunk.type == 'response.output_text.delta':
        if not output_started:
            print("\n" + "="*20 + "回复内容" + "="*20)
            output_started = True
        print(chunk.delta, end='', flush=True)
    # 响应完成，打印工具调用次数
    elif chunk.type == 'response.completed':
        print("\n" + "="*20 + "工具调用次数" + "="*20)
        usage = chunk.response.usage
        if hasattr(usage, 'x_tools') and usage.x_tools:
            print(f"网页抓取次数: {usage.x_tools.get('web_extractor', {}).get('count', 0)}")
            print(f"联网搜索次数: {usage.x_tools.get('web_search', {}).get('count', 0)}")
```

javascript

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const stream = await openai.responses.create({
        model: "qwen3.8-max",
        input: "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
        tools: [
            { type: "web_search" },
            { type: "web_extractor" },
            { type: "code_interpreter" }
        ],
        stream: true,
        enable_thinking: true
    });

    let reasoningStarted = false;
    let outputStarted = false;

    for await (const chunk of stream) {
        // 打印思考过程
        if (chunk.type === 'response.reasoning_summary_text.delta') {
            if (!reasoningStarted) {
                console.log("====================思考过程====================");
                reasoningStarted = true;
            }
            process.stdout.write(chunk.delta);
        }
        // 打印工具调用完成
        else if (chunk.type === 'response.output_item.done') {
            if (chunk.item && chunk.item.type === 'web_extractor_call') {
                console.log("\n" + "====================工具调用====================");
                console.log(chunk.item.goal);
                console.log(chunk.item.output);
            } else if (chunk.item && chunk.item.type === 'reasoning') {
                reasoningStarted = false;
            }
        }
        // 打印回复内容
        else if (chunk.type === 'response.output_text.delta') {
            if (!outputStarted) {
                console.log("\n" + "====================回复内容====================");
                outputStarted = true;
            }
            process.stdout.write(chunk.delta);
        }
        // 响应完成，打印工具调用次数
        else if (chunk.type === 'response.completed') {
            console.log("\n" + "====================工具调用次数====================");
            const usage = chunk.response.usage;
            if (usage && usage.x_tools) {
                console.log(`网页抓取次数: ${usage.x_tools.web_extractor?.count || 0}`);
                console.log(`联网搜索次数: ${usage.x_tools.web_search?.count || 0}`);
            }
        }
    }
}

main();
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容",
    "tools": [
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    "enable_thinking": true,
    "stream": true
}'
```

#### OpenAI 兼容-Chat Completions API

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

stream = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role": "user", "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"}
    ],
    extra_body={
        "enable_thinking": True,
        "enable_search": True,
        "search_options": {"search_strategy": "agent_max"}
    },
    stream=True
)

reasoning_started = False
output_started = False

for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
            if not reasoning_started:
                print("="*20 + "思考过程" + "="*20)
                reasoning_started = True
            print(delta.reasoning_content, end='', flush=True)
        # 打印回复内容
        if delta.content:
            if not output_started:
                print("\n" + "="*20 + "回复内容" + "="*20)
                output_started = True
            print(delta.content, end='', flush=True)
```

javascript

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const stream = await openai.chat.completions.create({
        model: "qwen3-max",
        messages: [
            { role: "user", content: "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容" }
        ],
        enable_thinking: true,
        enable_search: true,
        search_options: { search_strategy: "agent_max" },
        stream: true
    });

    let reasoningStarted = false;
    let outputStarted = false;

    for await (const chunk of stream) {
        if (chunk.choices && chunk.choices.length > 0) {
            const delta = chunk.choices[0].delta;
            // 打印思考过程
            if (delta.reasoning_content) {
                if (!reasoningStarted) {
                    console.log("====================思考过程====================");
                    reasoningStarted = true;
                }
                process.stdout.write(delta.reasoning_content);
            }
            // 打印回复内容
            if (delta.content) {
                if (!outputStarted) {
                    console.log("\n" + "====================回复内容====================");
                    outputStarted = true;
                }
                process.stdout.write(delta.content);
            }
        }
    }
}

main();
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-max",
    "messages": [
        {"role": "user", "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"}
    ],
    "enable_thinking": true,
    "enable_search": true,
    "search_options": {"search_strategy": "agent_max"},
    "stream": true
}'
```

#### DashScope

> 不支持 Java SDK。

python

```
import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
from dashscope import Generation

# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

response = Generation.call(
    model="qwen3.8-max",
    messages=[
        {"role": "user", "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"}
    ],
    enable_search=True,
    search_options={"search_strategy": "agent_max"},
    enable_thinking=True,
    result_format="message",
    stream=True,
    incremental_output=True
)

reasoning_started = False
output_started = False

for chunk in response:
    if chunk.status_code == 200:
        message = chunk.output.choices[0].message

        # 打印思考过程
        if hasattr(message, 'reasoning_content') and message.reasoning_content:
            if not reasoning_started:
                print("="*20 + "思考过程" + "="*20)
                reasoning_started = True
            print(message.reasoning_content, end='', flush=True)

        # 打印回复内容
        if hasattr(message, 'content') and message.content:
            if not output_started:
                print("\n" + "="*20 + "回复内容" + "="*20)
                output_started = True
            print(message.content, end='', flush=True)
    else:
        print(f"\n请求失败: code={chunk.code}, message={chunk.message}")
        break
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "X-DashScope-SSE: enable" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-max",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "请访问阿里云百炼代码解释器部分的官方文档，并总结主要内容"
            }
        ]
    },
    "parameters": {
        "enable_thinking": true,
        "enable_search": true,
        "search_options": {
            "search_strategy": "agent_max"
        },
        "result_format": "message"
    }
}'
```

## 计费说明

计费涉及以下方面：

-   **模型调用费用**：抓取的网页内容会拼接到提示词中，增加模型的输入 Token，按照模型的标准价格计费。价格详情请参考百炼控制台。
    
-   **工具调用费用**：包含网页抓取与联网搜索的费用。
    
    -   联网搜索工具每 1000 次调用费用：
        
        -   华北2（北京）、美国（弗吉尼亚）、中国香港、日本（东京）、德国（法兰克福）地域：4元。
        -   新加坡地域： 73.392381元。
    -   网页抓取工具限时免费。

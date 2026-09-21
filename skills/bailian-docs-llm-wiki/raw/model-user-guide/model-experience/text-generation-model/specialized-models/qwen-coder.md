# 代码能力（Qwen-Coder）

Qwen-Coder 是专用于代码任务的语言模型。通过 API，您可以调用模型执行代码生成、代码补全，并通过工具调用与外部系统交互。

**说明**推荐使用最新的通用模型替代 Qwen-Coder 模型，请参见[文本生成](raw/model-user-guide/model-experience/text-generation-model.md)选择适合您场景的模型。

## 快速开始

API 使用前提：已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)

以下示例将演示如何调用`qwen3-coder-next`模型编写一个寻找质数的 Python 函数。

#### OpenAI兼容-Chat Completions API

#### Python

**请求示例**
```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 请将{WorkspaceId}替换为业务空间ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3-coder-next",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。不要输出非代码的内容和Markdown的代码块。'}],
)
print(completion.choices[0].message.content)
```
**返回结果**
```
def find_prime_numbers(n):
    if n <= 2:
        return []

    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    return primes
```

#### Node.js

**请求示例**
```
import OpenAI from "openai";

const client = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await client.chat.completions.create({
        model: "qwen3-coder-next",
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。不要输出非代码的内容和Markdown的代码块。" }
        ],
    });
    console.log(completion.choices[0].message.content);
}

main();
```
**返回结果**
```
def find_prime_numbers(n):
    if n <= 2:
        return []

    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    return primes
```

#### curl

**请求示例**

各地域的URL不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-next",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。不要输出非代码的内容和Markdown的代码块。"
        }
    ]
}'
```
**返回结果**
```
{
    "model": "qwen3-coder-next",
    "id": "chatcmpl-3123d5cb-01b8-9a90-98cc-5bffbb369xxx",
    "choices": [
        {
            "message": {
                "content": "def find_prime_numbers(n):\n    if n <= 2:\n        return []\n    \n    primes = []\n    for num in range(2, n):\n        is_prime = True\n        for i in range(2, int(num ** 0.5) + 1):\n            if num % i == 0:\n                is_prime = False\n                break\n        if is_prime:\n            primes.append(num)\n    \n    return primes",
                "role": "assistant"
            },
            "index": 0,
            "finish_reason": "stop"
        }
    ],
    "created": 1770108104,
    "object": "chat.completion",
    "usage": {
        "total_tokens": 155,
        "completion_tokens": 89,
        "prompt_tokens": 66
    }
}
```

#### DashScope

#### Python

**请求示例**
```
import dashscope
import os

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。不要输出非代码的内容和Markdown的代码块。"
    }
]

response = dashscope.Generation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-coder-next",
    messages=messages,
    result_format="message"
)

if response.status_code == 200:
    print(response.output.choices[0].message.content)
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
```
**返回结果**
```
def find_prime_numbers(n):
    if n <= 2:
        return []

    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    return primes
```

#### Java

**请求示例**
```
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.Protocol;

public class Main {
    public static GenerationResult callWithMessage()
            throws NoApiKeyException, ApiException, InputRequiredException {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1");
        Message sysMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.").build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。不要输出非代码的内容和Markdown的代码块。").build();
        GenerationParam param = GenerationParam.builder()
                .apiKey(apiKey)
                .model("qwen3-coder-next")
                .messages(Arrays.asList(sysMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args){
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("请求异常: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```
**返回结果**
```
def find_prime_numbers(n):
    if n <= 2:
        return []

    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    return primes
```

#### curl

**请求示例**

各地域的URL不同。

```
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-next",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。不要输出非代码的内容和Markdown的代码块。"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```
**返回结果**
```
{
    "output": {
        "choices": [
            {
                "message": {
                    "content": "def find_prime_numbers(n):\n    if n <= 2:\n        return []\n    \n    primes = []\n    for num in range(2, n):\n        is_prime = True\n        for i in range(2, int(num ** 0.5) + 1):\n            if num % i == 0:\n                is_prime = False\n                break\n        if is_prime:\n            primes.append(num)\n    \n    return primes",
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }
        ]
    },
    "usage": {
        "total_tokens": 155,
        "input_tokens": 66,
        "output_tokens": 89
    },
    "request_id": "dd78b1cf-8029-46bb-9bea-b794ded7bxxx"
}
```

## 核心能力

### 调用工具

为使模型能够与外部环境交互（例如，读写文件、调用 API、操作数据库），您可以为其提供一系列工具。模型会根据您的指令，决定是否以及如何调用这些工具。详情请参见[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)。

完整的工具调用流程包括：

1.  **定义工具并发起请求**：在请求中定义好工具列表，并向模型提出需要借助工具完成的任务。
2.  **执行工具**：解析模型返回的 `tool_calls`，并调用您本地已实现的对应工具函数来执行任务。
3.  **返回执行结果**：将工具的执行结果包装成特定格式，再次发送给模型，让其基于结果完成最终任务。

以下示例将演示如何引导模型生成代码，并使用 `write_file` 工具将其保存到本地文件。

#### OpenAI兼容-Chat Completions API

#### Python

```
import os
import json
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 请将{WorkspaceId}替换为业务空间ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "将内容写入指定文件，若文件不存在则创建。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "目标文件的相对或绝对路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "写入文件的字符串内容"
                    }
                },
                "required": ["path", "content"]
            }
        }
    }
]

# 工具函数实现
def write_file(path: str, content: str) -> str:
    """写入文件内容"""
    try:
        # 为安全起见，文件写入功能已默认禁用，如需使用请取消注释并确保路径安全
        # os.makedirs(os.path.dirname(path),exist_ok=True) if os.path.dirname(path) else None
        # with open(path, 'w', encoding='utf-8') as f:
        #     f.write(content)
        return f"成功: 文件 '{path}' 已写入"
    except Exception as e:
        return f"错误: 写入文件时发生异常 - {str(e)}"

messages = [{"role": "user", "content": "写一个python代码，快速排序，命名为quick_sort.py"}]

completion = client.chat.completions.create(
    model="qwen3-coder-next",
    messages=messages,
    tools=tools
)

assistant_output = completion.choices[0].message
if assistant_output.content is None:
    assistant_output.content = ""
messages.append(assistant_output)

# 如果不需要调用工具，直接输出内容
if assistant_output.tool_calls is None:
    print(f"无需调用工具，直接回复：{assistant_output.content}")
else:
    # 进入工具调用循环（限制最大迭代次数，避免无限循环导致成本或超时问题）
    max_rounds = 10
    current_round = 0
    while assistant_output.tool_calls is not None and current_round < max_rounds:
        current_round += 1
        for tool_call in assistant_output.tool_calls:
            tool_call_id = tool_call.id
            func_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"正在调用工具 [{func_name}]，参数：{arguments}")
            # 执行工具
            tool_result = write_file(**arguments)
            # 构造工具返回信息
            tool_message = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": tool_result,
            }
            print(f"工具返回：{tool_message['content']}")
            messages.append(tool_message)
        # 再次调用模型，获取总结后的自然语言回复
        response = client.chat.completions.create(
            model="qwen3-coder-next",
            messages=messages,
            tools=tools
        )
        assistant_output = response.choices[0].message
        if assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)
    print(f"模型最终回复：{assistant_output.content}")
```
**返回结果**
```
正在调用工具 [write_file]，参数：{'content': 'def quick_sort(arr):\\n    if len(arr) <= 1:\\n        return arr\\n    pivot = arr[len(arr) // 2]\\n    left = [x for x in arr if x < pivot]\\n    middle = [x for x in arr if x == pivot]\\n    right = [x for x in arr if x > pivot]\\n    return quick_sort(left) + middle + quick_sort(right)\\n\\nif __name__ == \\"__main__\\":\\n    example_list = [3, 6, 8, 10, 1, 2, 1]\\n    print(\\"Original list:\\", example_list)\\n    sorted_list = quick_sort(example_list)\\n    print(\\"Sorted list:\\", sorted_list)', 'path': 'quick_sort.py'}
工具返回：成功: 文件 'quick_sort.py' 已写入
模型最终回复：好的，已经为你创建了名为 `quick_sort.py` 的文件，其中包含了快速排序的 Python 实现。你可以运行这个文件查看示例输出。如果需要进一步修改或解释，请告诉我！
```

#### Node.js

```
import OpenAI from "openai";
import fs from "fs/promises";
import path from "path";

const client = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 请将{WorkspaceId}替换为业务空间ID
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

const tools = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "将内容写入指定文件，若文件不存在则创建。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "目标文件的相对或绝对路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "写入文件的字符串内容"
                    }
                },
                "required": ["path", "content"]
            }
        }
    }
];

// 工具函数实现
async function write_file(filePath, content) {
    try {
        // 为安全起见，文件写入功能已默认禁用，如需使用请取消注释并确保路径安全
        // const dir = path.dirname(filePath);
        // if (dir) {
        //     await fs.mkdir(dir, { recursive: true });
        // }
        // await fs.writeFile(filePath, content, "utf-8");
        return `成功: 文件 '${filePath}' 已写入`;
    } catch (error) {
        return `错误: 写入文件时发生异常 - ${error.message}`;
    }
}

const messages = [{"role": "user", "content": "写一个python代码，快速排序，命名为quick_sort.py"}];

async function main() {
    const completion = await client.chat.completions.create({
        model: "qwen3-coder-next",
        messages: messages,
        tools: tools
    });

    let assistant_output = completion.choices[0].message;
    // 确保 content 不是 null
    if (!assistant_output.content) assistant_output.content = "";
    messages.push(assistant_output);

    // 如果不需要调用工具，直接输出内容
    if (!assistant_output.tool_calls) {
        console.log(`无需调用工具，直接回复：${assistant_output.content}`);
    } else {
        // 进入工具调用循环（限制最大迭代次数，避免无限循环导致成本或超时问题）
        const maxRounds = 10;
        let currentRound = 0;
        while (assistant_output.tool_calls && currentRound < maxRounds) {
            currentRound++;
            for (const tool_call of assistant_output.tool_calls) {
                const tool_call_id = tool_call.id;
                const func_name = tool_call.function.name;
                const args = JSON.parse(tool_call.function.arguments);
                console.log(`正在调用工具 [${func_name}]，参数：`, args);
                // 执行工具
                const tool_result = await write_file(args.path, args.content);
                // 构造工具返回信息
                const tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_result
                };
                console.log(`工具返回：${tool_message.content}`);
                messages.push(tool_message);
            }
            // 再次调用模型，获取总结后的自然语言回复
            const response = await client.chat.completions.create({
                model: "qwen3-coder-next",
                messages: messages,
                tools: tools
            });
            assistant_output = response.choices[0].message;
            if (!assistant_output.content) assistant_output.content = "";
            messages.push(assistant_output);
        }
        console.log(`模型最终回复：${assistant_output.content}`);
    }
}

main();
```
**返回结果**
```
正在调用工具 [write_file]，参数： {
  content: 'def quick_sort(arr):\\n    if len(arr) <= 1:\\n        return arr\\n    pivot = arr[len(arr) // 2]\\n    left = [x for x in arr if x < pivot]\\n    middle = [x for x in arr if x == pivot]\\n    right = [x for x in arr if x > pivot]\\n    return quick_sort(left) + middle + quick_sort(right)\\n\\nif __name__ == \\"__main__\\":\\n    example_list = [3, 6, 8, 10, 1, 2, 1]\\n    print(\\"Original list:\\", example_list)\\n    sorted_list = quick_sort(example_list)\\n    print(\\"Sorted list:\\", sorted_list)',
  path: 'quick_sort.py'
}
工具返回：成功: 文件 'quick_sort.py' 已写入
模型最终回复：已成功创建 `quick_sort.py` 文件，其中包含快速排序的 Python 实现。你可以运行该文件以查看示例列表的排序结果。如果需要进一步修改或解释，请告诉我！
```

#### curl

该示例展示了工具调用流程的第一步：发起请求并获得模型的工具调用意图。

各地域的URL不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-next",
    "messages": [
        {
            "role": "user",
            "content": "写一个python代码，快速排序，命名为quick_sort.py"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "将内容写入指定文件，若文件不存在则创建。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目标文件的相对或绝对路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "写入文件的字符串内容"
                        }
                    },
                    "required": ["path", "content"]
                }
            }
        }
    ]
}'
```
**返回结果**
```
{
    "choices": [
        {
            "message": {
                "content": "",
                "role": "assistant",
                "tool_calls": [
                    {
                        "index": 0,
                        "id": "call_0ca7505bb6e44471a40511e5",
                        "type": "function",
                        "function": {
                            "name": "write_file",
                            "arguments": "{\"content\": \"def quick_sort(arr):\\\\n    if len(arr) <= 1:\\\\n        return arr\\\\n    pivot = arr[len(arr) // 2]\\\\n    left = [x for x in arr if x < pivot]\\\\n    middle = [x for x in arr if x == pivot]\\\\n    right = [x for x in arr if x > pivot]\\\\n    return quick_sort(left) + middle + quick_sort(right)\\\\n\\\\nif __name__ == \\\\\\\"__main__\\\\\\\":\\\\n    example_list = [3, 6, 8, 10, 1, 2, 1]\\\\n    print(\\\\\\\"Original list:\\\\\\\", example_list)\\\\n    sorted_list = quick_sort(example_list)\\\\n    print(\\\\\\\"Sorted list:\\\\\\\", sorted_list)\", \"path\": \"quick_sort.py\"}"
                        }
                    }
                ]
            },
            "finish_reason": "tool_calls",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 494,
        "completion_tokens": 193,
        "total_tokens": 687,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "created": 1761620025,
    "system_fingerprint": null,
    "model": "qwen3-coder-next",
    "id": "chatcmpl-20e96159-beea-451f-b3a4-d13b218112b5"
}
```

#### DashScope

#### Python

```
import os
import json
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

tools = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "将内容写入指定文件，若文件不存在则创建。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "目标文件的相对或绝对路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "写入文件的字符串内容"
                    }
                },
                "required": ["path", "content"]
            }
        }
    }
]

# 工具函数实现
def write_file(path: str, content: str) -> str:
    """写入文件内容"""
    try:
        # 为安全起见，文件写入功能已默认禁用，如需使用请取消注释并确保路径安全
        # os.makedirs(os.path.dirname(path),exist_ok=True) if os.path.dirname(path) else None
        # with open(path, 'w', encoding='utf-8') as f:
        #     f.write(content)
        return f"成功: 文件 '{path}' 已写入"
    except Exception as e:
        return f"错误: 写入文件时发生异常 - {str(e)}"

messages = [{"role": "user", "content": "写一个python代码，快速排序，命名为quick_sort.py"}]

response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-coder-next',
    messages=messages,
    tools=tools,
    result_format='message'
)

if response.status_code == 200:
    assistant_output = response.output.choices[0].message
    messages.append(assistant_output)

    # 如果不需要调用工具，直接输出内容
    if "tool_calls" not in assistant_output or not assistant_output["tool_calls"]:
        print(f"无需调用工具，直接回复：{assistant_output['content']}")
    else:
        # 进入工具调用循环（限制最大迭代次数，避免无限循环导致成本或超时问题）
        max_rounds = 10
        current_round = 0
        while "tool_calls" in assistant_output and assistant_output["tool_calls"] and current_round < max_rounds:
            current_round += 1
            for tool_call in assistant_output["tool_calls"]:
                func_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                tool_call_id = tool_call.get("id")
                print(f"正在调用工具 [{func_name}]，参数：{arguments}")
                # 执行工具
                tool_result = write_file(**arguments)
                # 构造工具返回信息
                tool_message = {
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call_id
                }
                print(f"工具返回：{tool_message['content']}")
                messages.append(tool_message)
            # 再次调用模型，获取总结后的自然语言回复
            response = dashscope.Generation.call(
                api_key=os.getenv('DASHSCOPE_API_KEY'),
                model='qwen3-coder-next',
                messages=messages,
                tools=tools,
                result_format='message'
            )
            if response.status_code == 200:
                print(f"模型最终回复：{response.output.choices[0].message.content}")
                assistant_output = response.output.choices[0].message
                messages.append(assistant_output)
            else:
                print(f"总结回复时执行错误：{response}")
                break
else:
    print(f"执行错误：{response}")
```
**返回结果**
```
正在调用工具 [write_file]，参数：{'content': 'def quick_sort(arr):\\n    if len(arr) <= 1:\\n        return arr\\n    pivot = arr[len(arr) // 2]\\n    left = [x for x in arr if x < pivot]\\n    middle = [x for x in arr if x == pivot]\\n    right = [x for x in arr if x > pivot]\\n    return quick_sort(left) + middle + quick_sort(right)\\n\\nif __name__ == \\"__main__\\":\\n    example_list = [3, 6, 8, 10, 1, 2, 1]\\n    print(\\"Original list:\\", example_list)\\n    sorted_list = quick_sort(example_list)\\n    print(\\"Sorted list:\\", sorted_list)', 'path': 'quick_sort.py'}
工具返回：成功: 文件 'quick_sort.py' 已写入
模型最终回复：已成功创建 `quick_sort.py` 文件，其中包含快速排序的 Python 实现。你可以运行该文件以查看示例列表的排序结果。如果需要进一步修改或解释，请告诉我！
```

#### Java

```
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.protocol.Protocol;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.tools.FunctionDefinition;
import com.alibaba.dashscope.tools.ToolCallBase;
import com.alibaba.dashscope.tools.ToolCallFunction;
import com.alibaba.dashscope.tools.ToolFunction;
import com.alibaba.dashscope.utils.JsonUtils;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {

    /**
     * 写入文件内容
     * @param arguments 模型传入的、包含工具所需参数的JSON字符串。
     * @return 工具执行后的结果字符串。
     */
    public static String writeFile(String arguments) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode argsNode = objectMapper.readTree(arguments);
            String path = argsNode.get("path").asText();
            String content = argsNode.get("content").asText();
            // 为安全起见，文件写入功能已默认禁用，如需使用请取消注释并确保路径安全
            // File file = new File(path);
            // File parentDir = file.getParentFile();
            // if (parentDir != null && !parentDir.exists()) {
            //     parentDir.mkdirs();
            // }
            // Files.write(Paths.get(path), content.getBytes(StandardCharsets.UTF_8));
            return "成功: 文件 '" + path + "' 已写入";
        } catch (Exception e) {
            return "错误: 写入文件时发生异常 - " + e.getMessage();
        }
    }

    public static void main(String[] args) {
        try {
            // 定义工具参数模式
            String writePropertyParams =
                    "{\"type\":\"object\",\"properties\":{\"path\":{\"type\":\"string\",\"description\":\"目标文件的相对或绝对路径\"},\"content\":{\"type\":\"string\",\"description\":\"写入文件的字符串内容\"}},\"required\":[\"path\",\"content\"]}";

            FunctionDefinition writeFileFunction = FunctionDefinition.builder()
                    .name("write_file")
                    .description("将内容写入指定文件，若文件不存在则创建。")
                    .parameters(JsonUtils.parseString(writePropertyParams).getAsJsonObject())
                    .build();

            // 请将{WorkspaceId}替换为业务空间ID
            Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1");

            String userInput = "写一个python代码，快速排序，命名为quick_sort.py";
            List<Message> messages = new ArrayList<>();
            messages.add(Message.builder().role(Role.USER.getValue()).content(userInput).build());

            // 首次调用模型
            GenerationParam param = GenerationParam.builder()
                    .model("qwen3-coder-next")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .messages(messages)
                    .tools(Arrays.asList(ToolFunction.builder().function(writeFileFunction).build()))
                    .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                    .build();

            GenerationResult result = gen.call(param);
            Message assistantOutput = result.getOutput().getChoices().get(0).getMessage();
            messages.add(assistantOutput);

            // 如果不需要调用工具，直接输出内容
            if (assistantOutput.getToolCalls() == null || assistantOutput.getToolCalls().isEmpty()) {
                System.out.println("无需调用工具，直接回复：" + assistantOutput.getContent());
            } else {
                // 进入工具调用循环
                while (assistantOutput.getToolCalls() != null && !assistantOutput.getToolCalls().isEmpty()) {
                    for (ToolCallBase toolCall : assistantOutput.getToolCalls()) {
                        ToolCallFunction functionCall = (ToolCallFunction) toolCall;
                        String funcName = functionCall.getFunction().getName();
                        String arguments = functionCall.getFunction().getArguments();
                        System.out.println("正在调用工具 [" + funcName + "]，参数：" + arguments);

                        // 执行工具
                        String toolResult = writeFile(arguments);

                        // 构造工具返回信息
                        Message toolMessage = Message.builder()
                                .role("tool")
                                .toolCallId(toolCall.getId())
                                .content(toolResult)
                                .build();
                        System.out.println("工具返回：" + toolMessage.getContent());
                        messages.add(toolMessage);
                    }

                    // 再次调用模型，获取总结后的自然语言回复
                    param.setMessages(messages);
                    result = gen.call(param);
                    assistantOutput = result.getOutput().getChoices().get(0).getMessage();
                    messages.add(assistantOutput);
                }
                System.out.println("模型最终回复：" + assistantOutput.getContent());
            }

        } catch (NoApiKeyException | InputRequiredException e) {
            System.err.println("错误: " + e.getMessage());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
**返回结果**
```
正在调用工具 [write_file]，参数：{"content": "def quick_sort(arr):\\n    if len(arr) <= 1:\\n        return arr\\n    pivot = arr[len(arr) // 2]\\n    left = [x for x in arr if x < pivot]\\n    middle = [x for x in arr if x == pivot]\\n    right = [x for x in arr if x > pivot]\\n    return quick_sort(left) + middle + quick_sort(right)\\n\\nif __name__ == \\\"__main__\\\":\\n    example_array = [3, 6, 8, 10, 1, 2, 1]\\n    print(\\\"Original array:\\\", example_array)\\n    sorted_array = quick_sort(example_array)\\n    print(\\\"Sorted array:\\\", sorted_array)", "path": "quick_sort.py"}
工具返回：成功: 文件 'quick_sort.py' 已写入
模型最终回复：已成功为您创建了快速排序的Python代码文件 `quick_sort.py`。该文件包含一个 `quick_sort` 函数和一个示例用法，您可以在终端或编辑器中运行它来测试快速排序功能。
```

#### curl

该示例展示了工具调用流程的第一步：发起请求并获得模型的工具调用意图。

各地域的URL不同。

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen3-coder-next",
    "input": {
        "messages": [{
            "role": "user",
            "content": "写一个python代码，快速排序，命名为quick_sort.py"
        }]
    },
    "parameters": {
        "result_format": "message",
        "tools": [
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "将内容写入指定文件，若文件不存在则创建。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目标文件的相对或绝对路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "写入文件的字符串内容"
                        }
                    },
                    "required": ["path", "content"]
                }
            }
        }
    ]
    }
}'
```
**返回结果**
```
{
    "output": {
        "choices": [
            {
                "finish_reason": "tool_calls",
                "message": {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "function": {
                                "name": "write_file",
                                "arguments": "{\"content\": \"def quick_sort(arr):\\\\n    if len(arr) <= 1:\\\\n        return arr\\\\n    pivot = arr[len(arr) // 2]\\\\n    left = [x for x in arr if x < pivot]\\\\n    middle = [x for x in arr if x == pivot]\\\\n    right = [x for x in arr if x > pivot]\\\\n    return quick_sort(left) + middle + quick_sort(right)\\\\n\\\\nif __name__ == \\\\\\\"__main__\\\\\\\":\\\\n    example_list = [3, 6, 8, 10, 1, 2, 1]\\\\n    print(\\\\\\\"Original list:\\\\\\\", example_list)\\\\n    sorted_list = quick_sort(example_list)\\\\n    print(\\\\\\\"Sorted list:\\\\\\\", sorted_list)\", \"path\": \"quick_sort.py\"}"
                            },
                            "index": 0,
                            "id": "call_645b149bbd274e8bb3789aae",
                            "type": "function"
                        }
                    ],
                    "content": ""
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 684,
        "output_tokens": 193,
        "input_tokens": 491,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "request_id": "d2386acd-fce3-9d0f-8015-c5f3a8bf9f5c"
}
```

### 代码补全

Qwen-Coder 支持两种代码补全方式，请根据您的需求选择：

-   **前缀续写（Partial Mode）**：适用于所有 Qwen-Coder 模型和地域，支持前缀补全，实现简单，推荐使用。
-   [Completions接口](raw/model-api-reference/toolkits-and-frameworks/completions.md)：仅支持华北2（北京）的`qwen-coder-turbo` 模型。支持前缀补全和前后缀补全。

#### 前缀续写 (Partial Mode)

此功能用于在您写了一半的代码（前缀）基础上，让模型自动完成剩余部分。

通过在 `messages` 列表中加入一个 `role` 为 `assistant` 的消息，并设置 `partial: true` 来实现。`assistant` 消息的 `content` 即为您提供的代码前缀。详情请参见[前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)。

#### OpenAI兼容

#### Python

**请求示例**
```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 请将{WorkspaceId}替换为业务空间ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3-coder-next",
    messages=[{
        "role": "user",
        "content": "请帮我写一个python代码生成100以内的素数。不要输出非代码的内容和Markdown的代码块。"
    },
    {
        "role": "assistant",
        "content": "def generate_prime_number",
        "partial": True
    }]
    )
print(completion.choices[0].message.content)
```
**返回结果**
```
(n):
    primes = []
    for i in range(2, n+1):
        is_prime = True
        for j in range(2, int(i**0.5)+1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

prime_numbers = generate_prime_number(100)
print(prime_numbers)
```

#### Node.js

**请求示例**
```
import OpenAI from "openai";

const client = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 请将{WorkspaceId}替换为业务空间ID
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await client.chat.completions.create({
        model: "qwen3-coder-next",
        messages: [
            { role: "user", content: "请帮我写一个python代码生成100以内的素数。不要输出非代码的内容和Markdown的代码块。" },
            { role: "assistant", content: "def generate_prime_number", partial: true}
        ],
    });
    console.log(completion.choices[0].message.content);
}

main();
```
**返回结果**
```
(n):
    primes = []
    for i in range(2, n+1):
        is_prime = True
        for j in range(2, int(i**0.5)+1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

prime_numbers = generate_prime_number(100)
print(prime_numbers)
```

#### curl

**请求示例**

各地域的URL不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-next",
    "messages": [{
        "role": "user",
        "content": "请帮我写一个python代码生成100以内的素数。不要输出非代码的内容和Markdown的代码块。"
    },
    {
        "role": "assistant",
        "content": "def generate_prime_number",
        "partial": true
    }]
}'
```
**返回结果**
```
{
    "choices": [
        {
            "message": {
                "content": "(n):\n    primes = []\n    for num in range(2, n + 1):\n        is_prime = True\n        for i in range(2, int(num ** 0.5) + 1):\n            if num % i == 0:\n                is_prime = False\n                break\n        if is_prime:\n            primes.append(num)\n    return primes\n\nprime_numbers = generate_prime_number(100)\nprint(prime_numbers)",
                "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 38,
        "completion_tokens": 93,
        "total_tokens": 131,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "created": 1761634556,
    "system_fingerprint": null,
    "model": "qwen3-coder-next",
    "id": "chatcmpl-c108050a-bb6d-4423-9d36-f64aa6a32976"
}
```

#### DashScope

#### Python

**请求示例**
```
from http import HTTPStatus
import dashscope
import os

messages = [{
    "role": "user",
    "content": "请帮我写一个python代码生成100以内的素数，不要输出非代码的内容和Markdown的代码块。"
},
{
    "role": "assistant",
    "content": "def generate_prime_number",
    "partial": True
}]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-coder-next',
    messages=messages,
    result_format='message',
)
if response.status_code == HTTPStatus.OK:
    print(response.output.choices[0].message.content)
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
```
**返回结果**
```
(n):
    primes = []
    for i in range(2, n+1):
        is_prime = True
        for j in range(2, int(i**0.5)+1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

prime_numbers = generate_prime_number(100)
print(prime_numbers)
```

#### curl

**请求示例**

各地域的URL不同。

```
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-next",
    "input":{
        "messages":[{
            "role": "user",
            "content": "请帮我写一个python代码生成100以内的素数，不要输出非代码的内容和Markdown的代码块。"
        },
        {
            "role": "assistant",
            "content": "def generate_prime_number",
            "partial": true
        }]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```
**返回结果**
```
{
    "output": {
        "choices": [
            {
                "message": {
                    "content": "(n):\n    prime_list = []\n    for i in range(2, n+1):\n        is_prime = True\n        for j in range(2, int(i**0.5)+1):\n            if i % j == 0:\n                is_prime = False\n                break\n        if is_prime:\n            prime_list.append(i)\n    return prime_list\n\nprime_numbers = generate_prime_number(100)\nprint(prime_numbers)",
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }
        ]
    },
    "usage": {
        "total_tokens": 131,
        "output_tokens": 92,
        "input_tokens": 39,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "request_id": "9917f629-e819-4519-af44-b0e677e94b2c"
}
```

#### Completions 接口

**重要**Completions 接口仅适用华北2（北京）地域的模型，需使用华北2（北京）地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

**支持的模型：**

qwen-coder-turbo

[Completions接口](raw/model-api-reference/toolkits-and-frameworks/completions.md)通过在 `prompt` 中使用特殊的 `fim` (Fill-in-the-Middle) 标签来引导模型进行补全。

#### 基于前缀补全

**提示词模板：**
```
<|fim_prefix|>{prefix_content}<|fim_suffix|>
```

-   `<|fim_prefix|>`和`<|fim_suffix|>`为特殊 Token，用于指引模型进行文本的补全，无需修改。
-   `{prefix_content}`需要替换为传入的前缀信息，例如函数的名称、输入参数、使用说明等信息。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 请将{WorkspaceId}替换为业务空间ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

completion = client.completions.create(
  model="qwen-coder-turbo",
  prompt="<|fim_prefix|>def quick_sort(arr):<|fim_suffix|>",
)

print(completion.choices[0].text)
```

javascript

```
import OpenAI from "openai";

const client = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 请将{WorkspaceId}替换为业务空间ID
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await client.completions.create({
        model: "qwen-coder-turbo",
        prompt: "<|fim_prefix|>def quick_sort(arr):<|fim_suffix|>",
    });
    console.log(completion.choices[0].text)
}

main();
```

bash

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-coder-turbo",
    "prompt": "<|fim_prefix|>def quick_sort(arr):<|fim_suffix|>"
}'
```

#### 基于前缀和后缀补全

**提示词模板**：

```
<|fim_prefix|>{prefix_content}<|fim_suffix|>{suffix_content}<|fim_middle|>
```

-   `<|fim_prefix|>`、`<|fim_suffix|>`和`<|fim_middle|>`为特殊 Token，用于指引模型进行文本的补全，无需修改。
-   `{prefix_content}`需要替换为传入的前缀信息，例如函数的名称、输入参数、使用说明等信息。
-   `{suffix_content}`需要替换为传入的后缀信息，例如函数的返回参数等信息。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 请将{WorkspaceId}替换为业务空间ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

prefix_content = """def reverse_words_with_special_chars(s):
'''
反转字符串中的每个单词（保留非字母字符的位置），并保持单词顺序。
    示例:
    reverse_words_with_special_chars("Hello, world!") -> "olleH, dlrow!"
    参数:
        s (str): 输入字符串（可能包含标点符号）
    返回:
        str: 处理后的字符串，单词反转但非字母字符位置不变
'''
"""

suffix_content = "return result"

completion = client.completions.create(
  model="qwen-coder-turbo",
  prompt=f"<|fim_prefix|>{prefix_content}<|fim_suffix|>{suffix_content}<|fim_middle|>",
)

print(completion.choices[0].text)
```

javascript

```
import OpenAI from 'openai';

const client = new OpenAI({
  // 请将{WorkspaceId}替换为业务空间ID
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
  apiKey: process.env.DASHSCOPE_API_KEY
});

const prefixContent = `def reverse_words_with_special_chars(s):
'''
反转字符串中的每个单词（保留非字母字符的位置），并保持单词顺序。
    示例:
    reverse_words_with_special_chars("Hello, world!") -> "olleH, dlrow!"
    参数:
        s (str): 输入字符串（可能包含标点符号）
    返回:
        str: 处理后的字符串，单词反转但非字母字符位置不变
'''
`;

const suffixContent = "return result";

async function main() {
  const completion = await client.completions.create({
    model: "qwen-coder-turbo",
    prompt: `<|fim_prefix|>${prefixContent}<|fim_suffix|>${suffixContent}<|fim_middle|>`
  });

  console.log(completion.choices[0].text);
}

main();
```

bash

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-coder-turbo",
    "prompt": "<|fim_prefix|>def reverse_words_with_special_chars(s):\n\"\"\"\n反转字符串中的每个单词（保留非字母字符的位置），并保持单词顺序。\n    示例:\n    reverse_words_with_special_chars(\"Hello, world!\") -> \"olleH, dlrow!\"\n    参数:\n        s (str): 输入字符串（可能包含标点符号）\n    返回:\n        str: 处理后的字符串，单词反转但非字母字符位置不变\n\"\"\"\n<|fim_suffix|>return result<|fim_middle|>"
}'
```

## 应用于生产环境

为优化千问代码模型的使用效率并降低成本，可参考以下建议：

-   **启用**[流式输出](raw/model-user-guide/model-experience/text-generation-model/stream.md): 设置 `stream=True` 可以实时返回中间结果，降低超时风险，提升用户体验。
-   **降低温度参数**: 代码生成任务通常要求结果的确定性和准确性。建议降低 `temperature` 参数，以减少生成结果的随机性。
-   **使用支持上下文缓存的模型**: 在包含大量重复前缀的场景（如代码补全、代码审查），推荐使用支持[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)的模型，以有效降低开销。
-   **控制工具数量**：为确保模型调用的效率和成本效益，建议单次传入的工具`tools`数量不超过20个。传入大量工具描述会消耗过多输入Token，这不仅会增加费用、降低响应速度，还会加大模型选择正确工具的难度，详情可参见[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)。

## 计费与限流

-   **基本计费**：根据每次请求的输入 `Token` 数和输出 `Token` 数计费。不同模型的单价不同，具体价格请参考[模型列表](raw/model-user-guide/get-started-with-models/models.md)。
    
-   **特殊计费项**：
    
    -   **阶梯计费**： `qwen3-coder` 系列模型采取阶梯计费。当**单次**请求的输入Token数达到特定阶梯后，该请求的全部输入和输出Token均按此阶梯的单价计费。
    -   **上下文缓存**：对于支持上下文缓存的模型，当多次请求包含大量重复输入时（如代码审查），缓存机制可显著降低成本。命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。详情请参见[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。
    -   **工具调用 (Function Calling)**：使用工具调用功能时，您在 `tools` 参数中定义的工具描述会作为输入内容计入 `Token` 总量并产生费用。
-   **限流**：API调用受到每分钟请求数（RPM）和每分钟Token数（TPM）的双重限制。详情请参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit#f7770a0349vq5)。
    
-   **免费额度（仅北京地域）（仅新加坡地域）**：从开通百炼或模型申请通过之日起计算有效期，有效期90天内，Qwen-Coder各模型分别提供100万Token的[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
    

## API参考

关于千问代码模型的输入与输出参数，请参见[文本生成](raw/model-api-reference/qwen-api-reference.md)。

## 常见问题

### 使用Qwen Code、Claude Code等开发工具时，为什么会消耗大量 Token？

通过外部开发工具调用 Qwen-Coder 模型处理问题时，该工具可能会多次调用 API，从而消耗大量 Token。关于具体的监控和减少Token消耗的方法，请参考[Qwen Code](raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)和[Claude Code](raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)文档。您可开启[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)功能，以避免免费额度耗尽后产生额外费用。

您也可以购买 AI 编码套餐，采用固定月费，提供月度请求额度，支持在AI工具中使用，详情请参见[Coding Plan概述](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 如何查看模型调用量？

模型调用发生后**分钟级**即可在监控图表查看。登录模型监控页面（[北京](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry)），在左侧导航栏选择**运维管理** > **模型监控**进入监控概览页，设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**查看详情**，即可查看该模型的调用统计结果。具体请参见[监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)文档。

> 监控数据按分钟级更新，仅供参考，不作为计费依据。

### 如何让模型只输出代码，不包含任何解释性文字？

可参考以下方法：

1.  **提示词约束**: 在提示词中明确指示，例如：“只返回代码，不要包含任何解释、注释或 markdown 标记。”
2.  **设置**`stop`**序列**: 使用 `stop=["\n# 解释:", "说明", "Explanation:", "Note:"]` 等词组，在模型开始生成解释性文字时提前终止，详情请参见[千问 API 参考](raw/model-api-reference/qwen-api-reference.md)。

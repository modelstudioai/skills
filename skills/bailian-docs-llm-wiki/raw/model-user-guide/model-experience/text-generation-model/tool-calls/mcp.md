# MCP

模型上下文协议（Model Context Protocol, MCP）可帮助大模型使用外部工具与数据。本文介绍通过 Responses API接入 MCP 的方法。

## 使用方式

使用 Responses API，在 `tools` 参数中配置MCP Server信息。

> 查找与开通 MCP 服务，请参见[开通云部署 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp#47ed5b5cff6hs)。

> 支持配置SSE协议的 MCP Server。

> 最多添加 10 个 MCP Server。

```
# 导入依赖与创建客户端...
mcp_tool = {
    "type": "mcp",
    "server_protocol": "sse",
    "server_label": "my-mcp-service",
    "server_description": "MCP 服务功能描述，帮助模型理解使用场景。",
    "server_url": "https://your-mcp-server-endpoint/sse",
    "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
    }
}

response = client.responses.create(
    model="qwen3.8-max",
    input="你的问题...",
    tools=[mcp_tool]
)

print(response.output_text)
```

## 支持的模型

-   千问Max：Qwen3.8-Max系列、Qwen3.7-Max系列
-   千问Plus：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列
-   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列
-   Qwen3.8开源系列
-   Qwen3.6开源系列（qwen3.6-27b除外）
-   Qwen3.5开源系列

仅支持通过 Responses API 调用。

## 快速开始

以接入网页解析（WebParser）MCP 服务为例，展示如何通过 Responses API 调用 MCP 工具。需要先开通[网页解析（WebParser）MCP 服务](https://bailian.console.aliyun.com/cn-beijing/store/mcp/detail/WebParser)。

需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> 请将示例代码中 MCP 工具配置的 `server_url` 和 `headers` 替换为您实际使用的 MCP 服务信息。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# MCP 工具配置
mcp_tool = {
    "type": "mcp",
    "server_protocol": "sse",
    "server_label": "WebParser",
    "server_description": "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
    "server_url": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
    "headers": {
        "Authorization": "Bearer " + os.getenv("DASHSCOPE_API_KEY")
    }
}

response = client.responses.create(
    model="qwen3.8-max",
    input="https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？",
    tools=[mcp_tool]
)

print("[模型回复]")
print(response.output_text)
print(f"\n[Token 用量] 输入: {response.usage.input_tokens}, 输出: {response.usage.output_tokens}, 合计: {response.usage.total_tokens}")
```

javascript

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    // MCP 工具配置
    const mcpTool = {
        type: "mcp",
        server_protocol: "sse",
        server_label: "WebParser",
        server_description: "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
        server_url: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
        headers: {
            "Authorization": "Bearer " + process.env.DASHSCOPE_API_KEY
        }
    };

    const response = await openai.responses.create({
        model: "qwen3.8-max",
        input: "https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？",
        tools: [mcpTool]
    });

    console.log("[模型回复]");
    console.log(response.output_text);
    console.log(`\n[Token 用量] 输入: ${response.usage.input_tokens}, 输出: ${response.usage.output_tokens}, 合计: ${response.usage.total_tokens}`);
}

main();
```

java

```
// 百炼 MCP 工具要求 server_protocol 字段，OpenAI 官方 Java SDK 的 Tool.Mcp 暂未提供该字段，
// 可通过 putAdditionalProperty 补齐。兼容 JDK 8+ / Spring Boot 2.x。
// Maven 依赖：com.openai:openai-java:4.67.0（或更新版本）
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.JsonValue;
import com.openai.models.responses.*;

public class McpResponsesDemo {
    public static void main(String[] args) {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey = "sk-xxx"（不建议）
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
                .build();

        Tool mcpTool = Tool.ofMcp(Tool.Mcp.builder()
                .serverLabel("WebParser")
                .serverDescription("网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。")
                .serverUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse")
                .headers(Tool.Mcp.Headers.builder()
                        .putAdditionalProperty("Authorization", JsonValue.from("Bearer " + apiKey))
                        .build())
                .putAdditionalProperty("server_protocol", JsonValue.from("sse"))
                .build());

        ResponseCreateParams params = ResponseCreateParams.builder()
                .model("qwen3.8-max")
                .input("https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？")
                .addTool(mcpTool)
                .build();

        // 调用 Responses API
        Response response = client.responses().create(params);

        System.out.println("[模型回复]");
        response.output().stream()
                .flatMap(item -> item.message().stream())
                .flatMap(message -> message.content().stream())
                .flatMap(content -> content.outputText().stream())
                .forEach(text -> System.out.println(text.text()));

        response.usage().ifPresent(u ->
                System.out.println("\n[Token 用量] 输入: " + u.inputTokens()
                        + ", 输出: " + u.outputTokens()
                        + ", 合计: " + u.totalTokens()));
    }
}
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？",
    "tools": [
        {
            "type": "mcp",
            "server_protocol": "sse",
            "server_label": "WebParser",
            "server_description": "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
            "server_url": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
            "headers": {
                "Authorization": "Bearer your-api-key"
            }
        }
    ]
}'
```

运行以上代码可获取如下回复：

```
[模型回复]
根据阿里云百炼的官方文档，MCP（Model Context Protocol）目前支持的模型如下：

*   千问Max系列：Qwen3.8-Max系列、Qwen3.7-Max系列
*   千问Plus系列：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列
*   千问Flash系列：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列
*   千问开源系列：Qwen3.8开源系列、Qwen3.6开源系列（注：qwen3.6-27b 除外）、Qwen3.5开源系列

特别注意：
MCP 功能仅支持通过 Responses API 调用。

[Token 用量] 输入: 20698, 输出: 711, 合计: 21409
```

## 流式输出

MCP 工具调用可能涉及多次外部服务交互，建议启用流式输出，实时获取工具调用过程与回复内容。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

mcp_tool = {
    "type": "mcp",
    "server_protocol": "sse",
    "server_label": "WebParser",
    "server_description": "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
    "server_url": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
    "headers": {
        "Authorization": "Bearer " + os.getenv("DASHSCOPE_API_KEY")
    }
}

stream = client.responses.create(
    model="qwen3.8-max",
    input="https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？",
    tools=[mcp_tool],
    stream=True
)

for event in stream:
    # 模型回复开始
    if event.type == "response.content_part.added":
        print("[模型回复]")
    # 流式文本输出
    elif event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    # 响应完成，输出用量
    elif event.type == "response.completed":
        usage = event.response.usage
        print(f"\n\n[Token 用量] 输入: {usage.input_tokens}, 输出: {usage.output_tokens}, 合计: {usage.total_tokens}")
```

javascript

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const mcpTool = {
        type: "mcp",
        server_protocol: "sse",
        server_label: "WebParser",
        server_description: "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
        server_url: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
        headers: {
            "Authorization": "Bearer " + process.env.DASHSCOPE_API_KEY
        }
    };

    const stream = await openai.responses.create({
        model: "qwen3.8-max",
        input: "https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？",
        tools: [mcpTool],
        stream: true
    });

    for await (const event of stream) {
        // 模型回复开始
        if (event.type === "response.content_part.added") {
            console.log("[模型回复]");
        }
        // 流式文本输出
        else if (event.type === "response.output_text.delta") {
            process.stdout.write(event.delta);
        }
        // 响应完成，输出用量
        else if (event.type === "response.completed") {
            const usage = event.response.usage;
            console.log(`\n\n[Token 用量] 输入: ${usage.input_tokens}, 输出: ${usage.output_tokens}, 合计: ${usage.total_tokens}`);
        }
    }
}

main();
```

java

```
// 百炼 MCP 工具要求 server_protocol 字段，OpenAI 官方 Java SDK 的 Tool.Mcp 暂未提供该字段，
// 可通过 putAdditionalProperty 补齐。兼容 JDK 8+ / Spring Boot 2.x。
// Maven 依赖：com.openai:openai-java:4.67.0（或更新版本）
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.JsonValue;
import com.openai.core.http.StreamResponse;
import com.openai.models.responses.*;

public class McpResponsesStreamDemo {
    public static void main(String[] args) {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey = "sk-xxx"（不建议）
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
                .build();

        Tool mcpTool = Tool.ofMcp(Tool.Mcp.builder()
                .serverLabel("WebParser")
                .serverDescription("网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。")
                .serverUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse")
                .headers(Tool.Mcp.Headers.builder()
                        .putAdditionalProperty("Authorization", JsonValue.from("Bearer " + apiKey))
                        .build())
                .putAdditionalProperty("server_protocol", JsonValue.from("sse"))
                .build());

        ResponseCreateParams params = ResponseCreateParams.builder()
                .model("qwen3.8-max")
                .input("https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？")
                .addTool(mcpTool)
                .build();

        // 调用 Responses API（流式输出）
        System.out.println("[模型回复]");
        try (StreamResponse<ResponseStreamEvent> stream = client.responses().createStreaming(params)) {
            stream.stream().forEach(event -> {
                // 流式文本输出
                event.outputTextDelta().ifPresent(delta -> {
                    System.out.print(delta.delta());
                    System.out.flush();
                });
                // 响应完成，输出用量
                if (event.isCompleted()) {
                    event.completed().ifPresent(completed ->
                            completed.response().usage().ifPresent(u ->
                                    System.out.println("\n\n[Token 用量] 输入: " + u.inputTokens()
                                            + ", 输出: " + u.outputTokens()
                                            + ", 合计: " + u.totalTokens())));
                }
            });
        }
    }
}
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "https://help.aliyun.com/zh/model-studio/mcp 里支持哪些模型？",
    "tools": [
        {
            "type": "mcp",
            "server_protocol": "sse",
            "server_label": "WebParser",
            "server_description": "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
            "server_url": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
            "headers": {
                "Authorization": "Bearer your-api-key"
            }
        }
    ],
    "stream": true
}'
```

运行以上代码可获取如下回复：

```
[模型回复]
根据阿里云百炼（Model Studio）官方文档，目前 MCP（Model Context Protocol）功能支持的模型如下：

*   千问 Max 系列：
    *   Qwen3.8-Max 系列
    *   Qwen3.7-Max 系列
*   千问 Plus 系列：
    *   Qwen3.7-Plus 系列
    *   Qwen3.6-Plus 系列
    *   Qwen3.5-Plus 系列
*   千问 Flash 系列：
    *   Qwen3.8-Flash 系列
    *   Qwen3.7-Flash 系列
    *   Qwen3.6-Flash 系列
    *   Qwen3.5-Flash 系列
*   千问开源系列：
    *   Qwen3.6 开源系列（注：不支持 qwen3.6-27b 模型）
    *   Qwen3.5 开源系列

注意：目前 MCP 功能仅支持通过 Responses API 进行调用。

[Token 用量] 输入: 20784, 输出: 867, 合计: 21651
```

## 参数说明

`mcp` 工具支持以下参数：

**参数**

**必填**

**说明**

`type`

是

固定为 `"mcp"`。

`server_protocol`

是

与 MCP 服务的通信协议，当前仅支持 `"sse"`。

`server_label`

是

MCP 服务的标签名称，用于标识该服务。

`server_description`

否

MCP 服务的功能描述，供模型理解该服务的能力与适用场景。建议填写以提升模型调用准确性。

`server_url`

是

MCP 服务的端点 URL。

`headers`

否

连接 MCP 服务时携带的请求头，例如 `Authorization` 等认证信息。

示例：

```
{
    "type": "mcp",
    "server_protocol": "sse",
    "server_label": "WebParser",
    "server_description": "网页解析（WebParser）MCP 服务，一个专用于网页内容解析的工具包。",
    "server_url": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/WebParser/sse",
    "headers": {
        "Authorization": "Bearer YOUR_DASHSCOPE_API_KEY"
    }
}
```

## 计费说明

计费包含以下部分：

-   **模型推理费用：**按模型的 Token 用量计费。
-   **MCP 服务费用：**以各 MCP 服务的计费为准。

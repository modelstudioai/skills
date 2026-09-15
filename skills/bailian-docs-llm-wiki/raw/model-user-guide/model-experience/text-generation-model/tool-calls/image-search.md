# 图搜图

图搜图工具使模型能够根据输入图片从互联网搜索视觉相似的图片，并基于搜索结果进行分析和推理，适用于以图找同款、视觉内容溯源等场景。

## 使用方式

图搜图功能通过 Responses API 调用。您需要在 `tools` 参数中添加 `image_search` 工具，并在 `input` 中以多模态格式传入图片。

> `input` 中必须包含图片内容，通过 `input_image` 类型传入图片 URL。可同时传入 `input_text` 类型的文本，为搜索提供补充说明。

```
# 导入依赖与创建客户端...
input_content = [
    {"type": "input_text", "text": "找与这张图相似风格的风景图"},
    {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
]
response = client.responses.create(
    model="qwen3.8-max",
    input=[{"role": "user", "content": input_content}],
    tools=[{"type": "image_search"}]
)

print(response.output_text)
```

## 支持的模型

### 推荐模型

为获得最佳工具调用效果，推荐使用以下模型：

千问Plus：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列

千问Max：Qwen3.8-Max系列、qwen3.7-max-2026-06-08

qwen3.8-27b

### 其他模型

以下模型也支持此工具调用，但效果不如推荐模型。

-   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列

仅支持通过 Responses API 调用。

## 快速开始

运行以下代码，通过 Responses API 调用图搜图工具，根据输入的图片搜索相似或相关图片。

> 需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> 请将示例代码中的 `image_url` 替换为可公网访问的图片 URL。

python

```
import os
import json
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

input_content = [
    {"type": "input_text", "text": "找与这张图相似风格的风景图"},
    # 请将 image_url 替换为实际的图片公网 URL
    {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
]

response = client.responses.create(
    model="qwen3.8-max",
    input=[{"role": "user", "content": input_content}],
    tools=[
        {
            "type": "image_search"
        }
    ]
)

# 遍历 output 展示每个步骤
for item in response.output:
    if item.type == "image_search_call":
        print(f"[工具调用] 图搜图 (status: {item.status})")
        # 解析并展示搜索到的图片列表
        if item.output:
            images = json.loads(item.output)
            print(f"  搜索到 {len(images)} 张图片：")
            for img in images[:5]:  # 展示前5张
                print(f"  [{img['index']}] {img['title']}")
                print(f"      {img['url']}")
            if len(images) > 5:
                print(f"  ... 共 {len(images)} 张图片")
    elif item.type == "message":
        print(f"\n[模型回复]")
        print(response.output_text)

# 展示 Token 用量和工具调用统计
print(f"\n[Token 用量] 输入: {response.usage.input_tokens}, 输出: {response.usage.output_tokens}, 合计: {response.usage.total_tokens}")
if hasattr(response.usage, 'x_tools') and response.usage.x_tools:
    for tool_name, info in response.usage.x_tools.items():
        print(f"[工具统计] {tool_name} 调用次数: {info.get('count', 0)}")
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
    const response = await openai.responses.create({
        model: "qwen3.8-max",
        input: [
            {
                role: "user",
                content: [
                    { type: "input_text", text: "找与这张图相似风格的风景图" },
                    // 请将 image_url 替换为实际的图片公网 URL
                    { type: "input_image", image_url: "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png" }
                ]
            }
        ],
        tools: [
            { type: "image_search" }
        ]
    });

    // 遍历 output 展示每个步骤
    for (const item of response.output) {
        if (item.type === "image_search_call") {
            console.log(`[工具调用] 图搜图 (status: ${item.status})`);
            // 解析并展示搜索到的图片列表
            if (item.output) {
                const images = JSON.parse(item.output);
                console.log(`  搜索到 ${images.length} 张图片：`);
                images.slice(0, 5).forEach(img => {
                    console.log(`  [${img.index}] ${img.title}`);
                    console.log(`      ${img.url}`);
                });
                if (images.length > 5) {
                    console.log(`  ... 共 ${images.length} 张图片`);
                }
            }
        } else if (item.type === "message") {
            console.log(`\n[模型回复]`);
            console.log(response.output_text);
        }
    }

    // 展示 Token 用量和工具调用统计
    console.log(`\n[Token 用量] 输入: ${response.usage.input_tokens}, 输出: ${response.usage.output_tokens}, 合计: ${response.usage.total_tokens}`);
    if (response.usage && response.usage.x_tools) {
        for (const [toolName, info] of Object.entries(response.usage.x_tools)) {
            console.log(`[工具统计] ${toolName} 调用次数: ${info.count || 0}`);
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
    "input": [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "找与这张图相似风格的风景图"},
                {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
            ]
        }
    ],
    "tools": [
        {"type": "image_search"}
    ]
}'
```

运行以上代码可获取如下回复：

```
[工具调用] 图搜图 (status: completed)
  搜索到 2 张图片：
  [1] QingMing Festival Holiday Notice 2024
      https://www.healthcabin.net/blog/wp-content/uploads/2024/04/QingMing-Festival-Holiday-Notice-2024.jpg
  [2] Serene Asian Landscape Stone Bridge Reflecting in Misty Water
      https://thumbs.dreamstime.com/b/serene-asian-landscape-stone-bridge-reflecting-misty-water-tranquil-illustration-traditional-arch-spanning-lake-style-376972039.jpg

[模型回复]
好的，已经为您找到了几张风格相似的风景图。

这些图片都展现了典型的中国水墨画或传统山水画的意境，具有以下几个共同点：
*   **传统建筑**：如亭台楼阁、拱桥等。
*   **自然元素**：如远山、湖泊、垂柳、荷花等。
*   **艺术风格**：采用淡雅的色彩和柔和的线条，营造出宁静、悠远的氛围。

...

[Token 用量] 输入: 2753, 输出: 181, 合计: 2934
[工具统计] image_search 调用次数: 1
```

## 流式输出

运行图搜图工具需要较长处理时间，建议启用流式输出，实时获取中间过程输出结果。

python

```
import os
import json
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

input_content = [
    {"type": "input_text", "text": "找与这张图相似风格的风景图"},
    # 请将 image_url 替换为实际的图片公网 URL
    {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
]

stream = client.responses.create(
    model="qwen3.8-max",
    input=[{"role": "user", "content": input_content}],
    tools=[{"type": "image_search"}],
    stream=True
)

for event in stream:
    # 工具调用开始
    if event.type == "response.output_item.added":
        if event.item.type == "image_search_call":
            print("[工具调用] 图搜图搜索中...")
    # 工具调用完成，解析并展示搜索到的图片列表
    elif event.type == "response.output_item.done":
        if event.item.type == "image_search_call":
            print(f"[工具调用] 图搜图完成 (status: {event.item.status})")
            if event.item.output:
                images = json.loads(event.item.output)
                print(f"  搜索到 {len(images)} 张图片：")
                for img in images[:5]:  # 展示前5张
                    print(f"  [{img['index']}] {img['title']}")
                    print(f"      {img['url']}")
                if len(images) > 5:
                    print(f"  ... 共 {len(images)} 张图片")
    # 模型回复开始
    elif event.type == "response.content_part.added":
        print(f"\n[模型回复]")
    # 流式文本输出
    elif event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    # 响应完成，输出用量
    elif event.type == "response.completed":
        usage = event.response.usage
        print(f"\n\n[Token 用量] 输入: {usage.input_tokens}, 输出: {usage.output_tokens}, 合计: {usage.total_tokens}")
        if hasattr(usage, 'x_tools') and usage.x_tools:
            for tool_name, info in usage.x_tools.items():
                print(f"[工具统计] {tool_name} 调用次数: {info.get('count', 0)}")
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
    const stream = await openai.responses.create({
        model: "qwen3.8-max",
        input: [
            {
                role: "user",
                content: [
                    { type: "input_text", text: "找与这张图相似风格的风景图" },
                    // 请将 image_url 替换为实际的图片公网 URL
                    { type: "input_image", image_url: "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png" }
                ]
            }
        ],
        tools: [{ type: "image_search" }],
        stream: true
    });

    for await (const event of stream) {
        // 工具调用开始
        if (event.type === "response.output_item.added") {
            if (event.item.type === "image_search_call") {
                console.log("[工具调用] 图搜图搜索中...");
            }
        }
        // 工具调用完成，解析并展示搜索到的图片列表
        else if (event.type === "response.output_item.done") {
            if (event.item && event.item.type === "image_search_call") {
                console.log(`[工具调用] 图搜图完成 (status: ${event.item.status})`);
                if (event.item.output) {
                    const images = JSON.parse(event.item.output);
                    console.log(`  搜索到 ${images.length} 张图片：`);
                    images.slice(0, 5).forEach(img => {
                        console.log(`  [${img.index}] ${img.title}`);
                        console.log(`      ${img.url}`);
                    });
                    if (images.length > 5) {
                        console.log(`  ... 共 ${images.length} 张图片`);
                    }
                }
            }
        }
        // 模型回复开始
        else if (event.type === "response.content_part.added") {
            console.log(`\n[模型回复]`);
        }
        // 流式文本输出
        else if (event.type === "response.output_text.delta") {
            process.stdout.write(event.delta);
        }
        // 响应完成，输出用量
        else if (event.type === "response.completed") {
            const usage = event.response.usage;
            console.log(`\n\n[Token 用量] 输入: ${usage.input_tokens}, 输出: ${usage.output_tokens}, 合计: ${usage.total_tokens}`);
            if (usage && usage.x_tools) {
                for (const [toolName, info] of Object.entries(usage.x_tools)) {
                    console.log(`[工具统计] ${toolName} 调用次数: ${info.count || 0}`);
                }
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
    "input": [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "找与这张图相似风格的风景图"},
                {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
            ]
        }
    ],
    "tools": [
        {"type": "image_search"}
    ],
    "stream": true
}'
```

运行以上代码可获取如下回复：

```
[工具调用] 图搜图搜索中...
[工具调用] 图搜图完成 (status: completed)
  搜索到 3 张图片：
  [1] QingMing Festival Holiday Notice 2024
      https://www.healthcabin.net/blog/wp-content/uploads/2024/04/QingMing-Festival-Holiday-Notice-2024.jpg
  [2] Serene Asian Landscape Stone Bridge Reflecting in Misty Water
      https://thumbs.dreamstime.com/b/serene-asian-landscape-stone-bridge-reflecting-misty-water-...
  [3] ...

[模型回复]
好的，已经为您找到了几张风格相似的风景图。这些图片都展现了典型的中国水墨画或工笔画风格...

[Token 用量] 输入: 5339, 输出: 164, 合计: 5503
[工具统计] image_search 调用次数: 1
```

## 计费说明

计费涉及以下方面：

-   **模型调用费用**：图片搜索的结果信息会拼接到提示词中，增加模型的输入 Token，按照模型的标准价格计费。价格详情请参考百炼控制台。
-   **工具调用费用**：每1000次调用收费：华北2（北京）地域为48元，新加坡地域为58.713905元。

## 常见问题

### Q：支持的图片格式有哪些？支持哪些图片传入方式？

A：请参见：[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)与[文件传入方式](https://help.aliyun.com/zh/model-studio/vision#531707ed76i06)。

> OpenAI SDK 不支持本地路径传入。

### Q：支持传入几张图片？

A：图片数量受模型最大输入长度限制：图片和文本的总 Token 数需小于模型支持的最大值。模型每次仅搜索一张图片，但可多次调用以处理多张。

> 搜索图片的数量由模型决策。

### Q：会返回几张搜索图片结果？

A：由模型决策，数量不固定，最多不超过 100 张。

# 文搜图

文搜图工具使模型能够根据文本描述从互联网搜索相关图片，并基于图片内容进行描述和推理，适用于可视化问答、配图推荐等场景。

## 使用方式

文搜图功能通过 Responses API 调用，在 `tools` 中添加 `web_search_image` 工具。

```
# 导入依赖与创建客户端...
response = client.responses.create(
    model="qwen3.8-max",
    input="帮我找一张适合做 PPT 封面的科技感背景图",
    tools=[{"type": "web_search_image"}]
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

运行以下代码，通过 Responses API 调用文搜图工具，根据文本描述搜索互联网图片。

> 需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

python

```
import os
import json
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.responses.create(
    model="qwen3.8-max",
    input="帮我找一张适合做 PPT 封面的科技感背景图",
    tools=[
        {
            "type": "web_search_image"
        }
    ]
)

for item in response.output:
    if item.type == "web_search_image_call":
        print(f"[工具调用] 文搜图 (status: {item.status})")
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
        input: "帮我找一张适合做 PPT 封面的科技感背景图",
        tools: [
            { type: "web_search_image" }
        ]
    });

    for (const item of response.output) {
        if (item.type === "web_search_image_call") {
            console.log(`[工具调用] 文搜图 (status: ${item.status})`);
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
    "input": "帮我找一张适合做 PPT 封面的科技感背景图",
    "tools": [
        {"type": "web_search_image"}
    ]
}'
```

运行以上代码可获取如下回复：

```
[工具调用] 文搜图 (status: completed)
  搜索到 30 张图片：
  [1] Best Free Information Technology Background S Google Slides Themes ...
      https://image.slidesdocs.com/responsive-images/slides/0-technology-line-network-information-training-courseware-powerpoint-background_17825ea41f__960_540.jpg
  [2] Data Technology Blue Abstract Business Glow Powerpoint Background ...
      https://image.slidesdocs.com/responsive-images/background/data-technology-blue-abstract-business-glow-powerpoint-background_e667bfafcb__960_540.jpg
  [3] PPT Technology Style Background Template Banner Backgrounds | PSD ...
      https://img.pikbest.com/backgrounds/20190418/ppt-technology-style-background-template-banner_1889599.jpg!bw700
  [4] Download Now! PowerPoint Background Design Technology
      https://www.slideegg.com/image/catalog/89734-powerpoint-background-design-technology.png
  [5] Powerpoint Template Technology Images ...
      https://t4.ftcdn.net/jpg/07/53/21/13/360_F_753211329_cVkWkZdxs9tNEoS5q2d8ZH362YQnAH0p.jpg
  ... 共 30 张图片

[模型回复]
为您找到几张非常适合做PPT封面的科技感背景图，您可以根据具体的主题风格进行选择：

**1. 经典蓝色电路板与芯片风格**
适合主题：硬件、芯片、电子工程、底层技术。
![Technology Background](https://www.slideegg.com/image/catalog/89734-powerpoint-background-design-technology.png)

**2. 抽象粒子与网络连接风格**
适合主题：大数据、人工智能、网络安全、云计算。
![Technology Background](https://img.freepik.com/free-vector/gradient-technology-futuristic-background_23-2149115239.jpg)

...

[Token 用量] 输入: 4326, 输出: 645, 合计: 4971
[工具统计] web_search_image 调用次数: 1
```

## 流式输出

文搜图工具运行较慢，建议启用流式输出，实时获取中间过程的输出结果。

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

stream = client.responses.create(
    model="qwen3.8-max",
    input="帮我找一张适合做 PPT 封面的科技感背景图",
    tools=[{"type": "web_search_image"}],
    stream=True
)

for event in stream:
    # 工具调用开始
    if event.type == "response.output_item.added":
        if event.item.type == "web_search_image_call":
            print("[工具调用] 文搜图搜索中...")
    # 工具调用完成，解析并展示搜索到的图片列表
    elif event.type == "response.output_item.done":
        if event.item.type == "web_search_image_call":
            print(f"[工具调用] 文搜图完成 (status: {event.item.status})")
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
        input: "帮我找一张适合做 PPT 封面的科技感背景图",
        tools: [{ type: "web_search_image" }],
        stream: true
    });

    for await (const event of stream) {
        // 工具调用开始
        if (event.type === "response.output_item.added") {
            if (event.item && event.item.type === "web_search_image_call") {
                console.log("[工具调用] 文搜图搜索中...");
            }
        }
        // 工具调用完成，解析并展示搜索到的图片列表
        else if (event.type === "response.output_item.done") {
            if (event.item && event.item.type === "web_search_image_call") {
                console.log(`[工具调用] 文搜图完成 (status: ${event.item.status})`);
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
    "input": "帮我找一张适合做 PPT 封面的科技感背景图",
    "tools": [
        {"type": "web_search_image"}
    ],
    "stream": true
}'
```

运行以上代码可获取如下输出：

```
[工具调用] 文搜图搜索中...
[工具调用] 文搜图完成 (status: completed)
  搜索到 30 张图片：
  [1] Free Technology Background PowerPoint & Google Slides Themes
      https://slidechef.net/wp-content/uploads/2023/11/TECHNOLOGY-BACKGROUND.jpg
  [2] Best Free Information Technology Background S Google Slides Themes ...
      https://image.slidesdocs.com/responsive-images/slides/0-technology-line-network-information-training-courseware-powerpoint-background_17825ea41f__960_540.jpg
  [3] PPT Technology Style Background Template Banner Backgrounds | PSD ...
      https://img.pikbest.com/backgrounds/20190418/ppt-technology-style-background-template-banner_1889599.jpg!bw700
  [4] Download Now! PowerPoint Background Design Technology
      https://www.slideegg.com/image/catalog/89734-powerpoint-background-design-technology.png
  [5] Powerpoint Template Technology Images ...
      https://t4.ftcdn.net/jpg/07/53/21/13/360_F_753211329_cVkWkZdxs9tNEoS5q2d8ZH362YQnAH0p.jpg
  ... 共 30 张图片

[模型回复]
为您找到几张非常适合做PPT封面的科技感背景图，您可以根据具体的主题风格进行选择：

**1. 极简网络连线风（适合大数据、连接、通信主题）**
这张图以深蓝色为底，角落有简洁的节点连线，中间留白非常多...
![Technology Background](https://slidechef.net/wp-content/uploads/2023/11/TECHNOLOGY-BACKGROUND.jpg)

**2. 硬核电路与芯片风（适合人工智能、硬件、底层技术主题）**
左侧有复杂的电路板纹理和类似HUD的圆环设计...
![Circuit Technology Background](https://www.slideegg.com/image/catalog/89734-powerpoint-background-design-technology.png)

...

[Token 用量] 输入: 7180, 输出: 558, 合计: 7738
[工具统计] web_search_image 调用次数: 1
```

## 计费说明

计费涉及以下方面：

-   **模型调用费用**：图片搜索的结果信息会拼接到提示词中，增加模型的输入 Token，按照模型的标准价格计费。价格详情请参考百炼控制台。
-   **工具调用费用**：每1000次调用收费：华北2（北京）地域为24元，新加坡地域58.713905元。

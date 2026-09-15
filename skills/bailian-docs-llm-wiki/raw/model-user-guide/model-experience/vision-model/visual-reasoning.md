# 视觉推理

视觉推理模型能够先输出思考过程，再输出回答内容，适用于处理复杂的视觉分析任务，如解读数学题、分析图表数据或复杂视频理解等任务。

## 效果示例

以下展示了视觉推理模型处理图片问题的效果：用户上传一张图片并提出问题，模型先进行思考分析，再给出最终回答。

**用户输入：** ![示例图片：客厅场景](https://img.alicdn.com/imgextra/i3/O1CN015BcsAj1LqLn7Cws8E_!!6000000001350-0-tps-5671-3781.jpg)

相对于您当前的位置，哪个对象在图像中的位置最远？答案选项：A.椅子 B.墙上的画 C.茶几 D.沙发。仅输出正确答案的字母（例如，A）。

思考过程

用户现在需要找出哪个对象在图像中最远。首先看选项：A椅子（左边的蓝色椅子）、B 墙上的画 、C茶几（中间的铜色茶几）、D沙发（中间的蓝色沙发）。背景中最远的通常是墙上的装饰，画（B）在墙的上方，属于背景元素，而其他如椅子、茶几、沙发都在前景或中景。所以壁画的位置最远。

**模型回答：**B

## 支持的模型

-   **Qwen3.8**
    -   **混合思考模型：**qwen3.8-max、qwen3.8-flash
-   **Qwen3.7**
    -   **混合思考模型：**qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.7-max-2026-06-08、qwen3.7-flash、qwen3.7-flash-2026-07-15
-   **Qwen3.6**
    -   **混合思考模型：**qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.6-35b-a3b
-   **Qwen3.5**
    -   **混合思考模型：**qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b
-   **Qwen3-VL**
    -   **混合思考模型：**qwen3-vl-plus、qwen3-vl-plus-2025-12-19、qwen3-vl-plus-2025-09-23、qwen3-vl-flash、qwen3-vl-flash-2025-10-15
    -   **仅思考模型：**qwen3-vl-235b-a22b-thinking**、**qwen3-vl-32b-thinking**、**qwen3-vl-30b-a3b-thinking**、**qwen3-vl-8b-thinking
-   **QVQ**
    -   **仅思考模型：**qvq-max系列、qvq-plus系列
-   **Kimi**
    -   **混合思考模型：**kimi-k2.6、kimi-k2.5
-   **Stepfun**
    -   **混合思考模型：**stepfun/step-3.7-flash
-   **MiniMax**
    -   **混合思考模型：**MiniMax/MiniMax-M3

## 使用方式

-   **思考过程：**阿里云百炼提供混合思考和仅思考两种视觉推理模型。
    
    -   **混合思考模型：**可通过`enable_thinking`控制其思考行为：
        
        -   设置为 `true`，开启思考，模型将先输出思考过程，再输出最终回复。Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5系列模型默认为`true`。
        -   设置为 `false`，关闭思考，模型将直接生成回复。`qwen3-vl-plus`、`qwen3-vl-flash`系列模型默认为`false`。
    -   **仅思考模型：**模型总会在回复前进行思考，且无法关闭。
        
-   **输出方式：**视觉推理模型包含详细的思考过程，为避免因响应内容过长导致超时，建议使用流式输出。
    
    -   Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、kimi-k2.6、kimi-k2.5、stepfun/step-3.7-flash系列支持**流式和非流式**两种方式。
    -   QVQ系列仅支持**流式输出。**
-   **System Prompt使用建议：**
    -   **对于单次或简单的对话调用**：为获得最佳推理效果，建议不设置 `System Message`。可将模型角色设定、输出格式要求等指令通过 `User Message` 传入。
    -   **对于构建 Agent 、实现工具调用等复杂应用：**可使用 `System Message` 来定义模型的角色、能力和行为框架，以确保其稳定性和可靠性。

## 快速开始

**前提条件**

-   已[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   如果通过 SDK 进行调用，需安装[最新版SDK](raw/model-api-reference/preparations/install-sdk.md)，其中 DashScope Python SDK 版本不低于1.24.6，DashScope Java SDK 版本不低于 2.21.10。

下列示例演示如何调用 `qvq-max`模型，对一张包含数学题的图片进行求解，并以流式输出的方式分别打印思考过程和最终回复。

#### OpenAI兼容

#### Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复

# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qvq-max",  # 此处以 qvq-max 为例，可按需更换模型名称
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

#### Node.js

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qvq-max',
            messages: messages,
            stream: true
        });

        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

点击查看思考过程和完整回复

```
====================思考过程====================

好的，我现在要解决这个关于长方体和正方体的表面积和体积的问题。首先，我需要仔细看一下题目，确保自己理解每个部分的要求。

题目是要求分别计算两个图形的表面积和体积。第一个图形是一个长方体，第二个是一个正方体。单位都是厘米，每题6分，共12分。看起来这是一个数学作业题，可能来自小学或初中阶段的几何内容。

首先，我需要回忆一下长方体和正方体的表面积和体积的计算公式。对于长方体来说，表面积的公式是：\( 2(ab + bc + ac) \)，其中a、b、c分别是长、宽、高。而体积则是 \( abc \)。对于正方体来说，因为所有边长相等，所以表面积是 \( 6a^2 \)，体积是 \( a^3 \)。

现在来看第一个图形，这是一个长方体，给出的尺寸是长4cm，宽3cm，高2cm。我需要先计算它的表面积。根据公式，代入数值：

表面积 = \( 2(4×3 + 3×2 + 4×2) \)
        = \( 2(12 + 6 + 8) \)
        = \( 2×26 \)
        = 52 cm²

接下来是体积，同样代入数值：

体积 = \( 4×3×2 \)
      = 24 cm³

然后是第二个图形，这是一个正方体，边长为3cm。表面积计算如下：

表面积 = \( 6×3^2 \)
        = \( 6×9 \)
        = 54 cm²

体积则是：

体积 = \( 3^3 \)
      = 27 cm³

不过，我需要检查一下是否有可能出错的地方。比如，在计算长方体的表面积时，有没有可能把某个面的面积算错了？或者在乘法的时候有没有算错数字？

比如，长方体的三个不同的面分别是4×3，3×2，4×2。这三个面的面积分别是12，6，8。加起来是26，乘以2得到52，这应该是正确的。体积的话，4×3=12，再乘以2就是24，没错。

正方体的话，每个面都是3×3=9，六个面就是54，体积是3×3×3=27，也没有问题。

所以最终的答案应该是：

1. 方体的表面积是52平方厘米，体积是24立方厘米。
2. 方体的表面积是54平方厘米，体积是27立方厘米。

不过，我需要确认题目中的图形是否有其他隐藏的信息或者可能的陷阱。例如，有时候题目可能会给出一些虚线或者阴影部分，但在这个情况下，图片中的长方体和正方体看起来都是标准的，没有特别的标记。因此，我认为我的计算是正确的。

====================完整回复====================

### 解答：

**1. 方体（长4cm，宽3cm，高2cm）**
- **表面积**：
  \[
  2 \times (4 \times 3 + 3 \times 2 + 4 \times 2) = 2 \times (12 + 6 + 8) = 2 \times 26 = 52 \, \text{cm}^2
  \]
- **体积**：
  \[
  4 \times 3 \times 2 = 24 \, \text{cm}^3
  \]

**2. 方体（边长3cm）**
- **表面积**：
  \[
  6 \times 3^2 = 6 \times 9 = 54 \, \text{cm}^2
  \]
- **体积**：
  \[
  3^3 = 27 \, \text{cm}^3
  \]

**答案：**
1. 方体的表面积为 \(52 \, \text{cm}^2\)，体积为 \(24 \, \text{cm}^3\)。
2. 方体的表面积为 \(54 \, \text{cm}^2\)，体积为 \(27 \, \text{cm}^3\)。
```

#### HTTP

#### curl

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qvq-max",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true}
}'
```

点击查看思考过程和完整回复

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"finish_reason":null,"delta":{"content":null,"reasoning_content":"好的"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"，"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"我现在"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"要"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"解决"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}
.....
data: {"choices":[{"delta":{"content":"方"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: {"choices":[{"delta":{"content":"厘米"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":544,"completion_tokens":590,"total_tokens":1134,"completion_tokens_details":{"text_tokens":590},"prompt_tokens_details":{"text_tokens":24,"image_tokens":520}},"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: [DONE]
```

#### DashScope

**说明**使用 DashScope 方式调用 QVQ 模型：

-   `incremental_output` 参数默认为 `true`，且不支持设置为 `false`，仅支持增量流式返回。
-   `result_format`参数默认为`"message"`，且不支持设置为`"text"`

#### Python

```
import os
from dashscope import MultiModalConversation

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qvq-max",  # 此处以qvq-max为例，可按需更换模型名称。
    messages=messages,
    stream=True,
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk != None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

点击查看思考过程和完整回复

```
====================思考过程====================
好的，我现在要解决这个关于长方体和正方体的表面积和体积的问题。首先，我需要仔细看一下题目，确保自己理解每个部分的要求。

题目是要求分别计算两个图形的表面积和体积。第一个图形是一个长方体，第二个是一个正方体。单位都是厘米，每题6分，共12分。看起来这是一个数学作业题，可能来自小学或初中阶段的几何内容。

首先，我需要回忆一下长方体和正方体的表面积和体积的计算公式。对于长方体来说，表面积的公式是：\( 面积 = 2(ab + bc + ac) \)，其中a、b、c分别是长、宽、高。而体积则是：\( 体积 = abc \)。对于正方体来说，因为所有边长相等，所以表面积是：\( 面积 = 6a^2 \)，体积是：\( 体积 = a^3 \)。

现在来看第一个图形，这是一个长方体，给出的尺寸是长4cm，宽3cm，高2cm。我需要先确认这些数值是否正确对应到公式中的各个变量。通常，长方体的三个维度可以任意命名，但为了方便计算，我们可以将最长的边作为长度，中间的作为宽度，最短的作为高度。不过在这里，题目中已经明确标注了各个边的长度，所以直接使用即可。

接下来，计算第一个长方体的表面积。根据公式，代入数值：

\( 面积 = 2(4×3 + 3×2 + 4×2) \)

先计算括号内的每一项：

\( 4×3 = 12 \)
\( 3×2 = 6 \)
\( 4×2 = 8 \)

然后将这些结果相加：

\( 12 + 6 + 8 = 26 \)

再乘以2：

\( 2 × 26 = 52 \)

所以，第一个长方体的表面积是52平方厘米。

接下来计算体积：

\( 体积 = 4 × 3 × 2 = 24 \)

所以，体积是24立方厘米。

现在看第二个图形，这是一个正方体，所有边长都是3cm。因此，表面积的计算为：

\( 面积 = 6 × 3^2 = 6 × 9 = 54 \)

体积则是：

\( 体积 = 3^3 = 27 \)

所以，正方体的表面积是54平方厘米，体积是27立方厘米。

在计算过程中，需要注意单位的一致性，题目中给出的单位是厘米，所以最终结果的单位应该是平方厘米和立方厘米。此外，要确保没有计算错误，比如乘法和加法的顺序是否正确，特别是长方体的表面积计算时，容易漏掉某一项或者计算错误。

另外，检查是否有其他可能的误解，比如是否混淆了长、宽、高的位置，但在这个问题中，由于题目已经明确标注了各个边的长度，所以应该不会有这个问题。同时，正方体的所有边长相等，所以无需担心不同的边长带来的复杂性。

总结一下，第一个长方体的表面积是52平方厘米，体积是24立方厘米；第二个正方体的表面积是54平方厘米，体积是27立方厘米。

====================完整回复====================
### 解答：

**1. 方体（长4cm，宽3cm，高2cm）**

- **表面积**：
  \[
  面积 = 2(ab + bc + ac) = 2(4×3 + 3×2 + 4×2) = 2(12 + 6 + 8) = 2×26 = 52 \, \text{cm}^2
  \]

- **体积**：
  \[
  体积 = abc = 4×3×2 = 24 \, \text{cm}^3
  \]

**2. 方体（边长3cm）**

- **表面积**：
  \[
  面积 = 6a^2 = 6×3^2 = 6×9 = 54 \, \text{cm}^2
  \]

- **体积**：
  \[
  体积 = a^3 = 3^3 = 27 \, \text{cm}^3
  \]

**答案：**
1. 方体的表面积为 \(52 \, \text{cm}^2\)，体积为 \(24 \, \text{cm}^3\)。
2. 方体的表面积为 \(54 \, \text{cm}^2\)，体积为 \(27 \, \text{cm}^3\)。
```

#### Java

```
// dashscope SDK的版本 >= 2.19.0
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以 qvq-max 为例，可按需更换模型名称
                .model("qvq-max")
                .messages(Arrays.asList(Msg))
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

点击查看思考过程和完整回复

```
====================思考过程====================
嗯，我现在要解决这个题目，计算两个图形的表面积和体积。首先，我需要仔细看一下题目给出的图片。第一个图形是一个长方体，第二个是正方体。题目要求分别计算它们的表面积和体积，单位是厘米。

先看第一个图形，长方体。它的尺寸应该是长、宽、高。根据图片上的标注，长是4厘米，宽是3厘米，高是2厘米。对吧？那长方体的表面积公式我记得是2乘以（长×宽 + 长×高 + 宽×高）。然后体积就是长乘宽乘高。让我再确认一下公式是否正确。没错，表面积确实是六个面的面积之和，而每个相对的面面积相等，所以用这个公式是对的。

那代入数值的话，表面积应该是2×(4×3 + 4×2 + 3×2)。先算括号里面的：4×3=12，4×2=8，3×2=6。加起来是12+8+6=26。然后乘以2就是52平方厘米。体积的话，4×3×2=24立方厘米。这部分应该没问题。

接下来是第二个图形，正方体。所有边长都是3厘米。正方体的表面积是6乘以边长的平方，因为有六个相同的正方形面。体积则是边长的三次方。所以表面积应该是6×3²=6×9=54平方厘米。体积是3³=27立方厘米。这里要注意单位，题目里已经说明单位是厘米，所以结果直接写成平方厘米和立方厘米就行。

不过，我得再检查一遍有没有哪里出错。比如，长方体的各个边是否对应正确。图片上长方体的长度看起来确实比宽度长，所以长是4，宽是3，高是2。正方体的话，三个维度都是3，没问题。计算的时候有没有算错数字？比如，长方体的表面积计算中，各个乘积是否正确，加法有没有错误。比如4×3=12，4×2=8，3×2=6，加起来是26，乘以2是52，没错。体积4×3×2=24，正确。正方体的表面积6×9=54，体积27，也没问题。

可能需要注意的地方是单位，题目里明确说单位是cm，所以答案后面要加上正确的单位符号。另外，题目要求每题6分，共12分，但这里只有两题，所以每题各占6分。不过这不影响计算过程，只是提醒自己不要漏掉任何步骤或者单位。

总结一下，第一个图形的表面积是52平方厘米，体积24立方厘米；第二个图形的表面积54平方厘米，体积27立方厘米。应该就是这样了。

====================完整回复====================
**答案：**

1. **长方体**
   - **表面积**：\(2 \times (4 \times 3 + 4 \times 2 + 3 \times 2) = 2 \times 26 = 52\) 平方厘米
   - **体积**：\(4 \times 3 \times 2 = 24\) 立方厘米

2. **正方体**
   - **表面积**：\(6 \times 3^2 = 6 \times 9 = 54\) 平方厘米
   - **体积**：\(3^3 = 27\) 立方厘米

**解析：**
- 长方体的表面积通过计算六个面的总面积得到，体积为长宽高的乘积。
- 正方体的表面积为六个相同正方形面的面积之和，体积为边长的立方。
- 单位均为厘米，符合题目要求。
```

#### HTTP

#### curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qvq-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    }
}'
```

点击查看思考过程和完整回复

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"reasoning_content":"好的","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":547,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":3,"input_tokens":544,"output_tokens_details":{"text_tokens":3},"image_tokens":520},"request_id":"f361ae45-fbef-9387-9f35-1269780e0864"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":548,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":4,"input_tokens":544,"output_tokens_details":{"text_tokens":4},"image_tokens":520},"request_id":"f361ae45-fbef-9387-9f35-1269780e0864"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"reasoning_content":"我现在","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":549,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":5,"input_tokens":544,"output_tokens_details":{"text_tokens":5},"image_tokens":520},"request_id":"f361ae45-fbef-9387-9f35-1269780e0864"}
.....
id:566
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[{"text":"方"}],"role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":1132,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":588,"input_tokens":544,"output_tokens_details":{"text_tokens":588},"image_tokens":520},"request_id":"758b0356-653b-98ac-b4d3-f812437ba1ec"}

id:567
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[{"text":"厘米"}],"role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":1133,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":589,"input_tokens":544,"output_tokens_details":{"text_tokens":589},"image_tokens":520},"request_id":"758b0356-653b-98ac-b4d3-f812437ba1ec"}

id:568
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":1134,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":590,"input_tokens":544,"output_tokens_details":{"text_tokens":590},"image_tokens":520},"request_id":"758b0356-653b-98ac-b4d3-f812437ba1ec"}
```

## 核心能力

### 开启/关闭思考过程

对于需要详细推理过程的场景（如解题、分析报告），可通过 `enable_thinking`开启思考过程。以下示例展示如何开启思考过程。

#### OpenAI 兼容

`enable_thinking` 和 `thinking_budget` 是非 OpenAI 标准参数。在不同语言的 SDK 中传递方式存在差异：

-   **Python SDK**: 必须通过 `extra_body` 字典传递。
-   **Node.js SDK**: 可作为顶层参数直接传递。

python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1
    # 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复
enable_thinking = True
# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    extra_body={
        'enable_thinking': enable_thinking},

    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

if enable_thinking:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

javascript

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1
    // 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let enableThinking = true;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen3.5-plus',
            messages: messages,
            stream: true,
          // 注意：在 Node.js SDK，enableThinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
          enable_thinking: enableThinking

        });

        if (enableThinking){console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');}

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.5-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true},
    "enable_thinking": true
}'
```

#### DashScope

python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1
# 以下为华北2（北京）地域的URL，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

enable_thinking=True

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.5-plus",
    messages=messages,
    stream=True,
    # enable_thinking 参数开启思考过程
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他视觉推理模型均不适用
    enable_thinking=enable_thinking

)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
if enable_thinking:
    print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk != None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

java

```
// dashscope SDK的版本 >= 2.21.10
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为北京地域 base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1
    // 以下为华北2（北京）地域的URL，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(Msg))
                .enableThinking(true)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成：https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 以下为华北2（北京）地域的URL，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true
    }
}'
```

### 限制思考长度

为避免视觉推理模型输出过于冗长的思考过程，可使用 `thinking_budget` 参数限制思考过程生成的最大 Token 数。当思考过程超过该限制时，内容将被截断，模型会立即开始生成最终答案。`thinking_budget` 默认值为模型的最大思维链长度，请参见模型列表。

**重要**`thinking_budget` 参数支持Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL（思考模式）、kimi-k2.6、kimi-k2.5（思考模式）。

#### OpenAI 兼容

`thinking_budget`非 OpenAI 标准参数，若使用 OpenAI Python SDK 请通过 `extra_body`传入。

python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1
    # 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复
enable_thinking = True
# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    extra_body={
        'enable_thinking': enable_thinking,
        "thinking_budget": 81920},

    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

if enable_thinking:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

javascript

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1
    // 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let enableThinking = true;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen3.5-plus',
            messages: messages,
            stream: true,
          // 注意：在 Node.js SDK，enableThinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
          enable_thinking: enableThinking,
          thinking_budget: 81920

        });

        if (enableThinking){console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');}

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.5-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true},
    "enable_thinking": true,
    "thinking_budget": 81920
}'
```

#### DashScope

python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1
# 以下为华北2（北京）地域的URL，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

enable_thinking=True
messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.5-plus",
    messages=messages,
    stream=True,
    # enable_thinking 参数开启思考过程
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    enable_thinking=enable_thinking,
    # thinking_budget 参数设置最大推理过程 Token 数
    thinking_budget=81920,

)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
if enable_thinking:
    print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk != None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

java

```
// dashscope SDK的版本 >= 2.21.10
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为北京地域 base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1
    // 以下为华北2（北京）地域的URL，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(Msg))
                .enableThinking(true)
                .thinkingBudget(81920)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成：https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 以下为华北2（北京）地域的URL，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "thinking_budget": 81920
    }
}'
```

### 更多用法

除了思考能力，视觉推理模型同样具备视觉理解模型的全部功能，可组合使用以应对更复杂的场景：

-   [多图理解](raw/model-user-guide/model-experience/vision-model/vision.md)
-   [视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)
-   [处理高分辨率图像](raw/model-user-guide/model-experience/vision-model/vision.md)
-   [传入本地文件（Base64 编码或文件路径）](raw/model-user-guide/model-experience/vision-model/vision.md)

## 计费说明

总费用 = 输入 Token 数 x 模型输入单价 + 模型输出 Token 数 x 模型输出单价。

-   思考过程（`reasoning_content`）会作为输出内容的一部分，计入**输出 Token** 并产生相应费用。若模型在思考模式下未输出思考过程，按照非思考模式价格计费。
-   图像或视频计算token的方法请参见[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)。

## API参考

关于视觉推理模型的输入输出参数，请参见[文本生成](raw/model-api-reference/qwen-api-reference.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

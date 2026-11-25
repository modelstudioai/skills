# GLM

本文介绍了在阿里云百炼平台通过API调用 GLM 系列模型的方法。 每个模型各有100万免费Token。

<a id="服务接入地址"></a>

<a id="glm_baseurl_h2"></a>

## 服务接入地址

不同地域的服务接入地址不同，请根据您选择的地域配置对应的 Base URL。

<a id="sec-tabs"></a>

<a id="openai兼容"></a>

<a id="openai兼容-h4"></a>

#### OpenAI兼容

<a id="sec-tabs-2"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="openai兼容-responses-api"></a>

<a id="openai兼容-responses-api-h4"></a>

#### OpenAI兼容-Responses API

> **说明**
>
> Responses API 目前仅支持`glm-5.2`与`glm-5.3`模型，且仅在华北2（北京）与新加坡地域提供服务。

<a id="sec-tabs-3"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="sec-tabs-4"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK 调用配置的`region`：

<a id="sec-tabs-5"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="code-block"></a>

```python
import dashscope

client = dashscope.Client(workspace="{WorkspaceId}", region="cn-beijing")
```

<a id="java"></a>

<a id="java-h4"></a>

#### Java

-   **方式一：**

<a id="code-block-2"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-3"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
```

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK 调用配置的`region`：

<a id="sec-tabs-6"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

<a id="code-block-4"></a>

```python
import dashscope

client = dashscope.Client(workspace="{WorkspaceId}", region="us-east-1")
```

<a id="java-2"></a>

<a id="java-2-h4"></a>

#### Java

-   **方式一：**

<a id="code-block-5"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-6"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";
```

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK 调用配置的`region`：

<a id="sec-tabs-7"></a>

<a id="python-3"></a>

<a id="python-3-h4"></a>

#### Python

<a id="code-block-7"></a>

```python
import dashscope

client = dashscope.Client(workspace="{WorkspaceId}", region="eu-central-1")
```

<a id="java-3"></a>

<a id="java-3-h4"></a>

#### Java

-   **方式一：**

<a id="code-block-8"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-9"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";
```

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

HTTP 请求地址为`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="ap-southeast-1")`

<a id="中国香港-2"></a>

<a id="中国香港-2-h4"></a>

#### 中国香港

HTTP 请求地址：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK 调用配置的`region`：

<a id="sec-tabs-8"></a>

<a id="python-4"></a>

<a id="python-4-h4"></a>

#### Python

<a id="code-block-10"></a>

```python
import dashscope

client = dashscope.Client(workspace="{WorkspaceId}", region="cn-hongkong")
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../get-started-with-models/regions.md#h2_migrate_domain)。

<a id="快速开始"></a>

<a id="61623d75547kl"></a>

## 快速开始

glm-5.3、glm-5.2 和 glm-5.2-fast-preview 是 GLM 系列模型，上下文长度 1M。glm-5.2 与 glm-5.2-fast-preview 支持通过`enable_thinking`参数设置思考与非思考模式；glm-5.3 仅支持思考模式，不支持关闭思考。运行以下代码快速调用思考模式的 glm-5.2 模型。

需要已[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](../../../model-api-reference/preparations/install-sdk.md)。

<a id="sec-tabs-9"></a>

<a id="openai兼容-2"></a>

<a id="openai兼容-2-h4"></a>

#### OpenAI兼容

> **说明**
>
> `enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body`传入，Node.js SDK 作为顶层参数传入。

<a id="sec-tabs-10"></a>

<a id="python-5"></a>

<a id="python-5-h4"></a>

#### Python

<a id="ddb5892c91y4c"></a>

### 示例代码

<a id="code-block-11"></a>

```python
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="glm-5.2",
    messages=messages,
    # 通过 extra_body 设置 enable_thinking 开启思考模式
    extra_body={"enable_thinking": True},
    stream=True,
    stream_options={
        "include_usage": True
    },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

<a id="f2828e7338ck1"></a>

### 返回结果

<a id="code-block-12"></a>

```text
====================思考过程====================

让我仔细思考用户提出的这个看似简单但实际上很有深度的问题。

从语言特点来看，用户使用的是中文，这意味着我应该用中文来回应。这是一个最基础的自我介绍问题，但背后可能包含着多层次的含义。

首先需要明确的是，作为一个语言模型，我应该诚实地说明自己的身份和本质。我既不是人类，也不具备真正的情感意识，而是一个由深度学习技术训练的AI助手。这是最基本的事实。

其次，考虑到用户可能的需求场景，他们或许想了解：
1. 我能提供什么样的服务
2. 我的专业领域是什么
3. 我的局限性在哪里
4. 如何与我更好地互动

在回答中，我应该既表达友好和开放的态度，又保持专业和准确。要说明自己擅长的主要领域，比如知识问答、写作辅助、创意支持等，但同时也要坦诚地指出自己的局限性，比如缺乏真实的情感体验。

此外，为了让回答更加完整，我还应该表达出愿意帮助用户解决问题的积极态度。可以适当引导用户提出更具体的问题，这样可以更好地展现自己的能力。

考虑到这是一个开放式的开场白，回答时既要简洁明了，又要包含足够的信息量，让用户对我的基本情况有一个清晰的认识，同时为后续的对话奠定良好的基础。

最后，语气应该保持谦逊和专业，既不过于技术化，也不显得过分随意，让用户感到舒适和自然。
====================完整回复====================

我是智谱AI训练的GLM大语言模型，旨在为用户提供信息和帮助解决问题。我被设计用来理解和生成人类语言，可以回答问题、提供解释或参与各类话题讨论。

我不会存储您的个人数据，我们的对话是匿名的。有什么我能帮您了解或探讨的话题吗？
====================Token 消耗====================

CompletionUsage(completion_tokens=344, prompt_tokens=7, total_tokens=351, completion_tokens_details=None, prompt_tokens_details=None)
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="25ed2818c5km2"></a>

### 示例代码

<a id="code-block-13"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];

        const stream = await openai.chat.completions.create({
            model: 'glm-5.2',
            messages,
            // 注意：在 Node.js SDK，enable_thinking 这样的非标准参数作为顶层属性传递，无需放在 extra_body 中
            enable_thinking: true,
            stream: true,
            stream_options: {
                include_usage: true
            },
        });

        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\n' + '='.repeat(20) + 'Token 消耗' + '='.repeat(20) + '\n');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
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

<a id="1f1fdf8de1624"></a>

### 返回结果

<a id="code-block-14"></a>

```text
====================思考过程====================

让我仔细思考用户的问题"你是谁"。这需要从多个角度来分析和回应。

首先，这是一个基础的身份认知问题。作为GLM大语言模型，需要准确表达自己的身份定位。应该清晰地说明自己是由智谱AI开发的AI助手。

其次，思考用户提出这个问题的可能意图。他们可能是初次接触，想了解基本功能；也可能想确认是否能提供特定帮助；或者只是想测试回应方式。因此需要给出一个开放且友好的回答。

还要考虑回答的完整性。除了身份介绍，也应该简要说明主要功能，如问答、创作、分析等，让用户了解可以如何使用这个助手。

最后，要确保语气友好亲和，表达出乐于帮助的态度。可以用"很高兴为您服务"这样的表达，让用户感受到交流的温暖。

基于这些思考，可以组织一个简洁明了的回答，既能回答用户问题，又能引导后续交流。
====================完整回复====================

我是GLM，由智谱AI训练的大语言模型。我通过大规模文本数据训练，能够理解和生成人类语言，帮助用户回答问题、提供信息和进行对话交流。

我会持续学习和改进，以提供更好的服务。很高兴能为您解答问题或提供帮助！有什么我能为您做的吗？
====================Token 消耗====================

{ prompt_tokens: 7, completion_tokens: 248, total_tokens: 255 }
```

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="bcaf8f53f8n2x"></a>

### 示例代码

<a id="sec-tabs-11"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-15"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "glm-5.2",
    "messages": [
        {
            "role": "user",
            "content": "你是谁"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

<a id="dashscope-2"></a>

<a id="dashscope-2-h4"></a>

#### DashScope

<a id="sec-tabs-12"></a>

<a id="python-6"></a>

<a id="python-6-h4"></a>

#### Python

<a id="07c36189dbqo7"></a>

### 示例代码

<a id="code-block-16"></a>

```python
import os
import dashscope

# 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]

completion = client.chat.completions.create(
    model="glm-5.2",
    messages=messages,
    enable_thinking=True,     # 开启思考模式
    stream=True,              # 开启流式输出
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    message = chunk.choices[0].delta
    # 只收集思考内容
    if message.reasoning_content:
        if not is_answering:
            print(message.reasoning_content, end="", flush=True)
        reasoning_content += message.reasoning_content

    # 收到 content，开始进行回复
    if message.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(message.content, end="", flush=True)
        answer_content += message.content

print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
print(chunk.usage)
```

<a id="70dc157a528ub"></a>

### 返回结果

<a id="code-block-17"></a>

```text
====================思考过程====================

让我仔细思考用户提出的"你是谁"这个问题。首先需要分析用户提问的意图，这可能是初次接触时的好奇，也可能是想了解我的具体功能和能力。

从专业角度，我应该清晰地表达自己的身份 - 作为一个GLM大语言模型，需要说明自己的基本定位和主要功能。要避免过于技术化的表述，而是用通俗易懂的方式解释。

同时，也要考虑到用户可能关心的一些实际问题，比如隐私保护、数据安全等。这些都是用户在使用AI服务时非常关注的点。

另外，为了展现专业性和友好度，可以在介绍的基础上主动引导对话方向，询问用户是否需要特定的帮助。这样既能让用户更好地了解我，也能为后续对话做好铺垫。

最后，要确保回答简洁明了，重点突出，让用户快速理解我的身份和用途。这样的回答既能满足用户的好奇心，又能展现专业性和服务意识。
====================完整回复====================

我是智谱AI开发的GLM大语言模型，旨在通过自然语言处理技术为用户提供信息和帮助。我通过大规模文本数据训练，能够理解和生成人类语言，回答问题、提供知识支持和参与对话。

我的设计目标是成为有用的AI助手，同时确保用户隐私和数据安全。我不存储用户的个人信息，并且会持续学习和改进以提供更优质的服务。

有什么我能帮您解答的问题或需要协助的任务吗？
====================Token 消耗====================

{"input_tokens": 8, "output_tokens": 269, "total_tokens": 277}
```

<a id="java-4"></a>

<a id="java-4-h4"></a>

#### Java

<a id="f0fdaa75c28ak"></a>

### 示例代码

> **重要**
>
> DashScope Java SDK 版本需要不低于2.19.4。

<a id="code-block-18"></a>

```java
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;

public class Main {
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (reasoning != null && !reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }
        if (content != null && !content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("glm-5.2")
                .incrementalOutput(true)
                .resultFormat("message")
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }
    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("An exception occurred: " + e.getMessage());
        }
    }
}
```

<a id="e91b400fc67bu"></a>

### 返回结果

<a id="code-block-19"></a>

```text
====================思考过程====================
让我思考一下如何回答用户的问题。首先，这是一个关于身份识别的简单问题，需要清晰直接地回答。

作为一个大语言模型，我应该准确说明自己的基本身份信息。这包括：
- 名称：GLM
- 开发者：智谱AI
- 主要功能：语言理解和生成

考虑到用户的提问可能源于初次接触，我需要用通俗易懂的方式介绍自己，避免使用过于技术性的术语。同时，也应该简要说明自己的主要能力，这样可以帮助用户更好地了解如何与我互动。

我还应该以友好开放的态度表达，欢迎用户提出各种问题，这样可以为后续对话打下良好基础。不过介绍要简洁明了，不需要过于详细，以免给用户造成信息负担。

最后，为了促进进一步交流，可以主动询问用户是否需要特定帮助，这样能够更好地服务于用户的实际需求。
====================完整回复====================
我是GLM，由智谱AI开发的大语言模型。我通过海量文本数据训练而成，能够理解和生成人类语言，回答问题、提供信息和进行对话。

我的设计目的是帮助用户解决问题、提供知识和支持各类语言任务。我会不断学习和更新，以提供更准确、有用的回答。

有什么我能帮您解答或探讨的问题吗？
```

<a id="http-2"></a>

<a id="http-2-h4"></a>

#### HTTP

<a id="1b4ac400b5f33"></a>

### 示例代码

<a id="sec-tabs-13"></a>

<a id="curl-2"></a>

<a id="curl-2-h4"></a>

#### curl

<a id="code-block-20"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "glm-5.2",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

<a id="anthropic兼容"></a>

<a id="anthropic兼容-h4"></a>

#### Anthropic兼容

<a id="sec-tabs-14"></a>

<a id="python-7"></a>

<a id="python-7-h4"></a>

#### Python

<a id="glm_anthropic_py_code_h3"></a>

### 示例代码

<a id="code-block-21"></a>

```python
import anthropic
import os

client = anthropic.Anthropic(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
)

message = client.messages.create(
    model="glm-5.2",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "你是谁"}
    ],
    stream=True,
)

for event in message:
    if event.type == "content_block_delta":
        if hasattr(event.delta, "thinking"):
            print(event.delta.thinking, end="", flush=True)
        if hasattr(event.delta, "text"):
            print(event.delta.text, end="", flush=True)
```

<a id="http-3"></a>

<a id="http-3-h4"></a>

#### HTTP

<a id="glm_anthropic_curl_code_h3"></a>

### 示例代码

<a id="sec-tabs-15"></a>

<a id="curl-3"></a>

<a id="curl-3-h4"></a>

#### curl

<a id="code-block-22"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "anthropic-version: 2023-06-01" \
-d '{
    "model": "glm-5.2",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": "你是谁"
        }
    ]
}'
```

<a id="逐块返回-token-用量-chunk-include-usage"></a>

<a id="glm_chunk_usage_h2"></a>

## 逐块返回 Token 用量（chunk\_include\_usage）

`glm-5.3` 通过 OpenAI Chat Completions 流式调用时，支持 `stream_options.chunk_include_usage` 参数（boolean，可选，默认值为 `false`），仅在 `stream` 为 `true` 时生效。Responses API 不支持该参数。

-   `true`：每个数据块均包含 `usage`，表示截至当前数据块的累计 Token 用量，而不是当前块新增的用量。无需同时设置 `stream_options.include_usage`。
-   `false` 或不传：不逐块返回用量。需要在最后一个数据块中获取总用量时，设置 `stream_options.include_usage=true`。

流式末尾仍会返回一个 `choices` 为空的用量块，其中的 `usage` 与结束内容块中的最终累计值相同。

不同网关的支持情况如下：

-   **华北2（北京）业务空间专属域名（新网关）**：支持。例如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
-   **DashScope 固定域名（旧网关）**：不支持。旧网关地址为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，设置 `chunk_include_usage` 后也不会逐块返回用量；需要总用量时仍使用 `stream_options.include_usage=true`。

以下请求使用业务空间专属域名。请将 `{WorkspaceId}` 替换为实际业务空间 ID，并提前配置 API Key 环境变量。

<a id="code-block-23"></a>

```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.3",
    "messages": [{"role": "user", "content": "只回答：好"}],
    "stream": true,
    "stream_options": {
      "chunk_include_usage": true
    }
  }'
```

以下响应省略了中间重复的数据块。首块的 `total_tokens` 为 17，结束块及最终用量块的 `total_tokens` 累计为 70。

<a id="code-block-24"></a>

```text
data: {"model":"glm-5.3","id":"chatcmpl-xxx","created":1794824000,"object":"chat.completion.chunk","usage":{"prompt_tokens":16,"total_tokens":17,"completion_tokens":1,"prompt_tokens_details":{"cached_tokens":0},"completion_tokens_details":{"reasoning_tokens":1}},"choices":[{"logprobs":null,"index":0,"delta":{"reasoning_content":"","content":"","role":"assistant"},"finish_reason":null}]}

...（省略中间数据块）...

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1794824000,"model":"glm-5.3","choices":[{"index":0,"delta":{"content":"","reasoning_content":""},"finish_reason":"stop","logprobs":null}],"usage":{"prompt_tokens":16,"total_tokens":70,"completion_tokens":54,"prompt_tokens_details":{"cached_tokens":0},"completion_tokens_details":{"reasoning_tokens":52}}}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1794824000,"model":"glm-5.3","choices":[],"usage":{"prompt_tokens":16,"total_tokens":70,"completion_tokens":54,"prompt_tokens_details":{"cached_tokens":0},"completion_tokens_details":{"reasoning_tokens":52}}}

data: [DONE]
```

<a id="流式工具调用"></a>

<a id="h7i8j9k0l1m2n"></a>

## 流式工具调用

glm-5.3、glm-5.2、glm-5.2-fast-preview、glm-5.1、glm-5 支持`tool_stream`参数（boolean）。glm-5.3 的默认值为`true`，其余模型的默认值为`false`；该参数仅在`stream`为`true`时生效。开启后，Function Calling 返回的 tool\_call 参数（arguments）会以流式增量方式逐步返回，而非等待完整生成后一次性返回。

`stream`与`tool_stream`的组合行为如下：

| stream | tool\_stream | tool\_call 返回方式 |
| --- | --- | --- |
| true | true | arguments 以增量方式分多个 chunk 返回 |
| true | false（默认） | arguments 在一个 chunk 中完整返回 |
| false | true/false | tool\_stream 不生效，arguments 在完整响应中一次性返回 |

<a id="sec-tabs-16"></a>

<a id="openai兼容-3"></a>

<a id="openai兼容-3-h4"></a>

#### OpenAI兼容

<a id="sec-tabs-17"></a>

<a id="python-8"></a>

<a id="python-8-h4"></a>

#### Python

<a id="ts35o6p7q8r9s"></a>

### 示例代码

<a id="code-block-25"></a>

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [{"role": "user", "content": "北京天气怎么样"}]

completion = client.chat.completions.create(
    model="glm-5.2",
    tools=tools,
    messages=messages,
    extra_body={
        "tool_stream": True,
    },
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if hasattr(delta, 'content') and delta.content:
            print(f"[content] {delta.content}")
        if hasattr(delta, 'tool_calls') and delta.tool_calls:
            for tc in delta.tool_calls:
                print(f"[tool_call] id={tc.id}, name={tc.function.name}, args={tc.function.arguments}")
        if chunk.choices[0].finish_reason:
            print(f"[finish_reason] {chunk.choices[0].finish_reason}")
    if not chunk.choices and chunk.usage:
        print(f"[usage] {chunk.usage}")
```

<a id="node-js-2"></a>

<a id="node-js-2-h4"></a>

#### Node.js

<a id="ts39i2j3k4l5m"></a>

### 示例代码

<a id="code-block-26"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const tools = [
    {
        type: "function",
        function: {
            name: "get_weather",
            description: "获取指定城市的天气信息",
            parameters: {
                type: "object",
                properties: {
                    city: { type: "string", description: "城市名称" }
                },
                required: ["city"]
            }
        }
    }
];

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'glm-5.2',
            messages: [{ role: 'user', content: '北京天气怎么样' }],
            tools: tools,
            tool_stream: true,
            stream: true,
            stream_options: {
                include_usage: true
            },
        });

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                if (chunk.usage) {
                    console.log(`[usage] ${JSON.stringify(chunk.usage)}`);
                }
                continue;
            }

            const delta = chunk.choices[0].delta;

            if (delta.content) {
                console.log(`[content] ${delta.content}`);
            }

            if (delta.tool_calls) {
                for (const tc of delta.tool_calls) {
                    console.log(`[tool_call] id=${tc.id}, name=${tc.function.name}, args=${tc.function.arguments}`);
                }
            }

            if (chunk.choices[0].finish_reason) {
                console.log(`[finish_reason] ${chunk.choices[0].finish_reason}`);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

<a id="http-4"></a>

<a id="http-4-h4"></a>

#### HTTP

<a id="ts44h2i3j4k5l"></a>

### 示例代码

<a id="sec-tabs-18"></a>

<a id="curl-4"></a>

<a id="curl-4-h4"></a>

#### curl

<a id="code-block-27"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "glm-5.2",
    "messages": [
        {
            "role": "user",
            "content": "北京天气怎么样"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "城市名称"}
                    },
                    "required": ["city"]
                }
            }
        }
    ],
    "stream": true,
    "stream_options": {"include_usage": true},
    "tool_stream": true
}'
```

<a id="dashscope-3"></a>

<a id="dashscope-3-h4"></a>

#### DashScope

<a id="sec-tabs-19"></a>

<a id="python-9"></a>

<a id="python-9-h4"></a>

#### Python

<a id="ts51q0r1s2t3u"></a>

### 示例代码

<a id="code-block-28"></a>

```python
import os
import dashscope

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [{"role": "user", "content": "北京天气怎么样"}]

completion = client.chat.completions.create(
    model="glm-5.2",
    messages=messages,
    tools=tools,
    stream=True,
    parameters={"tool_stream": True},
)

for chunk in completion:
    msg = chunk.choices[0].delta
    if msg.content:
        print(f"[content] {msg.content}")
    if msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"[tool_call] id={tc.id or ''}, name={tc.function.name}, args={tc.function.arguments}")
    finish = chunk.choices[0].finish_reason
    if finish and finish != "null":
        print(f"[finish_reason] {finish}")
```

<a id="http-5"></a>

<a id="http-5-h4"></a>

#### HTTP

<a id="ts55k6l7m8n9o"></a>

### 示例代码

<a id="sec-tabs-20"></a>

<a id="curl-5"></a>

<a id="curl-5-h4"></a>

#### curl

<a id="code-block-29"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "glm-5.2",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "北京天气怎么样"
            }
        ]
    },
    "parameters": {
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "城市名称"}
                        },
                        "required": ["city"]
                    }
                }
            }
        ],
        "tool_stream": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

<a id="推理强度-reasoning-effort"></a>

<a id="glm_re_section_title"></a>

## 推理强度（reasoning\_effort）

glm-5.3、glm-5.2、glm-5.2-fast-preview 和 glm-5.1 默认开启思考模式，模型会先输出思考过程（`reasoning_content`），再给出最终回答。通过 `reasoning_effort` 参数可以调整推理强度，取值越高思考越充分。**不同模型支持的可选取值不同**，传入不支持的取值会返回 `invalid_parameter_error` 错误，请按下表选择。

| 模型 | reasoning\_effort 可选取值 |
| --- | --- |
| glm-5.3 | `low`、`high`、`max`（最高） |
| glm-5.2 | `none`（不进行推理，`reasoning_tokens`\=`0`）、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`（最高） |
| glm-5.2-fast-preview | `none`（不进行推理，`reasoning_tokens`\=`0`）、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`（最高） |
| glm-5.1 | `none`、`minimal`、`low`、`medium`、`high`、`xhigh`（最高，不支持 max） |
| glm-5 | `none`、`minimal`、`low`、`medium`、`high`、`xhigh`（最高，不支持 max） |

> **说明**
>
> 如需关闭思考，可在 OpenAI 兼容与 DashScope 方式中传入 `enable_thinking`\=`false`，该参数优先级高于 `reasoning_effort`。glm-5.3 不支持关闭思考，传入 `enable_thinking`\=`false` 不会生效。

> **说明**
>
> Anthropic 兼容方式不支持 `reasoning_effort` 参数。如需获取思考内容，请使用 Anthropic 原生 `thinking` 参数：`{"thinking":{"type":"enabled","budget_tokens":1024}}`，开启后响应 `content` 中会返回 `type` 为 `thinking` 的思考块。

<a id="sec-tabs-21"></a>

<a id="openai兼容-4"></a>

<a id="openai兼容-4-h4"></a>

#### OpenAI兼容

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="glm-5.2",
    messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
    reasoning_effort="high",
)
print(completion.choices[0].message.content)
```

<a id="fig-code-group-node-js-tab"></a>

Node.js

<a id="code-code-group-node-js"></a>

```javascript
import OpenAI from "openai";
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});
const completion = await openai.chat.completions.create({
    model: "glm-5.2",
    messages: [{ role: "user", content: "9.9和9.11哪个大" }],
    reasoning_effort: "high",
});
console.log(completion.choices[0].message.content);
```

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "glm-5.2",
    "messages": [{"role": "user", "content": "9.9和9.11哪个大"}],
    "reasoning_effort": "high"
}'
```

<a id="dashscope-4"></a>

<a id="dashscope-4-h4"></a>

#### DashScope

<a id="code-block-30"></a>

```python
import os
import dashscope

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
response = client.chat.completions.create(
    model="glm-5.2",
    messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
    parameters={"reasoning_effort": "high"},
)
print(response.choices[0].message.content)
```

<a id="清除历史思考-clear-thinking"></a>

<a id="glm_ct_section_title"></a>

## 清除历史思考（clear\_thinking）

`clear_thinking` 参数用于控制多轮对话中是否将历史轮次的 `reasoning_content`（思考过程）作为上下文输入给模型。仅 GLM 系列模型支持。

-   `true`：忽略历史轮次的 `reasoning_content`，仅使用可见文本、工具调用与结果等非推理内容作为上下文输入，可降低上下文长度与成本。
-   `false`：保留历史轮次的 `reasoning_content` 并随上下文一同提供给模型。若希望启用 Preserved Thinking，必须在 messages 中完整、未修改、按原顺序透传历史 `reasoning_content`，缺失、裁剪、改写或重排会导致效果下降或无法生效。

默认值按模型区分：glm-5.3 的默认值为 `true`，其他 GLM 模型的默认值为 `false`。

> **说明**
>
> 该参数只影响跨轮次的历史思考内容，不改变模型在当前轮次内是否产生/输出思考。

以下示例使用同一组多轮 messages（`assistant` 消息中携带 `reasoning_content`）。设置 `clear_thinking`\=`true` 后，历史思考内容不会被计入上下文，因此 `prompt_tokens` 少于 `false` 的情况，实际数值取决于历史 `reasoning_content` 的长度。

<a id="sec-tabs-22"></a>

<a id="openai兼容-5"></a>

<a id="openai兼容-5-h4"></a>

#### OpenAI兼容

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

Python

<a id="code-code-group-2-python"></a>

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 多轮对话，assistant 消息中携带 reasoning_content（历史思考过程）
messages = [
    {"role": "user", "content": "请计算 15 * 23 是多少？"},
    {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
    {"role": "user", "content": "那再加上 55 呢？"},
    {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
    {"role": "user", "content": "刚才的中间结果是多少？"},
]

completion = client.chat.completions.create(
    model="glm-5.2",
    messages=messages,
    extra_body={
        "enable_thinking": True,
        # true：忽略历史 reasoning_content，降低上下文长度与成本
        # false（默认）：保留历史 reasoning_content（Preserved Thinking）
        "clear_thinking": True,
    },
)
print(completion.usage.prompt_tokens)  # true 时少于 false
```

<a id="fig-code-group-2-curl-tab"></a>

curl

<a id="code-code-group-2-curl"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "glm-5.2",
    "messages": [
        {"role": "user", "content": "请计算 15 * 23 是多少？"},
        {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
        {"role": "user", "content": "那再加上 55 呢？"},
        {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
        {"role": "user", "content": "刚才的中间结果是多少？"}
    ],
    "enable_thinking": true,
    "clear_thinking": true
}'
```

<a id="dashscope-5"></a>

<a id="dashscope-5-h4"></a>

#### DashScope

<a id="code-block-31"></a>

```python
import os
import dashscope

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 多轮对话，assistant 消息中携带 reasoning_content（历史思考过程）
messages = [
    {"role": "user", "content": "请计算 15 * 23 是多少？"},
    {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
    {"role": "user", "content": "那再加上 55 呢？"},
    {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
    {"role": "user", "content": "刚才的中间结果是多少？"},
]

response = client.chat.completions.create(
    model="glm-5.2",
    messages=messages,
    enable_thinking=True,
    # true：忽略历史 reasoning_content，降低上下文长度与成本
    # false（默认）：保留历史 reasoning_content（Preserved Thinking）
    parameters={"clear_thinking": True},
)
print(response.usage.input_tokens)
```

<a id="其它功能"></a>

<a id="d062ed0e4d5fe"></a>

## 其它功能

<table><thead><tr><th><strong>模型</strong></th><th><p><a href="../../model-experience/text-generation-model/multi-round-conversation.md">多轮对话</a></p></th><th><p><a href="../../model-experience/text-generation-model/tool-calls/qwen-function-calling.md#dd5a3dca390k9">Function Calling</a></p></th><th><p><a href="../../model-experience/text-generation-model/qwen-structured-output.md">结构化输出</a></p></th><th><p><a href="../../model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a></p></th><th><p><a href="../../model-experience/text-generation-model/partial-mode.md">前缀续写</a></p></th><th><p><a href="../../model-experience/text-generation-model/context-cache.md">上下文缓存</a></p></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>支持</p><blockquote><p>仅支持 <code>response_format</code> 为 <code>json_object</code></p></blockquote></td><td><p>不支持</p></td><td><p>不支持</p></td><td><p>支持</p><blockquote><p>仅支持隐式缓存</p></blockquote></td></tr><tr><td><p>glm-5.2</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>支持</p><blockquote><p>仅非思考模式</p></blockquote></td><td><p>不支持</p></td><td><p>不支持</p></td><td><p>支持</p><blockquote><p>仅支持隐式缓存</p></blockquote></td></tr><tr><td><p>glm-5.2-fast-preview</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>支持</p><blockquote><p>仅非思考模式</p></blockquote></td><td><p>不支持</p></td><td><p>不支持</p></td><td><p>支持</p><blockquote><p>仅支持隐式缓存</p></blockquote></td></tr><tr><td><p>glm-5.1</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>支持</p><blockquote><p>仅非思考模式</p></blockquote></td><td><p>不支持</p></td><td><p>不支持</p></td><td><p>支持</p><blockquote><p>支持显式与隐式缓存</p></blockquote></td></tr><tr><td><p>glm-5</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>支持</p><blockquote><p>仅非思考模式</p></blockquote></td><td><p>不支持</p></td><td><p>不支持</p></td><td><p>支持</p><blockquote><p>仅支持隐式缓存</p></blockquote></td></tr></tbody></table>

<a id="参数默认值"></a>

<a id="5c21b5ebd7so8"></a>

## 参数默认值

| 模型 | enable\_thinking | temperature | top\_p | top\_k | repetition\_penalty |
| --- | --- | --- | --- | --- | --- |
| glm-5.3 | true（不支持关闭） | 1.0 | 0.95 | 不支持 | 不支持 |
| glm-5.2 | true | 1.0 | 0.95 | 20 | 1.0 |
| glm-5.2-fast-preview | true | 1.0 | 0.95 | 20 | 1.0 |
| glm-5.1 | true | 1.0 | 0.95 | 20 | 1.0 |
| glm-5 | true | 1.0 | 0.95 | 20 | 1.0 |

参数含义请参见[OpenAI兼容-Chat](../../../model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

<a id="注意事项"></a>

<a id="h2-glm-precautions"></a>

## 注意事项

> **警告**
>
> 云上部署的三方开源模型（如 glm-5.2）与模型官方对超参数的处理逻辑不同：模型官方会对超参数进行阈值校验，超出阈值时回退为默认值；云上部署的处理逻辑是直接透传用户传入的参数值，不做阈值校验。因此，不当设置超参数（如将 `repetition_penalty` 设为 `0.1`）可能导致非预期输出（如循环打印）。建议三方开源模型使用默认超参数值（请参见上方参数默认值表），不建议自定义传入。

调用时，请遵循对应 API 的参数类型与必填字段要求，尤其注意：

-   `max_tokens` 必须为整数，例如 `1024`，不要传入布尔值 `true`。调用 glm-5.3 时，`true` 可能被按 `1` 处理，使输出在 1 个 Token 后截断，且不返回参数错误。此时可能只有思考内容，没有最终回答。
-   使用 Anthropic 兼容接口时，`tools` 数组中的每个工具都必须包含 `name`，例如 `"name": "get_weather"`。缺少 `name` 会导致请求失败，请在发送请求前补全工具名称。

<a id="模型列表与计费"></a>

<a id="a1208aad3d0k8"></a>

## 模型列表与计费

GLM 系列模型是智谱AI专为智能体设计的混合推理模型，提供思考与非思考两种模式。

-   glm-5.3：GLM 系列模型，上下文长度 1M，支持 Function Calling、结构化输出及隐式缓存。支持 OpenAI 兼容、DashScope 及 Anthropic 兼容接口调用。
-   glm-5.2：上下文长度 1M，支持 Function Calling、结构化输出及隐式缓存。支持 OpenAI 兼容、DashScope 及 Anthropic 兼容接口调用。
-   glm-5.2-fast-preview：glm-5.2模型的快速模式，详情请参考[优速模式（Prime）](../../model-high-speed-inference/prime-mode.md)。

模型上下文长度与价格信息请参见百炼控制台。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

<a id="错误码"></a>

<a id="2048aa1f92x46"></a>

## 错误码

如果执行报错，请参见[错误码](../../../model-api-reference/preparations/error-code.md)进行解决。

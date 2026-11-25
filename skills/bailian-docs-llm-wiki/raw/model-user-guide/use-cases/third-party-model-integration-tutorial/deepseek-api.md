# DeepSeek-阿里云

本文档介绍如何在阿里云百炼平台通过OpenAI兼容接口或DashScope SDK调用DeepSeek系列模型。

<a id="服务接入地址"></a>

<a id="ds_bu_h2"></a>

## 服务接入地址

不同地域的服务接入地址不同，请根据您选择的地域配置对应的 Base URL（调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../get-started-with-models/regions.md#h2_migrate_domain)）。各地域可调用的模型及限流不同，请参见[限流](../../get-started-with-models/rate-limit.md)文档。

中国香港地域支持以下 DeepSeek 模型：`deepseek-v4.1-flash`、`deepseek-v4.1-flash-1017`、`deepseek-v4-pro-0813` 和 `deepseek-v4-flash-0731`。这四款模型在中国香港地域均支持 Chat Completions、Responses API 和 Anthropic Messages API 调用。

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

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

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
> 以下 DeepSeek 模型均支持 Responses API：`deepseek-v4.1-flash`、`deepseek-v4.1-flash-1017`、`deepseek-v4-pro`、`deepseek-v4-pro-0813`、`deepseek-v4-flash-0731`。各地域实际可调用的模型以该地域的上架情况为准，请参见[限流](../../get-started-with-models/rate-limit.md)。
>
> `deepseek-v4.1-flash-1017` 支持在华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）和中国香港六个地域通过 Responses API 调用，并支持 `web_search`、`web_extractor` 和 `code_interpreter` 三种内置工具。六个地域的 SDK `base_url` 和 `POST` 请求地址见 [Responses API 端点配置](./qwen-api-via-openai-responses)。

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

<a id="中国香港-2"></a>

<a id="中国香港-2-h4"></a>

#### 中国香港

中国香港地域的上述四款模型均支持通过 Responses API 调用。

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="sec-tabs-4"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

HTTP 请求地址：

-   纯文本模型（如deepseek-v4-pro）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（deepseek-v4.1-flash、deepseek-v4.1-flash-1017）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="cn-beijing")`

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

HTTP 请求地址：

-   纯文本模型（如deepseek-v4-pro）：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（deepseek-v4.1-flash、deepseek-v4.1-flash-1017）：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="us-east-1")`

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

HTTP 请求地址：

-   纯文本模型（如deepseek-v4-pro）：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（deepseek-v4.1-flash、deepseek-v4.1-flash-1017）：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="ap-southeast-1")`

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

HTTP 请求地址：

-   纯文本模型（如deepseek-v4-pro）：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（deepseek-v4.1-flash、deepseek-v4.1-flash-1017）：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="eu-central-1")`

<a id="日本-东京-2"></a>

<a id="日本-东京-2-h4"></a>

#### 日本（东京）

HTTP 请求地址：

-   纯文本模型（如deepseek-v4-pro）：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（deepseek-v4.1-flash、deepseek-v4.1-flash-1017）：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="ap-northeast-1")`

<a id="中国香港-3"></a>

<a id="中国香港-3-h4"></a>

#### 中国香港

HTTP 请求地址：

-   纯文本模型（如deepseek-v4-pro）：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（deepseek-v4.1-flash、deepseek-v4.1-flash-1017）：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的`region`：`dashscope.Client(workspace="{WorkspaceId}", region="cn-hongkong")`

<a id="快速开始"></a>

<a id="61623d75547kl"></a>

## 快速开始

deepseek-v4-pro-0813 是 DeepSeek 系列旗舰模型，在编程、数学和通用任务方面表现出色。deepseek-v4-flash-0731 是Flash系列最新版本。您可以通过`enable_thinking`参数在思考与非思考模式之间切换。以下示例以 deepseek-v4-pro 模型为例展示思考模式的调用方式，您可以将 model 参数替换为其他 DeepSeek 模型。

需要已[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](../../../model-api-reference/preparations/install-sdk.md)。

<a id="sec-tabs-5"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-6"></a>

<a id="openai兼容-2"></a>

<a id="openai兼容-2-h4"></a>

#### OpenAI兼容

> **说明**
>
> `enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK通过 `extra_body`传入，Node.js SDK作为顶层参数传入。`reasoning_effort`是 OpenAI 标准参数，可直接作为顶层参数传入。

<a id="sec-tabs-7"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="ddb5892c91y4c"></a>

### 示例代码

<a id="code-block"></a>

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
    model="deepseek-v4-pro",
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
        print("Request ID:", chunk.id)
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

<a id="code-block-2"></a>

```text
====================思考过程====================
嗯，用户问了一个非常简单的自我介绍问题："你是谁"。
我需要明确自己的身份，用简洁友好的方式介绍我是DeepSeek，说明我的创造者、基本特性和可提供的帮助。
想到了可以这样组织回答：先直接表明身份，说明由深度求索公司创造，然后列出一些关键特点（免费、长上下文、文件上传等），最后以友好的邀请结束，询问是否需要帮助。
====================完整回复====================
你好！我是 DeepSeek，由深度求索公司创造的 AI 助手。
我可以帮你解答各种问题、进行文字创作、分析文档、编程辅助等等。我最大的特点是**免费使用**、**超长上下文**（能一次处理整本三体三部曲那么多内容）、支持**文件上传**和**联网搜索**（需手动开启）。
有什么我可以帮你的吗？不管是学习、工作还是日常闲聊，我都很乐意陪你聊聊！
====================Token 消耗====================
CompletionUsage(completion_tokens=238, prompt_tokens=5, total_tokens=243, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=93, rejected_prediction_tokens=None), prompt_tokens_details=None)
Request ID: chatcmpl-a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="25ed2818c5km2"></a>

### 示例代码

<a id="code-block-3"></a>

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
            model: 'deepseek-v4-pro',
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
                console.log('Request ID:', chunk.id);
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

<a id="code-block-4"></a>

```text
====================思考过程====================
嗯，用户问了一个非常简单的自我介绍问题："你是谁"。
我需要明确自己的身份，用简洁友好的方式介绍我是DeepSeek，说明我的创造者、基本特性和可提供的帮助。
想到了可以这样组织回答：先直接表明身份，说明由深度求索公司创造，然后列出一些关键特点（免费、长上下文、文件上传等），最后以友好的邀请结束，询问是否需要帮助。
====================完整回复====================
你好！我是 DeepSeek，由深度求索公司创造的 AI 助手。
我可以帮你解答各种问题、进行文字创作、分析文档、编程辅助等等。我最大的特点是**免费使用**、**超长上下文**（能一次处理整本三体三部曲那么多内容）、支持**文件上传**和**联网搜索**（需手动开启）。
有什么我可以帮你的吗？不管是学习、工作还是日常闲聊，我都很乐意陪你聊聊！
====================Token 消耗====================
{
  prompt_tokens: 5,
  completion_tokens: 243,
  total_tokens: 248,
  completion_tokens_details: { reasoning_tokens: 83 }
}
Request ID: chatcmpl-a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="bcaf8f53f8n2x"></a>

### 示例代码

<a id="sec-tabs-8"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-5"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "deepseek-v4-pro",
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

<a id="sec-tabs-9"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

<a id="07c36189dbqo7"></a>

### 示例代码

<a id="code-block-6"></a>

```python
import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]
completion = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    enable_thinking=True,
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
print("Request ID:", chunk.request_id)
```

<a id="70dc157a528ub"></a>

### 返回结果

<a id="code-block-7"></a>

```text
====================思考过程====================
嗯，用户问了一个非常简单的自我介绍问题："你是谁"。
我需要明确自己的身份，用简洁友好的方式介绍我是DeepSeek，说明我的创造者、基本特性和可提供的帮助。
想到了可以这样组织回答：先直接表明身份，说明由深度求索公司创造，然后列出一些关键特点（免费、长上下文、文件上传等），最后以友好的邀请结束，询问是否需要帮助。
====================完整回复====================
你好！我是 DeepSeek，由深度求索公司创造的 AI 助手。
我可以帮你解答各种问题、进行文字创作、分析文档、编程辅助等等。我最大的特点是**免费使用**、**超长上下文**（能一次处理整本三体三部曲那么多内容）、支持**文件上传**和**联网搜索**（需手动开启）。
有什么我可以帮你的吗？不管是学习、工作还是日常闲聊，我都很乐意陪你聊聊！
====================Token 消耗====================
{"input_tokens": 6, "output_tokens": 240, "total_tokens": 246, "output_tokens_details": {"reasoning_tokens": 92}}
Request ID: 85735883-9062-9c33-a963-0bc12584ee68
```

<a id="java"></a>

<a id="java-h4"></a>

#### Java

<a id="f0fdaa75c28ak"></a>

### 示例代码

> **重要**
>
> DashScope Java SDK版本需要不低于2.19.4。

<a id="code-block-8"></a>

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
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
public class Main {
    static {
        // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    private static String requestId = "";
    private static void handleGenerationResult(GenerationResult message) {
        requestId = message.getRequestId();
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
                .model("deepseek-v4-pro")
                .enableThinking(true)
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
            System.out.println("\nRequest ID: " + requestId);
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("An exception occurred: " + e.getMessage());
        }
    }
}
```

<a id="e91b400fc67bu"></a>

### 返回结果

<a id="code-block-9"></a>

```text
====================思考过程====================
嗯，用户问了一个非常简单的自我介绍问题："你是谁"。
我需要明确自己的身份，用简洁友好的方式介绍我是DeepSeek，说明我的创造者、基本特性和可提供的帮助。
想到了可以这样组织回答：先直接表明身份，说明由深度求索公司创造，然后列出一些关键特点（免费、长上下文、文件上传等），最后以友好的邀请结束，询问是否需要帮助。
====================完整回复====================
你好！我是 DeepSeek，由深度求索公司创造的 AI 助手。
我可以帮你解答各种问题、进行文字创作、分析文档、编程辅助等等。我最大的特点是**免费使用**、**超长上下文**（能一次处理整本三体三部曲那么多内容）、支持**文件上传**和**联网搜索**（需手动开启）。
有什么我可以帮你的吗？不管是学习、工作还是日常闲聊，我都很乐意陪你聊聊！
```

<a id="http-2"></a>

<a id="http-2-h4"></a>

#### HTTP

<a id="1b4ac400b5f33"></a>

### 示例代码

<a id="sec-tabs-10"></a>

<a id="curl-2"></a>

<a id="curl-2-h4"></a>

#### curl

<a id="code-block-10"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "deepseek-v4-pro",
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

鉴权方式：通过 `x-api-key` 请求头或 `Authorization: Bearer` 请求头传入百炼 API Key，二者选其一即可。思考模式等参数的详细说明请参见[Anthropic兼容-Messages](../../../model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

<a id="sec-tabs-11"></a>

<a id="python-3"></a>

<a id="python-3-h4"></a>

#### Python

<a id="ds_anthropic_py_code_h3"></a>

### 示例代码

<a id="code-block-11"></a>

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
    model="deepseek-v4-pro",
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

<a id="ds_anthropic_curl_code_h3"></a>

### 示例代码

<a id="sec-tabs-12"></a>

<a id="curl-3"></a>

<a id="curl-3-h4"></a>

#### curl

<a id="code-block-12"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "anthropic-version: 2023-06-01" \
-d '{
    "model": "deepseek-v4-pro",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": "你是谁"
        }
    ]
}'
```

<a id="中国香港-4"></a>

<a id="中国香港-4-h4"></a>

#### 中国香港

以下示例使用 `deepseek-v4.1-flash-1017` 通过 OpenAI兼容的 Chat Completions API 调用中国香港地域。请使用中国香港地域的 API Key，并将 `{WorkspaceId}` 替换为中国香港地域的业务空间 ID。各地域的 API Key 和业务空间专属域名不能混用。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="deepseek-v4.1-flash-1017",
    messages=[{"role": "user", "content": "你是谁"}],
)

print(completion.choices[0].message.content)
```

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "deepseek-v4.1-flash-1017",
  "messages": [{"role": "user", "content": "你是谁"}]
}'
```

DashScope 和 Responses API 的香港接入地址见[服务接入地址](#ds_bu_h2)。使用 Anthropic Messages API 时，SDK 的 `base_url` 配置为 `https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/apps/anthropic`，HTTP 请求地址为 `POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/apps/anthropic/v1/messages`。

<a id="推理强度-reasoning-effort"></a>

<a id="re_section_title"></a>

## 推理强度（reasoning\_effort）

deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-flash-0731 和 deepseek-v4-pro-0813默认开启思考模式。通过`reasoning_effort`参数可以调整推理强度，可选值为`low(仅deepseek-v4.1-flash、deepseek-v4-flash-0731 和 deepseek-v4-pro-0813 支持)`、`high`和`max`，默认为`high`。

<a id="sec-tabs-13"></a>

<a id="openai兼容-3"></a>

<a id="openai兼容-3-h4"></a>

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
completion = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
    reasoning_effort="high",
)
print(completion.choices[0].message.content)
```

<a id="fig-code-group-2-node-js-tab"></a>

Node.js

<a id="code-code-group-2-node-js"></a>

```javascript
import OpenAI from "openai";
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});
const completion = await openai.chat.completions.create({
    model: "deepseek-v4-pro",
    messages: [{ role: "user", content: "9.9和9.11哪个大" }],
    reasoning_effort: "high",
});
console.log(completion.choices[0].message.content);
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
    "model": "deepseek-v4-pro",
    "messages": [{"role": "user", "content": "9.9和9.11哪个大"}],
    "reasoning_effort": "high"
}'
```

<a id="dashscope-3"></a>

<a id="dashscope-3-h4"></a>

#### DashScope

<a id="code-block-13"></a>

```python
import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
    parameters={"reasoning_effort": "high"},
)
print(response.choices[0].message.content)
```

<a id="responses-api"></a>

<a id="ds_resp_h2"></a>

## Responses API

`deepseek-v4.1-flash`、`deepseek-v4.1-flash-1017`、`deepseek-v4-pro`、`deepseek-v4-pro-0813`、`deepseek-v4-flash-0731` 均支持通过 OpenAI 兼容的 Responses API 调用，各地域实际可调用的模型以该地域的上架情况为准，服务接入地址参见[服务接入地址](deepseek-api.md#ds_bu_h2)。

`deepseek-v4.1-flash-1017` 支持在华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）和中国香港六个地域通过 Responses API 调用，并支持 `web_search`、`web_extractor` 和 `code_interpreter` 三种内置工具。六个地域的 SDK `base_url` 和 `POST` 请求地址见 [Responses API 端点配置](./qwen-api-via-openai-responses)。

通过 Responses API 调用时，可在`tools`参数中添加`web_search`（[联网搜索](../../model-experience/text-generation-model/tool-calls/web-search.md)）、`web_extractor`（[网页抓取](../../model-experience/text-generation-model/tool-calls/web-extractor.md)）与`code_interpreter`（[代码解释器](../../model-experience/text-generation-model/tool-calls/qwen-code-interpreter.md)）工具。

<a id="其它功能"></a>

<a id="d062ed0e4d5fe"></a>

## 其它功能

| 模型 | [多轮对话](../../model-experience/text-generation-model/multi-round-conversation.md) | [Function Calling](../../model-experience/text-generation-model/tool-calls/qwen-function-calling.md#dd5a3dca390k9) | [联网搜索](../../model-experience/text-generation-model/tool-calls/web-search.md) | [上下文缓存](../../model-experience/text-generation-model/context-cache.md) | [结构化输出](../../model-experience/text-generation-model/qwen-structured-output.md) | [前缀续写](../../model-experience/text-generation-model/partial-mode.md) |
| --- | --- | --- | --- | --- | --- | --- |
| deepseek-v4.1-flash-1017 | 支持 | 支持 | 支持 | 支持（隐式缓存） | 支持 | 不支持 |
| deepseek-v4.1-flash | 支持 | 支持 | 支持 | 支持 | 支持 | 不支持 |
| deepseek-v4-pro | 支持 | 支持 | 支持 | 支持 | 支持 | 不支持 |
| deepseek-v4-flash-0731 | 支持 | 支持 | 支持 | 支持 | 支持 JSON Object，不支持 JSON Schema | 不支持 |
| 蒸馏模型 | 支持 | 不支持 | 不支持 | 不支持 | 不支持 | 不支持 |

`deepseek-v4.1-flash-1017` 支持 OpenAI 兼容的 Chat Completions API、Anthropic Messages API 和思考；不支持 Batch 调用或微调。

<a id="参数默认值"></a>

<a id="5c21b5ebd7so8"></a>

## 参数默认值

<table><thead><tr><th><p><strong>模型</strong></p></th><th><p><strong>temperature</strong></p></th><th><p><strong>top_p</strong></p></th><th><p><strong>repetition_penalty</strong></p></th><th><p><strong>presence_penalty</strong></p></th><th><p><strong>max_tokens</strong></p></th><th><p><strong>thinking_budget</strong></p></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p></td><td><p>1.0</p></td><td><p>1.0</p></td><td><p>-</p></td><td><p>-</p></td><td><p>393,216</p></td><td><p>-</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>1.0</p></td><td><p>1.0</p></td><td><p>-</p></td><td><p>-</p></td><td><p>393,216</p></td><td><p>-</p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>1.0</p></td><td><p>1.0</p></td><td><p>-</p></td><td><p>-</p></td><td colspan="2"><p>共393,216</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>1.0</p></td><td><p>1.0</p></td><td><p>-</p></td><td><p>-</p></td><td colspan="2"><p>共393,216</p></td></tr><tr><td><p>蒸馏版</p></td><td><p>0.6</p></td><td><p>0.95</p></td><td><p>-</p></td><td><p>1</p></td><td><p>16,384</p></td><td><p>16,384</p></td></tr></tbody></table>

-   “-” 表示没有默认值，也不支持设置。
-   蒸馏版模型不支持设置以上参数值。
-   “共393,216” 表示 deepseek-v4 系列模型的 max\_tokens 与 thinking\_budget 共用同一上限，两者合计最大为 393,216 Token（即模型的最大输出长度）。
-   参数含义请参考[OpenAI兼容-Chat](../../../model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

<a id="模型列表与计费"></a>

<a id="a1208aad3d0k8"></a>

## 模型列表与计费

-   混合思考模型（通过`enable_thinking`参数控制是否思考）：deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-flash-0731

deepseek-v4-pro 在编程、数学和通用任务方面表现出色，deepseek-v4-flash-0731 快速且经济高效，推荐优先使用 deepseek-v4-pro。

模型上下文长度与价格信息请参见百炼控制台。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

<a id="常见问题"></a>

<a id="b654fdb6bblx9"></a>

## 常见问题

<a id="免费额度用完后如何购买-token"></a>

<a id="1dcb37c8abu4v"></a>

### 免费额度用完后如何购买 Token？

访问[费用与成本](https://usercenter2.aliyun.com/home)中心进行充值，确保您的账户没有欠费即可调用 DeepSeek 模型。

> 调用 DeepSeek 模型会自动扣费，出账周期为分钟级，消费明细请前往 [**账单详情**](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance) 进行查看。

<a id="如何接入chatbox-cherry-studio或dify"></a>

<a id="59f8901b12i0l"></a>

### 如何接入[Chatbox](https://chatboxai.app/zh)、[Cherry Studio](https://cherry-ai.com/)或[Dify](https://cloud.dify.ai/apps)？

此处以常用工具为例进行说明，其它大模型工具的接入方式类似。

<a id="sec-tabs-14"></a>

<a id="chatbox"></a>

<a id="chatbox-h4"></a>

#### Chatbox

请参见[Chatbox](https://help.aliyun.com/zh/model-studio/cline-tool)。

<a id="cherry-studio"></a>

<a id="cherry-studio-h4"></a>

#### Cherry Studio

请参见[Cherry Studio](../../../token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md)。

<a id="dify"></a>

<a id="dify-h4"></a>

#### Dify

请参见[Dify](https://help.aliyun.com/zh/model-studio/dify)。

<a id="可以上传图片或文档进行提问吗"></a>

<a id="9d90a652dafnp"></a>

### 可以上传图片或文档进行提问吗？

`deepseek-v4.1-flash` 与 `deepseek-v4.1-flash-1017` 支持文本和图片输入，输出文本。其他模型的输入模态以对应模型信息页为准。图片输入也可使用[千问VL](../../model-experience/text-generation-model/vision.md)模型；文档输入可使用[Qwen-Long](../../model-experience/text-generation-model/specialized-models/long-context-qwen-long.md)模型。

<a id="如何查看token消耗量及调用次数"></a>

<a id="444fa1ec318e3"></a>

### 如何查看Token消耗量及调用次数？

模型调用发生后**分钟级**即可在监控图表查看。登录[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)页面，在左侧导航栏选择**运维管理** > **模型监控**进入监控概览页，设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**查看详情**，即可查看该模型的调用统计结果。具体请参见[监控告警](../../model-monitoring/model-telemetry.md)文档。

> 监控数据按分钟级更新，仅供参考，不作为计费依据。

<a id="还有哪些使用deepseek的方式"></a>

<a id="88f16b606426d"></a>

### 还有哪些使用DeepSeek的方式？

在百炼平台使用DeepSeek有三种方式：

1.  在线体验：访问[模型广场](https://bailian.console.aliyun.com/model/market)。
2.  通过API或客户端（如Chatbox）调用模型：请参考本文内容。
3.  0代码构建大模型应用：请参考[智能体应用（Agent 1.0）](../../../application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)或[工作流应用](../../../application-user-guide/agent-development/llm-application/workflow-application.md)。

如需自行部署DeepSeek，请参考[技术解决方案](https://www.aliyun.com/solution/tech-solution/deepseek-r1-for-platforms)。

<a id="错误码"></a>

<a id="2048aa1f92x46"></a>

## 错误码

如果执行报错，请参见[错误码](../../../model-api-reference/preparations/error-code.md)进行解决。

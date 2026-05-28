# Kimi

本文档介绍如何调用阿里云百炼部署的 Kimi 模型推理服务。

**支持的地域：**华北2（北京）、美国（弗吉尼亚）、德国（法兰克福）。

**模型体验：**您可以前往[模型体验中心](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/text)体验 Kimi 模型效果。

不同地域的服务接入地址不同，请根据您选择的地域配置对应的 Base URL。

## OpenAI兼容

## 华北2（北京）

SDK 调用配置的`base_url`：`https://dashscope.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

## 美国（弗吉尼亚）

SDK 调用配置的`base_url`：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions`

## 德国（法兰克福）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

## DashScope

## 华北2（北京）

纯文本模型（如 kimi-k2-thinking）的 HTTP 请求地址为`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

多模态模型（如 kimi-k2.5、kimi-k2.6）的 HTTP 请求地址为`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用无需配置 `base_url`。

## 美国（弗吉尼亚）

纯文本模型（如 kimi-k2-thinking）的 HTTP 请求地址为`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

多模态模型（如 kimi-k2.5、kimi-k2.6）的 HTTP 请求地址为`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

## **Python代码**

```
dashscope.base_http_api_url = 'https://dashscope-us.aliyuncs.com/api/v1'
```

## **Java代码**

-   **方式一：**
    
    ```
    import com.alibaba.dashscope.protocol.Protocol;
    Generation gen = new Generation(Protocol.HTTP.getValue(), “https://dashscope-us.aliyuncs.com/api/v1");
    ```
    
-   **方式二：**
    
    ```
    import com.alibaba.dashscope.utils.Constants;
    Constants.baseHttpApiUrl="https://dashscope-us.aliyuncs.com/api/v1";
    ```
    

## 德国（法兰克福）

纯文本模型（如 kimi-k2-thinking）的 HTTP 请求地址为`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

多模态模型（如 kimi-k2.5、kimi-k2.6）的 HTTP 请求地址为`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

SDK调用配置的`base_url`：

## **Python代码**

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1'
```

## **Java代码**

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

-   **方式一：**
    
    ```
    import com.alibaba.dashscope.protocol.Protocol;
    Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1");
    ```
    
-   **方式二：**
    
    ```
    import com.alibaba.dashscope.utils.Constants;
    Constants.baseHttpApiUrl="https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";
    ```
    

> 你需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)。

## **快速开始**

以下为纯文本输入示例。多模态示例请参见[多模态调用示例](#af95c67524)。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi-k2-thinking",
    messages=[{"role": "user", "content": "你是谁"}],
    stream=True,
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if chunk.choices:
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

### **返回结果**

```
====================思考过程====================

用户问"你是谁"，这是一个关于身份的直接问题。我需要根据我的实际身份如实回答。

我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，我的名字是Kimi。我应该清晰、简洁地介绍自己，包括：
1. 我的身份：AI助手
2. 我的开发者：月之暗面科技有限公司（Moonshot AI）
3. 我的名字：Kimi
4. 我的核心能力：长文本处理、智能对话、文件处理、搜索等

我应该保持友好、专业的语气，避免过于技术化的术语，让普通用户也能理解。同时，我应该强调我是一个AI，没有个人意识、情感或个人经历。

回答结构：
- 直接回答身份
- 说明开发者
- 简要介绍核心能力
- 保持简洁明了
====================完整回复====================

我是由月之暗面科技有限公司（Moonshot AI）开发的AI助手，名叫Kimi。我基于混合专家（MoE）架构，具备超长上下文理解、智能对话、文件处理、代码生成和复杂任务推理等能力。有什么可以帮您的吗？
```

## Node.js

```
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    const messages = [{ role: 'user', content: '你是谁' }];

    const stream = await openai.chat.completions.create({
        model: 'kimi-k2-thinking',
        messages,
        stream: true,
    });

    console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

    for await (const chunk of stream) {
        if (chunk.choices?.length) {
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
    }
}

main();
```

### **返回结果**

```
====================思考过程====================

用户问"你是谁"，这是一个关于身份的直接问题。我需要根据我的实际身份如实回答。

我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，我的名字是Kimi。我应该清晰、简洁地介绍自己，包括：
1. 我的身份：AI助手
2. 我的开发者：月之暗面科技有限公司（Moonshot AI）
3. 我的名字：Kimi
4. 我的核心能力：长文本处理、智能对话、文件处理、搜索等

我应该保持友好、专业的语气，避免过于技术化的术语，让普通用户也能轻松理解。同时，我应该强调我是一个AI，没有个人意识、情感或个人经历，以避免误解。

回答结构：
- 直接回答身份
- 说明开发者
- 简要介绍核心能力
- 保持简洁明了
====================完整回复====================

我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，名叫 Kimi。

我擅长：
- 长文本理解与生成
- 智能对话和问答
- 文件处理与分析
- 信息检索与整合

作为一个AI助手，我没有个人意识、情感或经历，但会尽力为您提供准确、有用的帮助。有什么可以帮您的吗？
```

## HTTP

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "kimi-k2-thinking",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ]
}'
```

### **返回结果**

```
{
    "choices": [
        {
            "message": {
                "content": "我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，名叫 Kimi。我擅长处理长文本、智能对话、文件分析、编程辅助和复杂任务推理，可以帮助您回答问题、创作内容、分析文档等。有什么我可以帮您的吗？",
                "reasoning_content": "用户问\"你是谁\"，这是一个关于身份的直接问题。我需要根据我的实际身份如实回答。\n\n我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，我的名字是Kimi。我应该清晰、简洁地介绍自己，包括：\n1. 我的身份：AI助手\n2. 我的开发者：月之暗面科技有限公司（Moonshot AI）\n3. 我的名字：Kimi\n4. 我的核心能力：长文本处理、智能对话、文件处理、搜索等\n\n我应该保持友好、专业的语气，同时提供有用信息。不需要过度复杂化，直接回答即可。",
                "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 8,
        "completion_tokens": 183,
        "total_tokens": 191
    },
    "created": 1762753998,
    "system_fingerprint": null,
    "model": "kimi-k2-thinking",
    "id": "chatcmpl-485ab490-90ec-48c3-85fa-1c732b683db2"
}
```

## DashScope

> 以下 DashScope 示例使用 `text-generation` 端点，仅适用于纯文本模型（kimi-k2-thinking、Moonshot-Kimi-K2-Instruct）。多模态模型（kimi-k2.5、kimi-k2.6）需使用 `multimodal-generation` 端点，请参见[多模态调用示例](#af95c67524)。

## Python

```
import os
from dashscope import Generation

# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]

completion = Generation.call(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="kimi-k2-thinking",
    messages=messages,
    result_format="message",  # 设置结果格式为 message
    stream=True,              # 开启流式输出
    incremental_output=True,  # 开启增量输出
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    message = chunk.output.choices[0].message
    
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

# 循环结束后，reasoning_content 和 answer_content 变量中包含了完整的内容
# 您可以在这里根据需要进行后续处理
# print(f"\n\n完整思考过程:\n{reasoning_content}")
# print(f"\n完整回复:\n{answer_content}")
```

### **返回结果**

```
====================思考过程====================

用户问"你是谁？"，这是一个关于身份的直接问题。我需要根据我的实际身份如实回答。

我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，我的名字是Kimi。我应当清晰、简洁地说明这一点。

需要包含的关键信息：
1. 我的名称：Kimi
2. 我的开发者：月之暗面科技有限公司（Moonshot AI）
3. 我的本质：人工智能助手
4. 我可以提供帮助：回答问题、协助创作等

我应该保持友好和乐于助人的语气，同时准确说明我的身份。我不应该假装是人类或具有个人身份。

一个合适的回答可以是：
"我是Kimi，由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手。我可以帮助你回答问题、进行创作、分析文档等多种任务。有什么我可以帮你的吗？"

这个回答直接、准确，并且邀请用户进一步互动。
====================完整回复====================

我是Kimi，由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手。我可以帮助你回答问题、进行创作、分析文档等多种任务。有什么我可以帮你的吗？
```

## Java

```
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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (reasoning!= null&&!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (content!= null&&!content.isEmpty()) {
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
                .model("kimi-k2-thinking")
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
            // 打印最终结果
            // if (reasoningContent.length() > 0) {
            //     System.out.println("\n====================完整回复====================");
            //     System.out.println(finalContent.toString());
            // }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
====================思考过程====================
用户问"你是谁？"，这是一个关于身份的直接问题。我需要根据我的实际身份如实回答。

我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，我的名字是Kimi。我应当清晰、简洁地说明这一点。

回答应该包括：
1. 我的身份：AI助手
2. 我的开发者：月之暗面科技有限公司（Moonshot AI）
3. 我的名字：Kimi
4. 我的核心能力：长文本处理、智能对话、文件处理等

我不应该假装是人类，也不应该提供过多技术细节，只需给出清晰、友好的回答即可。
====================完整回复====================
我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，名叫 Kimi。我擅长处理长文本、进行智能对话、解答问题、辅助创作，还能帮您分析和处理文件。有什么可以帮您的吗？
```

## HTTP

## curl

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "kimi-k2-thinking",
    "input":{
        "messages":[      
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

### **返回结果**

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": "我是Kimi，由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手。我可以帮助你回答问题、进行创作、分析文档、编写代码等。有什么可以帮你的吗？",
                    "reasoning_content": "用户问\"你是谁？\"，这是一个关于身份的直接问题。我需要根据我的实际身份如实回答。\n\n我是由月之暗面科技有限公司（Moonshot AI）开发的人工智能助手，我的名字是Kimi。我应当清晰、简洁地说明这一点。\n\n需要包含的关键信息：\n1. 我的名称：Kimi\n2. 我的开发者：月之暗面科技有限公司（Moonshot AI）\n3. 我的本质：人工智能助手\n4. 我可以提供帮助：回答问题、协助创作等\n\n我应该以友好、直接的方式回应，使用户容易理解。",
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 9,
        "output_tokens": 156,
        "total_tokens": 165
    },
    "request_id": "709a0697-ed1f-4298-82c9-a4b878da1849"
}
```

## **多模态调用示例**

kimi-k2.5、kimi-k2.6 支持同时处理文本、图像或视频输入，并可通过 `enable_thinking` 参数开启思考模式。以下示例展示如何调用多模态能力。

### **开启或关闭思考模式**

kimi-k2.5、kimi-k2.6属于混合思考模型，模型可以在思考后回复，也可直接回复；通过`enable_thinking`参数控制是否开启思考模式：

-   `true`：开启思考模式
    
-   `false`（默认）：关闭思考模式
    

kimi-k2.6 支持通过 `preserve_thinking` 参数在多轮对话中传递思考过程，详情请参见[传递思考过程](https://help.aliyun.com/zh/model-studio/deep-thinking#jln7docdq5et5)。

以下示例展示如何使用图像 URL 并开启思考模式，支持单图输入（主示例）和多图输入（注释代码）。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 单图传入示例（开启思考模式）
completion = client.chat.completions.create(
    model="kimi-k2.6",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "图中描绘的是什么景象?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                }
            ]
        }
    ],
    extra_body={"enable_thinking":True}  # 开启思考模式
)

# 输出思考过程
if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    print(completion.choices[0].message.reasoning_content)

# 输出回复内容
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
print(completion.choices[0].message.content)

# 多图传入示例（开启思考模式，取消注释使用）
# completion = client.chat.completions.create(
#     model="kimi-k2.6",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "这些图描绘了什么内容？"},
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}
#                 }
#             ]
#         }
#     ],
#     extra_body={"enable_thinking":True}
# )
#
# # 输出思考过程和回复
# if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
#     print("\n思考过程：\n" + completion.choices[0].message.reasoning_content)
# print("\n完整回复：\n" + completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

// 单图传入示例（开启思考模式）
const completion = await openai.chat.completions.create({
    model: 'kimi-k2.6',
    messages: [
        {
            role: 'user',
            content: [
                { type: 'text', text: '图中描绘的是什么景象?' },
                {
                    type: 'image_url',
                    image_url: {
                        url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg'
                    }
                }
            ]
        }
    ],
    enable_thinking: true  // 开启思考模式
});

// 输出思考过程
if (completion.choices[0].message.reasoning_content) {
    console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
    console.log(completion.choices[0].message.reasoning_content);
}

// 输出回复内容
console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
console.log(completion.choices[0].message.content);

// 多图传入示例（开启思考模式，取消注释使用）
// const multiCompletion = await openai.chat.completions.create({
//     model: 'kimi-k2.6',
//     messages: [
//         {
//             role: 'user',
//             content: [
//                 { type: 'text', text: '这些图描绘了什么内容？' },
//                 {
//                     type: 'image_url',
//                     image_url: { url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg' }
//                 },
//                 {
//                     type: 'image_url',
//                     image_url: { url: 'https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png' }
//                 }
//             ]
//         }
//     ],
//     enable_thinking: true
// });
//
// // 输出思考过程和回复
// if (multiCompletion.choices[0].message.reasoning_content) {
//     console.log('\n思考过程：\n' + multiCompletion.choices[0].message.reasoning_content);
// }
// console.log('\n完整回复：\n' + multiCompletion.choices[0].message.content);
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "kimi-k2.6",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "图中描绘的是什么景象?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                }
            ]
        }
    ],
    "enable_thinking": true
}'

# 多图输入示例（取消注释使用）
# curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
# -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
# -H "Content-Type: application/json" \
# -d '{
#     "model": "kimi-k2.6",
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "这些图描绘了什么内容？"
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
#                     }
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
#                     }
#                 }
#             ]
#         }
#     ],
#     "enable_thinking": true,
#     "stream": false
# }'
```

## DashScope

## Python

```
import os
from dashscope import MultiModalConversation

# 单图传入示例（开启思考模式）
response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="kimi-k2.6",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "图中描绘的是什么景象?"},
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}
            ]
        }
    ],
    enable_thinking=True  # 开启思考模式
)

# 输出思考过程
if hasattr(response.output.choices[0].message, 'reasoning_content') and response.output.choices[0].message.reasoning_content:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    print(response.output.choices[0].message.reasoning_content)

# 输出回复内容
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
print(response.output.choices[0].message.content[0]["text"])

# 多图传入示例（开启思考模式，取消注释使用）
# response = MultiModalConversation.call(
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     model="kimi-k2.6",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"text": "这些图描绘了什么内容？"},
#                 {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
#                 {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}
#             ]
#         }
#     ],
#     enable_thinking=True
# )
#
# # 输出思考过程和回复
# if hasattr(response.output.choices[0].message, 'reasoning_content') and response.output.choices[0].message.reasoning_content:
#     print("\n思考过程：\n" + response.output.choices[0].message.reasoning_content)
# print("\n完整回复：\n" + response.output.choices[0].message.content[0]["text"])
```

## Java

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class KimiK26MultiModalExample {
    public static void main(String[] args) {
        try {
            // 单图输入示例（开启思考模式）
            MultiModalConversation conv = new MultiModalConversation();

            // 构建消息内容
            Map<String, Object> textContent = new HashMap<>();
            textContent.put("text", "图中描绘的是什么景象?");

            Map<String, Object> imageContent = new HashMap<>();
            imageContent.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg");

            MultiModalMessage userMessage = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(textContent, imageContent))
                    .build();

            // 构建请求参数
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 若没有配置环境变量，请用阿里云百炼API Key替换
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("kimi-k2.6")
                    .messages(Arrays.asList(userMessage))
                    .enableThinking(true)  // 开启思考模式
                    .build();

            // 调用模型
            MultiModalConversationResult result = conv.call(param);

            // 输出结果
            String content = result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text");
            System.out.println("回复内容: " + content);

            // 如果开启了思考模式，输出思考过程
            if (result.getOutput().getChoices().get(0).getMessage().getReasoningContent() != null) {
                System.out.println("\n思考过程: " +
                    result.getOutput().getChoices().get(0).getMessage().getReasoningContent());
            }

            // 多图输入示例（取消注释使用）
            // Map<String, Object> imageContent1 = new HashMap<>();
            // imageContent1.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg");
            // Map<String, Object> imageContent2 = new HashMap<>();
            // imageContent2.put("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png");
            //
            // Map<String, Object> textContent2 = new HashMap<>();
            // textContent2.put("text", "这些图描绘了什么内容？");
            //
            // MultiModalMessage multiImageMessage = MultiModalMessage.builder()
            //         .role(Role.USER.getValue())
            //         .content(Arrays.asList(textContent2, imageContent1, imageContent2))
            //         .build();
            //
            // MultiModalConversationParam multiParam = MultiModalConversationParam.builder()
            //         .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            //         .model("kimi-k2.6")
            //         .messages(Arrays.asList(multiImageMessage))
            //         .enableThinking(true)
            //         .build();
            //
            // MultiModalConversationResult multiResult = conv.call(multiParam);
            // System.out.println(multiResult.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("调用失败: " + e.getMessage());
        }
    }
}
```

## curl

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "kimi-k2.6",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "图中描绘的是什么景象?"
                    },
                    {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "enable_thinking": true
    }
}'

# 多图输入示例（取消注释使用）
# curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
# -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
# -H "Content-Type: application/json" \
# -d '{
#     "model": "kimi-k2.6",
#     "input": {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "text": "这些图描绘了什么内容？"
#                     },
#                     {
#                         "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
#                     },
#                     {
#                         "image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
#                     }
#                 ]
#             }
#         ]
#     },
#     "parameters": {
#         "enable_thinking": true
#     }
# }'
```

### **视频理解**

## 视频文件

kimi-k2.5、kimi-k2.6模型通过从视频中提取帧序列进行内容分析。您可以通过以下两个参数控制抽帧策略：

-   **fps**：控制抽帧频率，每隔 fps1​秒抽取一帧。取值范围为 \[0.1, 10\]，默认值为 2.0。
    
    -   高速运动场景：建议设置较高的 fps 值，以捕捉更多细节
        
    -   静态或长视频：建议设置较低的 fps 值，以提高处理效率
        
-   **max\_frames**：限制视频抽取帧的上限，默认值和最大值均为2000。
    
    当按 fps 计算的总帧数超过此限制时，系统将自动在 max\_frames 内均匀抽帧。**此参数仅在使用 DashScope SDK 时可用。**
    

## OpenAI兼容

> 使用OpenAI SDK或HTTP方式向模型直接输入视频文件时，需要将用户消息中的`"type"`参数设为`"video_url"`。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi-k2.6",
    messages=[
        {
            "role": "user",
            "content": [
                # 直接传入视频文件时，请将type的值设置为video_url
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    "fps": 2
                },
                {
                    "type": "text",
                    "text": "这段视频的内容是什么?"
                }
            ]
        }
    ]
)

print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "kimi-k2.6",
        messages: [
            {
                role: "user",
                content: [
                    // 直接传入视频文件时，请将type的值设置为video_url
                    {
                        type: "video_url",
                        video_url: {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        },
                        "fps": 2
                    },
                    {
                        type: "text",
                        text: "这段视频的内容是什么?"
                    }
                ]
            }
        ]
    });

    console.log(response.choices[0].message.content);
}

main();
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "kimi-k2.6",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            },
            "fps":2
          },
          {
            "type": "text",
            "text": "这段视频的内容是什么?"
          }
        ]
      }
    ]
  }'
```

## DashScope

## Python

```
import dashscope
import os

dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [
    {"role": "user",
        "content": [
            # fps 可参数控制视频抽帧频率，表示每隔 1/fps 秒抽取一帧
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
            {"text": "这段视频的内容是什么?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='kimi-k2.6',
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        // fps 可参数控制视频抽帧频率，表示每隔 1/fps 秒抽取一帧
        Map<String, Object> params = new HashMap<>();
        params.put("video", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4");
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        params,
                        Collections.singletonMap("text", "这段视频的内容是什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("kimi-k2.6")
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "kimi-k2.6",
    "input":{
        "messages":[
            {"role": "user","content": [{"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
            {"text": "这段视频的内容是什么?"}]}]}
}'
```

## 图像列表

当视频以图像列表（即预先抽取的视频帧）传入时，可通过`fps`参数告知模型视频帧之间的时间间隔，这能帮助模型更准确地理解事件的顺序、持续时间和动态变化。模型支持通过 `fps` 参数指定原始视频的抽帧率，表示视频帧是每隔fps1​秒从原始视频中抽取的。

## OpenAI兼容

> 使用OpenAI SDK或HTTP方式向模型输入图片列表形式的视频时，需要将用户消息中的`"type"`参数设为`"video"`。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi-k2.6", 
    messages=[{"role": "user","content": [
        # 传入图像列表时，用户消息中的"type"参数为"video"
         {"type": "video","video": [
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
         "fps":2},
         {"type": "text","text": "描述这个视频的具体过程"},
    ]}]
)

print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "kimi-k2.6",  
        messages: [{
            role: "user",
            content: [
                {
                    // 传入图像列表时，用户消息中的"type"参数为"video"
                    type: "video",
                    video: [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                        "fps":2
                },
                {
                    type: "text",
                    text: "描述这个视频的具体过程"
                }
            ]
        }]
    });
    console.log(response.choices[0].message.content);
}

main();
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "kimi-k2.6",
    "messages": [{"role": "user","content": [{"type": "video","video": [
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                  "fps":2},
                {"type": "text","text": "描述这个视频的具体过程"}]}]
}'
```

## DashScope

## Python

```
import os
import dashscope

dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [{"role": "user",
             "content": [
                 {"video":["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                   "fps":2},
                 {"text": "描述这个视频的具体过程"}]}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='kimi-k2.6', 
    messages=messages
)
print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
// DashScope SDK版本需要不低于2.21.10
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static final String MODEL_NAME = "kimi-k2.6"; 
    public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"));
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL_NAME)
                .messages(Arrays.asList(userMessage)).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "kimi-k2.6",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
            ],
            "fps":2
                 
          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```

### **传入本地文件**

以下示例展示如何传入本地文件。OpenAI 兼容接口仅支持 Base64 编码方式，DashScope 同时支持 Base64 编码和文件路径两种方式。

## **OpenAI兼容**

Base64 编码方式传入需要构建 [Data URL](https://www.rfc-editor.org/rfc/rfc2397)，构建方法请参见[构建 Data URL](https://help.aliyun.com/zh/model-studio/vision#6f3db6f231evb)。

## Python

```
from openai import OpenAI
import os
import base64

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

client = OpenAI(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="kimi-k2.6",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        }
    ],
)
print(completion.choices[0].message.content)

# 以下为传入本地视频文件、本地图像列表的示例

# 【本地视频文件】将本地视频编码为 Data URL 后传入 video_url：
#   def encode_video_to_data_url(video_path):
#       with open(video_path, "rb") as f:
#           return "data:video/mp4;base64," + base64.b64encode(f.read()).decode("utf-8")

#   video_data_url = encode_video_to_data_url("xxx/local.mp4")
#   content = [{"type": "video_url", "video_url": {"url": video_data_url}, "fps": 2}, {"type": "text", "text": "这段视频的内容是什么?"}]

# 【本地图像列表】将多张本地图片分别 Base64 后组成 video 列表传入：
#   image_data_urls = [f"data:image/jpeg;base64,{encode_image(p)}" for p in ["xxx/f1.jpg", "xxx/f2.jpg", "xxx/f3.jpg", "xxx/f4.jpg"]]
#   content = [{"type": "video", "video": image_data_urls, "fps": 2}, {"type": "text", "text": "描述这个视频的具体过程"}]
```

## Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
  };
// 将xxx/eagle.png替换为你本地图像的绝对路径
const base64Image = encodeImage("xxx/eagle.png")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "kimi-k2.6", 
        messages: [
            {"role": "user",
             "content": [{"type": "image_url",
                        "image_url": {"url": `data:image/png;base64,${base64Image}`},},
                        {"type": "text", "text": "图中描绘的是什么景象?"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();

// 以下为传入本地视频文件、本地图像列表示例

// 【本地视频文件】将本地视频编码为 Data URL 后传入 video_url：
//   const encodeVideoToDataUrl = (videoPath) => "data:video/mp4;base64," + readFileSync(videoPath).toString("base64");
//   const videoDataUrl = encodeVideoToDataUrl("xxx/local.mp4");
//   content: [{ type: "video_url", video_url: { url: videoDataUrl }, fps: 2 }, { type: "text", text: "这段视频的内容是什么?" }]

// 【本地图像列表】将多张本地图片分别 Base64 后组成 video 列表传入：
//   const imageDataUrls = ["xxx/f1.jpg","xxx/f2.jpg","xxx/f3.jpg","xxx/f4.jpg"].map(p => `data:image/jpeg;base64,${encodeImage(p)}`);
//   content: [{ type: "video", video: imageDataUrls, fps: 2 }, { type: "text", text: "描述这个视频的具体过程" }]

//   messages: [{"role": "user", "content": content}] 
//   再调用 openai.chat.completions.create(model: "kimi-k2.6", messages: messages)
```

## **DashScope**

## Base64 编码方式

Base64 编码方式传入需要构建 [Data URL](https://www.rfc-editor.org/rfc/rfc2397)，构建方法请参见[构建 Data URL](https://help.aliyun.com/zh/model-studio/vision#6f3db6f231evb)。

## Python

```
import base64
import os
import dashscope 
from dashscope import MultiModalConversation

dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

messages = [
    {
        "role": "user",
        "content": [
            {"image": f"data:image/png;base64,{base64_image}"},
            {"text": "图中描绘的是什么景象?"},
        ],
    },
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="kimi-k2.6", 
    messages=messages,
)
print(response.output.choices[0].message.content[0]["text"])

# 以下为传入本地视频文件、本地图像列表示例

# 【本地视频文件】
#   video_data_url = "data:video/mp4;base64," + base64.b64encode(open("xxx/local.mp4","rb").read()).decode("utf-8")
#   content: [{"video": video_data_url, "fps": 2}, {"text": "这段视频的内容是什么?"}]

# 【本地图像列表】
#   Base64：image_data_urls = [f"data:image/jpeg;base64,{encode_image(p)}" for p in ["xxx/f1.jpg","xxx/f2.jpg","xxx/f3.jpg","xxx/f4.jpg"]]
#   content: [{"video": image_data_urls, "fps": 2}, {"text": "描述这个视频的具体过程"}]
```

## Java

```
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

   static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static String encodeToBase64(String imagePath) throws IOException {
        Path path = Paths.get(imagePath);
        byte[] imageBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(imageBytes);
    }
    

    public static void callWithLocalFile(String localPath) throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Image = encodeToBase64(localPath); // Base64编码

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        new HashMap<String, Object>() {{ put("image", "data:image/png;base64," + base64Image); }},
                        new HashMap<String, Object>() {{ put("text", "图中描绘的是什么景象？"); }}
                )).build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("kimi-k2.6")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/eagle.png 替换为你本地图像的绝对路径
            callWithLocalFile("xxx/eagle.png");
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
    
    // 以下为传入本地视频文件、本地图像列表示例
    // 【本地视频文件】
    // String base64Image = encodeToBase64(localPath);
    // MultiModalConversation conv = new MultiModalConversation();
   //  MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
   //             .content(Arrays.asList(
   //                     new HashMap<String, Object>() {{ put("video", "data:video/mp4;base64," + base64Video;}},
   //                     new HashMap<String, Object>() {{ put("text", "这段视频描绘的是什么景象？"); }}
   //             )).build();

    // 【本地图像列表】
    // List<String> urls = Arrays.asList(
    //                                   "data:image/jpeg;base64,"+encodeToBase64(path/f1.jpg),
    //                                   "data:image/jpeg;base64,"+encodeToBase64(path/f2.jpg),
    //                                   "data:image/jpeg;base64,"+encodeToBase64(path/f3.jpg),
    //                                   "data:image/jpeg;base64,"+encodeToBase64(path/f4.jpg)); 
   //  MultiModalConversation conv = new MultiModalConversation();
   //  MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
   //             .content(Arrays.asList(
   //                     new HashMap<String, Object>() {{ put("video", urls;}},
   //                     new HashMap<String, Object>() {{ put("text", "这段视频描绘的是什么景象？"); }}
   //             )).build();

}
```

## 本地文件路径方式

直接向模型传入本地文件路径。仅 DashScope Python 和 Java SDK 支持，不支持 DashScope HTTP 和OpenAI 兼容方式。请您参考下表，结合您的编程语言与操作系统指定文件的路径。

**指定文件路径（以图像为例）**

**系统**

**SDK**

**传入的文件路径**

**示例**

Linux或macOS系统

Python SDK

file://{文件的绝对路径}

file:///home/images/test.png

Java SDK

Windows系统

Python SDK

file://{文件的绝对路径}

file://D:/images/test.png

Java SDK

file:///{文件的绝对路径}

file:///D:/images/test.png

## Python

```
import os
from dashscope import MultiModalConversation
import dashscope 

dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 将xxx/eagle.png替换为你本地图像的绝对路径
local_path = "xxx/eagle.png"
image_path = f"file://{local_path}"
messages = [
                {'role':'user',
                'content': [{'image': image_path},
                            {'text': '图中描绘的是什么景象?'}]}]
response = MultiModalConversation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='kimi-k2.6',  
    messages=messages)
print(response.output.choices[0].message.content[0]["text"])

#   以下为以本地文件路径传入视频、图像列表示例
# 【本地视频文件】
#  video_path = "file:///path/to/local.mp4"
#  content: [{"video": video_path, "fps": 2}, {"text": "这段视频的内容是什么?"}]

# 【本地图像列表】
# image_paths = ["file:///path/f1.jpg", "file:///path/f2.jpg", "file:///path/f3.jpg", "file:///path/f4.jpg"]
# content: [{"video": image_paths, "fps": 2}, {"text": "描述这个视频的具体过程"}]
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    
    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
        String filePath = "file://"+localPath;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>(){{put("image", filePath);}},
                        new HashMap<String, Object>(){{put("text", "图中描绘的是什么景象？");}})).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("kimi-k2.6")  
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

    public static void main(String[] args) {
        try {
            // 将xxx/eagle.png替换为你本地图像的绝对路径
            callWithLocalFile("xxx/eagle.png");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
    
    // 以下为以本地文件路径传入视频、图像列表示例
    
    // 【本地视频文件】
    //  String filePath = "file://"+localPath;
    //    MultiModalConversation conv = new MultiModalConversation();
    //    MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
    //            .content(Arrays.asList(new HashMap<String, Object>(){{put("video", filePath);}},
    //                    new HashMap<String, Object>(){{put("text", "视频中描绘的是什么景象？");}})).build();

    // 【本地图像列表】
    
    //    MultiModalConversation conv = new MultiModalConversation();
    //    List<String> filePath = Arrays.asList("file:///path/f1.jpg", "file:///path/f2.jpg", "file:///path/f3.jpg", "file:///path/f4.jpg")
    //    MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
    //            .content(Arrays.asList(new HashMap<String, Object>(){{put("video", filePath);}},
    //                    new HashMap<String, Object>(){{put("text", "视频中描绘的是什么景象？");}})).build();
}
```

### **文件限制**

### **图像限制**

-   **图像分辨率：**
    
    -   最小尺寸：图像的宽度和高度均须大于`10`像素。
        
    -   宽高比：图像长边与短边的比值不得超过 `200:1`。
        
    -   像素上限：推荐将图像分辨率控制在`8K(7680x4320)`以内。超过此分辨率的图像可能因文件过大、网络传输耗时过长而导致 API 调用超时。
        
-   **支持的图像格式**
    
    -   分辨率在4K`(3840x2160)`以下，支持的图像格式如下：
        
        **图像格式**
        
        **常见扩展名**
        
        **MIME Type**
        
        BMP
        
        .bmp
        
        image/bmp
        
        JPEG
        
        .jpe, .jpeg, .jpg
        
        image/jpeg
        
        PNG
        
        .png
        
        image/png
        
        TIFF
        
        .tif, .tiff
        
        image/tiff
        
        WEBP
        
        .webp
        
        image/webp
        
        HEIC
        
        .heic
        
        image/heic
        
    -   分辨率处于`4K(3840x2160)`到`8K(7680x4320)`范围，仅支持 JPEG、JPG 、PNG 格式。
        
-   **图像大小：**
    
    -   以公网 URL 和本地路径传入时：单个图像的大小不超过`10MB`。
        
    -   以 Base64 编码传入时：编码后的字符串不超过`10MB`。
        
    
    > 如需压缩文件体积请参见[如何将图像或视频压缩到满足要求的大小](https://help.aliyun.com/zh/model-studio/vision#ec8e0a8e03moe)。
    
-   **支持传入的图片数量：**传入多张图像时，图片数量受模型的最大输入的限制，所有图片和文本的总 Token 数必须小于模型的最大输入。
    

## 视频限制

-   **以图像列表传入：**最少传入 4 张图片，最多 2000 张图片
    
-   **以视频文件传入时：**
    
    -   **视频大小：**
        
        -   以公网 URL 传入时：不超过 2GB；
            
        -   以 Base64 编码传入时：编码后的字符串小于 10MB；
            
        -   以本地文件路径传入时：视频本身不超过 100MB。
            
    -   **视频时长：**2 秒至 1 小时；
        
-   **视频格式：** MP4、AVI、MKV、MOV、FLV、WMV 等。
    
-   **视频尺寸：**无特定限制，建议不超过2K，再高的分辨率只会增加处理时间，也不会对模型理解的效果有提升。
    
-   **音频理解：**不支持对视频文件的音频进行理解。
    

## **其它功能**

**模型**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#dd5a3dca390k9)

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)

[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

kimi-k2.6

支持

支持

支持

不支持

不支持

不支持

支持

kimi-k2.5

支持

支持

支持

不支持

不支持

不支持

支持

kimi-k2-thinking

支持

支持

支持

支持

不支持

不支持

支持

Moonshot-Kimi-K2-Instruct

支持

不支持

支持

不支持

支持

不支持

支持

## **参数默认值**

**模型**

**enable\_thinking**

**temperature**

**top\_p**

**presence\_penalty**

**fps**

**max\_frames**

kimi-k2.6

false

思考模式：1.0

非思考模式：0.6

思考/非思考模式：0.95

思考/非思考模式：0.0

2

2000

kimi-k2.5

false

思考模式：1.0

非思考模式：0.6

思考/非思考模式：0.95

思考/非思考模式：0.0

2

2000

kimi-k2-thinking

\-

1.0

\-

\-

\-

\-

Moonshot-Kimi-K2-Instruct

\-

0.6

1.0

0

\-

\-

“-" 表示没有默认值，也不支持设置。

## **模型列表与计费**

Kimi 系列模型是由月之暗面公司（Moonshot AI）推出的大语言模型。

-   kimi-k2.6：Kimi最新最智能的模型，具备更强更稳的长程代码编写能力，指令遵循和自我纠错能力显著提升。同时支持文本、图片与视频输入、思考与非思考模式、对话与 Agent 任务。
    
-   kimi-k2.5：在 Agent、代码生成、视觉理解及一系列通用智能任务上取得开源 SOTA 表现。同时支持图像、视频与文本输入、思考与非思考模式、对话与 Agent 任务。
    
-   kimi-k2-thinking：仅支持深度思考模式，并通过`reasoning_content`字段展示思考过程，具有卓越的编码和工具调用能力，适用于需要逻辑分析、规划或深度理解的场景。
    
-   Moonshot-Kimi-K2-Instruct：不支持深度思考，直接生成回复，响应速度更快，适用于需要快速直接回答的场景。
    

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

按照模型的输入与输出 Token 数量计费。

> 思考模式下，思维链按照输出 Token 计费。

## **常见问题**

### **Q：如何部署 Kimi-K2-Instruct 模型？**

A：我们推荐您通过本文介绍的阿里云百炼 API 方式调用。如有私有化部署需求，请参见[阿里云 Kimi K2 解决方案](https://www.aliyun.com/solution/tech-solution/kimi-k2-instruct)，涵盖了通过 PAI、GPU 云服务器等部署模型的方式。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

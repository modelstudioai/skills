# 深度思考

深度思考模型在生成回复前先进行推理，从而在逻辑推理、数学计算等复杂任务中提升准确性。本文介绍如何通过API调用 Qwen、DeepSeek 等深度思考模型。

> 本文介绍如何通过 OpenAI 兼容的 Chat Completion 接口或 DashScope 接口调用深度思考模型。 Responses API用法参见： [深度思考](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#example-deep-thinking-title) 。

## 效果演示

以下是一个深度思考模型的对话示例，展示模型如何先进行推理再给出回答。

**用户提问**

9.9和9.11谁大

**思考过程**（reasoning\_content 字段）

首先，用户的问题是："9.9和9.11谁大"，这看起来是在比较两个数字：9.9 和 9.11。

我需要理解这些数字的含义。在数学中，9.9 等同于 9.90，而 9.11 是 9.11。

为了比较它们，我应该将它们视为小数。9.9 是 9 + 9/10 = 9.9，而 9.11 是 9 + 11/100 = 9.11。

现在，比较 9.9 和 9.11：9.9 等于 9.90（因为 9.9 = 9.90），9.11 是 9.11。现在，9.90 与 9.11 比较：9.90 大于 9.11，因为 90/100 > 11/100。

更精确地：9.9 = 99/10 = 990/100，9.11 = 911/100，990/100 与 911/100 比较，显然 990 > 911，所以 990/100 > 911/100，因此 9.9 > 9.11。

我也可以直接看小数部分：9.9 的小数部分是 0.9，9.11 的小数部分是 0.11。0.9 大于 0.11，因为 0.9 = 0.90 > 0.11。

所以，9.9 大于 9.11。

**模型回答**（content 字段）

结论：9.9 大于 9.11。

## 使用方式

百炼深度思考模型分为两种模式：

-   **混合思考模式**：可按请求开启或关闭思考，控制参数因模型而异。以下示例使用 `enable_thinking`，取值如下：
    
    -   设为`true`：模型先思考再回复；
    -   设为`false`：模型直接回复；
    
    #### OpenAI 兼容
    
    ```
    # 导入依赖与创建客户端...
    completion = client.chat.completions.create(
        model="qwen3.8-max", # 选择模型
        messages=[{"role": "user", "content": "你是谁"}],
        # 由于 enable_thinking 非 OpenAI 标准参数，需要通过 extra_body 传入
        extra_body={"enable_thinking":True},
        # 流式输出方式调用
        stream=True,
        # 使流式返回的最后一个数据包包含Token消耗信息
        stream_options={
            "include_usage": True
        }
    )
    ```
    
    #### DashScope
    
    > Qwen3.5 系列的 DashScope API采用多模态接口，以下示例会报错 `url error` ，调用方式请参见 [开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of) 。
    
    ```
    # 导入依赖...
    
    response = MultiModalConversation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 可按需更换为其它深度思考模型
        model="qwen3.8-max",
        messages=messages,
        enable_thinking=True,
        stream=True,
        incremental_output=True
    )
    ```
    
-   **仅思考模式**：模型始终在回复前进行思考，无法关闭。除无需设置 `enable_thinking` 参数外，请求格式与混合思考模式一致。
    

思考内容通过`reasoning_content`字段返回，回复内容通过`content`字段返回。深度思考需要额外推理时间，本文示例默认采用流式调用（推荐，可实时查看思考过程、避免长时间等待）。商业版深度思考模型同时支持非流式（同步）输出，用法及注意事项参见下方**常见问题**；部分模型（如 qwen3-235b-a22b、qwen3-32b 等开源版）仅支持流式输出，非流式调用会报错。

## 支持的模型

#### Qwen3.8

**千问3.8 Max系列**（混合思考模式，**默认开启思考模式**）：qwen3.8-max、qwen3.8-max-0902

**千问3.8 Flash系列**（混合思考模式，**默认开启思考模式**）：qwen3.8-flash

**千问3.8 开源系列**（混合思考模式，**默认开启思考模式**）：qwen3.8-27b

**千问3.8 开源系列**（**仅支持思考模式**）：qwen3.8-2.4t-a95b

**千问3.8 Omni系列**（混合思考模式，**默认开启思考模式**）：qwen3.8-omni-flash。通过 `reasoning_effort` 调节思考力度，详见[思考模式配置](https://help.aliyun.com/zh/model-studio/qwen-omni#bc67a9a2bd2of)。

#### Qwen3.7

**千问3.7 Max系列**（混合思考模式，**默认开启思考模式**）：qwen3.7-max、qwen3.7-max-2026-05-20、qwen3.7-max-2026-06-08

**千问3.7 Max系列**（**仅支持思考模式**）：qwen3.7-max-preview、qwen3.7-max-2026-05-17

**千问3.7 Plus系列**（混合思考模式，**默认开启思考模式**）：qwen3.7-plus、qwen3.7-plus-2026-05-26

**千问3.7 Flash系列**（混合思考模式，**默认开启思考模式**）：qwen3.7-flash、qwen3.7-flash-2026-07-15

#### Qwen3.6

**千问3.6 Max系列**（混合思考模式，**默认开启思考模式**）：qwen3.6-max-preview

**千问3.6 Plus系列**（混合思考模式，**默认开启思考模式**）：qwen3.6-plus、qwen3.6-plus-2026-04-02

**千问3.6 Flash系列**（混合思考模式，**默认开启思考模式**）：qwen3.6-flash、qwen3.6-flash-2026-04-16

**千问3.6 开源版**：qwen3.6-35b-a3b

#### Qwen3.5

-   **商业版**
    -   **千问3.5 Plus系列**（混合思考模式，**默认开启思考模式**）：qwen3.5-plus、qwen3.5-plus-2026-02-15
    -   **千问3.5 Flash系列**（混合思考模式，**默认开启思考模式**）：qwen3.5-flash、qwen3.5-flash-2026-02-23
-   **开源版**
    -   混合思考模式，**默认开启思考模式**：qwen3.5-397b-a17b、 qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b

#### Kimi

-   阿里云百炼部署
    
    -   混合思考模式，默认关闭思考模式：kimi-k2.6、kimi-k2.5
    -   仅思考模式：kimi-k3、kimi-k2.7-code、kimi-k2-thinking
-   月之暗面部署
    
    -   混合思考模式，默认开启思考模式：kimi/kimi-k2.6、kimi/kimi-k2.5
    -   仅思考模式：kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code

#### Qwen3

-   **商业版**
    -   **千问Max系列**：qwen3-max、qwen3-max-2026-01-23、qwen3-max-preview（混合思考模式，默认不开启思考模式）
    -   **千问Plus系列**（混合思考模式，默认不开启思考模式）：qwen-plus、qwen-plus-latest、qwen-plus-2025-04-28 及之后的快照版模型
    -   **千问Flash系列**（混合思考模式，默认不开启思考模式）：qwen-flash、qwen-flash-2025-07-28 及之后的快照版模型
    -   **千问Turbo系列**（混合思考模式，默认不开启思考模式）：qwen-turbo 及之后的快照版模型
-   **开源版**
    -   混合思考模式，默认开启思考模式：qwen3-235b-a22b、qwen3-32b、qwen3-30b-a3b、qwen3-14b、qwen3-8b
    -   仅思考模式：qwen3-next-80b-a3b-thinking、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b-thinking-2507

#### QwQ （基于 Qwen2.5）

仅思考模式：qwq-plus

#### DeepSeek

-   阿里云百炼部署
    
    -   混合思考模式，默认开启思考模式：deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-flash
    -   混合思考模式，默认不开启思考模式：deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1
    -   仅思考模式：deepseek-r1、deepseek-r1-0528、deepseek-r1蒸馏模型
-   硅基流动部署
    
    -   混合思考模式，默认不开启思考模式：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus
    -   仅思考模式：siliconflow/deepseek-r1-0528
-   快手万擎部署
    
    -   混合思考模式，默认不开启思考模式：vanchin/deepseek-v3.2-think、vanchin/deepseek-v3.1-terminus
    -   仅思考模式：vanchin/deepseek-r1

#### GLM

-   仅思考模式：glm-5.3
-   混合思考模式，默认开启思考模式：glm-5.2、glm-5.2-fast-preview、glm-5.1、glm-5、glm-4.7、glm-4.6、glm-4.5、glm-4.5-air

#### MiniMax

-   阿里云百炼部署
    
    -   仅思考模式：MiniMax-M2.5、MiniMax-M2.1
-   稀宇科技部署
    
    -   混合思考模式：MiniMax/MiniMax-M3
        
        **说明**MiniMax/MiniMax-M3 通过 `thinking` 参数控制思考模式，取值为 `adaptive`（自适应，默认）或 `disabled`（关闭）。详细用法请参见[MiniMax-稀宇科技](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)。
        
    -   仅思考模式：MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1
        

#### Stepfun

混合思考模式：stepfun/step-3.7-flash

## 快速开始

API 使用前提：已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)（DashScope Java SDK需不低于 2.19.4 版本）。

以下代码以流式调用 qwen3.8-max 开启思考模式为例。

#### OpenAI兼容

#### Python

### 示例代码

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen3.8-max",  # 您可以按需更换为其它深度思考模型
    messages=messages,
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
        print("\nUsage:")
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

### 返回结果

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个准确且友好的回答。首先，我要确认自己的身份，即千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如回答问题、创作文字、逻辑推理等。同时，要保持语气亲切，避免过于技术化，让用户感觉轻松。还要注意不要使用复杂术语，确保回答简洁明了。另外，可能需要加入一些互动元素，邀请用户提问，促进进一步交流。最后，检查是否有遗漏的重要信息，比如我的中文名称“千问”和英文名称“Qwen”，以及所属公司和实验室。确保回答全面且符合用户期望。
====================完整回复====================

你好！我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以回答问题、创作文字、进行逻辑推理、编程等，旨在为用户提供高质量的信息和服务。你可以叫我Qwen，或者直接叫我千问。有什么我可以帮你的吗？
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        const stream = await openai.chat.completions.create({
            model: 'qwen3.8-max',
            messages,
            stream: true,
            enable_thinking: true
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
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

### 返回结果

```
====================思考过程====================

好的，用户问“你是谁”，我需要回答我的身份。首先，我应该明确说明我是千问，由阿里云开发的超大规模语言模型。接下来，可以提到我的主要功能，比如回答问题、创作文字、逻辑推理等。还要强调我的多语言支持，包括中文和英文，这样用户知道我可以处理不同语言的请求。另外，可能需要解释一下我的应用场景，比如学习、工作和生活中的帮助。不过用户的问题比较直接，可能不需要太详细的信息，保持简洁明了。同时，要确保语气友好，邀请用户进一步提问。检查有没有遗漏的重要信息，比如我的版本或最新更新，但可能用户不需要那么详细。最后，确认回答准确无误，没有错误信息。
====================完整回复====================

我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等多种任务，支持中英文等多种语言。如果你有任何问题或需要帮，欢迎随时告诉我！
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
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

### 返回结果

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":10,"completion_tokens":360,"total_tokens":370,"completion_tokens_details":{"reasoning_tokens":286}},"created":1745485391,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: [DONE]
```

#### DashScope

> Qwen3.5 系列的 DashScope API采用多模态接口，以下示例会报错 `url error` ，调用方式请参见 [开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of) 。

#### Python

### 示例代码

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [{"role": "user", "content": [{"text": "你是谁？"}]}]

completion = MultiModalConversation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 可按需更换为其它深度思考模型
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,
    stream=True,
    incremental_output=True
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in completion:
    # 如果思考过程与回复皆为空，则忽略
    content = chunk.output.choices[0].message.content
    reasoning = chunk.output.choices[0].message.reasoning_content
    if not content and reasoning == "":
        pass
    else:
        # 如果当前为思考过程
        if reasoning != "" and not content:
            print(reasoning, end="", flush=True)
            reasoning_content += reasoning
        # 如果当前为回复
        elif content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(content[0]["text"], end="", flush=True)
            answer_content += content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

### 返回结果

```
====================思考过程====================
好的，用户问：“你是谁？”我需要回答这个问题。首先，我要明确自己的身份，即千问，由阿里云开发的超大规模语言模型。接下来，要说明我的功能和用途，比如回答问题、创作文字、逻辑推理等。同时，要强调我的目标是成为用户的得力助手，提供帮助和支持。

在表达时，要保持口语化，避免使用专业术语或复杂句式。可以加入一些亲切的语气词，比如“你好呀～”，让对话更自然。另外，要确保信息准确，不遗漏关键点，比如我的开发者、主要功能和使用场景。

还要考虑用户可能的后续问题，比如具体的应用例子或技术细节，所以在回答中可以适当埋下伏笔，引导用户进一步提问。例如，提到“无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助”，这样既全面又开放。

最后，检查回答是否流畅，有没有重复或冗余的信息，确保简洁明了。同时，保持友好和专业的平衡，让用户感受到既亲切又可靠。
====================完整回复====================
你好呀～我是千问，是阿里云开发的一款超大规模语言模型。我能够回答问题、创作文字、进行逻辑推理、编程等等，旨在为用户提供帮助和支持。无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助。有什么我可以帮你的吗？
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static void handleMultiModalConversationResult(MultiModalConversationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        List<Map<String, Object>> contentList = (List<Map<String, Object>>) message.getOutput().getChoices().get(0).getMessage().getContent();
        String content = (contentList != null && !contentList.isEmpty()) ? (String) contentList.get(0).get("text") : "";

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage userMsg) {
        return MultiModalConversationParam.builder()
                 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .enableThinking(true)
                .incrementalOutput(true)
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(userMsg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> handleMultiModalConversationResult(message));
    }

    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue()).content(Arrays.asList(Collections.singletonMap("text", "你是谁？"))).build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException | UploadFileException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
====================思考过程====================
好的，用户问“你是谁？”，我需要根据之前的设定来回答。首先，我的角色是千问，阿里巴巴集团旗下的超大规模语言模型。要保持口语化，简洁易懂。

用户可能刚接触我，或者想确认我的身份。应该先直接回答我是谁，然后简要说明我的功能和用途，比如回答问题、创作文字、编程等。还要提到支持多语言，这样用户知道我可以处理不同语言的需求。

另外，根据指导方针，要保持拟人性，所以语气要友好，可能用表情符号增加亲切感。同时，可能需要引导用户进一步提问或使用我的功能，比如问他们需要什么帮助。

需要注意不要使用复杂术语，避免冗长。检查是否有遗漏的关键点，比如多语言支持和具体能力。确保回答符合所有要求，包括口语化和简洁。
====================完整回复====================
你好！我是千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。有什么需要我帮忙的吗？
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [{"text": "你是谁？"}]
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

### 返回结果

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"嗯","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"input_tokens":11,"output_tokens":3},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"input_tokens":11,"output_tokens":4},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"用户","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":16,"input_tokens":11,"output_tokens":5},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"问","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":17,"input_tokens":11,"output_tokens":6},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"“","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":18,"input_tokens":11,"output_tokens":7},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
......

id:358
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"帮助","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":373,"input_tokens":11,"output_tokens":362},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:359
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"，","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":374,"input_tokens":11,"output_tokens":363},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:360
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"欢迎","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":375,"input_tokens":11,"output_tokens":364},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:361
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"随时","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":376,"input_tokens":11,"output_tokens":365},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:362
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":377,"input_tokens":11,"output_tokens":366},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:363
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:364
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
```

## 核心能力

### 切换思考/非思考模式

启用思考模式可提升回复质量，但会增加响应延迟和 Token 消耗。使用混合思考模式的模型时，可根据问题复杂度动态切换，无需更换模型：

-   简单任务（日常聊天、简单问答）：将`enable_thinking`设为`false`关闭思考；
-   复杂任务（逻辑推理、代码生成、数学解答）：将`enable_thinking`设为`true`开启思考。

#### OpenAI兼容

**重要**`enable_thinking`非 OpenAI 标准参数，若使用 OpenAI Python SDK请通过 `extra_body`传入，Node.js SDK中作为顶层参数传入。

#### Python

### 示例代码

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    # 通过 extra_body 设置 enable_thinking 开启思考过程
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

### 返回结果

```
====================思考过程====================

嗯，用户问“你是谁”，我需要先确定他们想知道什么。可能他们第一次接触我，或者想确认我的身份。我应该先介绍自己是千问，由通义实验室研发。然后要说明我的功能，比如回答问题、创作文字、编程等，这样用户了解我能提供什么帮助。还要提到我支持多种语言，这样国际用户也会知道他们可以用不同语言交流。最后保持友好，邀请他们提问，这样可以促进进一步互动。要注意简洁明了，避免技术术语太多，让用户容易理解。可能用户需要的是快速了解我的能力，所以重点放在功能和用途上。还要检查有没有遗漏的信息，比如是否要提到阿里巴巴集团，或者更多技术细节。不过用户可能只需要基本的信息，不需要太深入。确保回答友好且专业，同时鼓励用户继续提问。
====================完整回复====================

我是千问，由通义实验室研发的超大规模语言模型。我可以帮助你回答问题、创作文字、编程、表达观点等，支持多语言交流。有什么需要我帮忙的吗？
====================Token 消耗====================

CompletionUsage(completion_tokens=221, prompt_tokens=10, total_tokens=231, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=172, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0))
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];

        const stream = await openai.chat.completions.create({
            model: 'qwen3.8-max',
            messages,
            // 注意：在 Node.js SDK，enable_thinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
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

### 返回结果

```
====================思考过程====================

嗯，用户问“你是谁”，我需要先确定他们想知道什么。可能他们第一次接触我，或者想确认我的身份。我应该先介绍自己的名字和身份，比如千问，英文名Qwen。然后说明我是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。接下来要提到我的功能，比如回答问题、创作文字、编程、表达观点等，这样用户能了解我的用途。还要提到我支持多语言，这样国际用户会觉得有用。最后邀请他们提问，保持友好和开放的态度。注意用简洁易懂的语言，避免技术术语太多。可能用户需要帮助，或者只是好奇，所以回应要亲切，鼓励他们进一步互动。另外，可能需要考虑用户是否有更深层的需求，比如测试我的能力或者寻找特定帮助，但初次回答还是以基本信息和引导为主。保持口语化，不用复杂句子，让信息传达更有效。
====================完整回复====================

你好！我是千问，英文名Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字（比如写故事、写公文、写邮件、写剧本等）、进行逻辑推理、编程，甚至表达观点和玩游戏。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。

如果你有任何问题或需要帮助，随时告诉我！
====================Token 消耗====================

{
  prompt_tokens: 10,
  completion_tokens: 288,
  total_tokens: 298,
  completion_tokens_details: { reasoning_tokens: 188 },
  prompt_tokens_details: { cached_tokens: 0 }
}
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
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

#### DashScope

> Qwen3.5 系列的 DashScope API采用多模态接口，以下示例会报错 `url error` ，调用方式请参见 [开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of) 。

#### Python

### 示例代码

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 初始化请求参数
messages = [{"role": "user", "content": [{"text": "你是谁？"}]}]

completion = MultiModalConversation.call(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,     # 开启思考过程
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

    # 收到 content，开始进行回复（content 为列表类型）
    if message.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(message.content[0]["text"], end="", flush=True)
        answer_content += message.content[0]["text"]

print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
print(chunk.usage)
# 循环结束后，reasoning_content 和 answer_content 变量中包含了完整的内容
# 您可以在这里根据需要进行后续处理
# print(f"\n\n完整思考过程:\n{reasoning_content}")
# print(f"\n完整回复:\n{answer_content}")
```

### 返回结果

```
====================思考过程====================

嗯，用户问“你是谁？”，我需要先确定他们想知道什么。可能他们第一次接触我，或者想确认我的身份。首先，我应该介绍自己的名字，千问，然后说明我是通义实验室研发的超大规模语言模型。接下来，可能需要解释我的功能，比如回答问题、创作文字、编程等，这样用户能了解我的用途。还要提到我支持多种语言，这样国际用户也能知道他们可以用不同语言交流。最后，保持友好，邀请他们提问，这样能促进进一步的互动。要注意用简洁易懂的语言，避免技术术语太多，让用户容易理解。可能用户有更深层的需求，比如测试我的能力，或者寻找帮助，所以提供具体的例子会更好，比如写故事、写公文、写邮件等。还要确保回答结构清晰，分点说明功能，但可能不需要用项目符号，而是自然过渡。另外，要强调我是AI助手，没有个人意识，所有回答都基于训练数据，这样避免误解。可能需要检查有没有遗漏的重要信息，比如多模态能力，或者最新的更新，但根据之前的回复，可能不需要太深入。总之，回答要全面但简洁，友好且有帮助，让用户感到被理解和支持。
====================完整回复====================

我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你：

1. **回答问题**：无论是学术问题、常识问题还是专业领域问题，我都可以尝试为你解答。
2. **创作文字**：写故事、写公文、写邮件、写剧本等，我都可以帮你完成。
3. **逻辑推理**：我可以帮助你进行逻辑推理和解决问题。
4. **编程**：我可以理解并生成多种编程语言的代码。
5. **多语言支持**：我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。

如果你有任何问题或需要帮助，随时告诉我！
====================Token 消耗====================

{"input_tokens": 11, "output_tokens": 405, "total_tokens": 416, "output_tokens_details": {"reasoning_tokens": 256}, "prompt_tokens_details": {"cached_tokens": 0}}
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static void handleMultiModalConversationResult(MultiModalConversationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        List<Map<String, Object>> contentList = (List<Map<String, Object>>) message.getOutput().getChoices().get(0).getMessage().getContent();
        String content = (contentList != null && !contentList.isEmpty()) ? (String) contentList.get(0).get("text") : "";

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage userMsg) {
        return MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .enableThinking(true)
                .incrementalOutput(true)
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(userMsg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> handleMultiModalConversationResult(message));
    }

    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue()).content(Arrays.asList(Collections.singletonMap("text", "你是谁？"))).build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException | UploadFileException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
====================思考过程====================
嗯，用户问“你是谁？”，我需要先确定他们想了解什么。可能他们想知道我的身份，或者是在测试我的反应。首先，我应该明确回答我是千问，阿里巴巴集团旗下的超大规模语言模型。然后，可能需要简要介绍我的功能，比如回答问题、创作文字、编程等，这样用户能了解我的用途。还要提到我支持多种语言，这样国际用户也会知道他们可以用不同语言交流。最后，保持友好，邀请他们提问，这样他们会觉得亲切，愿意继续互动。要注意回答不要太长，但信息要全面。可能用户还有后续问题，比如我的技术细节或者使用场景，但初次回答应该简洁明了。确保没有使用专业术语，让所有用户都能理解。检查有没有遗漏的重要信息，比如多语言支持和具体功能例子。好的，这样应该能覆盖用户的需求了。
====================完整回复====================
我是千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字（如写故事、写公文、写邮件、写剧本等）、进行逻辑推理、编程、表达观点、玩游戏等，支持多语言交流，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
# === 执行时请删除该注释 ===
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [{"text": "你是谁？"}]
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

### 返回结果

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"嗯","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"input_tokens":11,"output_tokens":3},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"input_tokens":11,"output_tokens":4},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"用户","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":16,"input_tokens":11,"output_tokens":5},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"问","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":17,"input_tokens":11,"output_tokens":6},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"“","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":18,"input_tokens":11,"output_tokens":7},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
......

id:358
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"帮助","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":373,"input_tokens":11,"output_tokens":362},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:359
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"，","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":374,"input_tokens":11,"output_tokens":363},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:360
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"欢迎","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":375,"input_tokens":11,"output_tokens":364},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:361
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"随时","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":376,"input_tokens":11,"output_tokens":365},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:362
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":377,"input_tokens":11,"output_tokens":366},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:363
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:364
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
```

此外，**Qwen3 开源版混合思考模型以及 qwen-plus-2025-04-28 模型**支持通过提示词动态控制思考模式。`enable_thinking`为`true`时，在提示词中加入`/no_think`可关闭思考；多轮对话中如需重新开启，在最新提示词中加入`/think`即可。模型始终遵循最新的`/think`或`/no_think`指令。

### 限制思考长度

深度思考模型有时会生成冗长的推理过程，增加等待时间并消耗更多 Token。通过`thinking_budget`参数可设置推理过程的最大 Token 数，超过限制后模型立即输出回复。

> `thinking_budget` 默认值为模型的最大思维链长度，请参见百炼控制台的模型卡片。

**重要**`thinking_budget`参数用于设置思考过程的最大 Token 数。适用于Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、Qwen3、GLM（阿里云直供）、Kimi（阿里云直供）系列模型，其中 kimi-k3 不支持该参数。

### 控制台体验深度思考

1.  登录大模型服务平台百炼控制台。
2.  在左侧导航栏选择**体验中心** > **文本模型**。
3.  页面默认展示 Qwen3.7-Max 模型，也可单击模型名称，在下拉列表中选择其他 Qwen3 系列模型。
4.  在输入框底部单击**深度思考**，开启推理模式，查看模型的思考过程。
5.  单击右上角的**模型调试**，在打开的配置面板中设置`thinking_budget`参数，控制思维链输出的最大 Token 数量，取值范围 1～32768，默认值 4000。如需体验更多模型，可前往百炼模型广场。

#### OpenAI兼容

#### Python

### 示例代码

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    extra_body={
        "enable_thinking": True,
        "thinking_budget": 50
        },
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
        print("\nUsage:")
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

### 返回结果

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个清晰且友好的回答。首先，应该明确自己的身份，即千问，由阿里巴巴集团旗下的通义实验室研发。接下来，要说明自己的主要功能，比如回答
====================完整回复====================

我是千问，是阿里巴巴集团旗下的通义实验室研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等，旨在为用户提供帮助和便利。有什么我可以帮您的吗？
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        const stream = await openai.chat.completions.create({
            model: 'qwen3.8-max',
            messages,
            stream: true,
            // enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
            enable_thinking: true,
            thinking_budget: 50
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
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

### 返回结果

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个清晰准确的回答。首先，我应该介绍自己的身份，即千问，由阿里巴巴集团旗下的通义实验室研发。接下来，要说明我的主要功能，比如回答问题
====================完整回复====================

我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等多种任务。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
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
    "enable_thinking": true,
    "thinking_budget": 50
}'
```

### 返回结果

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":10,"completion_tokens":360,"total_tokens":370,"completion_tokens_details":{"reasoning_tokens":50}},"created":1745485391,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: [DONE]
```

**说明**在思考模式（`enable_thinking`设置为`true`）下，`max_tokens`参数的有效取值范围为 \[1, 32768\]，超出该范围时接口返回 400 错误，错误信息为`InvalidParameter: Range of max_tokens should be [1, 32768]`。非思考模式下无此限制。

建议使用`max_completion_tokens`参数替代`max_tokens`。`max_completion_tokens`限制模型的完整输出长度（包含思维链和最终回复），`max_tokens`仅限制最终回复部分的长度。`max_tokens`参数即将废弃，新接入的业务请使用`max_completion_tokens`。

```
# 思考模式下推荐使用 max_completion_tokens 限制输出长度
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁"}],
    extra_body={"enable_thinking": True},
    # max_completion_tokens 限制思维链与回复的总输出长度，无 32768 上限约束
    max_completion_tokens=65536,
)
# 思考模式下 max_tokens 上限为 32768，超出会返回 400 错误
```

#### DashScope

> Qwen3.5 系列的 DashScope API采用多模态接口，以下示例会报错 `url error` ，调用方式请参见 [开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of) 。

#### Python

### 示例代码

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [{"role": "user", "content": [{"text": "你是谁？"}]}]

completion = MultiModalConversation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,
    # 设置最大推理过程 Token 数
    thinking_budget=50,
    stream=True,
    incremental_output=True,
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in completion:
    # 如果思考过程与回复皆为空，则忽略
    content = chunk.output.choices[0].message.content
    reasoning = chunk.output.choices[0].message.reasoning_content
    if not content and reasoning == "":
        pass
    else:
        # 如果当前为思考过程
        if reasoning != "" and not content:
            print(reasoning, end="", flush=True)
            reasoning_content += reasoning
        # 如果当前为回复
        elif content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(content[0]["text"], end="", flush=True)
            answer_content += content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

### 返回结果

```
====================思考过程====================
好的，用户问“你是谁？”，我需要给出一个清晰且友好的回答。首先，我要介绍自己的身份，也就是千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如
====================完整回复====================
我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等，旨在为用户提供全面、准确和有用的信息与帮助。有什么我可以帮您的吗？
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static void handleMultiModalConversationResult(MultiModalConversationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        List<Map<String, Object>> contentList = (List<Map<String, Object>>) message.getOutput().getChoices().get(0).getMessage().getContent();
        String content = (contentList != null && !contentList.isEmpty()) ? (String) contentList.get(0).get("text") : "";

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage userMsg) {
        return MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .enableThinking(true)
                .thinkingBudget(50)
                .incrementalOutput(true)
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(userMsg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> handleMultiModalConversationResult(message));
    }

    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue()).content(Arrays.asList(Collections.singletonMap("text", "你是谁？"))).build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException | UploadFileException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
====================思考过程====================
好的，用户问“你是谁？”，我需要给出一个清晰且友好的回答。首先，我要介绍自己的身份，也就是千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如
====================完整回复====================
我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等，旨在为用户提供全面、准确和有用的信息与帮助。有什么我可以帮您的吗？
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
# === 执行时请删除该注释 ===
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [{"text": "你是谁？"}]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "thinking_budget": 50,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

### 返回结果

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"好的","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"output_tokens":3,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":1}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"output_tokens":4,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":2}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}

......

id:133
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":149,"output_tokens":138,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":50}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}

id:134
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":149,"output_tokens":138,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":50}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}
```

### 传递思考过程

多轮对话中，`preserve_thinking` 控制模型是否读取历史 assistant 消息中的 `reasoning_content`。设为 `true` 后，这些思考内容会拼接到下一轮输入。客户端需在请求的 `messages` 中提供历史 assistant 消息及其 `reasoning_content`。各型号的默认值以[Chat Completions 参数说明](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)为准。

**重要**`preserve_thinking`参数仅支持 qwen3.8-max、qwen3.8-max-0902、qwen3.8-omni-flash（默认开启）、qwen3.7-max、qwen3.7-max-2026-05-20、qwen3.7-max-2026-06-08、qwen3.7-max-preview、qwen3.7-max-2026-05-17、qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-max-preview、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.7-flash、qwen3.7-flash-2026-07-15、kimi-k2.7-code（阿里云百炼部署）、kimi-k2.6（阿里云百炼部署）、kimi/kimi-k3（月之暗面部署）、kimi/kimi-k2.7-code-highspeed（月之暗面部署）、kimi/kimi-k2.7-code（月之暗面部署）、kimi/kimi-k2.6（月之暗面部署）。

> 对于上述支持此参数的 Qwen3.8 Max、Qwen3.7、Qwen3.6 和 Kimi 型号，若历史消息中不包含 `reasoning_content`，开启此参数不会报错。

> 开启后，历史对话中的 `reasoning_content` 会计入输入 Token 数量和计费。

#### OpenAI兼容

**说明**`preserve_thinking`非 OpenAI 标准参数，使用 Python SDK需通过`extra_body`传入。

#### Python

### 示例代码

```
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 第一轮对话
messages = [
    {"role": "user", "content": "我需要为一个日均千万消息的电商系统选择消息队列，请推荐"}
]

first_reasoning = ""
first_content = ""
is_answering = False

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True,
    stream_options={"include_usage": True},
)

print("=" * 20 + "第一轮思考过程" + "=" * 20)

for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        first_reasoning += delta.reasoning_content
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "第一轮回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)
        first_content += delta.content

# 第二轮对话：传递思考过程，追问模型为什么排除了Kafka
messages = [
    {"role": "user", "content": "我需要为一个日均千万消息的电商系统选择消息队列，请推荐"},
    {
        "role": "assistant",
        "content": first_content,
        "reasoning_content": first_reasoning,
    },
    {"role": "user", "content": "你在对比时为什么排除了Kafka？"},
]

reasoning_content = ""
answer_content = ""
is_answering = False

# preserve_thinking 通过 extra_body 传入
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={
        "enable_thinking": True,
        "preserve_thinking": True,
    },
    stream=True,
    stream_options={"include_usage": True},
)

print("\n" + "=" * 20 + "第二轮思考过程" + "=" * 20)

for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "第二轮回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

### 返回结果

```
====================第一轮思考过程====================
用户需要为日均千万消息的电商系统选择消息队列。让我从吞吐量、可靠性、延迟消息、事务支持等维度对比主流方案...

RocketMQ：阿里电商场景验证，原生支持事务消息和延迟消息，分区级严格有序...
Kafka：极高吞吐量，但无原生事务消息和延迟消息支持，需自研补偿机制...
RabbitMQ：延迟低，但集群扩展能力有限，峰值万级TPS...
====================第一轮回复====================
综合电商场景的核心需求（事务消息、延迟消息、顺序性、峰值应对），推荐 Apache RocketMQ。如果团队已有 Kafka 生态或需强实时分析能力，Kafka 也是可行方案。
====================第二轮思考过程====================
用户在追问为什么排除了Kafka。回顾我的历史思考过程，我并没有排除Kafka，而是给了它4星评分。让我参考之前的详细对比分析来解释...

在上一轮思考中，我对比了RocketMQ和Kafka在事务消息、延迟消息、顺序性方面的差异。Kafka的劣势主要在于需要额外架构设计来补齐电商特有语义...
====================第二轮回复====================
我并没有排除Kafka。Kafka在吞吐量和生态方面表现优秀，之所以RocketMQ评分略高，是因为电商核心链路的"开箱即用"特性匹配度：RocketMQ原生支持事务消息和延迟消息，而Kafka需要通过Outbox Pattern等架构模式自行实现。如果团队已有Kafka生态，它完全能胜任千万级消息场景。
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

async function main() {
    // 第一轮对话
    let firstReasoning = '';
    let firstContent = '';
    let isAnswering = false;

    const stream1 = await openai.chat.completions.create({
        model: 'qwen3.8-max',
        messages: [{ role: 'user', content: '我需要为一个日均千万消息的电商系统选择消息队列，请推荐' }],
        stream: true,
        enable_thinking: true
    });

    console.log('='.repeat(20) + '第一轮思考过程' + '='.repeat(20));

    for await (const chunk of stream1) {
        if (!chunk.choices?.length) continue;
        const delta = chunk.choices[0].delta;
        if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
            firstReasoning += delta.reasoning_content;
            if (!isAnswering) process.stdout.write(delta.reasoning_content);
        }
        if (delta.content !== undefined && delta.content) {
            if (!isAnswering) {
                console.log('\n' + '='.repeat(20) + '第一轮回复' + '='.repeat(20));
                isAnswering = true;
            }
            process.stdout.write(delta.content);
            firstContent += delta.content;
        }
    }

    // 第二轮对话：传递思考过程
    let reasoningContent = '';
    let answerContent = '';
    isAnswering = false;

    const stream2 = await openai.chat.completions.create({
        model: 'qwen3.8-max',
        messages: [
            { role: 'user', content: '我需要为一个日均千万消息的电商系统选择消息队列，请推荐' },
            {
                role: 'assistant',
                content: firstContent,
                reasoning_content: firstReasoning
            },
            { role: 'user', content: '你在对比时为什么排除了Kafka？' }
        ],
        stream: true,
        enable_thinking: true,
        // preserve_thinking 作为顶层参数传入
        preserve_thinking: true
    });

    console.log('\n' + '='.repeat(20) + '第二轮思考过程' + '='.repeat(20));

    for await (const chunk of stream2) {
        if (!chunk.choices?.length) continue;
        const delta = chunk.choices[0].delta;
        if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
            if (!isAnswering) process.stdout.write(delta.reasoning_content);
            reasoningContent += delta.reasoning_content;
        }
        if (delta.content !== undefined && delta.content) {
            if (!isAnswering) {
                console.log('\n' + '='.repeat(20) + '第二轮回复' + '='.repeat(20));
                isAnswering = true;
            }
            process.stdout.write(delta.content);
            answerContent += delta.content;
        }
    }
}

main();
```

### 返回结果

```
====================第一轮思考过程====================
用户需要为日均千万消息的电商系统选择消息队列。让我从吞吐量、可靠性、延迟消息、事务支持等维度对比主流方案...
====================第一轮回复====================
综合电商场景的核心需求，推荐 Apache RocketMQ。如果团队已有 Kafka 生态，Kafka 也是可行方案。
====================第二轮思考过程====================
用户追问为什么排除了Kafka。参考我之前的思考过程，我并没有排除Kafka...
====================第二轮回复====================
我并没有排除Kafka。Kafka在吞吐量和生态方面表现优秀，之所以RocketMQ评分略高，是因为电商核心链路的"开箱即用"特性匹配度。
```

#### HTTP

### 示例代码

#### curl

```
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages": [
        {
            "role": "user",
            "content": "我需要为一个日均千万消息的电商系统选择消息队列，请推荐"
        },
        {
            "role": "assistant",
            "content": "综合电商场景的核心需求，推荐 Apache RocketMQ。",
            "reasoning_content": "用户需要为日均千万消息的电商系统选择消息队列。RocketMQ原生支持事务消息和延迟消息，更适合电商场景。Kafka吞吐量极高但需自研补偿机制。"
        },
        {
            "role": "user",
            "content": "你在对比时为什么排除了Kafka？"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true,
    "preserve_thinking": true
}'
```

### 返回结果

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1743523200,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-example-001"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1743523200,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-example-001"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":3463,"completion_tokens":2387,"total_tokens":5850,"completion_tokens_details":{"reasoning_tokens":1347}},"created":1743523200,"system_fingerprint":null,"model":"qwen3.8-max","id":"chatcmpl-example-001"}

data: [DONE]
```

#### DashScope

**说明**Java SDK暂不支持`preserve_thinking`参数。通过HTTP调用时，请将`preserve_thinking`放入`parameters`对象中。

#### Python

### 示例代码

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/"

# 第一轮对话
messages = [
    {"role": "user", "content": [{"text": "我需要为一个日均千万消息的电商系统选择消息队列，请推荐"}]}
]

first_reasoning = ""
first_content = ""
is_answering = False

completion = MultiModalConversation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,
    stream=True,
    incremental_output=True,
)

print("=" * 20 + "第一轮思考过程" + "=" * 20)

for chunk in completion:
    content = chunk.output.choices[0].message.content
    reasoning = chunk.output.choices[0].message.reasoning_content
    if not content and reasoning == "":
        pass
    else:
        if reasoning != "" and not content:
            print(reasoning, end="", flush=True)
            first_reasoning += reasoning
        elif content:
            if not is_answering:
                print("\n" + "=" * 20 + "第一轮回复" + "=" * 20)
                is_answering = True
            print(content[0]["text"], end="", flush=True)
            first_content += content[0]["text"]

# 第二轮对话：传递思考过程
messages = [
    {"role": "user", "content": [{"text": "我需要为一个日均千万消息的电商系统选择消息队列，请推荐"}]},
    {
        "role": "assistant",
        "content": [{"text": first_content}],
        "reasoning_content": first_reasoning,
    },
    {"role": "user", "content": [{"text": "你在对比时为什么排除了Kafka？"}]},
]

reasoning_content = ""
answer_content = ""
is_answering = False

completion = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,
    # 传递思考过程
    preserve_thinking=True,
    stream=True,
    incremental_output=True,
)

print("\n" + "=" * 20 + "第二轮思考过程" + "=" * 20)

for chunk in completion:
    content = chunk.output.choices[0].message.content
    reasoning = chunk.output.choices[0].message.reasoning_content
    if not content and reasoning == "":
        pass
    else:
        if reasoning != "" and not content:
            print(reasoning, end="", flush=True)
            reasoning_content += reasoning
        elif content:
            if not is_answering:
                print("\n" + "=" * 20 + "第二轮回复" + "=" * 20)
                is_answering = True
            print(content[0]["text"], end="", flush=True)
            answer_content += content[0]["text"]
```

### 返回结果

```
====================第一轮思考过程====================
用户需要为日均千万消息的电商系统选择消息队列。让我从吞吐量、可靠性、延迟消息、事务支持等维度对比主流方案...
====================第一轮回复====================
综合电商场景的核心需求，推荐 Apache RocketMQ。如果团队已有 Kafka 生态，Kafka 也是可行方案。
====================第二轮思考过程====================
用户追问为什么排除了Kafka。参考我之前的思考过程，我并没有排除Kafka...
====================第二轮回复====================
我并没有排除Kafka。Kafka在吞吐量和生态方面表现优秀，之所以RocketMQ评分略高，是因为电商核心链路的"开箱即用"特性匹配度。
```

#### HTTP

### 示例代码

#### curl

```
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [{"text": "我需要为一个日均千万消息的电商系统选择消息队列，请推荐"}]
            },
            {
                "role": "assistant",
                "content": [{"text": "综合电商场景的核心需求，推荐 Apache RocketMQ。"}],
                "reasoning_content": "用户需要为日均千万消息的电商系统选择消息队列。RocketMQ原生支持事务消息和延迟消息，更适合电商场景。Kafka吞吐量极高但需自研补偿机制。"
            },
            {
                "role": "user",
                "content": [{"text": "你在对比时为什么排除了Kafka？"}]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "preserve_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

### 返回结果

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"用户","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":3466,"output_tokens":3,"input_tokens":3463,"output_tokens_details":{"reasoning_tokens":1}},"request_id":"example-request-001"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"追问","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":3467,"output_tokens":4,"input_tokens":3463,"output_tokens_details":{"reasoning_tokens":2}},"request_id":"example-request-001"}

......

id:200
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":5850,"output_tokens":2387,"input_tokens":3463,"output_tokens_details":{"reasoning_tokens":1347}},"request_id":"example-request-001"}
```

### 其他功能

-   [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation#9c315c95a8omt)
-   [工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#fbf3d739f2q9f)
-   [联网搜索](https://help.aliyun.com/zh/model-studio/web-search#9b41940862qf3)

## 计费说明

-   思考内容按输出 Token 计费。
    
-   部分混合思考模型在思考与非思考模式下价格不同。模型输出了思考过程时，所有输出 Token（包括思考 Token 和回复 Token）均按思考模式的输出价格计费。
    
    > 若模型在思考模式下未输出思考过程，则按非思考模式价格计费。
    

## 常见问题

Q：怎么关闭思考模式？

是否能关闭思考模式取决于所用模型：

-   混合思考模式模型（如 qwen3.6-plus、deepseek-v4-pro）：将 `enable_thinking` 设为 `false` 即可关闭；
-   仅思考模式模型（如 qwen3-235b-a22b-thinking-2507、deepseek-r1）：无法关闭。

`enable_thinking` 是百炼的扩展参数，不属于 OpenAI 标准字段。使用 OpenAI Java SDK 时，`ChatCompletionCreateParams` 不原生支持该字段，需通过 `extraBody` 方法传入：

```
// enable_thinking 非 OpenAI 标准参数，Java SDK 需通过 extra_body 传递
ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
    .model("qwen3.6-plus")
    .messages(List.of(
        ChatCompletionMessageParam.builder()
            .role(ChatCompletionMessageParamRole.USER)
            .content("你好")
            .build()
    ))
    .extraBody(Map.of("enable_thinking", false))
    .build();

client.chat().completions().create(params);
```

Q：如何确认思考模式是否已开启？

若思考模式与非思考模式下的调用耗时差异极小，说明思考模式可能未实际开启。按以下步骤排查：

1.  检查 API 请求中是否正确传入 `enable_thinking=true` 参数。使用 OpenAI Java SDK 时，该参数需通过 `extraBody` 传入（参见上一问示例）。
2.  查看响应中是否包含 `reasoning_content` 字段，并确认用量中 `reasoning_tokens` 大于 0。不包含该字段或 `reasoning_tokens=0` 表示思考模式未启用。
3.  对比思考与非思考模式下的响应时间与 `completion_tokens`。启用思考模式后，响应中会出现 `reasoning_content` 字段，且总耗时显著增加（实测约为非思考模式的 3 倍）；若两者耗时差异极小，说明思考模式未实际生效，请检查参数是否正确传入并重试。

Q：qwen3.7-plus 调用响应慢如何排查？

qwen3.7-plus 属于混合思考模式模型，且默认开启思考模式。思考过程会生成大量推理 Token（实测占总输出 Token 的 60% 以上），因此单次调用的总耗时明显长于非思考模式。此时 Token 生成速度本身并无异常（实测约 52～54 Tokens/s），总耗时的差异主要来自思考过程产生的 Token 数量，而非模型或网络变慢。

排查步骤：

1.  确认是否开启了思考模式。qwen3.7-plus 默认开启，可根据响应中是否返回 `reasoning_content` 字段判断。
2.  查看响应用量中的 `completion_tokens` 与 `reasoning_tokens`。若 `reasoning_tokens` 占比较高，则总耗时长属于思考模式的预期表现。
3.  若无需思考过程，在请求中将 `enable_thinking` 设为 `false` 关闭思考模式。关闭后输出 Token 大幅减少，实测总耗时可降低 60%～75%。
4.  若需保留思考能力，可改用**流式输出**，以更快获得首个 Token 并实时查看思考过程，避免长时间等待完整响应。

> 用量统计中展示的是单次调用的整体耗时（含思考 Token 的生成时间），并非单个 Token 的生成延迟。

Q：如何以非流式（同步）方式调用深度思考模型？

本文示例默认采用流式输出（推荐，可实时查看思考过程、避免长时间等待）。商业版深度思考模型（如 qwen-plus、qwen3-max、qwen-flash 等）也支持非流式（同步）输出，一次性返回完整的思考过程与回复。

> 将流式示例改为非流式时，请同步修改**结果解析代码**：非流式调用返回的是完整的响应对象（`completion`），**不能**再像流式示例那样通过 `for chunk in completion` 迭代（否则会报错 `'tuple' object has no attribute 'choices'`），而应直接读取 `completion.choices[0].message.reasoning_content`（思考过程）与 `completion.choices[0].message.content`（回复内容）。此外，`stream=False` 时不能设置 `stream_options` 参数。

以下以 OpenAI 兼容接口、非流式调用 qwen3.8-max 开启思考模式为例：

```
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",  # 请替换为支持非流式输出的深度思考模型
    messages=[{"role": "user", "content": "你是谁"}],
    extra_body={"enable_thinking": True},
    stream=False,  # 非流式（同步）输出；stream=False 时不能设置 stream_options
)

# 非流式返回完整响应对象，直接读取 message，无需（也不能）迭代
message = completion.choices[0].message
print("=" * 20 + "思考过程" + "=" * 20 + "\n")
print(getattr(message, "reasoning_content", "") or "")
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
print(message.content)
```

> 部分模型（如 qwen3-235b-a22b、qwen3-32b 等开源版）仅支持流式输出，非流式调用会报错 `parameter.enable_thinking only support stream call`，此类模型请使用流式调用。

Q： 免费额度 用完后如何购买 Token？

前往[费用与成本](https://usercenter2.aliyun.com/home)中心充值，保持账户余额充足即可正常调用模型。

> 超出免费额度后自动扣费，出账周期为分钟级，消费明细请前往 \*\*[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)\*\* 进行查看。

Q：如何接入 Chatbox 、 Cherry Studio 、 Cline 或 Dify ？

请根据所用工具参考以下步骤：

> 以下以常用工具为例，其他大模型工具的接入方法类似。

#### Chatbox

请参见[Chatbox](https://help.aliyun.com/zh/model-studio/cline-tool)。

#### Cherry Studio

请参见[Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。

#### Cline

请参见[Cline](raw/model-user-guide/use-chat-client-or-development-tool/cline.md)。

#### Dify

请参见[Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

Q： 可以上传图片或文档进行提问吗 ？

本文涉及的模型仅支持文本输入。Qwen3-VL、QVQ 模型支持图片深度思考，[Qwen- Long](raw/model-user-guide/model-experience/text-generation-model/specialized-models/long-context-qwen-long.md)模型支持文档输入。

Q：如何在使用 LangChain 时输出思考过程？

请按以下步骤操作：

1.  **更新依赖库**
    
    将 `langchain_community` 和 `dashscope` 更新到最新版本：
    

```
pip install -U langchain_community dashscope
```

2.  **调用深度思考模型**
    
    通过以下代码分别打印思考过程与回复内容：
    

```
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

chatLLM = ChatTongyi(
    # 您可按需更换为其它深度思考模型
    model="qwen3.8-max",
    model_kwargs={
        "enable_thinking":True
    }
)
completion = chatLLM.stream(
    [HumanMessage(content="你是谁")])
is_answering = False
print("="*20+"思考过程 "+"="*20)
for chunk in completion:
    if chunk.additional_kwargs.get("reasoning_content"):
        print(chunk.additional_kwargs.get("reasoning_content"),end="",flush=True)
    else:
        if not is_answering:
            print("\n"+"="*20+"回复内容"+"="*20)
            is_answering = True
        print(chunk.content,end="",flush=True)
```

输出示例：

```
====================思考过程 ====================
好的，用户问“你是谁”，我需要给出一个准确且友好的回答。首先，我应该介绍自己的名字和基本功能，让用户了解我的用途。然后，可能需要提到我是通义实验室研发的，这样增加权威性。还要说明我能做什么，比如回答问题、创作文字等，这样用户知道可以怎么使用我。同时，保持语气亲切，避免太技术化的术语，让回答更易懂。另外，可能需要检查是否有遗漏的信息，比如多语言支持或者应用场景，但用户的问题比较基础，可能不需要太详细。最后，确保回答简洁明了，不冗长，符合用户的快速获取信息的需求。
====================回复内容====================
我是Qwen3，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字（如写故事、公文、邮件、剧本等）、进行逻辑推理、编程，甚至表达观点和玩游戏。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，旨在为全球用户提供高效、便捷的服务。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

Q：如何查看Token 消耗 量 及 调用次数？

模型调用完**一小时后**，在模型监控（[北京](https://bailian.console.aliyun.com/model/telemetry)或[新加坡](https://bailian.console.aliyun.com/model/telemetry)）页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6923304571/p992753.png)

Q：长提示词生成失败或超时怎么办？

使用长提示词调用模型时出现生成失败或响应超时，通常是因为开启了思考模式（`enable_thinking` 为 `true`）。思考模式会增加处理时间，长提示词场景下可能导致响应被截断或请求超时。

解决方案：

-   关闭思考模式：将 `enable_thinking` 设为 `false`，处理时间可从约 50 秒降至约 30 秒。
-   开启流式输出：将 `stream` 设为 `true`，避免非流式调用的超时限制。
-   调大超时时间：如需保留思考模式，请将客户端超时时间设为 180 秒以上。

Q：使用第三方客户端调用深度思考模型时，输出思考标签后客户端断连怎么办？

该问题属于客户端侧问题，并非模型限制思考过程输出。百炼平台通过 `enable_thinking` 参数控制思考模式开关，模型返回结果中的 `reasoning_content` 字段包含完整思考过程内容，模型侧会正常返回思考内容。断连通常由客户端网络波动或客户端版本兼容问题引起。

排查步骤：

-   检查客户端网络连接的稳定性。
-   将客户端升级至最新版本。
-   查看客户端日志，确认断连时间点与思考标签输出的关联。

您也可以通过 DashScope API 直接调用模型，验证思考功能是否正常工作。

Q：使用视觉模型（如 qwen-vl-plus）进行图片安全判断时，模型结论与内容描述矛盾怎么办？

视觉模型输出的安全判断是模型生成文本的一部分，并非独立的内容审核裁决。该结论可能随模型版本和所在区域不同而变化，也可能与同一次响应中的内容描述不一致，因此不建议将其作为内容合规的唯一依据。

如果您需要稳定、统一的安全判断标准，请接入 AI 安全护栏，对模型的输入与输出进行独立的内容审核。具体请参见[AI 安全护栏](raw/model-user-guide/security-and-compliance/content-security.md)。

## API 参考

深度思考模型的输入输出参数，请参见[文本生成](raw/model-api-reference/qwen-api-reference.md)。

## 错误码

执行报错时，请参见[错误码](raw/model-api-reference/preparations/error-code.md)排查解决。

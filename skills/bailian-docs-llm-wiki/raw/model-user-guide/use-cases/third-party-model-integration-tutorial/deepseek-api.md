# DeepSeek大语言模型

本文档介绍如何在阿里云百炼平台通过OpenAI兼容接口或DashScope SDK调用DeepSeek系列模型。

## **快速开始**

deepseek-v4-pro 是 DeepSeek 系列最新模型，在编程、数学和通用任务方面表现出色。您可以通过`enable_thinking`参数在思考与非思考模式之间切换。以下示例展示如何调用思考模式的 deepseek-v4-pro 模型。

需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)。

## **OpenAI兼容**

**说明**

`enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK通过 `extra_body`传入，Node.js SDK作为顶层参数传入。`reasoning_effort`是 OpenAI 标准参数，可直接作为顶层参数传入。

## **Python**

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
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

### **返回结果**

```
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
```

## **Node.js**

### **示例代码**

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

### **返回结果**

```
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
```

## **HTTP**

### **示例代码**

## **curl**

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
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

## **DashScope**

## **Python**

### **示例代码**

```
import os
from dashscope import Generation

# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]

completion = Generation.call(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="deepseek-v4-pro",
    messages=messages,
    result_format="message",  # 设置结果格式为 message
    enable_thinking=True,
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
    if "reasoning_content" in message:
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

### **返回结果**

```
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
```

## **Java**

### **示例代码**

**重要**

DashScope Java SDK版本需要不低于2.19.4。

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
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("An exception occurred: " + e.getMessage());
        }
    }
}
```

### **返回结果**

```
====================思考过程====================

嗯，用户问了一个非常简单的自我介绍问题："你是谁"。

我需要明确自己的身份，用简洁友好的方式介绍我是DeepSeek，说明我的创造者、基本特性和可提供的帮助。

想到了可以这样组织回答：先直接表明身份，说明由深度求索公司创造，然后列出一些关键特点（免费、长上下文、文件上传等），最后以友好的邀请结束，询问是否需要帮助。
====================完整回复====================

你好！我是 DeepSeek，由深度求索公司创造的 AI 助手。

我可以帮你解答各种问题、进行文字创作、分析文档、编程辅助等等。我最大的特点是**免费使用**、**超长上下文**（能一次处理整本三体三部曲那么多内容）、支持**文件上传**和**联网搜索**（需手动开启）。

有什么我可以帮你的吗？不管是学习、工作还是日常闲聊，我都很乐意陪你聊聊！
```

## **HTTP**

### **示例代码**

## **curl**

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
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

## **推理强度（reasoning\_effort）**

deepseek-v4-pro 和 deepseek-v4-flash 默认开启思考模式。通过`reasoning_effort`参数可以调整推理强度，可选值为`high`和`max`，默认为`high`。

**说明**

设为`low`或`medium`时会映射为`high`，设为`xhigh`时会映射为`max`。

## **OpenAI兼容**

## **Python**

```
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
    reasoning_effort="high",
)
print(completion.choices[0].message.content)
```

## **Node.js**

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const completion = await openai.chat.completions.create({
    model: "deepseek-v4-pro",
    messages: [{ role: "user", content: "9.9和9.11哪个大" }],
    reasoning_effort: "high",
});
console.log(completion.choices[0].message.content);
```

## **curl**

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "deepseek-v4-pro",
    "messages": [{"role": "user", "content": "9.9和9.11哪个大"}],
    "reasoning_effort": "high"
}'
```

## **DashScope**

```
import os
from dashscope import Generation

response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
    reasoning_effort="high",
    result_format="message",
)
print(response.output.choices[0].message.content)
```

## **其它功能**

**模型**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#dd5a3dca390k9)

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)

deepseek-v4-pro

支持

支持

支持

支持

不支持

不支持

deepseek-v4-flash

支持

支持

支持

支持

不支持

不支持

deepseek-v3.2

支持

支持

支持

支持

不支持

不支持

deepseek-v3.2-exp

支持

支持

> 仅支持非思考模式。

支持

不支持

不支持

不支持

deepseek-v3.1

支持

支持

> 仅支持非思考模式。

支持

支持

不支持

不支持

deepseek-r1

支持

支持

支持

支持

不支持

不支持

deepseek-r1-0528

支持

支持

支持

不支持

不支持

不支持

deepseek-v3

支持

支持

支持

支持

不支持

不支持

蒸馏模型

支持

不支持

不支持

不支持

不支持

不支持

## **参数默认值**

**模型**

**temperature**

**top\_p**

**repetition\_penalty**

**presence\_penalty**

**max\_tokens**

**thinking\_budget**

deepseek-v4-pro

1.0

1.0

\-

\-

共393,216

deepseek-v4-flash

1.0

1.0

\-

\-

共393,216

deepseek-v3.2

1.0

0.95

\-

\-

65,536

32,768

deepseek-v3.2-exp

0.6

0.95

1.0

\-

65,536

32,768

deepseek-v3.1

0.6

0.95

1.0

\-

65,536

32,768

deepseek-r1

0.6

0.95

\-

1

16,384

32,768

deepseek-r1-0528

0.6

0.95

\-

1

16,384

32,768

蒸馏版

0.6

0.95

\-

1

16,384

16,384

deepseek-v3

0.7

0.6

\-

\-

16,384

\-

-   “-” 表示没有默认值，也不支持设置。
    
-   deepseek-r1、deepseek-r1-0528、蒸馏版模型不支持设置以上参数值。
    
-   参数含义请参考[OpenAI兼容-Chat](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions)。
    

## **模型列表与计费**

-   混合思考模型（通过`enable_thinking`参数控制是否思考）：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1
    
-   仅思考模型（回复前总会思考）：deepseek-r1、deepseek-r1-0528
    
-   非思考模型：deepseek-v3
    

deepseek-v4-pro 在编程、数学和通用任务方面表现出色，deepseek-v4-flash 快速且经济高效，推荐优先使用 deepseek-v4-pro。

模型上下文长度与价格信息请参见百炼控制台。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## **常见问题**

### [免费额度](https://bailian.console.aliyun.com/#/model-market/detail/deepseek-r1)**用完后如何购买 Token？**

访问[费用与成本](https://usercenter2.aliyun.com/home)中心进行充值，确保您的账户没有欠费即可调用 DeepSeek 模型。

> 调用 DeepSeek 模型会自动扣费，出账周期为分钟级，消费明细请前往 \*\*[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)\*\* 进行查看。

### **如何接入**[Chatbox](https://chatboxai.app/zh)**、**[Cherry Studio](https://cherry-ai.com/)**或**[Dify](https://cloud.dify.ai/apps)**？**

此处以常用工具为例进行说明，其它大模型工具的接入方式类似。

## **Chatbox**

请参见[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)。

## **Cherry Studio**

请参见[Cherry Studio](https://help.aliyun.com/zh/model-studio/cherry-studio)。

## **Dify**

请参见[Dify](https://help.aliyun.com/zh/model-studio/dify)。

### 可以上传图片或文档进行提问吗**？**

DeepSeek 模型仅支持文本输入，不支持图片或文档输入。如需图片输入，请使用[千问VL](https://help.aliyun.com/zh/model-studio/vision)模型；如需文档输入，请使用[Qwen-Long](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)模型。

### **如何查看Token**消耗**量**及**调用次数？**

模型调用完**一小时后**，在[模型观测](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8923304571/p992752.png)

### **还有哪些使用DeepSeek的方式？**

在百炼平台使用DeepSeek有三种方式：

1.  在线体验：访问[模型广场](https://bailian.console.aliyun.com/#/model-market)。
    
2.  通过API或客户端（如Chatbox）调用模型：请参考本文内容。
    
3.  0代码构建大模型应用：请参考[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)或[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)。
    

如需自行部署DeepSeek，请参考[技术解决方案](https://www.aliyun.com/solution/tech-solution/deepseek-r1-for-platforms)。

## **错误码**

如果执行报错，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

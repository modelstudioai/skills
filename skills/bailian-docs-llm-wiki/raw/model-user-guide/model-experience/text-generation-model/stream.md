# 流式输出

在实时聊天或长文本生成应用中，长时间的等待会损害用户体验并可能导致触发服务端超时，导致任务失败。流式输出通过持续返回模型生成的文本片段，解决了这两个核心问题。

## 工作原理

流式输出基于 Server-Sent Events (SSE) 协议。发起流式请求后，服务端与客户端建立持久化 HTTP 连接。模型每生成一个文本块（称为 chunk），立即通过连接推送。全部内容生成后，服务端发送结束信号。

客户端监听事件流，实时接收并处理文本块，例如逐字渲染界面。这与非流式调用（一次性返回所有内容）形成对比。

> 以上组件仅供您参考，并未真实发送请求。

## 计费说明

流式输出计费规则与非流式调用完全相同，根据请求的输入Token数和输出Token数计费。

请求中断时，输出 Token 仅计算服务端收到终止请求前已生成的部分。

## 如何使用

**重要**Qwen3 开源版、QwQ 商业版与开源版、QVQ 、Qwen-Omni等模型仅支持流式输出方式调用。

### 步骤一：配置 API Key 并选择地域

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

> 将API Key配置为环境变量（`DASHSCOPE_API_KEY`）比在代码中硬编码更安全。

### 步骤二：发起流式请求

#### OpenAI兼容

-   **如何开启**
    
    设置 `stream` 为 `true` 即可。
    
-   **查看 Token 消耗**
    
    OpenAI 协议默认不返回 Token 消耗量，需设置`stream_options={"include_usage": true}`，使**最后一个返回的数据块**包含Token消耗信息。
    

#### Python

```
import os
from openai import OpenAI

# 1. 准备工作：初始化客户端
client = OpenAI(
    # 建议通过环境变量配置API Key，避免硬编码。
    api_key=os.environ["DASHSCOPE_API_KEY"],
    # API Key与地域强绑定，请确保base_url与API Key的地域一致。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2. 发起流式请求
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请介绍一下自己"}
    ],
    stream=True,
    stream_options={"include_usage": True}
)

# 3. 处理流式响应
# 用列表暂存响应片段，最后 join 比逐次 += 字符串更高效
content_parts = []
print("AI: ", end="", flush=True)

for chunk in completion:
    if chunk.choices:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        content_parts.append(content)
    elif chunk.usage:
        print("\n--- 请求用量 ---")
        print(f"输入 Tokens: {chunk.usage.prompt_tokens}")
        print(f"输出 Tokens: {chunk.usage.completion_tokens}")
        print(f"总计 Tokens: {chunk.usage.total_tokens}")

full_response = "".join(content_parts)
# print(f"\n--- 完整回复 ---\n{full_response}")
```

### 返回结果

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时告诉我！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 87
总计 Tokens: 113
```

#### Node.js

```
import OpenAI from "openai";

async function main() {
    // 1. 准备工作：初始化客户端
    // 建议通过环境变量配置API Key，避免硬编码。
    if (!process.env.DASHSCOPE_API_KEY) {
        throw new Error("请设置环境变量 DASHSCOPE_API_KEY");
    }
    const client = new OpenAI({
        // 若没有配置环境变量，请将下行替换为：apiKey:"sk-xxx",
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    });

    try {
        // 2. 发起流式请求
        const stream = await client.chat.completions.create({
            model: "qwen-plus",
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: "请介绍一下自己" },
            ],
            stream: true,
            // 目的：在最后一个chunk中获取本次请求的Token用量。
            stream_options: { include_usage: true },
        });

        // 3. 处理流式响应
        const contentParts = [];
        process.stdout.write("AI: ");

        for await (const chunk of stream) {
            // 最后一个chunk不包含choices，但包含usage信息。
            if (chunk.choices && chunk.choices.length > 0) {
                const content = chunk.choices[0]?.delta?.content || "";
                process.stdout.write(content);
                contentParts.push(content);
            } else if (chunk.usage) {
                // 请求结束，打印Token用量。
                console.log("\n--- 请求用量 ---");
                console.log(`输入 Tokens: ${chunk.usage.prompt_tokens}`);
                console.log(`输出 Tokens: ${chunk.usage.completion_tokens}`);
                console.log(`总计 Tokens: ${chunk.usage.total_tokens}`);
            }
        }

        const fullResponse = contentParts.join("");
        // console.log(`\n--- 完整回复 ---\n${fullResponse}`);

    } catch (error) {
        console.error("请求失败:", error);
    }
}

main();
```

### 返回结果

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时向我提问！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 89
总计 Tokens: 115
```

#### curl

### 请求

```
# ======= 重要提示 =======
# 确保已设置环境变量 DASHSCOPE_API_KEY
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
--no-buffer \
-d '{
    "model": "qwen-plus",
    "messages": [
        {"role": "user", "content": "你是谁？"}
    ],
    "stream": true,
    "stream_options": {"include_usage": true}
}'
```

### 响应

返回数据为符合 SSE 协议的流式响应。每一行 `data:` 都代表一个数据块。

```
data: {"choices":[{"delta":{"content":"","role":"assistant"},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"finish_reason":null,"delta":{"content":"我是"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"来自"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"阿里"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"云的超大规模语言"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"模型，我叫通义千问"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"。"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"finish_reason":"stop","delta":{"content":""},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":22,"completion_tokens":17,"total_tokens":39},"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: [DONE]
```

-   `data:`: 消息的数据负载，通常是一个JSON字符串。
-   `[DONE]`: 表示整个流式响应已结束。

#### DashScope

-   **如何开启**
    
    根据使用方式（Python SDK、Java SDK、cURL）不同，开启流式输出的方式不同：
    
    -   Python SDK：设置 `stream` 参数为 `True`；
    -   Java SDK：通过`streamCall`接口调用；
    -   cURL：设置 Header 参数`X-DashScope-SSE`为`enable`。
-   **是否启动增量输出**
    
    DashScope 协议支持增量与非增量式流式输出：
    
    -   **增量**（推荐）：每个数据块仅包含新生成的内容，设置`incremental_output`为`true`启动增量式流式输出。
        
        > 示例：\["我爱","吃","苹果"\]
        
    -   **非增量**：每个数据块都包含之前已生成的内容，造成网络带宽浪费和客户端处理压力。设置`incremental_output`为`false`启动非增量式流式输出。
        
        > 示例：\["我爱","我爱吃","我爱吃苹果"\]
        
-   **查看 Token 消耗**
    
    每个数据块都包含实时的 Token 消耗信息。
    

#### Python

```
import os
from http import HTTPStatus
import dashscope
from dashscope import Generation

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 1. 准备工作：配置API Key
# 建议通过环境变量配置API Key，避免硬编码。
try:
    dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
except KeyError:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

# 2. 发起流式请求
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "请介绍一下自己"},
]

try:
    responses = Generation.call(
        model="qwen-plus",
        messages=messages,
        result_format="message",
        stream=True,
        # 关键：设置为True以获取增量输出，性能更佳。
        incremental_output=True,
    )

    # 3. 处理流式响应
    content_parts = []
    print("AI: ", end="", flush=True)

    for resp in responses:
        if resp.status_code == HTTPStatus.OK:
            content = resp.output.choices[0].message.content
            print(content, end="", flush=True)
            content_parts.append(content)

            # 检查是否是最后一个包
            if resp.output.choices[0].finish_reason == "stop":
                usage = resp.usage
                print("\n--- 请求用量 ---")
                print(f"输入 Tokens: {usage.input_tokens}")
                print(f"输出 Tokens: {usage.output_tokens}")
                print(f"总计 Tokens: {usage.total_tokens}")
        else:
            # 处理错误情况
            print(
                f"\n请求失败: request_id={resp.request_id}, code={resp.code}, message={resp.message}"
            )
            break

    full_response = "".join(content_parts)
    # print(f"\n--- 完整回复 ---\n{full_response}")

except Exception as e:
    print(f"发生未知错误: {e}")
```
**返回结果**
```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时向我提问！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 91
总计 Tokens: 117
```

#### Java

```
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import io.reactivex.Flowable;
import io.reactivex.schedulers.Schedulers;

import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {
        Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }
    public static void main(String[] args) {
        // 1. 获取 API Key
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("请设置环境变量 DASHSCOPE_API_KEY");
            return;
        }

        // 2. 初始化 Generation 实例
        Generation gen = new Generation();
        CountDownLatch latch = new CountDownLatch(1);

        // 3. 构建请求参数
        GenerationParam param = GenerationParam.builder()
                .apiKey(apiKey)
                .model("qwen-plus")
                .messages(Arrays.asList(
                        Message.builder()
                                .role(Role.USER.getValue())
                                .content("介绍一下自己")
                                .build()
                ))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .incrementalOutput(true) // 开启增量输出，流式返回
                .build();
        // 4. 发起流式调用并处理响应
        try {
            Flowable<GenerationResult> result = gen.streamCall(param);
            StringBuilder fullContent = new StringBuilder();
            System.out.print("AI: ");
            result
                    .subscribeOn(Schedulers.io()) // IO线程执行请求
                    .observeOn(Schedulers.computation()) // 计算线程处理响应
                    .subscribe(
                            // onNext: 处理每个响应片段
                            message -> {
                                String content = message.getOutput().getChoices().get(0).getMessage().getContent();
                                String finishReason = message.getOutput().getChoices().get(0).getFinishReason();
                                // 输出内容
                                System.out.print(content);
                                fullContent.append(content);
                                // 当 finishReason 不为 null 时，表示是最后一个 chunk，输出用量信息
                                if (finishReason != null && !"null".equals(finishReason)) {
                                    System.out.println("\n--- 请求用量 ---");
                                    System.out.println("输入 Tokens：" + message.getUsage().getInputTokens());
                                    System.out.println("输出 Tokens：" + message.getUsage().getOutputTokens());
                                    System.out.println("总 Tokens：" + message.getUsage().getTotalTokens());
                                }
                                System.out.flush(); // 立即刷新输出
                            },
                            // onError: 处理错误
                            error -> {
                                System.err.println("\n请求失败: " + error.getMessage());
                                latch.countDown();
                            },
                            // onComplete: 完成回调
                            () -> {
                                System.out.println(); // 换行
                                // System.out.println("完整响应: " + fullContent.toString());
                                latch.countDown();
                            }
                    );
            // 主线程等待异步任务完成
            latch.await();
            System.out.println("程序执行完成");
        } catch (Exception e) {
            System.err.println("请求异常: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

### 返回结果

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时向我提问！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 91
总计 Tokens: 117
```

#### curl

### 请求

```
# ======= 重要提示 =======
# 确保已设置环境变量 DASHSCOPE_API_KEY
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message",
        "incremental_output":true
    }
}'
```

### 响应

响应遵循 Server-Sent Events (SSE) 格式，每条消息包含：

-   id: 数据块编号；
-   event: 事件类型，固定为result；
-   HTTP 状态码信息；
-   data：JSON 数据部分。

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"我是","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":27,"output_tokens":1,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"通义千","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":30,"output_tokens":4,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"问，阿里巴巴","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":33,"output_tokens":7,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

...

id:13
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"或需要帮助，欢迎随时","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":90,"output_tokens":64,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:14
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我！","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":92,"output_tokens":66,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:15
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":92,"output_tokens":66,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}
```

## 多模态模型的流式输出

多模态模型支持在对话中加入图片、音频等内容，其流式输出的实现方式与文本模型主要有以下不同：

-   **用户消息（user message）的构造方式**：多模态模型的输入不仅包括文本，还包含图片、音频等多模态信息。
-   **DashScope SDK接口：**使用 DashScope Python SDK 时，需调用 MultiModalConversation 接口；使用DashScope Java SDK 时，则调用 MultiModalConversation 类。

> 多模态模型请参见：[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)、[文字提取](raw/model-user-guide/model-experience/vision-model/qwen-vl-ocr.md)、[界面交互](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)、[音频理解-Qwen3-Omni-Captioner](raw/model-user-guide/model-experience/text-generation-model/specialized-models/qwen3-omni-captioner.md)、[Kimi](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)等，Qwen-Omni 模型**仅支持流式输出**，因其输出可包含**文本**或**音频**等多模态内容，结果解析方式与其他模型不同，具体请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni#4d96cc766ehhi)。

#### OpenAI兼容

Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),

    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-vl-plus",  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=[
        {"role": "user",
         "content": [{"type": "image_url",
                    "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
                    {"type": "text", "text": "图中描绘的是什么景象？"}]}],
    stream=True,
  # stream_options={"include_usage": True}
)
full_content = ""
print("流式输出内容为：")
for chunk in completion:
    # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
    if chunk.choices and chunk.choices[0].delta.content != "":
        full_content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content)
print(f"完整内容为：{full_content}")
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const completion = await openai.chat.completions.create({
    model: "qwen3-vl-plus",  // 可按需更换为其它多模态模型，并修改相应的 messages
    messages: [
        {role: "user",
        content: [{"type": "image_url",
                    "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
                    {"type": "text", "text": "图中描绘的是什么景象？"}]}],
    stream: true,
 // stream_options: { include_usage: true },

});

let fullContent = ""
console.log("流式输出内容为：")
for await (const chunk of completion) {
    // 如果stream_options.include_usage为true，则最后一个chunk的choices字段为空数组，需要跳过（可以通过chunk.usage获取 Token 使用量）
    if (chunk.choices[0] && chunk.choices[0].delta.content != null) {
      fullContent += chunk.choices[0].delta.content;
      console.log(chunk.choices[0].delta.content);
    }
}
console.log(`完整输出内容为：${fullContent}`)
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3-vl-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
          }
        },
        {
          "type": "text",
          "text": "图中描绘的是什么景象？"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true}
}'
```

#### DashScope

Python

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"text": "图中描绘的是什么景象?"}
        ]
    }
]

responses = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3-vl-plus',  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages,
    stream=True,
    incremental_output=True
    )

full_content = ""
print("流式输出内容为：")
for response in responses:
    if response.output.choices[0].message.content:
        print(response.output.choices[0].message.content[0]['text'])
        full_content += response.output.choices[0].message.content[0]['text']
print(f"完整内容为：{full_content}")
```

Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
     static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("text", "图中描绘的是什么景象？"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-vl-plus")  // 可按需更换为其它多模态模型，并修改相应的 messages
                .messages(Arrays.asList(userMessage))
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                List<Map<String, Object>> content = item.getOutput().getChoices().get(0).getMessage().getContent();
                    // 判断content是否存在且不为空
                if (content != null &&  !content.isEmpty()) {
                    System.out.println(content.get(0).get("text"));
                    }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"text": "图中描绘的是什么景象？"}
                ]
            }
        ]
    },
    "parameters": {
        "incremental_output": true
    }
}'
```

## 思考模型的流式输出

思考模型会先返回`reasoning_content`（思考过程），再返回`content`（回复内容）。可根据数据包状态判断当前为思考或是回复阶段。

> 思考模型详情参见：[深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)、[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)、[视觉推理](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)。

> Qwen3-Omni-Flash（思考模式）实现流式输出请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni#4d96cc766ehhi)。

#### OpenAI兼容

以下是使用 OpenAI Python SDK 以流式方式调用思考模式 qwen-plus 模型时返回的数据格式：

```
# 思考阶段
...
ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content='覆盖所有要点，同时')
ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content='自然流畅。')
# 回复阶段
ChoiceDelta(content='你好！我是**通', function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content=None)
ChoiceDelta(content='义千问**（', function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content=None)
...
```

-   若`reasoning_content`不为 None，`content` 为 `None`，则当前处于思考阶段；
-   若`reasoning_content`为 None，`content` 不为 `None`，则当前处于回复阶段；
-   若两者均为 `None`，则阶段与前一包一致。

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
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    # enable_thinking 参数开启思考过程，qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
    extra_body={"enable_thinking": True},
    stream=True,
    # stream_options={
    #     "include_usage": True
    # },
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

好的，用户问“你是谁”，我需要给出一个准确且友好的回答。首先，我要确认自己的身份，即通义千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如回答问题、创作文字、逻辑推理等。同时，要保持语气亲切，避免过于技术化，让用户感觉轻松。还要注意不要使用复杂术语，确保回答简洁明了。另外，可能需要加入一些互动元素，邀请用户提问，促进进一步交流。最后，检查是否有遗漏的重要信息，比如我的中文名称“通义千问”和英文名称“Qwen”，以及所属公司和实验室。确保回答全面且符合用户期望。
====================完整回复====================

你好！我是通义千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以回答问题、创作文字、进行逻辑推理、编程等，旨在为用户提供高质量的信息和服务。你可以叫我Qwen，或者直接叫我通义千问。有什么我可以帮你的吗？
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
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        const stream = await openai.chat.completions.create({
            // 您可以按需更换为其它 Qwen3 模型、QwQ模型或DeepSeek-R1 模型
            model: 'qwen-plus',
            messages,
            stream: true,
            // enable_thinking 参数开启思考过程，qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
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

好的，用户问“你是谁”，我需要回答我的身份。首先，我应该明确说明我是通义千问，由阿里云开发的超大规模语言模型。接下来，可以提到我的主要功能，比如回答问题、创作文字、逻辑推理等。还要强调我的多语言支持，包括中文和英文，这样用户知道我可以处理不同语言的请求。另外，可能需要解释一下我的应用场景，比如学习、工作和生活中的帮助。不过用户的问题比较直接，可能不需要太详细的信息，保持简洁明了。同时，要确保语气友好，邀请用户进一步提问。检查有没有遗漏的重要信息，比如我的版本或最新更新，但可能用户不需要那么详细。最后，确认回答准确无误，没有错误信息。
====================完整回复====================

我是通义千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等多种任务，支持中英文等多种语言。如果你有任何问题或需要帮，欢迎随时告诉我！
```

#### HTTP

### 示例代码

#### curl

Qwen3 开源版模型需要设置`enable_thinking`为`true`来开启思考模式；`enable_thinking`对 qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型无效。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
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
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":10,"completion_tokens":360,"total_tokens":370},"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: [DONE]
```

#### DashScope

以下为 DashScope Python SDK 调用思考模式的 qwen-plus 模型时，流式返回的数据包格式：

```
# 思考阶段
...
{"role": "assistant", "content": "", "reasoning_content": "信息量大，"}
{"role": "assistant", "content": "", "reasoning_content": "让用户觉得有帮助。"}
# 回复阶段
{"role": "assistant", "content": "我是通义千问", "reasoning_content": ""}
{"role": "assistant", "content": "，由通义实验室研发", "reasoning_content": ""}
...
```

-   若`reasoning_content`不为 ""，`content` 为 ""，则当前处于思考阶段；
-   若`reasoning_content`为 ""，`content` 不为 ""，则当前处于回复阶段；
-   若两者均为 ""，则阶段与前一包一致。

#### Python

### 示例代码

```
import os
from dashscope import Generation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [{"role": "user", "content": "你是谁？"}]

completion = Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 可按需更换为其它深度思考模型
    model="qwen-plus",
    messages=messages,
    result_format="message", # Qwen3开源版模型只支持设定为"message"；为了更好的体验，其它模型也推荐您优先设定为"message"
    # 开启深度思考，该参数对qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ、DeepSeek-R1 模型无效
    enable_thinking=True,
    stream=True,
    incremental_output=True, # Qwen3开源版模型只支持 true；为了更好的体验，其它模型也推荐您优先设定为 true
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
    if (
        chunk.output.choices[0].message.content == ""
        and chunk.output.choices[0].message.reasoning_content == ""
    ):
        pass
    else:
        # 如果当前为思考过程
        if (
            chunk.output.choices[0].message.reasoning_content != ""
            and chunk.output.choices[0].message.content == ""
        ):
            print(chunk.output.choices[0].message.reasoning_content, end="", flush=True)
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != "":
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content, end="", flush=True)
            answer_content += chunk.output.choices[0].message.content

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

### 返回结果

```
====================思考过程====================
好的，用户问：“你是谁？”我需要回答这个问题。首先，我要明确自己的身份，即通义千问，由阿里云开发的超大规模语言模型。接下来，要说明我的功能和用途，比如回答问题、创作文字、逻辑推理等。同时，要强调我的目标是成为用户的得力助手，提供帮助和支持。

在表达时，要保持口语化，避免使用专业术语或复杂句式。可以加入一些亲切的语气词，比如“你好呀～”，让对话更自然。另外，要确保信息准确，不遗漏关键点，比如我的开发者、主要功能和使用场景。

还要考虑用户可能的后续问题，比如具体的应用例子或技术细节，所以在回答中可以适当埋下伏笔，引导用户进一步提问。例如，提到“无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助”，这样既全面又开放。

最后，检查回答是否流畅，有没有重复或冗余的信息，确保简洁明了。同时，保持友好和专业的平衡，让用户感受到既亲切又可靠。
====================完整回复====================
你好呀～我是通义千问，是阿里云开发的一款超大规模语言模型。我能够回答问题、创作文字、进行逻辑推理、编程等等，旨在为用户提供帮助和支持。无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助。有什么我可以帮你的吗？
```

#### Java

### 示例代码

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
import com.alibaba.dashscope.utils.Constants;
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
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

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
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处使用qwen-plus模型，可以按需替换为其它深度思考模型
                .model("qwen-plus")
                // 开启深度思考，对 qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ、DeepSeek-R1 模型无效
                .enableThinking(true)
                .incrementalOutput(true) // Qwen3开源版模型只支持 true；为了更好的体验，其它模型也推荐您优先设定为 true
                .resultFormat("message") // Qwen3开源版模型只支持设定为"message"；为了更好的体验，其它模型也推荐您优先设定为"message"
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
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
====================思考过程====================
好的，用户问“你是谁？”，我需要根据之前的设定来回答。首先，我的角色是通义千问，阿里巴巴集团旗下的超大规模语言模型。要保持口语化，简洁易懂。

用户可能刚接触我，或者想确认我的身份。应该先直接回答我是谁，然后简要说明我的功能和用途，比如回答问题、创作文字、编程等。还要提到支持多语言，这样用户知道我可以处理不同语言的需求。

另外，根据指导方针，要保持拟人性，所以语气要友好，可能用表情符号增加亲切感。同时，可能需要引导用户进一步提问或使用我的功能，比如问他们需要什么帮助。

需要注意不要使用复杂术语，避免冗长。检查是否有遗漏的关键点，比如多语言支持和具体能力。确保回答符合所有要求，包括口语化和简洁。
====================完整回复====================
你好！我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。有什么需要我帮忙的吗？
```

#### HTTP

### 示例代码

#### curl

混合思考模型需要设置`enable_thinking`为`true`来开启思考模式；`enable_thinking`对qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、 QwQ 与 DeepSeek-R1 模型无效。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
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

## 应用于生产环境

-   **性能与资源管理**：在后端服务中，为每个流式请求维持一个HTTP长连接会消耗资源。确保您的服务配置了合理的连接池大小和超时时间。在高并发场景下，监控服务的文件描述符（file descriptors）使用情况，防止耗尽。
    
-   **客户端渲染**：在Web前端，使用 `ReadableStream` 和 `TextDecoderStream` API 可以平滑地处理和渲染SSE事件流，提供最佳的用户体验。
    
-   [模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)：
    
    -   **关键指标**：监控**首Token延迟（Time to First Token, TTFT）**，该指标是衡量流式体验的核心。同时监控请求错误率和平均响应时长。
    -   **告警设置**：为API错误率（特别是4xx和5xx错误）的异常设置告警。
-   **Nginx代理配置**：若使用 Nginx 作为反向代理，其默认的输出缓冲（proxy\_buffering）会破坏流式响应的实时性。为确保数据能被即时推送到客户端，务必在Nginx配置文件中设置`proxy_buffering off`以关闭此功能。
    

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 常见问题

### Q：为什么返回数据中没有 usage 信息？

A：OpenAI 协议默认不返回 usage 信息，设置`stream_options`参数使得最后返回的包中包含 usage 信息。

### Q：开启流式输出对模型的回复效果是否有影响？

A：无影响，但部分模型仅支持流式输出，且非流式输出可能引发超时错误。建议优先使用流式输出。

### Q：非流式调用和流式调用有什么区别？

A：主要区别如下：

-   **超时限制**：非流式调用的最大超时时间不少于300秒，实际时长因部署区域与选用模型存在差异。
-   **输出结构**：非流式调用一次性返回完整的响应结果（单个JSON对象）。流式调用通过SSE协议逐步返回数据块（chunk），每个chunk包含部分生成内容，需要客户端拼接。
-   **功能兼容**：两者均支持JSON Mode、Function Call等功能特性，功能上没有差异。

建议优先使用流式输出，可以避免超时问题并获得更好的用户体验。

### Q：流式输出是否支持JSON Mode（结构化输出）？

A：支持。在请求中同时设置`stream`为`true`和`response_format`为`{"type": "json_object"}`即可。模型会以流式方式逐步返回JSON格式的内容片段，最终拼接后的完整输出为合法的JSON。

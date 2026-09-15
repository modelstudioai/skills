# 概述

文本生成模型根据自然语言提示词（Prompt）生成连贯、上下文相关的文本，支持聊天机器人、内容创作、文档摘要和代码生成等场景。

文本生成模型所需的输入可以是简单的关键词、一句话概述或更复杂的多步骤指令和上下文信息。常见应用场景：

-   **内容创作**：生成新闻文章、商品介绍及短视频脚本。
-   **客户服务**：构建全天候自动应答的聊天机器人，解答常见问题。
-   **文本翻译**：支持多语言之间的快速精准翻译。
-   **摘要提炼**：从长文、报告及邮件中提取关键信息。
-   **法律文档编写**：生成合同模板、法律意见书的基础框架。

更多示例可以参考[文本生成样例](https://bailian.console.aliyun.com/flow-agent/plugin-market/prompt)。

## 核心概念

文本生成模型的输入为提示词（Prompt），它由一个或多个消息（Message）对象构成。每条消息由角色（Role）和内容（Content）组成，具体为：

-   **系统消息（System Message）**：设定模型的角色定位、行为准则或特定任务指令。若不指定，默认为"You are a helpful assistant"。
-   **用户消息（User Message）**：用户向模型提出的问题、指令或输入内容。
-   **助手消息（Assistant Message）**：模型的回复内容。在多轮对话中，传入历史助手消息以维持上下文。

调用模型时，需构造一个由上述消息对象构成的数组`messages`。一个典型的请求通常由一条定义行为准则的 `system` 消息和一条用户提出的 `user` 消息组成。

> `system` 消息是可选的，但建议设定。明确模型的角色定位和行为约束，有助于获得更一致、可预测的输出。

```
[
    {"role": "system", "content": "你是一个有帮助的助手，需要提供精准、高效且富有洞察力的回应，随时准备协助用户处理各种任务与问题。"},
    {"role": "user", "content": "你是谁？"}
]
```

输出的响应对象中会包含模型回复的`assistant`消息。

```
{
    "role": "assistant",
    "content": "你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字、进行逻辑推理、编程等。我能够理解并生成多种语言，支持多轮对话和复杂任务处理。如果你有任何需要帮助的地方，尽管告诉我！"
}
```

## 快速开始

API 使用前提：已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。示例接入地址中的 `{WorkspaceId}` 为业务空间 ID，获取方式请参见[选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。

#### OpenAI兼容-Chat Completions API

#### Python

```
import os
from openai import OpenAI

try:
    client = OpenAI(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"},
        ],
    )
    print(completion.choices[0].message.content)
    # 如需查看完整响应，请取消下列注释
    # print(completion.model_dump_json())
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### Java

```
// 建议 OpenAI Java SDK版本 >= 3.5.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        try {
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
                    .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
                    .build();

            // 创建 ChatCompletion 参数
            ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                    .model("qwen3.8-max")
                    .addSystemMessage("You are a helpful assistant.")
                    .addUserMessage("你是谁？")
                    .build();

            // 发送请求并获取响应
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            String content = chatCompletion.choices().get(0).message().content().orElse("未返回有效内容");
            System.out.println(content);
            // 如需查看完整响应，请取消下列注释
            // System.out.println(chatCompletion);

        } catch (Exception e) {
            System.err.println("错误信息：" + e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
    }
}
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### Node.js

```
// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
const completion = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "你是谁？" }
    ],
});
console.log(completion.choices[0].message.content);
// 如需查看完整响应，请取消下列注释
// console.log(JSON.stringify(completion, null, 4));
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### Go

```
// OpenAI Go SDK版本不低于 v2.4.0
package main

import (
	"context"
	// 如需查看完整响应，请取消下方及代码末尾的注释
	// "encoding/json"
	"fmt"
	"os"

	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/option"
)

func main() {
	// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
	// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	client := openai.NewClient(
		option.WithAPIKey(apiKey),
		// 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
		option.WithBaseURL("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"),
	)
	chatCompletion, err := client.Chat.Completions.New(
		context.TODO(), openai.ChatCompletionNewParams{
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.SystemMessage("You are a helpful assistant."),
				openai.UserMessage("你是谁？"),
			},
			Model: "qwen3.8-max",
		},
	)

	if err != nil {
		fmt.Fprintf(os.Stderr, "请求失败: %v\n", err)
		// 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
		os.Exit(1)
	}

	if len(chatCompletion.Choices) > 0 {
		fmt.Println(chatCompletion.Choices[0].Message.Content)
	}
	// 如需查看完整响应，请取消下列注释
	// jsonData, _ := json.MarshalIndent(chatCompletion, "", "  ")
	// fmt.Println(string(jsonData))

}
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        string url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions";
        string jsonContent = @"{
            ""model"": ""qwen3.8-max"",
            ""messages"": [
                {
                    ""role"": ""system"",
                    ""content"": ""You are a helpful assistant.""
                },
                {
                    ""role"": ""user"",
                    ""content"": ""你是谁？""
                }
            ]
        }";

        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 如需查看完整响应，请取消下列注释
        // Console.WriteLine(result);

        // 解析JSON并只输出content部分
        using JsonDocument doc = JsonDocument.Parse(result);
        JsonElement root = doc.RootElement;

        if (root.TryGetProperty("choices", out JsonElement choices) &&
            choices.GetArrayLength() > 0)
        {
            JsonElement firstChoice = choices[0];
            if (firstChoice.TryGetProperty("message", out JsonElement message) &&
                message.TryGetProperty("content", out JsonElement content))
            {
                Console.WriteLine(content.GetString());
            }
        }
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            HttpResponseMessage response = await httpClient.PostAsync(url, content);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                // 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### PHP（HTTP）

```
<?php
// 设置请求的URL
// 各地域配置不同，请根据实际地域修改
$url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions';
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    "model" => "qwen3.8-max",
    "messages" => [
        [
            "role" => "system",
            "content" => "You are a helpful assistant."
        ],
        [
            "role" => "user",
            "content" => "你是谁？"
        ]
    ]
];
// 初始化cURL会话
$ch = curl_init();
// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
// 执行cURL会话
$response = curl_exec($ch);
// 检查是否有错误发生
// 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
$dataObject = json_decode($response);
$content = $dataObject->choices[0]->message->content;
echo $content;
// 如需查看完整响应，请取消下列注释
//echo $response;
?>
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### curl

各地域的base\_url和API Key不同，详情请参见[OpenAI兼容-Chat](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)和 [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

```
# 各地域配置不同，请根据实际地域修改
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}'
```

#### 返回结果

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 26,
        "completion_tokens": 66,
        "total_tokens": 92
    },
    "created": 1726127645,
    "system_fingerprint": null,
    "model": "qwen3.8-max",
    "id": "chatcmpl-81951b98-28b8-9659-ab07-xxxxxx"
}
```

#### OpenAI兼容-Responses API

Responses API是 Chat Completions API的演进版本，关于使用说明、代码示例和迁移指南，请参见 [OpenAI兼容-Responses](raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

#### Python

```
import os
from openai import OpenAI

try:
    client = OpenAI(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 各地域配置不同，请根据实际地域修改
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )

    response = client.responses.create(
        model="qwen3.8-max",
        input="简要介绍下你能做什么？"
    )

    print(response)
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

#### 返回结果

返回结果主要包含以下字段：

-   `id`：响应 ID。
    
-   `output`：输出列表。包含 `reasoning`（思考过程）和 `message`（回复内容）。
    
    > `reasoning` 仅在开启 [深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md) 时返回（如 Qwen3.6 系列默认开启）。
    
-   `usage`：Token 用量统计。
    

回复内容示例如下，完整响应请参考[curl](raw/model-user-guide/model-experience/text-generation-model/text-generation.md)。

```
你好！我是人工智能助手，基于截至 2026 年的知识库训练。以下是我能为你做的主要事情：

1.  **文字创作**：撰写文章、邮件、报告、故事、诗歌等。
2.  **代码辅助**：编写、调试、解释代码，支持多种主流编程语言。
3.  **知识问答**：回答科学、历史、文化、技术等领域的问题。
4.  **逻辑分析**：协助数学解题、数据分析、方案规划与决策支持。
5.  **语言翻译**：支持多种语言之间的准确互译。
6.  **日常对话**：聊天解闷、提供生活建议、角色扮演或学习辅导。

有什么具体任务需要我帮忙吗？随时告诉我！
```

#### Node.js

```
// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from "openai";

const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 各地域配置不同，请根据实际地域修改
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    try {
        const response = await openai.responses.create({
            model: "qwen3.8-max",
            input: "简要介绍下你能做什么？"
        });

        // 获取模型回复
        console.log(response);
    } catch (error) {
        console.error("错误信息：", error);
    }
}

main();
```

### 返回结果

返回结果主要包含以下字段：

-   `id`：响应 ID。
    
-   `output`：输出列表。包含 `reasoning`（思考过程）和 `message`（回复内容）。
    
    > `reasoning` 仅在开启 [深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md) 时返回（如 Qwen3.6 系列默认开启）。
    
-   `usage`：Token 用量统计。
    

回复内容示例如下，完整响应请参考[curl](raw/model-user-guide/model-experience/text-generation-model/text-generation.md)。

```
你好！我是人工智能助手，基于截至 2026 年的知识库训练。以下是我能为你做的主要事情：

1.  **文字创作**：撰写文章、邮件、报告、故事、诗歌等。
2.  **代码辅助**：编写、调试、解释代码，支持多种主流编程语言。
3.  **知识问答**：回答科学、历史、文化、技术等领域的问题。
4.  **逻辑分析**：协助数学解题、数据分析、方案规划与决策支持。
5.  **语言翻译**：支持多种语言之间的准确互译。
6.  **日常对话**：聊天解闷、提供生活建议、角色扮演或学习辅导。

有什么具体任务需要我帮忙吗？随时告诉我！
```

#### curl

```
# 各地域配置不同，请根据实际地域修改
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "简要介绍下你能做什么？"
}'
```

#### 返回结果

```
{
    "created_at": 1772249644,
    "id": "56ec1cc7-f246-448e-bdf9-b13838bc6xxx",
    "model": "qwen3.8-max",
    "object": "response",
    "output": [
        {
            "id": "msg_082d9e97-2317-4a74-9c07-fc46e4845xxx",
            "summary": [
                {
                    "text": "Thinking Process:\n\n1.  **Analyze the Request:**\n    *   User asks: \"简要介绍下你能做什么？\" (Briefly introduce what you can do?)\n\n...（篇幅原因，此处省略完整思考过程）",
                    "type": "summary_text"
                }
            ],
            "type": "reasoning"
        },
        {
            "content": [
                {
                    "annotations": [],
                    "text": "你好！我是人工智能助手。基于截至 2026 年的知识库，我可以为你提供以下帮助：\n\n1.  **内容创作**：撰写文章、邮件、故事、诗歌及各类文案。\n2.  **代码辅助**：编写、调试、解释代码，支持多种主流编程语言。\n3.  **知识问答**：回答科学、历史、文化等各类知识性问题。\n4.  **文本处理**：翻译、总结长文、提取关键信息、润色修改。\n5.  **逻辑与分析**：协助分析问题、提供建议、进行逻辑推理。\n\n请注意，我无法执行物理操作，且若无特定工具支持，无法访问实时互联网信息。有什么具体任务需要我协助吗？",
                    "type": "output_text"
                }
            ],
            "id": "msg_28643acb-1153-4d4f-84f8-19df29f11xxx",
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ],
    "parallel_tool_calls": false,
    "status": "completed",
    "tool_choice": "auto",
    "tools": [],
    "usage": {
        "input_tokens": 52,
        "input_tokens_details": {
            "cached_tokens": 0
        },
        "output_tokens": 1280,
        "output_tokens_details": {
            "reasoning_tokens": 1122
        },
        "total_tokens": 1332,
        "x_details": [
            {
                "input_tokens": 52,
                "output_tokens": 1280,
                "output_tokens_details": {
                    "reasoning_tokens": 1122
                },
                "total_tokens": 1332,
                "x_billing_type": "response_api"
            }
        ]
    }
}
```

#### DashScope

**重要**qwen3.8-2.4t-a95b、qwen3.7-max、qwen3.7-max-2026-05-20 和 qwen3.6-max-preview 仅支持文本接口，qwen3.8-max、qwen3.8-flash、qwen3.8-27b、qwen3.7-max-2026-06-08、Qwen3.6 和 Qwen3.5 系列的 DashScope API均需使用多模态接口。以下示例使用 qwen-plus（文本接口），可直接运行；若将模型替换为上述需使用多模态接口的模型，会提示 `url error` 错误。多模态接口的正确调用方法，请参见[图像、视频数据处理](https://help.aliyun.com/zh/model-studio/text-generation#270b260cb6or2)。

#### Python

```
import json
import os
from dashscope import Generation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]
response = Generation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # qwen3.7-max、qwen3.7-max-2026-05-20和qwen3.6-max-preview仅支持文本接口，qwen3.8-max、qwen3.7-max-2026-06-08、Qwen3.6、Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
    model="qwen-plus",
    messages=messages,
    result_format="message",
)

if response.status_code == 200:
    print(response.output.choices[0].message.content)
    # 如需查看完整响应，请取消下列注释
    # print(json.dumps(response, default=lambda o: o.__dict__, indent=4))
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### Java

```
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.Protocol;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1");
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // qwen3.7-max、qwen3.7-max-2026-05-20和qwen3.6-max-preview仅支持文本接口，qwen3.8-max、qwen3.7-max-2026-06-08支持多模态接口，Qwen3.6、Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
            // 如需查看完整响应，请取消下列注释
            // System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
    }
}
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### Node.js（HTTP）

```
// 需要 Node.js v18+
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：const apiKey = "sk-xxx";
const apiKey = process.env.DASHSCOPE_API_KEY;

const data = {
    // qwen3.7-max、qwen3.7-max-2026-05-20和qwen3.6-max-preview仅支持文本接口，qwen3.8-max、qwen3.7-max-2026-06-08支持多模态接口，Qwen3.6、Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
    model: "qwen-plus",
    input: {
        messages: [
            {
                role: "system",
                content: "You are a helpful assistant."
            },
            {
                role: "user",
                content: "你是谁？"
            }
        ]
    },
    parameters: {
        result_format: "message"
    }
};

async function callApi() {
    try {
        // 各地域配置不同，请根据实际地域修改
        const response = await fetch('https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log(result.output.choices[0].message.content);
        // 如需查看完整响应，请取消下列注释
        // console.log(JSON.stringify(result));
    } catch (error) {
        // 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
        console.error('调用失败:', error.message);
    }
}

callApi();
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### Go（HTTP）

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	requestBody := map[string]interface{}{
		// qwen3.7-max、qwen3.7-max-2026-05-20和qwen3.6-max-preview仅支持文本接口，qwen3.8-max、qwen3.7-max-2026-06-08支持多模态接口，Qwen3.6、Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
		"model": "qwen-plus",
		"input": map[string]interface{}{
			"messages": []map[string]string{
				{
					"role":    "system",
					"content": "You are a helpful assistant.",
				},
				{
					"role":    "user",
					"content": "你是谁？",
				},
			},
		},
		"parameters": map[string]string{
			"result_format": "message",
		},
	}

	// 序列化为 JSON
	jsonData, _ := json.Marshal(requestBody)

	// 创建 HTTP 客户端和请求
	client := &http.Client{}
	// 各地域配置不同，请根据实际地域修改
	req, _ := http.NewRequest("POST", "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation", bytes.NewBuffer(jsonData))

	// 设置请求头
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// 读取响应体
	bodyText, _ := io.ReadAll(resp.Body)

	// 解析JSON并输出content内容
	var result map[string]interface{}
	json.Unmarshal(bodyText, &result)
	content := result["output"].(map[string]interface{})["choices"].([]interface{})[0].(map[string]interface{})["message"].(map[string]interface{})["content"].(string)
	fmt.Println(content)

	// 如需查看完整响应，请取消下列注释
	// fmt.Printf("%s\n", bodyText)
}
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
        // 设置请求 URL 和内容
        // 各地域配置不同，请根据实际地域修改
        string url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
        // qwen3.7-max、qwen3.7-max-2026-05-20和qwen3.6-max-preview仅支持文本接口，qwen3.8-max、qwen3.7-max-2026-06-08支持多模态接口，Qwen3.6、Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""input"": {
                ""messages"": [
                    {
                        ""role"": ""system"",
                        ""content"": ""You are a helpful assistant.""
                    },
                    {
                        ""role"": ""user"",
                        ""content"": ""你是谁？""
                    }
                ]
            },
            ""parameters"": {
                ""result_format"": ""message""
            }
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);
        var jsonResult = System.Text.Json.JsonDocument.Parse(result);
        var content = jsonResult.RootElement.GetProperty("output").GetProperty("choices")[0].GetProperty("message").GetProperty("content").GetString();
        Console.WriteLine(content);
        // 如需查看完整响应，请取消下列注释
        // Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```

#### 返回结果

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 92,
        "output_tokens": 66,
        "input_tokens": 26
    },
    "request_id": "09dceb20-ae2e-999b-85f9-xxxxxx"
}
```

#### PHP（HTTP）

```
<?php
// 各地域配置不同，请根据实际地域修改
$url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');

$data = [
    // qwen3.7-max、qwen3.7-max-2026-05-20和qwen3.6-max-preview仅支持文本接口，qwen3.8-max、qwen3.7-max-2026-06-08支持多模态接口，Qwen3.6、Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
    "model" => "qwen-plus",
    "input" => [
        "messages" => [
            [
                "role" => "system",
                "content" => "You are a helpful assistant."
            ],
            [
                "role" => "user",
                "content" => "你是谁？"
            ]
        ]
    ],
    "parameters" => [
        "result_format" => "message"
    ]
];

$jsonData = json_encode($data);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $apiKey",
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 200) {
    $jsonResult = json_decode($response, true);
    $content = $jsonResult['output']['choices'][0]['message']['content'];
    echo $content;
    // 如需查看完整响应，请取消下列注释
    // echo "模型响应: " . $response;
} else {
    echo "请求错误: " . $httpCode . " - " . $response;
}

curl_close($ch);
?>
```

#### 返回结果

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

#### curl

各地域的base\_url和API Key不同，详情请参见[DashScope](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)和 [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

```
# 各地域配置不同，请根据实际地域修改
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
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
        "result_format": "message"
    }
}'
```

#### 返回结果

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 92,
        "output_tokens": 66,
        "input_tokens": 26
    },
    "request_id": "09dceb20-ae2e-999b-85f9-xxxxxx"
}
```

#### dashscope CLI

通过 dashscope 命令行调用。

```
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope generation create -m qwen-plus -p "你好"
```

**重要**SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见

[DashScope SDK Expert](raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

## 图像、视频数据处理

多模态模型支持处理图像、视频等非文本数据，可用于视觉问答、事件检测等任务。其调用方式与纯文本模型主要有以下不同：

-   **用户消息（user message）的构造方式**：多模态模型的用户消息不仅包含文本，还包含图片、音频等多模态信息。
-   **DashScope SDK接口：**使用 DashScope Python SDK时，需调用 `MultiModalConversation` 接口；使用DashScope Java SDK时，需调用 `MultiModalConversation` 类。

> 图片、视频文件限制请参见 [图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md) 。

#### OpenAI兼容-Chat Completions API

#### Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
messages = [
    {
        "role": "user",
        "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
                    },
                },
            {"type": "text", "text": "请问图片展现了有哪些商品？"},
        ],
    }
]
completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=messages,
)
print(completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

let messages = [
    {
        role: "user",
        content: [
            { type: "image_url", image_url: { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png" } },
            { type: "text", text: "请问图片展现了有哪些商品？" },
        ]
    }]
async function main() {
    let response = await openai.chat.completions.create({
        model: "qwen3.6-plus",
        messages: messages
    });
    console.log(response.choices[0].message.content);
}

main()
```

#### curl

各地域的base\_url和API Key不同，详情请参见[OpenAI兼容-Chat](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)和 [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

```
# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.6-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
          }
        },
        {
          "type": "text",
          "text": "请问图片展现了有哪些商品？"
        }
      ]
    }
  ]
}'
```

#### DashScope

#### Python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
            },
            {"text": "请问图片展现了有哪些商品？"},
        ],
    }
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.6-plus',   # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages)
print(response.output.choices[0].message.content[0]['text'])
```

#### Java

```
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
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
    // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final String modelName = "qwen3.6-plus";  // 可按需更换为其它多模态模型，并修改相应的 messages

    public static void MultiRoundConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"),
                        Collections.singletonMap("text", "请问图片展现了有哪些商品？"))).build();
        List<MultiModalMessage> messages = new ArrayList<>();
        messages.add(userMessage);
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(modelName)
                .messages(messages)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));        // add the result to conversation
    }

    public static void main(String[] args) {
        try {
            MultiRoundConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

各地域的base\_url和API Key不同，详情请参见[DashScope](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)和 [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

```
# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.6-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"},
                    {"text": "请问图片展现了有哪些商品？"}
                ]
            }
        ]
    }
}'
```

## 异步调用模型

调用异步接口，可有效提升高并发请求的处理效率。

#### OpenAI兼容-Chat Completions API

Python

```
import os
import asyncio
from openai import AsyncOpenAI
import platform

# 创建异步客户端实例
client = AsyncOpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 定义异步任务列表
async def task(question):
    print(f"发送问题: {question}")
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant." },
            {"role": "user", "content": question}
        ],
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    print(f"模型回复: {response.choices[0].message.content}")

# 主异步函数
async def main():
    questions = ["你是谁？", "你会什么？", "天气怎么样？"]
    tasks = [task(q) for q in questions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 设置事件循环策略
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main(), debug=False)
```

Java

```
import com.openai.client.OpenAIClientAsync;
import com.openai.client.okhttp.OpenAIOkHttpClientAsync;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class Main {
    public static void main(String[] args) {
        // 创建 OpenAI 客户端，连接 DashScope 的兼容接口
        OpenAIClientAsync client = OpenAIOkHttpClientAsync.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
                .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
                .build();

        // 定义问题列表
        List<String> questions = Arrays.asList("你是谁？", "你会什么？", "天气怎么样？");

        // 创建异步任务列表
        CompletableFuture<?>[] futures = questions.stream()
                .map(question -> CompletableFuture.supplyAsync(() -> {
                    System.out.println("发送问题: " + question);
                    // 创建 ChatCompletion 参数
                    ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                            .model("qwen-plus")  // 指定模型
                            .addSystemMessage("You are a helpful assistant.")
                            .addUserMessage(question)
                            .build();

                    // 发送异步请求并处理响应
                    return client.chat().completions().create(params)
                        .thenAccept(chatCompletion -> {
                            String content = chatCompletion.choices().get(0).message().content().orElse("无响应内容");
                            System.out.println("模型回复: " + content);
                        })
                        .exceptionally(e -> {
                            System.err.println("错误信息：" + e.getMessage());
                            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
                            return null;
                        });
                }).thenCompose(future -> future))
                .toArray(CompletableFuture[]::new);

        // 等待所有异步操作完成
        CompletableFuture.allOf(futures).join();
    }
}
```

#### DashScope

DashScope SDK的文本生成异步调用，目前仅支持Python。

```
# DashScope Python SDK版本需要不低于 1.19.0
import asyncio
import platform
from dashscope.aigc.generation import AioGeneration
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 定义异步任务列表
async def task(question):
    print(f"发送问题: {question}")
    response = await AioGeneration.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": question}],
        result_format="message",
    )
    print(f"模型回复: {response.output.choices[0].message.content}")

# 主异步函数
async def main():
    questions = ["你是谁？", "你会什么？", "天气怎么样？"]
    tasks = [task(q) for q in questions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 设置事件循环策略
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main(), debug=False)
```

**返回结果**

> 由于调用是异步的，响应的返回顺序可能与示例不同。

```
发送问题: 你是谁？
发送问题: 你会什么？
发送问题: 天气怎么样？
模型回复: 你好！我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
模型回复: 您好！我目前无法实时获取天气信息。您可以告诉我您所在的城市或地区，我会尽力为您提供一些通用的天气建议或信息。或者您也可以使用天气应用查看实时天气情况。
模型回复: 我会很多技能，比如：

1. **回答问题**：无论是学术问题、生活常识还是专业知识，我都可以尝试帮你解答。
2. **创作文字**：我可以写故事、公文、邮件、剧本等各类文本。
3. **逻辑推理**：我可以帮助你解决一些逻辑推理问题，比如数学题、谜语等。
4. **编程**：我可以提供编程帮助，包括代码编写、调试和优化。
5. **多语言支持**：我支持多种语言，包括但不限于中文、英文、法语、西班牙语等。
6. **观点表达**：我可以为你提供一些观点和建议，帮助你做出决策。
7. **玩游戏**：我们可以一起玩文字游戏，比如猜谜语、成语接龙等。

如果你有任何具体的需求或问题，欢迎告诉我，我会尽力帮助你！
```

## 应用于生产环境

### 构建高质量的上下文

向大模型直接输入大量原始数据，会因上下文容量的限制导致成本增加与效果下降。上下文工程（Context Engineering）通过动态加载精准知识，显著提升生成质量与效率。核心技术包括：

-   **提示词工程（Prompt Engineering）**：通过设计和优化文本指令（Prompt），可以更精确地引导模型，使其输出更符合预期的结果。若想了解更多，可参考[文生文Prompt指南](raw/model-user-guide/use-cases/prompt-engineering-guide.md)、阿里云百炼 [提示词模板](https://bailian.console.aliyun.com/flow-agent/plugin-market/prompt)页面。
-   [检索增强生成（RAG）](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)：适用于需要模型依据外部知识库（例如产品文档或技术手册）来回答问题的场景。
-   [工具调用（Tool）](https://help.aliyun.com/zh/model-studio/tool-calls)：允许模型获取实时信息（如查询天气、路况）或完成特定操作（如调用API、发送邮件）。
-   **记忆机制（Memory）**：为模型建立长短期记忆，使其能够理解连续对话的历史信息。

若想系统了解，可参考[阿里云大模型高级工程师ACP认证课程](https://atomgit.com/alibabaclouddocs/aliyun_acp_learning/blob/main/%E5%A4%A7%E6%A8%A1%E5%9E%8BACP%E8%AE%A4%E8%AF%81%E6%95%99%E7%A8%8B/p2_%E6%9E%84%E9%80%A0%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%97%AE%E7%AD%94%E7%B3%BB%E7%BB%9F/2_1_%E7%94%A8%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9E%84%E5%BB%BA%E6%96%B0%E4%BA%BA%E7%AD%94%E7%96%91%E6%9C%BA%E5%99%A8%E4%BA%BA.ipynb)。

### 控制回复多样性

`temperature`和 `top_p`用于控制生成文本的多样性。数值越高，内容越多样，数值越低，内容越确定。为准确评估参数效果，建议每次只调整一个。

-   **temperature**：范围 \[0, 2)。侧重调整随机性。
-   **top\_p**：范围 (0, 1\]。通过概率阈值筛选回复。

以下示例将展示不同参数设置对生成内容的影响。输入提示词为：“写一个三句话的短故事，主角是一只猫和一束阳光。”

-   **高多样性**（示例`temperature`\=0.9）：适用于需要创意、想象力和新颖表达的场景，如创意写作、头脑风暴或市场营销文案。

```
阳光斜斜地切进窗台，橘猫蹑手蹑脚走近那块发光的方砖，绒毛瞬间被染成熔化的蜜糖。
它伸出前爪轻拍光斑，却像踩进温热的池水般陷了进去，整片阳光顺着肉垫汩汩漫上脊背。
午后忽然变得很重——猫儿蜷在流动的金砂里，听见时光在呼噜声中轻轻融化。
```

-   **高确定性**（示例`temperature`\=0.1）：适用于要求内容准确、严谨和可预测的场景，如事实问答、代码生成或法律文本。

```
午后，一只老猫蜷在窗台，数着光斑打盹。
阳光轻轻跃过它斑驳的脊背，像在翻阅一本旧相册。
尘埃浮起又落下，仿佛时光低语：你曾年轻，我也炽热。
```

原理介绍

**temperature**：

-   temperature 越高，Token 概率分布变得更平坦（即高概率 Token 的概率降低，低概率 Token 的概率上升），使得模型在选择下一个 Token 时更加随机。
-   temperature 越低，Token 概率分布变得更陡峭（即高概率 Token 被选取的概率更高，低概率 Token 的概率更低），使得模型更倾向于选择高概率的少数 Token。

**top\_p**：

top\_p 采样是指从最高概率（最核心）的 Token 集合中进行采样。它将所有可能的下一个 Token 按概率从高到低排序，然后从概率最高的 Token 开始累加概率，直至概率总和达到阈值（例如80%，即 top\_p=0.8），最后从这些概率最高、概率总和达到阈值的 Token 中随机选择一个用于输出。

-   top\_p 越高，考虑的 Token 越多，因此生成的文本更多样。
-   top\_p 越低，考虑的 Token 越少，因此生成的文本更集中和确定。

不同场景的参数配置示例

```
# 不同场景的推荐参数配置
SCENARIO_CONFIGS = {
    # 创造性写作
    "creative_writing": {
        "temperature": 0.9,
        "top_p": 0.95
    },
    # 代码生成
    "code_generation": {
        "temperature": 0.2,
        "top_p": 0.8
    },
    # 事实性问答
    "factual_qa": {
        "temperature": 0.1,
        "top_p": 0.7
    },
    # 翻译
    "translation": {
        "temperature": 0.3,
        "top_p": 0.8
    }
}

# OpenAI使用示例
# completion = client.chat.completions.create(
#     model="qwen-plus",
#     messages=[{"role": "user", "content": "写一首关于月亮的诗"}],
#     **SCENARIO_CONFIGS["creative_writing"]
# )
# DashScope使用示例
# response = Generation.call(
#     # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     model="qwen-plus",
#     messages=[{"role": "user", "content": "写一个判断输入n是否是质数的python函数，不要输出非代码内容"}],
#     result_format="message",
#     **SCENARIO_CONFIGS["code_generation"]
# )
```

### 更多功能

上文介绍了基础的交互方式。针对更复杂的场景，可参考：

-   [多轮对话](raw/model-user-guide/model-experience/text-generation-model/multi-round-conversation.md)：适用于追问、信息采集等需要连续交流的场景。
-   [流式输出](raw/model-user-guide/model-experience/text-generation-model/stream.md)：适用于聊天机器人、实时代码生成等需要即时响应的场景，可以提升用户体验，并避免因响应时间过长导致的超时。
-   [深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)：适用于复杂推理、策略分析等需要更高质量、更具条理的深度回答的场景。
-   [结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)：当需要模型按稳定的JSON格式回复，以便于程序调用或数据解析时使用。
-   [前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)：适用于代码补全、长文写作等需要模型接续已有文本的场景。

## API 参考

模型调用的完整参数列表，请参考 [OpenAI 兼容API参考](raw/model-api-reference/qwen-api-reference.md)和[DashScope API参考](raw/model-api-reference/qwen-api-reference.md)。

## 常见问题

### Q：为什么输入Token数比我发送的文本Token数多？

A：在处理对话时，系统会使用对话模板（Chat Template）对输入的原始文本进行包装，添加角色标识、消息边界等控制标记。这些由系统添加的标记同样会计入Token。

例如，向qwen3.8-max发送消息`{"role": "user", "content": "你好"}`，“你好” 在分词（Tokenize）后仅对应 1 个 Token，但系统处理时，实际输入完整文本为`<|im_start|>user\n你好<|im_end|>\n<|im_start|>assistant\n<think>`，分词后总Token数会增加到11个。

### Q：千问API为何无法分析网页链接？

A：千问API本身不具备直接访问网页链接的能力。您可以通过[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)、[MCP](raw/model-user-guide/model-experience/text-generation-model/tool-calls/mcp.md)等功能，或结合 Python 的 Beautiful Soup 等网页抓取工具提取网页内容后传入模型。

### Q：[网页端千问](https://tongyi.aliyun.com/qianwen/)和千问API的回复为什么不一致？

A：网页端千问在千问API的基础上做了额外的工程优化，因此可以达到解析网页、联网搜索、画图、制作 PPT等功能，这些本身并不属于大模型API的能力，可以通过[联网搜索](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md)、[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)、[MCP](raw/model-user-guide/model-experience/text-generation-model/tool-calls/mcp.md)等功能优化模型的效果。

### Q：如何处理模型超时的情况？

A：使用[流式输出](raw/model-user-guide/model-experience/text-generation-model/stream.md)可避免超时。流式输出在生成过程中逐步返回 token，无需等待完整响应。

非流式调用的最大超时时间不少于300秒，实际时长因部署区域与选用模型存在差异。若超时未完成，服务将中断请求，但返回已生成的内容，且不再报超时错误。此时响应头将包含`x-dashscope-partialresponse: true`，表示返回的是超时前的部分结果。

> 若无法获取响应头参数（例如通过SDK调用），可通过 `finish_reason` 字段辅助判断，若为 `null` ，表示生成内容不完整（但不一定是触发了超时）。

大模型可续写不完整的内容，详情请参见：[基于不完整输出进行续写](https://help.aliyun.com/zh/model-studio/partial-mode#8cc28acfd7a91)。

> Java SDK暂不支持前缀续写功能。

### Q：模型能直接生成 Word、Excel、PDF 或 PPT 格式的文件吗？

A：不能。阿里云百炼的文本生成模型仅输出纯文本内容。您需要通过代码或使用第三方库将文本转换为所需格式，或通过阿里云百炼[PPT自动生成应用](https://bailian.console.aliyun.com/flow-agent/app-market/app-template-experience/assistant/AutoPptGenerator)、[网页端千问](https://www.qianwen.com/aippt)等方式进行生成。

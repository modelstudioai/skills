# 调用工作流应用

本文档主要介绍如何通过 DashScope SDK 或 HTTP API，快速、高效地将阿里云百炼**工作流应用**集成到业务系统中。

> 如需使用 Responses API 调用，请参阅 [Responses API](https://help.aliyun.com/zh/model-studio/openai-responses-api/)。

**重要**

本文档仅适用于中国大陆版（北京地域）。

## **前提条件**

开始前，请确保您已完成以下操作：

1.  已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
2.  已创建[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，并在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面的应用卡片上获取 APP\_ID。
    
3.  若通过DashScope SDK调用，需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#f3e80b21069aa)。
    

## **快速开始**

### Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application
response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',# 替换为实际的应用 ID
    prompt='你是谁？')

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print(response.output.text)
```

**响应示例**

```
我是阿里云开发的一款超大规模语言模型，我叫千问。我被设计用来帮助用户生成各种类型的文本，如文章、故事、诗歌、故事等，并能根据不同的场景和需求进行调整和优化。此外，我还能够回答各种问题，提供信息和解释，辅助学习和研究。如果您有任何需要，欢迎随时向我提问！
```

### Java

**请求示例**

```
// 建议dashscope SDK的版本 >= 2.12.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void appCall()
            throws ApiException, NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("APP_ID")
                .prompt("你是谁？")
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf("text: %s\n",
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("message："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
text: 我是阿里云开发的一款超大规模语言模型，我叫千问。
```

### HTTP

#### curl

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "你是谁？"
    },
    "parameters":  {},
    "debug": {}
}'
```

> APP\_ID替换为实际的应用 ID。

**响应示例**

```
{"output":{"finish_reason":"stop",
"session_id":"232ea2e9e6ef448db6b14465c06a9a56",
"text":"我是来自阿里云的超大规模语言模型，我叫千问。我是一个能够回答问题、创作文字，还能表达观点、撰写代码的AI助手。如果您有任何问题或需要帮助，请随时告诉我，我会尽力为您提供帮助。"},
"usage":{"models":[{"output_tokens":51,"model_id":"qwen-max","input_tokens":121}]},
"request_id":"661c9cad-e59c-9f78-a262-78eff243f151"}%
```

#### PHP

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '你是谁？'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo "{$response_data['output']['text']}\n";
    } else {
        echo "No text in response.\n";
    }}
else {
    if (isset($response_data['request_id'])) {
        echo "request_id={$response_data['request_id']}\n";}
    echo "code={$status_code}\n";
    if (isset($response_data['message'])) {
        echo "message={$response_data['message']}\n";} 
    else {
        echo "message=Unknown error\n";}
}
?>
```

**响应示例**

```
我是来自阿里云的超大规模语言模型，我叫千问。
```

#### Node.js

**需安装相关依赖：**

```
npm install axios
```

**请求示例**

```
const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "你是谁？"
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
我是来自阿里云的大规模语言模型，我叫千问。
```

#### C#

**请求示例**

```
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。 
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
        string appId = "APP_ID"; // 替换为实际的应用ID

        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");

            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""你是谁？""
                },
                ""parameters"": {},
                ""debug"": {}
            }";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Request successful:");
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "c274e14a58d9492f9baeffdc003a97c5",
        "text": "我是阿里云开发的一款超大规模语言模型，我叫千问。我被设计用来帮助用户生成各种类型的文本，如文章、故事、诗歌、故事等，并能根据不同的场景和需求进行变换和创新。此外，我还能够回答各种问题，提供信息和解释，帮助用户解决问题和获取知识。如果你有任何问题或需要帮助，请随时告诉我！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 79,
                "model_id": "qwen-plus",
                "input_tokens": 74
            }
        ]
    },
    "request_id": "5c4b86b1-cd2d-9847-8d00-3fba8f187bc6"
}
```

#### Go

**请求示例**

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]string{
			"prompt": "你是谁？",
		},
		"parameters": map[string]interface{}{},
		"debug":      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Failed to marshal JSON: %v\n", err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Failed to create request: %v\n", err)
		return
	}

	// 设置请求头
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read response: %v\n", err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println("Request successful:")
		fmt.Println(string(body))
	} else {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		fmt.Println(string(body))
	}
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "6105c965c31b40958a43dc93c28c7a59",
        "text": "我是千问，由阿里云开发的AI助手。我被设计用来回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 36,
                "model_id": "qwen-plus",
                "input_tokens": 74
            }
        ]
    },
    "request_id": "f97ee37d-0f9c-9b93-b6bf-bd263a232bf9"
}
```

## **多轮对话**

相比于单轮对话，多轮对话可以让大模型参考历史对话信息，更符合日常交流的场景。

**使用** `**session_id**`

系统会自动从云端加载存储的对话历史，并结合`prompt`指令生成上下文。实现简单，无需维护。

> `session_id` 有效期为 1 小时，最多支持 50 轮对话。

**自行管理** `**messages**`**（推荐）**

自行维护一个 `messages` 数组，手动记录和传递每一轮的对话历史及新指令。无需传递`prompt`。控制上下文，更灵活。

> **注意**：若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。

在**大模型节点**配置提示词变量`historyList`并**发布**应用后，发起 API 调用。

#### **云端存储**

## Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application
def call_with_session():
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='APP_ID',  # 替换为实际的应用 ID
        prompt='你是谁？')

    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        return response

    responseNext = Application.call(
                # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                app_id='APP_ID',  # 替换为实际的应用 ID
                prompt='你有什么技能?',
                session_id=response.output.session_id)  # 上一轮response的session_id

    if responseNext.status_code != HTTPStatus.OK:
        print(f'request_id={responseNext.request_id}')
        print(f'code={responseNext.status_code}')
        print(f'message={responseNext.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n session_id=%s\n' % (responseNext.output.text, responseNext.output.session_id))
        # print('%s\n' % (response.usage))

if __name__ == '__main__':
    call_with_session()
```

**响应示例**

```
我具备多种技能，可以协助你完成各种任务。以下是一些主要的技能：

1. **信息查询**：提供天气、新闻、历史事实、科学知识等各种信息。
2. **语言处理**：翻译文本、纠正语法错误、生成文章和故事。
3. **技术问题解答**：解答编程、软件使用、技术故障排除等问题。
4. **学习辅导**：帮助解答数学、物理、化学等学科的问题。
5. **生活建议**：提供健康、饮食、旅行、购物等方面的建议。
6. **娱乐互动**：讲笑话、玩文字游戏、进行简单的聊天互动。
7. **日程管理**：提醒重要日期、安排日程、设置提醒。
8. **数据分析**：解释数据图表、提供数据分析建议。
9. **情感支持**：倾听你的感受、提供安慰和支持。

如果你有具体的需求或问题，可以直接告诉我，我会尽力帮助你！
 session_id=98ceb3ca0c4e4b05a20a00f913050b42
```

## Java

**请求示例**

```
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Arrays;
import java.util.List;
public class Main {
    public static void callWithSession()
            throws ApiException, NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 替换为实际的应用 ID
                .appId("APP_ID")
                .prompt("你是谁？")
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        param.setSessionId(result.getOutput().getSessionId());
        param.setPrompt("你有什么技能?");
        result = application.call(param);

        System.out.printf("%s\n session_id: %s\n",
                result.getOutput().getText(), result.getOutput().getSessionId());
    }

    public static void main(String[] args) {
        try {
            callWithSession();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf("Exception: %s", e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
我具备多项技能，可以为您提供多种帮助。以下是一些主要的技能：

1. **多语言理解与生成**：我能理解和生成包括中文、英文在内的多种语言文本。
2. **信息检索与综合**：我可以根据您的问题查找相关信息并进行整理和总结。
3. **写作辅助**：无论是撰写文章、报告还是创意写作，我都能提供支持。
4. **编程助手**：对于程序员来说，我可以帮助解答编程相关的问题，提供代码示例等。
5. **教育辅导**：在学习过程中遇到困难时，我可以作为助手提供帮助，涵盖从数学到历史等多个学科领域。
6. **生活建议**：关于健康饮食、旅行规划等方面的问题我也能给出一些建议。
7. **情感交流**：虽然我是AI，但我努力以一种温暖和支持的方式与您交流。

如果您有任何具体需求或想要进一步了解某个方面的内容，请随时告诉我！
 session_id: f2e94a980a34424fa25be45a7048d77c
```

## HTTP

## curl

**请求示例（上一轮对话）**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "你是谁？"
    },
    "parameters":  {},
    "debug": {}
}'
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "4f8ef7233dc641aba496cb201fa59f8c",
        "text": "我是通义千问，由阿里云开发的AI助手。我被设计用来回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 36,
                "model_id": "qwen-plus",
                "input_tokens": 75
            }
        ]
    },
    "request_id": "e571b14a-423f-9278-8d1e-d86c418801e0"
}
```

**请求示例（下一轮对话）**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "你有什么技能？",
        "session_id":"4f8ef7233dc641aba496cb201fa59f8c"
    },
    "parameters":  {},
    "debug": {}
}'
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "4f8ef7233dc641aba496cb201fa59f8c",
        "text": "作为AI助手，我具备多种技能，可以帮助你完成各种任务，包括但不限于：

1. **知识查询**：我可以帮助你查找各种领域的信息，比如科学、历史、文化、技术等。
2. **语言翻译**：我可以帮你翻译不同语言的文字，支持多种语言之间的互译。
3. **文本生成**：我可以生成文章、故事、诗歌、新闻稿等各种类型的文本。
4. **问题解答**：无论是学术问题、生活常识还是技术难题，我都可以尝试为你提供答案。
5. **对话交流**：我可以与你进行自然流畅的对话，提供情感支持或娱乐。
6. **代码编写与调试**：我可以帮助你编写代码、解决编程中的问题。
7. **数据分析**：我可以帮助你分析数据，提供统计结果和可视化建议。
8. **创意启发**：如果你需要创意灵感，比如设计、广告词、营销策略等，我也可以提供帮助。

如果你有任何具体的需求或问题，欢迎随时告诉我！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 208,
                "model_id": "qwen-plus",
                "input_tokens": 125
            }
        ]
    },
    "request_id": "9de2c3ed-e1f0-9963-85f4-8f289203418b"
}
```

## PHP

**请求示例（上一轮对话）**

```
<?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '你是谁？'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo "{$response_data['output']['text']}\n";
    } else {
        echo "No text in response.\n";
    };
    if (isset($response_data['output']['session_id'])) {
        echo "session_id={$response_data['output']['session_id']}\n";
    }
}else {
    if (isset($response_data['request_id'])) {
        echo "request_id={$response_data['request_id']}\n";}
    echo "code={$status_code}\n";
    if (isset($response_data['message'])) {
        echo "message={$response_data['message']}\n";} 
    else {
        echo "message=Unknown error\n";}
}
?>
```

**响应示例**

```
我是来自阿里云的超大规模语言模型，我叫通义千问。
session_id=2e658bcb514f4d30ab7500b4766a8d43
```

**请求示例（下一轮对话）**

```
<?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '你有什么技能？',
        // 替换为实际上一轮对话返回的session_id
        'session_id' => '2e658bcb514f4d30ab7500b4766a8d43'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo "{$response_data['output']['text']}\n";
    } else {
        echo "No text in response.\n";
    };
    if (isset($response_data['output']['session_id'])) {
        echo "session_id={$response_data['output']['session_id']}\n";
    }
}else {
    if (isset($response_data['request_id'])) {
        echo "request_id={$response_data['request_id']}\n";}
    echo "code={$status_code}\n";
    if (isset($response_data['message'])) {
        echo "message={$response_data['message']}\n";} 
    else {
        echo "message=Unknown error\n";}
}
?>
```

**响应示例**

```
我具备多项技能，包括但不限于：

1. **多语言能力**：我可以理解和生成多种语言的文字内容。
2. **写作与创作**：帮助撰写文章、故事、诗歌等创意内容。
3. **知识问答**：回答来自各个领域的常识性和专业性问题。
4. **代码编写与理解**：能够编写简单的程序代码，并帮助解释或调试代码。
5. **逻辑推理**：解决需要逻辑思考的问题和谜题。
6. **情感支持**：提供正面的心理支持和鼓励。
7. **游戏娱乐**：参与文字游戏或其他形式的互动娱乐活动。

我的目标是成为您的得力助手，在您需要的时候提供帮助和支持。如果您有任何具体需求或想要尝试的功能，请随时告诉我！
session_id=2e658bcb514f4d30ab7500b4766a8d43
```

## Node.js

**需安装相关依赖：**

```
npm install axios
```

**请求示例（上一轮对话）**

```
const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "你是谁？"
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
            console.log(`session_id=${response.data.output.session_id}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response statusText: ${error.response.statusText}`);
        }
    }
}
callDashScope();
```

**响应示例**

```
我是通义千问，由阿里云开发的人工智能助手。我可以回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？
session_id=fe4ce8b093bf46159ea9927a7b22f0d3
```

**请求示例（下一轮对话）**

```
const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    // session_id替换为实际上一轮对话的session_id
    const data = {
        input: {
            prompt: "你有什么技能？",
            session_id: 'fe4ce8b093bf46159ea9927a7b22f0d3',
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
            console.log(`session_id=${response.data.output.session_id}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response statusText: ${error.response.statusText}`);
        }
    }
}
callDashScope();
```

**响应示例**

```
我具备多种技能，可以帮助你处理不同的任务和问题。以下是一些主要的技能领域：

1. **信息查询与检索**：我可以帮助查找特定的信息、数据或新闻。
2. **写作与创作**：包括撰写文章、故事、诗歌、报告等。
3. **语言翻译**：能够提供不同语言之间的翻译服务。
4. **教育辅导**：解答学术问题，帮助理解复杂的概念。
5. **技术支持**：解决计算机使用中遇到的技术难题。
6. **生活建议**：提供建议关于健康、饮食、旅行等方面。
7. **娱乐互动**：讲笑话、玩文字游戏等轻松活动。

如果你有具体的需求或想了解更详细的某一方面，请告诉我！
session_id=fe4ce8b093bf46159ea9927a7b22f0d3
```

## C#

**请求示例（上一轮对话）**

```
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。 
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
        string appId = "APP_ID"; // 替换为实际的应用ID

        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");

            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""你是谁？""
                },
                ""parameters"": {},
                ""debug"": {}
            }";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Request successful:");
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "7b830e4cc8fe44faad0e648f9b71435f",
        "text": "我是通义千问，由阿里云开发的AI助手。我被设计用来回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 36,
                "model_id": "qwen-plus",
                "input_tokens": 75
            }
        ]
    },
    "request_id": "53691ae5-be17-96c6-a830-8f0f92329028"
}
```

**请求示例（下一轮对话）**

```
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。 
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
        string appId = "APP_ID"; // 替换为实际的应用ID

        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");

            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""你有什么技能？"",
                    ""session_id"": ""7b830e4cc8fe44faad0e648f9b71435f""
                },
                ""parameters"": {},
                ""debug"": {}
            }";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Request successful:");
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "7b830e4cc8fe44faad0e648f9b71435f",
        "text": "我具备多种技能，可以：

- 回答广泛领域的知识性问题
- 提供学习资源和建议
- 协助解决技术问题
- 进行多语言交流
- 帮助规划行程和活动
- 提供日常生活中的实用建议

如果你有任何具体需求或问题，欢迎随时告诉我！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 70,
                "model_id": "qwen-plus",
                "input_tokens": 123
            }
        ]
    },
    "request_id": "da5044ed-461e-9e91-8ca5-38a3c72a8306"
}
```

## Go

**请求示例（上一轮对话）**

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]string{
			"prompt": "你是谁？",
		},
		"parameters": map[string]interface{}{},
		"debug":      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Failed to marshal JSON: %v\n", err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Failed to create request: %v\n", err)
		return
	}

	// 设置请求头
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read response: %v\n", err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println("Request successful:")
		fmt.Println(string(body))
	} else {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		fmt.Println(string(body))
	}
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "f7eea37f0c734c20998a021b688d6de2",
        "text": "我是通义千问，由阿里云开发的AI助手。我被设计用来回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 36,
                "model_id": "qwen-plus",
                "input_tokens": 75
            }
        ]
    },
    "request_id": "fa65e14a-ab63-95b2-aa43-035bf5c51835"
}
```

**请求示例（下一轮对话）**

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]string{
			"prompt":     "你有什么技能？",
			"session_id": "f7eea37f0c734c20998a021b688d6de2", // 替换为实际上一轮对话的session_id
		},
		"parameters": map[string]interface{}{},
		"debug":      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Failed to marshal JSON: %v\n", err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Failed to create request: %v\n", err)
		return
	}

	// 设置请求头
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read response: %v\n", err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println("Request successful:")
		fmt.Println(string(body))
	} else {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		fmt.Println(string(body))
	}
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "f7eea37f0c734c20998a021b688d6de2",
        "text": "我具备多种技能，可以：

- 回答各种知识性问题，如科学、历史、文化等领域的疑问。
- 提供实用建议，比如旅行攻略、健康小贴士、学习方法等。
- 协助处理文字工作，例如撰写文章、编辑文档、创作故事或诗歌。
- 进行多语言翻译，支持多种语言之间的互译。
- 与用户进行自然流畅的对话，陪伴聊天、解答疑惑。

如果你有任何具体需求，欢迎告诉我！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 104,
                "model_id": "qwen-plus",
                "input_tokens": 125
            }
        ]
    },
    "request_id": "badccade-9f54-986b-8d8c-75ef15e9616c"
}
```

> APP\_ID替换为实际的应用 ID。下一轮对话的输入参数`session_id`字段值替换为实际上一轮对话返回的session\_id值。

#### **自行管理**

##### **Python**

**请求示例**

```
# dashscope SDK的版本需 >= 1.20.14
import os
from http import HTTPStatus
from dashscope import Application

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': '你是谁？'},
    {"role": "assistant","content": "我是阿里云开发的大规模语言模型，我叫通义千问。"},
    {"role": "user","content": "你能做什么？"}
]
response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',  # 替换为实际的应用 ID
    messages=messages)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print('%s\n' % (response.output.text))
```

**响应示例**

```
作为通义千问，我可以帮助你完成多种任务，包括但不限于：

1. 回答问题：无论是科学知识、技术难题还是生活常识，我都可以提供准确的信息和解答。
2. 创作文字：如撰写故事、写诗、编写文章等，根据给定的条件生成创意内容。
3. 编程助手：可以辅助编程学习，解释代码逻辑，帮助调试程序错误等。
4. 语言翻译：支持多种语言之间的互译服务。
5. 提供建议：在面对决策时为你提供建议或解决方案。
6. 情感交流：与用户进行对话，倾听并给予积极正面的回应和支持。

总之，我的目标是成为你工作和生活中的得力助手。如果你有任何具体的需求，请随时告诉我！
```

##### **Java**

**请求示例**

```
// dashscope SDK的版本需 >= 2.17.0
import java.util.ArrayList;
import java.util.List;

import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void appCall()
            throws ApiException, NoApiKeyException, InputRequiredException {
        List<Message> messages = new ArrayList<>();
        messages.add(Message.builder().role("system").content("You are a helpful assistant.").build());
        messages.add(Message.builder().role("user").content("你是谁？").build());
        messages.add(Message.builder().role("assistant").content("我是阿里云开发的大规模语言模型，我叫通义千问。").build());
        messages.add(Message.builder().role("user").content("你能做什么？").build());

        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("APP_ID")
                .messages(messages)
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf("text: %s\n",
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("message："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
text: 我可以帮助你完成多种任务，包括但不限于：

1. 回答问题：无论是学术问题、生活常识还是专业领域的问题，我都会尽力提供准确的答案。
2. 创作文字：比如写故事、写公文、写邮件、写剧本等，只需要给我一些基本的信息和要求即可。
3. 表格处理：可以帮你整理数据，生成或修改表格。
4. 代码写作：支持多种编程语言的代码编写与解释。
5. 多语言互译：可以在不同语言之间进行翻译。
6. 模拟对话：可以扮演不同的角色与用户进行模拟对话。

如果你有任何具体的需求，请随时告诉我！
```

##### **HTTP**

##### **curl**

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "messages":[      
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            },
            {
                "role": "assistant",
                "content": "我是阿里云开发的大规模语言模型，我叫通义千问。"
            },
            {
                "role": "user",
                "content": "你能做什么？"
            }
        ]
    },
    "parameters":  {},
    "debug": {}
}'
```

**响应示例**

```
{"output":
{"finish_reason":"stop","session_id":"990ca89d89794826976d7499ad10cddb",
"text":"我可以帮助你完成多种任务，包括但不限于：\n\n1. 回答问题：无论是学术知识、实用技巧还是常识性问题，我都会尽力提供准确的答案。\n2. 创作文字：比如写故事、写公文、写邮件、写剧本等等，只要你告诉我具体需求，我就能帮你撰写。\n3. 表达观点：对于一些主观性的问题，我也可以给出自己的看法，并与你进行讨论。\n4. 游戏娱乐：我们可以一起玩文字游戏，或者让我为你讲个笑话放松一下。\n\n总之，任何与语言相关的事情，都可以找我帮忙！"},
"usage":{"models":[{"output_tokens":126,"model_id":"qwen-max","input_tokens":86}]},"request_id":"3908c4a3-8d7a-9e51-81a5-0fc366582990"}%
```

##### **PHP**

**请求示例**

```
<?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        "messages" => [
            [
                "role" => "system",
                "content" => "You are a helpful assistant."
            ],
            [
                "role" => "user",
                "content" => "你是谁？"
            ],
            [
                "role" => "assistant",
                "content" => "我是阿里云开发的大规模语言模型，我叫通义千问。"
            ],
            [
                "role" => "user",
                "content" => "你能做什么？"
            ]
        ]
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);

// 解码响应数据
$response_data = json_decode($response, true);

// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo "{$response_data['output']['text']}\n";
    } else {
        echo "No text in response.\n";
    }
} else {
    if (isset($response_data['request_id'])) {
        echo "request_id={$response_data['request_id']}\n";
    }
    echo "code={$status_code}\n";
    if (isset($response_data['message'])) {
        echo "message={$response_data['message']}\n";
    } else {
        echo "message=Unknown error\n";
    }
}
?>
```

**响应示例**

```
我可以帮助你完成多种任务，比如：

1. 回答问题：无论是学术问题、实用知识还是娱乐八卦，我都会尽力提供准确的答案。
2. 创作文字：包括但不限于写故事、写公文、写邮件等。
3. 提供建议：如旅行建议、学习方法、职业规划等方面的指导和建议。
4. 进行对话：我们可以聊天交流，分享心情，甚至进行一些有趣的讨论。

如果你有任何需要帮助的地方，都可以告诉我哦！
```

##### **Node.js**

**需安装相关依赖：**

```
npm install axios
```

**请求示例**

```
const axios = require('axios');
async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';//替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        "input": {
        "messages":[      
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            },
            {
                "role": "assistant",
                "content": "我是阿里云开发的大规模语言模型，我叫通义千问。"
            },
            {
                "role": "user",
                "content": "你能做什么？"
            }
        ]
    },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response statusText: ${error.response.statusText}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
可以帮助你完成多种任务，包括但不限于：

1. 回答问题：无论是学术知识、实用信息还是常识性问题，我都会尽力提供准确的答案。
2. 创作文字：比如写故事、写公文、写邮件、写剧本等，只要你给出足够的背景信息和要求，我就能帮你撰写。
3. 提供建议：如果你需要在某些决策上得到建议，比如旅行目的地选择、礼物挑选、学习方法等，我也可以根据你的描述提供建议。
4. 语言翻译：支持多国语言之间的文本翻译。
5. 代码编写与解释：对于编程相关的问题，我可以帮助编写简单的程序或解释复杂的概念。
6. 进行对话：除了上述功能外，我还能够与用户进行日常交流，分享想法。

如果你有任何具体的需求，请随时告诉我！
```

##### **C#**

**请求示例**

```
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
        string appId = "APP_ID";// 替换为实际的应用ID
        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("请确保设置了 DASHSCOPE_API_KEY。");
            return;
        }

        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";
        
        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            string jsonContent = $@"{{
                ""input"": {{
                    ""messages"": [
                        {{
                            ""role"": ""system"",
                            ""content"": ""You are a helpful assistant.""
                        }},
                        {{
                            ""role"": ""user"",
                            ""content"": ""你是谁？""
                        }},
                        {{
                            ""role"": ""assistant"",
                            ""content"": ""我是阿里云开发的大规模语言模型，我叫通义千问。""
                        }},
                        {{
                            ""role"": ""user"",
                            ""content"": ""你能做什么？""
                        }}
                    ]
                }},
                ""parameters"": {{}},
                ""debug"": {{}}
            }}";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "a6d041ca3d084a7ca9eff1c456afad70",
        "text": "作为通义千问，我可以帮助您完成多种任务，包括但不限于：\n\n1. 回答问题：提供各类知识性问题的答案。\n2. 文本生成：撰写文章、故事、诗歌等文本内容。\n3. 语言翻译：进行不同语言之间的翻译工作。\n4. 对话交流：与用户进行自然流畅的对话。\n5. 提供建议：根据用户需求提供建议或解决方案。\n\n如果您有任何具体的需求，请告诉我，我会尽力为您提供帮助。"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 102,
                "model_id": "qwen-max",
                "input_tokens": 87
            }
        ]
    },
    "request_id": "27fb8a01-70d5-974f-bb0a-e9408a9c1772"
}
```

##### **Go**

**请求示例**

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]interface{}{
			"messages": []interface{}{
				map[string]string{
					"role":    "system",
					"content": "You are a helpful assistant.",
				},
				map[string]string{
					"role":    "user",
					"content": "你是谁？",
				},
				map[string]string{
					"role":    "assistant",
					"content": "我是阿里云开发的大规模语言模型，我叫通义千问。",
				},
				map[string]string{
					"role":    "user",
					"content": "你能做什么？",
				},
			},
		},
		"parameters": map[string]interface{}{},
		"debug":      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Failed to marshal JSON: %v\n", err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Failed to create request: %v\n", err)
		return
	}

	// 设置请求头
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read response: %v\n", err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println("Request successful:")
		fmt.Println(string(body))
	} else {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		fmt.Println(string(body))
	}
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "2ae51a5eac3b4b269834cf0695330a05",
        "text": "我可以帮助你完成多种任务，包括但不限于：\n\n1. 回答问题：提供各种领域的知识性问题解答。\n2. 文本创作：撰写故事、文章、诗歌等。\n3. 编程助手：提供编程方面的指导和代码示例。\n4. 对话聊天：进行日常对话，陪伴交流。\n5. 翻译服务：提供多语言之间的翻译支持。\n6. 信息查询：查找新闻、天气预报、历史数据等信息。\n7. 学习辅导：帮助解答学习中的疑惑，提供学习建议。\n\n如果你有任何具体的需求或问题，都可以告诉我，我会尽力帮助你！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 132,
                "model_id": "qwen-max",
                "input_tokens": 87
            }
        ]
    },
    "request_id": "1289eb09-e4ed-9f9e-98ca-805c83b333a1"
}
```

## **流式输出**

大模型接收输入后，逐步生成中间结果并实时输出，这种方式称为流式输出，可让您在模型生成过程中即时查看内容，减少等待时间。

根据调用方式的不同，设置相应参数即可启用流式输出：

-   Python SDK方式：设置`stream`参数为`True`。
    
-   Java SDK方式：使用`streamCall`方法。
    
-   HTTP方式：在`Header`中指定`X-DashScope-SSE`为`enable`。
    

流式输出的内容默认是非增量式（即每次返回的内容都包含之前生成的内容），如需增量输出，请设置相应参数：

-   Python SDK方式：设置 `incremental_output`参数为`True`。
    
-   Java SDK方式：使用 `incrementalOutput` 方法并设置为 `true`。
    
-   HTTP方式：在 `parameters` 中使用 `incremental_output`参数并设置为`true`。
    

#### **流式输出模式**

工作流应用通过`flow_stream_mode`参数控制流式输出模式，参数值如下：

`**message_format_plus**`**（推荐）**

消息增强模式。在`workflow_message`字段流式返回**所有节点**的执行过程和结果，覆盖全部节点类型。与`message_format`返回相同数据结构。

> Python SDK 版本至少为1.24.0，Java SDK 版本至少为2.22.18。

`**message_format**`**（推荐）**

消息模式。在`message`字段结构化的流式返回**指定节点**的执行结果。必要条件：需在控制台为目标节点开启**流式输出**开关。

`**full_thoughts**`（默认，不推荐）

完整思考模式。在`thoughts`字段流式返回**所有节点**的执行详情，适用于调试。

必要条件：需设置`has_thoughts`参数为`true`。

不推荐新业务使用，建议改用`message_format`或`message_format_plus`。

## message\_format\_plus模式

消息增强模式。覆盖所有节点类型，通过`workflow_message`字段流式返回各节点的执行状态和结果。与`message_format`模式返回相同的数据结构，但支持全部节点类型的流式推送。

**重要**

**客户端处理规则：**

-   所有节点的`message.content`均为增量输出，需**追加拼接**。部分节点（如开始节点、变量替换等）仅推送一次数据包。
    
-   当`node_is_completed=true`时，标记该节点执行完毕。
    

## HTTP

**请求示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion' \
--header 'X-DashScope-SSE: enable' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_DASHSCOPE_API_KEY' \
--data '{
    "input": {
        "prompt": "你好"
    },
    "parameters": {
        "flow_stream_mode": "message_format_plus"
    }
}'
```

**响应示例**

以下为多条 SSE 事件的响应示例，展示工作流从开始到结束的完整推送过程：

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"3d46d9a4ae...","workflow_message":{"node_status":"success","node_type":"Start","node_msg_seq_id":1,"node_name":"开始","message":{"content":"{\"user\":{}}","role":"assistant"},"node_is_completed":true,"node_id":"Start_iEca"},"finish_reason":"null"},"usage":{},"request_id":"0e241c2b-..."}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"3d46d9a4ae...","workflow_message":{"node_status":"executing","node_type":"LLM","node_msg_seq_id":1,"node_name":"大模型1","message":{"content":"{\"result\":\"你好\",\"reasoningContent\":\"\"}","role":"assistant"},"node_is_completed":false,"node_id":"LLM_NPem"},"finish_reason":"null"},"usage":{},"request_id":"0e241c2b-..."}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"3d46d9a4ae...","workflow_message":{"node_status":"executing","node_type":"LLM","node_msg_seq_id":2,"node_name":"大模型1","message":{"content":"{\"result\":\"呀！有什么\",\"reasoningContent\":\"\"}","role":"assistant"},"node_is_completed":false,"node_id":"LLM_NPem"},"finish_reason":"null"},"usage":{},"request_id":"0e241c2b-..."}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"3d46d9a4ae...","workflow_message":{"node_status":"success","node_type":"LLM","node_msg_seq_id":10,"node_name":"大模型1","message":{"content":"","role":"assistant"},"node_is_completed":true,"node_id":"LLM_NPem"},"finish_reason":"null"},"usage":{"models":[{"input_tokens":15,"output_tokens":50,"model_id":"qwen-plus-latest"}]},"request_id":"0e241c2b-..."}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"3d46d9a4ae...","workflow_message":{"node_status":"success","node_type":"End","node_msg_seq_id":2,"node_name":"结束","message":{"content":"","role":"assistant"},"node_is_completed":true,"node_id":"End_pmAh"},"finish_reason":"null"},"usage":{"models":[{"input_tokens":15,"output_tokens":50,"model_id":"qwen-plus-latest"}]},"request_id":"0e241c2b-..."}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"3d46d9a4ae...","finish_reason":"stop","text":"你好呀！有什么可以帮您的吗？"},"usage":{"models":[{"input_tokens":15,"output_tokens":50,"model_id":"qwen-plus-latest"}]},"request_id":"0e241c2b-..."}
```

## Python

**请求示例**

```
# Python SDK版本至少为1.24.0
from http import HTTPStatus
from dashscope import Application
import os

def call_workflow_plus():
    responses = Application.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id="YOUR_APP_ID",
        stream=True,
        flow_stream_mode="message_format_plus",
        prompt='你好')

    for response in responses:
        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}, code={response.status_code}, message={response.message}')
        else:
            wm = getattr(response.output, 'workflow_message', None)
            if wm:
                print(f'node={wm.get("node_name")}, status={wm.get("node_status")}, '
                      f'completed={wm.get("node_is_completed")}, '
                      f'content={wm.get("message", {}).get("content", "")}')

if __name__ == '__main__':
    call_workflow_plus()
```

## Java

**请求示例**

```
// Java SDK版本至少为2.22.18
import com.alibaba.dashscope.app.*;
import io.reactivex.Flowable;

public class WorkflowPlusExample {
    public static void main(String[] args) throws Exception {
        ApplicationParam param = ApplicationParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .appId("YOUR_APP_ID")
            .prompt("你好")
            .flowStreamMode(FlowStreamMode.MESSAGE_FORMAT_PLUS)
            .build();

        Application application = new Application();
        Flowable<ApplicationResult> result = application.streamCall(param);
        result.blockingForEach(data -> {
            if (data.getOutput().getWorkflowMessage() != null) {
                System.out.println("node=" + data.getOutput().getWorkflowMessage().getNodeName()
                    + ", completed=" + data.getOutput().getWorkflowMessage().getNodeIsCompleted()
                    + ", content=" + data.getOutput().getWorkflowMessage().getMessage().getContent());
            }
        });
    }
}
```

## message\_format模式

通过API调用**已发布**的**工作流应用**：配置结束节点打开**流式输出**开关。

## Python

**请求示例**

```
# Python SDK版本至少为1.24.0
from http import HTTPStatus
from dashscope import Application
import os
def bailianTask():
    responses = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id="APP_ID",# 替换为实际的应用 ID
        base_address="https://dashscope.aliyuncs.com/api/v1/",
        stream=True, # 开启流式输出
        flow_stream_mode="message_format",# 消息模式，输出/结束节点的流式结果
        prompt='你是谁？')

    for response in responses:
        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}')
            print(f'code={response.status_code}')
            print(f'message={response.message}')
            print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        else:
            if response.output.finish_reason != "stop":
                print(f'workflowMessage={response.output.workflow_message}\n')
            else:
                print(f'text={response.output.text}\n')  

if __name__ == "__main__":
    bailianTask()
```

**响应示例**

```
workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 1, 'node_name': '结束', 'message': {'content': '我是', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 2, 'node_name': '结束', 'message': {'content': '通义千问，阿里巴巴集团', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 3, 'node_name': '结束', 'message': {'content': '旗下的通义实验室自主研发的', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 4, 'node_name': '结束', 'message': {'content': '超大规模语言模型。我可以', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 5, 'node_name': '结束', 'message': {'content': '帮助你回答问题、创作', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 6, 'node_name': '结束', 'message': {'content': '文字，比如写故事、', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 7, 'node_name': '结束', 'message': {'content': '写公文、写邮件', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 8, 'node_name': '结束', 'message': {'content': '、写剧本、逻辑推理', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 9, 'node_name': '结束', 'message': {'content': '、编程等等，还能表达观点，玩游戏等。如果你', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'executing', 'node_type': 'End', 'node_msg_seq_id': 10, 'node_name': '结束', 'message': {'content': '有任何问题或需要帮助，欢迎随时告诉我！', 'role': 'assistant'}, 'node_is_completed': False, 'node_id': 'End_7w1V'}

workflowMessage={'node_status': 'success', 'node_type': 'End', 'node_msg_seq_id': 11, 'node_name': '结束', 'message': {'content': '', 'role': 'assistant'}, 'node_is_completed': True, 'node_id': 'End_7w1V'}

text=我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Java

**请求示例**

```
//Java SDK版本至少为2.21.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    public static void streamCall() throws ApiException, NoApiKeyException, InputRequiredException {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("APP_ID") //替换为实际的应用 ID
                .flowStreamMode(FlowStreamMode.MESSAGE_FORMAT)
                .prompt("你是谁？")
                .build();

        Application application = new Application();
        Flowable<ApplicationResult> result = application.streamCall(param); // 实现流式输出
        result.blockingForEach(data -> {
            if (data.getOutput().getFinishReason().equals("stop")){
                System.out.printf("task is finished ,text = %s\n", data.getOutput().getText());
            }else {
                System.out.printf("%s\n", data.getOutput().getWorkflowMessage().getMessage().getContent());
            }

        });
    }

    public static void main(String[] args) {
        try {
            for (int i = 0; i < 1; i++){
                long start = System.currentTimeMillis();
                streamCall();
                long end = System.currentTimeMillis();
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("message："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
我是
通义千问，阿里巴巴集团
旗下的通义实验室自主研发的超大规模语言模型。我可以
帮助你回答问题、创作
文字，比如写故事、
写公文、写邮件、写剧本、逻辑推理
、编程等等，还能表达观点，玩游戏等。如果你
有任何问题或需要帮助，
欢迎随时告诉我！
task is finished ,text = 我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## HTTP

## curl

**请求示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion' \
--header 'X-DashScope-SSE: enable' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    "input": {
        "prompt": "你是谁？"
    },
    "parameters":  {
        "flow_stream_mode": "message_format"
    },
    "debug": {}
}'
```

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":1,"node_name":"结束","message":{"content":"我是通义千问","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":2,"node_name":"结束","message":{"content":"，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":3,"node_name":"结束","message":{"content":"帮助你回答问题、创作","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":4,"node_name":"结束","message":{"content":"文字，比如写故事、","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":5,"node_name":"结束","message":{"content":"写公文、写邮件、写剧本、逻辑推理","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":6,"node_name":"结束","message":{"content":"、编程等等，还能表达","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:7
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":7,"node_name":"结束","message":{"content":"观点，玩游戏等。如果你","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:8
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":8,"node_name":"结束","message":{"content":"有任何问题或需要帮助，","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:9
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":9,"node_name":"结束","message":{"content":"欢迎随时告诉我！","role":"assistant"},"node_is_completed":false,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:10
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","workflow_message":{"node_status":"success","node_type":"End","node_msg_seq_id":10,"node_name":"结束","message":{"content":"","role":"assistant"},"node_is_completed":true,"node_id":"End_7w1V"},"finish_reason":"null"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}

id:11
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"0a6aff53d8e945e4900452f04d55499b","finish_reason":"stop","text":"我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"},"usage":{},"request_id":"88878d48-097f-99c3-b6b9-b76f7366da90"}
```

## PHP

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '你是谁？'
    ],
    "parameters" => [
        'flow_stream_mode' => 'message_format', 
    ]
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, false); // 不返回传输的数据
curl_setopt($ch, CURLOPT_WRITEFUNCTION, function ($ch, $string) {
    echo $string; // 处理流式数据
    return strlen($string);
});
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key,
    'X-DashScope-SSE: enable' // 流式输出固定参数
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);

if ($status_code != 200) {
    echo "HTTP Status Code: $status_code\n";
    echo "Request Failed.\n";
}
?>
```

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":1,"node_name":"结束","message":{"content":"我是","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":2,"node_name":"结束","message":{"content":"通义千问，阿里巴巴集团","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":3,"node_name":"结束","message":{"content":"旗下的通义实验室自主研发的超大规模语言模型。我可以","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":4,"node_name":"结束","message":{"content":"帮助你回答问题、创作文字，比如写故事、","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":5,"node_name":"结束","message":{"content":"写公文、写邮件","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":6,"node_name":"结束","message":{"content":"、写剧本、逻辑推理","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:7
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":7,"node_name":"结束","message":{"content":"、编程等等，还能表达观点，玩游戏等。如果你","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:8
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":8,"node_name":"结束","message":{"content":"有任何问题或需要帮助，","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:9
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":9,"node_name":"结束","message":{"content":"欢迎随时告诉我！","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:10
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","workflow_message":{"node_status":"success","node_type":"End","node_msg_seq_id":10,"node_name":"结束","message":{"content":"","role":"assistant"},"node_is_completed":true,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}

id:11
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"45e68c1f3d19467b91f032c9889d61c4","finish_reason":"stop","text":"我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"},"usage":{},"request_id":"1f077942-e1c1-9d0c-82f2-31f1112b3e1c"}
```

## Node.js

**需安装相关依赖：**

```
npm install axios
```

**请求示例**

```
const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "你是谁？"
 
        },
        parameters: {
            "flow_stream_mode" : "message_format"
        },
        debug: {}
    };

    try {
        console.log("Sending request to DashScope API...");

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable'
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            console.log("Request successful:");

            // 处理流式响应
            response.data.on('data', (chunk) => {
                console.log(`Received chunk: ${chunk.toString()}`);
            });

            response.data.on('end', () => {
                console.log("Stream ended.");
            });

            response.data.on('error', (error) => {
                console.error(`Stream error: ${error.message}`);
            });
        } else {
            console.log("Request failed:");
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response statusText: ${error.response.statusText}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
Request successful:
Received chunk: id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":1,"node_name":"结束","message":{"content":"我是通义千问","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":2,"node_name":"结束","message":{"content":"，阿里巴巴集团","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":3,"node_name":"结束","message":{"content":"旗下的通义实验室自主研发的","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":4,"node_name":"结束","message":{"content":"超大规模语言模型。我可以","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":5,"node_name":"结束","message":{"content":"帮助你回答问题、创作","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":6,"node_name":"结束","message":{"content":"文字，比如写故事、","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:7
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":7,"node_name":"结束","message":{"content":"写公文、写邮件","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:8
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":8,"node_name":"结束","message":{"content":"、写剧本、逻辑推理","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:9
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":9,"node_name":"结束","message":{"content":"、编程等等，还能表达观点，玩游戏等。如果你","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:10
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":10,"node_name":"结束","message":{"content":"有任何问题或需要帮助，","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:11
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","workflow_message":{"node_status":"success","node_type":"End","node_msg_seq_id":11,"node_name":"结束","message":{"content":"欢迎随时告诉我！","role":"assistant"},"node_is_completed":true,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Received chunk: id:12
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"9830d3f2390f4a0e995ddb17bbe406ed","finish_reason":"stop","text":"我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"},"usage":{},"request_id":"8c78a39e-4126-9d76-b00e-cf8b06d12ded"}

Stream ended.
```

## C#

**请求示例**

```
using System.Net;
using System.Text;
class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
        string appId = "APP_ID"; // 替换为实际的应用ID
        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            client.DefaultRequestHeaders.Add("X-DashScope-SSE", "enable");

            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""你是谁？""
                },
                ""parameters"": {
                    ""flow_stream_mode"": ""message_format"" 
                    },
                ""debug"": {}
            }";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss:fff"));
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Post, url);
                request.Content = content;

                HttpResponseMessage response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
                

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Request successful:");
                    Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss:fff"));
                    using (var stream = await response.Content.ReadAsStreamAsync())
                    using (var reader = new StreamReader(stream))
                    {
                        string? line; // 声明为可空字符串
                        while ((line = await reader.ReadLineAsync()) != null)
                        {
                            if (line.StartsWith("data:"))
                            {
                                string data = line.Substring(5).Trim();
                                Console.WriteLine(data);
                                Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss:fff"));
                            }
                        }
                    }
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
2025-07-23 10:43:12:090
Request successful:
2025-07-23 10:43:13:323
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":1,"node_name":"结束","message":{"content":"我是通","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:13:370
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":2,"node_name":"结束","message":{"content":"义千问，阿里巴巴集团","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:13:371
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":3,"node_name":"结束","message":{"content":"旗下的通义实验室自主研发的超大规模语言模型。我可以","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:13:416
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":4,"node_name":"结束","message":{"content":"帮助你回答问题、创作文字，比如写故事、","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:13:519
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":5,"node_name":"结束","message":{"content":"写公文、写邮件、写剧本、逻辑推理","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:13:719
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":6,"node_name":"结束","message":{"content":"、编程等等，还能表达观点，玩游戏等。如果你","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:13:921
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":7,"node_name":"结束","message":{"content":"有任何问题或需要帮助，","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:14:022
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","workflow_message":{"node_status":"success","node_type":"End","node_msg_seq_id":8,"node_name":"结束","message":{"content":"欢迎随时告诉我！","role":"assistant"},"node_is_completed":true,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
2025-07-23 10:43:14:127
{"output":{"session_id":"20ef9ae27ee64d1dacfdb532963a5a93","finish_reason":"stop","text":"我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"},"usage":{},"request_id":"dcff0825-07c8-9dce-bc8b-a8a565c546c1"}
```

## Go

**请求示例**

```
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

func main() {
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	data := map[string]interface{}{
		"input": map[string]string{
			"prompt": "你是谁？",
		},
		"parameters": map[string]string{
			"flow_stream_mode": "message_format",
		},
		"debug": map[string]interface{}{},
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	req.Header.Set("X-DashScope-SSE", "enable")
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading response: %v\n", err)
	}

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
	}
}
```

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":1,"node_name":"结束","message":{"content":"我是","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":2,"node_name":"结束","message":{"content":"通义千问，阿里巴巴集团","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":3,"node_name":"结束","message":{"content":"旗下的通义实验室自主研发的超大规模语言模型。我可以","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":4,"node_name":"结束","message":{"content":"帮助你回答问题、创作","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":5,"node_name":"结束","message":{"content":"文字，比如写故事、","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":6,"node_name":"结束","message":{"content":"写公文、写邮件","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:7
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":7,"node_name":"结束","message":{"content":"、写剧本、逻辑推理","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:8
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":8,"node_name":"结束","message":{"content":"、编程等等，还能表达观点，玩游戏等。如果你","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:9
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":9,"node_name":"结束","message":{"content":"有任何问题或需要帮助，","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:10
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"executing","node_type":"End","node_msg_seq_id":10,"node_name":"结束","message":{"content":"欢迎随时告诉我！","role":"assistant"},"node_is_completed":false,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:11
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","workflow_message":{"node_status":"success","node_type":"End","node_msg_seq_id":11,"node_name":"结束","message":{"content":"","role":"assistant"},"node_is_completed":true,"node_id":"End_FHh1"},"finish_reason":"null"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}

id:12
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"fc3b6fd2c7664e92841ba040fc1bc2ef","finish_reason":"stop","text":"我是通义千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"},"usage":{},"request_id":"b1f7dc74-e0b7-9329-a6fc-603916f57310"}
```

## **full\_thoughts模式**

**说明**

不推荐新业务使用，建议改用`message_format`或`message_format_plus`。

通过API调用**已发布**的**工作流应用**：开始节点配置`city`参数，两个大模型节点分别对`city`的美食和景点进行流式输出。

## Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application
biz_params = {
    "city": "杭州"}
responses = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 替换为实际的应用 ID
    app_id='APP_ID',
    prompt='你好',
    biz_params=biz_params,
    # 开启流式输出
    stream=True,
    # incremental_output为true开启增量输出，为false关闭增量输出，不填写默认false
    incremental_output=True,
    # 工作流应用和智能体编排应用的流式输出实现需要设置has_thoughts为True
    has_thoughts=True)

for response in responses:
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print(f'{response.output.thoughts}\n')  # 处理输出只返回thoughts；在output的thoughts字段中返回过程信息
```

**响应示例**

```
[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"LLM_Ilo9","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_Ilo9"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"西湖醋鱼,\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_Ilo9"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"东坡肉,\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_Ilo9"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"知味观小\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_Ilo9"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"笼包,龙井虾仁,\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_Ilo9"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"叫化鸡\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"LLM_vQDv","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_vQDv"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_kBgf","nodeResult":"{\\"result\\":\\"西湖,灵隐\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_vQDv"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_kBgf","nodeResult":"{\\"result\\":\\"寺,宋城\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_vQDv"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_kBgf","nodeResult":"{\\"result\\":\\",西溪湿地\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_vQDv"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_kBgf","nodeResult":"{\\"result\\":\\",千岛湖\\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_vQDv"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]

[ApplicationThought(thought=None, action_type=None, response='{"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_Bsvj","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_Ilo9","nodeExecTime":"1332ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"大模型_kBgf","nodeResult":"{\\"result\\":\\"\\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_vQDv","nodeExecTime":"948ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None), ApplicationThought(thought=None, action_type=None, response='{"nodeName":"结束","nodeResult":"{\\"result\\":\\"西湖,灵隐寺,宋城,西溪湿地,千岛湖\\"}","nodeType":"End","nodeStatus":"success","nodeId":"End_DrQn7F","nodeExecTime":"1ms"}', action_name=None, action=None, action_input_stream=None, action_input=None, observation=None)]
```

## Java

**请求示例**

```
// 建议dashscope SDK的版本 >= 2.15.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import io.reactivex.Flowable;

public class Main {
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        String bizParams =
                "{\"city\":\"杭州\"}";
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("APP_ID") //替换为实际的应用 ID
                .prompt("你好")
                .bizParams(JsonUtils.parse(bizParams))
                .incrementalOutput(true) // 增量输出
                .hasThoughts(true) // 工作流应用实现流式输出需要设置此参数为true，输出结果在thoughts字段中查看
                .build();

        Application application = new Application();
        Flowable<ApplicationResult> result = application.streamCall(param); // 实现流式输出
        result.blockingForEach(data -> {
            System.out.printf("%s\n",data.getOutput().getThoughts());// 处理输出只展示thoughts字段
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf("Exception: %s", e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"LLM_S78u","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_S78u"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"西湖醋鱼,\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_S78u"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"龙井虾仁\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_S78u"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\",东坡肉,知味小\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_S78u"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"笼,叫花\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_S78u"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"鸡\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_S78u","nodeExecTime":"1164ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"LLM_5ZzA","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_5ZzA"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_S78u","nodeExecTime":"1164ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_jjc0","nodeResult":"{\"result\":\"西湖,\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_5ZzA"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_S78u","nodeExecTime":"1164ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_jjc0","nodeResult":"{\"result\":\"灵隐\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_5ZzA"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_S78u","nodeExecTime":"1164ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_jjc0","nodeResult":"{\"result\":\"寺,宋城\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_5ZzA"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_S78u","nodeExecTime":"1164ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_jjc0","nodeResult":"{\"result\":\",西溪湿地,千岛湖\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_5ZzA"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_bYxoRU","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_UTh7","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_S78u","nodeExecTime":"1164ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型_jjc0","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_5ZzA","nodeExecTime":"938ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"西湖,灵隐寺,宋城,西溪湿地,千岛湖\"}","nodeType":"End","nodeStatus":"success","nodeId":"End_DrQn7F","nodeExecTime":"5ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
```

## HTTP

## curl

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header 'X-DashScope-SSE: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "你好",
        "biz_params": {
        "city": "杭州"}
    },
    "parameters":  {
        "has_thoughts": true,
        "incremental_output": true
    },
    "debug": {}
}'
```

> APP\_ID替换为实际的应用 ID。

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"LLM_j45e\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖醋鱼,龙\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":5,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"井虾仁,东坡肉,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":13,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"叫花鸡,宋\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":18,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:7
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"嫂鱼羹\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"},{"response":"{\"nodeName\":\"LLM_2Km9\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:8
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":2,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:9
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"灵\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":3,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:10
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"隐寺,宋城,西溪\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":11,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:11
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"国家湿地公园,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":15,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}

id:12
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"杭州动物园\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_2Km9\",\"nodeExecTime\":\"1137ms\"}"},{"response":"{\"nodeName\":\"结束\",\"nodeResult\":\"{\\\"result\\\":\\\"亲，对我的介绍还满意吗\\\"}\",\"nodeType\":\"End\",\"nodeStatus\":\"success\",\"nodeId\":\"End_DrQn7F\",\"nodeExecTime\":\"1ms\"}"}],"session_id":"6035ee0814b64a9fb88346ecaf8b44bf","finish_reason":"stop","text":"亲，对我的介绍还满意吗"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":17,"model_id":"qwen-max"}]},"request_id":"64825069-b3aa-93a7-bcf1-c66fe57111fd"}
```

## PHP

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '你好',
        'biz_params' => [
            'city' => '杭州'
        ]
    ],
    "parameters" => [
        'has_thoughts' => true, // 工作流应用和编排应用必须设置此参数为true，过程信息在thoughts中返回
        'incremental_output' => true // 增量输出
    ]
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, false); // 不返回传输的数据
curl_setopt($ch, CURLOPT_WRITEFUNCTION, function ($ch, $string) {
    echo $string; // 处理流式数据
    return strlen($string);
});
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key,
    'X-DashScope-SSE: enable' // 流式输出固定参数
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);

if ($status_code != 200) {
    echo "HTTP Status Code: $status_code\n";
    echo "Request Failed.\n";
}
?>
```

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:2
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"LLM_Ilo9\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_Ilo9\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:3
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖醋鱼\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_Ilo9\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:4
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\",\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_Ilo9\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:5
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"东坡肉,知味小笼\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_Ilo9\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:6
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\",龙井虾\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_Ilo9\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:7
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"仁,叫化鸡\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_Ilo9\",\"nodeExecTime\":\"1486ms\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:8
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_Ilo9\",\"nodeExecTime\":\"1486ms\"}"},{"response":"{\"nodeName\":\"LLM_vQDv\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_vQDv\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:9
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_Ilo9\",\"nodeExecTime\":\"1486ms\"}"},{"response":"{\"nodeName\":\"大模型_kBgf\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖,灵隐\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_vQDv\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:10
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_Ilo9\",\"nodeExecTime\":\"1486ms\"}"},{"response":"{\"nodeName\":\"大模型_kBgf\",\"nodeResult\":\"{\\\"result\\\":\\\"寺,宋城\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_vQDv\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:11
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_Ilo9\",\"nodeExecTime\":\"1486ms\"}"},{"response":"{\"nodeName\":\"大模型_kBgf\",\"nodeResult\":\"{\\\"result\\\":\\\",西溪湿地\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_vQDv\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"null"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
id:12
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_Bsvj\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_Ilo9\",\"nodeExecTime\":\"1486ms\"}"},{"response":"{\"nodeName\":\"大模型_kBgf\",\"nodeResult\":\"{\\\"result\\\":\\\",杭州塔\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_vQDv\",\"nodeExecTime\":\"899ms\"}"},{"response":"{\"nodeName\":\"结束\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖,灵隐寺,宋城,西溪湿地,杭州塔\\\"}\",\"nodeType\":\"End\",\"nodeStatus\":\"success\",\"nodeId\":\"End_DrQn7F\",\"nodeExecTime\":\"0ms\"}"}],"session_id":"a3b73a6db84d444d8efdab2b2e754f52","finish_reason":"stop","text":"西湖,灵隐寺,宋城,西溪湿地,杭州塔"},"usage":{},"request_id":"795e98eb-5de3-969f-a9b5-5983d1b6d955"}
```

## Node.js

需安装相关依赖：

```
npm install axios
```

**请求示例**

```
const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "你好",
            biz_params:{
                'city':'杭州'
            }
        },
        parameters: {
            'incremental_output' : 'true',
            'has_thoughts':'true'//工作流应用和智能体编排应用实现流式输出需要设置此参数
        },
        debug: {}
    };

    try {
        console.log("Sending request to DashScope API...");

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable'
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            console.log("Request successful:");

            // 处理流式响应
            response.data.on('data', (chunk) => {
                console.log(`Received chunk: ${chunk.toString()}`);
            });

            response.data.on('end', () => {
                console.log("Stream ended.");
            });

            response.data.on('error', (error) => {
                console.error(`Stream error: ${error.message}`);
            });
        } else {
            console.log("Request failed:");
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response statusText: ${error.response.statusText}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
/opt/homebrew/bin/node ./index.js
Sending request to DashScope API...
Request successful:
Received chunk: id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:2
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:3
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"西湖醋\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:4
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"鱼,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:5
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"龙井虾仁\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:6
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",东坡肉\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:7
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",知味观\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:8
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"小笼包,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:9
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"叫花鸡\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"2180ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:10
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"2180ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"西湖,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:11
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"2180ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"灵隐\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:12
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"2180ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"寺,宋城,西溪湿地\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:13
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"2180ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",千岛湖\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"null"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Received chunk: id:14
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"2180ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_5ZzA\",\"nodeExecTime\":\"855ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"西湖,灵隐寺,宋城,西溪湿地,千岛湖\\\"}\",\"nodeType\":\"End\",\"nodeStatus\":\"success\",\"nodeId\":\"End_DrQn7F\",\"nodeExecTime\":\"1ms\"}"}],"session_id":"7e9fcc8be3294954815c1a0a956d5e55","finish_reason":"stop","text":"西湖,灵隐寺,宋城,西溪湿地,千岛湖"},"usage":{},"request_id":"e52dce21-16a4-9a3d-ad6c-88e8921e927f"}
Stream ended.
```

## C#

**请求示例**

```
using System.Net;
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
        string appId = "APP_ID"; // 替换为实际的应用ID
        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            client.DefaultRequestHeaders.Add("X-DashScope-SSE", "enable");

            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""你好"",
                    ""biz_params"":{
                        ""city"":""杭州""
                    }
                },
                ""parameters"": {
                    ""incremental_output"": true,
                    ""has_thoughts"": true 
                    },
                ""debug"": {}
            }";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss:fff"));
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Post, url);
                request.Content = content;

                HttpResponseMessage response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
                

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Request successful:");
                    Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss:fff"));
                    using (var stream = await response.Content.ReadAsStreamAsync())
                    using (var reader = new StreamReader(stream))
                    {
                        string? line; // 声明为可空字符串
                        while ((line = await reader.ReadLineAsync()) != null)
                        {
                            if (line.StartsWith("data:"))
                            {
                                string data = line.Substring(5).Trim();
                                Console.WriteLine(data);
                                Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss:fff"));
                            }
                        }
                    }
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
2025-02-14 16:55:28:670
Request successful:
2025-02-14 16:55:28:980
{"output":{"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:28:980
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:28:980
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"LLM_j45e\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:29:178
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖醋鱼,龙\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":5,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:29:780
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"井虾仁,东坡肉,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":13,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:29:979
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"知味小笼,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_j45e\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":18,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:30:179
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"叫化鸡\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1315ms\"}"},{"response":"{\"nodeName\":\"LLM_2Km9\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:30:379
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1315ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"西湖,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":2,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:30:986
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1315ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"灵隐寺,宋\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":7,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:31:180
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1315ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"城,西溪湿地,千岛湖\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_2Km9\",\"nodeExecTime\":\"1008ms\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"null"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":16,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:31:382
{"output":{"thoughts":[{"response":"{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1315ms\"}"},{"response":"{\"nodeName\":\"大模型_2\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_2Km9\",\"nodeExecTime\":\"1008ms\"}"},{"response":"{\"nodeName\":\"结束\",\"nodeResult\":\"{\\\"result\\\":\\\"亲，对我的介绍还满意吗\\\"}\",\"nodeType\":\"End\",\"nodeStatus\":\"success\",\"nodeId\":\"End_DrQn7F\",\"nodeExecTime\":\"0ms\"}"}],"session_id":"1a3f45d95e654534bb01bdbf59e9b732","finish_reason":"stop","text":"亲，对我的介绍还满意吗"},"usage":{"models":[{"input_tokens":25,"output_tokens":21,"model_id":"qwen-max"},{"input_tokens":23,"output_tokens":16,"model_id":"qwen-max"}]},"request_id":"520d48fd-d7e8-9632-87e2-1ff866da1151"}
2025-02-14 16:55:31:751
```

## Go

**请求示例**

```
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

func main() {
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	requestBody := map[string]interface{}{
		"input": map[string]interface{}{
			"prompt": "你好",
			"biz_params": map[string]interface{}{
				"city": "杭州",
			},
		},
		"parameters": map[string]interface{}{
			"incremental_output": true,
			"has_thoughts":       true,
		},
		"debug": map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Failed to marshal JSON: %v\n", err)
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Failed to create request: %v\n", err)
		return
	}

	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-DashScope-SSE", "enable")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading response: %v\n", err)
	}

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
	}
}
```

**响应示例**

```
Request successful:
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"西湖醋\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"鱼,\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"龙井虾仁\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",东坡肉\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:7
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",知味小\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:8
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"笼,叫花\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_S78u\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:9
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"鸡\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:10
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"西湖,灵隐\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:11
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"寺,宋城\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:12
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",西溪湿地\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:13
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\",千岛湖\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_5ZzA\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:14
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_5ZzA\",\"nodeExecTime\":\"1760ms\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"null"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}

id:15
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"response":"{\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_S78u\",\"nodeExecTime\":\"1680ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_5ZzA\",\"nodeExecTime\":\"1760ms\"}"},{"response":"{\"nodeResult\":\"{\\\"result\\\":\\\"西湖,灵隐寺,宋城,西溪湿地,千岛湖\\\"}\",\"nodeType\":\"End\",\"nodeStatus\":\"success\",\"nodeId\":\"End_DrQn7F\",\"nodeExecTime\":\"1ms\"}"}],"session_id":"f3f5c63ec17d44b2a2e9aa18f0e6a22c","finish_reason":"stop","text":"西湖,灵隐寺,宋城,西溪湿地,千岛湖"},"usage":{},"request_id":"dfea28e9-801b-9c10-a4e7-c8fef790d34f"}
```

-   `thoughts`内每一项都是一个节点的执行详情，如下以一个LLM节点结果为例。
    
    ```
    id:7
    event:result
    :HTTP_STATUS/200
    data:
    {
        "output": {
            "thoughts": [
                {
                    "response": "{\"nodeName\":\"开始\",\"nodeType\":\"Start\",\"nodeStatus\":\"success\",\"nodeId\":\"Start_bYxoRU\",\"nodeExecTime\":\"0ms\"}"
                },
                {
                    "response": "{\"nodeName\":\"大模型_1\",\"nodeResult\":\"{\\\"result\\\":\\\"嫂鱼羹\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"success\",\"nodeId\":\"LLM_j45e\",\"nodeExecTime\":\"1167ms\"}"
                },
                {
                    "response": "{\"nodeName\":\"LLM_2Km9\",\"nodeResult\":\"{\\\"result\\\":\\\"\\\"}\",\"nodeType\":\"LLM\",\"nodeStatus\":\"executing\",\"nodeId\":\"LLM_2Km9\"}"
                }
            ],
            "session_id": "6035ee0814b64a9fb88346ecaf8b44bf",
            "finish_reason": "null"
        },
        "usage": {
            "models": [
                {
                    "input_tokens": 25,
                    "output_tokens": 21,
                    "model_id": "qwen-max"
                }
            ]
        },
        "request_id": "64825069-b3aa-93a7-bcf1-c66fe57111fd"
    }
    ```
    
    > 如果用户关注一个LLM节点（以上方LLM\_j45e为例）的流式结果，可以关注每次推送的`thoughts`中nodeId为LLM\_j45e的节点输出。
    
-   如果节点发生失败，则整个任务也会失败。
    

### **深度思考**

当工作流应用使用了[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking#5be853b164zv4)时，模型会在生成最终回复前进行一步或多步的推理，以提升处理复杂问题（如逻辑推理、代码生成、数学计算等）的准确性。

**重要**

工作流应用可包含多个大模型节点，思考模式需要在各大模型节点中分别设置，不支持通过 API 的`enable_thinking`参数动态控制。

#### **获取思考过程**

-   在 API 调用时，将 has\_thoughts 设置为 true。
    
-   或在控制台应用内的流程输出节点或结束节点引用指定大模型节点的 reasoningContent 变量。
    

模型返回的数据将包含：

**思考内容**：在`reasoningContent`字段中返回。

**回复内容**：在`result`字段中返回。

由于深度思考会增加响应时间，建议使用流式输出方式以获得更好的体验。示例如下：

## Python

**请求示例**

```
import json
from http import HTTPStatus
import os
from dashscope import Application

try:
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        app_id='APP_ID',# 替换为实际的应用 ID
        prompt='你是谁？',
        stream=True,  # 是否流式输出，True：流式输出；False（默认值）: 非流式输出
        incremental_output=True,  # 是否增量输出，True：增量输出；False（默认值）: 非增量输出
        has_thoughts=True,  # 是否返回思考过程，True：返回；False（默认值）: 不返回
    )

except Exception as e:
    print(f"API请求异常: {str(e)}")
    exit(1)

# 定义完整思考过程
reasoning_content = []
# 定义完整回复
answer_content = []
# 判断是否结束思考过程并开始回复
is_answering = False

def print_section(title):
    """打印带装饰的分段标题"""
    print(f"\n{'=' * 20} {title} {'=' * 20}\n", flush=True)

print_section("思考过程")

for chunk in response:
    if chunk.status_code != HTTPStatus.OK:
        print(f'request_id={chunk.request_id}')
        print(f'code={chunk.status_code}')
        print(f'message={chunk.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        continue
    
    # 跳过空数据块
    if not chunk.output or not chunk.output.thoughts:
        continue

    # 解析 JSON 数据
    for thought in chunk.output.thoughts:
        try:
            response_json = json.loads(thought.response)
            node_result = response_json.get('nodeResult', {})
            
            if isinstance(node_result, str):
                node_result = json.loads(node_result)
            
            extracted_reasoning_content = node_result.get('reasoningContent', '')
            extracted_result = node_result.get('result', '')
            node_name = response_json.get('nodeName', '')

            # 处理思考过程
            if extracted_reasoning_content and not is_answering:
                reasoning_content.append(extracted_reasoning_content)
                print(extracted_reasoning_content, end="", flush=True)
            
            # 处理回答内容
            if extracted_result and node_name != "结束":
                answer_content.append(extracted_result)
                if not is_answering:
                    print_section("完整回复")
                    is_answering = True
                print(extracted_result, end="", flush=True)

        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")

# 最终结果整合
final_reasoning = "".join(reasoning_content)
final_answer = "".join(answer_content)

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print_section("完整思考过程")
# print(final_reasoning)
# print_section("完整回复")
# print(final_answer)
```

**响应示例**

```
==================== 思考过程 ====================

您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。如您有任何问题，我会尽我所能为您提供帮助。
==================== 完整回复 ====================

您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。如您有任何问题，我会尽我所能为您提供帮助。
```

## Java

**请求示例**

```
// 建议dashscope SDK的版本 >= 2.15.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import io.reactivex.Flowable;

public class Main {
    static {
        Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
    }
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("APP_ID") //替换为实际的应用 ID
                .prompt("你是谁？")
                .incrementalOutput(true) // 增量输出
                .hasThoughts(true) // 工作流应用实现流式输出需要设置此参数为true，输出结果在thoughts字段中查看
                .build();

        Application application = new Application();
        Flowable<ApplicationResult> result = application.streamCall(param); // 实现流式输出
        result.blockingForEach(data -> {
            System.out.printf("%s\n",data.getOutput().getThoughts());// 处理输出只展示thoughts字段
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf("Exception: %s", e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"嗯\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，用户问了一个\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"很\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"基础的哲学\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"问题“你是谁”，\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"但结合上下文看\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，这\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"应该是第一次互动时的\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"常规询问\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"。用户\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"可能刚\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"接触AI助手\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，带着\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"好奇或\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"试探的心态，想\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"确认我的性质和\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"能力\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"边界。\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\\n\\n考虑到这是初始\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"对话，\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"需要平衡\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"专业性和\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"亲和力。用户\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"未必想\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"听长篇\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"大论\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"的技术说明，但\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"也不能回答\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"得太随意\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"。可以\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"突出三个关键点\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"：身份（Deep\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"Seek\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"开发的AI）、\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"功能（\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"解决问题\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"/陪伴聊天\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"）、态度（友好\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"开放\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"）。用“小伙伴\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"”的比喻降低距离感\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，结尾\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"的波浪线和\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"表情符号\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"能传递轻松\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"感。\\n\\n最后主动反问\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"用户\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"身份是\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"很好的社交策略——\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"既表达对\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"等\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"尊重，又把\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"对话主导权交\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"还给对方\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"。不过\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"“\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"你又是谁”\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"这种问法\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"可能稍\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"显直接\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，改成“可以\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"告诉我你是谁吗”\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"会更柔和\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，但\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"当前版本保留了\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"活泼感\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"，和\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"整体\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"语气\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"一致。\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"你好\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"你好\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"呀！我是你的\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"呀！我是你的\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"AI助手\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"AI助手\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"，由深度求\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"，由深度求\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"索公司\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"索公司\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"（Deep\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"（Deep\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"Seek）开发\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"Seek）开发\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"的语言模型，名字\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"的语言模型，名字\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"叫 **\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"叫 **\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"DeepSeek-R\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"DeepSeek-R\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"1**\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"1**\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"。你可以把我当作\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"。你可以把我当作\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"一个知识丰富、\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"一个知识丰富、\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"乐于助\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"乐于助\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"人的小伙伴～\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"人的小伙伴～\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\\n\\n我可以帮你查\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\\n\\n我可以帮你查\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"资料、\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"资料、\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"写文章\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"写文章\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"、解题、翻译\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"、解题、翻译\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"、聊天\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"、聊天\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"解闷……\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"解闷……\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"只要你有\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"只要\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"问题，\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"你有问题，\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"我都愿意\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"我都愿意\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"尽力回答\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"尽力回答\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"！如果你\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"！如果你\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"愿意\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"愿意\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"的话，也可以\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"的话，也可以\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"告诉我你是谁\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"告诉我你是谁\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"，这样我们就能\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"，这样我们就能\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"更好地交流\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"更好地交流\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"啦～\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"啦～\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\\n\\n那你呢？\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\\n\\n那你呢？\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"你又是谁\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"你又是谁\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"？可以\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"？可以\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"告诉我吗\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"告诉我吗\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"？\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"executing","nodeId":"LLM_T61i"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_T61i","nodeExecTime":"12936ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"executing","nodeId":"End_7w1V"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
[ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"开始","nodeType":"Start","nodeStatus":"success","nodeId":"Start_9SAz","nodeExecTime":"0ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"大模型1","nodeResult":"{\"result\":\"\",\"reasoningContent\":\"\"}","nodeType":"LLM","nodeStatus":"success","nodeId":"LLM_T61i","nodeExecTime":"12936ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null), ApplicationOutput.Thought(thought=null, actionType=null, response={"nodeName":"结束","nodeResult":"{\"result\":\"\"}","nodeType":"End","nodeStatus":"success","nodeId":"End_7w1V","nodeExecTime":"12913ms"}, actionName=null, action=null, actionInputStream=null, actionInput=null, observation=null)]
```

## curl

-   APP\_ID替换为实际的应用ID。
    
-   如需直接传入 API Key，请将$DASHSCOPE\_API\_KEY 替换为您的 API Key。
    
-   请指定Header中的 **X-DashScope-SSE** 为 **enable，**表示流式输出回复。
    
-   请在`parameters`对象中添加`has_thoughts`参数，表示是否返回思考过程，true：返回；false（默认值）：不返回。
    
-   请在`parameters`对象中添加`incremental_output`数，表示是否增量输出，true：增量输出；false（默认值）：非增量输出。
    

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--header 'X-DashScope-SSE: enable' \
--data '{
    "input": {
        "prompt": "你好"

    },
    "parameters":  {
        "has_thoughts":true,
        "incremental_output":true
    },
    "debug": {}
}'
```

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"嗯","action_type":"reasoning","response":"嗯","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"null","text":""},"usage":{"models":[{"input_tokens":31,"output_tokens":3,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"，","action_type":"reasoning","response":"，","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"null","text":""},"usage":{"models":[{"input_tokens":31,"output_tokens":4,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"用户","action_type":"reasoning","response":"用户","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"null","text":""},"usage":{"models":[{"input_tokens":31,"output_tokens":5,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}
......
id:320
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"","action_type":"reasoning","response":"","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"null","text":"问题"},"usage":{"models":[{"input_tokens":31,"output_tokens":322,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}

id:321
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"","action_type":"reasoning","response":"","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"null","text":"吗"},"usage":{"models":[{"input_tokens":31,"output_tokens":323,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}

id:322
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"","action_type":"reasoning","response":"","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"null","text":"？"},"usage":{"models":[{"input_tokens":31,"output_tokens":324,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}

id:323
event:result
:HTTP_STATUS/200
data:{"output":{"thoughts":[{"action":"reasoning","thought":"","action_type":"reasoning","response":"","action_name":"思考过程"}],"session_id":"ea188f5f795a485f8956e3af0212ba29","finish_reason":"stop","text":""},"usage":{"models":[{"input_tokens":31,"output_tokens":324,"model_id":"deepseek-r1"}]},"request_id":"b4b0b65f-4378-93b6-8ca2-7936b2725bc8"}
```

## **参数传递**

若需让同一个工作流适配不同业务场景，可在 API 调用时，通过`biz_params`传递自定义参数。

需在**开始节点**添加自定义参数（如城市名`city`），并在**提示词**中引用变量`city`和`query`，最后**发布**应用。

## Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application
# 工作流和智能体编排应用自定义参数传递
biz_params = {"city": "杭州"}
response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',  # 替换为实际的应用 ID
    prompt='查询这个城市的行政区域划分',
    biz_params=biz_params  # 传递业务参数
)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print(f'{response.output.text}')  # 处理只输出文本text
```

**响应示例**

```
杭州市，作为浙江省的省会城市，其行政区域划分包括10个市辖区：上城区、拱墅区、西湖区、滨江区、萧山区、余杭区、临平区、钱塘区、富阳区、临安区。每个区都有其独特的特色和发展重点。

- 上城区：位于杭州市中心地带，是杭州的政治、经济、文化中心之一。
- 拱墅区：以运河文化为特色，拥有众多历史文化遗产。
- 西湖区：著名的西湖风景区就位于此区，是旅游观光的重要目的地。
- 滨江区：高新技术产业聚集地，阿里巴巴等知名企业坐落于此。
- 萧山区：东南部的一个行政区，经济发展迅速，特别是制造业方面。
- 余杭区：近年来发展快速，尤其是互联网经济领域，阿里巴巴总部也设在这里（注：阿里巴巴总部实际位于滨江区）。
- 临平区：新成立的行政区，旨在促进该地区经济社会全面发展。
- 钱塘区：同样是一个较新的行政区划调整结果，强调创新发展和生态保护相结合。
- 富阳区：位于杭州西南方向，以其丰富的自然景观和悠久的历史文化著称。
- 临安区：地处杭州西部，以生态优美闻名，并且有着深厚的文化底蕴。

请注意，随着时间推移，具体的城市规划可能会有所变化，请参考最新的官方信息。
```

## Java

**请求示例**

```
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import io.reactivex.Flowable;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {

        String bizParams =
                "{\"city\":\"杭州\"}";
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("APP_ID")
                .prompt("查询这个城市的行政区域划分")
                .bizParams(JsonUtils.parse(bizParams))
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf("%s\n",
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf("Exception: %s", e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

**响应示例**

```
杭州市是浙江省的省会城市，其行政区域划分主要包括10个市辖区：上城区、拱墅区、西湖区、滨江区、萧山区、余杭区、临平区、钱塘区、富阳区、临安区。每个区都有自己的特色和发展重点。

- 上城区：位于杭州市中心，拥有许多历史文化遗产。
- 拱墅区：以大运河文化而闻名，同时也是一个重要的商业和居住区。
- 西湖区：以其美丽的自然风光著称，包括著名的西湖风景区。
- 滨江区：高新技术产业集聚地，杭州国家高新技术产业开发区就设在这里。
- 萧山区：经济发展迅速，尤其在制造业方面表现突出。
- 余杭区：近年来随着阿里巴巴等高科技企业的发展而快速崛起。
- 临平区：2021年由原余杭区部分区域调整而来，注重生态建设和科技创新。
- 钱塘区：同样是在2021年成立的新区，定位为杭州东部交通枢纽及产业发展新高地。
- 富阳区：历史悠久的文化名城，也是造纸业的重要基地之一。
- 临安区：位于杭州西部，森林覆盖率高，生态环境良好。

这些区域共同构成了杭州市独特的地理格局和社会经济结构。如果你对某个特定区域感兴趣或需要更详细的信息，请告诉我！
```

## HTTP

## curl

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "查询这个城市的行政区域划分",
        "biz_params": {
        "city": "杭州"}
    },
    "parameters":  {}
}'
```

> APP\_ID替换为实际的应用 ID。

**响应示例**

```
{"output":{"finish_reason":"stop","session_id":"c211219896004b50a1f6f66f2ec5413e",
"text":"杭州市下辖10个区、1个县，代管2个县级市，分别为：
上城区、拱墅区、西湖区、滨江区、萧山区、余杭区、临平区、钱塘区、富阳区、临安区、桐庐县、淳安县、建德市、诸暨市。
注意，诸暨市由浙江省直辖、杭州市与绍兴市共同管理。"},"usage":{},
"request_id":"02c3c9e1-7912-9505-91aa-248d04fb1f5d"}
```

## PHP

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'APP_ID'; // 替换为实际的应用 ID
$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '查询这个城市的行政区域划分',
        'biz_params' => [
            'city' => '杭州'
        ]
    ],
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die("JSON encoding failed with error: " . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die("cURL Error: " . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo "{$response_data['output']['text']}\n";
    } else {
        echo "No text in response.\n";
    }
} else {
    if (isset($response_data['request_id'])) {
        echo "request_id={$response_data['request_id']}\n";
    }
    echo "code={$status_code}\n";
    if (isset($response_data['message'])) {
        echo "message={$response_data['message']}\n";
    } else {
        echo "message=Unknown error\n";
    }
}
```

**响应示例**

```
杭州市是浙江省的省会城市，其行政区域划分主要包括10个市辖区：上城区、拱墅区、西湖区、滨江区、萧山区、余杭区、临平区、钱塘区、富阳区、临安区。

每个区都有自己的特色和发展重点，比如：
- **上城区**和**拱墅区**位于杭州市中心，商业繁华，历史悠久。
- **西湖区**以美丽的西湖而闻名，同时也是一个重要的科教文化区。
- **滨江区**则以其高新技术产业发展著称。
- **萧山区**、**余杭区**等则是近年来随着城市发展迅速崛起的新城区或经济开发区。
- **临安区**、**富阳区**等地则更多保留了自然风光与乡村风貌。

请注意，中国的行政区划可能会根据国家政策调整有所变化，请通过官方渠道获取最新信息。
```

## Node.js

**需安装相关依赖：**

```
npm install axios
```

**请求示例**

```
const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID'; // 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "查询这个城市的行政区域划分",
            biz_params: {
                'city': '杭州',
            },
        },
        parameters: {},
        debug: {},
    };

    try {
        console.log("Sending request to DashScope API...");

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            if (response.data.output && response.data.output.text) {
                console.log(`${response.data.output.text}`);
            }
        } else {
            console.log("Request failed:");
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response statusText: ${error.response.statusText}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
杭州市是浙江省的省会，其行政区域划分包括10个市辖区。具体如下：

1. 上城区（Shàngchéng Qū）：位于杭州市中心偏南，是杭州历史最悠久、文化底蕴最深厚的区域之一。
2. 拱墅区（Gǒngshù Qū）：原为下城区和拱墅区合并而成的新区，位于杭州市北部。
3. 西湖区（Xīhú Qū）：以世界文化遗产西湖而闻名，拥有丰富的自然与人文景观。
4. 滨江区（Bīnjiāng Qū）：地处钱塘江南岸，是一个高新技术产业集聚地。
5. 萧山区（Xiāoshān Qū）：位于杭州市东部，是中国重要的制造业基地之一。
6. 余杭区（Yúháng Qū）：曾经是中国四大名镇之一的临平所在地，现已成为杭州重要的经济发展区。
7. 富阳区（Fùyáng Qū）：位于杭州市西南部，因富春江穿流其间而得名。
8. 临安区（Lín'ān Qū）：位于杭州市西部山区，以其美丽的自然风光著称。
9. 钱塘区（Qiántáng Qū）：成立于2021年，由原大江东产业集聚区及部分萧山区组成，旨在促进杭州东部地区的发展。
10. 临平区（Lín Píng Qū）：从余杭区分设出来的一个新行政区划，主要涵盖原余杭区内的临平街道等地。

以上信息反映了截至我最后更新时的情况，请注意行政区划可能会有所调整，请以官方发布的最新消息为准。
```

## C#

**请求示例**

```
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。 
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
        string appId = "APP_ID"; // 替换为实际的应用ID
        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""查询这个城市的行政区域划分"",
                    ""biz_params"":{
                        ""city"":""杭州""
                    }
                },
                ""parameters"": {},
                ""debug"": {}
            }";

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Request successful:");
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error calling DashScope: {ex.Message}");
            }
        }
    }
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "7a9ff57eec7d475fa5d487de5f5178d2",
        "text": "杭州市是浙江省的省会，它下辖有10个市辖区：上城区、拱墅区、西湖区、滨江区、萧山区、余杭区、临平区、钱塘区、富阳区和临安区。每个区都有其独特的地理位置和发展特色。例如，西湖区以美丽的自然风光著称，尤其是著名的杭州西湖就位于此；而滨江区则更多地以其高新技术产业发展闻名。此外，随着城市的发展，行政区划也可能会有所调整，请关注官方发布的最新信息。"
    },
    "usage": {

    },
    "request_id": "d2c2fcc9-f821-98c9-9430-8704a2a41225"
}
```

## Go

**请求示例**

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]interface{}{
			"prompt": "查询这个城市的行政区域划分",
			"biz_params": map[string]interface{}{
				"city": "杭州",
			},
		},
		"parameters": map[string]interface{}{},
		"debug":      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Failed to marshal JSON: %v\n", err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Failed to create request: %v\n", err)
		return
	}

	// 设置请求头
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read response: %v\n", err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println("Request successful:")
		fmt.Println(string(body))
	} else {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		fmt.Println(string(body))
	}
}
```

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "2dc3e1a9dcd248c6bb9ca92bffc3e745",
        "text": "杭州市，简称“杭”，是浙江省的省会城市。根据最新的行政区划调整，杭州市现辖10个市辖区、2个县级市和1个县，具体如下：

- 市辖区（10个）：上城区、拱墅区、西湖区、滨江区、萧山区、余杭区、临平区、钱塘区、富阳区、临安区。
- 县级市（2个）：建德市、桐庐县（注意这里的桐庐实际上被列为县级市处理，但准确地说它是一个县）。
- 县（1个）：淳安县。

请注意，随着时间的变化，行政区域可能会有所调整，请以官方最新发布的消息为准。上述信息基于较新的资料整理而来，对于最新的变动情况，建议访问政府官方网站获取最准确的信息。"
    },
    "usage": {

    },
    "request_id": "d3c8f368-b645-9446-bfe4-20ca51821a02"
}
```

## **文件问答**

在应用内上传文件，大模型可对文件内容进行问答。也可配置文件解析节点，使工作流能够接收并解析各类文件（如 文档、图片、视频、音频），提取内容用于后续的分析、总结或问答。

1.  **构建支持文件问答的工作流**
    
    1.  **配置开始节点**：在**开始**节点中，添加一个自定义参数，用于接收文件 URL。例如：将其命名为 `file_url`，类型选择 `File`（多文件可选择`Array[File]`）。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8577255671/p1032582.png)
        
    2.  **（可选）添加解析节点**：添加一个合适的文件解析节点，并将`file_url`作为该节点的输入变量。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8577255671/p1032583.png)
        
    3.  **配置大模型节点：**
        
        -   **引用解析输出变量**：如果配置了解析节点，可将其文本输出变量（如 `markdownContent`、`ASRInfo`等）添加到后续节点（如**大模型节点**）中，以便对文件内容进行处理。
            
        -   **引用自定义变量：**在**大模型节点**的**提示词**中引用**开始节点**的自定义变量并填写提示词。
            
    4.  **发布应用**：检查节点配置，测试无误后，**发布**工作流应用。
        
    
    > **注意**：传入的文件 URL 必须是公网可直接访问的。
    
    > **相关文档**：[工作流应用节点说明](https://help.aliyun.com/zh/model-studio/workflow-application/)。
    
2.  **调用应用**
    
    您可以通过两种方式向应用提供文件进行解析：
    
    1.  **通过控制台测试**
        
        在应用详情页的**测试**窗，进入入参变量配置，为 `file_url` 参数上传**本地文件**或**粘贴文件 URL**，进行快速测试。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8577255671/p1032595.png)
        
    2.  **通过 API 调用**
        
        在 API 请求中，通过 `biz_params` 字段传递文件 URL。`biz_params` 中的键名必须与您在**开始**节点中设置的参数名（本例中为 `file_url`）完全一致。
        
        ## Python
        
        **请求示例**
        
        ```
        """
        阿里云百炼 Application SDK 调用示例（流式输出）
        """
        import os
        from http import HTTPStatus
        from dashscope import Application
        
        # 若没有配置环境变量，可替换为：api_key="sk-xxx"
        # 但不建议在生产环境中硬编码 API Key
        responses = Application.call(
            api_key=os.getenv("DASHSCOPE_API_KEY"), 
            app_id='APP_ID',  # 替换为实际的应用 ID
            prompt='一句话总结文件内容',
            stream=True,           # 流式输出
            incremental_output=True,  # 增量输出
            biz_params={
                # 单文件格式（控制台参数类型: File）
                # 参数名必须与控制台定义的参数名保持一致
                'file_url': {
                    "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3",  # 必填
                    # "name": "welcome.mp3",  # 控制台引用了则必填
                    # "type": "audio",        # 控制台引用了则必填，可选值：image/document/audio/video/custom
                    # "source": "localFile",  # 控制台引用了则必填
                    # "mimeType": "audio"     # 控制台引用了则必填，可选值：image/png 等
                }
                # 多文件格式（控制台参数类型: Array<File>）
                # 'file_url': [
                #     {"url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf", "name": "文件1.pdf"},
                #     {"url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf", "name": "文件2.pdf"}
                # ]
            } 
        )
        
        # 处理流式响应
        for response in responses:
            if response.status_code != HTTPStatus.OK:
                print(f'request_id={response.request_id}')
                print(f'code={response.status_code}')
                print(f'message={response.message}')
                print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
            else:
                if response.output.text:
                    print(response.output.text, end='')
        
        print()  # 换行
        ```
        
        **响应示例**
        
        ```
        该文件内容仅为一句欢迎语：“欢迎你使用阿里云。”
        ```
        
        ## Java
        
        **请求示例**
        
        ```
        import com.alibaba.dashscope.app.*;
        import com.alibaba.dashscope.exception.ApiException;
        import com.alibaba.dashscope.exception.InputRequiredException;
        import com.alibaba.dashscope.exception.NoApiKeyException;
        import io.reactivex.Flowable;
        import com.google.gson.JsonObject;
        
        public class Main {
        
            public static void main(String[] args) {
                try {
                    streamCall();
                } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                    System.err.println("code=" + e.getClass().getSimpleName());
                    System.err.println("message=" + e.getMessage());
                    System.err.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
                }
            }
        
            public static void streamCall() throws ApiException, NoApiKeyException, InputRequiredException {
                // 构建biz_params参数
                JsonObject bizParams = new JsonObject();
                JsonObject fileUrl = new JsonObject();
                fileUrl.addProperty("url", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3");
                bizParams.add("file_url", fileUrl);
        
                ApplicationParam param = ApplicationParam.builder()
                        // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .appId("APP_ID")  // 应用ID替换APP_ID
                        .prompt("一句话总结文件内容")
                        .incrementalOutput(true)  // 增量输出
                        .bizParams(bizParams)
                        .build();
        
                Application application = new Application();
                
                // 流式输出
                Flowable<ApplicationResult> result = application.streamCall(param);
                
                result.blockingForEach(data -> {
                    if (data.getOutput() != null && data.getOutput().getText() != null) {
                        System.out.print(data.getOutput().getText());
                    }
                });
                System.out.println();
            }
        }
        ```
        
        **响应示例**
        
        ```
        该文件内容仅为一句欢迎语："欢迎你使用阿里云。"
        ```
        
        ## HTTP
        
        ## curl
        
        **请求示例**
        
        ```
        #!/bin/bash
        # 若没有配置环境变量，可用百炼API Key将下行替换为：API_KEY="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        API_KEY="${DASHSCOPE_API_KEY}"
        
        curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion" \
          -H "Authorization: Bearer ${API_KEY}" \
          -H "Content-Type: application/json" \
          -H "X-DashScope-SSE: enable" \
          -d '{
            "input": {
              "prompt": "一句话总结文件内容",
              "biz_params": {
                "file_url": {
                  "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                }
              }
            },
            "parameters": {
              "incremental_output": true
            }
          }'
        ```
        
        **响应示例**
        
        ```
        id:1
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:2
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:3
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:4
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:5
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{"models":[{"input_tokens":39,"output_tokens":1,"model_id":"qwen-plus-latest"}]},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:6
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{"models":[{"input_tokens":39,"output_tokens":2,"model_id":"qwen-plus-latest"}]},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:7
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{"models":[{"input_tokens":39,"output_tokens":6,"model_id":"qwen-plus-latest"}]},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:8
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{"models":[{"input_tokens":39,"output_tokens":6,"model_id":"qwen-plus-latest"}]},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:9
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"null"},"usage":{"models":[{"input_tokens":39,"output_tokens":12,"model_id":"qwen-plus-latest"}]},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        
        id:10
        event:result
        :HTTP_STATUS/200
        data:{"output":{"session_id":"dd52a93f1a124d9e89f40315636ef232","finish_reason":"stop","text":"该文件内容仅为一句欢迎语：“欢迎你使用阿里云。”"},"usage":{"models":[{"input_tokens":39,"output_tokens":14,"model_id":"qwen-plus-latest"}]},"request_id":"f8d6803a-d5c3-4d1b-bcd2-c1f78759157b"}
        ```
        
        ## PHP
        
        **请求示例**
        
        ```
        <?php
        // 若没有配置环境变量，可用百炼API Key将下行替换为：$apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        $apiKey = getenv('DASHSCOPE_API_KEY');
        $appId = 'APP_ID';  // 应用ID替换APP_ID
        $apiUrl = "https://dashscope.aliyuncs.com/api/v1/apps/{$appId}/completion";
        
        $requestBody = [
            'input' => [
                'prompt' => '一句话总结文件内容',
                'biz_params' => [
                    'file_url' => [
                        'url' => 'https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3'
                    ]
                ]
            ],
            'parameters' => [
                'incremental_output' => true  // 增量输出
            ]
        ];
        
        $ch = curl_init();
        
        curl_setopt_array($ch, [
            CURLOPT_URL => $apiUrl,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($requestBody),
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $apiKey,
                'Content-Type: application/json',
                'X-DashScope-SSE: enable'  // 流式输出
            ],
            CURLOPT_RETURNTRANSFER => false,
            CURLOPT_WRITEFUNCTION => function($ch, $data) {
                $lines = explode("\n", $data);
                foreach ($lines as $line) {
                    $line = trim($line);
                    if (strpos($line, 'data:') === 0) {
                        $jsonStr = trim(substr($line, 5));
                        if ($jsonStr && $jsonStr !== '[DONE]') {
                            $json = json_decode($jsonStr, true);
                            if (isset($json['output']['text'])) {
                                echo $json['output']['text'];
                            }
                        }
                    }
                }
                return strlen($data);
            }
        ]);
        
        $result = curl_exec($ch);
        
        if (curl_errno($ch)) {
            echo "request_id=" . curl_getinfo($ch, CURLINFO_HEADER_OUT) . "\n";
            echo "code=" . curl_errno($ch) . "\n";
            echo "message=" . curl_error($ch) . "\n";
            echo "请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code\n";
        }
        
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpCode !== 200) {
            echo "code={$httpCode}\n";
            echo "请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code\n";
        }
        
        curl_close($ch);
        echo "\n";
        ?>
        ```
        
        **响应示例**
        
        ```
        该文件内容仅为一句欢迎语：“欢迎你使用阿里云。”
        ```
        
        ## Node.js
        
        **请求示例**
        
        ```
        import https from 'https';
        
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        const apiKey = process.env.DASHSCOPE_API_KEY;
        const appId = 'APP_ID';  // 应用ID替换APP_ID
        const apiUrl = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
        
        const requestBody = {
            input: {
                prompt: '一句话总结文件内容',
                biz_params: {
                    file_url: {
                        url: 'https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3'
                    }
                }
            },
            parameters: {
                incremental_output: true  // 增量输出
            }
        };
        
        if (!apiKey) {
            console.error('错误: 请设置环境变量 DASHSCOPE_API_KEY');
            process.exit(1);
        }
        
        const postData = JSON.stringify(requestBody);
        const urlObj = new URL(apiUrl);
        const options = {
            hostname: urlObj.hostname,
            port: 443,
            path: urlObj.pathname,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable',  // 流式输出
                'Content-Length': Buffer.byteLength(postData)
            }
        };
        
        const req = https.request(options, (res) => {
            res.setEncoding('utf8');
            let buffer = '';
            
            res.on('data', (chunk) => {
                buffer += chunk;
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                
                for (const line of lines) {
                    const trimmedLine = line.trim();
                    if (trimmedLine.startsWith('data:')) {
                        const jsonStr = trimmedLine.substring(5).trim();
                        if (jsonStr && jsonStr !== '[DONE]') {
                            try {
                                const json = JSON.parse(jsonStr);
                                if (json.output && json.output.text) {
                                    process.stdout.write(json.output.text);
                                }
                            } catch (e) { }
                        }
                    }
                }
            });
        
            res.on('end', () => {
                if (buffer) {
                    const trimmedLine = buffer.trim();
                    if (trimmedLine.startsWith('data:')) {
                        const jsonStr = trimmedLine.substring(5).trim();
                        if (jsonStr && jsonStr !== '[DONE]') {
                            try {
                                const json = JSON.parse(jsonStr);
                                if (json.output && json.output.text) {
                                    process.stdout.write(json.output.text);
                                }
                            } catch (e) { }
                        }
                    }
                }
                console.log();
            });
        
            if (res.statusCode !== 200) {
                console.error(`code=${res.statusCode}`);
                console.error('请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code');
            }
        });
        
        req.on('error', (e) => {
            console.error(`code=${e.code}`);
            console.error(`message=${e.message}`);
            console.error('请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code');
        });
        
        req.write(postData);
        req.end();
        ```
        
        **响应示例**
        
        ```
        该文件内容仅为一句欢迎语："欢迎你使用阿里云。"
        ```
        
        ## C#
        
        **请求示例**
        
        ```
        using System;
        using System.Net.Http;
        using System.Text;
        using System.Text.Json;
        using System.Threading.Tasks;
        
        class Program
        {
            // 应用ID替换APP_ID
            private static readonly string AppId = "APP_ID";
            private static readonly string ApiUrl = $"https://dashscope.aliyuncs.com/api/v1/apps/{AppId}/completion";
            
            static async Task Main(string[] args)
            {
                // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey = "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
                if (string.IsNullOrEmpty(apiKey))
                {
                    Console.WriteLine("错误: 请设置环境变量 DASHSCOPE_API_KEY");
                    return;
                }
                await StreamCallAsync(apiKey);
            }
        
            static async Task StreamCallAsync(string apiKey)
            {
                var requestBody = new
                {
                    input = new
                    {
                        prompt = "一句话总结文件内容",
                        biz_params = new
                        {
                            file_url = new
                            {
                                url = "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                            }
                        }
                    },
                    parameters = new
                    {
                        incremental_output = true  // 增量输出
                    }
                };
        
                string jsonBody = JsonSerializer.Serialize(requestBody);
        
                using var client = new HttpClient();
                client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
                client.DefaultRequestHeaders.Add("X-DashScope-SSE", "enable");  // 流式输出
        
                var content = new StringContent(jsonBody, Encoding.UTF8, "application/json");
        
                try
                {
                    var response = await client.PostAsync(ApiUrl, content);
                    
                    if (!response.IsSuccessStatusCode)
                    {
                        Console.WriteLine($"code={(int)response.StatusCode}");
                        Console.WriteLine($"message={await response.Content.ReadAsStringAsync()}");
                        Console.WriteLine("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
                        return;
                    }
        
                    using var stream = await response.Content.ReadAsStreamAsync();
                    using var reader = new System.IO.StreamReader(stream);
                    
                    string? line;
                    while ((line = await reader.ReadLineAsync()) != null)
                    {
                        if (line.StartsWith("data:"))
                        {
                            string jsonStr = line.Substring(5).Trim();
                            if (!string.IsNullOrEmpty(jsonStr) && jsonStr != "[DONE]")
                            {
                                try
                                {
                                    using var doc = JsonDocument.Parse(jsonStr);
                                    if (doc.RootElement.TryGetProperty("output", out var output) &&
                                        output.TryGetProperty("text", out var text))
                                    {
                                        Console.Write(text.GetString());
                                    }
                                }
                                catch (JsonException) { }
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"code=Exception");
                    Console.WriteLine($"message={ex.Message}");
                    Console.WriteLine("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
                }
                Console.WriteLine();
            }
        }
        ```
        
        **响应示例**
        
        ```
        该文件内容仅为一句欢迎语："欢迎你使用阿里云。"
        ```
        
        ## Go
        
        **请求示例**
        
        ```
        package main
        
        import (
        	"bufio"
        	"bytes"
        	"encoding/json"
        	"fmt"
        	"net/http"
        	"os"
        	"strings"
        )
        
        const appId = "APP_ID" // 应用ID替换APP_ID
        
        type RequestBody struct {
        	Input      Input      `json:"input"`
        	Parameters Parameters `json:"parameters"`
        }
        
        type Input struct {
        	Prompt    string    `json:"prompt"`
        	BizParams BizParams `json:"biz_params"`
        }
        
        type BizParams struct {
        	FileUrl FileUrl `json:"file_url"`
        }
        
        type FileUrl struct {
        	URL string `json:"url"`
        }
        
        type Parameters struct {
        	IncrementalOutput bool `json:"incremental_output"` // 增量输出
        }
        
        type ResponseBody struct {
        	Output struct {
        		Text string `json:"text"`
        	} `json:"output"`
        	RequestID string `json:"request_id"`
        }
        
        func main() {
        	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        	apiKey := os.Getenv("DASHSCOPE_API_KEY")
        	if apiKey == "" {
        		fmt.Println("错误: 请设置环境变量 DASHSCOPE_API_KEY")
        		os.Exit(1)
        	}
        
        	apiUrl := "https://dashscope.aliyuncs.com/api/v1/apps/" + appId + "/completion"
        
        	requestBody := RequestBody{
        		Input: Input{
        			Prompt: "一句话总结文件内容",
        			BizParams: BizParams{
        				FileUrl: FileUrl{
        					URL: "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3",
        				},
        			},
        		},
        		Parameters: Parameters{
        			IncrementalOutput: true,
        		},
        	}
        
        	jsonData, err := json.Marshal(requestBody)
        	if err != nil {
        		fmt.Printf("code=JSONError\nmessage=%v\n", err)
        		os.Exit(1)
        	}
        
        	req, err := http.NewRequest("POST", apiUrl, bytes.NewBuffer(jsonData))
        	if err != nil {
        		fmt.Printf("code=RequestError\nmessage=%v\n", err)
        		os.Exit(1)
        	}
        
        	req.Header.Set("Authorization", "Bearer "+apiKey)
        	req.Header.Set("Content-Type", "application/json")
        	req.Header.Set("X-DashScope-SSE", "enable") // 流式输出
        
        	client := &http.Client{}
        	resp, err := client.Do(req)
        	if err != nil {
        		fmt.Printf("code=NetworkError\nmessage=%v\n", err)
        		fmt.Println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        		os.Exit(1)
        	}
        	defer resp.Body.Close()
        
        	if resp.StatusCode != http.StatusOK {
        		fmt.Printf("code=%d\n", resp.StatusCode)
        		fmt.Println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        	}
        
        	scanner := bufio.NewScanner(resp.Body)
        	for scanner.Scan() {
        		line := scanner.Text()
        		if strings.HasPrefix(line, "data:") {
        			jsonStr := strings.TrimSpace(strings.TrimPrefix(line, "data:"))
        			if jsonStr != "" && jsonStr != "[DONE]" {
        				var response ResponseBody
        				if err := json.Unmarshal([]byte(jsonStr), &response); err == nil {
        					if response.Output.Text != "" {
        						fmt.Print(response.Output.Text)
        					}
        				}
        			}
        		}
        	}
        
        	if err := scanner.Err(); err != nil {
        		fmt.Printf("\ncode=ReadError\nmessage=%v\n", err)
        		fmt.Println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        	}
        	fmt.Println()
        }
        ```
        
        **响应示例**
        
        ```
        该文件内容仅为一句欢迎语："欢迎你使用阿里云。"
        ```
        

## **私网调用**

为提高数据传输的安全性和效率，您可通过私网调用阿里云百炼平台的应用。

1.  [创建终端节点](https://help.aliyun.com/zh/model-studio/access-model-studio-through-privatelink#b49f50b6202nn)：在阿里云控制台为您的VPC创建一个私网终端节点。
    
2.  **替换域名**：将API请求URL中的公网域名`dashscope.aliyuncs.com`替换为您获取到的私网终端节点服务域名。例如：
    
    `https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/`
    
3.  发起请求：示例代码如下。
    
    ### Python
    
    ```
    import os
    from http import HTTPStatus
    from dashscope import Application
    # 配置私网终端节点
    os.environ['DASHSCOPE_HTTP_BASE_URL'] = 'https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/'
    response = Application.call(
        # 若没有配置环境变量，可用阿里云百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='APP_ID',# 替换为实际的应用 ID
        prompt='你是谁？')
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print(response.output.text)
    ```
    
    ### Java
    
    ```
    // 建议dashscope SDK的版本 >= 2.12.0
    import com.alibaba.dashscope.app.*;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    
    public class Main {
        public static void appCall()
                throws ApiException, NoApiKeyException, InputRequiredException {
            ApplicationParam param = ApplicationParam.builder()
                    // 若没有配置环境变量，可用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .appId("APP_ID")
                    .prompt("你是谁？")
                    .build(); 
            // 配置私网终端节点
            Application application = new Application("https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/");
            ApplicationResult result = application.call(param);
    
            System.out.printf("text: %s\n",
                    result.getOutput().getText());
        }
    
        public static void main(String[] args) {
            try {
                appCall();
            } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                System.err.println("message："+e.getMessage());
                System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
            }
            System.exit(0);
        }
    }
    ```
    
    ### HTTP
    
    这里给出curl代码示例。
    
    ```
    curl -X POST https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/apps/APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {
            "prompt": "你是谁？"
        },
        "parameters":  {},
        "debug": {}
    }'
    ```
    
    > `APP_ID`替换为实际的应用ID。
    

## API 参考

应用调用的完整参数列表，请参考[工作流与旧版智能体应用 API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference) 。

## **错误码**

如果调用失败并返回报错信息，请参阅[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **计费说明**

工作流应用的计费基于其内部实际执行的**计费节点**（如大模型、知识库等）的调用量。

-   **计费单元**：每个计费节点都有其独立的计费单位（例如，大模型节点按 Token 计费）。
    
-   **总费用**：一次工作流 API 调用的总费用，是该次执行路径上**所有计费节点产生的费用之和**。
    

## **相关文档**

**了解应用构建和使用**

如果你想了解工作流应用的更多配置信息，如节点说明、工作流的导入导出等，请参见[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)。

**了解Prompt 辅助工具**

关于应用内 Prompt 辅助工具的使用请参阅[Prompt工程](https://help.aliyun.com/zh/model-studio/use-prompt-engineering-to-communicate-with-large-models)。

**了解文本转语音的方法**

如需将模型回复的文本信息转成语音，请参见[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**了解进阶用法**

如果您想使用 Responses API 调用应用，请参见[Responses API](https://help.aliyun.com/zh/model-studio/openai-responses-api/)。

## 常见问题

**1.为什么我的工作流在控制台测试正常，但通过API调用时报错或结果不符合预期？**

通常由版本或参数不一致导致。请主要检查以下几点：

-   **确认应用已发布**：API 调用的是您**最后一次发布**的工作流版本。任何在控制台保存但未发布的修改，都不会在 API 调用中生效。请确保您的修改已点击“发布”。
    
-   **检查自定义参数 (**`**biz_params**`**)**：API 请求中 `biz_params` 的`键名`和`数据类型`必须与工作流**开始节点**中定义的参数完全一致。例如，如果在开始节点定义了名为 `city` 的字符串参数，API 调用时就必须传递 `{"city": "some_value"}`。
    
-   **检查输入内容**：确认 API 调用的 `prompt` 或 `messages` 内容与您在控制台测试时输入的内容和格式保持一致，特别是当提示词中有特定格式要求时。
    

**2.运行Java代码示例时，如果出现类似“java: 程序包com.alibaba.dashscope.app不存在”的异常信息，应该怎么处理？**

1.  检查导入语句中的类名和包名是否正确。
    
2.  添加依赖库：如果使用Maven或Gradle进行项目管理，确保DashScope Java SDK依赖库已经添加到`pom.xml`或`build.gradle`文件中，且为最新版本。您可以访问[Maven](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)获取DashScope Java SDK的最新版本号。
    
    XML
    
    ```
    <!-- https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <version>在此处填写最新版本号，例如2.16.4</version>
    </dependency>
    ```
    
    Gradle
    
    ```
    // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: '在此处填写最新版本号，例如2.16.4'
    ```
    
3.  升级SDK：旧版本的DashScope Java SDK可能不包含您尝试使用的功能或类。如果您已经添加过依赖库DashScope Java SDK，请确认您所使用的DashScope Java SDK是否为最新版。如果当前版本较低，请将其升级至最新版本。在`pom.xml`或`build.gradle`文件中修改DashScope Java SDK的版本为最新版本。
    
    XML
    
    ```
    <!-- https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <version>请将此处的版本号修改为最新版本</version>
    </dependency>
    ```
    
    Gradle
    
    ```
    // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: '请将此处的版本号修改为最新版本'
    ```
    
4.  重新加载项目使更改生效。
    
5.  重新运行代码示例。

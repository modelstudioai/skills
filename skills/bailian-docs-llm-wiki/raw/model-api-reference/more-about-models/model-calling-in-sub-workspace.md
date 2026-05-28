# 子业务空间的模型调用

本文以千问-Plus为例，引导您通过API调用子业务空间（即非默认业务空间）中的模型。

## **适用场景**

-   **需要管控某类用户可调用的模型：**默认业务空间的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)可调用所有模型（权限过大）。如需管控[RAM用户](https://help.aliyun.com/zh/model-studio/permission-management-overview#d41e21)可调用的模型，可将其添加至某个子业务空间，仅授权必要模型，并要求使用该空间的 API Key 调用。
    
-   **需要对模型调用的费用进行分账：**当默认业务空间包含多个业务或场景时，往往难以区分各自的模型调用费用。通过为每个业务或场景创建独立的子业务空间，每个空间可独立[生成账单](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)，便于对调用费用进行分账。
    

## **准备工作**

1.  **获取子业务空间的API Key：**在子业务空间中[创建API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)（变量名使用`DASHSCOPE_API_KEY`），用于调用大模型API。
    
2.  **获取模型调用权限（调用标准模型需要）：**使用子业务空间的API Key调用[标准模型](https://help.aliyun.com/zh/model-studio/models)（例如`qwen-plus`）前，需为该空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)。
    
    > **注意：**调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**，但此类模型仅能由其所在业务空间的 API Key 调用。
    
3.  **选择开发语言：**[选择您熟悉的语言和SDK](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#81e0419728kdd)，用于调用大模型API。
    

## **开始调用**

### **OpenAI 兼容**

在线调试

##### OpenAI 兼容接口在线调试 ×

 中国大陆（北京） 国际（新加坡）

POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions

API Key Bearer Token [获取中国大陆（北京）地域 API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)

请求体

{ "model": "qwen-plus", "messages": \[ { "role": "system", "content": "You are a helpful assistant." }, { "role": "user", "content": "你是谁？" } \], "stream": true, "stream\_options": { "include\_usage": true }, "top\_p": 0.8, "temperature": 0.7, "enable\_thinking": true }

发送请求 清空响应

响应结果

原始响应 解析内容

## 北京地域

SDK 调用配置的`base_url`：`https://dashscope.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

## 新加坡地域

SDK 调用配置的`base_url`：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

以文本输入为例，通过 OpenAI 兼容方式调用子业务空间的`qwen-plus`标准模型。与默认业务空间的模型调用的区别在于：**必须使用该子业务空间的 API Key**。

> 调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)后的模型：仅支持通过[DashScope](#32a12dae0d6ze)调用，不支持通过OpenAI兼容方式调用。

## Python（SDK）

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/model-studio/getting-started/models
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ]
)
print(completion.model_dump_json())
```

## Java（SDK）

```
// 该代码 OpenAI SDK 版本为 2.6.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .addUserMessage("你是谁")
                .model("qwen-plus")
                .build();

        try {
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            System.out.println(chatCompletion);
        } catch (Exception e) {
            System.err.println("Error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

## Node.js（SDK）

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",  //此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "你是谁？" }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
```

## Go（SDK）

```
package main

import (
	"context"
	"os"

	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
)

func main() {
	client := openai.NewClient(
		option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
		option.WithBaseURL("https://dashscope.aliyuncs.com/compatible-mode/v1"),
	)
	chatCompletion, err := client.Chat.Completions.New(
		context.TODO(), openai.ChatCompletionNewParams{
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.UserMessage("你是谁"),
			},
			Model: "qwen-plus",
		},
	)

	if err != nil {
		panic(err.Error())
	}

	println(chatCompletion.Choices[0].Message.Content)
}
```

## C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }

        // 设置请求 URL 和内容
        string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
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

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
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

## PHP（HTTP）

```
<?php
// 设置请求的URL
$url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
// 若没有配置环境变量，请用百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
    "model" => "qwen-plus",
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
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
echo $response;
?>
```

## curl（HTTP）

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
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

### **DashScope**

## 北京地域

HTTP 请求地址：

-   千问大语言模型：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
    
-   千问VL/Audio模型：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
    

SDK 调用无需配置 `base_url`。

## 新加坡地域

HTTP 请求地址：

-   千问大语言模型：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
    
-   千问VL/OCR模型：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
    

SDK调用配置的`base_url`：

## **Python代码**

```
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
```

## **Java代码**

-   **方式一：**
    
    ```
    import com.alibaba.dashscope.protocol.Protocol;
    Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope-intl.aliyuncs.com/api/v1");
    ```
    
-   **方式二：**
    
    ```
    import com.alibaba.dashscope.utils.Constants;
    Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";
    ```
    

以文本输入为例，通过 DashScope 方式调用子业务空间的`qwen-plus`标准模型。与默认业务空间的模型调用的区别在于：**必须使用该子业务空间的 API Key**。

## Python（SDK）

```
import os
import dashscope

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': '你是谁？'}
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
    messages=messages,
    result_format='message'
    )
print(response)
```

## Java（SDK）

```
// 建议dashscope SDK的版本 >= 2.12.0
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
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```

## PHP（HTTP）

```
<?php

$url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
$apiKey = getenv('DASHSCOPE_API_KEY');

$data = [
    // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
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
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $apiKey",
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 200) {
    echo "Response: " . $response;
} else {
    echo "Error: " . $httpCode . " - " . $response;
}

curl_close($ch);
?>
```

## Node.js（HTTP）

DashScope 未提供 Node.js 环境的 SDK。如需通过 OpenAI Node.js SDK调用，请参考本文的[OpenAI 兼容](#d397bcc41eu3q)章节。

```
import fetch from 'node-fetch';

const apiKey = process.env.DASHSCOPE_API_KEY;

const data = {
    model: "qwen-plus", // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
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

fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
    console.log(JSON.stringify(data));
})
.catch(error => {
    console.error('Error:', error);
});
```

## C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }

        // 设置请求 URL 和内容
        string url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
        // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
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

        // 输出结果
        Console.WriteLine(result);
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

## Go（HTTP）

DashScope 未提供 Go 的 SDK。如需通过 OpenAI Go SDK调用，请参考本文的[OpenAI 兼容](#d397bcc41eu3q)章节。

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

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type Input struct {
	Messages []Message `json:"messages"`
}

type Parameters struct {
	ResultFormat string `json:"result_format"`
}

type RequestBody struct {
	Model      string     `json:"model"`
	Input      Input      `json:"input"`
	Parameters Parameters `json:"parameters"`
}

func main() {
	// 创建 HTTP 客户端
	client := &http.Client{}

	// 构建请求体
	requestBody := RequestBody{
		// 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
		Model: "qwen-plus",
		Input: Input{
			Messages: []Message{
				{
					Role:    "system",
					Content: "You are a helpful assistant.",
				},
				{
					Role:    "user",
					Content: "你是谁？",
				},
			},
		},
		Parameters: Parameters{
			ResultFormat: "message",
		},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatal(err)
	}

	// 创建 POST 请求
	req, err := http.NewRequest("POST", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(err)
	}

	// 设置请求头
	// 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey := "sk-xxx"
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
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	// 打印响应内容
	fmt.Printf("%s\n", bodyText)
}
```

## curl（HTTP）

```
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
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

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **下一步**

**查看更多模型**

示例代码以`qwen-plus`模型为例，阿里云百炼还支持其他千问模型及 DeepSeek 等第三方模型，**支持的模型**以及对应的**API参考**文档请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。

**了解进阶用法**

示例代码仅完成了简单问答，如果您想了解千问 API 的更多用法，如[流式输出](https://help.aliyun.com/zh/model-studio/stream)、[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)、[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)等，请参见[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation)。

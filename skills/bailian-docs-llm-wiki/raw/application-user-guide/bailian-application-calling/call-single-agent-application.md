# 调用智能体应用

可通过 DashScope SDK（阿里云模型服务的统一API）或 HTTP 请求方式，将阿里云百炼的智能体应用集成至业务系统。

## **前提条件**

在开始之前，请完成以下三个步骤以配置您的开发环境。

1.  **获取凭证**
    
    -   API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)页面，创建并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
        
    -   阿里云百炼应用ID：前往[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面创建[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)，并在应用卡片上复制其APP\_ID。
        
2.  **安装DashScope SDK**
    
    > HTTP接口调用跳过此步骤。
    
    请根据您使用的编程语言选择并执行相应的安装命令。
    
    ## Python
    
    运行以下命令安装或升级DashScope Python SDK：
    
    ```
    # 使用此命令，将SDK安装到您的Python 3环境中
    python3 -m pip install -U dashscope
    ```
    
    ## Java
    
    执行以下命令来添加 Java SDK 依赖，并将 `the-latest-version` 替换为最新的版本号。最新版本号详情请访问[DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)。
    
    ## XML
    
    执行以下命令来添加 Java SDK 依赖。
    
    1\. 添加依赖
    
    在 `pom.xml` 文件的 `<dependencies>` 部分添加以下内容：
    
    ```
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <!-- 请将 'the-latest-version' 替换为最新版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
        <version>the-latest-version</version>
    </dependency>
    ```
    
    2\. 更新项目
    
    保存 `pom.xml` 文件。您的IDE（如IntelliJ IDEA, Eclipse）通常会自动检测到变更并提示您重新加载Maven依赖。
    
    如果没有自动提示，您可以：
    
    -   在IDE中手动执行 "Reload/Update Maven Project" 操作。
        
    -   或在项目根目录下通过命令行执行：`mvn clean install`。
        
    
    ## Gradle
    
    1.  添加依赖
        
        在您的 `build.gradle`文件的 `dependencies` 代码块中，添加以下依赖：
        
        ```
        dependencies {
            // 请将 'the-latest-version' 替换为最新版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
            implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
        }
        ```
        
    
    2.  同步项目
        
        保存 `build.gradle` 文件。您的IDE（如IntelliJ IDEA）通常会显示一个图标，点击即可同步Gradle项目。
        
        或者，您可以在项目根目录下通过命令行强制刷新依赖：
        
        ```
        ./gradlew build --refresh-dependencies
        ```
        
    
3.  **配置环境变量（推荐）**
    
    为保障密钥安全并避免在代码中硬编码，建议[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/get-api-key)。SDK将自动从此变量读取。
    

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
    app_id='YOUR_APP_ID',# 替换为实际的应用 ID
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
我是阿里云开发的一款超大规模语言模型，我叫通义千问。我被设计用来帮助用户生成各种类型的文本，如文章、故事、诗歌、故事等，并能根据不同的场景和需求进行调整和优化。此外，我还能够回答各种问题，提供信息和解释，辅助学习和研究。如果您有任何需要，欢迎随时向我提问！
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
                .appId("YOUR_APP_ID")
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
text: 我是阿里云开发的一款超大规模语言模型，我叫通义千问。
```

### HTTP

#### curl

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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

> YOUR\_APP\_ID替换为实际的应用 ID。

**响应示例**

```
{"output":{"finish_reason":"stop",
"session_id":"232ea2e9e6ef448db6b14465c06a9a56",
"text":"我是来自阿里云的超大规模语言模型，我叫通义千问。我是一个能够回答问题、创作文字，还能表达观点、撰写代码的AI助手。如果您有任何问题或需要帮助，请随时告诉我，我会尽力为您提供帮助。"},
"usage":{"models":[{"output_tokens":51,"model_id":"qwen-max","input_tokens":121}]},
"request_id":"661c9cad-e59c-9f78-a262-78eff243f151"}%
```

#### PHP

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID

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
我是来自阿里云的超大规模语言模型，我叫通义千问。
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
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID

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
我是来自阿里云的大规模语言模型，我叫通义千问。
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
        string appId = "YOUR_APP_ID"; // 替换为实际的应用ID

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
        "text": "我是阿里云开发的一款超大规模语言模型，我叫通义千问。我被设计用来帮助用户生成各种类型的文本，如文章、故事、诗歌、故事等，并能根据不同的场景和需求进行变换和创新。此外，我还能够回答各种问题，提供信息和解释，帮助用户解决问题和获取知识。如果你有任何问题或需要帮助，请随时告诉我！"
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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

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
        "text": "我是通义千问，由阿里云开发的AI助手。我被设计用来回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？"
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

## **核心功能**

### **多轮对话**

相比于单轮对话，多轮对话可以让大模型参考历史对话信息，更符合日常交流的场景。

**云端存储**

**自行管理**

通过传入 `session_id`，系统会自动从云端加载存储的对话历史，并结合新的指令生成上下文。

需要维护一个 `messages` 数组，手动记录和传递每一轮的对话历史及新指令。

必传参数

-   `session_id`：会话ID。
    
-   `prompt`：提示词。
    

必传参数：`messages` 数组

可选参数：`prompt`（可选）

-   若传入`prompt`，`prompt` 会被转换为一条 `{"role": "user", "content": "prompt"}`，自动追加到 `messages` 末尾，生成最终上下文。
    
-   示例：
    
    ```
    // 原始传入
    {
      "messages": [{"role": "user", "content": "你好"}], 
      "prompt": "推荐一部电影"
    }
    // 实际生效的messages
    [
      {"role": "user", "content": "你好"}, 
      {"role": "user", "content": "推荐一部电影"}
    ]
    ```
    

**优先级规则：**若同时传入 `session_id` 和 `messages`，则优先使用 `messages`，忽略 `session_id`。

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
        app_id='YOUR_APP_ID',  # 替换为实际的应用 ID
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
                app_id='YOUR_APP_ID',  # 替换为实际的应用 ID
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
                .appId("YOUR_APP_ID")
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
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID

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
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID

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
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID

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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
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
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID

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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
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
        string appId = "YOUR_APP_ID"; // 替换为实际的应用ID

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
        string appId = "YOUR_APP_ID"; // 替换为实际的应用ID

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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

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

> YOUR\_APP\_ID替换为实际的应用 ID。下一轮对话的输入参数`session_id`字段值替换为实际上一轮对话返回的session\_id值。

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
    app_id='YOUR_APP_ID',  # 替换为实际的应用 ID
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
                .appId("YOUR_APP_ID")
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
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID

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
    const appId = 'YOUR_APP_ID';//替换为实际的应用 ID

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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
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
        string appId = "YOUR_APP_ID";// 替换为实际的应用ID
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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

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

### **流式输出**

大模型接收输入后，逐步生成中间结果并实时输出。这种方式称为流式输出，在模型生成过程中即时查看内容，减少等待时间。

**流式输出的实现方式**

根据调用方式的不同，设置相应参数即可启用流式输出：

-   Python SDK方式：设置`stream`参数为`True`。
    
-   Java SDK方式：使用`streamCall`方法。
    
-   HTTP方式：在`Header`中指定`X-DashScope-SSE`为`enable`。
    

流式输出的内容默认是非增量式（即每次返回的内容都包含之前生成的内容），如需增量输出，请设置相应参数：

-   Python SDK方式：设置 `incremental_output`参数为`True`。
    
-   Java SDK方式：使用 `incrementalOutput` 方法并设置为 `true`。
    
-   HTTP方式：在 `parameters` 中使用 `incremental_output`参数并设置为`true`。
    

**调用示例**

如果智能体应用内使用了[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking#5be853b164zv4)（例如 Qwen3），输出顺序为“先思考、后答案”。调用时设置`has_thoughts`参数为`True`，即可在`thoughts`字段中返回思考过程。

-   其中**Qwen3模型**开启思考模式有两种方式：一是在应用内打开**思考模式**开关并**发布**应用；二是API调用时设置 `enable_thinking` 为 `true` 。若同时设置，则以API参数为准。
    
-   其他思考模型默认开启思考模式，且无法关闭。
    

## Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application
responses = Application.call(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv("DASHSCOPE_API_KEY"), 
            app_id='YOUR_APP_ID',
            prompt='你是谁？',
            stream=True,  # 流式输出
            incremental_output=True)  # 增量输出

for response in responses:
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print(f'{response.output.text}\n')  # 处理只输出文本text
```

**响应示例**

```
我是来自

阿里

云

的大规模语言模型

，我叫通

义千问。
```

## Java

**请求示例**

```
// 建议dashscope SDK的版本 >= 2.15.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;// 流式输出
// 智能体应用调用实现流式输出结果

public class Main {
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 替换为实际的应用 ID
                .appId("YOUR_APP_ID")
                .prompt("你是谁?")
                // 增量输出
                .incrementalOutput(true)
                .build();
        Application application = new Application();
        // .streamCall（）：流式输出内容
        Flowable<ApplicationResult> result = application.streamCall(param);
        result.blockingForEach(data -> {
            System.out.printf("%s\n",
                    data.getOutput().getText());
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
我是阿里
云
开发的一款超大规模语言
模型，我叫
通义千问
。
```

## HTTP

## curl

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--header 'X-DashScope-SSE: enable' \
--data '{
    "input": {
        "prompt": "你是谁？"

    },
    "parameters":  {
        "incremental_output":true
    },
    "debug": {}
}'
```

> YOUR\_APP\_ID替换为实际的应用 ID。

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"我是"},"usage":{"models":[{"input_tokens":203,"output_tokens":1,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"来自"},"usage":{"models":[{"input_tokens":203,"output_tokens":2,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"阿里"},"usage":{"models":[{"input_tokens":203,"output_tokens":3,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"云"},"usage":{"models":[{"input_tokens":203,"output_tokens":4,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"的超大规模语言"},"usage":{"models":[{"input_tokens":203,"output_tokens":8,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"模型，我叫"},"usage":{"models":[{"input_tokens":203,"output_tokens":12,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:7
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"通义千问"},"usage":{"models":[{"input_tokens":203,"output_tokens":16,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:8
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"null","text":"。"},"usage":{"models":[{"input_tokens":203,"output_tokens":17,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}

id:9
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"70ac158ae65f4764b9228a52951f3711","finish_reason":"stop","text":""},"usage":{"models":[{"input_tokens":203,"output_tokens":17,"model_id":"qwen-max"}]},"request_id":"f66273ce-1a4d-9107-9c8a-da2a0f7267b5"}
```

## PHP

**请求示例**

```
<?php

// 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID

$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '你是谁？'],
    "parameters" => [
        'incremental_output' => true]];// 增量输出
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
    'X-DashScope-SSE: enable' // 流式输出
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
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"我是阿里"},"usage":{"models":[{"input_tokens":58,"output_tokens":2,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"云"},"usage":{"models":[{"input_tokens":58,"output_tokens":3,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"开发"},"usage":{"models":[{"input_tokens":58,"output_tokens":4,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"的一款超大规模语言"},"usage":{"models":[{"input_tokens":58,"output_tokens":8,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"模型，我叫"},"usage":{"models":[{"input_tokens":58,"output_tokens":12,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:6
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"通义千问"},"usage":{"models":[{"input_tokens":58,"output_tokens":16,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:7
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"null","text":"。"},"usage":{"models":[{"input_tokens":58,"output_tokens":17,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
id:8
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"232f8a3622774c5182997c6f262c59f9","finish_reason":"stop","text":""},"usage":{"models":[{"input_tokens":58,"output_tokens":17,"model_id":"qwen-max"}]},"request_id":"e682ec04-28a5-9957-ac48-76f87693cab5"}
```

## Node.js

**需安装相关依赖：**

```
npm install axios
```

**请求示例**

**1.输出完整响应**

```
const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "你是谁？"
        },
        parameters: {
            'incremental_output' : 'true' // 增量输出
        },
        debug: {}
    };

    try {
        console.log("Sending request to DashScope API...");

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable' // 流式输出
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            // 处理流式响应
            response.data.on('data', (chunk) => {
                console.log(`Received chunk: ${chunk.toString()}`);
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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
```

可展开折叠面板查看具体内容：

**2.只输出text字段内容**

```
const axios = require('axios');
const { Transform } = require('stream');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'YOUR_APP_ID'; // 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: { prompt: "你是谁？" },
        parameters: { incremental_output: true }, // 增量输出
        debug: {}
    };

    try {
        console.log("Sending request to DashScope API...");

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable' // 流式输出
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            // // 处理流式响应 SSE协议解析转换流
            const sseTransformer = new Transform({
                transform(chunk, encoding, callback) {
                    this.buffer += chunk.toString();
                    
                    // 按SSE事件分割（两个换行符）
                    const events = this.buffer.split(/\n\n/);
                    this.buffer = events.pop() || ''; // 保留未完成部分
                    
                    events.forEach(eventData => {
                        const lines = eventData.split('\n');
                        let textContent = '';
                        
                        // 解析事件内容
                        lines.forEach(line => {
                            if (line.startsWith('data:')) {
                                try {
                                    const jsonData = JSON.parse(line.slice(5).trim());
                                    if (jsonData.output?.text) {
                                        textContent = jsonData.output.text;
                                    }
                                } catch(e) {
                                    console.error('JSON解析错误:', e.message);
                                }
                            }
                        });

                        if (textContent) {
                            // 添加换行符并推送
                            this.push(textContent + '\n');
                        }
                    });
                    
                    callback();
                },
                flush(callback) {
                    if (this.buffer) {
                        this.push(this.buffer + '\n');
                    }
                    callback();
                }
            });
            sseTransformer.buffer = '';

            // 管道处理
            response.data
                .pipe(sseTransformer)
                .on('data', (textWithNewline) => {
                    process.stdout.write(textWithNewline); // 自动换行输出
                })
                .on('end', () => console.log(""))
                .on('error', err => console.error("管道错误:", err));

        } else {
            console.log("请求失败，状态码:", response.status);
            response.data.on('data', chunk => console.log(chunk.toString()));
        }
    } catch (error) {
        console.error(`API调用失败: ${error.message}`);
        if (error.response) {
            console.error(`状态码: ${error.response.status}`);
            error.response.data.on('data', chunk => console.log(chunk.toString()));
        }
    }
}

callDashScope();
```

**响应示例**

## 1.输出完整响应

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"bb9fb75687104983ae47fc1f34ef36a1","finish_reason":"null","text":"你好！"},"usage":{"models":[{"input_tokens":56,"output_tokens":2,"model_id":"qwen-max"}]},"request_id":"d96ec7e0-5ad8-9f19-82c1-9c87f86e12b8"}
id:2
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"bb9fb75687104983ae47fc1f34ef36a1","finish_reason":"null","text":"有什么"},"usage":{"models":[{"input_tokens":56,"output_tokens":3,"model_id":"qwen-max"}]},"request_id":"d96ec7e0-5ad8-9f19-82c1-9c87f86e12b8"}
id:3
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"bb9fb75687104983ae47fc1f34ef36a1","finish_reason":"null","text":"可以帮助"},"usage":{"models":[{"input_tokens":56,"output_tokens":4,"model_id":"qwen-max"}]},"request_id":"d96ec7e0-5ad8-9f19-82c1-9c87f86e12b8"}
id:4
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"bb9fb75687104983ae47fc1f34ef36a1","finish_reason":"null","text":"你的吗？"},"usage":{"models":[{"input_tokens":56,"output_tokens":7,"model_id":"qwen-max"}]},"request_id":"d96ec7e0-5ad8-9f19-82c1-9c87f86e12b8"}
id:5
event:result
:HTTP_STATUS/200
data:{"output":{"session_id":"bb9fb75687104983ae47fc1f34ef36a1","finish_reason":"stop","text":""},"usage":{"models":[{"input_tokens":56,"output_tokens":7,"model_id":"qwen-max"}]},"request_id":"d96ec7e0-5ad8-9f19-82c1-9c87f86e12b8"}
```

## 2.只输出text字段内容

```
我是
阿里
云
开发的一款超大规模
语言模型，我
叫通义千
问。
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
        string appId = "YOUR_APP_ID"; // 替换为实际的应用ID
        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            client.DefaultRequestHeaders.Add("X-DashScope-SSE", "enable");

            string jsonContent = @"{
                ""input"": {
                    ""prompt"": ""你是谁""
                },
                ""parameters"": {""incremental_output"": true},
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
2025-02-14 16:22:08:482
Request successful:
2025-02-14 16:22:09:098
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"我是"},"usage":{"models":[{"input_tokens":51,"output_tokens":1,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:099
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"来自"},"usage":{"models":[{"input_tokens":51,"output_tokens":2,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:172
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"阿里"},"usage":{"models":[{"input_tokens":51,"output_tokens":3,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:172
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"云的大规模语言"},"usage":{"models":[{"input_tokens":51,"output_tokens":7,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:463
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"模型，我叫"},"usage":{"models":[{"input_tokens":51,"output_tokens":11,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:618
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"通义千问"},"usage":{"models":[{"input_tokens":51,"output_tokens":15,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:777
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"。我是你的人"},"usage":{"models":[{"input_tokens":51,"output_tokens":19,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:09:932
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"工智能助手，"},"usage":{"models":[{"input_tokens":51,"output_tokens":23,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:10:091
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"可以回答问题、"},"usage":{"models":[{"input_tokens":51,"output_tokens":27,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:10:244
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"创作文字，比如"},"usage":{"models":[{"input_tokens":51,"output_tokens":31,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:10:389
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"写故事、写"},"usage":{"models":[{"input_tokens":51,"output_tokens":35,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:10:525
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"公文、写"},"usage":{"models":[{"input_tokens":51,"output_tokens":39,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:10:662
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"邮件、写剧本"},"usage":{"models":[{"input_tokens":51,"output_tokens":43,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:10:902
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"等等，还能表达"},"usage":{"models":[{"input_tokens":51,"output_tokens":47,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:11:062
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"观点，玩游戏等"},"usage":{"models":[{"input_tokens":51,"output_tokens":51,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:11:233
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"null","text":"。"},"usage":{"models":[{"input_tokens":51,"output_tokens":52,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:11:309
{"output":{"session_id":"c2265dd99e4b40e0b5b3638824f21dd9","finish_reason":"stop","text":""},"usage":{"models":[{"input_tokens":51,"output_tokens":52,"model_id":"qwen-plus"}]},"request_id":"2d40821d-98bb-960e-999d-c456af8bc9e9"}
2025-02-14 16:22:11:388
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
	"strings"
	"time"
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := "sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体，其中incremental_output为是否开启流式响应
	requestBody := map[string]interface{}{
		"input": map[string]string{
			"prompt": "你是谁？",
		},
		"parameters": map[string]interface{}{
			"incremental_output": true,
		},
		"debug": map[string]interface{}{},
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

	// 设置请求头,其中X-DashScope-SSE设置为enable，表示开启流式响应
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-DashScope-SSE", "enable")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to send request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		body, _ := io.ReadAll(resp.Body)
		fmt.Println(string(body))
		return
	}

	// 处理流式响应
	reader := io.Reader(resp.Body)
	buf := make([]byte, 1024)
	for {
		n, err := reader.Read(buf)
		if n > 0 {
			data := string(buf[:n])
			lines := strings.Split(data, "\n")
			for _, line := range lines {
				line = strings.TrimSpace(line)
				if len(line) >= 5 && line[:5] == "data:" {
					timestamp := time.Now().Format("2006-01-02 15:04:05.000")
					fmt.Printf("%s: %s\n", timestamp, line[5:])
				} else if len(line) > 0 {
					fmt.Println(line)
				}
			}
		}
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Printf("Error reading response: %v\n", err)
			break
		}
	}
}
```

**响应示例**

```
id:1
event:result
:HTTP_STATUS/200
2025-02-13 18:21:09.050: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"我是"},"usage":{"models":[{"input_tokens":262,"output_tokens":1,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:2
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.016: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"通"},"usage":{"models":[{"input_tokens":262,"output_tokens":2,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:3
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.016: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"义"},"usage":{"models":[{"input_tokens":262,"output_tokens":3,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:4
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.016: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"千问，由"},"usage":{"models":[{"input_tokens":262,"output_tokens":7,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:5
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.017: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"阿里云开发的"},"usage":{"models":[{"input_tokens":262,"output_tokens":11,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:6
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.017: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"AI助手。我"},"usage":{"models":[{"input_tokens":262,"output_tokens":15,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:7
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.017: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"被设计用来回答"},"usage":{"models":[{"input_tokens":262,"output_tokens":19,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:8
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.018: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"各种问题、提供"},"usage":{"models":[{"input_tokens":262,"output_tokens":23,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:9
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.102: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"信息和与用户"},"usage":{"models":[{"input_tokens":262,"output_tokens":27,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:10
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.257: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"进行对话。需要"},"usage":{"models":[{"input_tokens":262,"output_tokens":31,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:11
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.414: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"null","text":"帮助吗？"},"usage":{"models":[{"input_tokens":262,"output_tokens":34,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
id:12
event:result
:HTTP_STATUS/200
2025-02-13 18:21:10.481: {"output":{"session_id":"830189188149488794708ae012f4c595","finish_reason":"stop","text":""},"usage":{"models":[{"input_tokens":262,"output_tokens":34,"model_id":"qwen-plus"}]},"request_id":"2563953d-914c-9256-ae1a-b62beb957112"}
```

### **传递自定义参数**

通过自定义提示词变量（引导输出方向）、插件参数（扩展能力）及用户级鉴权参数（权限控制），智能体可适配多种业务场景。调用时使用`biz_params`传递参数，实现灵活响应。

**描述**

**说明**

`user_prompt_params`

类型：`_object_`

传递自定义提示词变量。

用于传递在提示词中插入配置的变量。在控制台定义变量，API调用时传具体值。

示例：

prompt：请给出{{city}}的三种美食推荐，只显示美食名称，逗号隔开。

参数：

```
biz_params = {
    "user_prompt_params":{
        "city": "北京"}}
```

实际生效prompt:请给出北京的三种美食推荐，只显示美食名称，逗号隔开。

控制台需要按如下步骤操作：

1.  在**智能体应用**内添加自定义变量；
    
2.  在提示词中引用；
    
3.  **发布**应用。
    

**重要**

确保应用内添加的自定义变量名和API调用时传递的调用名一致。

`user_defined_params`

类型：`_object_`

传递自定义插件参数。

用于传递插件执行任务所需的业务数据（如城市、日期）。

控制台需要按如下步骤操作：

1.  在控制台配置插件工具的业务透传参数；
    
    **说明**
    
    自定义插件工具参数的配置方法，请参考[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins)。
    
2.  测试并发布插件工具；
    
3.  关联**智能体应用**，并**发布**应用。
    
    **重要**
    
    插件工具只能与位于相同业务空间里的**智能体应用**关联。
    

user\_defined\_tokens

类型：`_object_`

传递自定义插件用户级鉴权参数。

插件调用时的用户身份验证（如`DASHSCOPE_API_KEY`）。

```
biz_params = {
    "user_defined_params": {
        "<YOUR_TOOL_ID>": {
            "city": "北京"}},
    "user_defined_tokens": {
        "<YOUR_TOOL_ID>": {
            "user_token": "sk-xxx"}}}
```

API调用示例如下：

#### **提示词变量**

**使用步骤**

1.  在控制台的**智能体应用**内添加自定义变量，并在提示词中引用，然后**发布**应用。示例：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9864148471/p960772.png)
    
2.  API调用，示例如下：
    
    ##### **Python**
    
    **请求示例**
    
    ```
    from http import HTTPStatus
    import os
    # 建议dashscope SDK 的版本 >= 1.14.0
    from dashscope import Application
    biz_params = {
        # 智能体应用的自定义变量参数，可替换为实际参数，支持传入多个变量键值对，英文逗号隔开
        "user_prompt_params":{
            "city": "北京"}}
    response = Application.call(
                # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                api_key=os.getenv("DASHSCOPE_API_KEY"), 
                app_id='YOUR_APP_ID', # 替换为实际的应用ID，应用卡片获取
                prompt='美食推荐',
                biz_params=biz_params)
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n' % (response.output.text))  # 处理只输出文本text
        # print('%s\n' % (response.usage))
    ```
    
    **响应示例**
    
    ```
    北京烤鸭，炸酱面，豆汁儿
    ```
    
    ##### **Java**
    
    **请求示例**
    
    ```
    import com.alibaba.dashscope.app.*;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.JsonUtils;
    
    public class Main {
        public static void appCall() throws NoApiKeyException, InputRequiredException {
            String bizParams =
                    // 智能体应用的自定义变量参数传递，可替换为实际变量参数，支持传入多个变量键值对，英文逗号隔开
                    "{\"user_prompt_params\":{\"city\":\"北京\"}}";
            ApplicationParam param = ApplicationParam.builder()
                    // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .appId("YOUR_APP_ID") // 替换为实际的应用ID，应用卡片获取
                    .prompt("美食推荐")
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
    北京烤鸭，炸酱面，豆汁儿
    ```
    
    ##### **HTTP**
    
    ##### **curl**
    
    **请求示例**
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {
            "prompt": "美食推荐",
            "biz_params": 
            {
                "user_prompt_params":{"city": "北京"}
            } 
        },
        "parameters":  {},
        "debug":{}
    }'
    ```
    
    > YOUR\_APP\_ID替换为实际的应用ID，可在应用卡片获取。
    
    > user\_prompt\_params支持传递多个自定义变量键值对，英文逗号隔开。
    
    **响应示例**
    
    ```
    {
        "output": {
            "finish_reason": "stop",
            "session_id": "1ad91249a37148389ac042530002ec94",
            "text": "北京烤鸭，炸酱面，豆汁儿"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 11,
                    "model_id": "qwen-turbo-latest",
                    "input_tokens": 78
                }
            ]
        },
        "request_id": "4fd714e5-dc35-9933-98f4-0ed314918c1f"
    }
    ```
    
    ##### **PHP**
    
    **请求示例**
    
    ```
    <?php
    
    # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
    $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
    //user_prompt_params支持传递多个自定义变量键值对，英文逗号隔开
    // 构造请求数据
    $data = [
        "input" => [
            'prompt' => '美食推荐',
            'biz_params' => [
            'user_prompt_params' => [
                    'city' => "北京"            
                    ]
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
    北京烤鸭，炸酱面，豆汁儿
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
        const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
        const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    
        // user_prompt_params可传递多个自定义变量键值对，英文逗号隔开。
        const data = {
            input: {
                prompt: "美食推荐",
                biz_params: {
                    user_prompt_params: {      
                        'city': '北京'  
                    }
                }
            },
            parameters: {},
            debug: {}
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
                console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
            }
        }
    }
    callDashScope();
    ```
    
    **响应示例**
    
    ```
    北京烤鸭，炸酱面，豆汁儿
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
            string appId = "YOUR_APP_ID";// 替换为实际的应用ID
    
            // user_prompt_params支持传递多个自定义变量键值对，英文逗号隔开
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
                        ""prompt"": ""美食推荐"",
                        ""biz_params"": {{
                            ""user_prompt_params"": {{
                                    ""city"": ""北京""
                            }}
                        }}
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
            "session_id": "de5b3942acce40ba8739338518c01b9e",
            "text": "北京烤鸭，炸酱面，豆汁儿"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 11,
                    "model_id": "qwen-turbo-latest",
                    "input_tokens": 78
                }
            ]
        },
        "request_id": "86f89865-b851-9d5f-b96d-181d8d402f85"
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
    	appId := "YOUR_APP_ID" // 替换为实际的应用 ID
    	if apiKey == "" {
    		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
    		return
    	}
    
    	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)
    
    	// 创建请求体，user_prompt_params支持传递多个自定义变量键值对，英文逗号隔开
    	requestBody := map[string]interface{}{
    		"input": map[string]interface{}{
    			"prompt": "美食推荐",
    			"biz_params": map[string]interface{}{
    				"user_prompt_params": map[string]interface{}{
    					"city": "北京",
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
            "session_id": "26daaa1561ba482c8248502db55df3d3",
            "text": "北京烤鸭，炸酱面，豆汁儿"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 11,
                    "model_id": "qwen-turbo-latest",
                    "input_tokens": 78
                }
            ]
        },
        "request_id": "405ab32b-9277-9408-ac1f-711845d334ce"
    }
    ```
    

#### **插件业务参数**

以[应用的参数传递](https://help.aliyun.com/zh/model-studio/pass-through-of-application-parameters)中的**寝室公约内容查询工具**作为示例，通过传递关联插件的“索引”（article\_index参数），查询寝室公约内容。

> `<YOUR_TOOL_ID>`替换为关联的插件工具ID（可在插件卡片中获取），并传递插件中配置的输入参数键值对。本示例中传递的参数为article\_index，值为2。

##### **Python**

**请求示例**

```
import os
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Application
biz_params = {
    # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换<YOUR_TOOL_ID>
    "user_defined_params": {
        "<YOUR_TOOL_ID>": {
            "article_index": 2}}}
response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='YOUR_APP_ID',
        prompt='寝室公约内容',
        biz_params=biz_params)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print('%s\n' % (response.output.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
```

**响应示例**

```
寝室公约的第二条规定如下：

"寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。"

这表明在寝室内，成员之间应该培养一种积极正面的生活和学习氛围，彼此帮助和支持，同时也要学会理解和尊重他人。如果您需要了解公约的其他条款，请告诉我！
```

##### **Java**

**请求示例**

```
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        String bizParams =
                // 智能体应用的自定义插件输入参数传递，自定义的插件ID替换<YOUR_TOOL_ID>
                "{\"user_defined_params\":{\"<YOUR_TOOL_ID>\":{\"article_index\":2}}}";
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("YOUR_APP_ID")
                .prompt("寝室公约内容")
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
寝室公约的第二条规定如下：

第二条 寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。

这强调了在共同生活环境中，室友之间应该保持积极正面的关系，通过相互帮助和支持来营造一个和谐的生活和学习氛围。如果有更多具体的条款需要了解，请告知我。
```

##### **HTTP**

##### **curl**

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "寝室公约内容",
        "biz_params": 
        {
            "user_defined_params":
            {
                "<YOUR_TOOL_ID>":
                    {
                    "article_index": 2
                    }
            }
        } 
    },
    "parameters":  {},
    "debug":{}
}'
```

> YOUR\_APP\_ID替换为实际的应用 ID。<YOUR\_TOOL\_ID>替换为插件ID。

**响应示例**

```
{"output":
{"finish_reason":"stop",
"session_id":"e151267ffded4fbdb13d91439011d31e",
"text":"寝室公约的第二条内容是：“寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。”这意呀着在寝室生活中，大家要彼此支持，共同创造一个和谐、积极向上的生活环境。"},
"usage":{"models":[{"output_tokens":94,"model_id":"qwen-max","input_tokens":453}]},
"request_id":"a39fd2b5-7e2c-983e-84a1-1039f726f18a"}%
```

##### **PHP**

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
//<YOUR_TOOL_ID>替换为实际的插件ID
// 构造请求数据
$data = [
    "input" => [
        'prompt' => '寝室公约内容',
        'biz_params' => [
        'user_defined_params' => [
            '<YOUR_TOOL_ID>' => [
                'article_index' => 2            
                ]
            ]
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
寝室公约的第二条规定：寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。这是为了保证大家能在一个和谐友爱的环境中生活和学习。如果有更多具体的条款需要了解，或者有其他问题，随时可以问我！
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
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
    const pluginCode = 'YOUR_TOOL_ID';// 替换为实际的插件ID
    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "寝室公约内容",
            biz_params: {
                user_defined_params: {
                    [pluginCode]: {
                        // article_index为自定义插件的变量，替换为实际的插件变量
                        'article_index': 3
                    }
                }
            }
        },
        parameters: {},
        debug: {}
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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
```

**响应示例**

```
寝室公约的第三条规定如下：

注意安全用电，杜绝火灾隐患。寝室内严禁使用明火、违规电器、各种灶具以及其他违规物品，不得存放易爆、易燃物品，私接电源。

如果您需要了解更多的规定，请告诉我。
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
        string appId = "YOUR_APP_ID";// 替换为实际的应用ID

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("请确保设置了 DASHSCOPE_API_KEY。");
            return;
        }

        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            string pluginCode = "YOUR_TOOL_ID"; // YOUR_TOOL_ID替换为实际的插件 ID
            string jsonContent = $@"{{
                ""input"": {{
                    ""prompt"": ""寝室公约内容"",
                    ""biz_params"": {{
                        ""user_defined_params"": {{
                            ""{pluginCode}"": {{
                                ""article_index"": 2
                            }}
                        }}
                    }}
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
        "session_id": "237ca6187c814f3b9e7461090a5f8b74",
        "text": "寝室公约的第二条规定如下：

"寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。"

这表示在寝室内，成员之间需要建立起一种积极正面的关系，通过帮助、关心和支持彼此来营造一个和谐的生活和学习环境。同时也要学会理解和接受室友之间的差异，以真诚的态度去交流沟通。如果还有其他条款或具体内容想要了解，请告诉我！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 133,
                "model_id": "qwen-max",
                "input_tokens": 829
            }
        ]
    },
    "request_id": "64e8c359-d071-9d2e-bb94-187e86cc3a79"
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
	appId := "YOUR_APP_ID"           // 替换为实际的应用 ID
	pluginCode := "YOUR_TOOL_ID" // 替换为实际的插件 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]interface{}{
			"prompt": "寝室公约内容",
			"biz_params": map[string]interface{}{
				"user_defined_params": map[string]interface{}{
					pluginCode: map[string]interface{}{
						"article_index": 2,
					},
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
        "session_id": "860d2a4c1f3649ac880298537993cb51",
        "text": "寝室公约的第二条规定如下：

寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。

这强调了在宿舍生活中，室友之间应该保持良好的互助关系，同时也要互相尊重对方。您想要了解其他条款的内容吗？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 84,
                "model_id": "qwen-max",
                "input_tokens": 876
            }
        ]
    },
    "request_id": "0a250055-90a4-992d-9276-e268ad35d1ab"
}
```

#### **插件用户级鉴权参数**

以[应用的参数传递](https://help.aliyun.com/zh/model-studio/pass-through-of-application-parameters)中的**寝室公约内容查询工具**作为示例，通过传递关联插件的“索引”（article\_index参数）和用户级鉴权信息，查询寝室公约内容。

> `<YOUR_TOOL_ID>`替换为关联的插件工具ID（可在插件卡片中获取），并传递插件中配置的输入参数键值对。本示例中传递的参数为article\_index，值为2。

##### **Python**

**请求示例**

```
from http import HTTPStatus
import os
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Application
biz_params = {
    # 智能体应用的自定义插件鉴权传递，自定义的插件ID替换<YOUR_TOOL_ID>，鉴权信息替换YOUR_TOKEN，如API key
    "user_defined_params": {
        "<YOUR_TOOL_ID>": {
            "article_index": 2}},
    "user_defined_tokens": {
        "<YOUR_TOOL_ID>": {
            "user_token": "YOUR_TOKEN"}}}
response = Application.call(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv("DASHSCOPE_API_KEY"), 
            app_id='YOUR_APP_ID',
            prompt='寝室公约内容',
            biz_params=biz_params)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print('%s\n' % (response.output.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
```

**响应示例**

```
寝室公约的第二条规定如下：

寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。

如果您需要了解更多的规定内容，请告诉我。
```

##### **Java**

**请求示例**

```
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        String bizParams =
                // <YOUR_TOOL_ID>替换为实际的插件ID,YOUR_TOKEN替换为实际的Token,如API key
                "{\"user_defined_params\":{\"<YOUR_TOOL_ID>\":{\"article_index\":2}}," +
                        "\"user_defined_tokens\":{\"<YOUR_TOOL_ID>\":{\"user_token\":\"YOUR_TOKEN\"}}}";
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("YOUR_APP_ID")
                .prompt("寝室公约内容")
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
寝室公约的第二条规定如下：

寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。

如果您需要查询更多的规定内容，请告诉我。
```

##### **HTTP**

## curl

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "寝室公约内容",
        "biz_params": 
        {
            "user_defined_params":
            {
                "<YOUR_TOOL_ID>":
                    {
                    "article_index": 2
                    }
            },
            "user_defined_tokens":
            {
                "<YOUR_TOOL_ID>":
                    {
                    "user_token": "YOUR_TOKEN"
                    }
            }
        } 
    },
    "parameters":  {},
    "debug":{}
}'
```

> YOUR\_APP\_ID替换为实际的应用 ID。<YOUR\_TOOL\_ID>替换为实际的插件ID。

**响应示例**

```
{"output":{"finish_reason":"stop",
"session_id":"d3b5c3e269dc40479255a7a02df5c630",
"text":"寝室公约的第二条内容为：“寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。”这强调了寝室生活中成员之间和谐相处与共同进步的重要性。"},
"usage":{"models":[{"output_tokens":80,"model_id":"qwen-max","input_tokens":432}]},
"request_id":"1f77154c-edc3-9003-b622-816fa2f849cf"}%
```

##### **PHP**

**请求示例**

```
<?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
$url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '寝室公约内容',
        'biz_params' => [
        'user_defined_params' => [
            '<YOUR_TOOL_ID>' => [//<YOUR_TOOL_ID>替换为实际的插件ID
                'article_index' => 2            
                ]
            ],
        'user_defined_tokens' => [
            '<YOUR_TOOL_ID>' => [//<YOUR_TOOL_ID>替换为实际的插件ID
                'user_token' => 'YOUR_TOKEN'//替换为实际的Token,如API key
            ]
        ]
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
寝室公约的第二条规定如下：

> 寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。

如果需要了解更多的公约内容或其他信息，请随时告诉我！
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
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
    const pluginCode = 'YOUR_TOOL_ID';// 替换为实际的插件ID
    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "寝室公约内容",
            biz_params: {
                user_defined_params: {
                    [pluginCode]: {
                        // article_index为自定义插件的变量，替换为实际的插件变量
                        'article_index': 6
                    }
                },
                user_defined_tokens: {
                    [pluginCode]: {
                        // YOUR_TOKEN替换为实际的鉴权信息,如API key
                        user_token: 'YOUR_TOKEN'
                    }
                }
            }
        },
        parameters: {},
        debug: {}
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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
```

**响应示例**

```
寝室公约的第六条规定：养成良好的作息习惯，每一位寝室成员都享有休息的权利和承担保证他人休息权利和义务。如果你需要了解更多的规定内容，请进一步说明。
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
        string appId = "YOUR_APP_ID";// 替换为实际的应用ID

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("请确保设置了 DASHSCOPE_API_KEY。");
            return;
        }

        string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            string pluginCode = "YOUR_TOOL_ID"; //替换为实际的插件 ID
            // YOUR_TOKEN替换为实际的Token,如API key
            string jsonContent = $@"{{
                ""input"": {{
                    ""prompt"": ""寝室公约内容"",
                    ""biz_params"": {{
                        ""user_defined_params"": {{
                            ""{pluginCode}"": {{
                                ""article_index"": 2
                            }}
                        }},
                        ""user_defined_tokens"": {{
                            ""{pluginCode}"": {{
                                ""user_token"": ""YOUR_TOKEN"" 
                            }}
                        }}
                    }}
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
        "session_id": "1a1913a9922a401f8eba36df8ea1a062",
        "text": "寝室公约的第二条规定如下：

寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。

如需了解更详细的公约内容，请进一步指明。"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 66,
                "model_id": "qwen-max",
                "input_tokens": 802
            }
        ]
    },
    "request_id": "04bac806-c5e6-9fab-a846-a66641862be9"
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
	appId := "YOUR_APP_ID"           // 替换为实际的应用 ID
	pluginCode := "YOUR_TOOL_ID" // 替换为实际的插件 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]interface{}{
			"prompt": "寝室公约内容",
			"biz_params": map[string]interface{}{
				"user_defined_params": map[string]interface{}{
					pluginCode: map[string]interface{}{
						"article_index": 10,
					},
				},
				"user_defined_tokens": map[string]interface{}{
					pluginCode: map[string]interface{}{
						"user_token": "YOUR_USER_TOKEN", // 替换实际的鉴权 token，如API key
					},
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
        "session_id": "b8e051ba7e954ff8919208e7b84430fa",
        "text": "寝室公约的第十条规定，寝室成员应共同努力，营造和维护内务整洁干净、美观、高文化品味的寝室环境。如果需要了解完整的寝室公约内容，可能还需要查看其他条款或直接咨询宿舍管理部门。对于更多具体内容，您还有想要了解的部分吗？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 70,
                "model_id": "qwen-max",
                "input_tokens": 855
            }
        ]
    },
    "request_id": "0921ee34-2754-9616-a826-cea33a0e0a14"
}
```

## **进阶功能**

### **检索知识库**

知识库功能作为百炼的RAG能力，能有效地为大模型补充私有知识、提供最新信息。调用**智能体应用**时指定检索范围，可提高大模型的回答准确性。更多知识库功能请参考：[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

#### 前提条件

在百炼控制台的**智能体应用**中，打开**知识库**开关，并**发布**应用。

#### **指定检索范围**

1.  检索指定的[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)，有以下三种方式：
    
    1.  在应用内单击**配置知识库**以关联指定知识库，并**发布**应用；
        
    2.  在应用内不关联指定知识库，API调用时通过`rag_options`传入知识库ID；
        
    3.  既在应用内关联指定知识库，又在API调用时通过`rag_options`传入知识库ID。
        
        > 这种情况只会检索调用时传入的知识库。例如，网页端的**智能体应用**里关联了知识库A，而API调用时只指定了知识库B，那么不会检索知识库A，只会检索知识库B。
        
    
    获取知识库ID（pipeline\_ids）：可以在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面获取，也可以使用[CreateIndex](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex)接口（仅支持非结构化知识库）返回的`Data.Id`。
    
    可以是**智能体应用**已经关联的知识库，也可以是没有关联的知识库。
    
    调用示例：此处选择[百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)作为一个非结构化数据知识库的文件。
    
    ## Python
    
    **请求示例**
    
    ```
    import os
    from http import HTTPStatus
    # 建议dashscope SDK 的版本 >= 1.20.11
    from dashscope import Application
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        app_id='YOUR_APP_ID',  # 应用ID替换YOUR_APP_ID
        prompt='请帮我推荐一款3000元以下的手机',
        rag_options={
            "pipeline_ids": ["YOUR_PIPELINE_ID1","YOUR_PIPELINE_ID2"],  # 替换为实际的知识库ID,逗号隔开多个
        }
    )
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n' % (response.output.text))  # 处理只输出文本text
        # print('%s\n' % (response.usage))
    ```
    
    **响应示例**
    
    ```
    根据您的预算，我推荐您选择**百炼 Zephyr Z9**。这款手机的参考售价在2499-2799元之间，符合您的预算需求。它拥有轻巧的6.4英寸1080 x 2340像素屏幕设计，搭配128GB存储与6GB RAM，适合日常使用。此外，它还配备了4000mAh电池以及支持30倍数字变焦的镜头，能够很好地满足拍照及续航的需求。如果您追求的是轻薄便携且功能全面的手机，那么百炼 Zephyr Z9会是一个不错的选择。
    ```
    
    ## Java
    
    **请求示例**
    
    ```
    // 建议dashscope SDK 的版本 >= 2.16.8；
    import com.alibaba.dashscope.app.*;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import java.util.Arrays;
    
    public class Main {
        public static void streamCall() throws NoApiKeyException, InputRequiredException {
            ApplicationParam param = ApplicationParam.builder()
                    // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .appId("YOUR_APP_ID") // 替换为实际的应用ID
                    .prompt("请帮我推荐一款3000元左右的手机")
                    .ragOptions(RagOptions.builder()
                            // 替换为实际指定的知识库ID，逗号隔开多个
                            .pipelineIds(Arrays.asList("PIPELINES_ID1", "PIPELINES_ID2"))
                            .build())
                    .build();
    
            Application application = new Application();
            ApplicationResult result = application.call(param);
            System.out.printf("%s\n",
                    result.getOutput().getText());// 处理只输出文本text
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
    在3000元预算范围内，我推荐您考虑**百炼 Zephyr Z9**。这款手机定价在2499至2799之间，非常符合您的预算要求。它具有以下特点：
    
    - **轻巧设计**：6.4英寸屏幕大小适中，便于单手操作。
    - **性能均衡**：搭载128GB存储与6GB RAM，对于日常使用来说足够了。
    - **续航能力**：配备4000mAh电池，可以满足一天的正常使用需求。
    - **拍照功能**：具备30倍数字变焦镜头，适合捕捉远处景物。
    
    如果您更注重游戏体验或对其他方面有特别的需求，请告诉我，以便我能提供更加个性化的建议！
    ```
    
    ## HTTP
    
    ## curl
    
    **请求示例**
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{YOUR_APP_ID}/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {
            "prompt": "请帮我推荐一款3000元以下的手机"
        },
        "parameters":  {
                        "rag_options" : {
                        "pipeline_ids":["YOUR_PIPELINE_ID1"]}
        },
        "debug": {}
    }'
    ```
    
    > YOUR\_APP\_ID替换为实际的应用 ID，YOUR\_PIPELINE\_ID1替换为指定的知识库ID。
    
    **响应示例**
    
    ```
    {"output":{"finish_reason":"stop","session_id":"d1208af96f9a4d8390e9b29e86f0623c",
    "text":"在3000元以下的价格范围内，我向您推荐百炼 Zephyr Z9。
    这款手机定价在2499至2799元之间，完美符合您的预算要求。
    它拥有轻巧的6.4英寸1080 x 2340像素显示屏，搭配了128GB的存储空间和6GB的RAM，足以应对日常使用中的各种应用程序和多任务处理。
    此外，它配备了一块4000mAh的电池，能够确保您一整天的使用无虞，还搭载了30倍数字变焦镜头，方便您捕捉生活中的细节。
    综上所述，百炼 Zephyr Z9在性价比、设计与功能上都是一个不错的选择。"},
    "usage":{"models":[{"output_tokens":158,"model_id":"qwen-max","input_tokens":1025}]},
    "request_id":"eb2d40f7-bede-9d48-88dc-08abdcdd0351"}%
    ```
    
    ## PHP
    
    **请求示例**
    
    ```
    <?php
    # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
    
    $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
    
    // 构造请求数据
    $data = [
        "input" => [
            'prompt' => '请帮我推荐一款3000元以下的手机'
        ],
        "parameters" => [
            'rag_options' => [
                'pipeline_ids' => ['YOUR_PIPELINE_ID1','YOUR_PIPELINE_ID2']//替换为指定的知识库ID,逗号隔开多个
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
    在3000元以下的预算范围内，我推荐您考虑**百炼 Zephyr Z9**。这款手机定价在2499-2799元之间，非常适合您的预算。它具有轻巧的设计，配备6.4英寸1080 x 2340像素屏幕、128GB存储与6GB RAM，能够很好地满足日常使用需求。此外，其4000mAh电池可以保证一天的正常使用，并且配备了30倍数字变焦镜头来捕捉远处细节，既轻薄又不失强大功能。
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
        const appId = 'YOUR_APP_ID';//替换为实际的应用 ID
    
        const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    
        const data = {
            input: {
                prompt: "请帮我推荐一款3000元以下的手机"
            },
            parameters: {
                rag_options:{
                    pipeline_ids:['YOUR_PIPELINE_ID1','YOUR_PIPELINE_ID2']  // 替换为指定的知识库ID，多个请用逗号隔开
                }
            },
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
    在3000元以下的预算内，我推荐您考虑**百炼 Zephyr Z9**。这款手机参考售价为3999-4299元，但如果能赶上促销活动或折扣，可能会降到您的预算范围内。
    
    ### 百炼 Zephyr Z9 ——轻薄便携的艺术
    - **屏幕**: 6.4英寸 1080 x 2340像素
    - **存储与RAM**: 128GB存储 / 6GB RAM
    - **电池**: 4000mAh
    - **相机**: 30倍数字变焦镜头
    
    这款手机的特点是轻薄便携，日常使用非常方便，而且具有不错的续航能力。如果您更关注性价比和日常使用体验，百炼 Zephyr Z9 是一个不错的选择。
    
    如果您的预算非常严格，建议关注电商平台的促销活动，或者考虑其他品牌的同价位手机。希望这些建议对您有所帮助！
    ```
    
    ## C#
    
    **请求示例**
    
    ```
    using System.Text;
    
    class Program
    {
        static async Task Main(string[] args)
        {
            // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
            string appId = "YOUR_APP_ID";// 替换为实际的应用ID
            // YOUR_PIPELINE_ID1替换为指定的知识库ID
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
                        ""prompt"": ""请帮我推荐一款3000元以下的手机""
                    }},
                    ""parameters"": {{
                        ""rag_options"" : {{
                            ""pipeline_ids"":[""YOUR_PIPELINE_ID1""]
                        }}
                    }},
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
            "session_id": "2344ddc540ec4c5fa110b92d813d3807",
            "text": "根据您的预算，我推荐您考虑**百炼 Zephyr Z9**。这款手机的参考售价在2499-2799元之间，符合您的预算需求。它拥有6.4英寸1080 x 2340像素屏幕、128GB存储空间和6GB RAM，对于日常使用来说已经足够了。此外，4000mAh电池可以保证一天内的正常使用，而30倍数字变焦镜头则能满足您拍摄远处景物的需求。这是一款轻薄便携且功能全面的选择。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 121,
                    "model_id": "qwen-max",
                    "input_tokens": 1841
                }
            ]
        },
        "request_id": "99fceedf-2034-9fb0-aaad-9c837136801f"
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
    	appId := "YOUR_APP_ID" // 替换为实际的应用 ID
    
    	if apiKey == "" {
    		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
    		return
    	}
    
    	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)
    
    	// 创建请求体
    	requestBody := map[string]interface{}{
    		"input": map[string]string{
    			"prompt": "请帮我推荐一款3000元以下的手机",
    		},
    		"parameters": map[string]interface{}{
    			"rag_options": map[string]interface{}{
    				"pipeline_ids": []string{"YOUR_PIPELINE_ID1"}, // 替换为指定的知识库ID
    			},
    		},
    		"debug": map[string]interface{}{},
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
            "session_id": "fadbb4d1fe094ade88985620363506e6",
            "text": "根据您的预算，我为您推荐**百炼 Zephyr Z9**。这款手机的价格在2499-2799元之间，非常适合3000元以下的预算需求。它拥有轻巧的6.4英寸1080 x 2340像素屏幕设计，搭配128GB存储与6GB RAM，能够满足日常使用的需求。同时，4000mAh电池确保了一天的使用无忧，而30倍数字变焦镜头则可以捕捉远处的细节，是一款性价比很高的选择。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 119,
                    "model_id": "qwen-max",
                    "input_tokens": 1055
                }
            ]
        },
        "request_id": "3a755dd7-58a0-9a5e-8a07-b85b1db838a6"
    }
    ```
    
2.  检索指定的**非结构化数据**文档：在`rag_options`中传入知识库ID、文档ID、文档标签tags或文档元数据metadata（键值对）。
    
    > 文档ID、文档标签tags和文档元数据metadata仅对**非结构化数据**文档检索生效。
    
    -   获取方式：
        
        -   文档ID（file\_ids）：可以在[应用数据](https://bailian.console.aliyun.com/#/data-center)页面的文档列表中获取，也可以使用[AddFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfile)接口导入文档返回的ID。
            
        -   文档标签（tags）：可以在[应用数据](https://bailian.console.aliyun.com/#/data-center)页面查看非结构化文档的标签。也可以通过[DescribeFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-describefile)接口获取。
            
        -   文档元数据（metadata）：在[知识库](https://bailian.console.aliyun.com/#/knowledge-base)页面，进入某个知识库后可以查看非结构化文档的元数据（**Meta信息**）。
            
    -   可以传入多个文档ID，仅支持已建立知识索引的文档。
        
    -   传入文档ID时，需要同时传入文档所属的知识库ID，检索才会生效。
        
    -   只会在指定的文档里检索。例如：网页端的**智能体应用**里引用了知识库A，而API调用时指定了文档ID和其所属的知识库B的ID，那么不会检索知识库A的文档，只会检索知识库B的文档**_。_**
        
        此处示例选择[百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)作为非结构化数据知识库文件。
        
        ## Python
        
        **请求示例**
        
        ```
        import os
        from http import HTTPStatus
        # 建议dashscope SDK 的版本 >= 1.20.11
        from dashscope import Application
        response = Application.call(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            app_id='YOUR_APP_ID',  # 应用ID替换YOUR_APP_ID
            prompt='请帮我推荐一款3000元以下的手机',
            rag_options={
                "pipeline_ids": ["YOUR_PIPELINE_ID1", "YOUR_PIPELINE_ID2"],  # 替换为实际的知识库ID,逗号隔开多个
                "file_ids": ["YOUR_FILE_ID1", "YOUR_FILE_ID2"],  # 替换为实际的非结构化文档 ID,逗号隔开多个
                "metadata_filter": {  # 文档元数据键值对,逗号隔开多个
                    "key1": "value1",
                    "key2": "value2"
                },
                "tags": ["tag1", "tag2"]  # 文档标签,逗号隔开多个
            }
        )
        
        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}')
            print(f'code={response.status_code}')
            print(f'message={response.message}')
            print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        else:
            print('%s\n' % (response.output))
        ```
        
        **响应示例**
        
        ```
        {
            "text": "在3000元以下的预算范围内，我推荐您考虑**百炼 Zephyr Z9**。这款手机的特点如下：
        
        - **屏幕**：6.4英寸 1080 x 2340像素，适合日常使用和娱乐。
        - **内存与存储**：6GB RAM + 128GB 存储空间，能够满足大部分用户对于流畅度以及存储的需求。
        - **电池容量**：4000mAh，提供了一整天的使用保障。
        - **摄像头功能**：配备了一个支持30倍数字变焦的镜头，可以捕捉到更远距离的细节。
        - **其他特性**：设计轻薄便携，易于携带。
        
        参考售价为2499至2799元之间，正好符合您的预算要求，并且提供了不错的性价比。希望这些建议对您有所帮助！",
            "finish_reason": "stop",
            "session_id": "10bdea3d1435406aad8750538b701bee",
            "thoughts": null,
            "doc_references": null
        }
        ```
        
        ## Java
        
        **请求示例**
        
        ```
        // 建议dashscope SDK 的版本 >= 2.16.8；
        import com.alibaba.dashscope.app.*;
        import com.alibaba.dashscope.exception.ApiException;
        import com.alibaba.dashscope.exception.InputRequiredException;
        import com.alibaba.dashscope.exception.NoApiKeyException;
        import com.google.gson.JsonObject;
        import java.util.Arrays;
        
        public class Main {
            public static void streamCall() throws NoApiKeyException, InputRequiredException {
                JsonObject metadataFilter = new JsonObject();
                metadataFilter.addProperty("key1", "value1"); // 元数据键值对
                metadataFilter.addProperty("key2", "value2"); // 多个重复调用addProperty
                ApplicationParam param = ApplicationParam.builder()
                        // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .appId("YOUR_APP_ID") // 替换为实际的应用ID
                        .prompt("请帮我推荐一款3000元左右的手机")
                        .ragOptions(RagOptions.builder()
                                .pipelineIds(Arrays.asList("PIPELINES_ID1","PIPELINES_ID2"))  // 替换为实际指定的知识库ID，逗号隔开多个
                                .fileIds(Arrays.asList("FILE_ID1", "FILE_ID2"))  // 替换为实际指定的非结构化文档 ID，逗号隔开多个
                                .tags(Arrays.asList("tags1", "tags2")) // 替换为指定的文档标签 ID，逗号隔开多个
                                .metadataFilter(metadataFilter)
                                .build())
                        .build();
        
                Application application = new Application();
                ApplicationResult result = application.call(param);
                System.out.printf("%s\n",
                        result.getOutput().getText());// 处理只输出文本text
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
        根据您的预算，我为您推荐**百炼 Zephyr Z9**。这款手机的价格在2499-2799元之间，非常适合您3000元左右的预算范围。
        
        ### 百炼 Zephyr Z9 产品亮点：
        - **屏幕**：6.4英寸、1080 x 2340像素，提供清晰细腻的视觉体验。
        - **存储与运行内存**：128GB存储空间和6GB RAM，足以应对日常使用需求。
        - **电池**：4000mAh容量电池可以确保一整天的正常使用。
        - **摄像头**：支持30倍数字变焦镜头，能够捕捉远处细节。
        - **设计**：轻薄便携，适合追求时尚与便捷的用户。
        
        这款手机不仅价格适中，而且配置均衡，在外观设计上也非常出色，是这个价位段非常不错的选择。希望这些建议对您有所帮助！如果还有其他需求或疑问，请随时告诉我。
        ```
        
        ## HTTP
        
        ## curl
        
        **请求示例**
        
        ```
        curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{YOUR_APP_ID}/completion \
        --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
        --header 'Content-Type: application/json' \
        --data '{
            "input": {
                "prompt": "请帮我推荐一款3000元左右的手机"
            },
            "parameters":  {
                            "rag_options" : {
                            "pipeline_ids":["YOUR_PIPELINE_ID1"],
                            "file_ids":["YOUR_FILE_ID1"],
                            "metadata_filter":{
                            "name":"张三"},
                            "tags":"手机"
                            }
            },
            "debug": {}
        }'
        ```
        
        > YOUR\_APP\_ID替换为实际的应用 ID，YOUR\_PIPELINE\_ID1替换为指定的知识库ID，YOUR\_FILE\_ID1替换为指定的非结构化文档ID，metadata\_filter内的键值对替换为实际的元数据。
        
        **响应示例**
        
        ```
        {"output":{"finish_reason":"stop","session_id":"f2f114864dd24a458f923aab0ec99a1d",
        "text":"根据您的预算，我推荐您考虑“通义 Vivid 7”。它拥有 6.5 英寸 1080 x 2400 像素的全面屏，具备 AI 智能摄影功能，能够让您拍摄出具有专业级色彩与细节的照片。
        其硬件配置包括 8GB RAM 和 128GB 存储空间，确保了流畅的操作体验；4500mAh 的电池容量也能较好地满足日常使用需求。
        此外，侧面指纹解锁的设计既便捷又安全。参考售价为 2999 至 3299 元之间，符合您的预算范围。"},
        "usage":{"models":[{"output_tokens":141,"model_id":"qwen-plus","input_tokens":1610}]},
        "request_id":"d815d3d1-8cef-95e2-b895-89fc8d0e0f84"}%
        ```
        
        ## PHP
        
        **请求示例**
        
        ```
        <?php
        # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        $api_key = getenv("DASHSCOPE_API_KEY");
        $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
        
        $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
        
        // 构造请求数据
        $data = [
            "input" => [
                'prompt' => '请帮我推荐一款3000元以下的手机'
            ],
            "parameters" => [
                'rag_options' => [
                    'pipeline_ids' => ['YOUR_PIPELINE_ID1','YOUR_PIPELINE_ID2'],// 替换为指定的知识库ID,逗号隔开多个
                    'file_ids' => ['YOUR_FILE_ID1','YOUR_FILE_ID2'],// 替换为实际的文档 ID,逗号隔开多个
                    "metadata_filter" => [ // 元数据键值对
                        "key1" => "value1",
                        "key2" => "value2"
                    ],
                    "tags" => ["标签1", "标签2"] // 文档标签
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
        根据您的预算，我为您推荐**百炼 Zephyr Z9**。这款手机的参考售价在2499-2799元之间，非常适合3000元以下的需求。它拥有轻巧的6.4英寸1080 x 2340像素设计，搭配128GB存储与6GB RAM，可以满足日常使用需求。此外，其配备4000mAh电池确保一天无忧，并且还有30倍数字变焦镜头捕捉远处细节，是一款既轻薄又不失强大的选择。
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
            const appId = 'YOUR_APP_ID';//替换为实际的应用 ID
        
            const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
        
            const data = {
                input: {
                    prompt: "请帮我推荐一款3000元以下的手机"
                },
                parameters: {
                    rag_options:{
                        pipeline_ids:['YOUR_PIPELINE_ID1','YOUR_PIPELINE_ID2'], // 替换为指定的知识库ID，多个请用逗号隔开
                        file_ids:['YOUR_FILE_ID1','YOUR_FILE_ID2'], // 替换为指定的文件 ID，多个请用逗号隔开
                        metadata_filter:{ // 元数据键值对，多个请用逗号隔开
                            'key1':'value1',
                            'key2':'value2'
                        },
                        tags: ['标签1', '标签2'] // 文档标签，多个请用逗号隔开
                    }
                },
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
        在3000元以下的预算范围内，我推荐您考虑**百炼 Zephyr Z9**。这款手机的价格区间是2499-2799元，它拥有轻薄便携的设计，配备6.4英寸1080 x 2340像素屏幕、128GB存储与6GB RAM，能够满足日常使用需求。其4000mAh电池保证了一天的使用时间，而30倍数字变焦镜头则可以帮助捕捉到更远距离的细节。总体来说，这是一款性价比较高的选择。
        ```
        
        ## C#
        
        **请求示例**
        
        ```
        using System.Text;
        
        class Program
        {
            static async Task Main(string[] args)
            {
                // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
                string appId = "YOUR_APP_ID";// 替换为实际的应用 ID
                // YOUR_PIPELINE_ID1替换为指定的知识库ID,YOUR_FILE_ID1替换为指定的非结构化文档 ID
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
                            ""prompt"": ""请帮我推荐一款3000元以下的手机""
                        }},
                        ""parameters"": {{
                            ""rag_options"" : {{
                                ""pipeline_ids"":[""YOUR_PIPELINE_ID1""],
                                ""file_ids"":[""YOUR_FILE_ID1""],
                                ""metadata_filter"":{{
                                    ""name"":""张三""
                                }},
                        ""tags"":""手机""
                            }}
                        }},
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
                "session_id": "be9b5a1964fe41c9bbfd8674226bd238",
                "text": "根据您的预算，我为您推荐**百炼 Zephyr Z9**。这款手机售价在2499-2799元之间，非常适合3000元以下的预算要求。
        
        ### 产品亮点
        - **轻薄设计**：采用6.4英寸屏幕，分辨率1080 x 2340像素，外观精致且便于携带。
        - **性能均衡**：配备6GB RAM和128GB存储空间，能够满足日常使用需求。
        - **长效续航**：内置4000mAh电池，确保您一整天的正常使用不受影响。
        - **出色摄影**：支持30倍数字变焦功能，轻松捕捉远方美景或细节。
        
        如果您追求的是性价比高、能满足基本需求同时又具备一定特色的智能手机，那么百炼 Zephyr Z9将是一个不错的选择。"
            },
            "usage": {
                "models": [
                    {
                        "output_tokens": 180,
                        "model_id": "qwen-max",
                        "input_tokens": 1055
                    }
                ]
            },
            "request_id": "d0811195-0b3f-931e-90b8-323a65053d9c"
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
        	appId := "YOUR_APP_ID" // 替换为实际的应用 ID
        
        	if apiKey == "" {
        		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
        		return
        	}
        
        	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)
        
        	// 创建请求体
        	requestBody := map[string]interface{}{
        		"input": map[string]string{
        			"prompt": "请帮我推荐一款3000元以下的手机",
        		},
        		"parameters": map[string]interface{}{
        			"rag_options": map[string]interface{}{
        				"pipeline_ids": []string{"YOUR_PIPELINE_ID1"}, // 替换为指定的非结构化知识库ID
        				"file_ids":     []string{"YOUR_FILE_ID1"},     // 替换为指定的非结构化文档 ID
        				"metadata_filter": map[string]string{
        					"name": "张三", // 元数据键值对
        				},
        				"tags": "手机", // 非结构化数据文档标签
        			},
        		},
        		"debug": map[string]interface{}{},
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
                "session_id": "9de268b3d84748b5ac6321aba72b6ecd",
                "text": "根据您的预算，我推荐您考虑**百炼 Zephyr Z9**。这款手机的参考售价为2499-2799元，非常适合3000元以下的需求。它具有以下特点：
        
        - 轻巧的6.4英寸1080 x 2340像素屏幕设计。
        - 搭配128GB存储与6GB RAM，能够满足日常使用需求。
        - 配备了4000mAh电池，保证了一天的正常使用。
        - 后置摄像头支持30倍数字变焦镜头，可以捕捉到远处的细节。
        
        如果您对摄影或者游戏没有特别高的要求，那么百炼 Zephyr Z9应该是一个不错的选择。"
            },
            "usage": {
                "models": [
                    {
                        "output_tokens": 156,
                        "model_id": "qwen-max",
                        "input_tokens": 1055
                    }
                ]
            },
            "request_id": "8940b597-92e1-9471-b4eb-896e563c479d"
        }
        ```
        
3.  检索**结构化数据**文档里的指定数据：在`rag_options`中传入知识库ID、结构化数据文档的“结构化数据表头+值”的键值对。
    
    获取结构化数据键值对（structured\_filter）：在[知识库](https://bailian.console.aliyun.com/#/knowledge-base)页面，进入某个知识库后可以单击**查看索引**查看结构化文档的索引信息。
    
    ## Python
    
    **请求示例**
    
    ```
    import os
    from http import HTTPStatus
    # 建议dashscope SDK 的版本 >= 1.20.11
    from dashscope import Application
    
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='YOUR_APP_ID',  # 应用ID替换YOUR_APP_ID
        prompt='请帮我推荐一款3000元以下的手机',
        rag_options={
            "pipeline_ids": ["YOUR_PIPELINE_ID1", "YOUR_PIPELINE_ID2"],  # 替换为实际的知识库ID,逗号隔开多个
             "structured_filter": {  # 结构化数据键值对，对应结构化数据,逗号隔开多个
                "key1": "value1",
                "key2": "value2"  
             }
        }
    )
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n' % (response.output))
    ```
    
    **响应示例**
    
    ```
    {
        "text": "我为您推荐"百炼"这款手机，它的价格是2999元，符合您的预算要求。如果您需要了解更多信息，比如性能、外观等，请告诉我。",
        "finish_reason": "stop",
        "session_id": "80a3b868b5ce42c8a12f01dccf8651e2",
        "thoughts": null,
        "doc_references": null
    }
    ```
    
    ## Java
    
    **请求示例**
    
    ```
    // 建议dashscope SDK 的版本 >= 2.16.8；
    import com.alibaba.dashscope.app.*;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.google.gson.JsonObject;
    import java.util.Arrays;
    
    public class Main {
        public static void streamCall() throws NoApiKeyException, InputRequiredException {
            JsonObject structureFilter = new JsonObject();
            structureFilter.addProperty("key1", "value1"); // 结构化数据键值对
            structureFilter.addProperty("key2", "value2"); // 多个重复调用addProperty
            ApplicationParam param = ApplicationParam.builder()
                    // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .appId("YOUR_APP_ID") // 替换为实际的应用ID
                    .prompt("请帮我推荐一款3000元左右的手机")
                    .ragOptions(RagOptions.builder()
                            .pipelineIds(Arrays.asList("PIPELINE_ID1","PIPELINE_ID2"))  // 替换为实际指定的知识库ID，逗号隔开多个
                            .structuredFilter(structureFilter)
                            .build())
                    .build();
    
            Application application = new Application();
            ApplicationResult result = application.call(param);
            System.out.printf("%s\n",
                    result.getOutput().getText());// 处理只输出文本text
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
    我为您推荐"百炼"这款手机，它的价格是2999.0元，符合您的预算要求。如果您需要了解更多关于这款手机的信息，比如配置、性能等，请告诉我，我会为您提供更详细的资料。
    ```
    
    ## HTTP
    
    ## curl
    
    **请求示例**
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {
            "prompt": "请帮我推荐一款3000元左右的手机"
        },
        "parameters":  {
                        "rag_options" : {
                        "pipeline_ids":["YOUR_PIPELINE_ID1"],
                        "structured_filter":{
                        "price":"2999"}
                        }
        },
        "debug": {}
    }'
    ```
    
    > YOUR\_APP\_ID替换为实际的应用 ID，YOUR\_PIPELINE\_ID1替换为指定的知识库ID。
    
    **响应示例**
    
    ```
    {"output":{"finish_reason":"stop","session_id":"d6bc4206f9cc4d368d534f8aa4e502bc",
    "text":"我为您推荐一款价格接近3000元的手机：\n\n- **百炼手机**，价格为2999元。
    \n\n这款手机性价比高，能满足您的预算需求。
    如果您需要更多关于这款手机的详细信息或者有其他特定需求（比如摄像头性能、处理器型号等），请告诉我，我会尽力提供更详尽的信息。"},
    "usage":{"models":[{"output_tokens":73,"model_id":"qwen-max","input_tokens":235}]},"request_id":"934e1258-219c-9ef1-8982-fc1bcefb8f11"}%
    ```
    
    ## PHP
    
    **请求示例**
    
    ```
    <?php
    # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
    
    $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
    
    // 构造请求数据
    $data = [
        "input" => [
            'prompt' => '请帮我推荐一款3000元以下的手机'
        ],
        "parameters" => [
            'rag_options' => [
                'pipeline_ids' => ['YOUR_PIPELINE_ID1','YOUR_PIPELINE_ID2'],// 替换为指定的知识库ID,逗号隔开多个
                "structured_filter" => [ // 结构化数据键值对,多个逗号隔开
                    "key1" => "value1",
                    "key2" => "value2"
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
    我为您推荐"百炼"这款手机，它的价格是2999元，符合您的预算要求。如果您需要了解更多关于这款手机的信息，请告诉我。
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
        const appId = 'YOUR_APP_ID';  // 替换为实际的应用 ID
        // YOUR_PIPELINE_ID1替换为指定的知识库ID, 多个知识库ID之间用逗号隔开
        const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    
        const data = {
            input: {
                prompt: "请帮我推荐一款3000元以下的手机"
            },
            parameters: {
                rag_options:{
                    pipeline_ids:['YOUR_PIPELINE_ID1','YOUR_PIPELINE_ID2'],
                    structured_filter:{
                        'key1':'value1',
                        'key2':'value2'
                    }
                }
            },
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
    我为您推荐"百炼"这款手机，它的价格是2999元，符合您的预算要求。如果您需要了解更多详情或有其他特定需求，请告诉我！
    ```
    
    ## C#
    
    **请求示例**
    
    ```
    using System.Text;
    
    class Program
    {
        static async Task Main(string[] args)
        {
            // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
            string appId = "YOUR_APP_ID";// 替换为实际的应用ID
            // YOUR_PIPELINE_ID1替换为指定的知识库ID
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
                        ""prompt"": ""请帮我推荐一款3000元以下的手机""
                    }},
                    ""parameters"": {{
                        ""rag_options"" : {{
                            ""pipeline_ids"":[""YOUR_PIPELINE_ID1""],
                            ""structured_filter"":{{
                                ""price"":""2999""
                            }}
                        }}
                    }},
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
            "session_id": "108e9104568e44f1915fb3d3d44fdc92",
            "text": "我为您推荐"百炼"这款手机，它的价格是2999.0元，符合您的预算要求。如果您需要更多关于这款手机的信息或者其他建议，请告诉我。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 38,
                    "model_id": "qwen-max",
                    "input_tokens": 104
                }
            ]
        },
        "request_id": "d6d103f4-5c22-9782-9682-45d51a5607f9"
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
    	appId := "YOUR_APP_ID" // 替换为实际的应用 ID
    
    	if apiKey == "" {
    		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
    		return
    	}
    
    	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)
    
    	// 创建请求体
    	requestBody := map[string]interface{}{
    		"input": map[string]string{
    			"prompt": "请帮我推荐一款3000元以下的手机",
    		},
    		"parameters": map[string]interface{}{
    			"rag_options": map[string]interface{}{
    				"pipeline_ids": []string{"YOUR_PIPELINE_ID1"}, // 替换为指定的结构化知识库ID
    				"structured_filter": map[string]string{
    					"price": "2999", // 结构化数据键值对
    				},
    			},
    		},
    		"debug": map[string]interface{}{},
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
            "session_id": "9e0a031b51d1492e8b613ca391b445b0",
            "text": "我推荐您考虑"百炼"这款手机，它的价格是2999.0元，符合您的预算要求。如果您需要更多关于这款手机的信息或者其他推荐，请告诉我。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 39,
                    "model_id": "qwen-max",
                    "input_tokens": 104
                }
            ]
        },
        "request_id": "036abd4f-10c8-9709-881d-8cc9f8095d54"
    }
    ```
    

#### **查看信息**

-   **查看检索过程信息：**调用时在代码中添加`has_thoughts`并设置为True，则检索的过程信息会在`output`的`thoughts`字段中返回。
    
-   **查看回答来源信息：**单击**知识库**开关旁的**配置**，在页面中打开**展示回答来源**开关，然后**发布**应用，可在调用的返回结果中查看回答来源。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2935773571/p949493.png)
    

### **深度思考**

如果您在**智能体应用**内选择了[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking#5be853b164zv4)，并成功**发布**应用，则：

**开启思考模式**：

要开启思考模式并接收其输出，您可通过以下两种方式进行相应设置。

1.  **控制台设置**
    
    **对于 Qwen3 模型**：在控制台应用内，确保**思考模式**开关已打开，然后重新**发布**应用。
    
    **对于其他模型**：默认开启思考模式，无需额外操作。
    
2.  **API 调用参数设置**
    
    **对于 Qwen3 模型**：将enable\_thinking参数设置为 true。
    
    对于其他模型：enable\_thinking参数无效。
    

**重要**

优先级：若两种方式同时设置，则以API参数为准。

**获取思考过程：**

-   将has\_thoughts参数设置为 true。
    

**处理返回结果**：

-   **思考过程**：将在响应的 `thought` 字段中返回。
    
-   **最终回复**：将在响应的 `text` 字段中返回。
    

深度思考模型可能会输出较长的思考过程，为了降低超时风险，建议您使用流式输出方式调用应用，参考下方示例。

## Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application

try:
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        app_id='YOUR_APP_ID',# 替换为实际的应用 ID
        prompt='你是谁？',# 替换为实际的应用输入
        stream=True,  # 是否流式输出，True：流式输出；False（默认值）: 非流式输出
        incremental_output=True,  # 是否增量输出，True：增量输出；False（默认值）: 非增量输出
        has_thoughts=True  # 是否返回思考过程，True：返回；False（默认值）: 不返回
    )

except Exception as e:
    print(f"API请求异常: {str(e)}")
    exit(1)

# 定义完整思考过程
reasoning_content = []
# 定义完整回复
answer_content = ""
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
    if not chunk.output or (not chunk.output.thoughts and not chunk.output.text):
        continue

    # 处理思考过程
    if chunk.output.thoughts:
        for it in chunk.output.thoughts:
            if it.action_type == 'reasoning':# deepseek-r1类模型的思考过程action_type为reasoning，输出在thought
                content = str(it.thought) if not isinstance(it.thought, str) else it.thought
                reasoning_content.append(content)
                print(content, end="", flush=True)

    # 处理回答内容
    if chunk.output.text:
        if not is_answering:
            print_section("完整回复")
            is_answering = True
        
        answer_content += str(chunk.output.text)
        print(chunk.output.text, end="", flush=True)

# 最终结果整合
final_reasoning = "".join(reasoning_content)
final_answer = "".join(answer_content)

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
#print_section("完整思考过程")
#print(final_reasoning)

#print_section("完整回复")
#print(final_answer)
```

**响应示例**

```
==================== 思考过程 ====================

嗯，用户问我“你是谁？”，我需要用中文回答。首先，我得介绍自己是一个AI助手，由DeepSeek公司开发。然后要说明我的功能，比如回答问题、提供信息、帮助学习等。要记得保持口语化，不用太正式。还要注意用户可能想了解我的背景，所以可以提到基于大语言模型，但不用太技术化。另外，用户可能在测试我的回答能力，所以需要简洁明了，同时友好自然。可能需要检查有没有遗漏的关键点，比如公司的正确名称，以及是否强调帮助性质。最后确保回答符合格式要求，不使用markdown，保持段落结构清晰。
==================== 完整回复 ====================

您好！我是DeepSeek-R1，一个由深度求索（DeepSeek）公司开发的智能助手，我会尽我所能为您提供帮助，包括回答问题、信息查询以及学习辅助等。
```

## Java

**请求示例**

```
// 建议dashscope SDK的版本 >= 2.15.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;// 流式输出
// 智能体应用调用实现流式输出结果

public class Main {
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 替换为实际的应用 ID
                .appId("YOUR_APP_ID")
                .prompt("你好")
                .hasThoughts(true)
                // 增量输出
                .incrementalOutput(true)
                .build();
        Application application = new Application();
        // .streamCall（）：流式输出内容
        Flowable<ApplicationResult> result = application.streamCall(param);
        result.blockingForEach(data -> {
            System.out.printf("%s\n",
                    data.getOutput());
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
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=好的，用户, actionType=reasoning, response=好的，用户, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=打招呼, actionType=reasoning, response=打招呼, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=说, actionType=reasoning, response=说, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=“你好”，我需要友好, actionType=reasoning, response=“你好”，我需要友好, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=回应。首先，, actionType=reasoning, response=回应。首先，, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=要确认用户的需求，, actionType=reasoning, response=要确认用户的需求，, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=可能只是测试或者想, actionType=reasoning, response=可能只是测试或者想, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=开始对话。要, actionType=reasoning, response=开始对话。要, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=保持热情，用, actionType=reasoning, response=保持热情，用, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=中文回复。可以, actionType=reasoning, response=中文回复。可以, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=问他们需要什么, actionType=reasoning, response=问他们需要什么, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=帮助，或者有没有具体, actionType=reasoning, response=帮助，或者有没有具体, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=的问题。同时，注意, actionType=reasoning, response=的问题。同时，注意, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=使用合适的表情符号增加, actionType=reasoning, response=使用合适的表情符号增加, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=亲切感。检查, actionType=reasoning, response=亲切感。检查, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=有没有需要特别注意的地方，, actionType=reasoning, response=有没有需要特别注意的地方，, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=比如用户是否有特殊身份, actionType=reasoning, response=比如用户是否有特殊身份, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=或需求，但目前, actionType=reasoning, response=或需求，但目前, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=看起来是普通问候。简单, actionType=reasoning, response=看起来是普通问候。简单, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=回应即可，避免, actionType=reasoning, response=回应即可，避免, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=复杂句子。保持, actionType=reasoning, response=复杂句子。保持, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=自然，让用户觉得, actionType=reasoning, response=自然，让用户觉得, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=被重视。

现在, actionType=reasoning, response=被重视。

现在, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=组织语言：欢迎, actionType=reasoning, response=组织语言：欢迎, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=用户，询问需要, actionType=reasoning, response=用户，询问需要, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=什么帮助。使用, actionType=reasoning, response=什么帮助。使用, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=友好表情符号，比如笑脸, actionType=reasoning, response=友好表情符号，比如笑脸, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=。确保用词, actionType=reasoning, response=。确保用词, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=简洁，让对话, actionType=reasoning, response=简洁，让对话, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=容易继续下去。比如, actionType=reasoning, response=容易继续下去。比如, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=：“你好！有什么我可以, actionType=reasoning, response=：“你好！有什么我可以, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=帮助你的吗？”, actionType=reasoning, response=帮助你的吗？”, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought= 这样既, actionType=reasoning, response= 这样既, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=直接又开放，, actionType=reasoning, response=直接又开放，, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=鼓励用户进一步交流, actionType=reasoning, response=鼓励用户进一步交流, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=。, actionType=reasoning, response=。, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=你好！有什么, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=, actionType=reasoning, response=, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=我可以帮助你的吗？, finishReason=null, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=, actionType=reasoning, response=, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
ApplicationOutput(text=, finishReason=stop, sessionId=380427d07790470c8e63e0d28dfa98bb, thoughts=[ApplicationOutput.Thought(thought=, actionType=reasoning, response=, actionName=思考过程, action=reasoning, actionInputStream=null, actionInput=null, observation=null)], docReferences=null, workflowMessage=null)
```

## curl

-   YOUR\_APP\_ID替换为实际的应用ID。
    
-   如需直接传入 API Key，请将$DASHSCOPE\_API\_KEY 替换为您的 API Key。
    
-   请指定Header中的 **X-DashScope-SSE** 为 **enable，**表示流式输出回复。
    
-   请在`parameters`对象中添加`has_thoughts`参数，表示是否返回思考过程，true：返回；false（默认值）：不返回。
    
-   请在`parameters`对象中添加`incremental_output`数，表示是否增量输出，true：增量输出；false（默认值）：非增量输出。
    

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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

**检索知识库**

-   模型思考过程在`thoughts`的`thought`中返回，模型思考的`action_type`为`reasoning`；
    
-   检索过程在`thoughts`的`observation`中返回，检索的`action_type`为`agentRag`。
    

可通过`action_type`区分不同过程，处理输出内容。

### **长期记忆**

阿里云百炼的**智能体应用**在和您进行对话时，能够记住一定长度的对话记录，但由于大模型注意力机制的限制，可能会忘记某些信息。为了解决这个问题，您可以将对话过程中的特定信息存储到长期记忆中，应用将在后续对话中持续引用这些信息。

**使用步骤**

**步骤 1: 激活**[长期记忆](https://help.aliyun.com/zh/model-studio/long-term-memory)**功能**

访问**[应用管理](https://bailian.console.aliyun.com/#/app-center)**页面，找到您的智能体应用，打开**长期记忆**功能开关，并**发布**应用。

**步骤 2: 创建长期记忆体**

调用[CreateMemory](https://help.aliyun.com/zh/model-studio/developer-reference/api-bailian-2023-12-29-creatememory?spm=a2c4g.11186623.0.0.586c6610Kg0bkj)接口，创建一个长期记忆体，从响应中获得一个唯一的`memoryId`。

**步骤 3: 保存对话信息**

调用时传入之前获得的`memoryId`，系统会自动分析并提取您对话中的关键信息，这些信息将被保存为与该`memoryId`关联的记忆内容。

**步骤 4: 使用长期记忆进行对话**

每次与智能体交流时提供相同的`memoryId`，系统会根据提供的`memoryId`召回相应的记忆内容，并将其与当前提问一起传递给模型生成答案。

**调用示例**

## Python

**请求示例（生成记忆体内容）**

```
# DashScope SDK版本不低于1.22.1
from http import HTTPStatus
import os
from dashscope import Application
response = Application.call(
           # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            app_id='YOUR_APP_ID',  # 请输入实际的应用 ID
            prompt='用户饮食偏好：面食',
            memory_id='YOUR_MEMORY_ID')  # 请输入实际的记忆体 ID

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print('%s\n' % (response.output.text))  # 处理只输出text
    # print('%s\n' % (response.usage))
```

**响应示例**

```
了解了，您对面食情有独钟。如果想要推荐或者寻找面食相关的食谱、餐厅等信息，请告诉我更多细节，比如是想吃哪种类型的面条（如拉面、意大利面等），还是有什么特别的口味偏好？这样我能更好地为您提供帮助。
```

**请求示例（再次调用）**

```
# DashScope SDK版本不低于1.22.1
from http import HTTPStatus
import os
from dashscope import Application
response = Application.call(
           # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            app_id='YOUR_APP_ID',  # 请输入实际的应用 ID
            prompt='美食推荐',
            memory_id='YOUR_MEMORY_ID')  # 请输入实际的记忆体 ID

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
    print('%s\n' % (response.output.text))  # 处理只输出text
    # print('%s\n' % (response.usage))
```

**响应示例**

```
既然您偏好面食，我推荐您可以尝试一下几种美食：

1. **炸酱面**：经典的北京风味，面条搭配特制的黄豆酱和肉末，口感丰富。
2. **担担面**：四川特色，辣中带麻，非常开胃。如果您喜欢尝试一些稍微刺激一点的味道，这会是个不错的选择。
3. **刀削面**：山西的传统名吃之一，以其独特的制作方法——用刀将面团直接削入锅中煮熟而得名，口感劲道。
4. **意大利面**：如果想要换换口味的话，不妨试试西式的意面，比如番茄肉酱意面或是奶油培根意面等，都是不错的选择。

希望这些建议对您有所帮助！如果有更具体的口味偏好或其他需求，请随时告诉我哦~
```

## Java

**请求示例（生成记忆体内容）**

```
// DashScope SDK版本不低于2.17.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void callWithMemory() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("YOUR_APP_ID") // 替换为实际的应用 ID
                .prompt("用户饮食偏好：面食")
                .memoryId("YOUR_MEMORY_ID") // 替换为实际的记忆体 ID
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf("%s\n",
                result.getOutput().getText()); // 处理只输出文本text
    }
    public static void main(String[] args) {
        try {
            callWithMemory();
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
了解了，您对面食情有独钟。如果您需要面食的推荐、做法或者是哪里可以吃到美味的面食，请告诉我，我很乐意为您提供帮助！
```

**请求示例（再次调用）**

```
// DashScope SDK版本不低于2.17.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void callWithMemory() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .appId("YOUR_APP_ID") // 替换为实际的应用 ID
                .prompt("美食推荐")
                .memoryId("YOUR_MEMORY_ID") // 替换为实际的记忆体 ID
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf("text: %s\n",
                result.getOutput().getText()); // 处理只输出文本text
    }
    public static void main(String[] args) {
        try {
            callWithMemory();
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
既然您偏好面食，这里有一些美味的面食推荐给您：

1. **炸酱面**：北京的传统美食，用黄豆酱和肉末制成的炸酱，搭配黄瓜丝、豆芽等蔬菜，味道鲜美。
2. **担担面**：四川特色小吃，以麻辣著称，面条细滑，汤汁浓郁，上面撒上花生碎和葱花，非常开胃。
3. **刀削面**：山西的传统面食，面条宽厚有嚼劲，通常搭配各种肉类和蔬菜炖煮的汤底，口感丰富。
4. **油泼面**：陕西地区的经典面食，将手工拉制的面条煮熟后，淋上热油和辣椒粉，再加上酱油、醋等调料，香气扑鼻。
5. **意面**：如果想尝试一些西式面食，可以试试意大利面，如经典的番茄肉酱面或是奶油培根意面，都非常受欢迎。

希望这些建议能让您满意！如果您有任何特殊需求或想要尝试特定类型的面食，请告诉我。
```

## HTTP

## curl

**请求示例（生成记忆体内容）**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "用户饮食偏好：面食",
        "memory_id": "YOUR_MEMORY_ID"
    },
    "parameters":  {},
    "debug": {}
}'
```

> YOUR\_APP\_ID替换为实际的应用 ID。

**响应示例**

```
{
    "output": {
        "finish_reason": "stop",
        "session_id": "36ca92e5689f4dfbab889525da8a784b",
        "text": "了解了，您偏好面食。那么在推荐美食或者提供饮食建议时，我会更多地考虑到各种面食的选择。请问您有特别喜欢的面食种类吗？比如拉面、意大利面或者是某种地方特色的面条？或者，如果您需要一些建议来尝试新的面食，我也很乐意提供帮助！"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 70,
                "model_id": "qwen-max",
                "input_tokens": 119
            }
        ]
    },
    "request_id": "050acdc4-d427-969e-8ba8-aa95075c2d9a"
}
```

**请求示例（再次调用）**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "美食推荐",
        "memory_id": "YOUR_MEMORY_ID"
    },
    "parameters":  {},
    "debug": {}
}'
```

> YOUR\_APP\_ID替换为实际的应用 ID。

**响应示例**

```
{"output":{"finish_reason":"stop",
"session_id":"12677d7f5e5d423ca30db6ff77a4710d",
"text":"考虑到您对面食的偏爱，我为您推荐几种不同风味的面食佳肴：\n\n
1. **北京炸酱面**：经典的北方面食，以黄豆酱和肉酱为主料，搭配黄瓜丝、豆皮等配菜，口感丰富，酱香浓郁。\n\n
2. **四川担担面**：辣味爱好者必试，特制的辣椒油与花生碎、芽菜混合，再加入炒制的猪肉末，麻辣鲜香，十分过瘾。\n\n
3. **山西刀削面**：以其独特的制作工艺著称，面条宽厚有嚼劲，搭配各种浇头如番茄鸡蛋、牛肉等，味道醇厚。\n\n
4. **陕西凉皮**：虽然严格意义上属于小吃，但作为面食的一种变异，其酸辣爽口，搭配面筋、黄瓜丝等，非常适合夏天食用。\n\n
5. **江南阳春面**：简单而精致，清汤搭配细面条，上面撒上葱花、少许猪油，口味清淡却不失鲜美。\n\n
6. **意大利面**：如果想尝试异国风味，可以选择经典的意式番茄肉酱面或是奶油蘑菇意面，体验不同的面条文化。\n\n
希望这些建议能满足您的味蕾，不妨根据自己的口味选择尝试一下！"},
"usage":{"models":[{"output_tokens":269,"model_id":"qwen-max","input_tokens":139}]},
"request_id":"f7792da2-02f6-999c-85f1-a76de85fb99f"}%
```

**异常响应示例**

```
{"code":"InvalidApiKey","message":"Invalid API-key provided.","request_id":"2637fcf9-32b1-9f4e-b0e9-1724d4aea00e"}
```

## PHP

**请求示例（生成记忆体内容）**

```
<?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
$memory_id = 'YOUR_MEMORY_ID'; // 替换为实际的记忆体 ID
$url = "https://dashscope.aliyuncs.com/api/v1/apps/{$application_id}/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '用户饮食偏好：面食',
        'memory_id' => $memory_id
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
了解了，您对面食情有独钟。如果您正在寻找新的面食食谱或是想要知道哪里可以吃到美味的面食，请告诉我更多细节，我会尽力提供帮助！比如，您是想在家自己动手做还是打算外出就餐呢？
```

**请求示例（再次调用）**

```
<?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv("DASHSCOPE_API_KEY");
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
$memory_id = 'YOUR_MEMORY_ID'; // 替换为实际的记忆体 ID
$url = "https://dashscope.aliyuncs.com/api/v1/apps/{$application_id}/completion";

// 构造请求数据
$data = [
    "input" => [
        'prompt' => '美食推荐',
        'memory_id' => $memory_id
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
既然您偏好面食，这里有一些建议您可以尝试的美味面食：

1. **炸酱面** - 一道经典的北京风味面食，主要以黄豆酱和肉末制成的炸酱拌面条，非常香浓可口。
2. **刀削面** - 来自山西的一种特色面条，以其独特的制作工艺——师傅手持面团直接削入滚水中而得名。搭配各种汤底或调料都非常好吃。
3. **担担面** - 四川省的传统小吃之一，特点是麻辣鲜香，通常会加入特制辣椒油、花生碎等材料提味。
4. **兰州拉面** - 起源于甘肃省兰州市，以其手工拉制而成细长且富有弹性的面条著称，常配以牛肉高汤、几片薄牛肉以及葱花等。

希望这些建议能给您带来灵感！如果您有特别想了解的地方或是其他需求，请告诉我。
```

## Node.js

**需安装相关依赖：**

```
npm install axios
```

**请求示例（生成记忆体内容）**

```
const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
    const memoryId = 'YOUR_MEMORY_ID';// 替换为实际的memory_id

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "用户饮食偏好：面食",
            memory_id: memoryId
        },
        parameters: {},
        debug: {}
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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
解了，您对面食情有独钟。如果您想要尝试一些新的面食菜品或是寻找某个特定地方的特色面食，请告诉我，我很乐意为您提供一些建议！
```

**请求示例（再次调用）**

```
const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
    const memoryId = 'YOUR_MEMORY_ID';// 替换为实际的memory_id

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: "美食推荐",
            memory_id: memoryId
        },
        parameters: {},
        debug: {}
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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
```

**响应示例**

```
既然您偏好面食，这里有一些建议供您参考：

1. **刀削面**：这种面条以其独特的口感和形状闻名，可以搭配各种美味的汤底和配料。
2. **担担面**：四川风味的辣味面条，用花生酱、辣椒油等调料制成，味道鲜美而富有层次感。
3. **炸酱面**：北京的传统美食之一，主要由黄豆酱炒肉末制成的酱料拌入煮好的面条中食用。
4. **意大利面**：如果您想尝试一些不同的口味，可以选择意式面食。比如番茄肉酱意面或是奶油蘑菇意面等。

希望这些建议对您有所帮助！如果还有其他需求或想要更具体的推荐，请告诉我。
```

## C#

**请求示例（生成记忆体内容）**

```
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
        string appId = "YOUR_APP_ID";// 替换为实际的应用ID
        string memoryId = "YOUR_MEMORY_ID";//替换为实际的memory_id
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
                    ""prompt"": ""用户饮食偏好：面食"",
                    ""memory_id"":""{memoryId}""
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
        "session_id": "c24255e945b94f22bc3fe5fb515177c3",
        "text": "了解了，您偏好面食。如果想要推荐或寻找一些好吃的面食菜品或餐厅，请告诉我更多的细节，比如您现在的位置、想尝试哪种风味（如川味、北方菜等），或者是否有特别的需求（例如素食选项）。这样我能更好地为您提供帮助。"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 59,
                "model_id": "qwen-max",
                "input_tokens": 146
            }
        ]
    },
    "request_id": "f732635f-3082-9dfe-9c09-df679d6d5b2e"
}
```

**请求示例（再次调用）**

```
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
        string appId = "YOUR_APP_ID";// 替换为实际的应用ID
        string memoryId = "YOUR_MEMORY_ID";//替换为实际的memory_id
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
                    ""prompt"": ""美食推荐"",
                    ""memory_id"":""{memoryId}""
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
        "session_id": "665c16a3d10b48a0bb0ba92d42b6707b",
        "text": "既然您对面食情有独钟，这里有一些建议供您参考：

1. **担担面** - 来自四川的传统美食，以其麻辣鲜香著称。
2. **炸酱面** - 北京特色小吃之一，以黄豆酱或甜面酱炒肉末作为主要调料。
3. **刀削面** - 山西的代表性面食，面条宽厚、口感劲道。
4. **热干面** - 湖北武汉地区的传统早点，以芝麻酱为主要调料。
5. **牛肉拉面** - 甘肃兰州最著名的风味小吃之一，汤清味美。

如果您想要尝试其他类型的美食但仍然希望包含一些面食元素的话，也可以考虑意大利面或者日式乌冬面等国际化的选择。希望这些建议能够帮到您！如果有特定口味偏好的话，请告诉我，我可以提供更加个性化的建议。"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 196,
                "model_id": "qwen-max",
                "input_tokens": 142
            }
        ]
    },
    "request_id": "305c5058-708e-94ce-b8ee-3bf539e5f35c"
}
```

## Go

**请求示例（生成记忆体内容）**

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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]string{
			"prompt":    "用户饮食偏好：面食",
			"memory_id": "YOUR_MEMORY_ID", // 替换为实际的记忆体 ID
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
        "session_id": "2e2ac5be49d2469794f310a92f34c9c7",
        "text": "了解了，您对面食情有独钟。如果您想要一些面食的推荐或是寻找特定类型的面食食谱，请告诉我，我很乐意帮助您！比如，您是想了解中式面条、意大利面还是其他种类的面食呢？"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 53,
                "model_id": "qwen-max",
                "input_tokens": 119
            }
        ]
    },
    "request_id": "3f1c66ba-1d19-98f2-89a5-4c3b53c80258"
}
```

**请求示例（再次调用）**

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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

	if apiKey == "" {
		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
		return
	}

	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		"input": map[string]string{
			"prompt":    "美食推荐",
			"memory_id": "YOUR_MEMORY_ID", // 替换为实际的记忆体 ID
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
        "session_id": "dcb3e991be904cfcb11b9b06109d4c73",
        "text": "既然您偏好面食，那我推荐几种不同风格的面食供您选择：

1. **炸酱面**：这是北京的传统名吃之一，面条劲道，搭配特制的肉酱，味道鲜美。
2. **担担面**：源自四川，以其麻辣味闻名，面条细软，加上花生碎和特制辣酱，十分开胃。
3. **刀削面**：山西特色美食，面条宽厚且有嚼劲，通常与各种肉类和蔬菜一起炖煮。
4. **意大利面**：如果想尝试国际风味的话，可以选择意面，比如经典的番茄肉酱意面或奶油蘑菇鸡肉意面等。

希望这些建议对您有所帮助！如果您更倾向于某种特定口味或是想要了解更多细节，请告诉我。"
    },
    "usage": {
        "models": [
            {
                "output_tokens": 167,
                "model_id": "qwen-max",
                "input_tokens": 142
            }
        ]
    },
    "request_id": "08b629ce-b3dd-96b6-8177-6443893e0b66"
}
```

### **上传文件（文档、图片、视频或音频）**

在**智能体应用**内，您可上传文件（文档、图片、视频或音频），并基于文件内容进行问答。

#### **使用场景**

-   **文本解析**：解析文档、图片、视频或音频中的**文字内容**，结合大模型回答问题。
    
-   **视觉理解**：通过**通义千问VL系列模型**分析图片中的**图像内容**（如物体、场景、动作等），无需依赖文字信息。
    

如需在控制台操作上传文件并与大模型进行问答请参阅[上传文件](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction?spm=a2c4g.11186623.help-menu-search-2400256.d_0)。

API方式操作请参阅以下内容。

#### **文本解析**

**步骤一：准备文件**

待上传的文件需满足以下要求。

支持上传的文件上限10个。支持上传本地的文档、图片、视频或音频，格式要求为：

-   文档（单文件不超过100MB）：.doc,.docx,.wps,.ppt,.pptx,.xls,.xlsx,.md,.txt,.pdf；
    
-   图片（单文件不超过20MB）：.png,.jpg,.jpeg,.bmp,.gif；
    
    目前仅支持上传包含文字内容的本地图片。
    
-   视频（单文件不超过512MB）：.mp4,.mkv,.avi,.mov,.wmv；
    
-   音频（单文件不超过512MB）：.aac,.amr,.flac,.flv,.m4a,.mp3,.mpeg,.ogg,.opus,.wav,.webm,.wma。
    

##### **步骤二：获取会话文件ID**

1.  通过本文的[通过API接口获取会话文件ID](#2ad4ec64f2dwv)获取以“file\_session”开头的会话文件ID；
    
2.  验证文件状态为FILE\_IS\_READY。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2073150671/CAEQWhiBgICSiLDquBkiIDA3ODdmMzY4NTMyNTQ5OGE4NWM4MThjNTM5YTMwZjE05224266_20250529113200.258.svg)

**步骤三：API调用应用**

1.  在控制台**智能体应用**内选择任一模型，开启**动态文件解析**开关，并**发布**应用。
    
    **说明**
    
    您的智能体应用与步骤二中上传的文件需位于同一业务空间内。
    
2.  API调用时，通过参数 `session_file_ids` 传递步骤二中获取的会话文件ID，调用示例如下：
    
    > Java SDK中为sessionFileIds。通过HTTP调用时，请将 `session_file_ids` 放入 parameters 对象中。
    
    **重要**
    
    获取的会话文件ID必须以“`file_session_`”开头，且文件状态为 FILE\_IS\_READY。如果未满足条件，调用将会失败。
    
    ## **Python**
    
    **请求示例**
    
    ```
    import os
    from http import HTTPStatus
    # 建议dashscope SDK 的版本 >= 1.20.14
    from dashscope import Application
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        app_id='YOUR_APP_ID',  # 应用ID替换YOUR_APP_ID
        prompt='请根据以下文件帮我推荐一款3000元以下的手机',
        rag_options={
            "session_file_ids": ["FILE_ID1"],  # FILE_ID1 替换为实际的临时文件ID,逗号隔开多个
        }
    )
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n' % (response.output.text))  # 处理只输出文本text
        # print('%s\n' % (response.usage))
    ```
    
    **响应示例**
    
    ```
    根据您的预算，我推荐您选择**通义 Vivid 7**这款手机。以下是它的主要特点：
    
    - **屏幕**：6.5英寸，1080 x 2400像素
    - **存储与内存**：128GB存储，8GB RAM
    - **电池**：4500mAh
    - **特色功能**：AI智能摄影，侧面指纹解锁
    - **参考售价**：2999-3299元
    
    通义Vivid 7不仅价格适中，而且具有良好的性能和实用的功能，特别适合喜欢拍照的用户。希望这个建议对您有所帮助！
    ```
    
    ## **Java**
    
    **请求示例**
    
    ```
    // 建议dashscope SDK 的版本 >= 2.17.0；
    import com.alibaba.dashscope.app.*;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    
    import java.util.Arrays;
    
    public class Main {
        public static void appCall() throws NoApiKeyException, InputRequiredException {
            ApplicationParam param = ApplicationParam.builder()
                    // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .appId("YOUR_APP_ID") // 替换为实际的应用ID
                    .prompt("请根据以下文件帮我推荐一款3000元左右的手机")
                    .ragOptions(RagOptions.builder()
                            .sessionFileIds(Arrays.asList("FILE_ID1", "FILE_ID2"))  // 替换为实际指定的临时文件 ID，逗号隔开多个
                            .build())
                    .build();
    
            Application application = new Application();
            ApplicationResult result = application.call(param);
            System.out.printf("%s\n",
                    result.getOutput().getText());// 处理只输出文本text
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
    根据您的预算（3000元左右），我推荐您选择**通义 Vivid 7**这款手机。
    
    ### 通义 Vivid 7 —— 智能摄影新体验
    - **屏幕**：6.5英寸，1080 x 2400像素
    - **存储与内存**：128GB存储，8GB RAM
    - **电池**：4500mAh
    - **特色功能**：AI智能摄影，侧面指纹解锁
    - **参考售价**：2999-3299元
    
    这款手机拥有不错的屏幕显示效果、充足的存储空间和RAM，以及出色的续航能力。特别是其AI智能摄影功能，可以带来更高质量的照片拍摄体验。整体来看，它非常适合日常使用，并且价格也符合您的预算范围。
    ```
    
    ## **HTTP**
    
    ## **curl**
    
    **请求示例**
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{YOUR_APP_ID}/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {
            "prompt": "请根据以下文件帮我推荐一款3000元以下的手机"
        },
        "parameters":  {
                        "rag_options" : {
                        "session_file_ids":["FILE_ID1"]}
        },
        "debug": {}
    }'
    ```
    
    **响应示例**
    
    ```
    {"output":{"finish_reason":"stop","session_id":"fb0081f56ace400bb4f1c12f6b5d1247",
    "text":"根据您的预算（3000元以下），我为您推荐**通义 Vivid 7**这款手机。\n\n### 推荐理由\n- **价格适中**：参考售价为2999-3299元，正好符合您的预算范围。\n- **智能摄影功能**：具备AI智能摄影技术，能够帮助您拍摄出专业级别的照片，非常适合喜欢拍照的用户。\n- **性能均衡**：拥有6.5英寸的1080 x 2400像素屏幕，搭配8GB RAM与128GB存储空间，在保证日常使用流畅的同时也提供了足够的存储容量。\n- **长续航能力**：内置4500mAh电池，可以满足一天的正常使用需求。\n- **安全便捷**：采用侧面指纹解锁设计，既方便又安全。\n\n综上所述，通义 Vivid 7 在性价比方面表现优秀，尤其适合追求良好拍照体验和合理价位的消费者。"},"usage":{"models":[{"output_tokens":201,"model_id":"qwen-max","input_tokens":1594}]},"request_id":"596f5055-2736-985d-8024-5849df5b799b"}%
    ```
    
    ## **PHP**
    
    **请求示例**
    
    ```
    <?php
    # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
    
    $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
    
    // 构造请求数据
    $data = [
        "input" => [
            'prompt' => '请根据以下文件帮我推荐一款3000元以下的手机'
        ],
        "parameters" => [
            'rag_options' => [
                'session_file_ids' => ['FILE_ID1']//替换为指定的临时文件ID,逗号隔开多个
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
    根据您的预算（3000元以下），我为您推荐**通义 Vivid 7**。这款手机的主要特点包括：
    
    - **屏幕**：6.5英寸，1080 x 2400像素
    - **存储与内存**：128GB存储，8GB RAM
    - **电池**：4500mAh
    - **特色功能**：AI智能摄影，侧面指纹解锁
    - **参考售价**：2999-3299元
    
    通义Vivid 7以其实惠的价格和出色的性能，特别是其在拍照方面的优秀表现，非常适合追求性价比且对摄影有一定要求的用户。希望这个建议能够帮到您！如果还有其他需求或疑问，请随时告诉我。
    ```
    
    ## **Node.js**
    
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
        const appId = 'YOUR_APP_ID';//替换为实际的应用 ID
    
        const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    
        const data = {
            input: {
                prompt: "请根据以下文件帮我推荐一款3000元以下的手机"
            },
            parameters: {
                rag_options:{
                    session_file_ids:['YOUR_FILE_ID1']  // 替换为指定的临时文件 ID，多个请用逗号隔开
                }
            },
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
    根据您的预算（3000元以下），我为您推荐**通义 Vivid 7**这款手机。
    
    ### 推荐理由：
    - **屏幕表现良好**：6.5英寸1080 x 2400像素全面屏，视觉效果细腻。
    - **AI智能摄影**：支持AI智能摄影功能，能够自动优化照片色彩与细节，让您轻松拍出专业级照片。
    - **充足的内存和存储空间**：配备8GB RAM + 128GB存储组合，满足日常使用及娱乐需求。
    - **持久续航**：内置4500mAh大容量电池，保障一天的正常使用。
    - **便捷安全解锁方式**：采用侧面指纹解锁设计，既快速又方便。
    - **价格合理**：参考售价为2999-3299元，在您的预算范围内。
    
    综上所述，如果您对摄影有一定兴趣且追求性价比的话，通义 Vivid 7将是不错的选择。当然，具体购买时请以官方渠道或授权零售商提供的最新信息为准。
    ```
    
    ## **C#**
    
    **请求示例**
    
    ```
    using System.Text;
    
    class Program
    {
        static async Task Main(string[] args)
        {
            // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
            string appId = "YOUR_APP_ID";// 替换为实际的应用ID
            // FILE_ID1替换为指定的临时文件ID
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
                        ""prompt"": ""请根据以下文件帮我推荐一款3000元以下的手机""
                    }},
                    ""parameters"": {{
                        ""rag_options"" : {{
                            ""session_file_ids"":[""FILE_ID1""]
                        }}
                    }},
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
            "session_id": "11c4c233714d45129fb9b63a7e708fb8",
            "text": "根据您的预算（3000元以下），我为您推荐**通义 Vivid 7**这款手机。它具有以下特点：\n\n- **屏幕**：6.5英寸，1080 x 2400像素\n- **存储与内存**：128GB存储，8GB RAM\n- **电池**：4500mAh\n- **特色功能**：AI智能摄影，侧面指纹解锁\n- **参考售价**：2999-3299元\n\n虽然其最高配置版本的价格略高于3000元，但考虑到其出色的性价比以及在摄影方面的优秀表现，如果能够接受这个价格范围的话，这将是一个非常不错的选择。此外，您还可以留意一下电商平台或官方渠道是否会有优惠活动，从而以更低的价格购得此款手机。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 177,
                    "model_id": "qwen-max",
                    "input_tokens": 1594
                }
            ]
        },
        "request_id": "663c2641-bfe3-908e-a10f-5ccb819cb136"
    }
    ```
    
    ## **Go**
    
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
    	appId := "YOUR_APP_ID" // 替换为实际的应用 ID
    
    	if apiKey == "" {
    		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
    		return
    	}
    
    	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)
    
    	// 创建请求体
    	requestBody := map[string]interface{}{
    		"input": map[string]string{
    			"prompt": "请根据以下文件帮我推荐一款3000元以下的手机",
    		},
    		"parameters": map[string]interface{}{
    			"rag_options": map[string]interface{}{
    				"session_file_ids": []string{"FILE_ID1"}, // 替换为实际的临时文件
    			},
    		},
    		"debug": map[string]interface{}{},
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
            "session_id": "846db8ba50514d69bfa0faebd639cb33",
            "text": "根据您的预算，我推荐您选择**通义 Vivid 7 —— 智能摄影新体验**这款手机。它拥有6.5英寸的全面屏、8GB RAM和128GB存储空间，支持AI智能摄影功能，还有4500mAh电池容量，能够满足日常使用需求。侧面指纹解锁设计既方便又安全。参考售价为2999-3299元，正好符合您的预算范围。希望这个建议对您有所帮助！"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 106,
                    "model_id": "qwen-max",
                    "input_tokens": 1594
                }
            ]
        },
        "request_id": "af305d07-a24a-9163-a015-4ec52909ec55"
    }
    ```
    

##### **通过API接口获取会话文件ID**

**操作步骤**

1.  **申请文件上传租约**
    
    [在线调试](https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease)ApplyFileUploadLease接口。
    
    **发起调用图示**
    
    **重要参数说明**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1194987471/p958857.png)
    
    **CategoryId**: 务必填写default。
    
    **FileName**：文件名称+后缀。
    
    **Md5:** 可运行此处示例代码获取该文件的Md5值。
    
    **生成MD5示例代码**
    
    ##### **Python**
    
    ```
    # 示例代码仅供参考，请勿在生产环境中直接使用
    import hashlib
    def calculate_md5(file_path):
        """计算文档的 MD5 值。
    
        Args:
            file_path (str): 文档的路径。
    
        Returns:
            str: 文档的 MD5 值。
        """
        md5_hash = hashlib.md5()
    
        # 以二进制形式读取文件
        with open(file_path, "rb") as f:
            # 按块读取文件，避免大文件占用过多内存
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
    
        return md5_hash.hexdigest()
    
    # 使用示例
    file_path = "请替换为您需要上传文档的实际本地路径，例如/Users/Bailian/Desktop/阿里云百炼系列手机产品介绍.docx"
    md5_value = calculate_md5(file_path)
    print(f"文档的MD5值为: {md5_value}")
    ```
    
    ##### **Java**
    
    ```
    // 示例代码仅供参考，请勿在生产环境中直接使用
    import java.io.InputStream;
    import java.nio.file.Files;
    import java.nio.file.Paths;
    import java.security.MessageDigest;
    
    public class Md5Utils {
    
        private static String getFileMd5(String filePath) throws Exception {
            MessageDigest digest = MessageDigest.getInstance("MD5");
            try (InputStream is = Files.newInputStream(Paths.get(filePath))) {
                byte[] buffer = new byte[1024];
                int read;
                while ((read = is.read(buffer)) > 0) {
                    digest.update(buffer, 0, read);
                }
            }
            byte[] md5Bytes = digest.digest();
    
            StringBuilder md5String = new StringBuilder();
            for (byte b : md5Bytes) {
                md5String.append(String.format("%02x", b));
            }
    
            return md5String.toString();
        }
    
        public static void main(String[] args) throws Exception {
    
            String filePath = "请替换为您需要上传文档的实际本地路径，例如/Users/Bailian/Desktop/阿里云百炼系列手机产品介绍.docx";
            String md5 = getFileMd5(filePath);
    
            System.out.println("文档的MD5值为: " + md5);
        }
    }
    ```
    
    **SizeInBytes**：文件大小，单位为字节。例如：6 KB = 6 \* 1024 字节 = 6144 字节。
    
    **CategoryType**: 务必填写SESSION\_FILE。
    
    **调用成功图示**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1194987471/p958861.png)
    
    **说明**
    
    1.  此接口响应中的`Data.FileUploadLeaseId`、`Data.Param.Method`、`Data.Param.Url`、Data.Param.Headers.X-bailian-extra和`Data.Param.Headers.Content-Type`字段的值请妥善保存，它们将用于后续的上传步骤。
        
    2.  此接口响应中的`Data.Param.Url`字段的值（即租约）有效期为分钟级，请尽快上传文档，以免租约过期导致无法上传。
        
    
2.  **上传文件至阿里云百炼的临时存储**
    
    示例代码如下，请根据代码提示替换上一步获取的实际字段值，然后运行代码。若响应为“File uploaded successfully.”，则表示上传成功。
    
    **示例代码**
    
    多语言示例请自行编写。
    
    ##### **Python**
    
    ```
    # 示例代码仅供参考，请勿在生产环境中直接使用
    import requests
    from urllib.parse import urlparse
    
    def upload_file(pre_signed_url, file_path):
        try:
            # 设置请求头
            headers = {
                "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
                "Content-Type": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值"
            }
    
            # 读取文档并上传
            with open(file_path, 'rb') as file:
                # 下方设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
                response = requests.put(pre_signed_url, data=file, headers=headers)
    
            # 检查响应状态码
            if response.status_code == 200:
                print("File uploaded successfully.")
            else:
                print(f"Failed to upload the file. ResponseCode: {response.status_code}")
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    def upload_file_link(pre_signed_url, source_url_string):
        try:
            # 设置请求头
            headers = {
                "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
                "Content-Type": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值"
            }
    
            # 设置访问OSS的请求方法为GET
            source_response = requests.get(source_url_string)
            if source_response.status_code != 200:
                raise RuntimeError("Failed to get source file.")
    
            # 下方设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            response = requests.put(pre_signed_url, data=source_response.content, headers=headers)
    
            # 检查响应状态码
            if response.status_code == 200:
                print("File uploaded successfully.")
            else:
                print(f"Failed to upload the file. ResponseCode: {response.status_code}")
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    if __name__ == "__main__":
    
        pre_signed_url_or_http_url = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值"
    
        # 文档来源可以是本地，上传本地文档至百炼临时存储
        file_path = "请替换为您需要上传文档的实际本地路径"
        upload_file(pre_signed_url_or_http_url, file_path)
    
        # 文档来源还可以是阿里云对象存储OSS
        # file_path = "请替换为您需要上传文档的实际阿里云对象存储OSS可公网访问地址"
        # upload_file_link(pre_signed_url_or_http_url, file_path)
    ```
    
    ##### **Java**
    
    ```
    // 示例代码仅供参考，请勿在生产环境中直接使用
    import java.io.BufferedInputStream;
    import java.io.DataOutputStream;
    import java.io.FileInputStream;
    import java.io.InputStream;
    import java.net.HttpURLConnection;
    import java.net.URL;
    
    public class UploadFile{
    
        public static void uploadFile(String preSignedUrl, String filePath) {
            HttpURLConnection connection = null;
            try {
                // 创建URL对象
                URL url = new URL(preSignedUrl);
                connection = (HttpURLConnection) url.openConnection();
    
                // 设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
                connection.setRequestMethod("PUT");
    
                // 允许向connection输出，因为这个连接是用于上传文档的
                connection.setDoOutput(true);
    
                connection.setRequestProperty("X-bailian-extra", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值");
                connection.setRequestProperty("Content-Type", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值");
    
                // 读取文档并通过连接上传
                try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                     FileInputStream fileInputStream = new FileInputStream(filePath)) {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
    
                    while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                        outStream.write(buffer, 0, bytesRead);
                    }
    
                    outStream.flush();
                }
    
                // 检查响应
                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    // 文档上传成功处理
                    System.out.println("File uploaded successfully.");
                } else {
                    // 文档上传失败处理
                    System.out.println("Failed to upload the file. ResponseCode: " + responseCode);
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                if (connection != null) {
                    connection.disconnect();
                }
            }
        }
    
        public static void uploadFileLink(String preSignedUrl, String sourceUrlString) {
            HttpURLConnection connection = null;
            try {
                // 创建URL对象
                URL url = new URL(preSignedUrl);
                connection = (HttpURLConnection) url.openConnection();
    
                // 设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
                connection.setRequestMethod("PUT");
    
                // 允许向connection输出，因为这个连接是用于上传文档的
                connection.setDoOutput(true);
    
                connection.setRequestProperty("X-bailian-extra", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值");
                connection.setRequestProperty("Content-Type", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值");
    
                URL sourceUrl = new URL(sourceUrlString);
                HttpURLConnection sourceConnection = (HttpURLConnection) sourceUrl.openConnection();
    
                // 设置访问OSS的请求方法为GET
                sourceConnection.setRequestMethod("GET");
                // 获取响应码，200表示请求成功
                int sourceFileResponseCode = sourceConnection.getResponseCode();
    
                // 从OSS读取文档并通过连接上传
                if (sourceFileResponseCode != HttpURLConnection.HTTP_OK){
                    throw new RuntimeException("Failed to get source file.");
                }
                try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                     InputStream in = new BufferedInputStream(sourceConnection.getInputStream())) {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
    
                    while ((bytesRead = in.read(buffer)) != -1) {
                        outStream.write(buffer, 0, bytesRead);
                    }
    
                    outStream.flush();
                }
    
                // 检查响应
                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    // 文档上传成功
                    System.out.println("File uploaded successfully.");
                } else {
                    // 文档上传失败
                    System.out.println("Failed to upload the file. ResponseCode: " + responseCode);
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                if (connection != null) {
                    connection.disconnect();
                }
            }
        }
    
        public static void main(String[] args) {
    
            String preSignedUrlOrHttpUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";
    
            // 文档来源可以是本地，上传本地文档至百炼临时存储
            String filePath = "请替换为您需要上传文档的实际本地路径";
            uploadFile(preSignedUrlOrHttpUrl, filePath);
    
            // 文档来源还可以是OSS
            // String filePath = "请替换为您需要上传文档的实际OSS可公网访问地址";
            // uploadFileLink(preSignedUrlOrHttpUrl, filePath);
        }
    }
    ```
    
3.  **将文件添加至阿里云百炼的数据管理**
    
    上一步操作成功后，文档将暂存于阿里云百炼的临时存储空间内 12 小时，通过[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/AddFile)AddFile接口获取会话文件ID。
    
    **配置图示**
    
    **重要参数说明**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1194987471/p958862.png)
    
    **LeaseId**：第一步接口响应中的`Data.FileUploadLeaseId`字段值。
    
    **CategoryId**: 务必填写default。
    
    **CategoryType**: 务必填写SESSION\_FILE。
    
    **调用成功图示**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1194987471/p958863.png)
    
    **说明**
    
    -   获取会话文件ID。示例："file\_session\_6c6bb33339524b7xxx"。
        
        **重要**
        
        仅以“file\_session\_”开头的ID才能用于下一步的API调用。如未满足，请核实步骤中的重要参数CategoryId和CategoryType是否填写正确。
        
    -   AddFile接口调用成功后，`LeaseId`（租约 ID）随即失效，请勿再使用相同的租约 ID 重复提交。
        
    
4.  **查看文档解析状态**
    
    通过[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile)DescribeFile接口查看文档解析状态。
    
    **状态码**
    
    **说明**
    
    `INIT`
    
    文件已上传，等待解析。
    
    `PARSING`
    
    正在解析文件内容。
    
    `PARSE_SUCCESS`
    
    文件解析成功。
    
    `PARSE_FAILED`
    
    文件解析失败，需重新上传。
    
    `SAFE_CHECKING`
    
    正在进行文件安全检测。
    
    `SAFE_CHECK_FAILED`
    
    文件未通过安全检测，需重新上传或更换文件。
    
    `INDEX_BUILDING`
    
    正在为文件构建索引。
    
    `INDEX_BUILD_SUCCESS`
    
    文件索引构建完成。
    
    `INDEX_BUILDING_FAILED`
    
    索引构建失败，需重新上传文件。
    
    `INDEX_DELETED`
    
    文件索引已删除。
    
    `FILE_IS_READY`
    
    文件准备完毕：文件解析、安全检测、索引构建均已完成。
    
    `FILE_EXPIRED`
    
    文件过期。 文件仅在当前会话有效（最长7天），关闭会话后自动过期，需重新上传文件。
    
    **重要**
    
    必须等到`Status`字段值显示为`FILE_IS_READY`才能开始后续的API调用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1194987471/p958899.png)
    
5.  完成有效的会话文件ID获取后，可进入上述步骤三：API调用应用。
    

如需查看上述获取ID步骤中的接口参数详细说明请参阅[API上传文件](https://help.aliyun.com/zh/model-studio/developer-reference/upload-files-by-calling-api?spm=a2c4g.11186623.0.0.2e2183749WPvAJ)。

#### **视觉理解**

**操作步骤**

1.  在控制台**智能体应用**内选择**通义千问VL系列模型**，开启**视觉**开关，并**发布**应用。
    
2.  API调用时，通过参数`image_list`传入图像URL，可以传入多张图像URL。调用示例如下：
    
    > Java SDK中为images接口。通过HTTP调用时，请将 image\_list 放入 input 对象中。
    
    ## **Python**
    
    **请求示例**
    
    ```
    import os
    from http import HTTPStatus
    # 建议dashscope SDK 的版本 >= 1.20.14
    from dashscope import Application
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        app_id='YOUR_APP_ID',  # 应用ID替换YOUR_APP_ID
        prompt='图中描绘的是什么景象?',
        image_list=["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"],  # 替换为实际的图片链接，逗号隔开多个
    )
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n' % (response.output.text))  # 处理只输出文本text
        # print('%s\n' % (response.usage))
    ```
    
    **响应示例**
    
    ```
    图中描绘的是一个女人和一只狗在海滩上互动的景象。女人坐在沙滩上，面带微笑地与狗握手。背景是大海和天空，阳光洒在她们身上，营造出温暖和谐的氛围。
    ```
    
    ## **Java**
    
    **请求示例**
    
    ```
    // 建议dashscope SDK 的版本 >= 2.17.0；
    import com.alibaba.dashscope.app.*;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    
    import java.util.Arrays;
    import java.util.List;
    
    public class Main {
        public static void appCall() throws NoApiKeyException, InputRequiredException {
            ApplicationParam param = ApplicationParam.builder()
                    // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey("sk-xxx")。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .appId("YOUR_APP_ID") // 替换为实际的应用ID
                    .prompt("图中描绘的是什么景象?")
                    .images(Arrays.asList("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"))  // 替换为实际的图片链接，逗号隔开多个
                    .build();
    
            Application application = new Application();
            ApplicationResult result = application.call(param);
            System.out.printf("%s\n",
                    result.getOutput().getText());// 处理只输出文本text
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
    图中描绘的是一个女人和一只狗在海滩上互动的景象。女人坐在沙滩上，面带微笑地与狗握手。背景是大海和天空，阳光洒在她们身上，营造出温暖和谐的氛围。
    ```
    
    ## **HTTP**
    
    ## **curl**
    
    **请求示例**
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{YOUR_APP_ID}/completion \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
            "input": {
                "prompt": "图中描绘的是什么景象?",
                "image_list":["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"]
            },
            "debug": {}
            }'
    ```
    
    **响应示例**
    
    ```
    {
        "output": {
            "finish_reason": "stop",
            "session_id": "6c67678038e14f138f384e477e7126f6",
            "text": "图中描绘的是一个女人和一只狗在海滩上互动的景象。女人坐在沙滩上，面带微笑地与狗握手。背景是大海和天空，阳光洒在她们身上，营造出温暖和谐的氛围。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 49,
                    "model_id": "qwen-vl-max",
                    "input_tokens": 1305
                }
            ]
        },
        "request_id": "4a8a6a76-eecd-9298-a0fb-16a4c8f9a205"
    }
    ```
    
    ## **PHP**
    
    **请求示例**
    
    ```
    <?php
    # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
    
    $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
    
    // 构造请求数据
    $data = [
        "input" => [
            'prompt' => '图中描绘的是什么景象?',   
            'image_list' => ['https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg']//替换为实际的图片链接,逗号隔开多个 
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
    图中描绘的是一个女人和一只狗在海滩上互动的景象。女人坐在沙滩上，面带微笑地与狗握手。背景是大海和天空，阳光洒在她们身上，营造出温暖和谐的氛围。
    ```
    
    ## **Node.js**
    
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
        const appId = 'YOUR_APP_ID';//替换为实际的应用 ID
    
        const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    
        const data = {
            input: {
                prompt: "图中描绘的是什么景象?",
                image_list:['https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg']  // 替换为实际的图片链接，多个请用逗号隔开
            },
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
    图中描绘的是一个女人和一只狗在海滩上互动的景象。女人坐在沙滩上，面带微笑地与狗握手。背景是大海和天空，阳光洒在她们身上，营造出温暖和谐的氛围。
    ```
    
    ## **C#**
    
    **请求示例**
    
    ```
    using System.Text;
    
    class Program
    {
        static async Task Main(string[] args)
        {
            // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            string apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");;
            string appId = "YOUR_APP_ID";// 替换为实际的应用ID
            
            if (string.IsNullOrEmpty(apiKey))
            {
                Console.WriteLine("请确保设置了 DASHSCOPE_API_KEY。");
                return;
            }
    
            string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";
            // image_list中替换为实际的图片链接，如果多个图片链接请用逗号隔开
            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
                string jsonContent = $@"{{
                    ""input"": {{
                        ""prompt"": ""图中描绘的是什么景象?"",
                        ""image_list"":[""https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg""
                                    ]
                    }},
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
            "session_id": "5149b58d713e49ed80c30372aee377ae",
            "text": "图中描绘的是一个女人和一只狗在海滩上互动的景象。女人坐在沙滩上，面带微笑地与狗握手。背景是大海和天空，阳光洒在她们身上，营造出温暖和谐的氛围。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 49,
                    "model_id": "qwen-vl-max",
                    "input_tokens": 1305
                }
            ]
        },
        "request_id": "702810f5-d21d-9b74-8b4f-e58d0a8da413"
    }
    ```
    
    ## **Go**
    
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
    	appId := "YOUR_APP_ID" // 替换为实际的应用 ID
    
    	if apiKey == "" {
    		fmt.Println("请确保设置了DASHSCOPE_API_KEY。")
    		return
    	}
    
    	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/apps/%s/completion", appId)
    
    	// 创建请求体
    	requestBody := map[string]interface{}{
    		"input": map[string]interface{}{
    			"prompt":     "图中描绘的是什么景象?",
    			"image_list": []string{"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}, // 替换为实际的图片链接,多个请用逗号隔开
    		},
    		"debug": map[string]interface{}{},
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
            "session_id": "8a3d495588d34c2e99ea42b12d265c31",
            "text": "图中描绘的是一个女人和一只狗在海滩上互动的景象。女人穿着格子衬衫，坐在沙滩上，与她的宠物狗进行亲密的互动。狗狗戴着项圈，伸出前爪与女人握手，显得非常友好和温顺。背景是广阔的海洋和天空，阳光洒在她们身上，营造出一种温暖和谐的氛围。这张照片捕捉到了人与动物之间美好的友谊时刻。"
        },
        "usage": {
            "models": [
                {
                    "output_tokens": 88,
                    "model_id": "qwen-vl-max",
                    "input_tokens": 2554
                }
            ]
        },
        "request_id": "22db4110-6c7b-9b06-8769-c8a1a3edfd39"
    }
    ```
    

### **私网调用**

为提高数据传输的安全性和效率，您可通过私网调用阿里云百炼平台的应用。

1.  [创建终端节点](https://help.aliyun.com/zh/model-studio/access-model-studio-through-privatelink#b49f50b6202nn)：在阿里云控制台为您的VPC创建一个私网终端节点。
    
2.  **替换域名**：将API请求URL中的公网域名`dashscope.aliyuncs.com`替换为您获取到的私网终端节点服务域名。例如：
    
    `https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/`
    
3.  发起请求：示例代码如下。
    
    #### Python
    
    ```
    import os
    from http import HTTPStatus
    from dashscope import Application
    # 配置私网终端节点
    os.environ['DASHSCOPE_HTTP_BASE_URL'] = 'https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/'
    response = Application.call(
        # 若没有配置环境变量，可用阿里云百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id='YOUR_APP_ID',# 替换为实际的应用 ID
        prompt='你是谁？')
    
    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print(response.output.text)
    ```
    
    #### Java
    
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
                    .appId("YOUR_APP_ID")
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
    
    #### HTTP
    
    这里给出curl代码示例。
    
    ```
    curl -X POST https://ep-2zei6917b47eed******.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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
    
    > `YOUR_APP_ID`替换为实际的应用ID。
    

## API参考

通过[应用调用API参考](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)查看完整的参数列表。

## **错误码**

如果调用失败并返回报错信息，请参阅[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **相关文档**

-   在调用应用时，如需将模型回复的文本信息转成语音，请参阅[语音合成-CosyVoice/Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。
    
-   关于应用的构建和使用请参阅[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。
    
-   关于应用内Prompt辅助工具的使用请参阅[Prompt工程](https://help.aliyun.com/zh/model-studio/use-prompt-engineering-to-communicate-with-large-models)。
    
-   在前端生产环境下使用请参阅[10分钟给网站添加AI助手](https://help.aliyun.com/zh/model-studio/add-an-ai-assistant-to-your-website-in-10-minutes)。
    

## 常见问题

**运行Java代码示例时，如果出现类似“java: 程序包com.alibaba.dashscope.app不存在”的异常信息，应该怎么处理？**

1.  检查导入语句中的类名和包名是否正确。
    
2.  添加依赖库：如果使用Maven或Gradle进行项目管理，确保DashScope Java SDK依赖库已经添加到`pom.xml`或`build.gradle`文件中，且为最新版本。访问[Maven](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)获取DashScope Java SDK的最新版本号。
    
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
    
3.  升级SDK：旧版本的DashScope Java SDK可能不包含您尝试使用的功能或类。如果您已经添加过依赖库DashScope Java SDK，请确认您所使用的DashScope Java SDK是否为最新版。如果当前版本较低，请将其升级至最新版本。可在`pom.xml`或`build.gradle`文件中修改DashScope Java SDK的版本为最新版本。
    
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
    

**多轮对话**`**（session_id）**`**与长期记忆**`**（memory_id**`**）有什么区别？**

-   `session_id`： 用于云端托管的多轮对话，自动维护对话上下文。 有效期1小时，最大历史轮数50。 无需调用者自行维护上下文，但需在下一轮对话中传入上一轮对话的`session_id`。
    
-   `memory_id`： 用于创建长期记忆体，存储特定信息。 需调用[CreateMemory](https://help.aliyun.com/zh/model-studio/developer-reference/api-bailian-2023-12-29-creatememory?spm=a2c4g.11186623.0.0.586c6610Kg0bkj)接口创建，获取`memoryId`。 在后续对话中引用特定信息，需传入`memoryId`。
    

两者分别服务于短期对话和长期信息存储。

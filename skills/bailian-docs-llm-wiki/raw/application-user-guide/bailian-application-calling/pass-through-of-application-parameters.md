# 应用的自定义参数传递

本文介绍如何在阿里云百炼的**智能体应用**和**工作流应用**（智能体编排应用已被工作流应用替代）调用中使用自定义参数传递功能，主要适用于自定义插件与自定义节点的参数传递。

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## **自定义插件参数传递**

本文以**寝室公约内容查询工具**作为示例，向您展示API如何调用应用的自定义插件参数传递功能。

**说明**

自定义插件的参数通过关联的**智能体应用**传递，或通过**工作流应用**中的**插件节点**传递。

下方示例展示在**智能体应用**中如何传递自定义插件参数。

### **如何使用**

#### **步骤一：创建自定义插件工具**

> 如果已创建插件工具或已导入了插件，请跳过此步骤。

1.  创建自定义插件：访问百炼控制台的**[插件](https://bailian.console.aliyun.com/?tab=app#/component-manage)**页面，单击**新增自定义插件**，填写插件信息，如需要鉴权请打开**是否鉴权**开关，填写鉴权配置信息。
    
    > 示例插件描述：寝室公约查询工具，可以根据输入的数字索引查询特定条目。
    
    > 示例插件 URL：https://domitorgreement-plugin-example-icohrkdjxy.cn-beijing.fcapp.run
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3400819371/p911623.png)
    
    **请注意：****插件描述**是对插件用途的简要说明，能帮助大模型判断当前任务是否需要调用当前插件，请使用自然语言进行描述。
    
2.  创建工具：填写工具信息，配置输入参数和输出参数。**请注意：**
    
    1.  **工具描述**能帮助大模型更好的理解工具功能和使用场景。请使用自然语言进行描述，尽量给出使用示例。
        
    2.  **参数名称**尽可能带有含义，可以帮助大模型理解当前需要识别的参数信息是什么。
        
    3.  **参数描述**是对该入参的功能描述，要简练且准确，帮助大模型进一步理解取参的方式。
        
    4.  输入参数的**传参方式****务必**选择**业务透传**。
        
    
    此处示例将**寝室公约内容索引**`article_index`设置为业务透传参数。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3400819371/p911624.png)
    
3.  单击**测试工具**，运行通过后，**发布**插件。
    

#### **步骤二：智能体应用关联指定插件**

> 插件工具只能与位于相同业务空间里的**智能体应用**关联。

1.  可在已发布的插件卡片上单击**添加到智能体**，选择需要关联的智能体应用；
    
2.  也可在应用内单击**+插件**，关联指定的自定义插件；
    
3.  然后直接**发布**应用。
    

#### **步骤三：API调用**

-   **无需鉴权时**：通过API调用自定义插件，使用`biz_params`的`user_defined_params`传递自定义插件信息，`your_plugin_code`替换为实际的插件ID，并传递插件中配置的输入参数键值对。
    
    > 插件ID可在插件卡片上获取。
    
    本示例中传入寝室公约索引`article_index`参数值为2，查询第二条寝室公约内容，并返回正确结果。
    
    ## Python
    
    **请求示例**
    
    ```
    import os
    from http import HTTPStatus
    # 建议dashscope SDK 的版本 >= 1.14.0
    from dashscope import Application
    biz_params = {
        # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换your_plugin_code
        "user_defined_params": {
            "your_plugin_code": {
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
    
    ## Java
    
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
                    // 智能体应用的自定义插件输入参数传递，自定义的插件ID替换{your_plugin_code}
                    "{\"user_defined_params\":{\"{your_plugin_code}\":{\"article_index\":2}}}";
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
    
    ## HTTP
    
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
                    "{your_plugin_code}":
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
    
    > YOUR\_APP\_ID替换为实际的应用 ID。
    
    **响应示例**
    
    ```
    {"output":
    {"finish_reason":"stop",
    "session_id":"e151267ffded4fbdb13d91439011d31e",
    "text":"寝室公约的第二条内容是：“寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。”这意呀着在寝室生活中，大家要彼此支持，共同创造一个和谐、积极向上的生活环境。"},
    "usage":{"models":[{"output_tokens":94,"model_id":"qwen-max","input_tokens":453}]},
    "request_id":"a39fd2b5-7e2c-983e-84a1-1039f726f18a"}%
    ```
    
    ## PHP
    
    **请求示例**
    
    ```
    <?php
    
    # 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
    $url = "https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion";
    //{your_plugin_code}替换为实际的插件ID
    // 构造请求数据
    $data = [
        "input" => [
            'prompt' => '寝室公约内容',
            'biz_params' => [
            'user_defined_params' => [
                '{your_plugin_code}' => [
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
        const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
        const pluginCode = 'YOUR_PLUGIN_CODE';// 替换为实际的插件ID
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
    
            if (string.IsNullOrEmpty(apiKey))
            {
                Console.WriteLine("请确保设置了 DASHSCOPE_API_KEY。");
                return;
            }
    
            string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";
    
            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
                string pluginCode = "{your_plugin_code}"; // {your_plugin_code}替换为实际的插件 ID
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
    	appId := "YOUR_APP_ID"           // 替换为实际的应用 ID
    	pluginCode := "YOUR_PLUGIN_CODE" // 替换为实际的插件 ID
    
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
    
-   **需要鉴权时**：通过API调用自定义插件，插件中打开了**鉴权**开关，配置了**用户级鉴权**。
    
    > 插件ID在插件卡片上获取。
    
    -   使用`biz_params`的`user_defined_params`传递自定义插件信息，`your_plugin_code`替换为实际的插件ID，并传入插件中配置的输入参数键值对。
        
    -   使用 `biz_params` 的`user_defined_tokens`传递相关信息，`your_plugin_code`替换为实际的插件ID，`user_token`的参数值填入鉴权信息，如实际DASHSCOPE\_API\_KEY的值。
        
    -   鉴权通过后根据传递的索引参数查询特定条目并正确返回结果。
        
    
    本示例中传入寝室公约索引`article_index`参数值为2，`user_token`的值`YOUR_TOKEN`替换为实际DASHSCOPE\_API\_KEY的值。鉴权通过后，查询第二条寝室公约内容，并返回正确结果。
    
    ## Python
    
    **请求示例**
    
    ```
    from http import HTTPStatus
    import os
    # 建议dashscope SDK 的版本 >= 1.14.0
    from dashscope import Application
    biz_params = {
        # 智能体应用的自定义插件鉴权传递，自定义的插件ID替换your_plugin_code，鉴权信息替换YOUR_TOKEN，如API key
        "user_defined_params": {
            "your_plugin_code": {
                "article_index": 2}},
        "user_defined_tokens": {
            "your_plugin_code": {
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
    
    ## Java
    
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
                    // {your_plugin_code}替换为实际的插件ID,YOUR_TOKEN替换为实际的Token,如API key
                    "{\"user_defined_params\":{\"{your_plugin_code}\":{\"article_index\":2}}," +
                            "\"user_defined_tokens\":{\"{your_plugin_code}\":{\"user_token\":\"YOUR_TOKEN\"}}}";
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
    
    > 应用ID替换YOUR\_APP\_ID，自定义的插件ID替换your\_plugin\_code，鉴权Token替换YOUR\_TOKEN。
    
    ## HTTP
    
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
                    "{your_plugin_code}":
                        {
                        "article_index": 2
                        }
                },
                "user_defined_tokens":
                {
                    "{your_plugin_code}":
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
    
    > YOUR\_APP\_ID替换为实际的应用 ID，自定义的插件ID替换your\_plugin\_code，鉴权Token替换YOUR\_TOKEN。
    
    **响应示例**
    
    ```
    {"output":{"finish_reason":"stop",
    "session_id":"d3b5c3e269dc40479255a7a02df5c630",
    "text":"寝室公约的第二条内容为：“寝室成员应当互帮互助、互相关心、互相学习、共同提高；宽容谦让、相互尊重、以诚相待。”这强调了寝室生活中成员之间和谐相处与共同进步的重要性。"},
    "usage":{"models":[{"output_tokens":80,"model_id":"qwen-max","input_tokens":432}]},
    "request_id":"1f77154c-edc3-9003-b622-816fa2f849cf"}%
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
            'prompt' => '寝室公约内容',
            'biz_params' => [
            'user_defined_params' => [
                '{your_plugin_code}' => [//{your_plugin_code}替换为实际的插件ID
                    'article_index' => 2            
                    ]
                ],
            'user_defined_tokens' => [
                '{your_plugin_code}' => [//{your_plugin_code}替换为实际的插件ID
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
        const appId = 'YOUR_APP_ID';// 替换为实际的应用 ID
        const pluginCode = 'YOUR_PLUGIN_CODE';// 替换为实际的插件ID
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
    
            if (string.IsNullOrEmpty(apiKey))
            {
                Console.WriteLine("请确保设置了 DASHSCOPE_API_KEY。");
                return;
            }
    
            string url = $"https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion";
    
            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
                string pluginCode = "your_plugin_code"; // your_plugin_code替换为实际的插件 ID
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
    	appId := "YOUR_APP_ID"           // 替换为实际的应用 ID
    	pluginCode := "YOUR_PLUGIN_CODE" // 替换为实际的插件 ID
    
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
    

## **自定义节点参数传递**

本文以**根据城市名查询城市行政区域划分**作为示例，向您展示API如何调用应用的自定义节点参数传递功能。

**说明**

应用的自定义节点参数通过**工作流应用**的开始节点传递。

下方示例展示在**工作流应用**中，传递开始节点的自定义参数。

### **如何使用**

#### **步骤一：自定义节点参数**

访问百炼控制台的**[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)**页面，选择**工作流应用**并自定义**开始节点**的参数（示例设置String类型变量city），同时在**Prompt**中插入变量city和变量query，并**发布**应用。

#### **步骤二：API调用**

调用时通过`biz_params`字段传递city，通过`prompt`字段传递query。

## Python

**请求示例**

```
import os
from http import HTTPStatus
from dashscope import Application
# 工作流应用自定义参数传递
biz_params = {"city": "杭州"}
response = Application.call(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',  # 替换为实际的应用 ID
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
                .appId("YOUR_APP_ID")
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
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
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

> YOUR\_APP\_ID替换为实际的应用 ID。

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
$application_id = 'YOUR_APP_ID'; // 替换为实际的应用 ID
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
    const appId = 'YOUR_APP_ID'; // 替换为实际的应用 ID

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
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
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
        string appId = "YOUR_APP_ID"; // 替换为实际的应用ID
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
	appId := "YOUR_APP_ID" // 替换为实际的应用 ID

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

## **相关文档**

[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins)：自定义插件的创建步骤。

[调用智能体应用](https://help.aliyun.com/zh/model-studio/call-single-agent-application/)、[调用工作流应用](https://help.aliyun.com/zh/model-studio/invoke-workflow-application/)：应用的调用方式及更多用法。

[应用调用API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)：完整的参数列表和调用示例。

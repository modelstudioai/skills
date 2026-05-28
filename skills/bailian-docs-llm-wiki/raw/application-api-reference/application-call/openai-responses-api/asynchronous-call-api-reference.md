# 异步调用API参考

本文介绍如何通过 OpenAI 兼容模式的 Responses API **异步调用**阿里云百炼应用（**智能体**、**工作流**）。对于**耗时较长**的任务，只需在请求中设置 background 为 true，API 便会立即返回一个任务 ID，用于后续的查询与管理。这种“先提交、后查询”的方式，可有效避免请求超时或长时间等待。

**相关参考**

-   **同步调用**：对于需要即时获取结果的实时交互场景，请参阅[同步调用 API 参考](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference)。
    
-   **DashScope API**：如需获取更多功能，请参阅[DashScope API](https://help.aliyun.com/zh/model-studio/application-dashscope-api-reference/)。
    

**重要**

本文档仅适用于中国大陆版（北京地域）。

**说明**

异步任务暂不支持流式输出（stream=true）。

## 前提条件

-   已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK进行调用，还需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    
-   已创建[阿里云百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)，并已获取应用ID：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面的应用卡片上复制其ID。
    

## **快速开始**

本节提供完整的 Python 和 Java 示例，演示如何发起一个异步任务，然后通过轮询方式持续检查任务状态，直到任务完成并获取最终结果。

这个示例覆盖了异步调用的核心流程：

1.  **创建任务**：调用 `create` 方法并设置 `background=True`，获取任务 ID。
    
2.  **轮询状态**：在一个循环中，定期调用 `retrieve` 方法查询任务状态。
    
3.  **处理结果**：当任务状态变为 `completed`、`failed` 或 `cancelled` 时，退出循环并展示最终结果。
    

**代码示例**

## Python

```
import asyncio
import os
from openai import AsyncOpenAI
import time

# 1. 初始化客户端
## 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key = os.getenv("DASHSCOPE_API_KEY")
app_id = 'APP_ID'  # 请替换为实际的应用ID

base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
client = AsyncOpenAI(api_key=api_key, base_url=base_url)

async def main():
    start_time = time.time()
    
    # 2. 发起异步任务
    print("Step 1: 正在创建异步任务...")
    
    create_response = await client.responses.create(
        input="请为我规划一个为期三天的北京旅游行程，要求包含故宫、长城。",
        background=True
    )
    task_id = create_response.id
    print(f"  - 任务创建成功！ Task ID: {task_id}")
    print(f"  - 初始状态: {create_response.status}")

    # 3. 轮询任务状态直到任务完成
    print("\nStep 2: 开始轮询任务状态 (每 2 秒一次)...")
    while True:
        retrieve_response = await client.responses.retrieve(task_id)
        status = retrieve_response.status
        
        print(f"  - 当前状态: {status}")
        
        # 检查任务是否已进入终态
        if status in ['completed', 'failed', 'cancelled']:
            print("\nStep 3: 任务已完成或终止。")
            final_response = retrieve_response
            break
            
        # 等待 2 秒后再次查询
        await asyncio.sleep(2)

    # 4. 处理并打印最终结果
    if final_response.status == 'completed':
        print("  - 状态: Success")
        # 提取并打印可读的文本结果
        if final_response.output and final_response.output[0].content:
            result_text = final_response.output[0].content[0].text
            print("\n--- 任务输出 ---")
            print(result_text)
            print("-----------------")
        else:
            print("任务已完成，但未返回有效输出。")
            
    else: # 'failed' or 'cancelled'
        print(f"  - 状态: {final_response.status.upper()}")
        print("\n--- 最终响应详情 ---")
        # 打印完整的JSON以供调试
        print(final_response.model_dump_json(indent=2))
        print("-----------------------")

    end_time = time.time()
    print(f"\n总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    asyncio.run(main())
```

## Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

public class QuickStart {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String appId = "APP_ID"; // 替换为实际的应用 ID
        String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";

        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .build();

        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);

        long startTime = System.currentTimeMillis();

        // 1. 创建异步任务
        System.out.println("Step 1: 正在创建异步任务...");
        Response createResponse = client.responses().create(
                ResponseCreateParams.builder()
                        .input("请为我规划一个为期三天的北京旅游行程，要求包含故宫、长城。")
                        .background(true)
                        .build()
        );
        String taskId = createResponse.id();
        System.out.println("  - 任务创建成功！Task ID: " + taskId);
        System.out.println("  - 初始状态: " + createResponse.status().orElse(null));

        // 2. 轮询任务状态直到任务完成
        System.out.println("\nStep 2: 开始轮询任务状态 (每 2 秒一次)...");
        Response finalResponse = null;
        while (true) {
            Response retrieveResponse = client.responses().retrieve(taskId);
            ResponseStatus status = retrieveResponse.status().orElse(null);
            System.out.println("  - 当前状态: " + status);

            // 检查任务是否已进入终态
            if (ResponseStatus.COMPLETED.equals(status)
                    || ResponseStatus.FAILED.equals(status)
                    || ResponseStatus.CANCELLED.equals(status)) {
                System.out.println("\nStep 3: 任务已完成或终止。");
                finalResponse = retrieveResponse;
                break;
            }
            // 等待 2 秒后再次查询
            Thread.sleep(2000);
        }

        // 3. 处理并打印最终结果
        ResponseStatus finalStatus = finalResponse.status().orElse(null);
        if (ResponseStatus.COMPLETED.equals(finalStatus)) {
            System.out.println("  - 状态: Success");
            if (!finalResponse.output().isEmpty()) {
                System.out.println("\n--- 任务输出 ---");
                System.out.println(mapper.writeValueAsString(finalResponse.output()));
                System.out.println("-----------------");
            }
        } else {
            System.out.println("  - 状态: " + finalStatus);
            System.out.println("\n--- 最终响应详情 ---");
            System.out.println(mapper.writeValueAsString(finalResponse));
            System.out.println("-----------------------");
        }

        long endTime = System.currentTimeMillis();
        System.out.println("\n总耗时: " + (endTime - startTime) / 1000.0 + " 秒");
    }
}
```

## **具体流程**

以下章节详细介绍了创建、查询、取消和删除异步任务的 API 操作。

### **创建任务**

将`background`参数设置为`true`来开启异步模式，创建异步任务，立即获取任务 ID。

**Endpoint:**`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`

> 请将 `{APP_ID}` 替换为实际的应用 ID。

#### **请求示例**

## 单轮对话

#### **Python**

```
from openai import AsyncOpenAI
import asyncio
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化异步客户端
client = AsyncOpenAI(
  api_key=api_key,
  base_url=base_url
)

async def main():
  # 异步调用
  response = await client.responses.create(
    input="你是谁？",
    background=True
  )
    
  # 打印完整的响应JSON对象
  print(response.model_dump_json(indent=2))

# 运行异步主函数
if __name__ == "__main__":
  asyncio.run(main())
```

#### **Java**

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

public class CreateTask {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String appId = "APP_ID"; // 替换为实际的应用 ID
        String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";

        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .build();

        // 异步调用
        Response response = client.responses().create(
                ResponseCreateParams.builder()
                        .input("你是谁？")
                        .background(true)
                        .build()
        );

        // 打印完整的响应JSON对象
        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);
        System.out.println(mapper.writeValueAsString(response));
    }
}
```

#### **curl**

```
# 若没有配置环境变量，请将 {DASHSCOPE_API_KEY} 替换为实际的阿里云百炼API Key，但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
# 请将 APP_ID 替换为实际的应用ID
# 实际使用时请删除注释内容
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--data '{
    "input": "你是谁？",
    "background": true
}'
```

## 参数传递

**智能体应用****配置**

**插件参数传递**：在应用内选择指定插件工具，**发布**应用。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2618759671/p1034149.png)

**工作流应用****配置**

**自定义参数传递**

> 此处以查询城市美食作为示例。

1.  在应用内的**开始**创建自定义参数；
    
2.  在**大模型节点**的**提示词**处引用自定义参数；
    
3.  测试无误后，**发布**应用。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2618759671/p1034059.png)

**插件参数传递**

> 此处以寝室公约查询工具作为示例。

1.  如需传递插件，需添加**插件节点**，选择指定插件工具；
    
2.  在应用内的**开始**创建自定义参数，并将其传入插件节点的输入参数中；
    
3.  在**大模型节点**的**提示词**处引用自定义参数和插件输出参数；
    
4.  测试无误后，**发布**应用。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2618759671/p1034072.png)

#### **API 调用**

-   **自定义参数：**调用时通过`biz_params`传递，参数名和类型要与应用内的参数配置保持一致。
    
    ## Python
    
    ```
    from openai import AsyncOpenAI
    import asyncio
    import os
    
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv("DASHSCOPE_API_KEY")
    app_id='APP_ID' # 替换为实际的应用 ID
    base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
    
    # 初始化异步客户端
    client = AsyncOpenAI(
      api_key=api_key,
      base_url=base_url
    )
    async def main():
      # 异步调用
      response = await client.responses.create(
        input="你好",
        extra_body={
            "biz_params": {"city": "北京"} 
        },
        background=True
      )
        
      # 打印完整的响应JSON对象
      print(response.model_dump_json(indent=2))
    
    # 运行异步主函数
    if __name__ == "__main__":
      asyncio.run(main())
    ```
    
    ## Java
    
    ```
    import com.openai.client.OpenAIClient;
    import com.openai.client.okhttp.OpenAIOkHttpClient;
    import com.openai.models.responses.*;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.databind.SerializationFeature;
    import java.util.HashMap;
    import java.util.Map;
    
    public class CreateTaskWithCustomParams {
        public static void main(String[] args) throws Exception {
            // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            String apiKey = System.getenv("DASHSCOPE_API_KEY");
            String appId = "APP_ID"; // 替换为实际的应用 ID
            String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";
    
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .apiKey(apiKey)
                    .baseUrl(baseUrl)
                    .build();
    
            // 异步调用，通过 putAdditionalBodyProperty 传递自定义参数
            Map<String, Object> bizParams = new HashMap<>();
            bizParams.put("city", "北京");
    
            Response response = client.responses().create(
                    ResponseCreateParams.builder()
                            .input("你好")
                            .background(true)
                            .putAdditionalBodyProperty("biz_params",
                                    com.openai.core.JsonValue.from(bizParams))
                            .build()
            );
    
            // 打印完整的响应JSON对象
            ObjectMapper mapper = new ObjectMapper();
            mapper.enable(SerializationFeature.INDENT_OUTPUT);
            System.out.println(mapper.writeValueAsString(response));
        }
    }
    ```
    
    ## curl
    
    ```
    #!/bin/bash
    # ==================== 配置区域 ====================
    # 若没有配置环境变量，请将 ${DASHSCOPE_API_KEY} 替换为实际的阿里云百炼 API Key
    # 但不建议在生产环境中直接将 API Key 硬编码到代码中，以减少 API Key 泄露风险
    # {APP_ID} 替换为实际的应用 ID
    
    # ==================== 调用 API ====================
    curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --data '{
        "input": "你是谁？",
        "background": true,
        "biz_params": {
            "city": "杭州"
        }
    }'
    ```
    
-   **插件参数：**调用时通过`biz_params`传递，`user_defined_params`传递工具参数，`user_defined_tokens`传递鉴权参数，参数名和类型要与工具参数配置保持一致。
    
    ## Python
    
    ```
    """
    阿里云百炼应用调用示例
    异步调用
    """
    from openai import AsyncOpenAI
    import asyncio
    import os
    
    # ==================== 配置区域 ====================
    
    # API Key 配置
    # 若没有配置环境变量，可将下行替换为：api_key="sk-xxx"
    # 但不建议在生产环境中直接将 API Key 硬编码到代码中，以减少泄露风险
    api_key = os.getenv("DASHSCOPE_API_KEY")
    
    # 应用 ID（在百炼控制台 -> 应用 -> 发布渠道 -> API 中获取）
    app_id = 'YOUR_APP_ID'  # 替换为实际的应用 ID
    
    # Base URL
    base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
    
    # ==================== 客户端初始化 ====================
    
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # ==================== 业务参数配置（可选）====================
    
    # biz_params 用于传递自定义参数给应用中的工具/插件
    # YOUR_TOOL_ID 需要替换为实际的工具 ID（在百炼控制台的插件工具详情页获取）
    biz_params = {
        # 自定义参数：传递给指定工具的参数
        "user_defined_params": {
            "YOUR_TOOL_ID": {  # 替换为实际的工具 ID
                "article_index": 9   # 自定义参数，根据工具需求设置
            }
        },
        # 自定义 Token：为指定工具提供认证信息，YOUR_TOKEN替换为示例的认证 Token
        "user_defined_tokens": {
            "YOUR_TOOL_ID": {  # 替换为实际的工具 ID
                "user_token": "YOUR_TOKEN" # 工具所需的认证 Token
            }
        }
    }
    
    # ==================== 主函数 ====================
    
    async def main():
        """异步调用 Agent 应用"""
        
        # 发起异步请求
        # - input: 用户输入的问题或指令
        # - extra_body: 额外参数，包括 biz_params（业务参数）
        # - background: True 表示后台异步执行
        response = await client.responses.create(
            input="你好",
            extra_body={
                "biz_params": biz_params
            },
            background=True
        )
        
        # 打印完整的响应 JSON 对象
        print(response.model_dump_json(indent=2))
    
    
    # ==================== 程序入口 ====================
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    
    ## Java
    
    ```
    import com.openai.client.OpenAIClient;
    import com.openai.client.okhttp.OpenAIOkHttpClient;
    import com.openai.models.responses.*;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.databind.SerializationFeature;
    import java.util.HashMap;
    import java.util.Map;
    
    public class CreateTaskWithPluginParams {
        public static void main(String[] args) throws Exception {
            // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            String apiKey = System.getenv("DASHSCOPE_API_KEY");
            String appId = "YOUR_APP_ID"; // 替换为实际的应用 ID
            String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";
    
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .apiKey(apiKey)
                    .baseUrl(baseUrl)
                    .build();
    
            // 构建 biz_params，包含 user_defined_params 和 user_defined_tokens
            // 自定义参数：传递给指定工具的参数
            Map<String, Object> toolParams = new HashMap<>();
            toolParams.put("article_index", 9);  // 自定义参数，根据工具需求设置
            Map<String, Object> userDefinedParams = new HashMap<>();
            userDefinedParams.put("YOUR_TOOL_ID", toolParams);  // 替换为实际的工具 ID
    
            // 自定义 Token：为指定工具提供认证信息
            Map<String, Object> toolTokens = new HashMap<>();
            toolTokens.put("user_token", "YOUR_TOKEN");  // 工具所需的认证 Token
            Map<String, Object> userDefinedTokens = new HashMap<>();
            userDefinedTokens.put("YOUR_TOOL_ID", toolTokens);  // 替换为实际的工具 ID
    
            Map<String, Object> bizParams = new HashMap<>();
            bizParams.put("user_defined_params", userDefinedParams);
            bizParams.put("user_defined_tokens", userDefinedTokens);
    
            // 异步调用，通过 putAdditionalBodyProperty 传递插件参数
            Response response = client.responses().create(
                    ResponseCreateParams.builder()
                            .input("你好")
                            .background(true)
                            .putAdditionalBodyProperty("biz_params",
                                    com.openai.core.JsonValue.from(bizParams))
                            .build()
            );
    
            // 打印完整的响应JSON对象
            ObjectMapper mapper = new ObjectMapper();
            mapper.enable(SerializationFeature.INDENT_OUTPUT);
            System.out.println(mapper.writeValueAsString(response));
        }
    }
    ```
    
    ## curl
    
    ```
    #!/bin/bash
    # ==================== 配置区域 ====================
    # 若没有配置环境变量，请将 ${DASHSCOPE_API_KEY} 替换为实际的阿里云百炼 API Key
    # 但不建议在生产环境中直接将 API Key 硬编码到代码中，以减少 API Key 泄露风险
    
    APP_ID="YOUR_APP_ID"  # 替换为实际的应用 ID
    
    # ==================== 调用 API ====================
    curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/${APP_ID}/compatible-mode/v1/responses" \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --data '{
        "input": "你是谁？",
        "background": true,
        "biz_params": {
            "user_defined_params": {
                "YOUR_PLUGIN_ID": {
                    "article_index": 9
                }
            },
            "user_defined_tokens": {
                "YOUR_PLUGIN_ID": {
                    "user_token": "YOUR_TOKEN"
                }
            }
        }
    }'
    
    # ==================== 参数说明 ====================
    # biz_params 用于传递自定义参数给 Agent 中的工具/插件：
    #
    # user_defined_params - 自定义参数
    #   YOUR_PLUGIN_ID: 替换为实际的工具 ID
    #   article_index: 自定义参数名和值，根据工具需求设置
    #
    # user_defined_tokens - 自定义 Token（鉴权信息）
    #   YOUR_PLUGIN_ID: 替换为实际的工具 ID
    #   user_token: 工具所需的认证 Token
    ```
    

#### **请求字段说明**

**字段名**

**类型**

**必填**

**描述**

`input`

string/array

是

请求的核心输入内容。可以是单个字符串，或是一个包含多轮对话历史的消息数组。

`background`

boolean

是

是否以异步方式执行任务。

-   `false`（默认值）：启用同步模式。API将保持连接直到任务完成。
    
-   `true`：启用异步模式。API将立即返回一个任务ID，可通过查询接口来获取任务状态和结果。
    

extra\_body

_object_

否

额外参数字段。

extra\_body.biz\_params

_object_

否

应用通过自定义变量、节点或插件传递参数时，使用该字段进行传递。

user\_defined\_params

_object_

否

表示自定义插件参数信息。

一个应用内添加的插件不可重复，且上限 10 个。

user\_defined\_tokens

_object_

否

表示自定义插件的用户级鉴权信息。

一个应用内添加的插件不可重复，且上限 10 个。

user\_defined\_tokens.user\_token

_string_

否

传递该插件需要的用户鉴权信息。

#### **响应示例**

```
{
  "id": "bcb9728b-a7f8-480c-ace0-8d61ff776857",
  "created_at": 1761875532,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": null,
  "model": "",
  "object": "response",
  "output": [],
  "parallel_tool_calls": false,
  "temperature": null,
  "tool_choice": "auto",
  "tools": [],
  "top_p": null,
  "background": null,
  "conversation": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": null,
  "safety_identifier": null,
  "service_tier": null,
  "status": "queued",
  "text": null,
  "top_logprobs": null,
  "truncation": null,
  "usage": null,
  "user": null
}
```

#### **响应字段说明**

**字段名**

**类型**

**描述**

`id`

string

异步任务的唯一标识符，用于后续查询、取消或删除操作。

`status`

string

任务的初始状态，通常为 `queued`。

`created_at`

integer

任务创建时间的Unix时间戳（秒）。

`object`

string

对象类型，固定为`response`。

### **查询任务**

获取指定任务的当前状态和执行结果。

**Endpoint:**`GET https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses/{RESPONSE_ID}`

> 请将 `{APP_ID}` 替换为实际的应用 ID，将 `{RESPONSE_ID}` 替换为创建任务时返回的任务ID。

#### **请求示例**

#### **Python**

```
import asyncio
import os
from openai import AsyncOpenAI

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 1、替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = AsyncOpenAI(api_key=api_key, base_url=base_url)

async def main():
  # 查询任务状态
  response = await client.responses.retrieve("6e4ba287-0e93-4d67-9955-ef1017ed3384") # 2、替换为实际的任务 ID
  print(response.model_dump_json(indent=2))

if __name__ == "__main__":
  asyncio.run(main())
```

#### **Java**

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

public class RetrieveTask {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String appId = "APP_ID"; // 1、替换为实际的应用 ID
        String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";

        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .build();

        // 查询任务状态
        String responseId = "6e4ba287-0e93-4d67-9955-ef1017ed3384"; // 2、替换为实际的任务 ID
        Response response = client.responses().retrieve(responseId);

        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);
        System.out.println(mapper.writeValueAsString(response));
    }
}
```

#### **curl**

```
# 若没有配置环境变量，请将 {DASHSCOPE_API_KEY} 替换为实际的阿里云百炼API Key，但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
# 1、请将 APP_ID 替换为实际的应用ID
# 2、请将 RESPONSE_ID 替换为创建异步任务返回的ID
# 实际使用时请删除注释内容
curl "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses/{RESPONSE_ID}" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

#### **响应示例**

```
{
  "id": "bcb9728b-a7f8-480c-ace0-8d61ff776857",
  "created_at": 1761875537,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": null,
  "model": "",
  "object": "response",
  "output": [
    {
      "id": "msg_d89e8cb9-f8fa-4092-bb86-928e21839f64",
      "content": [
        {
          "annotations": [],
          "text": "你好，我是千问（Qwen），是阿里巴巴集团旗下的千问实验室自主研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本等等，还能进行逻辑推理、编程，甚至表达观点和玩游戏。我的目标是成为你值得信赖的智能助手。有什么我可以帮到你的吗？",
          "type": "output_text",
          "logprobs": null
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": false,
  "temperature": null,
  "tool_choice": "auto",
  "tools": [],
  "top_p": null,
  "background": null,
  "conversation": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": null,
  "safety_identifier": null,
  "service_tier": null,
  "status": "completed",
  "text": null,
  "top_logprobs": null,
  "truncation": null,
  "usage": null,
  "user": null
}
```

#### **响应字段说明**

**字段名**

**类型**

**描述**

`id`

string

异步任务的唯一标识符。

`status`

string

任务的当前状态，详见[任务生命周期](#2627a01eaf9z0)。

`output`

array

任务的输出结果。当 `status` 为 `completed` 时，此字段包含最终结果。

### **取消任务**

取消一个正在进行中的异步任务。此操作仅对状态为 `queued` 或 `running` 的任务有效。

**Endpoint:**`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses/{RESPONSE_ID}/cancel`

> 请将 `{APP_ID}` 替换为实际的应用ID，将 `{RESPONSE_ID}` 替换为创建任务时返回的任务ID。

#### **请求示例**

Python

```
import asyncio
import os
from openai import AsyncOpenAI

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 1、替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = AsyncOpenAI(api_key=api_key, base_url=base_url)

async def main():
  # 取消任务
  response = await client.responses.cancel("6e4ba287-0e93-4d67-9955-ef1017ed3384") # 2、替换为实际的任务 ID
  print(response.model_dump_json(indent=2))

if __name__ == "__main__":
  asyncio.run(main())
```

Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

public class CancelTask {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String appId = "APP_ID"; // 1、替换为实际的应用 ID
        String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";

        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .build();

        // 取消任务
        String responseId = "6e4ba287-0e93-4d67-9955-ef1017ed3384"; // 2、替换为实际的任务 ID
        Response response = client.responses().cancel(responseId);

        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);
        System.out.println(mapper.writeValueAsString(response));
    }
}
```

curl

```
# 若没有配置环境变量，请将 {DASHSCOPE_API_KEY} 替换为实际的阿里云百炼API Key，但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
# 1、请将 APP_ID 替换为实际的应用ID
# 2、请将 RESPONSE_ID 替换为创建异步任务返回的ID
# 实际使用时请删除注释内容
curl -X POST "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses/{RESPONSE_ID}/cancel" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

#### **响应示例**

```
{
    "created_at": 1761877521,
    "id": "568b1459-126d-4719-b58f-b41078bacb48",
    "model": "",
    "object": "response",
    "output": [

    ],
    "parallel_tool_calls": false,
    "status": "cancelled",
    "tool_choice": "auto",
    "tools": [

    ]
}
```

#### **响应字段说明**

**字段名**

**类型**

**描述**

`id`

string

被操作任务的唯一标识符。

`status`

string

任务被取消后的状态，如：

`cancelled`：表示任务已成功取消。

`failed`：表示取消失败，因为任务已经处于终态（如`completed`或`failed`）。

`object`

string

对象类型，固定为`response`。

### **删除任务记录**

删除一个已处于终态（`completed`, `failed`, `cancelled`）的任务记录。此操作不可恢复。

**Endpoint:**`DELETE https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses/{RESPONSE_ID}`

> 请将 `{APP_ID}` 替换为实际的应用ID，将 `{RESPONSE_ID}` 替换为创建任务时返回的任务ID。

#### **请求示例**

## Python

```
import asyncio
import os
from openai import AsyncOpenAI

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。
# 不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key = os.getenv("DASHSCOPE_API_KEY")
app_id = 'APP_ID'  # 1. 替换为您的应用ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

client = AsyncOpenAI(api_key=api_key, base_url=base_url)

async def main():
    # 2. 替换为要删除的任务ID
    response_id_to_delete = "b17c64f94-7034-403e-aef5-4f48647656d5" 
    try:
        response_wrapper = await client.responses.with_raw_response.delete(response_id_to_delete)
        http_response = response_wrapper.http_response
        response_json = http_response.json()

        # 检查响应内容中的 "deleted" 字段是否为 true。
        if response_json.get("deleted") is True:
            print("任务记录已成功删除。")
            print(response_json)
        else:
            print("删除操作未成功")
            print(response_json)

    except Exception as e:
        print(f"\n调用API时发生严重错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.*;

public class DeleteTask {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String appId = "APP_ID"; // 1. 替换为您的应用ID
        String baseUrl = "https://dashscope.aliyuncs.com/api/v2/apps/agent/" + appId + "/compatible-mode/v1/";

        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .build();

        // 2. 替换为要删除的任务ID
        String responseId = "b17c64f94-7034-403e-aef5-4f48647656d5";
        client.responses().delete(responseId);
        System.out.println("任务记录已成功删除。ID: " + responseId);
    }
}
```

## curl

```
# 若没有配置环境变量，请将 {DASHSCOPE_API_KEY} 替换为实际的阿里云百炼API Key，但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
# 1、请将 APP_ID 替换为实际的应用ID
# 2、请将 RESPONSE_ID 替换为创建异步任务返回的ID
# 实际使用时请删除注释内容
curl -X DELETE "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses/{RESPONSE_ID}" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

#### **响应示例**

```
{
    "deleted": true,
    "id": "c8eddc0e-faf5-4228-a853-9c411194015f",
    "object": "response"
}
```

#### **响应字段说明**

**字段名**

**类型**

**描述**

`id`

string

被删除任务的唯一标识符。

`deleted`

boolean

`true` 表示任务记录已成功删除。

`object`

string

对象类型，固定为`response`。

## **任务生命周期**

异步任务的生命周期包含以下状态：

**状态值**

**描述**

`queued`

任务已成功创建，正在队列中等待系统调度。

`running`

任务正在执行中。

`completed`

任务已成功完成。可在响应的 `output` 字段中获取结果。

`cancelled`

任务在执行完成前被用户主动取消。

`failed`

任务执行失败。可在响应的 `output` 字段中查看错误信息。

## 错误码

如果应用调用失败并返回报错信息，请参阅[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

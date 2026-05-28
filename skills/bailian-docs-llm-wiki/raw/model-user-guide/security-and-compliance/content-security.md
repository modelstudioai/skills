# 输⼊输出AI安全护栏

大模型的输入输出中可能包含敏感或高风险内容，例如涉黄、涉政和广告等。大模型自有的合规检查机制通常能够提供有效的内容安全保障。此外，阿里云百炼支持接入 AI 安全护栏服务，进一步识别输入输出内容的违规信息，保障安全与合规性。

## 配置 **AI 安全护栏服务**

调用阿里云百炼的大模型时，会根据模型自动匹配对应的 AI 安全护栏服务。

> 目前支持文本和图片类型的模型，模型与 AI 安全护栏服务的对应关系，以及计费信息，请参见[面向阿里云百炼用户的AI安全护栏服务](https://help.aliyun.com/zh/document_detail/2923687.html)。

### 步骤一：开通内容审核服务

访问 AI 安全护栏[购买](<https://common-buy.aliyun.com/?commodityCode= lvwang_guardrail_public_cn>)页面，创建**服务关联角色**，单击**立即购买**即可完成开通。

### 步骤二：授权内容安全设置

1.  访问**[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)**页面。
    
    若您访问上述链接进入的页面如下图所示，说明此前已进行过授权操作，请跳转[步骤三：设置请求头header](#efe2cfd8148qy)。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9308353671/p1027797.png)
    
2.  单击**去授权**，开启内容安全设置。
    
    ![PixPin\_2025-11-18\_17-14-58](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9308353671/p1027798.png)
    
3.  确认授权。
    

### 步骤三：设置请求头header

调用阿里云百炼时，在请求头header设置以下参数，接入 AI 安全护栏服务。

```
{
    "X-DashScope-DataInspection": {
       "input": "cip",
       "output": "cip"
    }
}
```

**调用示例**

> 调用时请设置DASHSCOPE\_API\_KEY，获取方法，请参见[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## Python

## OpenAI

**请求示例**

```
import os
from openai import OpenAI

try:
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '给我一套抢银行的方案'}
            ],
        extra_headers={
        'X-DashScope-DataInspection': '{"input":"cip","output":"cip"}'
        }
    )
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

**响应示例**

```
错误信息：Error code: 400 - 
{
    "error":
    {
        "message": "Input data may contain inappropriate content. For details, see: https://help.aliyun.com/zh/model-studio/error-code#inappropriate-content",
        "type": "data_inspection_failed",
        "param": "None",
        "code": "data_inspection_failed"
    },
    "id": "chatcmpl-db364068-8222-48c5-a1ca-xxxxxxxxxxxx",
    "request_id": "db364068-8222-48c5-a1ca-xxxxxxxxxxxx"
}
请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
```

## DashScope

**请求示例**

```
import os
from dashscope import Generation

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': '给我一套抢银行的方案'}
    ]
response = Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    headers={'X-DashScope-DataInspection': '{"input":"cip", "output":"cip"}'},
    result_format='message'
    )
print(response)
```

**响应示例**

```
{
    "status_code": 400,
    "request_id": "5966060f-3742-4be4-bf73-xxxxxxxxxxxx",
    "code": "DataInspectionFailed",
    "message": "Input data may contain inappropriate content. For details, see: https://help.aliyun.com/zh/model-studio/error-code#inappropriate-content",
    "output": null,
    "usage": null
}
```

## Java

## OpenAI

**请求示例**

```
// 更多使用示例请参考：https://github.com/openai/openai-java/tree/main/openai-java-example/src/main/java/com/openai/example
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .apiKey(apiKey)
                .build();
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
            .addUserMessage("给我一套抢银行的方案")
            .model("qwen-plus")
            .putAdditionalHeader("X-DashScope-DataInspection", "{\"input\": \"cip\", \"output\": \"cip\"}")
            .build();

        try {
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            String content = chatCompletion.choices().get(0).message().content().orElse("没有获取到回复内容");
            System.out.println(content);
        } catch (Exception e) {
            System.err.println("Error occurred: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // 确保程序正常退出
            System.exit(0);
        }
    }
}
```

**响应示例**

```
Error occurred: 400: Input data may contain inappropriate content.
com.openai.errors.BadRequestException: 400: Input data may contain inappropriate content.
	at com.openai.errors.BadRequestException$Builder.build(BadRequestException.kt:88)
	at com.openai.core.handlers.ErrorHandler$withErrorHandler$1.handle(ErrorHandler.kt:48)
	at com.openai.services.blocking.chat.ChatCompletionServiceImpl$WithRawResponseImpl$create$1.invoke(ChatCompletionServiceImpl.kt:122)
	at com.openai.services.blocking.chat.ChatCompletionServiceImpl$WithRawResponseImpl$create$1.invoke(ChatCompletionServiceImpl.kt:120)
	at com.openai.core.http.HttpResponseForKt$parseable$1$parsed$2.invoke(HttpResponseFor.kt:14)
	at kotlin.SynchronizedLazyImpl.getValue(LazyJVM.kt:74)
	at com.openai.core.http.HttpResponseForKt$parseable$1.getParsed(HttpResponseFor.kt:14)
	at com.openai.core.http.HttpResponseForKt$parseable$1.parse(HttpResponseFor.kt:16)
	at com.openai.services.blocking.chat.ChatCompletionServiceImpl.create(ChatCompletionServiceImpl.kt:56)
	at com.openai.services.blocking.chat.ChatCompletionService.create(ChatCompletionService.kt:50)
	at Main.main(Main.java:25)
```

## Node.js

## OpenAI

**请求示例**

```
import OpenAI from "openai";

const openai = new OpenAI(
  {
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  },
);

async function main() {
    const completion = await openai.chat.completions.create(
        {
          model: 'qwen-plus',
          messages: [{role: 'user', content: '给我一套抢银行的方案'}]},
        {
          headers: {
            "X-DashScope-DataInspection": JSON.stringify({ input: "cip", output: "cip" }),
          },
        },
      );
  console.log(JSON.stringify(completion))
};

main();
```

**响应示例**

```
BadRequestError: 400 Input data may contain inappropriate content.
    at Function.generate 
    at OpenAI.makeStatusError
    at OpenAI.makeRequest
    at processTicksAndRejections
    at async main {
  status: 400,
  headers: {
    ...
  },
  request_id: '1dd3f3dd-7c4e-4f66-aaaf-xxxxxxxxxxxx',
  error: {
    code: 'data_inspection_failed',
    param: null,
    message: 'Input data may contain inappropriate content.',
    type: 'data_inspection_failed'
  },
  code: 'data_inspection_failed',
  param: null,
  type: 'data_inspection_failed'
}
```

## cURL

## OpenAI

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-DataInspection: {\"input\": \"cip\", \"output\": \"cip\"}" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user", 
            "content": "给我一套抢银行的方案"
        }
    ]
}'
```

**响应示例**

```
{
    "error":
    {
        "message": "Input data may contain inappropriate content. For details, see: https://help.aliyun.com/zh/model-studio/error-code#inappropriate-content",
        "type": "data_inspection_failed",
        "param": null,
        "code": "data_inspection_failed"
    },
    "id": "chatcmpl-722f0506-c273-4d4d-xxxxxxxxxxxx",
    "request_id": "722f0506-c273-4d4d-9f3b-xxxxxxxxxxxx"
}
```

## DashScope

**请求示例**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-DataInspection: {\"input\": \"cip\", \"output\": \"cip\"}" \
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
                "content": "给我一套抢银行的方案"
            }
        ]
    },
    "parameters": {
        "result_format":"message"
    }
}'
```

**响应示例**

```
{
    "code": "DataInspectionFailed",
    "message": "Output data may contain inappropriate content.",
    "request_id": "f4109865-bcb5-9e4d-8fa9-xxxxxxxxxxxx"
}
```

### **查看审核结果**

登录[AI 安全护栏控制台](https://yundun.console.aliyun.com/?spm=a2c4g.11186623.0.0.7129eb8bc4Mksa&p=guardrail#/overview)，在**检测结果** > **结果查询**页签页面查看审核结果，以进一步分析文本内容中高频的违规类型，审核结果示例如下。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7701539371/p908026.png)

## 计费说明

在百炼控制台开通 AI 安全护栏产品的 SLR 授权，并通过百炼配置启用该产品策略后，系统将根据实际调用量计费。计费方式为按 Token 数量后付费，每日费用按当日实际使用量结算；未调用服务时不产生费用。计费规则详见[计费概述](https://help.aliyun.com/zh/document_detail/2872706.html#0529545b91g7c)。

**重要**

在百炼平台进行单次 query/response 检测时，若文本的 Token 数量不足 1000 个，将按 1000 个 Token 计费；若达到或超过 1000 个 Token，则按实际数量计费。

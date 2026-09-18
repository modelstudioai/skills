# 结构化输出

执行信息抽取或结构化数据生成任务时，大模型可能返回多余文本（如 \`\`\`json ）导致下游解析失败。开启结构化输出可确保大模型输出标准格式的 JSON 字符串，使用 JSON Schema 模式还能精确控制输出结构和类型，无需额外验证或重试。

## 使用方式

结构化输出支持JSON Object 与 JSON Schema两种模式：

-   **JSON Object 模式**：确保输出为标准格式的 JSON 字符串，但不保证符合特定结构。使用方式：
    
    1.  **设置**`response_format`**参数**：在请求体中，将 `response_format` 参数设置为 `{"type": "json_object"}`。
    2.  **提示词包含 JSON 关键词**：System Message 或 User Message 中需要包含 "JSON" 关键词（不区分大小写），否则会报错：`'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.`
-   [**JSON Schema 模式**](https://help.aliyun.com/zh/model-studio/qwen-structured-output#a4f5d7108anxd)：确保输出内容为指定的结构。使用方式：设置 `response_format` 为`{"type": "json_schema", "json_schema": {..., "strict": true}}`。
    
    > 提示词无需包含 JSON 关键词。
    

功能对比：

**特性**

**JSON Object 模式**

**JSON Schema 模式**

输出有效 JSON

是

是

严格遵循 Schema

否

是

支持模型

Qwen 大部分模型、Kimi、GLM、DeepSeek、Stepfun

仅支持部分模型

`response_format` 参数设置

`{"type": "json_object"}`

`{"type": "json_schema", "json_schema": {..., "strict": true}}`

提示词要求

必须包含 "JSON"

建议明确说明

适用场景

灵活的 JSON 输出

精确的结构验证

## 支持的模型

#### JSON Object

#### 千问

-   **文本生成模型**
    -   千问Max：Qwen3.8-Max系列、Qwen3.7-Max系列
    -   千问Max（非思考模式）：Qwen3.6-Max系列、Qwen3-Max系列、Qwen-Max系列
    -   千问Plus：Qwen3.7-Plus系列
    -   千问Plus（非思考模式）：Qwen3.6-Plus系列、Qwen3.5-Plus系列、Qwen-Plus系列
    -   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列
    -   千问Flash（非思考模式）：Qwen3.6-Flash系列、Qwen3.5-Flash系列、Qwen-Flash系列
    -   千问Turbo（非思考模式）：Qwen-Turbo系列
    -   千问Coder：Qwen3-Coder系列
    -   千问Long：Qwen-Long系列
    -   Qwen3.8开源系列
    -   Qwen3.6开源系列（非思考模式）
    -   Qwen3.5开源系列（非思考模式）
    -   Qwen3开源系列（非思考模式）
    -   Qwen3-Coder开源系列
    -   Qwen2.5开源系列（不含math与coder模型）
-   **多模态模型**
    -   千问VL（非思考模式）：Qwen3-VL-Plus系列、Qwen3-VL-Flash系列、Qwen-VL-Max系列（不包括最新版与快照版模型）、Qwen-VL-Plus系列（不包括最新版与快照版模型）
    -   千问Omni：Qwen3.8-Omni-Flash、Qwen3.5-Omni-Plus系列
    -   Qwen3-VL 开源系列（非思考模式）

**说明**标注为"非思考模式"的模型，在思考模式下设置 `response_format` 为 `{"type": "json_object"}` 不会报错，但结构化输出可能失效，如需稳定获取标准 JSON，可参考"常见问题"中的处理方式。

#### Kimi

-   阿里云百炼部署
    
    -   kimi-k3
    -   kimi-k2-thinking
-   月之暗面部署
    
    -   kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code 、kimi/kimi-k2.6、kimi/kimi-k2.5

#### DeepSeek

-   阿里云百炼部署
    
    -   deepseek-v4-pro、deepseek-v4-flash
-   快手万擎部署
    
    -   vanchin/deepseek-v3.2-think、vanchin/deepseek-v3、vanchin/deepseek-ocr

#### GLM

-   glm-5.1、glm-4.5、glm-4.5-air
-   非思考模式：glm-5、glm-4.7、glm-4.6

#### Stepfun

混合思考模式：stepfun/step-3.7-flash

#### JSON Schema

Qwen3.7-Plus 系列、Qwen3.8-Flash 系列、Qwen3.7-Flash 系列、Qwen3.7-Max 系列、Qwen3.8-Max 系列模型

## 快速开始

以从个人简介中抽取信息为例，演示结构化输出的基本用法。

> JSON Object 模式不保证键名与字段类型稳定，不同提示词或不同次调用的返回结果可能存在差异。如需固定结构，请使用 JSON Schema 模式。

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK或DashScope SDK进行调用，还需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

#### OpenAI兼容

#### Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
        },
    ],
    response_format={"type": "json_object"}
)

json_string = completion.choices[0].message.content
print(json_string)
```

### 返回结果

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 如果没有配置环境变量，请用API Key将下行替换为：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

const completion = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: [
        {
            role: "system",
            content: "请抽取用户的姓名与年龄信息，以JSON格式返回"
        },
        {
            role: "user",
            content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
        }
    ],
    response_format: {
        type: "json_object"
    }
});

const jsonString = completion.choices[0].message.content;
console.log(jsonString);
```

### 返回结果

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages": [
        {
            "role": "system",
            "content": [{"type": "text", "text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
        },
        {
            "role": "user",
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com"
        }
    ],
    "response_format": {
        "type": "json_object"
    }
}'
```

### 返回结果

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "{\"name\":\"刘五\",\"age\":\"34岁\"}"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 207,
        "completion_tokens": 20,
        "total_tokens": 227,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "created": 1756455080,
    "system_fingerprint": null,
    "model": "qwen3.8-max",
    "id": "chatcmpl-624b665b-fb93-99e7-9ebd-bb6d86d314d2"
}
```

#### DashScope

#### Python

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1"
messages=[
    {
        "role": "system",
        "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
    },
    {
        "role": "user",
        "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
    },
]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.8-max",
    messages=messages,
    response_format={'type': 'json_object'}
    )
json_string = response.output.choices[0].message.content[0]["text"]
print(json_string)
```

### 返回结果

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

#### Java

DashScope Java SDK版本需要不低于 2.21.4。

```
// DashScope Java SDK 版本需要不低于 2.21.4

import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.common.ResponseFormat;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "请抽取用户的姓名与年龄信息，以JSON格式返回"))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"))).build();
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(systemMessage, userMessage))
                .responseFormat(jsonMode)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

### 返回结果

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": {
        "messages": [
            {
                "role": "system",
                "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
            },
            {
                "role": "user",
                "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]
            }
        ]
    },
    "parameters": {
        "response_format": {
            "type": "json_object"
        }
    }
}'
```

### 返回结果

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "text": "{\n  \"姓名\": \"刘五\",\n  \"年龄\": 34\n}"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 72,
        "output_tokens": 18,
        "input_tokens": 54,
        "cached_tokens": 0
    },
    "request_id": "xxx-xxx-xxx-xxx-xxx"
}
```

## 图片、视频数据处理

多模态模型同样支持对图像和视频数据进行结构化输出。通过JSON Mode，可以从视觉内容中提取结构化数据，例如票据字段、图像中的目标位置或视频中的事件信息。

> 图片、视频文件限制请参见 [图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md) 。

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"
                    },
                },
                {"type": "text", "text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"},
            ],
        },
    ],
    response_format={"type": "json_object"}
)
json_string = completion.choices[0].message.content
print(json_string)
```

### 返回结果

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
  // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
  const response = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: [{
        role: "system",
        content: [{
          type: "text",
          text: "You are a helpful assistant."
        }]
      },
      {
        role: "user",
        content: [{
            type: "image_url",
            image_url: {
              "url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"
            }
          },
          {
            type: "text",
            text: "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"
          }
        ]
      }
    ],
    response_format: {type: "json_object"}
  });
  console.log(response.choices[0].message.content);
}

main()
```

### 返回结果

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.8-max",
  "messages": [
  {"role":"system",
  "content":[
    {"type": "text", "text": "You are a helpful assistant."}]},
  {
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"}},
      {"type": "text", "text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
    ]
  }],
  "response_format":{"type": "json_object"}
}'
```

### 返回结果

```
{
  "choices": [{
    "message": {
      "content": "{\n  \"ticket\": [\n    {\n      \"travel_date\": \"2013-06-29\",\n      \"trains\": \"流水\",\n      \"seat_num\": \"371\",\n      \"arrival_site\": \"开发区\",\n      \"price\": \"8.00\"\n    }\n  ],\n  \"invoice\": [\n    {\n      \"invoice_code\": \"221021325353\",\n      \"invoice_number\": \"10283819\"\n    }\n  ]\n}",
      "role": "assistant"
    },
    "finish_reason": "stop",
    "index": 0,
    "logprobs": null
  }],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 486,
    "completion_tokens": 112,
    "total_tokens": 598,
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "created": 1755767481,
  "system_fingerprint": null,
  "model": "qwen3.8-max",
  "id": "chatcmpl-33249829-e9f3-9cbc-93e4-0536b3d7d713"
}
```

#### DashScope

#### Python

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1"
messages = [
{
    "role": "system",
    "content": [
    {"text": "You are a helpful assistant."}]
},
{
    "role": "user",
    "content": [
    {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
    {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}]
}]
response = dashscope.MultiModalConversation.call(
    #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'qwen3.8-max',
    messages = messages,
    response_format={'type': 'json_object'}
)
json_string = response.output.choices[0].message.content[0]["text"]
print(json_string)
```
```
import os
import dashscope

# 若使用北京地域的模型，需将base_url替换为：https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1'

messages = [
{
    "role": "system",
    "content": [
    {"text": "You are a helpful assistant."}]
},
{
    "role": "user",
    "content": [
    {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
    {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}]
}]
response = dashscope.MultiModalConversation.call(
    #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'qwen3.8-max',
    messages = messages,
    response_format={'type': 'json_object'}
)
json_string = response.output.choices[0].message.content[0]["text"]
print(json_string)
```

### 返回结果

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

#### Java

```
// DashScope Java SDK 版本需要不低于 2.21.4

import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.common.ResponseFormat;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "You are a helpful assistant."))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"),
                        Collections.singletonMap("text", "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"))).build();
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(systemMessage, userMessage))
                .responseFormat(jsonMode)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

### 返回结果

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {"role": "system",
         "content": [
           {"text": "You are a helpful assistant."}]},
            {
             "role": "user",
             "content": [
               {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
               {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
                ]
            }
        ]
    },
    "parameters": {
        "response_format": {"type": "json_object"}
    }
}'
```

### 返回结果

```
{
  "output": {
    "choices": [
      {
        "message": {
          "content": [
            {
              "text": "{\n  \"ticket\": [\n    {\n      \"travel_date\": \"2013-06-29\",\n      \"trains\": \"流水\",\n      \"seat_num\": \"371\",\n      \"arrival_site\": \"开发区\",\n      \"price\": \"8.00\"\n    }\n  ],\n  \"invoice\": [\n    {\n      \"invoice_code\": \"221021325353\",\n      \"invoice_number\": \"10283819\"\n    }\n  ]\n}"
            }
          ],
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ]
  },
  "usage": {
    "total_tokens": 598,
    "input_tokens_details": {
      "image_tokens": 418,
      "text_tokens": 68
    },
    "output_tokens": 112,
    "input_tokens": 486,
    "output_tokens_details": {
      "text_tokens": 112
    },
    "image_tokens": 418
  },
  "request_id": "b129dce1-0d5d-4772-b8b5-bd3a1d5cde63"
}
```

## 思考模型的结构化输出

启用思考模型的结构化输出后，模型会先进行推理再生成 JSON，输出结果通常比非思考模型更准确。

#### OpenAI兼容

#### Python

### 示例代码

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages=[
    {
        "role": "system",
        "content": [{"type": "text", "text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
    },
    {
        "role": "user",
        "content": [{"type": "text", "text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
    },
]

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True,
    stream_options={
        "include_usage": True
    },
    response_format={"type": "json_object"}
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

用户要求抽取姓名与年龄信息，并以JSON格式返回。

从文本中可以看到：
- 姓名：刘五
- 年龄：34
- 邮箱：liuwu@example.com（但用户只要求姓名和年龄）
- 爱好：打篮球和旅游（但用户只要求姓名和年龄）

根据要求，只需要提取姓名和年龄信息，并以JSON格式返回。

JSON格式应该是：
{
  "姓名": "刘五",
  "年龄": 34
}

或者使用英文键名：
{
  "name": "刘五",
  "age": 34
}

考虑到用户使用的是中文提问，使用中文键名可能更合适。不过通常JSON键名使用英文也是常见做法。这里我采用中文键名，因为用户的指令是中文的，且提取的信息也是中文语境下的。

最终输出：
{
  "姓名": "刘五",
  "年龄": 34
}
====================完整回复====================

{"姓名":"刘五","年龄":34}
Usage:
CompletionUsage(completion_tokens=203, prompt_tokens=48, total_tokens=251, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=190, rejected_prediction_tokens=None), prompt_tokens_details=None)
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
            },
        ];
        const stream = await openai.chat.completions.create({
            model: 'qwen3.8-max',
            messages,
            stream: true,
            enable_thinking: true,
            response_format: {type: 'json_object'},
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

1.  **分析用户请求：**
    *   **核心任务：** 从给定文本中提取特定信息。
    *   **目标信息：** “姓名”和“年龄”。
    *   **输入文本：** “大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游”
    *   **输出格式：** “JSON格式”。

2.  **将输入文本分解为关键信息片段：**
......
    *   我应该以一个干净、不包含额外文本、可直接使用的JSON格式呈现最终答案。除非用户另有说明，否则无需向JSON本身添加对话性填充内容。

这个过程从理解请求、分解输入、提取数据、选择正确的格式和结构，到最终组装，确保了满足用户的所有约束条件。
====================完整回复====================

{  "姓名": "刘五",
  "年龄": 34
}
```

#### HTTP

### 示例代码

#### curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages": [
    {
            "role": "system",
            "content": [{"type": "text", "text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true,
    "response_format": {
        "type": "json_object"
    }
}'
```

#### DashScope

#### Python

### 示例代码

```
import os
import dashscope

messages = [
    {
        "role": "system",
        "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
    },
    {"role": "user", "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]}
]

completion = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,
    response_format={"type": "json_object"},
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
    if (
        not chunk.output.choices[0].message.content
        and chunk.output.choices[0].message.reasoning_content == ""
    ):
        pass
    else:
        # 如果当前为思考过程
        if (
            chunk.output.choices[0].message.reasoning_content != ""
            and not chunk.output.choices[0].message.content
        ):
            print(chunk.output.choices[0].message.reasoning_content, end="", flush=True)
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="", flush=True)
            answer_content += chunk.output.choices[0].message.content[0]["text"]
```

### 返回结果

```
====================思考过程====================
1.  **识别用户目标：**用户希望我从他们的句子中提取特定的信息（姓名和年龄），并以特定的格式（JSON）返回。
...
7.  **最终审查：**
    *   JSON是否包含姓名“刘五”？是的。
    *   JSON是否包含年龄34？是的。
    *   格式是有效的JSON吗？是的。
    *   它是否直接回答了用户的请求？是的。

这个过程很简单，因为它是一个直接的信息提取任务。关键在于解析中文句子以找到模式（“我叫...”，“今年...岁”），然后按照要求正确格式化提取的数据。
====================完整回复====================
{  "姓名": "刘五",
  "年龄": 34
}
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.22.1
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.common.ResponseFormat;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleResult(MultiModalConversationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (reasoning != null && !reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (content != null && !content.isEmpty()) {
            String text = (String) content.get(0).get("text");
            finalContent.append(text);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    private static MultiModalConversationParam buildParam(List<MultiModalMessage> msgs) {
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .enableThinking(true)
                .incrementalOutput(true)
                .messages(msgs)
                .responseFormat(jsonMode)
                .build();
    }
    public static void streamCall(MultiModalConversation conv, List<MultiModalMessage> msgs)
            throws NoApiKeyException, ApiException, UploadFileException {
        MultiModalConversationParam param = buildParam(msgs);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> handleResult(message));
    }

    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", "请抽取用户的姓名与年龄信息，以JSON格式返回"))).build();
            MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"))).build();
            List<MultiModalMessage> msgs = Arrays.asList(systemMsg, userMsg);
            streamCall(conv, msgs);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
    }
}
```

### 返回结果

```
====================思考过程====================
1.  **分析用户的请求。**
    *   **用户的输入：** "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游" （大家好，我叫刘五，我今年34岁，我的邮箱是 liuwu@example.com，我喜欢打篮球和旅游。）
    *   **核心任务：** "请抽取用户的姓名与年龄信息" （请提取用户的姓名和年龄信息。）
    *   **输出格式：** "以JSON格式返回" （以JSON格式返回）。
...
6.  **审查和优化输出。**
    *   JSON格式正确吗？是的，它有花括号、双引号包裹的键、正确的值（字符串加引号，数字不加）以及键值对之间的逗号。
    *   它是否按要求包含了*仅*姓名和年龄？是的。
    *   摘取的信息是否准确？是的，“刘五”和“34”直接来自用户的文本。
    *   输出可以直接使用。无需额外的解释，除非我想增加一些礼貌性。像“好的，已为您提取信息：”这样的简单短语是很好的客户服务。我们加上这个吧。
    *   最终的响应应该是：
        *   一段简短、礼貌的开场白。
        *   包含在 ```json ... ``` 代码块中的JSON对象，以实现良好的格式化并防止转义问题。

这个思考过程从理解高层级需求，到分析输入、提取特定数据、设计输出格式、构建它，最后再为清晰和正确性进行审查。这是一个系统性的方法，确保准确性并遵循用户指令。
====================完整回复====================
{  "姓名": "刘五",
  "年龄": 34
}
```

#### HTTP

### 示例代码

#### curl

```
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]
            },
            {
                "role": "user",
                "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "response_format": {
            "type": "json_object"
        }
    }
}'
```

## 优化提示词

模糊的提示词（如”返回用户信息”）会导致输出结构不可预期。为获得可靠的结果，建议在提示词中明确描述预期的 Schema：指定字段名称、类型、是否必填、格式要求（如日期格式），并提供示例。

#### OpenAI兼容

#### Python

```
from openai import OpenAI
import os
import json
import textwrap  # 用于处理多行字符串的缩进，提高代码可读性

# 预定义示例响应，用于向模型展示期望的输出格式
# 示例1：包含所有字段的完整响应
example1_response = json.dumps(
    {
        "info": {"name": "张三", "age": "25岁", "email": "zhangsan@example.com"},
        "hobby": ["唱歌"]
    },
    ensure_ascii=False
)
# 示例2：包含多个hobby的响应
example2_response = json.dumps(
    {
        "info": {"name": "李四", "age": "30岁", "email": "lisi@example.com"},
        "hobby": ["跳舞", "游泳"]
    },
    ensure_ascii=False
)
# 示例3：不包含hobby字段的响应（hobby非必需）
example3_response = json.dumps(
    {
        "info": {"name": "赵六", "age": "28岁", "email": "zhaoliu@example.com"}
    },
    ensure_ascii=False
)
# 示例4：另一个不包含hobby字段的响应
example4_response = json.dumps(
    {
        "info": {"name": "孙七", "age": "35岁", "email": "sunqi@example.com"}
    },
    ensure_ascii=False
)

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 使用dedent去除字符串缩进，使多行字符串在代码中美观，但运行时不包含额外空格
system_prompt = textwrap.dedent(f"""\
    请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

    【输出格式要求】
    输出必须严格遵循以下JSON结构：
    {{
      "info": {{
        "name": "字符串类型，必需字段，用户姓名",
        "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
        "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
      }},
      "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
    }}

    【字段提取规则】
    1. name: 从文本中识别用户姓名，必需提取
    2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
    3. email: 识别邮箱地址，保持原始格式，必需提取
    4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

    【参考示例】
    示例1（包含爱好）：
    Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
    A：{example1_response}

    示例2（包含多个爱好）：
    Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
    A：{example2_response}

    示例3（不包含爱好）：
    Q：我叫赵六，今年28岁，我的邮箱是zhaoliu@example.com
    A：{example3_response}

    示例4（不包含爱好）：
    Q：我是孙七，35岁，邮箱sunqi@example.com
    A：{example4_response}

    请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。\
""")

# 调用大模型API进行信息提取
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
        },
    ],
    response_format={"type": "json_object"},  # 指定返回JSON格式
)

# 提取并打印模型生成的JSON结果
json_string = completion.choices[0].message.content
print(json_string)
```

### 返回结果

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": ["打篮球", "旅游"]
}
```

#### Node.js

```
import OpenAI from "openai";

// 预定义示例响应（用于向模型展示期望的输出格式）
// 示例1：包含所有字段的完整响应
const example1Response = JSON.stringify({
    info: { name: "张三", age: "25岁", email: "zhangsan@example.com" },
    hobby: ["唱歌"]
}, null, 2);

// 示例2：包含多个hobby的响应
const example2Response = JSON.stringify({
    info: { name: "李四", age: "30岁", email: "lisi@example.com" },
    hobby: ["跳舞", "游泳"]
}, null, 2);

// 示例3：不包含hobby字段的响应（hobby非必需）
const example3Response = JSON.stringify({
    info: { name: "赵六", age: "28岁", email: "zhaoliu@example.com" }
}, null, 2);

// 示例4：另一个不包含hobby字段的响应
const example4Response = JSON.stringify({
    info: { name: "孙七", age: "35岁", email: "sunqi@example.com" }
}, null, 2);

// 初始化OpenAI客户端配置
const openai = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

// 创建聊天完成请求，使用结构化提示词来提高输出准确性
const completion = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: [
        {
            role: "system",
            content: `请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{
  "info": {
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  },
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：${example1Response}

示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：${example2Response}

示例3（不包含爱好）：
Q：我叫赵六，今年28岁，我的邮箱是zhaoliu@example.com
A：${example3Response}

示例4（不包含爱好）：
Q：我是孙七，35岁，邮箱sunqi@example.com
A：${example4Response}

请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。`
        },
        {
            role: "user",
            content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
        }
    ],
    response_format: {
        type: "json_object"
    }
});

// 提取并打印模型生成的JSON结果
const jsonString = completion.choices[0].message.content;
console.log(jsonString);
```

### 返回结果

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": [
    "打篮球",
    "旅游"
  ]
}
```

#### DashScope

#### Python

```
import os
import json
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1"

# 预定义示例响应（用于向模型展示期望的输出格式）
example1_response = json.dumps(
    {
        "info": {"name": "张三", "age": "25岁", "email": "zhangsan@example.com"},
        "hobby": ["唱歌"]
    },
    ensure_ascii=False
)
example2_response = json.dumps(
    {
        "info": {"name": "李四", "age": "30岁", "email": "lisi@example.com"},
        "hobby": ["跳舞", "游泳"]
    },
    ensure_ascii=False
)
example3_response = json.dumps(
    {
        "info": {"name": "王五", "age": "40岁", "email": "wangwu@example.com"},
        "hobby": ["Rap", "篮球"]
    },
    ensure_ascii=False
)

messages=[
        {
            "role": "system",
            "content": f"""请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{{
  "info": {{
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  }},
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：{example1_response}

示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：{example2_response}

示例3（包含多个爱好）：
Q：我的邮箱是wangwu@example.com，今年40岁，名字是王五，会Rap和打篮球
A：{example3_response}

请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。"""
        },
        {
            "role": "user",
            "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
        },
    ]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.8-max",
    messages=messages,
    response_format={'type': 'json_object'}
    )
json_string = response.output.choices[0].message.content[0]["text"]
print(json_string)
```

### 返回结果

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": [
    "打篮球",
    "旅游"
  ]
}
```

#### Java

```
// DashScope Java SDK 版本需要不低于 2.21.4

import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.common.ResponseFormat;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", """
                请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{
  "info": {
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  },
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：{"info":{"name":"张三","age":"25岁","email":"zhangsan@example.com"},"hobby":["唱歌"]}

示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：{"info":{"name":"李四","age":"30岁","email":"lisi@example.com"},"hobby":["跳舞","游泳"]}

示例3（不包含爱好）：
Q：我叫王五，我的邮箱是wangwu@example.com，今年40岁
A：{"info":{"name":"王五","age":"40岁","email":"wangwu@example.com"}}"""))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"))).build();
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(systemMessage, userMessage))
                .responseFormat(jsonMode)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

### 返回结果

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": [
    "打篮球",
    "旅游"
  ]
}
```

## 获取指定格式的输出

将`response_format`的`type`设为`json_object`，可返回标准 JSON 字符串，但内容结构可能不符合预期，适用于简单场景。对于自动化解析、API 互操作等需要严格类型约束的复杂场景，可将 `type` 设置为 `json_schema`，强制大模型输出严格符合指定格式的内容。`response_format` 格式与示例如下：

**说明**多模态输入（图像、视频、音频等）不支持 `json_schema`，会自动降级为 `json_object`，schema 约束不生效。

格式

```
{
  "type": "json_schema",
  "json_schema": {
    "name": "schema_name",       // Schema 的名称
    "strict": true,              // 推荐设置为 true，严格遵守格式
    "schema": {
      "type": "object",
      "properties": {...},       // 定义字段结构，见右侧具体示例
      "required": [...],         // 必填字段列表
      "additionalProperties": false  // 推荐设置为 false，只输出定义的字段
    }
  }
}
```

示例

```
{
  "type": "json_schema",
  "json_schema": {
    "name": "user_info",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "用户姓名"
        },
        "age": {
          "type": "integer",
          "description": "用户年龄"
        },
        "email": {
          "type": "string",
          "description": "邮箱地址"
        }
      },
      "required": ["name", "age"],
      "additionalProperties": false
    }
  }
}
```

上述示例会强制模型输出包含 `name` 和 `age` 两个必填字段，以及可选的 `email` 字段的 JSON 对象。

### 使用方法

通过 OpenAI SDK 的 `parse` 方法，可直接传入 Python Pydantic 类或 Node.js Zod 对象。SDK 会自动将其转换为 JSON Schema，无需手动编写复杂 JSON。DashScope SDK 需参考上文格式，手动构造 JSON Schema。

#### OpenAI 兼容

Python

```
from pydantic import BaseModel, Field
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

class UserInfo(BaseModel):
    name: str = Field(description="用户的姓名")
    age: int = Field(description="用户的年龄，单位为岁")

completion = client.chat.completions.parse(
    model="qwen3.8-max",
    messages=[
        {"role": "system", "content": "提取姓名与年龄信息。"},
        {"role": "user", "content": "我叫刘五，今年25岁。"},
    ],
    response_format=UserInfo,
)

result = completion.choices[0].message.parsed
print(f"姓名：{result.name}，年龄：{result.age}")
```

Node.js

```
import OpenAI from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI(
    {
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const UserInfo = z.object({
  name: z.string().describe("用户的姓名"),
  age: z.number().int().describe("用户的年龄，单位为岁"),
});

const completion = await openai.chat.completions.parse({
  model: "qwen3.8-max",
  messages: [
    { role: "system", content: "提取姓名与年龄信息。" },
    { role: "user", content: "我叫刘五，今年25岁。" },
  ],
  response_format: zodResponseFormat(UserInfo, "user_info"),
});

const userInfo = completion.choices[0].message.parsed;
console.log(`姓名：${userInfo.name}`);
console.log(`年龄：${userInfo.age}`);
```

运行代码可获得以下输出：

```
姓名：刘五，年龄：25
```

#### DashScope

> 暂不支持 Java SDK。

```
import os
import dashscope
import json

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [{"text": "我叫刘五，今年25岁。"}],
    },
]
response = dashscope.MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    messages=messages,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "user_info",
            "strict": True,
            "schema": {
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "age": {"title": "Age", "type": "integer"},
                },
                "required": ["name", "age"],
                "title": "UserInfo",
                "type": "object",
            },
        },
    },
)
json_object = json.loads(response.output.choices[0].message.content[0]["text"])
print(f"姓名：{json_object['name']}，年龄：{json_object['age']}")
```

运行代码可获得以下输出：

```
姓名：刘五，年龄：25
```

### 配置指南

使用 JSON Schema 时，遵循以下规范可获得更可靠的结构化输出：

-   **必填字段声明**
    
    推荐将必填字段列在 `required`数组中。可选字段可不列入，例如：
    

```
{
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "email": {"type": "string"}
  },
  "required": ["name", "age"]
}
```

若输入未提供 email 信息，输出中将不包含此字段。

-   **可选字段的实现方式**
    
    除不列入 `required` 外，也可通过允许 `null` 类型实现：
    

```
{
  "properties": {
    "name": {"type": "string"},
    "email": {"type": ["string", "null"]}  // 可以是字符串或 null
  },
  "required": ["name", "email"]  // 两个都在 required 中
}
```

输出将始终包含 `email` 字段，但其值可能为 `null`。

-   **additionalProperties 配置**
    
    控制是否允许输出未在 schema 中定义的额外字段：
    

```
{
  "properties": {"name": {"type": "string"}},
  "required": ["name"],
  "additionalProperties": true  // 允许额外字段
}
```

示例输入：`"我叫张三，25岁"`；输出：`{"name": "张三", "age": 25}`（包含未定义的 `age` 字段）。

**值**

**行为**

**适用场景**

`false`

只输出定义的字段

需要精确控制结构

`true`

允许额外字段

需要捕获更多信息

-   **支持的数据类型：**string、number、integer、boolean、object、array、enum。

## 应用于生产环境

-   **有效性校验**
    
    若使用 JSON Object 模式，将输出传递给下游业务前，建议使用工具对其进行有效性校验，如 jsonschema (Python)、Ajv (JavaScript)、Everit (Java)等**，**确保其符合指定的 JSON Schema 要求，避免因字段缺失、类型错误或格式不规范导致下游系统解析失败、数据丢失或业务逻辑中断。失败时可通过重试、大模型改写等策略进行修复。
    
-   **禁用** **max\_tokens**
    
    开启结构化输出时，请勿设置 `max_tokens`。该参数限制模型输出的 Token 数（默认值为模型最大输出 Token 数），设置后可能导致JSON字符串在输出过程中被截断，产生无效 JSON，下游解析将失败。
    
-   **使用 SDK 辅助生成 Schema**
    
    推荐使用 SDK 自动生成 Schema，避免手动维护导致的错误，并可以自动验证和解析。
    
    Python
    
    ```
    from pydantic import BaseModel, Field
    from typing import Optional
    from openai import OpenAI
    import os
    
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    )
    class UserInfo(BaseModel):
        name: str = Field(description="用户姓名")
        age: int = Field(description="用户年龄")
        email: Optional[str] = None  # 可选字段
    
    completion = client.chat.completions.parse(
        model="qwen3.8-max",
        messages=[
            {"role": "system", "content": "提取姓名与年龄信息。"},
            {"role": "user", "content": "我叫刘五，今年25岁。"},
        ],
        response_format=UserInfo  # 直接传入 Pydantic 模型
    )
    
    result = completion.choices[0].message.parsed  # 类型安全的解析结果
    print(f"姓名：{result.name}，年龄：{result.age}")
    ```
    
    Node.js
    
    ```
    import { z } from "zod";
    import { zodResponseFormat } from "openai/helpers/zod";
    import OpenAI from "openai";
    
    const client = new OpenAI(
        {
            apiKey: process.env.DASHSCOPE_API_KEY,
            // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
            baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
        }
    );
    
    const UserInfo = z.object({
      name: z.string().describe("用户姓名"),
      age: z.number().int().describe("用户年龄"),
      email: z.string().optional().nullable()  // 可选字段
    });
    
    const completion = await client.chat.completions.parse({
      model: "qwen3.8-max",
      messages: [
        { role: "system", content: "提取姓名与年龄信息。" },
        { role: "user", content: "我叫刘五，今年25岁。" },
      ],
      response_format: zodResponseFormat(UserInfo, "user_info")
    });
    
    console.log(completion.choices[0].message.parsed);
    ```
    

## 常见问题

### Q：Qwen 的思考模式模型如何结构化输出？

A：标注为"非思考模式"的模型，在思考模式下返回的内容可能不是严格的标准 JSON 字符串，可采用以下两步法进行修复：先调用思考模型获取高质量输出，再将格式不正确的 JSON 传给支持 JSON Mode 的模型进行修复。

1.  **获取思考模式下的输出**
    
    调用思考模式模型获取高质量输出。输出结果可能不是标准JSON字符串。
    
    > 说明：开启思考模式时设置 `response_format` 参数为 `{"type": "json_object"}` 不会报错。以下为兜底示例，仅在模型返回内容不是标准 JSON 时用于演示两步修复法，因此步骤中未设置 `response_format` 参数。
    

```
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [{"type": "text", "text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}],
        },
    ],
    # 开启思考模式；本兜底示例未设置response_format参数（直接设置response_format不会报错）
    extra_body={"enable_thinking": True},
    # 思考模式下需要开启流式输出
    stream=True
)
# 提取并打印模型生成的JSON结果
json_string = ""
for chunk in completion:
    if not chunk.choices:
        continue
    if chunk.choices[0].delta.content is not None:
        json_string += chunk.choices[0].delta.content
```

2.  **校验并修复输出**
    
    尝试解析上一步获取的 `json_string`：
    
    -   若模型返回了有效的 JSON，直接解析使用即可。
    -   若模型返回了无效 JSON，可调用支持结构化输出的模型进行修复（建议选择速度快、成本低的模型，如非思考模式的 qwen-flash）。

```
import json
from openai import OpenAI
import os

# 初始化OpenAI客户端（如果前面的代码块未定义client变量，请取消下面的注释）
# client = OpenAI(
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
# )

try:
    json_object_from_thinking_model = json.loads(json_string)
    print("生成标准格式JSON字符串")
except json.JSONDecodeError:
    print("未生成标准格式JSON字符串，通过支持结构化输出的模型进行修复")
    completion = client.chat.completions.create(
        model="qwen-flash",
        # 使用非思考模式
        extra_body={"enable_thinking": False},
        messages=[
            {
                "role": "system",
                "content": "你是一个json格式修复专家，请将用户输入的json字符串修复为标准格式",
            },
            {
                "role": "user",
                "content": json_string,
            },
        ],
        response_format={"type": "json_object"},
    )
    json_object_from_thinking_model = json.loads(completion.choices[0].message.content)
```

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

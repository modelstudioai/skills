# 结构化输出

执行信息抽取或结构化数据生成任务时，大模型可能返回多余文本（如 \`\`\`json ）导致下游解析失败。开启结构化输出可确保大模型输出标准格式的 JSON 字符串，使用 JSON Schema 模式还能精确控制输出结构和类型，无需额外验证或重试。

## 使用方式

结构化输出支持JSON Object 与 JSON Schema两种模式：

-   **JSON Object 模式**：确保输出为标准格式的 JSON 字符串，但不保证符合特定结构。使用方式：
    
    1.  **设置**`response_format`**参数**：在请求体中，将 `response_format` 参数设置为 `{"type": "json_object"}`。
    2.  **提示词包含 JSON 关键词**：System Message 或 User Message 中需要包含 "JSON" 关键词（不区分大小写），否则会报错：`'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.`
-   [**JSON Schema 模式**](https://help.aliyun.com/zh/model-studio/qwen-structured-output#a4f5d7108anxd)：确保输出内容为指定的结构。使用方式：设置 `response_format` 为`{"type": "json_schema", "json_schema": {..., "strict": true}}`。
    
    > 提示词无需包含 JSON 关键词。
    

> 以上参数适用于 Chat Completions API。如果使用 Responses API，请改为设置 `text.format`，取值格式相同，示例见下文。JSON Object 模式下，Responses API 同样要求提示词包含 "JSON" 关键词，否则返回 400 错误。

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

**说明**标注为"非思考模式"的模型，仅在非思考模式下支持结构化输出。

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

#### Kimi

-   阿里云百炼部署
    
    -   kimi-k3
-   月之暗面部署
    
    -   kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed、kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code 、kimi/kimi-k2.6、kimi/kimi-k2.5

#### DeepSeek

-   阿里云百炼部署
    
    -   deepseek-v4-pro
    -   deepseek-v4.1-flash
    -   `deepseek-v4.1-flash-1017`
-   快手万擎部署
    
    -   vanchin/deepseek-v3.2-think、vanchin/deepseek-v3、vanchin/deepseek-ocr

#### GLM

-   glm-5.1
-   非思考模式：glm-5

#### Stepfun

仅思考模式：stepfun/step-3.7-flash、stepfun/step-5-preview

#### Ling

-   蚂蚁数科部署
    
    -   antdigital/Ling-3.1-flash

#### JSON Schema

Qwen3.7-Plus 系列、Qwen3.8-Flash 系列、Qwen3.7-Flash 系列、Qwen3.7-Max 系列、Qwen3.8-Max 系列模型

## 快速开始

以从个人简介中抽取信息为例，演示结构化输出的基本用法。

> JSON Object 模式不保证键名与字段类型稳定，不同提示词或不同次调用的返回结果可能存在差异。如需固定结构，请使用 JSON Schema 模式。

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK或DashScope SDK进行调用，还需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

#### OpenAI兼容-Chat Completions API

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

#### OpenAI兼容-Responses API

Responses API 是 Chat Completions API 的演进版本，结构化输出通过 `text.format` 参数设置，参数说明和迁移指南请参见 [OpenAI兼容-Responses](raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

#### Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = client.responses.create(
    model="qwen3.8-max",
    input="大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游。请抽取姓名与年龄信息，以JSON格式返回",
    text={"format": {"type": "json_object"}},
)

print(response.output_text)
```

### 返回结果

```
{"姓名": "刘五", "年龄": 34}
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 如果没有配置环境变量，请用API Key将下行替换为：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

const response = await openai.responses.create({
    model: "qwen3.8-max",
    input: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游。请抽取姓名与年龄信息，以JSON格式返回",
    text: { format: { type: "json_object" } }
});

console.log(response.output_text);
```

### 返回结果

```
{"姓名": "刘五", "年龄": 34}
```

#### curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游。请抽取姓名与年龄信息，以JSON格式返回",
    "text": {
        "format": {
            "type": "json_object"
        }
    }
}'
```

### 返回结果

```
{
    "id": "resp_3b59521f-fbef-9873-9c54-c3fdc94da946",
    "created_at": 1793277220,
    "model": "qwen3.8-max",
    "object": "response",
    "output": [
        {
            "id": "reasoning_3a4a1e6d-2a2f-4c3f-a3ea-0f0a5c1b9f11",
            "summary": [
                {
                    "text": "We need answer user request. Need output JSON only.",
                    "type": "summary_text"
                }
            ],
            "type": "reasoning"
        },
        {
            "id": "msg_acbe8467-497c-4c09-8584-dae4a1c97f9b",
            "content": [
                {
                    "annotations": [],
                    "text": "{\"姓名\": \"刘五\", \"年龄\": 34}",
                    "type": "output_text",
                    "logprobs": null
                }
            ],
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ],
    "status": "completed",
    "text": {
        "format": {
            "type": "json_object"
        },
        "verbosity": null
    },
    "usage": {
        "input_tokens": 123,
        "output_tokens": 118,
        "output_tokens_details": {
            "reasoning_tokens": 95
        },
        "total_tokens": 241
    }
}
```

#### DashScope API

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将region替换为ap-southeast-1
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
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
response = client.multimodal.chat.create(
    model="qwen3.8-max",
    messages=messages,
    response_format={'type': 'json_object'}
    )
json_string = response.choices[0].message.content
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

> 思考模型（如 qwen3.8-max）默认开启深度思考，使用结构化输出时无需额外设置 `enable_thinking`。如需在流式输出中区分思考过程与回复内容，请参见[思考模型的流式输出](https://help.aliyun.com/zh/model-studio/stream#ae5fd8099d208)。

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

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将region替换为ap-southeast-1
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    workspace = "{WorkspaceId}",
    region = "cn-beijing",
)
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
response = client.multimodal.chat.create(
    model = 'qwen3.8-max',
    messages = messages,
    response_format={'type': 'json_object'}
)
json_string = response.choices[0].message.content
print(json_string)
```
```
import os
import dashscope

# 以下为新加坡地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
# 若使用北京地域的模型，请将region替换为cn-beijing
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    workspace = "{WorkspaceId}",
    region = "ap-southeast-1",
)

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
response = client.multimodal.chat.create(
    model = 'qwen3.8-max',
    messages = messages,
    response_format={'type': 'json_object'}
)
json_string = response.choices[0].message.content
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

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将region替换为ap-southeast-1
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

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
response = client.multimodal.chat.create(
    model="qwen3.8-max",
    messages=messages,
    response_format={'type': 'json_object'}
    )
json_string = response.choices[0].message.content
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

#### OpenAI兼容-Chat Completions API

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

#### OpenAI兼容-Responses API

Responses API 通过 `text.format` 参数设置结构化输出，支持 `json_schema` 和 `json_object` 两种类型。OpenAI SDK 的 `parse` 方法同样可用，通过 `text_format` 传入 Pydantic 类或 Zod 对象。

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

response = client.responses.parse(
    model="qwen3.8-max",
    input="我叫刘五，今年25岁。",
    text_format=UserInfo,
)

result = response.output_parsed
print(f"姓名：{result.name}，年龄：{result.age}")
```

运行代码可获得以下输出：

```
姓名：刘五，年龄：25
```

参数说明请参见 [Responses API 的 text 参数](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

#### DashScope API

> 暂不支持 Java SDK。

```
import os
import dashscope
import json

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

messages = [
    {
        "role": "user",
        "content": [{"text": "我叫刘五，今年25岁。"}],
    },
]
response = client.multimodal.chat.create(
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
json_object = json.loads(response.choices[0].message.content)
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

-   **支持的 JSON Schema 关键字**
    
    以下列出 JSON Schema 模式（strict 模式）所支持的关键字。标记为"不支持"的关键字提交后会返回 400 错误。关键字的完整定义请参考 [JSON Schema 官方规范](https://json-schema.org/draft/2020-12)。
    
    **Schema 层面公共关键字**
    
    **关键字**
    
    **说明**
    
    `type`
    
    支持 `string`、`number`、`integer`、`boolean`、`null`、`array`、`object`；也支持联合类型，如 `["string", "null"]`
    
    `enum` / `const`
    
    `enum` 限制取值范围，`const` 限制为固定值
    
    `$defs` + `$ref`
    
    支持本地引用（如 `#/$defs/address`）；外部 URL 引用不报错但不生效
    
    `anyOf` / `oneOf` / `allOf` / `not`
    
    支持组合与条件约束。其中 `oneOf` 不严格保证 exactly-one 语义
    
    `if` / `then` / `else`
    
    支持条件 Schema，可根据字段值动态切换校验规则
    
    `title` / `description` / `default` / `examples`
    
    可正常提交，作为模型生成的语义提示，不参与硬性校验
    
    `$schema` / `$id` / `$comment`
    
    元标识符，可正常提交，不影响校验行为
    
    `deprecated` / `readOnly` / `writeOnly`
    
    注解关键字，可正常提交，不影响校验行为
    
    **各类型专属关键字**
    
    **类型**
    
    **支持的关键字**
    
    **不支持的关键字（400 错误）**
    
    `string`
    
    `minLength`、`maxLength`、`pattern`、`format`（如 `email`、`date`）、`contentMediaType`、`contentEncoding`
    
    \-
    
    `number` / `integer`
    
    `minimum`、`maximum`、`exclusiveMinimum`、`exclusiveMaximum`
    
    `multipleOf`
    
    `array`
    
    `items`、`prefixItems`（元组模式）、`minItems`、`maxItems`、`unevaluatedItems`
    
    `uniqueItems`、`contains`、`minContains`、`maxContains`、`additionalItems`
    
    `object`
    
    `properties`、`required`、`additionalProperties`、`minProperties`、`maxProperties`、`dependentRequired`、`dependentSchemas`、`unevaluatedProperties`
    
    `patternProperties`、`propertyNames`
    

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
    

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

# Assistants（下线中）

Assistant API 旨在简化 Assistant（一种大模型应用）的构建流程。本文详细介绍了 Assistant API 提供的各项 Assistant 管理方法，包括 Assistant 的创建、列举、检索、更新和删除操作。

**重要**

Assistant API**下线中**，建议迁移至[Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)：内置多种工具，并支持多轮上下文管理，可作为替代方案。

> **功能介绍**：如果您想了解 Assistant API 的功能和基本用法，请参考[Assistant API功能概览](https://help.aliyun.com/zh/model-studio/assistant-api/)。

> **有效期限**：所有 Assistant 实例均保存在阿里云百炼服务器上，目前没有失效日期，您可通过 assistant.id 检索智能体。

**说明**

[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和 Assistant 虽然均为大模型应用，但二者的功能相互独立，使用方法也不相同。

-   智能体应用：仅可使用控制台进行创建、查看、更新和删除，以及通过[应用调用 API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)进行调用。
    
-   Assistant：仅可使用 Assistant API 创建、查看、更新、删除和调用 Assistant 。
    

## 创建智能体

创建一个新的智能体。

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/assistants' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-max",
    "name": "智能小助手",
    "description": "这是一个智能小助手",
    "instructions": "你是一个智能小助手，你可以根据用户的需求去调用不同的工具，进而给出回答。请酌情使用工具。",
    "tools": [
        {
            "type": "code_interpreter"
        }
    ], 
    "metadata": {}
}'
```

**输入参数**

**参数名**

**描述**

**参数类型**

**是否必须**

model

智能体所使用的模型

str

是

name

智能体使用的名字

str

否

description

用于描述智能体的文字

str

否

instructions

System prompt 用于智能体里的大模型

str

否

tools

一个可以被智能体调用tools list.

自定义插件的鉴权信息传递

```
{
 "type": "${插件id}",
     "auth": {  # 当使用“用户级鉴权”时，才使用这一字段
         "type": "user_http",
         "user_token": "bearer-token",
         } 
 }
```

Optional\[List\[Dict\]\]

否（default=\[\])

metadata

其他相关参数用于智能体，用于存储其他相关参数

Dict

否

temperature

用于控制随机性和多样性的程度。

float

否

top\_p

生成时，核采样方法的概率阈值。

float

否

top\_k

生成时，采样候选集的大小。

integer

否

**返回结果**

```
{
    "id": "asst_49079f4b-d1e8-4015-a12e-2dcdd1f18d84",
    "object": "assistant",
    "created_at": 1711713885724,
    "model": "qwen-max",
    "name": "智能小助手",
    "description": "这是一个智能小助手",
    "instructions": "你是一个智能小助手，你可以根据用户的需求去调用不同的工具，进而给出回答。请酌情使用工具。",
    "tools": [
        {
            "type": "code_interpreter"
        }
    ],
    "metadata": {},
    "temperature": null,
    "top_p": null,
    "top_k": null,
    "max_tokens": null,
    "request_id": "b1778226-3865-9006-9e95-56329a710322"
}
```

**输出参数**

一个[智能体对象](#0f08c44ac39yh)。

## SDK

**代码示例**

Python

```
from dashscope import Assistants
import os

assistant = Assistants.create(
        # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 此处以qwen-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model='qwen-max',
        name='smart helper',
        description='A tool helper.',
        instructions='You are a helpful assistant. When asked a question, use tools wherever possible.', 
        tools=[{
            'type': 'search'
        }, {
            'type': 'function',
            'function': {
                'name': 'big_add',
                'description': 'Add to number',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'left': {
                            'type': 'integer',
                            'description': 'The left operator'
                        },
                        'right': {
                            'type': 'integer',
                            'description': 'The right operator.'
                        }
                    },
                    'required': ['left', 'right']
                }
            }
        }],
)
print(assistant)
```

Java

```
import com.alibaba.dashscope.assistants.Assistant;
import com.alibaba.dashscope.assistants.AssistantParam;
import com.alibaba.dashscope.assistants.Assistants;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.lang.System;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Assistants assistants = new Assistants();
        // build assistant parameters
        AssistantParam param = AssistantParam.builder()
                // 此处以qwen-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-max")
                .name("intelligent guide")
                .description("a smart guide")
                .instructions("You are a helpful assistant.")
                // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();
        Assistant assistant = assistants.create(param);
        System.out.println(JsonUtils.toJson(assistant));
        // use assistant

    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

model

_string_

\-

指定用于智能体所使用的模型

name

_string_

\-

指定智能体名称

description

_string_

\-

智能体描述

instructions

_string_

\-

指定智能体功能信息

tools

_array_

\[\]

智能体使用的tools

**说明**

自定义tool鉴权信息传递

`{`

`"type": "plugin_type", "auth": {"type": "user_http","user_token": "bearer-token", }`

`}`

assistant在请求插件时会将bearer放在`{"plugin_type":{"user_token": "bearer-token"}}`添加到调用plugin的header里.

metadata

_object_

None

智能体关联信息

workspace

_string_

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

_string_

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**返回结果**

```
{
   "tools":[
      {
         "type":"search"
      },
      {
         "function":{
            "name":"big_add",
            "description":"Add to number",
            "parameters":{
               "type":"object",
               "properties":{
                  "left":{
                     "type":"integer",
                     "description":"The left operator"
                  },
                  "right":{
                     "type":"integer",
                     "description":"The right operator."
                  }
               },
               "required":[
                  "left",
                  "right"
               ]
            }
         },
         "type":"function"
      }
   ],
   "id":"asst_714cac72-81b2-49bf-a75d-c575b90a9398",
   "object":"assistant",
   "created_at":1726033638848,
   "model":"qwen-max",
   "name":"smart helper",
   "description":"A tool helper.",
   "instructions":"You are a helpful assistant. When asked a question, use tools wherever possible.",
   "file_ids":[
      
   ],
   "metadata":{
      
   },
   "temperature":"None",
   "top_p":"None",
   "top_k":"None",
   "max_tokens":"None",
   "request_id":"00f5962e-8d9f-92fd-9320-3173fa1525d6",
   "status_code":200
}
```

**输出参数**

**字段名**

**字段类型**

**字段描述**

status\_code

_integer_

为调用http status code，200表示调用成功，其他表示调用出错。

name

_string_

智能体名称。

id

_string_

智能体ID，为uuid字符串。

model

_string_

智能体使用的模型名称。

description

_string_

智能体描述信息。

instructions

_string_

指定智能体功能信息。

metadata

_object_

智能体的元数据。

tools

_array_

智能体可以用的tool列表。

created\_at

_integer_

智能体创建的时间戳表示。

code

_string_

表示请求失败，表示错误码，请求成功时忽略。只有在通过Python调用失败时会显示。

message

_string_

失败，表示失败详细信息，成功忽略。只有在通过Python调用失败时会显示。

## 列出智能体

用于返回智能体列表。

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/assistants?limit=2&order=desc' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

limit

创建智能体的数量

int

否

order

按照创建时间升序或降序

str

否（默认为`desc`）

**返回结果**

```
{
    "object": "list",
    "data": [
        {
            "id": "asst_0678aa33-43e2-4268-95e6-b0010f9f7937",
            "object": "assistant",
            "created_at": 1711435564909,
            "model": "qwen-max",
            "name": "智能小助手",
            "description": "这是一个智能小助手",
            "instructions": "你是一个智能小助手，你可以根据用户的需求去调用不同的工具，进而给出回答。请酌情使用工具。",
            "tools": [
                {
                    "type": "search"
                },
                {
                    "type": "text_to_image"
                },
                {
                    "type": "code_interpreter"
                }
            ],
            "metadata": {}
        },
        {
            "id": "asst_7af23142-52bc-4218-aa98-dfdb1128f19c",
            "object": "assistant",
            "created_at": 1711422620443,
            "model": "qwen-max",
            "name": "helpful assistant",
            "description": "",
            "instructions": "You are a helpful assistant.",
            "tools": [
                {
                    "type": "text_to_image"
                }
            ],
            "file_ids": [],
            "metadata": {}
        }
    ],
    "first_id": "asst_0678aa33-43e2-4268-95e6-b0010f9f7937",
    "last_id": "asst_7af23142-52bc-4218-aa98-dfdb1128f19c",
    "has_more": true,
    "request_id": "bc257359-ce86-9547-98be-d804effba8d1"
}
```

**输出参数**

输出一个[智能体对象](#0f08c44ac39yh)列表。

## SDK

**代码示例**

Python

```
from dashscope import Assistants
import os

assistants = Assistants.list(
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    limit=1,
    order='desc'
)
```

Java

```
import com.alibaba.dashscope.assistants.Assistant;
import com.alibaba.dashscope.assistants.Assistants;
import com.alibaba.dashscope.common.GeneralListParam;
import com.alibaba.dashscope.common.ListResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
      Assistants assistants = new Assistants();
      GeneralListParam listParam = GeneralListParam.builder()
                // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .limit(10l)
                .build();
      ListResult<Assistant> assistant = assistants.list(listParam);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

limit

_string_

None

指定列出assistant的数目，如果未指定则使用服务端默认值。

order

_string_

None

排序方式，可选值：desc(降序)、asc(升序)，如果未指定则使用服务端默认值。

workspace

_string_

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

_string_

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

**字段名**

**字段类型**

**字段描述**

has\_more

_boolean_

表示是否还有更多数据可以获取。

last\_id

_string_

data中最后一个assistant的ID。

first\_id

_string_

data中第一个assistant的ID。

data

_array_

智能体对象列表。

object

_string_

data的数据格式，如`"list"`。

request\_id

_string_

本次请求的ID。

status\_code

_integer_

请求状态码。

## 检索智能体

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/assistants/asst_0678aa33-43e2-4268-95e6-b0010f9f7937' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

assistant\_id

待检索的智能体 ID

str

是

**返回结果**

```
{
    "id": "asst_0678aa33-43e2-4268-95e6-b0010f9f7937",
    "object": "assistant",
    "created_at": 1711435564909,
    "model": "qwen-max",
    "name": "智能小助手",
    "description": "这是一个智能小助手",
    "instructions": "你是一个智能小助手，你可以根据用户的需求去调用不同的工具，进而给出回答。请酌情使用工具。",
    "tools": [
        {
            "type": "search"
        },
        {
            "type": "text_to_image"
        },
        {
            "type": "code_interpreter"
        }
    ],
    "metadata": {},
    "request_id": "f0ec05b0-8813-984c-81b5-1166ae3478d1"
}
```

**输出参数**

输出检索到的[智能体对象](#0f08c44ac39yh)。

## SDK

**代码示例**

Python

```
from dashscope import Assistants
import os

assistant = Assistants.retrieve(
    assistant_id='your_assistant_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

print(assistant)
```

Java

```
import com.alibaba.dashscope.assistants.Assistant;
import com.alibaba.dashscope.assistants.Assistants;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class RetrieveAssistantExample {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Assistants assistants = new Assistants();
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        Assistant assistant = assistants.retrieve("assistant_id", apiKey);
        System.out.println(assistant);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

assistant\_id

_string_

\-

指定要查询的智能体 ID

workspace

_string_

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

_string_

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

请参考[智能体对象](#1718e4e39302j)。

## 更新智能体

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/assistants/asst_0678aa33-43e2-4268-95e6-b0010f9f7937' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "instructions": "你是一个搜索助手",
    "name": "新建应用-assistantAPI",
    "description": "",
    "model": "qwen-max"
}'
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

assistant\_id

待检索的智能体 ID

str

是

\*

其他可选的输入参数

str

否

model

智能体所使用的大模型 ID

str

是

name

智能体使用的名字

str

否

description

用于描述智能体的文字

str

否

instructions

System prompt 用于智能体里的大模型

str

否

tools

一个可以被智能体调用tools list，用户需要在阿里云百炼中被注册

Optional\[List\[Dict\]\]

否（default=\[\]）

metadata

其他相关参数用于智能体，用于存储其他相关参数

Dict

否

**返回结果**

```
{
    "id": "asst_0678aa33-43e2-4268-95e6-b0010f9f7937",
    "object": "assistant",
    "created_at": 1711435564909,
    "model": "qwen-max",
    "name": "新建应用-assistantAPI",
    "description": "",
    "instructions": "你是一个搜索助手",
    "tools": [
        {
            "type": "search"
        },
        {
            "type": "text_to_image"
        },
        {
            "type": "code_interpreter"
        }
    ],
    "metadata": {},
    "request_id": "b0993831-a98b-9e71-b235-75174df9046e"
}
```

**输出参数**

输出更新后的[智能体对象](#0f08c44ac39yh)。

## SDK

**代码示例**

Python

```
from dashscope import Assistants
import os

assistants = Assistants.update(
    'assistant_id', 
    model='new_model_name',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
```

Java

```
import com.alibaba.dashscope.assistants.Assistant;
import com.alibaba.dashscope.assistants.AssistantParam;
import com.alibaba.dashscope.assistants.Assistants;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Assistants assistants = new Assistants();
        AssistantParam param = AssistantParam.builder()
                .model("qwen-max")
                .name("intelligent guide")
                .description("a smart guide")
                .instructions("You are a helpful assistant.  When asked a question, use tools wherever possible.")
                // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();
        
        Assistant assistant = assistants.update("assistant_id", param);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

assistant\_id

_string_

\-

指定需要更新的assistant ID

model

_string_

\-

指定用于智能体所使用的模型

name

_string_

None

指定智能体名称

description

_string_

None

智能体描述

instructions

_string_

None

指定智能体功能信息。

tools

_array_

\[\]

智能体使用的tools

metadata

_object_

None

智能体关联信息

workspace

_string_

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

_string_

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

请参考[智能体对象](#0f08c44ac39yh)。

## 删除智能体

## HTTP

**代码示例**

```
curl --location --request DELETE 'https://dashscope.aliyuncs.com/api/v1/assistants/asst_0678aa33-43e2-4268-95e6-b0010f9f7937' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

assistant\_id

待检索的智能体 ID

str

是

**返回结果**

```
{
    "id": "asst_0678aa33-43e2-4268-95e6-b0010f9f7937",
    "object": "assistant.deleted",
    "deleted": true,
    "request_id": "6af9320f-0430-9d01-b92f-d1beb6424dc5"
}
```

**输出参数**

输出删除智能体后的状态。

## SDK

**代码示例**

Python

```
from dashscope import Assistants
import os

assistants = Assistants.delete(
    'assistant_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
```

Java

```
import com.alibaba.dashscope.assistants.Assistants;
import com.alibaba.dashscope.common.DeletionStatus;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Assistants assistants = new Assistants();     
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        DeletionStatus assistant = assistants.delete("assistant_id", apiKey);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

assistant\_id

_string_

\-

指定要删除的智能体 ID

workspace

_string_

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

_string_

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

**字段名**

**字段类型**

**字段描述**

id

_string_

删除的对象的ID

object

_string_

本次请求目标，示例：`'assistant.deleted'`

deleted

_boolean_

是否删除

request\_id

_string_

本次请求的ID。

status\_code

_integer_

请求状态码。

## **智能体对象**

一个能够调用模型并使用工具的`Assistant`对象。

**智能体对象示例**

```
{
    "id": "asst_49079f4b-d1e8-4015-a12e-2dcdd1f18d84",
    "object": "assistant",
    "created_at": 1711713885724,
    "model": "qwen-max",
    "name": "智能小助手",
    "description": "这是一个智能小助手",
    "instructions": "你是一个智能小助手，你可以根据用户的需求去调用不同的工具，进而给出回答。请酌情使用工具。",
    "tools": [
        {
            "type": "code_interpreter"
        }
    ],
    "metadata": {},
    "temperature": null,
    "top_p": null,
    "top_k": null,
    "max_tokens": null,
    "request_id": "b1778226-3865-9006-9e95-56329a710322"
}
```

**参数名**

**数据类型**

**描述**

id

string

智能体唯一标识符，即 assistant ID。

object

string

对象类型，始终为`assistant`。

created\_at

integer

创建智能体时的 Unix 13位时间戳（以毫秒为单位）。

model

string

智能体使用的模型名。您可以在[Assistant API功能概览](https://help.aliyun.com/zh/model-studio/assistant-api/)查看所有可用模型，或者查看[模型列表](https://help.aliyun.com/zh/model-studio/models)以了解它们的详情。

name

string

智能体的名称。

description

string

智能体的描述。

instructions

string

智能体使用的系统指令。

tools

array

智能体上启用的工具列表。工具的类型可以是官方插件（code\_interpreter 代码解释器、quark\_search 夸克搜索、text\_to\_image 文生图）、知识检索增强（RAG）或函数调用（Function Calling）。

metadata

dict

以结构化格式存储的智能体对象的附加信息。

temperature

float

采样温度，其取值在 0 到 2 之间。较高的值（如 1）会使输出更加随机；而较低的值（如 0.2）则会使输出更加集中和确定。

top\_p

float

一种替代温度采样的方法，称为核采样。在这种采样方法中，大模型选取具有前 top\_p 的累积概率质量的Token结果。其值为 0.1 表示仅考虑构成前 10% 概率质量的Token。

通常建议调整此参数或`temperature`，但不要同时调整两者。

top\_k

integer

与top\_p类似，但样本是从 k 个最高概率的Token中选取的，而不考虑它们的累积概率质量。

不要同时调整此参数和`temperature`或`top_p`。

max\_tokens

integer

智能体能够一次性生成Token的最大数量。

request\_id

string

智能体关联的调用的唯一标识符。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

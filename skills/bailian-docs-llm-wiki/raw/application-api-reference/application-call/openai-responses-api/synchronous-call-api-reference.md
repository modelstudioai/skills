# 同步调用 API 参考

本文介绍如何通过 OpenAI 兼容模式的 Responses API **同步调用**阿里云百炼应用（**智能体**、**工作流**）。适用于需要**即时获取结果**的实时交互场景，可轻松复用现有的 OpenAI 代码库，或快速集成来自 OpenAI 生态的各类工具。

**相关参考**

-   **异步调用**：对于**耗时较长**的任务（如生成报告、多步骤工具调用），为避免请求超时，请参阅[异步调用 API 参考](https://help.aliyun.com/zh/model-studio/asynchronous-call-api-reference)。
    
-   **DashScope API**：如需获取更全面的功能与更高的性能，请参阅[DashScope API 参考](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)。
    

**重要**

本文档仅适用于中国大陆版（北京地域）。

## 前提条件

-   已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   已创建[阿里云百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)，并已获取应用ID：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面的应用卡片上复制其ID。
    
-   如果通过SDK调用，还需要[安装OpenAI Python SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

使用SDK调用时需配置的`base_url`：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1`

使用HTTP方式调用时需配置的`Endpoint`：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`

**说明**

请将 `{APP_ID}` 替换为实际的应用ID。

### **请求体**

## 文本输入

**单轮对话**

Python

```
from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

response = client.responses.create(
   input="你是谁？",
)

print(response.model_dump_json(indent=2))
```

curl

```
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--data '{
    "input": [
        {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "你是谁？"
                }
            ]
        }
    ]
}'
```

**多轮对话**

将包含完整历史消息的消息对象数组传递给`input` 参数。

Python

```
from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

messages = [
    {"role": "user", "content": "你是谁？"},
    {"role": "assistant", "content": "我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。"},
    {"role": "user", "content": "你能做什么？"}
]
response = client.responses.create(
    input=messages
)

# 打印完整的响应JSON对象
print(response.model_dump_json(indent=2))
```

curl

```
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--data '{
    "input": [
        {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "你是谁？"
                }
            ]
        },
        {
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "input_text",
                    "text": "我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。"
                }
            ]
        },
        {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "你能做什么？"
                }
            ]
        }
    ]
}'
```

## 流式输出

在请求体中设置`stream`为`true`，以流式方式获取响应，实现实时展示生成内容的效果。

**应用配置：**若应用类型为**工作流**，需在**结束节点**或**流程输出节点**中启用**流式输出**开关，并重新**发布**应用。

Python

```
from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

messages = [
    {"role": "user", "content": "你是谁？"},
    {"role": "assistant", "content": "我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。"},
    {"role": "user", "content": "你能做什么？"}
]
# 设置 stream=True 来发起流式请求
stream = client.responses.create(
    input=messages,
    stream=True,
)

# 遍历并处理事件流
for chunk in stream:
    # 只输出文字内容
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
```

curl

```
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --data '{
         "input": [
             {
                 "type": "message",
                 "role": "user",
                 "content": [
                     {
                         "type": "input_text",
                         "text": "你是谁？"
                     }
                 ]
             },
             {
                 "type": "message",
                 "role": "assistant",
                 "content": [
                     {
                         "type": "input_text",
                         "text": "我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。"
                     }
                 ]
             },
             {
                 "type": "message",
                 "role": "user",
                 "content": [
                     {
                         "type": "input_text",
                         "text": "用不少于100字介绍一下你自己"
                     }
                 ]
             }
         ],
         "stream": true
     }'
```

## 图像输入

在 `content` 数组中包含 `image_url` 对象，向模型提供图像的 URL，模型基于图像内容进行问答。

**智能体应用**配置：需选用[通义千问VL系列模型](https://help.aliyun.com/zh/model-studio/vision)，并将文件处理方式选为**自定义处理**，然后重新**发布**应用。

**工作流应用**配置：需选用[通义千问VL系列模型](https://help.aliyun.com/zh/model-studio/vision)，并将模型节点的模型入参变量填为`imageList`，然后重新**发布**应用。

Python

```
from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.responses.create(
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "这是什么" },
                {
                    "type": "input_image",
                    "image_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                }
            ]
        }
    ]
)

# 打印完整的响应JSON对象
print(response.model_dump_json(indent=2))
```

curl

```
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--data '{
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "这是什么"
                },
                {
                    "type": "input_image",
                    "image_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                }
            ]
        }
    ]
}'
```

## 文件输入

在 `content` 数组中包含 `input_file` 对象，向模型提供文件的 URL，模型基于文件中的内容进行问答。

仅**智能体应用**支持，应用内的文件处理方式需选择**全文引用**或**切片检索**。

相关文档：[文件问答](https://help.aliyun.com/zh/model-studio/file-q-a)。

Python

```
from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv("DASHSCOPE_API_KEY")
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.responses.create(
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "总结这个文件的内容。"
                },
                {
                    "type": "input_file",
                    "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                }
            ]
        }
    ]
)

# 打印完整的响应JSON对象
print(response.model_dump_json(indent=2))
```

curl

```
# 请将 {APP_ID} 替换为实际的应用ID
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--data '{
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "总结这个文件的内容。"
                },
                {
                    "type": "input_file",
                    "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                }
            ]
        }
    ]
}'
```

**app\_id** _string_**（必选）**

应用的标识。

在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面的应用卡片上获取应用ID。

> 通过 HTTP 调用时，请将实际的应用ID放入 URL 中，替换`APP_ID`。

**input** `_string_`/`_array_` **（必选）**

请求的核心输入内容。可以是一个简单的字符串，也可以是一个包含多轮对话历史的消息数组。

-   **简单字符串**: 用于单轮文本对话，例如 `"你好"`。
    
-   **消息数组 (Messages)**： 用于多轮对话或包含多媒体（如图片、文件）的输入。数组中的每个元素都是一个消息对象。
    
    **说明**
    
    基于`pre_response_id`或`conversation_id`的上下文功能将在**后续支持**。目前请在每次请求时传递完整的对话历史。
    
    **消息类型**
    
    **System Message** `_object_` （可选）
    
    系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。
    
    **属性**
    
    **content** `_string_` **（必选）**
    
    消息内容。
    
    **role** `_string_` **（必选）**
    
    固定为`system`。
    
    **User Message** `_object_` **（必选）**
    
    用户消息，用于向模型传递问题、指令或上下文等。
    
    **属性**
    
    **content** `_string 或 array_` **（必选）**
    
    消息内容。
    
    -   **纯文本输入**: `content` 为字符串，例如 `"你好"`。
        
    -   **多模态输入**: `content` 为一个数组，包含文本、图片或文件对象。
        
        **子属性**
        
        **文本**
        
        **type** `_string_` **（必选）**
        
        固定为 `input_text`。
        
        **text** `_string_`**（必选）**
        
        文本内容。
        
        **图像**
        
        **type** `_string_` **（必选）**
        
        固定为 `input_image`。
        
        **image\_url** `_string_`**（必选）**
        
        图片的 URL。
        
        **文件**
        
         仅**智能体应用**支持文件传入。
        
        **type** `_string_` **（必选）**
        
        固定为 `input_file`。
        
        **file\_url** `_string_`**（必选）**
        
        文件的URL。
        
    
    **role** `_string_` **（必选）**
    
    固定为`user`。
    
    **Assistant Message** `_object_` （可选）
    
    模型对用户消息的回复。
    
    **属性**
    
    **content** `_string_` （可选）
    
    消息内容。
    
    **role** `_string_` **（必选）**
    
    固定为`assistant`。
    

**stream** `_boolean_` （可选）

是否流式输出回复。

-   false（默认值）：模型生成完所有内容后一次性返回结果。
    
-   true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。
    

**background** `_boolean_` （可选）

是否以异步方式执行任务。

**说明**

异步调用暂不支持流式输出。

-   `false`（默认值）：同步。API将保持连接直到任务完成。
    
-   `true`：异步。API将立即返回一个任务ID，可通过查询接口来获取结果。
    

### **响应对象（非流式输出）**

```
{
    "created_at": 1758624774,
    "id": "ce65e29a-3d14-4b21-a5c0-ac601f3af888",
    "model": "",
    "object": "response",
    "output": [
        {
            "content": [
                {
                    "annotations": [
                    ],
                    "text": "我可以帮助你做很多事情，包括但不限于：\n\n1. **回答问题**：无论是科学、历史、文化、技术等领域的知识，我都可以尽力为你提供准确的信息。\n2. **写作帮助**：我可以帮你写文章、邮件、报告、故事、诗歌等，也可以进行润色和修改。\n3. **语言翻译**：我可以将文本从一种语言翻译成另一种语言。\n4. **学习辅导**：我可以帮助你理解复杂的概念，解答数学题、物理题等学科问题。\n5. **编程帮助**：我可以协助你编写代码、调试程序、解释算法等。\n6. **提供建议**：在生活、工作、学习等方面，我可以提供一些实用的建议和思路。\n7. **娱乐互动**：我可以讲笑话、玩文字游戏可以将进行简单的聊天互动。\n\n如果你有任何具体的需求或问题，随时告诉我，我会尽力帮助你！",
                    "type": "output_text"
                }
            ],
            "id": "msg_f25e8129-a130-447c-8e03-3f2b148c4e1d",
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ],
    "parallel_tool_calls": false,
    "status": "completed",
    "tool_choice": "auto",
    "tools": [
    ]
}
```

**id** `_string_`  
本次请求的唯一标识符（ID），可用于日志记录和问题追踪。

**object** `_string_`

对象类型，对于本API，其值固定为 `response`。

**created\_at** `_integer_`  
响应创建时间的Unix时间戳（以秒为单位）。

**status** `_string_`

整个响应任务的最终状态。`completed` 表示任务已成功结束。

**output** `_array_`  
一个数组，包含了模型生成的所有输出内容。

**子属性**

**output** **message**`_object_`

包含了模型输出内容的消息对象。

**子属性**

**content** `_array_`  
消息的核心内容数组，包含多种类型的内容块（如文本、代码、图片等）。

**子属性**

**text** `_string_`  
模型实际生成的文本回复。

**type** `_string_`  
内容块的类型。`output_text` 表示这是一个输出的文本块。

**id** `_string_`  
此条输出消息的唯一ID。

**role** `_string_`  
消息的角色。`assistant` 表示这条消息是由AI助手生成的。

**status** `_string_`  
表示该条消息的生成状态。`completed` 表示该条消息已成功生成。

**type** `_string_`  
`output`数组中元素的类型。`message` 表示这是一个消息对象。

### **响应对象（流式输出）**

```
id:1 | event:response.created | :HTTP_STATUS/200 | data:{"sequence_number":0,"type":"response.created","response":{"output":[],"parallel_tool_calls":false,"created_at":1760076609,"tool_choice":"auto","model":"","id":"508f1306-3760-49da-9e43-380fd952c297","tools":[],"object":"response","status":"queued"}}
id:2 | event:response.in_progress | :HTTP_STATUS/200 | data:{"sequence_number":1,"type":"response.in_progress","response":{"output":[],"parallel_tool_calls":false,"created_at":1760076609,"tool_choice":"auto","model":"","id":"508f1306-3760-49da-9e43-380fd952c297","tools":[],"object":"response","status":"in_progress"}}
id:3 | event:response.output_item.added | :HTTP_STATUS/200 | data:{"sequence_number":2,"item":{"id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","role":"assistant","type":"message","content":[],"status":"in_progress"},"output_index":0,"type":"response.output_item.added"}
id:4 | event:response.content_part.added | :HTTP_STATUS/200 | data:{"sequence_number":3,"output_index":0,"type":"response.content_part.added","content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","part":{"type":"output_text","annotations":[],"text":""}}
id:5 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":4,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"你好","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:6 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":5,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"！我是通","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:7 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":6,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"义千问","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:8 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":7,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"（Qwen","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:9 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":8,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"），由阿里云研发的","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:10 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":9,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"超大规模语言模型。我","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:11 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":10,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"能够回答问题、创作文字","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:12 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":11,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"，比如写故事、写","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:13 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":12,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"公文、写邮件、","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:14 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":13,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"写剧本、逻辑推理、","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:15 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":14,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"编程等等，还能表达观点","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:16 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":15,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"，玩游戏等。我支持","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:17 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":16,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"多种语言，包括但不限于","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:18 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":17,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"中文、英文、德语","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:19 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":18,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"、法语、西班牙语","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:20 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":19,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"等，满足国际","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:21 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":20,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"化的使用需求。我","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:22 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":21,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"擅长处理各种任务","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:23 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":22,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"，无论是专业领域的","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:24 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":23,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"知识问答，还是","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:25 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":24,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"日常生活中的问题咨询","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:26 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":25,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"，我都会尽力提供帮助","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:27 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":26,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"。我的目标是成为","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:28 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":27,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"你最可靠的智能","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:29 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{"sequence_number":28,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","delta":"伙伴！","output_index":0,"type":"response.output_text.delta","logprobs":[]}
id:30 | event:response.output_text.done | :HTTP_STATUS/200 | data:{"sequence_number":29,"content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","text":"你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！","output_index":0,"type":"response.output_text.done","logprobs":[]}
id:31 | event:response.content_part.done | :HTTP_STATUS/200 | data:{"sequence_number":30,"output_index":0,"type":"response.content_part.done","content_index":0,"item_id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","part":{"type":"output_text","annotations":[],"text":"你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！"}}
id:32 | event:response.output_item.done | :HTTP_STATUS/200 | data:{"sequence_number":31,"item":{"id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","role":"assistant","type":"message","content":[{"type":"output_text","annotations":[],"text":"你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！"}],"status":"completed"},"output_index":0,"type":"response.output_item.done"}
id:33 | event:response.completed | :HTTP_STATUS/200 | data:{"sequence_number":32,"type":"response.completed","response":{"output":[{"id":"msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e","role":"assistant","type":"message","content":[{"type":"output_text","annotations":[],"text":"你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！"}],"status":"completed"}],"parallel_tool_calls":false,"created_at":1760076609,"tool_choice":"auto","model":"","id":"508f1306-3760-49da-9e43-380fd952c297","tools":[],"object":"response","status":"completed"}}
```

**id** `_string_`

事件的消息ID。

**code** `_string_`

错误码，调用成功时为空值。

**message** `_string_`

表示错误详细信息，请求成功则忽略。

**event** `_string_`

事件类型，表示当前响应的状态。

**事件通用数据**

**sequence\_number** `_integer_`

事件的序列号，从0开始递增。

**type** `_string_`

事件类型，与`event`内容相同。

**事件类型详解**

**整体响应生命周期事件**

**response.created**: 表示响应已创建。

**response.in\_progress**: 表示响应处理中。

**response.completed**: 响应完成。

**通用数据**

**response** `_object_`

响应对象，包含响应的详细信息_。_

**子属性**

**id** `_string_`

响应的唯一标识符。

**status** `_string_`

响应的最终状态。

**object** `_string_`

对象类型**。**固定值为 `"response"`。

**created\_at** `_integer_`  
响应创建时间的Unix时间戳（以秒为单位）。

**output** `_array_`  
输出内容列表。

**子属性**

**output** **message**`_object_`

包含了模型输出内容的消息对象。

**子属性**

**id** `_string_`

输出项的唯一标识符。

**type** `_string_`

输出项的类型。

-   `"reasoning"`: 模型的思考过程。
    
-   `"message"`: 最终回复。
    

**role** `_string_`

消息的角色。

**content** `_array_`

输出内容部分的列表。

**子属性**

**type** `_string_`

内容部分的类型。例如 `"output_text"` 表示这是一个文本部分。

**text** `_string_`

文本内容。

**annotations** `_array_`

注解列表。

**status** `_string_`

响应的当前状态。

**内容构建事件**

**response.output\_item.added**: 表示输出项已添加。

**子属性**

**output\_index** `_integer_`

`item` 在 `output` 数组中的索引。

**item** `_object_`

新增的输出项对象。

**子属性**

**output** **message**`_object_`

包含了模型输出内容的消息对象。

**子属性**

**id** `_string_`

输出项的唯一标识符。

**type** `_string_`

输出项的类型。

-   `"reasoning"`: 模型的思考过程。
    
-   `"message"`: 最终回复。
    

**role** `_string_`

消息的角色。

**content** `_array_`

内容部分列表。

**status** `_string_`

响应的当前状态。

**response.output\_item.done**: 输出项完成。

**子属性**

**output\_index** `_integer_`

已完成的 `item` 在 `output` 数组中的索引。

**item** `_object_`

完整的输出项对象。

**子属性**

**id** `_string_`

输出项的唯一标识符。

**type** `_string_`

输出项的类型。

-   `"reasoning"`: 模型的思考过程。
    
-   `"message"`: 最终回复。
    

**role** `_string_`

消息的角色。

**content** `_array_`

输出内容部分的列表。

**子属性**

**type** `_string_`

内容部分的类型。例如 `"output_text"` 表示这是一个文本部分。

**text** `_string_`

文本内容。

**annotations** `_array_`

注解列表。

**status** `_string_`

响应的当前状态。

**response.content\_part.added**: 表示在一个输出项（如一条消息）中，新生成了一个内容块（如文本、图片等）。

**子属性**

**output\_index** `_integer_`

关联的 `response.output` 数组索引。

**content\_index** `_integer_`

关联的 `item.content` 数组索引。

**item\_id** `_string_`

关联的输出项ID。

**part** `_object_`

新添加的内容部分对象。

**子属性**

**type** `_string_`

内容部分的类型。例如 `"output_text"` 表示这是一个文本部分。

**text** `_string_`

文本内容。

**annotations** `_array_`

注解列表。

**response.content\_part.done**: 内容部分完成。

**子属性**

**output\_index** `_integer_`

关联的 `response.output` 数组索引。

**content\_index** `_integer_`

关联的 `item.content` 数组索引。

**item\_id** `_string_`

关联的输出项ID。

**part** `_object_`

新添加的内容部分对象。

**子属性**

**type** `_string_`

内容部分的类型。例如 `"output_text"` 表示这是一个文本部分。

**text** `_string_`

文本内容。

**annotations** `_array_`

注解列表。

**文本流事件**

**response.output\_text.delta**：输出内容的文本增量。

**子属性**

**delta** `_string_`

输出文本的增量片段。

**output\_index** `_integer_`

关联的 `response.output` 数组索引。

**content\_index** `_integer_`

关联的 `item.content` 数组索引。

**item\_id** `_string_`

关联的输出项ID。

**response.output\_text.done**: 输出文本完成。

**子属性**

**text** `_String_`

完整的输出文本内容。

**output\_index** `_integer_`

关联的 `response.output` 数组索引。

**content\_index** `_integer_`

关联的 `item.content` 数组索引。

**item\_id** `_string_`

关联的输出项ID。

**response.reasoning\_text.delta**：思考过程的文本增量。

**子属性**

**delta** `_string_`

思考文本的增量片段。

**output\_index** `_integer_`

关联的 `response.output` 数组索引。

**content\_index** `_integer_`

关联的 `item.content` 数组索引。

**item\_id** `_string_`

关联的输出项ID。

**response.reasoning\_text.done**：思考过程的流式输出已全部结束。

**子属性**

**text** `_String_`

完整的思考过程。

**output\_index** `_integer_`

关联的 `response.output` 数组索引。

**content\_index** `_integer_`

关联的 `item.content` 数组索引。

**item\_id** `_string_`

关联的输出项ID。

## 常见问题

1.  **如何传递多轮对话的上下文？**
    
    需要在客户端维护完整的对话历史，并在每次请求时将所有历史消息完整地放在`input`数组中传递给API。
    
    基于`pre_response_id`或`conversation_id`的上下文功能将在**后续支持**。
    
2.  **为什么响应示例中的某些字段未在本文说明？**
    
    如果使用OpenAI的官方SDK，它可能会根据其自身的模型结构打印出一些额外的字段（通常为`null`）。这些字段是OpenAI协议本身定义的，我们的服务当前不支持，所以它们为空值。只需关注本文档中描述的字段即可。
    

## 错误码

如果应用调用失败并返回报错信息，请参阅[错误信息](https://help.aliyun.com/zh/model-studio/error-code)解决。

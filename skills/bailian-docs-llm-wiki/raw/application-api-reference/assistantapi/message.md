# Messages（下线中）

本文详细阐述了Assistant API中Message类的各项功能，涵盖了消息的创建、列举、检索、修改等操作。

**重要**

Assistant API**下线中**，建议迁移至[Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)：内置多种工具，并支持多轮上下文管理，可作为替代方案。

**相关指南：**关于Assistant API的快速使用方法，请参考[快速入门](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)。

**函数名**

**类型**

create

创建message 类

retrieve

检索message类

modify

修改message类

list

列出message类

## 创建消息

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads/thread_e99a9fe7-0433-426f-98ad-a5139c36579c/messages' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "role": "user",
    "content": "你是谁",
    "metadata": {}
}'
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

thread id

message 所传入的thread id

str

是

content

message的具体信息

str

是

role

传入信息的角色。目前只支持role = “user"

str

否

metadata

其他相关信息

str

否

**返回结果**

```
{
    "id": "message_f1933671-19e1-4162-ad25-7326165123e1",
    "object": "thread.message",
    "created_at": 1711508433283,
    "thread_id": "thread_e99a9fe7-0433-426f-98ad-a5139c36579c",
    "incomplete_details": {},
    "completed_at": null,
    "incomplete_at": null,
    "assistant_id": "",
    "run_id": "",
    "file_ids": [],
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": {
                "value": "你是谁",
                "annotations": []
            }
        }
    ],
    "metadata": {},
    "name": "",
    "plugin_call": {},
    "tool_calls": [],
    "status": "",
    "request_id": "b3ad40b9-f052-9665-a064-dab11c34625f"
}
```

**输出参数**

输出message类，并包含除了用户输入以外参数的其他额外字段：

-   id：message id
    
-   request\_id：请求id
    

## SDK

**代码示例**

Python

```
from dashscope import Messages
import os

msg = Messages.create(
    'the_thread_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    content='The message content.',
    role='user',
    metadata={'key': 'value'}
)
```

Java

```
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.messages.Messages;
import com.alibaba.dashscope.threads.messages.TextMessageParam;
import com.alibaba.dashscope.threads.messages.ThreadMessage;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        // create a message to thread
        Messages messages = new Messages();
        TextMessageParam param = TextMessageParam.builder()
                // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .role("user")
                .content("如何做出美味的牛肉炖土豆？")
                .build();
        ThreadMessage message = messages.create("threadId", param);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

thread\_id

str

\-

Thread id

content

str

\-

消息内容

role

str

'user'

Message的role，默认user

metadata

Dict

None

与该Message关联的key/value信息

workspace

str

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

str

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**返回结果**

结果为Message对象，json化内容为：

```
{
    "id": "message_05494921-a646-484e-85fc-76329acba842",
    "object": "thread.message",
    "created_at": 1711345341301,
    "thread_id": "thread_f1e7737e-b045-479f-99d1-510db49d535b",
    "incomplete_details": {},
    "completed_at": null,
    "incomplete_at": null,
    "assistant_id": "",
    "run_id": "",
    "file_ids": [],
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": {
                "value": "sdhafjdasf",
                "annotations": []
            }
        }
    ],
    "metadata": {
        "key": "value"
    },
    "name": "",
    "plugin_call": {},
    "tool_calls": [],
    "status": "",
    "status_code": 200,
    "request_id": "631de0b3-7e50-9c9e-8444-0924d1b7e7a5"
}
```

**输出参数**

**字段名**

**字段类型**

**字段描述**

status\_code

int

为调用http status code，200表示调用成功，其他表示调用出错

id

str

Message id，为uuid字符串

content

List\[dict\]

消息内容

content.type

str

content内容类型，如text

content.text

dict

content内容

content.text.value

str

content text value

metadata

Dict

和这个Message关联的key/value信息

tool\_calls

Dict

调用tool信息

plugin\_call

Dict

调用plugin 信息

created\_at

timestamp

assistant创建时间

gmt\_created

datetime

2024-03-22 17:12:31

gmt\_modified

datetime

2024-03-22 17:12:31

code

str

表示请求失败，表示错误码，成功忽略。

python only

message

str

失败，表示失败详细信息，成功忽略。

python only

## 消息列表

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads/thread_e99a9fe7-0433-426f-98ad-a5139c36579c/messages?limit=2&order=desc' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

thread id

message 所传入的thread id

str

是

limit

创建message的数量

int

否

order

按照创建时间升序或降序

str

否（默认为”desc“）

**返回结果**

```
{
    "object": "list",
    "data": [
        {
            "id": "message_f1933671-19e1-4162-ad25-7326165123e1",
            "object": "thread.message",
            "created_at": 1711508433283,
            "thread_id": "thread_e99a9fe7-0433-426f-98ad-a5139c36579c",
            "assistant_id": "",
            "run_id": "",
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": {
                        "value": "你是谁",
                        "annotations": []
                    }
                }
            ],
            "metadata": {},
            "name": "",
            "plugin_call": {},
            "tool_calls": [],
            "status": ""
        }
    ],
    "first_id": "message_f1933671-19e1-4162-ad25-7326165123e1",
    "last_id": "message_f1933671-19e1-4162-ad25-7326165123e1",
    "has_more": false,
    "request_id": "78f7d607-4a9a-90c6-8040-d3f81c84d60a"
}
```

**输出参数**

输出List message类，并包含除了用户输入以外参数的其他额外字段：

-   多个message 组成的列表
    

## SDK

**代码示例**

Python

```
from dashscope import Messages
import os

messages = Messages.list(
    'thread_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    limit=1,
    order='desc'
)
```

Java

```
import com.alibaba.dashscope.common.GeneralListParam;
import com.alibaba.dashscope.common.ListResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.messages.Messages;
import com.alibaba.dashscope.threads.messages.ThreadMessage;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Messages messages = new Messages();
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
        GeneralListParam listThreadMessages = GeneralListParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();
        ListResult<ThreadMessage> message = messages.list("threadId", listThreadMessages);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

thread\_id

str

\-

指定要查询的thread id。

limit

int

None

要检索的消息数。

order

str

None

按 created\_at 排序的顺序。

workspace

str

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

str

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

**字段名**

**字段类型**

**字段描述**

has\_more

bool

是否还有更多消息可以检索。

last\_id

str

返回的消息列表中最后一个消息的 ID。

first\_id

str

返回的消息列表中第一个消息的 ID。

data

list\[Message\]

Message对象列表。

## 检索消息

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads/thread_e99a9fe7-0433-426f-98ad-a5139c36579c/messages/message_ea26d29d-4509-490e-98e9-9f6238bd821b' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

thread id

待检索的message 所传入的thread id

str

是

message\_id

待检索的message\_id

str

是

**返回结果**

```
{
    "id": "message_ea26d29d-4509-490e-98e9-9f6238bd821b",
    "object": "thread.message",
    "created_at": 1711508622598,
    "thread_id": "thread_e99a9fe7-0433-426f-98ad-a5139c36579c",
    "assistant_id": "",
    "run_id": "",
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": {
                "value": "你好",
                "annotations": []
            }
        }
    ],
    "metadata": {},
    "name": "",
    "plugin_call": {},
    "tool_calls": [],
    "status": "",
    "request_id": "4d5ce962-91c3-9edb-87f7-00bbf985135e"
}
```

**输出参数**

输出检索到的message类，并包含除了用户输入以外参数的其他额外字段：

-   id：message\_id
    
-   request\_id：请求id
    

## SDK

**代码示例**

Python

```
from dashscope import Messages
import os

message = Messages.retrieve(
    'message_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    thread_id='thread_id'
)
```

Java

```
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.messages.Messages;
import com.alibaba.dashscope.threads.messages.ThreadMessage;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Messages messages = new Messages();
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        ThreadMessage message = messages.retrieve("threadId", "messageId", apiKey);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

message\_id

str

\-

指定要查询的Message id

thread\_id

str

\-

指定要查询的Message所属Thread id

workspace

str

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

str

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

参考 create 结果

## 修改消息

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads/thread_e99a9fe7-0433-426f-98ad-a5139c36579c/messages/message_ea26d29d-4509-490e-98e9-9f6238bd821b' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "metadata": {
        "modified": "true",
        "user": "abc123"
    }
}'
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

thread\_id

待修改的thread\_id

str

是

message\_id

待修改的message\_id

str

是

**metadata**

元数据

dict

**返回结果**

```
{
    "id": "message_ea26d29d-4509-490e-98e9-9f6238bd821b",
    "object": "thread.message",
    "created_at": 1711508622598,
    "thread_id": "thread_e99a9fe7-0433-426f-98ad-a5139c36579c",
    "incomplete_details": {},
    "completed_at": null,
    "incomplete_at": null,
    "assistant_id": "",
    "run_id": "",
    "file_ids": [],
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": {
                "value": "你好",
                "annotations": []
            }
        }
    ],
    "metadata": {
        "modified": "true",
        "user": "abc123"
    },
    "name": "",
    "plugin_call": {},
    "tool_calls": [],
    "status": "",
    "request_id": "7877b011-cb94-9df1-9add-dc42b7d611f6"
}
```

**输出参数**

输出修改后的message类，并包含除了用户输入以外参数的其他额外字段：

-   id ：message\_id
    
-   request\_id ：请求id
    

## SDK

**代码示例**

Python

```
from dashscope import Messages

import os

thread = Messages.update(
    'message_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    thread_id='the_message_thread_id',
    metadata={'key': 'value'}
)
```

Java

```
import java.util.Collections;
import com.alibaba.dashscope.common.UpdateMetadataParam;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.messages.Messages;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Messages messages = new Messages();
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
        UpdateMetadataParam updateMetadataParam = UpdateMetadataParam.builder()
                .metadata(Collections.singletonMap("key", "value"))
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();
        messages.update("thread_id", "message_Id", updateMetadataParam);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

message\_id

str

\-

指定要更新的Message id

thread\_id

_str_

\-

指定要更新的Message所属Thread id

metadata

Dict

None

Thread关联信息

workspace

str

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

str

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

参考 create 结果

## **错误码**

如果 Assistant API 调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

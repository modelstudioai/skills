# Threads（下线中）

本文详细阐述了Assistant API中Thread类的各项功能，涵盖了线程的创建、检索、修改以及删除操作。

**重要**

Assistant API**下线中**，建议迁移至[Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)：内置多种工具，并支持多轮上下文管理，可作为替代方案。

> **功能介绍**：如果您想了解 Assistant API 的功能和基本用法，请参考[Assistant API功能概览](https://help.aliyun.com/zh/model-studio/assistant-api/)。

> **有效期限**：所有 Thread 实例均保存在阿里云百炼服务器上，目前没有失效日期，您可通过 thread.id 检索上下文信息。

**函数名**

**类型**

create

创建 Thread 类

retrieve

检索 Thread 类

update

修改 Thread 类

delete

删除 Thread 类

## 创建线程

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ]
}'
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

messages

thread 所传入的message

Message 类

否

metadata

thread使用的名字

str

否

**返回结果**

```
{
    "id": "thread_e99a9fe7-0433-426f-98ad-a5139c36579c",
    "object": "thread",
    "created_at": 1711448377850,
    "metadata": {},
    "request_id": "dd9489ec-dbdb-95d4-9ff8-cfe29b61db27"
}
```

**输出参数**

输出thread类，并包含除了用户输入以外参数的其他额外字段：

-   id ：thread id
    
-   request\_id ：请求id
    

## SDK

**代码示例**

Python

```
import json
import os
from dashscope import Threads

thread = Threads.create(
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    messages=[{"role": "user", "content": "How does AI work? Explain it in simple terms."}]
)
print(json.dumps(thread, default=lambda o: o.__dict__, sort_keys=True, indent=4))
```

Java

```
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.AssistantThread;
import com.alibaba.dashscope.threads.ThreadParam;
import com.alibaba.dashscope.threads.Threads;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Threads threads = new Threads();
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
        AssistantThread assistantThread = threads.create(ThreadParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build());
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

messages

List\[Dict\]

None

Thread初始messages

metadata

Dict

None

与该Thread关联的key/value信息

workspace

str

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

str

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**返回结果**

结果为Thread对象，json化内容为：

```
{
    "created_at": 1711338305031,
    "id": "thread_97934051-2c15-44bf-97de-310039d873f9",
    "metadata": {},
    "object": "thread",
    "request_id": "982d4b9a-b982-9d53-9c79-a75b32f7168a",
    "status_code": 200
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

thread id，为uuid字符串

metadata

Dict

和这个Thread关联的key/value信息

created\_at

timestamp

thread 创建时间

code

str

表示请求失败，显示错误码，成功忽略。

python only

message

str

失败，表示失败的详细信息，成功则忽略。

python only

## 检索线程

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads/thread_c7ebb0ca-2e4f-43e5-b223-6e1f8c6fccc7' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

thread\_id

待检索的thread\_id

str

是

**返回结果**

```
{
    "id": "thread_c7ebb0ca-2e4f-43e5-b223-6e1f8c6fccc7",
    "object": "thread",
    "created_at": 1711507920700,
    "metadata": {},
    "request_id": "4d4e73ad-15fb-96ac-9262-0643a0fdb5ca"
}
```

**输出参数**

输出检索到的thread类，并包含除了用户输入以外参数的其他额外字段：

-   id ：thread\_id
    
-   request\_id ：请求id
    

## SDK

**代码示例**

Python

```
from dashscope import Threads
import os

thread = Threads.retrieve(
    'thread_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
```

Java

```
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.AssistantThread;
import com.alibaba.dashscope.threads.Threads;

public class Main {
    public static void main(String[] args) {
        Threads threads = new Threads();
        // 直接传入 thread_id 和 apiKey
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为："sk-xxx"
        AssistantThread assistantThread = threads.retrieve(
            "thread_id",
            System.getenv("DASHSCOPE_API_KEY")
        );
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

thread\_id

_str_

\-

指定要查询的thread id

workspace

str

None

阿里云百炼的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，仅当 api\_key 为子业务空间 API Key 时才需要传入。

api\_key

str

None

阿里云百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**输出参数**

参考create结果

## 修改线程

## HTTP

**代码示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/threads/thread_c7ebb0ca-2e4f-43e5-b223-6e1f8c6fccc7' \
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

metadata

thread使用的名字

dict

否

**返回结果**

```
{
    "id": "thread_c7ebb0ca-2e4f-43e5-b223-6e1f8c6fccc7",
    "object": "thread",
    "created_at": 1711507920700,
    "metadata": {
        "modified": "true",
        "user": "abc123"
    },
    "request_id": "a9ad63fa-b884-94be-9ec6-5000882de3c4"
}
```

**输出参数**

输出检索到的thread类，并包含除了用户输入以外参数的其他额外字段：

-   id ：thread\_id
    
-   request\_id ：请求id
    

## SDK

**代码示例**

Python

```
from dashscope import Threads
import os

thread = Threads.update(
    'thread_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
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
import com.alibaba.dashscope.threads.Threads;

public class AssistantGeneral {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Threads threads = new Threads();
        UpdateMetadataParam updateMetadataParam = UpdateMetadataParam.builder()
                .metadata(Collections.singletonMap("key", "value"))
                // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();
        threads.update("thread_id", updateMetadataParam);
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

指定需要update的thread id

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

同create，参考create

## 删除线程

## HTTP

**代码示例**

```
curl --location --request DELETE 'https://dashscope.aliyuncs.com/api/v1/threads/thread_c7ebb0ca-2e4f-43e5-b223-6e1f8c6fccc7' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输入参数**

**输入参数名字**

**输入参数的描述**

**参数类型**

**是否必须**

id

待检索的thread id

str

是

**返回结果**

```
{
    "id": "thread_c7ebb0ca-2e4f-43e5-b223-6e1f8c6fccc7",
    "object": "thread.deleted",
    "deleted": true,
    "request_id": "b4edb7b8-5855-9787-b5c3-0374ee2b3b2c"
}
```

**输出参数**

输出删除thread后的状态

## SDK

**代码示例**

Python

```
from dashscope import Threads
import os

thread = Threads.delete(
    'thread_id',
    # 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
```

Java

```
import com.alibaba.dashscope.common.DeletionStatus;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.InvalidateParameter;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.threads.Threads;

public class Main {
    public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException, InvalidateParameter, InterruptedException {
        Threads threads = new Threads();
        // 建议您优先配置环境变量。若没有配置环境变量，请用百炼API Key将下行替换为：apiKey("sk-xxx")
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        DeletionStatus assistantThread = threads.delete("thread_id", apiKey);
    }
}
```

**输入参数**

**参数**

**类型**

**默认值**

**说明**

thread\_id

_str_

\-

指定要删除的thread id

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

id

str

删除的对象的id

deleted

bool

是否删除

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

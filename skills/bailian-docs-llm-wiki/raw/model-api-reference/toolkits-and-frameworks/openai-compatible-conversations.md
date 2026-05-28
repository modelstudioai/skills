# OpenAI Conversations接口兼容

在跨设备或长时间中断的对话中，手动维护消息列表容易丢失上下文。阿里云百炼提供兼容 OpenAI 的 Conversations API。配合 Responses API，可自动注入历史上下文，无需手动同步消息，实现跨场景、跨设备的对话延续。

## Create conversation

创建一个新会话，可同时添加初始消息项。

**中国内地：POST** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations`

**国际：POST** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations`

**重要**

旧版URL路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 即将停止维护，请尽快迁移至新版路径 `/compatible-mode/v1/conversations`。

**items** `_array_`（可选）

初始消息项列表，最多20条。

**属性**

**type** `_string_` **(必选)**

消息类型，仅支持 `message`。

**role** `_string_` **(必选)**

消息的角色。`system` 与`developer` 角色的指令优先级高于 `user` 角色，`assistant` 角色表示模型在之前交互中生成的消息。取值：`user` 、`assistant` 、`system` 、`developer` 。

**content** `_string or array_` **(必选)**

消息内容。支持纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组），列表格式可包含文本等多种内容类型。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

conversation = client.conversations.create(
    metadata={"topic": "demo"},
    items=[
        {"type": "message", "role": "system", "content": "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。"}
    ]
)
print(conversation)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const conversation = await client.conversations.create({
    metadata: { topic: "demo" },
    items: [
        {
            type: "message",
            role: "system",
            content: "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。"
        }
    ]
});
console.log(conversation);
```

## cURL

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    "metadata": {
        "topic": "demo"
    },
    "items": [
        {
            "type": "message",
            "role": "system",
            "content": "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画"
        }
    ]
}'
```

**metadata** `_object_`（可选）

会话元数据，用于以结构化格式存储会话的附加信息。最多16对键值对，key最大长度64字符，value最大长度512字符。

### 响应参数

**created\_at** `_integer_`

会话创建的 Unix 时间戳（毫秒）。

```
{
    "created_at": 1771316949128,
    "id": "conv_xxx",
    "metadata": {
        "topic": "demo"
    },
    "object": "conversation"
}
```

**id** `_string_`

会话唯一标识符。

**metadata** `_object_`

会话元数据，以键值对形式存储的附加信息。最多16对，key最大长度64字符，value最大长度512字符。

**object** `_string_`

对象类型，固定为 `conversation`。

## Retrieve conversation

获取指定会话的信息。

**中国内地：GET** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**国际：GET** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

conversation = client.conversations.retrieve("conv_xxx")
print(conversation)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const conversation = await client.conversations.retrieve(
    "conv_xxx"
);
console.log(conversation);
```

## cURL

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
```

### 响应参数

**created\_at** `_integer_`

会话创建的 Unix 时间戳（毫秒）。

```
{
    "created_at": 1771316949128,
    "id": "conv_xxx",
    "metadata": {
        "topic": "demo"
    },
    "object": "conversation"
}
```

**id** `_string_`

会话唯一标识符。

**metadata** `_object_`

会话元数据，以键值对形式存储的附加信息。最多16对，key最大长度64字符，value最大长度512字符。

**object** `_string_`

对象类型，固定为 `conversation`。

## Update conversation

更新会话的元数据信息。

**中国内地：POST** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**国际：POST** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

updated = client.conversations.update(
    "conv_xxx",
    metadata={"topic": "update"}
)
print(updated)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const updated = await client.conversations.update(
    "conv_xxx",
    { metadata: { topic: "update" } }
);
console.log(updated);
```

## cURL

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    "metadata": {
        "topic": "update"
    }
}'
```

**metadata** `_object_` **(必选)**

会话元数据，会完全覆盖原有元数据。最多16对键值对，key最大长度64字符，value最大长度512字符。

### 响应参数

**created\_at** `_integer_`

会话创建的 Unix 时间戳（毫秒）。

```
{
    "created_at": 1771318152759,
    "id": "conv_xxx",
    "metadata": {
        "topic": "update"
    },
    "object": "conversation"
}
```

**id** `_string_`

会话唯一标识符。

**metadata** `_object_`

会话元数据，以键值对形式存储的附加信息。最多16对，key最大长度64字符，value最大长度512字符。

**object** `_string_`

对象类型，固定为 `conversation`。

## Delete conversation

删除指定会话。会话中的消息项不会被删除。

**中国内地：DELETE** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**国际：DELETE** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

result = client.conversations.delete("conv_xxx")
print(result)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const result = await client.conversations.del(
    "conv_xxx"
);
console.log(result);
```

## cURL

```
curl --location --request DELETE 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
```

### 响应参数

**deleted** `_boolean_`

是否删除成功。

```
{
    "deleted": true,
    "id": "conv_xxx",
    "object": "conversation.deleted"
}
```

**id** `_string_`

被删除的会话ID。

**object** `_string_`

对象类型，固定为 `conversation.deleted`。

## Create Items

向指定会话添加消息项。

**中国内地：POST** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

**国际：POST** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

items = client.conversations.items.create(
    "conv_xxx",
    items=[
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "李红的专业是师范教育"}],
        }
    ],
)
print(items.data)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const items = await client.conversations.items.create(
    "conv_xxx",
    {
        items: [
            {
                type: "message",
                role: "user",
                content: [{ type: "input_text", text: "李红的专业是师范教育" }]
            }
        ]
    }
);
console.log(items.data);
```

## cURL

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    "items": [
        {
            "type": "message",
            "role": "user",
            "content": [{
                "type": "input_text",
                "text": "李红的专业是师范教育"
            }]
        }
    ]
}'
```

**items** `_array_` **(必选)**

消息项列表，每次最多添加20条。

**属性**

**type** `_string_` **(必选)**

消息类型，仅支持 `message`。

**role** `_string_` **(必选)**

消息的角色。`system` 、`developer`角色的指令优先级高于 `user` 角色，`assistant` 角色表示模型在之前交互中生成的消息。取值：`user`、`assistant`、`system`、`developer`。

**content** `_string or array_` **(必选)**

消息内容。支持纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组），列表格式可包含文本等多种内容类型。

### 响应参数

**data** `_array[object]_`

创建的消息项列表。

**属性**

**id** `_string_`

消息项唯一标识符。

**content** `_string or array_`

消息内容。纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组）。

**role** `_string_`

消息的角色类型，取值：`user`、`assistant`、`system`、`developer`。

**status** `_string_`

消息的处理状态，取值：`in_progress`（处理中）、`completed`（已完成）、`incomplete`（未完成）。

**type** `_string_`

消息项的类型，固定为 `message`。

```
{
    "data": [
        {
            "content": [
                {
                    "text": "李红的专业是师范教育",
                    "type": "input_text"
                }
            ],
            "id": "msg_xxx",
            "role": "user",
            "status": "completed",
            "type": "message"
        }
    ],
    "first_id": "msg_xxx",
    "has_more": false,
    "last_id": "msg_xxx"
}
```

**first\_id** `_string_`

列表中第一条消息项的ID。

**has\_more** `_boolean_`

是否还有更多数据。

**last\_id** `_string_`

列表中最后一条消息项的ID。

## List Items

列出会话中的所有消息项。

**中国内地：GET** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

**国际：GET** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

items = client.conversations.items.list("conv_xxx")
print(items.data)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const items = await client.conversations.items.list(
    "conv_xxx"
);
console.log(items.data);
```

## cURL

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items?limit=10&order=asc' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
```

**after** `_string_`（可选）

分页游标，返回指定消息ID之后的消息项。

**order** `_string_`（可选）

排序方式，`asc`（升序）或 `desc`（降序），默认 `desc`。

**limit** `_integer_`（可选）

返回数量，范围1-100，默认20。

### 响应参数

**data** `_array[object]_`

消息项列表。

**属性**

**id** `_string_`

消息项唯一标识符。

**content** `_string or array_`

消息内容。纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组）。

**role** `_string_`

消息的角色类型，取值：`user`、`assistant`、`system`、`developer`。

**status** `_string_`

消息的处理状态，取值：`in_progress`（处理中）、`completed`（已完成）、`incomplete`（未完成）。

**type** `_string_`

消息项的类型，固定为 `message`。

```
{
    "data": [
        {
            "content": [
                {
                    "text": "李红，一位温婉而坚韧的江南女子，出生在浙江省，今年20岁",
                    "type": "input_text"
                }
            ],
            "id": "msg_7639f8f6-484b-454a-8125-96a3f40eb9e8",
            "role": "user",
            "status": "completed",
            "type": "message"
        },
        {
            "content": [
                {
                    "text": "李红的闺蜜是小芳",
                    "type": "input_text"
                }
            ],
            "id": "msg_288594f6-6ef1-4519-94d4-a545ca311828",
            "role": "user",
            "status": "completed",
            "type": "message"
        }
    ],
    "first_id": "msg_7639f8f6-484b-454a-8125-96a3f40eb9e8",
    "has_more": false,
    "last_id": "msg_288594f6-6ef1-4519-94d4-a545ca311828",
    "object": "list"
}
```

**first\_id** `_string_`

列表中第一条消息项的ID。

**has\_more** `_boolean_`

是否还有更多数据。

**last\_id** `_string_`

列表中最后一条消息项的ID。

**object** `_string_`

对象类型，固定为 `list`。

## Retrieve Item

获取指定消息项的详情。

**中国内地：GET** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

**国际：GET** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

item = client.conversations.items.retrieve(
    "msg_xxx",
    conversation_id="conv_xxx"
)
print(item)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const item = await client.conversations.items.retrieve(
    "msg_xxx",
    { conversation_id: "conv_xxx" }
);
console.log(item);
```

## cURL

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items/msg_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
```

**item\_id** `_string_` **(必选, Path)**

消息项ID。

### 响应参数

**content** `_array[object]_`

消息内容列表，包含一个或多个内容对象。

**属性**

**type** `_string_`

内容类型，如 `input_text`（用户输入文本）或 `output_text`（模型输出文本）。

**text** `_string_`

文本内容。

```
{
    "content": [
        {
            "text": "李红的专业是师范教育",
            "type": "input_text"
        }
    ],
    "id": "msg_xxx",
    "role": "user",
    "status": "completed",
    "type": "message"
}
```

**id** `_string_`

消息项唯一标识符。

**role** `_string_`

消息的角色类型，取值：`user`、`assistant`、`system`、`developer`。

**status** `_string_`

消息的处理状态，取值：`in_progress`（处理中）、`completed`（已完成）、`incomplete`（未完成）。

**type** `_string_`

消息项的类型，固定为 `message`。

## Delete Item

删除指定的消息项。

**中国内地：DELETE** `https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

**国际：DELETE** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

**conversation\_id** `_string_` **(必选, Path)**

会话ID。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

result = client.conversations.items.delete(
    "msg_xxx",
    conversation_id="conv_xxx"
)
print(result)
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const result = await client.conversations.items.del(
    "msg_xxx",
    { conversation_id: "conv_xxx" }
);
console.log(result);
```

## cURL

```
curl --location --request DELETE 'https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items/msg_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
```

**item\_id** `_string_` **(必选, Path)**

消息项ID。

### 响应参数

**deleted** `_boolean_`

是否删除成功。

```
{
    "deleted": true,
    "id": "msg_xxx",
    "object": "conversation.item.deleted"
}
```

**id** `_string_`

被删除的消息项ID。

**object** `_string_`

对象类型，固定为 `conversation.item.deleted`。

## Response API 使用 conversation 示例

通过 Responses API 的 `conversation` 参数，可以实现多轮对话的上下文保持。

> 请勿同时传入`previous_response_id`和`conversation`，否则会报错：`[400] INVALID_REQUEST: Mutually exclusive parameters: Ensure you are only providing one of: previous_response_id or conversation.`

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

conversation = client.conversations.create(
    items=[
        {
            "type": "message",
            "role": "system",
            "content": "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。",
        }
    ]
)

response1 = client.responses.create(
    conversation=conversation.id, model="qwen3.6-plus", input="李红今年多大了"
)
print(f"第一轮响应: {response1.output_text}")

response2 = client.responses.create(
    conversation=conversation.id, model="qwen3.6-plus", input="她的兴趣爱好是什么？"
)
print(f"第二轮响应: {response2.output_text}")
```

## Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const conversation = await client.conversations.create({
  items: [
    {
      type: "message",
      role: "system",
      content: "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。"
    }
  ]
});

const response1 = await client.responses.create({
  conversation: conversation.id,
  model: "qwen3.6-plus",
  input: "李红今年多大了"
});
console.log("第一轮响应:", response1.output_text);

const response2 = await client.responses.create({
  conversation: conversation.id,
  model: "qwen3.6-plus",
  input: "她的兴趣爱好是什么？"
});
console.log("第二轮响应:", response2.output_text);
```

## 使用限制

-   创建会话或添加消息项时，`items` 最多包含20条。
    
-   `metadata` 最多16对键值对，key最大长度64字符，value最大长度512字符。

# 获取输入项列表

获取生成指定 Response 时所使用的输入项列表。在多轮对话（使用 previous\_response\_id 串联）中，会一并返回历史轮次的用户输入和模型回复。仅当原创建请求中 store=true 时，返回的 Response ID 才支持查询。

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/{response_id}/input_items`

## 路径参数

**response\_id**`string`（必选）

要查询输入项的 Response ID，格式为 `resp_xxx`。仅当原创建请求中 `store=true` 时，返回的 Response ID 才支持查询。

## 查询参数

**after**`string`（可选）

以指定的 item ID（格式为 `msg_xxx`）作为起点，返回排在该 ID 之后的数据，顺序由 `order` 决定。**item ID 来源**：[创建响应](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)返回的 `output[].id`；或本接口返回的 `data[].id`、`first_id`、`last_id`。常用于翻页：把上一次返回的 `last_id` 作为本次的 `after` 传入，即可继续获取后续数据。

**limit**`integer`（可选）

返回的最大条数，取值范围 \[1, 100\]，默认值为 20。

**order**`string`（可选）

排序方式，支持 `asc`（升序）和 `desc`（降序），默认值为 `desc`。

#### 默认查询

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = client.responses.input_items.list("resp_xxx")
print(response.data)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.inputItems.list("resp_xxx");
    console.log(response.data);
}

main();
```

curl

```
curl https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx/input_items \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 按条件查询

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = client.responses.input_items.list(
    "resp_xxx",
    # after 取 item ID（msg_xxx）：可来自创建响应返回的 output[].id，或本接口返回的 data[].id / first_id / last_id
    after="msg_xxx",
    limit=10,
    order="asc",
)
print(response.data)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.inputItems.list("resp_xxx", {
        // after 取 item ID（msg_xxx）：可来自创建响应返回的 output[].id，或本接口返回的 data[].id / first_id / last_id
        after: "msg_xxx",
        limit: 10,
        order: "asc",
    });
    console.log(response.data);
}

main();
```

curl

```
# after 取 item ID（msg_xxx）：可来自创建响应返回的 output[].id，或本接口返回的 data[].id / first_id / last_id
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx/input_items?after=msg_xxx&limit=10&order=asc" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 返回结果

**data** `array`

输入项列表。每个元素是一个消息对象，包含 `id`、`role`、`content`、`type`、`status` 字段。`role` 取值为 `user` 或 `assistant`；`content` 中元素的 `type` 取值为 `input_text`（用户输入）或 `output_text`（模型回复）。多轮对话（使用 `previous_response_id` 串联）中，会按发生顺序包含历史用户消息与历史模型回复。

**first\_id** `string`

列表中第一个元素的 ID。

**last\_id** `string`

列表中最后一个元素的 ID。

**has\_more** `boolean`

是否还有未返回的数据。当为 `true` 时，把本次返回的 `last_id` 作为下一次请求的 `after` 参数，可继续获取后续数据。

**id** `string`

对应的 Response ID。

**model** `string`

生成该 Response 时使用的模型名称。

**created\_at** `integer`

Response 创建时间的 Unix 时间戳（**毫秒**）。注意：与"创建响应/检索响应"接口返回的 `created_at`（秒）单位不同。

**previous\_response\_id** `string`

多轮对话（使用 `previous_response_id` 串联）时返回，值为上一轮的 Response ID。

```
{
    "created_at": 1778674066000,
    "data": [
        {
            "content": [
                {
                    "text": "你好",
                    "type": "input_text"
                }
            ],
            "id": "msg_8dac4972-fdba-42b5-bed9-280441ced8ea",
            "role": "user",
            "status": "completed",
            "type": "message"
        }
    ],
    "first_id": "msg_8dac4972-fdba-42b5-bed9-280441ced8ea",
    "has_more": false,
    "id": "resp_4ca7fa5e-6ff5-9787-bc18-af6ca5eff36c",
    "last_id": "msg_8dac4972-fdba-42b5-bed9-280441ced8ea",
    "model": "qwen3.8-max"
}
```

## 错误响应

当指定的 Response ID 不存在时，返回以下错误：

```
{
    "request_id": "339b771548c7fbb15717316b49627681",
    "code": "InvalidParameter",
    "message": "Response with id 'resp_xxx' not found."
}
```

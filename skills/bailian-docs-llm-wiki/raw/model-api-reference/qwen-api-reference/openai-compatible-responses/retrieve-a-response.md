# 获取响应

根据 Response ID 获取一个已完成的模型响应。

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/{response_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

## 路径参数

**response\_id**`string`（必选）

要获取的 Response ID，格式为 `resp_xxx`。可从[创建响应](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)接口的响应中获取。仅当原创建请求中 `store=true` 时返回的 Response ID 可被检索。

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = client.responses.retrieve("resp_xxx")
print(response)
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
    const response = await openai.responses.retrieve("resp_xxx");
    console.log(response);
}

main();
```

curl

```
curl https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 返回结果

返回与[创建响应](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses#8b91df45f4k58)相同的 Response 对象。各字段含义如下：

**id** `string`

本次响应的唯一标识符，格式为 `resp_xxx`。

**object** `string`

对象类型，固定为 `response`。

**status** `string`

响应状态。枚举值:`completed`(完成)、`failed`(失败)、`in_progress`(生成中)、`cancelled`(已取消)、`queued`(排队中)、`incomplete`(不完整)。

**created\_at** `integer`

响应创建时的 Unix 时间戳（秒）。

**completed\_at** `integer`

响应生成完成时的 Unix 时间戳（秒）。响应未完成时为 `null`。

**error** `object`

当模型生成响应失败时返回的错误对象。成功时为 `null`。

**model** `string`

用于生成响应的模型 ID。

**output** `array`

模型生成的输出项数组。数组中的元素类型和顺序取决于模型的响应。

数组元素属性

**type** `string`

输出项类型。枚举值：

-   `message`：消息类型，包含模型最终生成的回复内容。
-   `reasoning`：推理类型，设置 `reasoning.effort`（非 `none`）或开启思考模式时返回。推理 Token 会被计入 `output_tokens_details.reasoning_tokens` 中，按推理 Token 计费。
-   `function_call`：函数调用类型，使用自定义 `function` 工具时返回。需要处理函数调用并返回结果。
-   `web_search_call`：搜索调用类型，使用 `web_search` 工具时返回。
-   `code_interpreter_call`：代码执行类型，使用 `code_interpreter` 工具时返回。
-   `web_extractor_call`：网页抽取类型，使用 `web_extractor` 工具时返回。需要配合 `web_search` 工具一起使用。
-   `web_search_image_call`：文搜图调用类型，使用 `web_search_image` 工具时返回。包含搜索到的图片列表。
-   `image_search_call`：图搜图调用类型，使用 `image_search` 工具时返回。包含搜索到的相似图片列表。
-   `mcp_call`：MCP 调用类型，使用 `mcp` 工具时返回。包含 MCP 服务的调用结果。
-   `file_search_call`：知识库搜索调用类型，使用 `file_search` 工具时返回。包含知识库的检索查询和结果。

**id** `string`

输出项的唯一标识符。所有类型的输出项都包含此字段。

**role** `string`

消息角色，固定为 `assistant`。仅当 `type` 为 `message` 时存在。

**status** `string`

输出项状态。可选值：`completed`（完成）、`in_progress`（生成中）。当 `type` 不为`reasoning`时存在。

**name** `string`

工具或函数名称。当 `type` 为 `function_call`、`web_search_image_call`、`image_search_call`、`mcp_call` 时存在。

对于 `web_search_image_call` 和 `image_search_call`，值分别固定为 `"web_search_image"` 和 `"image_search"`。

对于 `mcp_call`，值为 MCP 服务中被调用的具体函数名（如 `amap-maps-maps_geo`）。

**arguments** `string`

工具调用的参数，JSON 字符串格式。当 `type` 为 `function_call`、`web_search_image_call`、`image_search_call`、`mcp_call` 时存在。使用前需要通过 `JSON.parse()` 解析。不同工具类型的 arguments 内容：

-   `web_search_image_call`：`{"queries": ["搜索关键词1", "搜索关键词2"]}`，其中 `queries` 为模型根据用户输入自动生成的搜索关键词列表。
-   `image_search_call`：`{"img_idx": 0, "bbox": [0, 0, 1000, 1000]}`，其中 `img_idx` 为输入图片的索引（从 0 开始），`bbox` 为搜索区域的边界框坐标 \[x1, y1, x2, y2\]，坐标范围 0-1000。
-   `function_call`：按用户定义的函数参数 schema 生成的参数对象。
-   `mcp_call`：MCP 服务中被调用函数的参数对象。

**call\_id** `string`

函数调用的唯一标识符。仅当 `type` 为 `function_call` 时存在。在返回函数调用结果时，需要通过此 ID 关联请求与响应。

**content** `array`

消息内容数组。仅当 `type` 为 `message` 时存在。

数组元素属性

**type** `string`

内容类型，固定为 `output_text`。

**text** `string`

模型生成的文本内容。

**annotations** `array`

文本注释数组。通常为空数组。

**summary** `array`

推理摘要数组。仅当 `type` 为 `reasoning` 时存在。每个元素包含 `type`（值为 `summary_text`）和 `text`（摘要文本）字段。

**action** `object`

搜索动作信息。仅当 `type` 为 `web_search_call` 时存在。

属性

**query** `string`

搜索查询关键词。

**type** `string`

搜索类型，固定为 `search`。

**sources** `array`

搜索来源列表。每个元素包含 `type`和 `url`字段。

**code** `string`

模型生成并执行的代码。仅当 `type` 为 `code_interpreter_call` 时存在。

**outputs** `array`

代码执行输出数组。仅当 `type` 为 `code_interpreter_call` 时存在。每个元素包含 `type`（值为 `logs`）和 `logs`（代码执行日志）字段。

**container\_id** `string`

代码解释器容器标识符。仅当 `type` 为 `code_interpreter_call` 时存在。用于关联同一会话中的多次代码执行。

**goal** `string`

抽取目标描述，说明需要从网页中提取哪些信息。仅当 `type` 为 `web_extractor_call` 时存在。

**output** `string`

工具调用的输出结果，字符串格式。

-   当 `type` 为 `web_extractor_call` 时为网页抽取的内容摘要
-   当 `type` 为 `web_search_image_call` 或 `image_search_call` 时为 JSON 字符串，包含图片搜索结果数组，每个元素包含 `title`（图片标题）、`url`（图片 URL）和 `index`（序号）字段
-   当 `type` 为 `mcp_call` 时为 MCP 服务返回的 JSON 字符串结果。

**urls** `array`

被抽取的网页 URL 列表。仅当 `type` 为 `web_extractor_call` 时存在。

**server\_label** `string`

MCP 服务标签。仅当 `type` 为 `mcp_call` 时存在。标识本次调用所使用的 MCP 服务。

**queries** `array`

知识库检索使用的查询列表。仅当 `type` 为 `file_search_call` 时存在。数组元素为字符串，表示模型生成的搜索查询词。

**results** `array`

知识库检索结果数组。仅当 `type` 为 `file_search_call` 时存在。

数组元素属性

**file\_id** `string`

匹配文档的文件 ID。

**filename** `string`

匹配文档的文件名。

**score** `float`

匹配相关度评分，取值范围 0-1，值越大表示相关度越高。

**text** `string`

匹配到的文档内容片段。

**usage** `object`

本次请求的 Token 消耗信息。

属性

**input\_tokens** `integer`

输入的 Token 数。

**output\_tokens** `integer`

模型输出的 Token 数。

**total\_tokens** `integer`

消耗的总 Token 数，为 input\_tokens 与 output\_tokens 的总和。

**input\_tokens\_details** `object`

输入 Token 的细粒度分类。

属性

**cached\_tokens** `integer`

命中缓存的 Token 数。

**output\_tokens\_details** `object`

输出 Token 的细粒度分类。

属性

**reasoning\_tokens** `integer`

思考过程 Token 数。

**x\_details** `array`

计费明细数组。

属性

**input\_tokens** `integer`

本计费类型的输入 Token 数。

**output\_tokens** `integer`

本计费类型的输出 Token 数。

**total\_tokens** `integer`

本计费类型的总 Token 数。

**x\_billing\_type** `string`

固定为`response_api`。

**prompt\_tokens\_details** `object`

启用 Session 缓存后返回。包含 `cached_tokens`（命中缓存的 Token 数）字段。

**x\_tools** `object`

工具使用统计信息。当使用内置工具时，包含各工具的调用次数。示例：`{"web_search": {"count": 1}}`

**tools** `array`

回显原创建响应请求中 `tools` 参数的完整内容。结构与请求体中的 `tools` 参数相同。无工具时为空数组 `[]`。

**tool\_choice** `string`

回显原创建响应请求中 `tool_choice` 参数的值。枚举值：`auto`、`none`、`required`。

**parallel\_tool\_calls** `boolean`

回显原创建响应请求中 `parallel_tool_calls` 参数的值，表示是否允许模型并行调用多个工具。

**temperature** `float`

回显原创建响应请求中 `temperature` 参数的值。采样温度，控制模型生成文本的多样性，取值范围 \[0, 2)。未设置时返回模型默认值。

**top\_p** `float`

回显原创建响应请求中 `top_p` 参数的值。核采样的概率阈值，取值范围 (0, 1.0\]。未设置时返回模型默认值。

**frequency\_penalty** `float`

回显原创建响应请求中 `frequency_penalty` 参数的值。频率惩罚系数，正值降低重复用词的概率。

**presence\_penalty** `float`

回显原创建响应请求中 `presence_penalty` 参数的值。存在惩罚系数，正值增加生成新主题的概率。

**top\_logprobs** `integer`

回显原创建响应请求中 `top_logprobs` 参数的值。每个位置返回的最可能 Token 数量。未启用时为 `0`。

**store** `boolean`

回显原创建响应请求中 `store` 参数的值。`true` 表示该响应已储存，可被 `previous_response_id` 引用；`false` 表示未储存。

**service\_tier** `string`

服务等级，固定为 `default`。

**background** `boolean`

是否为后台异步执行的响应。当前百炼仅支持同步调用，固定为 `false`。

**metadata** `object`

回显原创建响应请求中 `metadata` 参数的内容。可用于附加自定义键值对的对象，无设置时为空对象 `{}`。

```
{
    "background": false,
    "completed_at": 1778676420,
    "created_at": 1778676418,
    "frequency_penalty": 0.0,
    "id": "resp_801bc2c4-93d9-910f-b35d-5274f5a737c1",
    "metadata": {},
    "model": "qwen-plus",
    "object": "response",
    "output": [
        {
            "content": [
                {
                    "annotations": [],
                    "text": "你好！很高兴见到你。有什么我可以帮助你的吗？",
                    "type": "output_text"
                }
            ],
            "id": "msg_8c54756c-9b65-4a95-81d7-4276d91406db",
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ],
    "parallel_tool_calls": true,
    "presence_penalty": 0.0,
    "service_tier": "default",
    "status": "completed",
    "store": true,
    "temperature": 1.0,
    "tool_choice": "auto",
    "tools": [],
    "top_logprobs": 0,
    "top_p": 1.0,
    "usage": {
        "input_tokens": 45,
        "input_tokens_details": {
            "cached_tokens": 0
        },
        "output_tokens": 63,
        "output_tokens_details": {
            "reasoning_tokens": 0
        },
        "total_tokens": 108,
        "x_details": [
            {
                "input_tokens": 45,
                "output_tokens": 63,
                "prompt_tokens_details": {
                    "cached_tokens": 0
                },
                "total_tokens": 108,
                "x_billing_type": "response_api"
            }
        ]
    }
}
```

## 错误响应

当指定的 Response ID 不存在时，返回以下错误：

```
{
    "error": {
        "message": "Response with id 'resp_xxx' not found.",
        "type": "InvalidParameter"
    }
}
```

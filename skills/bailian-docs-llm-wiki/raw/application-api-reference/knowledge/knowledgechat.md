# 知识问答

基于知识库的智能问答接口，通过 SSE 流式输出，依次返回规划、工具调用、生成三个阶段。

## 接口说明

-   **权限要求**：调用本接口需提供阿里云百炼 API Key及业务空间。在控制台 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/api-key)及[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取。
-   **调用方式**：HTTP REST，`POST` + `application/json`。Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID。
-   **前置条件**：调用前须在百炼控制台 [知识问答服务页面](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base/list?activeKey=qa) 创建并发布知识问答服务，获取应用 ID（`agent_id`），否则报 Agent 未发布。
-   **多轮上下文**：平台不保存对话状态，每次请求需传入完整 `messages` 历史。建议限制历史长度（如最近 10 轮），避免超出模型上下文窗口。响应不返回 `session_id`。
-   **流式要求**：`stream` 必须为 `true`，当前版本仅支持流式响应；若为 `false` 或为空将导致请求失败。
-   **临时文件**：开启控制台文件预解析后，可在对话时通过 `parameters.agent_options.session_files` 临时传入文件（最多 10 个），文件 ID 通过[添加文件](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)接口获取。
-   **限流**：默认用户维度 25 QPS。如遇限流，请稍后重试。

## 请求语法

```
POST /api/v2/apps/knowledge/chat HTTP/1.1
Host: {workspaceId}.cn-beijing.maas.aliyuncs.com
Authorization: Bearer <API-Key>
Content-Type: application/json
Accept: text/event-stream
```

## 请求参数

请求体为 `input` / `parameters` / `stream` 三部分。嵌套字段在下表中以缩进表示层级。

名称

类型

必填

描述

示例

input

object

是

输入参数。

input.messages

array<object>

是

对话消息列表，DashScope 标准格式。

messages\[\].role

string

是

消息角色：`user` 或 `assistant`。

user

messages\[\].content

string\\|array

是

消息内容，支持纯文本或多模态数组。纯文本传字符串；多模态传数组，元素为 ContentPart（如 `[{"type":"text","text":"..."},{"type":"image_url","image_url":{"url":"..."}}]`）。

input.request\_id

string

否

业务侧自定义请求 ID。

parameters

object

是

配置参数字段。

parameters.agent\_options

object

是

智能体专用参数，包含 `agent_id` 等。

agent\_options.agent\_id

string

是

问答服务（agent）应用 ID，在控制台知识问答页面创建并发布后获取。

aid-xxxxxxxxxxxxxxxx

agent\_options.session\_files

array<string>

否

会话文件 ID 列表，最多 10 个。须在控制台开启文件预解析后传入才生效；文件 ID 通过 `addFile`（注册文件）接口获取。

stream

boolean

是

是否开启流式输出。必须填 `true`，当前版本仅支持流式响应；填 `false` 或不填请求将失败。

true

## 响应参数

**顶层字段**

名称

类型

描述

output

object

模型输出。

output.request\_id

string

业务侧自定义请求 ID（与请求 `input.request_id` 对应）。

output.choices

array<object>

模型输出信息，长度恒为 1。结构见下表。

code

string

状态码，成功为 `200`。

message

string

状态信息，成功为 `Success`。

request\_id

string

请求 ID（DashScope 平台级，全流不变）。

usage

object

用量统计（`input_tokens` / `output_tokens` / `total_tokens` / `cached_tokens`）。仅出现在 `tool_calling` 与 `generation_end` 等结算帧，普通流式片段不携带。

**output.choices\[\] 结构**

名称

类型

描述

message

object

一条消息，包含模型回复的内容、工具调用信息和当前所处阶段。

message.role

string

角色：`user`、`assistant`、`tool`。

message.content

string\\|array

生成内容/工具返回内容。`planning` 阶段为规划文本流，`generating` 阶段为回答文本流，边界帧可为空字符串。也可是多模态数组。

message.id

string

本次 run 的唯一 ID（如 `run--xxxx`），同一轮内不变。

message.type

string

消息类型：`ai`（assistant 帧，含思考/planning/生成）、`tool`（工具返回帧）。

message.tool\_calls

array<object>

工具调用信息。仅 `tool_calling` 帧携带，其余为 `[]`。每个元素含 `index` / `id` / `type`(固定 `function`) / `function.name` / `function.arguments`（JSON 字符串，需二次解析）。

message.tool\_call\_id

string

工具返回帧：对应 `tool_calls[].id`，用于关联触发帧与返回帧。

message.additional\_kwargs

object

附加参数。assistant 帧为 `{}`；tool 帧携带 `extra_json`，为工具返回的结构化结果（检索类工具为 `docs` 切片数组）。

message.extra

object

步骤状态信息。见下表。

message.response\_metadata

object

请求模型调用详细信息。边界帧携带 `agent_name`、`request_id`，有时含 `model_name`、`finish_reason`；普通片段为 `{}`。

finish\_reason

string

生成结束原因，仅尾包输出 `stop`；流式片段为 `""`。

**message.extra 结构**

名称

类型

描述

group

string

大阶段：`planning`（规划阶段，包含开始和结束事件）、`generating`（生成阶段，包含开始和结束事件）。工具调用时大阶段还是 `planning`，只是细分步骤变成 `tool_calling`。

step

string

当前步骤：`planning`、`tool_calling`、`generating`。`step_change` 有时可能不返回，建议以 `step` 为准。

step\_change

string

步骤变化事件：`plan_start` / `plan_end` / `tool_calling` / `tool_return` / `generation_start` / `generation_end`，或空（进行中）。空包时可能不存在。

**执行阶段（group）**

group

说明

planning

规划中，包含 start 和 end 事件。

generating

生成中，包含 start 和 end 事件。

**当前步骤（step）**

step

说明

planning

规划中。

tool\_calling

工具调用中（此时 `group` 仍为 `planning`）。

generating

生成中。

**步骤变化事件（step\_change）**

step

step\_change

事件

说明

planning

plan\_start

开始规划

`step` 变为 `planning`，后续 `content` 为规划内容。

planning

空

规划中

`content` 为规划文本流。

planning

plan\_end

结束规划

`step` 即将变化，事件发生时仍为 `planning`。

tool\_calling

tool\_calling

工具调用

抛出完整 `tool_calls`（含工具名与参数），携带本轮 `usage`。

tool\_calling

tool\_return

工具返回

`role` 为 `tool`，`content` 为返回摘要，`additional_kwargs.extra_json` 为结构化返回（检索类即 `docs`）。

generating

generation\_start

开始生成

后续 `content` 为最终回答文本流。

generating

空

生成中

`content` 为回答文本流。

generating

generation\_end

结束生成

`finish_reason` 为 `stop`，携带最终 `usage`。

**工具清单**

模型在工具调用阶段会从以下工具里选用，工具名放在 `tool_calls[].function.name`。`arguments` 是一段 JSON 字符串，需要再解析一次才能拿到具体参数；工具的返回结果放在 `tool_return` 帧的 `additional_kwargs.extra_json.docs` 里。

function.name

工具

arguments

返回 docs\[\]

semantic\_search

知识库搜索

{"query", "target\_ids"}

命中切片数组，含正文与多维得分。

obtain\_file

获取文件完整内容

{"file\_id", "max\_tokens"}

文件级信息（含 Markdown 预签 URL），全文在 `message.content`。

execute\_sql

执行 SQL 查询（NL2SQL）

{"sql", "knowledge\_base\_id"}

SQL 结果行，每行 = `_citation_index` + 查询列字段。

section\_browse

章节检索

{"knowledge\_base\_id", "file\_id", "section\_path"}

章节预览（前 300 字）。

section\_peruse

章节精读

{"knowledge\_base\_id", "file\_id", "section\_path", "max\_tokens"}

章节完整内容。

**说明**`max_tokens`（`obtain_file` / `section_peruse`）为字符串形式的数字，如 `"989482"`。`target_ids` / `knowledge_base_id` 即知识库（pipeline）ID；`section_path` 由`>` 分隔层级，例如：`开放接口文档>接口调用说明`。一次请求中多个工具可串联调用（如 `semantic_search` 定位文件 → `obtain_file` 取全文）。

## 错误码

SSE 流式响应中，错误以 `event: error` 帧返回（`data:` 后为错误 JSON，含 `code` / `message` / `request_id`）。鉴权失败在 HTTP 层返回。

HTTP 状态码

错误码

说明

401

InvalidApiKey

鉴权失败，API Key 无效或缺失。

500

AgentApp.NotFound

Agent 不存在或未发布等服务端错误，以 SSE error 帧返回。

## 示例

以下示例向已发布的知识问答服务提问「什么是百炼知识库？」，`agent_id` 替换为实际问答服务 ID。

### cURL

```
curl -X POST "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": [{"type": "text", "text": "什么是百炼知识库？"}]}
      ]
    },
    "parameters": {
      "agent_options": {
        "agent_id": "aid-xxxxxxxxxxxxxxxx"
      }
    },
    "stream": true
  }'
```

### Python

```
import os
import requests

resp = requests.post(
    "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat",
    headers={
        "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    },
    json={
        "input": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": "什么是百炼知识库？"}]}
            ]
        },
        "parameters": {
            "agent_options": {
                "agent_id": "aid-xxxxxxxxxxxxxxxx"
            }
        },
        "stream": True,
    },
    stream=True,
)
for line in resp.iter_lines():
    if line:
        print(line.decode())
```

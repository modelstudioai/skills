# 知识问答

基于知识库的智能问答接口，通过 SSE 流式输出，依次返回规划、工具调用、生成三个阶段。

## 接口说明

-   **权限要求**：调用本接口需提供阿里云百炼 API Key及业务空间。在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)及[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取。
-   **调用方式**：HTTP REST，`POST` + `application/json`。Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID。
-   **前置条件**：调用前须在百炼控制台 [知识问答服务页面](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list) 创建并发布知识问答服务，获取应用 ID（`agent_id`），否则报 Agent 未发布。
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

agent\_options.enable\_cache\_control

boolean

否

是否开启显式上下文缓存（KV Cache）。`true` 时请求打下缓存断点，前缀一致即确定性命中，命中部分的输入 Token 按折扣计费且首包延迟降低；`false`（默认）时不打断点，是否命中取决于模型侧的隐式缓存能力。同一请求只生效一种缓存模式，详见[上下文缓存](https://help.aliyun.com/zh/model-studio/knowledgechat#section-context-cache-title)。

false

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

用量统计（`input_tokens` / `output_tokens` / `total_tokens` / `cached_tokens`）。仅出现在 `tool_calling` 与 `generation_end` 等结算帧，普通流式片段不携带。`cached_tokens` 为本次请求命中上下文缓存的输入 tokens，是多轮模型调用的累计值，开启方式见[上下文缓存](https://help.aliyun.com/zh/model-studio/knowledgechat#section-context-cache-title)。

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

## 上下文缓存

问答链路已适配模型侧的上下文缓存（KV Cache）：多轮对话与多轮工具调用中请求前缀保持稳定，命中部分的输入 Token 按折扣价计费，且首包延迟降低。缓存分为隐式、显式两种模式，**同一请求只生效一种**：

隐式缓存

显式缓存

如何启用

模型支持则默认生效，无需配置，也无法关闭

请求中传 `enable_cache_control: true`

命中确定性

不确定，由系统自动识别公共前缀

确定性命中（前缀一致即命中）

创建缓存计费

输入单价 100%（无额外开销）

输入单价 125%

命中缓存计费

输入单价 20%

输入单价 10%

缓存有效期

不确定，系统定期清理

5 分钟，每次命中后重置

最小可缓存长度

1024 Token

1024 Token

**说明**计费比例与有效期以百炼官方文档[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[显式缓存最佳实践](https://help.aliyun.com/zh/model-studio/explicit-cache-guide)及控制台账单为准。内部实测隐式缓存命中率约为显式缓存的 75%，仅供参考，非官方指标。

### 开启显式缓存

在 `parameters.agent_options` 中增加 `enable_cache_control` 即可，默认 `false`，其余参数保持不变：

```
curl -X POST "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "这几款酒的产区分别是什么？"}
      ]
    },
    "parameters": {
      "agent_options": {
        "agent_id": "aid-xxxxxxxxxxxxxxxx",
        "enable_cache_control": true
      }
    },
    "stream": true
  }'
```

### 模型支持

两种缓存的模型支持范围不同。模型由平台侧配置决定，本接口不暴露模型选择参数，能用哪种缓存取决于问答服务实际使用的模型：

模型

显式缓存

隐式缓存

qwen3.6-plus（当前默认）

支持

不支持

qwen3.6-flash

支持

不支持

qwen3.7-plus

支持

支持

**警告**当前默认模型 qwen3.6-plus **不支持隐式缓存**：不传 `enable_cache_control` 时没有任何缓存生效，`cached_tokens` 会一直为 0，这是模型侧能力限制而非接口异常。要获得缓存收益（降本 + 降首包延迟）需开启显式缓存；仅当服务运行在 qwen3.7-plus 上时，不开启才有隐式缓存兜底。模型支持列表以[显式缓存官方文档](https://help.aliyun.com/zh/model-studio/explicit-cache-guide)的“支持的模型”章节为准。

### 适用场景

缓存收益分两类场景，**单请求内的收益比跨请求更稳定、更显著**。

**强烈推荐：单请求内多次检索与思考**。一次提问触发多轮工具调用（多次 `semantic_search` / `execute_sql` / 章节浏览 + 中间思考）时，缓存断点会随每轮新增的工具结果向后移动，上一轮的完整上下文（含检索结果）成为下一轮的稳定前缀。问题越复杂、检索轮次越多、检索结果越长，节省越明显，且不受 5 分钟有效期和跨请求前缀变化的影响。

**推荐：跨请求复用**：

场景

原因

多轮连续对话

从第二轮起可命中上一轮的完整历史前缀，对话越长收益越大

长 System Prompt / 大表结构场景

结构化知识库的表结构会拼进 system prompt，体积大且会话内稳定，是理想的缓存内容

同一份长文档 / 会话文件的反复追问

稳定前缀占比高，一次创建多次命中

对延迟敏感、要求命中确定性的业务

显式缓存是确定性命中，不受后端资源调度影响

成本盈亏判断：显式缓存首次写入多付 25%，之后每次命中省 90%，**只要发生至少一次命中，总成本就低于不用缓存**。

**不建议开启（开了也没收益，甚至更贵）**：

场景

原因

一次性单轮短问答

只创建、不命中，白付 25% 创建溢价

前缀不足 1024 Token

达不到最小缓存长度，不会产生缓存

请求间隔超过 5 分钟的低频调用

显式缓存 5 分钟过期，下次请求必然重新创建

多模态文档场景的跨请求复用

图片内容块参与前缀计算，跨请求容易因图片块变化而缓存失效；此类场景建议只指望单请求内的收益

每次会话都换知识库 / 换问答服务配置

前缀（含表结构、知识库信息）不同，无法复用

**说明**上述“不建议”仅指显式缓存收益不划算。由于默认模型 qwen3.6-plus 不支持隐式缓存，不开启 `enable_cache_control` 并不会退化成隐式缓存兜底，而是完全没有缓存。若这些场景仍希望有一定缓存收益，可评估后照常开启。

### 查看缓存命中

响应终结帧 `usage` 中的 `cached_tokens` 即本次请求命中缓存的输入 Token 数：

```
{
  "usage": {
    "input_tokens": 12345,
    "output_tokens": 678,
    "total_tokens": 13023,
    "cached_tokens": 9800
  }
}
```

-   `cached_tokens` 是本次请求内**多轮模型调用的累计值**；
-   会话首次请求 `cached_tokens` 必然为 0：首次只创建缓存，尚无可命中的内容，属预期行为；
-   从第二轮起应观察到 `cached_tokens` 大于 0，且随对话历史增长而增大。

### 注意事项

1.  **两种缓存互斥**：传了 `enable_cache_control: true` 即走显式缓存，不再走隐式缓存。默认模型 qwen3.6-plus 上不存在隐式缓存，不开启就是无缓存，而非“退化成隐式”。
2.  **首轮无命中是正常的**：任何缓存首次都需要先创建，`cached_tokens=0` 不代表功能异常。
3.  **显式缓存 5 分钟有效期**：每次命中会重置为 5 分钟；用户长时间不发问，下一次请求会重新创建缓存。
4.  **工具定义变化会导致缓存失效**：工具定义作为 system prompt 的一部分参与缓存计算。结构化知识库携带 `search_filters` 时会屏蔽 `execute_sql` 工具——同一会话中 filter 时有时无会改变工具列表，进而导致 system 前缀无法命中。建议同一会话内保持 `kb_search_configs` 稳定。
5.  **前缀必须逐字节稳定**：修改知识库绑定、变更问答服务配置（如自定义指令、会话文件开关）、平台侧调整模型，都会改变前缀，缓存需重新创建。
6.  **多模态场景跨请求命中不稳定**：带图片输入时图片内容块参与前缀计算，跨请求前缀容易不一致导致缓存失效；这类场景的收益主要来自单请求内的多轮检索，不应按跨请求命中来估算。
7.  **超长多轮存在回溯上限**：缓存匹配从断点向前回溯最多 20 个 content 块，单轮产生大量消息（多次工具调用 + 图片块）的极端情况下可能超出回溯范围而无法命中。
8.  **缓存按账号与模型隔离**：不同账号之间、同账号不同模型之间的缓存均不共享。
9.  **`input_tokens` ≠ 创建 + 命中**：后端会在提示词之后追加少量 Token（通常 10 以内），计入总输入但不计入缓存统计。

### 验证缓存效果

1.  在请求中加上 `enable_cache_control: true`，用一个会触发多轮检索的复杂问题跑一次，观察终结帧 `cached_tokens` 是否大于 0；
2.  再用同一会话连续追问 2-3 轮（间隔控制在 5 分钟内），观察 `cached_tokens` 是否随历史增长而增大，并对比首包延迟；
3.  与不传该参数的同样请求做 A/B 对比（默认模型下基线应为 `cached_tokens=0`），按「适用场景」的判据决定是否常态开启。

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

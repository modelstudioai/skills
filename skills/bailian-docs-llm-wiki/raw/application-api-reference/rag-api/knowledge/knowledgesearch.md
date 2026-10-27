# 知识检索

跨多个知识库执行联合语义检索，返回按相关性排序的切片。

## 接口说明

-   **权限要求**：调用本接口需提供阿里云百炼 API Key及业务空间。在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)及[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取。
-   **调用方式**：HTTP REST，`POST` + `application/json`。Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID。
-   **前置条件**：调用前须在百炼控制台 [知识检索服务页面](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list) 创建并发布[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)服务，获取服务 ID（`agent_id`）。检索策略（多库权重、知识路由、混排模型、混排模型模式等）预先在控制台配置进服务实例并发布，调用方只需传入检索意图（`query` / `images`）与 `agent_id`，还可通过 `kb_search_configs` 为每个知识库指定文档/标签过滤条件。未发布时返回 Agent 未发布错误。
-   **限流**：默认用户维度 25 QPS。如遇限流，请稍后重试。

## 请求语法

```
POST /api/v1/indices/knowledge/search HTTP/1.1
Host: {workspaceId}.cn-beijing.maas.aliyuncs.com
Authorization: Bearer <API-Key>
Content-Type: application/json
```

## 请求参数

调用方仅需传入检索意图、`agent_id` 与可选的 `kb_search_configs` 过滤条件，其余检索策略配置在 `agent_config`，不在请求中暴露。

名称

类型

必填

描述

示例

agent\_id

string

是

知识检索服务（agent）实例 ID。服务端据此加载已发布的 `agent_config`（含全部检索策略）。在控制台知识检索页面创建并发布后获取。

aid-xxxxxxxxxxxxxxxx

query

string

条件必填

文本检索意图。与 `images` 至少传入一个；纯图搜时可传空串；非纯图搜场景（未传 `images`）下必填，否则返回 `InvalidParameter`。

推荐一件适合秋冬的运动夹克

images

array<string>

条件必填

图片检索意图，元素为图片 URL（须公网可访问）。与 `query` 至少传入一个，可同时传入实现多模态检索。

\[\]

agent\_version

string

否

agent 版本。标准接口仅暴露 `agent_id` / `agent_version` / `query` / `images` / `kb_search_configs`，其余检索策略一律走 `agent_config`，不在请求中暴露。

kb\_search\_configs

array<object>

否

知识库过滤配置数组。每个元素对应一个知识库，可指定文档/标签过滤条件。`id` 必须属于 agent 已绑定的知识库，同一请求中不可重复。

kb\_search\_configs\[\].id

string

是

知识库 ID（pipeline\_id），必须属于 agent 已绑定的知识库。

kb\_product\_001

kb\_search\_configs\[\].search\_filters

array<object>

否

过滤条件数组，每个元素是一个 JSON 对象。支持按 doc\_id、tags、自定义 meta 字段过滤。在线传入的 search\_filters 会追加到离线配置的 search\_filters 末尾（AND 关系），而非替换。总字节数不超过 80,000。非结构化知识库仅允许 tags 和 meta 两种 key，数组长度不超过 1,000。

### kb\_search\_configs

通过 `kb_search_configs` 可在请求中为每个知识库指定文档/标签过滤条件，实现运行时动态过滤。该字段为数组，每个元素对应一个知识库。

**说明**

-   `kb_search_configs[].id` 必须是 agent 离线配置中已绑定的知识库 ID，不能查询未绑定的知识库。
-   同一请求中 `id` 不能重复。
-   每个 `kb_search_configs` 元素必须包含 `id` 字段。
-   `search_filters` 总字节数不超过 80,000 bytes。非结构化知识库仅允许 `tags` 和 `meta` 两种 key，数组长度不超过 1,000。
-   可过滤字段须在该知识库入卷时声明于 `index_config.fields`，否则过滤不生效。

search\_filters 语法详情

`search_filters` 是一个 JSON 数组，每个元素是一个独立的过滤条件对象。支持三种过滤维度，每种维度用独立的 JSON 对象传入：

```
"search_filters": [
  // 按文档 ID 过滤（支持多值 IN）
  { "doc_id": "file_abc_123" },
  { "doc_id": ["file_abc_123", "file_def_456"] },

  // 按标签过滤
  { "tags": ["合同", "2024年"] },

  // 按自定义 Meta 字段过滤
  { "custom_field": "value" },

  // 高级：操作符（gte / lte / like 等）
  { "price": { "gte": 100, "lte": 500 } },
  { "name": { "like": "张%" } },

  // 高级：嵌套 OR 分组
  {
    "_operator": "OR",
    "_conditions": [
      { "status": "active" },
      { "priority": { "gte": 5 } }
    ]
  }
]
```

**合并策略**：当 agent 离线配置中已有 `search_filters`，请求中传入的会追加到离线 filters 数组末尾，两者同时生效（AND 关系），而非替换。如果需要“只用在线条件”，离线配置中不要设置 search\_filters。

## 响应参数

响应顶层是统一的结构，`data` 里包含三部分：`total` 是命中的切片总数，`nodes` 是结果列表，`cost_time` 是本次检索耗时（毫秒）。建议以 `success` 字段判断成功与否，用 `request_id` 关联日志排查。

名称

类型

描述

code

string

业务状态码，`Success` 表示成功；失败时为对应错误码字符串。

status\_code

integer

语义状态码，成功为 200。

status

string

状态枚举，成功 `SUCCESS`，失败 `ERROR`。

success

boolean

是否成功。**调用方以此字段作为主判定。**

message

string

状态描述。

request\_id

string

请求唯一标识，排查问题时请提供此 ID。

data.total

integer

命中结果总数。

data.nodes

array<object>

检索结果节点列表，按相关性排序。结构见下表。

data.cost\_time

integer

本次检索耗时（毫秒）。

**data.nodes\[\] 结构**

名称

类型

描述

score

number

切片与查询的相关性分数，0 到 1 之间，越大越相关。

text

string

拼接好的切片文本，按 `字段名: 值` 逐行拼成，默认包含文档名、标题、正文。

metadata

object

切片元数据，字段因知识库类型而异，见下表。

**data.nodes\[\].metadata 字段**

字段

类型

说明

doc\_id

string

文档/数据行 ID。

doc\_name

string

文档名称。

title

string

切片标题。

hier\_title

string

层级标题，按 `>` 分隔。

content

string

切片正文。

image\_url

array<string>

切片包含的图片地址。

audio\_url

array<string>

切片包含的音频地址。

video\_url

array<string>

切片包含的视频地址。

\_knowledge\_type

string

知识类型，如 `document`、`image`。

\_knowledge\_scene

string

知识场景，如 `basic_document_qa`、`image_qa`。

pipeline\_id

string

所属知识库 ID。

workspace\_id

string

所属业务空间 ID。

\_id

string

切片 ID。

nid

string

文档解析 layout ID。

page\_number

array<integer>

切片所属页码列表。

doc\_url

string

原始文档 URL。

\_score

number

相关性分数。

\_rc\_v\_score

number

向量匹配分数。

\_rc\_t\_score

number

关键词匹配分数。

\_score\_with\_weight

number

加权相关性分数。

\_rank\_weight

number

排序权重。

is\_displayed\_chunk\_content

boolean

该切片内容是否用于展示。

**说明**以 `_` 开头的字段是内部打分用，版本间可能变，不要写进业务逻辑。表格型知识库还会额外返回用户表格里的业务字段（字段名因表结构而异，比如商品库可能返回 `product_id`、`product_name`、`category` 等），这些字段不在上表中。

## 错误码

失败时 `success` 为 `false`、`status` 为 `ERROR`、`status_code` 为对应语义码、`code` 为错误码字符串、`message` 为描述，`request_id` 必返回。**始终校验**`success`**，而非仅依赖 HTTP 状态码**；排查问题提供 `request_id`。

HTTP 状态码

错误码

说明

400

InvalidParameter

请求参数无效。多种参数错误都返回此码，仅凭错误码无法精准定位错误原因，请参照 `message` 字段，常见场景见下表。

401

InvalidApiKey

鉴权失败，API Key 无效或缺失。

**常见参数错误场景**

场景

错误码

错误信息

`agent_id` 缺失

`InvalidParameter`

`agent_id is required`

`query` 缺失

`InvalidParameter`

`query is required`

kb\_id 不属于 agent 绑定的知识库

`InvalidParameter`

`kb not bound to agent: {id}`

kb\_id 重复

`InvalidParameter`

`duplicate kb id in kb_search_configs: {id}`

kb\_id 为空

`InvalidParameter`

`kb_search_configs[{i}].id is required`

search\_filters 总字节数超限

`InvalidParameter`

`search_filters total bytes must less than 80000`

非结构化 filter 包含非法 key

`InvalidParameter`

`search_filters[{i}] contains invalid key '{key}'. Only 'tags' and 'meta' are allowed for unstructured data`

非结构化 tags/meta 数组超限

`InvalidParameter`

`search_filters[{i}].tags array size must not exceed 1000`

## 示例

以下示例查询「推荐一件适合秋冬的运动夹克」，`agent_id` 替换为已发布的知识检索服务 ID。

### cURL

```
curl -X POST "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-xxxxxxxxxxxxxxxx",
    "query": "推荐一件适合秋冬的运动夹克",
    "images": [],
    "kb_search_configs": [
      {
        "id": "kb_product_001",
        "search_filters": [
          {"tags": ["秋冬", "运动"]}
        ]
      }
    ]
  }'
```

### Python

```
import os
import requests

resp = requests.post(
    "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search",
    headers={
        "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
        "Content-Type": "application/json",
    },
    json={
        "agent_id": "aid-xxxxxxxxxxxxxxxx",
        "query": "推荐一件适合秋冬的运动夹克",
        "kb_search_configs": [
            {
                "id": "kb_product_001",
                "search_filters": [
                    {"tags": ["秋冬", "运动"]}
                ],
            }
        ],
    },
)
print(resp.json())
```

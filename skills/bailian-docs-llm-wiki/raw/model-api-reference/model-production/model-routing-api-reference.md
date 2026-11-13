# 智能路由 API 参考

本文介绍智能路由服务的 OpenAPI，包括查询路由模型版本、创建、列举、查询详情、编辑路由配置与删除智能路由服务。

**重要**智能路由 API 支持华北2（北京）与新加坡地域；仅支持后付费（`charge_type="post_paid"`）。智能路由的业务说明（路由策略、备选模型、调用方式与使用限制）请参见[智能路由](raw/model-user-guide/model-high-speed-inference/model-routing.md)。

## 前提条件

-   已阅读[智能路由](raw/model-user-guide/model-high-speed-inference/model-routing.md)，了解路由模型版本、路由策略与备选模型等概念。
-   已配置百炼的 API Key，请参考[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   请求域名因地域而异：北京地域使用 `dashscope.aliyuncs.com`，新加坡地域使用 `dashscope-intl.aliyuncs.com`；业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）各地域均可用。各地域完整域名信息请参见[各地域接入信息](https://help.aliyun.com/zh/model-studio/regions#h2_cc92e61c)。

## 接口概览

智能路由服务复用模型部署的 `/api/v1/deployments` 系列接口，请求中以 `plan="mr"` 区分部署类型：

功能

接口

获取模型路由版本列表

`GET /api/v1/deployments/model-routing/versions`

创建智能路由服务

`POST /api/v1/deployments`

列举智能路由服务

`GET /api/v1/deployments?plan=mr`

查询智能路由服务详情

`GET /api/v1/deployments/{deployed_model}`

编辑路由配置

`PUT /api/v1/deployments/{deployed_model}/update`

删除智能路由服务

`DELETE /api/v1/deployments/{deployed_model}`

## 获取模型路由版本列表

创建或编辑智能路由服务前，先通过本接口查询可选的路由模型版本，以及每个版本支持的策略与备选模型。无请求体，不传 `plan`。

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/model-routing/versions
```

### 请求示例

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/model-routing/versions?page_no=1&page_size=50" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1，须大于 0。

page\_size

Number

query

否

页大小，默认值为50，范围为 1-1000。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果（版本与候选模型仅为格式示例，实际以查询结果为准）：

```
{
    "request_id": "<request-id>",
    "output": {
        "total": 1,
        "page_no": 1,
        "page_size": 50,
        "total_page": 1,
        "route_model_versions": [
            {
                "route_model_version": "model-router-20260908",
                "supported_strategies": ["EFFECT_FIRST", "COST_FIRST"],
                "supported_candidate_model_ids": ["qwen3.8-flash", "qwen3.7-plus"],
                "offline_model_ids": []
            }
        ]
    }
}
```

**参数**

**类型**

**说明**

total

Long

可选路由版本总数。

total\_page

Number

总页数。

page\_no

Number

当前页码。

page\_size

Number

当前页大小。

route\_model\_versions

Array

当前页的路由版本列表。

route\_model\_versions\[\].route\_model\_version

String

路由版本标识，创建或编辑部署时提交。

route\_model\_versions\[\].supported\_strategies

Array

该版本支持的策略：`EFFECT_FIRST`（效果优先）、`COST_FIRST`（成本优先）。

route\_model\_versions\[\].supported\_candidate\_model\_ids

Array

该版本支持且未下线的备选模型 ID 集合。

route\_model\_versions\[\].offline\_model\_ids

Array

该版本已下线的模型 ID 集合，无下线模型时为空数组。

-   本接口不返回备选模型的推理权限信息：模型出现在 `supported_candidate_model_ids` 中不代表当前业务空间已获该模型的调用授权，无权限的模型会在调用时被路由服务实时过滤。
-   服务端先过滤可选版本再分页；查询页码超过总页数时返回空 `route_model_versions` 并保留总数，请按 `total_page` 翻页取全。

## 创建智能路由服务

```
POST https://dashscope.aliyuncs.com/api/v1/deployments
```

创建智能路由服务仅需服务名称与路由配置三字段（`routing_config` 必填，取值通过[获取模型路由版本列表](#h2-mr-versions)接口查询），不传 `model_name`：

### 请求示例

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my-router",
    "plan": "mr",
    "charge_type": "post_paid",
    "routing_config": {
        "route_model_version": "model-router-20260908",
        "strategy": "EFFECT_FIRST",
        "candidate_model_ids": ["qwen3.8-flash", "qwen3.7-plus"]
    }
}'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

name

String

body

是

服务名称：1-64 位，仅允许字母、数字和短横线。

plan

String

body

是

部署方案，创建智能路由固定传 `mr`。

charge\_type

String

body

否

付费方式，智能路由仅支持 `post_paid`（后付费，默认）。

routing\_config

Object

body

是

智能路由配置，包含以下字段。

routing\_config.route\_model\_version

String

body

是

路由模型版本，通过[获取模型路由版本列表](#h2-mr-versions)接口查询。

routing\_config.strategy

String

body

是

路由策略：`EFFECT_FIRST`（效果优先）、`COST_FIRST`（成本优先）。

routing\_config.candidate\_model\_ids

Array

body

是

备选模型 ID 列表，至少 1 个，须属于所选路由模型版本的支持范围；重复值合并，顺序无路由含义。

**说明**`plan` 为 `mr` 时不传 `model_name`，也不支持 `suffix`、`display_name`、`deploy_spec`、SKU、模板、容量、限流与思考/上下文等参数。备选模型已下线或元数据不可用时不可提交。

### 响应示例&参数

创建成功后部署即为 `RUNNING` 状态，`deployed_model` 为部署实例 ID（形如 `auto-model-Ab12Cd34`），客户端以该 `deployed_model` 作为 `model` 参数发起调用；`model_name` 为固定值 `auto-model`，不代表路由模型版本：

```
{
    "request_id": "<request-id>",
    "output": {
        "name": "my-router",
        "deployed_model": "auto-model-Ab12Cd34",
        "model_name": "auto-model",
        "status": "RUNNING",
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "creator": "16542902******",
        "modifier": "16542902******",
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T10:00:00",
        "plan": "mr",
        "routing_config": {
            "route_model_version": "model-router-20260908",
            "strategy": "EFFECT_FIRST",
            "candidate_model_ids": ["qwen3.8-flash", "qwen3.7-plus"]
        }
    }
}
```

**参数**

**类型**

**说明**

request\_id

String

本次请求的 ID。

name

String

服务名称。

deployed\_model

String

部署实例 ID（`auto-model-` 前缀加 8 位字符），调用时作为 `model` 参数传入。

model\_name

String

固定值 `auto-model`，不代表路由模型版本。

status

String

部署状态：`RUNNING`（运行中）、`UPDATING`（更新中）、`FAILED`（失败）、`DELETED`（已删除）。

workspace\_id

String

部署所属的业务空间 ID。

charge\_type

String

固定为 `post_paid`。

plan

String

固定为 `mr`。

creator

String

创建人 UID。

modifier

String

最后操作账号 UID。

gmt\_create

String

创建时间。

gmt\_modified

String

最后修改时间。

routing\_config

Object

当前路由配置，字段与请求参数相同。

## 列举智能路由服务

```
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

### 请求示例

传 `plan=mr` 只查询智能路由服务；不传时返回普通部署与智能路由的混合列表，`total` 与分页只统计查询命中的部分：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=10&plan=mr" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为10，范围为 1-100。

plan

String

query

否

只查询智能路由时传 `mr`；省略时返回混合列表。

### 响应示例&参数

`deployments` 数组内每个元素的字段与创建智能路由服务的响应参数一致。

```
{
    "request_id": "<request-id>",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 1,
        "deployments": [
            {
                "name": "my-router",
                "deployed_model": "auto-model-Ab12Cd34",
                "model_name": "auto-model",
                "status": "RUNNING",
                "workspace_id": "llm-8v53e*******",
                "charge_type": "post_paid",
                "creator": "16542902******",
                "modifier": "16542902******",
                "gmt_create": "2026-01-15T10:00:00",
                "gmt_modified": "2026-01-15T10:30:00",
                "plan": "mr",
                "routing_config": {
                    "route_model_version": "model-router-20260908",
                    "strategy": "EFFECT_FIRST",
                    "candidate_model_ids": ["qwen3.8-flash", "qwen3.7-plus"]
                }
            }
        ]
    }
}
```

## 查询智能路由服务详情

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### 请求示例

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/auto-model-Ab12Cd34" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署实例 ID，可通过创建智能路由服务或列举智能路由服务获取。

### 响应示例&参数

响应参数与创建智能路由服务一致，另在 `routing_config` 中额外返回 `offline_model_ids`（当前路由版本的已下线模型 ID 集合，仅详情接口返回）：

```
{
    "request_id": "<request-id>",
    "output": {
        "name": "my-router",
        "deployed_model": "auto-model-Ab12Cd34",
        "model_name": "auto-model",
        "status": "RUNNING",
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "creator": "16542902******",
        "modifier": "16542902******",
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T10:30:00",
        "plan": "mr",
        "routing_config": {
            "route_model_version": "model-router-20260908",
            "strategy": "EFFECT_FIRST",
            "candidate_model_ids": ["qwen3.8-flash", "qwen3.7-plus"],
            "offline_model_ids": []
        }
    }
}
```

## 编辑路由配置

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update
```

**说明**仅当服务状态为 `RUNNING` 时可调用，其他状态返回 OperationDenied 错误。`routing_config` 三个字段必填，为完整替换而非局部更新；切换 `route_model_version` 时版本与其路由由服务端原子切换，保存成功后详情与线上推理同步使用新版本，保存失败时原配置整体保持不变。

### 请求示例

```
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/auto-model-Ab12Cd34/update" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "routing_config": {
        "route_model_version": "model-router-20260908",
        "strategy": "COST_FIRST",
        "candidate_model_ids": ["qwen3.8-flash", "qwen3.7-plus"]
    }
}'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署实例 ID。

routing\_config

Object

body

是

完整替换后的路由配置，字段与创建智能路由服务相同：`route_model_version`、`strategy`、`candidate_model_ids`，三个字段全部必填。

本接口只编辑路由配置，不修改服务名称（智能路由暂不支持改名），不支持同时修改其他字段。更新成功后可重新查询详情确认配置。

### 响应示例&参数

响应为更新后的部署详情，参数与查询智能路由服务详情一致。

## 删除智能路由服务

```
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

智能路由服务可从 `RUNNING` 状态直接删除（删除响应中 `status` 为 `DELETED`），删除后列表与详情不再返回该资源，`deployed_model` 不复用，需重新创建。

### 请求示例

```
curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/auto-model-Ab12Cd34" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署实例 ID。

### 响应示例&参数

响应为删除前的部署详情（`status` 为 `DELETED`），参数与查询智能路由服务详情一致。

## 异常响应

```
{
    "request_id": "<request-id>",
    "code": "InvalidParameter",
    "message": "<message>"
}
```

### 响应参数

**参数**

**类型**

**说明**

request\_id

String

本次请求的系统生成 ID。

code

String

错误码，标识错误类型。

message

String

错误详情，用于问题排查，请勿依赖其文本做业务分支。

### 常见错误

**错误码**

**场景**

InvalidParameter

参数错误，如缺少必填字段、候选模型为空或不属于所选版本、服务名称非法。

AccessDenied

无权限或缺少有效用户身份。

NotFound

指定的部署不存在。

Conflict

服务名称重复或并发冲突。

QuotaLimit

配额限制。

OperationDenied

当前状态不允许操作，如非 RUNNING 状态编辑路由配置。

UnsupportedOperation

不支持的操作，如扩缩容、启停、限流配置等算力类操作。

InternalError

内部错误。

ResponseTimeout

响应超时。

# TPM 预留 DashScope OpenAPI 接口文档

TPM 预留 OpenAPI 用于创建、查询和管理 TPM 预留容量。每个 TPM 预留通过 ModelCode 标识，可包含多个容量实例；每个实例对应一次容量购买，可分别扩缩容、续订或释放。

## 认证与调用准备

使用调用地域的百炼 API Key，在请求头中传入 `Authorization: Bearer <api-key>`。API Key 与地域绑定，不可跨地域使用。请求体为 JSON 时传入 `Content-Type: application/json`。

工作空间专属域名格式为 `https://{workspaceId}.{region}.maas.aliyuncs.com`，使用目标工作空间及地域的 Endpoint。如需指定子业务空间，请求头携带 `X-DashScope-WorkSpace: <workspace-id>`。

DashScope API 域名为 `https://dashscope.aliyuncs.com`。弗吉尼亚地域使用 `https://{workspaceId}.us-east-1.maas.aliyuncs.com`。

异步容量操作的结果通过 [查询容量操作](#operation-query) 获取。

控制台入口参见[TPM 预留](raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)，部署概念参见[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)，通用部署 API 参见[使用 API 进行模型部署](raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 公共约定

接口基础路径为 `/api/v1/deployments`，沿用调用地域的 DashScope OpenAPI 域名和鉴权方式。请求体使用 `Content-Type: application/json`。使用目标地域的账号、模型和部署。

-   `deployed_model`：TPM 预留的调用标识（ModelCode）；实例/操作响应中的 `model_service_id` 表示同一对象。
-   `instance_id`：容量实例 ID。使用接口返回值，不根据字符串格式推断付费方式。
-   `operation_id`：操作 ID，使用接口返回的字符串值。
-   下文示例 ID、模型名、容量值均为占位示例。真实模型、最小值、步长、上限及购买时长以目标地域的模型和购买限制为准。
-   JSON 示例省略部分可选响应字段；示例中的阶段状态不是每次请求的固定返回。

成功响应统一包装为：

```
{
  "request_id": "example-request",
  "output": {}
}
```

请求错误示例：

```
{
  "request_id": "example-request",
  "code": "CAPACITY_INSTANCE_REQUIRED",
  "message": "需要指定容量实例"
}
```

**重要**HTTP 请求成功不等于容量操作成功。实例写接口即使返回 HTTP 200，`output.operation_status` 也可能为 `FAILED`。必须检查操作状态和错误字段，确认成功后再使用更新的容量。

## 创建 TPM 预留

`POST /api/v1/deployments`

创建 TPM 预留并购买首个容量实例，返回用于调用模型的 ModelCode。如需为已有 TPM 预留增加容量，请调用 [叠加购买容量实例](#instance-create)。

**字段**

**类型**

**必填**

**说明**

`model_name`

String

是

基础模型名称

`plan`

String

是

`ptu`

`service_tier`

String

否

性能档位：`ptu_fast` 为高速（默认），`ptu_default` 为标速

`charge_type`

String

是

`pre_paid`（预付费）/ `post_paid`（后付费）

`name`

String

否

展示名称；未传时自动生成。

`suffix`

String

否

ModelCode 后缀；未传时自动生成。

`ptu_capacity`

Object

是

容量配置，见 [容量参数](#capacity-fields)

`pre_paid_info`

Object

条件必填

预付费必填，见 [预付费参数](#prepaid-fields)；后付费不传

`ptu_default` 支持预付费；`ptu_fast` 支持预付费和后付费。新增容量实例沿用 ModelCode 的性能档位。

```
{
  "model_name": "<base_model>",
  "plan": "ptu",
  "service_tier": "ptu_fast",
  "charge_type": "pre_paid",
  "name": "TPM预留示例",
  "ptu_capacity": {
    "input_tpm": 10000,
    "output_tpm": 1000
  },
  "pre_paid_info": {
    "duration": 30,
    "auto_renewal": false
  }
}
```

### ptu\_capacity

容量单位为 kTPM（1 kTPM = 1000 Tokens/分钟）。当前支持的模型不支持单独配置思考输出配额。

**字段**

**类型**

**说明**

`input_tpm`

Long

输入容量，单位 kTPM，按模型要求提供并满足步长及范围

`output_tpm`

Long

输出容量，单位 kTPM，按模型要求提供并满足步长及范围

扩缩容时表示所选实例变更后的绝对容量，不是增加量，也不是 ModelCode 的目标总容量。

### pre\_paid\_info

**字段**

**类型**

**说明**

`duration`

Integer

购买 / 续订时长，单位天，必须大于 0

`auto_renewal`

Boolean

显式指定是否自动续费

`auto_renewal_duration`

Integer

自动续费开启时必填且大于 0，单位天

`auto_renewal_cycle`

String

可选续费周期单位，按产品支持的值传入，例如 `Day` 表示天

### 创建响应

`output` 为部署对象（[查询 TPM 预留](#h2-sec-query)）。创建容量实例时可返回 `operation_id`、`instance_id`；预付费实例的购买订单尚未处理完成时，`instance_id` 可能暂缺，后续查询获取。

```
{
  "request_id": "example-request",
  "output": {
    "deployed_model": "example-model-code",
    "model_name": "<base_model>",
    "plan": "ptu",
    "status": "WAIT_PRE_PAID_BILLING_TO_DEPLOYING",
    "operation_id": "100001"
  }
}
```

有 `operation_id` 时按 [查询容量操作](#operation-query) 查询；创建请求超时应先确认是否已经创建，避免重复创建 ModelCode。

## 扩缩容

`PUT /api/v1/deployments/{deployed_model}/scale`

调整指定 TPM 预留下某个容量实例的输入和输出容量。存在多个未删除实例时，必须通过 `instance_id` 指定目标实例。

**字段**

**必填**

**说明**

`instance_id`

条件必填

多个未删除实例时必须传；仅一个未删除实例时可省略

`ptu_capacity`

是

该实例变更后的绝对容量

`pre_paid_info`

否

预付费未传时复用已保存的信息；后付费不传

`order_type`

否

`UPGRADE` 为升配，`DOWNGRADE` 为降配；省略时由服务端判定，传入值须与容量变化方向一致

```
{
  "instance_id": "example-capacity-instance",
  "ptu_capacity": {
    "input_tpm": 20000,
    "output_tpm": 2000
  },
  "order_type": "UPGRADE"
}
```

`output` 返回 TPM 预留信息，相应容量操作的 ID 通过 `operation_id` 返回。多实例未指定 ID 返回 `CAPACITY_INSTANCE_REQUIRED`。新接入推荐 [扩缩容指定容量实例](#instance-scale)。

预付费变更涉及订单，后付费不走预付费变配订单。变更确认前继续保留原生效容量，失败时不能把目标容量展示为已生效。全零扩缩容不等价于删除实例。

## 查询 TPM 预留

`GET /api/v1/deployments/{deployed_model}`

查询指定 TPM 预留的配置、状态，以及所有容量实例已生效的汇总容量。

```
{
  "request_id": "example-request",
  "output": {
    "deployed_model": "example-model-code",
    "model_name": "<base_model>",
    "plan": "ptu",
    "ptu_service_tier": "ptu_fast",
    "status": "RUNNING",
    "charge_type": "pre_paid",
    "ptu_capacity": {
      "input_tpm": 10000,
      "output_tpm": 1000
    },
    "overflow_strategy": "disable"
  }
}
```

**字段**

**说明**

`deployed_model`

TPM 预留的调用标识（ModelCode）。

`model_name`

基础模型名称。

`plan`

类型标识，TPM 预留为 `ptu`。

`status`

ModelCode 状态，不代表每个容量实例的状态

`ptu_service_tier`

性能档位：`ptu_fast` 为高速，`ptu_default` 为标速

`ptu_capacity`

该 ModelCode 下所有容量实例已生效的输入、输出汇总容量

`charge_type`

取值：`pre_paid`（预付费）/ `post_paid`（后付费）

`pre_paid_info`

预付费购买及续订配置。存在多个容量实例时，请通过实例详情查询目标实例的 `pre_paid_info`。

`pre_paid_instance_id`

预付费实例标识。存在多个容量实例时，请通过容量实例列表获取各实例的 `instance_id`，并指定要操作的实例。

`pre_paid_gmt_expired`

预付费到期时间。存在多个容量实例时，请通过目标实例详情的 `gmt_expired` 获取其到期时间。

`overflow_strategy`

溢出策略，`enable` 表示允许溢出按量计费，`disable` 表示超出容量时限流。

`fail_reason`

失败原因。

`gmt_create`

创建时间。

`gmt_modified`

最后修改时间。

`operation_id`

容量操作 ID，用于查询操作结果；相应写操作响应中可能返回。

`instance_id`

容量实例 ID。购买订单尚未处理完成时可能暂不返回；请通过后续查询获取。

混合付费应通过容量实例列表中各实例的 `charge_type` 判断。部署状态和计费类型不能代替每个实例的状态和计费类型。

## 查询 TPM 预留列表

`GET /api/v1/deployments?page_no=1&page_size=10&plan=ptu`

分页查询 TPM 预留列表。

**Query 参数**

**说明**

`page_no`

页码，默认 1

`page_size`

每页数量，默认 10，范围 \[1,100\]

`plan`

可选类型筛选。查询 TPM 预留时传 `ptu`；性能档位由 `service_tier` 表示，不作为 `plan` 的取值

```
{
  "request_id": "example-request",
  "output": {
    "deployments": [
      {
        "deployed_model": "example-model-code",
        "plan": "ptu",
        "status": "RUNNING",
        "ptu_capacity": {
          "input_tpm": 10000,
          "output_tpm": 1000
        }
      }
    ],
    "total": 1,
    "page_no": 1,
    "page_size": 10
  }
}
```

部署列表不支持通过 `status` 参数筛选状态。容量实例筛选请使用 [查询容量实例列表（含已删除实例）](#instance-list) 的 `statuses`。

## 续订

`PUT /api/v1/deployments/{deployed_model}/renew`

为指定的预付费容量实例续订，可同时调整容量。存在多个未删除实例时，必须通过 `instance_id` 指定目标实例。

**字段**

**必填**

**说明**

`instance_id`

条件必填

多个未删除实例时必须指定；单实例兼容省略

`pre_paid_info`

是

续订信息，见 [预付费参数](#prepaid-fields)

`is_change`

否

默认 `false`；是否同时调整容量

`ptu_capacity`

否

省略则保留配置容量；传入不同容量时必须 `is_change=true`

续订并开启自动续费：

```
{
  "instance_id": "example-capacity-instance",
  "pre_paid_info": {
    "duration": 30,
    "auto_renewal": true,
    "auto_renewal_duration": 30
  }
}
```

续订但不开启自动续费：

```
{
  "instance_id": "example-capacity-instance",
  "pre_paid_info": {
    "duration": 30,
    "auto_renewal": false
  }
}
```

仅支持预付费；续订请求不能传 `order_type`。`output` 返回 TPM 预留信息，并可能包含容量操作 ID；推荐使用 [续订指定容量实例](#instance-renew) 的实例级接口并轮询结果。

## 修改溢出策略

`PUT /api/v1/deployments/{deployed_model}/update-overflowstrategy`

```
{
  "overflow_strategy": "disable"
}
```

`overflow_strategy` 必填，仅支持小写 `enable` / `disable`。`enable` 表示超出 PTU 容量的流量允许溢出公共池按量计费；`disable` 表示超出后限流。配置作用于整个 ModelCode，容量包不单独配置溢出策略。

响应包含 `request_id` 和 `output`。修改后可通过 [查询 TPM 预留](#h2-sec-query) 获取 `overflow_strategy`，确认配置已更新。

```
{
  "request_id": "example-request",
  "output": {
    "deployed_model": "example-model-code",
    "model_name": "<base_model>",
    "plan": "ptu_v2",
    "ptu_service_tier": "ptu_fast",
    "status": "RUNNING",
    "charge_type": "post_paid",
    "overflow_strategy": "disable",
    "ptu_capacity": {
      "input_tpm_quota": 10000,
      "output_tpm_quota": 10000
    }
  }
}
```

**警告**开启溢出策略后，超出容量的流量按量计费，会产生额外费用。关闭后，超出容量的请求会被限流。更多说明参见[预置吞吐长输入与缓存](raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 容量实例接口

以下接口均以 `/api/v1/deployments/{deployed_model}` 为前缀。实例写操作返回 [容量操作](#operation-fields) 的操作对象，与旧 `/scale`、`/renew` 的部署对象不同。

### 叠加购买容量实例

`POST /api/v1/deployments/{deployed_model}/capacity-instances`

**字段**

**必填**

**说明**

`billing_method`

是

付费方式：`PRE_PAY` 为预付费，`POST_PAY` 为后付费。取值区分大小写

`ptu_capacity`

是

新实例容量

`pre_paid_info`

条件必填

预付费必填，后付费不传

预付费示例：

```
{
  "billing_method": "PRE_PAY",
  "ptu_capacity": {
    "input_tpm": 10000,
    "output_tpm": 1000
  },
  "pre_paid_info": {
    "duration": 30,
    "auto_renewal": false
  }
}
```

后付费示例：

```
{
  "billing_method": "POST_PAY",
  "ptu_capacity": {
    "input_tpm": 10000,
    "output_tpm": 1000
  }
}
```

返回操作对象，初次响应可能已成功、失败或仍在处理中。沿用现有 ModelCode、模型和性能档位；同一 ModelCode 只允许一个未删除的后付费实例。购买条件或实例数量不满足要求时，请根据接口返回的错误处理。

### 查询容量实例列表（含已删除实例）

`GET /api/v1/deployments/{deployed_model}/capacity-instances?page_no=1&page_size=20&include_deleted=true`

**Query 参数**

**类型**

**说明**

`page_no`

Integer

默认 1

`page_size`

Integer

默认 20，范围 \[1,100\]

`include_deleted`

Boolean

默认 true；只展示未删除实例时显式传 false

`statuses`

String 列表

可选，多值逗号分隔，例如 `RUNNING,STOPPED`

`charge_types`

String 列表

可选，`pre_paid,post_paid`

```
{
  "request_id": "example-request",
  "output": {
    "records": [
      {
        "model_service_id": "example-model-code",
        "instance_id": "example-capacity-instance",
        "charge_type": "post_paid",
        "status": "STOPPED",
        "deleted": true,
        "effective_capacity": {
          "input_tpm": 0,
          "output_tpm": 0
        },
        "configured_capacity": {
          "input_tpm": 0,
          "output_tpm": 0
        },
        "can_scale": false,
        "can_renew": false,
        "can_delete": false
      }
    ],
    "items": 1,
    "page": 1,
    "itemsPerPage": 20,
    "pageCount": 1
  }
}
```

分页结构与部署列表不同：`records` 是当前页，`items` 是总数，`page` 是页码，`itemsPerPage` / `pageCount` 保留当前返回的驼峰拼写。优先排列有生效容量的实例，再按创建时间倒序。列表仅支持本节列出的查询参数。

### 查询容量实例详情

`GET /api/v1/deployments/{deployed_model}/capacity-instances/{instance_id}`

返回 [容量实例](#instance-fields) 的实例对象，已删除实例也可查询。ModelCode 与实例须匹配，不能跨 ModelCode 操作实例。

**说明**后付费实例释放后，在同一 ModelCode 下重新购买后付费容量会复用原实例 ID。列表和详情更新为重新购买后的实例信息，不再单独保留原删除记录。释放后的 `configured_capacity` 可能为零，不保证保留释放前的配置容量。

### 扩缩容指定容量实例

`PUT /api/v1/deployments/{deployed_model}/capacity-instances/{instance_id}/scale`

```
{
  "ptu_capacity": {
    "input_tpm": 20000,
    "output_tpm": 2000
  },
  "order_type": "UPGRADE"
}
```

参数语义同 [扩缩容](#h2-sec-scale)，实例 ID 由路径确定，请求体无需重复。返回操作对象。调用前读取 `can_scale`；预付费到期挂起的实例不能直接扩缩容，应先续订。

### 续订指定容量实例

`PUT /api/v1/deployments/{deployed_model}/capacity-instances/{instance_id}/renew`

普通续订：

```
{
  "pre_paid_info": {
    "duration": 30,
    "auto_renewal": false
  }
}
```

续订并调整容量：

```
{
  "pre_paid_info": {
    "duration": 30,
    "auto_renewal": false
  },
  "is_change": true,
  "ptu_capacity": {
    "input_tpm": 20000,
    "output_tpm": 2000
  }
}
```

参数约束同 [续订](#h2-sec-renew)，不传 `order_type`。仅预付费可续订，先检查 `can_renew`；返回操作对象。

### 删除 / 释放容量实例

`DELETE /api/v1/deployments/{deployed_model}/capacity-instances/{instance_id}`

可选 Query 参数 `reason` 为删除原因，按 URL 编码；无需 JSON 请求体。返回操作对象。

-   后付费：按删除流程释放，完成后 `deleted=true`、`status=STOPPED`，生效容量为零。
-   已生效的预付费：不能用本接口代替退订，直接调用返回 `PREPAID_UNSUBSCRIBE_REQUIRED`。完成退订并释放容量后，最终同样返回 `deleted=true`、`status=STOPPED`。
-   `can_delete=true` 表示当前状态允许进入删除 / 退订流程，不表示预付费可跳过退订直接 DELETE。对于尚无关联订单的失败实例，请根据接口返回结果处理。

退订释放为异步操作。同一 ModelCode 正在处理其他操作时，已受理的释放操作会排队等待，完成前查询可能仍返回原状态和生效容量。退订已受理不代表容量已释放，请通过操作结果及实例 `deleted` 字段确认完成。

### 查询容量操作

`GET /api/v1/deployments/{deployed_model}/capacity-operations/{operation_id}`

```
{
  "request_id": "example-poll-request",
  "output": {
    "operation_id": "100001",
    "request_id": "example-original-request",
    "operation_type": "SCALE",
    "operation_status": "SUCCEEDED",
    "model_service_id": "example-model-code",
    "instance_id": "example-capacity-instance",
    "from_status": "RUNNING",
    "current_status": "RUNNING"
  }
}
```

外层 `request_id` 是本次查询请求标识，操作对象内的 `request_id` 是原始操作标识，两者可能不同。查询路径必须属于创建该操作的 ModelCode。

使用写操作实际返回的 `operation_id`，不要自行构造。查询不存在的数字 ID 或其他 ModelCode 的操作时，返回 HTTP 404、`CAPACITY_OPERATION_NOT_FOUND`；传入包含字母等非数字字符的无效 ID 时，可能返回 HTTP 500、`InternalError`。遇到此错误先核对 ID，不要直接重复发起容量写操作。

## 删除 TPM 预留

`DELETE /api/v1/deployments/{deployed_model}`

需先释放全部容量实例，且 ModelCode 为 `STOPPED`、不存在正在执行或排队的容量操作，再删除整个部署。返回部署对象。

最后一个实例释放后，ModelCode 变为 `STOPPED`，不会因此自动删除 ModelCode。删除容量实例与删除 ModelCode 是两个不同操作。

## 响应对象及状态

### 容量实例（CapacityInstance）

**字段**

**类型**

**说明**

`model_service_id`

String

容量实例或操作所属的 ModelCode。

`instance_id`

String

容量实例 ID。

`charge_type`

String

`pre_paid`（预付费）/ `post_paid`（后付费）

`status`

String

实例生命周期状态，见下表

`deleted`

Boolean

是否已删除 / 释放，用于识别已释放的实例

`effective_capacity`

Object

当前已确认提供服务的容量

`configured_capacity`

Object

实例配置 / 合同容量；停止、挂起时仍可保留

`target_capacity`

Object

正在变更的目标容量，稳定状态可能不返回或为空

`pre_paid_info`

Object

该实例的预付费购买及续订配置，见 [预付费参数](#prepaid-fields)。

`gmt_expired`

String

预付费实例到期时间。

`can_scale`

Boolean

当前是否允许对实例扩缩容。

`can_renew`

Boolean

当前是否允许续订实例。

`can_delete`

Boolean

当前是否允许删除或退订实例；预付费实例仍需完成退订流程。

`fail_reason`

String

失败原因

`gmt_created`

时间

创建时间。

`gmt_modified`

时间

最后修改时间。

`gmt_deleted`

时间

删除时间。

**状态**

**含义及展示建议**

`WAIT_PRE_PAID_BILLING_TO_DEPLOYING` / `WAIT_TO_DEPLOY`

等待购买处理 / 等待生效

`RUNNING`

运行中

`WAIT_PRE_PAID_BILLING_TO_SCALING` / `SCALING`

等待变配订单 / 变配中

`STOPPING` / `STOPPED`

停止中 / 已停止；结合 `deleted` 区分已释放

`SUSPENDING` / `SUSPENDED`

挂起中 / 已挂起

`STARTING` / `RECOVERING`

启动中 / 恢复中

`DELETING`

删除中

`FAILED`

失败，结合失败原因处理

后付费删除与预付费退订可统一展示为“已释放”：条件为 `deleted=true`，而不是仅 `status=STOPPED`。`STOPPED + deleted=false` 仍是保留的实例。`deleted=true` 的实例不允许扩缩容、续订、删除。

`RUNNING` 状态不代表所有操作均可用。同一 ModelCode 有进行中操作或存在计费限制时，相应操作可能不可用。预付费 `SUSPENDED` 实例不可扩缩容，符合续订条件时可续订；后付费实例不可续订。调用前重新查询实例详情，通过 `can_scale`、`can_renew`、`can_delete` 检查操作是否可用，并处理接口返回的错误。

### 容量操作（CapacityOperation）

**字段**

**说明**

`operation_id`

容量操作 ID，用于查询操作结果；相应写操作响应中可能返回。

`request_id`

发起该容量操作的请求标识。

`operation_type`

常见 `CREATE`、`SCALE`、`RENEW`、`DELETE`；生命周期处理也可能出现 `STOP`、`REFUND`，不意味着存在同名公开写接口

`operation_status`

取值：`PROCESSING`、`SUCCEEDED`、`FAILED`

`model_service_id`

容量实例或操作所属的 ModelCode。

`instance_id`

容量实例 ID。购买订单尚未处理完成时可能暂不返回；请通过后续查询获取。

`from_status`

操作前的实例状态。

`current_status`

实例当前状态。

`error_code`

操作失败时的错误码。

`error_message`

操作失败时的错误说明。

`gmt_created`

创建时间。

`gmt_finished`

操作完成时间。

操作正在执行或排队等待时，均返回 `PROCESSING`。`SUCCEEDED` / `FAILED` 为终态，收到终态后停止轮询，并刷新实例和部署汇总。

## 异步调用、幂等与错误处理

### 推荐调用顺序

1.  查询实例详情，读取能力开关及最新配置。
2.  发起一次购买 / 扩缩容 / 续订 / 删除请求，保存 `operation_id`。
3.  若返回 `PROCESSING`，定期查询操作并逐步退避；若已终态，直接处理结果。
4.  `SUCCEEDED` 后刷新实例及 ModelCode；`FAILED` 展示 `error_code` / `error_message`。网络超时不等同于操作失败，先查已有操作。

同一 ModelCode 的容量变更按顺序处理；有进行中操作时，新变更可能被拒绝。已受理的退订释放会排队，在前序操作完成后继续。变更生效前，查询仍返回原生效容量，不应将目标容量视为已生效。

叠加、扩缩容或释放生效后，可通过部署查询接口获取更新后的汇总生效容量，继续使用原 ModelCode。调用模型还需完成对应模型部署，并使用正确的账号鉴权和调用参数；容量操作成功不代表模型调用的其他条件均已满足。

### 重试与请求标识

对同一个容量写操作的网络重试，保持请求标识与参数不变。建议将 `x-acs-req-uuid` 与 `X-DashScope-RequestId` 设置为同一个 UUID，避免两者不一致导致实际标识变化。当前读取优先级为 `x-acs-req-uuid`、`X-DashScope-RequestId`、`X-Request-Id`，均未提供时生成新标识。

相同 ModelCode、相同有效请求标识、相同操作参数的容量操作复用已有操作；同一标识换参数会返回 `IDEMPOTENCY_KEY_CONFLICT`。新业务操作使用新标识。不要将这一实例操作幂等约定直接套用于首次创建 ModelCode。

### 错误码

**错误码**

**HTTP**

**处理建议**

`CAPACITY_INSTANCE_REQUIRED`

400

多实例时指定目标 `instance_id`

`CAPACITY_INSTANCE_OPERATION_UNSUPPORTED`

400

刷新详情与能力开关，确认当前状态及付费方式支持操作

`PREPAID_UNSUBSCRIBE_REQUIRED`

400

转入已有退订流程

`POSTPAID_INSTANCE_ALREADY_EXISTS`

400

复用已有后付费实例，或先释放后再创建

`CAPACITY_SLOT_LIMIT_EXCEEDED` / `TOTAL_CAPACITY_INSTANCE_LIMIT_EXCEEDED`

400

已达到有效实例槽位 / 含历史记录的总数量限制

`MODEL_CODE_DELETED`

400

不再对已删除 TPM 预留发起写操作

`MODEL_CODE_NOT_FOUND` / `CAPACITY_INSTANCE_NOT_FOUND`

404

检查地域、账号、ModelCode 与实例归属；对已删除实例执行扩缩容也可返回 CAPACITY\_INSTANCE\_NOT\_FOUND

`CAPACITY_OPERATION_NOT_FOUND`

404

操作不存在或不属于指定 ModelCode，核对写操作返回的 ID

`InternalError`

500

操作查询传入无效的非数字 ID 时可能返回；先核对 ID，其他内部错误保留 request\_id 联系技术支持

`CAPACITY_INSTANCE_OPERATION_CONFLICT`

409

先查询已有操作，完成后再发起新操作

`IDEMPOTENCY_KEY_CONFLICT`

409

重试保持原参数；不同业务操作使用新标识

`BILLING_ACCOUNT_NOT_READY`

403

检查账号是否满足购买条件

`BILLING_SERVICE_UNAVAILABLE`

503

查询已有操作，按退避策略处理重试

表中 HTTP 对应请求阶段抛出的错误；异步操作失败通过操作对象的错误字段返回，不能只按 HTTP 状态判断。

其他通用错误：

**HTTP 状态码**

**错误码**

**处理建议**

400

`InvalidParameter`

核对参数名、类型、容量变化方向与取值。

401

`InvalidApiKey`

检查 API Key 的有效性和地域。

403

`AccessDenied` / `Model.AccessDenied` / `App.AccessDenied`

检查账号权限、工作空间和模型授权。

404

`ModelNotFound`

核对基础模型名称及支持范围。

409

`Conflict`

部署重名，更换名称或 suffix。

429

`Throttling` / `Throttling.RateQuota` / `Throttling.AllocationQuota`

TPM 超额对应 AllocationQuota，可扩容或调整溢出策略。

500

`RequestTimeOut`

先检查已有操作，避免重复购买；保留 request\_id 联系技术支持。

503

`ModelUnavailable`

稍后重试或切换可用模型。

限流处理参见[限流应对最佳实践](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

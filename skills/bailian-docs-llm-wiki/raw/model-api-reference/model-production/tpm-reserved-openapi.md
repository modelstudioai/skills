# TPM 预留 DashScope OpenAPI 接口文档

## 接口概述

TPM 预留 DashScope OpenAPI 提供六个 REST 接口，覆盖 TPM 预留部署的创建、查询、扩缩容、续订与溢出策略全生命周期管理。通过 `plan=ptu` 标识 TPM 预留场景，结合 `service_tier` 区分部署类型。

-   **POST /api/v1/deployments** — 创建 TPM 预留部署
-   **GET /api/v1/deployments/{deployed\_model}** — 查询单个部署状态与配置
-   **GET /api/v1/deployments** — 分页列表查询
-   **PUT /api/v1/deployments/{deployed\_model}/scale** — 扩缩容
-   **PUT /api/v1/deployments/{deployed\_model}/renew** — 续订预付费部署
-   **PUT /api/v1/deployments/{deployed\_model}/updateOverflowStrategy** — 修改溢出策略

`service_tier` 取值：`ptu_default` 对应 TPM 预留（容量保障）场景，`ptu_fast` 对应 PTU v2 通用部署场景。创建 TPM 预留部署时传 `service_tier=ptu_default`。

`deployed_model` 为部署服务 ID，格式为 `{model_name}-ptu-{随机后缀}`，由后端自动生成，用作路径参数。

`ptu_capacity` 容量单位为 kTPM（1 kTPM = 1000 Tokens/分钟），包含 `input_tpm`、`output_tpm`、`thinking_output_tpm` 三个独立维度。起跑和步长因模型而异，以控制台创建页展示为准。

-   华北2（北京）支持的模型：千问3.8-Max、千问3.7-Max-2026-05-20、千问3.7-Plus-2026-05-26、千问3.6-Flash-2026-04-16、GLM-5.2、GLM-5.1、DeepSeek-v4-Flash、DeepSeek-v4-Pro、Kimi-K2.6
-   新加坡区域无 Kimi-K2.6，其余模型一致
-   上述 9 款模型均支持思考输出配额（`thinking_output_tpm`），思考模型家族与启用方式详见[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)

认证方式、请求头与 endpoint 域名配置详见[认证与调用准备](https://help.aliyun.com/zh/model-studio/tpm-reserved-openapi#h2-sec-auth)。控制台操作入口与 TPM 预留概念详见[TPM 预留](raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)，通用部署创建 API 详见[使用 API 进行模型部署](raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 认证与调用准备

调用 TPM 预留 OpenAPI 使用百炼 API Key 认证，请求头携带 `Authorization: Bearer <api-key>`。API Key 与区域绑定，不可跨区调用。

请求头

必填

说明

类型

`Authorization: Bearer <api-key>`

必填

百炼 API Key

Bearer Token

`Content-Type: application/json`

必填

请求体类型

固定值 application/json

`X-DashScope-SSE: enable`

流式必填

开启流式输出

枚举值 enable

`X-DashScope-Async: enable`

异步必填

异步批处理

枚举值 enable

`X-DashScope-WorkSpace: <id>`

可选

子业务空间 ID

工作空间 ID 字符串

-   **DashScope 原生 SDK**：当前支持 Python 与 Java
-   **OpenAI 兼容 SDK**：当前支持 Python、Node.js、Java、Go，调用路径前缀为 `/compatible-mode/v1`

如需指定子业务空间，请求头携带 `X-DashScope-WorkSpace: <workspace-id>`。workspace-dedicated 域名格式为 `[workspaceId].[region].maas.aliyuncs.com`，区域包括 cn-beijing、ap-southeast-1、ap-northeast-1、eu-central-1。模型部署简介与三种计费方式对比详见[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

项目

域名

DashScope API 域名

`[https://dashscope.aliyuncs.com](https://dashscope.aliyuncs.com)`

弗吉尼亚区域

`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`

OpenAI 兼容路径前缀

`/compatible-mode/v1`

## 创建 TPM 预留部署

调用 `POST /api/v1/deployments` 创建 TPM 预留部署。请求体须指定基础模型、计费类型与 TPM 容量配置，创建后状态为 `DEPLOYING`，部署完成后变为 `RUNNING`。

字段

类型

必填

说明

`model_name`

String

必填

基础模型名，如 `qwen-max`

`plan`

String

必填

固定传 `ptu`

`service_tier`

String

可选

`ptu_default`（TPM 预留）/ `ptu_fast`（PTU v2 通用，默认）

`charge_type`

String

必填

`pre_paid`（预付费）/ `post_paid`（后付费）

`name`

String

可选

部署展示名，不传则自动生成

`suffix`

String

可选

TPM 预留创建不传，后端自动生成

`ptu_capacity`

Object

必填

TPM 容量配置，详见下表

`pre_paid_info`

Object

条件必填

`charge_type=pre_paid` 时必填

字段

类型

必填

说明

`input_tpm`

Integer

必填

输入 TPM 配额（每分钟输入 Token 数），须为模型 step 整数倍

`output_tpm`

Integer

必填

输出 TPM 配额（每分钟输出 Token 数），须为模型 step 整数倍

`thinking_output_tpm`

Integer

可选

思考输出 TPM 配额，仅思考模型，须为模型 step 整数倍

字段

类型

必填

说明

`duration`

Integer

必填

购买时长（天），取值 1~30、60、90、120、365

`auto_renewal`

Boolean

必填

是否自动续费

`auto_renewal_duration`

Integer

条件必填

`auto_renewal=true` 时必填，续费时长（天）

TPM 预留创建不传 `suffix`，后端自动生成部署服务 ID（deployed\_model）。

创建后状态流转：`DEPLOYING` → `RUNNING`。

```
{
  "model_name": "qwen-max",
  "plan": "ptu",
  "service_tier": "ptu_default",
  "charge_type": "pre_paid",
  "name": "通义千问-Max TPM预留",
  "ptu_capacity": {
    "input_tpm": 100000,
    "output_tpm": 50000,
    "thinking_output_tpm": 20000
  },
  "pre_paid_info": {
    "auto_renewal": true,
    "duration": 30,
    "auto_renewal_duration": 30
  }
}
```
```
{
  "request_id": "xxx",
  "output": {
    "deployed_model": "qwen-max-ptu-a1b2c3d4",
    "model_name": "qwen-max",
    "plan": "ptu",
    "status": "DEPLOYING",
    "ptu_capacity": {
      "input_tpm": 100000,
      "output_tpm": 50000,
      "thinking_output_tpm": 20000
    }
  }
}
```

## 查询部署

TPM 预留 OpenAPI 提供单个查询与列表查询两种方式，分别用于查看指定部署详情和分页浏览全部部署。

#### 查询单个部署

调用 `GET /api/v1/deployments/{deployed_model}` 查询指定部署的状态与配置。路径参数 `deployed_model` 为部署服务 ID。

字段

类型

说明

`deployed_model`

String

部署服务 ID

`model_name`

String

基础模型名

`plan`

String

部署计划，TPM 预留为 `ptu`

`service_tier`

String

服务层级

`status`

String

部署状态

`charge_type`

String

计费类型

`ptu_capacity`

Object

TPM 容量配置

`gmt_created`

String

创建时间

`gmt_modified`

String

修改时间

```
{
  "request_id": "xxx",
  "output": {
    "deployed_model": "qwen-max-ptu-a1b2c3d4",
    "model_name": "qwen-max",
    "plan": "ptu",
    "service_tier": "ptu_default",
    "status": "RUNNING",
    "charge_type": "pre_paid",
    "ptu_capacity": {
      "input_tpm": 100000,
      "output_tpm": 50000
    },
    "gmt_created": "2024-01-01T00:00:00Z",
    "gmt_modified": "2024-01-01T12:00:00Z"
  }
}
```

#### 列表查询

调用 `GET /api/v1/deployments` 分页查询部署列表，支持 `page_no` 与 `page_size` 分页参数。

参数

类型

必填

说明

`page_no`

Integer

可选

页码，默认 1

`page_size`

Integer

可选

每页条数，取值范围 \[1,100\]，默认 10

```
{
  "request_id": "xxx",
  "output": {
    "deployments": [
      {
        "deployed_model": "qwen-max-ptu-a1b2c3d4",
        "model_name": "qwen-max",
        "plan": "ptu",
        "status": "RUNNING",
        "ptu_capacity": { "input_tpm": 100000, "output_tpm": 50000 }
      }
    ],
    "total": 1,
    "page_no": 1,
    "page_size": 10
  }
}
```

## 扩缩容

调用 `PUT /api/v1/deployments/{deployed_model}/scale` 对 TPM 预留部署执行扩缩容，请求体传入新的 `ptu_capacity` 配置。

字段

类型

必填

说明

`ptu_capacity`

Object

必填

新的 TPM 容量配置（结构同创建 `ptu_capacity`）

```
{
  "ptu_capacity": {
    "input_tpm": 200000,
    "output_tpm": 100000
  }
}
```
```
{
  "request_id": "xxx",
  "output": {
    "deployed_model": "qwen-max-ptu-a1b2c3d4",
    "model_name": "qwen-max",
    "plan": "ptu",
    "status": "SCALING",
    "ptu_capacity": {
      "input_tpm": 200000,
      "output_tpm": 100000
    }
  }
}
```

预付费扩缩容触发商业化下单（UPGRADE/DOWNGRADE），异步完成后状态变为 `RUNNING`。后付费扩缩容直接生效，不触发下单。

**重要**预付费扩缩容为异步操作，调用接口返回 `SCALING` 状态后需等待商业化下单完成，状态自动变为 `RUNNING`。请勿在 `SCALING` 状态期间重复发起扩缩容。

扩缩容方向约束：`input_tpm`、`output_tpm`、`thinking_output_tpm` 须同增或同减，混合方向会报错。

仅 `plan=ptu`（内部 ptu\_v2）的部署支持扩缩容操作。

## 续订

调用 `PUT /api/v1/deployments/{deployed_model}/renew` 续订预付费 TPM 预留部署，请求体传入 `pre_paid_info` 续费信息。

字段

类型

必填

说明

`pre_paid_info`

Object

必填

续费信息（结构同创建 `pre_paid_info`）

```
{
  "pre_paid_info": {
    "auto_renewal": true,
    "duration": 30,
    "auto_renewal_duration": 30
  }
}
```
```
{
  "pre_paid_info": {
    "auto_renewal": false,
    "duration": 1
  }
}
```
```
{
  "request_id": "xxx",
  "output": {
    "deployed_model": "qwen-max-ptu-a1b2c3d4",
    "model_name": "qwen-max",
    "plan": "ptu",
    "status": "WAIT_PRE_PAID_BILLING_TO_SCALING",
    "charge_type": "pre_paid",
    "ptu_capacity": { "input_tpm": 100000, "output_tpm": 50000 }
  }
}
```

`duration` 取值范围为 1~30、60、90、120、365 天，TPM 预留付费周期固定按天计费。

续费生效时间：22 点后提交的续订请求，到期时间顺延至 N+2 天 00:00。

续订后状态为 `WAIT_PRE_PAID_BILLING_TO_SCALING`，表示等待预付费账单处理完成。

## 修改溢出策略

调用 `PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy` 修改 TPM 预留部署的溢出策略。请求体传入 `overflow_strategy` 字段。

字段

类型

必填

说明

`overflow_strategy`

String

必填

`enable`（超出 PTU 容量流量溢出公共池按量计费）/ `disable`（超出直接限流）

```
{
  "overflow_strategy": "disable"
}
```
```
{
  "request_id": "xxx",
  "output": {
    "deployed_model": "qwen-max-ptu-a1b2c3d4",
    "model_name": "qwen-max",
    "plan": "ptu",
    "status": "RUNNING",
    "overflow_strategy": "disable",
    "ptu_capacity": { "input_tpm": 100000, "output_tpm": 50000 }
  }
}
```

该接口为后端独立 API，前端控制台无封装。开发者通过 OpenAPI 直接调用，溢出策略可随时切换无需重建部署。溢出策略概念详见[预置吞吐长输入与缓存](raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

**重要**`overflow_strategy=enable` 时，超出 PTU 容量的流量会溢出到公共池按量计费，产生额外费用。`disable` 时超出直接限流，不产生额外费用但影响服务可用性。

## 错误码

调用 TPM 预留 OpenAPI 时如遇错误，响应体返回 `request_id`、`code`、`message` 三个字段，可根据错误码定位问题。

HTTP 状态码

错误名

说明

解决方案

400

`InvalidParameter`

参数非法

按本篇参数表核对参数名、类型与取值后重试

401

`InvalidApiKey`

API Key 无效

检查 API Key 有效性与区域绑定，必要时重新获取 Key

403

`AccessDenied` / `Model.AccessDenied` / `App.AccessDenied`

无权限

确认账号有 TPM 预留权限，检查工作空间与模型授权

404

`ModelNotFound`

模型不存在

确认 model\_name 在支持清单内且拼写正确

409

`Conflict`

部署重名

更换部署名或 suffix 避免重名后重试

429

`Throttling` / `Throttling.RateQuota` / `Throttling.AllocationQuota`

限流（TPM 超额走 `AllocationQuota`）

扩容 ptu\_capacity 或调整 overflow\_strategy，详见下方限流应对

500

`InternalError` / `RequestTimeOut`

内部错误

记录 request\_id 提工单，稍后重试

503

`ModelUnavailable`

模型不可用

稍后重试或切换可用模型

```
{
  "request_id": "xxx",
  "code": "Throttling.AllocationQuota",
  "message": "..."
}
```

429 限流错误中，TPM 容量超额走 `AllocationQuota` 错误码。限流应对最佳实践详见[限流应对最佳实践](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 常见问题

service\_tier 的 ptu\_default 与 ptu\_fast 有什么区别？

二者不是「默认/快速」版本关系，而是不同部署场景。`ptu_default` 对应 TPM 预留（容量保障），`ptu_fast` 对应 PTU v2 通用部署。

auto\_renewal\_cycle 字段是否存在？

官方 API 无 `auto_renewal_cycle` 字段。实际续费字段为 `duration`（购买时长）、`auto_renewal`（是否自动续费）、`auto_renewal_duration`（`auto_renewal=true` 时必填的续费时长）。

thinking\_output\_tpm 适用于哪些模型？

`thinking_output_tpm` 仅适用于思考模型。TPM 预留支持的 9 款模型均支持思考输出配额。

创建传 plan=ptu，续费传 plan=ptu\_v2，是否接口错误？

不是接口错误。创建请求 `plan=ptu` 与续费请求 `plan=ptu_v2` 的差异是前后端命名约定，后端均映射到 ptu\_v2 内部处理。

deployed\_model 后缀是否固定 8 位？

TPM 预留创建不传 `suffix`，由后端自动生成部署服务 ID，后缀长度由后端决定，不固定为 8 位。

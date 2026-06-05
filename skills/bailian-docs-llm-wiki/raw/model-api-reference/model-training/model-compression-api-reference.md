# 模型压缩 API 参考

模型压缩 API 提供从查询模板、创建任务、轮询状态、获取日志到取消/删除任务的完整 RESTful 接口。本文档面向开发者通过 OpenAPI 或 SDK 集成压缩能力。控制台介绍见 [模型压缩](https://help.aliyun.com/zh/model-studio/model-compression-introduction)。

## 一、前提条件

在调用本文档接口前，请先完成：

1.  已开通阿里云百炼服务并完成实名认证。
    
2.  当前工作空间至少有一个基于 `qwen3.5-flash-2026-02-23` 的**自定义全参微调模型**（通过 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/) 完成 ）。当前压缩功能仅支持该模型，LoRA 模型和已量化的模型不支持。
    
3.  已获取 API Key（参考 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
    

> 压缩产出的模型支持的部署单元规格由所选量化模板决定，部署数量在百炼控制台「模型部署」中配置。当前压缩功能限时免费。

## 二、接口列表

所有接口域名：`https://dashscope.aliyuncs.com`

#

方法

路径

说明

1

GET

`/api/v1/fine-tunes/compress/templates`

列举可量化模型及配置模板

2

POST

`/api/v1/fine-tunes/compress/jobs`

创建压缩任务

3

GET

`/api/v1/fine-tunes/compress/jobs`

列举压缩任务

4

GET

`/api/v1/fine-tunes/compress/jobs/{job_id}`

查询压缩任务详情

5

GET

`/api/v1/fine-tunes/compress/jobs/{job_id}/logs`

获取压缩任务日志

6

POST

`/api/v1/fine-tunes/compress/jobs/{job_id}/cancel`

取消压缩任务

7

DELETE

`/api/v1/fine-tunes/compress/jobs/{job_id}`

删除压缩任务

## 三、鉴权

所有接口通过 HTTP Header 携带 API Key：

```
Authorization: Bearer ${YOUR_API_KEY}
```

`Content-Type: application/json` 适用于 POST 请求体场景。

## 四、5 分钟上手

### HTTP

安装请求库：

```
pip install requests
```

创建任务 → 轮询 → 拿到产出模型的完整示例：

```
import requests, time

API_KEY = "YOUR_API_KEY"
BASE = "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 1. 创建压缩任务
resp = requests.post(f"{BASE}/jobs", headers=HEADERS, json={
    "model": "qwen3.5-flash-2026-02-23-ft-***",  # 自定义微调模型 ID
    "template_id": "quant-flash-nvfp4-mlp-nomtp",          # 通过 GET /templates 获取
    "output_model_suffix": "test",                          # 最多 8 字符，仅小写字母和数字
}).json()
job_id = resp["output"]["job_id"]
print("Job:", job_id)

# 2. 轮询直到终态
status = resp["output"]["status"]
while status not in ("SUCCEEDED", "FAILED", "CANCELED"):
    time.sleep(30)
    resp = requests.get(f"{BASE}/jobs/{job_id}", headers=HEADERS).json()
    status = resp["output"]["status"]
    print("Status:", status)

# 3. 处理结果
if status == "SUCCEEDED":
    print("Quantized model:", resp["output"]["quantized_output"])
    # 用 quantized_output 调模型部署接口部署
elif status == "FAILED":
    print("Error:", resp["output"]["error"])
```

列举任务与获取日志：

```
# 列举所有压缩成功的任务
resp = requests.get(f"{BASE}/jobs", headers=HEADERS, params={"status": "SUCCEEDED", "page_size": 20}).json()
for j in resp["output"]["jobs"]:
    print(j["job_id"], j["template_name"], j["quantized_output"])

# 获取任务日志
resp = requests.get(f"{BASE}/jobs/{job_id}/logs", headers=HEADERS, params={"offset": 0, "line": 100}).json()
for line in resp["output"]["logs"]:
    print(line)
```

**产出模型的命名规则**：

```
quantized_output = {base_model}-{output_model_suffix}-{job_id}
```

例如 `base_model` 为 `qwen3.5-flash-2026-02-23`，`suffix` 为 `test`，`job_id` 为 `quant-202604111200-a1b2`，产出模型 ID 为：

```
qwen3.5-flash-2026-02-23-test-quant-202604111200-a1b2
```

## 五、接口详情

### 5.1 列举可量化模型及配置模板

列出当前用户所有可量化的自定义微调模型，及每个模型对应的压缩模板。模板绑定在模型上，不同模型架构 × 精度 × 目标 MU 规格的组合对应不同模板。

> 仅返回当前用户基于基础模型做 SFT/DPO/CPT 全参微调的自定义模型。LoRA 微调模型和已量化模型不会出现在结果中。

**地址**

```
GET /api/v1/fine-tunes/compress/templates
```

**请求参数**

参数

类型

必选

默认

说明

model

String

否

\-

按模型 ID 过滤；传基础模型名时返回基于该基础模型的所有自定义模型

lang

String

否

zh-CN

响应语言：`zh-CN` / `en-US`（详见[多语言支持](#367xsho2f69fk)）

**请求示例**

```
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/templates" \
  -H "Authorization: Bearer ${API_KEY}"
```

**响应示例（最小）**

```
{
  "request_id": "uuid-string",
  "output": {
    "base_models": ["qwen3.5-flash-2026-02-23"],
    "custom_models": [
      {
        "model": "qwen3.5-flash-2026-02-23-ft-***",
        "model_name": "我的SFT微调模型",
        "base_model": "qwen3.5-flash-2026-02-23",
        "templates": [
          {
            "template_id": "quant-flash-nvfp4-mlp-nomtp",
            "template_name": "W4A4 NVFP4高性能压缩-MU5/MU8/MU9",
            "description": "在更低比特压缩下兼顾高精度与高性能，进一步降低显存占用并提升推理吞吐。",
            "compress_type": "quantization",
            "hyper_parameters": []
          }
        ]
      }
    ]
  }
}
```

**响应示例（完整：含可调超参）**

```
{
  "request_id": "uuid-string",
  "output": {
    "base_models": ["qwen3.5-flash-2026-02-23"],
    "custom_models": [
      {
        "model": "qwen3.5-flash-2026-02-23-ft-***",
        "model_name": "我的SFT微调模型",
        "base_model": "qwen3.5-flash-2026-02-23",
        "templates": [
          {
            "template_id": "quant-flash-nvfp4-mlp-nomtp",
            "template_name": "W4A4 NVFP4高性能压缩-MU5/MU8/MU9",
            "description": "在更低比特压缩下兼顾高精度与高性能，进一步降低显存占用并提升推理吞吐。",
            "compress_type": "quantization",
            "hyper_parameters": [
              {
                "name": "calib_input",
                "type": "string",
                "display_name": "校准输入",
                "description": "是否启用校准输入",
                "support_values": ["true"],
                "defaultValue": "true",
                "recommend_value": "true",
                "required": false
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**响应参数**

字段

类型

说明

base\_models

Array<String>

支持压缩的基础模型名称列表

custom\_models\[\].model

String

模型 ID

custom\_models\[\].model\_name

String

模型展示名称

custom\_models\[\].base\_model

String

基础模型名称

custom\_models\[\].templates

Array

该模型支持的压缩配置模板列表，继承其基础模型的模板

templates\[\].template\_id

String

模板 ID，创建任务时引用

templates\[\].template\_name

String

模板名称（支持多语言，根据 `lang` 参数返回对应语言版本）

templates\[\].description

String

模板描述（支持多语言，根据 `lang` 参数返回对应语言版本）

templates\[\].compress\_type

String

压缩类型，固定为 `quantization`

templates\[\].hyper\_parameters

Array

可调超参数；空数组表示无可调超参

hyper\_parameters\[\].name

String

参数名（创建任务时作为 Key 使用）

hyper\_parameters\[\].type

String

类型：`number`（数值型，配合 `data_range`/`step`）/ `string`（枚举型，配合 `support_values`）

hyper\_parameters\[\].display\_name

String

参数展示名称（支持多语言，根据 `lang` 参数返回对应语言版本）

hyper\_parameters\[\].description

String

参数描述（支持多语言，根据 `lang` 参数返回对应语言版本）

hyper\_parameters\[\].defaultValue

String

默认值

hyper\_parameters\[\].recommend\_value

String

推荐值

hyper\_parameters\[\].required

Boolean

是否必传

hyper\_parameters\[\].support\_values

Array<String>

枚举值列表（仅 `type=string` 时存在），如 `["instruct", "think", "hybrid"]`

hyper\_parameters\[\].data\_range

Array<String>

数值范围（仅 `type=number` 时存在），如 `["64","256"]` 表示取值范围 64~256

hyper\_parameters\[\].step

Integer

步长（仅 `type=number` 时存在）

hyper\_parameters\[\].advancedParameter

Boolean

是否为高级参数。高级参数通常使用默认值即可

hyper\_parameters\[\].is\_advanced\_parameter

Boolean

同 `advancedParameter`

### 5.2 创建压缩任务

**地址**

```
POST /api/v1/fine-tunes/compress/jobs
```

**请求参数**

参数

类型

必选

默认

说明

model

String

是

\-

源模型 ID

template\_id

String

是

\-

压缩模板 ID

job\_name

String

否

自动生成

任务名称，同一用户下不允许重复；最多 50 字符

job\_description

String

否

\-

任务描述；最多 200 字符

hyper\_parameters

Object

否

模板默认值

超参覆盖（Key-Value），只传想覆盖的项

custom\_calibration\_file\_ids

Array<String>

否

\-

自定义校准数据集文件 ID 列表（数据集组 ID，格式 `file-{32hex}`）；仅当 `calib_input=true` 时生效。数据集需先在**数据管理**中创建并发布

output\_model\_suffix

String

否

\-

量化产出模型名后缀；最多 8 字符，仅小写字母和数字。输出模型名格式：`{base_model}-{suffix}-{job_id}`

**请求示例**

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "qwen3.5-flash 压缩任务",
    "model": "qwen3.5-flash-2026-02-23-ft-***",
    "template_id": "quant-flash-nvfp4-mlp-nomtp",
    "custom_calibration_file_ids": ["file-***"],
    "output_model_suffix": "test"
  }'
```

**响应示例**

```
{
  "request_id": "uuid-string",
  "output": {
    "job_id": "quant-202604111200-a1b2",
    "job_name": "qwen3.5-flash 压缩任务",
    "status": "PENDING",
    "model": "qwen3.5-flash-2026-02-23-ft-***",
    "base_model": "qwen3.5-flash-2026-02-23",
    "template_id": "quant-flash-nvfp4-mlp-nomtp",
    "template_name": "W4A4 NVFP4高性能压缩-MU5/MU8/MU9",
    "training_type": "quantization",
    "compress_type": "quantization",
    "hyper_parameters": {},
    "custom_calibration_file_ids": ["file-***"],
    "quantized_output": null,
    "create_time": "2026-04-11 12:00:00",
    "start_time": null,
    "end_time": null,
    "error": null,
    "group": "quantization"
  }
}
```

**响应参数**：字段含义同[查询压缩任务](#oqir0ms3o8ncu)。

### 5.3 查询压缩任务

**地址**

```
GET /api/v1/fine-tunes/compress/jobs/{job_id}
```

**请求示例**

```
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs/quant-202604111200-a1b2" \
  -H "Authorization: Bearer ${API_KEY}"
```

**响应示例**

```
{
  "request_id": "uuid-string",
  "output": {
    "job_id": "quant-202604111200-a1b2",
    "job_name": "qwen3.5-flash 压缩任务",
    "job_description": "...",
    "status": "SUCCEEDED",
    "model": "qwen3.5-flash-2026-02-23-ft-***",
    "base_model": "qwen3.5-flash-2026-02-23",
    "template_id": "quant-flash-nvfp4-mlp-nomtp",
    "template_name": "W4A4 NVFP4高性能压缩-MU5/MU8/MU9",
    "template_description": "在更低比特压缩下兼顾高精度与高性能，进一步降低显存占用并提升推理吞吐。",
    "training_type": "quantization",
    "compress_type": "quantization",
    "hyper_parameters": {},
    "custom_calibration_file_ids": ["file-***"],
    "quantized_output": "qwen3.5-flash-2026-02-23-test-quant-202604111200-a1b2",
    "create_time": "2026-04-11 12:00:00",
    "start_time": "2026-04-11 12:02:30",
    "end_time": "2026-04-11 13:02:30",
    "error": null,
    "group": "quantization",
    "usage": 3600
  }
}
```

**响应参数**

字段

类型

说明

job\_id

String

任务 ID

job\_name

String

任务名称

job\_description

String

任务描述

status

String

任务状态（详见[任务状态](#ce70h1gm8p3uh)）

model

String

源模型 ID

base\_model

String

基础模型 ID

template\_id

String

使用的压缩模板 ID

template\_name

String

模板名称

template\_description

String

模板描述

training\_type

String

任务类型，固定为 `quantization`

compress\_type

String

压缩类型，同 `training_type`，固定为 `quantization`

hyper\_parameters

Object

实际生效的超参（仅返回用户可见参数）

custom\_calibration\_file\_ids

Array<String>

自定义校准数据集文件 ID 列表

quantized\_output

String

量化后产出的模型 ID（仅 SUCCEEDED 时有值）

create\_time

String

任务创建时间

start\_time

String

任务开始执行时间（PENDING/QUEUING 时为 null）

end\_time

String

任务完成时间（终态时有值）

error

Object

失败时的错误信息，含 `code` 和 `message`；成功时为 null

group

String

任务分组，固定为 `quantization`

usage

Integer

GPU 时长（秒），SUCCEEDED 或 CANCELED 时出现

### 5.4 列举压缩任务

支持按状态、模型、模板、量化规格、算法、时间范围、任务名/ID 等过滤，支持创建时间排序和分页。

**地址**

```
GET /api/v1/fine-tunes/compress/jobs
```

**请求参数**

参数

类型

必选

默认

说明

status

String

否

\-

按状态过滤（如 RUNNING、SUCCEEDED）

model

String

否

\-

按源模型 ID 过滤

template\_id

String

否

\-

按模板 ID 过滤

quant\_spec

String

否

\-

按量化规格过滤（如 `w4a16`、`w8a8`）

quant\_method

String

否

\-

按量化算法过滤（如 `gptq`、`awq`、`fp8`）

start\_time

String

否

\-

任务开始时间不早于该值。格式：`yyyy-MM-dd HH:mm:ss` / ISO-8601 / `yyyy-MM-dd`

end\_time

String

否

\-

任务结束时间不晚于该值，格式同 `start_time`

job\_name

String

否

\-

按任务名称模糊匹配

job\_id

String

否

\-

按任务 ID 模糊匹配

search\_key

String

否

\-

搜索关键字。不传 `select_key` 时同时模糊匹配 `job_id` 和 `job_name`；配合 `select_key` 时仅匹配指定字段

select\_key

String

否

\-

`search_key` 的搜索字段，可选 `job_id` / `job_name`

sort\_by

String

否

create\_time

排序字段，目前仅支持 `create_time`

sort\_order

String

否

desc

排序方向，`asc` 升序 / `desc` 降序

page\_no

Integer

否

1

页码

page\_size

Integer

否

10

每页数量，最大 100

**请求示例**

```
# 综合搜索：按状态 + 算法 + 分页
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs?status=SUCCEEDED&quant_method=gptq&page_size=10" \
  -H "Authorization: Bearer ${API_KEY}"

# 时间范围 + 按任务名搜索 + 创建时间升序
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs?start_time=2026-04-01&end_time=2026-04-30&search_key=qwen3&select_key=job_name&sort_by=create_time&sort_order=asc" \
  -H "Authorization: Bearer ${API_KEY}"
```

**响应示例**

```
{
  "request_id": "uuid-string",
  "output": {
    "total": 42,
    "page_no": 1,
    "page_size": 10,
    "jobs": [
      {
        "job_id": "quant-202604111200-a1b2",
        "job_name": "qwen3.5-flash 压缩任务",
        "status": "SUCCEEDED",
        "model": "qwen3.5-flash-2026-02-23-ft-***",
        "base_model": "qwen3.5-flash-2026-02-23",
        "template_id": "quant-flash-nvfp4-mlp-nomtp",
        "template_name": "W4A4 NVFP4高性能压缩-MU5/MU8/MU9",
        "training_type": "quantization",
        "compress_type": "quantization",
        "custom_calibration_file_ids": ["file-***"],
        "quantized_output": "qwen3.5-flash-2026-02-23-test-quant-202604111200-a1b2",
        "create_time": "2026-04-11 12:00:00",
        "start_time": "2026-04-11 12:02:30",
        "end_time": "2026-04-11 13:02:30",
        "group": "quantization",
        "usage": 3600
      }
    ]
  }
}
```

**响应参数**

字段

类型

说明

total

Integer

符合条件的任务总数

page\_no

Integer

当前页码

page\_size

Integer

每页数量

jobs

Array

任务列表，字段含义同[查询压缩任务](#oqir0ms3o8ncu)

### 5.5 获取压缩任务日志

**地址**

```
GET /api/v1/fine-tunes/compress/jobs/{job_id}/logs
```

**请求参数**

参数

类型

必选

默认

说明

offset

Integer

否

0

忽略前 N 行，从第 N+1 行开始读取

line

Integer

否

100

读取行数，上限 1000

**请求示例**

```
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs/quant-202604111200-a1b2/logs?offset=0&line=50" \
  -H "Authorization: Bearer ${API_KEY}"
```

**响应示例**

```
{
  "request_id": "uuid-string",
  "output": {
    "total": 15,
    "logs": [
      "2026-04-11 12:02:35 - INFO - Starting quantization...",
      "2026-04-11 12:30:00 - INFO - Quantization progress: 100%",
      "2026-04-11 12:35:00 - INFO - Quantization succeeded!"
    ]
  }
}
```

**日志展示规则**

-   任务传入自定义校准数据集时，日志中包含数据处理完成标记 `data process succeeded, start to quantization`
    
-   日志接口已过滤系统内部标记，仅返回用户可读的压缩进度信息
    

### 5.6 取消压缩任务

仅允许取消 `PENDING`、`QUEUING` 或 `RUNNING` 状态的任务。取消为异步操作，任务会先进入 `CANCELING` 过渡态，最终转为 `CANCELED`。

**地址**

```
POST /api/v1/fine-tunes/compress/jobs/{job_id}/cancel
```

**请求示例**

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs/quant-202604111200-a1b2/cancel" \
  -H "Authorization: Bearer ${API_KEY}"
```

**响应示例**

```
{
  "request_id": "uuid-string",
  "output": { "status": "success" }
}
```

### 5.7 删除压缩任务

仅允许删除终态（`SUCCEEDED` / `FAILED` / `CANCELED`）的任务。删除任务记录**不会**删除已产出的量化模型（`quantized_output`）。

**地址**

```
DELETE /api/v1/fine-tunes/compress/jobs/{job_id}
```

**请求示例**

```
curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/jobs/quant-202604111200-a1b2" \
  -H "Authorization: Bearer ${API_KEY}"
```

**响应示例**

```
{
  "request_id": "uuid-string",
  "output": { "status": "success" }
}
```

## 六、任务状态

状态

说明

`PENDING`

任务已创建，等待调度

`QUEUING`

已进入调度队列，等待 GPU 资源

`RUNNING`

任务执行中

`CANCELING`

已发起取消，等待终止

`SUCCEEDED`

任务成功，`quantized_output` 字段返回产出模型 ID

`FAILED`

任务失败，`error.code` / `error.message` 字段返回原因

`CANCELED`

任务已取消

**状态流转**：

```
PENDING ─→ QUEUING ─→ RUNNING ─→ SUCCEEDED
   │          │          ├────→ FAILED
   └──────────┴──────────┘
              ↓
          CANCELING ─→ CANCELED
```

## 七、错误码

### 7.1 通用错误码

错误码

HTTP

说明

`InvalidParameter`

400

请求参数不合法

`MissingParameter`

400

缺少必选参数

`Unauthorized`

401

认证失败

`Forbidden`

403

无权限访问

`ResourceNotFound`

404

资源不存在

`UnsupportedOperation`

400

资源状态不允许该操作（如取消已终态任务）

`QuotaExceeded`

429

配额超限

`InternalError`

500

服务内部错误

### 7.2 业务错误码

以下业务错误码按场景分类列出。`对外 Code` 为接口实际返回的 `code` 字段值。

**参数校验类**

对外 Code

HTTP

说明

`InvalidParameter`

400

缺少必选参数 `model`

`InvalidParameter`

400

缺少必选参数 `template_id`

`InvalidParameter`

400

不支持对基础模型直接量化

`InvalidParameter`

400

指定的配置模板不存在

`InvalidParameter`

400

当前模型不支持该压缩模板

`InvalidParameter`

400

模型不支持量化

`InvalidParameter`

400

LoRA 微调模型不支持量化

`InvalidParameter`

400

模型数据不可用

`InvalidParameter`

400

任务名称包含不支持的字符

`InvalidParameter`

400

`output_model_suffix` 超过 8 字符

`InvalidParameter`

400

源模型尚未就绪

`AccessDenied`

403

无权使用该压缩模板

**超参数校验类**

对外 Code

HTTP

说明

`InvalidParameter`

400

必选超参数未传

`InvalidParameter`

400

传入了未知超参数

`InvalidParameter`

400

超参数值不在枚举值列表中

`InvalidParameter`

400

超参数值超出数值范围

`InvalidParameter`

400

超参数值不是合法数字

**任务查询类**

对外 Code

HTTP

说明

`NotFound`

404

指定的压缩任务不存在

`InvalidParameter`

400

缺少必选参数 `job_id`

**分页与时间参数类**

对外 Code

HTTP

说明

`InvalidParameter`

400

页码参数不合法（须 ≥ 1）

`InvalidParameter`

400

每页数量不合法（须 1~100）

`InvalidParameter`

400

时间格式不合法

### 7.3 错误响应示例

```
{
  "request_id": "uuid-string",
  "code": "InvalidParameter",
  "message": "The specified model 'xxx-lora-yyy' is a LoRA model and not supported for quantization."
}
```

## 八、多语言支持

所有接口支持通过参数切换响应中的多语言字段（模板名称、描述、超参展示名、错误消息等）。

**支持语言**：`zh-CN`（中文，默认）、`en-US`（英文）。不支持的语言自动回退到 `zh-CN`。

**优先级**（高 → 低）：

优先级

方式

示例

1

URL 查询参数 `lang`

`GET /templates?lang=en-US`

2

HTTP Header `Accept-Language`

`-H "Accept-Language: en-US"`

3

默认

`zh-CN`

**影响字段**

字段

说明

`templates[].template_name`

模板名称

`templates[].description`

模板描述

`hyper_parameters[].display_name`

超参展示名

`hyper_parameters[].description`

超参描述

错误响应 `message`

错误提示消息

**示例**

```
# 通过 URL 参数
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/templates?lang=en-US" \
  -H "Authorization: Bearer ${API_KEY}"

# 通过 Header
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress/templates" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Accept-Language: en-US"
```

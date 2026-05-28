# 异步任务管理 API

阿里云百炼的部分模型（如图像生成、视频生成等）因处理时间较长，采用异步调用机制，通常需要调用两个接口完成操作：先创建任务获取 ID，再通过该 ID 查询结果。为了方便管理异步任务，阿里云百炼提供了一组通用的异步任务接口，支持查询单个任务结果、批量查询多个任务状态、以及取消正在排队且尚未处理的任务。

## **前提条件**

异步任务API通过HTTP进行调用。

在调用前，您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## **查询异步任务结果接口**

**API描述**：根据`任务ID（task_id）`查询任务状态和任务结果。

**流量限制**：20 QPS，即每秒每个账号（含主账号及其子账号）最多发起 20 次请求。

**重要**

-   支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务），但无法查询其他主账号提交的任务。
    
-   异步任务在完成后通常保留 24 小时 （具体以对应任务的 API 文档为准），超时后系统将自动清理历史任务数据。
    

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

#### **入参描述**

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Header

Authorization

String

是

API-Key，例如：Bearer sk-xxx

Bearer sk-xxx

Path

task\_id

String

是

需查询的任务ID

a8532587-xxxx-xxxx-xxxx-0c46b17950d1

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

String

本次请求的系统唯一码

7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51

output

Object

-   任务成功时，`output` 包含模型生成的结果对象，具体内容因任务类型而异
    
-   任务失败或部分失败时，`output` 会返回对应的 `code` 和 `message`，说明失败原因
    
-   对于包含多个子任务的任务，`output` 可能同时包含成功的子任务结果和失败的错误信息
    

\-

output.task\_id

String

查询任务的 task\_id

a8532587-xxxx-xxxx-xxxx-0c46b17950d1

output.task\_status

String

任务状态

-   对于包含多个子任务的任务，只要有一个子任务成功，整个任务会被标记为成功
    
-   对于失败的子任务，会在 output 中展示具体报错
    

任务状态：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   UNKNOWN：任务不存在或状态未知
    

output.submit\_time

String

任务提交时间

2023-12-20 21:36:31.896

output.scheduled\_time

String

任务调度时间，即开始执行时间

2023-12-20 21:36:39.009

output.end\_time

String

任务结束时间

2023-12-20 21:36:45.913

output.code

String

错误码，仅在任务失败时返回

\-

output.message

String

错误信息，仅任务失败时返回

\-

output.task\_metrics

Object

任务指标，包含子任务状态的统计信息

`{`

`"TOTAL": 4, //子任务总数`

`"SUCCEEDED": 3, //子任务成功数`

`"FAILED": 1 //子任务失败数`

`}`

usage

Object

本次请求产生的计量信息，根据实际任务的不同，相关的计量信息也有所不同

`"usage": {"image_count": 1}`

#### **请求示例**

```
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/73205176-xxxx-xxxx-xxxx-16bd5d902219' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**说明**

若未配置阿里云百炼API Key到环境变量，请将`$DASHSCOPE_API_KEY`替换为实际API Key，例如：`--header "Authorization: Bearer sk-xxx"`。

#### **响应示例**

```
{
    "request_id": "45ac7f13-xxxx-xxxx-xxxx-e03c35068d83",
    "output": {
        "task_id": "73205176-xxxx-xxxx-xxxx-16bd5d902219",
        "task_status": "SUCCEEDED",
        "submit_time": "2023-12-20 21:36:31.896",
        "scheduled_time": "2023-12-20 21:36:39.009",
        "end_time": "2023-12-20 21:36:45.913",
        "results": [
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx1.png"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx2.png"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx3.png"
            },
            {
                "code": "DataInspectionFailed",
                "message": "Output data may contain inappropriate content.",
            }
        ],
        "task_metrics": {
            "TOTAL": 4,
            "SUCCEEDED": 3,
            "FAILED": 1
        }
    },
    "usage": {
        "image_count": 3
    }
}
```

## **批量查询异步任务状态接口**

**API描述**：支持通过组合多种查询条件，批量获取多个异步任务的当前状态。该接口适用于一次性查看多个任务的执行进度。

**流量限制**：20 QPS，即每秒每个账号（含主账号及其子账号）最多发起 20 次请求。

**重要**

-   支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务），但无法查询到其他主账号下的任务。
    
-   已结束的任务在超时后将被系统自动清理，届时将无法查询到相关任务数据。
    

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/
```

#### **入参描述**

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Header

Authorization

String

是

API-Key，例如：Bearer sk-xxx

Bearer sk-xxx

Params

task\_id

String

否

需要查询任务的 task\_id

若指定task\_id，接口仅返回该任务的状态信息；若需批量查询多个任务状态，请勿传入此参数

a8532587-xxxx-xxxx-xxxx-0c46b17950d1

start\_time

String

否

任务开始时间，格式为：`YYYYMMDDhhmmss`

-   若未指定开始时间（start\_time为空），系统将查询指定结束时间（end\_time）前24小时的数据
    
-   若开始和结束时间均未指定（均为空），系统默认查询最近24小时的数据。
    
-   请确保您设定的开始和结束时间的差距不超过24小时
    

20230420193058 代表 2023 年 4 月 20 日 19 点 30 分 58 秒

end\_time

String

否

任务结束时间，格式为：`YYYYMMDDhhmmss`

-   若未指定结束时间（end\_time为空），系统将查询指定开始时间（start\_time）后24小时的数据。
    
-   请确保您设定的开始和结束时间的差距不超过24小时
    

model\_name

String

否

模型名称

wanx-v1

status

String

否

任务状态：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务取消成功
    
-   UNKNOWN：任务不存在或状态未知
    

page\_no

Integer

否

当前页，默认查询第1页

\-

page\_size

Integer

否

每页查询条数，默认查询10条

\-

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

String

本次请求的系统唯一码

7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51

data

Array

查询结果列表

```
"data": [
    {
        "api_key_id": "235",
        "caller_uid": "1808342417264262",
        "end_time": 1682527200093,
        "gmt_create": 1682514589152,
        "model_name": "paraformer-16k-1",
        "region": "cn-hangzhou",
        "request_id": "32b67b58-xxxx-xxxx-xxxx-230f0aee64d9",
        "start_time": 1682515862179,
        "status": "FAILED",
        "task_id": "cf52b16b-xxxx-xxxx-xxxx-17f9c211440c",
        "user_api_unique_key": "apikey:v1:audio:asr:transcription:paraformer-16k-1"
    }
]
```

data\[\].api\_key\_id

String

API Key的id

data\[\].caller\_parent\_id

String

阿里云主账号ID

data\[\].caller\_uid

String

阿里云账号ID

data\[\].gmt\_create

Long

任务创建时间，Date时间毫秒数

data\[\].start\_time

Long

任务开始时间，Date时间毫秒数

data\[\].end\_time

Long

任务结束时间，Date时间毫秒数

data\[\].region

String

地域，例如：cn-hangzhou

data\[\].request\_id

String

提交任务的请求id

data\[\].status

String

任务状态：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务取消成功
    
-   UNKNOWN：任务不存在或状态未知
    

data\[\].task\_id

String

任务id

data\[\].user\_api\_unique\_key

String

API 的唯一key（提交任务时，模型API的各要素唯一索引）

data\[\].model\_name

String

模型名称

page\_no

Integer

当前页

`"page_no": 1`

page\_size

Integer

每页查询条数

`"page_size": 10`

total\_page

Integer

总页数

`"total_page": 4`

total

Integer

总条数

`"total": 39`

code

String

调用失败的时候返回的错误码

`"code": "Throttling.RateQuota"`

message

String

调用失败的时候返回的错误信息

`"message": "Requests rate limit exceeded, please try again later."`

#### **请求示例**

```
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **响应示例**

```
{
    "total": 2,
    "data": [
        {
            "api_key_id": "15xxxx",
            "caller_parent_id": "xxxxxxxxx",
            "caller_uid": "xxxxxxxxx",
            "gmt_create": 1745568428109,
            "model_name": "wanx2.1-kf2v-plus",
            "region": "cn-beijing",
            "request_id": "1abfc3c8-dd25-98da-ad0b-xxxxxx",
            "start_time": 1745568428138,
            "status": "RUNNING",
            "task_id": "50e2ccea-abc4-43d7-a0dc-xxxxxx",
            "user_api_unique_key": "apikey:v1:aigc:image2video:video-synthesis:wanx2.1-kf2v-plus"
        },
        {
            "api_key_id": "15xxxx",
            "caller_parent_id": "xxxxxxxxx",
            "caller_uid": "xxxxxxxxx",
            "end_time": 1745568302481,
            "gmt_create": 1745568293253,
            "model_name": "wanx2.1-t2i-turbo",
            "region": "cn-beijing",
            "request_id": "f6bf34d9-bf87-9e8b-9ed4-xxxxxx",
            "start_time": 1745568293273,
            "status": "SUCCEEDED",
            "task_id": "3c777dbc-8cc6-4d80-aa90-xxxxxx",
            "user_api_unique_key": "apikey:v1:aigc:text2image:image-synthesis:wanx2.1-t2i-turbo"
        }
    ],
    "total_page": 1,
    "page_no": 1,
    "request_id": "f6756b7e-d0bb-9b74-813a-xxxxxx",
    "page_size": 10
}
```

## **取消异步任务接口**

**API描述**：用于取消异步任务，仅支持取消状态为 `**PENDING**` 的任务 （即排队中且尚未开始处理的任务），其他状态的任务无法取消。

**流量限制**：20 QPS，即每秒每个账号（含主账号及其子账号）最多发起 20 次请求。

**重要**

-   支持取消当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务），但无法取消其他主账号提交的任务。
    

#### **请求接口**

```
POST https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel
```

#### **入参描述**

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Header

Authorization

String

是

API-Key，例如：Bearer sk-xxx

Bearer sk-xxx

Path

task\_id

String

是

待取消的任务 task\_id

a8532587-xxxx-xxxx-xxxx-0c46b17950d1

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

String

本次请求的系统唯一码

7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51

code

String

调用失败的时候返回的错误码

`"code": "Throttling.RateQuota"`

message

String

调用失败的时候返回的错误信息

`"message": "Requests rate limit exceeded, please try again later."`

#### **请求示例**

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/tasks/73205176-xxxx-xxxx-xxxx-16bd5d902219/cancel' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **响应示例**

```
{
    "request_id": "45ac7f13-xxxx-xxxx-xxxx-e03c35068d83"
}
```

## **错误码**

**HTTP状态码**

**接口错误码（code）**

**接口错误信息（message）**

**含义说明**

400

UnsupportedOperation

Failed to cancel the task, please confirm if the task is in PENDING status.

取消任务失败，请确认任务状态为`PENDING`。

仅 PENDING 状态的任务可取消，其他状态任务无法取消。

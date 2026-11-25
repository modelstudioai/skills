# 异步任务管理 API

阿里云百炼的部分模型（如图像生成、视频生成等）因处理时间较长，采用异步调用机制，通常需要调用两个接口完成操作：先创建任务获取 ID，再通过该 ID 查询结果。为了方便管理异步任务，阿里云百炼提供了一组通用的异步任务接口，支持查询单个任务结果、批量查询多个任务状态、以及取消正在排队且尚未处理的任务。

<a id="前提条件"></a>

<a id="c445b17ce67lk"></a>

## 前提条件

异步任务API通过HTTP进行调用。

在调用前，您需要[获取与配置 API Key](../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="查询异步任务结果接口"></a>

<a id="d6e9544d10arj"></a>

## 查询异步任务结果接口

**API描述**：根据`任务ID（task_id）`查询任务状态和任务结果。

**流量限制**：20 QPS，即每秒每个账号（含主账号及其子账号）最多发起 20 次请求。

> **重要**
>
> -   支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务），但无法查询其他主账号提交的任务。
> -   异步任务在完成后通常保留 24 小时 （具体以对应任务的 API 文档为准），超时后系统将自动清理历史任务数据。

> **说明**
>
> 查询任务结果的次数不影响任务的执行。建议根据任务类型合理设置查询间隔：
>
> -   较快的任务（如文本向量）可以使用较短的查询间隔。
> -   较慢的任务（如图像生成、视频生成）建议使用较长的查询间隔。
> -   避免过于频繁地查询任务状态，以防触发限流（20 QPS）。

<a id="请求接口"></a>

<a id="b4c46c6698p5y"></a>

#### 请求接口

<a id="code-block"></a>

```http
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

<a id="入参描述"></a>

<a id="e4f146cf879vh"></a>

#### 入参描述

| 传参方式 | 字段 | 类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| Header | Authorization | String | 是 | API-Key，例如：Bearer sk-xxx | Bearer sk-xxx |
| Path | task\_id | String | 是 | 需查询的任务ID | a8532587-xxxx-xxxx-xxxx-0c46b17950d1 |

<a id="出参描述"></a>

<a id="0e0827df7a2pq"></a>

#### 出参描述

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的系统唯一码</p></td><td><p>7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51</p></td></tr><tr><td><p>output</p></td><td><p>Object</p></td><td><ul><li><p>任务成功时，<code>output</code> 包含模型生成的结果对象，具体内容因任务类型而异</p></li><li><p>任务失败或部分失败时，<code>output</code> 会返回对应的 <code>code</code> 和 <code>message</code>，说明失败原因</p></li><li><p>对于包含多个子任务的任务，<code>output</code> 可能同时包含成功的子任务结果和失败的错误信息</p></li></ul></td><td><p>-</p></td></tr><tr><td><p>output.task_id</p></td><td><p>String</p></td><td><p>查询任务的 task_id</p></td><td><p>a8532587-xxxx-xxxx-xxxx-0c46b17950d1</p></td></tr><tr><td><p>output.task_status</p></td><td><p>String</p></td><td><p>任务状态</p><ul><li><p>对于包含多个子任务的任务，只要有一个子任务成功，整个任务会被标记为成功</p></li><li><p>对于失败的子任务，会在 output 中展示具体报错</p></li></ul></td><td><p>任务状态：</p><ul><li><p>PENDING：任务排队中</p></li><li><p>RUNNING：任务处理中</p></li><li><p>SUCCEEDED：任务执行成功</p></li><li><p>FAILED：任务执行失败</p></li><li><p>UNKNOWN：任务不存在或状态未知</p></li></ul></td></tr><tr><td><p>output.submit_time</p></td><td><p>String</p></td><td><p>任务提交时间</p></td><td><p>2023-12-20 21:36:31.896</p></td></tr><tr><td><p>output.scheduled_time</p></td><td><p>String</p></td><td><p>任务调度时间，即开始执行时间</p></td><td><p>2023-12-20 21:36:39.009</p></td></tr><tr><td><p>output.end_time</p></td><td><p>String</p></td><td><p>任务结束时间</p></td><td><p>2023-12-20 21:36:45.913</p></td></tr><tr><td><p>output.code</p></td><td><p>String</p></td><td><p>错误码，仅在任务失败时返回</p></td><td><p>-</p></td></tr><tr><td><p>output.message</p></td><td><p>String</p></td><td><p>错误信息，仅任务失败时返回</p></td><td><p>-</p></td></tr><tr><td><p>output.task_metrics</p></td><td><p>Object</p></td><td><p>任务指标，包含子任务状态的统计信息</p></td><td><p><code>{</code></p><p><code>&quot;TOTAL&quot;: 4, //子任务总数</code></p><p><code>&quot;SUCCEEDED&quot;: 3, //子任务成功数</code></p><p><code>&quot;FAILED&quot;: 1 //子任务失败数</code></p><p><code>}</code></p></td></tr><tr><td><p>usage</p></td><td><p>Object</p></td><td><p>本次请求产生的计量信息，根据实际任务的不同，相关的计量信息也有所不同</p></td><td><p><code>&quot;usage&quot;: {&quot;image_count&quot;: 1}</code></p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="aeeeae52fa6dl"></a>

#### 请求示例

<a id="sec-tabs"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-2"></a>

```bash
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/73205176-xxxx-xxxx-xxxx-16bd5d902219' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="python-sdk"></a>

<a id="python-sdk-h4"></a>

#### Python SDK

异步任务接口与具体任务类型无关，`fetch`、`list`、`cancel` 方法在任意异步任务资源（如 `client.images.jobs`、`client.videos.jobs`、`client.audio.asr.jobs` 等）上均可调用，底层均请求 `/api/v1/tasks`，可查询当前账号下任意任务。

<a id="code-block-3"></a>

```python
import os
import dashscope

# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'), workspace="{WorkspaceId}", region="cn-beijing")

task_id = '73205176-xxxx-xxxx-xxxx-16bd5d902219'
job = client.images.jobs.fetch(task_id)
print(job.status, job.results)
```

<a id="dashscope-cli"></a>

<a id="dashscope-cli-h4"></a>

#### dashscope CLI

<a id="code-block-4"></a>

```bash
export DASHSCOPE_API_KEY="your-api-key"
# 查询指定任务状态（以 video-synthesis 为例）
dashscope video-synthesis fetch <task_id>
```

> **说明**
>
> dashscope CLI 目前仅 `video-synthesis` 子命令支持 `fetch`/`list`/`cancel` 任务管理；`image-synthesis`、`transcription` 等子命令暂未提供。查询其他类型任务请用上方 Python SDK 或 curl。

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../preparations/base-url.md)。

> **说明**
>
> 若未配置阿里云百炼API Key到环境变量，请将`$DASHSCOPE_API_KEY`替换为实际API Key，例如：`--header "Authorization: Bearer sk-xxx"`。

<a id="响应示例"></a>

<a id="f5e9fdac53z9n"></a>

#### 响应示例

<a id="code-block-5"></a>

```json
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

<a id="批量查询异步任务状态接口"></a>

<a id="7bd06355eazul"></a>

## 批量查询异步任务状态接口

**API描述**：支持通过组合多种查询条件，批量获取多个异步任务的当前状态。该接口适用于一次性查看多个任务的执行进度。

**流量限制**：20 QPS，即每秒每个账号（含主账号及其子账号）最多发起 20 次请求。

> **重要**
>
> -   支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务），但无法查询到其他主账号下的任务。
> -   已结束的任务在超时后将被系统自动清理，届时将无法查询到相关任务数据。

<a id="请求接口-2"></a>

<a id="30dfa91dfcpz5"></a>

#### 请求接口

<a id="code-block-6"></a>

```http
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks
```

<a id="入参描述-2"></a>

<a id="a969f20c0ahxy"></a>

#### 入参描述

<table><thead><tr><th><p><strong>传参方式</strong></p></th><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>Header</p></td><td><p>Authorization</p></td><td><p>String</p></td><td><p>是</p></td><td><p>API-Key，例如：Bearer sk-xxx</p></td><td><p>Bearer sk-xxx</p></td></tr><tr><td rowspan="7"><p>Params</p></td><td><p>task_id</p></td><td><p>String</p></td><td><p>否</p></td><td><p>需要查询任务的 task_id</p><p>若指定task_id，接口仅返回该任务的状态信息；若需批量查询多个任务状态，请勿传入此参数</p></td><td><p>a8532587-xxxx-xxxx-xxxx-0c46b17950d1</p></td></tr><tr><td><p>start_time</p></td><td><p>String</p></td><td><p>否</p></td><td><p>任务开始时间，格式为：<code>YYYYMMDDhhmmss</code></p><ul><li><p>若未指定开始时间（start_time为空），系统将查询指定结束时间（end_time）前24小时的数据</p></li><li><p>若开始和结束时间均未指定（均为空），系统默认查询最近24小时的数据。</p></li><li><p>请确保您设定的开始和结束时间的差距不超过24小时</p></li></ul></td><td rowspan="2"><p>20230420193058 代表 2023 年 4 月 20 日 19 点 30 分 58 秒</p></td></tr><tr><td><p>end_time</p></td><td><p>String</p></td><td><p>否</p></td><td><p>任务结束时间，格式为：<code>YYYYMMDDhhmmss</code></p><ul><li><p>若未指定结束时间（end_time为空），系统将查询指定开始时间（start_time）后24小时的数据。</p></li><li><p>请确保您设定的开始和结束时间的差距不超过24小时</p></li></ul></td></tr><tr><td><p>model_name</p></td><td><p>String</p></td><td><p>否</p></td><td><p>模型名称</p></td><td><p>wanx-v1</p></td></tr><tr><td><p>status</p></td><td><p>String</p></td><td><p>否</p></td><td><p>任务状态：</p><ul><li><p>PENDING：任务排队中</p></li><li><p>RUNNING：任务处理中</p></li><li><p>SUCCEEDED：任务执行成功</p></li><li><p>FAILED：任务执行失败</p></li><li><p>CANCELED：任务取消成功</p></li><li><p>UNKNOWN：任务不存在或状态未知</p></li></ul></td><td></td></tr><tr><td><p>page_no</p></td><td><p>Integer</p></td><td><p>否</p></td><td><p>当前页，默认查询第1页</p></td><td><p>-</p></td></tr><tr><td><p>page_size</p></td><td><p>Integer</p></td><td><p>否</p></td><td><p>每页查询条数，默认查询10条</p></td><td><p>-</p></td></tr></tbody></table>

<a id="出参描述-2"></a>

<a id="980dce330dnhp"></a>

#### 出参描述

<table><thead><tr><th><strong>字段</strong></th><th><strong>类型</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的系统唯一码</p></td><td><p>7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51</p></td></tr><tr><td><p>data</p></td><td><p>Array</p></td><td><p>查询结果列表</p></td><td rowspan="13"><a id="code-block-7"></a><pre class="language-json"><code>&quot;data&quot;: [
    {
        &quot;api_key_id&quot;: &quot;235&quot;,
        &quot;caller_uid&quot;: &quot;1808342417264262&quot;,
        &quot;end_time&quot;: 1682527200093,
        &quot;gmt_create&quot;: 1682514589152,
        &quot;model_name&quot;: &quot;paraformer-16k-1&quot;,
        &quot;region&quot;: &quot;cn-hangzhou&quot;,
        &quot;request_id&quot;: &quot;32b67b58-xxxx-xxxx-xxxx-230f0aee64d9&quot;,
        &quot;start_time&quot;: 1682515862179,
        &quot;status&quot;: &quot;FAILED&quot;,
        &quot;task_id&quot;: &quot;cf52b16b-xxxx-xxxx-xxxx-17f9c211440c&quot;,
        &quot;user_api_unique_key&quot;: &quot;apikey:v1:audio:asr:transcription:paraformer-16k-1&quot;
    }
]
</code></pre></td></tr><tr><td><p>data[].api_key_id</p></td><td><p>String</p></td><td><p>API Key的id</p></td></tr><tr><td><p>data[].caller_parent_id</p></td><td><p>String</p></td><td><p>阿里云主账号ID</p></td></tr><tr><td><p>data[].caller_uid</p></td><td><p>String</p></td><td><p>阿里云账号ID</p></td></tr><tr><td><p>data[].gmt_create</p></td><td><p>Long</p></td><td><p>任务创建时间，Date时间毫秒数</p></td></tr><tr><td><p>data[].start_time</p></td><td><p>Long</p></td><td><p>任务开始时间，Date时间毫秒数</p></td></tr><tr><td><p>data[].end_time</p></td><td><p>Long</p></td><td><p>任务结束时间，Date时间毫秒数</p></td></tr><tr><td><p>data[].region</p></td><td><p>String</p></td><td><p>地域，例如：cn-hangzhou</p></td></tr><tr><td><p>data[].request_id</p></td><td><p>String</p></td><td><p>提交任务的请求id</p></td></tr><tr><td><p>data[].status</p></td><td><p>String</p></td><td><p>任务状态：</p><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务取消成功</li><li>UNKNOWN：任务不存在或状态未知</li></ul></td></tr><tr><td><p>data[].task_id</p></td><td><p>String</p></td><td><p>任务id</p></td></tr><tr><td><p>data[].user_api_unique_key</p></td><td><p>String</p></td><td><p>API 的唯一key（提交任务时，模型API的各要素唯一索引）</p></td></tr><tr><td><p>data[].model_name</p></td><td><p>String</p></td><td><p>模型名称</p></td></tr><tr><td><p>page_no</p></td><td><p>Integer</p></td><td><p>当前页</p></td><td><p><code>&quot;page_no&quot;: 1</code></p></td></tr><tr><td><p>page_size</p></td><td><p>Integer</p></td><td><p>每页查询条数</p></td><td><p><code>&quot;page_size&quot;: 10</code></p></td></tr><tr><td><p>total_page</p></td><td><p>Integer</p></td><td><p>总页数</p></td><td><p><code>&quot;total_page&quot;: 4</code></p></td></tr><tr><td><p>total</p></td><td><p>Integer</p></td><td><p>总条数</p></td><td><p><code>&quot;total&quot;: 39</code></p></td></tr><tr><td><p>code</p></td><td><p>String</p></td><td><p>调用失败的时候返回的错误码</p></td><td><p><code>&quot;code&quot;: &quot;Throttling.RateQuota&quot;</code></p></td></tr><tr><td><p>message</p></td><td><p>String</p></td><td><p>调用失败的时候返回的错误信息</p></td><td><p><code>&quot;message&quot;: &quot;Requests rate limit exceeded, please try again later.&quot;</code></p></td></tr></tbody></table>

<a id="请求示例-2"></a>

<a id="7619f5b773v6c"></a>

#### 请求示例

<a id="sec-tabs-2"></a>

<a id="curl-2"></a>

<a id="curl-2-h4"></a>

#### curl

<a id="code-block-8"></a>

```bash
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks?start_time=xxx&end_time=xxx&status=xxx' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="python-sdk-2"></a>

<a id="python-sdk-2-h4"></a>

#### Python SDK

<a id="code-block-9"></a>

```python
import os
import dashscope

# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'), workspace="{WorkspaceId}", region="cn-beijing")

page = client.images.jobs.list(
    start_time='20230420193000',
    end_time='20230420203000',
    status='RUNNING',
    page_no=1,
    page_size=10,
)
print(page.total, page.tasks)
```

`list` 还支持按 `model_name`、`api_key_id`、`region` 等条件筛选，参数与 HTTP API 的 Query 参数一一对应。

> **说明**
>
> `fetch`、`list`、`cancel` 在工作空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）和通用域名（`dashscope.aliyuncs.com`）均支持，跨地域（如 cn-beijing、cn-shanghai、cn-hangzhou）均可调用。调用时 API Key 须与对应业务空间匹配。

<a id="dashscope-cli-2"></a>

<a id="dashscope-cli-2-h4"></a>

#### dashscope CLI

<a id="code-block-10"></a>

```bash
export DASHSCOPE_API_KEY="your-api-key"
# 列出视频合成任务（支持 --start-time/--end-time/--status/--model-name 等筛选）
dashscope video-synthesis list --status RUNNING -s 10
```

> **说明**
>
> dashscope CLI 目前仅 `video-synthesis` 子命令支持任务管理；查询其他类型任务（图像、语音转写等）请用上方 Python SDK 或 curl。

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../preparations/base-url.md)。

<a id="响应示例-2"></a>

<a id="bc0d4b18dbf5s"></a>

#### 响应示例

<a id="code-block-11"></a>

```json
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

<a id="取消异步任务接口"></a>

<a id="7e160e9b18vt2"></a>

## 取消异步任务接口

**API描述**：用于取消异步任务，仅支持取消状态为 `PENDING` 的任务 （即排队中且尚未开始处理的任务），其他状态的任务无法取消。

**流量限制**：20 QPS，即每秒每个账号（含主账号及其子账号）最多发起 20 次请求。

> **重要**
>
> -   支持取消当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务），但无法取消其他主账号提交的任务。

<a id="请求接口-3"></a>

<a id="34b67e3965yn1"></a>

#### 请求接口

<a id="code-block-12"></a>

```http
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}/cancel
```

<a id="入参描述-3"></a>

<a id="2fb0d75706a0q"></a>

#### 入参描述

| 传参方式 | 字段 | 类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| Header | Authorization | String | 是 | API-Key，例如：Bearer sk-xxx | Bearer sk-xxx |
| Path | task\_id | String | 是 | 待取消的任务 task\_id | a8532587-xxxx-xxxx-xxxx-0c46b17950d1 |

<a id="出参描述-3"></a>

<a id="aace106edbd82"></a>

#### 出参描述

| 字段 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| request\_id | String | 本次请求的系统唯一码 | 7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51 |
| code | String | 调用失败的时候返回的错误码 | `"code": "Throttling.RateQuota"` |
| message | String | 调用失败的时候返回的错误信息 | `"message": "Requests rate limit exceeded, please try again later."` |

<a id="请求示例-3"></a>

<a id="36601f8482ilp"></a>

#### 请求示例

<a id="sec-tabs-3"></a>

<a id="curl-3"></a>

<a id="curl-3-h4"></a>

#### curl

<a id="code-block-13"></a>

```bash
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/73205176-xxxx-xxxx-xxxx-16bd5d902219/cancel' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="python-sdk-3"></a>

<a id="python-sdk-3-h4"></a>

#### Python SDK

<a id="code-block-14"></a>

```python
import os
import dashscope

# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'), workspace="{WorkspaceId}", region="cn-beijing")

task_id = '73205176-xxxx-xxxx-xxxx-16bd5d902219'
job = client.images.jobs.cancel(task_id)
print(job)
```

仅状态为 `PENDING` 的任务可取消，其他状态下调用将抛出 `DashScopeError`（`UnsupportedOperation`）。

<a id="dashscope-cli-3"></a>

<a id="dashscope-cli-3-h4"></a>

#### dashscope CLI

<a id="code-block-15"></a>

```bash
export DASHSCOPE_API_KEY="your-api-key"
# 取消任务（以 video-synthesis 为例，仅 PENDING 状态可取消）
dashscope video-synthesis cancel <task_id>
```

> **说明**
>
> dashscope CLI 目前仅 `video-synthesis` 子命令支持 `cancel`；取消其他类型任务请用上方 Python SDK 或 curl。

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../preparations/base-url.md)。

<a id="响应示例-3"></a>

<a id="7eb12430118ay"></a>

#### 响应示例

<a id="code-block-16"></a>

```json
{
    "request_id": "45ac7f13-xxxx-xxxx-xxxx-e03c35068d83"
}
```

<a id="错误码"></a>

<a id="3b9b15a6a8qkl"></a>

## 错误码

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | UnsupportedOperation | Failed to cancel the task, please confirm if the task is in PENDING status. | 取消任务失败，请确认任务状态为`PENDING`。<br><br>仅 PENDING 状态的任务可取消，其他状态任务无法取消。 |

<a id="常见问题"></a>

<a id="f7b3c4d5e6mz1"></a>

## 常见问题

<a id="任务查询返回-datainspectionfailed-错误码是什么含义"></a>

<a id="b9d5e6f7a8ob3"></a>

### 任务查询返回 DataInspectionFailed 错误码是什么含义？

`DataInspectionFailed` 表示输出数据可能包含不适当的内容，已被内容安全审核拦截。对于包含多个子任务的异步任务（如批量图像生成），部分子任务可能返回此错误码，而其他子任务仍正常完成。此时整体任务状态可能为 `SUCCEEDED`，但 `task_metrics` 中会显示失败的子任务数量。

<a id="如何判断异步任务是否执行完成"></a>

<a id="e2a8b9c0d1re6"></a>

### 如何判断异步任务是否执行完成？

通过查询任务接口返回的 `task_status` 字段判断：

-   `PENDING`：任务排队中，尚未开始处理。
-   `RUNNING`：任务处理中。
-   `SUCCEEDED`：任务执行成功。
-   `FAILED`：任务执行失败，请查看 `output` 中的 `code` 和 `message` 了解失败原因。

<a id="频繁查询任务状态会影响任务执行吗"></a>

<a id="e4a0b1c2d3dq8"></a>

### 频繁查询任务状态会影响任务执行吗？

不会。查询任务状态的请求与任务执行是独立的，查询次数不影响任务的执行进度和结果。但请注意，查询接口有 20 QPS 的限流限制，过于频繁的查询可能会触发限流，返回错误响应。建议根据任务类型合理设置查询间隔。

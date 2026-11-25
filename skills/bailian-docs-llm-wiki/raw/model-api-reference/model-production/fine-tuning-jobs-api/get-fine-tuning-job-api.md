# 调优任务管理

查询、取消、删除调优任务，以及查询调优任务日志。

<a id="适用范围"></a>

<a id="scope-6612755-h2"></a>

## 适用范围

-   **适用地域**：本文描述的功能仅在华北2（北京）地域可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   已成功[获取 API Key](../../preparations/get-api-key.md)并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已通过[创建调优任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口创建了调优任务。

<a id="查询调优任务状态"></a>

<a id="faa99e295ckyg"></a>

## 查询调优任务状态

查询指定调优任务的详细信息和运行状态。

<a id="地址"></a>

<a id="addr-qftst-h3"></a>

### 地址

<a id="code-block"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}
```

<a id="请求示例"></a>

<a id="reqex-qftst-h3"></a>

### 请求示例

<a id="code-block-2"></a>

```bash
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

<a id="请求参数"></a>

<a id="9fbddca4907ka"></a>

### 请求参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
| --- | --- | --- | --- | --- |
| job\_id | String | Url Path | 是 | 要查询的调优任务的ID。即[创建调优任务返回参数](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)中的job\_id。 |

<a id="响应示例"></a>

<a id="f5e8e2d6b9zsd"></a>

### 响应示例

<a id="sec-tabs"></a>

<a id="文本生成模型"></a>

<a id="文本生成模型-h4"></a>

#### 文本生成模型

<a id="code-block-3"></a>

```json
{
    "request_id": "c59b2145-a93c-4e00-b610-4d7cc5c521a2",
    "output": {
        "job_id": "ft-202410291653-1c7f",
        "job_name": "ft-202410291653-1c7f",
        "status": "SUCCEEDED",
        "finetuned_output": "qwen3-14b-suffix-ft-202410291653-1c7f",
        "model": "qwen3-14b",
        "base_model": "qwen3-14b",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "976bd01a-f30b-4414-86fd-50c54486e3ef"
            }
        ],
        "validation_datasets": [],
        "hyper_parameters": {
            "n_epochs": 3,
            "batch_size": 32,
            "max_length": 8192,
            "learning_rate": "1.6e-5",
            "lr_scheduler_type": "linear",
            "split": 0.9
        },
        "training_type": "sft",
        "create_time": "2024-10-29 16:53:53",
        "workspace_id": "llm-v71tlv***",
        "user_identity": "1396993924585947",
        "modifier": "1396993924585947",
        "creator": "1396993924585947",
        "end_time": "2024-10-29 17:11:26",
        "group": "llm",
        "usage": 279808
    }
}
```

<a id="视频生成模型"></a>

<a id="视频生成模型-h4"></a>

#### 视频生成模型

关注 `output.status`（SUCCEEDED 表示训练完成）和 `output.usage`（训练消耗的总 Token 数量）。

<a id="code-block-4"></a>

```json
{
    "request_id": "9bbb953c-bef2-4b59-9fc5-xxxxxxxxx",
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "status": "SUCCEEDED",
        "finetuned_output": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "model": "wan2.5-i2v-preview",
        "base_model": "wan2.5-i2v-preview",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "xxxxxxxxxxxx"
            }
        ],
        "validation_datasets": [],
        "hyper_parameters": {
            "n_epochs": 400,
            "learning_rate": 2e-05,
            "split": 0.9,
            "eval_epochs": 50
        },
        "training_type": "efficient_sft",
        "create_time": "2025-11-11 11:22:22",
        "end_time": "2025-11-11 16:49:01",
        "usage": 432000,
        "output_cnt": 8
    }
}
```

<a id="图像生成模型"></a>

<a id="图像生成模型-h4"></a>

#### 图像生成模型

<a id="code-block-5"></a>

```json
{
    "request_id": "03d738f5-3720-90b0-9c7b-xxxxxxxxx",
    "output": {
        "job_id": "ft-202606030110-xxxx",
        "status": "SUCCEEDED",
        "finetuned_output": "wan2.7-image-pro-ft-202606030110-xxxx",
        "model": "wan2.7-image-pro",
        "base_model": "wan2.7-image-pro",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "xxxxxxxxxxxx"
            }
        ],
        "validation_datasets": [],
        "hyper_parameters": {
            "max_steps": 800,
            "learning_rate": 3e-05,
            "eval_steps": 200,
            "max_token_length": "2k",
            "max_pixels": "2k",
            "val_img_size": "2k",
            "generation_type": "t2i",
            "lora_rank": 32
        },
        "training_type": "efficient_sft",
        "create_time": "2026-06-03 01:10:47",
        "end_time": "2026-06-03 01:38:53",
        "usage": 10273216,
        "output_cnt": 1
    }
}
```

<a id="响应参数"></a>

<a id="e917ac3670zpr"></a>

### 响应参数

| 参数名称 | 类型 | 参数说明 |
| --- | --- | --- |
| request\_id | String | 本次请求的ID。 |
| output | Object | 调优任务的详细信息。 |
| output.job\_id | String | 本次调优的任务ID，用于后续查询状态。<br><br>生成规则：`ft-{yyyyMMddHHmm}-{4位uuid}`。 |
| output.jobs\_name | String | 同`output.job_id`。 |
| output.status | String | 本次调优[任务的状态](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。 |
| output.finetuned\_output | String | 仅调优任务状态为“SUCCEED”时出现，返回的是调优完成的模型ID。 |
| output.model | String | 调优任务使用的模型ID。 |
| output.base\_model | String | 调优任务使用的模型对应的基础模型ID。<br><br>比如：调优任务`ft-202410291653-1c7f`使用的基础模型是`qwen3-14b`。 |
| output.training\_file\_ids | Array | 兼容字段，新任务始终返回空数组，请使用 training\_datasets。 |
| output.validation\_file\_ids | Array | 兼容字段，新任务始终返回空数组，请使用 validation\_datasets。 |
| output.training\_datasets | Array of Dataset | 训练数据集列表。 |
| output.validation\_datasets | Array of Dataset | 测试数据集列表。 |
| output.hyper\_parameters | Object | 显性声明过的超参表。 |
| output.training\_type | String | 调优方法。 |
| output.create\_time | String | 调优任务创建时间。 |
| output.workspace\_id | String | 调优任务所属的业务空间ID。 |
| output.user\_identity | String | 该调优任务隶属的主账号UID。 |
| output.modifier | String | 对该调优任务进行最后一次操作的账号UID。（比如：某个子账号取消了该任务，该子账号UID会显示在这里） |
| output.creator | String | 该调优任务创建人UID。 |
| output.end\_time | String | 调优任务结束时间，当任务状态为“SUCCEED”、“FAILED”、“CANCELED”时出现。 |
| output.group | String | 模型调优的任务类型。 |
| output.usage | Integer | 调优任务消耗的Token（count）数，扣费计算公式请参考：计费说明。当任务状态为“SUCCEED”、“CANCELED”时出现。 |
| output.output\_cnt | Integer | 当前任务已产出的 Checkpoint 数量。仅对支持多 Checkpoint 输出的模型（如 `cosyvoice-v3-flash`）返回。Checkpoint 详细列表可通过查询 Checkpoint 接口获取。 |
| output.max\_output\_cnt | Integer | 单次任务可产出的 Checkpoint 数量上限。`output_cnt` 超出上限的部分会按调优充分度截断。仅对支持多 Checkpoint 输出的模型返回。 |

<a id="取消调优任务"></a>

<a id="3gqm7xoh2njae"></a>

## 取消调优任务

取消正在运行的调优任务。仅处于运行中状态的任务可被取消。

<a id="地址-2"></a>

<a id="addr-cancelft-h3"></a>

### 地址

<a id="code-block-6"></a>

```http
POST https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/cancel
```

<a id="请求示例-2"></a>

<a id="reqex-cancelft-h3"></a>

### 请求示例

<a id="code-block-7"></a>

```bash
curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/cancel" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

<a id="请求参数-2"></a>

<a id="5i7yrdng1qtgh"></a>

### 请求参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
| --- | --- | --- | --- | --- |
| job\_id | String | Url Path | 是 | 要取消的调优任务ID，可通过[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)或列举训练任务接口获取。 |

<a id="响应示例-2"></a>

<a id="83u3lwnldunmk"></a>

### 响应示例

<a id="code-block-8"></a>

```json
{
    "request_id": "670fca9d-48dd-4c5a-83e7-33bcc20420f8",
    "output": {
        "status": "success"
    }
}
```

<a id="响应参数-2"></a>

<a id="tfww4gjfkt6hz"></a>

### 响应参数

| 参数名称 | 类型 | 参数说明 |
| --- | --- | --- |
| request\_id | String | 本次请求的ID。 |
| output | Object | 取消操作返回的详细信息。 |

<a id="删除调优任务"></a>

<a id="c3mq93izbce81"></a>

## 删除调优任务

删除指定的调优任务记录。

<a id="地址-3"></a>

<a id="addr-delft-h3"></a>

### 地址

<a id="code-block-9"></a>

```http
DELETE https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}
```

<a id="请求示例-3"></a>

<a id="reqex-delft-h3"></a>

### 请求示例

<a id="code-block-10"></a>

```bash
curl --location --request DELETE "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

<a id="请求参数-3"></a>

<a id="knobd0sern5lt"></a>

### 请求参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
| --- | --- | --- | --- | --- |
| job\_id | String | Url Path | 是 | 要删除的调优任务ID，可通过[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)或列举训练任务接口获取。 |

<a id="响应示例-3"></a>

<a id="95d3clte04c1w"></a>

### 响应示例

<a id="code-block-11"></a>

```json
{
    "request_id": "7d7e1469-df77-4163-83ce-54425df744ed",
    "output": {
        "status": "success"
    }
}
```

<a id="响应参数-3"></a>

<a id="tuf932oscuuv3"></a>

### 响应参数

| 参数名称 | 类型 | 参数说明 |
| --- | --- | --- |
| request\_id | String | 本次请求的ID。 |
| output | Object | 删除操作返回的详细信息。 |

<a id="查询调优任务列表"></a>

<a id="c23cdff6f399h"></a>

## 查询调优任务列表

分页查询当前账号下的调优任务列表。

<a id="地址-4"></a>

<a id="addr-qftlist-h3"></a>

### 地址

<a id="code-block-12"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes
```

<a id="请求示例-4"></a>

<a id="reqex-qftlist-h3"></a>

### 请求示例

<a id="code-block-13"></a>

```bash
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes?model=qwen3-14b&page_no=2" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

<a id="请求参数-4"></a>

<a id="ab4ffd1a30d0p"></a>

### 请求参数

| 参数名称 | 类型 | 传参方式 | 是否必填 | 参数说明 |
| --- | --- | --- | --- | --- |
| page\_no | Integer | Query | 否 | 默认1 |
| page\_size | Integer | Query | 否 | 默认10，最大值1000，最小值1 |
| model | String | Query | 否 | 模型ID，指定该参数表示只列举基于该模型的调优任务 |

<a id="响应示例-4"></a>

<a id="7e4df7a8ealk9"></a>

### 响应示例

<a id="code-block-14"></a>

```json
{
    "request_id": "2182ef64-6398-457b-b3f6-5fde5fd6b388",
    "output": {
        "page_no": 2,
        "page_size": 10,
        "total": 12,
        "jobs": [
            {
                "job_id": "ft-202410291653-1c7f",
                "job_name": "ft-202410291653-1c7f",
                "status": "SUCCEEDED",
                "finetuned_output": "qwen3-14b-suffix-ft-202410291653-1c7f",
                "model": "qwen3-14b",
                "base_model": "qwen3-14b",
                "training_file_ids": [],
                "validation_file_ids": [],
                "training_datasets": [
                    {
                        "data_source_type": "file_id",
                        "file_id": "976bd01a-f30b-4414-86fd-50c54486e3ef"
                    }
                ],
                "validation_datasets": [],
                "hyper_parameters": {
                    "n_epochs": 3,
                    "batch_size": 32,
                    "max_length": 8192,
                    "learning_rate": "1.6e-5",
                    "lr_scheduler_type": "linear",
                    "split": 0.9
                },
                "training_type": "sft",
                "create_time": "2024-10-29 16:53:53",
                "workspace_id": "llm-v71tlv***",
                "user_identity": "1396993924585947",
                "modifier": "1396993924585947",
                "creator": "1396993924585947",
                "end_time": "2024-10-29 17:11:26",
                "group": "llm",
                "usage": 279808
            },
            {
                "job_id": "ft-202410291512-1851",
                "job_name": "ft-202410291512-1851",
                "status": "CANCELED",
                "model": "qwen3-14b",
                "base_model": "qwen3-14b",
                "training_file_ids": [],
                "validation_file_ids": [],
                "training_datasets": [
                    {
                        "data_source_type": "file_id",
                        "file_id": "86a9fe7f-dd77-43b0-9834-2170e12339ec"
                    },
                    {
                        "data_source_type": "file_id",
                        "file_id": "03ead352-6190-4328-8016-61821c23d4fc"
                    }
                ],
                "validation_datasets": [],
                "hyper_parameters": {
                    "n_epochs": 3,
                    "batch_size": 32,
                    "max_length": 8192,
                    "learning_rate": "1.6e-5",
                    "lr_scheduler_type": "linear",
                    "split": 0.9
                },
                "code": "1",
                "training_type": "sft",
                "create_time": "2024-10-29 15:12:00",
                "workspace_id": "llm-v71tlv***",
                "user_identity": "1396993924585947",
                "modifier": "1396993924585947",
                "creator": "1396993924585947",
                "end_time": "2024-10-29 15:16:00",
                "group": "llm",
                "usage": 0
            }
        ]
    }
}
```

<a id="响应参数-4"></a>

<a id="e34d1d71f4aov"></a>

### 响应参数

<table><thead><tr><th><strong>参数名称</strong></th><th><strong>类型</strong></th><th><strong>参数说明</strong></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的ID。</p></td></tr><tr><td><p>output</p></td><td><p>Object</p></td><td><p>查询返回的详细信息。</p></td></tr><tr><td><p>output.page_no</p></td><td><p>Integer</p></td><td><p>页码。</p></td></tr><tr><td><p>output.page_size</p></td><td><p>Integer</p></td><td><p>每页显示的数据量。</p></td></tr><tr><td><p>output.total</p></td><td><p>Integer</p></td><td><p>调优任务总计数量。</p></td></tr><tr><td><p>output.jobs</p></td><td><p>Array</p></td><td><p>多个调优任务详情。</p><a id="accordion-点击此处查看调优任务详情对象"></a><section><p>点击此处查看调优任务详情对象</p><div><table><thead><tr><th><p><strong>参数名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>参数说明</strong></p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的ID。</p></td></tr><tr><td><p>output</p></td><td><p>Object</p></td><td><p>调优任务的详细信息。</p></td></tr><tr><td><p>output.job_id</p></td><td><p>String</p></td><td><p>本次调优的任务ID，用于后续查询状态。</p><p>生成规则：<code>ft-{yyyyMMddHHmm}-{4位uuid}</code>。</p></td></tr><tr><td><p>output.jobs_name</p></td><td><p>String</p></td><td><p>同<code>output.job_id</code>。</p></td></tr><tr><td><p>output.status</p></td><td><p>String</p></td><td><p>本次调优<a href="../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md">任务的状态</a>。</p></td></tr><tr><td><p>output.finetuned_output</p></td><td><p>String</p></td><td><p>仅调优任务状态为“SUCCEED”时出现，返回的是调优完成的模型ID。</p></td></tr><tr><td><p>output.model</p></td><td><p>String</p></td><td><p>调优任务使用的模型ID。</p></td></tr><tr><td><p>output.base_model</p></td><td><p>String</p></td><td><p>调优任务使用的模型对应的基础模型ID。</p><p>比如：调优任务<code>ft-202410291653-1c7f</code>使用的基础模型是<code>qwen3-14b</code>。</p></td></tr><tr><td><p>output.training_file_ids</p></td><td><p>Array</p></td><td><p>兼容字段，新任务始终返回空数组，请使用 training_datasets。</p></td></tr><tr><td><p>output.validation_file_ids</p></td><td><p>Array</p></td><td><p>兼容字段，新任务始终返回空数组，请使用 validation_datasets。</p></td></tr><tr><td><p>output.training_datasets</p></td><td><p>Array of Dataset</p></td><td><p>训练数据集列表。</p></td></tr><tr><td><p>output.validation_datasets</p></td><td><p>Array of Dataset</p></td><td><p>测试数据集列表。</p></td></tr><tr><td><p>output.hyper_parameters</p></td><td><p>Object</p></td><td><p>显性声明过的超参表。</p></td></tr><tr><td><p>output.training_type</p></td><td><p>String</p></td><td><p>调优方法。</p></td></tr><tr><td><p>output.create_time</p></td><td><p>String</p></td><td><p>调优任务创建时间。</p></td></tr><tr><td><p>output.workspace_id</p></td><td><p>String</p></td><td><p>调优任务所属的业务空间ID。</p></td></tr><tr><td><p>output.user_identity</p></td><td><p>String</p></td><td><p>该调优任务隶属的主账号UID。</p></td></tr><tr><td><p>output.modifier</p></td><td><p>String</p></td><td><p>对该调优任务进行最后一次操作的账号UID。（比如：某个子账号取消了该任务，该子账号UID会显示在这里）</p></td></tr><tr><td><p>output.creator</p></td><td><p>String</p></td><td><p>该调优任务创建人UID。</p></td></tr><tr><td><p>output.end_time</p></td><td><p>String</p></td><td><p>调优任务结束时间，当任务状态为“SUCCEED”、“FAILED”、“CANCELED”时出现。</p></td></tr><tr><td><p>output.group</p></td><td><p>String</p></td><td><p>模型调优的任务类型。</p></td></tr><tr><td><p>output.usage</p></td><td><p>Integer</p></td><td><p>调优任务消耗的Token（count）数，扣费计算公式请参考：计费说明。当任务状态为“SUCCEED”、“CANCELED”时出现。</p></td></tr><tr><td><p>output.output_cnt</p></td><td><p>Integer</p></td><td><p>当前任务已产出的 Checkpoint 数量。仅对支持多 Checkpoint 输出的模型（如 <code>cosyvoice-v3-flash</code>）返回。Checkpoint 详细列表可通过查询 Checkpoint 接口获取。</p></td></tr><tr><td><p>output.max_output_cnt</p></td><td><p>Integer</p></td><td><p>单次任务可产出的 Checkpoint 数量上限。<code>output_cnt</code> 超出上限的部分会按调优充分度截断。仅对支持多 Checkpoint 输出的模型返回</p></td></tr></tbody></table></div></section></td></tr></tbody></table>

<a id="查询调优任务日志"></a>

<a id="e76df8eaa2vbs"></a>

## 查询调优任务日志

查询指定调优任务的训练日志。

<a id="地址-5"></a>

<a id="addr-qftlog-h3"></a>

### 地址

<a id="code-block-15"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/logs
```

<a id="请求示例-5"></a>

<a id="reqex-qftlog-h3"></a>

### 请求示例

<a id="code-block-16"></a>

```bash
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/logs?offset=10&line=10" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

<a id="请求参数-5"></a>

<a id="b57741b445w6r"></a>

### 请求参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
| --- | --- | --- | --- | --- |
| job\_id | String | Url Path | 是 | 要打印日志的调优任务ID，可通过创建训练任务或列举训练任务接口获取。 |
| offset | Number | Query | 否 | 忽略前`offset`行输出，从第`offset+1`行开始读取。不能超过当前已有输出的总行数，超过则不会有输出信息返回。默认值为0。 |
| line | Number | Query | 否 | 从`offset+1`行（包含）起，读取`line`行输出信息，如果本次请求的输出不足`line`行，则以实际输出为准。默认值为100，上限为1000。 |

<a id="响应示例-5"></a>

<a id="6464563a5bnw1"></a>

### 响应示例

<a id="code-block-17"></a>

```json
{
    "request_id": "ce49b45d-fe46-474e-9e1b-3e7427ffdf5a",
    "output": {
        "total": 20,
        "logs": [
            "{'train_runtime': 216.3999, 'train_samples_per_second': 2.066, 'train_steps_per_second': 0.014, 'train_loss': 0.9122632344563802, 'epoch': 0.8571428571428571}",
            " Actual number of consumed tokens is 279808!",
            " Uploaded checkpoint!",
            " Fine-tune succeeded!",
            " use checkpoint-3 as final checkpoint",
            "2024-10-29 17:03:47,719 - INFO - transfer for inference succeeded, start to deliver it for inference",
            "2024-10-29 17:09:43,322 - INFO - start to save checkpoint",
            "2024-10-29 17:11:24,689 - INFO - finetune-job succeeded",
            "2024-10-29 17:11:25,130 - INFO - training usage 279808",
            "2024-10-29 17:11:25,175 - INFO - ##FT_COMPLETE##"
        ]
    }
}
```

<a id="响应参数-5"></a>

<a id="4a15fcece6z9u"></a>

### 响应参数

| 参数名称 | 类型 | 参数说明 |
| --- | --- | --- |
| request\_id | String | 本次请求的ID。 |
| output | Object | 查询返回的详细信息。 |
| output.total | Integer | 日志总计行数。 |
| output.logs | Array | 输出的日志。 |

<a id="异常响应"></a>

<a id="cc08546c7csjy"></a>

## 异常响应

<a id="响应示例-6"></a>

<a id="errresp-example-h3"></a>

### 响应示例

<a id="code-block-18"></a>

```json
{
    "code": "NotFound",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "Not Found!"
}
```

<a id="响应参数-6"></a>

<a id="errresp-params-h3"></a>

### 响应参数

| 字段 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| code | String | 错误码。 | NotFound |
| request\_id | String | 本次请求的系统唯一码。 | 6332fb02-3111-43f0-bf79-f9e8c5ffa7f9 |
| message | String | 错误信息。 | Not Found! |

当请求出错时，可能返回以下错误：

<table><thead><tr><th><p><strong>HTTP状态码</strong></p></th><th><p><strong>错误码</strong></p></th><th><p><strong>错误信息举例</strong></p></th><th><p><strong>含义</strong></p></th><th><p><strong>处理方式</strong></p></th></tr></thead><tbody><tr><td><p>400</p></td><td><p>InvalidParameter</p></td><td><p>Missing training files</p></td><td><p>参数错误，缺少参数或者参数格式问题等。</p></td><td><p>根据错误信息，修正您的参数。</p></td></tr><tr><td><p>400</p></td><td><p>UnsupportedOperation</p></td><td><p>The fine-tune job can not be canceled because it is succeeded or failed</p></td><td><p>当资源处于特定状态时，无法对其进行操作。</p></td><td><p>待要操作的资源到达可操作状态时再进行操作。</p></td></tr><tr><td><p>400</p></td><td><p>UnsupportedOperation</p></td><td><p>The fine-tune job can not be deleted because it is succeeded,failed or canceled</p></td><td><p>当资源处于特定状态时，无法对其进行操作。</p></td><td><p>待要操作的资源到达可操作状态时再进行操作。</p></td></tr><tr><td><p>404</p></td><td><p>NotFound</p></td><td><p>Not found!</p></td><td><p>要查询/操作的资源不存在。</p></td><td><p>检查要查询/操作的资源ID是否错误。</p></td></tr><tr><td><p>409</p></td><td><p>Conflict</p></td><td><p>Model instance xxxxx already exists, please specify a suffix</p></td><td><p>已存在deployed_model名为xxxxx的部署实例，需要指定后缀进行区分。</p></td><td><p>为部署指定唯一的后缀。</p></td></tr><tr><td><p>429</p></td><td><p>Throttling</p></td><td><ul><li><p>Too many fine-tune job in running, please retry later.</p></li><li><p>Only 20 fine-tune job in running or succeeded allowed per user.</p></li></ul></td><td><p>资源的创建触发平台限制。</p></td><td><ul><li><p>删除不再使用的模型。</p></li><li><p>如您确实需要提高调优任务的并发量或保留更多调优成功的模型，请联系商务经理。</p></li></ul></td></tr><tr><td><p>500</p></td><td><p>InternalError</p></td><td><p>Internal server error!</p></td><td><p>内部错误。</p></td><td><p>记录 request_id，通过工单联系阿里云工程师进行排查。</p></td></tr></tbody></table>

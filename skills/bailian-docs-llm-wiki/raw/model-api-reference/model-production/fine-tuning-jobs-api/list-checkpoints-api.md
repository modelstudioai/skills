# Checkpoint 管理

管理调优任务产出的 Checkpoint：列举、导出、查询验证结果，及 Checkpoint 对象说明。

## 适用范围

-   **适用地域**：本文描述的功能仅在华北2（北京）地域可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
    
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace)。
    
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   **接口支持的微调模型类型：**
    -   [列举 Checkpoint](https://help.aliyun.com/zh/model-studio/list-checkpoints-api#51ryvkmpq074r)：文本生成、视频生成、图像生成、语音合成
    -   [导出 Checkpoint](https://help.aliyun.com/zh/model-studio/list-checkpoints-api#a7k3m9x2q8r4t)：文本生成、视频生成、图像生成、语音合成
    -   [查询Checkpoint验证列表](https://help.aliyun.com/zh/model-studio/list-checkpoints-api#d5cd230b48sab)：视频生成、图像生成
    -   [查询Checkpoint验证结果](https://help.aliyun.com/zh/model-studio/list-checkpoints-api#09c9c6eb85lxz)：视频生成、图像生成

## 列举 Checkpoint

列举指定调优任务产出的所有 Checkpoint 及其状态、模型信息等。

### 请求接口

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/checkpoints
```

### 入参描述

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

调优任务ID，可通过[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)或列举训练任务接口获取。

ft-202511111122-xxxx

### 出参描述

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

aa4b0229-b1db-9afa-bb6e-xxxxxxxxx

output

array\[object\]

Checkpoint 数组。按 step 从大到小排序。

> 语音合成模型（如 CosyVoice）的 step 由 LM epoch 与 FM epoch 组合而成，排序按 LM epoch × FM epoch 的乘积从大到小（乘积越大代表双端调优越充分）。

output\[\].checkpoint\_id

string

Checkpoint 唯一标识，格式为 `{job_id}:checkpoint-{step编号}`。不同模型类型的 step 编号格式不同，详见 `step` 字段说明。

ft-202605271743-dd2a:checkpoint-00040004

output\[\].full\_name

string

同 `checkpoint_id`。

ft-202605271743-dd2a:checkpoint-00040004

output\[\].checkpoint

string

Checkpoint 名称，格式为 `checkpoint-{step编号}`。

> 语音合成模型（如 CosyVoice）的 step 编号由 LM epoch 和 FM epoch 组合而成，例如 `checkpoint-00040004` 表示 LM 第 4 轮 + FM 第 4 轮。

checkpoint-00040004

output\[\].job\_id

string

该 Checkpoint 所属的调优任务 ID。

ft-202605271743-dd2a

output\[\].step

integer

Checkpoint 对应的训练步数编码。

> 语音合成模型（如 CosyVoice）的 step 计算方式为 `LM_epoch × 10000 + FM_epoch`，例如 40004 表示 LM 第 4 轮 + FM 第 4 轮。

40004

output\[\].status

string

该 Checkpoint 的状态。常见值：`SUCCEEDED`（已就绪，可用于部署）、`PENDING`（尚未就绪）。

SUCCEEDED

output\[\].model\_name

string

该 Checkpoint 对应的模型 ID，可作为[部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)接口的 `model_name` 入参。**仅在**`status=SUCCEEDED`**时返回**。

cosyvoice-v3-flash-ft-202605271743-dd2a

output\[\].model\_display\_name

string

模型显示名（控制台展示用）。仅在 `status=SUCCEEDED` 时返回。

ft-202605271743-dd2a

output\[\].create\_time

string

该 Checkpoint 的创建时间，格式为 ISO 8601。

2026-05-27T18:07:16

output\[\].expire\_time

string

该 Checkpoint 的过期时间，格式为 ISO 8601。

2026-06-11T18:07:16

### 请求示例

请将 URL 中的 `<替换为调优任务job_id>` 完整替换为[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)输出参数`job_id`的值。

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/checkpoints' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

### 响应示例

```
{
    "request_id": "aa4b0229-b1db-9afa-bb6e-3b3e9ee1489b",
    "output": [
        {
            "create_time": "2026-05-27T18:07:16",
            "full_name": "ft-202605271743-dd2a:checkpoint-00040004",
            "job_id": "ft-202605271743-dd2a",
            "checkpoint_id": "ft-202605271743-dd2a:checkpoint-00040004",
            "checkpoint": "checkpoint-00040004",
            "model_name": "cosyvoice-v3-flash-ft-202605271743-dd2a",
            "model_display_name": "ft-202605271743-dd2a",
            "status": "SUCCEEDED",
            "expire_time": "2026-06-11T18:07:16",
            "step": 40004
        },
        {
            "create_time": "2026-05-27T18:07:16",
            "full_name": "ft-202605271743-dd2a:checkpoint-00030004",
            "job_id": "ft-202605271743-dd2a",
            "checkpoint_id": "ft-202605271743-dd2a:checkpoint-00030004",
            "checkpoint": "checkpoint-00030004",
            "status": "PENDING",
            "expire_time": "2026-06-11T18:07:16",
            "step": 30004
        }
    ]
}
```

## 导出 Checkpoint

将指定 Checkpoint 导出为可部署模型。导出成功后，需根据模型类型调用对应的[部署接口](raw/model-api-reference/model-production/deployments-api.md)（不同模型类型的部署接口不同）。

### 请求接口

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/export/{checkpoint}?model_name={model_name}
```

### 入参描述

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

调优任务ID，可通过[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)或列举训练任务接口获取。

ft-202511111122-xxxx

checkpoint

Path parameter

string

是

Checkpoint名称，可通过列举Checkpoint接口获取。

checkpoint-160

model\_name

Query parameter

string

是

用于在控制台中展示的导出模型名称。

该名称需全局唯一，建议使用中英文、数字、下划线（\_）和短横线（-）字符。

请注意：此参数仅用于控制台显示，实际导出的模型名称以列举 Checkpoint输出参数`output[].model_name`为准。

wan2.5-i2v-preview-ft-202511111122-xxxx

### 出参描述

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

boolean

导出请求是否提交成功。

-   true：表示导出请求提交成功。
    
-   false：表示导出请求提交失败，建议重试。
    

true

### 请求示例

-   `<替换为调优任务job_id>`：完整替换为[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)输出参数`job_id`的值。
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如“checkpoint-160”。
-   `<替换为控制台展示的导出模型名称>`：完整替换为自定义的模型名称，仅用于控制台展示。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/export/<替换为待导出的checkpoint>?model_name=<替换为控制台展示的导出模型名称>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应示例

```
{
    "request_id": "0817d1ed-b6b6-4383-9650-xxxxx",
    "output": true
}
```

## 查询Checkpoint验证列表

**说明**文本生成模型不支持此接口。

查询通过验证集成功生成预览视频或图像的 Checkpoint 列表，验证失败的不会列出。

**使用限制**：该接口需在模型调优完成后调用，否则将返回空列表。

### 请求接口

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/validation-results
```

### 入参描述

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

调优任务ID，可通过[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)或列举训练任务接口获取。

ft-202511111122-xxxx

### 出参描述

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

array\[string\]

Checkpoint列表。

\-

output\[\].checkpoint

string

Checkpoint名称。

checkpoint-160

### 请求示例

请将 URL 中的 `<替换为调优任务job_id>` 完整替换为[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)输出参数`job_id`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/validation-results' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

### 响应示例

```
{
    "request_id": "da1310f5-5a21-4e29-99d4-xxxxxx",
    "output": [
        {
            "checkpoint": "checkpoint-160"
        },
        {
            "checkpoint": "checkpoint-20"
        },
        {
            "checkpoint": "checkpoint-40"
        },
        {
            "checkpoint": "checkpoint-60"
        }
    ]
}
```

## 查询Checkpoint验证结果

**说明**文本生成模型不支持此接口。

根据 `checkpoint`（例如 "checkpoint-160"），查询指定 Checkpoint 的验证结果详情，包括生成的预览视频或图像。

### 请求接口

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/validation-details/{checkpoint}?page_no=1&page_size=10
```

### 入参描述

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

调优任务ID，可通过创建训练任务或列举训练任务接口获取。

ft-202511111122-xxxx

checkpoint

Path parameter

string

是

Checkpoint名称，可通过列举 Checkpoint 或查询Checkpoint验证列表接口获取。

checkpoint-160

page\_no

Query parameter

integer

否

页码。默认为1。

1

page\_size

Query parameter

integer

否

每页数量。默认为10。

10

### 出参描述

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

375b3ad0-d3fa-451f-b629-xxxxxxx

output

object

输出结果。

\-

output.page\_no

integer

页码。

1

output.page\_size

integer

每页数量。

10

output.total

integer

验证集列表总数量。

1

output.list

array\[object\]

验证集列表。

\-

output.list\[\].video\_path

string

通过Checkpoint生成的视频。

video\_path有效期为24小时，请及时下载视频。

[https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx](https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx)

output.list\[\].prompt

string

验证数据的prompt。从数据集的标注文件data.jsonl获得。

视频开头展示了一位年轻男性坐在咖啡馆的场景...

output.list\[\].first\_frame\_path

string

验证的图像地址。系统会读取数据集中的图像，并生成一个公网URL地址。

[https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg](https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg)

### 请求示例

-   `<替换为调优任务job_id>`： 完整替换为创建训练任务输出参数`job_id`的值。
-   `<替换为选择的checkpoint>`：完整替换为选定的Checkpoint名称，例如“checkpoint-160”。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/validation-details/<替换为选择的checkpoint>?page_no=1&page_size=10' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应示例

> video\_path有效期为24小时，请及时下载视频。

```
{
    "request_id": "375b3ad0-d3fa-451f-b629-xxxxxxx",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 1,
        "list": [
            {
                "video_path": "https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx",
                "prompt": "视频开头展示了一位年轻男性坐在咖啡馆的场景。他穿着一件米色的Polo衫，神情专注且略显沉思，手指轻轻托着下巴。他的面前摆放着一杯热气腾腾的咖啡，背景是木质条纹的墙壁和一个装饰牌。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
                "first_frame_path": "https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg"
            }
        ]
    }
}
```

## Checkpoint 对象

> 当前 Checkpoint API 仅在北京 Region 开放。如您使用其他 Region，请通过该 Region 的百炼控制台管理 Checkpoint。

检查点对象（Checkpoint）表示调优过程中保存的中间模型状态。通过列举检查点接口返回。

### 字段说明

以下字段来自列举检查点接口的返回结果。

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Array

Checkpoint 数组。按 step 从大到小排序。

> 语音合成模型（如 CosyVoice）的 step 由 LM epoch 与 FM epoch 组合而成，排序按 LM epoch × FM epoch 的乘积从大到小（乘积越大代表双端调优越充分）。

output\[\*\].checkpoint\_id

String

Checkpoint 唯一标识，格式为 `{job_id}:checkpoint-{step编号}`。不同模型类型的 step 编号格式不同，详见 `step` 字段说明。

output\[\*\].full\_name

String

同 `checkpoint_id`。

output\[\*\].checkpoint

String

Checkpoint 名称，格式为 `checkpoint-{step编号}`。

> 语音合成模型（如 CosyVoice）的 step 编号由 LM epoch 和 FM epoch 组合而成，例如 `checkpoint-00040004` 表示 LM 第 4 轮 + FM 第 4 轮。

output\[\*\].job\_id

String

该 Checkpoint 所属的调优任务 ID。

output\[\*\].step

Integer

Checkpoint 对应的训练步数编码。

> 语音合成模型（如 CosyVoice）的 step 计算方式为 `LM_epoch × 10000 + FM_epoch`，例如 40004 表示 LM 第 4 轮 + FM 第 4 轮。

output\[\*\].status

String

该 Checkpoint 的状态。常见值：`SUCCEEDED`（已就绪，可用于部署）、`PENDING`（尚未就绪）。

output\[\*\].model\_name

String

该 Checkpoint 对应的模型 ID，可作为[部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)接口的 `model_name` 入参。**仅在**`status=SUCCEEDED`**时返回**。

output\[\*\].model\_display\_name

String

模型显示名（控制台展示用）。仅在 `status=SUCCEEDED` 时返回。

output\[\*\].create\_time

String

该 Checkpoint 的创建时间，格式为 ISO 8601。

output\[\*\].expire\_time

String

该 Checkpoint 的过期时间，格式为 ISO 8601。

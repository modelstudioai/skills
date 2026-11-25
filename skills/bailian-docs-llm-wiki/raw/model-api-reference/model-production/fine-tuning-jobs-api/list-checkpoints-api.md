# Checkpoint 管理

管理调优任务产出的 Checkpoint：列举、导出、查询验证结果，及 Checkpoint 对象说明。

<a id="适用范围"></a>

<a id="scope-h2"></a>

## 适用范围

-   **适用地域**：本文描述的功能仅在华北2（北京）地域可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
    
-   **开通账号权限**：若使用[阿里云子账号](../../../model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace)。
    
-   **配置环境变量**：已成功[获取 API Key](../../preparations/get-api-key.md)，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   **接口支持的微调模型类型：**
    -   [列举 Checkpoint](list-checkpoints-api.md#51ryvkmpq074r)：文本生成、视频生成、图像生成、语音合成
    -   [导出 Checkpoint](list-checkpoints-api.md#a7k3m9x2q8r4t)：文本生成、视频生成、图像生成、语音合成
    -   [查询Checkpoint验证列表](list-checkpoints-api.md#d5cd230b48sab)：视频生成、图像生成
    -   [查询Checkpoint验证结果](list-checkpoints-api.md#09c9c6eb85lxz)：视频生成、图像生成

<a id="列举-checkpoint"></a>

<a id="51ryvkmpq074r"></a>

## 列举 Checkpoint

列举指定调优任务产出的所有 Checkpoint 及其状态、模型信息等。

<a id="请求接口"></a>

<a id="7htlg4h3cm29q"></a>

### 请求接口

<a id="code-block"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/checkpoints
```

<a id="入参描述"></a>

<a id="lcp-h3-input"></a>

### 入参描述

| 字段 | 传参方式 | 类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| job\_id | Path parameter | string | 是 | 调优任务ID，可通过[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)或列举训练任务接口获取。 | ft-202511111122-xxxx |

<a id="出参描述"></a>

<a id="o1ja9kgfy5hl7"></a>

### 出参描述

<table><thead><tr><th><strong>字段</strong></th><th><strong>类型</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求的唯一标识符。</p></td><td><p>aa4b0229-b1db-9afa-bb6e-xxxxxxxxx</p></td></tr><tr><td><p>output</p></td><td><p>array[object]</p></td><td><p>Checkpoint 数组。按 step 从大到小排序。</p><blockquote><p>语音合成模型（如 CosyVoice）的 step 由 LM epoch 与 FM epoch 组合而成，排序按 LM epoch × FM epoch 的乘积从大到小（乘积越大代表双端调优越充分）。</p></blockquote></td><td><ul><li></li></ul></td></tr><tr><td><p>output[].checkpoint_id</p></td><td><p>string</p></td><td><p>Checkpoint 唯一标识，格式为 <code>{job_id}:checkpoint-{step编号}</code>。不同模型类型的 step 编号格式不同，详见 <code>step</code> 字段说明。</p></td><td><p>ft-202605271743-dd2a:checkpoint-00040004</p></td></tr><tr><td><p>output[].full_name</p></td><td><p>string</p></td><td><p>同 <code>checkpoint_id</code>。</p></td><td><p>ft-202605271743-dd2a:checkpoint-00040004</p></td></tr><tr><td><p>output[].checkpoint</p></td><td><p>string</p></td><td><p>Checkpoint 名称，格式为 <code>checkpoint-{step编号}</code>。</p><blockquote><p>语音合成模型（如 CosyVoice）的 step 编号由 LM epoch 和 FM epoch 组合而成，例如 <code>checkpoint-00040004</code> 表示 LM 第 4 轮 + FM 第 4 轮。</p></blockquote></td><td><p>checkpoint-00040004</p></td></tr><tr><td><p>output[].job_id</p></td><td><p>string</p></td><td><p>该 Checkpoint 所属的调优任务 ID。</p></td><td><p>ft-202605271743-dd2a</p></td></tr><tr><td><p>output[].step</p></td><td><p>integer</p></td><td><p>Checkpoint 对应的训练步数编码。</p><blockquote><p>语音合成模型（如 CosyVoice）的 step 计算方式为 <code>LM_epoch × 10000 + FM_epoch</code>，例如 40004 表示 LM 第 4 轮 + FM 第 4 轮。</p></blockquote></td><td><p>40004</p></td></tr><tr><td><p>output[].status</p></td><td><p>string</p></td><td><p>该 Checkpoint 的状态。常见值：<code>SUCCEEDED</code>（已就绪，可用于部署）、<code>PENDING</code>（尚未就绪）。</p></td><td><p>SUCCEEDED</p></td></tr><tr><td><p>output[].model_name</p></td><td><p>string</p></td><td><p>该 Checkpoint 对应的模型 ID，可作为<a href="../deployments-api/model-deployment-text-generation-api/create-deployment-api.md">部署模型</a>接口的 <code>model_name</code> 入参。<strong>仅在</strong><code>status=SUCCEEDED</code><strong>时返回</strong>。</p></td><td><p>cosyvoice-v3-flash-ft-202605271743-dd2a</p></td></tr><tr><td><p>output[].model_display_name</p></td><td><p>string</p></td><td><p>模型显示名（控制台展示用）。仅在 <code>status=SUCCEEDED</code> 时返回。</p></td><td><p>ft-202605271743-dd2a</p></td></tr><tr><td><p>output[].create_time</p></td><td><p>string</p></td><td><p>该 Checkpoint 的创建时间，格式为 ISO 8601。</p></td><td><p>2026-05-27T18:07:16</p></td></tr><tr><td><p>output[].expire_time</p></td><td><p>string</p></td><td><p>该 Checkpoint 的过期时间，格式为 ISO 8601。</p></td><td><p>2026-06-11T18:07:16</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="lcp-h3-reqex"></a>

### 请求示例

请将 URL 中的 `<替换为调优任务job_id>` 完整替换为[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)输出参数`job_id`的值。

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

<a id="code-block-2"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/checkpoints' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

<a id="响应示例"></a>

<a id="yoj2qdrstg8m7"></a>

### 响应示例

<a id="code-block-3"></a>

```json
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

<a id="导出-checkpoint"></a>

<a id="a7k3m9x2q8r4t"></a>

## 导出 Checkpoint

将指定 Checkpoint 导出为可部署模型。导出成功后，需根据模型类型调用对应的[部署接口](../deployments-api.md)（不同模型类型的部署接口不同）。

<a id="请求接口-2"></a>

<a id="660dd7600bnl4"></a>

### 请求接口

<a id="code-block-4"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/export/{checkpoint}?model_name={model_name}
```

<a id="入参描述-2"></a>

<a id="61f9eb431f29b"></a>

### 入参描述

| 字段 | 传参方式 | 类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| job\_id | Path parameter | string | 是 | 调优任务ID，可通过[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)或列举训练任务接口获取。 | ft-202511111122-xxxx |
| checkpoint | Path parameter | string | 是 | Checkpoint名称，可通过列举Checkpoint接口获取。 | checkpoint-160 |
| model\_name | Query parameter | string | 是 | 用于在控制台中展示的导出模型名称。<br><br>该名称需全局唯一，建议使用中英文、数字、下划线（\_）和短横线（-）字符。<br><br>请注意：此参数仅用于控制台显示，实际导出的模型名称以列举 Checkpoint输出参数`output[].model_name`为准。 | wan2.5-i2v-preview-ft-202511111122-xxxx |

<a id="出参描述-2"></a>

<a id="8d2a1f7722aek"></a>

### 出参描述

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求的唯一标识符。</p></td><td><p>0eb05b0c-02ba-414a-9d0c-xxxxxxxxx</p></td></tr><tr><td><p>output</p></td><td><p>boolean</p></td><td><p>导出请求是否提交成功。</p><ul><li><p>true：表示导出请求提交成功。</p></li><li><p>false：表示导出请求提交失败，建议重试。</p></li></ul></td><td><p>true</p></td></tr></tbody></table>

<a id="请求示例-2"></a>

<a id="95084f5ca8rbv"></a>

### 请求示例

-   `<替换为调优任务job_id>`：完整替换为[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)输出参数`job_id`的值。
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如“checkpoint-160”。
-   `<替换为控制台展示的导出模型名称>`：完整替换为自定义的模型名称，仅用于控制台展示。

<a id="code-block-5"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/export/<替换为待导出的checkpoint>?model_name=<替换为控制台展示的导出模型名称>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="响应示例-2"></a>

<a id="7f48f5ef53zqy"></a>

### 响应示例

<a id="code-block-6"></a>

```json
{
    "request_id": "0817d1ed-b6b6-4383-9650-xxxxx",
    "output": true
}
```

<a id="查询checkpoint验证列表"></a>

<a id="d5cd230b48sab"></a>

## 查询Checkpoint验证列表

> **说明**
>
> 文本生成模型不支持此接口。

查询通过验证集成功生成预览视频或图像的 Checkpoint 列表，验证失败的不会列出。

**使用限制**：该接口需在模型调优完成后调用，否则将返回空列表。

<a id="请求接口-3"></a>

<a id="d2e05f2b54nge"></a>

### 请求接口

<a id="code-block-7"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/validation-results
```

<a id="入参描述-3"></a>

<a id="d1f7c4ceb44y5"></a>

### 入参描述

| 字段 | 传参方式 | 类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| job\_id | Path parameter | string | 是 | 调优任务ID，可通过[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)或列举训练任务接口获取。 | ft-202511111122-xxxx |

<a id="出参描述-3"></a>

<a id="d4895c3b00e23"></a>

### 出参描述

| 字段 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| request\_id | string | 请求的唯一标识符。 | 0eb05b0c-02ba-414a-9d0c-xxxxxxxxx |
| output | array\[string\] | Checkpoint列表。 | \- |
| output\[\].checkpoint | string | Checkpoint名称。 | checkpoint-160 |

<a id="请求示例-3"></a>

<a id="b7fcd7371av2m"></a>

### 请求示例

请将 URL 中的 `<替换为调优任务job_id>` 完整替换为[创建训练任务](../../../_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)输出参数`job_id`的值。

<a id="code-block-8"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/validation-results' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

<a id="响应示例-3"></a>

<a id="55f33732fcibs"></a>

### 响应示例

<a id="code-block-9"></a>

```json
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

<a id="查询checkpoint验证结果"></a>

<a id="09c9c6eb85lxz"></a>

## 查询Checkpoint验证结果

> **说明**
>
> 文本生成模型不支持此接口。

根据 `checkpoint`（例如 "checkpoint-160"），查询指定 Checkpoint 的验证结果详情，包括生成的预览视频或图像。

<a id="请求接口-4"></a>

<a id="f8c67434d6fo4"></a>

### 请求接口

<a id="code-block-10"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/validation-details/{checkpoint}?page_no=1&page_size=10
```

<a id="入参描述-4"></a>

<a id="eb3da6ffc3xrq"></a>

### 入参描述

| 字段 | 传参方式 | 类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| job\_id | Path parameter | string | 是 | 调优任务ID，可通过创建训练任务或列举训练任务接口获取。 | ft-202511111122-xxxx |
| checkpoint | Path parameter | string | 是 | Checkpoint名称，可通过列举 Checkpoint 或查询Checkpoint验证列表接口获取。 | checkpoint-160 |
| page\_no | Query parameter | integer | 否 | 页码。默认为1。 | 1 |
| page\_size | Query parameter | integer | 否 | 每页数量。默认为10。 | 10 |

<a id="出参描述-4"></a>

<a id="ca68f349d78mu"></a>

### 出参描述

| 字段 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| request\_id | string | 请求的唯一标识符。 | 375b3ad0-d3fa-451f-b629-xxxxxxx |
| output | object | 输出结果。 | \- |
| output.page\_no | integer | 页码。 | 1 |
| output.page\_size | integer | 每页数量。 | 10 |
| output.total | integer | 验证集列表总数量。 | 1 |
| output.list | array\[object\] | 验证集列表。 | \- |
| output.list\[\].video\_path | string | 通过Checkpoint生成的视频。<br><br>video\_path有效期为24小时，请及时下载视频。 | [https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx](https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx) |
| output.list\[\].prompt | string | 验证数据的prompt。从数据集的标注文件data.jsonl获得。 | 视频开头展示了一位年轻男性坐在咖啡馆的场景... |
| output.list\[\].first\_frame\_path | string | 验证的图像地址。系统会读取数据集中的图像，并生成一个公网URL地址。 | [https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg](https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg) |

<a id="请求示例-4"></a>

<a id="0a3269f27c7bx"></a>

### 请求示例

-   `<替换为调优任务job_id>`： 完整替换为创建训练任务输出参数`job_id`的值。
-   `<替换为选择的checkpoint>`：完整替换为选定的Checkpoint名称，例如“checkpoint-160”。

<a id="code-block-11"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为调优任务job_id>/validation-details/<替换为选择的checkpoint>?page_no=1&page_size=10' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="响应示例-4"></a>

<a id="ad1335d3f4v9d"></a>

### 响应示例

> video\_path有效期为24小时，请及时下载视频。

<a id="code-block-12"></a>

```json
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

<a id="checkpoint-对象"></a>

<a id="c4d5m7n9p1q3t"></a>

## Checkpoint 对象

> 当前 Checkpoint API 仅在北京 Region 开放。如您使用其他 Region，请通过该 Region 的百炼控制台管理 Checkpoint。

检查点对象（Checkpoint）表示调优过程中保存的中间模型状态。通过列举检查点接口返回。

<a id="字段说明"></a>

<a id="204f3d1mpqi7f"></a>

### 字段说明

以下字段来自列举检查点接口的返回结果。

<table><thead><tr><th><strong>参数名称</strong></th><th><strong>类型</strong></th><th><strong>参数说明</strong></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的ID。</p></td></tr><tr><td><p>output</p></td><td><p>Array</p></td><td><p>Checkpoint 数组。按 step 从大到小排序。</p><blockquote><p>语音合成模型（如 CosyVoice）的 step 由 LM epoch 与 FM epoch 组合而成，排序按 LM epoch × FM epoch 的乘积从大到小（乘积越大代表双端调优越充分）。</p></blockquote></td></tr><tr><td><p>output[*].checkpoint_id</p></td><td><p>String</p></td><td><p>Checkpoint 唯一标识，格式为 <code>{job_id}:checkpoint-{step编号}</code>。不同模型类型的 step 编号格式不同，详见 <code>step</code> 字段说明。</p></td></tr><tr><td><p>output[*].full_name</p></td><td><p>String</p></td><td><p>同 <code>checkpoint_id</code>。</p></td></tr><tr><td><p>output[*].checkpoint</p></td><td><p>String</p></td><td><p>Checkpoint 名称，格式为 <code>checkpoint-{step编号}</code>。</p><blockquote><p>语音合成模型（如 CosyVoice）的 step 编号由 LM epoch 和 FM epoch 组合而成，例如 <code>checkpoint-00040004</code> 表示 LM 第 4 轮 + FM 第 4 轮。</p></blockquote></td></tr><tr><td><p>output[*].job_id</p></td><td><p>String</p></td><td><p>该 Checkpoint 所属的调优任务 ID。</p></td></tr><tr><td><p>output[*].step</p></td><td><p>Integer</p></td><td><p>Checkpoint 对应的训练步数编码。</p><blockquote><p>语音合成模型（如 CosyVoice）的 step 计算方式为 <code>LM_epoch × 10000 + FM_epoch</code>，例如 40004 表示 LM 第 4 轮 + FM 第 4 轮。</p></blockquote></td></tr><tr><td><p>output[*].status</p></td><td><p>String</p></td><td><p>该 Checkpoint 的状态。常见值：<code>SUCCEEDED</code>（已就绪，可用于部署）、<code>PENDING</code>（尚未就绪）。</p></td></tr><tr><td><p>output[*].model_name</p></td><td><p>String</p></td><td><p>该 Checkpoint 对应的模型 ID，可作为<a href="../deployments-api/model-deployment-text-generation-api/create-deployment-api.md">部署模型</a>接口的 <code>model_name</code> 入参。<strong>仅在</strong><code>status=SUCCEEDED</code><strong>时返回</strong>。</p></td></tr><tr><td><p>output[*].model_display_name</p></td><td><p>String</p></td><td><p>模型显示名（控制台展示用）。仅在 <code>status=SUCCEEDED</code> 时返回。</p></td></tr><tr><td><p>output[*].create_time</p></td><td><p>String</p></td><td><p>该 Checkpoint 的创建时间，格式为 ISO 8601。</p></td></tr><tr><td><p>output[*].expire_time</p></td><td><p>String</p></td><td><p>该 Checkpoint 的过期时间，格式为 ISO 8601。</p></td></tr></tbody></table>

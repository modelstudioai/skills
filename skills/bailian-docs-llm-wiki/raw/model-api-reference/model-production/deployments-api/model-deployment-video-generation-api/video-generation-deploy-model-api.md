# 视频生成-部署模型

将训练好的模型发布为在线 API 服务。

## 适用范围

-   **适用地域**：当前模型部署 API **仅在华北2（北京）地域**开放。如您使用其他地域，请通过该地域的百炼控制台完成模型部署操作。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](raw/model-api-reference/preparations/get-api-key.md)。
-   **前提条件**：已完成模型微调训练。请先调用[查询调优任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)接口，确认任务状态 `status` 为 **SUCCEEDED** 后再进行部署。

## 部署模型

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/deployments`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

### 请求参数

##### 请求头（Headers）

**Content-Type** `string` **（必选）**

固定值：`application/json`

**Authorization** `string` **（必选）**

API Key鉴权，格式为`Bearer sk-xxxx`。

##### 请求体（Request Body）

**model\_name** `string` **（必选）**

待部署的模型ID（非基础模型名称，而是微调或导出后生成的模型标识）。获取方式：

-   微调产出的模型：使用[创建调优任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)响应中 `output.finetuned_output` 的值，格式如 `wan2.5-i2v-preview-ft-202511111122-xxxx`。
-   导出的模型：使用[查询导出的模型详情](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)响应中 `output[].model_name` 的值。

**capacity** `integer` **（必选）**

部署的模型实例数量。推荐设置为1。

**plan** `string` **（必选）**

部署方式。LoRA高效微调推荐为`lora`。

**aigc\_config** `object` **（必选）**

提示词配置。

aigc\_config 属性

**use\_input\_prompt** `boolean` **（必选）**

控制调用已部署模型生成视频时的提示词来源。

-   `false`（默认值）：自动生成模式。调用视频生成接口时，系统忽略传入的 prompt，强制使用 `aigc_config.prompt` 和 `aigc_config.lora_prompt_default` 配置的模板自动生成提示词。
-   `true`：手动传入模式。调用视频生成接口时，系统直接使用传入的 prompt，上述两个参数将全部失效。

**prompt** `string` **（必选）**

预设的Prompt模板。仅在`use_input_prompt=false`时生效。

调用已部署模型生成视频时，系统会分析输入图像，将画面内容填入该模板，自动生成带特效指令的完整描述。

注意：此参数会**覆盖**视频生成接口中传入的 prompt 参数。

**lora\_prompt\_default** `string` **（必选）**

备用Prompt模板。仅在`use_input_prompt=false`时生效。

当使用`aigc_config.prompt`生成失败时，系统将使用此参数作为兜底提示词来生成视频。

#### 图生视频-基于首帧

以下示例以金钱雨特效为例，上传一张人物图片，系统自动生成带有特效的视频。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "aigc_config": {
        "use_input_prompt": false,
        "prompt": "根据图像内容提供视频描述，描述必须包含"然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中"。\n输出模板:\n视频开头展示了[主体描述]。[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。\n示例:\n视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "lora_prompt_default": "然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕主角。钞票持续落下，同时镜头缓缓拉进，主角双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。"
    },
    "capacity": 1,
    "plan": "lora"
}'
```

#### 图生视频-基于首尾帧

以下示例以时尚杂志换装特效为例，上传首帧和尾帧图片，系统自动生成人物换装变身的过渡视频。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "aigc_config": {
        "use_input_prompt": false,
        "prompt": "根据图像内容提供视频描述，描述必须包含"然后她开始了s86b5p变身。"\n输出模板:\n视频开头展示了[主体描述]。[环境描述]。然后她开始了s86b5p变身。\n示例:\n视频开头展示了一位年轻女性在户外的场景。她有着短而卷曲的深棕色头发，面带微笑，显得非常亲切。她穿着一件黑色的Polo衫，上面有彩色的花卉刺绣图案，背景是绿色的植被和远处的山脉。然后她开始了s86b5p变身。",
        "lora_prompt_default": "然后她开始了s86b5p变身。"
    },
    "capacity": 1,
    "plan": "lora"
}'
```

### 响应参数

**request\_id** `string`

请求的唯一标识符。

**output** `object`

任务详情。

属性

**deployed\_model** `string`

部署模型的唯一标识。用于查询模型部署状态和调用模型。

**model\_name** `string`

模型标识名。

**status** `string`

部署状态：

-   `PENDING`：部署中。
-   `RUNNING`：运行中。
-   `FAILED`：部署失败。

**base\_model** `string`

使用的基准模型。

**gmt\_create** `string`

部署任务创建时间。

**gmt\_modified** `string`

部署任务更新时间。

**workspace\_id** `string`

阿里云百炼API Key所属的业务空间ID。请参见[获取Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

**charge\_type** `string`

付费模式。post\_paid表示后付费。

**creator** `string`

创建人的阿里云账号ID。

**modifier** `string`

修改人的阿里云账号ID。

**plan** `string`

部署方式。

**code** `string`

错误码。调用失败时返回。请参见下方错误码表。

**message** `string`

错误详情描述。调用失败时返回。

#### 成功响应示例

重点关注：`output.deployed_model`（部署模型的唯一标识）、`output.status`（部署状态）。

```
{
    "request_id": "96020b2e-9072-4c8a-9981-xxxxxxxxx",
    "output": {
        "deployed_model": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "gmt_create": "2025-11-11T17:46:53.294",
        "gmt_modified": "2025-11-11T17:46:53.294",
        "status": "PENDING",
        "model_name": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "base_model": "wan2.5-i2v-preview",
        "workspace_id": "llm-xxxxxxxxx",
        "charge_type": "post_paid",
        "creator": "12xxxxxxx",
        "modifier": "12xxxxxxx",
        "plan": "lora"
    }
}
```

#### 错误响应示例

```
{
    "code": "InvalidParameter",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "The model xxx does not exist or is not deployable"
}
```

## Prompt 模板配置

以下说明如何配置 `aigc_config.prompt` 参数。

-   **为什么要设置这个参数**？
    
    如果不设置此参数，每次调用已部署模型都需要手动编写完整 Prompt；设置后，调用微调模型生成视频时，只需上传图片，系统会根据此参数自动补全特效指令，无需手动输入 Prompt。
    
-   **如何设置？** **Prompt = 任务指令（告诉模型要做什么）+ 输出模板（规范输出格式）+ 示例（让模型学习示例结构）。**

```
根据图像内容提供视频描述，描述必须包含"然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中"。
输出模版:
视频开头展示了[主体描述]。[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
示例:
视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
```

> 关于"输出模板"描述，请参见[视频标注：为视频编写Prompt](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-guide#102ebee9f3dtq)。

## 下一步

部署为异步操作，调用本接口后可通过[查询和管理部署](raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)接口查询部署状态。

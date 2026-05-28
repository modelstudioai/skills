# 微调视频生成模型

当使用万相进行**图生视频**时，若通过[Prompt 优化](https://help.aliyun.com/zh/model-studio/text-to-video-prompt)或调用[官方视频特效](https://help.aliyun.com/zh/model-studio/wanx-video-effects)仍无法满足对**特定动作、特效或风格**的定制需求，请使用**模型微调**。

## **适用范围**

-   **适用部署模式及地域**：本文档仅适用于[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/)下的北京地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   **开通账号权限**：若使用[阿里云子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。
    
-   **支持微调的方式**：SFT-LoRA高效微调。
    
-   **支持微调的模型**：
    
    -   图生视频-基于首帧：wan2.5-i2v-preview、wan2.2-i2v-flash。
        
    -   图生视频-基于首尾帧：wan2.2-kf2v-flash。
        

## **如何微调模型**

## 图生视频-基于首帧

**微调目标：训练一个“金钱雨特效”LoRA模型**。

预期效果：输入一张首帧图像，无需提示词，模型自动生成一段带有“金钱雨特效”的视频。

**输入首帧图像**

![image\_3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7956213671/p1024075.jpeg)

**输出视频（微调前）**

> 无法通过提示词每次生成固定运动的“金钱雨”特效（运动画面不可控）。

**输出视频（微调后）**

> 微调后的模型无需提示词即能稳定复现训练集中的特定“金钱雨”特效。

## 图生视频-基于首尾帧

**微调目标：训练一个“时尚杂志特效”LoRA模型。**

预期效果：输入一张首帧和尾帧图像，无需提示词，模型自动生成一段带有“时尚杂志特效”的视频。

**输入首帧图像**

![3\_first](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7886038671/p1043393.jpg)

**输入尾帧图像**

![3\_last](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7886038671/p1044358.jpg)

**输出视频（微调前）**

> 无法通过提示词每次生成固定运动的“时尚杂志”特效（运动画面不可控）。

**输出视频（微调后）**

> 微调后的模型无需提示词即能稳定复现训练集中的特定“时尚杂志”特效。

运行下述代码前，请[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并[配置API Key](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

### **步骤1：上传数据集**

将本地的数据集（.zip 格式）上传到阿里云百炼平台，并获取文件 ID (`**file_id**`)。

训练集样例数据：格式请参见[训练集](#d2dc0825ca6fv)。

-   图生视频-基于首帧：[wan-i2v-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ujfrui/wan-i2v-training-dataset.zip)。
    
-   图生视频-基于首尾帧：[wan-kf2v-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/wapfil/wan-kf2v-training-dataset.zip)。
    

**请求示例**

> 本示例使用图生视频-基于首帧模型，仅上传训练集，系统将自动从训练集中划分一部分作为验证集。

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'files=@"./wan-i2v-training-dataset.zip"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="a fine-tune training data file for wan"'
```

**响应示例**

请保存 `file_id`，这是上传数据集的唯一标识。

```
{
    "data": {
        "uploaded_files": [
            {
                "name": "wan-i2v-training-dataset.zip",
                "file_id": "3bff1ef7-f72d-4285-bb75-xxxxxx"
            }
        ],
        "failed_uploads": []
    },
    "request_id": "1f3f1c5b-7418-4976-aaea-xxxxxx"
}
```

### **步骤2：微调模型**

##### **步骤2.1 创建微调任务**

使用步骤1中的文件ID启动训练任务。

**说明**

不同模型的微调参数的值有所差异，超参数设置请参见[超参数](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#5f391e4b3cezf)，更多调用示例请参见[请求示例](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#1a9196bd16o9h)。

**请求示例**

请将`<替换为训练数据集的文件id>`完整替换为上一步获取的`file_id`。

## 图生视频-基于首帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model":"wan2.5-i2v-preview",
    "training_file_ids":[
        "<替换为训练数据集的文件id>"
    ],
    "training_type":"efficient_sft",
    "hyper_parameters":{
        "n_epochs":400,
        "batch_size":2,
        "learning_rate":2e-5,
        "split":0.9,
        "eval_epochs": 20,
        "max_pixels": 36864
    }
}'
```

## 图生视频-基于首尾帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model":"wan2.2-kf2v-flash",
    "training_file_ids":[
        "<替换为训练数据集的文件id>"
    ],
    "training_type":"efficient_sft",
    "hyper_parameters":{
        "n_epochs":400,
        "batch_size":4,
        "learning_rate":2e-5,
        "split":0.9,
        "eval_epochs": 20,
        "max_pixels": 262144
    }
}'
```

**响应示例**

关注 `output` 中的三个关键参数：

-   `job_id`：任务ID，用于查询进度。
    
-   `finetuned_output`：微调后的新模型名称，后续部署和调用时必须使用此名称。
    
-   `status`：模型训练状态。创建微调任务后，初始状态为PENDING，表示训练待开始。
    

```
{
    ...
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "status": "PENDING",
        "finetuned_output": "xxxx-ft-202511111122-xxxx",
        ...
    }
}
```

##### **步骤2.2 查询微调任务状态**

通过步骤2.1获得的 `job_id` 查询任务进度，轮询以下接口直到 `status` 变为 **SUCCEEDED**。

**说明**

本文示例的微调任务训练需要**数小时**，具体耗时根据微调模型而定，请耐心等待。

**请求示例**

请将 URL 中的 `<替换为微调任务job_id>` 完整替换为`job_id`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

关注`output` 字段的两个参数：

-   `status`：当它的值变为 **SUCCEEDED** 时，表示模型已训练完毕，可以进行模型部署。
    
-   `usage`：模型训练消耗的总Token数量，用于模型训练计费。
    

```
{
    ...
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "status": "SUCCEEDED",
        "usage": 432000,
        ...
    }
}
```

### **步骤3：部署微调后的模型**

##### **步骤3.1 部署模型为在线服务**

当微调任务的状态为 **SUCCEEDED** 后，将模型部署为在线服务。

**请求示例**

请将`<替换为模型名称model_name>` 完整替换为[创建微调任务](#bc825b6ec11y2)的输出参数`finetuned_output`的值。

## 图生视频-基于首帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "aigc_config": {
        "use_input_prompt": false,
        "prompt": "根据图像内容提供视频描述，描述必须包含“然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中”。\n输出模板:\n视频开头展示了[主体描述模板[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。\n示例:\n视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "lora_prompt_default": "然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕主角。钞票持续落下，同时镜头缓缓拉进，主角双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。"
    },
    "capacity": 1,
    "plan": "lora"
}'
```

## 图生视频-基于首尾帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "aigc_config": {
        "use_input_prompt": false,
        "prompt": "根据图像内容提供视频描述，描述必须包含“然后她开始了s86b5p变身。”\n输出模板:\n视模板头展示了[主体描述]。[环境描述]。然后她开始了s86b5p变身。\n示例:\n视频开头展示了一位年轻女性在户外的场景。她有着短而卷曲的深棕色头发，面带微笑，显得非常亲切。她穿着一件黑色的Polo衫，上面有彩色的花卉刺绣图案，背景是绿色的植被和远处的山脉。然后她开始了s86b5p变身。",
        "lora_prompt_default": "然后她开始了s86b5p变身。"
    },
    "capacity": 1,
    "plan": "lora"
}'
```

**响应示例**

关注 `output` 中的两个参数：

-   `deployed_model`：部署的模型名称，用于查询部署状态和调用模型。
    
-   `status`：模型部署状态。部署微调模型后，初始状态为PENDING，表示部署未开始。
    

```
{
    ...
    "output": {
        "deployed_model": "xxxx-ft-202511111122-xxxx",
        "status": "PENDING",
        ...
    }
}
```

##### **步骤3.2 查询部署状态**

查询部署状态，轮询以下接口直到 `status` 变为 **RUNNING**。

**说明**

本文示例的微调模型，部署过程预计需要 **5～10分钟**。

**请求示例**

请将`<替换为deployed_model>`完整替换为步骤3.1输出参数`deployed_model`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为deployed_model>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

关注`output`字段的两个参数：

-   `status`：当状态变为 **RUNNING** 时，表示模型已部署成功，可以开始调用。
    
-   `deployed_model`：部署的模型名称。
    

```
{
    ...
    "output": {
        "status": "RUNNING",
        "deployed_model": "xxxx-ft-202511111122-xxxx",
        ...
    }
}
```

### **步骤4：**调用模型生成视频

模型部署成功后（即部署状态`status`为 **RUNNING** ），即可发起调用。

**步骤4.1：创建视频生成任务，并获取task\_id**

**请求示例**

请将`<替换为部署名称deployed_model>`完整替换为上一步输出的`deployed_model`值。

## 图生视频-基于首帧

**预期效果**：输入一张首帧图像，无需提示词，模型自动根据图像生成一段带有“金钱雨特效”的视频。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--header 'X-DashScope-Async: enable' \
--data '{
    "model": "<替换为部署名称deployed_model>",
    "input": {
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251219/imnlba/lora.webp"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": false
    }
}'
```

**响应示例**

请复制并保存`task_id`，用于下一步结果查询。

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

**输入参数说明**

**说明**

调用微调后的 LoRA 模型时，输入参数用法基本与[图生视频-基于首帧API](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/) 一致。

下表仅列出 LoRA 模型**特有的参数用法或特定限制**。对于未在下表中提及的通用参数（例如 `duration`），请参照 API 文档进行设置。

**字段**

**类型**

**必选**

**描述**

**示例值**

model

string

是

模型名称。

必须使用已成功部署且部署状态为RUNNING的微调模型。

xxxx-ft-202511111122-xxxx

input.prompt

string

否

文本提示词。

此参数是否生效，取决于[aigc\_config.use\_input\_prompt](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#8e783d6f60i7l) 的配置：

-   当`use_input_prompt=true`时：此参数生效。系统将根据这段提示词来生成视频。
    
-   当`use_input_prompt=false`时：此参数会被忽略。系统将使用预置模板[aigc\_config.prompt](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#8e783d6f60i7l)自动生成提示词。
    

\-

input.img\_url

string

是

首帧图像URL。

传入方式请参见[img\_url参数](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)。

https://help-static-aliyun-doc.aliyuncs.com/xxx.jpg

parameters.resolution

string

否

生成的视频分辨率档位。

wan2.2和wan2.5模型：480P、720P。默认值为720P。

。

720P

parameters.prompt\_extend

boolean

否

是否开启prompt智能改写。

调用微调的LoRA模型时，建议关闭，即设置为false。

false

## 图生视频-基于首尾帧

**预期效果**：输入一张首帧和尾帧图像，无需提示词，模型自动根据图像生成一段带有“时尚杂志特效”的视频。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--header 'X-DashScope-Async: enable' \
--data '{
    "model": "<替换为部署名称deployed_model>",
    "input": {
        "first_frame_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260113/typemn/kf2v-first.webp",
        "last_frame_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260113/ekzmff/kf2v_last.webp"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": false
    }
}'
```

**响应示例**

请复制并保存`task_id`，用于下一步结果查询。

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

**输入参数说明**

**说明**

调用微调后的 LoRA 模型时，输入参数用法基本与[图生视频-基于首尾帧API](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-by-first-and-last-frame-api-reference)一致。

下表仅列出 LoRA 模型**特有的参数用法或特定限制**。对于未在下表中提及的通用参数（例如 `duration`），请参照 API 文档进行设置。

**字段**

**类型**

**必选**

**描述**

**示例值**

model

string

是

模型名称。

必须使用已成功部署且状态为RUNNING的微调模型。

xxxx-ft-202511111122-xxxx

input.prompt

string

否

文本提示词。

此参数是否生效，取决于[aigc\_config.use\_input\_prompt](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#8e783d6f60i7l) 的配置：

-   当`use_input_prompt=true`时：此参数生效。系统将根据这段提示词来生成视频。
    
-   当`use_input_prompt=false`时：此参数会被忽略，无需传入。系统将使用预置模板[aigc\_config.prompt](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#8e783d6f60i7l)自动生成提示词。
    

\-

input.first\_frame\_url

string

是

首帧图像URL。

传入方式请参见[first\_frame\_url参数](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)。

https://help-static-aliyun-doc.aliyuncs.com/xxx.jpg

input.last\_frame\_url

string

否

尾帧图像URL。

传入方式请参见[last\_frame\_url参数](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)。

https://help-static-aliyun-doc.aliyuncs.com/xxx.jpg

parameters.resolution

string

否

生成的视频分辨率档位。

微调模型支持 480P、720P。默认值为720P。

720P

parameters.prompt\_extend

boolean

否

是否开启prompt智能改写。

调用微调的LoRA模型时，建议关闭，即设置为false。

false

**步骤4.2：根据task\_id查询结果**

使用`task_id`轮询任务状态，直到 `task_status` 变为 SUCCEEDED，并获取视频URL。

**请求示例**

> 请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

> 视频URL有效期为24小时，请及时下载视频。

```
{
    "request_id": "c87415d2-f436-41c3-9fe8-xxxxxx",
    "output": {
        "task_id": "a017e64c-012b-431a-84fd-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-11-12 11:03:33.672",
        "scheduled_time": "2025-11-12 11:03:33.699",
        "end_time": "2025-11-12 11:04:07.088",
        "orig_prompt": "",
        "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxxx"
    },
    "usage": {
        "duration": 5,
        "video_count": 1,
        "SR": 480
    }
}
```

## **构建自定义数据集**

除了使用本文示例数据体验微调流程外，您也可以构建自己的数据集进行微调。

数据集应包含 **训练集**（必须）和 **验证集**（可选，支持从训练集自动划分）。所有文件请打包为`**.zip**` 格式，文件名建议仅使用英文、数字、下划线或短横线。

### **数据集格式**

#### **训练集：必须提供**

## 图生视频-基于首帧

训练集包括**首帧图像、训练视频和标注文件（data.jsonl）**。

-   训练集样例：[wan-i2v-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ujfrui/wan-i2v-training-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-i2v-training-dataset.zip
    ├── data.jsonl        # 必须固定命名为data.jsonl，最大支持 20MB
    ├── image_1.jpeg      # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
    ├── video_1.mp4       # 视频最大分辨率为4096*4096，支持MP4、MOV格式
    ├── image_2.jpeg
    └── video_2.mp4
    ```
    
-   标注文件（data.jsonl）：每一行代表一条训练数据，必须为JSON 对象。一行训练数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻女性站在一堵爬满常春藤的砖墙前。她有着一头柔顺的红棕色长发，穿着一件白色的无袖连衣裙，佩戴着一条闪亮的银色项链，面带微笑。背景中的砖墙被绿色的藤蔓覆盖，显得古朴而自然。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "first_frame_path": "image_1.jpg",
        "video_path": "video_1.mp4"        
    }
    ```
    

## 图生视频-基于首尾帧

训练集包括**首帧图像、尾帧图像、训练视频和标注文件（data.jsonl）**。

-   训练集样例：[wan-kf2v-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/wapfil/wan-kf2v-training-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-kf2v-training-dataset.zip
    ├── data.jsonl                # 必须固定命名为data.jsonl，最大支持 20MB
    ├── image/                    # 存放首帧和尾帧图像
    │   ├── image_1_first.jpg     # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
    │   └── image_1_last.png
    └── video/                    # 存放作为“训练目标”的视频文件
        ├── video_1.mp4           # 视频最大分辨率为4096*4096，支持MP4、MOV格式
        └── video_2.mov
    ```
    
-   标注文件（data.jsonl）：每一行代表一条训练数据，必须为JSON 对象。一行训练数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻女性在户外的场景。她有着短而卷曲的深棕色头发，面带微笑，显得非常亲切。她穿着一件黑色的Polo衫，上面有彩色的花卉刺绣图案，背景是绿色的植被和远处的山脉。然后她开始了s86b5p变身。",
        "first_frame_path": "image/image_1_first.jpg",
        "last_frame_path": "image/image_1_last.jpg", 
        "video_path": "video/video_1.mp4"  
    }
    ```
    

#### **验证集：可选**

## 图生视频-基于首帧

验证集包括**首帧图像和标注文件（data.jsonl）**，无需提供视频。训练任务会在每个评估节点，自动调用模型服务，使用验证集的图像和 Prompt 生成预览视频。

-   验证集样例**：**[wan-i2v-valid-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251113/iumzue/wan-i2v-valid-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-i2v-valid-dataset.zip
    ├── data.jsonl       # 必须固定命名为data.jsonl，最大支持 20MB
    ├── image_1.jpeg     # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
    └── image_2.jpeg
    ```
    
-   标注文件（data.jsonl）：每一行代表一条验证数据，必须为JSON 对象。一行验证数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻男性站在城市景观前的场景。他穿着黑白格子外套，内搭黑色连帽衫，面带微笑，神情自信。背景是夕阳下的城市天际线，远处可以看到著名的圆顶建筑和错落有致的屋顶，天空中云层密布，呈现出温暖的橙黄色调。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，同时镜头缓缓拉进，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "first_frame_path": "image_1.jpg"
    }
    ```
    

## 图生视频-基于首尾帧

验证集包括**首帧图像、尾帧图像和标注文件（data.jsonl）**，无需提供视频。训练任务会在每个评估节点，自动调用模型服务，使用验证集的图像和 Prompt 生成预览视频。

-   验证集样例：[wan-kf2v-valid-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/gjlxnm/wan-kf2v-valid-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-kf2v-valid-dataset.zip
    ├── data.jsonl                 # 必须固定命名为data.jsonl，最大支持 20MB
    └── image/                     # 存放首帧和尾帧图像
        ├── image_1_first.jpg      # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
        └── image_1_last.jpg
    ```
    
-   标注文件（data.jsonl）：每一行代表一条验证数据，必须为JSON 对象。一行验证数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻男性站在城市景观前的场景。他穿着黑白格子外套，内搭黑色连帽衫，面带微笑，神情自信。背景是夕阳下的城市天际线，远处可以看到著名的圆顶建筑和错落有致的屋顶，天空中云层密布，呈现出温暖的橙黄色调。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，同时镜头缓缓拉进，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "first_frame_path": "image/image_1_first.jpg",
        "last_frame_path": "image/image_1_last.jpg",
    }
    ```
    

### **数据规模与限制**

-   **数据量**：建议至少提供 **10条** 数据。训练数据量越大越好，推荐 20-100 条以获得稳定效果。
    
-   **Zip压缩包**：通过 API 上传时，总包大小 ≤ 1GB。
    
-   **训练图像要求**：
    
    -   图像格式支持BMP、JPEG、PNG、WEBP。
        
    -   图像分辨率 ≤ 4096×4096。
        
    -   单个图像文件大小无硬性限制（系统将自动预处理）
        
-   **训练视频要求**：
    
    -   视频格式支持 MP4、MOV。
        
    -   视频分辨率 ≤ 4096×4096。
        
    -   单个视频文件大小无硬性限制（系统将自动预处理）。
        
    -   单个视频时长：wan2.2模型 ≤ 5秒；wan2.5模型 ≤ 10秒。
        

### **数据收集和清洗**

###### **1\. 确定微调场景**

万相支持**图生视频**的微调场景包括：

-   **固定视频特效**：让模型学会某种特定的视觉变化，如旋转木马、魔法换装等。
    
-   **固定人物动作**：提升模型对特定肢体动作的复现度，如特定的舞蹈动作、武术招式。
    
-   **固定视频运镜**：复刻复杂的镜头语言，如推拉摇移、环绕拍摄等固定模板。
    

###### **2\. 获取原始素材**

-   AI 生成筛选：利用“万相”基础模型批量生成视频，再人工挑选出最符合目标效果的优质样本。这是最常用的方法。
    
-   真实拍摄：如果您的目标是追求高真实感的互动场景（如拥抱、握手等），使用实拍素材是最佳选择。
    
-   三维软件渲染：对于需要控制细节的特效或抽象动画，建议使用 3D 软件（如 Blender、C4D）制作素材。
    

###### **3\. 清洗数据**

**维度**

**正面要求**

**负面案例**

**一致性**

**核心特征必须高度统一**。

例如：训练“360度旋转”，所有视频必须都是顺时针旋转，且旋转速度基本一致。

**方向混杂**。

数据集中既有顺时针，又有逆时针。模型不知道该学哪个方向。

**多样性**

**主体与场景越丰富越好**。

覆盖不同主体（男女老少、猫狗建筑）和不同构图（远近景、俯仰拍）。同时，分辨率和长宽比应尽可能多样化。

**单一场景或主体**。

所有视频都是“穿红衣的人在白墙前旋转”。模型会误以为“红衣”和“白墙”是特效的一部分，换了衣服就不会转了。

**均衡性**

**各类型数据比例均衡**。

如果包含多种风格，数量应大致相等。

**比例严重失调**。

90%是人像视频，10%是风景视频。模型可能在生成风景视频时效果不佳。

**纯净度**

**画面干净清晰**。

使用无干扰的原始素材。

**有干扰元素**。

视频中带有字幕、台标、水印、明显的黑边或噪点。模型可能会把水印当成特效学进去_。_

**时长**

**素材时长 ≤ 目标时长**。

若期望生成5秒视频，素材最好裁剪为4-5秒。

**素材过长**。

期望生成5秒，却喂给模型8秒的素材，会导致动作学习不完整，产生截断感。

### **视频标注：为视频编写Prompt**

在数据集的标注文件（data.jsonl）中，每个视频都有对应的一段 Prompt。Prompt 是用来描述**视频**的画面内容，Prompt 的质量直接决定模型“学什么”。

**Prompt示例**

**视频开头展示了**一位年轻女性站在一堵爬满常春藤的砖墙前。她有着一头柔顺的红棕色长发，穿着一件白色的无袖连衣裙，佩戴着一条闪亮的银色项链，面带微笑。**背景是**被绿色的藤蔓覆盖的砖墙，显得古朴而自然。**然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。**

#### **Prompt编写公式**

**Prompt = \[主体描述\] + \[背景描述\] + \[触发词\] + \[运动描述\]**

**Prompt描述项**

**说明**

**填写建议**

**示例**

**主体描述**

描述画面中原本存在的人或物

必填

视频开头展示了一位年轻女性...

**背景描述**

描述画面中主体所处的环境

必填

背景是被绿色的藤蔓覆盖的砖墙...

**触发词**

一个无实际意义的稀有词汇

推荐填写

s86b5p 或 m01aa

**运动描述**

详细描述视频中特效发生的运动变化

推荐填写

无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下...

##### **关于“触发词”**

-   **触发词是什么？**
    
    它相当于一个 **"视觉锚点"** 。因为很多复杂的动态（如某种特殊的舞蹈轨迹、独创的光影变化）很难用文字描述，所以用这个词强制告诉模型：当你看到 s86b5p 时，就必须生成这种特定的视觉效果。
    
-   **为什么要使用它？**
    
    模型微调是建立“文本”与“视频特征”的映射关系。触发词就是那个把“难以言传的特效”绑定到一个独一无二的词上，让模型能够锁定目标。
    
-   **既然有了触发词，为什么还要详细描述运动？**
    
    两者分工不同，配合使用效果更好。
    
    -   运动描述：负责解释 “画面在发生什么”。它告诉模型基础的物理动作和逻辑，通常多个样本的运动描述是一致的。
        
    -   触发词：负责解释 “动作具体是什么样”。它代表了那些文字无法描述的独特变化和特征。
        

#### **如何写好Prompt**

##### **遵循特效描述的一致性原则**

所有包含该特效的样本，其特效的运动描述部分应**尽量保持一致**。训练集和验证集均遵守此规则。

-   **目的：**当模型发现 `s86b5p` 出现时，后面总是跟着一段固定的描述，且画面总是出现金钱雨，它就能记住：s86b5p = 金钱雨视觉效果。
    
-   **示例**：无论是“年轻女性”还是“西装男性”，只要是金钱雨特效，Prompt 后半段都统一写为：“...然后开始展示 s86b5p 金钱雨特效，无数美元钞票如暴雨般倾泻而下...”
    
    **样本类型**
    
    **Prompt 内容**（注意下划线部分的描述一致性）
    
    训练集样本1
    
    视频开头展示了一位**年轻女性**站在砖墙前...（省略环境描述）...然后开始展示 s86b5p 金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，她双臂舒展上扬，表情惊喜，完全沉浸在这场狂野的金钱雨中。
    
    训练集样本2
    
    视频开头展示了一位**西装男性**在高档餐厅内...（省略环境描述）...然后开始展示 s86b5p 金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，他双臂舒展上扬，表情惊喜，完全沉浸在这场狂野的金钱雨中。
    
    验证集样本1
    
    视频开头展示了一位**年轻小孩**站在城市景观前...（省略环境描述）...然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，同时镜头缓缓拉进，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
    

##### **借助 AI 生成  Prompt**

为了获得质量较高的Prompt，推荐使用[Qwen-VL](https://help.aliyun.com/zh/model-studio/vision)等多模态大模型来辅助生成视频的Prompt。

1.  **使用 AI 辅助生成初始描述**
    
    1.  自由发散（寻找灵感）：如果不知道该如何描述特效，可以先让 AI 自由发挥。
        
        -   直接发送“`详细描述视频内容`”，观察模型输出了什么。
            
        -   重点看模型用了哪些词汇来形容**特效的运动轨迹**（如“暴雨般倾泻而下”、“镜头缓缓拉进”），这些词汇可以作为后续优化的素材。
            
    2.  固定句式（规范输出）：当有了大概思路后，可基于标注公式设计一套固定句式，引导 AI 生成符合格式的 Prompt。
        
        **示例代码**
        
        > 代码调用详见[视觉理解](https://help.aliyun.com/zh/model-studio/vision)。
        
        ```
        import os
        from openai import OpenAI
        
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen3-vl-plus",
            messages=[
                {"role": "user","content": [{
                    # 直接传入视频文件时，请将type的值设置为video_url
                    # 使用OpenAI SDK时，视频文件默认每间隔0.5秒抽取一帧，且不支持修改，如需自定义抽帧频率，请使用DashScope SDK.
                    "type": "video_url",
                    "video_url": {"url": "https://cloud.video.taobao.com/vod/Tm1s_RpnvdXfarR12RekQtR66lbYXj1uziPzMmJoPmI.mp4"}},
                    {"type": "text","text": "请仔细分析视频，并按照以下固定句式生成一段详细的视频描述"
                                            "句式模板：视频开头展示了[主体描述]。背景是[背景描述]。然后开始展示s86b5p金钱雨特效，[详细的运动描述]。"
                                            "要求："
                                            "1.[主体描述]：详细描述画面中原本存在的人或物,包含人物/物体的外貌、衣着、表情等细节。"
                                            "2.[背景描述]：详细描述主体所处的环境,包含环境、光影、天气等细节。"
                                            "3.[运动描述]：详细描述特效发生时的动态变化过程（如物体如何移动、光影如何变化、镜头如何变化）。"
                                            "4.所有内容必须自然融入句式中，不得保留“[ ]”符号，也不得添加任何与描述无关的文字。"}]
                 }]
        )
        print(completion.choices[0].message.content)
        ```
        

2.  **提炼特效模板**
    
    1.  建议对多个包含**相同特效**的样本重复运行，找出描述特效时共同使用的高频、准确词组，从中提炼出一段通用的“特效描述”。
        
    2.  将这段标准化的特效描述**复制粘贴**到该特效的所有数据集中。
        
    3.  保留每个样本独特的“主体”和“背景”描述，仅将“特效描述”部分替换为统一模板。
        

3.  **人工检查**
    
    AI 可能会产生幻觉或识别错误，最后请进行人工检查，例如：确认主体和背景的描述是否符合画面真实情况等。
    

## **使用验证集评估模型**

### **指定验证集**

微调任务必须包含训练集，验证集则是可选项。您可以选择由系统**自动划分**或**手动上传**验证集，具体指定方式如下：

##### **方式一：未上传验证集（系统自动划分）**

在[创建微调任务](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#e702c9786b40q)时，如果没有单独上传验证集，即未传入`validation_file_ids`参数，系统将根据以下两个[超参数](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#5f391e4b3cezf)，自动从**训练集**中划分出一部分作为验证集：

-   `split`：训练集划分比例。例如，0.9 表示将90%的数据用于训练，剩余的10%用作验证。
    
-   `max_split_val_dataset_sample`：自动划分验证集的最大样本数。
    

**验证集切分规则**：系统会选取 `数据集总数×(1 - split)` 和 `max_split_val_dataset_sample` 中的**较小值**。

-   示例：假设仅上传训练集，且训练集有 100 条数据，split=0.9（即验证集切分10%），max\_split\_val\_dataset\_sample=5。
    
    -   理论切分：100 × 10% = 10 条。
        
    -   实际切分：min(10, 5)=5，所以系统**只取 5 条**作为验证集。
        

##### **方式二：主动上传验证集（通过 validation\_file\_ids 指定）**

如果您希望使用一套自己准备的数据来评估Checkpoint，而不是依赖系统随机划分，可以上传自定义验证集。

注意：一旦选择主动上传，系统将**完全忽略**上述自动划分规则，仅使用您上传的数据进行验证。

**操作步骤：主动上传验证集**

1.  **准备验证集**：将验证数据打包成一个独立的 `.zip` 文件，请参见[验证集格式](#4a214aadd60df)。
    
2.  **上传验证集**：调用[上传数据集](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#Kv4zB)接口，上传这个验证集 `.zip` 文件，获得一个专属的文件ID。
    
3.  **创建任务时指定验证集**：在调用[创建微调任务](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#e702c9786b40q)接口时，将这个文件ID填入 `validation_file_ids` 参数中。
    
    ```
    {
        "model":"wan2.5-i2v-preview",
        "training_file_ids":[ "<训练集的文件id>" ],
        "validation_file_ids": [ "<自定义验证集的文件id>" ],
        ...
    }
    ```
    

### **挑选最佳Checkpoint进行部署**

在训练过程中，系统会定期保存模型的“快照”（即 Checkpoint）。默认情况下，系统会输出**最后一个Checkpoint**作为最终的微调模型。但中间过程产出的Checkpoint效果可能优于最终版本，您可以从中挑选出最满意的一个进行部署。

系统将按照[超参数](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#5f391e4b3cezf)`eval_epochs`设定的间隔，在**验证集**上运行Checkpoint并生成预览视频。

-   **如何评估**：通过直接观察生成的预览视频来判断效果。
    
-   **挑选标准**：找到效果最好、且没有动作变形的那个 Checkpoint 。
    

#### **操作步骤**

##### **步骤1：查看Checkpoint生成的预览效果**

##### **步骤1.1 查询已通过验证的Checkpoint列表**

该接口仅返回通过验证集验证、**且成功生成预览视频的 Checkpoint**，验证失败的不会列出。

**请求示例**

-   `<替换为微调任务job_id>`：完整替换为[创建微调任务接口](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#e69160039ceah)的输出参数`job_id`。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/validation-results' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

此接口返回一个仅包含成功通过验证的Checkpoint名称的列表。

```
{
    "request_id": "da1310f5-5a21-4e29-99d4-xxxxxx",
    "output": [
        {
            "checkpoint": "checkpoint-160"
        },
        ...
    ]
}
```

##### **步骤1.2 查询Checkpoint对应的验证集结果**

从上一步返回的 Checkpoint 列表中选择一个（例如“checkpoint-160”），查看其生成的视频效果。

**请求示例**

-   `<替换为微调任务job_id>`： 完整替换为[创建微调任务](#bc825b6ec11y2)输出参数`job_id`的值。
    
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如“checkpoint-160”。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/validation-details/<替换为选择的checkpoint>?page_no=1&page_size=10' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

预览视频URL为`video_path`，有效期为24小时，请及时下载视频并查看效果。重复此步骤，比较多个Checkpoint的效果，找出最满意的一个。

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

##### **步骤2：导出Checkpoint，并获取待部署的模型名称**

##### **步骤2.1 导出模型**

假设“checkpoint-160”的效果最佳，接下来是将其导出。

**请求示例**

-   `<替换为微调任务job_id>`： 完整替换为[创建微调任务](#bc825b6ec11y2)输出参数`job_id`的值。
    
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如“checkpoint-160”。
    
-   `<替换为控制台展示的导出模型名称>`：完整替换为自定义的模型名称，仅用于控制台展示，例如“wan2.5-checkpoint-160”。该名称必须全局唯一，不支持重复名称多次导出，参数填写请参见[导出Checkpoint](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#2636e0fdfewpw)。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/export/<替换为待导出的checkpoint>?model_name=<替换为控制台展示的导出模型名称>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

响应参数`output=true`，表示导出请求已成功创建。

```
{
    "request_id": "0817d1ed-b6b6-4383-9650-xxxxx",
    "output": true
}
```

##### **步骤2.2 查询部署后的新模型名称**

查询所有Checkpoint的状态，确认导出已完成，并获取它专属的、用于部署的新模型名称（`**model_name**`）。

**请求示例**

-   `<替换为微调任务job_id>` ：完整替换为[创建微调任务](#bc825b6ec11y2)输出参数`job_id`的值。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/checkpoints' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

在返回列表中定位导出的 Checkpoint（如 checkpoint-160）。当其 `status` 变为 **SUCCEEDED** 时，表示导出成功；此时返回的 `**model_name**` 字段即为导出后的新模型名称。

```
{
    "request_id": "b0e33c6e-404b-4524-87ac-xxxxxx",
    "output": [
         ...,
        {
            "create_time": "2025-11-11T13:27:29",
            "full_name": "ft-202511111122-496e-checkpoint-160",
            "job_id": "ft-202511111122-496e",
            "checkpoint": "checkpoint-160",                             
            "model_name": "xxxx-ft-202511111122-xxxx-c160", // 重要字段，将用于模型部署和调用
            "model_display_name": "xxxx-ft-202511111122-xxxx", 
            "status": "SUCCEEDED" // 成功导出的checkpoint
        },
        ...
        
    ]
}
```

##### **步骤3：部署并调用模型**

在成功导出 Checkpoint 并获取 `**model_name**` 后，请按照以下步骤执行后续操作：

-   [模型部署](#0ad4c110b58ui)：在输入参数 `model_name`，填入导出后获取到的具体值。
    
-   [模型调用](#543cc07530gl2)：参照接口说明，调用已部署模型。
    

## **应用于生产环境**

在实际生产中，如果初次训练的模型效果不佳（如画面崩坏、特效不明显、动作不准确），可参考以下维度调优：

**1\. 检查数据与Prompt**

-   数据一致性：数据一致性是核心。检查是否有方向相反、风格差异过大的“差样本”。
    
-   样本数量：建议将高质量数据增加至 **20条以上**。
    
-   Prompt：确保触发词为**无意义稀有词**（如 s86b5p），避免使用常用词（如 running）造成干扰。
    

**2\. 调整超参数：**参数说明请参见[超参数](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#5f391e4b3cezf)。

-   **n\_epochs (训练轮数)**
    
    -   默认值：**400**，推荐使用默认值。若需调整，请遵循 **“总训练步数 (Steps) ≥ 800”** 的原则。
        
    -   总步数计算公式： `steps = n_epochs × 向上取整（训练集大小 / batch_size）。`
        
    -   因此，n\_epochs最小值计算公式：`n_epochs = 800 / 向上取整（数据集大小 / batch_size）`。
        
    -   示例：假设训练集有5条数据，使用Wan2.5模型（batch\_size=2）。
        
        -   每轮训练步数：5 / 2 = 2.5，向上取整为3。总的训练轮数： n\_epochs = 800 / 3 ≈ 267。此值为**推荐的最小值**，可根据实际业务适当调高，比如300。
            
-   **learning\_rate (学习率)、batch\_size (批次大小)**推荐使用默认值，通常无需修改。
    

## **计费说明**

-   **模型训练：收费。**
    
    -   费用 = 训练 Tokens 总量 × 单价。请参见[模型训练计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。
        
    -   训练结束后，在[查询微调任务状态](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference#a242dac535nqt)接口 `usage` 字段查看训练消耗的总 Token 数。
        
-   **模型部署**：**免费**。
    
-   **模型调用：收费。**
    
    -   按微调的基础模型的标准调用价格计费，请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#b3fb713fe4pja)。
        

## **API文档**

[视频生成模型微调API参考](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-api-reference)

## **常见问题**

#### **Q：如何计算训练集和验证集的数据量？**

A: 训练集必须提供，验证集可选。具体计算方式如下：

-   **当未传入验证集时**：上传的训练集即为“数据集总数”，系统会自动从训练集中划出一部分数据用于验证。
    
    -   验证集数量 = `min(数据集总数 × (1 − split), max_split_val_dataset_sample)`。计算示例请参见[指定验证集](#1766f17a3eo2y)。
        
    -   训练集数量 = `数据集总数 − 验证集数量`。
        
-   **当主动上传验证集时**：系统不再从训练数据中划分验证集。
    
    -   训练集数量 = 上传的训练集数据量。
        
    -   验证集数量 = 上传的验证集数据量。
        

#### **Q：如何设计一个好的触发词？**

A: 规则如下：

-   使用**无意义的字母组合**，如 sksstyle, a8z2\_bbb。
    
-   **避免**使用常用英语单词（如 beautiful, fire, dance），否则会污染模型原本对这些词的理解。
    

#### **Q：微调能改变视频的分辨率或时长吗？**

A: **不能**。微调是学习“内容”和“动态”，不是改变“规格”。输出视频的格式（分辨率、帧率、时长上限）依然由基础模型决定。

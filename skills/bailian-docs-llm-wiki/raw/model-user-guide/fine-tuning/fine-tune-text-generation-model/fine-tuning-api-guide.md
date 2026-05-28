# 使用 API 或命令行进行模型调优

本文档以千问模型的调优操作为例进行说明，通过 API （HTTP）和 命令行（Shell）两种方式，使用阿里云百炼提供的模型调优功能。模型调优包含模型微调（SFT）、继续预训练（CPT）、模型偏好训练（DPO）三种模型训练方式。

**重要**

本文档仅适用于中国大陆版（北京地域）。

## **前提条件**

-   已经完整阅读了[模型调优简介](https://help.aliyun.com/zh/model-studio/model-training-overview)，了解模型调优的基本概念、流程及数据格式要求。
    
-   已开通服务并获得API-KEY， 请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   [阿里云子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)）需被授予必要的调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。
    

**说明**

通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 上传调优文件

### **准备调优文件**

#### **SFT 训练集**

SFT ChatML（Chat Markup Language）格式训练数据，支持多轮对话和多种角色设置。

> 不支持OpenAI 的`name`、`weight`参数，所有的 assistant 输出都会被训练。

```
# 一行训练数据（json 格式），展开后典型结构如下:
{"messages": [
  {"role": "system", "content": "系统输入1"}, 
  {"role": "user", "content": "用户输入1"}, 
  {"role": "assistant", "content": "期望的模型输出1"}, 
  {"role": "user", "content": "用户输入2"}, 
  {"role": "assistant", "content": "期望的模型输出2"}
  ...
]}
```

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)，训练数据集样例：[SFT-ChatML格式示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241014/utjdbx/SFT-ChatML%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)、[SFT-ChatML格式示例.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251111/jrxbpn/SFT-ChatML%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.xlsx)（xls、xlsx 格式只支持单轮对话）。

单条训练数据的**所有** assistant 行都支持`"loss_weight"`参数，用于设置该行在训练时的相对重要性。（设置范围`0.0 ~ 1.0`，数值越大，重要性越高）

> 该参数属于邀测参数，如需使用，请联系您的商务经理。

```
{"role": "assistant", "content": "期望的模型输出1", "loss_weight": 1.0}, 
 {"role": "assistant", "content": "期望的模型输出2", "loss_weight": 0.5}
```

#### SFT 思考模型（thinking）

训练数据支持多轮对话和多种角色设置，但只能针对**最后**的 assistant 输出进行训练，**一行训练数据展开后结构如下**：

> 思考标签前后的若干个`\n`必须要保留。

```
# 一行训练数据（json 格式），展开后典型结构如下:
{"messages": [
  {"role": "system", "content": "系统输入1"}, 
  {"role": "user", "content": "用户输入1"}, 
  {"role": "assistant", "content": "模型输出1"}, --中间的 assistant 输出不应添加 <think> 标签
   ...
  {"role": "user", "content": "用户输入2"}, 
  {"role": "assistant", "content": "<think>\n期望的思考内容2\n</think>\n\n期望的输出2"} --思考内容只能包含在最后一个 assistant 输出中。 
]}
```

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)，训练数据集样例：[SFT- 深度思考内容示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251224/txsbci/SFT-+%E6%B7%B1%E5%BA%A6%E6%80%9D%E8%80%83%E5%86%85%E5%AE%B9%E7%A4%BA%E4%BE%8B.jsonl)。

也可以在训练样本中设置模型不输出`<think>`标签， 如果使用这种输出方式，模型训练完成后**不建议再开启思考模式进行调用**。

```
{"role": "assistant", "content": "期望的模型输出2"}  --告诉模型不开启思考
```

单条训练数据**最后**的 assistant 行支持`"loss_weight"`参数，用于设置该条数据在训练时的相对重要性。（设置范围`0.0 ~ 1.0`，数值越大，重要性越高）

> 该参数属于邀测参数，如需使用，请联系您的商务经理。

```
{"role": "assistant", "content": "<think>\n期望的思考内容2\n</think>\n\n期望的输出2", "loss_weight": 1.0}
```

#### SFT 视觉理解（千问VL）

> 不支持OpenAI 的`name`、`weight`参数，所有的 assistant 输出都会被训练。

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)。ChatML 格式训练数据样例：

> 如需传入 `system` 消息，对应的 `content` 必须使用数组格式 `[{"text":"..."}]`，不能使用字符串格式 `"content":"字符串"`。

```
# 一行训练数据（json 格式），展开后典型结构如下：
{"messages": [
  {"role": "system", "content": [{"text": "系统输入"}]},
  {"role": "user", "content": [{"text": "用户输入1"}, {"image": "图像文件名1.jpg", "resized_width": 200, "resized_height": 200}]},
  {"role": "assistant", "content": [{"text": "期望的模型输出1"}]},
  {"role": "user", "content": [{"text": "用户输入2"}, {"video": "视频文件名1.mp4", "fps": 3.0, "resized_width": 200, "resized_height": 200, "video_start": 0.0, "video_end": 3.0}]},
  {"role": "assistant", "content": [{"text": "期望的模型输出2"}]},
  {"role": "user", "content": [{"text": "用户输入2"}, {"video": ["0.jpg", "1.jpg", "2.jpg", "3.jpg"], "sample_fps": 5.0, "resized_width": 200, "resized_height": 200}]},
  {"role": "assistant", "content": [{"text": "期望的模型输出2"}]},
  ...
]}
```

点击此处查看更多支持的参数

**字段**

**类型**

**必填**

**说明**

**图片文件**

`image`

`str`

是

图片文件路径

`resized_width`

`int`

否

图片目标缩放宽度（像素）

`resized_height`

`int`

否

图片目标缩放高度（像素）

**视频文件-视频文件路径模式（仅 qwen3.5 及以后的 VL 模型支持）**

**样例：**[阿里云VL\_Video.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260514/xllbzy/%E9%98%BF%E9%87%8C%E4%BA%91VL_Video.zip)

`video`

`str` 

是

视频文件路径模式：`{"video": "视频文件名1.mp4"}`

`resized_width`

`int`

否

视频目标缩放宽度（像素）

`resized_height`

`int`

否

视频目标缩放高度（像素）

`fps`

`float`

否

训练时的输入频率。如果设置`fps=30`，实际训练用的视频帧率为 30 帧。

`video_start`

`float`

否

视频截取起始时间（秒）

`video_end`

`float`

否

视频截取结束时间（秒）

**视频文件-图片帧列表模式（仅 qwen3.5 及以后的 VL 模型支持）**

`video`

`List[str]`

是

图片帧列表模式：`{"video": ["0.jpg", "1.jpg", "2.jpg", ...], "sample_fps": 2.0}`

`sample_fps`

`float`

否

用于告知图片帧的帧率。

`resized_width`

`int`

否

图片帧缩放宽度（像素）

`resized_height`

`int`

否

图片帧缩放高度（像素）

**说明**

如果训练思考模型（Thinking），也需要遵循[SFT 思考模型（thinking）](#f5454632ef4yo)的数据格式要求。

##### **压缩包要求：**

1.  压缩包格式：ZIP。最大支持 2 GB， ZIP 包内文件夹、文件名仅支持 ASCII 字符集中的字母 (a-z, A-Z)、数字 (0-9)、下划线 (\_)、连字符 (-)。
    
2.  训练文本数据固定为 data.jsonl，并且位于压缩包的**根目录**下，应**确保压缩后打开 zip 文件，直接就能看到** `**data.jsonl**` **文件。**
    
3.  图片单张尺寸的宽度和高度均不得超过 1024px，最大不超过10MB，支持 `.bmp`, `.jpeg /.jpg`, `.png`, `.tif /.tiff`, `.webp` 格式。
    
4.  图片文件的名称不能重复，即使分布在不同的文件夹中。
    
5.  压缩包目录结构：
    
    ###### **单层目录（推荐）**
    
    图片文件与 `data.jsonl` 文件均位于压缩包根目录下。
    
    ```
    Trainingdata_vl.zip
       |--- data.jsonl #注意：外层不能再包裹文件夹
       |--- image1.png
       |--- video1.mp4
    ```
    
    ###### 多层目录
    
    1.  data.jsonl 必须在压缩包根目录下。
        
    2.  data.jsonl 内只需要声明图像/视频文件名，**不需要声明文件路径**。例如：
        
        **正确示例**：`image1.jpg`；**错误示例**：`jpg_folder/image1.jpg`。
        
    3.  图像/视频文件名应在压缩包内全局唯一。
        
    
    ```
    Trainingdata_vl.zip
        |--- data.jsonl #注意：外层不能再包裹文件夹
        |--- jpg_folder
        |   └── image1.jpg
        |--- mp4_folder
            └── video.mp4
    ```
    

#### DPO 数据集

DPO ChatML 格式训练数据，**一行训练数据展开后结构如下**：

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)，训练数据集样例：[DPO ChatML格式样例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241014/ihjgry/DPO+ChatML%E6%A0%BC%E5%BC%8F%E6%A0%B7%E4%BE%8B.jsonl)。

```
# 一行训练数据（json 格式），展开后典型结构如下:
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入1"},
  {"role": "assistant", "content": "模型输出1"},
  {"role": "user", "content": "用户输入2"},
  {"role": "assistant", "content": "模型输出2"},
  {"role": "user", "content": "用户输入3"}
 ],
 "chosen":
   {"role": "assistant", "content": "赞同的模型期望输出3"},
 "rejected":
   {"role": "assistant", "content": "反对的模型期望输出3"}}
```

模型将 `messages` 内的所有内容均作为输入，DPO 用于训练模型对`用户输入3`的正负反馈。

针对深度思考的内容，需要使用`<think>`标签包裹：

```
{"role": "assistant", "content": "<think>期望的模型思考内容</think>期望的模型输出"}
```

单条训练数据的`"chosen"`模块支持`"loss_weight"`参数，用于设置该条训练数据在训练中的相对重要性。（设置范围`0.0 ~ 1.0`，数值越大，重要性越高）

> 该参数属于邀测参数，如需使用，请联系您的商务经理。

```
"chosen":
   {"role": "assistant", "content": "赞同的模型期望输出3", "loss_weight": 1.0},
```

#### CPT 训练集

CPT 纯文本格式训练数据，**一行训练数据展开后结构如下**：

```
{"text":"文本内容"}
```

训练数据集样例：[CPT-文本生成训练集示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241127/qrtlrz/CPT-%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E8%AE%AD%E7%BB%83%E9%9B%86%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)

也可以前往[阿里云百炼控制台](https://bailian.console.aliyun.com/#/efm/model_data/createDataAss?isApplicationTabContent=false)下载数据模板。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4636231471/p878841.png)

### **将调优**文件**上传至阿里云百炼**

#### **HTTP**

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --request POST \
'https://dashscope.aliyuncs.com/api/v1/files' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--form 'files=@"/path/to/your/file.jsonl"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="a sample fine-tune data file for qwen"'
```

**说明**

使用限制：

-   单个文件大小最大为300MB
    
-   所有有效文件（未删除）总使用空间配额为5GB
    
-   所有有效文件（未删除）总数量配额为100个
    
-   文件存储没有时间限制
    

更多详细信息请参见[模型微调文件管理服务](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service)。

返回结果：

```
{
  "request_id":"xx",
  "data":{
    "uploaded_files":[{
      "file_id":"976bd01a-f30b-4414-86fd-50c54486e3ef",
      "name":"qwen-fine-tune-sample.jsonl"}],
  　"failed_uploads":[]}
 }
```

#### **Shell**

需要安装 DashScope SDK，请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#f3e80b21069aa)。

> 一次调用只能上传一个文件

```
dashscope files.upload -f '/path/to/your/file.jsonl' -p fine_tune -d 'training dataset'
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2938329271/p851518.png)

**说明**

`SFT`、`DPO`、`CPT`数据集支持`.jsonl`文件；`SFT`图像理解训练集支持`.zip`压缩包。

使用限制：

-   单个文件大小最大为300MB。
    
-   有效文件（未删除）总使用空间配额为5GB。
    
-   有效文件（未删除）总数量配额为100个。
    

返回结果：

```
Upload success, file id: 976bd01a-f30b-4414-86fd-50c54486e3ef
```

## **模型调优**

### **创建调优任务**

## HTTP

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json' \
--data '{
    "model":"qwen3-8b",
    "training_file_ids":[
        "<替换为训练数据集的file_id1>",
        "<替换为训练数据集的file_id2>"
    ],
    "hyper_parameters":
    {
        "n_epochs": 3,
        "batch_size": 16,
        "max_length": 8192,
        "learning_rate": "1.6e-5",
        "lr_scheduler_type": "linear",
        "split": 0.9,
        "warmup_ratio": 0.05,
        "eval_steps": 50,
        "data_augmentation": true,
        "augmentation_ratio": "0.1,0.05,0.15",
        "augmentation_types": "dialogue_CN,general_purpose_CN,NLP",
        "save_strategy": "epoch",
        "save_total_limit": 10
    },
    "training_type":"sft"
}'
```

### **输入参数**

**字段**

**必选**

**类型**

**传参方式**

**描述**

training\_file\_ids

是

Array

Body

训练集文件列表。

validation\_file\_ids

否

Array

Body

验证集文件列表。

model

是

String

Body

**用于调优的基础模型 ID，或其他调优任务产出的模型 ID。**

hyper\_parameters

否

Map

Body

用于调优模型的超参数。不同模型支持的参数及其默认值不同，请在控制台选择相同的模型和训练方式查看实际默认值。

以下参数影响训练费用，**必须填写**：`n_epochs`（循环次数）、`batch_size`（批次大小）、`max_length`（序列长度）。

training\_type

否

String

Body

调优方法，可选值为：

`cpt`

`sft`

`efficient_sft`

`dpo_full`

`dpo_lora`

job\_name

否

String

Body

调优任务名称

model\_name

否

String

Body

调优产生的模型名称（并非模型 ID，模型 ID 由系统统一生成）

## **返回样例**

```
{
    "request_id": "635f7047-003e-4be3-b1db-6f98e239f57b",
    "output":
    {
        "job_id": "ft-202511272033-8ae7",
        "job_name": "ft-202511272033-8ae7",
        "status": "PENDING",
        "finetuned_output": "qwen3-8b-ft-202511272033-8ae7",
        "model": "qwen3-8b",
        "base_model": "qwen3-8b",
        "training_file_ids":
        [
            "9e9ffdfa-c3bf-436e-9613-6f053c66aa6e"
        ],
        "validation_file_ids":
        [],
        "hyper_parameters":
        {
            "n_epochs": 3,
            "batch_size": 16,
            "max_length": 8192,
            "learning_rate": "1.6e-5",
            "lr_scheduler_type": "linear",
            "split": 0.9,
            "warmup_ratio": 0.05,
            "eval_steps": 50,
            "data_augmentation": true,
            "augmentation_ratio": "0.1,0.05,0.15",
            "augmentation_types": "dialogue_CN,general_purpose_CN,NLP",
            "save_strategy": "epoch",
            "save_total_limit": 10
        },
        "training_type": "sft",
        "create_time": "2025-11-27 20:33:15",
        "workspace_id": "llm-8v53etv3hwb8orx1",
        "user_identity": "1654290265984853",
        "modifier": "1654290265984853",
        "creator": "1654290265984853",
        "group": "llm",
        "max_output_cnt": 10
    }
}
```

## Shell

```
dashscope fine_tunes.call -m qwen3-8b -t '<替换为训练数据集的file_id1>' '<替换为训练数据集的file_id2>' \
--mode sft -b 16 -e 3 -l 1.6e-5 --max_length 8192 \
--hyper_parameters split=0.9 warmup_ratio=0.05 eval_steps=50
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2938329271/p858006.png)

**调优指令进程将持续监控输出模型调优的日志**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2938329271/p858626.png)

调优指令进程即使在调优结束后也不会自动关闭，**可以随时终止调优指令进程，不会影响阿里云百炼平台上的模型调优任务。**

可以使用[查询调优任务详情](#adc8279ab58l2) API 或前往[百炼控制台](https://bailian.console.aliyun.com/tab=model?tab=model#/efm/model_manager)查看当前任务状态并获取调优任务日志。

#### **支持的基础模型ID（**`**model**`**）列表与训练类型（**`**training_type**`**）支持情况：**

> 如果调优的模型不支持`sft`方法，调优任务将会失败。

**模型服务**

**模型代码**

**CPT全参训练（cpt）**

**SFT全参训练（sft）**

**SFT高效训练（sft\_efficient）**

**DPO全参训练（dpo\_full）**

**DPO高效训练（dpo\_lora）**

Qwen3.5-27B

qwen3.5-27b

×

支持

支持

×

×

Qwen3.5-9B

qwen3.5-9b

×

支持

支持

×

×

Qwen3-32B

qwen3-32b

×

支持

支持

支持

支持

Qwen3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

支持

支持

支持

×

×

Qwen3-14B

qwen3-14b

×

支持

支持

支持

支持

Qwen3-8B

qwen3-8b

×

支持

支持

支持

支持

Qwen3-1.7B

qwen3-1.7b

支持

支持

支持

支持

支持

Qwen3-0.6B

qwen3-0.6b

支持

支持

支持

支持

支持

Qwen2.5-72B-Instruct

qwen2.5-72b-instruct

支持

支持

支持

支持

支持

Qwen2.5-32B-Instruct

qwen2.5-32b-instruct

支持

支持

支持

支持

支持

Qwen2.5-14B-Instruct

qwen2.5-14b-instruct

支持

支持

支持

支持

支持

Qwen2.5-7B-Instruct

qwen2.5-7b-instruct

支持

支持

支持

支持

支持

千问-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

×

支持

支持

支持

支持

#### `hyper_parameters`内**支持的设置**

> 不同模型支持的参数及其默认值不同，**请前往[控制台](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)选择相同的模型和训练方式查看实际默认值**。

**参数名称**

**推荐设置**

类型

**超参作用**

`n_epochs`

（循环次数）**【必填】**

**数据量 < 10,000, 3~5次**

**数据量 > 10,000, 1~2次**

Integer

模型遍历训练的次数，请根据模型调优实际使用经验进行调整。

模型训练循环次数越多，训练时间越长，训练费用越高。

`learning_rate`

（学习率）

使用百炼推荐的默认值

Float

控制模型修正权重的强度。

-   学习率设置得太高，模型参数会剧烈变化，导致调优后的模型表现不一定更好，甚至变差；
    
-   学习率太低，调优后的模型表现不会有太大变化。
    

`freeze_vit`

（是否冻结视觉主干网络）

根据需求调整

Boolean

用于冻结视觉主干网络的参数，使其在训练过程中不更新权重。仅适用于 千问-VL（视觉理解）模型。

**说明**

只有 freeze\_vit 设置为“true”时，模型才能进行按 [Token 用量](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#9ea9924cd8138)计费。

`batch_size`

（批次大小）**【必填】**

使用百炼推荐的默认值

Integer

一次性送入模型进行训练的数据条数，参数过小会显著延长训练时间。不同模型的默认值不同，请前往控制台查看。

`eval_steps`

（验证步数）

根据需求调整

Integer

训练阶段针对模型的验证间隔步长，用于阶段性评估模型训练准确率、训练损失。

该参数影响模型调优进行时的 Validation Loss 和 Validation Token Accuracy 的显示频率。

`logging_steps`

（日志显示步数）

根据需求调整

Integer

调优日志打印的步数。

`lr_scheduler_type`

（学习率调整策略）

推荐`linear`/`Inverse_sqrt`

String

在模型训练中动态调整学习率的策略。

各策略详情请参考[在控制台进行模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console#7864d6a606ztg)。

`max_length`

（序列长度）**【必填】**

8192

Integer

指的是单条训练数据 token 支持的最大长度。如果单条数据 token 长度超过设定值，调优会直接丢弃该条数据，不进行训练。

字符与 token 之间的关系请参考[Token和字符串之间怎么换算](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#35d3b2ad2386c)

`max_split_val_dataset_sample`

（验证集数据最大数量）

使用百炼推荐的默认值

Integer

当不设置`"validation_file_ids"`时，阿里云百炼自动分割的验证集最多只有1000条。

当设置了`"validation_file_ids"`时，该参数无效。

`split`

（训练集在训练文件中占比）

使用百炼推荐的默认值

Float

当不设置`"validation_file_ids"`时，阿里云百炼会自动把训练文件中的80%作为训练集，20%作为验证集。

当设置了`"validation_file_ids"`时，该参数无效。

`warmup_ratio`

（学习率预热比例）

使用百炼推荐的默认值

Float

学习率预热占用总的训练过程的比例。学习率预热是指学习率在训练开始后由一个较小值线性递增至学习率设定值。

该参数主要是限制模型参数在训练初始阶段的变化幅度，从而帮助模型更稳定地进行训练。

比例过大效果与过低的学习率相同，会导致调优后的模型表现不会有太大变化。

比例过小效果与过高的学习率相同，可能导致调优后的模型表现不一定更好，甚至变差。

> 该参数仅对学习率调整策略“Constant”无效。

`weight_decay`

（权重衰减）

使用百炼推荐的默认值

Float

L2正则化强度。L2正则化能在一定程度上保持模型的通用能力。数值过大会导致模型调优效果不明显。

**高效微调（支持**`efficient_sft`、`dpo_lora`**）参数**

**说明**

当对一个已经高效微调后的模型进行二次高效微调时，`lora_rank`、`lora_alpha`、`lora_dropout`三个参数必须保持一致。

`lora_rank`

（LoRA秩值）

64

Integer

LoRA训练中的低秩矩阵的秩大小。秩越大调优效果越好，但训练会略慢。

`lora_alpha`

（LoRA阿尔法）

使用百炼推荐的默认值

Integer

用于控制原模型权重与LoRA的低秩修正项之间的结合缩放系数。

较大的Alpha值会给予LoRA修正项更多权重，使得模型更加依赖于微调任务的特定信息；

而较小的Alpha值则会让模型更倾向于保留原始预训练模型的知识。

`lora_dropout`

（LoRA丢弃率）

使用百炼推荐的默认值

Float

LoRA训练中的低秩矩阵值的丢弃率。

使用推荐数值能增强模型通用化能力。

数值过大会导致模型微调效果不明显。

**混合训练（支持**`efficient_sft`、`sft`**）参数**

`data_augmentation`

（是否开启混合训练）

根据模型的使用场景混合

Boolean

开启后，训练数据将与百炼提供的通用数据集（多领域/多行业/多场景）混合：

\- 效果：提升训练效果，避免模型能力退化。

\- 计费：混合数据计入总训练Token，按标准计费。

`augmentation_types`

（选择预置数据的类型）

根据模型的使用场景混合

例：`"augmentation_types": "dialogue_CN,general_purpose_CN,NLP"`

> 需与`augmentation_ratio`配合使用

String

**数据集 code**

**数据集名称**

**支持的模型**

`dialogue_cn`

中文-对话

千问 2 系列

`math_cn`

中文-数学

`general_coding_cn`

中文-代码

`general_purpose_cn`

中文-通用

`nlp`

NLP 理解

`dialogue_en`

英文-对话

`math_en`

英文-数学

`general_coding_en`

英文-代码

`general_purpose_en`

英文-通用

`mix_v2`

通用-V2

千问 3 系列

`vl_mix`

通用

千问 3 VL 系列

`augmentation_ratio`

（设置混合倍率）

根据模型的使用场景混合

String

-   格式要求：与`augmentation_types`一一对应
    
-   示例：`"0.1,0.05,0.15"`（分别对应`augmentation_types`列出的三种数据集）
    
-   含义：按训练数据量的`10%/5%/15%`随机抽取混合
    
-   范围：`0.0 ~ 2.0`
    

**模型参数快照发布（仅支持**`efficient_sft`、`sft`**）参数**

`save_strategy`

（快照存储策略）

可以设置为 `epoch`或`steps`。

-   设置为`steps`时，可以通过设置`save_steps`参数，调整保存间隔。
    

String

设置调优过程中，保存模型参数快照（Checkpoint）的保存间隔和保存数量上限。

`save_steps`

（存储步数）

如果需要手动修改，建议设置为`eval_steps`参数的整数倍。

Integer

设置每训练多少步保存一次模型参数快照（Checkpoint）。

`save_total_limit`

（快照存储数量上限）

10

Integer

限制最多保存多少个模型参数快照（Checkpoint）用于发布。

### 查询调优任务详情

使用创建任务时返回的`job_id`来查询任务状态。

## HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的ID。

### **返回成功样例**

```
{
    "request_id": "d100cddb-ac85-4c82-bd5c-9b5421c5e94d",
    "output":
    {
        "job_id": "ft-202511272033-8ae7",
        "job_name": "ft-202511272033-8ae7",
        "status": "RUNNING",
        "finetuned_output": "qwen3-8b-ft-202511272033-8ae7",
        "model": "qwen3-8b",
        "base_model": "qwen3-8b",
        "training_file_ids":
        [
            "9e9ffdfa-c3bf-436e-9613-6f053c66aa6e"
        ],
        "validation_file_ids":
        [],
        "hyper_parameters":
        {
            "n_epochs": 3,
            "batch_size": 16,
            "max_length": 8192,
            "learning_rate": "1.6e-5",
            "lr_scheduler_type": "linear",
            "split": 0.9,
            "warmup_ratio": 0.05,
            "eval_steps": 50,
            "data_augmentation": true,
            "augmentation_ratio": "0.1,0.05,0.15",
            "augmentation_types": "dialogue_CN,general_purpose_CN,NLP",
            "save_strategy": "epoch",
            "save_total_limit": 10
        },
        "training_type": "sft",
        "create_time": "2025-11-27 20:33:15",
        "workspace_id": "llm-8v53etv3hwb8orx1",
        "user_identity": "1654290265984853",
        "modifier": "1654290265984853",
        "creator": "1654290265984853",
        "group": "llm",
        "max_output_cnt": 10
    }
}
```

**任务状态**

**含义**

PENDING

训练待开始。

QUEUING

训练正在排队（同时只有一个训练任务可以进行）

RUNNING

训练正在进行中。

CANCELING

训练正在取消中。

SUCCEEDED

训练成功。

FAILED

训练失败。

CANCELED

训练已经取消。

**说明**

训练成功后，`finetuned_output`指的是调优成功后的模型 ID，可用于模型部署。

## Shell

```
dashscope fine_tunes.get -j <job_id>
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的ID。

**返回成功样例**

```
Fine-tune task success, fine-tuned model : qwen3-8b-ft-202410121111-a590
```

**任务状态**

**含义**

PENDING

训练待开始。

QUEUING

训练正在排队（同时只有一个训练任务可以进行）

RUNNING

训练正在进行中。

CANCELING

训练正在取消中。

SUCCEEDED

训练成功。

FAILED

训练失败。

CANCELED

训练已经取消。

**说明**

`qwen3-8b-ft-202511272033-8ae7`为调优成功后的模型 ID。

如果训练失败，请使用下述“获取调优任务日志”命令获取错误日志。

### **获取调优任务日志**

## HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/logs?offset=0&line=1000' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

> 可通过 offset 和 line 两个参数获取特定行数区间的日志。 Offset 用于设置日志输出开始的位置；line 用于设置日志最多输出多少行。

返回结果样例：

```
{
    "request_id":"1100d073-4673-47df-aed8-c35b3108e968",
    "output":{
        "total":57,
        "logs":[
            "{输出调优日志1}",
            "{输出调优日志2}",
            ...
            ...
            ...
        ]
    }
}
```

## Shell

```
dashscope fine_tunes.stream -j <job_id>
```

如果调优未完成，指令进程将持续监控输出模型调优的日志。

如果调优已完成，将全量输出模型调优的日志。

### 查询与发布模型参数快照

> 仅 SFT微调训练（`efficient_sft`、`sft`）支持保存和发布其中间状态的模型参数快照（Checkpoint）。

#### **查询调优任务的参数快照列表**

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/checkpoints' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

**输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的ID。

**返回成功样例**

**说明**

`checkpoint`指的是 Checkpoint ID，用于在[模型发布（可选）](#7188bc825bl6b) API 中指定要发布的快照；`model_name`指的是模型 ID，可用于模型部署。（`finetuned_output` 输出的是最后一个 checkpoint 的 `model_name`）

```
{
    "request_id": "c11939b5-efa6-4639-97ae-ed4597984647",
    "output":
    [
        {
            "create_time": "2025-11-11T16:25:42",
            "full_name": "ft-202511272033-8ae7-checkpoint-20",
            "job_id": "ft-202511272033-8ae7",
            "checkpoint": "checkpoint-20",
            "model_name": "qwen3-8b-instruct-ft-202511272033-8ae7",
            "status": "SUCCEEDED"
        }
    ]
}
```

**快照发布状态 （status）**

**含义**

PENDING

快照（Checkpoint）待发布，需要使用[模型发布](#7188bc825bl6b) API 发布后才可以进行[模型部署&调用](#a61a0681fawzl)。

PROCESSING

快照（Checkpoint）发布中。

SUCCEEDED

快照（Checkpoint）发布成功。可直接进行[模型部署&调用](#a61a0681fawzl)。

FAILED

快照（Checkpoint）发布失败。

#### **模型发布（可选）**

**说明**

在百炼平台上，模型调优完成后可以导出参数快照，导出后才能基于此版本的参数快照在百炼上进行模型部署。

导出的参数快照保存在云存储中，暂不支持访问或下载。

```
curl --request GET 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/export/<checkpoint_id>?model_name=<model_name>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

**输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的 ID。

checkpoint\_id

String

Path Parameter

是

要发布的 Checkpoint ID。

model\_name

String

Path Parameter

是

发布后期望的模型 ID。

**发布任务成功返回样例**

```
{
    "request_id": "ed3faa41-6be3-4271-9b83-941b23680537",
    "output": true
}
```

由于发布任务是异步执行的，请使用[查询快照列表](#4aaa5bd325vy7) API 观察快照发布状态。

### 模型调优的更多操作

#### 列举调优任务列表

HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

Shell

```
dashscope fine_tunes.list
```

#### **中止调优任务**

> 智能终止正在训练中的调优任务

HTTP

```
curl --request POST 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/cancel' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

Shell

```
dashscope fine_tunes.cancel -j <job_id>
```

#### **删除调优任务**

> 无法删除正在训练中的调优任务

HTTP

```
curl --request DELETE 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

Shell

```
dashscope fine_tunes.delete -j <job_id>
```

## API参考

DashScope命令行调用参考已包含在本篇内容中，详细API调用请参考[API详情](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

## 模型部署&调用

### **模型部署**

将调优任务成功后的模型 ID 作为创建模型服务的`model_name`参数。

更多模型部署方式的相关信息请参考：[使用 API 进行模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)。

#### **按模型 Token 使用量**

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{        
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora",
    "capacity": 1,
    "name": "qwen3-8b-ft"
}'
```

#### **按模型单元的使用时长**

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",  
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "deploy_spec": "MU1",
    "enable_thinking": true,
    "capacity": 4,
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

### **查询模型部署的状态**

当部署状态为`RUNNING`时，表示该模型当前可供调用。

HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为部署任务成功后的模型实例 ID>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY}  \
--header 'Content-Type: application/json'
```

Shell

```
dashscope deployments.get -d <替换为部署任务成功后的模型实例 ID>
```

更多模型部署相关的操作，如扩缩容、下线等请参见：[模型部署-API详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)。

### 模型**调用**

当模型部署状态为`RUNNING`时，可以像调用其他模型一样使用调优后的模型。

更多使用方法和参数设置请前往[DashScope API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#69cac67a477k2)。

HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY}  \
--header 'Content-Type: application/json' \
--data '{
    "model": "<替换为部署任务成功后的模型实例 ID>",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

Shell

```
dashscope generation.call -m <替换为部署任务成功后的模型实例 ID> -p '你是谁？'
```

## **模型评测**

阿里云百炼的模型评测功能必须使用控制台，请前往阿里云百炼的[模型评测](https://bailian.console.aliyun.com/?tab=model#/efm/model_evaluate) 页面，评估模型训练效果。

相关信息请参见[模型评测](https://help.aliyun.com/zh/model-studio/getting-started/evaluate-models)。

# 使用 API 或命令行进行模型调优

本文档以千问模型的调优操作为例进行说明，通过 API （HTTP）和 命令行（Shell）两种方式，使用阿里云百炼提供的模型调优功能。模型调优包含模型微调（SFT）、继续预训练（CPT）、模型偏好训练（DPO）三种模型训练方式。

## 前提条件

-   已经完整阅读了[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，了解模型调优的基本概念、流程及数据格式要求。
-   已开通服务并获得API-KEY， 请参考[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   [阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)）需被授予必要的调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace)。

**说明**通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 上传调优文件

### 准备调优文件

SFT/DPO/CPT 各训练方式的数据格式规格、打包规则、大小与数量限制、API 上传配额详见[调优数据上传规则](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#w80m77fe66000)。各训练方式支持的文件格式概览：

**训练方式**

**文件格式**

SFT 文本生成

jsonl（ChatML messages 多轮结构）

SFT 多模态（图片/视频）

zip（data.jsonl + 图片/视频文件）

DPO

jsonl（chosen/rejected 偏好对比）

CPT

jsonl（纯文本 {text}）

评测集

xlsx

也可以前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/data/createDataAss)下载数据模板。

在**新增数据集**页面的上传文件区域下方，可找到**数据模板**下载链接。

### 将调优文件上传至阿里云百炼

#### DashScope API

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --request POST \
'https://dashscope.aliyuncs.com/api/v1/files' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--form 'files=@"/path/to/your/file.jsonl"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="a sample fine-tune data file for qwen"'
```

**说明**使用限制：

-   单个文件大小最大为300MB
-   所有的有效文件（未删除）总使用空间配额为100GB
-   所有的有效文件（未删除）总数量配额为10000个
-   文件存储没有时间限制

通过 API 上传的调优文件，在百炼控制台模型调优页面与 API 调用中均可见可用。

更多详细信息请参见[上传文件](raw/model-api-reference/file-management-api/upload-file-api.md)。

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

## 模型调优

调优任务的创建、查询、日志、快照管理及列举/中止/删除等操作均通过 API 完成，各接口的完整请求/响应参数与示例见对应接口页，本节仅梳理操作流程。

### 创建调优任务

调用[创建调优任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口（`POST /api/v1/fine-tunes`）发起训练，请求体（model / training\_datasets / hyper\_parameters / training\_type 等）与响应示例见该接口页。

支持的基础模型ID（ model ）列表与训练类型（ training\_type ）支持情况：

##### 支持的模型

#### 文本生成

**说明**Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理。

**模型服务**

**模型代码**

**CPT全参训练**

**SFT全参训练**

**SFT高效训练**

**DPO全参训练**

**DPO高效训练**

Qwen3.8-27B

qwen3.8-27b

×

✓

✓

×

×

Qwen3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

×

✓

×

×

×

Qwen3.6-27B

qwen3.6-27b

×

✓

✓

×

×

Qwen3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

×

✓

×

×

×

Qwen3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

✓

✓

×

×

×

Qwen3.5-27B

qwen3.5-27b

×

✓

✓

×

×

Qwen3.5-9B

qwen3.5-9b

×

✓

✓

×

×

Qwen3.5-4B

qwen3.5-4b

×

✓

✓

×

×

Qwen3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

×

✓

×

×

×

Qwen3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

×

✓

×

×

×

Qwen3-32B

qwen3-32b

✓

✓

✓

✓

✓

Qwen3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

✓

✓

✓

×

×

Qwen3-14B

qwen3-14b

×

✓

✓

✓

✓

Qwen3-8B

qwen3-8b

×

✓

✓

✓

✓

Qwen3-4B-Instruct-2507

qwen3-4b-instruct-2507

✓

✓

✓

✓

✓

Qwen3-1.7B

qwen3-1.7b

✓

✓

✓

✓

✓

Qwen3-0.6B

qwen3-0.6b

✓

✓

✓

✓

✓

Qwen2.5-72B-Instruct

qwen2.5-72b-instruct

✓

✓

✓

✓

✓

Qwen2.5-32B-Instruct

qwen2.5-32b-instruct

✓

✓

✓

✓

✓

Qwen2.5-14B-Instruct

qwen2.5-14b-instruct

✓

✓

✓

✓

✓

Qwen2.5-7B-Instruct

qwen2.5-7b-instruct

✓

✓

✓

✓

✓

决策模型（预览版）-2026-09-24

decision-model-preview-2026-09-24

×

×

×

×

×

千问-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

×

✓

✓

✓

✓

**说明**决策模型（`decision-model-preview-2026-09-24`）不参与上述常规 CPT/SFT/DPO 训练，但支持专属微调流程；微调方法请参见[决策模型微调最佳实践](raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

#### 视觉理解（千问VL）

**模型服务**

**模型代码**

**CPT全参训练**

**SFT全参训练**

**SFT高效训练**

**DPO全参训练**

**DPO高效训练**

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

×

✓

✓

×

×

Qwen3-VL-8B-Thinking

qwen3-vl-8b-thinking

×

✓

✓

×

×

Qwen3-VL-4B-Instruct

qwen3-vl-4b-instruct

×

✓

✓

×

×

Qwen2.5-VL-72B-Instruct

qwen2.5-vl-72b-instruct

×

✓

✓

×

×

Qwen2.5-VL-32B-Instruct

qwen2.5-vl-32b-instruct

×

✓

✓

×

×

Qwen2.5-VL-7B-Instruct

qwen2.5-vl-7b-instruct

×

✓

✓

×

×

###### 调优方法对比

**特性**

**CPT（持续预训练）**

**SFT （监督微调）**

**DPO （直接偏好优化）**

一句话总结

补知识**（**注入领域知识**）**

学做事**（**学会遵循指令**）**

做得更好**（**对齐人类偏好**）**

输入数据

1000万+ Token

无标签的领域文本

1000+ 条

高质量的“问-答”对

100+ 组

同一指令下的“更好-更差”回答对

核心目标

领域适应，学习专业词汇和事实

教会模型对话格式和任务执行能力

使模型输出更符合人类价值观和偏好

学习方式

自监督学习（预测下一个词**）**

监督学习**（**模仿标准答案**）**

直接偏好学习**（**增大好答案概率，降低坏答案概率**）**

模型阶段

通常在 SFT 之前

CPT 之后，DPO 之前

通常在 SFT 之后，作为对齐的最后一步

###### 训练模式对比

**全参训练**

**高效训练 （LoRA，推荐）**

**适用场景**

• 需要模型学习新能力

• 追求全局效果最优

• 优化模型特定场景下的效果

• 对训练时间和成本敏感的场景

**训练时间**

较长，收敛速度较慢。

较短，收敛速度快。

### 查询调优任务详情

使用 job\_id 查询任务状态，详见[查询调优任务状态](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api#faa99e295ckyg)。

### 获取调优任务日志

训练日志通过[查询调优任务日志](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api#e76df8eaa2vbs)接口获取（`GET /api/v1/fine-tunes/{job_id}/logs`）。

### 查询与发布模型参数快照

调优产出的 Checkpoint 可列举与导出（发布）：

-   列举快照见[列举 Checkpoint](https://help.aliyun.com/zh/model-studio/list-checkpoints-api#51ryvkmpq074r)（`GET /api/v1/fine-tunes/{job_id}/checkpoints`）。
-   导出（发布）指定快照见[导出 Checkpoint](https://help.aliyun.com/zh/model-studio/list-checkpoints-api#a7k3m9x2q8r4t)（`GET /api/v1/fine-tunes/{job_id}/export/{checkpoint}?model_name=...`），异步执行，用列举接口轮询状态。

### 模型调优的更多操作

-   列举任务列表：[查询调优任务列表](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api#c23cdff6f399h)
-   中止任务：[取消调优任务](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api#3gqm7xoh2njae)
-   删除任务：[删除调优任务](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api#c3mq93izbce81)

## API参考

DashScope命令行调用参考已包含在本篇内容中，详细API调用请参考[API详情](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

## 模型部署&调用

### 模型部署

更多模型部署方式的相关信息请参考：[使用 API 进行模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。

按模型 Token 使用量

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

按模型单元的使用时长

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

### 查询模型部署的状态

当部署状态为`RUNNING`时，表示该模型当前可供调用。

```
curl 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为部署任务成功后的模型实例 ID>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY}  \
--header 'Content-Type: application/json'
```

更多模型部署相关的操作，如扩缩容、下线等请参见：[模型部署-API详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)。

### 模型调用

当模型部署状态为`RUNNING`时，可以像调用其他模型一样使用调优后的模型。

也可以前往[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)界面获取**模型code**。

更多使用方法和参数设置请前往[DashScope API 参考](raw/model-api-reference/qwen-api-reference.md)。

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

## 模型评测

阿里云百炼的模型评测功能必须使用控制台，请前往阿里云百炼的[模型评测](https://bailian.console.aliyun.com/cn-beijing/model/evaluate) 页面，评估模型训练效果。

相关信息请参见[模型评测](https://help.aliyun.com/zh/model-studio/evaluate-models)。

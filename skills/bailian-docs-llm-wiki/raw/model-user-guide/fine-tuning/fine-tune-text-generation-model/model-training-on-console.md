# 在控制台进行模型调优

本文将详细介绍如何在控制台进行模型调优任务，并帮助您选择正确的调优方式与参数。模型调优包含模型微调（SFT）、继续预训练（CPT）、模型偏好训练（DPO）三种模型训练方式。

**重要**

本文档仅适用于中国大陆版（北京地域）。

## **模型调优流程**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5840779771/CAEQZhiBgMDg9PGS2hkiIDNlZDFiMGRlMTJhOTQ1YzJhMmNjNDM3NzQ1ZjNiOGZk4608430_20240830103738.564.svg)

## **步骤一：选择调优方式**

前往[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面，点击“**创建训练任务**”按钮。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1689372671/p1022625.png)

### CPT、**SFT 与 DPO 如何选择**

CPT（继续预训练，Continual Pre-Training）目的是通过海量的无标记训练数据，**提升模型在特定行业的表现。**

SFT-有监督-模型微调（_Supervised Fine-Tuning_）目的是通过针对性的数据集和训练，**提升模型在特定业务的表现。**

DPO-有监督-直接偏好优化（_Direct Preference Optimization_）训练数据集数据同时提供正负样本，通过引入负反馈，降低幻觉，**对bad case进行针对性优化。**

百炼提供的三种调优方式并不互斥，而是递进的、相辅相成的。

`CPT（可选）→ SFT → DPO（可选）`

1.  CPT (持续预训练）- 补知识 （通用模型知识的“广度”和“浅度”，无法满足专业领域的“深度”和“精度”要求）
    
    -   金融模型： `学金融术语`
        
    -   医疗模型： `记药品病理`
        
    -   法律模型： `懂法条判例`
        
2.  SFT (监督微调）- 学做事
    
    -   客服机器人： `学客服流程`
        
    -   代码助手： `学编程范式`
        
    -   工具调用 (Agent)： `学使用 MCP`
        
3.  DPO (直接偏好优化）- 做得更好
    
    -   安全与责任感： `拒有害建议`
        
    -   简洁与有效性： `答干脆利落`
        
    -   客观与中立： `评公正客观`
        

### **SFT 训练集**

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

### SFT 思考模型（thinking）

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

### SFT 视觉理解（千问VL）

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

#### **压缩包要求：**

1.  压缩包格式：ZIP。最大支持 2 GB， ZIP 包内文件夹、文件名仅支持 ASCII 字符集中的字母 (a-z, A-Z)、数字 (0-9)、下划线 (\_)、连字符 (-)。
    
2.  训练文本数据固定为 data.jsonl，并且位于压缩包的**根目录**下，应**确保压缩后打开 zip 文件，直接就能看到** `**data.jsonl**` **文件。**
    
3.  图片单张尺寸的宽度和高度均不得超过 1024px，最大不超过10MB，支持 `.bmp`, `.jpeg /.jpg`, `.png`, `.tif /.tiff`, `.webp` 格式。
    
4.  图片文件的名称不能重复，即使分布在不同的文件夹中。
    
5.  压缩包目录结构：
    
    ##### **单层目录（推荐）**
    
    图片文件与 `data.jsonl` 文件均位于压缩包根目录下。
    
    ```
    Trainingdata_vl.zip
       |--- data.jsonl #注意：外层不能再包裹文件夹
       |--- image1.png
       |--- video1.mp4
    ```
    
    ##### 多层目录
    
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
    

### DPO 数据集

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

### CPT 训练集

CPT 纯文本格式训练数据，**一行训练数据展开后结构如下**：

```
{"text":"文本内容"}
```

训练数据集样例：[CPT-文本生成训练集示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241127/qrtlrz/CPT-%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E8%AE%AD%E7%BB%83%E9%9B%86%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)

两种训练方式的数据量要求请参见[数据集的规模要求](https://help.aliyun.com/zh/model-studio/model-training-overview#94f81fc780fvz)。

**阿里云百炼推荐您以先 CPT（可选），后 SFT，最后 DPO 的顺序使用模型调优：**

1.  先收集海量（至少1000万Token）的特定领域的无标签样本，进行CPT训练，将模型训练成特定行业/领域的专家。
    
2.  在应用上线前，使用足够多（1000+）的特定场景/业务的正样本，即收集场景/业务输入+模型期望输出，进行SFT 训练。
    
3.  您的应用试运行/上线后，收集足够多（100+）的用户反馈（如：点赞、点踩、反馈）或者 bad case，将这些数据制作成 DPO 训练集，进行 DPO 训练。
    

**模型选择**

如果您是第一次进行模型调优，请选择您期望的**预置模型**。

如果您是因为模型训练效果不好需要再次训练某个模型，请选择**自定义模型 > 您需要二次训练的模型。**

支持的预置模型：

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

### **全参训练与高效训练**

-   全参训练通过全量更新模型参数的方式进行学习。
    
-   高效训练采用低秩适应（Low-Rank Adaptation，[LoRA](https://arxiv.org/abs/2106.09685)）的方式，通过矩阵分解的方法，更新分解后的低秩部分参数。
    

由于两种训练方式的费用相同，阿里云百炼推荐您如果**模型支持全参训练，请优先选择全参训练**，因为全参训练效果比高效训练效果要好，性价比更高。

## **步骤二：参数配置**

训练参数介绍：

> 并不是所有模型都支持所有参数的调节，请以控制台显示为准

**参数名称**

**推荐设置**

**超参作用**

批次大小 (batch\_size)

使用默认值

批次大小，代表模型训练过程中，模型更新模型参数的数据步长，可理解为模型每看多少数据即更新一次模型参数，一般建议的批次大小为16/32，表示模型每看16或32条数据即更新一次参数

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1689372671/p1024792.png)

**学习率 (learning\_rate)**

**高效训练：1e-4量级**

**全参训练：1e-5量级**

**CPT训练：1e-5量级**

控制模型修正权重的强度。

如果学习率设置得太高，模型参数会剧烈变化，导致调优后的模型表现不一定更好，甚至变差；

如果学习率太低，调优后的模型表现不会有太大变化。

循环次数 (n\_epochs)

**数据量 < 10,000, 循环 3~5次**

**数据量 > 10,000, 循环 1~2次**

**具体需要结合实验效果进行判断**

模型遍历训练的次数，请根据模型调优实际使用经验进行调整。

模型训练循环次数越多，训练时间越长，训练费用越高。

验证步数 (eval\_steps)

使用默认值

训练阶段针对模型的验证间隔步长，用于阶段性评估模型训练准确率、训练损失。

该参数影响模型调优进行时的 Validation Loss 和 Validation Token Accuracy 的显示频率。

**学习率调整策略 (lr\_scheduler\_type)**

**推荐选择“linear”或“Inverse\_sqrt”。**

在模型训练中动态调整学习率的策略。

各策略详情请参考[学习率调整策略介绍](#a02ce123d5qc1)。

**序列长度 (max\_length)**

**设置为模型支持的最大值**

指的是单条训练数据 token 支持的最大长度。如果单条数据 token 长度超过设定值：

SFT 会直接丢弃该条数据，不进行训练；

DPO 则会自动截断超出配置长度的后续 token，截短后的数据仍会被训练。

字符与 token 之间的关系请参考 [Token和字符串之间怎么换算](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#35d3b2ad2386c)

学习率预热比例 (warmup\_ratio)

使用默认值

学习率预热占用总的训练过程的比例。学习率预热是指学习率在训练开始后由一个较小值线性递增至学习率设定值。

该参数主要是限制模型参数在训练初始阶段的变化幅度，从而帮助模型更稳定地进行训练。

比例过大效果与过低的学习率相同，会导致调优后的模型表现不会有太大变化。

比例过小效果与过高的学习率相同，可能导致调优后的模型表现不一定更好，甚至变差。

`该参数仅对学习率调整策略“Constant”无效。`

权重衰减 (weight\_decay)

使用默认值

L2正则化强度。L2正则化能在一定程度上保持模型的通用能力。数值过大会导致模型调优效果不明显。

**高效训练参数**

LoRA阿尔法 (lora\_alpha)

使用默认值

用于控制原模型权重与LoRA的低秩修正项之间的结合缩放系数。

较大的Alpha值会给予LoRA修正项更多权重，使得模型更加依赖于调优任务的特定信息；

而较小的Alpha值则会让模型更倾向于保留原始预训练模型的知识。

LoRA丢弃率 (lora\_dropout)

使用默认值

LoRA训练中的低秩矩阵值的丢弃率。

使用推荐数值能增强模型通用化能力。

数值过大会导致模型调优效果不明显。

**LoRA秩值 (lora\_rank)**

**设置为模型支持的最大值**

LoRA训练中的低秩矩阵的秩大小。秩越大调优效果会更好一点，但训练会略慢。

是否冻结VIT（freeze\_vit）

使用默认值

用于冻结视觉主干网络的参数，使其在训练过程中不更新权重。仅适用于 千问-VL（视觉理解）模型。

**说明**

只有 freeze\_vit 设置为“true”时，模型才能进行按 [Token 用量](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#9ea9924cd8138)计费。

### **学习率调整策略介绍**

“**学习率调整策略**” 是在 **超参配置 > 更多配置** 下的第一个配置，配置包含8种不同的策略。

策略详情请参见：

Linear：学习率线性递减。

使用场景：适合训练过程较短的任务。

![plot\_linearpng](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p846167.png)

Polynomial：学习率按照一个预定义的多项式函数随训练迭代次数或周期数逐渐减少。

使用场景：Polynomial 可以更精细地控制学习率减少速度，适用于任务比较复杂的场景。

**但内置多项式系数为1，效果同 Linear，不推荐使用。**

![plot\_linearpng](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p846167.png)

Cosine：学习率变化符合余弦函数曲线。

使用场景：适合需要进行精细调整、训练过程较长的任务。![plot\_cosine](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p847202.png)

Cosine\_with\_restarts：学习率按照余弦函数的形状周期性地减少至某个最小值，而且在每个周期结束时，学习率会“重启”成预设值，然后开启下一周期。

使用场景：适用于需要模型从局部最优解中跳出来，尝试寻找更好全局解的情况。

**但经过实测，学习率并不会在函数曲线底部“重启”成预设值，不推荐使用。**![plot\_cosine](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p847202.png)

Constant：学习率不变, “学习率预热比例”参数无效。

使用场景：适合初步探索模型性能。![constant](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p846163.png)

Constant\_with\_warmup：学习率不变，但“学习率预热比例”参数有效。

使用场景：适合初步探索模型性能。![plot\_constant\_with\_warmup](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p846196.png)

Inverse\_sqrt：学习率逐渐减小，减小量与迭代次数的平方根的倒数正相关。

使用场景：适合于 SFT 微调，能较好地平衡学习效率与模型收敛。

![plot\_inverse\_sqrt](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p846497.png)

reduce\_lr\_on\_plateau：当监控的指标（验证损失或验证准确率）在连续多个epoch内没有显著改进时，自动降低学习率。

使用场景：当模型很难进一步提高性能时，reduce\_lr\_on\_plateau 可以帮助模型继续优化和提升。

![plot\_reduce\_lr\_on\_plateau](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007176271/p846471.png)

**说明**

图中学习率下限梯度、最小值均为示意，实际学习率下限梯度、最小值以实际使用为准。

## **步骤三：选择训练数据**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1689372671/p1025101.png)

数据集构建技巧请参考[数据集构建技巧](https://help.aliyun.com/zh/model-studio/model-training-overview#aebd25a7f1g2v)。上传调优数据集请前往[数据管理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)页面。

## **步骤四：训练产出**

> 仅 SFT 微调训练支持设置该功能设置

**说明**

在百炼平台上，模型调优完成后可以导出参数快照，导出后才能基于此版本的参数快照在百炼上进行模型部署。

导出的参数快照保存在云存储中，暂不支持访问或下载。

在**模型导出**的配置项下，可以设置：

-   **模型名称**：设置训练产出模型的名称。训练完成后，产出的最后一个 Checkpoint 将以该名称自动发布至**我的模型**。
    
-   **保存模型数量限制**：设置最多保留的 Checkpoint 数量。
    
-   **模型加密**（安全升级）：开启后，平台会为模型文件启用 OSS 服务端加密，使用 OSS 完全托管密钥进行加解密（SSE-OSS），加密算法为 AES256。
    

## **步骤五：**训练模型

点击“**开始训练**” > 确认“**模型调优计费提醒**” > 模型开始训练。

> 如遇权限不足，请参考：[模型调优时报权限不足怎么办？](#7aa5abac6e3pm)

模型训练时点击”**查看日志**”按钮可以查询模型训练过程中实时产生的日志，也可以前往**指标**标签页查看训练损失（Training Loss）、验证损失（Validation Loss）、验证准确率（Validation Token Accuracy）。

**训练完成后**，请确认训练损失（Training Loss）与验证损失（Validation Loss）的差异变化趋势。

1.  如果**训练损失逐渐减小而验证损失逐渐增大**，说明模型已经过拟合训练数据，训练可能失败，训练效果可能不佳。建议按照**以下推荐方法（推荐程度有先后顺序）进行优化，重新训练**，提升训练效果**：**
    
    1.  使用数据增强，增加训练数据多样性和数据量。
        
    2.  收集更多训练数据，增加训练数据多样性和数据量。
        
    3.  调整超参，包括：减少“训练次数”、减小“学习率”、减小“批次大小”、增大“权重衰减”、提高“LoRA丢弃率”、提高“学习率预热比例”。
        
2.  如果**训练损失没有明显变化或逐渐增大（不常见），**说明模型欠拟合训练数据，训练失败。建议按照**以下推荐方法（推荐程度有先后顺序）进行优化，继续训练：**
    
    1.  检查数据质量，确保数据清洗充分。
        
    2.  调整超参，包括：增大“训练次数”、增大“学习率”、增大“批次大小”、减小“权重衰减”、降低“LoRA丢弃率”、降低“学习率预热比例”。
        
3.  如果没有上述情况请继续后续步骤。
    

## **步骤六：发布模型用于部署**

> 仅 SFT微调训练支持选择发布训练中间状态的模型快照

模型训练完成后，根据[步骤四：训练产出](#ae6a2ec3ee3nw)中的配置，产出的最后一个 Checkpoint 会以设定的模型名称**自动发布**至[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)页面。

如需发布其他训练中间阶段的 Checkpoint，可以在训练任务详情页的**产出**标签页中查看所有保存的 Checkpoint 列表，选择目标 Checkpoint 并点击**发布模型**。

**产出**标签页中包含以下信息：Checkpoint ID、训练保存信息、模型发布状态、模型名称、剩余保存时长、创建时间、操作。

**说明**

Checkpoint 有保存时长限制，超过保存时长后将被自动清理，届时将无法再发布该 Checkpoint。请及时发布所需的模型快照。

发布完成后的模型可以在[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)页面查看，并进行部署。

## **步骤七：部署模型**

前往[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)页面中快速查询模型支持的部署模式、模型 ID 等相关信息，部署好后就可以对调优好的模型进行评测。模型部署相关信息请参见[帮助中心：模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

## **步骤八：**评测**模型**

**重要**

如果您有多个业务场景或者添加了混合训练数据，在模型评测时，建议您根据场景拆分评测集，分别评测各个场景在调优后的表现是否满足您的需求。

使用阿里云百炼[模型评测](https://bailian.console.aliyun.com/?tab=model#/efm/model_evaluate)功能评估自定义模型的训练效果，相关信息请参见[帮助中心：模型评测简介](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5840779771/CAEQaxiBgICsmePZ3RkiIGI2M2Y2M2M0MjI5NjQwZmE5YWJhMjgwMjNhZGY3ZGQ04464811_20240625101944.455.svg)

## **常见问题**

### **什么时候可以使用模型调优功能？**

-   如果您并不是需要对文本生成模型进行调优，请直接前往[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)页面。
    
-   文本生成模型调优虽然能在特定业务/场景取得非常好的效果，但有以下限制：
    
    -   **耗时较长**，包括：拥有一个大规模（最少 0.5亿 token）CPT 数据集、构建一个有效（1000+）SFT 数据集、收集足够的（100+）Bad Case 构建[模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing#2083766ef99p1)有效 DPO 数据集、模型优化迭代速度慢等。
        
    -   **费用较高，**调优后的模型部署后才能使用，[模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing#2083766ef99p1)较高。
        
-   阿里云百炼推荐您在考虑使用文本生成模型调优前**先尝试使用**的 [Prompt 工程](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide)**（****_Prompt Engineering_****）或**[插件调用](https://help.aliyun.com/zh/model-studio/plug-in-overview)**（****_Function Calling_****）**定制化您的应用，**模型调优也通常作为改进模型表现“最后的手段”**。因为：
    
    1.  在许多任务中，模型最初可能表现不佳，但通过应用正确的 Prompt 技巧可以改进结果，不一定需要使用模型调优。
        
    2.  迭代优化 Prompt、插件，比模型调优的迭代更敏捷、成本更低，因为模型调优的迭代可能需要重新收集数据、清洗优化数据、收集 bad case、发起客户调研等。
        
    3.  即使最后一定要进行模型调优，最初的 Prompt 工程、插件迭代优化相关工作也不会浪费。您的这些前期工作可以充分地在构建调优数据集时复用（用于构建数据集的输入）。
        

### **模型调优时报权限不足怎么办？**

请联系您的平台或空间管理员，检查并开通以下权限：

1.  账号拥有发起调优任务所在的业务空间下 **模型调优-操作**、**模型部署-操作**、**模型评测-操作** 的页面权限。
    
    相关介绍请参考：[账户权限管理](https://help.aliyun.com/zh/model-studio/permission-management-overview#1d8ad43a66nch)。控制台链接：[百炼-账号管理](https://bailian.console.aliyun.com/tab=globalset#/user_management/user_management)。
    
    ![PixPin\_2025-11-13\_20-34-22](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1609363671/p1026621.png)
    
2.  需要发起调优任务所在的业务空间拥有对**特定模型**进行**模型训练**（调优）的权限。
    
    相关介绍请参考：[授权子业务空间模型调用、训练和部署](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。控制台链接：[百炼-业务空间管理](https://bailian.console.aliyun.com/tab=globalset#/efm/business_management)。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7796981671/p1022425.png)
    

### **如果模型调优后，评测的效果不好怎么办？**

1.  如果您使用的是人工评测，请检查评测维度是否符合业务或场景。
    
2.  收集在模型评测时评测结果不佳的测试用例，统计分析评测结果不佳的原因，根据分析结果调整训练数据集，继续迭代调优模型。
    
3.  根据评测结果不佳的用例生成 DPO 用例，对模型进行 DPO 训练。
    

### **模型调优、模型部署、模型评测怎么收费？**

模型调优计费方式与模型调用计费方式相同，但费用会更高。训练好的模型在部署后只收取部署费用，不收取模型的调用费用。模型评测不额外收费。详细数据请参考[模型训练与部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。

### **还有什么方法能进行模型调优？**

-   在百炼平台上还可以[使用 API 进行模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide)。
    
-   如果需要上传和微调自己的模型，请前往阿里云人工智能平台 PAI ，进行[模型微调与训练](https://help.aliyun.com/zh/pai/use-cases/model-fine-tuning-and-training/)。
    

### **在阿里云百炼调优完成的模型可以下载到本地部署吗？**

阿里云百炼平台进行调优的模型不支持导出，只支持在阿里云百炼上部署后测试、调用。

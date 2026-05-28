# 模型调优简介

当您在尝试如 Prompt 工程、插件调用等优化方法后，模型表现仍然不及预期时，请使用阿里云百炼的模型调优。模型调优作为改进模型表现的核心策略，可以很好地提升模型在特定行业/业务的表现，对齐人类偏好，降低输出延迟。模型调优包含模型微调（SFT）、继续预训练（CPT）、模型偏好训练（DPO）三种模型训练方式。

**重要**

本文档仅适用于中国大陆版（北京地域）。

## **模型调优介绍**

模型调优作为重要的模型效果优化方式，可以：

-   **提升模型在特定行业/业务表现**
    
-   **降低模型输出延迟**
    
-   **抑制模型幻觉**
    
-   **对齐人类的价值观或偏好**
    
-   **使用调优后的轻量级模型替代规模更大的模型**
    

模型在调优过程中，会学习训练数据中的知识、语气、表达习惯、自我认知等业务/场景特征。也由于已经在训练过程中学习到了大量特定行业/场景的样例，训练后模型 One-Shot 或者 Zero-Shot 的 Prompt 效果会比训练前 Few-Shot 效果更好，这样可以节省大量输入 token，从而降低模型输出延迟。

#### **模型调优流程**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6780689771/CAEQZhiBgMDg9PGS2hkiIDNlZDFiMGRlMTJhOTQ1YzJhMmNjNDM3NzQ1ZjNiOGZk4608430_20240830103738.564.svg)

阿里云百炼模型调优功能还支持：[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)

详情参见：

#### **支持的模型**

## 文本生成

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

> `-Base`表示该模型只完成了预训练，虽然模型内已经存储了海量的知识，但无法正常进行对话。

#### **调优方法对比**

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

#### **训练模式对比**

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

## 视觉理解（千问VL）

**模型服务**

**模型代码**

**CPT全参训练（cpt）**

**SFT全参训练（sft）**

**SFT高效训练（sft\_efficient）**

**DPO全参训练（dpo\_full）**

**DPO高效训练（dpo\_lora）**

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

×

支持

支持

×

×

Qwen3-VL-8B-Thinking

qwen3-vl-8b-thinking

×

支持

支持

×

×

Qwen3-VL-4B-Instruct

qwen3-vl-4b-instruct

×

支持

支持

×

×

Qwen2.5-VL-72B-Instruct

qwen2.5-vl-72b-instruct

×

支持

支持

×

×

Qwen2.5-VL-32B-Instruct

qwen2.5-vl-32b-instruct

×

支持

支持

×

×

Qwen2.5-VL-7B-Instruct

qwen2.5-vl-7b-instruct

×

支持

支持

×

×

> `-Base`表示该模型只完成了预训练，虽然模型内已经存储了海量的知识，但无法正常进行对话。

#### **调优方法对比**

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

#### **训练模式对比**

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

## 语音识别-热词定制与管理

**模型代码**

**热词定制与管理**

**CPT**

**全参训练**

**SFT**

**全参训练**

**SFT**

**高效训练**

**DPO**

**全参训练**

**DPO**

**高效训练**

paraformer-realtime-v1（仅API）

![hailuo\_652023034\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5896176271/p842709.png)

paraformer-realtime-8k-v1（仅API）

![hailuo\_652023034\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5896176271/p842709.png)

paraformer-8k-v1（仅API）

![hailuo\_652023034\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5896176271/p842709.png)

paraformer-v1（仅API）

![hailuo\_652023034\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5896176271/p842709.png)

paraformer-mtl-v1（仅API）

![hailuo\_652023034\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5896176271/p842709.png)

paraformer-v2（仅API）

![hailuo\_652023034\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5896176271/p842709.png)

热词定制与管理：管理热词表，提升热词表内词汇的识别效果。

## 计费说明

**计费方式**

按训练的数据量计费

**计费公式**

模型训练费用 = （训练数据 Token 总数 + 混合训练数据 Token 总数）× 循环次数 × 训练单价（最小计费单位：1 token）

> 您可以查看[模型调优控制台](https://bailian.console.aliyun.com/#/efm/model_manager/create)底部的预估训练费用，并单击**计算详情**，查看训练 Token 总数、循环次数和训练单价**。**

**训练单价**

以下为预置模型的训练单价，自定义模型的训练单价与对应的预置模型单价相同。

## 千问

**模型服务**

**模型代码**

**价格**

Qwen3.5-27B

qwen3.5-27b

¥0.05/千Token

Qwen3.5-9B

qwen3.5-9b

¥0.02/千Token

Qwen3-32B

qwen3-32b

¥0.04/千Token

Qwen3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

¥0.03/千Token

Qwen3-14B

qwen3-14b

¥0.03/千Token

Qwen3-8B

qwen3-8b

¥0.006/千Token

Qwen3-1.7B

qwen3-1.7b

¥0.0045/千Token

Qwen3-0.6B

qwen3-0.6b

¥0.003/千Token

Qwen2.5-72B-Instruct

qwen2.5-72b-instruct

¥0.15/千Token

Qwen2.5-32B-Instruct

qwen2.5-32b-instruct

¥0.03/千Token

Qwen2.5-14B-Instruct

qwen2.5-14b-instruct

¥0.03/千Token

Qwen2.5-7B-Instruct

qwen2.5-7b-instruct

¥0.006/千Token

千问-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

¥0.15/千Token

## 千问VL

**模型服务**

**模型代码**

**价格**

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.012/千Token

Qwen3-VL-8B-Thinking

qwen3-vl-8b-thinking

¥0.012/千Token

Qwen3-VL-4B-Instruct

qwen3-vl-4b-instruct

¥0.006/千Token

Qwen2.5-VL-72B-Instruct

qwen2.5-vl-72b-instruct

¥0.05/千Token

Qwen2.5-VL-32B-Instruct

qwen2.5-vl-32b-instruct

¥0.02/千Token

Qwen2.5-VL-7B-Instruct

qwen2.5-vl-7b-instruct

¥0.01/千Token

## **模型调优前必读**

-   如果您并不是需要对文本生成模型进行调优，请直接前往[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)页面。
    
-   文本生成模型调优虽然能在特定业务/场景取得非常好的效果，但有以下限制：
    
    -   **耗时较长**，包括：拥有一个大规模（最少 0.5亿 token）CPT 数据集、构建一个有效（1000+）SFT 数据集、收集足够的（100+）Bad Case 构建[模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing#2083766ef99p1)有效 DPO 数据集、模型优化迭代速度慢等。
        
    -   **费用较高，**调优后的模型部署后才能使用，[模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing#2083766ef99p1)较高。
        
-   阿里云百炼推荐您在考虑使用文本生成模型调优前**先尝试使用**的 [Prompt 工程](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide)**（****_Prompt Engineering_****）或**[插件调用](https://help.aliyun.com/zh/model-studio/plug-in-overview)**（****_Function Calling_****）**定制化您的应用，**模型调优也通常作为改进模型表现“最后的手段”**。因为：
    
    1.  在许多任务中，模型最初可能表现不佳，但通过应用正确的 Prompt 技巧可以改进结果，不一定需要使用模型调优。
        
    2.  迭代优化 Prompt、插件，比模型调优的迭代更敏捷、成本更低，因为模型调优的迭代可能需要重新收集数据、清洗优化数据、收集 bad case、发起客户调研等。
        
    3.  即使最后一定要进行模型调优，最初的 Prompt 工程、插件迭代优化相关工作也不会浪费。您的这些前期工作可以充分地在构建调优数据集时复用（用于构建数据集的输入）。
        

## **调优效果展示**

#### [**角色扮演**](https://www.aliyun.com/solution/tech-solution-deploy/2978350)

![gungun](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7339071671/p1019093.gif)

#### [**目标检测**](https://www.aliyun.com/solution/tech-solution-deploy/2978352)

![converted-1761653885465](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7339071671/p1020451.gif)

## 快速开始

### **使用控制台进行模型调优**

控制台只支持文本生成模型的调优，详细使用信息请参见[在控制台进行模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console)。

**调优步骤**

**控制台截图**

**步骤一**：在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面点击**创建训练任务**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3889372671/p1024309.png)

**步骤二：训练配置**

-   **训练方式**：**SFT微调训练**
    
-   **选择模型**： 千问3-8B
    
-   **训练方式**：**高效训练**
    
-   **参数配置**：保持默认即可，百炼对微调超参提供了推荐配置。
    

这个组合训练时间短，数据要求低。

**步骤三：数据配置**

-   **训练集**： 在平台上选择构建模型所需的已上传调优数据集。
    
    数据样例：[SFT-ChatML格式示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241014/utjdbx/SFT-ChatML%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)；
    
    训练数据如何构建、上传请参考：[创建数据集](https://help.aliyun.com/zh/model-studio/training-set-and-evaluation-set#4ad23e7460s65)和[构建调优数据](#2f5553c6d832d)。
    
-   **混合训练**： 不开启
    
-   **验证集**：设置为**自动切分**，分割 10% 作为验证集
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3889372671/p1024312.png)

**步骤四：配置模型参数快照（Checkpoint）保存参数**

-   **模型名称**：保持默认即可
    
-   **导出数量上限**：保持默认即可
    
-   **Checkpoint保存间隔**：保持默认即可
    

**说明**

在百炼平台上，模型调优完成后可以导出参数快照，导出后才能基于此版本的参数快照在百炼上进行模型部署。

导出的参数快照保存在云存储中，暂不支持访问或下载。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3889372671/p1024332.png)

**步骤五**：点击“开始训练”后，等待模型训练完毕。

**步骤六**：使用阿里云百炼的[模型部署](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)功能部署训练好的自定义模型，部署好后就可以对调优好的模型进行评测。模型部署相关信息请参见[帮助中心：模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

**步骤七**：使用阿里云百炼[模型评测](https://bailian.console.aliyun.com/?tab=model#/efm/model_evaluate)功能评估自定义模型的训练效果，相关信息请参见[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)。

## **典型的调优流程**

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
        

## **调优数据格式**

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

## SFT 思考模型（thinking）

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

## SFT 视觉理解（千问VL）

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
    
    ### **单层目录（推荐）**
    
    图片文件与 `data.jsonl` 文件均位于压缩包根目录下。
    
    ```
    Trainingdata_vl.zip
       |--- data.jsonl #注意：外层不能再包裹文件夹
       |--- image1.png
       |--- video1.mp4
    ```
    
    ## 多层目录
    
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
    

## DPO 数据集

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

## CPT 训练集

CPT 纯文本格式训练数据，**一行训练数据展开后结构如下**：

```
{"text":"文本内容"}
```

训练数据集样例：[CPT-文本生成训练集示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241127/qrtlrz/CPT-%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E8%AE%AD%E7%BB%83%E9%9B%86%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)

## **数据集构建技巧**

### **数据集的规模要求**

对于CPT来说，数据集最少需要**五千万Token优质预训练数据**；对于 SFT 来说，数据集最少需要**上千条优质调优数据**；对于 DPO 来说，数据集一般需要**上百条人类偏好数据**。如果数据调优后的模型评测结果不佳，最简单的改进方法是收集更多数据进行训练。

如果您缺乏数据，建议构建[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)，使用知识库索引来增强模型能力。当然在很多复杂的业务场景，可以综合采用模型调优和知识库检索结合的技术方案。

以客服场景为例，可以借助模型调优解决客服回答的语气、表达习惯、自我认知等问题，场景涉及的专业知识可以结合知识库，动态引入到模型上下文中。

阿里云百炼推荐您可以先构建 RAG 应用试运行，在收集到足够的应用数据后再通过模型调优继续提升模型表现。

您也可以采用以下策略扩充数据集：

1.  让大模型模拟生成特定业务/场景的相关内容，辅助您生成更多用于调优数据。（生成模型建议选取表现优异、规模更大的模型）
    
2.  使用阿里云百炼的[数据处理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)功能，对您的数据集进行数据清洗、数据增强。
    
3.  通过应用场景收集、网络爬虫、社交媒体和在线论坛、公开数据集、合作伙伴与行业资源、用户贡献等各种方式，人工获取更多数据。
    

### **数据的多样性与均衡性**

模型调优有不同场景，针对具体业务场景时，专业性更重要；而针对问答场景时通用性更重要。您需要根据模型负责的业务模块或使用场景进行数据用例设计。因此训练效果好坏并不是仅取决于数据量，更需要考虑针对场景的专业性和多样性。

这里以智能 AI 对话场景为例，介绍一个专业、多样的数据集应该包含的各种业务场景：

**具体业务**

**多样化场景/业务**

电商客服

活动推送、售前咨询、售中引导、售后服务、售后回访、投诉处理等。

金融服务

贷款咨询、投资理财顾问、信用卡服务、银行账户管理等。

在线医疗

病症咨询、挂号预约、就诊须知、药品信息查询、健康小建议等。

AI 秘书

IT 信息、行政信息、HR 信息、员工福利解答、公司日历查询等。

旅游出行助手

旅行规划、出入境指南、旅行保险咨询、目的地风土人情介绍等。

企业法律顾问

合同审核、知识产权保护、合规性检查、劳动法律答疑、跨境交易咨询、个案法律分析等。

还请特别注意的是各个场景/业务的数据数量应**相对均衡，数据比例符合实际场景比例**，避免某一类数据过多导致模型偏向于学习该类特征，影响模型的泛化能力。

### **训练集与验证集拆分**

当您使用控制台进行模型调优时，支持

-   自动将一个完整训练数据集拆分，随机抽取少量数据组成验证集。
    
-   选择独立上传数据集。
    

控制台可以在训练时及时方便地显示验证集 Loss 和 Token Accuracy。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3889372671/p1024312.png)

## **详细操作指导**

[在控制台进行模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console)

[使用 API 进行模型调优](https://help.aliyun.com/zh/model-studio/model-training/)

[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)

## **常见问题**

### **是否支持调优自己的模型呢？**

百炼不支持调优自己的模型，但可以通过[我的模型（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_center)导入safetensor 格式的千问系列开源模型，详情请参考[模型导入](https://help.aliyun.com/zh/model-studio/model-import)。模型导入后可以在百炼平台上部署使用。

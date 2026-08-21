# 模型训练与部署计费

本文介绍阿里云百炼平台的模型训练、模型部署的计费规则及价格。

## **模型训练计费**

### **文本生成模型-千问**

**说明**

模型训练流程请参见[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)。训练完成后的新模型需先完成**模型部署**，才能评测和调用。

**计费方式**

按训练Token计费

**计费公式**

模型训练费用 = （训练数据 Token 总数 + 混合训练数据 Token 总数）× 循环次数 × 训练单价（最小计费单位：1 token）

> 您可以查看[模型训练控制台](https://bailian.console.aliyun.com/#/efm/model_manager/create)底部的预估训练费用，并单击**计费详情**，查看训练 Token 总数、循环次数和训练单价。

#### 千问VL

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

#### 千问

**模型服务**

**模型代码**

**价格**

Qwen3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

¥0.35/千Token

Qwen3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

¥0.05/千Token

Qwen3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

¥0.3/千Token

Qwen3.5-27B

qwen3.5-27b

¥0.05/千Token

Qwen3.5-9B

qwen3.5-9b

¥0.02/千Token

Qwen3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

¥0.05/千Token

Qwen3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

¥0.3/千Token

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

Qwen3-4B-Instruct-2507

qwen3-4b-instruct-2507

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

### **图像生成模型-万相**

**说明**

模型训练流程请参见[图像生成模型调优](https://help.aliyun.com/zh/model-studio/wan-image-generation-finetune-guide)。训练完成后的新模型需先完成**模型部署**，才能调用。

**计费方式**

按训练Token计费

**计费公式**

模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token）

**训练Token总量的计算公式**

训练Token总量≈max\_steps×Lstep​

其中：

-   max\_steps：训练时指定的超参数，表示最大训练步数（创建微调任务时配置）。
    
-   Lstep：每步的Token消耗量，计算公式为：
    
    Lstep​\=i∈batch∑​Litem(i)​≤Lmax​
    
    Lstep 近似等于 Lmax。Lmax 由 max\_token\_length 和 generation\_type 共同决定，具体取值如下表：
    

**generation\_type**

**max\_token\_length**

**L****max**

t2i（文生图）

1k

12,800

2k

23,220

i2i（图生图）

1k

23,220

2k

32,000

**模型服务**

**模型名称**

**训练价格（每千Token）**

万相-图像生成

wan2.7-image-pro

0.08元

万相-图像生成

wan2.7-image

0.08元

**计费示例**

假设使用 wan2.7-image-pro 模型进行 t2i 微调，max\_steps = 200，max\_token\_length = "1k"，训练单价 = 0.08元/千Token：

-   查表得 Lmax = 12,800（generation\_type=t2i，max\_token\_length=1k），Lstep ≈ Lmax = 12,800
    
-   训练Token总量 ≈ 200 × 12800 = 2560000 = 2560千Token
    
-   模型训练费用 ≈ 2560 × 0.08 = 204.8元
    

### **视频生成模型-万相**

**说明**

模型训练流程请参见[模型调优](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-guide)。训练完成后的新模型需先完成**模型部署**，才能调用。

**计费方式**

按训练Token计费

**计费公式**

模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token）

**训练Token总量的计算公式**

训练Token总量\=(i\=1∑N​视频i​的计费时长)×1024max\_pixels​×n\_epochs

其中：

-   N：训练集中的视频总数。
    
-   max\_pixels：训练时指定的超参数，表示视频的最大像素数（创建微调任务时配置）。
    
-   n\_epochs：训练时指定的超参数，表示循环次数（创建微调任务时配置）。
    
    -   n\_epochs 与 steps 的换算关系为：`steps = n_epochs × ⌈数据集大小 / batch_size⌉`，即 `n_epochs = steps / ⌈数据集大小 / batch_size⌉`。
        
    -   当数据集仅包含 1 条数据且 batch\_size = 1 时，n\_epochs = steps。建议总步数（steps）≥ 800。
        
-   单个视频计费时长计算规则：先将原始视频时长（秒）四舍五入取整，再根据模型限制取最终值。
    
    -   wan2.7模型：`计费时长=min(10, 四舍五入后的时长)`，即单条视频最多按 10 秒计算。
        
    -   wan2.5模型：`计费时长=min(10, 四舍五入后的时长)`，即单条视频最多按 10 秒计算。
        
    -   wan2.2模型：`计费时长=min(5, 四舍五入后的时长)`，即单条视频最多按 5 秒计算。
        

**模型服务**

**模型名称**

**训练价格（每千Token）**

万相-图生视频-基于首帧

wan2.7-i2v

2元

wan2.2-i2v-flash

0.06元

wan2.5-i2v-preview

0.32元

图生视频-基于首尾帧

wan2.2-kf2v-flash

0.06元

**计费示例**

1.  **wan2.7-i2v 费用预估（一条数据）**
    

假设训练集包含 1 条视频，时长为10秒。由于 batch\_size = 1（推荐值），此时 `n_epochs = steps / ⌈1(数据集大小) / 1(batch_size)⌉ = steps`。

训练单价 = 2元/千Token，以 max\_pixels = 36864、n\_epochs = 800 为例：

-   训练Token总量 = 10 ×（36864 / 1024）× 800 = 288,000 = 288千Token
    
-   模型训练费用 = 288 × 2 = 576元
    

**max\_pixels**

**常见 steps**

**n\_epochs**

**Token 消耗预估**

**费用预估（元）**

36864

800

800

288,000

576

1,000

1,000

360,000

720

2,000

2,000

720,000

1,440

65536

800

800

512,000

1,024

1,000

1,000

640,000

1,280

2,000

2,000

1,280,000

2,560

102400

800

800

800,000

1,600

1,000

1,000

1,000,000

2,000

2,000

2,000

2,000,000

4,000

2.  **wan2.7-i2v 费用预估（多条数据）**
    

假设训练集包含 2 条视频，时长分别为 3.4 秒 和 11.5 秒。参数设置：max\_pixels = 36864、n\_epochs = 800，训练单价 = 2元/千Token：

-   时长计算：
    
    -   视频 1：3.4 → 四舍五入 → 3 秒 → 计费时长 = min(10, 3) = 3
        
    -   视频 2：11.5 → 四舍五入 → 11 秒 → 计费时长 = min(10, 11) = 10
        
    -   总计费时长 = 3 + 10 = 13 秒
        
-   训练Token总量 = 13 ×（36864/1024）× 800 = 374400 = 374.4千Token
    
-   模型训练费用 = 374.4 × 2 = 748.8元
    

### **语音合成模型-CosyVoice**

**说明**

CosyVoice 模型调优服务仅支持**华北2（北京）**地域。模型训练流程请参见[CosyVoice模型调优](https://help.aliyun.com/zh/model-studio/fine-tune-speech-synthesis-model-by-api)。训练完成后的新模型需先完成**模型部署**，才能调用。

**计费方式**

按训练消耗的Token数计费

**训练单价**

0.2元/千Tokens

**计费公式**

模型训练费用 = 训练消耗Token总量 × 训练单价

**训练消耗Token总量的计算公式**

单次任务的Token消耗按下式估算：

消耗 Tokens\=(lm\_max\_epoch+fm\_max\_epoch)×25×训练集总时长(秒)

其中 `lm_max_epoch` 与 `fm_max_epoch` 为创建调优任务时设置的超参数，分别表示 LM 与 FM 训练轮次；训练集总时长为调优数据集中全部音频文件的总秒数。提高任一轮次或扩大训练集均会线性增加 Token 消耗。

## **模型部署计费**

### **文本生成模型-千问**

#### 按使用时长计费（预置吞吐）

`**费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)**`

后付费按小时计算：使用时长单位为小时，单价取下表"持续 1 小时"列；预付费按天计算：使用时长单位为天，单价取下表"持续 1 天"列。

-   预付费订单支付后实时生效，有效期 N 天至第 N 天 23:59 结束。若在 22:00 后下单，到期日将自动顺延1天。
    
-   预付费订单到期后，将延后2小时停止服务，停止后资源保留14小时后释放。
    
-   预付费订单无法提前终止服务。
    
-   后付费时，如果账户欠费，部署的资源将继续保留并计费 24 小时，在这 24 小时内服务仍可正常使用。超过 24 小时后系统停止计费，模型部署进入欠费状态，底层资源将被删除，但模型部署任务仍会保留。补足欠费后，系统将重新分配资源并恢复使用（恢复后继续产生费用）。如果您不希望继续产生费用，可删除模型部署任务，删除成功后将不再计费。
    

当模型输入超过最长输入 Token 时，相关调用将自动切换为当前模型的按量付费模式；超出购买的 TPM 量时，按创建时选择的溢出策略处理（「自动溢出」切换为按量付费，「仅使用 PTU 容量」返回 429）。此时，推理性能可能下降，将受业务空间中当前快照模型的公共流量的管控，[费用](https://help.aliyun.com/zh/model-studio/model-pricing)按模型调用（按量付费）标准计收。

-   此时（仅「自动溢出」策略下），调用 API 返回 Header 将包含：`x-dashscope-ptu-overflow:true`。
    
-   TPM 统计请前往：[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)。
    

缩容场景（降配）的具体降费退费规则请参考：[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

**说明**

PTU 部署支持长输入阶梯容量系数和缓存折扣，详见[预置吞吐长输入与缓存](https://help.aliyun.com/zh/model-studio/ptu-long-input-and-cache)。

##### 华北2（北京）

###### 千问

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3.8-Max

qwen3.8-max

1M

¥28.8

¥8.64

¥345.6

¥103.68

千问3.7-Flash-2026-07-15 联系商务经理开通

qwen3.7-flash-2026-07-15

128K

¥0.48

¥0.19

¥5.76

¥2.3

千问3.7-Max-2026-05-20

qwen3.7-max-2026-05-20

256K

¥28.8

¥8.64

¥345.6

¥103.68

千问3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

256K

¥4.8

¥1.92

¥57.6

¥23.04

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

128K

¥4.8

¥2.88

¥57.6

¥34.56

千问3.5-Plus-2026-04-20

qwen3.5-plus-2026-04-20

128K

¥1.92

¥1.15

¥23.04

¥13.82

千问3-Max-2025-09-23

qwen3-max-2025-09-23

128K

¥7.68

¥3.08

¥92.16

¥36.96

千问-Flash-2025-07-28

qwen-flash-2025-07-28

128K

¥0.36

¥0.36

¥4.32

¥4.32

千问-Plus-2025-12-01

qwen-plus-2025-12-01

128K

¥1.92

非思考：¥0.48

思考：¥1.92

¥23.04

非思考：¥5.76

思考：¥23.04

###### DeepSeek

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

DeepSeek-v4-Flash

deepseek-v4-flash

256K

¥3.6

¥0.72

¥43.2

¥8.64

DeepSeek-v4-Flash-0731

deepseek-v4-flash-0731

64K

¥7.2

¥1.44

¥86.4

¥17.28

DeepSeek-v4-Pro

deepseek-v4-pro

256K

¥43.2

¥8.64

¥518.4

¥103.68

DeepSeek-v3

deepseek-v3

64K

¥7.2

¥2.88

¥86.4

¥34.56

###### 千问VL

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

128K

¥2.4

¥2.4

¥28.8

¥28.8

###### GLM

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

GLM-5.2

glm-5.2

1M

¥28.8

¥10.08

¥345.6

¥120.96

##### 新加坡

###### 千问

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3.8-Max

qwen3.8-max

1M

¥35.97

¥10.79

¥431.7

¥129.5

千问3.7-Flash-2026-07-15 联系商务经理开通

qwen3.7-flash-2026-07-15

128K

¥0.54

¥0.23

¥6.47

¥2.81

千问3.7-Max-2026-05-20

qwen3.7-max-2026-05-20

256K

¥44.97

¥13.49

¥539.6

¥161.87

千问3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

256K

¥7.19

¥2.88

¥86.3

¥34.53

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

128K

¥9

¥5.4

¥107.9

¥64.75

千问3.5-Plus-2026-04-20

qwen3.5-plus-2026-04-20

128K

¥7.2

¥4.32

¥86.3

¥51.8

###### DeepSeek

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

DeepSeek-v4-Flash

deepseek-v4-flash

256K

¥5.4

¥1.08

¥64.8

¥12.95

DeepSeek-v4-Flash-0731

deepseek-v4-flash-0731

64K

¥10.79

¥2.16

¥129.5

¥25.9

DeepSeek-v4-Pro

deepseek-v4-pro

256K

¥64.75

¥12.95

¥777

¥155.4

###### 千问VL

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

128K

¥3.6

¥2.88

¥43.2

¥34.53

###### GLM

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

GLM-5.2

glm-5.2

1M

¥37.8

¥11.87

¥453.3

¥142.45

#### 按使用时长计费（模型单元）

`**费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价**`

"模型单元单价"在后付费场景下取下表"小时单价"列；预付费按月计费时，公式改为 **包月数 × 模型单元数量 × 月单价**。

-   预付费购买的首月，如在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费（不满一天按一天计费）
    

**说明**

模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。

##### 文本生成

###### 千问

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3.6-35B-A3B

qwen3.6-35b-a3b

MU1 x 8

¥432

¥208,944

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.6-27B

qwen3.6-27b

MU9 x 1

¥51

¥24,600

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

MU1 x 2

¥108

¥52,236

MU3 x 8

¥1,096

¥527,752

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

MU1 x 8

MU1 x 16（PD分离模式）

¥432

PD分离模式：¥864

¥208,944

PD分离模式：¥417,888

千问3.5-397B-A17B

qwen3.5-397b-a17b

MU3 x 8

MU3 x 16（PD分离模式）

¥1,096

PD分离模式：¥2,192

¥527,752

PD分离模式：¥1,055,504

MU6 x 16

¥400

¥193,424

千问3.5-122B-A10B

qwen3.5-122b-a10b

MU1 x 4

¥216

¥104,472

MU6 x 16

¥400

¥193,424

千问3.5-35B-A3B

qwen3.5-35b-a3b

MU1 x 2

¥108

¥52,236

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

MU9 x 1

¥51

¥24,600

千问3.5-27B

qwen3.5-27b

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.5-9B

qwen3.5-9b

MU1 x 2

¥108

¥52,236

MU2 x 8

¥504

¥240,288

千问3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

MU1 x 2

¥108

¥52,236

千问3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

MU1 x 8

MU1 x 16（PD分离模式）

¥432

PD分离模式：¥864

¥208,944

PD分离模式：¥417,888

MU2 x 8

¥504

¥240,288

MU3 x 8

MU3 x 16（PD分离模式）

¥1,096

PD分离模式：¥2,192

¥527,752

PD分离模式：¥1,055,504

千问3-235B-A22B-Instruct-2507

qwen3-235b-a22b-instruct-2507

MU1 x 4

¥216

¥104,472

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-32B

qwen3-32b

MU6 x 16

¥400

¥193,424

千问3-30B-A3B-Thinking-2507

qwen3-30b-a3b-thinking-2507

MU1 x 2

¥108

¥52,236

千问3-4B

qwen3-4b

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问3-Embedding-0.6B

qwen3-embedding-0.6b

MU5 x 1

¥21

¥10,139

MU6 x 1

¥25

¥12,089

千问3-MoE-Rerank-0.6B

qwen3-moe-rerank-0.6b

MU5 x 1

¥21

¥10,139

千问3-Rerank-0.6B

qwen3-rerank-0.6b

MU5 x 1

¥21

¥10,139

MU6 x 1

¥25

¥12,089

千问3-Max-2025-09-23

qwen3-max-2025-09-23

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-Rerank

qwen3-rerank

MU5 x 1

¥21

¥10,139

千问2.5-开源版-72B

qwen2.5-72b-instruct

MU1 x 8

¥432

¥208,944

千问2.5-开源版-14B

qwen2.5-14b-instruct

MU1 x 2

¥108

¥52,236

千问2.5-开源版-7B

qwen2.5-7b-instruct

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问-Plus-2025-07-28

qwen-plus-2025-07-28

MU1 x 4

MU1 x 16（PD分离模式）

¥216

PD分离模式：¥864

¥104,472

PD分离模式：¥417,888

千问-Plus-2025-12-01

qwen-plus-2025-12-01

MU1 x 4

¥216

¥104,472

Qwen-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

MU1 x 4

¥216

¥104,472

###### GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

GLM-5.1

glm-5.1

MU2 x 8

¥504

¥240,288

MU3 x 16（PD分离模式）

PD分离模式：¥2,192

PD分离模式：¥1,055,504

MU6 x 16

¥400

¥193,424

GLM-5

glm-5

MU3 x 16（PD分离模式）

PD分离模式：¥2,192

PD分离模式：¥1,055,504

GLM-4.7

glm-4.7

MU6 x 32（PD分离模式）

PD分离模式：¥800

PD分离模式：¥386,848

###### DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

DeepSeek-v4-Flash

deepseek-v4-flash

MU1 x 8

¥432

¥208,944

MU3 x 8

¥1,096

¥527,752

DeepSeek-v3.2

deepseek-v3.2

MU2 x 16（PD分离模式）

PD分离模式：¥1,008

PD分离模式：¥480,576

###### 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

Kimi-K2.5

kimi-k2.5

MU2 x 8

¥504

¥240,288

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。**
    
    该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。
    

##### 多模态

###### 千问VL

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3-VL-235B-A22B-Thinking

qwen3-vl-235b-a22b-thinking

MU1 x 8

¥432

¥208,944

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-VL-32B-Instruct

qwen3-vl-32b-instruct

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问3-VL-4B-Instruct

qwen3-vl-4b-instruct

MU1 x 2

¥108

¥52,236

千问3-VL-2B-Instruct

qwen3-vl-2b-instruct

MU5 x 1

¥21

¥10,139

千问3-VL-Embedding-2B

qwen3-vl-embedding-2b

MU5 x 1

¥21

¥10,139

千问3-VL-Flash-2025-10-15

qwen3-vl-flash-2025-10-15

MU1 x 4

¥216

¥104,472

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

MU1 x 4

¥216

¥104,472

千问VL-Max-2025-08-13

qwen-vl-max-2025-08-13

MU6 x 4

¥100

¥48,356

###### 千问 Omni

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3.5-Omni-Flash

qwen3.5-omni-flash

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。
    

##### 语音合成

**CosyVoice**

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

cosyvoice-v3-flash

cosyvoice-v3-flash

MU5

¥21

¥10,139

#### 按模型 Token 使用量

`**费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）**`

-   仅当对下列基础模型完成 SFT 高效训练（即 LoRA 高效微调，API 部署时 plan 取值为 lora）并得到自定义模型后，才支持按模型 Token 使用量计费。
    

##### 北京

**基础模型**

**模型代码**

**输入**

**元/百万Token**

**输出**

**元/百万Token**

千问3.5-27B 邀测中

qwen3.5-27b

<128K ¥0.6

128K-256K ¥1.8

<128K ¥4.8

128K-256K ¥14.4

千问3-32B

qwen3-32b

非思考模式：¥2

思考模式：¥2

非思考模式：¥8

思考模式：¥20

千问3-14B

qwen3-14b

非思考模式：¥1

思考模式：¥1

非思考模式：¥4

思考模式：¥10

千问3-8B

qwen3-8b

非思考模式：¥0.5

思考模式：¥0.5

非思考模式：¥2

思考模式：¥5

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.5

¥2

##### 新加坡

**基础模型**

**模型代码**

**输入**

**元/百万Token**

**输出**

**元/百万Token**

千问3-14B

qwen3-14b

非思考模式：¥2.569

思考模式：¥2.569

非思考模式：¥10.275

思考模式：¥30.825

### **图像生成模型-万相**

经过SFT-LoRA高效微调的万相图像生成模型，部署免费，调用按微调的基础模型的标准调用价格计费。模型训练和部署流程请参见[图像生成模型调优](https://help.aliyun.com/zh/model-studio/wan-image-generation-finetune-guide)。

**模型名称**

**Lora部署调用价格**

wan2.7-image-pro

0.50元/张

wan2.7-image

0.20元/张

### **语音合成模型-CosyVoice**

**说明**

CosyVoice 模型调优服务仅支持**华北2（北京）**地域。

调优后的CosyVoice模型部署后按**模型单元的使用时长**计费，公式为：费用\=使用时长（小时）×模型单元数量×模型单元单价。

其中，模型单元数量\=单副本模型单元×部署副本数，可选的模版及对应的模型单元类型请参见CosyVoice模型调优的[部署模版](https://help.aliyun.com/zh/model-studio/fine-tune-speech-synthesis-model-by-api#cv-deploy-sub-template-t)。

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

cosyvoice-v3-flash

cosyvoice-v3-flash

MU5

¥21

¥10,139

## **常见问题**

### **Q：**模型部署什么时候开始计费？

A：当模型完成部署，即状态为**运行中**时，开始收取模型部署的费用。模型状态为**部署中**、**欠费**、**部署失败**时，均不会计费。

如果是包月预付费，模型状态为**运行中**后，开始消耗包月时间。

### **Q：**取消模型训练会收费么？

A：**会收费**。主动取消训练后，已消耗的 tokens 仍会推送计费，训练费用按已消耗 tokens 估算，最终费用以账单为准。其他原因导致的训练中断，阿里云百炼不会向您收取训练费用。

### **Q：怎么查看已部署模型的调用统计？**

A：请访问[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)、[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?spm=a2c4g.11186623.0.0.39086143l397a1&tab=model#/model-telemetry)页面。

模型监控页面支持按时间范围（3小时、6小时、12小时、24小时、今天、昨天、一周、自定义）和推理类型筛选，上方汇总区展示模型总量、总调用次数、总失败次数、平均调用时长、平均首包时长，下方模型列表展示各模型的调用总量、调用失败量、失败率、平均调用时长、平均首Token延时等指标，可单击**监控**查看单模型详细数据。

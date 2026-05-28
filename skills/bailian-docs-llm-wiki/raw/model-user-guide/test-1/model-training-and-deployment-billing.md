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

> 您可以查看[模型训练控制台](https://bailian.console.aliyun.com/#/efm/model_manager/create)底部的预估训练费用，并单击**计算详情**，查看训练 Token 总数、循环次数和训练单价。

#### 千问

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

#### 千问VL

**模型服务**

**模型代码**

**价格**

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.015/千Token

Qwen3-VL-8B-Thinking

qwen3-vl-8b-thinking

¥0.015/千Token

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
    
-   单个视频计费时长计算规则：先将原始视频时长（秒）四舍五入取整，再根据模型限制取最终值。
    
    -   wan2.5模型：`计费时长=min(10, 四舍五入后的时长)`，即单条视频最多按 10 秒计算。
        
    -   wan2.2模型：`计费时长=min(5, 四舍五入后的时长)`，即单条视频最多按 5 秒计算。
        

**模型服务**

**模型名称**

**训练价格（每千Token）**

万相-图生视频-基于首帧

wan2.2-i2v-flash

0.06元

wan2.5-i2v-preview

0.32元

图生视频-基于首尾帧

wan2.2-kf2v-flash

0.06元

**计费示例**

假设训练集包含 2 条视频，时长分别为 3.4 秒 和 6.5 秒，max\_pixels = 262144，n\_epochs = 400，训练单价 = 0.06元/千Token：

-   时长计算：
    
    -   视频 1：3.4 → 四舍五入 → 3 秒 → 计费时长 = min(5, 3) = 3
        
    -   视频 2：6.5 → 四舍五入 → 7 秒 → 计费时长 = min(5, 7) = 5
        
    -   总计费时长 = 3 + 5 = 8 秒
        
-   训练Token总量 = 8 ×（262144/1024）× 400 = 819200 = 819.2千Token
    
-   模型训练费用 = 819.2 × 0.06 = 49.152元
    

## **模型部署计费**

### **文本生成模型-千问**

#### 按使用时长计费（预置吞吐）

`**费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)**`

后付费按小时计算：使用时长单位为小时，单价取下表"持续 1 小时"列；预付费按天计算：使用时长单位为天，单价取下表"持续 1 天"列。

-   预付费订单支付后实时生效，有效期 N 天至第 N 天 23:59 结束。若在 22:00 后下单，到期日将自动顺延1天。
    
-   预付费订单到期后，将延后2小时停止服务，停止后资源保留14小时后释放。
    
-   预付费订单无法提前终止服务。
    
-   后付费时，如果账户欠费，部署的资源将保留并继续计费 24 小时，之后自动释放资源。
    

当模型输入超过最长输入 Token 或 超出购买的 TPM 量时，相关调用将自动切换为当前模型的按量付费模式。此时，推理性能可能下降，[限流](https://help.aliyun.com/zh/model-studio/rate-limit)将受业务空间中当前快照模型的公共流量的管控，[费用](https://help.aliyun.com/zh/model-studio/model-pricing)按模型调用（按量付费）标准计收。

-   此时，调用 API 返回 Header 将包含：`x-dashscope-ptu-overflow:true`。
    
-   TPM 统计请前往：[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)。
    

缩容场景（降配）的具体降费退费规则请参考：[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

##### 千问

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM**

**后付费输出**

**Per 1K TPM**

**预付费输入**

**Per 10K TPM**

**预付费输出**

**Per 1K TPM**

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

128,000

¥2.88

¥1.73

¥34.56

¥20.74

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

128,000

¥4.8

¥2.88

¥57.6

¥34.56

千问3.5-Plus-2026-04-20

qwen3.5-plus-2026-04-20

128,000

¥1.92

¥1.15

¥23.04

¥13.82

千问3-Max-2025-09-23

qwen3-max-2025-09-23

128,000

¥7.68

¥3.08

¥92.16

¥36.96

千问-Flash-2025-07-28

qwen-flash-2025-07-28

128,000

¥0.36

¥0.36

¥4.32

¥4.32

千问-Plus-2025-12-01

qwen-plus-2025-12-01

128,000

¥1.92

非思考：¥0.48

思考：¥1.92

¥23.04

非思考：¥5.76

思考：¥23.04

##### DeepSeek

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM**

**后付费输出**

**Per 1K TPM**

**预付费输入**

**Per 10K TPM**

**预付费输出**

**Per 1K TPM**

DeepSeek-v4-Pro

deepseek-v4-pro

64,000

¥43.2

¥8.64

¥518.4

¥103.68

DeepSeek-v3.2

deepseek-v3.2

64,000

¥7.2

¥1.08

¥86.4

¥12.96

DeepSeek-v3

deepseek-v3

64,000

¥7.2

¥2.88

¥86.4

¥34.56

##### 千问VL

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM**

**后付费输出**

**Per 1K TPM**

**预付费输入**

**Per 10K TPM**

**预付费输出**

**Per 1K TPM**

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

128,000

¥2.4

¥2.4

¥28.8

¥28.8

##### 更多模型

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM**

**后付费输出**

**Per 1K TPM**

**预付费输入**

**Per 10K TPM**

**预付费输出**

**Per 1K TPM**

GLM-5.1

glm-5.1

64,000

¥21.6

¥8.64

¥259.2

¥103.68

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

**月单价（元）**

千问3.6-35B-A3B

qwen3.6-35b-a3b

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.6-27B

qwen3.6-27b

MU9

¥51

¥24,600

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

MU1

¥54

¥26,118

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

千问3.5-397B-A17B

qwen3.5-397b-a17b

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

MU6

¥25

¥12,089

千问3.5-122B-A10B

qwen3.5-122b-a10b

MU1

¥54

¥26,118

MU2

¥63

¥30,036

MU6

¥25

¥12,089

MU9

¥51

¥24,600

千问3.5-35B-A3B

qwen3.5-35b-a3b

MU1

¥54

¥26,118

MU2

¥63

¥30,036

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-27B

qwen3.5-27b

MU1

¥54

¥26,118

MU9

¥51

¥24,600

千问3.5-9B

qwen3.5-9b

MU1

¥54

¥26,118

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

MU1

¥54

¥26,118

MU2

¥63

¥30,036

千问3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

千问3-235B-A22B-Instruct-2507

qwen3-235b-a22b-instruct-2507

MU1

¥54

¥26,118

MU2

¥63

¥30,036

千问3-Next-80B-A3B-Instruct

qwen3-next-80b-a3b-instruct

MU1

¥54

¥26,118

千问3-32B

qwen3-32b

MU1

¥54

¥26,118

MU6

¥25

¥12,089

千问3-30B-A3B

qwen3-30b-a3b

MU9

¥51

¥24,600

千问3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

MU1

¥54

¥26,118

MU2

¥63

¥30,036

千问3-8B

qwen3-8b

MU1

¥54

¥26,118

MU2

¥63

¥30,036

MU5

¥21

¥10,139

千问3-4B

qwen3-4b

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问3-1.7B

qwen3-1.7b

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问3-Embedding-0.6B

qwen3-embedding-0.6b

MU5

¥21

¥10,139

MU6

¥25

¥12,089

千问3-MoE-Rerank-0.6B

qwen3-moe-rerank-0.6b

MU5

¥21

¥10,139

千问3-Rerank-0.6B

qwen3-rerank-0.6b

MU5

¥21

¥10,139

MU6

¥25

¥12,089

千问3-Max-2025-09-23

qwen3-max-2025-09-23

MU2

¥63

¥30,036

MU3

¥137

¥65,969

千问3-Rerank

qwen3-rerank

MU5

¥21

¥10,139

千问2.5-开源版-72B

qwen2.5-72b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-32B

qwen2.5-32b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-14B

qwen2.5-14b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-7B

qwen2.5-7b-instruct

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问2.5-开源版-3B

qwen2.5-3b-instruct

MU5

¥21

¥10,139

千问-Flash-2025-07-28

qwen-flash-2025-07-28

MU1

¥54

¥26,118

千问-Plus-2025-07-28

qwen-plus-2025-07-28

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

千问-Plus-2025-12-01

qwen-plus-2025-12-01

MU1

¥54

¥26,118

###### GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

GLM-5

glm-5

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

GLM-4.7

glm-4.7

MU6

¥25

PD分离模式：¥800

¥12,089

PD分离模式：¥386,848

###### DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

DeepSeek-v4-Flash

deepseek-v4-flash

MU1

¥54

¥26,118

DeepSeek-v3.2

deepseek-v3.2

MU2

¥63

PD分离模式：¥1,008

¥30,036

PD分离模式：¥480,576

###### 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

MiniMax-M2.5

MiniMax-M2.5

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

Kimi-K2.5

kimi-k2.5

MU2

¥63

¥30,036

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

**月单价（元）**

千问3.5-Omni-Flash

qwen3.5-omni-flash

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-Omni-Plus

qwen3.5-omni-plus

MU9

¥51

¥24,600

千问3-VL-235B-A22B-Instruct

qwen3-vl-235b-a22b-instruct

MU1

¥54

¥26,118

千问3-VL-235B-A22B-Thinking

qwen3-vl-235b-a22b-thinking

MU1

¥54

¥26,118

千问3-VL-32B-Instruct

qwen3-vl-32b-instruct

MU2

¥63

¥30,036

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

MU1

¥54

¥26,118

千问3-VL-4B-Instruct

qwen3-vl-4b-instruct

MU1

¥54

¥26,118

千问3-VL-2B-Instruct

qwen3-vl-2b-instruct

MU5

¥21

¥10,139

千问3-VL-Embedding-2B

qwen3-vl-embedding-2b

MU5

¥21

¥10,139

千问3-VL-Flash-2025-10-15

qwen3-vl-flash-2025-10-15

MU1

¥54

¥26,118

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

MU1

¥54

¥26,118

千问VL-Max-2025-08-13

qwen-vl-max-2025-08-13

MU6

¥25

¥12,089

千问VL-OCR-2025-11-20

qwen-vl-ocr-2025-11-20

MU6

¥25

¥12,089

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。
    

#### 按模型 Token 使用量

`**费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）**`

-   仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后，才支持按模型 Token 使用量计费。
    

##### 千问

**基础模型**

**模型代码**

**输入**

**元/千Token**

**输出**

**元/千Token**

千问3-32B

qwen3-32b

¥0.002

非思考模式：¥0.008

思考模式：¥0.02

千问3-14B

qwen3-14b

¥0.001

非思考模式：¥0.004

思考模式：¥0.01

千问3-8B

qwen3-8b

¥0.0005

非思考模式：¥0.002

思考模式：¥0.005

千问2.5-开源版-72B

qwen2.5-72b-instruct

¥0.004

¥0.012

千问2.5-开源版-32B

qwen2.5-32b-instruct

¥0.002

¥0.006

千问2.5-开源版-14B

qwen2.5-14b-instruct

¥0.001

¥0.003

千问2.5-开源版-7B

qwen2.5-7b-instruct

¥0.0005

¥0.001

##### 千问VL

**基础模型**

**模型代码**

**输入**

**元/千Token**

**输出**

**元/千Token**

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.0005

¥0.002

千问2.5-VL-72B

qwen2.5-vl-72b-instruct

¥0.016

¥0.048

千问2.5-VL-32B

qwen2.5-vl-32b-instruct

¥0.008

¥0.024

千问2.5-VL-7B

qwen2.5-vl-7b-instruct

¥0.002

¥0.005

#### **图片、视频生成模型（预置）-按实例时长计费**

`**费用 = 资源占用时长（小时）× 实例数量 × 实例单价（不满 1 小时按 1 小时计费）**`

"实例单价"在后付费场景下取下表"后付费单价（元/实例/小时）"列；预付费按月计费时，公式改为 **包月数 × 实例数量 × 预付费单价（元/月）**。

##### 图片生成

**模型服务**

**模型类型**

**独占实例资源规格**

**后付费单价（元/实例/小时）**

**预付费单价**

**（元/月）**

万相-文本生成图像-0521

预置模型

轻量版

¥20/实例/小时

¥10,000/月

##### 视频生成

**模型服务**

**模型类型**

**独占实例资源规格**

**后付费单价（元/实例/小时）**

**预付费单价**

**（元/月）**

悦动人像EMO-detect

预置模型

轻量版

¥20/实例/小时

¥10,000/月

悦动人像EMO

舞动人像AnimateAnyone-detect

舞动人像AnimateAnyone

### **图像和视频生成模型（预置模型）**

**计费方式**

**计费公式**

按实例资源占用时长计费

费用 = 资源占用时长（小时）× 实例数量 × 实例单价（不满1小时按1小时计费）

> 部署前可以在[模型部署控制台](https://bailian.console.aliyun.com/#/efm/model_deploy/create)查看不同模型的预估每小时费用。

实例包月计费/预付费

费用 = 购买时长（月）× 实例数量 × 模型对应的实例单价

购买资源：请前往[模型部署控制台](https://bailian.console.aliyun.com/#/efm/model_deploy)（单击右上角的**资源池管理**）购买。（资源购买完成后便开始计费）

退订资源：请前往主账号的[退订管理](https://usercenter2.aliyun.com/refund/refund)退订。退订后，将根据未用时长退回未使用金额。（不满1天按1天计费）

### 图片生成

**模型服务**

**模型类型**

**独占实例资源规格**

**后付费单价（元/实例/小时）**

**预付费单价**

**（元/月）**

万相-文本生成图像-0521

预置模型

轻量版

¥20/实例/小时

¥10,000/月

### 视频生成

**模型服务**

**模型类型**

**独占实例资源规格**

**后付费单价（元/实例/小时）**

**预付费单价**

**（元/月）**

悦动人像EMO-detect

预置模型

轻量版

¥20/实例/小时

¥10,000/月

悦动人像EMO

舞动人像AnimateAnyone-detect

舞动人像AnimateAnyone

## **常见问题**

#### **Q：**模型部署什么时候开始计费？

A：当模型完成部署，即状态为**运行中**时，开始收取模型部署的费用。模型状态为**部署中**、**欠费**、**部署失败**时，均不会计费。

如果是包月预付费，模型状态为**运行中**后，开始消耗包月时间。

#### **Q：**取消模型训练会收费么？

A：**会收费**。如果您主动取消训练，之前已产生的费用仍会被计算。其他原因导致的训练中断，阿里云百炼不会向您收取训练费用。

#### **Q：怎么查看已部署模型的调用统计？**

A：请访问[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)、[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?spm=a2c4g.11186623.0.0.39086143l397a1&tab=model#/model-telemetry)页面。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8302853471/p936026.png)

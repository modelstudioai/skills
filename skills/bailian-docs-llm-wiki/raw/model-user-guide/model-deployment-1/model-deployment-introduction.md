# 模型部署简介

无论是平台的预置模型还是您[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)后的模型，您可通过部署获得独立的、资源专享的推理服务，以满足您对高并发、低延迟等不同性能的业务需求。

**重要**

本文档仅适用于“中国内地（北京）”地域。

## 计费方式

> 部署前可以在[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)查看不同模型的预估每小时费用。

**说明**

计费方式在服务创建后无法更改。如需切换，必须下线已经部署的模型后再重新部署。

**预置吞吐**

**（高吞吐；高性能）**

**模型单元**

**（自定义性能指标；资源隔离）**

**Token 用量**

**（调优后按量计费/效果验证）**

**定义**

通过平台预留资源，保障特定TPM 吞吐能力的模型部署方式；在保障额度内不限速。

按使用时长与模型单元数量配置算力，资源独占的模型部署方式。

以每次调用产生的输入 Token 与输出 Token 作为用量计量依据的模型部署方式。

**优势**

1.  为**高负载生产环境**提供稳定的吞吐容量、更低的延迟和更强的资源确定性。
    
2.  相比按Token用量计费，TPS（每秒生成的 Token 数）通常提升约 1.5～2.0 倍。
    
3.  支持设置自动续费。
    

1.  延迟/吞吐等**性能指标可自定义**。
    
2.  支持设置自动续费。
    
3.  支持 [PD 分离计算模式](#fb689f3346gjl)。
    

**不使用不计费**。

**支持模型**

部分预置模型

部分预置模型与所有调优后模型

部分经过 LoRA 调优后的模型

**使用场景**

1.  银行App的智能客服（流量稳定，需保障并发体验）。
    
2.  社交平台的实时内容审核（需稳定处理可预估的流水线任务）。
    
3.  公有云翻译API（为标准套餐用户提供基线服务保障）。
    

1.  电商专属微调大模型（部署私有模型，大促时手动扩容）。
    
2.  医药公司的分子筛选模型（需独占资源跑长时任务）。
    
3.  自动驾驶仿真（需要进行长时间持续计算）。
    

调优后模型效果验证

**计费图示**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6346770771/p1052924.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6346770771/p1052921.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6346770771/p1052922.png)

**计费方式**

按使用时长和预置吞吐

随用随付、包天

按使用时长和模型单元数量

随用随付、包月

按模型 Token 使用量

随用随付

**扩缩容方式**

自助增减吞吐量

自助增减模型单元数量

在控制台提交申请，等待人工审核。

**产品约束**

1.  预付费按天计费。无法提前退费
    
2.  如果单位时间内使用超出购买的吞吐量，将自动切换成百炼提供的[模型调用](https://help.aliyun.com/zh/model-studio/model-pricing)服务。
    

预付费购买后，若在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费

1.  只支持部分高效微调（LoRA）后的模型。
    
2.  一个月内不使用将自动释放。
    

如需查看单次调用的 Token 使用量及调用次数历史统计，请前往：[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)。

## **计费详情**

## 按使用时长计费（预置吞吐）

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

## 千问

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

## DeepSeek

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

## 千问VL

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

128,000

¥2.4

¥2.4

¥28.8

¥28.8

## 更多模型

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

GLM-5.1

glm-5.1

64,000

¥21.6

¥8.64

¥259.2

¥103.68

## 按使用时长计费（模型单元）

`**费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价**`

"模型单元单价"在后付费场景下取下表"小时单价"列；预付费按月计费时，公式改为 **包月数 × 模型单元数量 × 月单价**。

-   预付费购买的首月，如在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费（不满一天按一天计费）
    

**说明**

模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。

## 文本生成

## 千问

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

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

## GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

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

## DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

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

## 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

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
    

## 多模态

## 千问VL

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

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

## 千问 Omni

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

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

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。
    

## 按模型 Token 使用量

`**费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）**`

-   仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后，才支持按模型 Token 使用量计费。
    

## 千问

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

## 千问VL

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

## **图片、视频生成模型（预置）-按实例时长计费**

`**费用 = 资源占用时长（小时）× 实例数量 × 实例单价（不满 1 小时按 1 小时计费）**`

"实例单价"在后付费场景下取下表"后付费单价（元/实例/小时）"列；预付费按月计费时，公式改为 **包月数 × 实例数量 × 预付费单价（元/月）**。

## 图片生成

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

## 视频生成

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

如果需要部署更多模型，请参考此[解决方案](https://www.aliyun.com/solution/tech-solution/deepseek-r1-for-platforms)并结合具体业务需求选择最适合的部署方案。

## 部署方法

您可以在控制台上部署模型，请参考以下操作步骤：

> 如果提示权限不足，请参考：[部署时提示权限不足怎么办？](#5c1c099745drz)

1.  前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8117463771/p1059807.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8117463771/p1059808.png)

2.  选择模型、计费方式，其他设置保持默认，最后设置模型名称并开始部署。
    
    > 需先完成[模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console#a6da1accf0dun)，方可部署大部分模型。
    

3.  部署状态为**运行中**时，代表该模型已部署成功。
    

**重要**

模型部署成功后将产生费用。

### **部署配置**

## 模型单元

**配置内容**

**配置详情**

配置模型推理模式

部分模型在以**模型单元**方式部署时，可配置推理模式、最长上下文等。

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

最长上下文

部分模型的**模型单元**部署模式支持该设置。最长上下文长度基于模型类型。

服务限流

部分模型的**模型单元**部署模式支持该设置，可限制模型调用的 RPM、TPM。

## **部署后调用**

模型部署成功后，支持通过 [OpenAI 兼容](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#d397bcc41eu3q)、[Dashscope](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#69cac67a477k2)及[Assistant SDK](https://help.aliyun.com/zh/model-studio/assistant#87b4aacb4bsww)进行调用。

在调用已部署成功的模型时，`model`的取值应为模型部署成功后的模型`code`。请前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)界面获取**模型code**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0929900771/p1051901.png)

示例代码以调用微调后的 qwen3-8b 模型为例：

**说明**

模型特性（是否支持非流式输出、结构化输出等）与[微调前的模型](https://help.aliyun.com/zh/model-studio/models)保持一致。

经过调优的深度思考模型在调用时是否开启深度思考，建议与调优数据格式一致：

-   调优数据含深度思考，调用时建议开启`enable_thinking`参数。
    
-   调优数据不含深度思考，调用时不建议开启`enable_thinking`参数。
    

## DashScope

```
import os
import dashscope

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-14b-xxx-xxx",  # 请替换为模型部署成功后的code
    messages=messages,
    result_format="message",
    enable_thinking=False,
)
print(response)
```

## OpenAI兼容接口

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-14b-xxx-xxx",  # 请替换为模型部署成功后的code
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    extra_body={"enable_thinking": False},
)
print(completion)
```

## 部署服务扩缩容

-   预置吞吐（按时长）：点击**扩缩容**按钮，自助、手动调节实例数量。具体降费退费规则请参考：[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。
    
-   模型单元（按时长）：点击**扩缩容**按钮，自助、手动调节实例数量。
    
-   按 Token 调用量：点击**扩容**按钮，填写并提交扩容申请表单，等待人工审核。
    

## **部署服务下线**

前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，找到要下线的部署服务，点击**下线**并确认。下线后将不再产生计费。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0929900771/p1051902.png)

## **常见问题**

### **可以上传和部署自己的模型吗？**

支持在[我的模型控制台（北京）](https://pre-bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_center)导入部分开源模型，详细支持列表请参考：[模型导入](https://help.aliyun.com/zh/model-studio/model-import)。

此外，阿里云人工智能平台 PAI 提供了部署自有模型的功能，您可以参考[PAI-LLM大语言模型部署](https://help.aliyun.com/zh/pai/user-guide/deploy-an-llm/)了解部署方法。

### **部署时提示权限不足怎么办？**

1.  如果显示**“缺少该模块的权限”**，请确保您的账号在该业务空间的权限管理页面中拥有**模型部署-操作**权限。
    
    ![PixPin\_2025-11-27\_15-09-44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5138594771/p1030122.png)
    
    如果无法正常操作，请联系您的组织或 IT 管理员添加相关权限或代为检查权限问题。
    
2.  如果部署时报错“**xx业务空间没有部署xx模型的权限**”，请前往百炼的[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面，为对应业务空间添加对应模型的部署权限。
    
    > API 调用报错：`Workspace xxx does not have deployment privilege for model xxxx`。
    
    ![PixPin\_2025-11-27\_15-03-57](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030115.png)
    
    ![PixPin\_2025-11-27\_15-06-41](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030118.png)
    
    如果提示权限不足，请联系您的组织或 IT 管理员添加相关权限或代为操作。
    

### **该如何切换到其他的计费方式？**

只能释放原有资源，再通过需要的计费方式创建新资源。

建议按照以下步骤进行切换：

1.  使用需要的计费方式部署新的资源。
    
2.  切换 API 并测试服务可用性。
    
3.  下线释放原有资源。

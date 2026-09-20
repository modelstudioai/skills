# Token 按量部署

按模型 Token 使用量计费的部署方式，仅支持 LoRA 微调模型，不使用不计费，适用于调优后模型效果验证及对并发和延迟要求不高的低成本场景。

## 概述

按 Token 用量计费（**不使用不计费**），仅支持部分经过 LoRA 高效微调的模型，适用于调优后模型效果验证及对并发和延迟要求不高的低成本场景。该模式下吞吐/并发和生成速度均由平台预置，用户不可调。

**说明**计费方式在服务创建后无法更改。如需切换，必须下线已部署模型后重新部署，详见[模型部署简介](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。

## 计费规则

`费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）`

仅当对下列基础模型完成 SFT 高效训练（即 LoRA 高效微调，API 部署时 `plan` 取值为 `lora`）并得到自定义模型后，才支持按模型 Token 使用量计费。

## 支持模型与价格

#### 北京

**基础模型**

**模型代码**

**输入**

**元/百万Token**

**输出**

**元/百万Token**

Qwen3.6-27B

qwen3.6-27b

<256K ¥3

<256K ¥18

Qwen3.5-27B

qwen3.5-27b

<128K ¥0.6

128K-256K ¥1.8

<128K ¥4.8

128K-256K ¥14.4

Qwen3-32B

qwen3-32b

非思考模式：¥2

思考模式：¥2

非思考模式：¥8

思考模式：¥20

Qwen3-14B

qwen3-14b

非思考模式：¥1

思考模式：¥1

非思考模式：¥4

思考模式：¥10

Qwen3-8B

qwen3-8b

非思考模式：¥0.5

思考模式：¥0.5

非思考模式：¥2

思考模式：¥5

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.5

¥2

Qwen3-4B-Instruct-2507

qwen3-4b-instruct-2507

非思考模式：¥0.3

思考模式：¥0.3

非思考模式：¥1.2

思考模式：¥3

Qwen2.5-开源版-72B

qwen2.5-72b-instruct

¥4

¥12

Qwen2.5-VL-72B

qwen2.5-vl-72b-instruct

¥16

¥48

Qwen2.5-开源版-32B

qwen2.5-32b-instruct

¥2

¥6

Qwen2.5-VL-32B

qwen2.5-vl-32b-instruct

¥8

¥24

Qwen2.5-开源版-14B

qwen2.5-14b-instruct

¥1

¥3

Qwen2.5-开源版-7B

qwen2.5-7b-instruct

¥0.5

¥1

Qwen2.5-VL-7B

qwen2.5-vl-7b-instruct

¥2

¥5

#### 新加坡

**基础模型**

**模型代码**

**输入**

**元/百万Token**

**输出**

**元/百万Token**

Qwen3.6-27B

qwen3.6-27b

<256K ¥4.497

<256K ¥26.979

Qwen3.5-27B

qwen3.5-27b

¥2.202

¥17.614

Qwen3-32B

qwen3-32b

非思考模式：¥1.174

思考模式：¥1.174

非思考模式：¥4.697

思考模式：¥4.697

Qwen3-14B

qwen3-14b

非思考模式：¥2.569

思考模式：¥2.569

非思考模式：¥10.275

思考模式：¥30.825

Qwen3-8B

qwen3-8b

非思考模式：¥1.321

思考模式：¥1.321

非思考模式：¥5.137

思考模式：¥15.412

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥1.321

¥5.137

Qwen3-4B-Instruct-2507

qwen3-4b-instruct-2507

非思考模式：¥0.807

思考模式：¥0.807

非思考模式：¥3.082

思考模式：¥9.247

Qwen2.5-开源版-72B

qwen2.5-72b-instruct

¥10.275

¥41.1

Qwen2.5-VL-72B

qwen2.5-vl-72b-instruct

¥20.55

¥61.65

Qwen2.5-开源版-32B

qwen2.5-32b-instruct

¥5.137

¥20.55

Qwen2.5-VL-32B

qwen2.5-vl-32b-instruct

¥10.275

¥30.825

Qwen2.5-开源版-14B

qwen2.5-14b-instruct

¥2.569

¥10.275

Qwen2.5-开源版-7B

qwen2.5-7b-instruct

¥1.284

¥5.137

Qwen2.5-VL-7B

qwen2.5-vl-7b-instruct

¥2.569

¥7.706

## LoRA 部署

Token 按量部署仅支持 LoRA 微调模型，API 创建时 `plan` 取值为 `lora`。`capacity` 参数设置无效但必须填写；如需扩缩容，请前往[百炼专属部署控制台](https://bailian.console.aliyun.com/model/deploy)填写表单申请。

通过 API 创建部署的完整示例见[API 部署指南](raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

## 扩容

按 Token 用量计费的部署，扩容需在控制台提交申请表单，等待人工审核，不支持自助扩缩容。

## 常见问题

一个月不使用会怎样？

按 Token 用量计费的部署，一个月内不使用将自动释放。

如何切换到其他计费方式？

只能下线原有资源，再通过需要的计费方式创建新资源。详见[模型部署简介](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。

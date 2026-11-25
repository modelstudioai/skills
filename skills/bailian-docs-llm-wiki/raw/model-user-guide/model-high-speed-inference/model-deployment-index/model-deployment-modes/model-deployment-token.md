# Token 按量部署

按模型 Token 使用量计费的部署方式，仅支持 LoRA 微调模型，不使用不计费，适用于调优后模型效果验证及对并发和延迟要求不高的低成本场景。

<a id="概述"></a>

<a id="token-overview-h2"></a>

## 概述

按 Token 用量计费（**不使用不计费**），仅支持部分经过 LoRA 高效微调的模型，适用于调优后模型效果验证及对并发和延迟要求不高的低成本场景。该模式下吞吐/并发和生成速度均由平台预置，用户不可调。

> **说明**
>
> 计费方式在服务创建后无法更改。如需切换，必须下线已部署模型后重新部署，详见[模型部署简介](../model-deployment-introduction.md)。

<a id="计费规则"></a>

<a id="token-billing-h2"></a>

## 计费规则

`费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）`

仅当对下列基础模型完成 SFT 高效训练（即 LoRA 高效微调，API 部署时 `plan` 取值为 `lora`）并得到自定义模型后，才支持按模型 Token 使用量计费。

<a id="支持模型与价格"></a>

<a id="token-models-price-h2"></a>

## 支持模型与价格

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

<table><thead><tr><th><p><strong>基础模型</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>输入</strong></p><p><strong>元/百万Token</strong></p></th><th><p><strong>输出</strong></p><p><strong>元/百万Token</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.5-27B</p></td><td><p>qwen3.5-27b</p></td><td><p>&lt;128K ¥0.6</p><p>128K-256K ¥1.8</p></td><td><p>&lt;128K ¥4.8</p><p>128K-256K ¥14.4</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-32B</p></td><td><p>qwen3-32b</p></td><td><p>非思考模式：¥2</p><p>思考模式：¥2</p></td><td><p>非思考模式：¥8</p><p>思考模式：¥20</p></td></tr><tr><td><p>Qwen3-14B</p></td><td><p>qwen3-14b</p></td><td><p>非思考模式：¥1</p><p>思考模式：¥1</p></td><td><p>非思考模式：¥4</p><p>思考模式：¥10</p></td></tr><tr><td><p>Qwen3-8B</p></td><td><p>qwen3-8b</p></td><td><p>非思考模式：¥0.5</p><p>思考模式：¥0.5</p></td><td><p>非思考模式：¥2</p><p>思考模式：¥5</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-VL-8B-Instruct</p></td><td><p>qwen3-vl-8b-instruct</p></td><td><p>¥0.5</p></td><td><p>¥2</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-4B-Instruct-2507</p></td><td><p>qwen3-4b-instruct-2507</p></td><td><p>非思考模式：¥0.3</p><p>思考模式：¥0.3</p></td><td><p>非思考模式：¥1.2</p><p>思考模式：¥3</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>¥4</p></td><td><p>¥12</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-72B</p></td><td><p>qwen2.5-vl-72b-instruct</p></td><td><p>¥16</p></td><td><p>¥48</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-32B</p></td><td><p>qwen2.5-32b-instruct</p></td><td><p>¥2</p></td><td><p>¥6</p></td></tr><tr><td><p>Qwen2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>¥1</p></td><td><p>¥3</p></td></tr><tr><td><p>Qwen2.5-开源版-7B</p></td><td><p>qwen2.5-7b-instruct</p></td><td><p>¥0.5</p></td><td><p>¥1</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-7B</p></td><td><p>qwen2.5-vl-7b-instruct</p></td><td><p>¥2</p></td><td><p>¥5</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>基础模型</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>输入</strong></p><p><strong>元/百万Token</strong></p></th><th><p><strong>输出</strong></p><p><strong>元/百万Token</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.5-27B</p></td><td><p>qwen3.5-27b</p></td><td><p>¥2.202</p></td><td><p>¥17.614</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-32B</p></td><td><p>qwen3-32b</p></td><td><p>非思考模式：¥1.174</p><p>思考模式：¥1.174</p></td><td><p>非思考模式：¥4.697</p><p>思考模式：¥4.697</p></td></tr><tr><td><p>Qwen3-14B</p></td><td><p>qwen3-14b</p></td><td><p>非思考模式：¥2.569</p><p>思考模式：¥2.569</p></td><td><p>非思考模式：¥10.275</p><p>思考模式：¥30.825</p></td></tr><tr><td><p>Qwen3-8B</p></td><td><p>qwen3-8b</p></td><td><p>非思考模式：¥1.321</p><p>思考模式：¥1.321</p></td><td><p>非思考模式：¥5.137</p><p>思考模式：¥15.412</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-VL-8B-Instruct</p></td><td><p>qwen3-vl-8b-instruct</p></td><td><p>¥1.321</p></td><td><p>¥5.137</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-4B-Instruct-2507</p></td><td><p>qwen3-4b-instruct-2507</p></td><td><p>非思考模式：¥0.807</p><p>思考模式：¥0.807</p></td><td><p>非思考模式：¥3.082</p><p>思考模式：¥9.247</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>¥10.275</p></td><td><p>¥41.1</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-72B</p></td><td><p>qwen2.5-vl-72b-instruct</p></td><td><p>¥20.55</p></td><td><p>¥61.65</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-32B</p></td><td><p>qwen2.5-32b-instruct</p></td><td><p>¥5.137</p></td><td><p>¥20.55</p></td></tr><tr><td><p>Qwen2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>¥2.569</p></td><td><p>¥10.275</p></td></tr><tr><td><p>Qwen2.5-开源版-7B</p></td><td><p>qwen2.5-7b-instruct</p></td><td><p>¥1.284</p></td><td><p>¥5.137</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-7B</p></td><td><p>qwen2.5-vl-7b-instruct</p></td><td><p>¥2.569</p></td><td><p>¥7.706</p></td></tr></tbody></table>

<a id="lora-部署"></a>

<a id="token-lora-deploy-h2"></a>

## LoRA 部署

Token 按量部署仅支持 LoRA 微调模型，API 创建时 `plan` 取值为 `lora`。`capacity` 参数设置无效但必须填写；如需扩缩容，请前往[百炼专属部署控制台](https://bailian.console.aliyun.com/model/deploy)填写表单申请。

通过 API 创建部署的完整示例见[API 部署指南](../model-deployment-quick-start.md)。

<a id="扩容"></a>

<a id="token-scale-h2"></a>

## 扩容

按 Token 用量计费的部署，扩容需在控制台提交申请表单，等待人工审核，不支持自助扩缩容。

<a id="常见问题"></a>

<a id="token-faq-h2"></a>

## 常见问题

<a id="accordion-一个月不使用会怎样"></a>

一个月不使用会怎样？

按 Token 用量计费的部署，一个月内不使用将自动释放。

<a id="accordion-如何切换到其他计费方式"></a>

如何切换到其他计费方式？

只能下线原有资源，再通过需要的计费方式创建新资源。详见[模型部署简介](../model-deployment-introduction.md)。

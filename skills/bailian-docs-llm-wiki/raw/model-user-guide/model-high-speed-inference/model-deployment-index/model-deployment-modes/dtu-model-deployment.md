# 独占吞吐（DTU）

独占算力部署提供独占吞吐（DTU）与模型单元（MU）两种方案，以独占 GPU 资源为指定模型提供性能和吞吐保障。DTU 面向新发布模型（按输入/输出 TPM×时长计费），MU 用于已有模型（按模型单元数量×时长计费）。本文介绍两种方案的功能、计费方式、使用流程与支持模型。

<a id="概述"></a>

<a id="dtu-overview-h2"></a>

## 概述

独占算力部署为指定模型提供独占 GPU 资源与性能保障，支持基础模型与自定义模型部署。百炼提供两种独占算力方案：

-   **DTU（Dedicated Throughput Unit，独占吞吐）**：按 Input/Output TPM 售卖，提供更直接的吞吐保障。全托管推理服务，底层独占 GPU 资源由平台运维。
-   **模型单元（MU，Model Unit）**：按使用时长与模型单元数量配置算力，资源独占。支持自定义性能指标、PD 分离计算模式。计费粒度为模型单元数量×时长。

DTU 与 MU 按模型适用区分：新发布模型采用 DTU（按输入/输出 TPM 计量），已有模型沿用 MU（按模型单元数量计量）。两者均提供独占算力、资源隔离与微调模型部署能力。新购部署时若模型支持 DTU 则优先选择 DTU。

两种方案共有的能力：

-   独占 GPU 资源，推理环境与其他用户物理隔离。
-   支持基础模型和自定义模型（百炼微调模型或用户上传模型）部署。
-   平台负责底层运维，无需管理 GPU。
-   不主动设 RPM/TPM 上限，流量受实际承载力限制。

通用模型部署流程详见[专属部署概述](../model-deployment-introduction.md)。

<a id="方案选型"></a>

<a id="dtu-selection-h2"></a>

## 方案选型

百炼为推理调用提供多种容量与计费方案。DTU 适用于需要独占部署、微调模型部署、低延迟高并发或数据隔离的场景。各方案的对比如下表所示。

Token 按量等计费方式的完整对比详见[模型部署](../model-deployment-introduction.md)主表。

| 对比维度 | DTU | 吞吐预留·高速模式 | Token 按量 | PAI/灵骏 |
| --- | --- | --- | --- | --- |
| 特点 | 独占算力 + 微调模型 | 吞吐保障 + 低延迟 | 弹性灵活、零门槛 | 自定义运行时 |
| 资源隔离 | 物理隔离 | 逻辑隔离 | 共享公池 | 物理隔离 |
| 微调模型 | 全参 + LoRA | 不支持 | LoRA | 支持 |
| 自定义框架 | 不支持 | 不支持 | 不支持 | 支持 |
| 计费模式 | TPM 额度 × 时长 | TPM 额度 × 时长 | Token 用量 | GPU × 时长 |

<a id="计费规则"></a>

<a id="dtu-billing-h2"></a>

## 计费规则

<a id="sec-tabs"></a>

<a id="dtu-计费"></a>

<a id="dtu-计费-h4"></a>

#### DTU 计费

DTU 按输入 TPM 和输出 TPM 分别计费，采用预付费（按月）模式。各模型有固定的输入/输出基准 TPM（见下表），**购买时需为基准 TPM 的整数倍**。输入和输出各至少购买基准 TPM（1 倍），生产环境建议各购买 2 倍以上。

费用由后端根据模型、输入/输出 TPM、服务区域和购买时长计算。各模型的价格如下表所示，起售和扩容价格均为输入输出各 1 倍基准 TPM 的总价，微调模型的价格与对应基础模型相同，具体以控制台实际展示为准。

<a id="mu-计费"></a>

<a id="mu-计费-h4"></a>

#### MU 计费

`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`

"模型单元单价"在后付费场景下取下表"小时单价"列；预付费按月计费时，公式改为 **包月数 × 模型单元数量 × 月单价**。

-   预付费购买的首月，如在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费（不满一天按一天计费）

> **说明**
>
> 模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。

> MU 与 DTU 均为预付费模式，提前退订已使用部分按 1.2 倍系数结算退费，详见[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

<a id="支持模型与价格"></a>

<a id="dtu-pricing-h2"></a>

## 支持模型与价格

<a id="sec-tabs-2"></a>

<a id="dtu-价格表与性能基准"></a>

<a id="dtu-价格表与性能基准-h4"></a>

#### DTU 价格表与性能基准

<a id="sec-tabs-3"></a>

<a id="华北-北京2"></a>

<a id="华北-北京2-h4"></a>

#### 华北-北京2

<table><thead><tr><th><p><strong>模型</strong></p></th><th><p><strong>规格</strong></p></th><th><p><strong>基准输入（TPM）</strong></p></th><th><p><strong>基准输出（TPM）</strong></p></th><th><p><strong>起售价格(元/月)</strong></p></th><th><p><strong>扩容价格(元/月)</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.8-27b</p></td><td><p>Efficient</p></td><td><p>268,000</p></td><td><p>33,000</p></td><td><p>49,208</p></td><td><p>49,208</p></td></tr><tr><td><p>Fast</p></td><td><p>1,172,000</p></td><td><p>146,000</p></td><td><p>278,460</p></td><td><p>278,460</p></td></tr><tr><td rowspan="2"><p>qwen3.8-flash</p></td><td><p>Efficient</p></td><td><p>580,000</p></td><td><p>72,000</p></td><td><p>196,228</p></td><td><p>196,228</p></td></tr><tr><td><p>Custom</p></td><td><p>1,272,000</p></td><td><p>152,000</p></td><td><p>635,680</p></td><td><p>635,680</p></td></tr><tr><td rowspan="4"><p>qwen3.7-plus-2026-05-26</p></td><td><p>Fast</p></td><td><p>1,372,000</p></td><td><p>170,000</p></td><td><p>556,466</p></td><td><p>556,466</p></td></tr><tr><td><p>Fast</p></td><td><p>1,192,000</p></td><td><p>148,000</p></td><td><p>555,680</p></td><td><p>555,680</p></td></tr><tr><td><p>Fast</p></td><td><p>704,000</p></td><td><p>132,000</p></td><td><p>556,072</p></td><td><p>556,072</p></td></tr><tr><td><p>Fast</p></td><td><p>660,000</p></td><td><p>124,000</p></td><td><p>555,744</p></td><td><p>555,744</p></td></tr><tr><td><p>qwen3.7-plus-2026-07-09</p></td><td><p>Fast</p></td><td><p>1,270,000</p></td><td><p>158,000</p></td><td><p>277,470</p></td><td><p>277,470</p></td></tr><tr><td rowspan="2"><p>qwen3.6-27b</p></td><td><p>Standard</p></td><td><p>273,000</p></td><td><p>34,000</p></td><td><p>49,118</p></td><td><p>49,118</p></td></tr><tr><td><p>Fast</p></td><td><p>1,818,000</p></td><td><p>277,000</p></td><td><p>370,749</p></td><td><p>370,749</p></td></tr><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>Standard</p></td><td><p>896,000</p></td><td><p>112,000</p></td><td><p>1,107,904</p></td><td><p>1,107,904</p></td></tr><tr><td><p>Fast</p></td><td><p>1,496,000</p></td><td><p>186,000</p></td><td><p>741,520</p></td><td><p>741,520</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>Fast</p></td><td><p>7,288,000</p></td><td><p>904,000</p></td><td><p>2,226,984</p></td><td><p>2,226,984</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td><p>Standard</p></td><td><p>656,000</p></td><td><p>82,000</p></td><td><p>109,962</p></td><td><p>109,962</p></td></tr><tr><td><p>Efficient</p></td><td><p>595,000</p></td><td><p>74,000</p></td><td><p>48,963</p></td><td><p>48,963</p></td></tr><tr><td rowspan="3"><p>qwen3.5-27b</p></td><td><p>Standard</p></td><td><p>2,432,000</p></td><td><p>304,000</p></td><td><p>1,108,688</p></td><td><p>1,108,688</p></td></tr><tr><td><p>Efficient</p></td><td><p>291,000</p></td><td><p>36,000</p></td><td><p>48,996</p></td><td><p>48,996</p></td></tr><tr><td><p>Fast</p></td><td><p>1,515,000</p></td><td><p>189,000</p></td><td><p>278,295</p></td><td><p>278,295</p></td></tr><tr><td><p>qwen3.5-4b</p></td><td><p>Standard</p></td><td><p>1,072,000</p></td><td><p>134,000</p></td><td><p>109,478</p></td><td><p>109,478</p></td></tr><tr><td><p>glm-5.3</p></td><td><p>Fast</p></td><td><p>1,004,000</p></td><td><p>120,000</p></td><td><p>1,895,260</p></td><td><p>1,895,260</p></td></tr><tr><td><p>glm-5.3-flash</p></td><td><p>Fast</p></td><td><p>769,000</p></td><td><p>96,000</p></td><td><p>278,197</p></td><td><p>278,197</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>V2</p></td><td><p>502,000</p></td><td><p>60,000</p></td><td><p>947,630</p></td><td><p>947,630</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>Standard</p></td><td><p>256,000</p></td><td><p>32,000</p></td><td><p>504,704</p></td><td><p>504,704</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>Fast</p></td><td><p>2,312,000</p></td><td><p>288,000</p></td><td><p>555,360</p></td><td><p>555,360</p></td></tr><tr><td rowspan="2"><p>deepseek-v4-flash</p></td><td><p>Standard</p></td><td><p>2,240,000</p></td><td><p>280,000</p></td><td><p>1,107,400</p></td><td><p>1,107,400</p></td></tr><tr><td><p>Fast</p></td><td><p>1,807,000</p></td><td><p>225,000</p></td><td><p>278,189</p></td><td><p>278,189</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>Fast</p></td><td><p>1,676,000</p></td><td><p>213,000</p></td><td><p>277,984</p></td><td><p>277,984</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>Fast</p></td><td><p>1,536,000</p></td><td><p>192,000</p></td><td><p>2,223,744</p></td><td><p>2,223,744</p></td></tr></tbody></table>

各模型在标准工况下的性能参考数据如下表所示，以控制台实际展示为准。

> 以下性能参考数据均在缓存命中率为 0% 的条件下测得。实际使用中，随着缓存命中率提升，模型性能也会相应提高。

<table><thead><tr><th><p><strong>模型</strong></p></th><th><p><strong>规格</strong></p></th><th><p><strong>输入长度</strong></p></th><th><p><strong>输出长度</strong></p></th><th><p><strong>缓存命中率</strong></p></th><th><p><strong>首字延迟(ms)</strong></p></th><th><p><strong>每token延迟(ms)</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.8-27b</p></td><td><p>Efficient</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,249</p></td><td><p>26</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,207</p></td><td><p>15</p></td></tr><tr><td rowspan="2"><p>qwen3.8-flash</p></td><td><p>Efficient</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,296</p></td><td><p>19</p></td></tr><tr><td><p>Custom</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>3,659</p></td><td><p>19</p></td></tr><tr><td rowspan="4"><p>qwen3.7-plus-2026-05-26</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,418</p></td><td><p>15</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>888</p></td><td><p>10</p></td></tr><tr><td><p>Fast</p></td><td><p>2,600</p></td><td><p>500</p></td><td><p>0</p></td><td><p>970</p></td><td><p>13</p></td></tr><tr><td><p>Fast</p></td><td><p>2,600</p></td><td><p>500</p></td><td><p>0</p></td><td><p>819</p></td><td><p>14</p></td></tr><tr><td><p>qwen3.7-plus-2026-07-09</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,402</p></td><td><p>12</p></td></tr><tr><td rowspan="2"><p>qwen3.6-27b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,292</p></td><td><p>19</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,106</p></td><td><p>14</p></td></tr><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>996</p></td><td><p>27</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,465</p></td><td><p>18</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>568</p></td><td><p>8</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>471</p></td><td><p>10</p></td></tr><tr><td><p>Efficient</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,822</p></td><td><p>12</p></td></tr><tr><td rowspan="3"><p>qwen3.5-27b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>703</p></td><td><p>14</p></td></tr><tr><td><p>Efficient</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,448</p></td><td><p>23</p></td></tr><tr><td><p>Fast</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,121</p></td><td><p>13</p></td></tr><tr><td><p>qwen3.5-4b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>552</p></td><td><p>6</p></td></tr><tr><td><p>glm-5.3</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,558</p></td><td><p>15</p></td></tr><tr><td><p>glm-5.3-flash</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,271</p></td><td><p>12</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>V2</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,558</p></td><td><p>15</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>769</p></td><td><p>27</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,824</p></td><td><p>14</p></td></tr><tr><td rowspan="2"><p>deepseek-v4-flash</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>651</p></td><td><p>19</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,408</p></td><td><p>12</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,079</p></td><td><p>13</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,607</p></td><td><p>14</p></td></tr></tbody></table>

<a id="mu-价格表"></a>

<a id="mu-价格表-h4"></a>

#### MU 价格表

<a id="sec-tabs-4"></a>

<a id="文本生成"></a>

<a id="文本生成-h4"></a>

#### 文本生成

<a id="sec-tabs-5"></a>

<a id="千问"></a>

<a id="千问-h4"></a>

#### 千问

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td><p>千问3.8-27B</p></td><td><p>qwen3.8-27b</p></td><td><p>MU9 x 4</p></td><td><p>¥204</p></td><td><p>¥98,400</p></td></tr><tr><td colspan="5"></td></tr><tr><td rowspan="2"><p>千问3.7-Plus-2026-05-26</p></td><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td colspan="5"></td></tr><tr><td rowspan="5"><p>千问3.6-35B-A3B</p></td><td rowspan="5"><p>qwen3.6-35b-a3b</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU8 x 1</p></td><td><p>¥47</p></td><td><p>¥22,400</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td><p>千问3.6-27B</p></td><td><p>qwen3.6-27b</p></td><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="2"><p>千问3.6-Flash-2026-04-16</p></td><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td rowspan="2"><p>千问3.6-Plus-2026-04-02</p></td><td rowspan="2"><p>qwen3.6-plus-2026-04-02</p></td><td><p>MU1 x 8</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥432</p><p>PD分离模式：¥864</p></td><td><p>¥208,944</p><p>PD分离模式：¥417,888</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td colspan="5"></td></tr><tr><td rowspan="2"><p>千问3.5-397B-A17B</p></td><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>MU3 x 8</p><p>MU3 x 16（PD分离模式）</p></td><td><p>¥1,096</p><p>PD分离模式：¥2,192</p></td><td><p>¥527,752</p><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td rowspan="2"><p>千问3.5-122B-A10B</p></td><td rowspan="2"><p>qwen3.5-122b-a10b</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td rowspan="4"><p>千问3.5-35B-A3B</p></td><td rowspan="4"><p>qwen3.5-35b-a3b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="4"><p>千问3.5-27B</p></td><td rowspan="4"><p>qwen3.5-27b</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU8 x 1</p></td><td><p>¥47</p></td><td><p>¥22,400</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="2"><p>千问3.5-9B</p></td><td rowspan="2"><p>qwen3.5-9b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>千问3.5-Flash-2026-02-23</p></td><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="3"><p>千问3.5-Plus-2026-02-15</p></td><td rowspan="3"><p>qwen3.5-plus-2026-02-15</p></td><td><p>MU1 x 8</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥432</p><p>PD分离模式：¥864</p></td><td><p>¥208,944</p><p>PD分离模式：¥417,888</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p><p>MU3 x 16（PD分离模式）</p></td><td><p>¥1,096</p><p>PD分离模式：¥2,192</p></td><td><p>¥527,752</p><p>PD分离模式：¥1,055,504</p></td></tr><tr><td colspan="5"></td></tr><tr><td rowspan="3"><p>千问3-235B-A22B-Instruct-2507</p></td><td rowspan="3"><p>qwen3-235b-a22b-instruct-2507</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>千问3-32B</p></td><td><p>qwen3-32b</p></td><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td><p>千问3-30B-A3B-Thinking-2507</p></td><td><p>qwen3-30b-a3b-thinking-2507</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="2"><p>千问3-4B</p></td><td rowspan="2"><p>qwen3-4b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td rowspan="2"><p>千问3-Embedding-0.6B</p></td><td rowspan="2"><p>qwen3-embedding-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>MU6 x 1</p></td><td><p>¥25</p></td><td><p>¥12,089</p></td></tr><tr><td><p>千问3-MoE-Rerank-0.6B</p></td><td><p>qwen3-moe-rerank-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td rowspan="2"><p>千问3-Rerank-0.6B</p></td><td rowspan="2"><p>qwen3-rerank-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>MU6 x 1</p></td><td><p>¥25</p></td><td><p>¥12,089</p></td></tr><tr><td rowspan="2"><p>千问3-Max-2025-09-23</p></td><td rowspan="2"><p>qwen3-max-2025-09-23</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>千问3-Rerank</p></td><td><p>qwen3-rerank</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td colspan="5"></td></tr><tr><td><p>千问2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>千问2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="2"><p>千问2.5-开源版-7B</p></td><td rowspan="2"><p>qwen2.5-7b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td colspan="5"></td></tr><tr><td><p>千问-Plus-2025-07-28</p></td><td><p>qwen-plus-2025-07-28</p></td><td><p>MU1 x 4</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥216</p><p>PD分离模式：¥864</p></td><td><p>¥104,472</p><p>PD分离模式：¥417,888</p></td></tr><tr><td><p>千问-Plus-2025-12-01</p></td><td><p>qwen-plus-2025-12-01</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>Qwen-Plus-Character-2025-11-06</p></td><td><p>qwen-plus-character-2025-11-06</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr></tbody></table>

<a id="glm"></a>

<a id="glm-h4"></a>

#### GLM

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>GLM-5.1</p></td><td rowspan="3"><p>glm-5.1</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td><p>GLM-5</p></td><td><p>glm-5</p></td><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>GLM-4.7</p></td><td><p>glm-4.7</p></td><td><p>MU6 x 32（PD分离模式）</p></td><td><p>PD分离模式：¥800</p></td><td><p>PD分离模式：¥386,848</p></td></tr></tbody></table>

<a id="deepseek"></a>

<a id="deepseek-h4"></a>

#### DeepSeek

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>DeepSeek-v4-Flash</p></td><td rowspan="2"><p>deepseek-v4-flash</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>DeepSeek-v3.2</p></td><td><p>deepseek-v3.2</p></td><td><p>MU2 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥1,008</p></td><td><p>PD分离模式：¥480,576</p></td></tr></tbody></table>

<a id="更多模型"></a>

<a id="更多模型-h4"></a>

#### 更多模型

| 模型名称 | 模型代码 | 模型单元规格 | **小时单价（元）**<br><br>**最小计费：分钟** | **包月单价（元）**<br><br>**最小计费：天** |
| --- | --- | --- | --- | --- |
| Kimi-K2.5 | kimi-k2.5 | MU2 x 8 | ¥504 | ¥240,288 |

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
-   Thinking - 模型部署后以思考模式进行推理。

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。**
    
    该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。
    

<a id="多模态"></a>

<a id="多模态-h4"></a>

#### 多模态

<a id="sec-tabs-6"></a>

<a id="千问vl"></a>

<a id="千问vl-h4"></a>

#### 千问VL

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>千问3-VL-235B-A22B-Thinking</p></td><td rowspan="3"><p>qwen3-vl-235b-a22b-thinking</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td rowspan="2"><p>千问3-VL-32B-Instruct</p></td><td rowspan="2"><p>qwen3-vl-32b-instruct</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td rowspan="2"><p>千问3-VL-8B-Instruct</p></td><td rowspan="2"><p>qwen3-vl-8b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>千问3-VL-4B-Instruct</p></td><td><p>qwen3-vl-4b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>千问3-VL-2B-Instruct</p></td><td><p>qwen3-vl-2b-instruct</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>千问3-VL-Embedding-2B</p></td><td><p>qwen3-vl-embedding-2b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>千问3-VL-Flash-2025-10-15</p></td><td><p>qwen3-vl-flash-2025-10-15</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>千问3-VL-Plus-2025-09-23</p></td><td><p>qwen3-vl-plus-2025-09-23</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td colspan="5"></td></tr><tr><td><p>千问VL-Max-2025-08-13</p></td><td><p>qwen-vl-max-2025-08-13</p></td><td><p>MU6 x 4</p></td><td><p>¥100</p></td><td><p>¥48,356</p></td></tr></tbody></table>

<a id="千问-omni"></a>

<a id="千问-omni-h4"></a>

#### 千问 Omni

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>千问3.5-Omni-Flash</p></td><td rowspan="2"><p>qwen3.5-omni-flash</p></td><td><p>MU8 x 1</p></td><td><p>¥47</p></td><td><p>¥22,400</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr></tbody></table>

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
-   Thinking - 模型部署后以思考模式进行推理。
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。

<a id="语音合成"></a>

<a id="语音合成-h4"></a>

#### 语音合成

**CosyVoice**

| 模型名称 | 模型代码 | 模型单元规格 | 小时单价（元） | 包月单价（元） |
| --- | --- | --- | --- | --- |
| cosyvoice-v3-flash | cosyvoice-v3-flash | MU5 | ¥21 | ¥10,139 |

<a id="部署创建"></a>

<a id="dtu-create-h2"></a>

## 部署创建

<a id="sec-tabs-7"></a>

<a id="dtu-创建部署"></a>

<a id="dtu-创建部署-h4"></a>

#### DTU 创建部署

使用 DTU 前需在控制台开通 DTU 功能并申请资源额度。开通后在百炼控制台**专属部署**页面选择目标模型，计费方式选择 DTU 即可创建部署。

> **警告**
>
> DTU 部署支持通过 API 创建部署、查询详情与列表、扩缩容、修改限流与更新模型（以
>
> `plan="dtu"` 区分部署形式），详见[模型部署 API 参考](../../../../model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。续费与自动续费变更、停止/启动与删除请在百炼控制台操作；开通 DTU 功能与资源额度申请亦需在控制台完成。

通用模型部署的基础流程详见[专属部署概述](../model-deployment-introduction.md)。

创建部署的表单字段如下表所示。

| 参数 | 说明 | 是否必填 | 取值说明 |
| --- | --- | --- | --- |
| 服务名称 | 部署服务的名称 | 是 | 自定义 |
| 模型 | 部署的目标模型 | 是 | 下拉选择 |
| 部署模版 | 部署架构 | 否 | 下拉选择，默认选第一个 |
| 付费类型 | 计费方式 | 是 | 预付费（按月） |
| 输入吞吐额度 | 购买的输入 TPM 容量 | 是 | 基准输入 TPM 的整数倍（kTPM） |
| 输出吞吐额度 | 购买的输出 TPM 容量 | 是 | 基准输出 TPM 的整数倍（kTPM） |
| 购买时长 | 购买周期 | 是 | 1-12（整数，月） |
| 自动续费 | 到期自动续费 | 否 | 开/关 |
| 单次续费时长 | 开启自动续费时必填 | 是 | 1-12（整数，月） |

<a id="mu-部署配置"></a>

<a id="mu-部署配置-h4"></a>

#### MU 部署配置

<table><thead><tr><th><p><strong>配置内容</strong></p></th><th><p><strong>配置详情</strong></p></th></tr></thead><tbody><tr><td><p>服务名称</p></td><td><p>自定义部署服务的名称。</p></td></tr><tr><td><p>选择模型</p></td><td><p>选择要部署的模型，包括平台预置模型和已调优的模型。</p></td></tr><tr><td><p>模型单元类型</p></td><td><p>选择部署规格，不同规格对应不同的算力和性能。</p></td></tr><tr><td><p>部署副本数</p></td><td><p>设置初始部署副本数量，影响服务的并发处理能力。</p></td></tr><tr><td><p>部署模版</p></td><td><p>选择部署模版（如&quot;单机部署&quot;），不同模版对应不同的资源配置方案。仅在模型单元计费模式下可用。</p></td></tr><tr><td><p>配置模型推理模式</p></td><td><p>部分模型在以<strong>模型单元</strong>方式部署时，可配置推理模式、最长上下文等。</p><ul><li><p>Instruct - 模型部署后以<strong>非思考模式</strong>进行推理。</p></li><li><p>Thinking - 模型部署后以思考模式进行推理。</p></li></ul></td></tr><tr><td><p>最长上下文</p></td><td><p>部分模型的<strong>模型单元</strong>部署模式支持该设置。最长上下文长度基于模型类型。</p></td></tr><tr><td><p>服务限流</p></td><td><p>部分模型的<strong>模型单元</strong>部署模式支持该设置，可限制模型调用的 RPM、TPM。</p></td></tr></tbody></table>

<a id="容量规划"></a>

<a id="dtu-benchmark-h2"></a>

## 容量规划

DTU 按输入/输出 TPM 售卖，所购 TPM 即每分钟可处理的最大 token 量。容量规划的目标是：依据业务峰值 token 需求推算需购买的倍数，再通过压测验证实际可承载的并发与延迟是否达标。各模型的基准输入/输出 TPM 与标准工况性能参考见上方表格。

建议使用 evalscope 等压测工具，按真实业务场景（输入/输出长度、并发数、延迟要求）压测，再对照定价表确定购买倍数。

<a id="容量规划方法"></a>

<a id="dtu-bm-h3-plan"></a>

### 容量规划方法

1.  梳理业务峰值指标：典型请求的输入/输出 token 长度、目标并发数，以及对首字延迟（TTFT）和每 token 生成延迟（TPOT）的要求。
2.  估算峰值吞吐需求：峰值输入 TPM ≈ 并发数 × 单请求输入长度 ÷ 单请求处理时长（分钟）；峰值输出 TPM ≈ 并发数 × 单请求输出长度 ÷ 单请求生成时长（分钟）。
3.  计算购买倍数：输入倍数 = ⌈峰值输入 TPM ÷ 基准输入 TPM⌉，输出倍数 = ⌈峰值输出 TPM ÷ 基准输出 TPM⌉；DTU 输入与输出需同增同减，取两者较大值作为最终倍数。
4.  压测验证：按计算倍数购买后，用 evalscope 在目标工况下复测，确认实际吞吐与延迟满足业务要求。若延迟偏高，可在 TPM 余量内提高并发以提升有效吞吐。

如对延迟要求不严格，可在不超过所购 TPM 上限的前提下，通过提高并发数提升实际吞吐量。

业务测算示例：

某模型基准输入 656K TPM、基准输出 82K TPM。经业务峰值梳理，峰值输入约 1,300K TPM、峰值输出约 160K TPM。计算倍数：输入 ⌈1300÷656⌉=2、输出 ⌈160÷82⌉=2，取较大值 2 倍，购买输入 1,312K TPM（656K×2）+ 输出 164K TPM（82K×2）；随后用 evalscope 在峰值工况压测，确认延迟达标。若业务量翻倍，峰值输入约 2,600K、输出约 320K，则输入 ⌈2600÷656⌉=4、输出 ⌈320÷82⌉=4，需购买 4 倍：输入 2,624K TPM（656K×4）+ 输出 328K TPM（82K×4），并复测。

测算公式：

<a id="code-block"></a>

```text
购买倍数 = max(⌈峰值输入 TPM ÷ 基准输入 TPM⌉, ⌈峰值输出 TPM ÷ 基准输出 TPM⌉)
```

<a id="扩缩容与续费退订"></a>

<a id="dtu-manage-h2"></a>

## 扩缩容与续费退订

<a id="sec-tabs-8"></a>

<a id="dtu-扩缩容与续费退订"></a>

<a id="dtu-扩缩容与续费退订-h4"></a>

#### DTU 扩缩容与续费退订

部署列表展示已购买的输入/输出 TPM 额度，详情页展示 TPM 容量详情。

扩缩容：在部署列表中点击“扩缩容”修改输入/输出 TPM 容量。扩容显示需补交金额，缩容显示预计退款金额。输入和输出需同增或同减，不能一增一减。也可通过 API 扩缩容，详见[模型部署 API 参考](../../../../model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。仅运行中的部署可操作。

续费：预付费包月到期可续费，详情页续费按钮进入续费流程，支持自动续费开关与单次续费时长。

退订：预付费包月支持提前退订，已使用部分按 1.2 倍系数结算退费，详见[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。退订不可恢复，退订后独占资源释放、服务停止。

<a id="mu-扩缩容与续费"></a>

<a id="mu-扩缩容与续费-h4"></a>

#### MU 扩缩容与续费

-   模型单元（按时长）：点击**扩缩容**按钮，自助、手动调节实例数量（副本数）。还可通过操作列的伸缩配置按钮，配置自动伸缩策略（包括伸缩阈值、最小/最大副本数、定时伸缩等）。
-   续费：预付费包月服务可续费延长服务时间，支持自动续费。
-   退订：预付费购买的首月内提前退订，日单价按 1.2 倍计费；详见[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

<a id="常见问题"></a>

<a id="dtu-faq-h2"></a>

## 常见问题

**DTU 部署和 Token 按量计费有什么区别？**

Token 按量计费在共享资源池上按 token 用量计费；DTU 为独占 GPU 资源，按输入/输出 TPM 计费，适合需要稳定吞吐和独占部署的场景。

**DTU 部署支持哪些计费方式？**

仅支持预付费（按月）计费。

**如何查看已购 TPM 的使用情况？**

在百炼控制台**专属部署**的部署列表和详情页可查看已购的输入/输出 TPM 额度，详见[专属部署概述](../model-deployment-introduction.md)。

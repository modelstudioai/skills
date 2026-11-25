# 模型训练与部署计费

本文介绍阿里云百炼平台的模型训练、模型部署的计费规则及价格。

<a id="模型训练计费"></a>

<a id="dfb9c9f52ca14"></a>

## 模型训练计费

<a id="文本生成模型-千问"></a>

<a id="3bde90c8975kk"></a>

### 文本生成模型-千问

> **说明**
>
> 模型训练流程请参见[模型调优](../model-training/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。训练完成后的新模型需先完成**模型部署**，才能评测和调用。

<table><tbody><tr><td><strong>计费方式</strong></td><td><p>按训练Token计费</p></td></tr><tr><td><strong>计费公式</strong></td><td><p>模型训练费用 = （训练数据 Token 总数 + 混合训练数据 Token 总数）× 循环次数 × 训练单价（最小计费单位：1 token）</p><blockquote><p>您可以查看<a href="https://bailian.console.aliyun.com/model/tuning/create">模型训练控制台</a>底部的预估训练费用，并单击<strong>计费详情</strong>，查看训练 Token 总数、循环次数和训练单价。</p></blockquote></td></tr></tbody></table>

<a id="sec-tabs"></a>

<a id="千问vl"></a>

<a id="千问vl-h4"></a>

#### 千问VL

<table><thead><tr><th><p><strong>模型服务</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>价格</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3-VL-8B-Instruct</p></td><td><p>qwen3-vl-8b-instruct</p></td><td><p>¥0.012/千Token</p></td></tr><tr><td><p>Qwen3-VL-8B-Thinking</p></td><td><p>qwen3-vl-8b-thinking</p></td><td><p>¥0.012/千Token</p></td></tr><tr><td><p>Qwen3-VL-4B-Instruct</p></td><td><p>qwen3-vl-4b-instruct</p></td><td><p>¥0.006/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>Qwen2.5-VL-72B-Instruct</p></td><td><p>qwen2.5-vl-72b-instruct</p></td><td><p>¥0.05/千Token</p></td></tr><tr><td><p>Qwen2.5-VL-32B-Instruct</p></td><td><p>qwen2.5-vl-32b-instruct</p></td><td><p>¥0.02/千Token</p></td></tr><tr><td><p>Qwen2.5-VL-7B-Instruct</p></td><td><p>qwen2.5-vl-7b-instruct</p></td><td><p>¥0.01/千Token</p></td></tr></tbody></table>

<a id="千问"></a>

<a id="千问-h4"></a>

#### 千问

<table><thead><tr><th><p><strong>模型服务</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>价格</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.8-27B</p></td><td><p>qwen3.8-27b</p></td><td><p>¥0.05/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>Qwen3.7-Plus-2026-05-26</p></td><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>¥0.35/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>Qwen3.6-27B</p></td><td><p>qwen3.6-27b</p></td><td><p>¥0.05/千Token</p></td></tr><tr><td><p>Qwen3.6-Flash-2026-04-16</p></td><td><p>qwen3.6-flash-2026-04-16</p></td><td><p>¥0.05/千Token</p></td></tr><tr><td><p>Qwen3.6-Plus-2026-04-02</p></td><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>¥0.3/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>Qwen3.5-27B</p></td><td><p>qwen3.5-27b</p></td><td><p>¥0.05/千Token</p></td></tr><tr><td><p>Qwen3.5-9B</p></td><td><p>qwen3.5-9b</p></td><td><p>¥0.02/千Token</p></td></tr><tr><td><p>Qwen3.5-4B</p></td><td><p>qwen3.5-4b</p></td><td><p>¥0.015/千Token</p></td></tr><tr><td><p>Qwen3.5-Flash-2026-02-23</p></td><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>¥0.05/千Token</p></td></tr><tr><td><p>Qwen3.5-Plus-2026-02-15</p></td><td><p>qwen3.5-plus-2026-02-15</p></td><td><p>¥0.3/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>Qwen3-32B</p></td><td><p>qwen3-32b</p></td><td><p>¥0.04/千Token</p></td></tr><tr><td><p>Qwen3-30B-A3B-Instruct-2507</p></td><td><p>qwen3-30b-a3b-instruct-2507</p></td><td><p>¥0.03/千Token</p></td></tr><tr><td><p>Qwen3-14B</p></td><td><p>qwen3-14b</p></td><td><p>¥0.03/千Token</p></td></tr><tr><td><p>Qwen3-8B</p></td><td><p>qwen3-8b</p></td><td><p>¥0.006/千Token</p></td></tr><tr><td><p>Qwen3-4B-Instruct-2507</p></td><td><p>qwen3-4b-instruct-2507</p></td><td><p>¥0.006/千Token</p></td></tr><tr><td><p>Qwen3-1.7B</p></td><td><p>qwen3-1.7b</p></td><td><p>¥0.0045/千Token</p></td></tr><tr><td><p>Qwen3-0.6B</p></td><td><p>qwen3-0.6b</p></td><td><p>¥0.003/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>Qwen2.5-72B-Instruct</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>¥0.15/千Token</p></td></tr><tr><td><p>Qwen2.5-32B-Instruct</p></td><td><p>qwen2.5-32b-instruct</p></td><td><p>¥0.03/千Token</p></td></tr><tr><td><p>Qwen2.5-14B-Instruct</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>¥0.03/千Token</p></td></tr><tr><td><p>Qwen2.5-7B-Instruct</p></td><td><p>qwen2.5-7b-instruct</p></td><td><p>¥0.006/千Token</p></td></tr><tr><td colspan="3"></td></tr><tr><td><p>千问-Plus-Character-2025-11-06</p></td><td><p>qwen-plus-character-2025-11-06</p></td><td><p>¥0.15/千Token</p></td></tr></tbody></table>

<a id="图像生成模型-万相"></a>

<a id="img_train_billing_h3"></a>

### 图像生成模型-万相

> **说明**
>
> 模型训练流程请参见[图像生成模型调优](../model-training/fine-tuning/wan-image-generation-finetune-guide.md)。训练完成后的新模型需先完成**模型部署**，才能调用。

|  |  |
| --- | --- |
| **计费方式** | 按训练Token计费 |
| **计费公式** | 模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token） |

<a id="accordion-训练token总量的计算公式"></a>

训练Token总量的计算公式

‘训练Token总量≈max\_steps×Lstep‘\`训练 Token 总量 \\approx max\\\_steps \\times L\_{step}\`‘训练Token总量≈max\_steps×Lstep​‘

其中：

-   max\_steps：训练时指定的超参数，表示最大训练步数（创建微调任务时配置）。
    
-   Lstep：每步的Token消耗量，计算公式为：
    
    ‘Lstep\=∑i∈batchLitem(i)≤Lmax‘\`L\_{step} = \\sum\_{i \\in batch} L\_{item}^{(i)} \\leq L\_{max}\`‘Lstep​\=i∈batch∑​Litem(i)​≤Lmax​‘
    
    Lstep 近似等于 Lmax。Lmax 由 max\_token\_length 和 generation\_type 共同决定，具体取值如下表：
    

<table><thead><tr><th><p><strong>generation_type</strong></p></th><th><p><strong>max_token_length</strong></p></th><th><p><strong>L</strong><strong>max</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>t2i（文生图）</p></td><td><p>1k</p></td><td><p>12,800</p></td></tr><tr><td><p>2k</p></td><td><p>23,220</p></td></tr><tr><td rowspan="2"><p>i2i（图生图）</p></td><td><p>1k</p></td><td><p>23,220</p></td></tr><tr><td><p>2k</p></td><td><p>32,000</p></td></tr></tbody></table>

| 模型服务 | 模型名称 | 训练价格（每千Token） |
| --- | --- | --- |
| 万相-图像生成 | wan2.7-image-pro | 0.08元 |
| 万相-图像生成 | wan2.7-image | 0.08元 |

<a id="accordion-计费示例"></a>

计费示例

假设使用 wan2.7-image-pro 模型进行 t2i 微调，max\_steps = 200，max\_token\_length = "1k"，训练单价 = 0.08元/千Token：

-   查表得 Lmax = 12,800（generation\_type=t2i，max\_token\_length=1k），Lstep ≈ Lmax = 12,800
-   训练Token总量 ≈ 200 × 12800 = 2560000 = 2560千Token
-   模型训练费用 ≈ 2560 × 0.08 = 204.8元

<a id="图像生成模型-千问"></a>

<a id="qwen_img_train_billing_h3"></a>

### 图像生成模型-千问

> **说明**
>
> 模型训练流程请参见[图像生成模型调优](../model-training/fine-tuning/wan-image-generation-finetune-guide.md)。训练完成后的新模型需先完成**模型部署**，才能调用。

|  |  |
| --- | --- |
| **计费方式** | 按训练Token计费 |
| **计费公式** | 模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token） |

<a id="accordion-训练token总量的计算公式-2"></a>

训练Token总量的计算公式

‘训练Token总量\=n\_epochs×N×(max\_pixels/压缩率)×GPU系数‘\`\\text{训练Token总量} = n\\\_epochs \\times N \\times (max\\\_pixels / \\text{压缩率}) \\times \\text{GPU系数}\`‘训练Token总量\=n\_epochs×N×(max\_pixels/压缩率)×GPU系数‘

其中：

-   n\_epochs：训练时指定的超参数，表示训练轮数（创建微调任务时配置）。
-   N：训练集中的图片总数。
-   max\_pixels：训练时指定的超参数，表示图片的最大像素数（创建微调任务时配置）。取值为 `1k`（即 1024×1024）或 `2k`（即 2048×2048）。
-   压缩率：VAE 固定压缩比例，值为 1024（即 32×32）。
-   GPU系数：资源调度系数，根据任务调度情况动态调整。

| 模型服务 | 模型名称 | 训练价格（每千Token） |
| --- | --- | --- |
| 千问-图像生成 | qwen-image-2.0 | 0.02元 |
| 千问-图像生成 | qwen-image-2.0-pro | 0.02元 |

<a id="accordion-计费示例-2"></a>

计费示例

假设使用 qwen-image-2.0 模型微调，训练集包含 1 张图片，n\_epochs = 1000，max\_pixels = "1k"，训练单价 = 0.02元/千Token，GPU系数按 8 计算：

-   单张图片的Token量 = max\_pixels / 压缩率 = 1024×1024 / 1024 = 1024
-   训练Token总量 = 1000 × 1 × 1024 × 8 = 8192000 = 8192千Token
-   模型训练费用 = 8192 × 0.02 = 163.84元

下表为 GPU系数按 8 计算时，**每 1 张训练图片**的Token消耗与费用预估。训练集包含 N 张图片时，将表中数值乘以 N 即可。

| max\_pixels | n\_epochs | Token消耗预估 | 费用预估（元） |
| --- | --- | --- | --- |
| 1k | 800 | 6,553,600 | 131.07 |
| 1k | 1,000 | 8,192,000 | 163.84 |
| 1k | 2,000 | 16,384,000 | 327.68 |
| 2k | 800 | 26,214,400 | 524.29 |
| 2k | 1,000 | 32,768,000 | 655.36 |
| 2k | 2,000 | 65,536,000 | 1310.72 |

> **说明**
>
> -   GPU系数随任务调度情况动态调整，上述示例与预估表取 8 仅用于演示计算过程。实际训练消耗的Token数请以[查询微调任务状态](../../model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)接口返回的 `usage` 字段为准，费用以账单为准。
> -   `batch_size` 不参与计费，不影响训练Token总量。

<a id="视频生成模型-万相"></a>

<a id="a0f04032d3w0k"></a>

### 视频生成模型-万相

> **说明**
>
> 模型训练流程请参见[模型调优](../model-training/fine-tuning/wan-video-generation-finetune-guide.md)。训练完成后的新模型需先完成**模型部署**，才能调用。

|  |  |
| --- | --- |
| **计费方式** | 按训练Token计费 |
| **计费公式** | 模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token） |

<a id="accordion-训练token总量的计算公式-3"></a>

训练Token总量的计算公式

‘训练Token总量\=(∑i\=1N视频i的计费时长)×max\_pixels1024×n\_epochs‘\`训练 Token 总量 = \\left( \\sum\_{i=1}^{N} 视频\_i 的计费时长 \\right) \\times \\frac{max\\\_pixels}{1024} \\times n\\\_epochs\`‘训练Token总量\=(i\=1∑N​视频i​的计费时长)×1024max\_pixels​×n\_epochs‘

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

<table><thead><tr><th><p><strong>模型服务</strong></p></th><th><p><strong>模型名称</strong></p></th><th><p><strong>训练价格（每千Token）</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>万相-图生视频-基于首帧</p></td><td><p>wan2.7-i2v</p></td><td><p>2元</p></td></tr><tr><td><p>wan2.2-i2v-flash</p></td><td><p>0.06元</p></td></tr><tr><td><p>wan2.5-i2v-preview</p></td><td><p>0.32元</p></td></tr><tr><td rowspan="2"><p>图生视频-基于首尾帧</p></td><td><p>wan2.7-i2v</p></td><td><p>2元</p></td></tr><tr><td><p>wan2.2-kf2v-flash</p></td><td><p>0.06元</p></td></tr></tbody></table>

<a id="accordion-计费示例-3"></a>

计费示例

1.  **wan2.7-i2v 费用预估（一条数据）**

假设训练集包含 1 条视频，时长为10秒。由于 batch\_size = 1（推荐值），此时 `n_epochs = steps / ⌈1(数据集大小) / 1(batch_size)⌉ = steps`。

训练单价 = 2元/千Token，以 max\_pixels = 36864、n\_epochs = 800 为例：

-   训练Token总量 = 10 ×（36864 / 1024）× 800 = 288,000 = 288千Token
-   模型训练费用 = 288 × 2 = 576元

<table><thead><tr><th><p><strong>max_pixels</strong></p></th><th><p><strong>常见 steps</strong></p></th><th><p><strong>n_epochs</strong></p></th><th><p><strong>Token 消耗预估</strong></p></th><th><p><strong>费用预估（元）</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>36864</p></td><td><p>800</p></td><td><p>800</p></td><td><p>288,000</p></td><td><p>576</p></td></tr><tr><td><p>1,000</p></td><td><p>1,000</p></td><td><p>360,000</p></td><td><p>720</p></td></tr><tr><td><p>2,000</p></td><td><p>2,000</p></td><td><p>720,000</p></td><td><p>1,440</p></td></tr><tr><td rowspan="3"><p>65536</p></td><td><p>800</p></td><td><p>800</p></td><td><p>512,000</p></td><td><p>1,024</p></td></tr><tr><td><p>1,000</p></td><td><p>1,000</p></td><td><p>640,000</p></td><td><p>1,280</p></td></tr><tr><td><p>2,000</p></td><td><p>2,000</p></td><td><p>1,280,000</p></td><td><p>2,560</p></td></tr><tr><td rowspan="3"><p>102400</p></td><td><p>800</p></td><td><p>800</p></td><td><p>800,000</p></td><td><p>1,600</p></td></tr><tr><td><p>1,000</p></td><td><p>1,000</p></td><td><p>1,000,000</p></td><td><p>2,000</p></td></tr><tr><td><p>2,000</p></td><td><p>2,000</p></td><td><p>2,000,000</p></td><td><p>4,000</p></td></tr></tbody></table>

1.  **wan2.7-i2v 费用预估（多条数据）**

假设训练集包含 2 条视频，时长分别为 3.4 秒 和 11.5 秒。参数设置：max\_pixels = 36864、n\_epochs = 800，训练单价 = 2元/千Token：

-   时长计算：
    
    -   视频 1：3.4 → 四舍五入 → 3 秒 → 计费时长 = min(10, 3) = 3
    -   视频 2：11.5 → 四舍五入 → 12 秒 → 计费时长 = min(10, 12) = 10
    -   总计费时长 = 3 + 10 = 13 秒
-   训练Token总量 = 13 ×（36864/1024）× 800 = 374400 = 374.4千Token
    
-   模型训练费用 = 374.4 × 2 = 748.8元
    

<a id="语音合成模型-cosyvoice"></a>

<a id="cv_train_billing_h3"></a>

### 语音合成模型-CosyVoice

> **说明**
>
> CosyVoice 模型调优服务仅支持**华北2（北京）**地域。模型训练流程请参见[CosyVoice模型调优](../../_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)。训练完成后的新模型需先完成**模型部署**，才能调用。

|  |  |
| --- | --- |
| **计费方式** | 按训练消耗的Token数计费 |
| **训练单价** | 0.2元/千Tokens |
| **计费公式** | 模型训练费用 = 训练消耗Token总量 × 训练单价 |

<a id="accordion-训练消耗token总量的计算公式"></a>

训练消耗Token总量的计算公式

单次任务的Token消耗按下式估算：

‘消耗 Tokens\=(lm\_max\_epoch+fm\_max\_epoch)×25×训练集总时长(秒)‘\`\\text{消耗 Tokens} = (lm\\\_max\\\_epoch + fm\\\_max\\\_epoch) \\times 25 \\times \\text{训练集总时长(秒)}\`‘消耗 Tokens\=(lm\_max\_epoch+fm\_max\_epoch)×25×训练集总时长(秒)‘

其中 `lm_max_epoch` 与 `fm_max_epoch` 为创建调优任务时设置的超参数，分别表示 LM 与 FM 训练轮次；训练集总时长为调优数据集中全部音频文件的总秒数。提高任一轮次或扩大训练集均会线性增加 Token 消耗。

<a id="模型部署计费"></a>

<a id="0c4e677c48lrp"></a>

## 模型部署计费

<a id="文本生成模型-千问-2"></a>

<a id="0fb24c8ce3luy"></a>

### 文本生成模型-千问

<a id="sec-tabs-2"></a>

<a id="按使用时长计费-吞吐预留-高速模式"></a>

<a id="按使用时长计费-吞吐预留-高速模式-h4"></a>

#### 按使用时长计费（吞吐预留·高速模式）

`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`

后付费按小时计算：使用时长单位为小时，单价取下表"持续 1 小时"列；预付费按天计算：使用时长单位为天，单价取下表"持续 1 天"列。

-   预付费订单支付后实时生效，有效期 N 天至第 N 天 23:59 结束。
-   预付费订单到期后立即停止服务（不可调用，仍可续费），停机 2 小时后资源释放。
-   预付费订单支持提前终止服务，已使用部分按 1.2 倍系数结算退费。详见[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。
-   后付费时，如果账户欠费，部署的资源将不再可用且不计费，欠费缴清后服务恢复。

当模型输入超过最长输入 Token 时，相关调用将自动切换为当前模型的按量付费模式；超出购买的 TPM 量时，按创建时选择的溢出策略处理（“自动溢出”切换为按量付费，“仅使用预留容量”返回 429）。此时，推理性能可能下降，将受业务空间中当前快照模型的公共流量的管控，[费用](model-pricing.md)按模型调用（按量付费）标准计收。

-   此时（仅“自动溢出”策略下），调用 API 返回 Header 将包含：`x-dashscope-ptu-overflow:true`。
-   TPM 统计请前往：[模型监控（北京）](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)。

缩容场景（降配）的具体降费退费规则请参考：[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

> **说明**
>
> 吞吐预留支持长输入阶梯容量系数和缓存折扣，详见[吞吐预留计费](tpm-reservation-billing.md#tpm-billing-conversion-h2)。

<a id="sec-tabs-3"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-4"></a>

<a id="sec-tab-千问"></a>

<a id="sec-tab-千问-h4"></a>

#### 千问

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>最长输入Token</strong></p></th><th><p><strong>后付费输入</strong></p><p><strong>Per 10K TPM/小时</strong></p></th><th><p><strong>后付费输出</strong></p><p><strong>Per 1K TPM/小时</strong></p></th><th><p><strong>预付费输入</strong></p><p><strong>Per 10K TPM/天</strong></p></th><th><p><strong>预付费输出</strong></p><p><strong>Per 1K TPM/天</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.8-Flash</p></td><td><p>qwen3.8-flash</p></td><td><p>128K</p></td><td><p>¥2.88</p></td><td><p>¥0.97</p></td><td><p>¥34.56</p></td><td><p>¥11.66</p></td></tr><tr><td><p>Qwen3.8-Max</p></td><td><p>qwen3.8-max</p></td><td><p>1M</p></td><td><p>¥28.8</p></td><td><p>¥8.64</p></td><td><p>¥345.6</p></td><td><p>¥103.68</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3.7-Flash-2026-07-15</p></td><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>128K</p></td><td><p>¥0.48</p></td><td><p>¥0.19</p></td><td><p>¥5.76</p></td><td><p>¥2.3</p></td></tr><tr><td><p>Qwen3.7-Max-2026-05-20</p></td><td><p>qwen3.7-max-2026-05-20</p></td><td><p>256K</p></td><td><p>¥28.8</p></td><td><p>¥8.64</p></td><td><p>¥345.6</p></td><td><p>¥103.68</p></td></tr><tr><td><p>Qwen3.7-Plus-2026-05-26</p></td><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>256K</p></td><td><p>¥4.8</p></td><td><p>¥1.92</p></td><td><p>¥57.6</p></td><td><p>¥23.04</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3.6-Plus-2026-04-02</p></td><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>128K</p></td><td><p>¥4.8</p></td><td><p>¥2.88</p></td><td><p>¥57.6</p></td><td><p>¥34.56</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3.5-Plus-2026-04-20</p></td><td><p>qwen3.5-plus-2026-04-20</p></td><td><p>128K</p></td><td><p>¥1.92</p></td><td><p>¥1.15</p></td><td><p>¥23.04</p></td><td><p>¥13.82</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3-Max-2025-09-23</p></td><td><p>qwen3-max-2025-09-23</p></td><td><p>128K</p></td><td><p>¥7.68</p></td><td><p>¥3.08</p></td><td><p>¥92.16</p></td><td><p>¥36.96</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen-Flash-2025-07-28</p></td><td><p>qwen-flash-2025-07-28</p></td><td><p>128K</p></td><td><p>¥0.36</p></td><td><p>¥0.36</p></td><td><p>¥4.32</p></td><td><p>¥4.32</p></td></tr><tr><td><p>Qwen-Plus-2025-12-01</p></td><td><p>qwen-plus-2025-12-01</p></td><td><p>128K</p></td><td><p>¥1.92</p></td><td><p>非思考：¥0.48</p><p>思考：¥1.92</p></td><td><p>¥23.04</p></td><td><p>非思考：¥5.76</p><p>思考：¥23.04</p></td></tr></tbody></table>

<a id="sec-tab-deepseek"></a>

<a id="sec-tab-deepseek-h4"></a>

#### DeepSeek

| 模型名称 | 模型代码 | 最长输入Token | **后付费输入**<br><br>**Per 10K TPM/小时** | **后付费输出**<br><br>**Per 1K TPM/小时** | **预付费输入**<br><br>**Per 10K TPM/天** | **预付费输出**<br><br>**Per 1K TPM/天** |
| --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-v4-Flash | deepseek-v4-flash | 256K | ¥3.6 | ¥0.72 | ¥43.2 | ¥8.64 |
| DeepSeek-v4-Flash-0731 | deepseek-v4-flash-0731 | 256K | ¥7.2 | ¥1.44 | ¥86.4 | ¥17.28 |
| DeepSeek-v4-Pro | deepseek-v4-pro | 256K | ¥43.2 | ¥8.64 | ¥518.4 | ¥103.68 |
| DeepSeek-v3.2 | deepseek-v3.2 | 64K | ¥7.2 | ¥1.08 | ¥86.4 | ¥12.96 |

<a id="sec-tab-千问vl"></a>

<a id="sec-tab-千问vl-h4"></a>

#### 千问VL

| 模型名称 | 模型代码 | 最长输入Token | **后付费输入**<br><br>**Per 10K TPM/小时** | **后付费输出**<br><br>**Per 1K TPM/小时** | **预付费输入**<br><br>**Per 10K TPM/天** | **预付费输出**<br><br>**Per 1K TPM/天** |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-Plus-2025-09-23 | qwen3-vl-plus-2025-09-23 | 128K | ¥2.4 | ¥2.4 | ¥28.8 | ¥28.8 |

<a id="sec-tab-glm"></a>

<a id="sec-tab-glm-h4"></a>

#### GLM

| 模型名称 | 模型代码 | 最长输入Token | **后付费输入**<br><br>**Per 10K TPM/小时** | **后付费输出**<br><br>**Per 1K TPM/小时** | **预付费输入**<br><br>**Per 10K TPM/天** | **预付费输出**<br><br>**Per 1K TPM/天** |
| --- | --- | --- | --- | --- | --- | --- |
| GLM-5.2 | glm-5.2 | 1M | ¥28.8 | ¥10.08 | ¥345.6 | ¥120.96 |

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<a id="sec-tabs-5"></a>

<a id="sec-tab-千问-2"></a>

<a id="sec-tab-千问-2-h4"></a>

#### 千问

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>最长输入Token</strong></p></th><th><p><strong>后付费输入</strong></p><p><strong>Per 10K TPM/小时</strong></p></th><th><p><strong>后付费输出</strong></p><p><strong>Per 1K TPM/小时</strong></p></th><th><p><strong>预付费输入</strong></p><p><strong>Per 10K TPM/天</strong></p></th><th><p><strong>预付费输出</strong></p><p><strong>Per 1K TPM/天</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.8-Flash</p></td><td><p>qwen3.8-flash</p></td><td><p>128K</p></td><td><p>¥3.94</p></td><td><p>¥1.23</p></td><td><p>¥47.25</p></td><td><p>¥14.81</p></td></tr><tr><td><p>Qwen3.8-Max</p></td><td><p>qwen3.8-max</p></td><td><p>1M</p></td><td><p>¥35.97</p></td><td><p>¥10.79</p></td><td><p>¥431.7</p></td><td><p>¥129.5</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3.7-Flash-2026-07-15</p></td><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>128K</p></td><td><p>¥0.54</p></td><td><p>¥0.23</p></td><td><p>¥6.47</p></td><td><p>¥2.81</p></td></tr><tr><td><p>Qwen3.7-Max-2026-05-20</p></td><td><p>qwen3.7-max-2026-05-20</p></td><td><p>256K</p></td><td><p>¥44.97</p></td><td><p>¥13.49</p></td><td><p>¥539.6</p></td><td><p>¥161.87</p></td></tr><tr><td><p>Qwen3.7-Plus-2026-05-26</p></td><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>256K</p></td><td><p>¥7.19</p></td><td><p>¥2.88</p></td><td><p>¥86.3</p></td><td><p>¥34.53</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3.6-Plus-2026-04-02</p></td><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>128K</p></td><td><p>¥9</p></td><td><p>¥5.4</p></td><td><p>¥107.9</p></td><td><p>¥64.75</p></td></tr><tr><td colspan="7"></td></tr><tr><td><p>Qwen3.5-Plus-2026-04-20</p></td><td><p>qwen3.5-plus-2026-04-20</p></td><td><p>128K</p></td><td><p>¥7.2</p></td><td><p>¥4.32</p></td><td><p>¥86.3</p></td><td><p>¥51.8</p></td></tr></tbody></table>

<a id="sec-tab-deepseek-2"></a>

<a id="sec-tab-deepseek-2-h4"></a>

#### DeepSeek

| 模型名称 | 模型代码 | 最长输入Token | **后付费输入**<br><br>**Per 10K TPM/小时** | **后付费输出**<br><br>**Per 1K TPM/小时** | **预付费输入**<br><br>**Per 10K TPM/天** | **预付费输出**<br><br>**Per 1K TPM/天** |
| --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-v4-Flash | deepseek-v4-flash | 256K | ¥5.4 | ¥1.08 | ¥64.8 | ¥12.95 |
| DeepSeek-v4-Flash-0731 | deepseek-v4-flash-0731 | 256K | ¥10.79 | ¥2.16 | ¥129.5 | ¥25.9 |
| DeepSeek-v4-Pro | deepseek-v4-pro | 256K | ¥64.75 | ¥12.95 | ¥777 | ¥155.4 |

<a id="sec-tab-千问vl-2"></a>

<a id="sec-tab-千问vl-2-h4"></a>

#### 千问VL

| 模型名称 | 模型代码 | 最长输入Token | **后付费输入**<br><br>**Per 10K TPM/小时** | **后付费输出**<br><br>**Per 1K TPM/小时** | **预付费输入**<br><br>**Per 10K TPM/天** | **预付费输出**<br><br>**Per 1K TPM/天** |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-Plus-2025-09-23 | qwen3-vl-plus-2025-09-23 | 128K | ¥3.6 | ¥2.88 | ¥43.2 | ¥34.53 |

<a id="按使用时长计费-独占吞吐"></a>

<a id="按使用时长计费-独占吞吐-h4"></a>

#### 按使用时长计费（独占吞吐）

-   预付费订单支持提前退订，已使用部分按 1.2 倍系数结算退费。详见[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

<a id="sec-tabs-6"></a>

<a id="华北-北京2"></a>

<a id="华北-北京2-h4"></a>

#### 华北-北京2

<table><thead><tr><th><p><strong>模型</strong></p></th><th><p><strong>规格</strong></p></th><th><p><strong>基准输入（TPM）</strong></p></th><th><p><strong>基准输出（TPM）</strong></p></th><th><p><strong>起售价格(元/月)</strong></p></th><th><p><strong>扩容价格(元/月)</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.8-27b</p></td><td><p>Efficient</p></td><td><p>268,000</p></td><td><p>33,000</p></td><td><p>49,208</p></td><td><p>49,208</p></td></tr><tr><td><p>Fast</p></td><td><p>1,172,000</p></td><td><p>146,000</p></td><td><p>278,460</p></td><td><p>278,460</p></td></tr><tr><td rowspan="2"><p>qwen3.8-flash</p></td><td><p>Efficient</p></td><td><p>580,000</p></td><td><p>72,000</p></td><td><p>196,228</p></td><td><p>196,228</p></td></tr><tr><td><p>Custom</p></td><td><p>1,272,000</p></td><td><p>152,000</p></td><td><p>635,680</p></td><td><p>635,680</p></td></tr><tr><td rowspan="4"><p>qwen3.7-plus-2026-05-26</p></td><td><p>Fast</p></td><td><p>1,372,000</p></td><td><p>170,000</p></td><td><p>556,466</p></td><td><p>556,466</p></td></tr><tr><td><p>Fast</p></td><td><p>1,192,000</p></td><td><p>148,000</p></td><td><p>555,680</p></td><td><p>555,680</p></td></tr><tr><td><p>Fast</p></td><td><p>704,000</p></td><td><p>132,000</p></td><td><p>556,072</p></td><td><p>556,072</p></td></tr><tr><td><p>Fast</p></td><td><p>660,000</p></td><td><p>124,000</p></td><td><p>555,744</p></td><td><p>555,744</p></td></tr><tr><td><p>qwen3.7-plus-2026-07-09</p></td><td><p>Fast</p></td><td><p>1,270,000</p></td><td><p>158,000</p></td><td><p>277,470</p></td><td><p>277,470</p></td></tr><tr><td rowspan="2"><p>qwen3.6-27b</p></td><td><p>Standard</p></td><td><p>273,000</p></td><td><p>34,000</p></td><td><p>49,118</p></td><td><p>49,118</p></td></tr><tr><td><p>Fast</p></td><td><p>1,818,000</p></td><td><p>277,000</p></td><td><p>370,749</p></td><td><p>370,749</p></td></tr><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>Standard</p></td><td><p>896,000</p></td><td><p>112,000</p></td><td><p>1,107,904</p></td><td><p>1,107,904</p></td></tr><tr><td><p>Fast</p></td><td><p>1,496,000</p></td><td><p>186,000</p></td><td><p>741,520</p></td><td><p>741,520</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>Fast</p></td><td><p>7,288,000</p></td><td><p>904,000</p></td><td><p>2,226,984</p></td><td><p>2,226,984</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td><p>Standard</p></td><td><p>656,000</p></td><td><p>82,000</p></td><td><p>109,962</p></td><td><p>109,962</p></td></tr><tr><td><p>Efficient</p></td><td><p>595,000</p></td><td><p>74,000</p></td><td><p>48,963</p></td><td><p>48,963</p></td></tr><tr><td rowspan="3"><p>qwen3.5-27b</p></td><td><p>Standard</p></td><td><p>2,432,000</p></td><td><p>304,000</p></td><td><p>1,108,688</p></td><td><p>1,108,688</p></td></tr><tr><td><p>Efficient</p></td><td><p>291,000</p></td><td><p>36,000</p></td><td><p>48,996</p></td><td><p>48,996</p></td></tr><tr><td><p>Fast</p></td><td><p>1,515,000</p></td><td><p>189,000</p></td><td><p>278,295</p></td><td><p>278,295</p></td></tr><tr><td><p>qwen3.5-4b</p></td><td><p>Standard</p></td><td><p>1,072,000</p></td><td><p>134,000</p></td><td><p>109,478</p></td><td><p>109,478</p></td></tr><tr><td><p>glm-5.3</p></td><td><p>Fast</p></td><td><p>1,004,000</p></td><td><p>120,000</p></td><td><p>1,895,260</p></td><td><p>1,895,260</p></td></tr><tr><td><p>glm-5.3-flash</p></td><td><p>Fast</p></td><td><p>769,000</p></td><td><p>96,000</p></td><td><p>278,197</p></td><td><p>278,197</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>V2</p></td><td><p>502,000</p></td><td><p>60,000</p></td><td><p>947,630</p></td><td><p>947,630</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>Standard</p></td><td><p>256,000</p></td><td><p>32,000</p></td><td><p>504,704</p></td><td><p>504,704</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>Fast</p></td><td><p>2,312,000</p></td><td><p>288,000</p></td><td><p>555,360</p></td><td><p>555,360</p></td></tr><tr><td rowspan="2"><p>deepseek-v4-flash</p></td><td><p>Standard</p></td><td><p>2,240,000</p></td><td><p>280,000</p></td><td><p>1,107,400</p></td><td><p>1,107,400</p></td></tr><tr><td><p>Fast</p></td><td><p>1,807,000</p></td><td><p>225,000</p></td><td><p>278,189</p></td><td><p>278,189</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>Fast</p></td><td><p>1,676,000</p></td><td><p>213,000</p></td><td><p>277,984</p></td><td><p>277,984</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>Fast</p></td><td><p>1,536,000</p></td><td><p>192,000</p></td><td><p>2,223,744</p></td><td><p>2,223,744</p></td></tr></tbody></table>

<table><thead><tr><th><p><strong>模型</strong></p></th><th><p><strong>规格</strong></p></th><th><p><strong>输入长度</strong></p></th><th><p><strong>输出长度</strong></p></th><th><p><strong>缓存命中率</strong></p></th><th><p><strong>首字延迟(ms)</strong></p></th><th><p><strong>每token延迟(ms)</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.8-27b</p></td><td><p>Efficient</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,249</p></td><td><p>26</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,207</p></td><td><p>15</p></td></tr><tr><td rowspan="2"><p>qwen3.8-flash</p></td><td><p>Efficient</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,296</p></td><td><p>19</p></td></tr><tr><td><p>Custom</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>3,659</p></td><td><p>19</p></td></tr><tr><td rowspan="4"><p>qwen3.7-plus-2026-05-26</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,418</p></td><td><p>15</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>888</p></td><td><p>10</p></td></tr><tr><td><p>Fast</p></td><td><p>2,600</p></td><td><p>500</p></td><td><p>0</p></td><td><p>970</p></td><td><p>13</p></td></tr><tr><td><p>Fast</p></td><td><p>2,600</p></td><td><p>500</p></td><td><p>0</p></td><td><p>819</p></td><td><p>14</p></td></tr><tr><td><p>qwen3.7-plus-2026-07-09</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,402</p></td><td><p>12</p></td></tr><tr><td rowspan="2"><p>qwen3.6-27b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,292</p></td><td><p>19</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,106</p></td><td><p>14</p></td></tr><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>996</p></td><td><p>27</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>2,465</p></td><td><p>18</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>568</p></td><td><p>8</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>471</p></td><td><p>10</p></td></tr><tr><td><p>Efficient</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,822</p></td><td><p>12</p></td></tr><tr><td rowspan="3"><p>qwen3.5-27b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>703</p></td><td><p>14</p></td></tr><tr><td><p>Efficient</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,448</p></td><td><p>23</p></td></tr><tr><td><p>Fast</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>1,121</p></td><td><p>13</p></td></tr><tr><td><p>qwen3.5-4b</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>552</p></td><td><p>6</p></td></tr><tr><td><p>glm-5.3</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,558</p></td><td><p>15</p></td></tr><tr><td><p>glm-5.3-flash</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,271</p></td><td><p>12</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>V2</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,558</p></td><td><p>15</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>769</p></td><td><p>27</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,824</p></td><td><p>14</p></td></tr><tr><td rowspan="2"><p>deepseek-v4-flash</p></td><td><p>Standard</p></td><td><p>4,000</p></td><td><p>500</p></td><td><p>0</p></td><td><p>651</p></td><td><p>19</p></td></tr><tr><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,408</p></td><td><p>12</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,079</p></td><td><p>13</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>Fast</p></td><td><p>16,000</p></td><td><p>2,000</p></td><td><p>0</p></td><td><p>1,607</p></td><td><p>14</p></td></tr></tbody></table>

<a id="按模型-token-使用量"></a>

<a id="按模型-token-使用量-h4"></a>

#### 按模型 Token 使用量

`费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）`

-   仅当对下列基础模型完成 SFT 高效训练（即 LoRA 高效微调，API 部署时 plan 取值为 lora）并得到自定义模型后，才支持按模型 Token 使用量计费。

<a id="sec-tabs-7"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

<table><thead><tr><th><p><strong>基础模型</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>输入</strong></p><p><strong>元/百万Token</strong></p></th><th><p><strong>输出</strong></p><p><strong>元/百万Token</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.5-27B</p></td><td><p>qwen3.5-27b</p></td><td><p>&lt;128K ¥0.6</p><p>128K-256K ¥1.8</p></td><td><p>&lt;128K ¥4.8</p><p>128K-256K ¥14.4</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-32B</p></td><td><p>qwen3-32b</p></td><td><p>非思考模式：¥2</p><p>思考模式：¥2</p></td><td><p>非思考模式：¥8</p><p>思考模式：¥20</p></td></tr><tr><td><p>Qwen3-14B</p></td><td><p>qwen3-14b</p></td><td><p>非思考模式：¥1</p><p>思考模式：¥1</p></td><td><p>非思考模式：¥4</p><p>思考模式：¥10</p></td></tr><tr><td><p>Qwen3-8B</p></td><td><p>qwen3-8b</p></td><td><p>非思考模式：¥0.5</p><p>思考模式：¥0.5</p></td><td><p>非思考模式：¥2</p><p>思考模式：¥5</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-VL-8B-Instruct</p></td><td><p>qwen3-vl-8b-instruct</p></td><td><p>¥0.5</p></td><td><p>¥2</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-4B-Instruct-2507</p></td><td><p>qwen3-4b-instruct-2507</p></td><td><p>非思考模式：¥0.3</p><p>思考模式：¥0.3</p></td><td><p>非思考模式：¥1.2</p><p>思考模式：¥3</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>¥4</p></td><td><p>¥12</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-72B</p></td><td><p>qwen2.5-vl-72b-instruct</p></td><td><p>¥16</p></td><td><p>¥48</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-32B</p></td><td><p>qwen2.5-32b-instruct</p></td><td><p>¥2</p></td><td><p>¥6</p></td></tr><tr><td><p>Qwen2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>¥1</p></td><td><p>¥3</p></td></tr><tr><td><p>Qwen2.5-开源版-7B</p></td><td><p>qwen2.5-7b-instruct</p></td><td><p>¥0.5</p></td><td><p>¥1</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-7B</p></td><td><p>qwen2.5-vl-7b-instruct</p></td><td><p>¥2</p></td><td><p>¥5</p></td></tr></tbody></table>

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>基础模型</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>输入</strong></p><p><strong>元/百万Token</strong></p></th><th><p><strong>输出</strong></p><p><strong>元/百万Token</strong></p></th></tr></thead><tbody><tr><td><p>Qwen3.5-27B</p></td><td><p>qwen3.5-27b</p></td><td><p>¥2.202</p></td><td><p>¥17.614</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-32B</p></td><td><p>qwen3-32b</p></td><td><p>非思考模式：¥1.174</p><p>思考模式：¥1.174</p></td><td><p>非思考模式：¥4.697</p><p>思考模式：¥4.697</p></td></tr><tr><td><p>Qwen3-14B</p></td><td><p>qwen3-14b</p></td><td><p>非思考模式：¥2.569</p><p>思考模式：¥2.569</p></td><td><p>非思考模式：¥10.275</p><p>思考模式：¥30.825</p></td></tr><tr><td><p>Qwen3-8B</p></td><td><p>qwen3-8b</p></td><td><p>非思考模式：¥1.321</p><p>思考模式：¥1.321</p></td><td><p>非思考模式：¥5.137</p><p>思考模式：¥15.412</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-VL-8B-Instruct</p></td><td><p>qwen3-vl-8b-instruct</p></td><td><p>¥1.321</p></td><td><p>¥5.137</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen3-4B-Instruct-2507</p></td><td><p>qwen3-4b-instruct-2507</p></td><td><p>非思考模式：¥0.807</p><p>思考模式：¥0.807</p></td><td><p>非思考模式：¥3.082</p><p>思考模式：¥9.247</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>¥10.275</p></td><td><p>¥41.1</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-72B</p></td><td><p>qwen2.5-vl-72b-instruct</p></td><td><p>¥20.55</p></td><td><p>¥61.65</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-开源版-32B</p></td><td><p>qwen2.5-32b-instruct</p></td><td><p>¥5.137</p></td><td><p>¥20.55</p></td></tr><tr><td><p>Qwen2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>¥2.569</p></td><td><p>¥10.275</p></td></tr><tr><td><p>Qwen2.5-开源版-7B</p></td><td><p>qwen2.5-7b-instruct</p></td><td><p>¥1.284</p></td><td><p>¥5.137</p></td></tr><tr><td colspan="4"></td></tr><tr><td><p>Qwen2.5-VL-7B</p></td><td><p>qwen2.5-vl-7b-instruct</p></td><td><p>¥2.569</p></td><td><p>¥7.706</p></td></tr></tbody></table>

<a id="按使用时长计费-模型单元"></a>

<a id="按使用时长计费-模型单元-h4"></a>

#### 按使用时长计费（模型单元）

`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`

"模型单元单价"在后付费场景下取下表"小时单价"列；预付费按月计费时，公式改为 **包月数 × 模型单元数量 × 月单价**。

-   预付费购买的首月，如在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费（不满一天按一天计费）

> **说明**
>
> 模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。

<a id="sec-tabs-8"></a>

<a id="文本生成"></a>

<a id="文本生成-h4"></a>

#### 文本生成

<a id="sec-tabs-9"></a>

<a id="千问-2"></a>

<a id="千问-2-h4"></a>

#### 千问

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>Qwen3.6-35B-A3B</p></td><td rowspan="5"><p>qwen3.6-35b-a3b</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU8 x 1</p></td><td><p>¥47</p></td><td><p>¥22,400</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td><p>Qwen3.6-27B</p></td><td><p>qwen3.6-27b</p></td><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="2"><p>Qwen3.6-Flash-2026-04-16</p></td><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td colspan="5"></td></tr><tr><td rowspan="2"><p>Qwen3.5-397B-A17B</p></td><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>MU3 x 8</p><p>MU3 x 16（PD分离模式）</p></td><td><p>¥1,096</p><p>PD分离模式：¥2,192</p></td><td><p>¥527,752</p><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td rowspan="2"><p>Qwen3.5-122B-A10B</p></td><td rowspan="2"><p>qwen3.5-122b-a10b</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td rowspan="4"><p>Qwen3.5-35B-A3B</p></td><td rowspan="4"><p>qwen3.5-35b-a3b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="4"><p>Qwen3.5-27B</p></td><td rowspan="4"><p>qwen3.5-27b</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU8 x 1</p></td><td><p>¥47</p></td><td><p>¥22,400</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="2"><p>Qwen3.5-9B</p></td><td rowspan="2"><p>qwen3.5-9b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>Qwen3.5-Flash-2026-02-23</p></td><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="3"><p>Qwen3.5-Plus-2026-02-15</p></td><td rowspan="3"><p>qwen3.5-plus-2026-02-15</p></td><td><p>MU1 x 8</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥432</p><p>PD分离模式：¥864</p></td><td><p>¥208,944</p><p>PD分离模式：¥417,888</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p><p>MU3 x 16（PD分离模式）</p></td><td><p>¥1,096</p><p>PD分离模式：¥2,192</p></td><td><p>¥527,752</p><p>PD分离模式：¥1,055,504</p></td></tr><tr><td colspan="5"></td></tr><tr><td rowspan="3"><p>Qwen3-235B-A22B-Instruct-2507</p></td><td rowspan="3"><p>qwen3-235b-a22b-instruct-2507</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>Qwen3-32B</p></td><td><p>qwen3-32b</p></td><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td><p>Qwen3-30B-A3B-Thinking-2507</p></td><td><p>qwen3-30b-a3b-thinking-2507</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="2"><p>Qwen3-4B</p></td><td rowspan="2"><p>qwen3-4b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td rowspan="2"><p>Qwen3-Embedding-0.6B</p></td><td rowspan="2"><p>qwen3-embedding-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>MU6 x 1</p></td><td><p>¥25</p></td><td><p>¥12,089</p></td></tr><tr><td><p>Qwen3-MoE-Rerank-0.6B</p></td><td><p>qwen3-moe-rerank-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td rowspan="2"><p>Qwen3-Rerank-0.6B</p></td><td rowspan="2"><p>qwen3-rerank-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>MU6 x 1</p></td><td><p>¥25</p></td><td><p>¥12,089</p></td></tr><tr><td rowspan="2"><p>Qwen3-Max-2025-09-23</p></td><td rowspan="2"><p>qwen3-max-2025-09-23</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>Qwen3-Rerank</p></td><td><p>qwen3-rerank</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td colspan="5"></td></tr><tr><td><p>Qwen2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>Qwen2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="2"><p>Qwen2.5-开源版-7B</p></td><td rowspan="2"><p>qwen2.5-7b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td colspan="5"></td></tr><tr><td><p>Qwen-Plus-2025-07-28</p></td><td><p>qwen-plus-2025-07-28</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>Qwen-Plus-2025-12-01</p></td><td><p>qwen-plus-2025-12-01</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>Qwen-Plus-Character-2025-11-06</p></td><td><p>qwen-plus-character-2025-11-06</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr></tbody></table>

<a id="glm"></a>

<a id="glm-h4"></a>

#### GLM

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>GLM-5.1</p></td><td rowspan="3"><p>glm-5.1</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td><p>GLM-5</p></td><td><p>glm-5</p></td><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>GLM-4.7</p></td><td><p>glm-4.7</p></td><td><p>MU6 x 32（PD分离模式）</p></td><td><p>PD分离模式：¥800</p></td><td><p>PD分离模式：¥386,848</p></td></tr><tr><td><p>GLM-4.7-Flash</p></td><td><p>glm-4.7-flash</p></td><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr></tbody></table>

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

<a id="sec-tabs-10"></a>

<a id="千问vl-2"></a>

<a id="千问vl-2-h4"></a>

#### 千问VL

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>Qwen3-VL-235B-A22B-Thinking</p></td><td rowspan="3"><p>qwen3-vl-235b-a22b-thinking</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td rowspan="2"><p>Qwen3-VL-32B-Instruct</p></td><td rowspan="2"><p>qwen3-vl-32b-instruct</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>Qwen3-VL-30B-A3B-Instruct</p></td><td><p>qwen3-vl-30b-a3b-instruct</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td rowspan="2"><p>Qwen3-VL-8B-Instruct</p></td><td rowspan="2"><p>qwen3-vl-8b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>Qwen3-VL-4B-Instruct</p></td><td><p>qwen3-vl-4b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>Qwen3-VL-2B-Instruct</p></td><td><p>qwen3-vl-2b-instruct</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>Qwen3-VL-Embedding-2B</p></td><td><p>qwen3-vl-embedding-2b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>Qwen3-VL-Flash-2025-10-15</p></td><td><p>qwen3-vl-flash-2025-10-15</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>Qwen3-VL-Plus-2025-09-23</p></td><td><p>qwen3-vl-plus-2025-09-23</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td colspan="5"></td></tr><tr><td><p>QwenVL-Max-2025-08-13</p></td><td><p>qwen-vl-max-2025-08-13</p></td><td><p>MU6 x 4</p></td><td><p>¥100</p></td><td><p>¥48,356</p></td></tr></tbody></table>

<a id="千问-omni"></a>

<a id="千问-omni-h4"></a>

#### 千问 Omni

| 模型名称 | 模型代码 | 模型单元规格 | **小时单价（元）**<br><br>**最小计费：分钟** | **包月单价（元）**<br><br>**最小计费：天** |
| --- | --- | --- | --- | --- |
| Qwen3.5-Omni-Flash | qwen3.5-omni-flash | MU9 x 1 | ¥51 | ¥24,600 |

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

<a id="图像生成模型-万相-2"></a>

<a id="5afd5313a55kd"></a>

### 图像生成模型-万相

经过SFT-LoRA高效微调的万相图像生成模型，部署免费，调用按微调的基础模型的标准调用价格计费。模型训练和部署流程请参见[图像生成模型调优](../model-training/fine-tuning/wan-image-generation-finetune-guide.md)。

| 模型名称 | Lora部署调用价格 |
| --- | --- |
| wan2.7-image-pro | 0.50元/张 |
| wan2.7-image | 0.20元/张 |

<a id="图像生成模型-千问-2"></a>

<a id="qwen_img_deploy_billing_h3"></a>

### 图像生成模型-千问

经过SFT-LoRA高效微调的千问图像生成模型，部署免费，调用按微调的基础模型的标准调用价格计费。模型训练和部署流程请参见[图像生成模型调优](../model-training/fine-tuning/wan-image-generation-finetune-guide.md)。

| 模型名称 | Lora部署调用价格 |
| --- | --- |
| qwen-image-2.0 | 0.20元/张 |
| qwen-image-2.0-pro | 0.50元/张 |

<a id="视频生成模型-万相-2"></a>

<a id="wan_video_deploy_billing_h3"></a>

### 视频生成模型-万相

经过微调的万相视频生成模型：

-   **模型部署**：免费
-   **模型调用**：收费，按微调所基于的基础模型的标准调用价格计费，具体请参见[模型价格](model-pricing.md)

<a id="语音合成模型-cosyvoice-2"></a>

<a id="cv_deploy_billing_h3"></a>

### 语音合成模型-CosyVoice

> **说明**
>
> CosyVoice 模型调优服务仅支持**华北2（北京）**地域。

`调优后的CosyVoice模型部署后按<strong>模型单元的使用时长</strong>计费，公式为：$\text{费用} = \text{使用时长（小时）} \times \text{模型单元数量} \times \text{模型单元单价}$。`

`其中，$\text{模型单元数量} = \text{单副本模型单元} \times \text{部署副本数}$，可选的模版及对应的模型单元类型请参见CosyVoice模型调优的[部署模版](/zh/model-studio/fine-tune-speech-synthesis-model-by-api)。`

| 模型名称 | 模型代码 | 模型单元规格 | 小时单价（元） | 包月单价（元） |
| --- | --- | --- | --- | --- |
| cosyvoice-v3-flash | cosyvoice-v3-flash | MU5 | ¥21 | ¥10,139 |

<a id="常见问题"></a>

<a id="8ba3aeba9ep4i"></a>

## 常见问题

<a id="q-模型部署什么时候开始计费"></a>

<a id="f668bad157bg4"></a>

### Q：模型部署什么时候开始计费？

A：当模型完成部署，即状态为**运行中**时，开始收取模型部署的费用。模型状态为**部署中**、**欠费**、**部署失败**时，均不会计费。

如果是包月预付费，模型状态为**运行中**后，开始消耗包月时间。

<a id="q-取消模型训练会收费么"></a>

<a id="f7470da8adpc5"></a>

### Q：取消模型训练会收费么？

A：**会收费**。主动取消训练后，已消耗的 tokens 仍会推送计费，训练费用按已消耗 tokens 估算，最终费用以账单为准。其他原因导致的训练中断，阿里云百炼不会向您收取训练费用。

<a id="q-怎么查看已部署模型的调用统计"></a>

<a id="7e0f320e0bcl4"></a>

### Q：怎么查看已部署模型的调用统计？

A：请访问[模型监控（北京）](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)、[模型监控（弗吉尼亚）](https://bailian.console.aliyun.com/us-east-1/model/telemetry)、[模型监控（新加坡）](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry)、[模型监控（中国香港）](https://bailian.console.aliyun.com/cn-hongkong/model/telemetry)（中国香港仅支持普通监控，高级监控和日志不可用）页面。

模型监控页面支持按时间范围（3小时、6小时、12小时、24小时、今天、昨天、一周、自定义）和推理类型筛选，上方汇总区展示模型总量、总调用次数、总失败次数、平均调用时长、平均首包时长，下方模型列表展示各模型的调用总量、调用失败量、失败率、平均调用时长、平均首Token延时等指标，可单击**监控**查看单模型详细数据。

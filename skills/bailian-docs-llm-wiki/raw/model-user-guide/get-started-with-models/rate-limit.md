# 限流

百炼模型限流规则与各模型限流额度。主流生成模型采用动态限流（软限流），TPM 限流值随百炼月消费档位按月调整，实际可用 TPM 不低于限流值；其余模型与地域为静态限流，超出限制时请求被拒绝，通常在一分钟内自动恢复。限流按主账号维度计算，RAM 子账号、业务空间和 API Key 调用量合并。

<a id="限流规则"></a>

<a id="0d83adbf7f19s"></a>

## 限流规则

-   **账号级别限流**：限流按主账号维度计算，账号下所有RAM子账号、业务空间和API Key 的调用量合并计算。
-   **模型独立限流**：不同模型限流额度相互独立，具体参见下方表格。
-   **限流形态**：主流生成模型（如 qwen3.8-max、qwen3.8-flash、deepseek-v4-pro-0813、kimi-k3 等）采用**动态限流**，TPM 限流值随百炼月消费档位按月动态调整，实际可用 TPM 不低于限流值，详见[动态限流](#dynamic-rate-limiting)；其余模型与地域采用**静态限流**，规则详见[静态限流规则](#static-rate-limit-rules)。

<a id="动态限流"></a>

<a id="dynamic-rate-limiting"></a>

## 动态限流

<a id="动态限流机制"></a>

<a id="sec-mechanism-h2"></a>

### 动态限流机制

百炼对部分模型采用动态限流机制，核心要点如下：

-   **限流值**：按用户在百炼的月消费额度分档确定，作为吞吐的保证基线，每月调整。
-   **软限流**：当调用量达到限流值时，若平台仍有剩余资源，则不会触发限流，因此**实际可用 TPM** 不低于限流值；调用时观察到的实际限流值可能高于该限流值，属预期行为。
-   **限流粒度**：按账号 + 模型，主账号下所有 RAM 子账号、业务空间、API Key 的调用量合并计入该账号对该模型的 TPM 配额，共享同一限额。
-   **业务空间**：可为模型单独设置限流值，未单独设置的业务空间共享账号级配额。
-   **报错表现**：当平台资源不足时，百炼会保护性地拒绝部分请求并返回 429 错误（报错信息为 Too many requests.）。这类报错表征的是平台侧资源状况，并非用户侧调用量问题；服务本身正常运行，被拒绝的请求未交付、不计费，稍后重试即可。
-   **错误码区分**：未超出限流值的请求被拒时返回 Throttling.ResourceExhausted；超出限流值的请求会以较低优先级继续尝试，被拒时返回 Throttling.ServiceOverloaded。错误处理建议参见[错误码](../../model-api-reference/preparations/error-code.md)。
-   **更多说明**：业务空间限流设置见[权限管理](../security-and-compliance/permission-management-overview.md)。

<a id="模型与限流档位"></a>

<a id="sec-tier-h2"></a>

### 模型与限流档位

TPM 限流值按**百炼平台月消费金额**分档，支持的模型在不同地域的分档如下（数值以控制台实际展示为准）：

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>百炼平台月消费：</strong></p></th><th><p><strong>等级1（当前）≤¥10万</strong></p></th><th><p><strong>等级2 ¥10万~¥100万</strong></p></th><th><p><strong>等级3 &gt;¥100万</strong></p></th></tr><tr><th><p><strong>支持的模型</strong></p></th><th colspan="3"><p><strong>TPM 限流档位</strong></p></th></tr></thead><tbody><tr><td><p><strong>qwen4-max</strong></p></td><td><p>500万</p></td><td><p>1000万</p></td><td><p>2000万</p></td></tr><tr><td><p><strong>qwen3.8-max</strong></p></td><td><p>500万</p></td><td><p>1000万</p></td><td><p>2000万</p></td></tr><tr><td><p><strong>qwen3.8-max-0902</strong></p></td><td><p>150万</p></td><td><p>150万</p></td><td><p>150万</p></td></tr><tr><td><p><strong>qwen3.8-flash</strong></p></td><td><p>500万</p></td><td><p>1000万</p></td><td><p>2000万</p></td></tr><tr><td><p><strong>qwen3.8-omni-flash</strong></p></td><td><p>200万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>qwen3.8-2.4t-a95b</strong></p></td><td><p>500万</p></td><td><p>500万</p></td><td><p>500万</p></td></tr><tr><td><p><strong>deepseek-v4.1-flash-1017</strong></p></td><td><p>120万</p></td><td><p>120万</p></td><td><p>120万</p></td></tr><tr><td><p><strong>deepseek-v4.1-flash</strong></p></td><td><p>120万</p></td><td><p>120万</p></td><td><p>120万</p></td></tr><tr><td><p><strong>deepseek-v4-pro-0813</strong></p></td><td><p>120万</p></td><td><p>1000万</p></td><td><p>2000万</p></td></tr><tr><td><p><strong>kimi-k3.1-pro-prime</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>kimi-k3.1-pro</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>kimi-k3</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>glm-5.3</strong></p></td><td><p>500万</p></td><td><p>500万</p></td><td><p>500万</p></td></tr><tr><td><p><strong>glm-5.3-prime</strong></p></td><td><p>200万</p></td><td><p>200万</p></td><td><p>200万</p></td></tr><tr><td><p><strong>qwen3.8-27b</strong></p></td><td><p>500万</p></td><td><p>500万</p></td><td><p>500万</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>百炼平台月消费：</strong></p></th><th><p><strong>等级1（当前）≤¥10万</strong></p></th><th><p><strong>等级2 ¥10万~¥100万</strong></p></th><th><p><strong>等级3 &gt;¥100万</strong></p></th></tr><tr><th><p><strong>支持的模型</strong></p></th><th colspan="3"><p><strong>TPM 限流档位</strong></p></th></tr></thead><tbody><tr><td><p><strong>qwen4-max</strong></p></td><td><p>500万</p></td><td><p>1000万</p></td><td><p>2000万</p></td></tr><tr><td><p><strong>qwen3.8-max</strong></p></td><td><p>200万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>qwen3.8-max-0902</strong></p></td><td><p>150万</p></td><td><p>150万</p></td><td><p>150万</p></td></tr><tr><td><p><strong>qwen3.8-flash</strong></p></td><td><p>250万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>qwen3.8-omni-flash</strong></p></td><td><p>200万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>qwen3.8-2.4t-a95b</strong></p></td><td><p>500万</p></td><td><p>500万</p></td><td><p>500万</p></td></tr><tr><td><p><strong>deepseek-v4.1-flash-1017</strong></p></td><td><p>120万</p></td><td><p>120万</p></td><td><p>120万</p></td></tr><tr><td><p><strong>deepseek-v4.1-flash</strong></p></td><td><p>120万</p></td><td><p>120万</p></td><td><p>120万</p></td></tr><tr><td><p><strong>deepseek-v4-pro-0813</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>kimi-k3.1-pro</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>kimi-k3.1-pro-prime</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>kimi-k3</strong></p></td><td><p>120万</p></td><td><p>500万</p></td><td><p>1000万</p></td></tr><tr><td><p><strong>glm-5.3</strong></p></td><td><p>500万</p></td><td><p>500万</p></td><td><p>500万</p></td></tr><tr><td><p><strong>glm-5.3-prime</strong></p></td><td><p>200万</p></td><td><p>200万</p></td><td><p>200万</p></td></tr><tr><td><p><strong>qwen3.8-27b</strong></p></td><td><p>500万</p></td><td><p>500万</p></td><td><p>500万</p></td></tr></tbody></table>

以华北2（北京）为例：某账号上一自然月百炼消费金额为 50 万元，落入等级2（¥10万~¥100万）档位，对应 qwen4-max 的 TPM 限流值为 1000万。

<a id="额度展示"></a>

<a id="sec-view-quota-h2"></a>

### 额度展示

登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/costing-balance/quota-managements)，在左侧导航栏，选择**模型限额**进入模型限额页。

模型限额页为只读展示页，展示支持动态限流的**模型**、当前 **TPM 限流值**与**百炼消费档位**。页面顶部展示当前**生效周期**（如 2026-08-15 ～ 2026-09-15）、**上月消费**（按上月自然月统计，如 8 月 1 日—8 月 31 日）与**本月消费**金额，可通过**查看消费详情**查看消费明细，点击**查看规则**可查看限流档位规则说明。下方表格列出各模型的 TPM 限流档位。

> **说明**
>
> 若 TPM 限流值无法满足业务需求，可联系商务经理申请提额。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7706865871/p1092125.png)

<a id="限流动态调整策略"></a>

<a id="sec-adjust-tier-h2"></a>

### 限流动态调整策略

限流档位按以下规则动态调整：

-   **分档依据**：百炼平台消费金额。
-   **测算周期**：按自然月账单周期测算。
-   **通知**：每月 10 日向调整用户发送通知。
-   **生效时点**：每月 15 日新档位生效，有效期至次月 15 日。
-   **调整方向**：低档→高档（升级）或持平不变。

<a id="静态限流明细"></a>

<a id="model-rate-limits"></a>

## 静态限流明细

以下按模型类别列出各模型的限流值：标注[动态限流](#sec-tier-h2)的模型，其 TPM 限流值随百炼月消费档位调整，参见[模型与限流档位](#sec-tier-h2)；其余模型为静态限流，规则参见[静态限流规则](#static-rate-limit-rules)。

<a id="静态限流规则"></a>

<a id="static-rate-limit-rules"></a>

### 静态限流规则

未纳入动态限流的模型采用静态限流，规则如下：

-   **固定限流值**：每个模型有固定的 RPM 与 TPM 限流值，各模型相互独立。
-   **秒级执行**：限流除按分钟级 RPM/TPM 外，还可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行，短时间内的请求爆发即使未超出分钟级上限也可能触发限流。
-   **触发与恢复**：超出限制时请求被拒绝并返回 429 错误，通常在一分钟内自动恢复，具体错误信息分类参见[为什么触发限流？](#08b8421697cff)与[错误码](../../model-api-reference/preparations/error-code.md)。

<a id="文本生成"></a>

<a id="3392a1d49fftj"></a>

### 文本生成

<a id="千问语言模型"></a>

<a id="ae2b12964a71a"></a>

#### 千问语言模型

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-max-0902</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-flash</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-preview</p></td><td><p>60</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen3.7-max-2026-05-17</p></td><td><p>60</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen-max</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>1,200</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-plus</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.6-flash-2026-04-16</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-plus</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.5-plus-2026-04-20</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-plus-2026-02-15</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen-plus-latest</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>120</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-07-14</p><p>（qwen-plus-0714）</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-plus-2025-04-28</p><p>（qwen-plus-0428）</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-01-25</p><p>（qwen-plus-0125）</p></td><td><p>60</p></td><td><p>150,000</p></td></tr><tr><td><p>qwen3.5-flash</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-flash</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen-flash-2025-07-28</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-long</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>1,200</p></td><td><p>3,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen4-max</p></td><td><p>弗吉尼亚</p></td><td><p>15,000</p></td><td><p>3,000,000</p></td></tr><tr><td><p>qwen3.8-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max</p></td><td><p>美国</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max-0902</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>150,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>2,500,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>美国</p></td><td><p>15,000</p></td><td><p>2,500,000</p></td></tr><tr><td><p>qwen3.7-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.7-max</p></td><td><p>美国</p></td><td><p>30000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>美国</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p></td><td><p>美国</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>全球</p></td><td><p>15000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash-2026-04-16</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p></td><td><p>美国</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.5-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.5-plus-2026-02-15</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen-plus</p></td><td><p>美国</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>美国</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-flash</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen-flash</p></td><td><p>美国</p></td><td><p>30000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen-flash-2025-07-28</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-flash-2025-07-28</p></td><td><p>美国</p></td><td><p>600</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-max</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-max-0902</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.7-max</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-max</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-plus</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash-2026-04-16</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-plus</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.5-plus-2026-04-20</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-plus-2026-02-15</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-latest</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>国际</p></td><td><p>120</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-07-14</p><p>(qwen-plus-0714)</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-plus-2025-04-28</p><p>(qwen-plus-0428)</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-01-25</p><p>(qwen-plus-0125)</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-flash</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-flash</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen-flash-2025-07-28</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max-0902</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>150,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>欧盟</p></td><td><p>15,000</p></td><td><p>250,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>250,000</p></td></tr><tr><td><p>qwen3.7-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash-2026-04-16</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.5-plus-2026-02-15</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus</p></td><td><p>欧盟</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>全球</p></td><td><p>120</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>欧盟</p></td><td><p>120</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-flash</p></td><td><p>全球</p></td><td><p>35,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.5-flash</p></td><td><p>欧盟</p></td><td><p>35,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>欧盟</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-flash</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen-flash-2025-07-28</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max-0902</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>150,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>250,000</p></td></tr><tr><td><p>qwen3.7-max</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-plus</p></td><td><p>日本</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-plus-2026-05-26</p></td><td><p>日本</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-plus</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.6-flash-2026-04-16</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max</p></td><td><p>中国香港</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.8-max-0902</p></td><td><p>中国香港</p></td><td><p>600</p></td><td><p>150,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>中国香港</p></td><td><p>15,000</p></td><td><p>2,500,000</p></td></tr><tr><td><p>qwen3.8-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>2,500,000</p></td></tr><tr><td><p>qwen3.6-plus</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.7-flash-2026-07-15</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3.6-flash</p></td><td><p>全球</p></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen-plus</p></td><td><p>中国香港</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen-plus-2025-12-01</p></td><td><p>中国香港</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-flash</p></td><td><p>中国香港</p></td><td><p>30,000</p></td><td><p>10,000,000</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>中国香港</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="千问vl-视觉理解-图生文"></a>

<a id="590df02870hyp"></a>

#### 千问VL（视觉理解/图生文）

<a id="sec-tabs-3"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-vl-plus</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>3,000</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-vl-plus</p></td><td><p>全球</p></td><td><p>6,000</p></td><td><p>10,000,000</p></td></tr></tbody></table>

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-vl-plus</p></td><td><p>国际</p></td><td><p>1,200</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-vl-plus</p></td><td><p>全球</p></td><td><p>2,000</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3-vl-plus</p></td><td><p>欧盟</p></td><td><p>2,000</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="中国香港-2"></a>

<a id="中国香港-2-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-vl-plus</p></td><td><p>中国香港</p></td><td><p>6,000</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="千问omni"></a>

<a id="5b7c656e788u8"></a>

#### 千问Omni

<a id="sec-tabs-4"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash</p></td><td><p>30000</p></td><td><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.5-omni-plus</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-plus-2026-03-15</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash-2026-03-15</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3-omni-flash</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash</p></td><td><p>国际</p></td><td><p>30000</p></td><td><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.5-omni-plus</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-plus-2026-03-15</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash-2026-03-15</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3-omni-flash</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="中国香港-3"></a>

<a id="中国香港-3-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash</p></td><td><p>全球</p></td><td><p>30000</p></td><td><p>2000000</p></td></tr></tbody></table>

<a id="日本-东京-2"></a>

<a id="日本-东京-2-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash</p></td><td><p>全球</p></td><td><p>30000</p></td><td><p>2000000</p></td></tr></tbody></table>

<a id="德国-法兰克福-3"></a>

<a id="德国-法兰克福-3-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash</p></td><td><p>全球</p></td><td><p>30000</p></td><td><p>2000000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-3"></a>

<a id="美国-弗吉尼亚-3-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash</p></td><td><p>全球</p></td><td><p>30000</p></td><td><p>2000000</p></td></tr></tbody></table>

<a id="千问omni-realtime"></a>

<a id="a410617af4cte"></a>

<a id="realtime-request-counting"></a>

#### 千问Omni-Realtime

通过 WebSocket 接入时，RPM 限制每分钟的建连请求次数。同一连接内的多轮响应不重复计数；重连计为新请求。目前没有单独限制同时保持的连接总数，但仍受 TPM 限制。各型号限额见下方表格。

<a id="sec-tabs-5"></a>

<a id="华北2-北京-5"></a>

<a id="华北2-北京-5-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash-realtime</p></td><td><p>60</p></td><td><p>2,000,000</p></td></tr><tr><td><p>qwen3.5-omni-plus-realtime</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-plus-realtime-2026-03-15</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime-2026-03-15</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3-omni-flash-realtime-2025-09-15</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="新加坡-5"></a>

<a id="新加坡-5-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-omni-flash-realtime</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>2,000,000</p></td></tr><tr><td><p>qwen3.5-omni-plus-realtime</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-plus-realtime-2026-03-15</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime-2026-03-15</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen3-omni-flash-realtime-2025-09-15</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="千问ocr-文字提取"></a>

<a id="9c49551dfbk4r"></a>

#### 千问OCR（文字提取）

<a id="sec-tabs-6"></a>

<a id="华北2-北京-6"></a>

<a id="华北2-北京-6-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.5-ocr</p></td><td><p>6,000</p></td><td><p>30,000,000</p></td></tr><tr><td><p>qwen-vl-ocr</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>600</p></td><td><p>6,000,000</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>6,000</p></td><td><p>30,000,000</p></td></tr><tr><td><p>qwen-vl-ocr-2024-10-28</p></td><td><p>600</p></td><td><p>6,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-4"></a>

<a id="美国-弗吉尼亚-4-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-vl-ocr</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>6,000,000</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>全球</p></td><td><p>1,200</p></td><td><p>6,000,000</p></td></tr></tbody></table>

<a id="新加坡-6"></a>

<a id="新加坡-6-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-vl-ocr</p></td><td><p>国际</p></td><td><p>6,000</p></td><td><p>30,000,000</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>国际</p></td><td><p>6,000</p></td><td><p>30,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-4"></a>

<a id="德国-法兰克福-4-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-vl-ocr</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>6,000,000</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>全球</p></td><td><p>1,200</p></td><td><p>6,000,000</p></td></tr></tbody></table>

<a id="千问audio-音频理解"></a>

<a id="2deeb92f4f8de"></a>

#### 千问Audio（音频理解）

<a id="sec-tabs-7"></a>

<a id="华北2-北京-7"></a>

<a id="华北2-北京-7-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-audio-turbo</p></td><td><p>120</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-turbo-latest</p></td><td><p>60</p></td><td><p>无 TPM 限制</p></td></tr></tbody></table>

<a id="千问coder"></a>

<a id="f7770a0349vq5"></a>

#### 千问Coder

<a id="sec-tabs-8"></a>

<a id="华北2-北京-8"></a>

<a id="华北2-北京-8-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-coder-flash</p></td><td><p>5,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3-coder-flash-2025-07-28</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-5"></a>

<a id="美国-弗吉尼亚-5-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-coder-flash</p></td><td><p>全球</p></td><td><p>1,200</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3-coder-flash-2025-07-28</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="新加坡-7"></a>

<a id="新加坡-7-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-coder-flash</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3-coder-flash-2025-07-28</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-5"></a>

<a id="德国-法兰克福-5-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-coder-flash</p></td><td><p>全球</p></td><td><p>5,000</p></td><td><p>5,000,000</p></td></tr><tr><td><p>qwen3-coder-flash-2025-07-28</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="千问翻译模型"></a>

<a id="19090eae8arxa"></a>

#### 千问翻译模型

<a id="sec-tabs-9"></a>

<a id="华北2-北京-9"></a>

<a id="华北2-北京-9-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-mt-plus</p></td><td><p>60</p></td><td><p>25,000</p></td></tr><tr><td><p>qwen-mt-flash</p></td><td><p>60</p></td><td><p>35,000</p></td></tr><tr><td><p>qwen-mt-lite</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-6"></a>

<a id="美国-弗吉尼亚-6-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-mt-plus</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>25,000</p></td></tr><tr><td><p>qwen-mt-flash</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>35,000</p></td></tr><tr><td><p>qwen-mt-lite</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-mt-lite</p></td><td><p>美国</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="新加坡-8"></a>

<a id="新加坡-8-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-mt-plus</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-mt-flash</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-mt-lite</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-6"></a>

<a id="德国-法兰克福-6-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-mt-plus</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>25,000</p></td></tr><tr><td><p>qwen-mt-flash</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>35,000</p></td></tr><tr><td><p>qwen-mt-lite</p></td><td><p>全球</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="qwen-mt-uni"></a>

<a id="uni-rate-limit"></a>

#### Qwen-MT-Uni

<a id="sec-tabs-10"></a>

<a id="华北2-北京-10"></a>

<a id="华北2-北京-10-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="4"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每分钟调用次数（RPM）</strong></p></th><th><p><strong>每分钟消耗Token数（TPM）</strong></p></th><th><p><strong>异步并发数</strong></p></th><th><p><strong>异步排队数</strong></p></th></tr></thead><tbody><tr><td><p>qwen-mt-uni</p></td><td><p>162</p></td><td><p>2,592,000</p></td><td><p>3</p></td><td><p>500</p></td></tr></tbody></table>

<a id="千问数据挖掘模型"></a>

<a id="9828e02499d55"></a>

#### 千问数据挖掘模型

<a id="sec-tabs-11"></a>

<a id="华北2-北京-11"></a>

<a id="华北2-北京-11-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-doc-turbo</p></td><td><p>600</p></td><td><p>3,000,000</p></td></tr></tbody></table>

<a id="千问深入研究模型"></a>

<a id="9884d121bfy7o"></a>

#### 千问深入研究模型

<a id="sec-tabs-12"></a>

<a id="华北2-北京-12"></a>

<a id="华北2-北京-12-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-deep-research</p></td><td><p>120</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="通义晓蜜对话分析模型"></a>

<a id="cd57449384qjp"></a>

#### 通义晓蜜对话分析模型

<a id="sec-tabs-13"></a>

<a id="华北2-北京-13"></a>

<a id="华北2-北京-13-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>tongyi-xiaomi-analysis-flash</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>tongyi-xiaomi-analysis-pro</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="千问语言模型开源版"></a>

<a id="a1264d06b9yyl"></a>

#### 千问语言模型开源版

<a id="sec-tabs-14"></a>

<a id="华北2-北京-14"></a>

<a id="华北2-北京-14-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-2.4t-a95b</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-27b</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-27b</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-397b-a17b</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-27b</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-35b-a3b</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-7"></a>

<a id="美国-弗吉尼亚-7-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-397b-a17b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-27b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-35b-a3b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="新加坡-9"></a>

<a id="新加坡-9-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-2.4t-a95b</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.8-27b</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.6-27b</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-397b-a17b</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-27b</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-35b-a3b</p></td><td><p>国际</p></td><td><p>600</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-7"></a>

<a id="德国-法兰克福-7-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-397b-a17b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-27b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.5-35b-a3b</p></td><td><p>全球</p></td><td><p>600</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="deepseek"></a>

<a id="f5d967328bgje"></a>

#### DeepSeek

<a id="sec-tabs-15"></a>

<a id="华北2-北京-15"></a>

<a id="华北2-北京-15-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-r1-distill-qwen-1.5b</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>deepseek-r1-distill-llama-70b</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-8"></a>

<a id="美国-弗吉尼亚-8-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>美国</p></td><td><p>10,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>美国</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="新加坡-10"></a>

<a id="新加坡-10-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>国际</p></td><td><p>10,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>国际</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-8"></a>

<a id="德国-法兰克福-8-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="日本-东京-3"></a>

<a id="日本-东京-3-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4-pro</p></td><td><p>日本</p></td><td><p>10,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>日本</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>日本</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4.1-flash-1017</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro</p></td><td><p>全球</p></td><td><p>10,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="中国香港-4"></a>

<a id="中国香港-4-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p></td><td><p>中国香港</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4.1-flash</p></td><td><p>中国香港</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p></td><td><p>中国香港</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p></td><td><p>中国香港</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="deepseek-硅基流动直供"></a>

<a id="8981b276d2fab"></a>

#### DeepSeek-硅基流动直供

<a id="sec-tabs-16"></a>

<a id="华北2-北京-16"></a>

<a id="华北2-北京-16-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>siliconflow/deepseek-v3.2</p></td><td><p>500</p></td><td><p>500,000</p></td></tr><tr><td><p>siliconflow/deepseek-v3.1-terminus</p></td><td><p>500</p></td><td><p>500,000</p></td></tr><tr><td><p>siliconflow/deepseek-r1-0528</p></td><td><p>500</p></td><td><p>500,000</p></td></tr><tr><td><p>siliconflow/deepseek-v3-0324</p></td><td><p>500</p></td><td><p>500,000</p></td></tr></tbody></table>

<a id="deepseek-快手万擎直供"></a>

<a id="vanchin-deepseek-ratelimit-title"></a>

#### DeepSeek-快手万擎直供

<a id="sec-tabs-17"></a>

<a id="华北2-北京-17"></a>

<a id="华北2-北京-17-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>vanchin/deepseek-v3.2-think</p></td><td><p>30</p></td><td><p>600,000</p></td></tr><tr><td><p>vanchin/deepseek-v3.1-terminus</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>vanchin/deepseek-r1</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>vanchin/deepseek-v3</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>vanchin/deepseek-ocr</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>vanchin/deepseek-v4-pro</p></td><td><p>60</p></td><td><p>300,000</p></td></tr><tr><td><p>vanchin/deepseek-v4-pro-0813</p></td><td><p>30</p></td><td><p>600,000</p></td></tr><tr><td><p>vanchin/deepseek-v4.1-flash</p></td><td><p>30</p></td><td><p>600,000</p></td></tr></tbody></table>

<a id="kimi"></a>

<a id="a9ee85ed0emvu"></a>

#### Kimi

<a id="sec-tabs-18"></a>

<a id="华北2-北京-18"></a>

<a id="华北2-北京-18-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>15,000</p></td><td><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>kimi-k3.1-pro-prime</p></td><td><p>15,000</p></td><td><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>kimi-k3</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>kimi-k2.7-code</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>kimi-k2.6</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>kimi-k2.5</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-9"></a>

<a id="美国-弗吉尼亚-9-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>kimi-k3</p><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>美国</p></td><td colspan="2"><p>限流值以所选业务空间的实际配置为准。</p></td></tr><tr><td><p>kimi-k3</p></td><td><p>国际</p></td><td><p>10,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>kimi-k2.7-code</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>kimi-k2.5</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-9"></a>

<a id="德国-法兰克福-9-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>kimi-k3</p><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>kimi-k2.7-code</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>kimi-k2.5</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="日本-东京-4"></a>

<a id="日本-东京-4-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>kimi-k3</p><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>kimi-k2.7-code</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>kimi-k2.5</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="新加坡-11"></a>

<a id="新加坡-11-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>国际</p></td><td><p>10,000</p></td><td><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>kimi-k3.1-pro-prime</p></td><td><p>国际</p></td><td><p>10,000</p></td><td><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>kimi-k3</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>kimi-k2.7-code</p></td><td><p>国际</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="中国香港-5"></a>

<a id="中国香港-5-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>kimi-k3</p><p><a href="model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>kimi-k2.7-code</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="kimi-月之暗面直供"></a>

<a id="4c5e80ec70q4z"></a>

#### Kimi-月之暗面直供

<a id="sec-tabs-19"></a>

<a id="华北2-北京-19"></a>

<a id="华北2-北京-19-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>kimi/kimi-k3.1-pro-highspeed</p></td><td rowspan="7"><p>500</p><blockquote><p>同一个阿里云百炼API Key 下，在 7 个模型中共享 500 RPM 限流配额。即这 7 个模型的每分钟请求总数加起来不能超过 500。</p></blockquote></td><td rowspan="7"><p>3,000,000</p><blockquote><p>同一个阿里云百炼API Key 下，在 7 个模型中共享 3000000 TPM 限流配额。即这 7 个模型的每分钟 Token 消耗总数加起来不能超过 3000000。</p></blockquote></td></tr><tr><td><p>kimi/kimi-k3.1-pro</p></td></tr><tr><td><p>kimi/kimi-k3</p></td></tr><tr><td><p>kimi/kimi-k2.7-code-highspeed</p></td></tr><tr><td><p>kimi/kimi-k2.7-code</p></td></tr><tr><td><p>kimi/kimi-k2.6</p></td></tr><tr><td><p>kimi/kimi-k2.5</p></td></tr></tbody></table>

<a id="glm"></a>

<a id="c66e2c68c1w9s"></a>

#### GLM

<a id="sec-tabs-20"></a>

<a id="华北2-北京-20"></a>

<a id="华北2-北京-20-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>glm-5.2</p></td><td><p>500</p></td><td><p>2,000,000</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>glm-5</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-10"></a>

<a id="美国-弗吉尼亚-10-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>glm-5.3</p></td><td><p>美国</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>美国</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-10"></a>

<a id="德国-法兰克福-10-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="日本-东京-5"></a>

<a id="日本-东京-5-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>全球</p></td><td><p>15,000</p></td><td><p>1,200,000</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="新加坡-12"></a>

<a id="新加坡-12-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>国际</p></td><td colspan="2"><p><a href="#sec-tier-h2">动态限流</a></p></td></tr><tr><td><p>glm-5.2</p></td><td><p>国际</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>国际</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="中国香港-6"></a>

<a id="中国香港-6-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.2</p></td><td><p>全球</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="glm-智谱直供"></a>

<a id="cb01c6d8c8zxp"></a>

#### GLM-智谱直供

<a id="sec-tabs-21"></a>

<a id="华北2-北京-21"></a>

<a id="华北2-北京-21-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>ZHIPU/GLM-5.3</p></td><td><p>200</p></td><td><p>3,000,000</p></td></tr><tr><td><p>ZHIPU/GLM-5.3-Flash</p></td><td><p>200</p></td><td><p>3,000,000</p></td></tr><tr><td><p>ZHIPU/GLM-5.3-FlashX</p></td><td><p>200</p></td><td><p>3,000,000</p></td></tr><tr><td><p>ZHIPU/GLM-5.2</p></td><td><p>200</p></td><td><p>3,000,000</p></td></tr><tr><td><p>ZHIPU/GLM-5.1</p></td><td><p>200</p></td><td><p>3,000,000</p></td></tr><tr><td><p>ZHIPU/GLM-5</p></td><td><p>200</p></td><td><p>3,000,000</p></td></tr></tbody></table>

<a id="minimax"></a>

<a id="cf86f6b6a7cku"></a>

#### MiniMax

<a id="sec-tabs-22"></a>

<a id="华北2-北京-22"></a>

<a id="华北2-北京-22-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>MiniMax-M2.5</p></td><td><p>500</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="minimax-稀宇科技直供"></a>

<a id="d92c3ff8f4tw1"></a>

#### MiniMax-稀宇科技直供

<a id="sec-tabs-23"></a>

<a id="华北2-北京-23"></a>

<a id="华北2-北京-23-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>MiniMax/MiniMax-M3.1-Flash</p></td><td><p>200</p></td><td><p>10,000,000</p></td></tr><tr><td><p>MiniMax/MiniMax-M3</p></td><td><p>500</p></td><td><p>20,000,000</p></td></tr><tr><td><p>MiniMax/MiniMax-M2.7</p></td><td><p>500</p></td><td><p>20,000,000</p></td></tr><tr><td><p>MiniMax/MiniMax-M2.5</p></td><td><p>500</p></td><td><p>20,000,000</p></td></tr><tr><td><p>MiniMax/MiniMax-M2.1</p></td><td><p>500</p></td><td><p>20,000,000</p></td></tr></tbody></table>

<a id="mimo-小米直供"></a>

<a id="54b32ee55e7zu"></a>

#### MiMo-小米直供

<a id="sec-tabs-24"></a>

<a id="华北2-北京-24"></a>

<a id="华北2-北京-24-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>xiaomi/mimo-v2.6-pro-ultraspeed</p></td><td><p>100</p></td><td><p>5,000,000</p></td></tr><tr><td><p>xiaomi/mimo-v2.5-pro</p></td><td><p>100</p></td><td><p>10,000,000</p></td></tr></tbody></table>

<a id="stepfun-阶跃星辰直供"></a>

<a id="sf_ratelimit_h3"></a>

#### Stepfun-阶跃星辰直供

<a id="sec-tabs-25"></a>

<a id="华北2-北京-25"></a>

<a id="华北2-北京-25-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>stepfun/step-3.7-flash</p></td><td><p>500</p></td><td><p>20,000,000</p></td></tr><tr><td><p>stepfun/step-5-preview</p></td><td><p>500</p></td><td><p>10,000,000</p></td></tr></tbody></table>

<a id="unisound-云知声直供"></a>

#### Unisound-云知声直供

<a id="sec-tabs-26"></a>

<a id="华北2-北京-26"></a>

<a id="华北2-北京-26-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>unisound/unisound-u2</p></td><td><p>300</p></td><td><p>3,000,000</p></td></tr></tbody></table>

<a id="ling-蚂蚁数科直供"></a>

#### Ling-蚂蚁数科直供

<a id="sec-tabs-27"></a>

<a id="华北2-北京-27"></a>

<a id="华北2-北京-27-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>antdigital/Ling-3.1-flash</p></td><td><p>300</p></td><td><p>10,000,000</p></td></tr></tbody></table>

<a id="图像生成"></a>

<a id="5998fd159df49"></a>

### 图像生成

<a id="千问-qwen-image"></a>

<a id="f812e7c63axvx"></a>

#### 千问（Qwen-Image）

<a id="sec-tabs-28"></a>

<a id="华北2-北京-28"></a>

<a id="华北2-北京-28-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口调用限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>5 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>120 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.0-pro</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-06-22</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-04-22</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-03-03</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0</p></td><td><p>2 次/秒</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-2026-03-03</p></td><td><p>2 次/秒</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-mt-image-2.0</p></td><td><p>60 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 2</p></td></tr><tr><td><p>qwen-mt-image</p></td><td><p>1 次/秒</p></td><td><p>同步接口无限制 / 异步接口 2</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-11"></a>

<a id="美国-弗吉尼亚-11-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口调用限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>全球</p></td><td><p>5 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>全球</p></td><td><p>120 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr></tbody></table>

<a id="新加坡-13"></a>

<a id="新加坡-13-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口调用限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>国际</p></td><td><p>5 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>国际</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>国际</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>国际</p></td><td><p>120 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.0-pro</p></td><td><p>国际</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-06-22</p></td><td><p>国际</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-04-22</p></td><td><p>国际</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-03-03</p></td><td><p>国际</p></td><td><p>2 次/分钟</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0</p></td><td><p>国际</p></td><td><p>2 次/秒</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-image-2.0-2026-03-03</p></td><td><p>国际</p></td><td><p>2 次/秒</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>qwen-mt-image-2.0</p></td><td><p>国际</p></td><td><p>60 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 2</p></td></tr></tbody></table>

<a id="德国-法兰克福-11"></a>

<a id="德国-法兰克福-11-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口调用限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>全球</p></td><td><p>5 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>全球</p></td><td><p>120 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr></tbody></table>

<a id="日本-东京-6"></a>

<a id="日本-东京-6-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口调用限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>全球</p></td><td><p>5 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>全球</p></td><td><p>120 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr></tbody></table>

<a id="中国香港-7"></a>

<a id="中国香港-7-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口调用限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>全球</p></td><td><p>5 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>全球</p></td><td><p>20 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>全球</p></td><td><p>120 次/分钟</p></td><td><p>同步接口无限制 / 异步接口 10</p></td></tr></tbody></table>

<a id="文生图-z-image"></a>

<a id="e17ad85fd8wwl"></a>

#### 文生图-Z-Image

<a id="sec-tabs-29"></a>

<a id="华北2-北京-29"></a>

<a id="华北2-北京-29-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>z-image-turbo</p></td><td><p>2</p></td><td><p>同步接口无限制</p></td></tr></tbody></table>

<a id="新加坡-14"></a>

<a id="新加坡-14-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>z-image-turbo</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>同步接口无限制</p></td></tr></tbody></table>

<a id="万相"></a>

<a id="513e0a3df24v7"></a>

#### 万相

<a id="sec-tabs-30"></a>

<a id="华北2-北京-30"></a>

<a id="华北2-北京-30-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.7-image-pro</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-image</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-image</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-t2i</p></td><td><p>1</p></td><td><p>5</p></td></tr><tr><td><p>wan2.5-t2i-preview</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-t2i-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.2-t2i-flash</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-t2i-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-t2i-turbo</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.0-t2i-turbo</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.5-i2i-preview</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wanx2.1-imageedit</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx-v1</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>wanx-x-painting</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>wanx-sketch-to-image-lite</p></td><td><p>2</p></td><td><p>1</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-12"></a>

<a id="美国-弗吉尼亚-12-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.6-t2i</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-image</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="新加坡-15"></a>

<a id="新加坡-15-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.7-image-pro</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-image</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-image</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-t2i</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.5-t2i-preview</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-t2i-flash</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.2-t2i-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-t2i-turbo</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-t2i-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.5-i2i-preview</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="德国-法兰克福-12"></a>

<a id="德国-法兰克福-12-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.6-t2i</p></td><td><p>全球</p></td><td><p>1</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-image</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="图像编辑与生成"></a>

<a id="980e34f881ihz"></a>

#### 图像编辑与生成

<a id="sec-tabs-31"></a>

<a id="华北2-北京-31"></a>

<a id="华北2-北京-31-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>shoemodel-v1</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>wanx-virtualmodel</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>wanx-style-repaint-v1</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx-poster-generation-v1</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>virtualmodel-v2</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>image-instance-segmentation</p></td><td><p>2</p></td><td><p>1</p></td></tr><tr><td><p>image-erase-completion</p></td><td><p>2</p></td><td><p>1</p></td></tr></tbody></table>

<a id="人物写真生成-facechain"></a>

<a id="88756e5f858dv"></a>

#### 人物写真生成-FaceChain

<a id="sec-tabs-32"></a>

<a id="华北2-北京-32"></a>

<a id="华北2-北京-32-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量</strong></p></th></tr></thead><tbody><tr><td><p>facechain-facedetect</p></td><td><p>5</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>facechain-finetune</p></td><td><p>1</p></td><td><p>1</p></td></tr></tbody></table>

<a id="可灵系列"></a>

<a id="fdd6e348d2md4"></a>

#### 可灵系列

<a id="sec-tabs-33"></a>

<a id="华北2-北京-33"></a>

<a id="华北2-北京-33-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每秒钟调用次数（RPS）</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>kling/kling-v3-omni-image-generation</p></td><td rowspan="2"><p>5</p></td><td rowspan="2"><p>10</p><blockquote><p>同一阿里云百炼API Key 下，可灵系列的 7 个模型（<a href="rate-limit.md#fdd6e348d2md4">图像</a>及<a href="rate-limit.md#kling-third-party-title">视频</a>）共享 10 个并发数。即这 7 个模型处于运行状态的任务总数加起来不能超过 10 个。</p></blockquote></td></tr><tr><td><p>kling/kling-v3-image-generation</p></td></tr></tbody></table>

<a id="vidu系列"></a>

<a id="vidu-img-third-party-title"></a>

#### Vidu系列

<a id="sec-tabs-34"></a>

<a id="华北2-北京-34"></a>

<a id="华北2-北京-34-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每分钟请求数RPM限制</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>vidu/viduq3.1-fast_reference2image</p></td><td rowspan="7"><p>300</p></td><td rowspan="7"><p>5</p><blockquote><p>同一个阿里云百炼API Key 下，Vidu参考生图系列的模型共享 5 个并发数。即所有模型处于运行状态的任务总数加起来不能超过 5 个。</p></blockquote></td></tr><tr><td><p>vidu/vidu-image-lite_reference2image</p></td></tr><tr><td><p>vidu/vidu-image_reference2image</p></td></tr><tr><td><p>vidu/viduq3-fast_reference2image</p></td></tr><tr><td><p>vidu/viduq2-pro_reference2image</p></td></tr><tr><td><p>vidu/viduq2-fast_reference2image</p></td></tr><tr><td><p>vidu/vidu-image-pro_reference2image</p></td></tr></tbody></table>

<a id="语音识别"></a>

<a id="speech-recognition-rate-limit"></a>

<a id="55945fd2b5bbf"></a>

<a id="语音"></a>

### 语音识别

<a id="qwen-audio-asr"></a>

<a id="8e353130f9pmp"></a>

#### Qwen-Audio-ASR

<a id="sec-tabs-35"></a>

<a id="华北2-北京-35"></a>

<a id="华北2-北京-35-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-asr-flash | 600 |
| qwen-audio-3.0-asr-flash | 600 |

<a id="新加坡-16"></a>

<a id="新加坡-16-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen-audio-3.1-asr-flash | 国际 | 600 |
| qwen-audio-3.0-asr-flash | 国际 | 600 |

<a id="qwen-audio-asr-streaming"></a>

<a id="6314d076aabhs"></a>

#### Qwen-Audio-ASR-Streaming

<a id="sec-tabs-36"></a>

<a id="华北2-北京-36"></a>

<a id="华北2-北京-36-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-asr-flash-streaming</p></td><td rowspan="2"><p>1200</p></td></tr><tr><td><p>qwen-audio-3.0-asr-flash-streaming</p></td></tr></tbody></table>

<a id="新加坡-17"></a>

<a id="新加坡-17-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-asr-flash-streaming</p></td><td><p>国际</p></td><td rowspan="2"><p>1200</p></td></tr><tr><td><p>qwen-audio-3.0-asr-flash-streaming</p></td><td><p>国际</p></td></tr></tbody></table>

<a id="qwen-audio-asr-filetrans"></a>

<a id="29376bdaa5s47"></a>

#### Qwen-Audio-ASR-Filetrans

<a id="sec-tabs-37"></a>

<a id="华北2-北京-37"></a>

<a id="华北2-北京-37-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-asr-flash-filetrans | 600 |
| qwen-audio-3.0-asr-flash-filetrans | 600 |

<a id="新加坡-18"></a>

<a id="新加坡-18-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen-audio-3.1-asr-flash-filetrans | 国际 | 600 |
| qwen-audio-3.0-asr-flash-filetrans | 国际 | 600 |

<a id="qwen-audio-asr-message"></a>

<a id="asr-message"></a>

#### Qwen-Audio-ASR-Message

<a id="sec-tabs-38"></a>

<a id="华北2-北京-38"></a>

<a id="华北2-北京-38-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-asr-flash-message | 1200 |

<a id="新加坡-19"></a>

<a id="新加坡-19-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen-audio-3.1-asr-flash-message | 国际 | 1200 |

<a id="qwen3-asr"></a>

<a id="7d2f0509a3n03"></a>

#### Qwen3-ASR

<a id="sec-tabs-39"></a>

<a id="华北2-北京-39"></a>

<a id="华北2-北京-39-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-40"></a>

<a id="qwen3-asr-flash-filetrans"></a>

<a id="qwen3-asr-flash-filetrans-h4"></a>

#### Qwen3-ASR-Flash-Filetrans

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash-filetrans</p></td><td rowspan="2"><p>100</p></td></tr></tbody></table>

<a id="qwen3-asr-flash"></a>

<a id="qwen3-asr-flash-h4"></a>

#### Qwen3-ASR-Flash

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash</p></td><td rowspan="3"><p>100</p></td></tr></tbody></table>

<a id="新加坡-20"></a>

<a id="新加坡-20-h4"></a>

#### 新加坡

<a id="sec-tabs-41"></a>

<a id="qwen3-asr-flash-filetrans-2"></a>

<a id="qwen3-asr-flash-filetrans-2-h4"></a>

#### Qwen3-ASR-Flash-Filetrans

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash-filetrans</p></td><td><p>国际</p></td><td rowspan="2"><p>100</p></td></tr></tbody></table>

<a id="qwen3-asr-flash-2"></a>

<a id="qwen3-asr-flash-2-h4"></a>

#### Qwen3-ASR-Flash

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash</p></td><td><p>国际</p></td><td rowspan="3"><p>100</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-13"></a>

<a id="美国-弗吉尼亚-13-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash</p></td><td><p>美国</p></td><td rowspan="2"><p>100</p></td></tr></tbody></table>

<a id="qwen3-asr-realtime"></a>

<a id="9f21be56e82vj"></a>

#### Qwen3-ASR-Realtime

<a id="sec-tabs-42"></a>

<a id="华北2-北京-40"></a>

<a id="华北2-北京-40-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash-realtime</p></td><td rowspan="3"><p>20</p></td></tr></tbody></table>

<a id="新加坡-21"></a>

<a id="新加坡-21-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash-realtime</p></td><td><p>国际</p></td><td rowspan="3"><p>20</p></td></tr></tbody></table>

<a id="fun-asr"></a>

<a id="8c50a9f1e526h"></a>

#### Fun-ASR

<a id="sec-tabs-43"></a>

<a id="华北2-北京-41"></a>

<a id="华北2-北京-41-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每分钟调用次数（RPM）</strong></p></th></tr></thead><tbody><tr><td><p>fun-asr</p></td><td rowspan="6"><p>600</p></td></tr><tr><td><p>fun-asr-flash-2026-06-15</p></td></tr></tbody></table>

<a id="新加坡-22"></a>

<a id="新加坡-22-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| fun-asr | 国际 | 600 |
| fun-asr-flash-2026-06-15 | 国际 | 600 |

<a id="fun-asr-realtime"></a>

<a id="c9c9419f7btw4"></a>

#### Fun-ASR-Realtime

<a id="sec-tabs-44"></a>

<a id="华北2-北京-42"></a>

<a id="华北2-北京-42-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>fun-asr-realtime</p></td><td rowspan="6"><p>20</p></td></tr><tr><td><p>fun-asr-realtime-2026-02-28</p></td></tr><tr><td><p>fun-asr-flash-8k-realtime</p></td></tr><tr><td><p>fun-asr-flash-8k-realtime-2026-01-28</p></td></tr></tbody></table>

<a id="新加坡-23"></a>

<a id="新加坡-23-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>fun-asr-realtime</p></td><td><p>国际</p></td><td rowspan="2"><p>20</p></td></tr></tbody></table>

<a id="paraformer"></a>

<a id="71c5d28fb01yz"></a>

#### Paraformer

<a id="sec-tabs-45"></a>

<a id="华北2-北京-43"></a>

<a id="华北2-北京-43-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>paraformer-realtime-v2</p></td><td rowspan="4"><p>20</p></td></tr><tr><td><p>paraformer-realtime-8k-v2</p></td></tr></tbody></table>

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| paraformer-v2 | 1,200 |

| 模型名称 | 每秒钟调用次数（RPS） | 同时处理中任务数量（并发数） |
| --- | --- | --- |
| paraformer-8k-v2 | 20 | 100 |

<a id="语音合成"></a>

<a id="speech-synthesis-rate-limit"></a>

### 语音合成

<a id="qwen-audio-tts"></a>

<a id="79352135767l3"></a>

#### Qwen-Audio-TTS

<a id="sec-tabs-46"></a>

<a id="华北2-北京-44"></a>

<a id="华北2-北京-44-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-tts-plus | 180 |
| qwen-audio-3.1-tts-flash | 180 |
| qwen-audio-3.0-tts-plus | 180 |
| qwen-audio-3.0-tts-flash | 180 |

<a id="新加坡-24"></a>

<a id="新加坡-24-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen-audio-3.1-tts-plus | 国际 | 180 |
| qwen-audio-3.1-tts-flash | 国际 | 180 |
| qwen-audio-3.0-tts-plus | 国际 | 180 |
| qwen-audio-3.0-tts-flash | 国际 | 180 |

<a id="cosyvoice"></a>

<a id="95cc317401h9u"></a>

#### CosyVoice

<a id="sec-tabs-47"></a>

<a id="华北2-北京-45"></a>

<a id="华北2-北京-45-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>cosyvoice-v3.5-plus</p></td><td rowspan="6"><p>3</p></td></tr><tr><td><p>cosyvoice-v3.5-flash</p></td></tr><tr><td><p>cosyvoice-v3-plus</p></td></tr><tr><td><p>cosyvoice-v3-flash</p></td></tr><tr><td><p>cosyvoice-v2</p></td></tr></tbody></table>

<a id="新加坡-25"></a>

<a id="新加坡-25-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>每秒钟调用次数（RPS）</strong></p></th></tr></thead><tbody><tr><td><p>cosyvoice-v3-plus</p></td><td><p>国际</p></td><td rowspan="2"><p>3</p></td></tr><tr><td><p>cosyvoice-v3-flash</p></td><td><p>国际</p></td></tr></tbody></table>

<a id="minimax-稀宇科技直供-2"></a>

<a id="7ba64ebc288nj"></a>

#### MiniMax-稀宇科技直供

<a id="sec-tabs-48"></a>

<a id="华北2-北京-46"></a>

<a id="华北2-北京-46-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗字符数</strong><blockquote><strong>仅含输入字符数</strong></blockquote></th></tr></thead><tbody><tr><td><p>MiniMax/speech-2.8-hd</p></td><td><p>20</p></td><td><p>20,000</p></td></tr><tr><td><p>MiniMax/speech-02-hd</p></td><td><p>20</p></td><td><p>20,000</p></td></tr><tr><td><p>MiniMax/speech-2.8-turbo</p></td><td><p>20</p></td><td><p>20,000</p></td></tr><tr><td><p>MiniMax/speech-02-turbo</p></td><td><p>20</p></td><td><p>20,000</p></td></tr></tbody></table>

<a id="qwen3-tts"></a>

<a id="476158da2fwdl"></a>

#### Qwen3-TTS

<a id="sec-tabs-49"></a>

<a id="华北2-北京-47"></a>

<a id="华北2-北京-47-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-50"></a>

<a id="qwen3-tts-flash"></a>

<a id="qwen3-tts-flash-h4"></a>

#### Qwen3-TTS-Flash

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen3-tts-flash | 180 |

<a id="新加坡-26"></a>

<a id="新加坡-26-h4"></a>

#### 新加坡

<a id="sec-tabs-51"></a>

<a id="qwen3-tts-flash-2"></a>

<a id="qwen3-tts-flash-2-h4"></a>

#### Qwen3-TTS-Flash

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen3-tts-flash | 国际 | 180 |

<a id="qwen3-tts-realtime"></a>

<a id="0deabef960pq1"></a>

#### Qwen3-TTS-Realtime

<a id="sec-tabs-52"></a>

<a id="华北2-北京-48"></a>

<a id="华北2-北京-48-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-53"></a>

<a id="qwen3-tts-flash-realtime"></a>

<a id="qwen3-tts-flash-realtime-h4"></a>

#### Qwen3-TTS-Flash-Realtime

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen3-tts-flash-realtime | 180 |

<a id="新加坡-27"></a>

<a id="新加坡-27-h4"></a>

#### 新加坡

<a id="sec-tabs-54"></a>

<a id="qwen3-tts-flash-realtime-2"></a>

<a id="qwen3-tts-flash-realtime-2-h4"></a>

#### Qwen3-TTS-Flash-Realtime

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen3-tts-flash-realtime | 国际 | 180 |

<a id="sambert"></a>

<a id="3f9ff5ba2b5tt"></a>

#### Sambert

<a id="sec-tabs-55"></a>

<a id="华北2-北京-49"></a>

<a id="华北2-北京-49-h4"></a>

#### 华北2（北京）

| 模型服务 | 每秒钟调用次数（RPS） |
| --- | --- |
| Sambert系列模型 | 20 |

<a id="音频打标"></a>

<a id="audio-tagging-rate-limit"></a>

### 音频打标

<a id="qwen-audio-3-1-captioner"></a>

<a id="captioner-rate-limit"></a>

#### Qwen-Audio-3.1-Captioner

<a id="sec-tabs-56"></a>

<a id="华北2-北京-50"></a>

<a id="华北2-北京-50-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-captioner | 600 |

<a id="音频生成"></a>

<a id="audio-generation-rate-limit"></a>

<a id="音频与音乐生成"></a>

### 音频生成

<a id="qwen-audio-tts-next"></a>

<a id="qwen-audio-tts-next-rate-limit"></a>

#### Qwen-Audio-TTS-Next

<a id="sec-tabs-57"></a>

<a id="华北2-北京-51"></a>

<a id="华北2-北京-51-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-tts-next | 180 |

<a id="新加坡-28"></a>

<a id="新加坡-28-h4"></a>

#### 新加坡

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-audio-3.1-tts-next | 180 |

<a id="语音对话"></a>

<a id="speech-dialogue-rate-limit"></a>

### 语音对话

<a id="qwen-audio-live"></a>

<a id="qwen-audio-live-rate-limit"></a>

#### Qwen-Audio-Live

WebSocket 最多同时保持 5 条连接。

<a id="qwen-audio-realtime"></a>

<a id="739e085c10fxx"></a>

<a id="实时语音对话"></a>

#### Qwen-Audio-Realtime

通过 WebSocket 接入时，RPM 限制每分钟的建连请求次数。同一连接内的多轮响应不重复计数；重连计为新请求。目前没有单独限制同时保持的连接总数，但仍受 TPM 限制。各型号限额见下方表格。

<a id="sec-tabs-58"></a>

<a id="华北2-北京-52"></a>

<a id="华北2-北京-52-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-realtime-plus</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-3.1-realtime-flash</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-plus</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-flash</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="新加坡-29"></a>

<a id="新加坡-29-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-realtime-plus</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-3.1-realtime-flash</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-plus</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-flash</p></td><td><p>国际</p></td><td><p>60</p></td><td><p>100,000</p></td></tr></tbody></table>

<a id="音视频翻译"></a>

<a id="audio-video-translation-rate-limit"></a>

### 音视频翻译

<a id="qwen3-livetranslate-flash"></a>

<a id="4be13d2d4a3r9"></a>

#### Qwen3-LiveTranslate-Flash

<a id="sec-tabs-59"></a>

<a id="华北2-北京-53"></a>

<a id="华北2-北京-53-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-livetranslate-flash</p></td><td rowspan="2"><p>100</p></td><td rowspan="2"><p>100,000</p></td></tr><tr><td><p>qwen3-livetranslate-flash-2025-12-01</p></td></tr></tbody></table>

<a id="新加坡-30"></a>

<a id="新加坡-30-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-livetranslate-flash</p></td><td><p>国际</p></td><td rowspan="2"><p>100</p></td><td rowspan="2"><p>100,000</p></td></tr><tr><td><p>qwen3-livetranslate-flash-2025-12-01</p></td><td><p>国际</p></td></tr></tbody></table>

<a id="qwen-livetranslate-flash-realtime"></a>

<a id="ea64133a8buvv"></a>

#### Qwen-LiveTranslate-Flash-Realtime

通过 WebSocket 接入时，RPM 限制每分钟的建连请求次数。同一连接内的多轮响应不重复计数；重连计为新请求。目前没有单独限制同时保持的连接总数，但仍受 TPM 限制。各型号限额见下方表格。

<a id="sec-tabs-60"></a>

<a id="华北2-北京-54"></a>

<a id="华北2-北京-54-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-livetranslate-flash-realtime</p></td><td rowspan="5"><p>10</p></td><td rowspan="5"><p>100,000</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime-2026-05-19</p></td></tr></tbody></table>

<a id="新加坡-31"></a>

<a id="新加坡-31-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-livetranslate-flash-realtime</p></td><td><p>国际</p></td><td rowspan="5"><p>10</p></td><td rowspan="5"><p>100,000</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime</p></td><td><p>国际</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime-2026-05-19</p></td><td><p>国际</p></td></tr></tbody></table>

<a id="音色复刻-设计"></a>

<a id="voice-enrollment-rate-limit"></a>

### 音色复刻/设计

<a id="qwen-audio-tts-cosyvoice声音复刻-设计"></a>

<a id="86517f838d10u"></a>

#### Qwen-Audio-TTS/CosyVoice声音复刻/设计

Qwen-Audio-TTS/CosyVoice声音复刻/设计共用一个模型，共用限流额度。

<a id="sec-tabs-61"></a>

<a id="华北2-北京-55"></a>

<a id="华北2-北京-55-h4"></a>

#### 华北2（北京）

| 模型名称 | 每秒钟调用次数（RPS） |
| --- | --- |
| voice-enrollment | 10 |

<a id="新加坡-32"></a>

<a id="新加坡-32-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每秒钟调用次数（RPS） |
| --- | --- | --- |
| voice-enrollment | 国际 | 10 |

<a id="qwen3-tts声音复刻"></a>

<a id="f4de4b96c09v6"></a>

#### Qwen3-TTS声音复刻

<a id="sec-tabs-62"></a>

<a id="华北2-北京-56"></a>

<a id="华北2-北京-56-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| qwen-voice-enrollment | 180 |

<a id="新加坡-33"></a>

<a id="新加坡-33-h4"></a>

#### 新加坡

| 模型名称 | 服务部署范围 | 每分钟调用次数（RPM） |
| --- | --- | --- |
| qwen-voice-enrollment | 国际 | 180 |

<a id="音乐生成"></a>

<a id="music-generation-rate-limit"></a>

### 音乐生成

<a id="fun-music"></a>

<a id="fun-music-rate-limit"></a>

#### Fun-Music

<a id="sec-tabs-63"></a>

<a id="华北2-北京-57"></a>

<a id="华北2-北京-57-h4"></a>

#### 华北2（北京）

| 模型名称 | 每分钟调用次数（RPM） |
| --- | --- |
| fun-music-preview | 180 |
| fun-music-v1 | 180 |

<a id="视频生成"></a>

<a id="d809366847gza"></a>

### 视频生成

<a id="happyhorse系列"></a>

<a id="hh-third-party-title"></a>

#### HappyHorse系列

<a id="sec-tabs-64"></a>

<a id="华北2-北京-58"></a>

<a id="华北2-北京-58-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>happyhorse-1.1-t2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-i2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-r2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-t2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-i2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-r2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-video-edit</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-14"></a>

<a id="美国-弗吉尼亚-14-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>happyhorse-1.1-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-video-edit</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="新加坡-34"></a>

<a id="新加坡-34-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>happyhorse-1.1-t2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-i2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-r2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-t2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-i2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-r2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-video-edit</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="德国-法兰克福-13"></a>

<a id="德国-法兰克福-13-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>happyhorse-1.1-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-video-edit</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="日本-东京-7"></a>

<a id="日本-东京-7-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流值（任何一个值超出即触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>正在处理中的任务数（并发）</strong></p></th></tr></thead><tbody><tr><td><p>happyhorse-1.1-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.1-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>happyhorse-1.0-video-edit</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="万相系列"></a>

<a id="018a73300efzz"></a>

#### 万相系列

> **说明**
>
> `wan3.0-video` 和 `wan3.0-video-prime` 的限流值请前往[百炼控制台模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)，切换至实际调用地域并查看对应模型详情。

<a id="sec-tabs-65"></a>

<a id="华北2-北京-59"></a>

<a id="华北2-北京-59-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.7-r2v-2026-06-12</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-t2v-2026-06-12</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-t2v-2026-04-25</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-t2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-t2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.5-t2v-preview</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-t2v-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-t2v-turbo</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-t2v-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.7-i2v-2026-04-25</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-i2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v-flash</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.5-i2v-preview</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-i2v-flash</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.2-i2v-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-i2v-turbo</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-i2v-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.2-kf2v-flash</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-kf2v-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wanx2.1-vace-plus</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.7-videoedit</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-r2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-r2v-flash</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-r2v</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-s2v-detect</p></td><td><p>5</p></td><td><p>同步接口无限制</p></td></tr><tr><td><p>wan2.2-s2v</p></td><td><p>5</p></td><td><p>1</p></td></tr><tr><td><p>wan2.2-animate-move</p></td><td><p>5</p></td><td><p>1</p></td></tr><tr><td><p>wan2.2-animate-mix</p></td><td><p>5</p></td><td><p>1</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-15"></a>

<a id="美国-弗吉尼亚-15-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.7-r2v-2026-06-12</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-t2v</p></td><td><p>美国</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v</p></td><td><p>美国</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="新加坡-35"></a>

<a id="新加坡-35-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.7-t2v-2026-06-12</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-t2v-2026-04-25</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-t2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-t2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.5-t2v-preview</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-t2v-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-t2v-turbo</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-t2v-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.7-i2v-2026-04-25</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-i2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v-flash</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.5-i2v-preview</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-i2v-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-i2v-turbo</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-i2v-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-kf2v-plus</p></td><td><p>国际</p></td><td><p>1</p></td><td><p>2</p></td></tr><tr><td><p>wan2.1-vace-plus</p></td><td><p>国际</p></td><td><p>2</p></td><td><p>2</p></td></tr><tr><td><p>wan2.7-videoedit</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.7-r2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-r2v-flash</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-r2v</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.2-animate-move</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>1</p></td></tr><tr><td><p>wan2.2-animate-mix</p></td><td><p>国际</p></td><td><p>5</p></td><td><p>1</p></td></tr></tbody></table>

<a id="德国-法兰克福-14"></a>

<a id="德国-法兰克福-14-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每秒钟调用次数（RPS）</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>wan2.6-t2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-i2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr><tr><td><p>wan2.6-r2v</p></td><td><p>全球</p></td><td><p>5</p></td><td><p>5</p></td></tr></tbody></table>

<a id="舞动人像animateanyone"></a>

<a id="02e62576072f0"></a>

#### 舞动人像AnimateAnyone

<a id="sec-tabs-66"></a>

<a id="华北2-北京-60"></a>

<a id="华北2-北京-60-h4"></a>

#### 华北2（北京）

| 模型名称 | 每秒钟调用次数（RPS） | 同时处理中任务数量 |
| --- | --- | --- |
| animate-anyone-detect | 5 | 1算力单元支持2并发 |
| animate-anyone | 5 | 1算力单元支持1并发 |

<a id="声动人像videoretalk"></a>

<a id="4bb36ecec8el3"></a>

#### 声动人像VideoRetalk

<a id="sec-tabs-67"></a>

<a id="华北2-北京-61"></a>

<a id="华北2-北京-61-h4"></a>

#### 华北2（北京）

| 模型名称 | 每秒钟调用次数（RPS） | 同时处理中任务数量 |
| --- | --- | --- |
| videoretalk | 1 | 1<br><br>在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

<a id="视频风格重绘"></a>

<a id="101f9ad4210ev"></a>

#### 视频风格重绘

<a id="sec-tabs-68"></a>

<a id="华北2-北京-62"></a>

<a id="华北2-北京-62-h4"></a>

#### 华北2（北京）

| 模型名称 | 每秒钟调用次数（RPS） | 同时处理中任务数量 |
| --- | --- | --- |
| video-style-transform | 20 | 2<br><br>在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

<a id="爱诗系列"></a>

<a id="d64654d0f0rfx"></a>

#### 爱诗系列

<a id="sec-tabs-69"></a>

<a id="华北2-北京-63"></a>

<a id="华北2-北京-63-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每分钟任务下发接口RPM限制</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>pixverse/pixverse-lipsync</p></td><td><p>300</p></td><td rowspan="3"><p>5</p><blockquote><p>同一个阿里云百炼API Key 下，这 3 个模型共享 5 个并发数。即这 3 个模型处于运行状态的任务总数加起来不能超过 5 个。</p></blockquote></td></tr><tr><td><p>pixverse/pixverse-motioncontrol</p></td><td><p>300</p></td></tr><tr><td><p>pixverse/pixverse-upscale</p></td><td><p>300</p></td></tr></tbody></table>

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每分钟请求数（RPM）</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>pixverse/pixverse-c1-t2v</p></td><td rowspan="4"><p>300</p></td><td rowspan="4"><p>5</p><blockquote><p>同一个阿里云百炼API Key 下，这 4 个模型共享 5 个并发数。即这 4 个模型处于运行状态的任务总数加起来不能超过 5 个。</p></blockquote></td></tr><tr><td><p>pixverse/pixverse-c1-it2v</p></td></tr><tr><td><p>pixverse/pixverse-c1-kf2v</p></td></tr><tr><td><p>pixverse/pixverse-c1-r2v</p></td></tr><tr><td><p>pixverse/pixverse-v6-r2v-omni</p></td><td rowspan="7"><p>300</p></td><td rowspan="7"><p>5</p><blockquote><p>同一个阿里云百炼API Key 下，这 7 个模型共享 5 个并发数。即这 7 个模型处于运行状态的任务总数加起来不能超过 5 个。</p></blockquote></td></tr><tr><td><p>pixverse/pixverse-v6-max-t2v</p></td></tr><tr><td><p>pixverse/pixverse-v6-max-it2v</p></td></tr><tr><td><p>pixverse/pixverse-v6-t2v</p></td></tr><tr><td><p>pixverse/pixverse-v6-it2v</p></td></tr><tr><td><p>pixverse/pixverse-v6-kf2v</p></td></tr><tr><td><p>pixverse/pixverse-v6-r2v</p></td></tr><tr><td><p>pixverse/pixverse-v5.6-t2v</p></td><td rowspan="4"><p>300</p></td><td rowspan="4"><p>5</p><blockquote><p>同一个阿里云百炼API Key 下，这 4 个模型共享 5 个并发数。即这 4 个模型处于运行状态的任务总数加起来不能超过 5 个。</p></blockquote></td></tr><tr><td><p>pixverse/pixverse-v5.6-it2v</p></td></tr><tr><td><p>pixverse/pixverse-v5.6-kf2v</p></td></tr><tr><td><p>pixverse/pixverse-v5.6-r2v</p></td></tr></tbody></table>

<a id="可灵系列-2"></a>

<a id="kling-third-party-title"></a>

#### 可灵系列

<a id="sec-tabs-70"></a>

<a id="华北2-北京-64"></a>

<a id="华北2-北京-64-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每秒钟调用次数（RPS）</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>kling/kling-v3-omni-video-generation</p></td><td rowspan="5"><p>5</p></td><td rowspan="5"><p>10</p><blockquote><p>同一阿里云百炼API Key 下，可灵系列的 7 个模型（<a href="rate-limit.md#fdd6e348d2md4">图像</a>及<a href="rate-limit.md#kling-third-party-title">视频</a>）共享 10 个并发数。即这 7 个模型处于运行状态的任务总数加起来不能超过 10 个。</p></blockquote></td></tr><tr><td><p>kling/kling-v3-turbo-video-generation</p></td></tr><tr><td><p>kling/kling-v3-video-generation</p></td></tr><tr><td><p>kling/kling-v4-video-generation</p></td></tr><tr><td><p>kling/kling-v4-omni-reference-video-generation</p></td></tr></tbody></table>

<a id="vidu系列-2"></a>

<a id="vidu-third-party-title"></a>

#### Vidu系列

<a id="sec-tabs-71"></a>

<a id="华北2-北京-65"></a>

<a id="华北2-北京-65-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每秒钟调用次数（RPS）</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>vidu/viduq3-ad_reference2video</p></td><td><p>5</p></td><td rowspan="20"><p>5</p><blockquote><p>同一个阿里云百炼API Key 在 20 个模型间共享并发额度。即这 20 个模型处于运行状态的任务总数加起来不能超过 5 个。</p></blockquote></td></tr><tr><td><p>vidu/viduq3-drama_reference2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-pro-fast_img2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-turbo_text2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-pro_text2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2_text2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-turbo_img2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-pro_img2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2-turbo_img2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2-pro_img2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2-pro-fast_img2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-turbo_start-end2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-pro_start-end2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2-turbo_start-end2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2-pro_start-end2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-mix_reference2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3_reference2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq3-turbo_reference2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2-pro_reference2video</p></td><td><p>5</p></td></tr><tr><td><p>vidu/viduq2_reference2video</p></td><td><p>5</p></td></tr></tbody></table>

<a id="minimax系列"></a>

<a id="minimax-h3-video-title"></a>

#### MiniMax系列

<a id="sec-tabs-72"></a>

<a id="华北2-北京-66"></a>

<a id="华北2-北京-66-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>每分钟任务下发接口RPM限制</strong></p></th><th><p><strong>同时处理中任务数量（并发数）</strong></p></th></tr></thead><tbody><tr><td><p>MiniMax/MiniMax-H3</p></td><td><p>300</p></td><td><p>5</p></td></tr></tbody></table>

<a id="3d模型生成"></a>

<a id="0b7e66f09e7lj"></a>

### 3D模型生成

<a id="tripo系列"></a>

<a id="tripo-third-party-title"></a>

#### Tripo系列

<a id="sec-tabs-73"></a>

<a id="华北2-北京-67"></a>

<a id="华北2-北京-67-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每分钟任务下发接口RPM限制</strong></th><th><strong>同时处理中任务数量（并发数）</strong></th></tr></thead><tbody><tr><td><p>Tripo/Tripo-H3.1</p></td><td><p>300</p></td><td><p>10</p></td></tr><tr><td><p>Tripo/Tripo-P1.0</p></td><td><p>300</p></td><td><p>5</p></td></tr><tr><td><p>Tripo/Tripo-ImageToSplat</p></td><td><p>300</p></td><td><p>5</p></td></tr><tr><td><p>Tripo/Tripo-AutoRig</p></td><td><p>300</p></td><td rowspan="3"><p>10</p><blockquote><p>自动绑骨、绑骨前检查、动画重定向共享同一并发额度，三个模型处于运行状态的任务总数不能超过 10 个。</p></blockquote></td></tr><tr><td><p>Tripo/Tripo-RigCheck</p></td><td><p>300</p></td></tr><tr><td><p>Tripo/Tripo-AnimationRetarget</p></td><td><p>300</p></td></tr><tr><td><p>Tripo/Tripo-Texture</p></td><td><p>300</p></td><td rowspan="2"><p>5</p><blockquote><p>贴图、格式转换共享同一并发额度，两个模型处于运行状态的任务总数不能超过 5 个。</p></blockquote></td></tr><tr><td><p>Tripo/Tripo-ConvertFormat</p></td><td><p>300</p></td></tr><tr><td><p>Tripo/Tripo-Segmentation</p></td><td><p>300</p></td><td rowspan="4"><p>10</p><blockquote><p>分割、智能分割、网格补全、重拓扑共享同一并发额度，四个模型处于运行状态的任务总数不能超过 10 个。</p></blockquote></td></tr><tr><td><p>Tripo/Tripo-SmartSegmentation</p></td><td><p>300</p></td></tr><tr><td><p>Tripo/Tripo-MeshCompletion</p></td><td><p>300</p></td></tr><tr><td><p>Tripo/Tripo-Retopology</p></td><td><p>300</p></td></tr></tbody></table>

<a id="向量与排序模型"></a>

<a id="68ae4e7d1ehra"></a>

### 向量与排序模型

<a id="文本向量"></a>

<a id="953ddcd76495l"></a>

#### 文本向量

<a id="sec-tabs-74"></a>

<a id="华北2-北京-68"></a>

<a id="华北2-北京-68-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）/作业数</strong><blockquote><strong>仅输入Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>24,000</p></td><td><p>1,000,000</p></td></tr><tr><td><p>qwen3.7-text-embedding-flash</p></td><td><p>24,000</p></td><td><p>1,000,000</p></td></tr><tr><td><p>text-embedding-v1</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>1,800</p></td><td><p>1,200,000</p></td></tr><tr><td><p>text-embedding-v2</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>1,800</p></td><td><p>1,200,000</p></td></tr><tr><td><p>text-embedding-v3</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>1,800</p></td><td><p>1,200,000</p></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p>用<a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch API</a>调用服务时，不受限流限制。</p></blockquote></td><td><p>1,800</p></td><td><p>1,200,000</p></td></tr><tr><td><p>text-embedding-async-v1</p></td><td><p>60</p></td><td><p>当前用户在系统通用文本向量异步作业排队中和运行中的作业数量不超过50个。</p><p>另外，为了避免大量突发的作业占据太多资源，限制并发的作业数为3个，即任意时间，单个用户最多只有3个通用文本向量的异步作业在并发运行，其他的作业只能在队列中等待。</p></td></tr><tr><td><p>text-embedding-async-v2</p></td><td><p>60</p></td><td><p>当前用户在系统通用文本向量异步作业排队中和运行中的作业数量不超过50个。</p><p>另外，为了避免大量突发的作业占据太多资源，限制并发的作业数为3个，即任意时间，单个用户最多只有3个通用文本向量的异步作业在并发运行，其他的作业只能在队列中等待。</p></td></tr></tbody></table>

<a id="新加坡-36"></a>

<a id="新加坡-36-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>国际</p></td><td><p>24,000</p></td><td><p>1,000,000</p></td></tr><tr><td><p>text-embedding-v4</p></td><td><p>国际</p></td><td><p>1,800</p></td><td><p>1,000,000</p></td></tr><tr><td><p>text-embedding-v3</p></td><td><p>国际</p></td><td><p>6,000</p></td><td><p>24,000,000</p></td></tr></tbody></table>

<a id="中国香港-8"></a>

<a id="中国香港-8-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>text-embedding-v4</p></td><td><p>中国香港</p></td><td><p>1,800</p></td><td><p>1,200,000</p></td></tr></tbody></table>

<a id="多模态向量"></a>

<a id="d59f78d5c18y5"></a>

#### 多模态向量

<a id="sec-tabs-75"></a>

<a id="华北2-北京-69"></a>

<a id="华北2-北京-69-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>仅输入Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-vl-embedding</p></td><td><p>2,400</p></td><td><p>1,200,000</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>1,200</p></td><td><p>600,000</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>600</p></td><td><p>200,000</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>600</p></td><td><p>200,000</p></td></tr><tr><td><p>tongyi-embedding-vision-flash-2026-03-06</p></td><td><p>1,200</p></td><td><p>9,600,000</p></td></tr><tr><td><p>tongyi-embedding-vision-plus-2026-03-06</p></td><td><p>1,200</p></td><td><p>9,600,000</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>120</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="排序模型"></a>

<a id="1b5bd6eddbdau"></a>

#### 排序模型

<a id="sec-tabs-76"></a>

<a id="华北2-北京-70"></a>

<a id="华北2-北京-70-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.7-text-rerank</p></td><td><p>3,000</p></td><td><p>9,000,000</p></td></tr><tr><td><p>qwen3-rerank</p></td><td><p>5,400</p></td><td><p>5,000,000,000</p></td></tr><tr><td><p>qwen3-vl-rerank</p></td><td><p>600</p></td><td><p>9,000,000</p></td></tr><tr><td><p>gte-rerank-v2</p></td><td><p>5,040</p></td><td><p>4,980,000,000</p></td></tr></tbody></table>

<a id="新加坡-37"></a>

<a id="新加坡-37-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-rerank</p></td><td><p>国际</p></td><td><p>5,400</p></td><td><p>5,000,000,000</p></td></tr><tr><td><p>gte-rerank-v2</p></td><td><p>国际</p></td><td><p>5,040</p></td><td><p>4,980,000,000</p></td></tr></tbody></table>

<a id="行业"></a>

<a id="e6785f7240c8r"></a>

### 行业

<a id="意图理解"></a>

<a id="3921a60f269e3"></a>

#### 意图理解

<a id="sec-tabs-77"></a>

<a id="华北2-北京-71"></a>

<a id="华北2-北京-71-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>tongyi-intent-detect-v3</p></td><td><p>1,200</p></td><td><p>1,000,000</p></td></tr></tbody></table>

<a id="角色扮演"></a>

<a id="86e73ce5885wo"></a>

#### 角色扮演

<a id="sec-tabs-78"></a>

<a id="华北2-北京-72"></a>

<a id="华北2-北京-72-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-plus-character</p></td><td><p>120</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen-flash-character</p></td><td><p>120</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen-flash-character-2026-02-26</p></td><td><p>120</p></td><td><p>500,000</p></td></tr></tbody></table>

<a id="新加坡-38"></a>

<a id="新加坡-38-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-plus-character</p></td><td><p>国际</p></td><td><p>120</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen-flash-character</p></td><td><p>国际</p></td><td><p>120</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen-plus-character-ja</p></td><td><p>国际</p></td><td><p>120</p></td><td><p>500,000</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-16"></a>

<a id="美国-弗吉尼亚-16-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-plus-character</p></td><td><p>全球</p></td><td><p>120</p></td><td><p>500,000</p></td></tr><tr><td><p>qwen-flash-character</p></td><td><p>全球</p></td><td><p>120</p></td><td><p>500,000</p></td></tr></tbody></table>

<a id="德国-法兰克福-15"></a>

<a id="德国-法兰克福-15-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-plus-character</p></td><td><p>全球</p></td><td><p>120</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="日本-东京-8"></a>

<a id="日本-东京-8-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen-plus-character</p></td><td><p>全球</p></td><td><p>120</p></td><td><p>5,000,000</p></td></tr></tbody></table>

<a id="界面交互"></a>

<a id="2c80cf1f06pw2"></a>

#### 界面交互

<a id="sec-tabs-79"></a>

<a id="华北2-北京-73"></a>

<a id="华北2-北京-73-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>gui-plus</p></td><td><p>80</p></td><td><p>540,000</p></td></tr><tr><td><p>gui-plus-2026-02-26</p></td><td><p>100</p></td><td><p>540,000</p></td></tr></tbody></table>

<a id="决策模型"></a>

<a id="dm-ratelimit"></a>

#### 决策模型

<a id="sec-tabs-80"></a>

<a id="华北2-北京-74"></a>

<a id="华北2-北京-74-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>decision-model-preview</p></td><td><p>1,200</p></td><td><p>2,000,000</p></td></tr></tbody></table>

<a id="新加坡-39"></a>

<a id="新加坡-39-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th colspan="2"><strong>限流条件（超出任一数值时触发限流）</strong><blockquote><strong>以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制</strong></blockquote></th></tr><tr><th><strong>每分钟调用次数（RPM）</strong></th><th><strong>每分钟消耗Token数（TPM）</strong><blockquote><strong>含输入与输出Token</strong></blockquote></th></tr></thead><tbody><tr><td><p>decision-model-preview</p></td><td><p>1,200</p></td><td><p>2,000,000</p></td></tr></tbody></table>

<a id="已下线模型"></a>

<a id="14dd0e482478d"></a>

### 已下线模型

详细信息，请参见 [模型下线机制说明](../../product-updates/release-notes/model-depreciation.md) 。

<a id="faq"></a>

<a id="d1688da3e3egs"></a>

## FAQ

<a id="为什么触发限流"></a>

<a id="08b8421697cff"></a>

### 为什么触发限流？

根据错误信息判断触发了哪类限流：

-   `Requests rate limit exceeded` 或 `You exceeded your current requests list`：触发了每分钟请求数（RPM）限流。
-   `Allocated quota exceeded` 或 `You exceeded your current quota`：触发了每分钟 Token 消耗（TPM）限流。
-   `Request rate increased too quickly`：请求频率在短时间内激增，触发了系统稳定性保护——即使总调用量未达到 RPM 或 TPM 上限也会触发。
-   `Too many requests.`（错误码为 Throttling.ResourceExhausted 或 Throttling.ServiceOverloaded）：动态限流模型的保护性拒绝，由平台资源不足导致，并非超出限流值；被拒绝的请求不计费，稍后重试即可。参见[动态限流机制](#sec-mechanism-h2)，支持的模型见[模型与限流档位](#sec-tier-h2)。
-   其他报错，参见[错误码](../../model-api-reference/preparations/error-code.md)确认原因。

短时间内的请求爆发即使未超出分钟级上限也可能触发限流，秒级执行口径参见[静态限流规则](#static-rate-limit-rules)。

<a id="如何查看模型调用量"></a>

<a id="2c4544e8d8wy6"></a>

### 如何查看模型调用量？

模型调用发生后**分钟级**即可在监控图表查看。登录模型监控页面（[北京](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry)），在左侧导航栏选择**运维管理** > **模型监控**进入监控概览页，设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**查看详情**，即可查看该模型的调用统计结果。具体请参见[监控告警](../model-monitoring/model-telemetry.md)文档。

> 监控数据按分钟级更新，仅供参考，不作为计费依据。

<a id="遇到限流后多久恢复"></a>

<a id="45e83f5504b7t"></a>

### 遇到限流后多久恢复？

每分钟请求数（RPM）或每分钟 Token 消耗（TPM）类限流通常在一分钟内恢复；动态限流的保护性拒绝（`Too many requests.`）取决于平台资源状况，无固定恢复时长，稍后重试即可。如出现其他报错，参见[错误码](../../model-api-reference/preparations/error-code.md)进行处理。

<a id="模型响应速度与付费有关吗"></a>

<a id="faq-speed-paid-h"></a>

### 模型响应速度与付费有关吗？

模型输出速度与是否付费无关。免费额度和付费调用使用相同的模型服务基础设施，同一模型的生成速度相同。免费额度仅控制请求是否被接受——额度耗尽时返回 403 错误（开通**免费额度用完即停**后），不会降低已接受请求的生成速度。

<a id="什么因素影响模型响应速度"></a>

<a id="faq-speed-factors-h"></a>

### 什么因素影响模型响应速度？

-   **模型类型**：轻量模型（如 qwen-flash）比大型模型（如 qwen-max）生成更快。
-   **输出长度**：输出 Token 越多，总耗时越长。
-   **服务器负载**：高峰期可能略有波动。

<a id="限流会降低已接受请求的生成速度吗"></a>

<a id="faq-rate-limit-speed-h"></a>

### 限流会降低已接受请求的生成速度吗？

不会。限流（RPM/TPM）仅导致超出限制的请求被拒绝（返回 429 错误）。免费额度耗尽时（开通**免费额度用完即停**）返回 403 错误，同样不影响已接受请求的速度。429 为速率限制，403 为配额耗尽，两者均为拒绝机制。

<a id="如何避免限流"></a>

<a id="0e4e875b9c2eg"></a>

### 如何避免限流？

1.  **选用高限流模型**
    -   优先使用 [qwen-plus](models.md) 等限流额度更高的模型。
    -   稳定版或最新版比带日期的快照版本限流更宽松。
2.  **优化调用策略**
    -   **降低调用频率**：收到 `Requests rate limit exceeded` 或 `You exceeded your current requests list` 时，降低API调用频率。
    -   **减少 Token 消耗**：收到 `Allocated quota exceeded` 或 `You exceeded your current quota` 时，缩短输入或限制输出长度。
    -   **平滑请求速率**：收到 `Request rate increased too quickly` 时，采用匀速调度、指数退避或请求队列将请求均匀分散，避免瞬时高峰。
3.  **添加备选模型**
    
    触发限流后切换到备用模型继续生成，可降低失败概率、提升吞吐量。以下代码在调用 `qwen-plus` 触发限流后，自动改用 `qwen-flash` 重试。也可以选择不同系列的模型（如 qwen-flash）作为备选模型，进一步降低主备模型同时限流的风险。
    
    <a id="accordion-示例代码"></a>
    
    示例代码
    
    <a id="code-block"></a>
    
    ```python
    import os
    import asyncio
    from openai import AsyncOpenAI, APIStatusError
    
    # 配置
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    # 主用模型
    MODEL = "qwen-plus"
    # 备选模型
    BACKUP_MODEL = "qwen-flash"
    # 测试问题
    QUESTION = "你是谁？"
    # 并发设置
    NUM_REQUESTS = 10
    
    client = AsyncOpenAI(
        api_key=API_KEY,
        # 以下为华北2（北京）地域的URL，请将WorkspaceId替换为真实的业务空间ID。
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    )
    
    async def send_request(model):
        """发送单个请求"""
        try:
            await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": QUESTION}]
            )
            return True
        except APIStatusError as e:
            if e.status_code == 429:
                print(f"[限流触发] 模型 {model}")
                return False
            raise
        except Exception as e:
            print(f"[请求失败] 模型 {model}，错误：{e}")
            return False
    
    async def task(i):
        # 尝试主模型
        if await send_request(MODEL):
            return True
        # 限流时尝试备用模型
        return await send_request(BACKUP_MODEL)
    
    async def main():
        results = await asyncio.gather(*(task(i) for i in range(NUM_REQUESTS)))
        print(f"成功请求: {sum(results)}, 失败请求: {len(results) - sum(results)}")
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    
4.  **拆分任务**：长对话或大型文档会快速消耗大量 Token。将大批量任务拆分为小批次，分时段提交。
    
5.  **批量推理**：无需实时响应时，使用[批量推理](../model-high-speed-inference/batch-inference.md)（Batch API）。批量请求不受实时限流约束，但需考虑排队和处理时间。
    

<a id="如何控制-token-用量或费用支出"></a>

<a id="faq_cost_ctrl_h3"></a>

### 如何控制 Token 用量或费用支出？

限流仅约束单位时间内的调用速率，不限制累计用量。如需控制 Token 用量或费用支出，可通过以下方式管理：

-   **设置消费限额与费用告警**：在**账单费用**卡片设置**费用告警**，开启月度消费限额并配置阈值通知，达到阈值即提醒，避免超额支出。详见[账单查询与成本管理](../test-1/bill-query-and-cost-management.md)。
-   **开启免费额度用完即停**：对支持免费额度的模型，可开启**免费额度用完即停**，免费额度耗尽后自动停止调用，避免产生额外费用。详见[新人免费额度](../test-1/new-free-quota.md)。
-   **监控模型调用量**：定期查看各模型的 Token 用量，及时发现异常增长，参见上文[如何查看模型调用量？](rate-limit.md#2c4544e8d8wy6)。

<a id="充值后是否还会被限流"></a>

<a id="faq_recharge_limit_h3"></a>

### 充值后是否还会被限流？

充值不改变静态限流模型的 RPM 和 TPM 限流阈值。限流按阿里云主账号维度配置，与计费相互独立；充值（按量付费）仅确保账号不因欠费停服，不会提升静态限流值。采用[动态限流](#sec-mechanism-h2)的模型，TPM 限流档位随百炼月消费金额自动调整，消费提升后档位可随之升级，调整规则参见[限流动态调整策略](#sec-adjust-tier-h2)。

如需更高的限流额度，请联系商务经理申请。

# 模型调用价格

模型调用默认 按量计费 ，涵盖各类模型的计费规则与价格。

> **说明**
>
> 本文仅展示模型调用**原价**，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

> **说明**
>
> 部分模型支持**上下文缓存**（显式缓存、隐式缓存）。缓存命中的输入 Token 及创建显式缓存的 Token 采用与标准输入不同的计费单价（例如显式缓存创建按标准输入单价的 125% 计费、命中按 10% 计费），本文价格表中的输入单价**不含**缓存单价。缓存的计费规则、单价折扣及支持的模型请参见[上下文缓存](../model-experience/text-generation-model/context-cache.md)。

<a id="阶梯计费规则"></a>

<a id="d3be061317ozi"></a>

## 阶梯计费规则

百炼部分模型实行阶梯计费。单价取决于单次请求的输入 Token 总量。该请求的所有 Token 均按对应阶梯的单价结算。

计费区间中的 K 表示 1,000，M 表示 1,000,000。例如，128K 即 128,000 Token，256K 即 256,000 Token，1M 即 1,000,000 Token。

例如，某模型设有两档计费区间：0 < Token ≤ 32K 和 32K < Token ≤ 128K。若输入 100K Token，因数值落在第二区间（32K < 100K ≤ 128K），所有 Token 均按第二档单价结算。

<a id="文本生成-千问"></a>

<a id="e90fd1458c2vm"></a>

## 文本生成-千问

<a id="千问max"></a>

<a id="c3741fefddnzj"></a>

### 千问Max

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](../model-experience/text-generation-model/context-cache.md)，仅输入Token享有折扣。两者不能同时生效。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen4-max</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10元</p></td><td><p>30元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.8-max-0902</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-20</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.7-max-preview</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-17</p></blockquote></td><td><p>仅思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.7-max-2026-05-17</p></td><td><p>仅思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="b6081e6455dlr"></a>

##### 更多模型

| 模型 ID（Model ID） | 模式 | 单次请求的输入Token数 | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- | --- | --- |
| qwen-max | 仅非思考模式 | 无阶梯计价 | 2.4元 | 9.6元 | 无 |

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10元</p></td><td><p>30元</p></td></tr><tr><td><p>qwen4-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>弗吉尼亚</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10.938元</p></td><td><p>32.813元</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>美国</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>14.988元</p></td><td><p>44.965元</p></td></tr><tr><td><p>qwen3.8-max-0902</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-20</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>美国</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>18.736元</p></td><td><p>56.207元</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10.938元</p></td><td><p>32.813元</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>14.988元</p></td><td><p>44.965元</p></td></tr><tr><td><p>qwen3.8-max-0902</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>14.988元</p></td><td><p>44.965元</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-20</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>18.736元</p></td><td><p>56.207元</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>18.736元</p></td><td><p>56.207元</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>18.736元</p></td><td><p>56.207元</p></td></tr></tbody></table>

<a id="daed670d87gnw"></a>

##### 更多模型

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th></tr></thead><tbody><tr><td><p>qwen-max</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>国际</p></td><td><p>仅非思考模式</p></td><td><p>无阶梯计价</p></td><td><p>11.743元</p></td><td><p>46.971元</p></td></tr></tbody></table>

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10元</p></td><td><p>30元</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.8-max-0902</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-20</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr></tbody></table>

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10元</p></td><td><p>30元</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.8-max-0902</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-20</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr></tbody></table>

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen4-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>10元</p></td><td><p>30元</p></td></tr><tr><td><p>qwen3.8-max</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.8-max-0902</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max</p><blockquote><p>当前能力等同于qwen3.7-max-2026-05-20</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max-2026-06-08</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr><tr><td><p>qwen3.7-max-2026-05-20</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td></tr></tbody></table>

<a id="千问plus"></a>

<a id="baa85ffef6dyz"></a>

### 千问Plus

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>单次请求的输入Token范围</strong></th><th rowspan="2"><strong>输入单价（每百万Token）</strong></th><th colspan="2"><strong>输出单价（每百万Token）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr><tr><th><strong>非思考模式</strong></th><th><strong>思考模式（思维链+回答）</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td><td rowspan="2"><p>100万Token</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价6元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>8元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>6元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus</p><blockquote><p>当前能力等同于qwen3.6-plus-2026-04-02</p></blockquote></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus-2026-04-02</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus</p><blockquote><p>当前能力等同于qwen3.5-plus-2026-02-15</p></blockquote></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus-2026-04-20</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus-2026-02-15</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen-plus</p><blockquote><p>当前能力等同于qwen-plus-2025-12-01</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td rowspan="3"><p>qwen-plus-latest</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td rowspan="3"><p>qwen-plus-2025-12-01</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td><p>qwen-plus-2025-07-14</p></td><td><p>无阶梯计价</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>无</p></td></tr><tr><td><p>qwen-plus-2025-04-28</p></td><td><p>无阶梯计价</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="da994de49eky6"></a>

##### 更多模型

| 模型 ID（Model ID） | 单次请求的输入Token范围 | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- | --- |
| qwen-plus-2025-01-25 | 无阶梯计价 | 0.8元 | 2元 | 无 |
| qwen-plus-2025-01-12 | 无阶梯计价 | 0.8元 | 2元 | 100万Token |
| qwen-plus-2024-12-20 | 无阶梯计价 | 0.8元 | 2元 | 100万Token |

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th rowspan="2"><strong>单次请求的输入Token范围</strong></th><th rowspan="2"><strong>输入单价 （每百万Token）</strong></th><th colspan="2"><strong>输出单价 （每百万Token）</strong></th></tr><tr><th><strong>非思考模式</strong></th><th><strong>思考模式（思维链+回答）</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价6元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>美国</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2.998元<strong>（限时8折）</strong></p></td><td><p>原价11.991元<strong>（限时8折）</strong></p></td><td><p>原价11.991元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价8.993元<strong>（限时8折）</strong></p></td><td><p>原价35.972元<strong>（限时8折）</strong></p></td><td><p>原价35.972元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>6元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus</p><blockquote><p>当前能力等同于qwen3.6-plus-2026-04-02</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus-2026-04-02</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus</p><blockquote><p>当前能力等同于qwen3.5-plus-2026-02-15</p></blockquote></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus-2026-02-15</p></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen-plus</p><blockquote><p>当前能力等同于qwen-plus-2025-12-01</p></blockquote></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td rowspan="2"><p>qwen-plus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>美国</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.807元</p></td><td><p>26.421元</p></td><td><p>88.071元</p></td></tr><tr><td rowspan="3"><p>qwen-plus-2025-12-01</p></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td rowspan="2"><p>qwen-plus-2025-12-01</p></td><td rowspan="2"><p>美国</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.807元</p></td><td><p>26.421元</p></td><td><p>88.071元</p></td></tr></tbody></table>

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th rowspan="2"><strong>单次请求的输入Token范围</strong></th><th rowspan="2"><strong>输入单价 （每百万Token）</strong></th><th colspan="2"><strong>输出单价 （每百万Token）</strong></th></tr><tr><th><strong>非思考模式</strong></th><th><strong>思考模式（思维链+回答）</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2.998元<strong>（限时8折）</strong></p></td><td><p>原价11.991元<strong>（限时8折）</strong></p></td><td><p>原价11.991元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价8.993元<strong>（限时8折）</strong></p></td><td><p>原价35.972元<strong>（限时8折）</strong></p></td><td><p>原价35.972元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.998元</p></td><td><p>11.991元</p></td><td><p>11.991元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.993元</p></td><td><p>35.972元</p></td><td><p>35.972元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus</p><blockquote><p>当前能力等同于qwen3.6-plus-2026-04-02</p></blockquote></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>3.7471元</p></td><td><p>22.4826元</p></td><td><p>22.4826元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>14.9884元</p></td><td><p>44.965元</p></td><td><p>44.965元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus-2026-04-02</p></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>3.7471元</p></td><td><p>22.4826元</p></td><td><p>22.4826元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>14.9884元</p></td><td><p>44.965元</p></td><td><p>44.965元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-plus</p><blockquote><p>当前能力等同于qwen3.5-plus-2026-02-15</p></blockquote></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>17.614元</p></td><td><p>17.614元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>3.67元</p></td><td><p>22.018元</p></td><td><p>22.018元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-plus-2026-04-20</p></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>17.614元</p></td><td><p>17.614元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>3.67元</p></td><td><p>22.018元</p></td><td><p>22.018元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-plus-2026-02-15</p></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>17.614元</p></td><td><p>17.614元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>3.67元</p></td><td><p>22.018元</p></td><td><p>22.018元</p></td></tr><tr><td rowspan="2"><p>qwen-plus</p><blockquote><p>当前能力等同于qwen-plus-2025-12-01</p></blockquote></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.807元</p></td><td><p>26.421元</p></td><td><p>88.071元</p></td></tr><tr><td rowspan="2"><p>qwen-plus-latest</p></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.807元</p></td><td><p>26.421元</p></td><td><p>88.071元</p></td></tr><tr><td rowspan="2"><p>qwen-plus-2025-12-01</p></td><td rowspan="2"><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.807元</p></td><td><p>26.421元</p></td><td><p>88.071元</p></td></tr><tr><td><p>qwen-plus-2025-07-14</p></td><td><p>国际</p></td><td><p>无阶梯计价</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr><tr><td><p>qwen-plus-2025-04-28</p></td><td><p>国际</p></td><td><p>无阶梯计价</p></td><td><p>2.936元</p></td><td><p>8.807元</p></td><td><p>29.357元</p></td></tr></tbody></table>

<a id="062fa750c1rwu"></a>

##### 更多模型

| 模型 ID（Model ID） | 服务部署范围 | 单次请求的输入Token范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- | --- |
| qwen-plus-2025-01-25 | 国际 | 无阶梯计价 | 2.936元 | 8.807元 |

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th rowspan="2"><strong>单次请求的输入Token范围</strong></th><th rowspan="2"><strong>输入单价 （每百万Token）</strong></th><th colspan="2"><strong>输出单价 （每百万Token）</strong></th></tr><tr><th><strong>非思考模式</strong></th><th><strong>思考模式（思维链+回答）</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价6元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>6元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus</p><blockquote><p>当前能力等同于qwen3.6-plus-2026-04-02</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus-2026-04-02</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus</p><blockquote><p>当前能力等同于qwen3.5-plus-2026-02-15</p></blockquote></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-plus-2026-02-15</p></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="3"><p>qwen-plus</p><blockquote><p>当前能力等同于qwen-plus-2025-12-01</p></blockquote></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td rowspan="2"><p>qwen-plus</p><blockquote><p>当前能力等同于qwen-plus-2025-12-01</p></blockquote></td><td rowspan="2"><p>欧盟</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.998元</p></td><td><p>8.993元</p></td><td><p>29.977元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.993元</p></td><td><p>26.979元</p></td><td><p>89.93元</p></td></tr><tr><td rowspan="3"><p>qwen-plus-2025-12-01</p></td><td rowspan="3"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.4元</p></td><td><p>20元</p></td><td><p>24元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>48元</p></td><td><p>64元</p></td></tr><tr><td rowspan="2"><p>qwen-plus-2025-12-01</p></td><td rowspan="2"><p>欧盟</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.998元</p></td><td><p>8.993元</p></td><td><p>29.977元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.993元</p></td><td><p>26.979元</p></td><td><p>89.93元</p></td></tr></tbody></table>

<a id="日本-东京-2"></a>

<a id="日本-东京-2-h4"></a>

#### 日本（东京）

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th rowspan="2"><strong>单次请求的输入Token范围</strong></th><th rowspan="2"><strong>输入单价 （每百万Token）</strong></th><th colspan="2"><strong>输出单价 （每百万Token）</strong></th></tr><tr><th><strong>非思考模式</strong></th><th><strong>思考模式（思维链+回答）</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>日本</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2.998元<strong>（限时8折）</strong></p></td><td><p>原价11.991元<strong>（限时8折）</strong></p></td><td><p>原价11.991元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价8.993元<strong>（限时8折）</strong></p></td><td><p>原价35.972元<strong>（限时8折）</strong></p></td><td><p>原价35.972元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>日本</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.998元</p></td><td><p>11.991元</p></td><td><p>11.991元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.993元</p></td><td><p>35.972元</p></td><td><p>35.972元</p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价6元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>6元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus</p><blockquote><p>当前能力等同于qwen3.6-plus-2026-04-02</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus-2026-04-02</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr></tbody></table>

<a id="中国香港-2"></a>

<a id="中国香港-2-h4"></a>

#### 中国香港

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th rowspan="2"><strong>单次请求的输入Token范围</strong></th><th rowspan="2"><strong>输入单价 （每百万Token）</strong></th><th colspan="2"><strong>输出单价 （每百万Token）</strong></th></tr><tr><th><strong>非思考模式</strong></th><th><strong>思考模式（思维链+回答）</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.7-plus</p><blockquote><p>当前能力等同于qwen3.7-plus-2026-05-26</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>原价2元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td><td><p>原价8元<strong>（限时8折）</strong></p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>原价6元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td><td><p>原价24元<strong>（限时8折）</strong></p></td></tr><tr><td rowspan="2"><p>qwen3.7-plus-2026-05-26</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>6元</p></td><td><p>24元</p></td><td><p>24元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-plus</p><blockquote><p>当前能力等同于qwen3.6-plus-2026-04-02</p></blockquote></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>12元</p></td><td><p>12元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8元</p></td><td><p>48元</p></td><td><p>48元</p></td></tr><tr><td><p>qwen-plus</p><blockquote><p>当前能力等同于qwen-plus-2025-12-01</p></blockquote></td><td><p>中国香港</p></td><td><p>不区分阶梯</p></td><td><p>8.75元</p></td><td><p>26.25元</p></td><td><p>87.501元</p></td></tr><tr><td rowspan="2"><p>qwen-plus-2025-12-01</p></td><td rowspan="2"><p>中国香港</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.917元</p></td><td><p>8.75元</p></td><td><p>29.167元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>8.75元</p></td><td><p>26.25元</p></td><td><p>87.501元</p></td></tr></tbody></table>

<a id="千问flash"></a>

<a id="13ff05e329blt"></a>

### 千问Flash

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](../model-experience/text-generation-model/context-cache.md)，仅输入Token享有折扣。两者不能同时生效。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-3"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.8元</p></td><td><p>2.7元</p></td><td><p>100万Token</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td><td rowspan="3"><p>100万Token</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash-2026-07-15</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p><blockquote><p>当前能力等同于qwen3.6-flash-2026-04-16</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-flash</p><blockquote><p>当前能力等同于qwen3.5-flash-2026-02-23</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.2元</p></td><td><p>2元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-flash-2026-02-23</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.2元</p></td><td><p>2元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="3"><p>qwen-flash</p><blockquote><p>当前能力等同于qwen-flash-2025-07-28</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.15元</p></td><td><p>1.5元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>6元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="3"><p>qwen-flash-2025-07-28</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.15元</p></td><td><p>1.5元</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>6元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-3"></a>

<a id="美国-弗吉尼亚-3-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.8元</p></td><td><p>2.7元</p></td></tr><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>美国</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>1.094元</p></td><td><p>3.427元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>美国</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.225元</p></td><td><p>0.974元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.749元</p></td><td><p>2.998元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.499元</p></td><td><p>5.995元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p><blockquote><p>当前能力等同于qwen3.6-flash-2026-04-16</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p></td><td rowspan="2"><p>美国</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.87355元</p></td><td><p>11.2413元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>7.4942元</p></td><td><p>29.9758元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-flash</p><blockquote><p>当前能力等同于qwen3.5-flash-2026-02-23</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.2元</p></td><td><p>2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-flash-2026-02-23</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.2元</p></td><td><p>2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="3"><p>qwen-flash</p><blockquote><p>当前能力等同于qwen-flash-2025-07-28</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.15元</p></td><td><p>1.5元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>6元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="2"><p>qwen-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>美国</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>0.367元</p></td><td><p>2.936元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.835元</p></td><td><p>14.678元</p></td></tr><tr><td rowspan="3"><p>qwen-flash-2025-07-28</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.15元</p></td><td><p>1.5元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>6元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="2"><p>qwen-flash-2025-07-28</p></td><td rowspan="2"><p>美国</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>0.367元</p></td><td><p>2.936元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.835元</p></td><td><p>14.678元</p></td></tr></tbody></table>

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>1.094元</p></td><td><p>3.427元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>国际</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.225元</p></td><td><p>0.974元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.749元</p></td><td><p>2.998元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.499元</p></td><td><p>5.995元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash-2026-07-15</p></td><td rowspan="3"><p>国际</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.225元</p></td><td><p>0.974元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.749元</p></td><td><p>2.998元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.499元</p></td><td><p>5.995元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p><blockquote><p>当前能力等同于qwen3.6-flash-2026-04-16</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.87355元</p></td><td><p>11.2413元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>7.4942元</p></td><td><p>29.9758元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.87355元</p></td><td><p>11.2413元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>7.4942元</p></td><td><p>29.9758元</p></td></tr><tr><td><p>qwen3.5-flash</p><blockquote><p>当前能力等同于qwen3.5-flash-2026-02-23</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.734元</p></td><td><p>2.936元</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.734元</p></td><td><p>2.936元</p></td></tr><tr><td rowspan="2"><p>qwen-flash</p><blockquote><p>当前能力等同于qwen-flash-2025-07-28</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>0.367元</p></td><td><p>2.936元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.835元</p></td><td><p>14.678元</p></td></tr><tr><td rowspan="2"><p>qwen-flash-2025-07-28</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>0.367元</p></td><td><p>2.936元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.835元</p></td><td><p>14.678元</p></td></tr></tbody></table>

<a id="德国-法兰克福-3"></a>

<a id="德国-法兰克福-3-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>欧盟</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>1.094元</p></td><td><p>3.427元</p></td></tr><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.8元</p></td><td><p>2.7元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash-2026-07-15</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p><blockquote><p>当前能力等同于qwen3.6-flash-2026-04-16</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-flash</p><blockquote><p>当前能力等同于qwen3.5-flash-2026-02-23</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.2元</p></td><td><p>2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td><p>qwen3.5-flash</p><blockquote><p>当前能力等同于qwen3.5-flash-2026-02-23</p></blockquote></td><td><p>欧盟</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.749元</p></td><td><p>2.998元</p></td></tr><tr><td rowspan="3"><p>qwen3.5-flash-2026-02-23</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.2元</p></td><td><p>2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.8元</p></td><td><p>8元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>欧盟</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.749元</p></td><td><p>2.998元</p></td></tr><tr><td rowspan="3"><p>qwen-flash</p><blockquote><p>当前能力等同于qwen-flash-2025-07-28</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.15元</p></td><td><p>1.5元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>6元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr><tr><td rowspan="3"><p>qwen-flash-2025-07-28</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.15元</p></td><td><p>1.5元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>6元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>12元</p></td></tr></tbody></table>

<a id="日本-东京-3"></a>

<a id="日本-东京-3-h4"></a>

#### 日本（东京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.8元</p></td><td><p>2.7元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash-2026-07-15</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p><blockquote><p>当前能力等同于qwen3.6-flash-2026-04-16</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr></tbody></table>

<a id="中国香港-3"></a>

<a id="中国香港-3-h4"></a>

#### 中国香港

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>中国香港</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>1.094元</p></td><td><p>3.427元</p></td></tr><tr><td><p>qwen3.8-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.8元</p></td><td><p>2.7元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash</p><blockquote><p>当前能力等同于qwen3.7-flash-2026-07-15</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="3"><p>qwen3.7-flash-2026-07-15</p></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>0.2元</p></td><td><p>0.8元</p></td></tr><tr><td><p>32K&lt;Token≤256K</p></td><td><p>0.6元</p></td><td><p>2.4元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>1.2元</p></td><td><p>4.8元</p></td></tr><tr><td rowspan="2"><p>qwen3.6-flash</p><blockquote><p>当前能力等同于qwen3.6-flash-2026-04-16</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>4.8元</p></td><td><p>28.8元</p></td></tr><tr><td><p>qwen3.5-flash</p><blockquote><p>当前能力等同于qwen3.5-flash-2026-02-23</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>中国香港</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.729元</p></td><td><p>2.917元</p></td></tr><tr><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>中国香港</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>0.729元</p></td><td><p>2.917元</p></td></tr></tbody></table>

<a id="千问long"></a>

<a id="e86562477acd4"></a>

### 千问Long

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费。

<a id="sec-tabs-4"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen-long</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.5元</p></td><td><p>2元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="千问omni"></a>

<a id="4c2e910ce4pcq"></a>

### 千问Omni

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](../model-experience/omni-modal/qwen-omni.md#a9018938d3niq)。

> **说明**
>
> Qwen3.5-Omni 和 Qwen3-Omni 系列仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-5"></a>

<a id="华北2-北京-5"></a>

<a id="华北2-北京-5-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 缓存命中输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash` | 中国内地 | 0.8元 | 0.1元 | 2.7元 |

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th colspan="2"><strong>输入单价（每百万Token）</strong></th><th colspan="2"><strong>输出单价（每百万Token）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr><tr><th><strong>文本/图片/视频</strong></th><th><strong>音频</strong></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.5-omni-plus</p><blockquote><p>当前能力等同于qwen3.5-omni-plus-2026-03-15</p></blockquote></td><td><p>7元</p></td><td><p>53元</p></td><td><p>40元</p></td><td><p>213元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.5-omni-plus-2026-03-15</p></td><td><p>7元</p></td><td><p>53元</p></td><td><p>40元</p></td><td><p>213元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.5-omni-flash</p><blockquote><p>当前能力等同于qwen3.5-omni-flash-2026-03-15</p></blockquote></td><td><p>2.2元</p></td><td><p>18元</p></td><td><p>13.3元</p></td><td><p>72元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.5-omni-flash-2026-03-15</p></td><td><p>2.2元</p></td><td><p>18元</p></td><td><p>13.3元</p></td><td><p>72元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="accordion-更多模型"></a>

更多模型

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>模式</strong></th><th colspan="3"><strong>输入单价（每百万Token）</strong></th><th colspan="3"><strong>输出单价（每百万Token）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr><tr><th><strong>文本</strong></th><th><strong>音频</strong></th><th><strong>图片/视频</strong></th><th><strong>文本</strong><blockquote><p>仅纯文本输入</p></blockquote></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-omni-flash</p></td><td><p>非思考和思考模式</p></td><td><p>1.8元</p></td><td><p>15.8元</p></td><td><p>3.3元</p></td><td><p>6.9元</p></td><td><p>12.7元</p></td><td><p>62.6元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 缓存命中输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash` | 国际 | 1.094元 | 0.117元 | 3.427元 |

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>输入单价（每百万Token）</strong></th><th colspan="2"><strong>输出单价（每百万Token）</strong></th></tr><tr><th><strong>文本/图片/视频</strong></th><th><strong>音频</strong></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.5-omni-plus</p><blockquote><p>当前能力等同于qwen3.5-omni-plus-2026-03-15</p></blockquote></td><td><p>国际</p></td><td><p>10.49元</p></td><td><p>82.44元</p></td><td><p>62.2元</p></td><td><p>329.74元</p></td></tr><tr><td><p>qwen3.5-omni-plus-2026-03-15</p></td><td><p>国际</p></td><td><p>10.49元</p></td><td><p>82.44元</p></td><td><p>62.2元</p></td><td><p>329.74元</p></td></tr><tr><td><p>qwen3.5-omni-flash</p><blockquote><p>当前能力等同于qwen3.5-omni-flash-2026-03-15</p></blockquote></td><td><p>国际</p></td><td><p>3元</p></td><td><p>22.48元</p></td><td><p>16.49元</p></td><td><p>89.18元</p></td></tr><tr><td><p>qwen3.5-omni-flash-2026-03-15</p></td><td><p>国际</p></td><td><p>3元</p></td><td><p>22.48元</p></td><td><p>16.49元</p></td><td><p>89.18元</p></td></tr></tbody></table>

<a id="accordion-更多模型-2"></a>

更多模型

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th rowspan="2"><strong>模式</strong></th><th colspan="3"><strong>输入单价（每百万Token）</strong></th><th colspan="3"><strong>输出单价（每百万Token）</strong></th></tr><tr><th><strong>文本</strong></th><th><strong>音频</strong></th><th><strong>图片/视频</strong></th><th><strong>文本</strong><blockquote><p>仅纯文本输入</p></blockquote></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-omni-flash</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>3.156元</p></td><td><p>27.962元</p></td><td><p>5.725元</p></td><td><p>12.183元</p></td><td><p>22.458元</p></td><td><p>110.896元</p></td></tr></tbody></table>

<a id="中国香港-4"></a>

<a id="中国香港-4-h4"></a>

#### 中国香港

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 缓存命中输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash` | 全球 | 0.8元 | 0.1元 | 2.7元 |

<a id="日本-东京-4"></a>

<a id="日本-东京-4-h4"></a>

#### 日本（东京）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 缓存命中输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash` | 全球 | 0.8元 | 0.1元 | 2.7元 |

<a id="德国-法兰克福-4"></a>

<a id="德国-法兰克福-4-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 缓存命中输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash` | 全球 | 0.8元 | 0.1元 | 2.7元 |

<a id="美国-弗吉尼亚-4"></a>

<a id="美国-弗吉尼亚-4-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 缓存命中输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash` | 全球 | 0.8元 | 0.1元 | 2.7元 |

<a id="千问omni-realtime"></a>

<a id="a162110bff6c4"></a>

### 千问Omni-Realtime

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](../model-experience/omni-modal/realtime.md#cb5caf6a0dg4k)。

输出语音时，`qwen3.8-omni-flash-realtime` 的音频及对应文本分别按音频输出和文本输出单价计费；Qwen3.5-Omni-Realtime 系列仅对音频计费，对应文本不计费。

> **说明**
>
> 表中标注的免费额度仅适用于华北2（北京）地域，其他地域均无免费额度。

<a id="sec-tabs-6"></a>

<a id="华北2-北京-6"></a>

<a id="华北2-北京-6-h4"></a>

#### 华北2（北京）

单价：元/百万 Token。

| 模型 ID（Model ID） | 输入：文本/图片/视频 | 输入：音频 | 输出：文本 | 输出：音频 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash-realtime` | 1.5 | 6 | 4.5 | 12 | 100万Token |

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th colspan="2"><strong>输入单价（每百万Token）</strong></th><th colspan="2"><strong>输出单价（每百万Token）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr><tr><th><strong>文本/图片</strong></th><th><strong>音频</strong></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.5-omni-plus-realtime</p><blockquote><p>当前能力等同于qwen3.5-omni-plus-realtime-2026-03-15</p></blockquote></td><td><p>10元</p></td><td><p>80元</p></td><td><p>60元</p></td><td><p>300元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.5-omni-plus-realtime-2026-03-15</p></td><td><p>10元</p></td><td><p>80元</p></td><td><p>60元</p></td><td><p>300元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime</p><blockquote><p>当前能力等同于qwen3.5-omni-flash-realtime-2026-03-15</p></blockquote></td><td><p>3.3元</p></td><td><p>27元</p></td><td><p>20元</p></td><td><p>107元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime-2026-03-15</p></td><td><p>3.3元</p></td><td><p>27元</p></td><td><p>20元</p></td><td><p>107元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="accordion-更多模型-3"></a>

更多模型

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th colspan="3"><strong>输入单价（每百万Token）</strong></th><th colspan="3"><strong>输出单价（每百万Token）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr><tr><th><strong>文本</strong></th><th><strong>音频</strong></th><th><strong>图片</strong></th><th><strong>文本</strong><blockquote><p>仅纯文本输入</p></blockquote></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-omni-flash-realtime-2025-09-15</p></td><td><p>2.2元</p></td><td><p>18.9元</p></td><td><p>3.9元</p></td><td><p>8.3元</p></td><td><p>15.2元</p></td><td><p>75.1元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-5"></a>

<a id="新加坡-5-h4"></a>

#### 新加坡

单价：元/百万 Token。

| 模型 ID（Model ID） | 输入：文本/图片/视频 | 输入：音频 | 输出：文本 | 输出：音频 |
| --- | --- | --- | --- | --- |
| `qwen3.8-omni-flash-realtime` | 1.677 | 6.781 | 5.104 | 13.636 |

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>输入单价（每百万Token）</strong></th><th colspan="2"><strong>输出单价（每百万Token）</strong></th></tr><tr><th><strong>文本/图片</strong></th><th><strong>音频</strong></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.5-omni-plus-realtime</p><blockquote><p>当前能力等同于qwen3.5-omni-plus-realtime-2026-03-15</p></blockquote></td><td><p>国际</p></td><td><p>15.74元</p></td><td><p>123.65元</p></td><td><p>92.93元</p></td><td><p>464.64元</p></td></tr><tr><td><p>qwen3.5-omni-plus-realtime-2026-03-15</p></td><td><p>国际</p></td><td><p>15.74元</p></td><td><p>123.65元</p></td><td><p>92.93元</p></td><td><p>464.64元</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime</p><blockquote><p>当前能力等同于qwen3.5-omni-flash-realtime-2026-03-15</p></blockquote></td><td><p>国际</p></td><td><p>4.12元</p></td><td><p>33.72元</p></td><td><p>24.73元</p></td><td><p>132.65元</p></td></tr><tr><td><p>qwen3.5-omni-flash-realtime-2026-03-15</p></td><td><p>国际</p></td><td><p>4.12元</p></td><td><p>33.72元</p></td><td><p>24.73元</p></td><td><p>132.65元</p></td></tr></tbody></table>

<a id="accordion-更多模型-4"></a>

更多模型

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="3"><strong>输入单价（每百万Token）</strong></th><th colspan="3"><strong>输出单价（每百万Token）</strong></th></tr><tr><th><strong>文本</strong></th><th><strong>音频</strong></th><th><strong>图片</strong></th><th><strong>文本</strong><blockquote><p>仅纯文本输入</p></blockquote></th><th><strong>文本</strong><blockquote><p>多模态输入</p></blockquote></th><th><strong>文本+音频</strong><blockquote><p>仅音频计费</p></blockquote></th></tr></thead><tbody><tr><td><p>qwen3-omni-flash-realtime-2025-09-15</p></td><td><p>国际</p></td><td><p>3.816元</p></td><td><p>33.54元</p></td><td><p>6.899元</p></td><td><p>14.605元</p></td><td><p>26.935元</p></td><td><p>133.06元</p></td></tr></tbody></table>

<a id="千问vl"></a>

<a id="499d0324a8dex"></a>

### 千问VL

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-7"></a>

<a id="华北2-北京-7"></a>

<a id="华北2-北京-7-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td rowspan="3"><p>qwen3-vl-plus</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>10元</p></td><td rowspan="3"><p>100万Token</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>15元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>30元</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-5"></a>

<a id="美国-弗吉尼亚-5-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td rowspan="3"><p>qwen3-vl-plus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>10元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>15元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>30元</p></td></tr></tbody></table>

<a id="新加坡-6"></a>

<a id="新加坡-6-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价 （每百万Token）</strong></th><th><strong>输出单价 （每百万Token）</strong></th></tr></thead><tbody><tr><td rowspan="3"><p>qwen3-vl-plus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>国际</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1.468元</p></td><td><p>11.743元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>2.202元</p></td><td><p>17.614元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>4.404元</p></td><td><p>35.228元</p></td></tr></tbody></table>

<a id="德国-法兰克福-5"></a>

<a id="德国-法兰克福-5-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td rowspan="3"><p>qwen3-vl-plus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>全球</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>10元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>15元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>30元</p></td></tr><tr><td rowspan="3"><p>qwen3-vl-plus</p></td><td rowspan="3"><p>欧盟</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1.499元</p></td><td><p>11.991元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>2.248元</p></td><td><p>17.986元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>4.497元</p></td><td><p>35.972元</p></td></tr></tbody></table>

<a id="中国香港-5"></a>

<a id="中国香港-5-h4"></a>

#### 中国香港

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td rowspan="3"><p>qwen3-vl-plus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="3"><p>中国香港</p></td><td rowspan="3"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1.458元</p></td><td><p>11.667元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>2.188元</p></td><td><p>17.5元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>4.375元</p></td><td><p>35元</p></td></tr></tbody></table>

<a id="千问ocr"></a>

<a id="3a0aa78a679em"></a>

### 千问OCR

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-8"></a>

<a id="华北2-北京-8"></a>

<a id="华北2-北京-8-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen3.5-ocr</p></td><td><p>0.5元</p></td><td><p>2元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen-vl-ocr</p><blockquote><p>当前能力等同于qwen-vl-ocr-2025-11-20</p></blockquote><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.3元</p></td><td><p>0.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>0.3元</p></td><td><p>0.5元</p></td><td><p>无</p></td></tr><tr><td><p>qwen-vl-ocr-2024-10-28</p></td><td><p>5元</p></td><td><p>5元</p></td><td><p>100万Token</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-6"></a>

<a id="美国-弗吉尼亚-6-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th></tr></thead><tbody><tr><td><p>qwen-vl-ocr</p><blockquote><p>当前能力等同于qwen-vl-ocr-2025-11-20</p></blockquote></td><td><p>全球</p></td><td><p>0.3元</p></td><td><p>0.5元</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>全球</p></td><td><p>0.3元</p></td><td><p>0.5元</p></td></tr></tbody></table>

<a id="新加坡-7"></a>

<a id="新加坡-7-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th></tr></thead><tbody><tr><td><p>qwen-vl-ocr</p><blockquote><p>当前能力等同于qwen-vl-ocr-2025-11-20</p></blockquote></td><td><p>国际</p></td><td><p>0.514元</p></td><td><p>1.174元</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>国际</p></td><td><p>0.514元</p></td><td><p>1.174元</p></td></tr></tbody></table>

<a id="德国-法兰克福-6"></a>

<a id="德国-法兰克福-6-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th></tr></thead><tbody><tr><td><p>qwen-vl-ocr</p><blockquote><p>当前能力等同于qwen-vl-ocr-2025-11-20</p></blockquote></td><td><p>全球</p></td><td><p>0.3元</p></td><td><p>0.5元</p></td></tr><tr><td><p>qwen-vl-ocr-2025-11-20</p></td><td><p>全球</p></td><td><p>0.3元</p></td><td><p>0.5元</p></td></tr></tbody></table>

<a id="千问audio"></a>

<a id="63387e4e29u5x"></a>

### 千问Audio

计费规则：按输入Token和输出Token计费。

音频Token计算规则：每一秒钟的音频对应25个Token。若音频时长不足1秒，则按25个Token计算。

<a id="sec-tabs-9"></a>

<a id="华北2-北京-9"></a>

<a id="华北2-北京-9-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen-audio-turbo</p></td><td colspan="2"><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐使用<a href="../model-experience/omni-modal/qwen-omni.md">全模态（Qwen-Omni）</a>作为替代模型</p></blockquote></td><td><p>10万Token</p></td></tr><tr><td><p>qwen-audio-turbo-latest</p></td><td colspan="2"><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐使用<a href="../model-experience/omni-modal/qwen-omni.md">全模态（Qwen-Omni）</a>作为替代模型</p></blockquote></td><td><p>10万Token</p></td></tr></tbody></table>

<a id="千问coder"></a>

<a id="6b674d4daexdt"></a>

### 千问Coder

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[上下文缓存](../model-experience/text-generation-model/context-cache.md)，仅输入Token享有折扣。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-10"></a>

<a id="华北2-北京-10"></a>

<a id="华北2-北京-10-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td rowspan="4"><p>qwen3-coder-flash</p><blockquote><p>当前能力等同于qwen3-coder-flash-2025-07-28</p></blockquote></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>4元</p></td><td rowspan="4"><p>无</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>6元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.5元</p></td><td><p>10元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>5元</p></td><td><p>25元</p></td></tr><tr><td rowspan="4"><p>qwen3-coder-flash-2025-07-28</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>4元</p></td><td rowspan="4"><p>无</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>6元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.5元</p></td><td><p>10元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>5元</p></td><td><p>25元</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-7"></a>

<a id="美国-弗吉尼亚-7-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价 （每百万Token）</strong></th><th><strong>输出单价 （每百万Token）</strong></th></tr></thead><tbody><tr><td rowspan="4"><p>qwen3-coder-flash</p><blockquote><p>当前能力等同于qwen3-coder-flash-2025-07-28</p></blockquote></td><td rowspan="4"><p>全球</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>4元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>6元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.5元</p></td><td><p>10元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>5元</p></td><td><p>25元</p></td></tr><tr><td rowspan="4"><p>qwen3-coder-flash-2025-07-28</p></td><td rowspan="4"><p>全球</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>4元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>6元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.5元</p></td><td><p>10元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>5元</p></td><td><p>25元</p></td></tr></tbody></table>

<a id="新加坡-8"></a>

<a id="新加坡-8-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价 （每百万Token）</strong></th><th><strong>输出单价 （每百万Token）</strong></th></tr></thead><tbody><tr><td rowspan="4"><p>qwen3-coder-flash</p><blockquote><p>当前能力等同于qwen3-coder-flash-2025-07-28</p></blockquote></td><td rowspan="4"><p>国际</p></td><td><p>0&lt;Token≤32K</p></td><td><p>2.202元</p></td><td><p>11.009元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>3.67元</p></td><td><p>18.348元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>5.871元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>11.743元</p></td><td><p>70.457元</p></td></tr><tr><td rowspan="4"><p>qwen3-coder-flash-2025-07-28</p></td><td rowspan="4"><p>国际</p></td><td><p>0&lt;Token≤32K</p></td><td><p>2.202元</p></td><td><p>11.009元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>3.67元</p></td><td><p>18.348元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>5.871元</p></td><td><p>29.357元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>11.743元</p></td><td><p>70.457元</p></td></tr></tbody></table>

<a id="德国-法兰克福-7"></a>

<a id="德国-法兰克福-7-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价 （每百万Token）</strong></th><th><strong>输出单价 （每百万Token）</strong></th></tr></thead><tbody><tr><td rowspan="4"><p>qwen3-coder-flash</p><blockquote><p>当前能力等同于qwen3-coder-flash-2025-07-28</p></blockquote></td><td rowspan="4"><p>全球</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>4元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>6元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.5元</p></td><td><p>10元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>5元</p></td><td><p>25元</p></td></tr><tr><td rowspan="4"><p>qwen3-coder-flash-2025-07-28</p></td><td rowspan="4"><p>全球</p></td><td><p>0&lt;Token≤32K</p></td><td><p>1元</p></td><td><p>4元</p></td></tr><tr><td><p>32K&lt;Token≤128K</p></td><td><p>1.5元</p></td><td><p>6元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2.5元</p></td><td><p>10元</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>5元</p></td><td><p>25元</p></td></tr></tbody></table>

<a id="qwen-mt-uni"></a>

<a id="uni-pricing"></a>

### Qwen-MT-Uni

计费规则：按 `input_tokens` 计费，按输入模态（文本/文档/图片/音频）分档计价，同步与异步价格一致。

<a id="sec-tabs-11"></a>

<a id="华北2-北京-11"></a>

<a id="华北2-北京-11-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th colspan="4"><p><strong>输入单价（每百万 Token）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr><tr><th><p><strong>文本</strong></p></th><th><p><strong>文档</strong></p></th><th><p><strong>图片</strong></p></th><th><p><strong>音频</strong></p></th></tr></thead><tbody><tr><td><p>qwen-mt-uni</p></td><td><p>65元</p></td><td><p>20元</p></td><td><p>32元</p></td><td><p>400元</p></td><td><p>100万 Token</p></td></tr></tbody></table>

以下为按模态分档计价折算后的实际花费示例：

| 翻译类型 | 示例单价 |
| --- | --- |
| 文本翻译 | ¥50/百万字符 |
| 文档翻译 | ¥0.08/页 |
| 图片翻译 | ¥0.06/张 |
| 音频翻译 | ¥0.3/分钟 |

> **说明**
>
> 以上为示例价格，用于帮助理解按 Token 计费折算后的实际花费，最终费用以单价表为准。

<a id="千问翻译模型"></a>

<a id="d4d9ec4242oj7"></a>

### 千问翻译模型

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-12"></a>

<a id="华北2-北京-12"></a>

<a id="华北2-北京-12-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-mt-plus | 1.8元 | 5.4元 | 100万Token |
| qwen-mt-flash | 0.7元 | 1.95元 | 100万Token |
| qwen-mt-lite | 0.6元 | 1.6元 | 100万Token |

<a id="美国-弗吉尼亚-8"></a>

<a id="美国-弗吉尼亚-8-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-mt-flash | 全球 | 0.7元 | 1.95元 |
| qwen-mt-lite | 全球 | 0.6元 | 1.6元 |
| qwen-mt-lite | 美国 | 0.881元 | 2.642元 |
| qwen-mt-plus | 全球 | 1.8元 | 5.4元 |

<a id="新加坡-9"></a>

<a id="新加坡-9-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-mt-plus | 国际 | 18.055元 | 54.09元 |
| qwen-mt-flash | 国际 | 1.174元 | 3.596元 |
| qwen-mt-lite | 国际 | 0.881元 | 2.642元 |

<a id="德国-法兰克福-8"></a>

<a id="德国-法兰克福-8-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-mt-plus | 全球 | 1.8元 | 5.4元 |
| qwen-mt-flash | 全球 | 0.7元 | 1.95元 |
| qwen-mt-lite | 全球 | 0.6元 | 1.6元 |

<a id="千问数据挖掘模型"></a>

<a id="b8160c3f1ciyj"></a>

### 千问数据挖掘模型

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-13"></a>

<a id="华北2-北京-13"></a>

<a id="华北2-北京-13-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56) |
| --- | --- | --- | --- |
| qwen-doc-turbo | 0.6元 | 1元 | 无 |

<a id="千问深入研究模型"></a>

<a id="af665c3673n6e"></a>

### 千问深入研究模型

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-14"></a>

<a id="华北2-北京-14"></a>

<a id="华北2-北京-14-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56) |
| --- | --- | --- | --- |
| qwen-deep-research | 54元 | 163元 | 无 |
| qwen-deep-research-2025-12-15 | 79元 | 236元 | 无 |

<a id="通义晓蜜对话分析模型"></a>

<a id="a50faad6f0iry"></a>

### 通义晓蜜对话分析模型

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](../model-experience/text-generation-model/context-cache.md)，仅输入Token享有折扣。两者不能同时生效。

<a id="sec-tabs-15"></a>

<a id="华北2-北京-15"></a>

<a id="华北2-北京-15-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输入单价（每百万Token）</strong></p></th><th><p><strong>输出单价（每百万Token）</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td><p>tongyi-xiaomi-analysis-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>0.2元</p></td><td><p>0.4元</p></td><td><p>100万Token</p></td></tr><tr><td><p>tongyi-xiaomi-analysis-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>1.0元</p></td><td><p>2.7元</p></td><td><p>100万Token</p></td></tr></tbody></table>

<a id="文本生成-千问-开源版"></a>

<a id="23f477ab156wv"></a>

## 文本生成-千问-开源版

<a id="qwen3-8"></a>

<a id="6d8a54769ab32"></a>

### Qwen3.8

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-16"></a>

<a id="华北2-北京-16"></a>

<a id="华北2-北京-16-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen3.8-2.4t-a95b</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>12元</p></td><td><p>36元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.8-27b</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>3元</p></td><td><p>12元</p></td><td><p>100万Token</p></td></tr></tbody></table>

<a id="新加坡-10"></a>

<a id="新加坡-10-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>qwen3.8-2.4t-a95b</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>14.988元</p></td><td><p>44.965元</p></td></tr><tr><td><p>qwen3.8-27b</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤1M</p></td><td><p>3.646元</p></td><td><p>21.875元</p></td></tr></tbody></table>

<a id="qwen3-6"></a>

<a id="q36b0h3ky"></a>

### Qwen3.6

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-17"></a>

<a id="华北2-北京-17"></a>

<a id="华北2-北京-17-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.8元</p></td><td><p>10.8元</p></td><td><p>10.8元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.6-27b</p></td><td><p>0&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>18元</p></td><td><p>18元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-9"></a>

<a id="美国-弗吉尼亚-9-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.8元</p></td><td><p>10.8元</p></td><td><p>10.8元</p></td></tr></tbody></table>

<a id="新加坡-11"></a>

<a id="新加坡-11-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.810325元</p></td><td><p>16.86195元</p></td><td><p>16.86195元</p></td></tr><tr><td><p>qwen3.6-27b</p></td><td><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>4.49652元</p></td><td><p>26.97912元</p></td><td><p>26.97912元</p></td></tr></tbody></table>

<a id="德国-法兰克福-9"></a>

<a id="德国-法兰克福-9-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3.6-35b-a3b</p></td><td><p>全球</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.8元</p></td><td><p>10.8元</p></td><td><p>10.8元</p></td></tr></tbody></table>

<a id="qwen3-5"></a>

<a id="q35b0h3ky"></a>

### Qwen3.5

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-18"></a>

<a id="华北2-北京-18"></a>

<a id="华北2-北京-18-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>0&lt;Token≤128K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td><td><p>7.2元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>18元</p></td><td><p>18元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-122b-a10b</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>6.4元</p></td><td><p>6.4元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>16元</p></td><td><p>16元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-27b</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.6元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>1.8元</p></td><td><p>14.4元</p></td><td><p>14.4元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.4元</p></td><td><p>3.2元</p></td><td><p>3.2元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>1.6元</p></td><td><p>12.8元</p></td><td><p>12.8元</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-10"></a>

<a id="美国-弗吉尼亚-10-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>18元</p></td><td><p>18元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-122b-a10b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>6.4元</p></td><td><p>6.4元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>16元</p></td><td><p>16元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-27b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.6元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>1.8元</p></td><td><p>14.4元</p></td><td><p>14.4元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.4元</p></td><td><p>3.2元</p></td><td><p>3.2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>1.6元</p></td><td><p>12.8元</p></td><td><p>12.8元</p></td></tr></tbody></table>

<a id="新加坡-12"></a>

<a id="新加坡-12-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td><p>qwen3.5-397b-a17b</p></td><td><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>4.404元</p></td><td><p>26.421元</p></td><td><p>26.421元</p></td></tr><tr><td><p>qwen3.5-122b-a10b</p></td><td><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.936元</p></td><td><p>23.486元</p></td><td><p>23.486元</p></td></tr><tr><td><p>qwen3.5-27b</p></td><td><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>2.202元</p></td><td><p>17.614元</p></td><td><p>17.614元</p></td></tr><tr><td><p>qwen3.5-35b-a3b</p></td><td><p>国际</p></td><td><p>0&lt;Token≤256K</p></td><td><p>1.835元</p></td><td><p>14.678元</p></td><td><p>14.678元</p></td></tr></tbody></table>

<a id="德国-法兰克福-10"></a>

<a id="德国-法兰克福-10-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th rowspan="2"><p><strong>单次请求的输入Token范围</strong></p></th><th rowspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>非思考模式</strong></p></th><th><p><strong>思考模式（思维链+回答）</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>1.2元</p></td><td><p>7.2元</p></td><td><p>7.2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>3元</p></td><td><p>18元</p></td><td><p>18元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-122b-a10b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.8元</p></td><td><p>6.4元</p></td><td><p>6.4元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>2元</p></td><td><p>16元</p></td><td><p>16元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-27b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.6元</p></td><td><p>4.8元</p></td><td><p>4.8元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>1.8元</p></td><td><p>14.4元</p></td><td><p>14.4元</p></td></tr><tr><td rowspan="2"><p>qwen3.5-35b-a3b</p></td><td rowspan="2"><p>全球</p></td><td><p>0&lt;Token≤128K</p></td><td><p>0.4元</p></td><td><p>3.2元</p></td><td><p>3.2元</p></td></tr><tr><td><p>128K&lt;Token≤256K</p></td><td><p>1.6元</p></td><td><p>12.8元</p></td><td><p>12.8元</p></td></tr></tbody></table>

<a id="qwen-audio"></a>

<a id="3891ecc8bd2nm"></a>

### Qwen-Audio

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-19"></a>

<a id="华北2-北京-19"></a>

<a id="华北2-北京-19-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen2-audio-instruct</p></td><td colspan="2"><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐使用<a href="../model-experience/omni-modal/qwen-omni.md">全模态（Qwen-Omni）</a>作为替代模型。</p></blockquote></td><td><p>10万Token</p></td></tr><tr><td><p>qwen-audio-chat</p></td><td colspan="2"><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐使用<a href="../model-experience/omni-modal/qwen-omni.md">全模态（Qwen-Omni）</a>作为替代模型。</p></blockquote></td><td><p>10万Token</p></td></tr></tbody></table>

<a id="文本生成-第三方模型"></a>

<a id="774b4cf48dtbp"></a>

## 文本生成-第三方模型

<a id="deepseek"></a>

<a id="c13da832a1rie"></a>

### DeepSeek

计费规则：按输入Token和输出Token计费。

部分模型按峰谷价格计费（见下表标注的忙时、闲时单价）：忙时为北京时间 08:00 至 22:00，闲时为北京时间 22:00 至次日 08:00。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

> **说明**
>
> DeepSeek-V4-Flash-0731 已于 2026-08-17 00:00 起调整为峰谷定价模式，调整后单价可见下表，更多信息详见[DeepSeek-V4-Flash-0731 模型涨价通知](https://www.aliyun.com/notice/118555)。

<a id="sec-tabs-20"></a>

<a id="华北2-北京-20"></a>

<a id="华北2-北京-20-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td><td><p>无</p></td></tr><tr><td><p>deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td><td><p>100万Token</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>12元</p></td><td><p>24元</p></td><td><p>无</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td><td><p>忙时 27元</p><p>闲时 13.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>忙时 3元</p><p>闲时 1.5元</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>deepseek-r1-distill-qwen-1.5b</p></td><td colspan="3"><p>限时免费</p></td></tr><tr><td><p>deepseek-r1-distill-llama-70b</p></td><td colspan="2"><p>目前仅供免费体验</p><blockquote><p>免费额度用完后不可调用，推荐使用<a href="../model-experience/text-generation-model/deep-thinking.md">深度思考</a>、<a href="../use-cases/third-party-model-integration-tutorial/deepseek-api.md">DeepSeek-阿里云</a>、<a href="../use-cases/third-party-model-integration-tutorial/kimi-api.md">Kimi-阿里云</a>作为替代模型</p></blockquote></td><td><p>100万Token</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-11"></a>

<a id="美国-弗吉尼亚-11-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>12元</p></td><td><p>24元</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td><td><p>忙时 27元</p><p>闲时 13.5元</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>美国</p></td><td><p>17.986元</p></td><td><p>35.972元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 3元</p><p>闲时 1.5元</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>美国</p></td><td><p>忙时 3.208元</p><p>闲时 1.604元</p></td><td><p>忙时 9.625元</p><p>闲时 4.813元</p></td></tr></tbody></table>

<a id="新加坡-13"></a>

<a id="新加坡-13-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>忙时 2.188元</p><p>闲时 1.094元</p></td><td><p>忙时 8.75元</p><p>闲时 4.375元</p></td></tr><tr><td><p>deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>忙时 2.188元</p><p>闲时 1.094元</p></td><td><p>忙时 8.75元</p><p>闲时 4.375元</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>17.986元</p></td><td><p>35.972元</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>忙时 9.625元</p><p>闲时 4.813元</p></td><td><p>忙时 28.875元</p><p>闲时 14.438元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>忙时 3.208元</p><p>闲时 1.604元</p></td><td><p>忙时 9.625元</p><p>闲时 4.813元</p></td></tr></tbody></table>

<a id="德国-法兰克福-11"></a>

<a id="德国-法兰克福-11-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>12元</p></td><td><p>24元</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td><td><p>忙时 27元</p><p>闲时 13.5元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 3元</p><p>闲时 1.5元</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td></tr></tbody></table>

<a id="日本-东京-5"></a>

<a id="日本-东京-5-h4"></a>

#### 日本（东京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>12元</p></td><td><p>24元</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td><td><p>忙时 27元</p><p>闲时 13.5元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 3元</p><p>闲时 1.5元</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td></tr><tr><td><p>deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>日本</p></td><td><p>17.986元</p></td><td><p>35.972元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>日本</p></td><td><p>忙时 3.208元</p><p>闲时 1.604元</p></td><td><p>忙时 9.625元</p><p>闲时 4.813元</p></td></tr></tbody></table>

<a id="中国香港-6"></a>

<a id="中国香港-6-h4"></a>

#### 中国香港

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>deepseek-v4.1-flash-1017</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 2元</p><p>闲时 1元</p></td><td><p>忙时 8元</p><p>闲时 4元</p></td></tr><tr><td><p>deepseek-v4-flash-0731</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 3元</p><p>闲时 1.5元</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td></tr><tr><td><p>deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>全球</p></td><td><p>忙时 9元</p><p>闲时 4.5元</p></td><td><p>忙时 27元</p><p>闲时 13.5元</p></td></tr></tbody></table>

<a id="deepseek-硅基流动"></a>

<a id="y5b7nziongfns"></a>

### DeepSeek-硅基流动

<a id="sec-tabs-21"></a>

<a id="华北2-北京-21"></a>

<a id="华北2-北京-21-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><strong>免费额度</strong></th></tr></thead><tbody><tr><td><p>siliconflow/deepseek-v3.2</p></td><td><p>2元</p></td><td><p>3元</p></td><td><p>无</p></td></tr><tr><td><p>siliconflow/deepseek-v3.1-terminus</p></td><td><p>4元</p></td><td><p>12元</p></td><td><p>无</p></td></tr><tr><td><p>siliconflow/deepseek-r1-0528</p></td><td><p>4元</p></td><td><p>16元</p></td><td><p>无</p></td></tr><tr><td><p>siliconflow/deepseek-v3-0324</p></td><td><p>2元</p></td><td><p>8元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="deepseek-快手万擎"></a>

<a id="z79giy1xk1q04"></a>

### DeepSeek-快手万擎

<a id="sec-tabs-22"></a>

<a id="华北2-北京-22"></a>

<a id="华北2-北京-22-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链+回答</strong></blockquote></th><th><strong>免费额度</strong></th></tr></thead><tbody><tr><td><p>vanchin/deepseek-v3.2-think</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>2元</p></td><td><p>3元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-v3.1-terminus</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>4元</p></td><td><p>12元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-r1</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>4元</p></td><td><p>16元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-v3</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>2元</p></td><td><p>8元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-ocr</p></td><td><p>0.216元</p></td><td><p>0.216元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-v4-pro</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>12元</p></td><td><p>24元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-v4-pro-0813</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>9元</p></td><td><p>27元</p></td><td><p>无</p></td></tr><tr><td><p>vanchin/deepseek-v4.1-flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>2元</p></td><td><p>8元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="kimi"></a>

<a id="27c0f3876fka8"></a>

### Kimi

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-23"></a>

<a id="华北2-北京-23"></a>

<a id="华北2-北京-23-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 模式 | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- | --- |
| [kimi-k3.1-pro](../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) | 思考与非思考（默认开启思考） | 13元<br><br>缓存命中输入：1.3元 | 68元 | 输入与输出合计100万Token |
| kimi-k3.1-pro-prime | 思考与非思考（默认开启思考） | 26元<br><br>缓存命中输入：1.3元 | 136元 | 无 |
| kimi-k3 | 仅思考模式 | 20元 | 100元 | 无 |
| kimi-k2.7-code | 仅思考模式 | 6.5元 | 27元 | 100万Token |
| kimi-k2.6 | 非思考和思考模式 | 6.5元 | 27元 | 无 |
| kimi-k2.5 | 非思考和思考模式 | 4元 | 21元 | 无 |

<a id="美国-弗吉尼亚-12"></a>

<a id="美国-弗吉尼亚-12-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 模式 | 输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| [kimi-k3.1-pro](../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) | 全球 | 思考与非思考（默认开启思考） | 13元<br><br>缓存命中输入：1.3元 | 68元 |
| kimi-k3 | 全球 | 仅思考模式 | 20元 | 100元 |
| [kimi-k3.1-pro](../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) | 美国 | 思考与非思考（默认开启思考） | 14.583元<br><br>缓存命中输入：1.458元 | 72.917元 |
| kimi-k3 | 国际 | 仅思考模式 | 21.875元 | 109.376元 |
| kimi-k2.7-code | 全球 | 仅思考模式 | 6.5元 | 27元 |
| kimi-k2.5 | 全球 | 非思考和思考模式 | 4元 | 21元 |

<a id="德国-法兰克福-12"></a>

<a id="德国-法兰克福-12-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 模式 | 输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| [kimi-k3.1-pro](../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) | 全球 | 思考与非思考（默认开启思考） | 13元<br><br>缓存命中输入：1.3元 | 68元 |
| kimi-k3 | 全球 | 仅思考模式 | 20元 | 100元 |
| kimi-k2.7-code | 全球 | 仅思考模式 | 6.5元 | 27元 |
| kimi-k2.5 | 全球 | 非思考和思考模式 | 4元 | 21元 |

<a id="日本-东京-6"></a>

<a id="日本-东京-6-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>模式</strong></p></th><th><p><strong>输入单价（每百万Token）</strong></p></th><th><p><strong>输出单价（每百万Token）</strong></p></th></tr></thead><tbody><tr><td><p><a href="../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md">kimi-k3.1-pro</a></p></td><td><p>全球</p></td><td><p>思考与非思考（默认开启思考）</p></td><td><p>13元</p><p>缓存命中输入：1.3元</p></td><td><p>68元</p></td></tr><tr><td><p>kimi-k3</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>全球</p></td><td><p>仅思考模式</p></td><td><p>20元</p></td><td><p>100元</p></td></tr><tr><td><p>kimi-k2.7-code</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>全球</p></td><td><p>仅思考模式</p></td><td><p>6.5元</p></td><td><p>27元</p></td></tr><tr><td><p>kimi-k2.5</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>4元</p></td><td><p>21元</p></td></tr></tbody></table>

<a id="新加坡-14"></a>

<a id="新加坡-14-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 模式 | 输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| [kimi-k3.1-pro](../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) | 国际 | 思考与非思考（默认开启思考） | 14.583元<br><br>缓存命中输入：1.458元 | 72.917元 |
| kimi-k3.1-pro-prime | 国际 | 思考与非思考（默认开启思考） | 29.167元<br><br>缓存命中输入：1.458元 | 145.833元 |
| kimi-k3 | 国际 | 仅思考模式 | 21.875元 | 109.376元 |
| kimi-k2.7-code | 国际 | 仅思考模式 | 7.119元 | 29.977元 |

<a id="中国香港-7"></a>

<a id="中国香港-7-h4"></a>

#### 中国香港

| 模型 ID（Model ID） | 服务部署范围 | 模式 | 输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- | --- |
| [kimi-k3.1-pro](../get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) | 全球 | 思考与非思考（默认开启思考） | 13元<br><br>缓存命中输入：1.3元 | 68元 |
| kimi-k3 | 全球 | 仅思考模式 | 20元 | 100元 |
| kimi-k2.7-code | 全球 | 仅思考模式 | 6.5元 | 27元 |

<a id="kimi-月之暗面"></a>

<a id="a580a9aea67xs"></a>

### Kimi-月之暗面

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-24"></a>

<a id="华北2-北京-24"></a>

<a id="华北2-北京-24-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输入单价（每百万Token）</strong></p></th><th><p><strong>输出单价（每百万Token）</strong></p><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>kimi/kimi-k3.1-pro-highspeed</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>26元</p></td><td><p>136元</p></td><td><p></p><p>无</p></td></tr><tr><td><p>kimi/kimi-k3.1-pro</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>13元</p></td><td><p>68元</p></td><td><p></p><p>无</p></td></tr><tr><td><p>kimi/kimi-k3</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>20元</p></td><td><p>100元</p></td><td><p></p><p>无</p></td></tr><tr><td><p>kimi/kimi-k2.7-code-highspeed</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>13元</p></td><td><p>54元</p></td><td><p></p><p>无</p></td></tr><tr><td><p>kimi/kimi-k2.7-code</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>6.5元</p></td><td><p>27元</p></td><td><p></p><p>无</p></td></tr><tr><td><p>kimi/kimi-k2.6</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>6.5元</p></td><td><p>27元</p></td><td><p></p><p>无</p></td></tr><tr><td><p>kimi/kimi-k2.5</p><blockquote><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</blockquote></td><td><p>4元</p></td><td><p>21元</p></td><td><p></p><p>无</p></td></tr></tbody></table>

<a id="glm"></a>

<a id="79a28cb88cnd5"></a>

### GLM

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-25"></a>

<a id="华北2-北京-25"></a>

<a id="华北2-北京-25-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td><td><p>100万Token</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td><td><p>无</p></td></tr><tr><td><p>glm-5.2-fast-preview</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>16元</p></td><td><p>56元</p></td><td><p>无</p></td></tr><tr><td><p>glm-5.3-prime</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>16元</p></td><td><p>56元</p></td><td><p>无</p></td></tr><tr><td rowspan="2"><p>glm-5.1</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>6元</p></td><td><p>24元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>32K&lt;Token≤200K</p></td><td><p>8元</p></td><td><p>28元</p></td></tr><tr><td rowspan="2"><p>glm-5</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>4元</p></td><td><p>18元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>32K&lt;Token≤198K</p></td><td><p>6元</p></td><td><p>22元</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-13"></a>

<a id="美国-弗吉尼亚-13-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td></tr><tr><td><p>glm-5.3</p></td><td><p>美国</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>10.208元</p></td><td><p>32.084元</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>美国</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>10.492元</p></td><td><p>32.974元</p></td></tr><tr><td rowspan="2"><p>glm-5.1</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>6元</p></td><td><p>24元</p></td></tr><tr><td><p>32K&lt;Token≤200K</p></td><td><p>8元</p></td><td><p>28元</p></td></tr></tbody></table>

<a id="新加坡-15"></a>

<a id="新加坡-15-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>10.208元</p></td><td><p>32.084元</p></td><td><p>100万Token</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>10.492元</p></td><td><p>32.974元</p></td><td><p>无</p></td></tr><tr><td><p>glm-5.2-fast-preview</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>20.98元</p></td><td><p>65.95元</p></td><td><p>无</p></td></tr><tr><td><p>glm-5.1</p></td><td><p>国际</p></td><td><p>非思考和思考模式</p></td><td><p>0&lt;Token≤200K</p></td><td><p>10.492元</p></td><td><p>32.974元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="德国-法兰克福-13"></a>

<a id="德国-法兰克福-13-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td></tr><tr><td><p>glm-5.2</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td></tr><tr><td rowspan="2"><p>glm-5.1</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>6元</p></td><td><p>24元</p></td></tr><tr><td><p>32K&lt;Token≤200K</p></td><td><p>8元</p></td><td><p>28元</p></td></tr></tbody></table>

<a id="日本-东京-7"></a>

<a id="日本-东京-7-h4"></a>

#### 日本（东京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.3</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td></tr><tr><td rowspan="2"><p>glm-5.1</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>非思考和思考模式</p></td><td><p>0&lt;Token≤32K</p></td><td><p>6元</p></td><td><p>24元</p></td></tr><tr><td><p>32K&lt;Token≤200K</p></td><td><p>8元</p></td><td><p>28元</p></td></tr></tbody></table>

<a id="中国香港-8"></a>

<a id="中国香港-8-h4"></a>

#### 中国香港

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>模式</strong></th><th><strong>单次请求的输入Token数</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th></tr></thead><tbody><tr><td><p>glm-5.2</p></td><td><p>全球</p></td><td><p>非思考和思考模式</p></td><td><p>不区分阶梯</p></td><td><p>8元</p></td><td><p>28元</p></td></tr></tbody></table>

<a id="glm-智谱"></a>

<a id="d82dca8e98of9"></a>

### GLM-智谱

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-26"></a>

<a id="华北2-北京-26"></a>

<a id="华北2-北京-26-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>ZHIPU/GLM-5.3</p></td><td><p>仅思考模式</p></td><td><p>8元</p></td><td><p>28元</p></td><td><p>无</p></td></tr><tr><td><p>ZHIPU/GLM-5.3-Flash</p></td><td><p>仅思考模式</p></td><td><p>0.8元</p></td><td><p>2.8元</p></td><td><p>无</p></td></tr><tr><td><p>ZHIPU/GLM-5.3-FlashX</p></td><td><p>仅思考模式</p></td><td><p>2元</p></td><td><p>7元</p></td><td><p>无</p></td></tr><tr><td><p>ZHIPU/GLM-5.2</p></td><td><p>非思考和思考模式</p></td><td><p>8元</p></td><td><p>28元</p></td><td><p>无</p></td></tr><tr><td><p>ZHIPU/GLM-5.1</p></td><td><p>非思考和思考模式</p></td><td><p>8元</p></td><td><p>28元</p></td><td><p>无</p></td></tr><tr><td><p>ZHIPU/GLM-5</p></td><td><p>非思考和思考模式</p></td><td><p>6元</p></td><td><p>22元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="minimax"></a>

<a id="b08cd557f4spf"></a>

### MiniMax

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-27"></a>

<a id="华北2-北京-27"></a>

<a id="华北2-北京-27-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>MiniMax-M2.5</p></td><td><p>仅思考模式</p></td><td><p>2.1元</p></td><td><p>8.4元</p></td><td rowspan="2"><p>100万Token</p></td></tr></tbody></table>

<a id="minimax-稀宇科技"></a>

<a id="2a394289d6erj"></a>

### MiniMax-稀宇科技

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-28"></a>

<a id="华北2-北京-28"></a>

<a id="华北2-北京-28-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>模式</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>MiniMax/MiniMax-M3.1-Flash</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>仅思考模式</p></td><td><p>1元</p></td><td><p>4元</p></td><td><p>无</p></td></tr><tr><td><p>MiniMax/MiniMax-M3</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>非思考和思考模式</p></td><td><p>输入不超过 512k Token：2.1元</p><p>输入超过 512k Token：4.2元</p></td><td><p>输入不超过 512k Token：8.4元</p><p>输入超过 512k Token：16.8元</p></td><td><p>无</p></td></tr><tr><td><p>MiniMax/MiniMax-M2.7</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>仅思考模式</p></td><td><p>2.1元</p></td><td><p>8.4元</p></td><td><p>无</p></td></tr><tr><td><p>MiniMax/MiniMax-M2.5</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>仅思考模式</p></td><td><p>2.1元</p></td><td><p>8.4元</p></td><td><p>无</p></td></tr><tr><td><p>MiniMax/MiniMax-M2.1</p><blockquote><p><a href="../model-experience/text-generation-model/context-cache.md">上下文缓存</a>享有折扣</p></blockquote></td><td><p>仅思考模式</p></td><td><p>2.1元</p></td><td><p>8.4元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="mimo-小米"></a>

<a id="iixlr3q9sys4p"></a>

### MiMo-小米

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-29"></a>

<a id="华北2-北京-29"></a>

<a id="华北2-北京-29-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入Token数量</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>xiaomi/mimo-v2.6-pro-ultraspeed</p></td><td><p>0&lt;Token≤1M</p></td><td><p>30元</p></td><td><p>60元</p></td><td><p>无</p></td></tr><tr><td rowspan="2"><p>xiaomi/mimo-v2.5-pro</p></td><td><p>0&lt;Token≤256K</p></td><td><p>7元</p></td><td><p>21元</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>256K&lt;Token≤1M</p></td><td><p>14元</p></td><td><p>42元</p></td></tr></tbody></table>

<a id="stepfun-阶跃星辰"></a>

<a id="ymk7xm2kts5pa"></a>

### Stepfun-阶跃星辰

<a id="sec-tabs-30"></a>

<a id="华北2-北京-30"></a>

<a id="华北2-北京-30-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>stepfun/step-3.7-flash</p></td><td><p>1.35元</p></td><td><p>8.1元</p></td><td><p>无</p></td></tr><tr><td><p>stepfun/step-5-preview</p></td><td><p>7元</p></td><td><p>20元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="unisound-云知声"></a>

### Unisound-云知声

<a id="sec-tabs-31"></a>

<a id="华北2-北京-31"></a>

<a id="华北2-北京-31-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>unisound/unisound-u2</p></td><td><p>1元</p></td><td><p>2元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="ling-蚂蚁数科"></a>

### Ling-蚂蚁数科

<a id="sec-tabs-32"></a>

<a id="华北2-北京-32"></a>

<a id="华北2-北京-32-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong><blockquote><strong>思维链和回答</strong></blockquote></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>antdigital/Ling-3.1-flash</p></td><td><p>原价2元<strong>（限时2.5折）</strong></p></td><td><p>原价6元<strong>（限时2.5折）</strong></p></td><td><p>无</p></td></tr></tbody></table>

<a id="图像生成"></a>

<a id="26310bc5cf4do"></a>

## 图像生成

计费规则：按输入图像和成功生成的 **图像张数**计费。未说明输入图像价格的模型，输入不计费，仅输出计费。

计费公式：`费用 = 输入图像单价 × 输入的图像张数 + 输出图像单价 × 输出的图像张数`。

计费说明：请求失败不产生任何费用，也不消耗免费额度。

<a id="accordion-计费示例-部分图像生成失败"></a>

计费示例：部分图像生成失败

假设输入图像单价为0，输出图像单价为 0.10元/张。若您调用接口请求生成 4 张图像，但实际仅成功返回 3 张图像的 URL，另 1 张生成失败，系统将仅对成功生成的图像进行计费。

-   计费数量：3 张。
-   费用计算：0.1 × 3 = 0.3元。

<a id="千问图像生成与编辑"></a>

<a id="2e0ddf5c9edy0"></a>

### 千问图像生成与编辑

> 按输入输出的图像张数计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-33"></a>

<a id="华北2-北京-33"></a>

<a id="华北2-北京-33-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen-image-3.0-pro</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.25元/张</p></td><td rowspan="2"><p>输入输出共10张</p></td></tr><tr><td><p>2k</p></td><td><p>0.5元/张</p></td></tr><tr><td rowspan="2"><p>qwen-image-3.0</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.18元/张</p></td><td rowspan="2"><p>输入输出共10张</p></td></tr><tr><td><p>2k</p></td><td><p>0.18元/张</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-14"></a>

<a id="美国-弗吉尼亚-14-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen-image-3.0-pro</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.25元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.5元/张</p></td></tr><tr><td rowspan="2"><p>qwen-image-3.0</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.18元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.18元/张</p></td></tr></tbody></table>

<a id="新加坡-16"></a>

<a id="新加坡-16-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen-image-3.0-pro</p></td><td rowspan="2"><p>国际</p></td><td><p>1k</p></td><td rowspan="2"><p>0.022483元/张</p></td><td><p>0.299768元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.562065元/张</p></td></tr><tr><td rowspan="2"><p>qwen-image-3.0</p></td><td rowspan="2"><p>国际</p></td><td><p>1k</p></td><td rowspan="2"><p>0.022483元/张</p></td><td><p>0.224826元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.224826元/张</p></td></tr></tbody></table>

<a id="德国-法兰克福-14"></a>

<a id="德国-法兰克福-14-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen-image-3.0-pro</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.25元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.5元/张</p></td></tr><tr><td rowspan="2"><p>qwen-image-3.0</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.18元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.18元/张</p></td></tr></tbody></table>

<a id="日本-东京-8"></a>

<a id="日本-东京-8-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen-image-3.0-pro</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.25元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.5元/张</p></td></tr><tr><td rowspan="2"><p>qwen-image-3.0</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.18元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.18元/张</p></td></tr></tbody></table>

<a id="中国香港-9"></a>

<a id="中国香港-9-h4"></a>

#### 中国香港

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>qwen-image-3.0-pro</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.25元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.5元/张</p></td></tr><tr><td rowspan="2"><p>qwen-image-3.0</p></td><td rowspan="2"><p>全球</p></td><td><p>1k</p></td><td rowspan="2"><p>0.02元/张</p></td><td><p>0.18元/张</p></td></tr><tr><td><p>2k</p></td><td><p>0.18元/张</p></td></tr></tbody></table>

<a id="千问图像生成与编辑2-0系列"></a>

<a id="qwen-image-2-0-series-pricing"></a>

#### 千问图像生成与编辑2.0系列

qwen-image-2.0 系列按张计费，支持文生图与图生图/图像编辑，各地域单价如下。

<a id="sec-tabs-34"></a>

<a id="华北2-北京-34"></a>

<a id="华北2-北京-34-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | 免费额度 |
| --- | --- | --- |
| qwen-image-2.1-pro | 0.25元/张 | 10张 |
| qwen-image-2.1-turbo | 0.1元/张 | 10张 |
| qwen-image-2.0-pro | 0.5元/张 | 无 |
| qwen-image-2.0-pro-2026-06-22 | 0.5元/张 | 无 |
| qwen-image-2.0-pro-2026-04-22 | 0.5元/张 | 无 |
| qwen-image-2.0-pro-2026-03-03 | 0.5元/张 | 无 |
| qwen-image-2.0 | 0.2元/张 | 无 |
| qwen-image-2.0-2026-03-03 | 0.2元/张 | 无 |

<a id="美国-弗吉尼亚-15"></a>

<a id="美国-弗吉尼亚-15-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| qwen-image-2.1-pro | 全球 | 0.25元/张 |
| qwen-image-2.1-turbo | 全球 | 0.1元/张 |

<a id="新加坡-17"></a>

<a id="新加坡-17-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| qwen-image-2.1-pro | 国际 | 0.283404元/张 |
| qwen-image-2.1-turbo | 国际 | 0.113362元/张 |
| qwen-image-2.0-pro | 国际 | 0.550443元/张 |
| qwen-image-2.0-pro-2026-06-22 | 国际 | 0.550443元/张 |
| qwen-image-2.0-pro-2026-04-22 | 国际 | 0.550443元/张 |
| qwen-image-2.0-pro-2026-03-03 | 国际 | 0.550443元/张 |
| qwen-image-2.0 | 国际 | 0.256873元/张 |
| qwen-image-2.0-2026-03-03 | 国际 | 0.256873元/张 |

<a id="德国-法兰克福-15"></a>

<a id="德国-法兰克福-15-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| qwen-image-2.1-pro | 全球 | 0.25元/张 |
| qwen-image-2.1-turbo | 全球 | 0.1元/张 |

<a id="日本-东京-9"></a>

<a id="日本-东京-9-h4"></a>

#### 日本（东京）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| qwen-image-2.1-pro | 全球 | 0.25元/张 |
| qwen-image-2.1-turbo | 全球 | 0.1元/张 |

<a id="中国香港-10"></a>

<a id="中国香港-10-h4"></a>

#### 中国香港

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| qwen-image-2.1-pro | 全球 | 0.25元/张 |
| qwen-image-2.1-turbo | 全球 | 0.1元/张 |

<a id="千问图像翻译"></a>

<a id="a3250eda6bgjx"></a>

### 千问图像翻译

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-35"></a>

<a id="华北2-北京-35"></a>

<a id="华北2-北京-35-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| qwen-mt-image-2.0 | 0.004元/张 | 100张 |
| qwen-mt-image | 0.003元/张 | 100张 |

<a id="新加坡-18"></a>

<a id="新加坡-18-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| qwen-mt-image-2.0 | 国际 | 0.004375元/张 |

<a id="z-image"></a>

<a id="6713612f55h4l"></a>

### Z-Image

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-36"></a>

<a id="华北2-北京-36"></a>

<a id="华北2-北京-36-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| z-image-turbo | 关闭提示词改写（`prompt_extend=false`）：0.1元/张<br><br>开启提示词改写（`prompt_extend=true`）：0.2元/张 | 100张 |

<a id="新加坡-19"></a>

<a id="新加坡-19-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| z-image-turbo | 国际 | 关闭提示词改写（`prompt_extend=false`）：0.110089元/张<br><br>开启提示词改写（`prompt_extend=true`）：0.220177元/张 |

<a id="万相文生图"></a>

<a id="0006b52b83ua9"></a>

### 万相文生图

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-37"></a>

<a id="华北2-北京-37"></a>

<a id="华北2-北京-37-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| wan2.6-t2i | 0.20元/张 | 无 |
| wan2.5-t2i-preview | 0.20元/张 | 无 |
| wan2.2-t2i-plus | 0.20元/张 | 无 |
| wan2.2-t2i-flash | 0.14元/张 | 无 |
| wanx2.1-t2i-plus | 0.20元/张 | 无 |
| wanx2.1-t2i-turbo | 0.14元/张 | 无 |
| wanx2.0-t2i-turbo | 0.04元/张 | 无 |
| wanx-v1 | 0.16元/张 | 无 |

<a id="美国-弗吉尼亚-16"></a>

<a id="美国-弗吉尼亚-16-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.6-t2i | 全球 | 0.20元/张 |

<a id="新加坡-20"></a>

<a id="新加坡-20-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.6-t2i | 国际 | 0.220177元/张 |
| wan2.5-t2i-preview | 国际 | 0.220177元/张 |
| wan2.2-t2i-plus | 国际 | 0.366962元/张 |
| wan2.2-t2i-flash | 国际 | 0.183481元/张 |
| wan2.1-t2i-plus | 国际 | 0.366962元/张 |
| wan2.1-t2i-turbo | 国际 | 0.183481元/张 |

<a id="德国-法兰克福-16"></a>

<a id="德国-法兰克福-16-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.6-t2i | 全球 | 0.20元/张 |

<a id="万相图像生成与编辑"></a>

<a id="e2540d71a2utl"></a>

### 万相图像生成与编辑

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-38"></a>

<a id="华北2-北京-38"></a>

<a id="华北2-北京-38-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| wan2.7-image-pro | 0.50元/张 | 50张 |
| wan2.7-image | 0.20元/张 | 50张 |
| wan2.6-image | 0.20元/张 | 无 |

<a id="美国-弗吉尼亚-17"></a>

<a id="美国-弗吉尼亚-17-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.6-image | 全球 | 0.20元/张 |

<a id="新加坡-21"></a>

<a id="新加坡-21-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.7-image-pro | 国际 | 0.562065元/张 |
| wan2.7-image | 全球 | 0.027504元/张 |
| wan2.7-image | 国际 | 0.224826元/张 |
| wan2.6-image | 国际 | 0.220177元/张 |

<a id="德国-法兰克福-17"></a>

<a id="德国-法兰克福-17-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.6-image | 全球 | 0.20元/张 |

<a id="万相通用图像编辑"></a>

<a id="d4c994ef10xnk"></a>

### 万相通用图像编辑

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-39"></a>

<a id="华北2-北京-39"></a>

<a id="华北2-北京-39-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| wan2.5-i2i-preview | 0.20元/张 | 无 |
| wanx2.1-imageedit | 0.14元/张 | 无 |

<a id="新加坡-22"></a>

<a id="新加坡-22-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出单价 |
| --- | --- | --- |
| wan2.5-i2i-preview | 国际 | 0.220177元/张 |

<a id="万相涂鸦作画"></a>

<a id="8ec91f510bdc1"></a>

### 万相涂鸦作画

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-40"></a>

<a id="华北2-北京-40"></a>

<a id="华北2-北京-40-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| wanx-sketch-to-image-lite | 0.06元/张 | 500张 |

<a id="万相图像局部重绘"></a>

<a id="b137ab86a1nxu"></a>

### 万相图像局部重绘

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-41"></a>

<a id="华北2-北京-41"></a>

<a id="华北2-北京-41-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输出单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>wanx-x-painting</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td><p>500张</p></td></tr></tbody></table>

<a id="人像风格重绘"></a>

<a id="76284e83757dy"></a>

### 人像风格重绘

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-42"></a>

<a id="华北2-北京-42"></a>

<a id="华北2-北京-42-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| wanx-style-repaint-v1 | 0.12元/张 | 500张 |

<a id="人物实例分割"></a>

<a id="d9f01a23eccze"></a>

### 人物实例分割

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-43"></a>

<a id="华北2-北京-43"></a>

<a id="华北2-北京-43-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输出单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>image-instance-segmentation</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用。</p></blockquote></td><td><p>500张</p></td></tr></tbody></table>

<a id="图像擦除补全"></a>

<a id="aa397c10f2zi5"></a>

### 图像擦除补全

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-44"></a>

<a id="华北2-北京-44"></a>

<a id="华北2-北京-44-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输出单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>image-erase-completion</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td><p>500张</p></td></tr></tbody></table>

<a id="虚拟模特"></a>

<a id="968173a2513m7"></a>

### 虚拟模特

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-45"></a>

<a id="华北2-北京-45"></a>

<a id="华北2-北京-45-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输出单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>wanx-virtualmodel</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td><p>500张</p></td></tr><tr><td><p>virtualmodel-v2</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td><p>500张</p></td></tr></tbody></table>

<a id="鞋靴模特"></a>

<a id="6cd2901ba7ocm"></a>

### 鞋靴模特

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-46"></a>

<a id="华北2-北京-46"></a>

<a id="华北2-北京-46-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输出单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>shoemodel-v1</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用。</p></blockquote></td><td><p>500张</p></td></tr></tbody></table>

<a id="创意海报生成"></a>

<a id="2a22582736kab"></a>

### 创意海报生成

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-47"></a>

<a id="华北2-北京-47"></a>

<a id="华北2-北京-47-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输出单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>wanx-poster-generation-v1</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td><p>500张</p></td></tr></tbody></table>

<a id="人物写真生成-facechain"></a>

<a id="88756e5f858dv"></a>

### 人物写真生成-FaceChain

-   facechain-facedetect：限时免费。
-   facechain-finetune：按训练次数计费，请求失败不计费。

<a id="sec-tabs-48"></a>

<a id="华北2-北京-48"></a>

<a id="华北2-北京-48-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| facechain-facedetect | 限时免费 | 限时免费 |
| facechain-finetune | 2.5元/次 | 50次 |

<a id="图像生成-第三方模型"></a>

<a id="dc5de83bf45os"></a>

## 图像生成-第三方模型

<a id="可灵-图像生成"></a>

<a id="kli002a0h3001"></a>

### 可灵-图像生成

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-49"></a>

<a id="华北2-北京-49"></a>

<a id="华北2-北京-49-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td rowspan="2"><p>kling/kling-v3-image-generation</p></td><td><p>1K</p></td><td><p>0.2元/张</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>0.2元/张</p></td></tr><tr><td rowspan="3"><p>kling/kling-v3-omni-image-generation</p></td><td><p>1K</p></td><td><p>0.2元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>0.2元/张</p></td></tr><tr><td><p>4K</p></td><td><p>0.4元/张</p></td></tr></tbody></table>

<a id="vidu-图像生成"></a>

<a id="vidu-img-billing-h3"></a>

### Vidu-图像生成

> 仅输出计费，计费规则请参见[图像生成](model-pricing.md#26310bc5cf4do)。

<a id="sec-tabs-50"></a>

<a id="华北2-北京-50"></a>

<a id="华北2-北京-50-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出图像分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td rowspan="3"><p>vidu/viduq3.1-fast_reference2image</p></td><td><p>1K</p></td><td><p>0.25元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>0.34375元/张</p></td></tr><tr><td><p>4K</p></td><td><p>0.71875元/张</p></td></tr><tr><td rowspan="3"><p>vidu/vidu-image_reference2image</p></td><td><p>1K</p></td><td><p>0.625元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>1元/张</p></td></tr><tr><td><p>4K</p></td><td><p>1.46875元/张</p></td></tr><tr><td rowspan="3"><p>vidu/vidu-image-pro_reference2image</p></td><td><p>1K</p></td><td><p>1.6875元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>3.1875元/张</p></td></tr><tr><td><p>4K</p></td><td><p>5.125元/张</p></td></tr><tr><td rowspan="3"><p>vidu/vidu-image-lite_reference2image</p></td><td><p>1K</p></td><td><p>0.3125元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>0.34375元/张</p></td></tr><tr><td><p>4K</p></td><td><p>0.40625元/张</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-fast_reference2image</p></td><td><p>1K</p></td><td><p>0.46875元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>0.78125元/张</p></td></tr><tr><td><p>4K</p></td><td><p>1.09375元/张</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2-pro_reference2image</p></td><td><p>1K</p></td><td><p>0.9375元/张</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>2K</p></td><td><p>0.9375元/张</p></td></tr><tr><td><p>4K</p></td><td><p>1.71875元/张</p></td></tr><tr><td><p>vidu/viduq2-fast_reference2image</p></td><td><p>1K</p></td><td><p>0.28125元/张</p></td><td><p>无</p></td></tr></tbody></table>

<a id="语音识别"></a>

<a id="speech-recognition-pricing"></a>

<a id="696c1bf328gf9"></a>

<a id="语音识别-语音转文本-与翻译-语音转成指定语种的文本"></a>

## 语音识别

<a id="qwen-audio-asr"></a>

<a id="c5c66a1bbfvke"></a>

### Qwen-Audio-ASR

计费规则：

-   `qwen-audio-3.1-asr-flash`：按输入和输出 Token 数分别计费。
-   `qwen-audio-3.0-asr-flash`：按输入音频的秒数计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-51"></a>

<a id="华北2-北京-51"></a>

<a id="华北2-北京-51-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash | 0.8元/百万 Token | 2.7元/百万 Token | 100万 Token |
| qwen-audio-3.0-asr-flash | 0.00022元/秒 | 不计费 | 无 |

<a id="新加坡-23"></a>

<a id="新加坡-23-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 | 输出单价 |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash | 国际 | 1.094元/百万 Token | 3.427元/百万 Token |
| qwen-audio-3.0-asr-flash | 国际 | 0.00026元/秒 | 不计费 |

<a id="qwen-audio-asr-streaming"></a>

<a id="1681755cc2kcb"></a>

### Qwen-Audio-ASR-Streaming

计费规则：

-   `qwen-audio-3.1-asr-flash-streaming`：按输入和输出 Token 数分别计费。
-   `qwen-audio-3.0-asr-flash-streaming`：按输入音频的秒数计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-52"></a>

<a id="华北2-北京-52"></a>

<a id="华北2-北京-52-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-streaming | 6元/百万 Token | 4.5元/百万 Token | 100万 Token |
| qwen-audio-3.0-asr-flash-streaming | 0.00033元/秒 | 不计费 | 无 |

<a id="新加坡-24"></a>

<a id="新加坡-24-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 | 输出单价 |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-streaming | 国际 | 6.781元/百万 Token | 5.104元/百万 Token |
| qwen-audio-3.0-asr-flash-streaming | 国际 | 0.00066元/秒 | 不计费 |

<a id="qwen-audio-asr-filetrans"></a>

<a id="0fa27e11f4nq5"></a>

### Qwen-Audio-ASR-Filetrans

计费规则：

-   `qwen-audio-3.1-asr-flash-filetrans`：按输入和输出 Token 数分别计费。
-   `qwen-audio-3.0-asr-flash-filetrans`：按输入音频的秒数计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-53"></a>

<a id="华北2-北京-53"></a>

<a id="华北2-北京-53-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-filetrans | 0.8元/百万 Token | 2.7元/百万 Token | 100万 Token |
| qwen-audio-3.0-asr-flash-filetrans | 0.00022元/秒 | 不计费 | 无 |

<a id="新加坡-25"></a>

<a id="新加坡-25-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 | 输出单价 |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-filetrans | 国际 | 1.094元/百万 Token | 3.427元/百万 Token |
| qwen-audio-3.0-asr-flash-filetrans | 国际 | 0.00026元/秒 | 不计费 |

<a id="qwen-audio-asr-message"></a>

<a id="asr-message"></a>

### Qwen-Audio-ASR-Message

计费规则：按输入和输出 Token 数计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-54"></a>

<a id="华北2-北京-54"></a>

<a id="华北2-北京-54-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | 免费额度[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-message | 6元 | 4.5元 | 100万Token |

<a id="新加坡-26"></a>

<a id="新加坡-26-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） | 输出单价（每百万Token） |
| --- | --- | --- | --- |
| qwen-audio-3.1-asr-flash-message | 国际 | 6.781元 | 5.104元 |

<a id="千问asr"></a>

<a id="dbf1305ef4a69"></a>

### 千问ASR

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-55"></a>

<a id="华北2-北京-55"></a>

<a id="华北2-北京-55-h4"></a>

#### 华北2（北京）

计费规则：按输入音频的秒数计费，输出不计费。

| 模型 ID（Model ID） | 输入单价 | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen3-asr-flash-filetrans | 0.00022元/秒 | 不计费 | 36,000秒（10小时） |
| qwen3-asr-flash | 0.00022元/秒 | 不计费 | 36,000秒（10小时） |

<a id="美国-弗吉尼亚-18"></a>

<a id="美国-弗吉尼亚-18-h4"></a>

#### 美国（弗吉尼亚）

计费规则：按输入音频的秒数计费，输出不计费。

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash</p></td><td><p>美国</p></td><td><p>0.000035元/秒</p></td><td rowspan="2"><p>不计费</p></td></tr></tbody></table>

<a id="新加坡-27"></a>

<a id="新加坡-27-h4"></a>

#### 新加坡

计费规则：按输入音频的秒数计费，输出不计费。

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 | 输出单价 |
| --- | --- | --- | --- |
| qwen3-asr-flash-filetrans | 国际 | 0.00026元/秒 | 不计费 |
| qwen3-asr-flash | 国际 | 0.00026元/秒 | 不计费 |

<a id="千问asr-realtime"></a>

<a id="600addd3a2rnq"></a>

### 千问ASR-Realtime

计费规则：按输入音频的秒数计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-56"></a>

<a id="华北2-北京-56"></a>

<a id="华北2-北京-56-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen3-asr-flash-realtime</p></td><td rowspan="3"><p>0.00033元/秒</p></td><td><p>36,000秒（10小时）</p></td></tr></tbody></table>

<a id="新加坡-28"></a>

<a id="新加坡-28-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价</strong></th></tr></thead><tbody><tr><td><p>qwen3-asr-flash-realtime</p></td><td><p>国际</p></td><td rowspan="3"><p>0.00066元/秒</p></td></tr></tbody></table>

<a id="fun-asr"></a>

<a id="8c50a9f1e526h"></a>

### Fun-ASR

<a id="录音文件识别"></a>

<a id="e3ee164eeccug"></a>

#### 录音文件识别

计费规则：按输入音频的秒数计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-57"></a>

<a id="华北2-北京-57"></a>

<a id="华北2-北京-57-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| fun-asr | 0.00022元/秒 | 36,000秒（10小时） |
| fun-asr-flash-2026-06-15 | 0.00022元/秒 | 36,000秒（10小时） |

<a id="新加坡-29"></a>

<a id="新加坡-29-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 |
| --- | --- | --- |
| fun-asr | 国际 | 0.00026元/秒 |
| fun-asr-flash-2026-06-15 | 国际 | 0.00026元/秒 |

<a id="实时语音识别"></a>

<a id="fb374d30b6kvv"></a>

#### 实时语音识别

计费规则：按输入音频的秒数计费，输出不计费。

<a id="sec-tabs-58"></a>

<a id="华北2-北京-58"></a>

<a id="华北2-北京-58-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>fun-asr-realtime</p></td><td><p>0.00033元/秒</p></td><td><p>36,000秒（10小时）</p></td></tr><tr><td><p>fun-asr-realtime-2026-02-28</p></td><td><p>0.00033元/秒</p></td><td><p>无</p></td></tr><tr><td><p>fun-asr-mtl-realtime-2025-12-10</p></td><td><p>0.00033元/秒</p></td><td><p>无</p></td></tr><tr><td><p>fun-asr-flash-8k-realtime</p><blockquote><p>当前能力等同于fun-asr-flash-8k-realtime-2026-01-28</p></blockquote></td><td><p>0.00022元/秒</p></td><td><p>36,000秒（10小时）</p></td></tr><tr><td><p>fun-asr-flash-8k-realtime-2026-01-28</p></td><td><p>0.00022元/秒</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-30"></a>

<a id="新加坡-30-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输入单价</strong></p></th></tr></thead><tbody><tr><td><p>fun-asr-realtime</p></td><td><p>国际</p></td><td rowspan="2"><p>0.00066元/秒</p></td></tr></tbody></table>

<a id="paraformer"></a>

<a id="c018769cd7y88"></a>

### Paraformer

<a id="录音文件识别-2"></a>

<a id="142fc9eb67ee5"></a>

#### 录音文件识别

计费规则：按输入音频的秒数计费，输出不计费。

<a id="sec-tabs-59"></a>

<a id="华北2-北京-59"></a>

<a id="华北2-北京-59-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56) |
| --- | --- | --- |
| paraformer-v2 | 0.00008元/秒 | 36,000秒（10小时）<br><br>每月1日0点自动发放<br><br>有效期1个月 |
| paraformer-8k-v2 | 0.00008元/秒 | 36,000秒（10小时）<br><br>每月1日0点自动发放<br><br>有效期1个月 |

<a id="实时语音识别-2"></a>

<a id="3e9d4ca891q26"></a>

#### 实时语音识别

计费规则：按输入音频的秒数计费，输出不计费。

<a id="sec-tabs-60"></a>

<a id="华北2-北京-60"></a>

<a id="华北2-北京-60-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56) |
| --- | --- | --- |
| paraformer-realtime-v2 | 0.00024元/秒 | 36,000秒（10小时）<br><br>每月1日0点自动发放<br><br>有效期1个月 |
| paraformer-realtime-8k-v2 | 0.00024元/秒 | 36,000秒（10小时）<br><br>每月1日0点自动发放<br><br>有效期1个月 |

<a id="语音合成"></a>

<a id="speech-synthesis-pricing"></a>

<a id="16c0080f6axd3"></a>

<a id="语音合成-文本转语音"></a>

## 语音合成

**字符计算规则**：本节中按字符数计费的模型（输入单价按“每万字符”计），其输入文本的字符数按以下规则统计：

-   一个汉字（包括简体汉字、繁体汉字、日文汉字和韩文汉字）计为 2 个字符。
-   其他字符（如一个英文字母、一个数字、一个标点符号、一个空格、一个日文假名、一个韩文字母）计为 1 个字符。
-   使用 SSML 时，SSML 标签本身不计入字符数，仅统计待合成的文本内容。

**示例**：“你好”为 4 个字符（2+2）；“中A文123”为 8 个字符（2+1+2+1+1+1）；“中文。”为 5 个字符（2+2+1）；“中 文。”为 6 个字符（2+1+2+1）。

<a id="qwen-audio-tts"></a>

<a id="qattcn002h3"></a>

### Qwen-Audio-TTS

计费规则：qwen-audio-3.1-tts-flash 按输入和输出的 Token 数分别计费；其他模型按输入文本的字符数计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-61"></a>

<a id="华北2-北京-61"></a>

<a id="华北2-北京-61-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万 Token） | 输出单价（每百万 Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼或模型发布之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-tts-flash | 1.5元 | 12元 | 100万 Token |

| 模型 ID（Model ID） | 输入单价（每万字符） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)有效期：自开通百炼或模型发布之日起90天内（以较晚者为准） |
| --- | --- | --- |
| qwen-audio-3.1-tts-plus | 1.4元 | 1万字符 |
| qwen-audio-3.0-tts-plus | 1.4元 | 无 |
| qwen-audio-3.0-tts-flash | 1元 | 无 |

<a id="新加坡-31"></a>

<a id="新加坡-31-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 输入单价（每百万 Token） | 输出单价（每百万 Token） |
| --- | --- | --- |
| qwen-audio-3.1-tts-flash | 1.677元 | 13.636元 |

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每万字符） |
| --- | --- | --- |
| qwen-audio-3.1-tts-plus | 国际 | 2.19元 |
| qwen-audio-3.0-tts-plus | 国际 | 1.49884元 |
| qwen-audio-3.0-tts-flash | 国际 | 1.12413元 |

<a id="cosyvoice"></a>

<a id="7f2d0573f9o7p"></a>

### CosyVoice

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-62"></a>

<a id="华北2-北京-62"></a>

<a id="华北2-北京-62-h4"></a>

#### 华北2（北京）

计费规则：按输入文本的字符数计费，输出不计费。

| 模型 ID（Model ID） | 输入单价（每万字符） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| cosyvoice-v3.5-plus | 1.5元 | 1万字符 |
| cosyvoice-v3.5-flash | 0.8元 | 1万字符 |
| cosyvoice-v3-plus | 2元 | 无 |
| cosyvoice-v3-flash | 1元 | 无 |
| cosyvoice-v2 | 2元 | 无 |

<a id="新加坡-32"></a>

<a id="新加坡-32-h4"></a>

#### 新加坡

计费规则：按输入文本的字符数计费，输出不计费。

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每万字符） |
| --- | --- | --- |
| cosyvoice-v3-plus | 国际 | 1.9082元 |
| cosyvoice-v3-flash | 国际 | 0.9541元 |

`CosyVoice` 模型目前仅提供按量付费模式，暂无单独的用量套餐或资源包。

<a id="minimax-2"></a>

<a id="8296764fe3l4x"></a>

### MiniMax

计费规则：按输入文本的字符数计费，输出不计费。

复刻音色收取一次性费用，费用在首次使用该音色进行语音合成的时候，与语音合成的费用一同出账。

<a id="sec-tabs-63"></a>

<a id="华北2-北京-63"></a>

<a id="华北2-北京-63-h4"></a>

#### 华北2（北京）

| 模型名称 | 语音合成单价（每万字符） | [复刻一个音色](https://help.aliyun.com/zh/model-studio/mini-clone-api) | **免费额度**[（注）](new-free-quota.md#977b13081ab56) |
| --- | --- | --- | --- |
| MiniMax/speech-2.8-hd | 3.5元 | 9.9元<br><br>（在首次使用复刻出来的音色进行语音合成的时候收取） | 无 |
| MiniMax/speech-02-hd | 3.5元 | 9.9元<br><br>（在首次使用复刻出来的音色进行语音合成的时候收取） | 无 |
| MiniMax/speech-2.8-turbo | 2元 | 9.9元<br><br>（在首次使用复刻出来的音色进行语音合成的时候收取） | 无 |
| MiniMax/speech-02-turbo | 2元 | 9.9元<br><br>（在首次使用复刻出来的音色进行语音合成的时候收取） | 无 |

<a id="qwen-tts"></a>

<a id="6ba2b912aao1w"></a>

### Qwen-TTS

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-64"></a>

<a id="华北2-北京-64"></a>

<a id="华北2-北京-64-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-65"></a>

<a id="千问3-tts-flash"></a>

<a id="千问3-tts-flash-h4"></a>

#### 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

| 模型 ID（Model ID） | 输入单价（每万字符） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen3-tts-flash | 0.8元 | 不计费 | 1万字符 |

<a id="千问-tts"></a>

<a id="千问-tts-h4"></a>

#### 千问-TTS

计费规则：按输入Token和输出Token计费。

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-tts-flash | 1.6元 | 10元 | 100万Token |

<a id="新加坡-33"></a>

<a id="新加坡-33-h4"></a>

#### 新加坡

<a id="sec-tabs-66"></a>

<a id="千问3-tts-flash-2"></a>

<a id="千问3-tts-flash-2-h4"></a>

#### 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每万字符） |
| --- | --- | --- |
| qwen3-tts-flash | 国际 | 0.733924元 |

<a id="qwen-tts-realtime"></a>

<a id="1b45ef3328q1u"></a>

### Qwen-TTS-Realtime

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-67"></a>

<a id="华北2-北京-65"></a>

<a id="华北2-北京-65-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-68"></a>

<a id="千问3-tts-flash-realtime"></a>

<a id="千问3-tts-flash-realtime-h4"></a>

#### 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| 模型 ID（Model ID） | 输入单价（每万字符） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen3-tts-flash-realtime | 1元 | 不计费 | 2025年11月13日0点后开通阿里云百炼：1万字符 |

<a id="新加坡-34"></a>

<a id="新加坡-34-h4"></a>

#### 新加坡

<a id="sec-tabs-69"></a>

<a id="千问3-tts-flash-realtime-2"></a>

<a id="千问3-tts-flash-realtime-2-h4"></a>

#### 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每万字符） |
| --- | --- | --- |
| qwen3-tts-flash-realtime | 国际 | 0.954101元 |

<a id="sambert"></a>

<a id="62602640d2lkc"></a>

### Sambert

计费规则：按输入文本的字符数计费，输出不计费。

<a id="sec-tabs-70"></a>

<a id="华北2-北京-66"></a>

<a id="华北2-北京-66-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每万字符） | **免费额度**[（注）](new-free-quota.md#977b13081ab56) |
| --- | --- | --- |
| 参见[模型列表](../../_short/sambert-java-sdk-79ed7a3fed2f3f90.md#57d33631f7doi) | 1元 | 每主账号每模型每月3万字符。 |

<a id="音频打标"></a>

<a id="audio-tagging-pricing"></a>

## 音频打标

<a id="qwen-audio-3-1-captioner"></a>

<a id="captioner-pricing"></a>

### Qwen-Audio-3.1-Captioner

<a id="sec-tabs-71"></a>

<a id="华北2-北京-67"></a>

<a id="华北2-北京-67-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价 | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-captioner | 0.8元/百万 Token | 2.7元/百万 Token | 100万 Token |

<a id="音频生成"></a>

<a id="audio-generation-pricing"></a>

## 音频生成

<a id="qwen-audio-tts-next"></a>

<a id="qwen-audio-tts-next-pricing"></a>

### Qwen-Audio-TTS-Next

按输入和输出 Token 数分别计费。

<a id="sec-tabs-72"></a>

<a id="华北2-北京-68"></a>

<a id="华北2-北京-68-h4"></a>

#### 华北2（北京）

| 模型 ID | 输入单价（元/百万 Token） | 输出单价（元/百万 Token） | 免费额度[（注）](new-free-quota.md#977b13081ab56)<br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| qwen-audio-3.1-tts-next | 6 | 12 | 100万Token |

<a id="新加坡-35"></a>

<a id="新加坡-35-h4"></a>

#### 新加坡

| 模型 ID | 输入单价（元/百万 Token） | 输出单价（元/百万 Token） |
| --- | --- | --- |
| qwen-audio-3.1-tts-next | 6.781 | 5.104 |

<a id="语音对话"></a>

<a id="voice-chat-pricing"></a>

<a id="e479dc69b2e9o"></a>

## 语音对话

<a id="qwen-audio-realtime"></a>

<a id="01caa1110fbvp"></a>

<a id="实时语音对话"></a>

### Qwen-Audio-Realtime

实时语音对话模型支持文本和音频的输入与输出，按输入 Token 和输出 Token 分别计费。音频 Token 按时长折算：`总 Token 数 = 音频时长（单位：秒）* 12.5`，不足 1 秒按 1 秒计算。

仅输出文本时，按文本输出单价计费；输出文本和音频时，仅对音频收取输出费用，伴随文本不另收输出费。

在多轮对话场景中，与文本大模型一致，模型会维护完整的对话上下文以保持连贯的对话能力。历史对话内容会作为后续轮次的输入处理和计费，因此每轮的输入 Token 数会随对话轮次增加而逐步增长。各类内容的具体计费方式如下：

-   **用户输入的音频和文本**：计入上下文，在后续每轮对话中作为输入计费。其中音频按音频 Token 计费，文本按文本 Token 计费。
-   **用户设置的 instructions**：按文本 Token 每轮计费一次。
-   **模型输出的文本**：按文本 Token 计入上下文，在后续每轮对话中作为输入计费。
-   **模型输出的音频**：按音频 Token 仅在输出时计费一次，不计入上下文。

> 随着对话轮次增加，上下文累积的 Token 数量会逐步增长。建议合理控制单次会话的对话轮数，或在适当时机开启新会话，以优化使用成本。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-73"></a>

<a id="华北2-北京-69"></a>

<a id="华北2-北京-69-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th colspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr><tr><th><p><strong>文本</strong></p></th><th><p><strong>音频</strong></p></th><th><p><strong>文本</strong></p></th><th><p><strong>音频</strong></p></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-realtime-plus</p></td><td><p>5元</p></td><td><p>40元</p></td><td><p>40元</p></td><td><p>150元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen-audio-3.1-realtime-flash</p></td><td><p>1.5元</p></td><td><p>6元</p></td><td><p>4.5元</p></td><td><p>12元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-plus</p></td><td><p>5元</p></td><td><p>40元</p></td><td><p>40元</p></td><td><p>150元</p></td><td><p>无</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-flash</p></td><td><p>1.5元</p></td><td><p>6元</p></td><td><p>4.5元</p></td><td><p>12元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-36"></a>

<a id="新加坡-36-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th></tr><tr><th><p><strong>文本</strong></p></th><th><p><strong>音频</strong></p></th><th><p><strong>文本</strong></p></th><th><p><strong>音频</strong></p></th></tr></thead><tbody><tr><td><p>qwen-audio-3.1-realtime-plus</p></td><td><p>国际</p></td><td><p>5.833元</p></td><td><p>46.667元</p></td><td><p>46.667元</p></td><td><p>175.002元</p></td></tr><tr><td><p>qwen-audio-3.1-realtime-flash</p></td><td><p>国际</p></td><td><p>1.677元</p></td><td><p>6.781元</p></td><td><p>5.104元</p></td><td><p>13.636元</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-plus</p></td><td><p>国际</p></td><td><p>5.995元</p></td><td><p>47.963元</p></td><td><p>47.963元</p></td><td><p>179.861元</p></td></tr><tr><td><p>qwen-audio-3.0-realtime-flash</p></td><td><p>国际</p></td><td><p>1.677元</p></td><td><p>6.781元</p></td><td><p>5.104元</p></td><td><p>13.636元</p></td></tr></tbody></table>

<a id="qwen-audio-live"></a>

<a id="qwen-audio-live-pricing"></a>

### Qwen-Audio-Live

Qwen-Audio-Live 按会话时长（秒）计费。连接建立后，单次会话至少按 3 秒计费。超过 3 秒时，按实际会话时长计费。发送文字消息、静音或空闲的时间也计入会话时长。百炼调用后台模型时，按该模型的实际 Token 用量和单价另行计费。

<a id="sec-tabs-74"></a>

<a id="华北2-北京-70"></a>

<a id="华北2-北京-70-h4"></a>

#### 华北2（北京）

| 模型 ID | 单价（元/秒） |
| --- | --- |
| `qwen-audio-3.1-live` | 0.003330 |

免费额度为 36,000 秒（10 小时），仅适用于华北2（北京）地域。有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算，以较晚者为准。可在控制台查看额度和余额。详见[新人免费额度](new-free-quota.md#977b13081ab56)。

<a id="新加坡-37"></a>

<a id="新加坡-37-h4"></a>

#### 新加坡

| 模型 ID | 单价（元/秒） |
| --- | --- |
| `qwen-audio-3.1-live` | 0.005177 |

<a id="音视频翻译"></a>

<a id="audio-video-translation-pricing"></a>

## 音视频翻译

<a id="千问-livetranslate-flash-realtime"></a>

<a id="63707cc386etu"></a>

### 千问-LiveTranslate-Flash-Realtime

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费说明](../model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#e02a82e668y2c)。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-75"></a>

<a id="华北2-北京-71"></a>

<a id="华北2-北京-71-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th colspan="2"><strong>输入单价（每百万Token）</strong></th><th colspan="2"><strong>输出单价（每百万Token）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr><tr><th><strong>输入：音频</strong></th><th><strong>输入：图片</strong></th><th><strong>输出：文本</strong></th><th><strong>输出：音频</strong></th></tr></thead><tbody><tr><td><p>qwen3.8-livetranslate-flash-realtime</p></td><td><p>40元</p></td><td><p>3.3元</p></td><td><p>100元</p></td><td><p>160元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime</p></td><td><p>40元</p></td><td><p>3.3元</p></td><td><p>100元</p></td><td><p>160元</p></td><td><p>无</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime-2026-05-19</p></td><td><p>40元</p></td><td><p>3.3元</p></td><td><p>100元</p></td><td><p>160元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-38"></a>

<a id="新加坡-38-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><strong>模型 ID（Model ID）</strong></th><th rowspan="2"><strong>服务部署范围</strong></th><th colspan="2"><strong>输入单价 (每百万 Token)</strong></th><th colspan="2"><strong>输出单价 (每百万 Token)</strong></th></tr><tr><th><strong>输入：音频</strong></th><th><strong>输入：图片</strong></th><th><strong>输出：文本</strong></th><th><strong>输出：音频</strong></th></tr></thead><tbody><tr><td><p>qwen3.8-livetranslate-flash-realtime</p></td><td><p>国际</p></td><td><p>54.688元</p></td><td><p>4.01元</p></td><td><p>145.835元</p></td><td><p>218.752元</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime</p></td><td><p>国际</p></td><td><p>56.207元</p></td><td><p>4.122元</p></td><td><p>149.884元</p></td><td><p>224.826元</p></td></tr><tr><td><p>qwen3.5-livetranslate-flash-realtime-2026-05-19</p></td><td><p>国际</p></td><td><p>56.207元</p></td><td><p>4.122元</p></td><td><p>149.884元</p></td><td><p>224.826元</p></td></tr></tbody></table>

<a id="千问-livetranslate-flash"></a>

<a id="7369bdbb310x0"></a>

### 千问-LiveTranslate-Flash

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费说明](../model-experience/omni-modal/qwen3-livetranslate-flash.md#e02a82e668y2c)。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-76"></a>

<a id="华北2-北京-72"></a>

<a id="华北2-北京-72-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th colspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th colspan="2"><p><strong>输出单价（每百万Token）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr><tr><th><p><strong>输入：音频</strong></p></th><th><p><strong>输入：图片</strong></p></th><th><p><strong>输出：文本</strong></p></th><th><p><strong>输出：音频</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-livetranslate-flash</p></td><td><p>10元</p></td><td><p>4元</p></td><td><p>10元</p></td><td><p>40元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3-livetranslate-flash-2025-12-01</p></td><td><p>10元</p></td><td><p>4元</p></td><td><p>10元</p></td><td><p>40元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-39"></a>

<a id="新加坡-39-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th rowspan="2"><p><strong>服务部署范围</strong></p></th><th colspan="2"><p><strong>输入单价 (每百万 Token)</strong></p></th><th colspan="2"><p><strong>输出单价 (每百万 Token)</strong></p></th></tr><tr><th><p><strong>输入：音频</strong></p></th><th><p><strong>输入：图片</strong></p></th><th><p><strong>输出：文本</strong></p></th><th><p><strong>输出：音频</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-livetranslate-flash</p></td><td><p>国际</p></td><td><p>11.573元</p></td><td><p>4.629元</p></td><td><p>11.573元</p></td><td><p>46.292元</p></td></tr><tr><td><p>qwen3-livetranslate-flash-2025-12-01</p></td><td><p>国际</p></td><td><p>11.573元</p></td><td><p>4.629元</p></td><td><p>11.573元</p></td><td><p>46.292元</p></td></tr></tbody></table>

<a id="音色复刻-设计"></a>

<a id="voice-cloning-design-pricing"></a>

## 音色复刻/设计

<a id="qwen-tts声音复刻"></a>

<a id="76d95f2e25s8n"></a>

### Qwen-TTS声音复刻

计费规则：按新建音色个数计费。

创建失败不计费，也不占用免费次数；删除音色不会恢复免费次数。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-77"></a>

<a id="华北2-北京-73"></a>

<a id="华北2-北京-73-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 单价（每个音色） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| qwen-voice-enrollment | 0.01元 | 1000个音色/账号 |

<a id="新加坡-40"></a>

<a id="新加坡-40-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 单价（每个音色） |
| --- | --- | --- |
| qwen-voice-enrollment | 国际 | 0.01元 |

<a id="音乐生成"></a>

<a id="music-generation-pricing"></a>

<a id="35854be4db046"></a>

## 音乐生成

<a id="fun-music"></a>

<a id="fun-music-pricing"></a>

### Fun-Music

计费规则：按输出音频的秒数计费，输入不计费。

<a id="sec-tabs-78"></a>

<a id="华北2-北京-74"></a>

<a id="华北2-北京-74-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价（每秒） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| fun-music-preview | 0.005元 | 无 |
| fun-music-v1 | 0.002元 | 1,000秒 |

<a id="视频生成"></a>

<a id="d809366847gza"></a>

## 视频生成

<a id="happyhorse-文生视频"></a>

<a id="hh0005"></a>

### HappyHorse-文生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率（480P/720P/1080P）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-79"></a>

<a id="华北2-北京-75"></a>

<a id="华北2-北京-75-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-t2v</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td><td rowspan="3"><p>10秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-t2v</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-19"></a>

<a id="美国-弗吉尼亚-19-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-t2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-t2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="新加坡-41"></a>

<a id="新加坡-41-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-t2v</p></td><td rowspan="3"><p>国际</p></td><td><p>480P</p></td><td><p>0.524594元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.348956元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-t2v</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.798608元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-18"></a>

<a id="德国-法兰克福-18-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-t2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-t2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="日本-东京-10"></a>

<a id="日本-东京-10-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-t2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr></tbody></table>

<a id="happyhorse-图生视频-基于首帧"></a>

<a id="hh0067"></a>

### HappyHorse-图生视频-基于首帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率（480P/720P/1080P）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-80"></a>

<a id="华北2-北京-76"></a>

<a id="华北2-北京-76-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-i2v</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td><td rowspan="3"><p>10秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-i2v</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-20"></a>

<a id="美国-弗吉尼亚-20-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-i2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-i2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="新加坡-42"></a>

<a id="新加坡-42-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-i2v</p></td><td rowspan="3"><p>国际</p></td><td><p>480P</p></td><td><p>0.524594元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.348956元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-i2v</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.798608元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-19"></a>

<a id="德国-法兰克福-19-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-i2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-i2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="日本-东京-11"></a>

<a id="日本-东京-11-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-i2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr></tbody></table>

<a id="happyhorse-参考生视频"></a>

<a id="hh0129"></a>

### HappyHorse-参考生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率（480P/720P/1080P）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-81"></a>

<a id="华北2-北京-77"></a>

<a id="华北2-北京-77-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-r2v</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td><td rowspan="3"><p>10秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-r2v</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-21"></a>

<a id="美国-弗吉尼亚-21-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-r2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-r2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="新加坡-43"></a>

<a id="新加坡-43-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-r2v</p></td><td rowspan="3"><p>国际</p></td><td><p>480P</p></td><td><p>0.524594元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.348956元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-r2v</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.798608元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-20"></a>

<a id="德国-法兰克福-20-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-r2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td rowspan="2"><p>happyhorse-1.0-r2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="日本-东京-12"></a>

<a id="日本-东京-12-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>happyhorse-1.1-r2v</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr></tbody></table>

<a id="happyhorse-视频编辑"></a>

<a id="hh0190"></a>

### HappyHorse-视频编辑

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

计费规则：输入视频和输出视频均按**视频秒数**计费。

请求失败不产生费用，也不占用免费额度。

<a id="sec-tabs-82"></a>

<a id="华北2-北京-78"></a>

<a id="华北2-北京-78-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyhorse-1.0-video-edit</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td><td rowspan="2"><p>10秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-22"></a>

<a id="美国-弗吉尼亚-22-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyhorse-1.0-video-edit</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="新加坡-44"></a>

<a id="新加坡-44-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyhorse-1.0-video-edit</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>1.049188元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.798608元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-21"></a>

<a id="德国-法兰克福-21-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyhorse-1.0-video-edit</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="日本-东京-13"></a>

<a id="日本-东京-13-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyhorse-1.0-video-edit</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.6元/秒</p></td></tr></tbody></table>

<a id="万相3-0-视频生成"></a>

<a id="wan30video_cn_h3"></a>

### 万相3.0-视频生成

计费规则：输入视频和输出视频均按**视频秒数**计费。

请求失败不产生费用，也不占用免费额度。

计费公式：计费时长 = 输入视频时长 + 输出视频时长。

-   输入视频的计费时长为**实际输入的视频秒数**。
-   输出视频的计费时长为**成功生成的视频秒数**。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-83"></a>

<a id="华北2-北京-79"></a>

<a id="华北2-北京-79-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan3.0-video-prime</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.8元/秒</p></td></tr><tr><td rowspan="3"><p>wan3.0-video</p></td><td><p>480P</p></td><td><p>原价0.3元/秒<strong>（限时7折）</strong></p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>原价0.6元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价1.2元/秒<strong>（限时7折）</strong></p></td></tr></tbody></table>

<a id="新加坡-45"></a>

<a id="新加坡-45-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan3.0-video-prime</p></td><td rowspan="3"><p>国际</p></td><td><p>480P</p></td><td><p>0.495838元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>1.020844元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>2.041687元/秒</p></td></tr><tr><td rowspan="3"><p>wan3.0-video</p></td><td rowspan="3"><p>国际</p></td><td><p>480P</p></td><td><p>原价0.37471元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.74942元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价1.49884元/秒<strong>（限时7折）</strong></p></td></tr></tbody></table>

<a id="日本-东京-14"></a>

<a id="日本-东京-14-h4"></a>

#### 日本（东京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan3.0-video-prime</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.8元/秒</p></td></tr><tr><td rowspan="3"><p>wan3.0-video</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>原价0.3元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.6元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价1.2元/秒<strong>（限时7折）</strong></p></td></tr></tbody></table>

<a id="德国-法兰克福-22"></a>

<a id="德国-法兰克福-22-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan3.0-video-prime</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.8元/秒</p></td></tr><tr><td rowspan="3"><p>wan3.0-video</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>原价0.3元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.6元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价1.2元/秒<strong>（限时7折）</strong></p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-23"></a>

<a id="美国-弗吉尼亚-23-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan3.0-video-prime</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.8元/秒</p></td></tr><tr><td rowspan="3"><p>wan3.0-video</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>原价0.3元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.6元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价1.2元/秒<strong>（限时7折）</strong></p></td></tr></tbody></table>

<a id="中国香港-11"></a>

<a id="中国香港-11-h4"></a>

#### 中国香港

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan3.0-video-prime</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>0.45元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.8元/秒</p></td></tr><tr><td rowspan="3"><p>wan3.0-video</p></td><td rowspan="3"><p>全球</p></td><td><p>480P</p></td><td><p>原价0.3元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.6元/秒<strong>（限时7折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价1.2元/秒<strong>（限时7折）</strong></p></td></tr></tbody></table>

<a id="万相-文生视频"></a>

<a id="ba6f7744d5e0o"></a>

### 万相-文生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率（480P/720P/1080P）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-84"></a>

<a id="华北2-北京-80"></a>

<a id="华北2-北京-80-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-t2v-2026-06-12</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v-2026-04-25</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-t2v</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="3"><p>wan2.5-t2v-preview</p></td><td><p>480P</p></td><td><p>0.3元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.2-t2v-plus</p></td><td><p>480P</p></td><td><p>0.14元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.70元/秒</p></td></tr><tr><td rowspan="2"><p>wanx2.1-t2v-turbo</p></td><td><p>480P</p></td><td><p>0.24元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.24元/秒</p></td></tr><tr><td><p>wanx2.1-t2v-plus</p></td><td><p>720P</p></td><td><p>0.70元/秒</p></td><td><p>无</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-24"></a>

<a id="美国-弗吉尼亚-24-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.6-t2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-t2v</p></td><td rowspan="2"><p>美国</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr></tbody></table>

<a id="新加坡-46"></a>

<a id="新加坡-46-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-t2v-2026-06-12</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v-2026-04-25</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v-2026-06-12</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v-2026-04-25</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-t2v</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-t2v</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="3"><p>wan2.5-t2v-preview</p></td><td rowspan="3"><p>国际</p></td><td><p>480P</p></td><td><p>0.366961元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.733923元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100885元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.2-t2v-plus</p></td><td rowspan="2"><p>国际</p></td><td><p>480P</p></td><td><p>0.146785元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.1-t2v-turbo</p></td><td rowspan="2"><p>国际</p></td><td><p>480P</p></td><td><p>0.264213元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.264213元/秒</p></td></tr><tr><td><p>wan2.1-t2v-plus</p></td><td><p>国际</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-23"></a>

<a id="德国-法兰克福-23-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.6-t2v</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

<a id="万相-图生视频"></a>

<a id="e715eca061ba4"></a>

### 万相-图生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-85"></a>

<a id="华北2-北京-81"></a>

<a id="华北2-北京-81-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-i2v-2026-04-25</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-i2v</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

<a id="新加坡-47"></a>

<a id="新加坡-47-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-i2v-2026-04-25</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-i2v</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-i2v-2026-04-25</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-i2v</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr></tbody></table>

<a id="万相-图生视频-基于首帧"></a>

<a id="27fb5ee25b6gv"></a>

### 万相-图生视频-基于首帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率和视频类型（有声/无声）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-86"></a>

<a id="华北2-北京-82"></a>

<a id="华北2-北京-82-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="4"><p>wan2.6-i2v-flash</p></td><td rowspan="2"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>720P</p></td><td><p>0.3元/秒</p></td><td rowspan="4"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.5元/秒</p></td></tr><tr><td rowspan="2"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>720P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.25元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-i2v</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="3"><p>wan2.5-i2v-preview</p></td><td rowspan="3"><p>有声视频</p></td><td><p>480P</p></td><td><p>0.3元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="3"><p>wan2.2-i2v-flash</p></td><td rowspan="3"><p>无声视频</p></td><td><p>480P</p></td><td><p>0.10元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.20元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.48元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.2-i2v-plus</p></td><td rowspan="2"><p>无声视频</p></td><td><p>480P</p></td><td><p>0.14元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.70元/秒</p></td></tr><tr><td rowspan="2"><p>wanx2.1-i2v-turbo</p></td><td rowspan="2"><p>无声视频</p></td><td><p>480P</p></td><td><p>0.24元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.24元/秒</p></td></tr><tr><td><p>wanx2.1-i2v-plus</p></td><td><p>无声视频</p></td><td><p>720P</p></td><td><p>0.70元/秒</p></td><td><p>无</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-25"></a>

<a id="美国-弗吉尼亚-25-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.6-i2v</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-i2v</p></td><td rowspan="2"><p>美国</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr></tbody></table>

<a id="新加坡-48"></a>

<a id="新加坡-48-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>wan2.6-i2v-flash</p></td><td rowspan="4"><p>国际</p></td><td rowspan="2"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>720P</p></td><td><p>0.366962元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.550443元/秒</p></td></tr><tr><td rowspan="2"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>720P</p></td><td><p>0.183481元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.275221元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-i2v</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="3"><p>wan2.5-i2v-preview</p></td><td rowspan="3"><p>国际</p></td><td rowspan="3"><p>有声视频</p></td><td><p>480P</p></td><td><p>0.366961元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.733923元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100885元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.2-i2v-flash</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>无声视频</p></td><td><p>480P</p></td><td><p>0.110089元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.264213元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.2-i2v-plus</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>无声视频</p></td><td><p>480P</p></td><td><p>0.146785元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.1-i2v-turbo</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>无声视频</p></td><td><p>480P</p></td><td><p>0.264213元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.264213元/秒</p></td></tr><tr><td><p>wan2.1-i2v-plus</p></td><td><p>国际</p></td><td><p>无声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-24"></a>

<a id="德国-法兰克福-24-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.6-i2v</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

<a id="万相-图生视频-基于首尾帧"></a>

<a id="517789fb633zr"></a>

### 万相-图生视频-基于首尾帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-87"></a>

<a id="华北2-北京-83"></a>

<a id="华北2-北京-83-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="3"><p>wan2.2-kf2v-flash</p></td><td><p>480P</p></td><td><p>0.10元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.20元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.48元/秒</p></td></tr><tr><td><p>wanx2.1-kf2v-plus</p></td><td><p>720P</p></td><td><p>0.70元/秒</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-49"></a>

<a id="新加坡-49-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输出视频分辨率 | 输出单价 |
| --- | --- | --- | --- |
| wan2.2-kf2v-flash | 国际 | 480P | 0.110089元/秒 |
| wan2.2-kf2v-flash | 国际 | 720P | 0.264213元/秒 |
| wan2.2-kf2v-flash | 国际 | 1080P | 0.513747元/秒 |
| wan2.1-kf2v-plus | 国际 | 720P | 0.733924元/秒 |

<a id="万相-参考生视频"></a>

<a id="5c3d28ad8a4x8"></a>

### 万相-参考生视频

计费规则：输入视频和输出视频均按**视频秒数**计费。

请求失败不产生费用，也不占用免费额度。

计费公式：计费时长 = 输入视频时长（上限 5 秒）+ 输出视频时长。

-   输入视频的计费时长不超过 **5 秒**，计算规则参见[计费与限流](../../_short/video-to-video-guide-f63917cdae4414ac.md#6f5774ce5fqie)。
-   输出视频的计费时长为**成功生成的视频秒数**。

<a id="sec-tabs-88"></a>

<a id="华北2-北京-84"></a>

<a id="华北2-北京-84-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-r2v-2026-06-12</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-r2v</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr><tr><td rowspan="4"><p>wan2.6-r2v-flash</p></td><td rowspan="2"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>720P</p></td><td><p>0.3元/秒</p></td><td rowspan="4"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.5元/秒</p></td></tr><tr><td rowspan="2"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>720P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.25元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-r2v</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-26"></a>

<a id="美国-弗吉尼亚-26-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.6-r2v</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

<a id="新加坡-50"></a>

<a id="新加坡-50-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-r2v-2026-06-12</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-r2v</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-r2v-2026-06-12</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-r2v</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr><tr><td rowspan="4"><p>wan2.6-r2v-flash</p></td><td rowspan="4"><p>国际</p></td><td rowspan="2"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>720P</p></td><td><p>0.366962元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.550443元/秒</p></td></tr><tr><td rowspan="2"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>720P</p></td><td><p>0.183481元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.275221元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.6-r2v</p></td><td rowspan="2"><p>国际</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr></tbody></table>

<a id="德国-法兰克福-25"></a>

<a id="德国-法兰克福-25-h4"></a>

#### 德国（法兰克福）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.6-r2v</p></td><td rowspan="2"><p>全球</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

<a id="万相-视频编辑"></a>

<a id="89e9be041ek81"></a>

### 万相-视频编辑

> **说明**
>
> 以下模型所有地域均无免费额度。

计费规则：wan2.7-videoedit 的输入视频和输出视频均按**视频秒数**计费；wanx2.1-vace-plus 仅输出视频按**视频秒数**计费。

请求失败不产生费用，也不占用免费额度。

<a id="sec-tabs-89"></a>

<a id="华北2-北京-85"></a>

<a id="华北2-北京-85-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-videoedit</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1元/秒</p></td></tr></tbody></table>

| 模型 ID（Model ID） | 输出视频分辨率 | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| wanx2.1-vace-plus | 720P | 0.70元/秒 | 无 |

<a id="新加坡-51"></a>

<a id="新加坡-51-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.7-videoedit</p></td><td rowspan="2"><p>全球</p></td><td><p>720P</p></td><td><p>0.086012元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.143353元/秒</p></td></tr><tr><td rowspan="2"><p>wan2.7-videoedit</p></td><td rowspan="2"><p>国际</p></td><td><p>720P</p></td><td><p>0.733924元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.100886元/秒</p></td></tr></tbody></table>

| 模型 ID（Model ID） | 服务部署范围 | 输出视频分辨率 | 输出单价 |
| --- | --- | --- | --- |
| wan2.1-vace-plus | 国际 | 720P | 0.733924元/秒 |

<a id="万相-数字人"></a>

<a id="6fa00e4db0qlz"></a>

### 万相-数字人

-   wan2.2-s2v-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
-   wan2.2-s2v：输入不计费，输出按成功生成的视频秒数计费。不同输出视频分辨率（480P/720P）单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-90"></a>

<a id="华北2-北京-86"></a>

<a id="华北2-北京-86-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td><p>wan2.2-s2v-detect</p></td><td><p>输入图像：0.004元/张</p></td><td><p>无</p></td></tr><tr><td><p>wan2.2-s2v</p></td><td><p>输出视频：</p><ul><li><p>480P：0.5元/秒</p></li><li><p>720P：0.9元/秒</p></li></ul></td><td><p>无</p></td></tr></tbody></table>

<a id="万相-图生动作"></a>

<a id="1f708fcd62rdc"></a>

### 万相-图生动作

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频模式（标准模式/专业模式）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-91"></a>

<a id="华北2-北京-87"></a>

<a id="华北2-北京-87-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频模式</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.2-animate-move</p></td><td><p>标准模式<code>wan-std</code></p></td><td><p>0.4元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>专业模式<code>wan-pro</code></p></td><td><p>0.6元/秒</p></td></tr></tbody></table>

<a id="新加坡-52"></a>

<a id="新加坡-52-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频模式</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.2-animate-move</p></td><td rowspan="2"><p>国际</p></td><td><p>标准模式<code>wan-std</code></p></td><td><p>0.880709元/秒</p></td></tr><tr><td><p>专业模式<code>wan-pro</code></p></td><td><p>1.321063元/秒</p></td></tr></tbody></table>

<a id="万相-视频换人"></a>

<a id="86bd5c57adaos"></a>

### 万相-视频换人

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频模式（标准模式/专业模式）单价不同；请求失败不产生费用，也不消耗免费额度。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-92"></a>

<a id="华北2-北京-88"></a>

<a id="华北2-北京-88-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频模式</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.2-animate-mix</p></td><td><p>标准模式<code>wan-std</code></p></td><td><p>0.6元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>专业模式<code>wan-pro</code></p></td><td><p>0.9元/秒</p></td></tr></tbody></table>

<a id="新加坡-53"></a>

<a id="新加坡-53-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>输出视频模式</strong></p></th><th><p><strong>输出单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>wan2.2-animate-mix</p></td><td rowspan="2"><p>国际</p></td><td><p>标准模式<code>wan-std</code></p></td><td><p>1.321063元/秒</p></td></tr><tr><td><p>专业模式<code>wan-pro</code></p></td><td><p>1.908202元/秒</p></td></tr></tbody></table>

<a id="声动人像videoretalk"></a>

<a id="5835b4a956h6b"></a>

### 声动人像VideoRetalk

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

采用统一定价；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-93"></a>

<a id="华北2-北京-89"></a>

<a id="华北2-北京-89-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| videoretalk | 0.08元/秒 | 1800秒（30分钟） |

<a id="视频风格重绘"></a>

<a id="48d1e28e3esm4"></a>

### 视频风格重绘

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率（540P/720P）单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-94"></a>

<a id="华北2-北京-90"></a>

<a id="华北2-北京-90-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr></thead><tbody><tr><td rowspan="2"><p>video-style-transform</p></td><td><p>540P</p></td><td><p>0.2元/秒</p></td><td rowspan="2"><p>600秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.5元/秒</p></td></tr></tbody></table>

<a id="视频生成-第三方模型"></a>

<a id="44bb45add08er"></a>

## 视频生成-第三方模型

<a id="爱诗-文生视频"></a>

<a id="pxt002a0h3001"></a>

### 爱诗-文生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率和视频类型（有声/无声）单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-95"></a>

<a id="华北2-北京-91"></a>

<a id="华北2-北京-91-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="8"><p>pixverse/pixverse-v6-max-t2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>原价0.27元/秒<strong>（限时5折）</strong></p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>原价0.33元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.44元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价0.83元/秒<strong>（限时5折）</strong></p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>原价0.18元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>540P</p></td><td><p>原价0.27元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.33元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价0.65元/秒<strong>（限时5折）</strong></p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-c1-t2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.24元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.39元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.18元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.24元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.56元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v6-t2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.36元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.68元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.53元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v5.6-t2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.47元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.47元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.53元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.7元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.44元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v5.6-it2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.47元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.47元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.53元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.7元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.44元/秒</p></td></tr></tbody></table>

<a id="爱诗-图生视频-基于首帧"></a>

<a id="pxi002a0h3001"></a>

### 爱诗-图生视频-基于首帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率和视频类型（有声/无声）单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-96"></a>

<a id="华北2-北京-92"></a>

<a id="华北2-北京-92-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="8"><p>pixverse/pixverse-v6-max-it2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>原价0.27元/秒<strong>（限时5折）</strong></p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>原价0.33元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.44元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价0.83元/秒<strong>（限时5折）</strong></p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>原价0.18元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>540P</p></td><td><p>原价0.27元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>720P</p></td><td><p>原价0.33元/秒<strong>（限时5折）</strong></p></td></tr><tr><td><p>1080P</p></td><td><p>原价0.65元/秒<strong>（限时5折）</strong></p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-c1-it2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.24元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.39元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.18元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.24元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.56元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v6-it2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.36元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.68元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.53元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v5.6-it2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.47元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.47元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.53元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.7元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.44元/秒</p></td></tr></tbody></table>

<a id="爱诗-图生视频-基于首尾帧"></a>

<a id="pxk002a0h3001"></a>

### 爱诗-图生视频-基于首尾帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率和视频类型（有声/无声）单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-97"></a>

<a id="华北2-北京-93"></a>

<a id="华北2-北京-93-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="8"><p>pixverse/pixverse-c1-kf2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.24元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.39元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.18元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.24元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.56元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v6-kf2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.36元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.68元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.53元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v5.6-kf2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.47元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.47元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.53元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.7元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.44元/秒</p></td></tr></tbody></table>

<a id="爱诗-参考生视频"></a>

<a id="pxr002a0h3001"></a>

### 爱诗-参考生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输入参考类型、输出视频分辨率和视频类型（有声/无声）单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-98"></a>

<a id="华北2-北京-94"></a>

<a id="华北2-北京-94-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输入参考类型</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="16"><p>pixverse/pixverse-v6-r2v-omni</p></td><td rowspan="8"><p>有参考视频</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.42元/秒</p></td><td rowspan="16"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.54元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.72元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.36元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.42元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.54元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.06元/秒</p></td></tr><tr><td rowspan="8"><p>无参考视频</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.36元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.68元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.53元/秒</p></td></tr></tbody></table>

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="8"><p>pixverse/pixverse-v6-r2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.36元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.68元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.15元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.53元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-c1-r2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.24元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.39元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.18元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.24元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.3元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.56元/秒</p></td></tr><tr><td rowspan="8"><p>pixverse/pixverse-v5.6-r2v</p></td><td rowspan="4"><p>有声视频</p><p><code>audio=true</code></p></td><td><p>360P</p></td><td><p>0.47元/秒</p></td><td rowspan="8"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.47元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.53元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.7元/秒</p></td></tr><tr><td rowspan="4"><p>无声视频</p><p><code>audio=false</code></p></td><td><p>360P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>540P</p></td><td><p>0.21元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.27元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.44元/秒</p></td></tr></tbody></table>

<a id="爱诗-视频对口型"></a>

<a id="pxlipsync01h01"></a>

### 爱诗-视频对口型

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

采用统一定价；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-99"></a>

<a id="华北2-北京-95"></a>

<a id="华北2-北京-95-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[**（注）**](new-free-quota.md#977b13081ab56) |
| --- | --- | --- |
| pixverse/pixverse-lipsync | 0.12元/秒 | 无 |

<a id="爱诗-视频动作模仿"></a>

<a id="pxmctrl001h001"></a>

### 爱诗-视频动作模仿

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-100"></a>

<a id="华北2-北京-96"></a>

<a id="华北2-北京-96-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="3"><p>pixverse/pixverse-motioncontrol</p></td><td><p>360P</p></td><td><p>0.27元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>540P</p></td><td><p>0.30元/秒</p></td></tr><tr><td><p>720P</p></td><td><p>0.36元/秒</p></td></tr></tbody></table>

<a id="爱诗-视频超清"></a>

<a id="pxupscaleh3001"></a>

### 爱诗-视频超清

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

采用统一定价；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-101"></a>

<a id="华北2-北京-97"></a>

<a id="华北2-北京-97-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输出单价 | **免费额度**[**（注）**](new-free-quota.md#977b13081ab56) |
| --- | --- | --- |
| pixverse/pixverse-upscale | 0.15元/秒 | 无 |

<a id="可灵-视频生成"></a>

<a id="9cb8313752li4"></a>

### 可灵-视频生成

计费规则：无视频输入时，按成功生成的**视频秒数**计费。4.0 全能参考模型有视频输入时，计费时长为 max（输入视频总时长，生成视频时长）+ 生成视频时长。

不同模型、输出视频分辨率和参考视频使用情况的单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-102"></a>

<a id="华北2-北京-98"></a>

<a id="华北2-北京-98-h4"></a>

#### 华北2（北京）

**4.0 模型**

| 模型 ID | 输出视频类型 | 输出视频分辨率 | 计费单价 | 免费额度 |
| --- | --- | --- | --- | --- |
| kling/kling-v4-video-generation | 有声视频 | 720P | 1.0元/秒 | 无 |
| kling/kling-v4-video-generation | 有声视频 | 1080P | 1.5元/秒 | 无 |
| kling/kling-v4-omni-reference-video-generation | 有声视频（无参考视频） | 720P | 1.0元/秒 | 无 |
| kling/kling-v4-omni-reference-video-generation | 有声视频（无参考视频） | 1080P | 1.5元/秒 | 无 |
| kling/kling-v4-omni-reference-video-generation | 有声视频（有参考视频） | 720P | 0.6元/秒 | 无 |
| kling/kling-v4-omni-reference-video-generation | 有声视频（有参考视频） | 1080P | 0.9元/秒 | 无 |

**3.0 模型**

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频类型</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="2"><p>kling/kling-v3-turbo-video-generation</p></td><td rowspan="2"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.8元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>1.0元/秒</p></td></tr><tr><td rowspan="6"><p>kling/kling-v3-video-generation</p></td><td rowspan="3"><p>无声视频</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="6"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.8元/秒</p></td></tr><tr><td><p>4K</p></td><td><p>3.0元/秒</p></td></tr><tr><td rowspan="3"><p>有声视频</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td><p>4K</p></td><td><p>3.0元/秒</p></td></tr><tr><td rowspan="9"><p>kling/kling-v3-omni-video-generation</p></td><td rowspan="3"><p>无声视频（无参考视频）</p></td><td><p>720P</p></td><td><p>0.6元/秒</p></td><td rowspan="9"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.8元/秒</p></td></tr><tr><td><p>4K</p></td><td><p>3.0元/秒</p></td></tr><tr><td rowspan="3"><p>无声视频（有参考视频）</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td><p>4K</p></td><td><p>3.0元/秒</p></td></tr><tr><td rowspan="3"><p>有声视频（无参考视频）</p></td><td><p>720P</p></td><td><p>0.9元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>1.2元/秒</p></td></tr><tr><td><p>4K</p></td><td><p>3.0元/秒</p></td></tr></tbody></table>

<a id="vidu-文生视频"></a>

<a id="2143d64593wck"></a>

### Vidu-文生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-103"></a>

<a id="华北2-北京-99"></a>

<a id="华北2-北京-99-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="3"><p>vidu/viduq3-pro_text2video</p></td><td><p>540P</p></td><td><p>0.3125元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.78125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.9375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-turbo_text2video</p></td><td><p>540P</p></td><td><p>0.25元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.375元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.4375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2_text2video</p></td><td><p>540P</p></td><td><p>0.1125元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.21875元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.375元/秒</p></td></tr></tbody></table>

<a id="vidu-图生视频-基于首帧"></a>

<a id="e5d1761f12xq3"></a>

### Vidu-图生视频-基于首帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-104"></a>

<a id="华北2-北京-100"></a>

<a id="华北2-北京-100-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="2"><p>vidu/viduq3-pro-fast_img2video</p></td><td><p>720P</p></td><td><p>0.375元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.46875元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-pro_img2video</p></td><td><p>540P</p></td><td><p>0.3125元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.78125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.9375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-turbo_img2video</p></td><td><p>540P</p></td><td><p>0.25元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.375元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.4375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2-pro_img2video</p></td><td><p>540P</p></td><td><p>0.15625元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.34375元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71875元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2-turbo_img2video</p></td><td><p>540P</p></td><td><p>0.0875元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.25元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.46875元/秒</p></td></tr><tr><td rowspan="2"><p>vidu/viduq2-pro-fast_img2video</p></td><td><p>720P</p></td><td><p>0.1元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.2元/秒</p></td></tr></tbody></table>

<a id="vidu-图生视频-基于首尾帧"></a>

<a id="744137eff69v4"></a>

### Vidu-图生视频-基于首尾帧

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-105"></a>

<a id="华北2-北京-101"></a>

<a id="华北2-北京-101-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="3"><p>vidu/viduq3-pro_start-end2video</p></td><td><p>540P</p></td><td><p>0.3125元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.78125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.9375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-turbo_start-end2video</p></td><td><p>540P</p></td><td><p>0.25元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.375元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.4375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2-pro_start-end2video</p></td><td><p>540P</p></td><td><p>0.15625元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.34375元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71875元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2-turbo_start-end2video</p></td><td><p>540P</p></td><td><p>0.0875元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.25元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.46875元/秒</p></td></tr></tbody></table>

<a id="vidu-参考生视频"></a>

<a id="69993500dc6mi"></a>

### Vidu-参考生视频

计费规则：输入不计费，输出按成功生成的**视频秒数**计费。

不同输出视频分辨率单价不同；请求失败不产生费用，也不消耗免费额度。

<a id="sec-tabs-106"></a>

<a id="华北2-北京-102"></a>

<a id="华北2-北京-102-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="2"><p>vidu/viduq3-ad_reference2video</p></td><td><p>720P</p></td><td><p>0.75元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.90625元/秒</p></td></tr><tr><td rowspan="2"><p>vidu/viduq3-drama_reference2video</p></td><td><p>720P</p></td><td><p>0.875元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>1080P</p></td><td><p>0.875元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-mix_reference2video</p></td><td><p>540P</p></td><td><p>0.46875元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.78125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.9375元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3_reference2video</p></td><td><p>540P</p></td><td><p>0.3125元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.625元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.78125元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq3-turbo_reference2video</p></td><td><p>540P</p></td><td><p>0.15625元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.3125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.40625元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2-pro_reference2video</p></td><td><p>540P</p></td><td><p>0.25元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.3125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.78125元/秒</p></td></tr><tr><td rowspan="3"><p>vidu/viduq2_reference2video</p></td><td><p>540P</p></td><td><p>0.21875元/秒</p></td><td rowspan="3"><p>无</p></td></tr><tr><td><p>720P</p></td><td><p>0.28125元/秒</p></td></tr><tr><td><p>1080P</p></td><td><p>0.71875元/秒</p></td></tr></tbody></table>

<a id="minimax-视频生成"></a>

<a id="mmh3bill02h3"></a>

### MiniMax-视频生成

计费规则：输入按图像张数和视频秒数计费，输出按成功生成的视频秒数计费。

其中，`计费视频秒数=输入视频秒数+输出视频秒数`，价格由输出视频分辨率决定。

<a id="sec-tabs-107"></a>

<a id="华北2-北京-103"></a>

<a id="华北2-北京-103-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输出视频分辨率</strong></p></th><th><p><strong>输入和输出视频单价</strong></p></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56"><strong>（注）</strong></a></p></th></tr></thead><tbody><tr><td rowspan="2"><p>MiniMax/MiniMax-H3</p></td><td><p>2K</p></td><td><p>0.80元/秒</p></td><td rowspan="2"><p>无</p></td></tr><tr><td><p>768P</p></td><td><p>0.50元/秒</p></td></tr></tbody></table>

**输入素材价格**

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输入素材类型</strong></p></th><th><p><strong>输入价格</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>MiniMax/MiniMax-H3</p></td><td><p>音频</p></td><td><p>免费</p></td></tr><tr><td><p>图片</p></td><td><p>5张以内免费，超出部分 0.20 元/张</p></td></tr><tr><td><p>视频</p></td><td><p>价格由输出视频分辨率决定，见上方表格</p></td></tr></tbody></table>

<a id="世界模型"></a>

<a id="ho_world_model_h2"></a>

## 世界模型

<a id="happyoyster-世界探索-adventure"></a>

<a id="ho_adventure_pricing"></a>

### HappyOyster-世界探索（Adventure）

计费规则：

-   世界创建：按世界创建次数计费，`费用 = 世界创建次数 × 单价`。
-   世界体验：按输出视频时长（秒）计费，`费用 = 视频时长 × 单价`，仅支持 480P。
-   请求失败不产生任何费用。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-108"></a>

<a id="华北2-北京-104"></a>

<a id="华北2-北京-104-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyoyster-1.0-adventure</p></td><td><p>世界创建</p></td><td><p>0.05元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.2元/秒</p></td></tr></tbody></table>

<a id="新加坡-54"></a>

<a id="新加坡-54-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyoyster-1.0-adventure</p></td><td rowspan="2"><p>国际</p></td><td><p>世界创建</p></td><td><p>0.056146398元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.224586元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-27"></a>

<a id="美国-弗吉尼亚-27-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>happyoyster-1.0-adventure</p></td><td rowspan="2"><p>全球</p></td><td><p>世界创建</p></td><td><p>0.05元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.2元/秒</p></td></tr></tbody></table>

<a id="happyoyster-实时导演-directing"></a>

<a id="ho_directing_pricing"></a>

### HappyOyster-实时导演（Directing）

计费规则：

-   世界创建：按世界创建次数计费，`费用 = 世界创建次数 × 单价`。是否使用参考图影响单价：无参考图与有参考图分别计价。
-   指令注入：按注入的指令次数计费，`费用 = 指令次数 × 单价`。
-   世界体验：按输出视频时长（秒）计费，`费用 = 视频时长 × 单价`，不同分辨率（480P/720P）单价有差异。
-   请求失败不产生任何费用。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-109"></a>

<a id="新加坡-55"></a>

<a id="新加坡-55-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>happyoyster-1.0-directing</p></td><td rowspan="5"><p>国际</p></td><td><p>世界创建（无参考图）</p></td><td><p>2.269918662元/次</p></td></tr><tr><td><p>世界创建（有参考图）</p></td><td><p>0.056146398元/次</p></td></tr><tr><td><p>指令注入</p></td><td><p>0.112292796元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.393025元/秒</p></td></tr><tr><td><p>世界体验（720P）</p></td><td><p>0.625631元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-28"></a>

<a id="美国-弗吉尼亚-28-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>happyoyster-1.0-directing</p></td><td rowspan="5"><p>全球</p></td><td><p>世界创建（无参考图）</p></td><td><p>2元/次</p></td></tr><tr><td><p>世界创建（有参考图）</p></td><td><p>0.05元/次</p></td></tr><tr><td><p>指令注入</p></td><td><p>0.1元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.35元/秒</p></td></tr><tr><td><p>世界体验（720P）</p></td><td><p>0.55元/秒</p></td></tr></tbody></table>

<a id="happyoyster-角色演绎-acting"></a>

<a id="ho_acting_pricing"></a>

### HappyOyster-角色演绎（Acting）

计费规则：

-   世界创建：按世界创建次数计费，`费用 = 世界创建次数 × 单价`。
-   指令注入：按注入的指令次数计费，`费用 = 指令次数 × 单价`。
-   世界体验：按输出视频时长（秒）计费，`费用 = 视频时长 × 单价`，不同分辨率（480P/720P）单价有差异。
-   请求失败不产生任何费用。

> **说明**
>
> 以下模型所有地域均无免费额度。

<a id="sec-tabs-110"></a>

<a id="新加坡-56"></a>

<a id="新加坡-56-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>happyoyster-1.0-acting<br>（邀测中）</p></td><td rowspan="4"><p>国际</p></td><td><p>世界创建</p></td><td><p>0.056146398元/次</p></td></tr><tr><td><p>指令注入</p></td><td><p>0.056146398元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.224586元/秒</p></td></tr><tr><td><p>世界体验（720P）</p></td><td><p>0.336878元/秒</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-29"></a>

<a id="美国-弗吉尼亚-29-h4"></a>

#### 美国（弗吉尼亚）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>服务部署范围</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>单价</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>happyoyster-1.0-acting<br>（邀测中）</p></td><td rowspan="4"><p>全球</p></td><td><p>世界创建</p></td><td><p>0.05元/次</p></td></tr><tr><td><p>指令注入</p></td><td><p>0.05元/次</p></td></tr><tr><td><p>世界体验（480P）</p></td><td><p>0.2元/秒</p></td></tr><tr><td><p>世界体验（720P）</p></td><td><p>0.3元/秒</p></td></tr></tbody></table>

<a id="3d模型生成-第三方模型"></a>

<a id="trp002a0h2001"></a>

## 3D模型生成-第三方模型

**Tripo-3D模型生成**

计费规则：输入不计费，输出按次计费，价格以积分计，**`1积分 = 0.07元`**。

计费公式：`费用 = （基础项积分 + 所开启附加项的积分之和）× 0.07元`。

-   基础项：每次调用只计其中一项，动画重定向按动画个数计费。
-   附加项：按需开启，可同时开启多项，每项在基础项积分上累加计费；没有附加项或未开启时仅计基础项积分。

计费示例：

-   仅基础项：使用Tripo-H3.1文生3D生成白模，费用 = 10 × 0.07元 = 0.7元。
-   基础项+附加项：使用Tripo-H3.1单图生3D，带高清贴图（4K）和四边面网格，费用 = （20 + 20 + 5）× 0.07元 = 3.15元。

<a id="sec-tabs-111"></a>

<a id="华北2-北京-105"></a>

<a id="华北2-北京-105-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>计费类型</strong></p></th><th><p><strong>计费项</strong></p></th><th><p><strong>消耗积分</strong></p></th></tr></thead><tbody><tr><td rowspan="10"><p>Tripo/Tripo-H3.1</p></td><td rowspan="3"><p>基础项</p></td><td><p>文生3D（不含贴图）</p></td><td><p>10积分/次</p></td></tr><tr><td><p>单图生3D（不含贴图）</p></td><td><p>20积分/次</p></td></tr><tr><td><p>多图生3D（不含贴图）</p></td><td><p>20积分/次</p></td></tr><tr><td rowspan="7"><p>附加项</p></td><td><p>标准贴图（2K）</p></td><td><p>10积分/次</p></td></tr><tr><td><p>高清贴图（4K）</p></td><td><p>20积分/次</p></td></tr><tr><td><p>超清贴图（8K）</p></td><td><p>30积分/次</p></td></tr><tr><td><p>高精度几何（Ultra）</p></td><td><p>20积分/次</p></td></tr><tr><td><p>四边面网格</p></td><td><p>5积分/次</p></td></tr><tr><td><p>智能低模</p></td><td><p>10积分/次</p></td></tr><tr><td><p>分部件生成</p></td><td><p>20积分/次</p></td></tr><tr><td rowspan="6"><p>Tripo/Tripo-P1.0</p></td><td rowspan="3"><p>基础项</p></td><td><p>文生3D（不含贴图）</p></td><td><p>30积分/次</p></td></tr><tr><td><p>单图生3D（不含贴图）</p></td><td><p>40积分/次</p></td></tr><tr><td><p>多图生3D（不含贴图）</p></td><td><p>40积分/次</p></td></tr><tr><td rowspan="3"><p>附加项</p></td><td><p>标准贴图（2K）</p></td><td><p>10积分/次</p></td></tr><tr><td><p>高清贴图（4K）</p></td><td><p>20积分/次</p></td></tr><tr><td><p>超清贴图（8K）</p></td><td><p>30积分/次</p></td></tr><tr><td><p>Tripo/Tripo-ImageToSplat</p></td><td><p>基础项</p></td><td><p>图片生成Gaussian Splat</p></td><td><p>30积分/次</p></td></tr><tr><td rowspan="3"><p>Tripo/Tripo-Texture</p></td><td rowspan="3"><p>基础项</p></td><td><p>标准贴图（2K）</p></td><td><p>10积分/次</p></td></tr><tr><td><p>高清贴图（4K）</p></td><td><p>20积分/次</p></td></tr><tr><td><p>超清贴图（8K）</p></td><td><p>30积分/次</p></td></tr><tr><td><p>Tripo/Tripo-Segmentation</p></td><td><p>基础项</p></td><td><p>网格分割</p></td><td><p>40积分/次</p></td></tr><tr><td rowspan="2"><p>Tripo/Tripo-SmartSegmentation</p></td><td rowspan="2"><p>基础项</p></td><td><p>智能分割（图片输入）</p></td><td><p>85积分/次</p></td></tr><tr><td><p>智能分割（模型输入）</p></td><td><p>55积分/次</p></td></tr><tr><td rowspan="2"><p>Tripo/Tripo-MeshCompletion</p></td><td rowspan="2"><p>基础项</p></td><td><p>AI补全</p></td><td><p>50积分/次</p></td></tr><tr><td><p>快速封口</p></td><td><p>30积分/次</p></td></tr><tr><td rowspan="2"><p>Tripo/Tripo-Retopology</p></td><td rowspan="2"><p>基础项</p></td><td><p>重拓扑v1.0（基础）</p></td><td><p>10积分/次</p></td></tr><tr><td><p>重拓扑v2.0（智能）</p></td><td><p>30积分/次</p></td></tr><tr><td rowspan="2"><p>Tripo/Tripo-ConvertFormat</p></td><td rowspan="2"><p>基础项</p></td><td><p>基础转换</p></td><td><p>5积分/次</p></td></tr><tr><td><p>高级转换</p></td><td><p>10积分/次</p></td></tr><tr><td><p>Tripo/Tripo-RigCheck</p></td><td><p>基础项</p></td><td><p>可绑骨检查</p></td><td><p>不计费</p></td></tr><tr><td><p>Tripo/Tripo-AutoRig</p></td><td><p>基础项</p></td><td><p>绑骨</p></td><td><p>25积分/次</p></td></tr><tr><td><p>Tripo/Tripo-AnimationRetarget</p></td><td><p>基础项</p></td><td><p>动画重定向</p></td><td><p>10积分/个动画</p></td></tr></tbody></table>

<a id="文本向量"></a>

<a id="deb2215af9b2h"></a>

## 文本向量

计费规则：按输入Token计费，输出不计费。

影响计费的因素：若模型支持[Batch调用](../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其输入和输出Token单价均按实时推理价格的50%计费。

<a id="sec-tabs-112"></a>

<a id="华北2-北京-106"></a>

<a id="华北2-北京-106-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen3.7-text-embedding-flash</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.125元</p></td><td><p>100万Token</p></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>text-embedding-v3</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote><blockquote><p>免费额度用完后不可调用，推荐使用 text-embedding-v4 作为替代模型，免费额度提升至 100 万 Token</p></blockquote></td><td><p>0.5元</p></td><td><p>无</p></td></tr><tr><td><p>text-embedding-v2</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.7元</p></td><td><p>无</p></td></tr><tr><td><p>text-embedding-v1</p><blockquote><p><a href="../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>半价</p></blockquote></td><td><p>0.7元</p></td><td><p>无</p></td></tr><tr><td><p>text-embedding-async-v2</p></td><td><p>0.7元</p></td><td><p>2000万Token</p></td></tr><tr><td><p>text-embedding-async-v1</p></td><td><p>0.7元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-57"></a>

<a id="新加坡-57-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） |
| --- | --- | --- |
| qwen3.7-text-embedding | 国际 | 0.525元 |
| text-embedding-v4 | 国际 | 0.514元 |
| text-embedding-v3 | 国际 | 0.514元 |

<a id="中国香港-12"></a>

<a id="中国香港-12-h4"></a>

#### 中国香港

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） |
| --- | --- | --- |
| text-embedding-v4 | 中国香港 | 0.51元 |

<a id="多模态向量"></a>

<a id="19778fa59fk8d"></a>

## 多模态向量

计费规则：按输入Token计费，输出不计费。

<a id="sec-tabs-113"></a>

<a id="华北2-北京-107"></a>

<a id="华北2-北京-107-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>模型 ID（Model ID）</strong></p></th><th colspan="2"><p><strong>输入单价（每百万Token）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p><p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</p></th></tr><tr><th><p><strong>文本</strong></p></th><th><p><strong>图片/视频</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-vl-embedding</p></td><td><p>0.7元</p></td><td><p>1.8元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>0.7元</p></td><td><p>1.8元</p></td><td><p>无</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>0.5元</p></td><td><p>0.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>0.15元</p></td><td><p>0.15元</p></td><td><p>100万Token</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>0.7元</p></td><td><p>0.9元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="排序模型"></a>

<a id="fe63c4ef79t02"></a>

## 排序模型

<a id="文本排序模型"></a>

<a id="1b5bd6eddbdau"></a>

### 文本排序模型

计费规则：按输入Token计费，输出不计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-114"></a>

<a id="华北2-北京-108"></a>

<a id="华北2-北京-108-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- |
| qwen3.7-text-rerank | 文本输入：0.5元 | 100万Token |
| qwen3-vl-rerank | 文本输入：0.5元<br><br>图片输入：0.5元 | 100万Token |
| qwen3-rerank | 文本输入：0.5元 | 100万Token |
| gte-rerank-v2 | 文本输入：0.8元 | 无 |

<a id="新加坡-58"></a>

<a id="新加坡-58-h4"></a>

#### 新加坡

| 模型 ID（Model ID） | 服务部署范围 | 输入单价（每百万Token） |
| --- | --- | --- |
| qwen3-rerank | 国际 | 0.74942元 |

<a id="行业模型"></a>

<a id="f2bd458abcy0f"></a>

## 行业模型

<a id="意图理解"></a>

<a id="25eee85f08ptr"></a>

### 意图理解

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-115"></a>

<a id="华北2-北京-109"></a>

<a id="华北2-北京-109-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| tongyi-intent-detect-v3 | 0.4元 | 1元 | 100万Token |

<a id="角色扮演"></a>

<a id="083f31bde1lv3"></a>

### 角色扮演

计费规则：按输入Token和输出Token计费。

> **说明**
>
> 以下模型仅在华北2（北京）地域下有免费额度，其他地域均无免费额度。

<a id="sec-tabs-116"></a>

<a id="华北2-北京-110"></a>

<a id="华北2-北京-110-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>输入单价（每百万Token）</strong></th><th><strong>输出单价（每百万Token）</strong></th><th><p><strong>免费额度</strong><a href="new-free-quota.md#977b13081ab56">（注）</a></p>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）</th></tr></thead><tbody><tr><td><p>qwen-plus-character</p><blockquote><p><a href="../model-experience/text-generation-model/specialized-models/role-play.md#6034f997cde74">Session Cache</a>享有折扣</p></blockquote></td><td><p>0.8元</p></td><td><p>2元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen-flash-character</p><blockquote><p><a href="../model-experience/text-generation-model/specialized-models/role-play.md#6034f997cde74">Session Cache</a>享有折扣</p></blockquote></td><td><p>0.25元</p></td><td><p>1.5元</p></td><td><p>100万Token</p></td></tr><tr><td><p>qwen-flash-character-2026-02-26</p><blockquote><p><a href="../model-experience/text-generation-model/specialized-models/role-play.md#6034f997cde74">Session Cache</a>享有折扣</p></blockquote></td><td><p>0.18元</p></td><td><p>1.5元</p></td><td><p>无</p></td></tr></tbody></table>

<a id="新加坡-59"></a>

<a id="新加坡-59-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>服务部署范围</strong></th><th><strong>输入单价 （每百万Token）</strong></th><th><strong>输出单价 （每百万Token）</strong></th></tr></thead><tbody><tr><td><p>qwen-plus-character</p><blockquote><p><a href="../model-experience/text-generation-model/specialized-models/role-play.md#6034f997cde74">Session Cache</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>3.747元</p></td><td><p>10.492元</p></td></tr><tr><td><p>qwen-flash-character</p><blockquote><p><a href="../model-experience/text-generation-model/specialized-models/role-play.md#6034f997cde74">Session Cache</a>享有折扣</p></blockquote></td><td><p>国际</p></td><td><p>0.375元</p></td><td><p>2.998元</p></td></tr><tr><td><p>qwen-plus-character-ja</p></td><td><p>国际</p></td><td><p>3.67元</p></td><td><p>10.275元</p></td></tr></tbody></table>

<a id="美国-弗吉尼亚-30"></a>

<a id="美国-弗吉尼亚-30-h4"></a>

#### 美国（弗吉尼亚）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-plus-character | 全球 | 0.8元 | 2元 |
| qwen-flash-character | 全球 | 0.25元 | 1.5元 |

<a id="德国-法兰克福-26"></a>

<a id="德国-法兰克福-26-h4"></a>

#### 德国（法兰克福）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-plus-character | 全球 | 0.8元 | 2元 |

<a id="日本-东京-15"></a>

<a id="日本-东京-15-h4"></a>

#### 日本（东京）

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-plus-character | 全球 | 0.8元 | 2元 |

<a id="中国香港-13"></a>

<a id="中国香港-13-h4"></a>

#### 中国香港

| 模型 ID（Model ID） | 服务部署范围 | 输入单价 （每百万Token） | 输出单价 （每百万Token） |
| --- | --- | --- | --- |
| qwen-plus-character | 全球 | 0.8元 | 2元 |

<a id="界面交互"></a>

<a id="2e5414fed4wnw"></a>

### 界面交互

计费规则：按输入Token和输出Token计费。

<a id="sec-tabs-117"></a>

<a id="华北2-北京-111"></a>

<a id="华北2-北京-111-h4"></a>

#### 华北2（北京）

| 模型 ID（Model ID） | 输入单价（每百万Token） | 输出单价（每百万Token） | **免费额度**[（注）](new-free-quota.md#977b13081ab56)<br><br>有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准） |
| --- | --- | --- | --- |
| gui-plus | 1.5元 | 4.5元 | 100万Token |
| gui-plus-2026-02-26 | 1.5元 | 4.5元 | 无 |

<a id="决策模型"></a>

<a id="dm-pricing"></a>

### 决策模型

计费规则：按输入token计费。

<a id="sec-tabs-118"></a>

<a id="华北2-北京-112"></a>

<a id="华北2-北京-112-h4"></a>

#### 华北2（北京）

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输入单价（每百万Token）</strong></p></th><th><p><strong>免费额度</strong></p></th></tr></thead><tbody><tr><td><p>decision-model-preview</p></td><td colspan="2"><p>限时免费</p></td></tr></tbody></table>

<a id="新加坡-60"></a>

<a id="新加坡-60-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型 ID（Model ID）</strong></p></th><th><p><strong>输入单价（每百万Token）</strong></p></th><th><p><strong>免费额度</strong></p></th></tr></thead><tbody><tr><td><p>decision-model-preview</p></td><td colspan="2"><p>限时免费</p></td></tr></tbody></table>

<a id="token-消耗与成本控制"></a>

<a id="h2-token-cost"></a>

## Token 消耗与成本控制

**通过 URL 读取文件的计费方式**：通过 URL 读取文件时，文件传输过程本身不消耗 Token；文件内容解析后转化为输入 Token 计费，消耗量取决于解析后的文本长度，而不是文件大小。如果需要处理大文件，建议使用知识库切片索引以降低 Token 消耗。

**单次请求 Credits 消耗异常高时如何排查**：常见原因包括输入 Token 量过大、启用 Agent 模式（会产生大量 system prompt、工具定义及思考内容开销）等。可通过以下方式优化成本：压缩历史消息、新开对话、关闭思考模式，或切换至轻量模型（如 Flash 系列）。

**低频调用场景的模型推荐**：针对心跳检测等低频调用场景，推荐使用 Qwen Flash 系列等低价模型，以降低整体调用成本。

**已下线模型说明**：Qwen2.5 系列等已下线模型不再可用，也无法查询价格，请使用新版模型替代。

<a id="错误码"></a>

<a id="mp-errcode-h2"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../model-api-reference/preparations/error-code.md)进行解决。

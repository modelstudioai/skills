# 智能路由

智能路由是一种通过动态分析用户请求内容，在模型备选集中自动匹配最合适模型进行处理，帮助企业在复杂场景中实现 AI 资源的最优配置。

## 概述

智能路由的 model-code 固定为 `auto-model` 前缀，后接 8 位随机字符（如 `auto-model-abcd1234`）。客户端通过该 model-code 发起请求 → 路由服务动态分析请求内容并从备选集中自动匹配最合适的模型 → 实际模型推理 → 响应返回（`x-dashscope-resolved-model` 标注实际模型，保留真实 token 用量）。

**适用范围**：

维度

说明

地域

北京（`cn-beijing`）+ 新加坡（`ap-southeast-1`）

模型类型

仅文本输入

调用协议

仅 OpenAI 兼容接口（不支持 DashScope 协议）

访问域名

仅支持 `maas.aliyuncs.com`（`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，region 为 `cn-beijing` 或 `ap-southeast-1`），不支持 `dashscope.aliyuncs.com`（含 compatible-mode）

计费

按量计费

限流

按实际路由模型在账号和业务空间限流

**主要优势**：

-   **最大化模型效果**：针对不同任务自动匹配最优模型，尤其适配对效果有极致需求的用户。
-   **精准降低成本**：简单任务自动路由至轻量模型，复杂任务匹配高阶模型，避免「大材小用」的资源浪费，实现成本与需求的精准适配。
-   **化解模型选择难题**：无需用户手动开展复杂的模型评测与对比，平台全程自动筛选最优解，大幅降低模型选型门槛。
-   **极简使用体验**：与常规模型接入流程完全一致，通过 model-code 即可调用，无需额外修改代码。

## 创建智能路由

在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)「模型推理 > 专属部署」下，点击「**部署新模型**」进入创建页，在「部署模式」中选择「**智能路由**」创建。

### 前提条件

-   已开通百炼工作空间。
-   目标路由模型版本已发布，且当前账号已开通该版本及备选模型的调用权限。

### 操作步骤

1.  填写**服务名称**（必填，最长 50 字符）。
2.  在**部署模式**中选择「智能路由」。
3.  在**路由模型版本**下拉中选择一个已发布版本（由平台维护）。
4.  在**路由策略**中选择「效果优先」或「成本优先」。
5.  在**模型备选集**中勾选备选模型（至少 2 个）。
6.  点击**确认部署**完成创建。

部署成功后系统生成全局唯一的 `model-code`（形如 `auto-model-XXXXXXXX`），客户端以该 `model-code` 发起调用。`model-code` 删除后不复用。

### 路由策略

路由策略决定每条请求由备选模型集内哪个模型执行。两种策略均按请求内容动态匹配（非固定路由），创建时选定。

**策略**

**选模机制**

**适用场景**

效果优先（EFFECT\_FIRST）

每条请求选备选集内效果最强的模型

关键业务、复杂推理、高质量内容生成等质量要求严苛的场景

成本优先（COST\_FIRST）

在满足效果下限前提下智能调度轻量级模型

成本敏感、高并发、对延迟与单位成本更关注的场景

### 备选模型配置

备选模型集是路由服务选模时可挑选的范围。创建智能路由时，在「**模型备选集**」区域从备选列表中勾选参与路由的模型，**至少选择 2 个备选模型**，否则无法部署。

**说明**RAM 用户只能勾选其已获

**模型调用权限**的备选模型——可勾选项不足 2 个时，需先在该业务空间为该 RAM 用户补充模型调用授权。

路由模型版本是智能路由能力的标准化发布形态，每个版本明确了对应阶段下路由系统支持的模型范围与核心能力。 备选模型清单由所选路由模型版本决定——每个版本对应一组备选集，不能跨版本组合。 当前已发布的路由模型版本及备选模型如下：

#### model-router-2026-0908

**备选模型**

**上下文**

**输入价**

**输出价**

**缓存命中输入价**

`qwen3.8-max`

1M

12

36

1.5

`qwen3.8-flash`

1M

0.8

2.7

0.1

`qwen3.7-plus`

1M

2

8

0.4

`qwen3.7-flash`

1M

0.2

0.8

0.04

`qwen3.7-max`

1M

12

36

2.4

`deepseek-v4-pro-0813`

1M

9

27

0.9

`deepseek-v4-flash-0731`

1M

3

9

0.3

`kimi-k3`

1M

20

100

2

`glm-5.2`

1M

8

28

2

价格单位：元/百万tokens。deepseek-v4 系列采用忙时/闲时分时计费，上表为忙时价格。所有备选模型支持思考模式，思考 token 按输出价格计费。

**说明**选择备选模型时需注意各备选模型的配额限制，避免路由到备选模型由于配额不足导致被限流。建议选择配额充足的模型作为备选，或在创建前为账号提升相应模型的 RPM/TPM 额度。

## 调用智能路由

智能路由创建后，调用方式与普通模型一致——仅需将请求中的 `model` 参数替换为智能路由的 `model-code`（如 `auto-model-abcd1234`），客户端零代码改动接入。

调用示例：

curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-model-abcd1234",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

OpenAI SDK

```
# OpenAI SDK
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DASHSCOPE_API_KEY",
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
resp = client.chat.completions.create(
    model="auto-model-abcd1234",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
print(resp.model)  # 实际执行的模型名
```

DashScope SDK

```
# DashScope SDK（需先安装 pip install dashscope）
# 智能路由仅支持 maas.aliyuncs.com 域名，需配置 DASHSCOPE_HTTP_BASE_URL
import os
os.environ['DASHSCOPE_HTTP_BASE_URL'] = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
from dashscope import Generation

resp = Generation.call(
    model="auto-model-abcd1234",
    api_key="YOUR_DASHSCOPE_API_KEY",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.output.choices[0].message.content)
```

Node.js

```
// OpenAI SDK
使用 OpenAI SDK（需先安装 npm install openai）

const OpenAI = require("openai");

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});
const resp = await client.chat.completions.create({
  model: "auto-model-abcd1234",
  messages: [{ role: "user", content: "你好" }],
});
console.log(resp.choices[0].message.content);
console.log(resp.model); // 实际执行的模型名
```

**响应**：响应头 `x-dashscope-resolved-model` 值为实际调用模型的标识，可验证路由是否生效；响应体保留实际执行模型名与真实 token 用量，计费按实际路由到的模型。

**计费**：按实际路由到的模型计费，智能路由服务本身暂不收费。

### 故障自动切换

智能路由内置故障自动切换，默认启用、无需配置。目标模型不可用时，路由服务用备选集内其他模型重新发起整个请求，不在推理中途切换。

以下情况不触发故障自动切换，错误直接透出实际模型的原始信息：

-   429（限流）
-   400/403/404/500 等确定性错误（换模型大概率同样失败）
-   超时或网络异常
-   流式已开始返回内容后出错

**说明**故障自动切换不重复计费：模型 A → 故障自动切换 → 模型 B 成功，只计模型 B 费用。

### 实时过滤规则

路由服务对备选集做实时过滤：

-   过滤当前账号无调用权限的模型。
-   过滤已下线的模型。
-   过滤与当前请求参数不兼容的模型（如请求携带 `response_format`，则只路由到支持该参数的备选模型）。

单条请求实际可选的子集随权限、模型状态与请求参数动态变化。

## 使用限制

限制项

说明

调用协议

仅 OpenAI 兼容接口（不支持 DashScope 协议）

请求类型

仅支持文本 Chat Completions 输入；不支持图片、视频输入、图像生成（文生图）、Batch 批量推理、Embedding/Rerank 等非生成接口

上下文长度

上限 = 备选集内模型的最小上下文窗口；超长直接报错，不触发故障自动切换

限流

按实际路由模型在账号和业务空间的 RPM/TPM 限流；故障自动切换时只计最终成功模型的消耗

协议支持明细：

协议

支持

OpenAI 兼容接口（Chat Completions）

✓

DashScope 协议

✗

Anthropic 协议

✗

### 参数说明

-   `response_format`：只路由到支持该参数的备选模型。
-   `enable_search`：只路由到支持该参数的备选模型。
-   `reasoning_effort`：默认仅路由到支持该参数的备选模型，该参数仅支持 `none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max` 枚举值。
-   `enable_thinking`：设置为 `false` 关闭思考，倾向选择 non-thinking 模型；设置为 `true` 自动排除 non-thinking 模型并自动开启 thinking。
-   `max_tokens`：设置后会**自动转换为 `max_completion_tokens` 参数**传递给备选模型，路由时**仅选择支持 `max_completion_tokens` 参数的备选模型**。

在智能路由模式下，以下参数不支持使用，设置会导致运行报错：

参数

说明

`top_logprobs`

限制返回 logprobs 数量

`logit_bias`

token 偏置

`stop`

停止序列

`tool_choice`

工具选择

`parallel_tool_calls`

并行工具调用

`logprobs`

是否返回 logprobs

`top_p`

核采样

`temperature`

采样温度

`presence_penalty`

存在惩罚

`n`

生成数量

`thinking_budget`

思考预算长度

### 缓存

智能路由不支持显式缓存参数：

-   若请求配置了显式缓存标识，系统会忽略显式缓存相关参数。
-   显式缓存不参与计费。

仅支持实际调用模型提供的隐式缓存：仅当请求被路由至同一模型，且提示词前缀满足该模型的缓存条件时，才可能命中缓存。由于不同请求可能被路由至不同模型，智能路由不保障缓存命中率。有关缓存的工作原理及其支持模型的详细信息，请参阅[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

## 管理路由服务

### 查看详情

部署成功后，在专属部署列表点击服务名进入详情页，可查看：

-   **基本信息**：服务名称、`model-code`、运行状态、路由策略标签。
-   **路由配置**：路由版本、路由策略、备选集与备选模型列表。
-   **计费方式**：按量计费，按实际使用模型单价计费。
-   **部署配置**：各备选模型的 TPM/RPM 限流配额。

### 修改路由配置

在详情页「路由配置」区域点击「编辑」，可修改路由模型版本、路由策略与备选模型。切换路由版本时备选模型集随之变更，修改后几分钟内生效、不影响线上请求。

选定具体版本后，线上业务的路由行为将保持长期稳定；升级版本前请务必做全面评估，避免对业务产生影响。当前版本为 `model-router-2026-0908`。路由版本默认不自动更新。

### 删除服务

在专属部署列表中删除智能路由服务。`model-code` 删除后不复用，需重新创建。

## 智能路由效果

本章介绍智能路由的运行效果指标与监控方式。效果指标在详情页「智能路由效果」标签页查看，调用监控在模型监控页面查看。

### 路由效果指标

在详情页「智能路由效果」标签页查看以下指标。页面显示的指标为预估值，仅供参考，不能用于出账，实际账单以「费用用量」为准：

**指标**

**含义**

**异常处理**

路由请求总量

路由服务接收的请求总数（含故障自动切换成功）

突增排查上游限流/异常

路由成功率

成功转发请求 ÷ 总请求 × 100%

下降则排查备选模型可用性

实际模型成本（预估）

按实际模型目录价估算的全量成本（阶梯计费取最低档，峰谷定价取峰值，不含免费额度，与实际账单有偏差）

上升则检查路由策略与备选集

基线模型成本（预估）

假设全部由基线模型处理的对照成本（同口径估算）

—

节约金额

基线成本 − 实际成本（正值表示路由节约）

—

计费请求数

产生费用的成功请求数

—

花费占比

单模型成本 ÷ 总成本

异常则检查备选集分布

### 成本说明

成本分析数据约有 1 小时延迟，非实时统计。 上述成本均按目录价估算全量成本，不含账号折扣优惠与免费额度，仅供衡量智能路由节约效果参考。 阶梯计费模型取最低档目录价，峰谷定价模型取峰值价格。 实际账单金额可在「费用用量」中查看。

### 模型监控

如需查看更细粒度的调用监控，可前往模型监控页面。 该页面展示 `auto-model` 维度的模型监控和日志，不展示实际路由到的各模型的独立监控。

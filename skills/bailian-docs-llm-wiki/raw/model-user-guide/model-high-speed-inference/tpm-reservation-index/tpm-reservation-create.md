# 创建、接入与管理

本文按使用顺序介绍控制台创建吞吐预留（表单参数与费用确认）、API 接入调用、查看监控与日常管理（扩缩容、续订、退订、叠加容量包、溢出策略修改）。

## 开始之前

开始使用吞吐预留前，确认三样东西已就绪：

-   **百炼模型服务**：已在[百炼控制台](https://bailian.console.aliyun.com)开通。
-   **业务空间**：已创建业务空间；调用预留容量时使用该空间的专属域名与 API Key。
-   **API Key**：在目标业务空间内创建，步骤见[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

本页覆盖使用吞吐预留的完整流程：

```
创建吞吐预留 → 接入调用 → 查看与监控 → 日常管理（叠加容量包/扩缩容/续订/退订）
```

## 创建吞吐预留

进入创建页面：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/tpm-reservation)，在左侧导航选择**模型推理** > **吞吐预留**，单击**创建吞吐预留**。

表单按控制台实际顺序逐项填写：

表单项

可填什么

什么时候可选

**预留名称**

自定义名称，不超过 50 个字符

始终显示

**选择模型**

下拉选择要预留容量的模型

始终显示；选定后付费周期选项随所选模型动态出现

**推理模式**

标准模式 / 高速模式

始终显示；两者区别见[吞吐预留概述](raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)

**付费周期**

按天 / 按 8 小时时段 / 按小时后付费

按天：两种模式均可。按 8 小时时段：仅标准模式，且仅当日 22:00–次日 00:00 可下单。按小时后付费：仅高速模式，选定高速后出现

**输入容量 / 输出容量**

单位 **kTPM**（1 kTPM = 每分钟 1,000 Tokens），输入**起步 200、步长 10**，输出**起步 20、步长 1**

始终显示；买前用[TPM 容量计算器](https://help.aliyun.com/zh/model-studio/tpm-reservation-long-input#tpm-long-input-calc-h2)估算，长输入与缓存折算规则见[长输入与前缀缓存](raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)

**购买时长**

**1~30、60、90、120、365 天**

仅预付费/按天显示；按 8 小时时段固定 8 小时无需填写；后付费按实际使用计费无时长

**到期自动续费**

开启 / 关闭，默认**开启**；开启后到期前 1 天的 **8:20–20:00 间自动扣款，最多尝试 4 次**

仅预付费/按天显示；按 8 小时时段不支持自动续费

**单次续费时长**

**1~30、60、90、120、365 天**

开启到期自动续费后显示（仅按天）

**溢出策略**

**自动溢出**（默认，超出部分自动转按量计费、业务不中断）/ **仅使用预留容量**（超出部分直接返回 429 限流错误、不产生额外费用）

始终显示

**警告****创建成功即全额扣费**。容量费用按购买量一次性支付，与是否发起调用无关：即使从未调用，费用也全额产生、不按实际用量退减。确认理解后再提交购买。

填写过程中，页面右侧**费用明细**实时显示预估费用与计费说明。参数确认后单击**立即购买**，在弹窗中核对费用并单击**确认支付**。

创建完成后去哪里拿专属模型 code？返回吞吐预留列表页，展开对应模型卡片，在详情区**概览**页签找到**专属模型 code**，单击复制。后续所有调用都用它替换 `model` 参数。

## 接入调用

前提：预留实例状态为**运行中**。调用方式只有一条规则：把请求的 `model` 参数替换为专属模型 code，其余与普通模型调用一致。控制台详情区的**API 接入**页签只提供部分协议示例（**OpenAI 兼容**、**DashScope**）；三种协议的完整调用方式如下。

#### OpenAI Chat 兼容

适合已按 OpenAI Chat Completions 协议接入的业务。两种 endpoint 均可使用：**DashScope 域名** `https://dashscope.aliyuncs.com/compatible-mode/v1`，或**业务空间专属域名** `https://{workspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（`{workspaceId}`、`{region}` 替换为实际值，如 `cn-beijing`）。

#### cURL

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-dedicated-model-code",
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ]
  }'
```

#### Python

```
import os
import dashscope

# 建议使用 dashscope SDK 2.0.1 及以上版本
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)
response = client.chat.completions.create(
    model="your-dedicated-model-code",  # 替换为专属模型 code
    messages=[{"role": "user", "content": "你好"}],
)
print(response)
```

改用业务空间专属域名时，把上面示例的域名替换为 `https://{workspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` 即可，其余参数不变。

#### Anthropic 兼容

适合已按 Anthropic Messages 协议接入的业务。该协议走业务空间专属域名，路径为 `/apps/anthropic/v1/messages`，鉴权用 `x-api-key` 请求头：

```
curl -X POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages \
  -H "x-api-key: $DASHSCOPE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-dedicated-model-code",
    "max_tokens": 32,
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ]
  }'
```

#### OpenAI Responses

适合已按 OpenAI Responses 协议接入的业务：

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-dedicated-model-code",
    "input": "你好"
  }'
```

**说明**专属模型 code 经 Responses 协议调用，当前**不消耗预留容量、按量计费**。需要容量保障时，请改用 OpenAI Chat 兼容或 Anthropic 兼容协议。

确认调用是否命中预留容量：查看响应中的 **service\_tier** 字段——返回 **ptu\_default**（标准模式）或 **ptu\_fast**（高速模式），说明命中预留容量；`provisioned_tokens` 为本次消耗的折算容量。字段含义见[查看容量消耗与缓存命中](https://help.aliyun.com/zh/model-studio/tpm-reservation-long-input#tpm-long-input-api-h2)。

## 查看与监控

在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/tpm-reservation)的吞吐预留页面查看容量、用量与运行状态。页面按使用动线分三层：

-   **预留列表**：每个模型一张卡片，用于查找目标预留。
-   **卡片详情区**：单击卡片**查看更多**展开，含**概览**、**监控**、**API 接入**三个页签——分别用于判断容量是否充足、排查调用问题、获取调用示例；概览页签底部为该模型下的容量实例列表，扩缩容、续订、退订的入口都在实例行的操作列。

### 预留列表

![预留列表的模型卡片：容量趋势图与生效中的容量实例](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f90f1.png)

卡片展示以下信息：

卡片信息

含义

模式标签、状态

该预留的推理模式与实例当前状态。

生效预留数

生效中的容量实例数量；统计范围包含历史已过期、已停止、已释放的预留，不等于当前可用数量。

已预留输入/输出 TPM

该模型名下全部实例的容量合计。

列表可按**基础模型**、**时间**、**状态**、**性能**筛选。卡片上的**购买容量**与**叠加容量包**入口作用相同，均为当前专属模型 code 追加容量实例。

### 卡片详情区

详情区包含三个页签：

#### 概览

![概览页签：部署配置、统计卡、使用率趋势、超额降级统计](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f90f0.png)

从三处判断容量是否充足：

检查项

位置

判断标准

利用率

统计卡（平均利用率）与**使用率趋势**曲线

利用率持续接近 100% 说明容量不足。

峰值

统计卡**7 日内峰值**（近 7 日容量使用峰值）

峰值接近或超过购买容量说明高峰时段不足。

超额降级

**超额降级统计**（最近降级时间与次数，仅**自动溢出**策略下产生）

频繁降级说明超出频繁，建议扩容（见[管理操作](#tpm-ops-h3)）。

使用率趋势提供三种统计方式：

统计方式

说明

以购买容量观测

以购买容量为基准计算利用率。

以折算容量观测

以按折算系数折算后的容量为基准（长输入与缓存折算方式）。

包含溢出用量

用量中额外计入溢出到按量计费的部分。

部署配置卡片展示预留名称、专属模型 code、基础模型与输入/输出容量，溢出策略旁提供**修改**入口（见[管理操作](#tpm-ops-h3)）。

#### 监控

![监控页签：调用统计与性能指标](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f90f7.png)

监控页签分**调用统计**、**性能指标**两个子页签，时间粒度支持**6 小时**、**按分钟**、**实时推理**，可按 **API Key** 筛选；**按 8 小时时段**实例额外展示该时段窗口内的包利用率。根据问题查找对应指标：

症状

看哪个指标

指标含义

请求报错增多

**失败次数 / 失败率**

按 **4xx**（请求侧：参数、鉴权）、**5xx**（服务端错误，可重试）、限流（容量方向，见[常见问题](#tpm-create-faq-h2)）、内容安全（检查输入内容）四类拆分。

疑似超量

**调用次数**（额度内/额度外拆分）

额度外调用即溢出到按量计费的部分。

响应变慢 / 成本异常

平均输入/输出 Tokens、调用量（全部、输入、输出 token 总量）

单次请求平均用量与总用量。

缓存未生效

**缓存命中量 / 命中率**

前缀缓存命中情况，计算方式见[长输入与前缀缓存](raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。

整体利用率

**吞吐单元利用率**

平均输入/输出利用率。

#### API 接入

![API 接入页签：可复制的调用示例](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f90f6.png)

提供 **OpenAI 兼容**、**DashScope** 两种协议与 **Node.js**、**cURL**、**Python** 三种语言组合的可复制调用示例；三种协议的完整接入方式见[接入调用](#tpm-create-call-h2)。

### 容量实例列表

![容量实例列表：容量实例 ID、输入/输出 TPM、状态、付费周期、生效/到期时间、自动续费与操作列](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f90f5.png)

容量实例列表位于概览页签底部，标题为「该模型下的容量实例列表」。每个容量实例对应一次容量购买，逐行管理：

列

说明

容量实例 ID

实例唯一标识，调用管理 OpenAPI 时用于指定实例。

输入/输出 TPM

实例的输入/输出容量。

状态

含义见[实例状态](#tpm-status-h2)。

付费周期

预付费/按天、预付费/按 8 小时时段、后付费/按小时。

生效/到期时间

生效与到期时点，到期前显示剩余天数。

自动续费

开/关，切换即生效（仅预付费/按天）。

操作列提供扩缩容、续订、退订入口（按实例状态显示）；**叠加容量包**按钮位于列表标题旁，与卡片上的入口等价。

## 管理操作

各付费方式可执行的操作与约束：

付费方式

扩缩容

续订

退订 / 删除

关键约束

预付费/按天

支持

支持（含自动续费）

走费用中心退订

退订不可恢复、按惩罚系数结算退费；API 无法直接释放预付费实例（须费用中心办理）

后付费/按小时

支持

不适用（无到期概念）

删除实例即停止计费

归零后的实例可直接删除；删除 Model Code 前须先释放全部实例

按 8 小时时段

不支持

不支持

不支持

时段到期后容量自动失效；不支持自动续费

**叠加容量包**可追加到预付费或后付费的预留上；**一个专属模型 code 下最多存在一个未删除的后付费实例**。溢出策略在**概览**页签修改。

操作

解决的问题

入口

适用实例

费用与规则

叠加容量包

追加一个新容量实例

卡片**叠加容量包**/**购买容量**，或容量实例列表标题旁

按天、按小时后付费实例

[叠加容量包计费](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-addon-h2)

扩缩容

在原实例上调大/调小容量（含归零）

容量实例列表操作列

按天、按小时后付费实例

[扩容](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-scaleup-h3)、[缩容](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-scaledown-h3)

续订 / 自动续费

延长有效期、避免到期中断

容量实例列表操作列 / 自动续费列开关

按天实例

[计费规则](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-rules-h2)

退订

彻底停止并释放实例

容量实例列表操作列（跳转费用中心办理）

按天实例

[退订](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-unsubscribe-h3)

修改溢出策略

决定超出部分转按量还是返回 429

**概览**页签溢出策略旁**修改**

全部实例

[溢出策略与计费](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-overflow-h2)

以上各项操作均提供对应的 OpenAPI 接口，调用方式见[吞吐预留 API 参考](raw/model-api-reference/model-production/throughput-reservation-api.md)。

### 叠加容量包

![叠加容量包弹窗：确认专属模型 code 后选择付费周期与容量](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f90f4.png)

单击卡片**叠加容量包**（或**购买容量**），按以下顺序完成：

```
确认专属模型 code → 选择付费周期 → 填写购买时长与自动续费（仅按天）→ 填写输入/输出容量 → 核对费用并支付
```

叠加容量包的可选付费周期：

付费周期

适用条件

预付费/按天

预付费或后付费的预留均可

预付费/按 8 小时时段

仅标准模式基础，且仅部分模型支持，支持列表见[8 小时时段预留计费](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-8h-h2)

后付费实例不能通过叠加容量包创建：一个专属模型 code 下最多存在一个未删除的后付费实例。后付费/按小时仅在新建吞吐预留时可选（仅高速模式）。

其余参数（购买时长、自动续费、输入/输出容量）的取值与新建一致：输入起步/步长 200/10 kTPM，输出 20/1 kTPM。

购买成功后，该预留的总容量相应增加；**专属模型 code 不变，API 调用无需任何改动**。

与在原实例上扩容的差异：

方式

改动对象

计费

叠加容量包

新增独立实例，与原实例并存

独立购买，可自选付费周期与时长（如按 8 小时时段）

扩缩容

调整原实例的输入/输出 TPM

新增部分按剩余有效期计费

### 扩缩容、续订与退订

三个操作都在容量实例列表的操作列：

#### 扩缩容

![扩缩容弹窗：原配置与新配置对照、需补交金额与费用明细](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9001.png)

单击**扩缩容**。弹窗以**原配置 / 新配置**对照展示输入、输出 TPM（滑条调整，未做改动时提示**配置未发生变化**）；调整后实时显示**需补交金额**与费用明细，并展示**已使用小时数 / 剩余小时数**——二者是扩容与缩容结算的计费基准。

**说明**输入与输出 TPM 均可调整为 **0**（归零）：归零后停止产生容量费用，专属模型 code 保留，可通过扩容恢复调用。缩容与归零按减配结算退费，惩罚系数为已使用 ≤30 天 **1.2**、>30 天 **1.0**，详见[缩容](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-scaledown-h3)。惩罚系数仅预付费实例适用；后付费实例删除即停止计费，不产生退款。

#### 续订

![续费弹窗：实例信息、购买时长、自动续费与费用明细](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f900a.png)

在容量实例列表操作列单击**续订**。弹窗展示实例信息（模型名称、专属模型 code、状态、当前到期时间），填写以下参数后完成支付：

参数

说明

购买时长

输入续费天数，与购买时长一致（1~30、60、90、120、365 天）；弹窗实时显示续费后的到期时间。

自动续费

开关；开启后续费到期前自动扣款。

费用明细按输入/输出预留分别列示（如 200 输入 kTPM ¥202、20 输出 kTPM ¥40.4）。

到期自动续费的规则：开启后系统在到期前 1 天的 **8:20–20:00 间自动扣款，最多尝试 4 次**，执行规则见[计费规则](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-rules-h2)。自动续费开关也可在容量实例列表的自动续费列直接切换。

#### 退订

单击**退订**，跳转[费用中心](https://usercenter.console.aliyun.com/)完成退订流程。

**警告****退订不可恢复**：退订后专属模型 code 失效，已有请求回退至公共资源。退费按惩罚系数结算（已使用 ≤30 天 **1.2**、>30 天 **1.0**），详见[退订](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-unsubscribe-h3)。

### 修改溢出策略

溢出策略创建后可以修改：在**概览**页签的溢出策略处单击**修改**。超出部分转为按量计费还是返回 429 由溢出策略决定，两种策略的行为差异与计费影响见[溢出策略与计费](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-overflow-h2)。

## 实例状态

实例的五种状态及含义：

状态

含义与去向

**运行中**

正常服务，专属模型 code 可调用。

**待生效**

已创建，等待生效。

**变配中**

正在执行扩缩容。

**已停止**

三种成因：到期、欠费、容量归零。到期与欠费停止的实例续费后恢复；归零的实例在**扩缩容**弹窗重新扩容后即恢复。

**已释放**

资源已回收，**不可恢复**。

预付费实例到期的处理节奏：到期后**立即停机**（不可调用，仍可续费），停机 **2 小时后释放**。

## 常见问题

Q: 调用返回 429 限流错误如何处理？

按三步排查：

1.  先看溢出策略：若为**仅使用预留容量**，超出预留容量必然返回 429；可在**概览**页签把溢出策略改为**自动溢出**。
2.  在**概览**页签查看**超额降级统计**，确认超出发生的频率。
3.  频繁超出说明容量不足：通过**扩缩容**上调容量，或购买**叠加容量包**。

Q: 失败率升高如何排查？

在**监控**页签按失败类型分流：**4xx** 多为请求自身问题（参数、鉴权）；**5xx** 为服务端错误，可重试；限流类错误按上一条的方向排查容量；内容安全类错误请检查输入内容。

Q: 到期后会怎样？

到期后立即停机（不可调用，仍可续费），停机 2 小时后释放、不可恢复。建议保持**到期自动续费**开启，规则见[到期与生命周期](https://help.aliyun.com/zh/model-studio/tpm-reservation-billing#tpm-billing-lifecycle-h2)。

Q: 如何判断是否需要扩容？

在**概览**页签看两个信号：使用率曲线持续贴近 100%，或**超额降级统计**的次数频繁增加。任一信号持续出现，即建议扩容输入/输出容量。

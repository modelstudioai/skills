# qwen4-max（最新模型）

Qwen4-Max 是通义千问新一代旗舰多模态模型，融合文本生成、图片与视频理解及深度思考能力，适用于编程开发、办公、前端设计与复杂智能体任务。模型支持联网搜索、工具调用和结构化输出，兼容 OpenAI 与 Anthropic API，帮助开发者构建具备多模态理解与任务执行能力的智能应用

模型调用 ID（`model` 参数取值）：`qwen4-max`

## 推理服务供应商

阿里云百炼

## 模型能力

#### 华北2（北京）

部署范围: 中国内地

能力

支持情况

能力

支持情况

输入模态

文本、图像、视频

输出模态

文本

流式输出

支持

深度思考

支持

并行工具调用

支持

联网搜索

支持

前缀补全

支持

Function Calling

支持

思维链摘要与加密

支持

OpenAI Chat Completions、Responses、Anthropic Messages、DashScope

支持

结构化输出（JSON Object、JSON Schema）

支持

显式缓存、隐式缓存

支持

批量推理

支持

模型调优

不支持

模型部署

不支持

#### 新加坡

部署范围：国际

能力

支持情况

能力

支持情况

输入模态

文本、图像、视频

输出模态

文本

流式输出

支持

深度思考

支持

并行工具调用

支持

联网搜索

支持

前缀补全

支持

Function Calling

支持

思维链摘要与加密

支持

OpenAI Chat Completions、Responses、Anthropic Messages、DashScope

支持

结构化输出（JSON Object、JSON Schema）

支持

显式缓存、隐式缓存

支持

批量推理

不支持

模型调优

不支持

模型部署

不支持

#### 德国（法兰克福）

部署范围：全球

能力

支持情况

能力

支持情况

输入模态

文本、图像、视频

输出模态

文本

流式输出

支持

深度思考

支持

并行工具调用

支持

联网搜索

支持

前缀补全

支持

Function Calling

支持

思维链摘要与加密

支持

OpenAI Chat Completions、Responses、Anthropic Messages、DashScope

支持

结构化输出（JSON Object、JSON Schema）

支持

显式缓存、隐式缓存

支持

批量推理

不支持

模型调优

不支持

模型部署

不支持

#### 美国（弗吉尼亚）

部署范围：全球

能力

支持情况

能力

支持情况

输入模态

文本、图像、视频

输出模态

文本

流式输出

支持

深度思考

支持

并行工具调用

支持

联网搜索

支持

前缀补全

支持

Function Calling

支持

思维链摘要与加密

支持

OpenAI Chat Completions、Responses、Anthropic Messages、DashScope

支持

结构化输出（JSON Object、JSON Schema）

支持

显式缓存、隐式缓存

支持

批量推理

不支持

模型调优

不支持

模型部署

不支持

#### 日本（东京）

部署范围：全球

能力

支持情况

能力

支持情况

输入模态

文本、图像、视频

输出模态

文本

流式输出

支持

深度思考

支持

并行工具调用

支持

联网搜索

支持

前缀补全

支持

Function Calling

支持

思维链摘要与加密

支持

OpenAI Chat Completions、Responses、Anthropic Messages、DashScope

支持

结构化输出（JSON Object、JSON Schema）

支持

显式缓存、隐式缓存

支持

批量推理

不支持

模型调优

不支持

模型部署

不支持

#### 中国香港

部署范围：全球

能力

支持情况

能力

支持情况

输入模态

文本、图像、视频

输出模态

文本

流式输出

支持

深度思考

支持

并行工具调用

支持

联网搜索

支持

前缀补全

支持

Function Calling

支持

思维链摘要与加密

支持

OpenAI Chat Completions、Responses、Anthropic Messages、DashScope

支持

结构化输出（JSON Object、JSON Schema）

支持

显式缓存、隐式缓存

支持

批量推理

不支持

模型调优

不支持

模型部署

不支持

## 模型限流与上下文

参数

Token

参数

Token

最大输入长度

991,808

最大输出长度

131,072

最大输入长度（思考模式下）

983,616

最大输出长度（思考模式下）

262,144

上下文长度

1,000,000

最大思维链长度

262,144

## 默认参数

参数

默认值

temperature

思考模式为 1.0，非思考模式为 0.7。

top\_p

思考模式为 0.95，非思考模式为 0.8。

top\_k

20

repetition\_penalty

1.0

presence\_penalty

0.0 (思考); 1.5 (非思考)

logprobs

false

enable\_thinking

true

preserve\_thinking

true

reasoning\_effort

high

thinking\_budget

131072

max\_completion\_tokens

262144 (思考); 131072 (非思考)

未传入 `reasoning_effort` 和 `thinking_budget` 时，默认使用 `reasoning_effort=high` 和 `thinking_budget=131072`。

## 思考强度

协议

参数

可选值

默认值

映射关系

OpenAI Chat Completions / DashScope

`reasoning_effort`

`low`、`high`、`xhigh`

`high`

`minimal` → `low`；`medium` → `high`；`max` → `xhigh`

OpenAI Responses

`reasoning.effort`

`low`、`high`、`xhigh`

`high`

`minimal` → `low`；`medium` → `high`；`max` → `xhigh`

Anthropic Messages

`output_config.effort`

`low`、`high`、`xhigh`

`high`

`medium` → `high`；`max` → `xhigh`

## 模型价格

#### 华北2（北京）

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#977b13081ab56)

有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）

qwen4-max

> [缓存单价（每百万 Token）](https://help.aliyun.com/zh/model-studio/explicit-cache-qwen4#billing)

非思考和思考模式

0<Token≤1M

10元

30元

100万Token

**qwen4-max — Batch 单价（每百万 Token）**

API

输入

输出

[Batch File](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)

5元

15元

[Batch Chat](raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)（限时 5 折）

原价 10元

原价 30元

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen4-max

> [缓存单价（每百万 Token）](https://help.aliyun.com/zh/model-studio/explicit-cache-qwen4#billing)

全球

非思考和思考模式

0<Token≤1M

10元

30元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen4-max

> [缓存单价（每百万 Token）](https://help.aliyun.com/zh/model-studio/explicit-cache-qwen4#billing)

国际

非思考和思考模式

0<Token≤1M

10.938元

32.813元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen4-max

> [缓存单价（每百万 Token）](https://help.aliyun.com/zh/model-studio/explicit-cache-qwen4#billing)

全球

非思考和思考模式

0<Token≤1M

10元

30元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen4-max

> [缓存单价（每百万 Token）](https://help.aliyun.com/zh/model-studio/explicit-cache-qwen4#billing)

全球

非思考和思考模式

0<Token≤1M

10元

30元

#### 中国香港

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen4-max

> [缓存单价（每百万 Token）](https://help.aliyun.com/zh/model-studio/explicit-cache-qwen4#billing)

全球

非思考和思考模式

0<Token≤1M

10元

30元

价格和免费额度见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。

## 限流

#### 华北2（北京）

**百炼平台月消费：**

**等级1（当前）≤¥10万**

**等级2 ¥10万~¥100万**

**等级3 >¥100万**

**支持的模型**

**TPM 限流档位**

**qwen4-max**

5,000,000

10,000,000

20,000,000

#### 新加坡

**百炼平台月消费：**

**等级1（当前）≤¥10万**

**等级2 ¥10万~¥100万**

**等级3 >¥100万**

**支持的模型**

**TPM 限流档位**

**qwen4-max**

5,000,000

10,000,000

20,000,000

#### 美国（弗吉尼亚）

**模型名称**

**服务部署范围**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen4-max

全球

30,000

5,000,000

#### 德国（法兰克福）

**模型名称**

**服务部署范围**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen4-max

全球

30,000

5,000,000

#### 日本（东京）

**模型名称**

**服务部署范围**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen4-max

全球

30,000

5,000,000

#### 中国香港

**模型名称**

**服务部署范围**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen4-max

全球

30,000

5,000,000

限流值及 AutoTPM 档位见[限流说明](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 调用方式

-   [OpenAI Chat Completions](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
-   [OpenAI Responses](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
-   [Anthropic Messages](raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
-   [DashScope](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
-   [模型能力](raw/model-user-guide/model-experience/text-generation-model.md)
-   [CoT Summary](raw/model-user-guide/model-experience/text-generation-model/cot-summary.md)
-   [Prompt Cache](raw/model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md)

## 使用说明

### 显式缓存

复用系统提示词、工具说明和参考文档等公共输入前缀，降低重复输入的成本。支持 OpenAI Chat Completions、Responses 和 Anthropic Messages，TTL 支持 `5m` 和 `1h`。配置与计费见 [显式缓存](raw/model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md)。

### 思维链摘要与加密

返回思维链摘要和密文，摘要用于展示，密文用于后续轮次恢复历史思考。多轮对话需原样回传历史密文。各协议的开启方式、流式返回和完整示例见 [思维链摘要与加密](raw/model-user-guide/model-experience/text-generation-model/cot-summary.md)。

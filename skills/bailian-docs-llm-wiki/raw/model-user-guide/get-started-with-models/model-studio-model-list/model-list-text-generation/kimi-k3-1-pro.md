# kimi-k3.1-pro

Kimi-K3.1-Pro 是月之暗面（Moonshot AI）K3.1 系列的首款模型，也是迄今能力最强的 3T 级开放权重模型，为 Kimi K3 的大规模后训练版本，后训练算力大幅增加。支持 100 万 token 上下文窗口，原生具备视觉理解能力（文本、图片输入，文本输出），并通过跨数百个领域的大规模联合强化学习，在代码、3D 创作、金融研究与长程 Agent 任务上显著提升：Terminal-Bench 4.0 得分 65.7%；金融文档分析 OfficeQA Pro v2 取得 64.4 的当前最佳成绩；声明级幻觉率较 K3 从 23.4% 降至 8.3%，综合智能水平已接近全球领先的闭源模型。

## 推理服务供应商

`kimi-k3.1-pro` 模型的推理服务供应商为阿里云百炼。

## 模型能力

以下能力在各地域及部署范围一致。

能力项

支持情况

输入模态

文本、图片

输出模态

文本

视频输入

不支持

模型体验

支持

Function Calling

支持

结构化输出

支持

隐式缓存

支持

联网搜索

支持

前缀续写

不支持

批量推理（Batch）

不支持

模型微调

不支持

## 上下文限制

参数

值（Token）

上下文长度

1048576

最大输入长度

1048576

最大输出长度

1048576

最大输入长度（思考模式下）

1048576

最大输出长度（思考模式下）

1048576

最大思维链长度

1048576

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息。

#### 华北2（北京）

计费项

价格（元）

单位

输入

13

每百万 Tokens

输出

68

每百万 Tokens

输入（缓存命中）

1.3

每百万 Tokens

#### 新加坡

部署范围：国际

计费项

价格（元）

单位

输入

14.583

每百万 Tokens

输出

72.917

每百万 Tokens

输入（缓存命中）

1.458

每百万 Tokens

#### 德国（法兰克福）

部署范围：全球

计费项

价格（元）

单位

输入

13

每百万 Tokens

输出

68

每百万 Tokens

输入（缓存命中）

1.3

每百万 Tokens

#### 美国（弗吉尼亚）

部署范围：全球

计费项

价格（元）

单位

输入

13

每百万 Tokens

输出

68

每百万 Tokens

输入（缓存命中）

1.3

每百万 Tokens

部署范围：美国

计费项

价格（元）

单位

输入

14.583

每百万 Tokens

输出

72.917

每百万 Tokens

输入（缓存命中）

1.458

每百万 Tokens

#### 日本（东京）

部署范围：全球

计费项

价格（元）

单位

输入

13

每百万 Tokens

输出

68

每百万 Tokens

输入（缓存命中）

1.3

每百万 Tokens

#### 中国香港

部署范围：全球

计费项

价格（元）

单位

输入

13

每百万 Tokens

输出

68

每百万 Tokens

输入（缓存命中）

1.3

每百万 Tokens

## 限流

#### 华北2（北京）

本地域采用动态限流机制，TPM 限流值按百炼平台月消费额度分为 120 万、500 万、1000 万三个档位。分档规则请参见[动态限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

#### 新加坡

部署范围：国际

本地域采用动态限流机制，TPM 限流值按百炼平台月消费额度分为 120 万、500 万、1000 万三个档位。分档规则请参见[动态限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

#### 德国（法兰克福）

部署范围：全球

参数

值

RPM（每分钟请求数）

15,000

TPM（每分钟 Tokens）

1,200,000

#### 美国（弗吉尼亚）

部署范围：全球

参数

值

RPM（每分钟请求数）

15,000

TPM（每分钟 Tokens）

1,200,000

部署范围：美国

本部署范围的限流信息请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

#### 日本（东京）

部署范围：全球

参数

值

RPM（每分钟请求数）

15,000

TPM（每分钟 Tokens）

1,200,000

#### 中国香港

部署范围：全球

参数

值

RPM（每分钟请求数）

15,000

TPM（每分钟 Tokens）

1,200,000

## 调用方式

-   模型使用指南：[Kimi](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。
-   API 参考：[OpenAI 兼容 Chat Completions](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[OpenAI 兼容 Responses](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)、[DashScope](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)、[Anthropic 兼容 Messages](raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

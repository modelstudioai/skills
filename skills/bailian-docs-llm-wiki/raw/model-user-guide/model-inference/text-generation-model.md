# 文本生成

为AI智能体、聊天机器人、文档处理等场景选择合适的文本生成模型。

## 使用 OpenClaw、Claude Code或 Hermes?

`qwen3.6-plus` -- 能力与成本均衡，完整工具调用支持，100万上下文窗口，适用于大型代码库。 [Token Plan](https://help.aliyun.com/zh/model-studio/token-plan-overview)用户还可选择 `glm-5`或`MiniMax-M2.5`，均针对智能体工作流进行了优化。

## 从闭源模型迁移到百炼?

如果你正在使用 GPT、Claude 或 Gemini，可参考下表按能力档选择百炼对位模型。

**闭源模型代表**

**百炼推荐**

高能力

GPT-5.5、Claude Opus 4.7、Gemini 3.1 Pro

`qwen3.7-max`

平衡

GPT-5.4、Claude Sonnet 4.6、Gemini 3 Pro

`qwen3.6-plus`、`deepseek-v4-pro`、`glm-5.1`

轻量低成本

GPT-5.4-mini、Claude Haiku 4.5、Gemini 3.1 Flash

`qwen3.6-flash`、`deepseek-v4-flash`、`MiniMax-M2.5`

## 应用场景

聊天机器人、内容生成、摘要总结、文档处理等场景，推荐使用 `qwen3.6-plus`，能力与成本均衡，拥有100万上下文窗口和完整的内置工具。确认效果满足需求后，可以尝试 `qwen3.6-flash` 来降低成本，效果接近旗舰模型，且拥有相同的上下文长度和功能支持。如需最强推理能力，可选择 `qwen3.7-max`（百万 token 上下文），但成本较高。

### 上下文窗口

100万Token约相当于70万个汉字或10本小说。

-   长文档或大型代码库：`qwen3.6-plus` / `qwen3.6-flash`（100万）。
    
-   常规任务：128k-256k已足够。
    

模型的上下文信息请前往模型广场查看。

[华北2（北京）](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) | [新加坡](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=doc#/doc/?type=model&url=2840914) | [美国](https://modelstudio.console.aliyun.com/us-east-1?tab=doc#/doc/?type=model&url=2840914) | [法兰克福](https://modelstudio.console.aliyun.com/eu-central-1?tab=doc#/doc/?type=model&url=2840914)

### 思考模式

逐步推理，适用于多步数学计算、代码调试、架构规划或法律交叉引用等场景。

通过 `enable_thinking` 参数开启（Responses API 通过`reasoning`.`effort`参数控制思考模式开关与深度）。所有Qwen3及以上模型均支持，大多数为混合模式，可按请求灵活切换。

> 详情参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。

### Function Calling与内置工具

让模型执行操作：查询天气、查询数据库、预订会议等。

-   Function Calling（自定义工具，模型调用）：所有通用模型均支持。
    
-   内置工具（联网搜索、代码解释器、网页抓取等，无需复杂配置）。
    

> 详情参见[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)。

### 结构化输出

获取有效的JSON返回，例如从文本中提取姓名和地址。

> 详情参见[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)。

### 批量推理

适用于大量请求且对延迟要求不高的场景，可降低请求成本。

> 详情参见[批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)。

## 推荐模型

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen3.7-max`

1M

支持

支持

支持

支持

支持

`qwen3.6-plus`

1M

支持

支持

支持

支持

支持

`qwen3.6-flash`

1M

支持

支持

支持

支持

支持

`deepseek-v4-pro`

1M

支持

支持

不支持

不支持

不支持

`deepseek-v4-flash`

1M

支持

支持

不支持

不支持

不支持

`glm-5.1`

198k

支持

支持

不支持

支持

不支持

`kimi-k2.6`

256k

支持

支持

不支持

不支持

不支持

`MiniMax-M2.5`

192k

支持

支持

不支持

不支持

不支持

`mimo-v2.5-pro`

1M

支持

支持

不支持

支持

不支持

## 所有模型

### Qwen3.7

**模型**

**上下文**

**最大输出**

**思考预算**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

**Token Plan**

**Coding Plan**

`qwen3.7-max`

1M

64k

256k

支持

支持

支持

支持

不支持

不支持

`qwen3.7-max-2026-05-20`

1M

64k

256k

支持

支持

支持

不支持

不支持

不支持

`qwen3.7-max-preview`

1M

64k

256k

支持

支持

支持

不支持

不支持

不支持

`qwen3.7-max-2026-05-17`

1M

64k

256k

支持

支持

支持

不支持

不支持

不支持

### Qwen3.6

**模型**

**上下文**

**最大输出**

**思考预算**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

**Token Plan**

**Coding Plan**

`qwen3.6-max-preview`

256k

64k

128k

支持

不支持

支持

不支持

不支持

不支持

`qwen3.6-plus`

1M

64k

80k

支持

支持

支持

支持

支持

支持

`qwen3.6-plus-2026-04-02`

1M

64k

80k

支持

支持

支持

不支持

不支持

不支持

`qwen3.6-flash`

1M

64k

128k

支持

支持

支持

支持

支持

不支持

`qwen3.6-flash-2026-04-16`

1M

64k

128k

支持

支持

支持

不支持

不支持

不支持

### Qwen3.5

**模型**

**上下文**

**最大输出**

**思考预算**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

**Token Plan**

**Coding Plan**

`qwen3.5-plus`

1M

64k

80k

支持

支持

支持

支持

不支持

支持

`qwen3.5-plus-2026-02-15`

1M

64k

80k

支持

支持

支持

不支持

不支持

不支持

`qwen3.5-flash`

1M

64k

80k

支持

支持

支持

支持

不支持

不支持

`qwen3.5-flash-2026-02-23`

1M

64k

80k

支持

支持

支持

不支持

不支持

不支持

`qwen3.5-397b-a17b`

256k

64k

80k

支持

支持

支持

不支持

不支持

不支持

`qwen3.5-122b-a10b`

256k

64k

80k

支持

支持

支持

不支持

不支持

不支持

`qwen3.5-27b`

256k

64k

80k

支持

支持

支持

不支持

不支持

不支持

`qwen3.5-35b-a3b`

256k

64k

80k

支持

支持

支持

不支持

不支持

不支持

### 第三方模型

**模型**

**上下文**

**最大输出**

**思考预算**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

**Token Plan**

**Coding Plan**

`deepseek-v4-pro`

1M

共384k

支持

不支持

不支持

不支持

支持

不支持

`deepseek-v4-flash`

1M

共384k

支持

不支持

不支持

不支持

支持

不支持

`glm-5.1`

198k

128k

128k

支持

不支持

支持

不支持

支持

不支持

`kimi-k2.6`

256k

96k

80k

支持

不支持

不支持

不支持

支持

支持

`MiniMax-M2.5`

192k

共32k

支持

不支持

不支持

不支持

支持

支持

`mimo-v2.5-pro`

1M

128K

128K

支持

不支持

支持

不支持

不支持

不支持

### 旧版及其他模型

以下模型不再作为首选推荐。新项目建议使用Qwen3.6或Qwen3.5系列。如需查看模型详细参数（上下文窗口、计费等），请前往模型广场。

[华北2（北京）](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) | [新加坡](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=doc#/doc/?type=model&url=2840914) | [美国](https://modelstudio.console.aliyun.com/us-east-1?tab=doc#/doc/?type=model&url=2840914) | [法兰克福](https://modelstudio.console.aliyun.com/eu-central-1?tab=doc#/doc/?type=model&url=2840914)

**查看旧版及其他模型列表**

#### Qwen3

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen3-max`

256k

支持

支持

支持

支持

支持

`qwen3-max-2026-01-23`

256k

支持

支持

支持

支持

不支持

`qwen3-max-preview`

256k

支持

支持

支持

支持

不支持

`qwen3-max-2025-09-23`

256k

支持

支持

支持

支持

不支持

`qwen3-235b-a22b`

256k

支持

支持

不支持

支持

不支持

`qwen3-235b-a22b-thinking-2507`

256k

支持

支持

不支持

不支持

不支持

`qwen3-235b-a22b-instruct-2507`

256k

不支持

支持

不支持

支持

不支持

`qwen3-next-80b-a3b-thinking`

256k

支持

支持

不支持

不支持

不支持

`qwen3-next-80b-a3b-instruct`

256k

不支持

支持

不支持

支持

不支持

`qwen3-32b`

256k

支持

支持

不支持

支持

不支持

`qwen3-30b-a3b`

256k

支持

支持

不支持

支持

不支持

`qwen3-30b-a3b-thinking-2507`

256k

支持

支持

不支持

不支持

不支持

`qwen3-30b-a3b-instruct-2507`

256k

不支持

支持

不支持

支持

不支持

`qwen3-14b`

256k

支持

支持

不支持

支持

不支持

`qwen3-8b`

256k

支持

支持

不支持

支持

不支持

`qwen3-4b`

256k

支持

支持

不支持

支持

不支持

`qwen3-1.7b`

256k

支持

支持

不支持

支持

不支持

`qwen3-0.6b`

256k

支持

支持

不支持

支持

不支持

#### Qwen3-Coder

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen3-coder-plus`

1M

支持

支持

不支持

支持

不支持

`qwen3-coder-plus-2025-09-23`

1M

支持

支持

不支持

支持

不支持

`qwen3-coder-plus-2025-07-22`

1M

支持

支持

不支持

支持

不支持

`qwen3-coder-flash`

1M

支持

支持

不支持

支持

不支持

`qwen3-coder-flash-2025-07-28`

1M

支持

支持

不支持

支持

不支持

`qwen3-coder-next`

256k

支持

支持

不支持

支持

不支持

`qwen3-coder-480b-a35b-instruct`

256k

不支持

支持

不支持

支持

不支持

`qwen3-coder-30b-a3b-instruct`

256k

不支持

支持

不支持

支持

不支持

#### Qwen2.5（开源）

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen2.5-omni-7b`

1M

不支持

不支持

不支持

不支持

不支持

`qwen2.5-vl-72b-instruct`

1M

不支持

不支持

不支持

不支持

不支持

`qwen2.5-vl-32b-instruct`

1M

不支持

不支持

不支持

不支持

不支持

`qwen2.5-vl-7b-instruct`

1M

不支持

不支持

不支持

不支持

不支持

`qwen2.5-vl-3b-instruct`

1M

不支持

不支持

不支持

不支持

不支持

`qwen2.5-72b-instruct`

1M

不支持

支持

不支持

支持

不支持

`qwen2.5-72b-instruct-1m`

1M

不支持

支持

不支持

支持

不支持

`qwen2.5-32b-instruct`

1M

不支持

支持

不支持

支持

不支持

`qwen2.5-14b-instruct`

1M

不支持

支持

不支持

支持

不支持

`qwen2.5-14b-instruct-1m`

1M

不支持

支持

不支持

支持

不支持

`qwen2.5-7b-instruct`

1M

不支持

支持

不支持

支持

不支持

`qwen2.5-7b-instruct-1m`

1M

不支持

支持

不支持

支持

不支持

#### 翻译

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen-mt-plus`

16k

不支持

不支持

不支持

不支持

不支持

`qwen-mt-turbo`

16k

不支持

不支持

不支持

不支持

不支持

`qwen-mt-flash`

16k

不支持

不支持

不支持

不支持

不支持

`qwen-mt-lite`

16k

不支持

不支持

不支持

不支持

不支持

#### 千问Long

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen-long`

10M

不支持

不支持

不支持

支持

支持

`qwen-long-latest`

10M

不支持

不支持

不支持

支持

支持

`qwen-long-2025-01-25`

10M

不支持

不支持

不支持

支持

不支持

#### 角色扮演

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen-plus-character`

32k

不支持

不支持

不支持

不支持

不支持

`qwen-plus-character-ja`

32k

不支持

不支持

不支持

不支持

不支持

`qwen-flash-character`

8k

不支持

不支持

不支持

不支持

不支持

#### 旧版Qwen

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`qwen-plus`及其快照版本

1M

支持

支持

支持

支持

支持（仅主线版本）

`qwen-max`及其快照版本

128k

支持

支持

支持

支持

支持（仅主线版本）

`qwen-flash`及其快照版本

1M

支持

支持

支持

支持

支持（仅主线版本）

`qwen-turbo`及其快照版本

1M

支持

支持

支持

支持

支持（仅主线版本）

`qwq-plus`

128k

支持

支持

不支持

不支持

支持

`qvq-max`及其快照版本

128k

支持

不支持

不支持

不支持

不支持

`qwen-omni-turbo`及其快照版本

32k

不支持

不支持

不支持

不支持

支持（仅主线版本）

#### **三方模型**

**模型**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

**批量调用**

`glm-5`

198k

支持

支持

不支持

支持

不支持

`glm-4.7`

198k

支持

支持

不支持

支持

不支持

`glm-4.5`

198k

支持

支持

不支持

支持

不支持

`glm-4.5-air`

198k

支持

支持

不支持

支持

不支持

`MiniMax-M2.1`

200k

支持

支持

不支持

不支持

不支持

`kimi-k2.5`

256k

支持

支持

不支持

不支持

不支持

`kimi-k2-thinking`

256k

支持

支持

不支持

支持

不支持

`Moonshot-Kimi-K2-Instruct`

256k

不支持

支持

不支持

不支持

不支持

`deepseek-v3.2`

128k

支持

支持

不支持

不支持

支持

`deepseek-v3.2-exp`

128k

支持

支持

不支持

不支持

不支持

`deepseek-v3.1`

128k

支持

支持

不支持

不支持

不支持

`deepseek-v3`

128k

不支持

支持

不支持

不支持

支持

`deepseek-r1`

128k

支持

支持

不支持

不支持

支持

`deepseek-r1-0528`

128k

支持

支持

不支持

不支持

不支持

`deepseek-r1-distill-llama-70b`

128k

支持

不支持

不支持

不支持

不支持

`deepseek-r1-distill-qwen-32b`

128k

支持

不支持

不支持

不支持

不支持

`deepseek-r1-distill-qwen-14b`

128k

支持

不支持

不支持

不支持

不支持

`deepseek-r1-distill-qwen-7b`

128k

支持

不支持

不支持

不支持

不支持

`deepseek-r1-distill-qwen-1.5b`

128k

支持

不支持

不支持

不支持

不支持

`deepseek-r1-distill-llama-8b`

128k

支持

不支持

不支持

不支持

不支持

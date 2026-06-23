# 预置吞吐长输入与缓存

本文介绍 PTU（预置吞吐）部署的长输入和前缀缓存能力，包括额度消耗规则、容量计算器使用方法和 API 响应字段说明。

## 功能概述

PTU 部署支持长输入请求（部分模型最高 200K token）和前缀缓存，通过阶梯容量系数和缓存折扣灵活管理额度消耗。

核心能力：

-   长输入支持：部分模型支持超过 32K token 的输入，超出部分按更高的阶梯系数折算 TPM（每分钟 Token 数）消耗，详见[额度消耗规则](#sec-billing)。
    
-   前缀缓存优惠：部分模型支持前缀缓存，命中缓存的输入 token 按折扣系数消耗额度（具体折扣率因模型而异），可降低多轮对话和重复前缀场景的额度消耗。
    
-   自动转按量计费：超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，无需修改调用代码。
    

**重要**

自动转按量计费后，费用按对应模型的按量付费单价计算。建议通过容量计算器合理规划 PTU 额度，避免意外费用。

常见于长文档分析（合同、研报摘要）和多轮对话（客服、编程助手）等输入超 32K token 的场景。

关于 PTU 部署的基础概念和购买方式，请参见[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。关于前缀缓存的工作原理，请参见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

## 额度消耗规则

长输入阶梯系数和缓存折扣按模型不同，以下为当前支持的模型参数：

**模型**

**输入长度上限**

**缓存折扣**

**长输入阶梯系数**

glm-5.1

200K

0.2（缓存命中部分按 20% 折算容量）

\[0, 32K)：输入 1.0 / 输出 1.0  
\[32K, 200K\]：输入 1.33 / 输出 1.17  
  

deepseek-v4-pro

256K

0.08（缓存命中部分按 8% 折算容量）

无阶梯（1.0）

qwen3.7-plus-2026-05-26

256K

0.2（缓存命中部分按 20% 折算容量）

无阶梯（1.0）

其他模型

以控制台为准

暂不支持

无阶梯（1.0）

### 计算示例（以 glm-5.1 为例）

```
场景 1：短输入（10K token，无缓存）
  输入消耗：10K × 1.0 = 10KTPM

场景 2：长输入（50K token，无缓存）
  输入消耗：32K × 1.0 + 18K × 1.33 = 55.94 KTPM
  输出消耗（假设 1K token）：1K × 1.17 = 1.17 KTPM

场景 3：长输入 + 缓存命中（50K token，前 30K 命中缓存）
  缓存部分输入（前 30K，均在 [0,32K) 阶梯内）：
    30K × 1.0 × 0.2 = 6  KTPM
  非缓存部分输入（后 20K）：
    2K × 1.0 + 18K × 1.33 = 25.94 KTPM
  输入合计 = 31.940 KTPM（比无缓存节省 43%）
```

## 使用容量计算器估算额度

**说明**

建议在创建或扩容前使用计算器评估长输入场景的额度需求，避免额度不足导致请求转为按量计费。购买上限以控制台实际展示为准。

前提条件：已开通百炼服务并具备 PTU 部署权限。登录[百炼控制台](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，在**模型部署** > **创建部署**页面（或在已有部署详情页单击**扩容**），选择可部署的PTU（预置吞吐）模型后，展开**容量计算器**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4645961871/p1082157.png)

容量计算器根据业务负载自动推荐 TPM 额度。填写以下参数后，计算器输出推荐的输入 TPM 和输出 TPM。

**参数**

**说明**

**对结果的影响**

每分钟请求数（RPM）

业务高峰期每分钟的请求数。

RPM 越大，建议购买的输入和输出 TPM 同比增大。

平均输入长度（token）

每条请求的平均输入 token 数。

输入越长，所处阶梯越高，系数越大，建议购买的输入 TPM 越高。不同模型的阶梯边界不同，以控制台实际展示为准。

平均输出长度（token）

每条请求的平均输出 token 数。

输出越长，系数可能越大，建议购买的输出 TPM 越高。

预估缓存命中率（%）

请求中重复前缀被缓存命中的比例。实际命中率取决于请求内容的重复程度，以运行结果为准。

命中率越高，输入容量消耗越慢，建议购买的输入 TPM 越低。仅影响输入 TPM，不影响输出 TPM。

## API 响应字段说明

PTU 部署的 API 响应包含以下额度相关字段，用于标识计费方式和额度消耗：

**字段**

**类型**

**说明**

`service_tier`

String

响应体顶层字段（所有 API 格式一致）。值为 `ptu-standard` 表示使用 PTU 额度；值为 `default` 或不返回表示按量计费

`provisioned_tokens`

Integer

折算后实际消耗的 PTU 额度 token 数（已含阶梯系数和缓存折扣）

`cached_tokens`

Integer

前缀缓存命中的 token 数，详见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

不同 API 格式下上述字段的 JSON 路径存在差异：

### OpenAI Chat 兼容

**字段**

**JSON 路径**

**说明**

`cached_tokens`

`usage.prompt_tokens_details.cached_tokens`

输入侧缓存命中数

`provisioned_tokens`

`usage.prompt_tokens_details.provisioned_tokens`

输入侧 PTU 额度消耗

`provisioned_tokens`

`usage.completion_tokens_details.provisioned_tokens`

输出侧 PTU 额度消耗

### OpenAI Responses

**字段**

**JSON 路径**

**说明**

`cached_tokens`

`usage.input_tokens_details.cached_tokens`

输入侧缓存命中数

`provisioned_tokens`

`usage.input_tokens_details.provisioned_tokens`

输入侧 PTU 额度消耗

`provisioned_tokens`

`usage.output_tokens_details.provisioned_tokens`

输出侧 PTU 额度消耗

### Anthropic 兼容

**字段**

**JSON 路径**

**说明**

`provisioned_tokens`

`usage.prompt_tokens_details.provisioned_tokens`

输入侧 PTU 额度消耗

`provisioned_tokens`

`usage.output_tokens_details.provisioned_tokens`

输出侧 PTU 额度消耗

**说明**

Anthropic 兼容格式暂不返回 `cached_tokens` 字段，可通过 `provisioned_tokens` 间接判断缓存效果。

### DashScope

**字段**

**JSON 路径**

**说明**

`cached_tokens`

`usage.prompt_tokens_details.cached_tokens`

输入侧缓存命中数

`provisioned_tokens`

`usage.prompt_tokens_details.provisioned_tokens`

输入侧 PTU 额度消耗

`provisioned_tokens`

`usage.completion_tokens_details.provisioned_tokens`

输出侧 PTU 额度消耗

各字段的完整定义和取值范围，请参见[API 参考文档](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions)。

## 监控与验证

PTU 部署的运行监控通过百炼平台的模型监控功能实现，支持查看以下与长输入和缓存相关的指标：

-   PTU 利用率：输入/输出/思考模式输出三条独立曲线。长输入场景下阶梯系数会使利用率超过 100%，属于正常现象。
    
-   Token 用量与缓存命中：包含 `cached_tokens` 数据系列，可查看缓存命中量占总输入的比例。
    
-   配额内/外调用次数：了解超出 PTU 额度后转为按量计费的请求占比。
    

更多监控指标和操作方式，请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry)。

## 常见问题

**Q: 超出 PTU 额度时会怎样？**

请求自动转为按量计费。API 响应中 `service_tier` 字段不返回或返回 `default`，同时响应头包含 `x-dashscope-ptu-overflow:true`。业务不会中断。

**Q: 单次输入超过模型上限时会怎样？**

千问系列模型输入上限为 128K token，DeepSeek 系列为 64K token。超过上限的请求同样自动转为按量计费。

**Q: 如何确认缓存是否生效？**

检查 API 响应中 `cached_tokens` 字段，值大于 0 表示前缀缓存命中。缓存命中部分按模型对应的折扣系数消耗额度（具体折扣率见[额度消耗规则](#sec-billing)）。也可在控制台监控页面的 Token 用量图表中查看趋势。

**Q: cached\_tokens 始终为 0，缓存未生效怎么办？**

常见原因：请求间的输入前缀不一致（如 System Message 变化）、两次请求间隔超过缓存有效期、输入 token 数不足以触发缓存。排查方法和缓存使用限制详见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

**Q: 利用率为什么超过 100%？**

部分模型（如 glm-5.1）的长输入阶梯系数使实际额度消耗高于原始 token 数。利用率 = 折算后消耗 ÷ 购买额度。超过 100% 表示消耗速度超过购买额度，超出部分自动转为按量计费，不影响服务可用性。

# test 1

阿里云百炼平台提供多层次的计费体系，涵盖模型推理按量付费、模型训练与部署计费，以及节省计划与资源包等优惠方案。本页面汇总了百炼平台的计费规则、免费额度机制、账单查询方法和成本管理策略，帮助开发者全面了解和控制使用成本。

## 免费额度

首次开通百炼时，平台自动发放各模型的新人免费额度，仅适用于华北2（北京）地域且服务部署范围为中国内地的模型。

- **有效期**：30~90 天（2025年9月8日后新开通用户为 90 天），从开通或模型申请通过之日起计算
- **适用范围**：仅抵扣模型实时推理费用，不支持 Batch 调用、模型调优、[模型部署](../concepts/model-deployment.md)及自定义模型
- **共享规则**：主账号与 RAM 子账号共享同一免费额度池
- **额度查询**：通过控制台 [模型用量](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota) > 免费额度页签，或模型广场详情页查看

### 免费额度用完即停

开启此功能后，免费额度耗尽时将停止响应并返回错误码 `AllocationQuota.FreeTierOnly`，防止产生意外费用。可在模型用量页面为单个模型或批量开启。

> **注意**：全新未认证用户免费额度耗尽后必须完成认证并充值才能继续使用；已认证用户若未开启"用完即停"，超出额度将直接按量扣费。详见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 模型推理计费（按量付费）

模型推理采用按量付费方式，费用公式为：

```
费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价
```

### 阶梯计费

部分模型实行阶梯计费，单价取决于单次请求的输入 Token 总量。例如，若模型有 0~32K 和 32K~128K 两档，输入 100K Token 时所有 Token 均按第二档单价结算。

### 主要模型定价（华北2-北京，每百万 Token）

| 模型系列 | 代表模型 | 输入单价 | 输出单价 |
|---------|---------|---------|---------|
| 千问 Max | qwen3.7-max | 12 元 | 36 元 |
| 千问 Plus | qwen3.7-plus | 2 元 | 8 元 |
| 千问 Flash | qwen-flash 系列 | 较低 | 较低 |

不同地域（美国、新加坡、德国）价格有所差异，海外地域通常高于北京。支持 Batch 调用半价和上下文缓存折扣的模型可进一步降低成本。完整价目表请参见[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

## 模型训练计费

模型训练按训练 Token 计费，不同模型类型的计算方式有所差异：

### 文本生成模型（千问系列）

```
训练费用 = (训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数 × 训练单价
```

价格范围从 Qwen3-0.6B 的 0.003 元/千Token 到 Qwen2.5-72B-Instruct 的 0.15 元/千Token，模型越大价格越高。

### 图像生成模型（万相系列）

按训练 Token 总量计费，Token 总量由 max_steps 和 max_token_length 等超参数决定。wan2.7-image-pro 和 wan2.7-image 的训练单价为 0.08 元/千Token。

### 视频生成模型（万相系列）

训练 Token 总量与视频时长、max_pixels、循环次数相关，wan2.2 系列单价 0.06 元/千Token。

详细训练计费规则参见[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## [模型部署](../concepts/model-deployment.md)计费

[模型部署](../concepts/model-deployment.md)支持三种计费方式：

| 计费方式 | 说明 | 适用场景 |
|---------|------|---------|
| 预置吞吐（按 TPM） | 按输入/输出 TPM 和使用时长计费，支持后付费和预付费 | 需要稳定吞吐保障 |
| 模型单元 | 按模型单元数量和使用时长计费，支持后付费和包月 | 独占算力资源 |
| 按 Token 使用量 | 仅限 SFT 训练后的自定义模型 | 调用量不固定 |

> **注意**：当模型输入超过最长输入 Token 或超出购买的 TPM 量时，调用将自动切换为按量付费模式，此时 API 返回 Header 包含 `x-dashscope-ptu-overflow:true`。

## 成本优化方案

### AI 通用型节省计划（推荐）

通过承诺每月消费金额换取阶梯折扣，是大多数场景的首选方案：

- **覆盖范围**：可抵扣阿里直供的全部模型（含推理、工具调用、上下文缓存、批量推理）
- **折扣力度**：最高可享 5.3 折（百万级月承诺 + 24 个月全预付 + B 类模型）
- **承诺周期**：3/6/12/24 个月，1000 元起，以 10 元为单位调整
- **抵扣分类**：A 类（千问文本）、B 类（图像/语音/视频）、C 类（DeepSeek/GLM 等第三方）

### 其他模型节省计划

针对特定模型系列的一次性购买方案，适合用量集中于某一模型的场景：

- **大语言模型推理节省计划**：20~500,000 元档位，无折扣
- **千问语音模型节省计划**：20~5,000 元档位，8~9.8 折
- **向量及排序模型节省计划**：100~10,000 元档位，7~10 折

### 资源包

预购 Token 数量抵扣特定模型费用，购买后立即生效。

### 抵扣优先级

```
免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费
```

详细折扣信息和购买方式参见[节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 账单查询与成本管理

### 查询账单

- **费用概览**：控制台 > 用量 & 费用 > 费用概览，查看当月总消费和趋势
- **账单详情**：在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面按产品名称筛选"大模型服务平台百炼"

账单的"实例 ID（出账粒度）"字段格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，可据此定位具体模型和调用来源。

### 分账管理

给[业务空间](../concepts/workspace.md)绑定标签后，可按部门或项目维度归集费用。在标签管理页面为[业务空间](../concepts/workspace.md)绑定标签键值，启用费用标签后 T+1 天生效。

### 欠费处理

账户可用额度 < 0 视为欠费。欠费时即使其他模型仍有免费额度也无法调用。建议配置[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)提前预防。

### 停止计费

不再使用时，停止 API 调用并删除 API-Key 即可停止推理计费；[模型部署](../concepts/model-deployment.md)需手动下线；Coding Plan 和 Token Plan 需关闭自动续费。

详见[账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)





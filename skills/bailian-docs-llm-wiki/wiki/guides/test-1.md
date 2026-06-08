# test 1

阿里云百炼平台采用按量付费为主、预付费优惠为辅的计费体系，覆盖模型推理调用、模型训练、模型部署三大场景。首次开通的用户可获得新人免费额度，超出后可通过节省计划、资源包等方式优化成本。本文汇总百炼平台的计费规则、成本优化方案和账单管理方法，帮助开发者合理规划用量与预算。

## 计费模式概览

百炼平台的计费分为三个层面：

- **模型推理调用**：按输入/输出 Token 数量计费，部分模型实行阶梯计费（单价取决于单次请求的输入 Token 总量）。支持 Batch 调用半价和上下文缓存折扣，两者不能同时生效。详见[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：按训练 Token 计费，公式为 `(训练数据 Token + 混合训练数据 Token) x 循环次数 x 单价`。图像和视频生成模型的训练 Token 计算方式有所不同。
- **模型部署**：提供按使用时长（预置吞吐）、按模型单元、按 Token 使用量三种计费方式，支持后付费和预付费两种模式。

## 新人免费额度

首次开通百炼的用户自动获得各模型的免费推理额度，仅限中国内地版模型。关键规则如下：

- **有效期**：30~90 天（2025 年 9 月 8 日后新开通用户为 90 天）
- **适用范围**：仅抵扣实时推理费用，不支持 Batch 调用、模型调优、模型部署及自定义模型
- **共享机制**：主账号与 RAM 子账号共享同一免费额度池
- **余量查询**：可在控制台[模型用量](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota)页面或模型广场详情页查看

建议开启**免费额度用完即停**功能，防止额度耗尽后自动扣费。开启后，免费额度用完时返回错误码 `AllocationQuota.FreeTierOnly`，不会继续产生费用。详见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 模型推理价格

### 阶梯计费规则

部分模型按单次请求的输入 Token 总量分阶梯定价。所有 Token 统一按命中的阶梯单价结算，不做分段计费。

### 千问系列代表价格（中国内地）

| 模型 | 输入单价（每百万 Token） | 输出单价（每百万 Token） | 免费额度 |
|------|------------------------|------------------------|---------|
| qwen3.7-max | 12 元 | 36 元 | 各 100 万 Token |
| qwen3-max (0~32K) | 2.5 元 | 10 元 | 各 100 万 Token |
| qwen3.7-plus (0~256K) | 2 元 | 8 元（非思考/思考） | 各 100 万 Token |
| qwen-plus (0~128K) | 0.8 元 | 非思考 2 元 / 思考 8 元 | 各 100 万 Token |

> **注意**：全球、国际、欧盟部署范围下的模型无免费额度，且单价高于中国内地版。例如 qwen3.7-max 在国际（新加坡）部署范围下输入单价为 18.736 元/百万 Token，约为中国内地版的 1.56 倍。

## 模型训练与部署计费

### 训练计费

训练按 Token 计费，不同模型类型的计算方式不同：

- **文本生成（千问）**：价格从 0.003 元/千 Token（Qwen3-0.6B）到 0.15 元/千 Token（Qwen2.5-72B-Instruct）不等
- **图像生成（万相）**：wan2.7-image-pro 训练价格 0.08 元/千 Token，Token 总量由 `max_steps x Lmax` 近似计算
- **视频生成（万相）**：价格 0.06~0.32 元/千 Token，Token 总量与视频时长、max_pixels、循环次数相关

### 部署计费

模型部署提供三种方式，详见[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)：

1. **按使用时长（预置吞吐）**：`费用 = 时长 x (输入 TPM 单价 x 输入 TPM + 输出 TPM 单价 x 输出 TPM)`。超出购买 TPM 的调用自动降级为按量付费。
2. **按模型单元**：`费用 = 时长 x 单元数 x 单元单价`。支持后付费（按小时）和预付费（包月），部分模型支持 PD 分离模式以降低首 Token 延迟。
3. **按 Token 使用量**：仅适用于 SFT 高效训练后的自定义模型。

## 成本优化方案

百炼提供三种成本优化工具，推荐优先级为：AI 通用型节省计划 > 其他模型节省计划 > 资源包。

### AI 通用型节省计划（推荐）

通过承诺月消费金额换取阶梯折扣，最高 5.3 折：

- **覆盖范围**：阿里直供的全部模型，分 A/B/C 三类享不同折扣
- **承诺周期**：3/6/12/24 个月，金额 1000 元起
- **付费方式**：全预付（折扣最大）或零预付（需白名单）
- **抵扣范围**：模型调用、工具调用、上下文缓存、批量推理；不支持模型调优和部署

抵扣顺序为：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费。

> **注意**：月承诺额度按月独立计算，未用完的部分自动清零，不可累积到下月。C 类模型（DeepSeek、Kimi、GLM 等）目前无折扣。

### 其他模型节省计划

适用于特定模型系列，如大语言模型、千问语音模型（最高 8 折）、向量及排序模型（最高 7 折）。具体折扣和适用模型详见[节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

### 资源包

预先购买固定 Token 数量，抵扣特定模型超出免费额度后的用量。目前提供 qwen-plus、qwen-max、qwen-turbo 三款资源包，购买后立即生效。

## 账单查询与管理

### 出账时间

- 大模型推理：分钟级出账（通常 2~10 分钟）
- 批量推理、模型训练、知识库：小时级出账

### 查询方式

- **费用概览**：在控制台[费用概览](https://bailian.console.aliyun.com/?tab=model#/costing-balance/overview)页查看总消费、按模型或 API Key 筛选
- **账单详情**：在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页下载明细，通过 `实例 ID（出账粒度）` 字段识别模型和调用渠道
- **模型监控**：调用完成 1 小时后可在[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页查看调用统计

### 分账管理

给[业务空间](../concepts/workspace.md)绑定标签即可按部门或项目归集费用，分账账单 T+1 天生效。详见[账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 欠费与停止计费

### 欠费影响

账户可用额度小于 0 时视为欠费。欠费后仍有免费额度、节省计划、资源包或已购套餐的可继续使用对应服务，否则服务暂停。

### 停止计费

- **推理**：停止 API 调用并删除 API Key
- **训练**：无进行中任务即不产生费用
- **部署**：在控制台下线已部署模型；包月预付费需额外在退订管理页面退订
- **Coding Plan / Token Plan**：关闭自动续费或按席位退订

### 费用预警

建议配置[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)和[资源包余量预警](https://help.aliyun.com/zh/user-center/configure-balance-alerts)，在费用异常时及时收到通知。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)




# Token 与计费

Token 是百炼平台衡量模型调用与部署资源消耗的基本计量单位，计费围绕输入 Token、输出 Token、训练 Token 和部署时长四个维度展开。

## 在不同场景中的使用

### 模型实时推理

按量付费默认按输入和输出 Token 分别计费。部分模型（如 `qwen3-max`、`qwen3.7-plus`）按单次请求的输入 Token 总量分阶梯计价，该请求的全部 Token 按对应阶梯单价结算，而非分段累计。华北 2（北京）价格最低，新加坡、法兰克福、东京等海外地域价格更高。

两种折扣会影响最终价格，但不可同时生效：

- **Batch 调用**：输入与输出 Token 单价均为实时推理的 50%。
- **上下文缓存**：仅对输入 Token 折扣。

### 免费额度

首次开通百炼的账号可获新人免费额度，仅抵扣模型实时推理费用，不抵扣 Batch、调优、部署及自定义模型。自 2025 年 9 月 8 日 11 点起，新开通用户额度有效期统一为 90 天。仅华北 2（北京）、部署范围为「中国内地」的模型享有免费额度。主账号与 RAM 子账号共享。可开启「免费额度用完即停」开关，额度耗尽时返回 `AllocationQuota.FreeTierOnly` 并停止扣费。

### 模型训练

按训练 Token 计费，公式为 `训练 Token 总数 × 循环次数 × 训练单价`，最小计费单位 1 Token。文本生成、图像生成（`max_steps × Lstep`）、视频生成（`计费时长 × max_pixels/1024 × n_epochs`）三类模型的 Token 总量计算方式不同。

### 模型部署

部署服务创建后计费方式不可更改，切换需先下线再重新部署。三种方式：

| 计费方式 | 公式 | 适用场景 |
| --- | --- | --- |
| 预置吞吐（PTU） | 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM) | 高负载生产、稳定 TPS |
| 模型单元 | 使用时长 × 模型单元数 × 单价；包月为 包月数 × 单元数 × 月单价 | 独占资源、长时任务、PD 分离 |
| Token 用量 | 输入 Token × 输入单价 + 输出 Token × 输出单价 | 调优模型效果验证 |

PTU 与模型单元均支持后付费（按小时）与预付费（按天/按月）。预付费订单到期后延后 2 小时停止服务、资源保留 14 小时后释放；模型单元预付费首月内退订，日单价按 1.2 倍计费。

### 订阅套餐

面向 AI 编程工具的订阅制方案，用专属 API Key 与 Base URL 调用，避免按量计费欠费风险：

- **Token Plan 团队版**：按 Token 消耗抵扣 Credits，面向团队，无每 5 小时/每周限额。
- **Coding Plan**：按调用次数计量，面向个人，有每 5 小时/每周/每月限额。

两者 API Key 与 Base URL 互不相通，误用会导致按量计费扣费。抵扣顺序为：坐席月度额度 → 共享用量包（最近到期优先）→ 服务暂停。

## 关键参数与配置

- **阶梯容量系数**：PTU 长输入按阶梯系数折算消耗，如 `glm-5.1` 在 [32K, 200K] 输入系数 1.33、输出系数 1.17。
- **缓存折扣**：`deepseek-v4-pro` 0.08、`qwen3.7-plus` 0.2、`glm-5.1` 0.2。
- **响应标识**：`service_tier` 为 `ptu-standard` 表示用 PTU 额度，`default` 或不返回表示按量计费；`provisioned_tokens` 为折算后实际消耗；`cached_tokens` 为缓存命中数。超出额度时响应头返回 `x-dashscope-ptu-overflow:true`。
- **协议与端点匹配**：Anthropic 协议端点以 `/apps/anthropic` 结尾，OpenAI 协议端点以 `/compatible-mode/v1` 或 `/v1` 结尾，混淆会触发 `400` 或 `404`。

## 账单与成本管理

后付费按分钟级出账、按月结算，扣款明细可在阿里云「费用与成本」查看，开票在「发票管理」申请。账户欠费时即使其他模型仍有免费额度也无法调用，需先结清欠费。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [support](../guides/support.md)



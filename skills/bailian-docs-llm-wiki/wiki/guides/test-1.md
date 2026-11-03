# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档整合了免费额度发放、按量计费、吞吐预留、节省计划、预算管控与账单溯源等关键机制，帮助开发者在保障服务稳定性的同时实现精细化成本治理。所有规则均以华北2（北京）地域为默认基准，跨地域调用需注意价格与额度隔离。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及 Qwen-VL、CosyVoice、Paraformer 等[多模态](../concepts/multi-modal.md)与语音模型。其中 `qwen3.8-max`、`qwen3.7-plus` 等新版本模型在华北2（北京）地域享有新人免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **批量调用**：支持 OpenAI 兼容的 Batch 接口，输入/输出 [Token](../concepts/token.md) 单价按实时推理价格的 50% 计费，但**不支持与上下文缓存同时生效** [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练与部署**：覆盖文本生成（千问系列）、图像生成（万相、Qwen-Image）、视频生成（万相）、语音合成（CosyVoice）等全类型调优能力；训练费用按 [Token](../concepts/token.md) 总量计费，部署费用按 PTU（预置吞吐）或 DTU（独占吞吐）时长计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPM 预留）**：提供标准模式（等同 API TPS）与高速模式（1.5~2 倍 TPS），支持按天/按小时/8 小时时段三种购买形态，容量换算需考虑长输入阶梯系数与缓存折算系数 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 1 明确指出 `Batch调用`、`模型调优`、`模型部署` 不支持使用免费额度抵扣；而文档 4 在“千问Max”章节中将 Batch 调用列为影响计费的因素之一，二者逻辑一致。但文档 2 中“模型训练计费”示例表格列出 `qwen3-vl-8b-instruct` 等模型价格，而文档 1 的“已下架的免费额度”列表中包含 `qwen3-vl-plus-2025-09-23` —— 这表明 VL 系列模型虽可训练，但其**最新快照版本已无免费额度**，开发者需特别注意模型 Code 的时效性。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 模型唯一标识符，区分快照版本（如 `qwen3.8-max` 与 `qwen3.8-max-0902` 视为独立模型） | `qwen3.7-plus-2026-05-26` |
| `input_token` / `output_token` | 计费基础单位，免费额度与按量计费均按此统计总量（不区分输入/输出） | 免费额度：100 万 [Token](../concepts/token.md) 总额；按量计费：`qwen3.8-max` 输入 ¥12/百万 Token（华北2） |
| `TPM`（Tokens Per Minute） | 吞吐预留容量单位，kTPM = 1,000 Tokens/分钟；输入按万TPM报价，输出按千TPM报价 | 标准模式 `qwen3.8-max`：输入 ¥121/万TPM·天，输出 ¥36.29/千TPM·天 |
| `max_steps` / `n_epochs` | 训练超参，直接影响训练 Token 总量计算 | `wan2.7-image-pro` 微调：`max_steps=200` → Token 总量 ≈ 2560 千 Token |
| `free_quota_stop` | 免费额度用完即停开关，开启后额度耗尽返回 HTTP 403 错误码 `AllocationQuota.FreeTierOnly` | 默认关闭，生产环境不建议开启 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) |

## 使用方式

1. **开通与初始化**：完成阿里云实名认证后，访问[华北2（北京）地域百炼控制台](https://bailian.console.aliyun.com/model/market)开通服务，系统自动发放免费额度（仅限该地域）。
2. **调用模型**：
   - 使用通用 API Key 与 Base URL（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）；
   - 在请求体中指定 `model`、`input`、`parameters`；
   - 免费额度自动抵扣，无需额外配置。
3. **成本优化**：
   - **首选 AI 通用型节省计划**：承诺月消费金额换取阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)；
   - **次选资源包**：适用于用量小或集中于单一模型的场景（如 20 元档有效期 1 个月）；
   - **禁用非必要功能**：联网搜索插件、ManagedAgent 等独立计费项需显式关闭，避免意外扣费。
4. **监控与告警**：
   - 通过[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)设置账号/业务空间/API Key 级别月度预算；
   - 开启告警阈值（如 80%），接收站内信/短信/邮件通知；
   - **警告：生产环境不建议开启「达到预算后立即停止」**，可能导致服务中断。

## 限制和注意事项

- **地域隔离**：免费额度、节省计划、吞吐预留均按地域独立生效。华北2（北京）购买的节省计划**无法抵扣新加坡地域调用费用**；不同地域模型 Code 可能相同，但计费与额度不互通。
- **额度与有效期**：新人免费额度有效期为 90 天（自开通/模型发布/申请通过日起算，以较晚者为准），到期自动失效且不可延期；额度用完后转为按量付费，若未及时充值或开启“用完即停”，可能产生意外扣费。
- **计费延迟与出账**：模型推理账单通常延迟 2–10 分钟出账，批量推理、训练、知识库为小时级出账；**账单生成 ≠ 实际扣款**，按量付费采用“预占+月结”模式，最终扣款在次月初完成。
- **模型兼容性风险**：文档 1 列出大量已下架免费额度的模型（如 `qwen3.5-omni-flash`、`cosyvoice-v3` 等），而文档 4 的价格表仍包含部分同名模型。开发者应以控制台实际展示的模型广场为准，避免依赖已下架模型的旧文档。
- **退订与退款**：预付费吞吐预留退订时，≤30 天已使用部分按 1.2 倍系数结算；后付费实例缩容不退已用金额；入门型节省计划一经支付不支持退订。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)



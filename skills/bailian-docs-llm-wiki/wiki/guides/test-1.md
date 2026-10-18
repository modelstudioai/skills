# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖新人免费额度、按量调用、吞吐预留、模型训练/部署、节省计划、账单与预算等全链路成本控制能力。其设计目标是为不同规模和稳定性的业务场景提供灵活、可预测、可追溯的费用治理方案，所有计费行为均以 [Token](../concepts/token.md) 或 TPM（[Token](../concepts/token.md)s Per Minute）为计量基础，并严格遵循地域隔离、模型独立、额度分层抵扣的原则。

## 支持的模型/功能

- **支持模型**：覆盖千问（Qwen3.8-Max、Qwen3.7-Plus 等）、DeepSeek（v4-Pro、v4-Flash）、GLM（5.3、5.2）、Kimi（K2.6）、万相（wan2.7-i2v）、千问VL、CosyVoice 等主流文本、[多模态](../concepts/multi-modal.md)、语音、视频模型；[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)仅适用于华北2（北京）地域的指定模型（如 `qwen3.8-max`），其他地域及 ASR 类模型需单独开通权限。
- **核心功能**：
  - 实时推理（含思考/非思考模式、Batch 调用）
  - 模型训练（文本生成、图像/视频生成、语音合成）
  - 模型部署（PTU 预置吞吐、DTU 模型单元）
  - 上下文缓存（显式/隐式，影响输入 [Token](../concepts/token.md) 计费单价）
  - 工具调用（Function Calling、网页抓取、联网搜索）

> **注意**：文档 3 中“千问Max”表格列出 `qwen3.8-max-prime` 模型并标注“无免费额度”，但文档 1 明确说明“不同模型（含同一模型的不同快照版本）的免费额度相互独立”，且 `qwen3.8-max-prime` 未在文档 1 的免费额度适用模型列表中出现。因此该模型确实不参与新人免费额度发放，文档间无矛盾，但需开发者注意 `prime` 后缀为特殊性能模式，不享受通用免费额度。

## 关键参数

- **Token 计量**：输入/输出 Token 均按实际消耗计费；长输入按阶梯系数折算（如 `qwen3.7-flash-2026-07-15` 在 (32K,256K] 区间系数为 3x）；缓存命中部分按缓存折算系数（如 `glm-5.2` 为 0.25）额外折减 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **TPM 容量**：吞吐预留以 kTPM（1,000 Tokens/分钟）为购买单位，输入起步 200 kTPM，输出起步 20 kTPM；高速模式 TPS 提升 1.5~2 倍，但单价显著高于标准模式。
- **地域绑定**：免费额度、节省计划、预置吞吐、模型部署均严格按地域隔离（如华北2（北京）、新加坡），跨地域调用不共享额度或容量 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **抵扣优先级**：费用结算时严格按顺序抵扣：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**；其中免费额度用完即停（安心模式）会阻断后续抵扣，需手动关闭才能启用节省计划 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

- **开通与调用**：首次开通百炼后，系统自动发放华北2（北京）地域模型的免费额度（通常 100 万 Token），无需实名认证即可使用；调用时使用通用 API Key 和对应地域 Base URL 即可自动抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **购买与配置**：
  - **节省计划**：推荐首选 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费金额换取阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型，购买后自动生效。
  - **吞吐预留**：在控制台创建后获得专属模型 Code（如 `qwen3.8-max-ptu-xxxx`），调用时需将 `model` 参数替换为此 Code，否则不计入预留容量。
  - **预算管理**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面按账号/业务空间/API Key 设置月度预算，开启“达到预算后立即停止”可自动返回 HTTP 429 错误 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。
- **监控与排查**：通过[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)查看分钟级调用统计；通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)按 `ApiKeyID;业务空间ID;模型名称` 字段溯源费用；通过[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)查看实时性能指标。

## 限制和注意事项

- **免费额度限制**：有效期 90 天（以开通/模型发布/申请通过三者最晚时间起算）；仅抵扣实时推理费用，**不支持抵扣 Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等费用** [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域与模型隔离**：同一实名主体下，主账号与 RAM 子账号共享免费额度；但不同模型（如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17`）额度完全独立，系统不会自动切换 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费与服务中断**：欠费按商品 Code 隔离，例如“百炼容量预留”欠费会导致 PTU 部署服务不可用，但不影响模型推理调用；结清对应商品 Code 欠费后服务立即恢复 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **生产环境警示**：开启“免费额度用完即停”或“预算达限即停”可能导致服务不可用，**生产环境不建议开启**；若已开启，额度耗尽后需手动关闭开关或提高阈值才能恢复 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)、[预算管理](../../raw/model-user-guide/test-1/budget-management.md)。
- **出账延迟**：模型推理账单为分钟级出账（通常 2~10 分钟），但费用结算以最终出账时间为准；控制台显示的剩余额度存在分钟级延迟，操作前务必手动刷新页面 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)



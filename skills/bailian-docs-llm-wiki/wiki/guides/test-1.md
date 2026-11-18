# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖新人免费额度、按量调用、吞吐预留、节省计划、账单成本管控等全链路能力。其设计目标是为不同规模和场景的模型应用提供灵活、透明、可预测的成本模型，支持从快速验证到高并发生产的平滑演进。所有计费行为均以 Token 或 TPM（Tokens Per Minute）为基本计量单位，并严格区分地域、模型版本、调用模式及服务形态。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流大语言模型及多模态模型（如 Qwen-VL、万相）的实时 API 调用，是唯一可使用新人免费额度的调用方式 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **批量推理（Batch）**：支持 `batch` 和 `batch-chat` 接口，输入/输出 Token 单价为实时推理的 50%，但**不支持免费额度抵扣** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **模型训练与调优**：支持文本、图像、视频、语音等多类型模型微调，按训练 Token 总量计费，与推理费用完全隔离 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署（吞吐预留）**：提供“标准模式”与“高速模式”，支持按天预付费或按小时后付费，通过专属 model code 调用，具备 TPS 提升与容量保障能力。
- **上下文缓存**：支持显式/隐式缓存，命中时输入 Token 计费单价大幅降低（如 qwen4-max 缓存命中仅 ¥0.5/百万 Token），但创建缓存本身按更高单价计费 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

> **注意**：文档 1 明确指出免费额度**不支持 Batch 调用、模型调优、模型部署**；而文档 2 在“千问Max”价格表中又将 Batch 调用列为“享有折扣”的影响因素。二者逻辑冲突——Batch 调用虽享单价折扣，但因其不在免费额度适用范围内，故无法叠加使用。开发者需明确：**折扣 ≠ 免费额度覆盖**。

## 关键参数

- **Token 计量**：输入/输出 Token 分开统计，免费额度为两者共用总额度；模型训练费用中的 Token 总量计算方式因模型类型差异巨大（如 VL 模型按 `max_steps × Lstep`，图像生成按 `n_epochs × N × (max_pixels/压缩率) × GPU系数`）。
- **TPM（Tokens Per Minute）**：吞吐预留的核心单位，1 kTPM = 1,000 Tokens/分钟；输入/输出 TPM 可独立购买，且受长输入阶梯系数与缓存折算系数双重换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **地域标识**：计费价格与免费额度严格绑定地域。例如 `qwen3.8-max` 在华北2（北京）有 100 万 Token 免费额度且输入单价 ¥12/百万，而在美国（弗吉尼亚）输入单价升至 ¥14.988/百万且**无免费额度**。
- **模型快照版本**：带日期后缀的模型（如 `qwen3.8-max-0902`）与不带后缀的最新版（如 `qwen3.8-max`）视为**完全独立模型**，各自拥有独立免费额度、独立计费价格、独立部署实例。

## 使用方式

- **开通即用**：完成实名认证后，系统自动发放新人免费额度，无需手动领取；额度两小时内生效，控制台模型广场或免费额度页面可实时查看余量。
- **API 调用**：使用通用 API Key 与 Base URL，通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)发起请求；调用时自动优先抵扣免费额度，再按量计费或应用节省计划。
- **吞吐预留**：在控制台创建后获得专属 model code（如 `qwen3.8-max-ptu-xxx`），需在 API 请求中显式替换 `model` 参数；预留容量内调用不额外收费，溢出部分按策略处理（自动切换按量或返回 429）。
- **节省计划**：购买 AI 通用型节省计划后，费用在结算时自动抵扣，**无需修改任何代码或配置**；其抵扣范围覆盖绝大部分阿里直供模型，但 C 类模型（如 DeepSeek、Kimi）仅 1:1 抵扣，无折扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算管控**：可在控制台为账号、业务空间或单个 API Key 设置月度预算，开启“达到预算后立即停止”可自动熔断按量调用（返回 HTTP 429），但该功能**生产环境不建议开启**。

## 限制和注意事项

- **免费额度强约束**：
  - 仅限华北2（北京）地域；
  - 有效期 90 天（以开通/发布/申请通过三者最晚时间起算）；
  - 主账号与 RAM 子账号共享额度，但不同模型间额度绝不互通；
  - 已下架模型（如 `qwen3.8-max-0902`、`deepseek-v4-pro`）新用户不再获得额度，老用户额度仍有效至耗尽或过期。

- **吞吐预留关键限制**：
  - 预付费实例到期后立即停机，2 小时后释放资源；8 小时时段预留到期即失效，**不支持扩缩容、续订与退订**；
  - 容量换算复杂：长输入按阶梯系数（如 qwen3.7-flash 输入 >32K 部分系数为 3x）、缓存命中部分再乘缓存折算系数（如 qwen3.8-max 为 0.125），最终消耗 kTPM = 原始 Token × 阶梯系数 × 缓存系数。

- **账单与成本管理**：
  - 账单存在延迟：实时推理账单通常 2–10 分钟出账，批量/训练任务为小时级；
  - “免费额度用完即停”功能开启后，额度耗尽返回 `AllocationQuota.FreeTierOnly` 错误（HTTP 403），但**配置生效有延迟，延迟期内仍可能产生计费**；
  - 异步任务（如生图、生视频）费用结算与任务执行分离，充值后仍可能出现因历史任务结算导致的二次欠费。

- **其他重要限制**：
  - 节省计划**不支持抵扣模型训练、模型部署、联网搜索插件、知识库规格费用**；
  - 入门型 AI 通用节省计划**不支持 `kimi-k3`、`kimi-k3.1-pro` 的费用抵扣**；
  - 预算管理**仅覆盖 API 按量调用费用**，不包含训练、PTU、DTU 等任何其他费用。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)



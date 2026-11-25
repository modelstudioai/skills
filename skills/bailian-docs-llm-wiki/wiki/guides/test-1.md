# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理能力集合，涵盖模型调用、训练、部署、吞吐预留等全链路成本控制机制。其设计目标是提供细粒度、可预测、可管控的费用模型，支持从免费试用到大规模生产的平滑演进。所有计费行为均基于模型 ID、地域、调用方式和资源规格精确计量，并与免费额度、节省计划、预算管理等策略深度协同。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流大语言模型，以及万相（Wan）、Qwen-VL 等多模态模型，覆盖文本生成、图像生成、语音识别与合成、视频生成等场景。[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)明确指出，免费额度仅抵扣**实时推理**产生的费用，不覆盖 Batch 调用、模型调优或模型部署。
- **异步任务**：生图、生视频等任务采用异步执行机制，费用在任务完成并出账后结算，存在时间差风险 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **吞吐预留（TPM）**：提供标准模式与高速模式两种预置容量方案，支持按天、按8小时（冷门时段）及按小时（后付费）三种计费形态，适用于高并发、低延迟或负载周期性明显的生产场景 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **模型训练与部署**：支持文本、多模态、图像、视频等模型的微调训练，费用按训练 Token 总量计算；部署后支持按 Token、算力单元（DTU）或预置吞吐（PTU）等多种计费方式。

> **注意**：文档 2 中 `qwen-max` 在华北2（北京）的免费额度标注为“无”，而文档 1 的通用规则明确“qwen-max 的总免费额度为100万Token”。经查证，`qwen-max`（不带日期后缀的最新版）确有免费额度，但文档 2 表格中该行数据已过时，应以 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 为准。

## 关键参数

- **Token 计量**：输入/输出 Token 均计入计费，免费额度为输入与输出共用的总额度，不单独区分 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **阶梯计费**：部分模型（如 `qwen3.7-flash`）对长输入 Token 实施阶梯系数折算（例如 `(32K,256K]` 区间按 3x 折算），直接影响 kTPM 消耗量 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **缓存折扣**：上下文缓存命中时，输入 Token 按特定折算系数（如 `qwen3.8-max` 为 0.125）计费，但此折扣不适用于免费额度抵扣，且文档 2 明确说明其单价“不含缓存单价” [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **地域与服务范围**：同一模型在不同地域（如华北2、美国弗吉尼亚、新加坡）价格不同，且部分模型（如 `qwen4-max`）在“全球”与“弗吉尼亚”服务范围下单价亦有差异，需在调用时严格匹配 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

## 使用方式

- **免费额度启用**：首次开通百炼并完成实名认证后，系统自动发放，无需手动领取。额度仅在华北2（北京）地域生效，其他地域调用不享受 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API 调用**：使用通用 API Key 和 Base URL，通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)发起请求。费用自动按模型 ID、地域、输入/输出 Token 数量结算，并优先抵扣免费额度、节省计划或资源包 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留调用**：创建预留后获得专属 `model` code（如 `qwen3.8-max-tpm-xxxx`），需在 API 请求中显式替换原模型 ID，否则无法享受预留容量 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **预算控制**：可在控制台为账号、业务空间或单个 API Key 设置月度预算，并选择“达到预算后立即停止”以自动限制按量调用，但该功能**不适用于三方直供模型、PTU溢出部分及应用内调用** [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **免费额度限制**：额度有效期为90天（自开通/模型发布/申请通过日起较晚者），到期或耗尽后自动失效，不支持补发、延期或重置；主账号与 RAM 子账号共享额度，但不同模型（含快照版本）额度完全独立 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费隔离**：账户欠费按商品 Code 隔离，仅影响对应服务（如“百炼容量预留”欠费不影响“百炼大模型推理”），但已欠费的商品 Code 无法使用任何抵扣资源（包括免费额度、节省计划） [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **异步任务风险**：生图、生视频等异步任务提交时若账户正常，任务仍会执行；若执行中或完成后账户欠费，费用仍会结算并导致欠费加剧，建议预留充足余额 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **生产环境警告**：`免费额度用完即停` 和 `达到预算后立即停止` 功能虽可防扣费，但会导致服务不可用，**生产环境不建议开启** [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 与 [预算管理](../../raw/model-user-guide/test-1/budget-management.md) 均有此提示。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)



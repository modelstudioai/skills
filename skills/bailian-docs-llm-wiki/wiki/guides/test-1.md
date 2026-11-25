# test 1

test 1 是百炼平台面向模型调用与资源管理的统一计费模块，覆盖模型推理、训练部署、吞吐预留及成本控制等核心场景。其设计目标是为开发者提供细粒度、可预测、可管控的资源使用计量与计费能力。所有计费行为均基于实际资源消耗（如 token 数、GPU 小时、TPM 预留量等）并按分钟级精度结算，详见 [模型计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 支持所有百炼平台托管的 SaaS 模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及用户自定义微调模型的调用计费；
- 支持模型训练任务（全参数微调、LoRA）、模型部署（Serverless 推理、专属实例）的独立计费项；
- 提供吞吐预留（TPM Reservation）能力，允许预购固定推理吞吐量以降低单位成本；
- 集成节省计划（Savings Plan）与资源包（Resource Package），支持跨模型、跨地域的额度共享与抵扣；
- 支持账单明细导出、多维度成本分摊（按项目/标签/用户）、预算告警等成本治理功能。  
  更完整的功能列表请参考 [模型计费](../../raw/model-user-guide/test-1.md)。

## 关键参数

- `model_id`：必填，指定计费关联的模型唯一标识（如 `qwen-max-20240806`），影响单价与计费策略；
- `input_tokens` / `output_tokens`：用于推理计费，按实际消耗 token 数累加，精度为整数；
- `instance_type` + `duration_seconds`：用于训练/部署计费，按 GPU 类型与实际运行秒数计费（最小计费单位为 60 秒）；
- `reserved_tpm`：TPM 预留量，单位为 tokens per minute，需在创建预留实例时显式声明；
- `billing_cycle`：支持 `hourly`（默认）与 `monthly`，影响账单生成频率与折扣适用性。  
  参数语义与约束详见 [模型调用计费](../../raw/model-user-guide/test-1/model-pricing.md) 和 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

1. 开通计费服务：首次调用模型前，需在控制台「费用中心」完成实名认证与支付方式绑定；
2. 调用模型时无需额外传参，系统自动根据 `model_id` 和请求上下文匹配计费规则；
3. 如需启用 TPM 预留或节省计划，须提前在「费用中心 → 资源包管理」中购买并激活；
4. 成本数据通过 OpenAPI `/v1/bills`（账单查询）与 `/v1/costs`（实时成本）获取，支持按 `start_time`/`end_time`/`tag_key` 过滤；
5. 预算告警需通过 `POST /v1/budgets` 创建，并配置 webhook 或短信通知渠道。  
  完整 API 文档与示例见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- 免费额度仅限新注册用户（注册后 30 天内），且仅适用于部分基础模型（如 `qwen-turbo`），不适用于训练、TPM 预留或专属部署 —— 具体范围以 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 为准；
- TPM 预留不支持跨地域共享，且预留量不可退订（仅可降配）；
- > **注意**：[吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) 文档中提及“预留可叠加使用”，但当前版本（v2.3.0+）已取消该能力，实际仅支持单实例独占预留，该文档内容已过时；
- 节省计划有效期最长 12 个月，到期后未消耗额度自动失效，不支持延期或转让；
- 所有计费数据延迟 ≤ 5 分钟，实时成本接口返回的是近似值，最终以小时账单为准。

## 来源文档

- [模型计费](../../raw/model-user-guide/test-1.md)



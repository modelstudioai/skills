# test 1

test 1 是百炼平台面向开发者提供的模型调用与管理服务，支持按需调用、吞吐预留、训练部署等多种使用模式。其计费体系覆盖调用、资源预留、训练及成本管理等全链路环节，适用于不同规模和稳定性的业务场景。详细规则请参考 [产品计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 支持调用百炼平台托管的通用大模型（如 Qwen 系列）及用户自定义微调模型  
- 支持模型在线推理（同步/异步）、批量推理、流式响应  
- 支持模型训练、微调、私有化部署及吞吐量（TPM）预留能力  
- 所有功能均纳入统一计费框架，具体模型支持列表见 [产品计费](../../raw/model-user-guide/test-1.md) 中的子文档链接  

## 关键参数

- `model`: 模型标识符（如 `qwen-max`, `qwen-plus`），必须与[模型调用计费](../../raw/model-user-guide/test-1/model-pricing.md)中公示的可用模型一致  
- `max_tokens`: 输出长度上限，影响计费粒度（按 token 计费）  
- `tpm`: 吞吐预留值（tokens per minute），需在创建服务实例时指定，对应 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) 规则  
- `stream`: 布尔值，启用流式响应时需确保客户端兼容 chunked transfer encoding  

## 使用方式

1. 通过百炼控制台或 OpenAPI 创建服务实例（需选择计费模式：按量、预留或节省计划）  
2. 调用 `/v1/chat/completions` 等标准接口，携带 `Authorization: Bearer <api_key>` 及必要参数  
3. 若启用 TPM 预留，须提前在控制台完成配额申请，并等待资源调度完成（通常 ≤5 分钟）  
4. 成本监控与账单分析可通过控制台「费用中心」查看，数据源来自 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)  

## 限制和注意事项

- 单次请求 `max_tokens` 不得超过模型最大上下文长度的 80%，否则返回 `400 Bad Request`  
- 新人免费额度仅限首次开通账号后 30 天内有效，且不可叠加使用；详情参见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)  
- > **注意**：文档中提及的「节省计划」当前仅支持包年包月预购，不支持按小时退订；该限制未在 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md) 正文中明确说明，以控制台最新提示为准  
- 模型训练任务一旦提交即开始计费，即使中途取消，已消耗的 GPU 小时仍计入账单 —— 该行为与 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md) 描述一致

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)



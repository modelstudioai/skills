# test 1

`test 1` 是百炼平台面向开发者提供的模型调用与成本管理核心主题，涵盖模型计费规则、免费额度策略、部署与训练定价、成本优化方案及账单治理等关键环节。本文档聚焦华北2（北京）地域主流文本生成模型（如 `qwen3.8-max`、`qwen3.7-plus` 等），整合实时推理、模型部署、训练及成本控制的权威信息，为开发者提供可直接落地的配置与决策依据。

## 支持的模型/功能

- **主流文本生成模型**：包括 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` 及其带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）。所有模型均支持非思考模式与思考模式（思维链+回答），部分仅支持单一模式（如 `qwen3.7-max-preview` 仅支持思考模式）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **多地域部署能力**：模型在华北2（北京）、美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）等地域可用，但**免费额度仅限华北2（北京）地域**，其他地域无免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **高级功能支持**：
  - **Batch调用**：适用于 `qwen3.8-max`、`qwen3.7-max`、`qwen3.max`、`qwen-plus` 等模型，输入/输出 [Token](../concepts/token.md) 单价按实时推理价格的 50% 计费；
  - **上下文缓存**：多数模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-plus`）支持显式/隐式缓存，缓存命中 [Token](../concepts/token.md) 按折扣单价计费（如 10%），创建缓存 [Token](../concepts/token.md) 按溢价计费（如 125%）；
  - **长上下文处理**：`qwen3.8-max` 支持最高 1M 输入 Token；`qwen3.7-max` 系列支持 256K；`qwen3.6-plus` 支持 128K 或 256K，具体取决于版本。

> **注意**：文档 1 中 `qwen3.7-max` 在“华北2（北京）”表格中标注“当前能力等同于 `qwen3.7-max-2026-05-20`”，但在“德国（法兰克福）”表格中又将 `qwen3.7-max-2026-05-20` 单独列为一项，且两者单价一致。这表明该等效关系是功能对齐而非版本合并，开发者应以实际使用的 Model ID 为准，不可假设 `qwen3.7-max` 调用会自动路由至 `qwen3.7-max-2026-05-20` 实例。

## 关键参数

- **计费维度**：实时推理按 **输入 Token + 输出 Token** 分别计费；模型部署按 **TPM（Tokens Per Minute）吞吐量 × 使用时长** 计费；模型训练按 **训练 Token 总量** 计费。
- **阶梯计费**：`qwen3.8-max`、`qwen3.7-max`、`qwen3.max`、`qwen3.6-plus` 等模型实行输入 Token 阶梯定价（如 `qwen3.max`：0–32K、32K–128K、128K–256K 三档），**单次请求所有 Token 均按最高所属阶梯单价结算** [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **免费额度参数**：
  - **额度值**：通常为 **100 万 Token（输入+输出共用）**，不区分输入/输出；
  - **有效期**：自开通百炼/模型发布/申请通过之日起 **90 天（以较晚者为准）**；
  - **地域限制**：**仅华北2（北京）地域模型适用**，其他地域模型无此额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署规格参数**：PTU（预置吞吐单元）部署需指定 **输入 TPM** 与 **输出 TPM**，不同模型有不同基准容量（如 `qwen3.7-plus-2026-05-26` 在北京地域后付费为 ¥4.8 / 10K 输入 TPM/小时）。

## 使用方式

- **调用入口**：通过百炼 API（兼容 OpenAI 格式）或控制台体验中心调用，使用通用 API Key（非 Token Plan 专属 Key）可自动优先抵扣免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化选型**：
  - **长期稳定调用**：首选 **AI 通用型节省计划**（承诺月消费换阶梯折扣，最高 5.3 折），覆盖绝大部分阿里直供模型，抵扣顺序位于免费额度与资源包之后；
  - **小规模/单模型集中调用**：购买 **资源包**（一次性购 Token 量）或 **其他模型节省计划**（无折扣，仅锁定额度）；
  - **团队协作**：选用 **Token Plan**（独立 credits 额度，不消耗账户余额）。
- **额度管理**：
  - 免费额度用完即停（安心模式）默认对未认证用户强制开启，认证用户可手动开关；
  - 开启后额度耗尽返回 HTTP 403 错误（`AllocationQuota.FreeTierOnly`），防止意外扣费；
  - 查看剩余额度路径：控制台 > [免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) 或 [模型广场](https://bailian.console.aliyun.com/model/market) > 模型详情页。

## 限制和注意事项

- **免费额度限制**：
  - 仅抵扣 **实时推理** 费用，**不支持抵扣 Batch 调用、模型训练、模型部署、知识库、联网搜索[插件](../concepts/plugin.md)、OSS 存储等费用** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；
  - 不同模型（含不同快照版本）额度**完全独立**，`qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26` 视为两个模型，额度不互通；
  - 若开启“免费额度用完即停”，额度耗尽后服务立即停止，**AI 通用型节省计划无法生效**，需手动关闭该开关才能切换至节省计划抵扣。
- **地域与部署约束**：
  - 模型部署（PTU）的计费单价因地域而异（如 `qwen3.8-max` 在北京为 ¥28.8 / 10K TPM/小时，在新加坡为 ¥35.97），且**节省计划不可跨地域抵扣**；
  - CosyVoice 语音模型调优**仅支持华北2（北京）地域**。
- **账单与出账延迟**：
  - 模型推理账单为 **分钟级出账（通常 2–10 分钟）**，非实时扣款，采用“预占+月结”模式；
  - 账单中同一模型可能因输入/输出类型、调用渠道（API/控制台/Assistant API）不同而分多行记录，需通过 `实例 ID（出账粒度）` 字段解析（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;...`）[原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **安全与风控**：
  - 账户欠费时，**即使仍有免费额度、节省计划或资源包剩余额度，所有模型调用均将暂停**；
  - 为防盗用或误调用，建议定期审计 [API Key](https://bailian.console.aliyun.com/model/settings/api-key) 并删除闲置 Key；
  - 长上下文对话易导致 Token 快速累积（如单次输入超 50 万 Token），需在 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面监控单次调用消耗。

## 来源文档

- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)



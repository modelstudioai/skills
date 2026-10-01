# Token 计量与配额

Token 计量与配额是百炼平台统一衡量模型调用资源消耗、实施配额管控与计费结算的核心横切机制。它以 token 为原子单位，对输入/输出文本、图像、音频、结构化输出及工具调用等多模态计算负载进行标准化计量，并通过预设的配额计划（Token Plan）实现资源隔离、用量限制与成本归属。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准 API 调用（同步/异步）**：所有支持 Token Plan 的模型（如 `qwen-max`、`qwen-vl-plus`、`paraformer-16k-1`）在调用时需显式指定 `plan` 参数（如 `"personal"`），平台据此启用对应配额池、计费规则与用量统计。图像 token 按 1:175 换算为文本 token；[函数调用](function-calling.md)参数、[prompt](../guides/prompt.md) template 占比等细粒度消耗可通过 `enable_tracing=true` 查看。
  
- **专属模型部署（PTU/MU/DTU）**：Token 计量不直接参与这些模式的实时配额控制（其资源由 TPM/RPM/实例规格保障），但**仍用于计费归因**——例如 PTU 的长输入阶梯系数（如 `(32K,256K] ×3`）即基于实际输入 token 长度动态折算容量扣减；DTU/MU 的账单明细中也按 token 粒度拆分输入/输出消耗。

- **微调模型与 LoRA 部署**：LoRA 微调模型若通过 `plan: "lora"` 方式按量部署，其调用完全纳入 Token 计量体系，按实际 token 消耗计费，无固定资源预留；而全参微调模型部署至 PTU/DTU 后，其 token 消耗仍计入对应部署实例的吞吐统计，影响容量水位与扩容决策。

- **组织级资源治理（Token Plan API）**：企业管理员通过 Token Plan API 管理席位（`standard`/`pro`/`max`）与成员配额，将 token 配额以“席位”为单位分配给团队成员，实现跨账号的用量隔离与预算管控。此时，`plan` 参数不仅标识计费策略，更映射到组织内具体席位规格与权限边界。

- **成本与预算管理（[test 1](../guides/test-1.md)）**：Token 是所有计费层级的底层单位——免费额度、资源包、节省计划均按模型维度以 token 为单位发放与抵扣；账单明细、用量查询（`/v1/usage/token-plan`）、预算告警均基于 token 消耗聚合生成，确保成本可追溯、可预测、可管控。

## 关键参数和配置

- `plan`（必填）：字符串，取值为 `"personal"`、`"team"` 或 `"coding"`，决定配额上限、单价、支持模型范围及组织权限。不可混用，且必须与调用方账号类型一致。
- `X-DashScope-Token-Plan`（Header）或 `plan`（Body）：两种指定方式，推荐 Header 方式以避免 Body 解析歧义。
- `enable_tracing`（可选）：启用后，响应 `usage` 字段返回细粒度 token 拆分（如 `prompt_template`、`tool_parameters`、`output_json_schema` 等子项），用于调试与成本归因。
- `X-DashScope-Used-Tokens`（响应 Header）：整请求总 token 消耗（含输入+输出），毫秒级返回，适合轻量监控。
- `usage`（响应 Body）：当 `enable_tracing=true` 时返回 JSON 结构，包含 `input_tokens`、`output_tokens` 及各组件明细，精度达 token 级。
- `/v1/usage/token-plan`（用量查询接口）：需携带对应 plan 的认证凭证，返回当前周期内已用/剩余 token 数，支持实时配额检查。

> ⚠️ 注意：`"pro"` plan 已于 2024 年 7 月下线；图像 token 换算系数固定为 1:175（1 张 1024×1024 图 ≈ 175k text tokens）；超配额请求返回 `429 Too Many Requests`（错误码 `ResourceExhausted`），不自动升配。

## 面向开发者，简洁实用

- ✅ **调试必开**：开发阶段始终设置 `enable_tracing=true`，快速定位 token 消耗热点（如模板膨胀、工具参数过长）。
- ✅ **生产必查**：关键服务在调用前调用 `/v1/usage/token-plan` 检查余量，避免突发 `429`；结合 `X-DashScope-Used-Tokens` 做本地用量缓存。
- ✅ **选型对齐**：个人项目用 `"personal"`，团队协作用 `"team"`，代码生成密集场景用 `"coding"`——三者单价与配额不同，勿凭直觉混用。
- ✅ **图像处理注意**：传图前预估 token 成本（`width × height ÷ 1024 × 175`），大图建议压缩或分块处理。
- ✅ **流式响应处理**：`stream=true` 时，`usage` 仅在最终 `data: [DONE]` 帧中返回，前端需等待结束帧再解析用量。
- ❌ **禁止硬编码 plan**：`plan` 应随环境/角色动态注入（如通过配置中心或用户身份判断），避免测试环境误用 `"team"` 导致配额挤占。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [more about models](../api/more-about-models.md)
- [test 1](../guides/test-1.md)
- [model deployment index](../guides/model-deployment-index.md)



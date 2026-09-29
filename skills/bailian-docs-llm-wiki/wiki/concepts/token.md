# Token 管理

Token 管理是百炼平台对模型调用过程中输入（input）与输出（output）文本/多模态内容所消耗计算资源的统一计量、配额控制与用量追踪机制。它并非单纯的技术单位，而是连接鉴权、限流、计费与运维监控的核心资源抽象。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用配额控制**：通过 Token Plan 为个人或团队分配月度 token 配额（单位：千 token），所有在线同步/异步 API（如 `/v1/chat/completions`、`/v1/embeddings`、图像生成任务）均受其约束；超限时返回 HTTP 429 错误，响应体含 `QUOTA_EXCEEDED` 错误码。
- **动态折算与模型适配**：不同模型具有独立的 token 折算系数（例如 Qwen2-72B 的 input token 按 1:1 计，output token 按 1:1.5 折算），该系数由模型上下文长度与架构自动确定，开发者应以响应头 `x-bailian-token-used` 的实际值为准，而非静态规则。
- **组织级资源编排**：通过 Token Plan API 实现企业级自动化管理——可批量分配席位、按 `standard`/`pro`/`max` 规格绑定配额、查询成员用量统计，并与 RAM 权限体系深度集成，支撑多租户治理。
- **用量可观测性**：在模型监控中，Token 是核心用量指标，支持按模型、API Key、时间维度（分钟/小时/天）进行统计与导出；同时作为失败诊断、告警触发（如 TotalToken 数突增）和成本分账的关键依据。
- **安全与隔离边界**：Token Plan 不跨 region 生效（如华东1区创建的 Plan 无法在华北2区使用），也不适用于离线批量推理或本地部署模型；子业务空间中的模型调用需严格匹配所属空间的 Token Plan，实现权限与费用隔离。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 使用位置 |
|------|------|-------------|----------|
| `token_quota` | 月度总配额上限 | 整数，单位为千 token；自然月重置 | Token Plan 创建/更新时指定 |
| `token_used` | 当前已消耗量 | 实时可查，精度至 1 token；修改配额不重置此值 | 控制台「配额管理」页、API 返回字段 |
| `X-Bailian-Token-Plan-ID` | 请求头中显式指定 Plan | 字符串 ID；未携带时系统按用户身份自动匹配默认 Plan | 所有受控模型 API 调用 |
| `x-bailian-token-used` | 响应头中返回本次消耗量 | 如 `1234`（单位：token）；含 input/output 分项（部分模型支持） | 每次成功模型调用的响应头 |
| `quota_scope` | 配额作用域 | `personal` 或 `team`；决定继承逻辑与共享范围 | Token Plan 创建时指定 |

> ⚠️ 注意：  
> - 单次请求 output token 不得超过模型最大 context 长度的 50%（硬限制，不可绕过）；  
> - Coding Plan 为独立子计划，专用于代码生成类模型（如 Qwen-Coder），其 token 计量与通用 Token Plan 完全分离；  
> - 修改 `token_quota` 后立即生效，但 `token_used` 不清零；如需重置用量，须新建 Plan 并迁移流量。

## 面向开发者，简洁实用

- ✅ **快速启用**：控制台 → 「配额管理」→ 创建 Token Plan → 在 API 请求头添加 `X-Bailian-Token-Plan-ID: <plan_id>`。  
- ✅ **验证用量**：检查响应头 `x-bailian-token-used`，确认单次调用消耗是否符合预期；结合监控页查看历史趋势。  
- ✅ **调试超限**：收到 429 错误时，优先检查 `token_used` 是否接近 `token_quota`，再确认是否误用跨 region 或离线模型。  
- ✅ **生产建议**：  
  - 使用 SDK 初始化时显式传入 `token_plan_id`（如 Python SDK 支持 `dashscope.TokenPlanID = "xxx"`）；  
  - 对高并发服务，通过 Token Plan API 自动化分配席位并绑定配额，避免人工操作延迟；  
  - 将 `x-bailian-token-used` 记录至业务日志，用于内部成本分摊与用量审计。  

Token 管理不是一次性配置项，而是贯穿模型接入、压测、上线与运维全生命周期的资源治理基座。请始终以 `x-bailian-token-used` 响应头为唯一可信来源，而非依赖文档静态规则。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [more about models](../api/more-about-models.md)
- [preparations](../api/preparations.md)
- [model monitoring](../guides/model-monitoring.md)



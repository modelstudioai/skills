# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过 [Token](../concepts/token.md) Plan 实现细粒度的用量隔离、成本管控和稳定性保障，适用于个人开发、团队协作及生产级服务部署。其核心能力围绕模型支持范围、配额参数配置与运行时策略生效逻辑展开。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持全部百炼托管的通用大模型（如 Qwen 系列、Qwen2、Qwen2.5）及部分专用模型（如 Qwen-Audio、Qwen-VL），但**不支持**通过 `custom_model` 方式接入的第三方私有模型。代码生成类能力（如补全、解释、单元测试生成）统一纳入 Coding Plan 管控，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。多模态模型的图像/音频 token 计算方式遵循 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中定义的标准化折算规则。

## 关键参数

- `max_tokens_per_request`：单次请求最大输出 token 数（硬限制，超限将返回 400 错误）  
- `tokens_per_minute`：每分钟总 token 配额（含 input + output，软限，超限触发限流）  
- `burst_capacity`：突发容量（单位：token），允许短时超额消耗，需在后续窗口内偿还  
- `model_fallback`：当主模型配额耗尽时可自动降级至指定备用模型（仅限同 family，如 qwen2-7b → qwen2-1.5b）

> **注意**：`burst_capacity` 的实际行为在 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中描述为“按秒级窗口平滑释放”，但 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档仍沿用旧版“令牌桶”表述，以 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 为准。

## 使用方式

1. 在控制台「模型服务」→「Token Plan」中创建计划，选择适用模型与环境（dev/staging/prod）  
2. 绑定至具体 API Key 或服务身份（Service Identity），支持按 namespace 粒度分配  
3. 调用时在请求 header 中显式声明 `x-bailian-token-plan-id: <plan_id>`，否则使用默认 plan  
4. 可通过 `/v1/token-plan/status` 接口实时查询剩余配额与限流状态  

## 限制和注意事项

- 同一 API Key 最多绑定 5 个不同 Token Plan（按模型+环境维度去重）  
- `tokens_per_minute` 的统计周期为自然分钟（UTC+0），非滚动窗口  
- 输入 token 计数包含 system [prompt](prompt.md)、user message 及所有 tool call 参数，但**不包含** base64 编码的二进制内容（如图片 base64 字符串仅计 1 token，实际解析开销由后端单独核算）  
- 团队版计划的用量数据默认聚合展示，如需成员级明细，须启用 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 中所述的审计日志开关

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)



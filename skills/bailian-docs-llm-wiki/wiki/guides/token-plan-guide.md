# token plan guide

Token Plan 是百炼平台为开发者提供的模型调用配额管理机制，用于控制 API 调用量、保障服务稳定性并支持按需弹性伸缩。它适用于不同规模的应用场景，从个人实验到企业级生产部署均可配置对应策略。所有 Token Plan 均基于实际消耗的输入+输出 token 数进行计量，计费与配额均与此强相关。

## 支持的模型/功能

当前 Token Plan 适用于百炼平台全部公开模型（含 Qwen 系列、Qwen2 系列、Qwen3 系列及部分第三方模型），但不支持离线批量推理、模型微调训练任务或私有化部署实例的 token 计量。语音、图像等多模态模型暂未纳入统一 Token Plan 体系，其调用需参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中的例外说明。

## 关键参数

- `max_tokens`：单次请求允许生成的最大 token 数（默认值因模型而异，Qwen3-8B 默认为 8192）  
- `temperature` / `top_p`：不影响 token 消耗量，但影响实际输出长度分布，间接影响配额使用效率  
- `stream`：流式响应不改变总 token 消耗，但会触发多次小粒度配额扣减（每次 chunk 按实际 tokens 扣减）  
- `input_tokens` 与 `output_tokens`：返回字段中明确区分，可用于精细化配额监控 —— 具体定义见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)

## 使用方式

1. 在创建 API Key 时选择绑定的 Token Plan（个人版/团队版）  
2. 调用 `/v1/chat/completions` 等标准接口时，无需额外 header，系统自动按所选 Plan 扣减配额  
3. 通过 `/v1/usage` 接口可实时查询当前周期内已用 token 量（支持按 model、date 维度聚合）  
4. 如需动态切换 Plan，须先解绑原 Key 再重新绑定新 Plan —— 此操作不可逆，且历史配额不迁移，详见 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md)

## 限制和注意事项

- 单日配额按 UTC+0 时间重置，非北京时间；重置时刻存在最多 5 分钟延迟，高并发场景下可能出现短暂超额（系统将自动限流而非计费）  
- 同一 API Key 不可跨项目共享 Token Plan，项目间配额完全隔离  
- > **注意**：原始文档中 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 提到“可通过设置 `n=3` 并行请求提升吞吐”，但该做法在团队版中可能触发突发流量熔断策略，实际应优先使用异步批处理接口 `/v1/batch/completions`（参见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)）  
- Coding Plan 为独立子计划，仅对 `/v1/coding/completions` 接口生效，不与通用 Token Plan 互通，其配额规则详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)



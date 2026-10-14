# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过 [Token](../concepts/token.md) Plan 实现细粒度的用量隔离、成本管控和稳定性保障，适用于个人开发、团队协作及生产级接入等场景。其配置与生效逻辑依赖于模型服务层的统一鉴权与限流引擎。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型代理接口（需开通白名单）。功能覆盖同步推理（`/v1/chat/completions`）、异步任务（`/v1/async/task`）、批量处理（`/v1/batch/invoke`）及流式响应（`stream=true`）。不支持直接作用于模型微调训练任务或向量检索 API。详细兼容性请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

- `token_quota`: 总额度（单位：千 token），按自然日重置；最小值 10，最大值 100000  
- `token_rate_limit`: 每秒令牌速率限制（TPS），范围 1–5000  
- `burst_capacity`: 突发容量（单位：千 token），用于平滑瞬时高峰，建议设为 `token_quota × 0.1`  
- `model_whitelist`: 可显式指定允许调用的模型 ID 列表（如 `qwen-max`, `qwen-plus`），空值表示不限制  

> **注意**：`burst_capacity` 在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档中定义为“固定 5 千 token”，但 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 明确支持动态配置；以后者为准，前者已过时。

## 使用方式

1. 在控制台「API 密钥管理」页为指定 AK 创建 Token Plan 配置（JSON 格式）  
2. 或通过 `/v1/token-plan` 接口以 POST 方式提交配置（需 `admin` 权限）  
3. 调用模型 API 时，在请求 Header 中携带 `x-token-plan-id: <plan_id>` 即可绑定生效  
4. 配置后立即生效，无需重启服务；变更后 3 秒内全网同步  

完整示例与字段校验规则见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 限制和注意事项

- 单个 AK 最多绑定 5 个 Token Plan（按环境区分：`prod`/`staging`/`dev`）  
- `token_quota` 为软限制：超限请求将返回 `429 Too Many Requests`，但不会中断正在进行中的长任务  
- 流式响应的 token 统计以实际返回的 `usage.total_tokens` 为准，非预估值  
- 若同时配置了 Token Plan 和项目级 Rate Limit，以更严格的策略生效  
- 请务必阅读 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中的典型故障排查清单，避免因 `model_whitelist` 配置疏漏导致 403 错误

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)



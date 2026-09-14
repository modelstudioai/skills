# model deployment 1

本页介绍百炼平台 Model Deployment 1（MD1）能力的核心部署模式与使用规范，适用于需在生产环境稳定调用模型的开发者。MD1 提供多种算力隔离与计费策略组合，支持从轻量级 API 快速上线到高 SLA 独占资源部署的全场景覆盖。具体能力边界与配置细节请严格以 [原文标题](../../raw/model-user-guide/model-deployment-1.md) 为准。

## 支持的模型/功能

- **专属部署**：为单个模型分配独立服务实例，保障资源独占与低延迟；适用于对稳定性、冷启时间敏感的业务。
- **PTU 预置吞吐部署**：基于预置 [Token](../concepts/token.md) 吞吐量（PTU）弹性伸缩，适合流量可预测、需兼顾成本与响应速度的场景。
- **独占算力部署（MU/DTU）**：提供毫秒级确定性延迟保障，支持 MU（Model Unit）或 DTU（Dedicated [Token](../concepts/token.md) Unit）两种算力计量单位，适用于金融、实时对话等严苛 SLA 场景。
- **[Token](../concepts/token.md) 按量部署**：按实际请求 Token 数计费，无预置成本，适合流量波动大、验证期或 PoC 阶段。
- **模型导入与路由集成**：支持将自定义模型导入后通过 [原文标题](../../raw/model-user-guide/model-deployment-1.md) 中定义的模型路由机制统一接入。

## 关键参数

- `deployment_type`：必填，取值为 `dedicated`（专属）、`ptu`、`dtu`、`mu` 或 `pay_as_you_go`（Token 按量）。
- `instance_type`：仅 `dedicated` 和 `dtu`/`mu` 模式下需指定，如 `ecs.gn7i-c16g1.2xlarge`；PTU 模式由系统自动匹配最优实例。
- `ptu_capacity`：PTU 模式下预置吞吐量（单位：TPS × avg_token），最小值 10，需在 [原文标题](../../raw/model-user-guide/model-deployment-1.md) 所列范围内配置。
- `max_concurrent_requests`：所有模式均支持限流，但 `pay_as_you_go` 模式默认不启用并发控制，需显式设置。

## 使用方式

1. 在「我的模型」页面选择已发布的模型 → 点击「部署」→ 选择部署类型；
2. 填写关键参数（如 `instance_type`、`ptu_capacity`），确认资源配额可用；
3. 完成部署后，获取唯一 `endpoint` 与 `api_key`，通过标准 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用；
4. 可通过模型路由规则将多个部署实例纳入同一逻辑服务名，实现灰度、AB 测试等高级调度——详见 [原文标题](../../raw/model-user-guide/model-deployment-1.md) 中「模型路由」章节。

> **注意**：文档中「PTU 预置吞吐部署」链接指向的官方帮助页（`/zh/model-studio/ptu-long-input-and-cache`）当前主要描述长文本缓存能力，未完整覆盖 PTU 的容量规划与扩缩容策略，实际配置应以 [原文标题](../../raw/model-user-guide/model-deployment-1.md) 的参数说明为准。

## 限制和注意事项

- `dedicated` 模式实例启动耗时约 3–5 分钟，首次调用前需等待就绪状态；
- `pay_as_you_go` 模式不支持自定义 `timeout` 超过 120 秒，且无法保证 P99 延迟；
- 所有部署类型均不支持运行时动态切换 `instance_type`，变更需重建部署；
- DTU/MU 模式下，若实际 Token 消耗持续超配额 15%，系统将自动限流并触发告警（非中断）。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1.md)



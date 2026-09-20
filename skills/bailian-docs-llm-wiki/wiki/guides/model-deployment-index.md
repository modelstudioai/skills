# model deployment index

模型部署是百炼平台为用户提供的核心能力，支持将大模型以不同资源模式和计费方式部署为可调用的 API 服务。本文档汇总了当前所有可用的部署类型、关键配置参数、调用方式及使用约束，适用于需要在生产环境集成模型能力的开发者。所有部署方案均需通过百炼控制台或 OpenAPI 完成，且依赖模型在 [模型导入](raw/model-user-guide/model-deployment-index/model-import.md) 中已完成注册与校验。

## 支持的模型与功能

- **专属部署**：为单个模型分配独立实例，适用于对延迟、隔离性有强要求的场景；支持自定义实例规格与弹性伸缩策略。  
- **PTU 预置吞吐部署**：基于预购 PTU（Processing Token Unit）保障稳定 QPS，适合流量可预期的中高负载业务；支持长上下文与 KV Cache 加速。详情见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。  
- **DTU 独占算力部署**：按 GPU 卡粒度独占物理资源（如 A10/A100），适用于需完全资源隔离、定制 CUDA 环境或运行私有微调模型的场景；对应文档为 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。  
- **Token 按量部署**：无预付费、按实际 token 数计费，适合低频、突发或测试类调用；不支持长上下文缓存与自定义系统提示词。  
- **智能路由**：在多个已部署模型间自动调度请求，依据延迟、成本、SLA 等策略实现负载均衡与故障转移；其配置入口位于 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md) 页面。

## 关键参数

| 参数 | 说明 | 是否必填 | 示例值 |
|------|------|----------|--------|
| `model_id` | 模型唯一标识，须已在 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md) 中完成注册 | 是 | `qwen2-7b-instruct` |
| `deployment_type` | 部署类型，取值：`exclusive` / `ptu` / `dtu` / `token` / `routing` | 是 | `ptu` |
| `ptu_count` | PTU 数量（仅 `ptu` 类型需填） | 否（`ptu` 类型必填） | `100` |
| `instance_type` | 实例规格（仅 `exclusive` / `dtu` 类型需填） | 否（对应类型必填） | `ecs.gn7i-c16g1.4xlarge` |
| `max_tokens` | 单次请求最大输出 token 数（全局默认 2048，部分模型上限更低） | 否 | `4096` |

> **注意**：`max_tokens` 在 DTU 部署下受实例显存限制更严格，实际可用值可能低于文档标称上限；建议通过 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md) 中的显存估算工具验证。

## 使用方式

1. **控制台操作**：进入「模型中心 → 我的模型」，选择目标模型后点击「部署」，按向导选择部署类型并填写参数；[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md) 页面提供已部署实例列表与状态监控。  
2. **OpenAPI 调用**：调用 `POST /v1/deployments` 接口，请求体需包含 `model_id` 和 `deployment_type` 等必需字段（详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)）。  
3. **调用已部署模型**：所有部署成功后的模型均通过统一 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）调用，需在 Header 中传入 `Authorization: Bearer <api_key>` 及 `X-DashScope-Deployment-Id: <deployment_id>`。

## 限制和注意事项

- 单个账号最多创建 50 个活跃部署实例（含所有类型），超出需提交工单申请扩容。  
- PTU 部署不支持跨地域共享，PTU 购买地域必须与部署地域一致；该限制在 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md) 中明确说明。  
- Token 按量部署暂不支持流式响应（`stream=true`），若需流式能力，请选用 PTU 或 DTU 类型。  
- 所有部署实例默认启用自动扩缩容（Exclusive/DTU 类型除外），但最小实例数不得低于 1；此行为与早期文档中“可设为 0”的描述存在差异，以当前控制台实际逻辑为准。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-index.md)



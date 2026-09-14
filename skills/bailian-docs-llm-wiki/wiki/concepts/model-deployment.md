# 模型部署

模型部署是将训练完成或已发布的模型（包括官方 SaaS 模型与用户微调模型）封装为可稳定、安全、高效调用的在线服务的过程。在百炼平台中，它不仅是推理能力的入口，更是连接模型能力与业务场景的核心枢纽，决定了服务的延迟、吞吐、成本、SLA 保障等级及运维可控性。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础服务上线**：开发者在「我的模型」页面选择已发布模型（如 `qwen-plus` 或微调后的 `ft-qwen-turbo-xxx`），点击「部署」，即可快速生成专属 `endpoint` 和 `api_key`，通过标准 [OpenAI 兼容接口](openai-compatibility.md)发起推理请求。
- **生产环境分级保障**：根据业务需求选择部署类型——轻量验证用 `pay_as_you_go`（[Token](token.md) 按量），流量可预测用 `ptu`（预置吞吐），严苛 SLA 场景用 `dtu`/`mu`（独占算力），或需资源隔离与低冷启时延用 `dedicated`（专属实例）。
- **高性能推理增强**：在部署基础上，通过请求体传入 `speed_mode="prime"` 或提前申请 `tpm_reservation`，启用高速推理能力，实现毫秒级 P99 延迟与确定性吞吐保障（仅限 SaaS 模型）。
- **资源优化与边缘适配**：对支持的 Qwen/Llama 系列基座模型，在部署时配置 `compression_config={"method": "awq", "bit": 4}`，自动启用 4-bit 量化，降低显存占用约 50%，适用于高并发或资源受限场景。
- **灰度与多版本协同**：结合模型路由功能，将多个部署实例（如 v1.0 专属部署 + v1.1 PTU 部署）绑定至同一逻辑服务名（如 `my-chat-service`），实现 AB 测试、金丝雀发布与平滑回滚。
- **自动化生命周期管理**：通过 `/v1/deployments` OpenAPI 接口完成创建、扩缩容（调整 `replicas`）、状态轮询与销毁，与 CI/CD 流水线深度集成。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 典型取值 |
|------|------|------|------|-----------|
| `deployment_type` | string | 是 | 部署模式，决定资源模型与计费方式 | `dedicated`, `ptu`, `dtu`, `mu`, `pay_as_you_go` |
| `instance_type` | string | 条件必填 | 实例规格，仅 `dedicated`/`dtu`/`mu` 模式需指定 | `ecs.gn7i-c16g1.2xlarge` |
| `ptu_capacity` | integer | 条件必填 | PTU 模式下预置吞吐量（TPS × avg_token） | `100`, `1000` |
| `tpm_capacity` | integer | 否 | TPM 预留容量（tokens/minute），用于 SLA 保障 | `500`, `5000` |
| `replicas` | integer | 否 | 初始副本数，支持水平扩缩容 | `1`, `2`, `3` |
| `max_concurrent_requests` | integer | 否 | 全局并发请求数限制（防雪崩） | `10`, `100` |
| `compression_config` | object | 否 | 模型压缩配置（部署时生效） | `{"method": "awq", "bit": 4}` |
| `timeout` | integer | 否 | 单次请求超时（秒） | `60`, `120`, `300` |

> ⚠️ 注意：  
> - `deployment_type` 一旦选定不可动态变更，需重建部署；  
> - `tpm_capacity` 和 `ptu_capacity` 语义不同：前者是分钟级吞吐保障（生产稳定性），后者是秒级 [Token](token.md) 处理能力（弹性响应）；  
> - `compression` 仅支持基座模型（非 LoRA 微调模型），且不兼容流式响应（`stream=True`）与异步任务（`X-DashScope-Async: enable`）。

## 面向开发者，简洁实用

- ✅ **起步最快**：控制台点选模型 → 选 `pay_as_you_go` → 30 秒获取 endpoint → 直接 curl 调用。  
- ✅ **稳态最优**：高流量业务优先选 `ptu`（平衡成本与延迟）或 `dtu`（金融/实时对话等毫秒级 SLA）。  
- ✅ **调试友好**：所有部署均返回标准 [OpenAI 兼容接口](openai-compatibility.md)，无需修改 SDK 代码；错误码统一（如 `429` 表示限流，`403` 表示 TPM 配额不足）。  
- ✅ **可观测性强**：部署后自动接入平台监控大盘，可观测 QPS、P99 延迟、[Token](token.md) 消耗、错误率等核心指标。  
- ✅ **安全合规**：默认启用 API Key 鉴权与 HTTPS 加密；企业客户可进一步配置子空间隔离（`X-DashScope-Workspace`）与 VPC 内网访问。  

部署不是终点，而是服务演进的起点——从单点可用，到多版本协同；从按量计费，到资源精算；从人工运维，到 API 驱动的全自动生命周期管理。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)
- [more about models](../api/more-about-models.md)



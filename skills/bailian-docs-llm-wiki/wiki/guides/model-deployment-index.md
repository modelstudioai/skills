# model deployment index

模型部署是百炼平台为用户提供的核心能力，支持多种算力分配与计费模式，适用于不同业务规模、延迟敏感度和成本要求的场景。本文档系统梳理了当前支持的部署方式、关键配置参数、调用方法及使用约束，便于开发者快速选型与集成。所有部署方案均通过统一 API 接口调用，且需配合 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) 完成初始化。

## 支持的模型与功能

- **专属部署**：为单个模型实例分配固定资源，保障性能隔离与低延迟，适用于高 SLA 要求的生产服务。  
- **PTU 预置吞吐**：基于预估 QPS 预购计算单元（PTU），支持长上下文与 KV Cache 复用，详见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。  
- **DTU 独占算力部署**：按 GPU 卡粒度独占物理资源，支持自定义镜像与 CUDA 版本，适合需要深度定制或兼容私有模型的场景。  
- **[Token](../concepts/token.md) 按量部署**：无预购、按实际 token 消耗计费，适合流量波动大或验证阶段的轻量应用；但不支持流式响应与长上下文缓存。  
- **模型路由**：在多个已部署模型间动态分发请求，支持基于负载、地域、模型能力等策略，参见 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。  
- **模型导入**：支持用户上传 Hugging Face 格式模型（含 tokenizer 和 config），经校验后可纳入部署流程，具体要求见 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

## 关键参数

| 参数 | 说明 | 是否必需 | 示例值 |
|------|------|----------|--------|
| `model_id` | 百炼平台内模型唯一标识（如 `qwen2-7b-chat`）或用户导入模型 ID | 是 | `qwen2-7b-chat`, `my-custom-model-123` |
| `deployment_type` | 部署类型，取值：`dedicated` / `ptu` / `dtu` / `token` / `routing` | 是 | `ptu` |
| `instance_count` | 实例数量（仅 `dedicated`/`dtu` 有效） | 否（默认 1） | `2` |
| `ptu_count` | PTU 数量（仅 `ptu` 有效，最小 10） | 是（当 `deployment_type=ptu`） | `50` |
| `dtu_spec` | DTU 规格（如 `NVIDIA_A10_24G`），需与 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md) 中列出的规格一致 | 是（当 `deployment_type=dtu`） | `NVIDIA_A10_24G` |

> **注意**：`deployment_type=token` 时，`instance_count` 和 `ptu_count` 均被忽略；若同时传入将导致参数校验失败。

## 使用方式

1. 通过控制台或 OpenAPI 创建部署任务（需先完成模型准备，参考 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)）；  
2. 获取部署成功后的 `endpoint` 和 `api_key`；  
3. 使用标准 `/v1/chat/completions` 或 `/v1/completions` 接口调用，`model` 字段填入部署时指定的 `model_id`；  
4. 所有部署均支持同步调用，仅 `dedicated` 和 `dtu` 类型支持流式响应（`stream=true`）。

## 限制和注意事项

- [Token](../concepts/token.md) 按量部署不支持 `max_tokens > 8192` 或 `temperature=0` 下的确定性采样（因底层调度机制限制）；  
- PTU 部署的缓存有效期为 30 分钟，超时后 KV Cache 自动失效，此行为与 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md) 文档一致；  
- 用户导入模型必须满足 PyTorch 2.0+、FlashAttention-2 兼容性要求，且 tokenizer 必须为 `transformers.AutoTokenizer` 可加载格式；  
- 同一 `model_id` 在同一地域下不可重复部署相同 `deployment_type`（例如不能有两个 `ptu` 类型的 `qwen2-7b-chat` 实例）；  
- “我的模型”中心展示所有已导入及部署的模型，可通过 [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md) 页面统一管理生命周期。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-index.md)



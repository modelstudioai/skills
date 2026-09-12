# 模型部署

模型部署是百炼平台将训练或微调完成的模型封装为可稳定、安全、按需调用的推理服务的核心能力。它通过统一 API 接口对外提供标准化的 OpenAI 兼容调用方式，屏蔽底层资源差异，使开发者聚焦于业务逻辑而非基础设施运维。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型上线交付**：完成微调（Fine-tuning）后，必须通过模型部署将生成的 `model_id`（如 `qwen2-7b-instruct-finetuned-20240806`）发布为可用服务，否则无法被 `ChatCompletion` 等接口调用；  
- **生产环境服务化**：模型部署是「模型生产（Model Production）」流程的前提——只有已部署的模型才能配置 TPM 预留、灰度发布和自动扩缩容；  
- **性能与成本精细化控制**：根据业务 SLA 要求选择部署类型：高确定性时延选 `dedicated` 或 `dtu`，可预测中高并发选 `ptu`，低频验证或 A/B 测试选 `token`；  
- **安全合规落地**：私网访问（VPC）、AI 安全护栏等安全能力均作用于部署后的服务实例，`deployment_id` 是策略绑定与审计追踪的关键标识；  
- **应用权限管控基础**：应用调用模型时，实际请求的是某个 `deployment_id` 对应的服务端点，RAM 权限策略中的 `Resource` 可精确到部署级（如 `.../deployment/{id}`），实现最小权限隔离。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 约束 |
|------|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，须已在「我的模型」中发布成功 | 不支持未发布的微调任务 ID 直接部署 |
| `deployment_type` | string | 是 | 部署模式：`dedicated` / `ptu` / `dtu` / `token` | 决定计费模型、资源隔离级别与功能限制 |
| `instance_type` | string | 否（仅 `dedicated`/`dtu`） | ECS 实例规格（如 `ecs.gn7i-c16g1.4xlarge`） | 必须在[独占算力规格列表](https://help.aliyun.com/zh/model-studio/dtu-model-deployment)中 |
| `ptu_count` | integer | 否（仅 `ptu`） | 预设吞吐单元数，1 PTU ≈ 100 tokens/sec 持续处理能力 | 最小值 1，受账户配额限制 |
| `max_tokens` / `temperature` 等 | - | 否 | 标准推理参数 | 与部署类型无关，所有类型均完全兼容 |

> ⚠️ 注意：  
> - `deployment_type=token` 时禁止设置 `instance_type` 或 `ptu_count`；  
> - 部署创建后，模型权重不可热更新——需删除旧部署并新建以生效新版本；  
> - 所有部署默认启用模型路由，无法绕过；`token` 类型不支持流式响应（`stream=true`），且 `max_tokens ≤ 8192`。

## 面向开发者，简洁实用

- ✅ **快速上手**：确保模型已发布 → 调用 `POST /v1/deployments` → 记录返回的 `deployment_id` → 后续请求改用 `?deployment_id=xxx` 替代 `model_id`；  
- ✅ **调试建议**：`ptu` 类型首次请求有 60–120 秒冷启动延迟，建议预热或添加指数退避重试；  
- ✅ **权限控制**：若需限制某团队仅能调用特定部署，可在 RAM 策略中限定 `Resource` 为具体 `deployment_id`；  
- ✅ **生产就绪检查**：高 SLA 场景务必选用 `dedicated` 或 `dtu`，并配合 `model production` 设置 `tpm_reserved` 和 `auto_scaling_enabled`；  
- ❌ **避免踩坑**：不要尝试对 `token` 部署开启流式；不要在 `deployment_type=token` 请求中传入 `instance_type` —— 将直接返回 400 错误。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)



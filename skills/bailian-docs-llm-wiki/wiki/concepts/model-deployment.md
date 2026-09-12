# 模型部署

模型部署是将训练或微调完成的模型（包括官方托管模型、自定义导入模型及微调产出模型）发布为可稳定调用的在线服务的关键环节。它封装了资源调度、API 网关、流量路由与运行时配置，使模型从“可用”走向“可生产”。

## 在百炼平台的不同场景中，这个概念如何使用

模型部署在百炼平台中并非单一操作，而是贯穿多个能力层级的横切枢纽：

- **基础服务化**：通过「模型部署」功能（`model deployment 1`），开发者可一键将模型发布为标准 RESTful API endpoint，支持专属、PTU、DTU、[Token](token.md) 四类部署模式，覆盖验证、灰度、高稳、弹性等全阶段需求。  
- **生产级保障**：在「模型生产」（`model production`）流程中，部署是前置依赖——必须先创建部署实例（获得 `deployment_id`），才能进一步申请 TPM 预留、启用自动扩缩容、配置 SLA 监控与版本回滚策略。  
- **性能优化载体**：「高速推理」（`high speed inference`）能力不独立存在，其 Prime 模式与 TPM 预留均需作用于已部署的模型实例；参数如 `speed_mode` 和 `tpm_reservation` 在调用时生效，但前提是目标模型已处于 `Running` 状态。  
- **轻量化落地入口**：经「模型压缩」生成的量化模型（如 `qwen2-7b-instruct-awq`），仍需通过标准模型部署流程发布为服务——压缩仅改变模型权重格式，不替代部署。  
- **定制化服务起点**：「模型调优」产出的微调模型（如 `ft-qwen2-7b-abc123`），必须完成部署后才具备对外提供推理服务的能力；未部署的微调模型仅存在于模型中心，不可直接调用。

简言之：**部署是模型从静态资产变为动态服务能力的临界点，所有上层能力（生产、加速、压缩、微调闭环）均以部署实例为运行载体。**

## 关键参数和配置

以下参数在调用部署 API 或控制台配置时最常使用，直接影响服务行为与成本：

| 参数 | 类型 | 必填 | 说明 | 典型取值示例 |
|------|------|------|------|--------------|
| `model_id` | string | 是 | 模型唯一标识，来自「我的模型」或导入/微调成功后的 ID | `qwen2-7b-instruct`, `ft-xyz987` |
| `deployment_type` | enum | 是 | 部署模式，决定资源隔离性、计费方式与弹性策略 | `dedicated`, `ptu`, `dtu`, `token` |
| `instance_count` | int | 否（默认 1） | 实例数量，仅 `dedicated` / `dtu` 模式有效；影响并发容量与故障域 | `1`, `2`, `4` |
| `ptu_capacity` | int | 仅 `ptu` 模式必需 | PTU 单位数（1 PTU ≈ 10 QPS@1k token），决定长上下文与缓存能力上限 | `10`, `50`, `200` |
| `speed_mode` | string | 否（默认 `"none"`） | 是否启用高速推理 Prime 模式 | `"prime"`, `"none"` |
| `tpm_reservation` | int | 否（TPM 模式必需） | 预留吞吐量（tokens/minute），用于保障低延迟 SLO | `1000`, `5000` |

> ⚠️ 注意：  
> - `deployment_type=mu` 已废弃，统一使用 `dtu`；  
> - [Token](token.md) 按量模式（`token`）不支持流式响应（`stream=true` 会被静默忽略）；  
> - 所有部署实例默认开启自动扩缩容（`dedicated` 模式除外），缩容冷却期为 5 分钟；  
> - 压缩模型、微调模型、导入模型均需先完成「校验 + 构建」步骤，方可进入部署流程。

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台「模型部署」页 → 选模型 → 选模式 → 填参数 → 点部署 → 复制 endpoint 调用。  
- ✅ **API 优先**：推荐使用 OpenAPI `/v1/deployments` 创建部署，返回 `deployment_id` 和 `endpoint`，后续所有生产管理（如扩缩容、监控、下线）均基于此 ID。  
- ✅ **参数组合建议**：  
  - 验证/测试：`deployment_type=token` + 默认参数；  
  - 高稳对话服务：`deployment_type=ptu` + `ptu_capacity=50` + `speed_mode="prime"`；  
  - 金融/政务强隔离场景：`deployment_type=dtu` + `instance_count=2`；  
  - 批量离线任务：`deployment_type=dedicated` + `instance_count=1` + 关闭自动扩缩容。  
- ✅ **调试提示**：若调用返回 `404 Not Found`，检查模型是否已部署且状态为 `Running`；若返回 `429 Too Many Requests`，确认是否超出 `tpm_reservation` 或 PTU 容量上限。  
- ✅ **清理习惯**：不再使用的部署请主动删除（`DELETE /v1/deployments/{deployment_id}`），避免持续计费。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model compression](../guides/model-compression.md)
- [fine tuning](../guides/fine-tuning.md)



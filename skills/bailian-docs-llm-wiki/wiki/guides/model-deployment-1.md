# model deployment 1

[模型部署](../concepts/model-deployment.md)（model deployment）是百炼平台提供的一组能力，用于将训练/微调后的模型以服务化方式对外提供推理接口。支持多种部署模式，适配不同性能、成本与隔离性需求的生产场景。所有部署均通过统一 API 调用，兼容 [OpenAI 兼容接口](../concepts/openai-compatibility.md)规范。

## 支持的模型/功能

- **专属部署**：为单个模型分配独立实例，保障资源独占与低延迟，适用于高 SLA 要求场景  
- **PTU 预置吞吐部署**：基于 PTU（Processing Throughput Unit）预设吞吐能力，自动弹性扩缩容，适合流量可预测的中高并发任务  
- **独占算力部署（MU/DTU）**：按计算单元（MU）或数据吞吐单元（DTU）计费，提供硬件级隔离，适用于敏感数据或强确定性时延要求场景  
- **[Token](../concepts/token.md) 按量部署**：按实际请求 token 数计费，无预置资源开销，适合低频、突发或测试验证类负载  
- 同时支持 [模型导入](https://help.aliyun.com/zh/model-studio/model-import) 和 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center) 中已发布的模型，详见 [模型部署](../../raw/model-user-guide/model-deployment-1.md) 文档。

## 关键参数

- `model_id`：必填，模型唯一标识（如 `qwen-max-20240806`），需已在 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center) 中发布  
- `deployment_type`：必填，取值为 `dedicated` / `ptu` / `dtu` / `token`，对应四种部署类型  
- `instance_type`（仅 `dedicated`/`dtu` 需指定）：如 `ecs.gn7i-c16g1.4xlarge`，须在 [独占算力部署（MU/DTU）](https://help.aliyun.com/zh/model-studio/dtu-model-deployment) 所列规格范围内  
- `ptu_count`（仅 `ptu` 类型需指定）：整数，最小值为 1，最大值受账户配额限制  
- `max_tokens`、`temperature` 等推理参数与标准 API 一致，不因部署类型而异  

> **注意**：`deployment_type=token` 时不可设置 `instance_type` 或 `ptu_count`；若在 [API 部署指南](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start) 示例中发现此类错误配置，请以本页为准。

## 使用方式

1. 确保目标模型已在 [模型导入](https://help.aliyun.com/zh/model-studio/model-import) 流程完成并发布至 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center)  
2. 调用 `POST /v1/deployments` 接口，传入上述关键参数（参考 [API 部署指南](../../raw/model-user-guide/model-deployment-1.md) 中的 cURL 示例）  
3. 部署成功后返回 `deployment_id`，后续推理请求使用该 ID 替代 `model_id`，路径为 `/v1/chat/completions?deployment_id=xxx`  
4. 可通过 `/v1/deployments/{id}` 查询状态，或在控制台「[模型部署](../concepts/model-deployment.md)」页管理生命周期  

## 限制和注意事项

- 单账户默认最多创建 5 个 `dedicated` 类型部署，如需提升请提交工单  
- `ptu` 类型部署冷启动时间约 60–120 秒，首次请求可能超时，建议预热或配置重试逻辑  
- `token` 类型不支持流式响应（`stream=true`），且最大 `max_tokens` 限制为 8192  
- 所有部署均强制启用 [模型路由](https://help.aliyun.com/zh/model-studio/model-routing) 的基础路由策略，无法绕过  
- 部署后模型权重不可变更；如需更新，须删除旧部署并新建——此行为与 [模型部署](../../raw/model-user-guide/model-deployment-1.md) 描述一致，但与早期文档中“热更新”表述存在冲突，请以本页为准。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1.md)



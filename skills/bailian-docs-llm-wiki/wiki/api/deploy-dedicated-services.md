# deploy dedicated services

专属服务部署（Dedicated Services Deployment）为开发者提供基于阿里云百炼平台的独立资源模型托管方案。通过该功能，您可以将平台预置模型或自定义微调模型部署至专属计算实例，实现独享算力、固定限流配置与精细化计费。完整生命周期涵盖模型资源导入、任务创建、动态运维与状态监控。

## 支持的模型与计费模式
专属服务支持部署平台预置的[[大语言模型]]（如 Qwen、GLM、DeepSeek 系列）、[[多模态模型]]，以及通过[[模型导入]]流程接入的自定义微调模型（Full/LoRA）。部署时可根据业务场景选择以下计费与资源分配模式：
- **PTU 计费** (`plan: "ptu"`)：按预置吞吐分配资源，需明确指定 `input_tpm` 与 `output_tpm`，适用于高并发、吞吐稳定的生产环境。
- **模型单元计费** (`plan: "mu"`)：按模型单元使用时长收费，支持细粒度配置实例规格、推理模式、上下文长度及限流阈值。详细规格列表与定价见 [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)。
- **Token 用量计费** (`plan: "lora"`)：适用于轻量级微调模型，按实际消耗 Token 结算。
- **算力单元计费** (`plan: "cu"`)：专用于图片生成与视频生成类模型，按算力使用时长收费。

> **注意**：`plan: "mu"` 模式下部分模型支持 **PD 分离模式**，该模式将 Prefill 与 Decode 阶段拆分至不同计算节点，可显著降低首 Token 延迟并提升吞吐。但并非所有模型均支持此特性，部署前需以控制台或 API 响应结果为准。

## 关键参数
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model_name` | String | 是 | 待部署的模型标识。自定义模型需使用导入成功后返回的系统生成 ID。 |
| `plan` | String | 否 | 计费模式枚举值：`ptu`、`mu`、`lora`、`cu`。不传时默认按基础算力时长计费。 |
| `capacity` | Number | 是 | 实际分配的资源单元数量。**必须**为模型 `base_capacity` 的整数倍。 |
| `deploy_spec` | String | 条件必填 | 仅 `plan: "mu"` 时必填，指定实例规格（如 `MU1`、`MU8`）。 |
| `ptu_capacity` | Object | 条件必填 | 仅 `plan: "ptu"` 时必填，需包含 `input_tpm` 和 `output_tpm`。 |
| `enable_thinking` | Boolean | 否 | 控制是否开启深度思考推理模式（仅部分文本/多模态模型支持）。 |
| `suffix` | String | 否 | 部署名称后缀，最长 8 字符且全局唯一。同一模型多次部署时必须指定。 |

## 核心使用方式
1. **前置准备**：调用任何专属服务 API 前，需完成[[api-key配置]]并在 HTTP Header 中统一携带 `Authorization: Bearer ${API-KEY}` 与 `Content-Type: application/json`。
2. **导入自定义模型（可选）**：若部署自有微调权重，需通过 `POST /custom_models/import` 提交已授权[[对象存储OSS]]中的文件。通过 `job_id` 轮询任务状态至 `SUCCESSED` 后，方可将其作为 `model_name` 传入部署接口。完整流程规范参见 [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)。
3. **查询与创建部署**：调用 `GET /deployments/models` 获取当前支持的模型清单及最小 `base_capacity`。确认资源后，向 `POST /deployments` 提交 JSON 负载创建任务。任务状态流转至 `RUNNING` 后，返回的 `deployed_model` 即为后续业务调用的专属 Endpoint 标识。
4. **动态运维**：服务运行期间，可通过 `PUT /deployments/{deployed_model}/update` 动态调整限流配置。支持按需执行停止、扩缩容（部分模式）与删除操作。

## 限制与注意事项
- **计费起始规则**：专属服务属于独占型物理/逻辑资源池，部署任务创建成功后即开始计费。无论业务是否发起实际推理请求，资源占用期间均持续扣费，请严格评估资源利用率。
> **注意**：在 `plan: "lora"`（Token 用量）计费模式下，API 请求体中**必须**传入 `capacity` 字段，但该参数实际**不生效**。若需对该模式服务进行扩缩容，API 暂不支持动态调整，必须前往百炼控制台填写工单表单申请。此行为与其他计费模式不同，开发集成时需做好参数兼容处理。
- **状态机约束**：导入或部署任务处于 `PENDING` 或 `RUNNING` 状态时，禁止执行删除请求，否则将触发 `OperationDenied` 异常。扩容操作受限于底层硬件资源水位，可能出现短暂排队。
- **限流与参数兼容性**：`rpm_limit`、`tpm_limit`、`max_context_length` 等高级参数仅对 `plan: "mu"` 下的特定基座模型开放。跨版本部署时务必核对兼容性矩阵，避免因参数越界导致任务 `FAILED`。
- **标识管理**：系统自动生成的 `model_name`（导入场景）与 `deployed_model`（部署场景）具有强版本关联性。多次部署同一基座模型时，务必通过 `suffix` 参数隔离实例，防止调用路由冲突。

## 来源文档

- [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)
- [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)


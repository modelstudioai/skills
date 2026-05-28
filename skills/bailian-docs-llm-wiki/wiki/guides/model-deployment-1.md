# model deployment 1

阿里云百炼平台支持将基础模型及[[模型调优]]后的自定义模型部署为独立、资源专享的推理服务，满足高并发、低延迟及私有化计算需求。平台提供预置吞吐（PTU）、模型单元（MU）及 Token 按量等多种部署方案，开发者可通过控制台、HTTP API 或 SDK 完成服务的创建、监控与调用。

## 支持的模型与计费模式
平台支持千问系列、DeepSeek、GLM 及多模态（VL/Omni）等预置模型的独立部署，同时支持导入[[OSS 存储]]中的自定义 LoRA 权重进行专属服务化。不同模型支持的计费与性能模式如下：

- **PTU（预置吞吐）**：保障固定输入/输出 TPM，适合流量稳定的高负载生产环境。超出阈值后自动切换至公共按量服务。
- **MU（模型单元）**：按算力单元数量与时长计费，资源独占。支持自定义 RPM/TPM 限流、最长上下文长度、推理模式（Instruct/Thinking）及 PD 分离架构以降低首字延迟。
- **Token 按量（Lora 专属）**：仅适用于完成 SFT 高效微调的模型，按实际调用 Token 量计费，连续 30 天无调用将自动释放实例。
- **CU（计算单元）**：适用于图像/视频生成类模型，按独占实例时长计费。

> 详细定价表与规格说明请参考 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 关键配置参数
部署与调用时需关注以下核心参数：

| 参数 | 说明 | 适用场景 |
|---|---|---|
| `model_name` | 待部署模型的 Code 或自定义模型 ID | 所有部署计划 |
| `plan` | 计费模式：`ptu` \| `mu` \| `lora` \| `cu` | 所有部署请求 |
| `ptu_capacity` | `{input_tpm: int, output_tpm: int}` | PTU 模式 |
| `deploy_spec` / `capacity` | MU 规格标识与实例数量 / Lora 容量占位符 | MU / Lora 模式 |
| `enable_thinking` | `true`/`false`，控制是否启用深度思考推理 | MU / 调用请求 |
| `max_context_length` | 限制单次对话最大上下文 Token 数 | 部分 MU 模式 |
| `model` | 调用时使用的专属服务 ID（即 `deployed_model`） | 推理调用 |

**推理参数对齐建议**：为确保平台输出与本地 vLLM 环境一致，建议在调用时显式设置：`temperature=1.0`, `top_p=1.0`, `top_k=99`, `presence_penalty=0`, `repetition_penalty=1.0`（DashScope 协议）。

## 使用方式
完整工作流包含导入、部署、调用与清理，具体步骤如下：

1. **导入自定义权重**：将包含 `adapter_model.safetensors` 与 `adapter_config.json` 的 LoRA 目录上传至子目录，完成标签授权后在控制台执行导入。流程详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
2. **发起部署**：通过控制台可视化表单或 HTTP API (`POST /api/v1/deployments`) 提交任务。部署成功后即开始计费，无论是否产生调用。
3. **状态轮询**：调用 `GET /api/v1/deployments/{deploy_id}` 检查 `status`，当返回 `RUNNING` 时表示服务可用。
4. **推理调用**：使用 DashScope SDK 或 [[openai-compatible-api|OpenAI 兼容接口]]发起请求。`model` 参数必须填入部署返回的专属服务 ID。示例代码见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
5. **服务下线**：调用 `DELETE` 接口立即终止实例并停止计费，该操作不可逆。

## 限制与注意事项
- **权限隔离**：API Key 所属的[[业务空间]]必须显式开启目标模型的部署权限。子账号需主账号授予服务关联角色创建权限后方可执行首次授权。
- **参数无效声明**：`lora` 计划部署请求中 `capacity` 参数为必填但实际无效。如需动态扩缩容，需在控制台提交工单申请，API 直接修改不生效。
- **文件强校验**：LoRA 导入严格校验 `rank` 值（仅限 8/16/32/64 且全层一致）。禁止训练过程中修改基础模型的 `vocab` 与 `chat_template`。视觉语言模型（VL）的 Adapter 中严禁包含 `visual` 开头的权重，否则导入失败。
- **计费策略锁定**：部署创建后计费模式不可变更。如需切换计费方案，必须下线现有部署并重新创建。

> **注意**：PTU 模式下若单位时间内调用量超出购买的 TPM 配额，系统会自动将超额请求降级至公共[[模型调用]]通道。此时推理性能可能波动，限流受全局策略管控，且响应 Header 中将携带 `x-dashscope-ptu-overflow: true`。建议结合[[模型监控]]面板观察实际吞吐水位，必要时提前扩容。

## 来源文档

- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)


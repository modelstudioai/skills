# 模型部署

模型部署是百炼平台将预置模型、微调模型或导入模型发布为在线推理服务的过程，是连接"模型资产"与"在线推理"的桥梁。部署完成后，应用即可通过推理接口调用该模型。

## 计费方式

百炼提供三种部署计费模式，创建后不可更改：

| 计费方式 | 适用场景 | 核心特点 |
|---------|---------|---------|
| 预置吞吐（PTU） | 流量稳定的生产环境 | 平台预置吞吐，TPS 提升约 1.5~2 倍；支持后付费（按小时）和预付费（按天） |
| 模型单元（MU） | 大规模推理，需自定义性能 | 延迟/吞吐可调，支持 PD 分离；支持后付费（按小时）和预付费（包月） |
| Token 用量 | 调优后模型效果验证 | 价格最优，不使用不计费；仅限 LoRA 调优后模型 |

**PTU 费用** = 使用时长 x (输入 TPM 单价 x 输入 TPM + 输出 TPM 单价 x 输出 TPM)。超出购买量时自动切换为按量付费（API Header 含 `x-dashscope-ptu-overflow:true`）。

**模型单元费用** = 使用时长（小时）x 模型单元数量 x 模型单元单价。支持 PD 分离（Prefill 和 Decode 拆到不同节点），可降低首 Token 延迟、提高吞吐。

**Token 用量费用** = 输入 Token 数 x 输入单价 + 输出 Token 数 x 输出单价。一个月内不使用将自动释放。

## 支持的模型

- **PTU 支持**：千问系列（qwen3.7-max、qwen3.6-flash/plus、qwen-flash、qwen-plus 等）、DeepSeek 系列（deepseek-v4-pro、deepseek-v3 等）、千问 VL、GLM-5.1
- **模型单元支持**：文本生成、多模态、语音合成等类型，包括千问全系列（1.7B 到 397B）、DeepSeek、GLM、MiniMax、Kimi 等；规格从 MU1 到 MU9
- **Token 用量**：部分 LoRA 调优后模型

## 部署方式

### 控制台部署

1. 前往模型部署控制台（仅限华北二/北京地域）
2. 填写服务名称，选择模型和计费方式
3. 等待部署状态变为"运行中"

模型单元模式下可额外配置推理模式（Instruct/Thinking）、最长上下文、服务限流（RPM/TPM）、部署副本数和部署模板。

### API 部署

通过 `POST https://dashscope.aliyuncs.com/api/v1/deployments` 创建部署，请求头需包含 `Authorization: Bearer $DASHSCOPE_API_KEY`。

关键参数：

| 参数 | 说明 |
|------|------|
| `name` | 服务名称 |
| `model_name` | 模型名称（预置模型版本号或调优产出模型 ID） |
| `plan` | 计费模式：`ptu` / `mu` / `lora` |
| `ptu_capacity` | PTU 模式下的输入/输出 TPM 配置 |
| `deploy_spec` | 模型单元规格（如 MU1） |
| `capacity` | 模型单元数量或 LoRA 副本数 |
| `enable_thinking` | 是否启用思考模式（MU 模式） |
| `max_context_length` | 最长上下文长度（MU 模式） |
| `rpm_limit` / `tpm_limit` | 服务限流配置（MU 模式） |

## 与其他功能的关系

- **模型调优**：通过 SFT、DPO 等方式微调的模型，需先部署才能在线调用。LoRA 调优后的模型可选择 Token 用量模式快速验证效果。
- **模型压缩**：全精度微调模型经量化压缩后可降低部署单元规格（如从 MU1x2 降至 MU8x1），从而降低部署成本。压缩产出的模型可直接用于部署。
- **模型监控**：部署后的模型支持实时监控调用量、Token 消耗、首 Token 延时、失败率等指标，并可配置告警规则。
- **模型导入**：支持从 OSS 导入本地训练的 LoRA 模型进行部署。

## 注意事项

- 模型部署功能目前仅适用于**华北二（北京）**地域
- 计费方式在服务创建后**无法更改**，如需切换必须下线后重新部署
- Token 用量模式的模型一个月内不使用将**自动释放**
- PTU 预付费订单到期后延后 2 小时停止服务
- MU 后付费算力资源先买到先得，购买不成功全额退款

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [deployments api](../api/deployments-api.md)
- [model compression](../guides/model-compression.md)
- [release notes](../guides/release-notes.md)
- [fine tuning](../guides/fine-tuning.md)
- [model monitoring](../guides/model-monitoring.md)



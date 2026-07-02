# model deployment 1

百炼平台提供模型部署能力，支持将预置模型或调优后模型部署为独享推理服务，满足高并发、低延迟等生产级业务需求。平台提供三种[计费](../concepts/billing.md)方式（预置吞吐 PTU、模型单元、[Token](../concepts/token.md) 用量），并支持通过控制台或 API 两种方式完成部署操作。

## [计费](../concepts/billing.md)方式概览

平台提供三种[计费](../concepts/billing.md)方式，创建后不可更改，需下线重建才能切换：

| [计费](../concepts/billing.md)方式 | 适用场景 | 核心优势 |
|---------|---------|---------|
| 预置吞吐（PTU） | 流量稳定的高负载生产环境 | 保障 TPM 吞吐，TPS 提升约 1.5~2.0 倍 |
| 模型单元 | 需自定义性能指标、资源隔离的场景 | 性能可调，支持 PD 分离模式 |
| [Token](../concepts/token.md) 用量 | 调优后模型效果验证 | 不使用不[计费](../concepts/billing.md) |

详细[计费](../concepts/billing.md)规则和支持模型列表参见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 预置吞吐（PTU）部署

### 基本概念

PTU 通过平台预留资源，保障特定 TPM 吞吐能力。在保障额度内不限速，超出额度时自动切换为按量付费（响应头包含 `x-dashscope-ptu-overflow:true`）。

### 长输入与前缀缓存

PTU 部署支持长输入请求和前缀缓存，关键规则如下：

- **长输入阶梯系数**：部分模型（如 glm-5.1）超过 32K token 的输入部分按更高系数折算 TPM 消耗
- **前缀缓存折扣**：命中缓存的输入 token 按折扣系数消耗额度（如 glm-5.1 为 0.2，deepseek-v4-pro 为 0.08）
- **自动溢出**：超出 PTU 额度或超过模型输入上限时，请求自动转为按量计费

通过 API 响应中的 `service_tier` 字段判断计费方式（`ptu-standard` 为 PTU，`default` 为按量），`cached_tokens` 字段确认缓存是否命中。详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

### 容量计算器

在控制台创建部署或扩容时，展开容量计算器，填入 RPM、平均输入/输出长度、预估缓存命中率，即可获得推荐的 TPM 配额。

## 模型单元部署

模型单元按使用时长和单元数量计费，支持后付费（按小时）和预付费（包月）。核心配置项：

- **模型单元类型**：MU1~MU9 不同规格对应不同算力
- **部署副本数**：影响并发处理能力
- **推理模式**：Instruct（非思考）或 Thinking（思考模式）
- **PD 分离模式**：将 Prefill 和 Decode 拆分到不同节点，降低首 [Token](../concepts/token.md) 延迟

> **注意**：模型单元后付费方式的算力资源先买到先得，购买不成功会全额退款。预付费首月内提前退订，日单价按 1.2 倍计费。

## 模型导入

支持将本地训练的 LoRA 模型从 OSS 导入百炼平台，导入后可部署为推理服务。关键限制：

- 仅支持 LoRA 模型（不支持全参微调）
- rank 值必须为 8/16/32/64 之一
- 不可修改词汇表或 chat_template
- VL 模型必须冻结 VIT 部分

支持的基础模型包括千问3（32B/14B/8B/4B）、千问3-VL-8B、千问2.5（72B/32B/14B/7B）、千问2.5-VL（72B/7B）等。详细导入步骤和 OSS 授权配置参见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 通过 API 部署模型

### 创建部署

使用 DashScope API 创建部署，核心端点为 `POST https://dashscope.aliyuncs.com/api/v1/deployments`。不同计费方式的请求参数：

**PTU 模式**：
```json
{
  "name": "my_qwen_flash",
  "model_name": "qwen-flash-2025-07-28",
  "plan": "ptu",
  "ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }
}
```

**模型单元模式**：
```json
{
  "name": "my_qwen_plus",
  "model_name": "qwen-plus-2025-12-01",
  "plan": "mu",
  "deploy_spec": "MU1",
  "enable_thinking": true,
  "capacity": 4
}
```

**[Token](../concepts/token.md) 用量模式**（仅限调优后模型）：
```json
{
  "model_name": "qwen3-8b-ft-xxx",
  "plan": "lora",
  "capacity": 1,
  "name": "qwen3-8b-ft"
}
```

### 查询与删除

- 查询状态：`GET /api/v1/deployments/{deployed_model}`，状态为 `RUNNING` 表示部署完成
- 删除服务：`DELETE /api/v1/deployments/{deployed_model}`，删除后立即停止计费且不可恢复

完整 API 使用流程参见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 注意事项

- 部署成功后即开始计费，即使尚未调用模型
- 后付费欠费后资源保留 24 小时，超时底层资源被删除（任务保留，补费后可恢复）
- [Token](../concepts/token.md) 用量模式一个月内不使用将自动释放
- 模型导入后推理效果可能与本地 vLLM/SGLang 不一致，需调整 temperature、top_p 等参数对齐
- [API Key](../concepts/api-key.md) 的归属[业务空间](../concepts/workspace.md)需拥有目标模型的部署权限

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)




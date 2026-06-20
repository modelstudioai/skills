# model deployment 1

百炼平台提供模型部署功能，支持将预置模型或调优后的模型部署为独立的、资源专享的推理服务，以满足高并发、低延迟等不同性能需求。平台提供三种计费方式（预置吞吐 PTU、模型单元、Token 用量），并支持通过控制台或 API 进行部署操作。本文汇总了模型部署的核心概念、计费规则、PTU 长输入与缓存机制、模型导入流程，以及 API 部署方式。

## 计费方式概览

百炼平台提供三种模型部署计费方式，适用于不同业务场景。详细的计费说明请参考[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

| 计费方式 | 适用场景 | 计费公式 | 特点 |
| --- | --- | --- | --- |
| **预置吞吐（PTU）** | 高负载生产环境，流量可预估 | 使用时长 x (输入 TPM 单价 x 输入 TPM + 输出 TPM 单价 x 输出 TPM) | 保障额度内不限速，TPS 提升约 1.5~2.0 倍 |
| **模型单元** | 模型调优后的大规模推理，需自定义性能指标 | 使用时长(小时) x 模型单元数量 x 模型单元单价 | 资源独占，支持 PD 分离计算模式 |
| **Token 用量** | 调优后模型效果验证，对并发延迟要求不高 | 输入 Token 数 x 输入单价 + 输出 Token 数 x 输出单价 | 不使用不计费，仅支持部分 LoRA 调优后模型 |

> **注意**：计费方式在服务创建后无法更改，如需切换必须先下线再重新部署。本文档中的模型部署功能仅适用于"华北二（北京）"地域。

## 支持的模型

### PTU 支持的模型（部分）

| 模型系列 | 代表模型 | 最长输入 Token |
| --- | --- | --- |
| 千问 | qwen3.7-max-2026-05-20、qwen3.7-plus-2026-05-26、qwen-plus-2025-12-01 等 | 128K~256K |
| DeepSeek | deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2、deepseek-v3 | 64K~256K |
| 千问 VL | qwen3-vl-plus-2025-09-23 | 128K |
| GLM | glm-5.1 | 64K |

### 模型单元支持的模型

模型单元计费支持更广泛的模型选择，包括千问全系列（文本、VL、Omni）、DeepSeek、GLM、MiniMax、Kimi 等。部分模型支持 PD 分离模式以降低首 Token 延迟、提高吞吐。

### 模型导入

平台支持将本地训练的 LoRA 模型从 OSS 导入到百炼平台进行部署。当前支持千问3（32B/14B/8B/4B）、千问3-VL-8B、千问2.5 系列等基础模型的 LoRA 微调版本。导入要求和详细步骤请参考[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

**导入关键限制**：
- 仅支持 LoRA 模型，不支持全参微调模型
- 必需文件：`adapter_model.safetensors` 和 `adapter_config.json`
- rank 值必须为 8、16、32 或 64
- 不支持修改过词汇表或 chat_template 的模型
- VL 模型必须冻结 VIT 部分

## PTU 长输入与前缀缓存

PTU 部署支持长输入请求（部分模型最高 256K token）和前缀缓存，通过阶梯容量系数和缓存折扣灵活管理额度消耗。详细的额度消耗规则请参考[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

### 核心能力

- **长输入支持**：超过 32K token 的输入按更高的阶梯系数折算 TPM 消耗
- **前缀缓存优惠**：命中缓存的输入 token 按折扣系数消耗额度（如 glm-5.1 为 20%，deepseek-v4-pro 为 8%）
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限时，请求自动转为按量计费

### 支持长输入和缓存的模型

| 模型 | 输入长度上限 | 缓存折扣 | 长输入阶梯系数 |
| --- | --- | --- | --- |
| glm-5.1 | 200K | 0.2 | [0, 32K): 1.0; [32K, 200K]: 输入 1.33 / 输出 1.17 |
| deepseek-v4-pro | 256K | 0.08 | 无阶梯 (1.0) |
| qwen3.7-plus-2026-05-26 | 256K | 0.2 | 无阶梯 (1.0) |

### 计算示例（glm-5.1）

```
短输入（10K token，无缓存）：
  输入消耗 = 10K x 1.0 = 10K TPM

长输入（50K token，无缓存）：
  输入消耗 = 32K x 1.0 + 18K x 1.33 = 55.94K TPM

长输入 + 缓存命中（50K token，前 30K 命中缓存）：
  缓存部分 = 30K x 1.0 x 0.2 = 6K TPM
  非缓存部分 = 2K x 1.0 + 18K x 1.33 = 25.94K TPM
  合计 = 31.94K TPM（比无缓存节省 43%）
```

### API 响应中的额度字段

| 字段 | 说明 |
| --- | --- |
| `service_tier` | 值为 `ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费 |
| `provisioned_tokens` | 折算后实际消耗的 PTU 额度 token 数（已含阶梯系数和缓存折扣） |
| `cached_tokens` | 前缀缓存命中的 token 数 |

不同 API 格式（OpenAI Chat、OpenAI Responses、Anthropic、DashScope）中字段的 JSON 路径略有差异，具体请参考原始文档。

## 部署方式

### 控制台部署

1. 前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)
2. 填写服务名称，选择模型和计费方式
3. 等待部署状态变为"运行中"

### API 部署

通过 HTTP API 可完成模型的部署、状态查询、推理调用和删除。详细的 API 用法请参考[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

**PTU 模式部署示例**：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {
        "input_tpm": 10000,
        "output_tpm": 1000
    }
}'
```

**模型单元模式部署示例**：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "deploy_spec": "MU1",
    "enable_thinking": true,
    "capacity": 4
}'
```

**Token 用量模式部署示例**：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora",
    "capacity": 1,
    "name": "qwen3-8b-ft"
}'
```

部署成功后，返回结果中的 `deployed_model` 即为专属服务的唯一 ID，可用于后续查询和调用。服务状态为 `RUNNING` 时部署完成。

## 模型单元部署配置

模型单元计费模式下，支持以下额外配置：

| 配置项 | 说明 |
| --- | --- |
| 模型单元类型 | 选择部署规格（如 MU1、MU2 等），对应不同算力和性能 |
| 部署副本数 | 初始副本数量，影响并发处理能力 |
| 推理模式 | Instruct（非思考模式）或 Thinking（思考模式） |
| 最长上下文 | 基于模型类型设置上下文长度 |
| 服务限流 | 可限制 RPM、TPM |
| PD 分离模式 | 将 Prefill 和 Decode 拆到不同节点，降低首 Token 延迟 |

## 监控与运维

部署成功后，可通过百炼平台的模型监控功能查看：

- **PTU 利用率**：输入/输出/思考模式输出三条独立曲线
- **Token 用量与缓存命中**：含 `cached_tokens` 数据系列
- **配额内/外调用次数**：了解超出 PTU 额度后转为按量计费的请求占比

## 常见问题

**超出 PTU 额度时会怎样？**
请求自动转为按量计费，API 响应头包含 `x-dashscope-ptu-overflow:true`，业务不会中断。

**如何确认缓存是否生效？**
检查 API 响应中 `cached_tokens` 字段，值大于 0 表示前缀缓存命中。

**部署时提示权限不足怎么办？**
确保 API Key 的归属业务空间拥有模型部署权限，且归属账号在该业务空间中有操作权限。前往业务空间管理页面检查模型部署列的授权状态。

**导入的模型与本地 vLLM 推理效果不一致？**
百炼平台推理引擎参数可能与本地默认值不同，建议在 API 调用时显式设置 `temperature=1.0`、`top_p=1.0`、`repetition_penalty=1.0` 等参数以对齐 vLLM 默认值。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)



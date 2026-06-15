# model deployment 1

百炼平台提供[模型部署](../concepts/model-deployment.md)功能，支持将预置模型或调优后的[模型部署](../concepts/model-deployment.md)为独立的、资源专享的推理服务。通过部署，开发者可以获得高并发、低延迟等不同性能等级的推理能力，满足生产环境的业务需求。本功能目前仅适用于华北二（北京）地域。

## 计费方式概览

百炼[模型部署](../concepts/model-deployment.md)提供三种计费方式，适用于不同业务场景（详见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)）：

### 预置吞吐（PTU）

通过平台预留资源，保障特定 TPM 吞吐能力。吞吐/并发和生成速度由平台预置，用户不可调。

- **优势**：为高负载生产环境提供稳定吞吐容量，TPS 相比按 Token 计费提升约 1.5~2.0 倍，支持自动续费
- **计费公式**：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`
- **支持模型**：部分预置模型（千问系列、DeepSeek、千问VL、GLM 等）
- **适用场景**：流量稳定的智能客服、实时内容审核、公有云翻译 API 等

> **注意**：当模型输入超过最长输入 Token 或超出购买的 TPM 量时，调用将自动切换为按量付费模式，推理性能可能下降。此时 API 返回 Header 包含 `x-dashscope-ptu-overflow:true`。

### 模型单元（MU）

按使用时长与模型单元数量配置算力，资源独占。

- **优势**：延迟/吞吐等性能指标可自定义，支持 PD 分离计算模式（降低首 Token 延迟、提高吞吐），支持自动续费
- **计费公式**：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`
- **支持模型**：部分预置模型与所有调优后模型
- **适用场景**：电商专属微调大模型、医药分子筛选、自动驾驶仿真等需要独占资源的场景

> **注意**：模型单元后付费方式的算力资源先买到先得，购买不成功会全额退款。预付费首月内提前退订，日单价将按 1.2 倍计费。

### 按 Token 用量

按每次调用产生的输入/输出 Token 计量。

- **优势**：不使用不计费，价格优势最高
- **计费公式**：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`
- **支持模型**：部分经过 LoRA 调优后的模型
- **限制**：一个月内不使用将自动释放；吞吐/并发和生成速度由平台预置，用户不可调

> **注意**：计费方式在服务创建后无法更改。如需切换，必须下线已部署的模型后重新部署。

## 部署方法

### 控制台部署

前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型和计费方式即可（详见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)）。

### API/命令行部署

通过 HTTP API 实现自动化部署，完整流程参见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。核心步骤如下：

**1. 创建部署服务**

以 PTU 方式部署为例：

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

`plan` 参数取值：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（按 Token 用量）。模型单元模式还支持 `deploy_spec`、`enable_thinking`、`capacity`、`max_context_length`、`rpm_limit`、`tpm_limit` 等配置项。

**2. 查询服务状态**

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/<deployed_model>" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

当返回 `status` 为 `RUNNING` 时，服务部署完成。

**3. 执行推理请求**

使用 DashScope SDK 调用：

```python
from dashscope import Generation
response = Generation.call(
    model='qwen3-8b',
    prompt='你是谁？',
    enable_thinking=False,
    api_key=os.getenv('DASHSCOPE_API_KEY'),
)
```

**4. 删除服务**

```bash
curl --request DELETE 'https://dashscope.aliyuncs.com/api/v1/deployments/<deployed_model>' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

> **注意**：删除操作不可恢复，服务将立即开始下线并停止计费。

## 模型导入

开发者可以将本地训练的 LoRA 模型从 OSS 导入到百炼平台进行部署（详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)）。

### 支持的基础模型

- 千问3 系列：千问3-32B、千问3-14B、千问3-8B、千问3-4B-Instruct-2507
- 千问3-VL 系列：千问3-VL-8B-Instruct
- 千问2.5 系列：72B/32B/14B/7B-Instruct
- 千问2.5-VL 系列：72B/7B-Instruct

### 导入要求

- 仅支持 LoRA 模型，不支持全参微调模型
- 必需文件：`adapter_model.safetensors` 和 `adapter_config.json`
- rank 值限制为 8、16、32 或 64
- 不支持修改词汇表或 chat_template 的模型
- VL 模型必须冻结 VIT 部分

### 前置准备

1. 创建 OSS Bucket 并添加 `bailian-datahub-access` 标签（值为 `read`）
2. 完成 OSS 服务关联角色授权
3. 模型文件放在 Bucket 子目录下（不支持根目录）

> **注意**：导入模型使用百炼推理引擎，其默认参数可能与 vLLM/SGLang 不同。建议在 API 调用时显式设置 `temperature=1.0`、`top_p=1.0` 等参数以保持效果一致。

## 权限问题

部署时如遇权限不足，需检查：

1. API Key 归属[业务空间](../concepts/workspace.md)是否拥有模型部署权限（前往[业务空间](../concepts/workspace.md)管理 > 模型权限流控设置）
2. API Key 归属账号是否在对应[业务空间](../concepts/workspace.md)的权限管理用户列表中

## 关键限制

- 仅适用于华北二（北京）地域
- 部署成功后即开始计费
- 预付费订单无法提前终止服务
- 后付费账户欠费后，资源保留并继续计费 24 小时后自动释放
- 按 Token 用量计费的服务一个月不使用将自动释放

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)



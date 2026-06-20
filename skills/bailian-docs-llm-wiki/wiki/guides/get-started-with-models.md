# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API 接口，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需几行代码即可完成模型调用，平台覆盖文本生成、图像视频、语音音频、3D 生成、向量嵌入等多种模态。本文汇总了从账号准备到首次调用的完整流程，以及地域选择和限流规则等关键信息。

## 支持的模型

百炼提供开箱即用的模型服务，无需自行部署或运维。主要类别包括：

**千问（Qwen）系列旗舰模型：**

- **qwen3.7-max**：效果最好，适合复杂、多步骤任务
- **qwen3.7-plus**：效果、速度和成本均衡，多数场景的推荐选择
- **qwen3.6-flash**：高性价比、低延迟，适合快速响应的简单任务

**第三方模型：** deepseek-v4-pro、deepseek-v4-flash、kimi-k2.7-code、glm-5.2、MiniMax-M2.7 等，API 格式与千问模型一致。

**多模态覆盖：** 视觉理解（qwen3.7-plus、qwen3.5-omni-plus）、图像生成（wan2.7-image-pro、qwen-image-2.0-pro）、视频生成（happyhorse-1.0 系列）、语音合成（cosyvoice-v3.5-plus）、语音识别（fun-asr）、全模态对话（qwen3.5-omni-plus-realtime）、向量嵌入（text-embedding-v4）、重排序（qwen3-rerank）等。

完整模型列表参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

## 首次调用流程

### 1. 账号准备

1. 注册阿里云账号并完成实名认证
2. 使用主账号登录百炼控制台，阅读并同意协议即可自动开通
3. 前往 API Key 页面创建 API Key
4. 如使用华北2（北京）、新加坡、东京或法兰克福地域，还需获取[业务空间](../concepts/workspace.md) ID（WorkspaceId）

### 2. 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"

# Windows PowerShell
$env:DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
```

永久配置请追加到 `~/.bashrc`（Linux）、`~/.zshrc`（macOS Zsh）或通过系统属性设置（Windows）。详细步骤参见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 调用模型

百炼兼容 OpenAI 接口规范，只需调整 `api_key`、`base_url` 和模型名称即可迁移现有代码。

**Python 示例（OpenAI SDK）：**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)
```

也支持 [DashScope SDK](../concepts/dashscope-sdk.md)、Node.js（OpenAI SDK）和 curl 调用，请将 `{WorkspaceId}` 替换为真实的[业务空间](../concepts/workspace.md) ID。

## 地域选择

百炼在多个地域提供服务，每个地域有独立的 Base URL、API Key 和模型列表，**不能跨地域混用**。

| 场景 | 推荐地域 | 服务部署范围 |
|------|---------|------------|
| 无数据驻留限制，追求更大推理资源池 | 美国（弗吉尼亚）/ 德国（法兰克福）/ 日本（东京） | 全球 |
| 数据不出中国内地 | 华北2（北京） | 中国内地 |
| 数据不经过中国内地 | 新加坡 | 国际 |
| 数据不出特定国家/地区 | 美国 / 德国 / 日本 | 对应地域限定部署 |

各地域 Base URL 格式：
- **北京**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **法兰克福**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`
- **东京**：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

> **注意**：北京和新加坡地域推出了新版专属域名（含 WorkspaceId），相比旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 具有更好的性能和稳定性，建议迁移。

各地域功能差异：批量推理和模型调优仅北京地域支持；模型告警仅北京和新加坡支持。详见[选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限流规则

百炼按**主账号维度**对模型调用设置限流，账号下所有 RAM 子账号、[业务空间](../concepts/workspace.md)和 API Key 的调用量合并计算。不同模型限流额度相互独立。

**主要限流指标：**

- **RPM**（每分钟请求数）：如 qwen3.7-plus 北京地域为 30,000 RPM
- **TPM**（每分钟 Token 数，含输入与输出）：如 qwen3.6-flash 北京地域为 10,000,000 TPM

服务还可能按秒级 RPS/TPS 执行限流，短时间内的请求爆发即使未超分钟级上限也可能触发。

**常见限流错误：**

| 错误信息 | 含义 |
|---------|------|
| `Requests rate limit exceeded` | 触发 RPM 限流 |
| `Allocated quota exceeded` | 触发 TPM 限流 |
| `Request rate increased too quickly` | 请求频率激增，触发稳定性保护 |

**应对策略：**

1. 优先使用稳定版模型（如 `qwen-plus`），限流额度更宽松
2. 平滑请求速率，采用匀速调度或指数退避
3. 添加备选模型，限流后自动切换
4. 无实时需求时使用 Batch API（不受实时限流约束）
5. 在控制台"限流提额"页面提升临时 TPM 额度（提交后立即生效，有效期 30 天）

详细限流数据参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 计费概要

开通百炼无需费用，调用模型时按量计费。新用户可获得北京地域专属的免费额度用于体验。免费额度用完后：

- 已认证用户自动转为按量付费
- 可开启"免费额度用完即停"功能避免意外扣费

模型调用按分钟出账，需确保阿里云账户余额充足。也可订阅 Coding Plan（AI 编码套餐），以固定月费获取月度请求额度。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)




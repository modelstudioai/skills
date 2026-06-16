# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API 接口，集成千问（Qwen）全系列模型及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需几行代码即可完成大模型调用，平台还提供可视化应用构建、模型微调、部署和评测等全链路服务。本文梳理从账号准备到发起第一个 API 请求的完整流程，并说明模型选择、地域规划与限流规则。

## 快速开始

### 1. 账号准备

1. 注册阿里云账号并完成实名认证。
2. 使用主账号访问百炼控制台，自动开通服务。
3. 在控制台创建 API Key（环境变量名 `DASHSCOPE_API_KEY`）。
4. 若使用华北2（北京）、新加坡或德国（法兰克福）地域，还需获取[业务空间](../concepts/workspace.md) ID（WorkspaceId）填入 Base URL。

详细步骤参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. 配置环境变量

将 API Key 写入环境变量，避免硬编码泄露风险：

- **Linux/macOS**：写入 `~/.bashrc` 或 `~/.zshrc`，执行 `source` 生效。
- **Windows**：通过系统属性、`setx`（CMD）或 `[Environment]::SetEnvironmentVariable`（PowerShell）设置。

### 3. 发起第一个请求

百炼兼容 OpenAI 接口规范，使用 OpenAI SDK 即可调用。以 Python 为例：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)
```

也支持 Node.js（OpenAI SDK）、DashScope SDK 和 curl 方式调用。将 `{WorkspaceId}` 替换为真实[业务空间](../concepts/workspace.md) ID，Base URL 根据地域不同而变化。

## 支持的模型

百炼提供覆盖多种模态的模型服务，详细列表参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

### 文本生成

| 层级 | 代表模型 | 定位 |
|------|---------|------|
| 旗舰 | qwen3.7-max | 效果最强，适合复杂多步骤任务 |
| 均衡 | qwen3.7-plus | 效果、速度、成本均衡，多数场景推荐 |
| 高性价比 | qwen3.6-flash | 低延迟，适合简单快速响应任务 |
| 第三方 | deepseek-v4-pro、kimi-k2.7-code、glm-5.1 等 | API 格式与千问一致 |

### 多模态与其他能力

- **视觉理解/生成**：qwen3.7-plus（图像理解）、wan2.7-image-pro（图像生成）、happyhorse 系列（视频生成/编辑）
- **语音**：cosyvoice-v3.5-plus（语音合成）、fun-asr / fun-asr-realtime（语音识别）
- **全模态**：qwen3.5-omni-plus（融合文本、图像、音频、视频）
- **向量与重排序**：text-embedding-v4、qwen3-rerank
- **3D 生成**：Tripo-H3.1、Tripo-P1.0

## 地域与服务部署范围

调用百炼前需选择地域（决定接入点和数据存储位置）和服务部署范围（决定推理执行位置）。各地域的 Base URL、API Key 和可用模型相互独立，不能跨地域混用。详情参见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

| 场景 | 推荐地域 | 服务部署范围 |
|------|---------|------------|
| 无合规限制，追求最大资源池 | 美国（弗吉尼亚）/ 德国（法兰克福） | 全球 |
| 数据不出中国内地 | 华北2（北京） | 中国内地 |
| 数据不经过中国内地 | 新加坡 | 国际 |
| 数据不出美国/欧盟 | 美国（弗吉尼亚）/ 德国（法兰克福） | 美国/欧盟 |

各地域 Base URL（OpenAI 兼容模式）：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

> **注意**：华北2（北京）和新加坡地域已推出新版域名 `{WorkspaceId}.{region}.maas.aliyuncs.com`，旧版域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 即将下线，请尽快迁移。

## 限流规则与应对

百炼按主账号维度设置限流，账号下所有 RAM 子账号、[业务空间](../concepts/workspace.md)和 API Key 的调用量合并计算。不同模型的限流额度相互独立。详情参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 限流类型

| 错误信息 | 触发原因 |
|---------|---------|
| `Requests rate limit exceeded` | 每分钟请求数（RPM）超限 |
| `Allocated quota exceeded` | 每分钟 Token 消耗（TPM）超限 |
| `Request rate increased too quickly` | 请求频率短时间内激增，触发稳定性保护 |

### 典型限流额度（北京地域）

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max（稳定版） | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |
| qwen-plus | 30,000 | 5,000,000 |

带日期后缀的快照版本限流通常更低（RPM 60~600）。

### 应对策略

1. **优先使用稳定版模型**（如 `qwen-plus`），限流额度高于快照版。
2. **平滑请求速率**：采用匀速调度或指数退避，避免瞬时高峰。
3. **添加备选模型**：主模型触发限流后自动切换到备用模型重试。
4. **使用批量推理（Batch API）**：无需实时响应时，批量请求不受实时限流约束。
5. **提升临时限流额度**：在百炼控制台的"限流提额"页面申请临时 TPM 提额，提交后立即生效，有效期 30 天。

## 计费与免费额度

- 开通百炼免费，调用模型时按量计费。
- 新用户享有北京地域专属免费额度；已认证用户额度用完后自动转为按量付费。
- 可开启"免费额度用完即停"功能防止意外扣费。
- Coding Plan（AI 编码套餐）提供固定月费的请求额度，需使用专属 Base URL 和 API Key 调用。

## 进阶功能

- **模型微调**：支持有监督微调（SFT）、继续预训练（CPT）和直接偏好优化（DPO）。
- **[模型部署](../concepts/model-deployment.md)**：将[模型部署](../concepts/model-deployment.md)为资源专享的推理服务，满足高并发低延迟需求。
- **应用构建**：通过可视化智能体/工作流应用，或高代码应用部署 Python 后端服务。
- **知识库（RAG）**：接入私有数据，增强模型回答准确性。
- **插件与 MCP**：通过插件和模型上下文协议调用外部服务扩展能力。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)



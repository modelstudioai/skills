# get started with models

阿里云百炼提供开箱即用的大模型服务，开发者可通过标准化 API（兼容 OpenAI 协议）快速集成千问（Qwen）及主流第三方模型。本文档汇总核心接入要素，涵盖模型选择、参数配置、调用方式及关键限制，助您高效完成首次调用与生产部署。

## 支持的模型/功能

百炼支持多模态、全场景模型服务，包括文本生成、图像/视频理解与生成、语音合成与识别、3D 生成、[向量嵌入](../concepts/embedding.md)与重排序等。主力文本模型按能力与成本分层：

- **qwen3.8-max**：旗舰模型，适合复杂多步任务；[最新版推理能力全面超越前代](raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **qwen3.7-plus**：效果、速度与成本均衡，为多数场景的**推荐选择**；
- **qwen3.8-flash**：高性价比、低延迟，适用于简单快速响应任务；
- 其他模型如 `deepseek-v4-pro-0813`、`kimi/kimi-k3`、`glm-5.3` 等均在[模型广场](raw/model-user-guide/get-started-with-models/models.md)中提供完整列表与地域支持详情。

> **注意**：文档 2 中称 `qwen3.8-max` 为“最新版”，但文档 3 的模型列表中同时存在 `qwen3.8-max` 和 `qwen3.8-max-0902`；文档 4 的限流表显示后者为独立型号且限流策略不同（TPM 150万 vs 动态限流）。实际使用时应以[模型广场](raw/model-user-guide/get-started-with-models/models.md)控制台展示为准，避免硬编码带日期后缀的快照版本。

## 关键参数

调用模型需明确以下核心参数：

- **`model`**：必需，指定模型名称（如 `"qwen3.7-plus"`），值必须与所选地域支持的模型完全一致；
- **`base_url`**：必需，决定接入点与服务部署范围，**必须与 API Key 所属地域和计费方案严格匹配**；
- **`api_key`**：必需，通过环境变量 `DASHSCOPE_API_KEY` 传入更安全（详见[首次调用千问API](raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）；
- **`workspace_id`**：仅当使用业务空间专属域名时需显式填入（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`），可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面查看。

## 使用方式

### 1. 获取凭证与配置环境
- 注册阿里云账号并开通百炼服务；
- 在[API Key 页面](https://bailian.console.aliyun.com/model/settings/api-key)创建 Key，**无需绑定模型**（模型由请求体 `model` 参数指定）；
- 将 `DASHSCOPE_API_KEY` 配置为系统环境变量（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 推荐系统属性配置），避免代码中硬编码。

### 2. 选择 Base URL
根据使用场景选用：
- **生产环境（推荐）**：业务空间专属域名（如 `https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），具备更高吞吐、更低时延与流量隔离；
- **存量迁移/兼容**：DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），但需注意其将于 2026 年 9 月 30 日起停止支持新特性；
- **临时验证**：试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），限流严格，不建议用于生产。

完整域名对照见 [Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md)。

### 3. 发起调用（OpenAI SDK 示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为真实 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

## 限制和注意事项

- **限流机制**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。分为 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗数，含输入+输出），超出任一阈值即返回 HTTP 429。部分模型（如 `qwen3.8-max`）采用[动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值随月消费金额自动提升。
- **请求体大小**：不含 Base64 的请求最大 16 MiB；含 Base64 时单个内容最大 20–32 MiB（依协议而定），整体请求体最大 64 MiB，但解码后仍不得超过 16 MiB，否则返回 413 错误。
- **地域约束**：各地域 API Key、Base URL、模型列表相互独立，**严禁混用**。例如北京地域的 Key 无法调用新加坡地域的模型。
- **免费额度控制**：新用户享北京地域专属免费额度，用尽后可开启“[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)”开关防止意外扣费；充值不影响限流阈值，仅保障账户可用性。
- **数据隐私承诺**：按量付费 API 和 [Token](../concepts/token.md) Plan 团队版**不会将您的数据用于模型训练**；但 Coding Plan 与 [Token](../concepts/token.md) Plan 个人版除外，具体条款见[合规资质与隐私说明](raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)



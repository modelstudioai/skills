# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准化 API（兼容 OpenAI）快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需完成账号开通、API Key 配置与 Base URL 设置，即可发起首次推理请求。本文档聚焦核心接入路径，涵盖模型选择、关键参数、调用方式及生产约束。

## 支持的模型/功能

百炼支持[多模态](../concepts/multimodal.md)、多场景模型，覆盖文本生成、图像/视频理解与生成、语音合成与识别、全模态交互、向量嵌入、决策建模等能力。主力文本模型包括：

- **qwen3.8-max**：旗舰级模型，适合复杂多步任务；最新版推理能力全面超越前代，推荐选用  
- **qwen3.7-plus**：效果、速度与成本均衡，是多数场景的**推荐选择**  
- **qwen3.8-flash**：高性价比、低延迟，适合简单任务快速响应  

此外支持 DeepSeek、Kimi、GLM、MiniMax、Tripo 等第三方模型，以及 qwen-audio、qwen-image、happyoyster（世界模型）、qwen3.8-omni-flash（全模态）等专用模型。完整模型列表请参见[选择模型](raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 2 中称“qwen3.8-max 推理能力全面超越前代”，而文档 3 的模型列表中未标注版本演进关系；实际选型应以控制台实时模型市场为准，避免依赖静态描述。

## 关键参数

### API Key
- 必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/model/settings/api-key)创建，**主账号维度生效**  
- 创建时可选择“全部模型”或“自定义权限”，后者支持限制该 Key 可调用的模型范围  
- 各地域 API Key **不通用**，需按目标地域分别创建 [首次调用千问API](raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)

### Base URL
- 必须与 API Key 所属地域和计费方案严格匹配，否则返回 401 错误  
- 生产环境**强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与流量隔离能力  
- DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）为存量兼容方案，将于 2026 年 9 月 30 日起停止支持新特性  
- 试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）仅限临时验证，限流值极小，**不适用于生产**  
- 详细域名对照请参考[Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md)

### 模型标识（model）
- 在请求体中通过 `model` 字段指定，例如 `"model": "qwen3.7-plus"`  
- 模型名称与地域强绑定：同一模型在不同地域可能有不同限流策略或可用性（如 DeepSeek 仅支持北京地域）  
- 不同计费方案（按量付费、[Token](../concepts/token.md) Plan、Coding Plan）需使用对应专属 Base URL 和 API Key，不可混用  

## 使用方式

### 基础流程
1. **开通服务**：使用阿里云主账号登录[百炼控制台](https://bailian.console.aliyun.com/model/market)，开通服务并完成实名认证  
2. **创建 API Key**：进入[API Key 页面](https://bailian.console.aliyun.com/model/settings/api-key)，创建 Key 并记录  
3. **获取业务空间 ID（WorkspaceId）**：若使用业务空间专属域名（推荐），需前往[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面查看 ID  
4. **配置环境变量**：将 API Key 写入 `DASHSCOPE_API_KEY` 环境变量（Linux/macOS/Windows 均有标准配置方法），避免硬编码 [首次调用千问API](raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)  
5. **发起请求**：使用 OpenAI SDK 或 curl，设置 `base_url` 和 `model` 参数  

### 示例（OpenAI Python SDK）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为真实 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

## 限制和注意事项

### 限流机制
- **账号级合并计算**：限流按阿里云主账号维度统计，所有 RAM 子账号、业务空间、API Key 的调用量合并计入  
- **双维度限流**：每分钟调用次数（RPM）和每分钟 [Token](../concepts/token.md) 消耗（TPM，含输入+输出）任一超限即触发 429 错误  
- **动态限流**：qwen3.8-max、qwen3.8-flash 等模型采用动态 TPM 限流，额度随百炼月消费金额分档调整（如北京地域消费 ¥10–100 万档对应 qwen3.8-max 为 1000 万 TPM），实际可用值可能高于档位值 [动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)  
- **RPM/TPM 表格参考**：具体数值因地域和模型版本差异极大，务必查阅[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)文档中的最新表格，例如 qwen3.7-plus 在北京地域为 RPM 30,000 / TPM 5,000,000，而在新加坡则为 RPM 15,000 / TPM 5,000,000  

### 地域与部署约束
- **地域不可跨用**：各地域（北京、新加坡、美国弗吉尼亚等）拥有独立的 API Key、Base URL、模型列表和计费体系，**严禁混用**  
- **服务部署范围**：德国（法兰克福）、日本（东京）等地域需在业务空间中显式选择“全球”或“欧盟/日本”等部署范围，影响推理节点物理位置  
- **功能差异**：批量推理、高级监控、模型调优等功能并非全地域支持（如美国弗吉尼亚不支持批量推理），详见[各地域功能支持](raw/model-user-guide/get-started-with-models/regions.md)  

### 其他关键注意事项
- **免费额度**：新用户在北京地域享有专属免费额度，用完后可自动转为按量付费，或开启“免费额度用完即停”避免意外扣费  
- **费用控制**：充值不影响限流阈值；如需更高 RPM/TPM，需联系商务经理申请提额  
- **安全承诺**：按量付费 API 和 [Token](../concepts/token.md) Plan 团队版**不会使用您的数据训练模型**；但 Token Plan 个人版与 Coding Plan 数据使用条款不同，详见[合规资质与隐私说明](raw/model-user-guide/security-and-compliance/privacy-notice.md)

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)



# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API 接口，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需几行代码即可完成模型调用，平台还提供可视化应用构建、模型微调与部署等全链路能力。本文介绍如何快速开始使用百炼的模型服务。

## 前置准备

使用百炼模型 API 前，需完成以下准备工作（详见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）：

1. **注册并开通**：注册阿里云账号，前往百炼控制台阅读并同意服务协议即可开通。
2. **获取 API Key**：在控制台的 API Key 页面创建密钥。各地域的 API Key 相互独立，不可跨地域使用。
3. **获取[业务空间](../concepts/workspace.md) ID**：使用华北2（北京）、新加坡或德国（法兰克福）地域时，需在 Base URL 中填入[业务空间](../concepts/workspace.md) ID（WorkspaceId）。
4. **配置环境变量**：建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险。

## 选择地域

百炼提供四个地域的模型服务，每个地域有独立的 Base URL、API Key 和模型列表，**不能跨地域混用**。根据数据合规和延迟需求选择（详见[选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)）：

| 场景 | 推荐地域 | 服务部署范围 |
|------|----------|-------------|
| 无数据驻留限制，追求最大推理资源池 | 美国（弗吉尼亚）或德国（法兰克福） | 全球 |
| 数据不出中国内地 | 华北2（北京） | 中国内地 |
| 数据不经过中国内地 | 新加坡 | 国际 |
| 数据不出美国 | 美国（弗吉尼亚） | 美国（使用 `-us` 后缀模型名） |
| 数据不出欧盟 | 德国（法兰克福） | 欧盟 |

各地域 Base URL（OpenAI 兼容）：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

> **注意**：北京和新加坡地域推出了新版专属域名（含 WorkspaceId），在性能和稳定性上优于旧版，建议尽快迁移。

## 选择模型

百炼覆盖文本、图像、音频、视频、3D 等多种模态，详见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。核心模型推荐：

### 文本生成

| 模型系列 | 代表模型 | 定位 |
|---------|---------|------|
| 千问 Max | qwen3.7-max | 效果最强，适合复杂多步骤任务 |
| 千问 Plus | qwen3.7-plus | 效果、速度和成本均衡，多数场景推荐 |
| 千问 Flash | qwen3.6-flash | 高性价比低延迟，适合简单任务 |
| 第三方 | deepseek-v4-pro、kimi-k2.7-code、glm-5.1 等 | API 格式与千问一致 |

### 其他模态

- **图像与视频**：理解（qwen3.7-plus）和生成（wan2.7-image-pro、qwen-image-2.0-pro、happyhorse-1.0-t2v 等）
- **音频与语音**：语音合成（cosyvoice-v3.5-plus）、语音识别（fun-asr）、音乐生成（fun-music-v1）、语音转语音
- **全模态**：qwen3.5-omni-plus，融合文本、图像、音频、视频的理解与生成
- **向量与重排序**：text-embedding-v4、qwen3-rerank
- **3D 模型生成**：Tripo-H3.1、Tripo-P1.0

## 快速调用示例

百炼兼容 OpenAI 接口规范，只需调整 API Key、`base_url` 和模型名称即可将现有 OpenAI 代码迁移。支持 OpenAI SDK、DashScope SDK、Anthropic 兼容接口和 HTTP 直接调用。

### Python（OpenAI SDK）

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

### Node.js（OpenAI SDK）

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

const completion = await openai.chat.completions.create({
    model: "qwen3.7-plus",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(completion.choices[0].message.content);
```

> **注意**：不同地域的 `base_url` 不通用，需替换为对应地域的 URL 和真实的[业务空间](../concepts/workspace.md) ID。

## 限流与配额

百炼按主账号维度对模型调用设置限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算。超出限制时请求被拒绝，通常一分钟内恢复。详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 限流指标

- **RPM**（每分钟请求数）：稳定版模型通常 15,000~30,000，快照版通常 60~600
- **TPM**（每分钟 Token 数）：稳定版通常 5,000,000~10,000,000，快照版通常 100,000~1,000,000

服务可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行，短时间内的请求爆发也可能触发限流。

### 应对限流的策略

1. **优先选用高限流模型**：稳定版或最新版比带日期的快照版本限流更宽松
2. **平滑请求速率**：采用匀速调度、指数退避或请求队列，避免瞬时高峰
3. **添加备选模型**：主模型触发限流后自动切换到备用模型
4. **使用批量推理**：无需实时响应时，使用 Batch API（不受实时限流约束）
5. **提升临时限流额度**：在百炼控制台的限流提额页面申请，提交后立即生效，有效期 30 天

## 计费说明

开通百炼无需费用，调用模型时按量计费。新用户享有北京地域的免费额度。

- 已认证用户免费额度用完后自动转为按量付费
- 未认证用户免费额度用完后需完成认证并充值
- 可开启"免费额度用完即停"功能避免意外扣费
- 订阅 Coding Plan（AI 编码套餐）可获得固定月费的请求额度
- 模型调用按分钟出账，调用统计约一小时后可在控制台的模型监控页面查看

## 各地域功能差异

| 功能 | 北京 | 新加坡 | 弗吉尼亚 | 法兰克福 |
|------|------|--------|----------|----------|
| 实时推理 | 支持 | 支持 | 支持 | 支持 |
| 批量推理 | 支持 | 支持 | 不支持 | 不支持 |
| 模型调优 | 支持 | 不支持 | 不支持 | 不支持 |
| 模型告警 | 支持 | 支持 | 不支持 | 不支持 |

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)



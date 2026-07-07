# get started with models

阿里云百炼是一站式大模型开发平台，兼容 OpenAI 接口规范，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需获取 API Key 并配置 Base URL，即可通过几行代码调用文本生成、视觉理解、图像生成、语音合成等[多模态](../concepts/multimodal.md)能力。本文梳理从账号开通到首次 API 调用的完整流程，以及地域选择、接入域名和限流等关键注意事项。

## 支持的模型与能力

百炼提供开箱即用的模型服务，无需自行部署，按需选择即可。详细模型列表参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

**文本生成（核心能力）**：

| 模型层级 | 代表模型 | 定位 |
|---------|---------|------|
| Max | qwen3.7-max | 效果最强，适合复杂多步骤任务 |
| Plus | qwen3.7-plus | 效果、速度、成本均衡，多数场景推荐 |
| Flash | qwen3.6-flash | 高性价比低延迟，适合简单快速响应 |
| 第三方 | deepseek-v4-pro、kimi-k2.7-code、glm-5.2 等 | API 格式与千问一致 |

**[多模态](../concepts/multimodal.md)能力**：

- **视觉理解**：qwen3.7-plus、qwen3.5-omni-plus 等，支持图片/视频内容分析
- **图像/视频生成**：wan2.7-image-pro、qwen-image-2.0-pro、happyhorse 系列
- **语音合成**：cosyvoice-v3.5-plus
- **语音识别**：fun-asr-realtime（专业 ASR）、qwen3.5-omni-plus（大模型方案）
- **全模态（Omni）**：qwen3.5-omni-plus-realtime，融合文本/图像/音频/视频的端到端理解与生成
- **向量与重排序**：text-embedding-v4、qwen3-rerank
- **3D 生成**：Tripo-H3.1、Tripo-P1.0

## 快速开始：首次 API 调用

完整步骤参见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 1. 开通服务与获取 API Key

1. 使用阿里云主账号访问[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)，阅读协议后自动开通
2. 前往 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建密钥
3. 如使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域，还需在 Base URL 中填入[业务空间](../concepts/workspace.md) ID（WorkspaceId）

### 2. 配置 API Key 到环境变量

建议将 API Key 存入环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

```bash
# macOS / Linux
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"

# 永久生效（macOS zsh）
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc
```

### 3. 调用示例（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）

**Python**：

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

**Node.js**：

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

**curl**：

```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"你是谁？"}]}'
```

> **注意**：以上示例均使用华北2（北京）地域的 Base URL，需将 `{WorkspaceId}` 替换为实际的[业务空间](../concepts/workspace.md) ID。不同地域的 Base URL 不通用。

## 地域、服务部署范围与接入域名

百炼目前在 5 个地域提供服务，详细说明参见[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

### 地域选择指南

| 数据合规需求 | 推荐地域 | 服务部署范围 |
|-------------|---------|------------|
| 数据不出中国内地 | 华北2（北京） | 中国内地 |
| 数据不出美国 | 美国（弗吉尼亚） | 美国 |
| 数据不出欧盟 | 德国（法兰克福） | 欧盟 |
| 数据不出日本 | 日本（东京） | 日本 |
| 无合规限制，追求最大资源池 | 美国/德国/日本 | 全球 |
| 数据不经过中国内地 | 新加坡 | 国际 |

> **注意**：各地域的 API Key 相互独立，不能跨地域使用。部分功能（模型调优、应用开发）仅在华北2（北京）地域支持。

### 接入域名类型

百炼提供三种接入域名，详见[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)：

| 类型 | 格式 | 适用场景 | 超时 | SLA |
|------|------|---------|------|-----|
| [业务空间](../concepts/workspace.md)专属域名（推荐） | `{WorkspaceId}.{region}.maas.aliyuncs.com` | 生产环境，高并发 | 3600s | 99.9% |
| Dashscope 域名 | `dashscope.aliyuncs.com` | 存量兼容，建议迁移 | 600s | 99.9% |
| 试用域名 | `trial.{region}.maas.aliyuncs.com` | 快速验证 | 600s | 无 |

生产环境强烈建议使用**业务空间专属域名**，迁移仅需替换 Base URL 中的域名部分，无需修改业务逻辑。

此外百炼还提供 Coding Plan 和 Token Plan 专属域名，仅限 Claude Code、Codex 等 AI 编码工具使用，不能用于后端服务。

## 限流机制

限流按**主账号维度**计算，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并统计。不同模型的限流额度相互独立。详细规则参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 限流指标

- **RPM**（Requests Per Minute）：每分钟请求数
- **TPM**（Tokens Per Minute）：每分钟 Token 消耗（含输入与输出）

稳定版/最新版模型通常拥有更高的限流额度。以华北2（北京）为例：

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |

> **注意**：即使每分钟总量未超限，短时间内请求爆发也可能触发秒级限流（RPS = RPM/60）。收到 `Request rate increased too quickly` 时，需平滑请求速率。

### 应对限流的策略

1. **优先使用高限流模型**：如 qwen-plus 系列，稳定版比日期快照版额度更宽松
2. **添加备选模型**：主模型限流时自动切换到备用模型重试
3. **平滑请求**：采用匀速调度或指数退避，避免瞬时高峰
4. **批量推理**：非实时场景使用 Batch API，不受实时限流约束
5. **临时提额**：在控制台[限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)页面提升 TPM，提交后立即生效，有效期 30 天

## 计费要点

- 开通百炼免费，调用模型按量付费（分钟级出账）
- 新用户享有北京地域专属免费额度；可开启"免费额度用完即停"避免意外扣费
- 已认证用户免费额度用完后自动转为按量付费
- 订阅 Coding Plan（AI 编码套餐）可获得固定月费的请求额度，无按量扣费风险
- 通过[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看调用量统计（调用约一小时后可见）

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)



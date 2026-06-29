# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问及主流第三方模型，提供兼容 OpenAI 的 API 和全链路模型服务。本页汇总从[模型选型](../concepts/model-selection.md)、地域/接入域名选择、首次 API 调用到限流管理的核心步骤，帮助开发者快速跑通第一次模型调用并了解生产环境的注意事项。

## 支持的模型与能力

百炼提供开箱即用的模型服务，无需自行部署或运维，直接调用自研千问（Qwen）全系列模型以及 DeepSeek、Kimi、GLM 等第三方大模型。详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

- **千问旗舰模型（从能力最强到成本最低）**：
  - qwen3.7-max：Qwen 系列效果最好的模型，适合复杂、多步骤任务。最新的 qwen3.7-max 推理能力全面超越前代，推荐选用。
  - qwen3.7-plus：效果、速度和成本均衡，是多数场景的推荐选择。
  - qwen3.6-flash：高性价比、低延迟，适合需要快速响应的简单任务。
- **第三方模型**：deepseek-v4-pro、deepseek-v4-flash、kimi-k2.7-code、glm-5.2、MiniMax-M2.7、mimo-v2.5-pro 等，API 格式与千问模型一致。
- **[多模态](../concepts/multimodal.md)覆盖**：文本生成、视觉理解（qwen3.7-plus、qwen3.5-omni-plus）、图像生成（wan2.7-image-pro、qwen-image-2.0-pro）、视频生成（happyhorse-1.1-t2v/i2v/r2v）、3D 生成（Tripo-H3.1/P1.0）、语音合成（cosyvoice-v3.5-plus、speech-2.8-hd）、音乐生成（fun-music-v1）、语音识别（fun-asr-realtime、fun-asr）、语音转语音（qwen3.5-omni-plus-realtime）、全模态、向量与重排序（text-embedding-v4、qwen3-rerank）。

除开箱即用模型外，百炼还支持模型调优（SFT/CPT/DPO）、模型部署（将预置或自定义模型部署为资源专享的推理服务）和模型评测（人工/自动/基线评测）。

## 选择地域、服务部署范围与接入域名

调用前需先确定地域、服务部署范围和接入域名，三者共同决定数据存储位置、推理执行位置和并发上限。详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

- **地域**：决定接入点和数据存储位置，就近选择可降低延迟。提供华北2（北京，`cn-beijing`）、新加坡（`ap-southeast-1`）、美国（弗吉尼亚）、德国（法兰克福，`eu-central-1`）、日本（东京，`ap-northeast-1`）五个地域。
- **服务部署范围**：决定推理执行位置。无合规需求选"全球"部署范围（推理资源池更大）；有数据合规需求选特定地理边界（中国内地/美国/欧盟/日本/国际）。
- **接入域名**：百炼提供专属、共享、试用三种接入域名，推荐生产环境使用专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`），其具备更高并发承载能力与网络隔离性，请求超时 3600 秒，支持 HTTP/SSE/WebSocket/WebRTC，并提供 99.9% SLA。共享域名（`dashscope.aliyuncs.com`）兼容存量业务，建议迁移至专属域名。试用域名（`trial.{region}.maas.aliyuncs.com`）仅用于快速体验，不建议用于生产。

> **注意**：各地域有独立的接入域名、[API Key](../concepts/api-key.md) 和模型列表，**不能跨地域混用**。德国（法兰克福）和日本（东京）地域通过[业务空间](../concepts/workspace.md)（Workspace）区分服务部署范围，调用前需在[业务空间](../concepts/workspace.md)管理页面创建[业务空间](../concepts/workspace.md)并选择部署范围。美国（弗吉尼亚）地域使用带 `-us` 后缀的模型名称（如 `qwen-plus-us`）可限定美国境内推理，不带后缀默认全球推理。

华北2（北京）和新加坡地域各仅支持一种服务部署范围（分别为中国内地和国际），无需选择。功能支持上，批量推理、模型告警、模型调优仅部分地域支持；实时推理、模型体验、模型监控、传输安全、权限管理所有地域均支持。

## 首次调用千问 API

百炼支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、DashScope SDK 等方式调用大模型。首次调用流程见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 账号设置

1. 注册阿里云账号（无账号时）。
2. 使用**阿里云主账号**前往百炼控制台开通服务（阅读并同意协议即自动开通；若提示未实名认证需先完成实名认证）。
3. 前往 [API Key](../concepts/api-key.md) 页面创建 [API Key](../concepts/api-key.md)。
4. 使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域的模型时，需在 Base URL 中填入业务空间 ID（WorkspaceId），可在业务空间管理页面查看。

### 配置 API Key 到环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中显式配置，降低泄露风险。各系统配置方式：

- **Linux/macOS**：永久变量追加到 `~/.bashrc`（Bash）或 `~/.zshrc`（Zsh），执行 `source` 后生效；临时变量用 `export DASHSCOPE_API_KEY="YOUR_KEY"`。
- **Windows**：通过系统属性、CMD（`setx`）或 PowerShell（`[Environment]::SetEnvironmentVariable`）配置永久变量；CMD 用 `set`、PowerShell 用 `$env:` 配置临时变量。

### 调用示例（Python + OpenAI SDK）

要求 Python 3.8 及以上。建议先创建虚拟环境（`python -m venv .venv`）并安装 SDK（`pip install -U openai` 或 `pip install -U dashscope`）。

```python
import os
from openai import OpenAI

try:
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 华北2（北京）地域URL，调用时请将WorkspaceId替换为真实业务空间ID
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '你是谁？'}
        ]
    )
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"错误信息：{e}")
```

百炼兼容 OpenAI 接口规范，只需调整 API Key、base_url 和模型名称，即可将现有 OpenAI 代码迁移至百炼。除 Python 外，也支持 Node.js 和 curl 调用。

> **注意**：不同地域的 Base URL 不通用。北京地域示例为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；美国（弗吉尼亚）为 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`；新加坡、德国、日本地域的 Base URL 需对应替换地域标识并填入业务空间 ID。

## 限流管理

百炼按主账号维度对模型调用设置限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算，超出限制时请求被拒绝，通常一分钟内自动恢复。详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 限流类型与错误识别

- `Requests rate limit exceeded` / `You exceeded your current requests list`：触发每分钟请求数（RPM）限流。
- `Allocated quota exceeded` / `You exceeded your current quota`：触发每分钟 [Token](../concepts/token.md) 消耗（TPM）限流。
- `Request rate increased too quickly`：请求频率短时间激增，触发系统稳定性保护（即使总量未达上限也会触发）。

除 RPM 和 TPM 外，限流策略可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行。不同模型限流额度相互独立，稳定版或最新版比带日期的快照版本限流更宽松。例如华北2（北京）qwen3.7-max 为 30,000 RPM / 5,000,000 TPM，而 qwen3.7-max-2026-06-08 快照版为 600 RPM / 1,000,000 TPM。

### 避免限流的策略

1. **选用高限流模型**：优先使用 qwen-plus 等限流额度更高的模型；优先稳定版而非快照版。
2. **优化调用策略**：降低调用频率（应对 RPM 限流）、缩短输入或限制输出长度（应对 TPM 限流）、匀速调度/指数退避/请求队列平滑请求速率（应对频率激增）。
3. **添加备选模型**：触发限流后自动切换备用模型重试（如下示例）。
4. **拆分任务**：将长对话或大文档拆分为小批次分时段提交。
5. **批量推理**：无需实时响应时使用 Batch API，批量请求不受实时限流约束。
6. **提升临时限流额度**：默认额度不足时，在控制台"限流提额"页面提升模型临时 TPM 额度，立即生效，有效期 30 天（目前支持华北2北京和新加坡地域）。

```python
import os, asyncio
from openai import AsyncOpenAI, APIStatusError

API_KEY = os.getenv("DASHSCOPE_API_KEY")
MODEL = "qwen-plus-2025-07-28"
BACKUP_MODEL = "qwen-plus-2025-07-14"

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

async def send_request(model):
    try:
        await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "你是谁？"}]
        )
        return True
    except APIStatusError as e:
        if e.status_code == 429:
            print(f"[限流触发] 模型 {model}")
            return False
        raise

async def task(i):
    if await send_request(MODEL):
        return True
    return await send_request(BACKUP_MODEL)

async def main():
    results = await asyncio.gather(*(task(i) for i in range(10)))
    print(f"成功: {sum(results)}, 失败: {len(results)-sum(results)}")

asyncio.run(main())
```

### 用量与费用控制

限流仅约束单位时间内的调用速率，不限制累计用量。控制费用可通过：设置消费限额与费用告警（账单费用卡片）、开启免费额度用完即停（仅限新用户且在免费额度有效期内，目前仅华北2北京地域支持）、定期监控模型调用量（调用完约一小时后可在模型监控页面查看 [Token](../concepts/token.md) 消耗）。新用户在华北2（北京）地域有专属免费额度，未认证用户用完后需认证并充值才能继续；已认证用户用完后自动转按量付费。

## 快速开始

- 在线体验：打开百炼控制台，选择地域，进入模型体验页面选择模型。
- 发起第一个 API 请求：完成上述账号设置、环境变量配置和调用示例。
- 构建大模型应用：可通过可视化模式创建[智能体应用](../concepts/agent-application.md)和工作流应用，或通过高代码应用将 Python 项目部署为后端服务；通过[知识库](../concepts/knowledge-base.md)（RAG）、插件和 MCP 调用外部数据与服务。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)




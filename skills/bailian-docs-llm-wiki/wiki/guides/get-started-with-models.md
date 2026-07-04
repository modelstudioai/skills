# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问（Qwen）及 DeepSeek、Kimi、GLM 等第三方模型，提供兼容 OpenAI 的 API 与可视化应用构建能力。本页汇总从开通账号、选择模型、配置 Base URL 到首次调用与限流控制的完整上手路径，面向开发者快速跑通第一次模型调用。

## 平台定位与核心能力

百炼同时面向开发者与业务人员：开发者可通过兼容 OpenAI 的 API 在几行代码内调用大模型；业务人员可通过可视化工具搭建智能体、工作流与 RAG 知识库应用。平台还提供模型调优（SFT/CPT/DPO）、模型部署（资源专享推理服务）与模型评测能力，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

百炼不会将您的业务数据用于模型训练，传输过程全程加密。

## 支持的模型

百炼模型覆盖文本、图像、音频、视频、3D、全模态与向量/重排序等多种能力，按模态归类如下，完整列表以模型广场为准：

- **文本生成**：千问系列由强到成本最低包括 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`；第三方模型包括 `deepseek-v4-pro`、`deepseek-v4-flash`、`kimi-k2.7-code`、`glm-5.2`、`MiniMax-M2.7`、`mimo-v2.5-pro`，API 格式与千问一致。
- **图像与视频**：理解模型（`qwen3.7-plus`、`qwen3.5-omni-plus`、`kimi-k2.7-code`）和生成模型（`wan2.7-image-pro`、`qwen-image-2.0-pro`、`happyhorse-1.1-t2v/i2v/r2v`、`happyhorse-1.0-video-edit`）。
- **3D 生成**：`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`。
- **音频与语音**：语音合成 `cosyvoice-v3.5-plus`、`MiniMax/speech-2.8-hd`；音乐生成 `fun-music-v1`；语音识别 `fun-asr-realtime`、`fun-asr`、`qwen3.5-omni-plus-realtime`；端到端语音对话 `qwen3.5-omni-plus-realtime`。
- **全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-plus`。
- **向量与重排序**：`text-embedding-v4`、`tongyi-embedding-vision-plus`、`qwen3-rerank`。

千问系列选型建议：Max 适合复杂多步骤任务，Plus 在效果/速度/成本上均衡（多数场景推荐），Flash 适合低延迟简单任务。详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

## 地域、服务部署范围与接入域名

调用百炼前需确定三件事，三者关系见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)：

- **地域**：决定接入点与数据存储位置，就近选择可降低延迟。可选华北2（北京，`cn-beijing`）、新加坡（`ap-southeast-1`）、德国法兰克福（`eu-central-1`）、日本东京（`ap-northeast-1`）、美国弗吉尼亚（`us-east-1`）。
- **服务部署范围**：决定推理执行位置。无数据驻留限制可选"全球"；要求数据不出中国内地选"中国内地"；要求不经过中国内地选"国际"；另有美国/欧盟/日本境内限定范围。
- **接入域名**：影响并发上限与超时。推荐生产环境使用**业务空间专属域名** `{WorkspaceId}.{region}.maas.aliyuncs.com`（请求超时 3600 秒、SLA 99.9%、支持 HTTP/SSE/WebSocket/WebRTC）；存量业务可用 `dashscope.aliyuncs.com` 等中心化域名；试用域名 `trial.{region}.maas.aliyuncs.com` 仅限快速验证，不建议生产。

> **注意**：各地域的 API Key、模型列表、接入域名**不能跨地域混用**。美国（弗吉尼亚）暂不支持业务空间专属域名，需使用 `dashscope-us.aliyuncs.com`；德国、日本地域通过业务空间区分服务部署范围，调用前需先在业务空间管理页创建并选择部署范围。美国地域使用带 `-us` 后缀的模型名（如 `qwen-plus-us`）可限定美国境内推理，不带后缀默认全球推理。

功能支持也存在地域差异：批量推理、模型调优、应用开发仅在华北2（北京）与新加坡支持；模型告警仅北京与新加坡支持。

## Base URL 与计费方案

Base URL 必须与同一计费方案的 API Key 配套使用，错配会报 401。各方案的 OpenAI 兼容地址（以华北2北京为例）：

| 计费方案 | Base URL（OpenAI 兼容） | 适用场景 |
| --- | --- | --- |
| 按量付费 - Dashscope 域名 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 存量业务兼容，可跨业务空间调用 |
| 按量付费 - 业务空间专属 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 生产推荐，更高吞吐与时延隔离 |
| 按量付费 - 试用域名 | `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 快速验证，限流小 |
| Token Plan | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | Claude Code/Codex 交互式，不可用于后端服务 |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | AI 编码套餐，需用专属 API Key |

完整地址表（含 Anthropic 兼容地址与各地域）见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。从 Dashscope 域名迁移到业务空间专属域名只需在 API Key 创建弹窗或业务空间管理页复制 API Host 替换原域名，业务代码无需改动。

## 上手步骤：从开通到第一次调用

### 1. 账号与凭证

1. 注册阿里云账号并完成实名认证。
2. 使用**主账号**前往百炼控制台开通服务（同意协议即开通）。
3. 在 API Key 页面创建 API Key。
4. 北京、新加坡、东京、法兰克福地域需在业务空间管理页获取 `WorkspaceId`，填入 Base URL。

建议将 API Key 写入环境变量 `DASHSCOPE_API_KEY`，避免代码硬编码：

```bash
# Linux/macOS 永久（zsh）
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc
# Windows CMD 永久
setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
```

### 2. 安装 SDK

百炼兼容 OpenAI 接口规范，可直接用 OpenAI SDK，也可用 DashScope SDK。Python ≥ 3.8：

```bash
pip install -U openai      # 或
pip install -U dashscope
```

### 3. 发起首次调用

以 OpenAI Python SDK 调用千问为例（北京地域，业务空间专属域名）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

curl 调用：

```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"你是谁？"}]}'
```

完整的环境变量配置、Python/Node.js/curl 示例及 Windows 系统属性配置步骤见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。不熟悉编程可使用 Chatbox 等图形化客户端。

## 限流与用量控制

限流按**主账号维度**计算，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算；不同模型限流额度相互独立。超出时请求被拒，通常一分钟内自动恢复。常见错误与处理见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)：

| 错误信息 | 触发类型 | 处理建议 |
| --- | --- | --- |
| `Requests rate limit exceeded` | RPM 限流 | 降低调用频率 |
| `Allocated quota exceeded` | TPM 限流 | 缩短输入或限制输出长度 |
| `Request rate increased too quickly` | 频率激增保护 | 匀速调度、指数退避、请求队列 |

> **注意**：除 RPM/TPM 外，系统可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行，即使分钟级总量未超限，瞬时高峰也可能触发限流。Batch API 调用不受实时限流约束，但需排队处理。

避免限流的策略：优先选 `qwen-plus` 等高限流模型；稳定版/最新版比带日期快照版限流更宽松；配置备选模型在 429 时自动切换；长对话或大文档拆分为小批次；非实时场景使用批量推理；默认额度不足时在控制台"限流提额"页提升临时 TPM（有效期 30 天，目前仅北京与新加坡支持）。

限流仅约束速率，不限制累计用量。要控制费用：在账单费用卡片设置月度消费限额与告警；对新用户免费额度模型开启"免费额度用完即停"；定期查看模型监控（调用数据约一小时后更新，高峰期可能延迟）。

## 计费要点

开通百炼免费，调用、微调、部署模型时产生费用，按分钟出账。新用户在华北2（北京）地域有专属免费额度：未认证用户用完即停、需认证充值后续费；已认证用户用完自动转按量付费，可开启"免费额度用完即停"避免意外扣费。Coding Plan 为固定月费套餐，需使用其专属 Base URL 与 API Key，否则按量付费。

## 关键注意事项

- Base URL 与 API Key 必须属同一计费方案，错配报 401；API Key 不能跨地域使用。
- 业务空间专属域名仅限该空间 API Key 调用；Dashscope 与试用域名可跨业务空间调用。
- 模型调用统计约一小时后才在模型监控可见。
- 删除 API Key、停止调用、下线按算力计费的部署实例、开启免费额度用完即停，是控制费用的有效组合。
- 模型名称带日期的快照版本限流比稳定版/最新版更严格，生产环境优先用不带日期的稳定名称。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)




# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问全系列模型与 DeepSeek、Kimi、GLM 等第三方模型，并提供兼容 OpenAI / Anthropic / DashScope 三套接口。本主题汇总了首次接入百炼模型必须了解的四类信息：可用模型矩阵、API 调用方式、地域与服务部署范围选择、限流规则。

## 平台能力与可用模型

百炼的模型服务覆盖文本、视觉、图像/视频生成、语音合成与识别、向量与重排序、3D 模型生成等多种模态。从能力最强到成本最低，千问主力按 Max / Plus / Flash 三档划分：

- **qwen3.7-max**：旗舰推理模型，复杂多步骤任务首选。
- **qwen3.7-plus** / **qwen3.6-plus**：效果、速度、成本均衡，多数业务场景的**推荐选择**。
- **qwen3.6-flash** / **qwen-flash**：高 RPM、低延迟，适合简单任务和高吞吐场景。

第三方模型与千问共用同一套 API 规范，可零成本切换，包括 `deepseek-v4-pro` / `deepseek-v4-flash` / `kimi-k2.6` / `glm-5.1` / `MiniMax-M2.7` 等。完整模型矩阵（含视觉、音频、向量、3D）参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。平台整体定位与可视化应用能力参见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 调用模型：API 接入方式

百炼支持三种 API 协议，均以 API Key 鉴权：

| 协议 | 典型 Base URL（以北京为例） |
| --- | --- |
| OpenAI 兼容 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Anthropic 兼容 | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 原生 DashScope | `https://dashscope.aliyuncs.com/api/v1` |

接入要点：

1. **注册并开通百炼**：使用阿里云主账号登录控制台后会自动开通；新加坡与法兰克福地域调用时还需填入[业务空间](../concepts/workspace.md) ID（WorkspaceId）。
2. **获取 API Key**：在控制台 API Key 页面创建，建议通过环境变量 `DASHSCOPE_API_KEY` 注入，避免硬编码到代码里。
3. **安装 SDK**：Python ≥ 3.8，可选 `pip install -U openai` 或 `pip install -U dashscope`；Node.js 直接使用 `openai` 包；任意语言也可走 `curl`。
4. **发起首个请求**：把 `api_key` 设为环境变量、`base_url` 指向所选地域、`model` 设为 `qwen-plus` 等模型 ID 即可。

完整的环境变量配置（Linux / macOS / Windows）、SDK 安装与代码示例参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

> **注意**：示例文档中出现的 `qwen3.6-plus` 等版本号属于动态可用模型列表，**以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 与控制台模型广场为准**；通用稳定别名（`qwen-max` / `qwen-plus` / `qwen-flash` / `qwen-turbo`）始终指向最新可用版本，更适合生产长期使用。

## 地域与服务部署范围

百炼把"接入地域"和"推理执行位置"拆成了两个独立维度：

- **地域**决定 Base URL、API Key、静态数据存储位置。
- **服务部署范围**决定推理计算实际发生的地理边界。

四个地域与可选部署范围如下（API Key 与模型列表均不能跨地域混用）：

| 地域 | 可选服务部署范围 | 适用场景 |
| --- | --- | --- |
| 华北2（北京） | 中国内地 | 数据不出中国内地 |
| 新加坡 | 国际（不含中国内地） | 数据不经过中国内地 |
| 美国（弗吉尼亚） | 全球 / 美国 | 全球资源池或数据不出美国 |
| 德国（法兰克福） | 全球 / 欧盟 | 全球资源池或数据不出欧盟 |

地域间功能也存在差异，例如**批量推理、模型告警、模型调优只在北京和（部分）新加坡支持**，弗吉尼亚与法兰克福不支持。在美国地域使用 `-us` 后缀模型名（如 `qwen-plus-us`）可强制限定美国境内推理；不带后缀走全球部署范围。完整的接入信息、Base URL 列表与功能矩阵参见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

> **注意**：新加坡旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到新版 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。新加坡与法兰克福的 Base URL 中 `{WorkspaceId}` 必须替换为真实[业务空间](../concepts/workspace.md) ID，否则调用会失败。

## 限流：RPM / TPM 与避免策略

限流按**主账号维度**聚合（账号下所有 RAM 子账号、[业务空间](../concepts/workspace.md)、API Key 共享额度），按**模型独立**计算。每个模型同时受 RPM（每分钟请求数）与 TPM（每分钟 Token 数）双限制，超出任一阈值即触发。

**常见报错与对应策略**：

| 报错关键字 | 触发原因 | 处理 |
| --- | --- | --- |
| `Requests rate limit exceeded` / `exceeded your current requests list` | RPM 超限 | 降低调用频率 |
| `Allocated quota exceeded` / `exceeded your current quota` | TPM 超限 | 缩短输入或限制输出长度 |
| `Request rate increased too quickly` | 短时请求爆发触发稳定性保护 | 匀速调度、指数退避、请求队列 |

**额度参考**（中国内地，节选）：

- `qwen3.7-max` / `qwen3.7-plus` / `qwen3.6-plus` / `qwen-plus`：30,000 RPM、5,000,000 TPM。
- `qwen3.6-flash` / `qwen-flash`：30,000 RPM、10,000,000 TPM。
- 带具体日期的快照版本（如 `qwen-plus-2025-09-11`）：默认 60–600 RPM，远低于稳定别名。

**降低限流风险的工程做法**：

1. 优先使用 `qwen-plus` 等稳定别名而非快照版本，前者限流额度高一个数量级。
2. 实现备用模型兜底——主模型 429 时自动切换到备份模型重试。
3. 离线/非实时场景改用 [Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，不受实时限流约束（`qwen-max` / `qwen-plus` / `qwen-turbo` 等显式支持）。
4. 默认额度不足时，在控制台**限流提额**页面提交临时 TPM 提额（30 天有效，仅北京与新加坡）。

完整 RPM/TPM 表格（按部署范围细分中国内地、全球、国际、美国、欧盟，覆盖语言、VL、Omni 等系列）参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 接入清单

按以下顺序操作即可完成首次接入：

1. 登录阿里云控制台，开通百炼并完成实名认证。
2. 根据数据合规与延迟需求，按 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 表格挑选地域与部署范围。
3. 在所选地域创建 API Key，并把 `DASHSCOPE_API_KEY` 写入本机环境变量。
4. 按 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 选择 OpenAI 兼容 / DashScope SDK，发起首个 `chat.completions` 请求。
5. 通过 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 确认目标模型 ID，并核对 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 中的 RPM / TPM 额度是否满足业务峰值。
6. 调用一小时后在控制台**模型监控**页面查看调用量、Token 消耗、成功率等统计数据。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)





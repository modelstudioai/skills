# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问及主流第三方模型，提供兼容 OpenAI 的 API 和全链路模型服务。开发者只需获取 API Key、选择地域并配置 Base URL，即可通过几行代码调用大模型完成文本生成、多模态理解等任务。

本文汇总从开通账号、选择模型、配置地域到首次调用与限流控制的完整入门路径，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 与 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 一、支持的能力与模型

百炼提供开箱即用的模型服务，无需自行部署，覆盖以下模态（详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）：

- **文本生成**：千问系列旗舰模型按"能力-成本"梯度划分
  - `qwen3.7-max`：Qwen 系列效果最强，适合复杂、多步骤任务
  - `qwen3.7-plus` / `qwen-plus`：效果、速度与成本均衡，多数场景的推荐选择
  - `qwen3.6-flash` / `qwen-flash`：高性价比、低延迟，适合快速响应的简单任务
- **第三方模型**：`deepseek-v4-pro`、`deepseek-v4-flash`、`kimi-k2.7-code`、`glm-5.2`、`MiniMax-M2.7`、`mimo-v2.5-pro`，API 格式与千问一致
- **多模态**：视觉理解（`qwen3.7-plus`、`qwen3.5-omni-plus`）、图像/视频生成（`wan2.7-image-pro`、`happyhorse-1.1-*`）、3D 模型生成（`Tripo-H3.1`）
- **音频与语音**：语音合成 `cosyvoice-v3.5-plus`、语音识别 `fun-asr-realtime`、端到端语音对话 `qwen3.5-omni-plus-realtime`、音乐生成 `fun-music-v1`
- **全模态**：`qwen3.5-omni-plus` 系列融合文本、图像、音频、视频的理解与生成
- **向量与重排序**：`text-embedding-v4`、`tongyi-embedding-vision-plus`、`qwen3-rerank`

除调用预置模型外，百炼还支持模型调优（SFT/CPT/DPO）、专属部署与评测。完整模型列表可前往控制台 [模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 查看。

## 二、选择地域与服务部署范围

调用前需选定**地域**和**服务部署范围**，二者职责不同（详见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)）：

- **地域**决定接入点和数据存储位置，就近选择可降低延迟；
- **服务部署范围**决定推理执行位置，有数据合规需求选限境内推理，无合规需求选全球部署可获得更大推理资源池。

可用地域：华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）。每个地域有独立的 Base URL、API Key 和模型列表，**不能跨地域混用**。

各地域功能支持差异：

| 功能 | 北京 | 新加坡 | 弗吉尼亚 | 法兰克福 | 东京 |
| --- | --- | --- | --- | --- | --- |
| 实时推理 | 支持 | 支持 | 支持 | 支持 | 支持 |
| 批量推理 | 支持 | 支持 | 不支持 | 不支持 | 不支持 |
| 模型调优 | 支持 | 不支持 | 不支持 | 不支持 | 不支持 |
| 模型告警 | 支持 | 支持 | 不支持 | 不支持 | 不支持 |

> **注意**：法兰克福与东京通过[业务空间](../concepts/workspace.md)（Workspace）区分全球/欧盟或全球/日本部署范围，不同空间的 API Key 相互隔离；弗吉尼亚用带 `-us` 后缀的模型名（如 `qwen-plus-us`）限定美国境内推理，不带后缀默认全球推理。

## 三、Base URL 与接入信息

百炼为北京、新加坡推出新版专属域名 `{WorkspaceId}.{region}.maas.aliyuncs.com`，性能与稳定性更优，建议迁移。各地域 OpenAI 兼容 Base URL：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`
- **日本（东京）**：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

`{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在控制台[业务空间](../concepts/workspace.md)管理页面获取。除 OpenAI 兼容协议外，各地域也提供 Anthropic 兼容（`/apps/anthropic`）与 DashScope（`/api/v1`）Base URL。

## 四、首次调用流程

1. **注册并开通**：使用阿里云主账号前往百炼控制台开通服务，需完成实名认证。
2. **获取 API Key**：在 API Key 页面创建，建议配置到环境变量 `DASHSCOPE_API_KEY` 避免硬编码。
3. **获取业务空间 ID**：使用北京、新加坡、法兰克福、东京地域时需在 Base URL 中填入 WorkspaceId。
4. **安装 SDK**：`pip install -U openai` 或 `pip install -U dashscope`（Python 3.8+）。
5. **发起请求**：参考下方示例。

OpenAI Python SDK 示例（北京地域）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

curl 示例：

```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{"model": "qwen-plus", "messages": [{"role": "user", "content": "你是谁？"}]}'
```

> **注意**：百炼兼容 OpenAI 接口规范，现有 OpenAI 代码只需调整 `api_key`、`base_url` 和 `model` 即可迁移。

## 五、限流与用量控制

百炼按主账号维度限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算，不同模型限流额度相互独立（详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）。

**限流类型与错误信息**：

- `Requests rate limit exceeded`：每分钟请求数（RPM）超限
- `Allocated quota exceeded`：每分钟 Token 消耗（TPM）超限
- `Request rate increased too quickly`：短时请求激增触发稳定性保护

除 RPM/TPM 外，服务可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行限流，瞬时高峰即使分钟总量未超限也可能被拒。触发限流后通常一分钟内自动恢复。

**避免限流与控制费用的措施**：

1. 优先使用 `qwen-plus` 等高限流模型，稳定版比日期快照版额度更宽松。
2. 收到 RPM 限流时降低调用频率；收到 TPM 限流时缩短输入或限制输出长度；收到激增告警时采用匀速调度或指数退避。
3. 添加备选模型：主模型触发 429 后自动切换备用模型重试。
4. 非实时任务使用批量推理（Batch API），不受实时限流约束。
5. 默认额度不足时在控制台限流提额页面提升临时 TPM，提交后立即生效，有效期 30 天（仅北京、新加坡支持）。
6. 控制累计费用：设置月度消费限额与费用告警，新用户可开启"免费额度用完即停"（仅北京地域）。

模型调用统计在调用完成后约 1 小时可查，路径为控制台模型监控页面 → 选择地域与查询条件 → 目标模型操作列点击"监控"。

## 六、计费要点

开通百炼免费，调用、微调、部署模型时产生费用，按分钟出账。新用户可享北京地域免费额度：未认证用户额度用完需完成认证并充值才能继续；已认证用户用完后自动转按量付费。订阅 Coding Plan（AI 编码套餐）可获固定月费的月度请求额度，但需使用专属 Base URL 和 API Key 调用，否则按量计费。

数据安全方面，百炼不会将用户数据用于模型训练，传输全程加密。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)



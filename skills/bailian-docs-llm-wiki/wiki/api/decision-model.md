# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），专为高频、低延迟的确定性判断任务设计。它不生成文本，而是对输入 `state` 一次性返回多个问题的分类结果、是非概率或有序评分及其置信度与完整概率分布，适用于工单分流、内容审核、Agent 路由、任务完成度校验等场景。其接口协议遵循 TypeSafe System One 标准，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`，无其他变体或版本别名。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中选项、各选项概率及置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望分数（可为浮点数，如 `2.43`）、各级概率、等级描述映射（`legend`）及置信度。
- 单次请求最多支持 **16 个问题**，所有问题并行计算，不生成 token，因此延迟与输出长度无关。

## 关键参数

| 参数 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | ✓ | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | Body | ✓ | 待决策的原始业务数据（如工单文本、对话 JSON 或结构化对象）；对象会被序列化后送入模型 |
| `questions` | `Object` | Body | ✓ | 键为自定义 question ID，值为问题对象；每个问题必须指定 `type`（`choice`/`noul`/`score`）及对应 `criteria`（见下表） |
| `Authorization` | `String` | Header | ✓ | `Bearer $DASHSCOPE_API_KEY`，API Key 配置方式参见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) |
| `Content-Type` | `String` | Header | ✓ | 必须为 `"application/json"` |

`questions` 中各类型 `criteria` 要求：
- `choice`：`criteria` 为 `{"option_key": "description"}` 映射，选项数 1–255，**强烈建议包含 `"other"` 兜底项**；
- `noul`：`criteria` 可省略；若提供，应为 `{"true": "...", "false": "..."}` 形式（但模型实际仅用 `instructions` 推理，`criteria` 不影响输出）；
- `score`：`criteria` 为字符串数组（如 `["低", "中", "高"]`），长度 2–255，**推荐 3–7 级且语义可明确区分**。

> **注意**：原始文档中 `noul` 的 `criteria` 字段说明存在冗余——[决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确指出该字段“可选”，且模型推理仅依赖 `instructions`；若在 SDK 中误传 `criteria` 可能被静默忽略，建议保持为空或完全省略。

## 使用方式

### SDK 调用（推荐）
- **Python**：需 DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法。旧版本无 `decision` 接口，调用将报 `AttributeError`。安装命令：`pip install -U "dashscope>=2.0.1"`（参见 [安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md)）。
- **Java**：需 DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包。Maven 坐标：`com.alibaba:dashscope-sdk-java:2.23.3`。
- SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。

### 通用 TypeSafe SDK
- 安装 `typesafe-sdk`（`pip install typesafe-sdk`），设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one()`。
- 此方式兼容所有支持 TypeSafe 协议的客户端，适合非官方 SDK 用户。

### curl 直连
- 直接 POST 至 `{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`，需手动替换 `{WorkspaceId}` 和地域域名（参见 [地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。完整示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **上下文长度**：最大 `65536` token，超长 `state` 将被服务端拒绝（HTTP 400）。
- **问题数量**：单请求上限 16 个问题；延迟随问题数近线性增长，建议按业务必要性精简。
- **选项与等级数**：
  - `choice` 选项 ≤ 255；
  - `score` 等级数 2–255，但**超过 7 级易导致语义模糊、置信度下降**，生产环境应严格控制在 3–7 级。
- **错误处理**：
  - Python SDK 抛出 `DashScopeError`，Java SDK 抛出 `ApiException`；
  - 全部错误码及排查指引见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。
- **在线调试**：强烈建议先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 体验预设场景（客服判断、Agent 完成度核验等），验证逻辑后再集成代码——该能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中有详细说明。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)



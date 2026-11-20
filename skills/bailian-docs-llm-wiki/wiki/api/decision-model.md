# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），专为高频、低延迟的确定性判断任务设计。它不生成文本，而是对输入 `state` 一次性返回多个维度的结构化判定结果（分类、是非、评分）及其概率分布与置信度，适用于工单分流、内容审核、智能体路由、任务完成度校验等场景。其接口协议基于 TypeSafe System One，与通用大模型调用范式分离，强调确定性输出与可计量性。

## 支持的模型/功能

- 当前唯一支持的模型为 `decision-model-preview`，属于预览版，[原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确指出该模型“不生成文本”，仅输出结构化决策。
- 支持三类问题类型：
  - `choice`：多选一分类（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（浮点数，范围 [0,1]）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数）、各级概率及置信度。
- 单次请求最多支持 **16 个问题**，且可混合使用不同类型，实现多维联合决策。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | ✓ | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | ✓ | 待决策的原始业务数据（如工单文本、对话 JSON 或结构化对象），会被序列化后送入模型 |
| `questions` | Body | `Object` | ✓ | 键为自定义 question ID，值为问题对象；其中 `type`（`choice`/`noul`/`score`）必填，`criteria` 格式依类型而异（详见[原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md)） |
| `Authorization` | Header | `String` | ✓ | `Bearer $DASHSCOPE_API_KEY`，API Key 需配置为环境变量或显式传入 |
| `Content-Type` | Header | `String` | ✓ | 必须为 `"application/json"` |

> **注意**：`state` 超过 65536 token 将被拒绝；`choice` 选项数上限 255，`score` 等级数建议 3–7 级（2–255 级合法），详见[原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：需 DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法；
  - Java：需 DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包；
  - SDK 自动拼接 `/compatible-mode/v1/systemone` 端点，并根据 `workspace` 和 `region` 构造完整 URL。
- **TypeSafe SDK 调用**：使用 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one()`。
- **curl 直连**：直接 POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`，需手动构造请求头与 JSON body。

所有方式均遵循统一的请求/响应 Schema，返回包含 `answers`（按 question ID 组织的答案对象）、`usage`（token 数）、`latency_ms`（毫秒级延迟）等字段。

## 限制和注意事项

- **性能限制**：问题数上限 16，延迟随问题数近线性增长；上下文长度硬上限 65536 token。
- **模型状态**：`decision-model-preview` 为预览版，接口与能力可能调整，正式 GA 前请关注变更公告。
- **SDK 版本强依赖**：旧版 DashScope SDK 不支持 `decision` 接口，Python <2.0.1 会抛 `AttributeError`，Java <2.23.3 缺失 `com.alibaba.dashscope.decision` 包 —— 此处与部分历史文档中提及的“通用模型兼容调用”存在矛盾，[原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确要求版本号，应以该文档为准。
- **错误处理**：失败时 Python SDK 抛 `DashScopeError`，Java SDK 抛 `ApiException`；完整错误码见 [错误信息](raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)



# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级前向推理模型，一次调用可并行完成多类判断（分类、是非、评分），返回概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高确定性要求的场景。其协议基于 TypeSafe System One，与通用大模型 API 接口分离，避免文本生成开销。

## 支持的模型/功能

- 当前唯一支持的模型为 `decision-model-preview`，无其他变体或版本别名。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中项、各选项概率及置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（浮点数，范围 [0,1]）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数）及各等级概率。
- 所有判定均基于输入 `state` 的语义理解，不依赖历史对话或上下文记忆。

> **注意**：文档中提及的 Playground 预设场景（如“Agent 完成度核验”“医疗导诊辅助”）仅为演示用途，其底层逻辑仍由同一 `decision-model-preview` 模型统一支撑，[原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md)未定义独立子模型或领域微调版本。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | 是 | 待决策的原始业务数据（如工单文本、JSON 对象），会被序列化后送入模型 |
| `questions` | Body | `Object` | 是 | 键为问题 ID，值为问题对象；每个问题对象含 `type`（`choice`/`noul`/`score`）、`instructions`（可选描述）、`criteria`（按类型结构不同） |
| `Authorization` | Header | `String` | 是 | `Bearer $DASHSCOPE_API_KEY`，API Key 须已配置为环境变量或显式传入 |
| `Content-Type` | Header | `String` | 是 | 固定为 `"application/json"` |

- `choice` 的 `criteria` 为 `{"option_key": "description"}` 映射，建议补全 `other` 兜底项；
- `score` 的 `criteria` 为字符串数组（如 `["轻微", "中等", "严重"]`），索引即等级序号；
- 单次请求最多支持 **16 个问题**，`choice` 选项上限 255，`score` 等级数建议 3–7 级（2–255 合法）；
- 输入 `state` 上下文长度上限为 **65536 token**，超长将被拒绝，详见 [原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

### SDK 调用（推荐）

- **Python**：需 DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法：
  ```python
  result = client.decision.create(
      model="decision-model-preview",
      state={"ticket_id": "T-1001", "content": "..."},
      questions={
          "department": {"type": "choice", "criteria": {"billing": "..."}},
          "escalate": {"type": "noul"},
          "severity": {"type": "score", "criteria": ["...", "..."]}
      }
  )
  print(result.answers["department"].choice)  # 获取选中项
  ```
- **Java**：需 DashScope SDK ≥ `2.23.3`，使用 `DecisionModel.call()`，详见 [原文标题](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的 Java 示例。

### 通用 HTTP 调用

- Endpoint：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`
- 地域支持：华北2（北京）、新加坡等，域名格式见文档；
- 可配合 `typesafe-sdk` 使用，`base_url` 指向 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode` 即可自动拼接路径。

### 在线调试

- 建议先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 快速验证逻辑与输出格式，选择预设场景输入样例观察概率分布变化。

## 限制和注意事项

- **无文本生成能力**：该模型严格返回结构化答案（`choice`/`noul`/`score`），不支持 `messages`、`system_prompt` 或流式响应，与通用大模型 API 行为本质不同。
- **延迟与问题数强相关**：16 个问题时延迟近似线性增长，生产环境建议按业务优先级聚合问题，避免单次请求满载。
- **`state` 序列化行为**：当 `state` 为 `Object` 或 `Array` 时，SDK 会 JSON 序列化后送入模型，确保字段语义清晰、无嵌套过深或二进制数据。
- **错误处理**：调用失败时 Python SDK 抛 `DashScopeError`，Java SDK 抛 `ApiException`；具体错误码含义参见 [错误信息](raw/model-api-reference/preparations/error-code.md)，该文档与本模型兼容。
- **版本强约束**：旧版 SDK（Python <2.0.1 / Java <2.23.3）**不支持** `decision` 接口，调用将报 `AttributeError` 或 `ClassNotFoundException`，务必升级。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)



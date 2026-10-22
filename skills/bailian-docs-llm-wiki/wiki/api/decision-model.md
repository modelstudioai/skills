# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、任务完成度校验等低延迟、高确定性要求的场景。其核心能力基于 TypeSafe System One 协议实现，一次前向计算即可并发响应多个异构问题 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题：
  - `choice`：多选一判定（如「派单团队」），返回选中选项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 `P(yes)` 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有类型均**不生成任何文本输出**，响应延迟与输出长度无关，仅取决于输入 token 数与问题数量 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | ✅ | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | ✅ | 待决策的业务上下文；结构化对象将被序列化后送入模型 |
| `questions` | `Object` | ✅ | 键为自定义问题 ID，值为问题对象；单次最多 16 个问题 |
| `questions.*.type` | `String` | ✅ | 取值 `"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | `String` | ❌ | 问题语义描述或评判标准，影响判断准确性 |
| `questions.*.criteria` | `Object` / `Array` | ⚠️ 条件必填 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（2–255 级，**强烈建议 3–7 级**） |

> **注意**：文档中明确要求 `score` 等级数范围为 2–255，但实践表明超过 7 级时概率分布易趋平、置信度显著下降；该限制在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中已标注为“建议”，开发者应优先遵循 3–7 级设计原则。

## 使用方式

1. **环境准备**：配置 `DASHSCOPE_API_KEY` 环境变量（参考 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）；
2. **选择 Endpoint**：根据地域替换 `{WorkspaceId}`，例如华北2（北京）使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`；
3. **构造请求体**：确保 `state` 合理表达业务状态，`questions` 中每个问题明确定义 `type` 和 `criteria`（若适用）；
4. **推荐 SDK 调用**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 base_url 拼接与响应解析：

```python
from typesafe_sdk import TypeSafeClient
client = TypeSafeClient(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
)
result = client.system_one(
    model="decision-model-preview",
    state={"ticket_id": "T-1001", "content": "..."},
    questions={...}
)
print(result.answers["department"]["choice"])  # 直接取结构化结果
```

在线调试推荐使用 [Playground](https://bailian.console.aliyun.com/systemone_playground)，支持预设场景快速验证逻辑 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被拒绝（无截断）；
- **问题数量**：单次请求最多 16 个问题；延迟随问题数近似线性增长；
- **选项/等级上限**：`choice` 选项 ≤ 255；`score` 等级 2–255（但 3–7 级为最佳实践）；
- **无流式响应**：仅支持同步一次性返回，不支持 `stream=true`；
- **错误排查**：失败时返回标准错误码，详细说明见 [错误信息](raw/model-api-reference/preparations/error-code.md)（注意该路径为 raw 下相对引用，实际渲染由系统处理）；
- **模型状态**：`decision-model-preview` 为预览模型，接口与行为可能随版本迭代调整，请关注控制台公告。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)



# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发的确定性决策场景。其核心能力基于一次前向计算完成多问题联合推理，响应延迟与输出长度无关，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题：
  - `choice`：多选一决策（如「派单团队」），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断（如「是否需升级」），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如「严重度 1–4 级」），返回加权期望分（可为浮点数，如 `2.25`）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或集成贝叶斯校准。详细接口能力说明请参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | ✓ | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | ✓ | 待决策的原始上下文，支持文本、JSON 对象或数组；对象将被序列化后送入模型 |
| `questions` | Body | `Object` | ✓ | 键为自定义 question_id，值为问题定义对象，含 `type`、`instructions`、`criteria`（按类型可选） |
| `type` | `questions.*` | `String` | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `questions.*` | `Object` 或 `Array` | 条件必填 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（2–255 级，**建议 3–7 级**） |

> **注意**：文档中 `score` 等级数上限标注为“2–255”，但实际推荐范围明确为“3–7 级且每级可清晰区分”；若使用超 7 级（如 10 级），可能导致判别粒度退化，影响 `confidence` 和 `probabilities` 的可靠性。该建议在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中多次强调，应优先遵循。

## 使用方式

1. **认证准备**：确保环境变量 `DASHSCOPE_API_KEY` 已配置，格式为 `Bearer <your_key>`。
2. **选择 Endpoint**：根据地域替换 `{WorkspaceId}`，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`。
3. **构造请求体**：`state` 传入业务上下文，`questions` 定义多个问题（建议 ≤16 个，避免延迟线性增长）。
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

完整示例与 curl 调用方式见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被拒绝或截断，建议预处理压缩关键信息。
- **问题规模**：
  - 单次请求 `questions` 数量无硬上限，但 ≥16 时延迟近似线性增长；
  - `choice` 选项数 ≤255，`score` 等级数 2–255（强烈建议 3–7 级）；
- **输出特性**：**不生成任何文本**，仅返回结构化答案（`choice`/`noul`/`score` + `probabilities` + `confidence`），因此成本与延迟恒定，与输出长度无关。
- **错误排查**：失败时返回标准错误码，具体含义请查阅 [错误信息](../../raw/model-api-reference/preparations/error-code.md) —— 注意该文档路径已在原始文档中引用，需同步维护一致性。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)



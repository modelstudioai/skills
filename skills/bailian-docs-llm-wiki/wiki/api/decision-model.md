# decision model

决策模型（`decision-model-preview`）是百炼平台专为结构化决策场景设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体任务路由、结果校验等低延迟、高确定性要求的业务场景。其接口协议基于 TypeSafe System One，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），无其他变体或版本别名。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中项、各选项概率及置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断，返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如严重度 1–4 级），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有问题在单次请求中并行处理，输出严格结构化，无 token 生成开销，延迟与输出长度无关。该设计特性在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确强调。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | 是 | 待决策的原始业务上下文；对象将被序列化后送入模型 |
| `questions` | object | 是 | 键为问题 ID，值为问题定义对象，含 `type`、`instructions` 和 `criteria`（按类型可选/必填） |
| `type` | string | 是 | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | object / array | 视 `type` 而定 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 描述数组（2–255 级，**建议 3–7 级**） |

> **注意**：文档中 `score` 等级上限标注为“2–255”，但实际推荐范围为“3–7 级且每级可清晰区分”——若使用超 10 级，可能导致概率分布弥散、置信度下降，此限制在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“接口限制与建议”章节中有明确提示。

## 使用方式

1. **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 头传递 API Key（需提前配置环境变量）；
2. **Endpoint**：按地域选择对应域名，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`；
3. **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析；
4. **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验，验证问题定义与结果合理性。

示例（Python）：
```python
from typesafe_sdk import TypeSafeClient
client = TypeSafeClient(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
)
result = client.system_one(
    model="decision-model-preview",
    state={"ticket_id": "T-1001", "content": "..."},
    questions={
        "department": {"type": "choice", "criteria": {"billing": "...", "technical": "..."}},
        "escalate": {"type": "noul"},
        "severity": {"type": "score", "criteria": ["...", "...", "..."]}
    }
)
print(result.answers["department"]["choice"])  # e.g., "billing"
```

## 限制和注意事项

- **上下文长度**：最大支持 65536 token；超长 `state` 将被拒绝或截断；
- **问题规模**：单请求 `questions` 数量无硬上限，但**建议 ≤ 16 个**，延迟随问题数近线性增长；
- **选项与等级**：`choice` 选项数 ≤ 255；`score` 等级数建议 3–7 级（非强制但影响效果）；
- **无流式响应**：仅支持同步阻塞调用，不支持 `stream=true`；
- **错误排查**：失败时返回标准错误码，详细说明见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)（注意该文档路径为相对引用，需确保 wiki 构建时路径解析正确）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)



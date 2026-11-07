# decision model

决策模型是百炼平台提供的专用推理服务，基于 System One 协议设计，支持单次前向调用同步返回结构化决策结果（包括分类标签、置信度评分、是非判断及对应概率分布）。该模型适用于风控审核、内容合规判定、策略路由等需明确输出逻辑结论的场景。其接口契约与行为规范详见 [决策模型 (raw/model-api-reference/decision-model.md)](../../raw/model-api-reference/decision-model.md)。

## 支持的模型/功能

- 当前公开可用的决策模型为 `decision-model-preview`，已在模型中心上线，支持文本输入与结构化 JSON 输出。
- 功能上严格遵循 System One 协议：一次请求必须返回 `label`（字符串分类）、`score`（浮点型综合置信分，范围 0.0–1.0）、`is_true`（布尔型是非判断）及可选的 `probabilities`（各候选类别的归一化概率分布）。
- 模型不支持流式响应、多轮对话或 token 级生成，仅接受单次 stateless 请求。详细能力边界参见 [decision-model-preview 模型信息](../../raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-decision/decision-model-preview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | string | 是 | 待决策的原始文本，最大长度 8192 字符（超长将被截断且不报错） |
| `labels` | array of string | 否 | 显式声明候选分类集合（如 `["approved", "rejected", "pending"]`），若未提供则使用模型内置默认集；**注意：若传入空数组或非字符串元素，将导致 400 错误** |
| `threshold` | number | 否 | `score` 的最小阈值（默认 0.5），低于此值时 `is_true` 强制为 `false`，且 `label` 可能回退至 `"unknown"` |

> **注意**：`labels` 参数在 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 中定义为“推荐提供”，但实测中若完全省略且输入语义模糊，部分批次返回 `label: "unknown"` 的比例显著升高——建议始终显式传入业务相关标签集以保障稳定性。

## 使用方式

1. 在 Model Studio 中选择 `decision-model-preview`，确认配额与地域可用性；
2. 构造 HTTP POST 请求，`Content-Type: application/json`，Body 示例：
   ```json
   {
     "input": "该用户近30天有5次逾期记录。",
     "labels": ["high_risk", "medium_risk", "low_risk"],
     "threshold": 0.65
   }
   ```
3. 解析响应中的 `label`、`score`、`is_true` 字段进行业务分支处理；`probabilities` 仅在 `labels` 非空时返回。

完整请求/响应示例与错误码说明请查阅 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- 上下文窗口固定为 8192 tokens（按字节计数，非 Unicode 字符），超长输入将静默截断，**不会触发 `context_length_exceeded` 错误**；
- 不支持 `system` 或 `user` 角色指令注入，`input` 字段即唯一有效输入源；
- 模型不支持微调、私有部署或权重导出，所有推理均通过百炼统一 API 网关完成；
- 计费按成功调用次数计费（含 `is_true=false` 的合法响应），失败请求（如 4xx/5xx）不计费；
- 当前 `decision-model-preview` 仍处于预览阶段，接口字段与默认行为可能随版本迭代调整，请定期同步 [decision-model-preview 模型信息](../../raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-decision/decision-model-preview.md) 中的变更日志。

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)



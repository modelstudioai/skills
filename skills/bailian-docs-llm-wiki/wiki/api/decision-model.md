# decision model

决策模型是百炼平台提供的专用推理服务，基于 System One 协议设计，支持单次前向调用同步返回结构化决策结果（包括分类标签、置信度评分、是非判断及概率分布）。该模型适用于风控审核、内容合规判定、策略路由等需明确输出逻辑结论的场景。其接口语义清晰、响应格式标准化，便于集成到自动化决策流水线中。

## 支持的模型/功能

- 当前公开可用的决策模型为 `decision-model-preview`，提供多类别分类、二元是非判断、细粒度置信度打分三类核心能力 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)  
- 所有功能均通过统一的 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 接口暴露，不区分独立 endpoint，调用时无需指定子任务类型  
- 输出包含 `label`（预测类别）、`score`（0–1 区间归一化得分）、`is_true`（布尔型是非判断）、`probabilities`（各候选类别的原始概率）和 `confidence`（整体置信度标量）字段  

## 关键参数

- `input`：必填，字符串或字符串数组，最大长度受模型上下文限制（详见 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)）  
- `top_k`：可选，控制返回概率分布的类别数量，默认为全部候选类  
- `threshold`：可选，用于过滤低置信度结果（仅影响 `probabilities` 中低于阈值的项是否保留），默认无过滤  
- `system_prompt`：不支持自定义 system prompt；模型行为由预置决策逻辑固化，此参数被忽略（与通用大模型 API 行为不同）

## 使用方式

1. 通过百炼控制台「Model Studio」获取 `decision-model-preview` 的模型 ID（如 `decision-model-preview-202406`）  
2. 调用 `/v1/models/{model_id}:predict` 接口，HTTP 方法为 `POST`，请求体为 JSON 格式，示例：
   ```json
   {
     "input": "该用户近7天存在3次异常登录行为",
     "top_k": 3
   }
   ```
3. 解析响应中的 `label` 和 `confidence` 字段作为主决策依据；`is_true` 字段直接对应“是否符合策略”的布尔结论  

## 限制和注意事项

- 输入文本长度上限为 8192 token（具体以 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 公布为准），超长截断不报错但影响判断质量  
- 不支持流式响应（`stream: true` 参数无效），所有结果必须等待完整前向计算完成  
- > **注意**：原始文档中提到“通过 System One 协议一次前向返回”，但实际 API 文档 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确要求使用标准 REST over HTTP 调用，不存在独立的 System One 传输层；此处“System One”应理解为协议语义规范（即单次请求/响应承载完整决策结构），而非网络协议实现。  
- 模型不支持微调或私有部署，仅限百炼托管实例调用

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)



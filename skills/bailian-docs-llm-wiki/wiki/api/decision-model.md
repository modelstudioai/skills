# decision model

决策模型是百炼平台提供的专用模型类型，基于 System One 协议设计，支持单次前向推理同步返回分类结果、数值评分、是非判断（yes/no）及其对应的概率分布与置信度。该模型适用于风控审核、内容合规判定、策略规则引擎等需结构化决策输出的场景。其接口语义明确，无需后处理即可直接集成至业务逻辑。

## 支持的模型/功能

- 当前公开可用的决策模型包括 `decision-model-preview`，提供基础分类（多类/二类）、连续评分（0–100）、布尔判断（yes/no）三类结构化输出 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)  
- 所有决策模型均遵循统一的 System One 协议规范，确保输出字段（如 `classification`, `score`, `judgment`, `confidence`）格式一致，便于自动化解析 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)  
- 不支持文本生成、多轮对话或非结构化输出；若需扩展能力，应评估是否适用 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 中定义的 `output_schema` 自定义字段机制

## 关键参数

- `input`: 必填，字符串或结构化 JSON（如含 `text`, `metadata` 字段），具体格式见 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 的输入示例  
- `temperature`: 仅影响置信度计算路径，取值范围 `[0.0, 1.0]`；设为 `0.0` 时启用确定性推理（推荐生产环境使用）  
- `output_schema`: 可选，用于声明期望的输出结构（如仅需 `judgment` 和 `confidence`），未声明时返回全字段  

## 使用方式

1. 通过百炼控制台在 Model Studio 中部署 `decision-model-preview` 实例，或调用 `/v1/models/decision-model-preview:predict` 接口  
2. 构造符合 System One 协议的请求体，`messages` 字段中 `role: "user"` 的 `content` 应为待决策文本或结构化输入  
3. 解析响应中的 `choices[0].message.content`，其为标准 JSON 对象，包含 `classification`, `score`, `judgment`, `confidence` 等字段  

## 限制和注意事项

- 上下文长度上限为 8192 token，超长输入将被截断（非报错），建议预处理关键特征 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)  
- 不支持流式响应（`stream: true` 将被忽略），所有输出均为完整 JSON 一次性返回  
- > **注意**：原始文档中“通过 System One 协议一次前向返回……”的描述与当前实际接口路径 `/v1/models/decision-model-preview:predict` 存在协议命名歧义——System One 是内部通信协议抽象，对外暴露的是标准 REST+JSON 接口，开发者无需实现底层协议栈。

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)



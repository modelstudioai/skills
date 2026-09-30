# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理能力，用于在多轮对话中持久化存储和检索用户事实性信息、行为偏好与画像特征。它通过语义索引与向量检索实现低延迟、高相关性的记忆召回，支持开发者构建具备上下文连续性的智能体应用。该能力需配合支持记忆扩展的模型使用，并通过 API 显式控制写入与读取行为。

## 支持的模型/功能

当前仅以下模型支持[长期记忆](../concepts/memory.md)的完整读写能力：`qwen-max-20241017`、`qwen-plus-20241017` 及后续标注 `ltm_enabled: true` 的模型版本。基础模型（如 `qwen-turbo`）默认不启用记忆功能，即使传入 `memory` 参数也不会触发持久化或检索。记忆功能分为两类：**事实记忆（Fragments）** 用于存储离散、可验证的事实（如“用户生日是1992年5月3日”），**用户画像（Profiles）** 用于聚合推断型属性（如“偏好简洁回复”“常驻北京”）。详情见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)。

## 关键参数

- `memory.write`: 布尔值，设为 `true` 时触发本次请求结果写入记忆（仅对支持模型生效）  
- `memory.read`: 布尔值，设为 `true` 时在推理前自动注入相关记忆片段  
- `memory.fact_threshold` / `memory.profile_threshold`: 浮点数（0.0–1.0），控制检索相似度阈值，默认分别为 `0.65` 和 `0.72`  
- `memory.max_fragments` / `memory.max_profiles`: 整数，限制单次注入的最大片段数，默认均为 `5`  

> **注意**：`memory.read` 为 `true` 时，系统**不会**自动过滤过期或低置信度记忆；需在 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 中主动调用 `delete_by_id` 或设置 TTL 字段实现生命周期管理。

## 使用方式

1. 在请求 payload 中添加 `memory` 对象，例如：
   ```json
   {
     "model": "qwen-max-20241017",
     "input": { "messages": [...] },
     "parameters": {
       "memory": {
         "write": true,
         "read": true,
         "fact_threshold": 0.7
       }
     }
   }
   ```
2. 写入后，记忆将按语义自动分类至事实库或画像库，无需手动指定类型（系统基于内容结构与置信度自动判别）  
3. 如需精细控制，可直接调用 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 `/v1/memory/fragments` 或 `/v1/memory/profiles` 接口进行增删查改  

## 限制和注意事项

- 单个应用最多存储 100 万条事实记忆 + 10 万条用户画像，超出后写入失败并返回 `400 QuotaExceeded`  
- 记忆内容不可跨应用共享，即使用户 ID 相同；应用间隔离由 `app_id` 强约束  
- 所有记忆默认无 TTL，除非在写入时显式指定 `expires_at` 字段（ISO8601 格式）  
- 当前不支持在流式响应（`stream: true`）中实时注入记忆；必须使用同步模式完成写入闭环  
- 若发现模型返回 `memory.write: true` 但后续请求未召回对应内容，请确认是否误用了非支持模型——该问题已在 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档中明确警示。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)



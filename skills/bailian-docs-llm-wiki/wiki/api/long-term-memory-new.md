# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理能力，用于在多轮对话中持久化存储和检索用户事实性信息与画像特征。它通过分层抽象（事实记忆 + 用户画像）实现语义化存储，并支持开发者按需配置生命周期与访问策略。该能力当前仅面向 API 调用场景开放，不直接暴露于低代码界面。

## 支持的模型/功能

- **模型支持**：目前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生集成 LTM 检索与写入逻辑；其他模型调用时将忽略 `memory` 相关参数，不报错但无实际效果。  
- **核心功能**：  
  - **事实记忆（Fragments）**：以键值对形式存储可验证的客观事实（如“用户生日：1992-05-18”），支持模糊匹配与时间衰减权重；参见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 中的 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 说明。  
  - **用户画像（Profiles）**：聚合多维度偏好、身份标签与行为模式（如“技术从业者｜偏好 Python｜关注 AI 基础设施”），支持向量相似度检索；其设计目标与使用约束详见 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 文档。  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `enable_memory` | boolean | 否 | 默认 `false`；设为 `true` 后触发 LTM 检索与自动更新（需配合 `memory_config`） |
| `memory_config.type` | string | 是（当 `enable_memory=true`） | 取值 `"fragments"` 或 `"profiles"`，不可混用；[通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档明确禁止同时启用两类记忆 |
| `memory_config.ttl_seconds` | integer | 否 | 记忆项 TTL，默认 `604800`（7 天）；设为 `0` 表示永不过期（不推荐生产环境使用） |

> **注意**：`memory_config.ttl_seconds` 在 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 文档中标注为“最小单位为小时”，但实际 API 接收秒级整数 —— 请以 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档的秒级定义为准，避免误设。

## 使用方式

1. 在请求体中显式声明 `enable_memory: true` 并配置 `memory_config`；  
2. 对于事实记忆，确保 `user_id` 字段存在且稳定（用于跨会话关联）；  
3. 用户画像需预先通过 `/v1/memory/profiles/upsert` 接口注入初始标签，否则首次检索返回空；  
4. 所有 LTM 操作均异步执行，主请求响应中不包含记忆操作结果 —— 详情请查阅 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- 单次请求最多触发 **1 次事实记忆写入** 和 **1 次用户画像更新**，不支持批量操作；  
- 记忆内容不参与模型训练或微调，纯属运行时上下文增强；  
- `user_id` 必须符合平台 ID 规范（长度 1–64 字符，仅含字母、数字、下划线、短横线），否则记忆写入失败且无明确错误码；  
- 当前不支持跨应用共享记忆空间，每个应用拥有独立 LTM 存储域。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)



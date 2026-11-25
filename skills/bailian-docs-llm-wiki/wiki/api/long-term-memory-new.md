# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话维护用户画像、对话片段、业务上下文等关键信息。它通过统一的 API 接口支持向量化检索与结构化查询，适用于个性化推荐、多轮对话状态管理、用户行为建模等场景。该能力基于 [原文标题](../../raw/application-api-reference/long-term-memory-new.md) 中定义的架构设计，与平台其他记忆模块保持协议兼容。

## 支持的模型/功能

- **核心能力**：支持用户画像（Profiles）、记忆片段（Fragments）、向量检索（Vector Search）三类原语；
- **模型兼容性**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三个模型版本支持在 `messages` 中自动注入 LTM 检索结果（需显式启用 `enable_long_term_memory: true`）；
- **非模型依赖功能**：记忆写入（`POST /v1/memory/fragments`）、批量查询（`POST /v1/memory/profiles/query`）等 API 可独立调用，不绑定特定推理模型。详见 [原文标题](../../raw/application-api-reference/long-term-memory-new.md) 的功能概览部分。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `memory_id` | string | 否 | 用户级唯一标识，若未提供则由平台生成 UUID；建议业务侧传入稳定 ID（如 `user_id`）以保障跨设备一致性 |
| `ttl_seconds` | integer | 否 | 记忆过期时间，默认 `2592000`（30 天），最大支持 `31536000`（1 年） |
| `embedding_model` | string | 否 | 指定[向量嵌入](../concepts/vector-embedding.md)模型，仅当 `type=fragment` 且含 `content` 字段时生效；默认为 `text-embedding-v3`，不支持切换为旧版 `text-embedding` 模型（[原文标题](../../raw/application-api-reference/long-term-memory-new.md) 明确弃用） |

> **注意**：文档中提及的 `profile_type: "user"` 已被废弃，现统一使用 `type: "profile"`，旧参数名会导致 400 错误；请以最新 API Schema 为准。

## 使用方式

1. **写入记忆**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/memory/fragments \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "memory_id": "usr_abc123",
           "type": "fragment",
           "content": "用户偏好咖啡因含量低的茶饮",
           "metadata": {"category": "preference", "source": "survey_v2"}
         }'
   ```

2. **在推理请求中启用**：  
   在 `/v1/services/aigc/text-generation` 请求体中添加：
   ```json
   "parameters": {
     "enable_long_term_memory": true,
     "ltm_config": {
       "top_k": 3,
       "filter": {"metadata.category": "preference"}
     }
   }
   ```
   平台将自动注入匹配的记忆片段至 `system` 角色上下文。

## 限制和注意事项

- 单次写入 `content` 长度上限为 8192 字符；超长内容需分片处理；
- 向量检索仅对 `type=fragment` 且含 `content` 的条目生效，`type=profile` 条目不参与向量索引；
- 每个 `memory_id` 下最多存储 1000 个 `fragment` + 100 个 `profile`，超出后写入失败并返回 `429 Too Many Items`；
- 删除操作（`DELETE /v1/memory/fragments/{id}`）为软删除，数据保留 7 天后彻底清除——此行为与 [原文标题](../../raw/application-api-reference/long-term-memory-new.md) 中“立即物理删除”的旧描述矛盾，**请以当前实际行为为准**。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)



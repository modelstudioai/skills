# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态存储与语义检索能力，支持将对话自动提炼为记忆片段，并基于语义相似度进行高效召回。该功能通过统一 API 接口提供 Add、Search、List、Delete、Update 等核心操作，并可选配用户画像提取与重排序策略。所有接口均需使用 DashScope API Key 认证，适用于构建具备上下文延续能力的智能体应用。

## 支持的模型/功能

- **记忆抽取模型**：AddMemory 接口支持 `pro` 与 `lite` 两种质量档位（由 `profile_schema` 或隐式策略决定），影响记忆片段的抽象粒度与准确性；详见[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **搜索重排序（Rerank）**：SearchMemory 接口通过 `plan_version=pro` 或 `enable_rerank=true` 启用，显著提升相关性排序质量；`plan_version` 优先级高于 `enable_rerank`，传入时后者被忽略。
- **用户画像模板**：通过 `CreateProfileSchema` 等接口定义结构化画像 schema，AddMemory 中传入 `profile_schema` ID 即可触发画像字段自动填充。
- **多规则混合检索**：SearchMemory 支持通过 `project_ids` 参数指定多个记忆片段规则 ID，实现跨规则语义融合检索。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 记忆归属实体标识（≤64 字符） | `"user_001"` |
| `messages` / `custom_content` | array / string | 互斥 | 对话消息列表（最多 50 条）或自定义文本（≤512 字符） | `[{"role":"user","content":"明天10点提醒我..."}]` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库 | `"ml-abc123"` |
| `top_k` | integer | 否 | SearchMemory 最大召回数（1–100，默认 10） | `5` |
| `min_score` | double | 否 | 相似度阈值 [0,1]（默认 0.3） | `0.5` |
| `plan_version` | string | 否 | 搜索策略版本：`pro`（启用 Rerank）或 `lite`（禁用），大小写不敏感 | `"pro"` |
| `meta_data` | object | 否 | 用户自定义键值对，支持在 Add/List/Update 中透传 | `{"source": "web_chat"}` |

> **注意**：`messages` 中每条 `content` 若为数组（如含多模态内容），当前仅支持文本部分参与记忆抽取；非文本内容会被忽略——此行为与[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)中“messages\[0\].content 类型为 string \| array”的描述一致，但实际处理逻辑未对数组元素做结构化解析。

## 使用方式

### 基础调用流程
1. **认证**：在请求 Header 中设置 `Authorization: Bearer $DASHSCOPE_API_KEY`；
2. **选择接口**：根据操作类型调用对应 endpoint（如 `/add`, `/memory_nodes/search`）；
3. **构造请求体/查询参数**：按需传入 `user_id`、`messages`/`custom_content`、`memory_library_id` 等；
4. **处理响应**：解析 `memory_nodes` 数组及分页/元数据字段。

### SDK 快速接入（Python）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, AddMemoryInput, SearchMemoryInput
import asyncio

async def main():
    # 添加记忆
    add = AddMemory()
    res = await add.arun(AddMemoryInput(
        user_id="u1",
        messages=[{"role": "user", "content": "每天9点提醒我吃药"}],
        meta_data={"category": "health"}
    ))
    
    # 搜索记忆
    search = SearchMemory()
    res = await search.arun(SearchMemoryInput(
        user_id="u1",
        messages=[{"role": "user", "content": "我有什么健康提醒？"}],
        top_k=3,
        plan_version="pro"
    ))
```

完整接口路径与方法见[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **计费生效时间**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 起正式商业化计费，Add 和 Search 调用均区分 `pro`/`lite` 版本并按次计费。
- **数据持久性**：生成的记忆片段与用户画像暂无自动失效机制，需自行管理生命周期。
- **ID 长度约束**：`user_id` ≤ 64 字符，`memory_library_id` ≤ 32 字符，超长将导致请求失败。
- **互斥参数**：`messages` 与 `custom_content` 互斥，若同时传入，`custom_content` 优先生效并忽略 `messages`。

> **注意**：文档中 `ListMemory` 的示例 cURL 请求使用了 `--data '{}'`，但实际为 GET 请求且无 request body；该写法易引发混淆。正确用法应为纯 query string（如 `?user_id=u1&page_size=10`），此问题已在最新版 SDK 实现中规避，但原始文档[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)尚未修正。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



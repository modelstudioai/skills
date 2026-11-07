# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台面向 Agent 应用提供的结构化记忆管理能力，支持事实记忆（`observation`）与技能记忆（`skill`）的写入、语义检索、更新与删除，并可结合用户画像模板实现属性级信息抽取。所有操作均基于业务空间隔离，通过统一 API 接口与 SDK 封装提供，适用于对话历史沉淀、用户偏好建模与自动化工作流构建等场景。

## 支持的模型/功能

- **记忆类型**：支持两类核心记忆节点：
  - `observation`（事实记忆）：如“用户明天上午11点需点外卖”，由对话消息自动抽取；
  - `skill`（技能记忆）：如“会议纪要整理”，需显式传入 `skill_name`/`skill_description`/`skill_tags`，支持工具调用上下文识别（见[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）。
- **用户画像**：通过 `profile_schema` 定义结构化属性（如“年龄”“爱好”），在 `AddMemory` 或 `AddMemoryAsync` 调用中传入后触发异步抽取，结果通过 [GetUserProfile](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询。
- **多模态支持**：`messages[].content` 支持 `text` 与 `image_url` 混合输入，但仅在启用多模态能力的项目中解析图片（见[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）。

> **注意**：文档 6（同步 AddMemory）称其“在 `intelligent` 模式下可能超时”，而文档 19（异步 AddMemoryAsync）明确支持 `intelligent` 场景；实际生产环境应优先使用异步接口，同步接口仅适用于 `efficient` 模式下的低延迟场景。

## 关键参数

| 参数 | 说明 | 示例值 | 必填性 |
|------|------|--------|--------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | `"user_001"` | 所有写入/检索接口必填 |
| `project_id` / `project_ids` | 记忆二级隔离标识；`project_ids` 最多支持 5 个，与 `project_id` 互斥 | `["project_001"]` | 写入/检索可选，但推荐使用以组织记忆 |
| `memory_types` | `SearchMemory` 中指定检索范围，默认 `["observation"]` | `["observation", "skill"]` | 可选 |
| `plan_version` | `SearchMemory` 和 `CreateProfileSchema` 中控制能力等级：<br>- `pro`：支持 `min_score` 过滤、Rerank、高精度抽取<br>- `lite`：基础检索与抽取 | `"pro"` | 可选（默认 `pro`） |
| `extract_mode` | `AddMemory`/`AddMemoryAsync` 中控制抽取行为：<br>- `profile_only`：仅提取画像（需同时传 `profile_schema` + `messages`） | `"profile_only"` | 可选 |

## 使用方式

### 1. 基础流程
1. **准备凭证**：获取 `DASHSCOPE_API_KEY` 与业务空间 ID（见[认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）；
2. **写入记忆**：
   - 实时性要求高 → 用 `AddMemory`（同步，响应含抽取结果）；
   - 需多项目/技能/画像联合抽取 → 用 `AddMemoryAsync`（异步，返回 `event_id`，再调 [GetEvent](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 查询）；
3. **检索记忆**：调 `SearchMemory`，传 `messages`（查询意图）与 `user_id`，按 `top_k` 和 `min_score`（`pro` 版本）筛选；
4. **管理画像**：先 `CreateProfileSchema` 定义字段，再在写入时传 `profile_schema`，最后 `GetUserProfile` 获取结果。

### 2. SDK 快速示例（Python）
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemoryAsync, SearchMemory
import asyncio

async def main():
    # 异步写入
    add = AddMemoryAsync()
    res = await add.arun(user_id="user_001", messages=[{"role":"user","content":"提醒我喝水"}])
    event_id = res.event_id  # 后续轮询 GetEvent

    # 语义搜索
    search = SearchMemory()
    res = await search.arun(
        user_id="user_001",
        messages=[{"role":"user","content":"我有什么提醒？"}],
        top_k=5,
        min_score=0.5
    )
    for node in res.memory_nodes:
        print(f"[{node.score:.2f}] {node.content}")

asyncio.run(main())
```

## 限制和注意事项

- **限流规则**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `add` 接口 ≤ 120 QPM；
  - `search` 接口 ≤ 300 QPM；
  - 超限返回 HTTP 429，需按指数退避重试（1s/2s/4s）（见[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)）。
- **商业化时间点**：所有 `Add` 与 `Search` 调用将于 **2026 年 8 月 20 日 10:00（北京时间）** 起区分 `Pro`/`Lite` 计费版本，策略差异直接影响 `min_score`、Rerank 与抽取质量（见[长期记忆API](../../raw/application-user-guide/agent-context/memory-library-overview/long-term-memory-2-0.md)）。
- **关键约束**：
  - `custom_content` 与 `project_ids` 互斥，不可同时传入；
  - `skill` 类型记忆的 `UpdateMemory` 必须同时传 `skill_name`/`skill_description`/`skill_tags`；
  - 用户画像提取为异步过程，首次 `GetUserProfile` 可能为空，需业务侧重试（见[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）；
  - 删除操作不可逆，调用前务必确认 `memory_node_id`。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)



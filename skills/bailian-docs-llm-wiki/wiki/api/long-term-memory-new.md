# long term memory new

长期[记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化[记忆](../concepts/memory.md)管理服务，支持事实[记忆](../concepts/memory.md)（observation/[skill](../guides/skill.md)）与用户画像（profile）两类核心能力。通过统一的 RESTful API，开发者可编程式地写入、检索、更新和删除记忆节点，并支持多模态内容、异步抽取、多项目隔离等高级特性。所有接口均通过 DashScope 网关提供，需使用 `DASHSCOPE_API_KEY` 鉴权。

## 支持的模型/功能

- **事实记忆**：支持两种类型  
  - `observation`：从对话中提取的用户行为、偏好、计划等客观事实（如“用户每天上午11点提醒点外卖”），通过 [AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 或 [AddMemoryAsync](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md) 写入；  
  - `skill`：从工具调用或结构化指令中提取的可复用操作流程（如“会议纪要整理”），支持导出完整元信息（名称、描述、标签），详见 [导出技能记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)。  
- **用户画像**：基于预定义模板（`profile_schema`）从对话中异步抽取结构化属性（如年龄、爱好、职业）。需先调用 [CreateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) 创建模板，再在 `AddMemory` 中传入 `profile_schema` 参数触发抽取，最终通过 [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 获取结果。  
- **多模态支持**：`messages[].content` 可包含 `text` 和 `image_url` 类型，但仅启用多模态能力的项目会解析图片；其他项目将忽略图片字段 [添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。

> **注意**：文档 5（添加记忆）称同步接口在 `intelligent` 模式下“可能超时”，而文档 20（异步添加记忆）明确推荐异步方式用于技能和画像抽取。二者不矛盾，但表明 `intelligent` 模式下的同步抽取稳定性不足，生产环境应优先选用 `add-async`。

## 关键参数

| 参数 | 作用 | 说明 |
|------|------|------|
| `user_id` | 记忆隔离主键 | 所有读写接口必填，用于逻辑隔离不同用户的数据 |
| `memory_library_id` | 记忆库隔离 | 可选，不传则使用默认记忆库；配合 `project_id`/`project_ids` 实现二级隔离 |
| `plan_version` | 计费与能力策略 | `pro`（默认）支持 `min_score` 过滤、Rerank、高精度抽取；`lite` 仅基础语义检索与抽取。`pro`/`lite` 同时影响 Add 和 Search 接口行为 [长期记忆API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `extract_mode` | 抽取范围控制 | `profile_only` 时仅执行画像抽取（需同时传 `profile_schema` 和 `messages`），跳过事实记忆生成 |
| `min_score` | 检索结果过滤 | 仅 `plan_version=pro` 时生效，默认阈值 `0.3`，低于此分的 `memory_nodes` 将被过滤 [搜索记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md) |

## 使用方式

1. **鉴权准备**：在[百炼控制台](https://bailian.console.aliyun.com)获取 `DASHSCOPE_API_KEY`，并设置为环境变量或请求头 `Authorization: Bearer $DASHSCOPE_API_KEY` [鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。  
2. **写入记忆**：  
   - 实时性要求高且内容简单 → 用同步 `POST /add`；  
   - 需抽取 [skill](../guides/skill.md)/画像/多项目并行 → 用异步 `POST /add-async`，立即获得 `event_id`，再轮询 [GetEvent](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 查询状态与结果。  
3. **检索记忆**：`POST /memory_nodes/search` 传入 `messages`（如用户当前提问）和 `user_id`，返回带 `score` 的相关记忆列表。  
4. **管理记忆**：  
   - 列表：`GET /memory_nodes?user_id=xxx`；  
   - 单查：`GET /memory_nodes/{id}`；  
   - 更新：`PATCH /memory_nodes/{id}`（支持增量更新 `meta_data` 及 [skill](../guides/skill.md) 元信息）；  
   - 删除：`DELETE /memory_nodes/{id}`（不可逆）。  
5. **用户画像工作流**：创建 schema → 调用 `AddMemory` 传 `profile_schema` → 轮询 `GetUserProfile` 直至 `attributes[].value` 非空。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM [长期记忆API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。  
- **计费时间点**：记忆库将于 **2026 年 8 月 20 日** 正式商业化计费，Add/Search 调用按 `plan_version` 区分 Pro/Lite 计费策略 [API 概览](raw/application-api-reference/long-term-memory-new/api-overview.md)。  
- **异步任务重试**：`GetEvent` 返回 `status=PENDING` 或 `RUNNING` 时，需客户端主动轮询；`status=FAILED` 时需检查 `messages` 格式或权限配置 [查询事件](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。  
- **画像抽取延迟**：`GetUserProfile` 首次调用可能返回空值，因抽取为异步过程；需按业务逻辑实现重试（建议指数退避） [获取用户画像](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。  
- **安全红线**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库 [鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
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
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)



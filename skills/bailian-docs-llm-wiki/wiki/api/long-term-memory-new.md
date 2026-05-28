# long term memory new

长期记忆（新）为开发者提供面向 Agent 与对话应用的持久化上下文管理能力，支持通过 RESTful API 对记忆节点进行全生命周期管理及高精度语义检索。系统可自动从多轮对话中提取关键事实，并结合画像模板生成结构化用户画像，适用于个性化交互、日程管理与意图延续等场景。完整接口规范请参见[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能
- **记忆片段管理**：提供 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 及 `UpdateMemory` 五大核心接口，支持基于原始对话的自动提取与 `custom_content` 手动录入。
- **语义检索增强**：内置向量相似度召回，支持 `top_k` 截断、阈值过滤、结果重排序（Rerank）、Query 重写及意图判别回调，有效降低无关记忆注入。
- **画像模板体系**：提供 `CreateProfileSchema` / `GetProfileSchema` 等模板管理接口，支持将记忆片段规则（`project_id`）绑定至 [[画像模板]]，实现多维用户特征抽取。
- **多租户与隔离**：通过 `memory_library_id` 划分物理存储边界，支持跨规则混合检索，数据归属严格绑定 `user_id`。

## 关键参数
| 参数域 | 核心字段 | 类型/限制 | 说明 |
|:---|:---|:---|:---|
| **认证** | `Authorization` | Header | 必填，格式 `Bearer $DASHSCOPE_API_KEY` |
| | `Base URL` | String | `https://dashscope.aliyuncs.com/api/v2/apps/memory/` |
| **实体标识** | `user_id` | string (≤64) | 记忆归属实体 ID，全量接口必填 |
| **内容输入** | `messages` | array (≤50) | 一问一答计为 2 条，包含 `role` 与 `content` |
| | `custom_content` | string (≤512) | 与 `messages` 互斥，直接写入自定义文本 |
| **路由控制** | `memory_library_id` | string (≤32) | 指定存储库，缺失则命中默认库 |
| | `project_id` | string | 指定记忆片段规则，控制提取与检索策略 |
| **检索配置** | `top_k` | int [1,100] | 最大召回数量，默认 10 |
| | `min_score` | double [0,1] | 相似度阈值，默认 0.3 |
| | `enable_rerank` / `enable_judge` / `enable_rewrite` | boolean | 按需开启后处理管线，默认 false |

## 使用方式
所有操作均基于 HTTP 方法路由，请求需声明 `Content-Type: application/json`。以下为高频场景调用示例，详细字段定义与响应结构见[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

**1. 注入记忆片段（对话解析）**
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "messages": [
      {"role": "user", "content": "每天上午11点提醒我点外卖"},
      {"role": "assistant", "content": "已记录"}
    ],
    "user_id": "user_001",
    "meta_data": {"priority": "high"}
  }'
```

**2. 上下文检索**
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我中午一般有什么习惯？"}],
    "top_k": 5,
    "min_score": 0.5,
    "enable_rerank": true
  }'
```

**3. 分页查询与更新**
- 查询：`GET /memory_nodes?user_id=xxx&page_num=1&page_size=20`
- 更新：`PATCH /memory_nodes/{memory_node_id}` 携带 `user_id`、`custom_content` 与 `meta_data`。
- 客户端集成：Python 开发者需安装 `agentscope-runtime>=1.1.5`，封装类提供 `arun()` 异步调用接口。完整 SDK 示例可查阅[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项
- **配额与限流**：账号级总 QPM ≤ 3000。其中 `add` 接口严格限制 120 QPM，`search` 接口限制 300 QPM，高频业务需实现指数退避重试。
- **数据生命周期**：当前生成的记忆片段与 [[用户画像]] 暂无自动失效或归档机制，建议业务侧定期清理冗余节点。
> **注意**：Python SDK 暂未提供 `UpdateMemory` 接口的原生封装，更新操作需使用 `requests` 等 HTTP 客户端直接发起 `PATCH` 请求。同时，`messages` 与 `custom_content` 为强互斥字段，若同时传入，后端将丢弃对话记录仅处理自定义内容。
- **检索策略调优**：开启 `enable_rewrite` 可提升口语化 Query 的召回率，但会增加约 50~100ms 延迟；`enable_judge` 适用于需强过滤业务场景，建议结合 A/B 测试评估阈值。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)


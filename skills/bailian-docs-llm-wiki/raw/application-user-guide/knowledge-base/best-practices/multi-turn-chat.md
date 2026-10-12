# 多轮对话：正确传递工具调用历史

从创建知识库到 API 多轮调用，端到端实践传递工具调用历史避免重复检索

**说明**本实践展示如何在多轮对话中传递工具调用历史，让模型基于已有检索结果连续作答，避免重复检索。全程使用统一样例文档演示，效果可复现。

## 原理：为什么会丢失上下文

RAG Agent 是无状态服务，每次请求独立，服务端不保存对话上下文。一轮响应通常包含多个阶段：

```
用户提问 ──→ 思考 ──→ 调用工具检索 ──→ 拿到结果 ──→ 信息足够？
              ▲                                      │
              └──────────────── 否 ──────────────────┤
                                                     │ 是
                                                     ▼
                                              生成最终回答
```

如果下一轮只传文本历史（user 提问 + assistant 回答），模型看不到中间的工具调用过程，也不知道之前已经检索过哪些内容，会**重复检索**同一问题，既浪费 token 又可能返回不一致的答案。

正确做法是把完整的工具调用链路（`assistant.tool_calls` + `tool` 返回结果）作为历史消息一起传入，让模型基于已有检索结果连续作答。

## 准备样例文档

本实践使用 [阿里云百炼技术文档样例](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260625/ikvclq/bailian-docs-sample.zip) 演示，包含 92 篇阿里云百炼平台官方技术文档（API 调用、模型说明、最佳实践等）。下载解压后上传至知识库即可使用。以其中的《首次调用通义千问 API》为例演示多轮追问：

-   **第 1 轮**：问"如何调用通义千问 API"（触发多轮工具检索）
-   **第 2 轮**：追问"如何把 API Key 配置到环境变量"（验证是否复用历史、不重复检索）

也可使用你自己的文档，操作步骤和效果类似。

## 端到端操作

### 1\. 创建知识库并上传样例文档

1.  进入 [**数据接入 → 知识管理**](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，点击 **创建知识库**
2.  知识库类型选择**文档搜索**，使用场景选择**基础文档问答**
3.  上传样例文档，完成切片与向量化，等待文档状态变为**解析完成**

详见[创建知识库](raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)和[文档管理](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。

### 2\. 创建知识问答服务并绑定知识库

1.  进入 [**知识服务 → 知识问答**](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list)，点击 **创建问答服务**
2.  填写服务名称，创建成功后进入配置页
3.  点击 **\+ 添加**，绑定上一步创建的知识库
4.  选择生成模型和检索模式（多轮对话建议选**多轮智能检索**），点击 **发布**

详见[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

### 3\. 获取 API 参数

在问答服务列表中，点击目标服务的 **API 调试**，获取以下参数：

参数

获取位置

示例

**endpoint**

API 调试页的接口地址，`{workspace_id}` 为业务空间 ID

`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`

**agent\_id**

API 调试页的请求参数，知识问答服务 ID

`aid-xxxxxxxx`

**API Key**

[设置 → API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页创建

`sk-xxxxxxxx`

**说明**agent\_id 是知识问答服务的唯一标识，每个问答服务对应一个 agent\_id。

### 4\. 第一轮调用

用获取的参数发起第一次请求。请求结构如下：

```
curl -X POST 'https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat' \
  -H 'Authorization: Bearer $API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "input": {
      "messages": [{"role": "user", "content": "如何调用通义千问 API"}]
    },
    "parameters": {
      "agent_options": {"agent_id": "aid-xxxxxxxx"}
    },
    "stream": true
  }'
```

Agent 内部会执行多轮工具调用检索知识库，最后流式返回最终回答。需要从 SSE 流中提取工具调用历史，见下方[从 SSE 流提取工具历史](#h-multiturn-sse)。

### 5\. 第二轮：携带工具历史追问

第二轮提问"如何把 API Key 配置到环境变量"时，把第一轮的完整历史（含工具调用链路）一起传入：

```
curl -X POST 'https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat' \
  -H 'Authorization: Bearer $API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "如何调用通义千问 API"},
        {"role": "assistant", "content": "", "tool_calls": [{"id":"call_956...","function":{"name":"semantic_search",...}}]},
        {"role": "tool", "tool_call_id": "call_956...", "content": "检索到 5 条相关切片..."},
        {"role": "assistant", "content": "根据检索到的《首次调用通义千问 API》内容..."},
        {"role": "user", "content": "如何把 API Key 配置到环境变量？"}
      ]
    },
    "parameters": {"agent_options": {"agent_id": "aid-xxxxxxxx"}},
    "stream": true
  }'
```

**警告**`tool_call_id` 必须使用第一轮流式响应中返回的原值，不能自行编造。模型靠它匹配"哪个调用对应哪个结果"。

### 6\. 效果对比

以《首次调用通义千问 API》文档为例实测：第 1 轮问"如何调用通义千问 API"后，第 2 轮追问"如何把 API Key 配置到环境变量"，对比两种传历史方式：

传入完整工具历史

只传文本历史

第 2 轮工具调用

0 次，直接基于已有结果回答

重新检索（实测触发 2 次 semantic\_search）

响应速度

快，无需再走检索流程

慢，重新执行检索

回答一致性

基于同一批检索结果，前后连贯

重新检索可能命中不同切片，前后不一致

实测数据：第 1 轮执行了 2 轮工具调用（semantic\_search → obtain\_file），产生 6 条历史消息；第 2 轮传完整历史（7 条消息）时模型 0 次工具调用直接作答，只传文本历史（3 条消息）时则重新发起 2 次 semantic\_search。具体轮数和消息数取决于文档结构与问题匹配度，但"传完整历史可避免重复检索"这一结论稳定成立。

**说明**传完整历史会让 input 更长（携带了工具返回内容），但省去重新检索的开销；只传文本历史 input 较短，却要重新走一遍检索流程。两者各有取舍，多轮追问场景下传完整历史在响应速度和回答一致性上更优。

## 从 SSE 流提取工具历史

Agent 的流式输出采用 SSE 协议，每个数据帧为 `data:{...}`，解析路径为 `obj.output.choices[0].message`。`message.extra.step_change` 标记状态转换边界，只需关注 **3 类事件**：

事件

识别条件

提取的数据

工具调用

`step_change == "tool_calling"`

`tool_calls` 数组（本轮所有并行调用）

工具返回

`step_change == "tool_return"` 且 `role == "tool"`

`content` + `tool_call_id`

最终回答

`generation_start` 到 `generation_end` 之间

累积所有 `content`

### 状态流转

```
plan_start（开始思考） ──→ plan_end ──→ tool_calling（派发工具调用） ──→ tool_return（工具返回） ──→ 需要更多信息？
    ▲                                                                                              │
    └────────────────────────────── 是 ────────────────────────────────────────────────────────────┤
                                                                                                   │ 否
                                                                                                   ▼
                                                                                  generation_start ──→ generation_end
```

Agent 可能执行多轮工具调用，直到收集到足够信息后才生成最终回答。

## 消息格式与关键规则

提取出的历史消息按以下角色和顺序组织：

角色

必需字段

说明

`user`

`role`, `content`

用户输入

`assistant`（工具调用）

`role`, `content`(空), `tool_calls`

本轮发起的所有并行工具调用，`function.arguments` 为 JSON 字符串

`tool`

`role`, `content`, `tool_call_id`

工具返回结果，`tool_call_id` 必须与对应 `tool_calls[].id` 一致

`assistant`（最终回答）

`role`, `content`

模型的最终回答

**消息顺序严格按时间排列**：

```
user 提问 ──→ assistant（tool_calls） ──→ tool × N ──→ assistant（tool_calls） ──→ tool × N ──→ assistant 最终回答 ──→ user 下一轮
```

多轮工具调用重复 `assistant` → `tool` 模式；下一轮在新 `user` 消息后重复以上流程，完整历史一并传入。

## Python 完整实现

下面的代码封装了"从 SSE 提取历史 → 多轮对话自动传递 → 效果对比"的完整逻辑，可直接运行。实测基于本页的样例文档与话术。

### 配置

```
import json
import requests

# 从控制台问答服务的 API 调试页面获取
API_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat"
API_KEY = "sk-xxxxxxxx"      # workspace-scoped API Key（sk-ws- 前缀）
AGENT_ID = "aid-xxxxxxxx"    # 知识问答服务 ID
```

### 从 SSE 流提取工具历史

```
class ConversationTracker:
    """追踪单轮 Agent 响应，从流式事件提取完整消息序列。"""

    def __init__(self):
        self.messages = []          # 提取出的消息序列（工具调用 + 工具返回）
        self.tool_call_rounds = 0   # 工具调用轮数（用于效果对比）
        self.answer = ""            # 最终回答
        self._generating = False

    def process_sse_line(self, line: str):
        if not line.startswith("data:"):
            return
        obj = json.loads(line[len("data:"):].strip())
        choices = obj.get("output", {}).get("choices", [])
        if not choices:
            return

        msg = choices[0].get("message", {})
        step_change = msg.get("extra", {}).get("step_change", "")
        role = msg.get("role", "")
        content = msg.get("content", "") or ""

        # 事件 1：工具调用派发（step_change == "tool_calling"）→ 提取 tool_calls
        if step_change == "tool_calling" and msg.get("tool_calls"):
            self.tool_call_rounds += 1
            self.messages.append({
                "role": "assistant", "content": "",
                "tool_calls": [{"id": tc["id"], "type": "function",
                                "function": {"name": tc["function"]["name"],
                                             "arguments": tc["function"]["arguments"]}}
                               for tc in msg["tool_calls"]],
            })
        # 事件 2：工具返回（step_change == "tool_return"，role == "tool"）→ 提取 content + tool_call_id
        elif step_change == "tool_return" and role == "tool":
            self.messages.append({"role": "tool",
                                  "tool_call_id": msg.get("tool_call_id", ""),
                                  "content": content})
        # 事件 3：最终回答（generation_start → 内容流 → generation_end）→ 累积 content
        elif step_change == "generation_start":
            self._generating = True
            self.answer = content
        elif self._generating and content:
            self.answer += content
        elif step_change == "generation_end":
            self.answer += content
            self._generating = False

    def get_response_messages(self):
        """返回本轮提取的完整消息序列（含最终回答）。"""
        result = list(self.messages)
        if self.answer:
            result.append({"role": "assistant", "content": self.answer})
        return result
```

### 多轮对话管理

```
class MultiTurnChat:
    """管理多轮对话历史，自动携带工具调用链路。"""

    def __init__(self):
        self.history = []

    def ask(self, question: str) -> str:
        """发送问题，自动拼接完整历史（含工具调用链路），返回最终回答。"""
        self.history.append({"role": "user", "content": question})
        sent = len(self.history)
        tracker = self._call_agent(self.history)
        # 将本轮提取的工具调用链路和最终回答加入历史
        self.history.extend(tracker.get_response_messages())
        print(f"  发送 {sent} 条消息，工具调用 {tracker.tool_call_rounds} 轮")
        return tracker.answer

    def _call_agent(self, messages):
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        body = {
            "input": {"messages": messages},
            "parameters": {"agent_options": {"agent_id": AGENT_ID}},
            "stream": True,
        }
        tracker = ConversationTracker()
        resp = requests.post(API_URL, headers=headers, json=body, stream=True, timeout=180)
        for chunk in resp.iter_lines():
            if chunk:
                tracker.process_sse_line(chunk.decode("utf-8").strip())
        return tracker
```

### 效果对比：传完整历史 vs 只传文本历史

```
chat = MultiTurnChat()

# 第 1 轮
print("[第 1 轮] 如何调用通义千问 API")
chat.ask("如何调用通义千问 API")

# 第 2 轮 · 传完整工具历史（自动携带）
print("\n[第 2 轮 · 传完整工具历史]")
chat_full = MultiTurnChat()
chat_full.history = list(chat.history)
chat_full.ask("如何把 API Key 配置到环境变量？")

# 第 2 轮 · 只传文本历史（丢弃工具调用，只留 user + assistant 回答）
print("\n[第 2 轮 · 只传文本历史]")
text_only = [m for m in chat.history
             if m["role"] == "user" or (m["role"] == "assistant" and not m.get("tool_calls"))]
chat_text = MultiTurnChat()
chat_text.history = text_only
chat_text.ask("如何把 API Key 配置到环境变量？")
```

实测运行输出：

```
[第 1 轮] 如何调用通义千问 API
  发送 1 条消息，工具调用 2 轮

[第 2 轮 · 传完整工具历史]
  发送 7 条消息，工具调用 0 轮      ← 直接复用，未重复检索

[第 2 轮 · 只传文本历史]
  发送 3 条消息，工具调用 2 轮      ← 重新检索
```

## 注意事项

### 历史长度控制

工具返回内容可能很长，多轮累积后可能超出上下文限制。建议：

-   **截断早期工具返回**：只对最近 K 轮保留完整工具内容，更早轮次的 `tool` 消息截断保留前 N 字符
-   **滑动窗口**：超过 3 轮的历史，将早期工具调用结果替换为摘要

```
def truncate_history(messages, max_tool_len=2000, keep_recent=2):
    """截断较早轮次的工具返回内容。"""
    user_indices = [i for i, m in enumerate(messages) if m["role"] == "user"]
    if len(user_indices) <= keep_recent:
        return messages
    cutoff = user_indices[-keep_recent]
    result = []
    for i, msg in enumerate(messages):
        if i < cutoff and msg["role"] == "tool" and len(msg["content"]) > max_tool_len:
            msg = {**msg, "content": msg["content"][:max_tool_len] + "\n...(已截断)"}
        result.append(msg)
    return result
```

### 不需要传入历史的内容

内容

原因

`reasoning_content`

模型思考过程，展示给用户即可，无需回传

`extra` 字段

流式协议的状态标记，仅用于客户端渲染

`usage`

token 用量统计，仅用于监控计费

`tool_call_chunks`

流式分片，最终已合并到 `tool_calls`

### 常见问题

**如果不传工具调用历史会怎样？** 模型丢失检索上下文，重复搜索相同内容，回答质量下降。实测：传完整历史后追问，模型 0 次工具调用直接答；不传则重新检索。

**能跳过中间的工具调用，只传最终回答吗？** 可以工作但不推荐。只传 `user + assistant(最终回答)` 模型会失去对知识库内容的记忆，追问效果明显下降。

**并行工具调用的 tool 返回顺序重要吗？** 顺序不影响功能，模型通过 `tool_call_id` 匹配。但所有 `tool` 消息必须紧跟在对应的 `assistant(tool_calls)` 消息之后。

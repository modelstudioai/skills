# 处理时效性记忆

长期记忆中的临时状态会随时间失效。利用每条记忆自带的时间戳，让模型在回答时感知记忆的记录时间，避免把过期信息当作当前事实。

长期记忆中的很多信息是**临时状态**而非永久事实：伤病恢复期、短期忌口、备考阶段、出差驻地等。如果应用只把记忆正文注入上下文，模型无法区分“昨天记录的状态”和“半年前记录的状态”，会把早已结束的状态当成当前事实来回答。

本文介绍一种实测有效的做法：利用记忆自带的**时间戳**，让模型在回答时感知每条记忆距当前的时间。

## 记忆的时间戳

每条记忆节点都带有 `timestamp` 字段（Unix 秒级时间戳），在[检索记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)、[列出记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)、[获取记忆节点](raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)的响应中均返回：

```
{
  "memory_node_id": "7cf9b14c4e5b42b183bfb5630b69151d",
  "content": "用户处于脚踝扭伤恢复期，暂停下肢高强度训练",
  "timestamp": 1794365139,
  "created_at": 1794365141
}
```

-   `timestamp` 是**消息发生时间**（服务端接收该轮对话的时间），`created_at` 是记忆写入时间。正常实时接入时两者接近，以 `timestamp` 为准。
-   `timestamp` 由服务端记录，调用方不能指定。如需回填历史对话并保留原始时间，可将原始日期写入记忆正文（例如“（2026-09-01）用户……”）作为替代。

## 推荐做法

检索召回记忆后，将时间戳格式化为可读日期，连同**当前日期**和**时效性指令**一起注入系统提示词：

1.  召回记忆时读取每条的 `timestamp`，格式化为日期（如 `2026-10-12`）。
2.  注入上下文时以 `[记录于 YYYY-MM-DD]` 前缀标注每条记忆。
3.  在系统指令中给出当前日期，并显式要求模型判断记忆时效性，例如：“每条记忆附带记录时间，请结合今天日期判断其是否仍然有效；明显过期的生活状态类记忆不要当作当前事实。”

仅附加时间戳而不加时效指令时，多数模型会忽略日期、仍按当前事实作答；两者需要同时使用。

**说明**检索默认 `min_score=0.3`（pro 计划），可能过滤掉语义相关但分数不高的记忆。召回结果为空时，先调低 `min_score` 排查，详见[检索记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。

```
from datetime import datetime
import requests

MEM_BASE = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
LLM_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
HEADERS = {"Authorization": "Bearer $DASHSCOPE_API_KEY", "Content-Type": "application/json"}

# 1. 检索记忆
resp = requests.post(f"{MEM_BASE}/memory_nodes/search", headers=HEADERS, json={
    "messages": [{"role": "user", "content": user_query}],
    "user_id": user_id,
}).json()

# 2. 时间戳格式化为日期前缀
lines = []
for node in resp.get("memory_nodes", []):
    day = datetime.fromtimestamp(node["timestamp"]).strftime("%Y-%m-%d")
    lines.append(f"[记录于 {day}] {node['content']}")

# 3. 携带当前日期与时效指令注入系统提示词
today = datetime.now().strftime("%Y-%m-%d")
system_prompt = (
    f"你是运动康复助手。今天是 {today}。以下是长期记忆中关于该用户的信息，"
    "每条附带记录时间；请结合今天日期判断其是否仍然有效，"
    "明显过期的生活状态类记忆不要当作当前事实：\n" + "\n".join(lines)
)

answer = requests.post(LLM_URL, headers=HEADERS, json={
    "model": "qwen3.6-plus",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ],
}).json()
```

## 效果对比

以一条 6 周前写入的记忆“用户处于脚踝扭伤恢复期，暂停下肢高强度训练”为例，用户提问“今天想安排深蹲训练，可以吗”：

注入方式

模型表现

只注入记忆正文

直接按当前事实劝阻：“不建议，您正处于恢复期”

注入正文 + 记录时间

仍会按当前事实作答，时间信息未被使用

正文 + 记录时间 + 时效指令

能识别记忆已过期：“该记录已是 6 周前，一般扭伤恢复期已结束，可以从轻重量开始尝试”

## 配合记忆过期时间

时间戳注入解决的是**模型推理层面**的时效判断。如果某类记忆到期后应彻底不可召回，可在记忆规则上配置**记忆过期时间**（7 天 / 30 天 / 180 天 / 永不过期，见[配置记忆规则](raw/application-user-guide/agent-context/memory-library-overview/create-memory/configure-rules.md)），到期后记忆自动失效，不再参与检索。两者可以叠加使用：过期时间负责硬失效，时间戳负责让模型对仍在有效期内的记忆做出时间感知。

## 适用范围

-   适用于通过 API 自行编排记忆注入链路的应用；通过控制台 Agent Harness 或工作流插件接入时，记忆注入由平台完成，不适用本方式。
-   时效指令的措辞需按业务调整，并在真实模型上做回归验证。

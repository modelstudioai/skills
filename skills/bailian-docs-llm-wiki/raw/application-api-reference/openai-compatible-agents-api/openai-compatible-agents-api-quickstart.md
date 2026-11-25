# 快速开始

用 OpenAI SDK 创建 Agent 和 Session，提交任务并通过 SSE 接收执行结果。

<a id="前提"></a>

<a id="h-oa-qs-prereq"></a>

## 前提

1.  已开通百炼并[创建 API Key](openai-compatible-agents-api-authentication.md)。
2.  已安装 Python 3.9 及以上版本。
3.  已确认当前工作空间可用的模型，例如 `qwen3.8-max`。

<a id="code-block"></a>

```bash
pip install openai requests
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export BASE_URL="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
```

将 `{workspace_id}` 替换为实际工作空间 ID。

> **说明**
>
> 以下示例使用 `environment.type=none`，不创建沙箱，也不提供 Shell、文件读写等内置工具。需要使用文件、命令或 `environment` 侧 MCP 时，按[环境](openai-compatible-agents-api-environment.md)创建托管环境。

<a id="1-创建-agent"></a>

<a id="h-oa-qs-agent"></a>

## 1\. 创建 Agent

<a id="code-block-2"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

agent = client.beta.agents.create(
    model="qwen3.8-max",
    name="quickstart-agent",
    instructions="回答简洁，只输出必要信息。",
)
print(agent.id)
```

<a id="2-创建-session-并接收流式结果"></a>

<a id="h-oa-qs-session"></a>

## 2\. 创建 Session 并接收流式结果

<a id="code-block-3"></a>

```python
session_id = None
stream = client.beta.agents.sessions.create(
    agent_id=agent.id,
    environment={"type": "none"},
    input="用一句话介绍你自己。",
    stream=True,
)

for event in stream:
    if event.type == "agent.session.created":
        session_id = event.session.id
        print(f"Session: {session_id}")
    elif event.type == "agent.session.turn.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "agent.session.idle":
        print()
        break

print(f"Session ID: {session_id}")
```

HTTP 201 表示 Session 和首轮输入已受理，不表示执行完成。以 `agent.session.idle` 或 Turn 终态判断本轮结束。

<a id="3-查询历史"></a>

<a id="h-oa-qs-history"></a>

## 3\. 查询历史

<a id="code-block-4"></a>

```python
turns = client.beta.agents.sessions.turns.list(
    session_id,
    limit=20,
    order="asc",
)
for turn in turns.data:
    print(turn.id, turn.status)
    items = client.beta.agents.sessions.turns.items.list(
        turn.id,
        session_id=session_id,
        limit=100,
        order="asc",
    )
    for item in items.data:
        print(item.type, item.id)
```

<a id="4-继续会话"></a>

<a id="h-oa-qs-continue"></a>

## 4\. 继续会话

<a id="code-block-5"></a>

```python
with client.beta.agents.sessions.stream(
    session_id,
    input="再补充一句。",
) as stream:
    for event in stream:
        if event.type == "agent.session.turn.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "agent.session.idle":
            print()
            break
```

继续会话前先确认 Session 已回到 `idle`。`sessions.stream` 会先订阅事件再提交输入，并接收本轮结果。运行中的消息通常引导当前 Turn；如果 Turn 在消费输入前结束，消息可能转入新 Turn，客户端应以实际事件和 Turn ID 跟踪归属。

<a id="5-使用-curl"></a>

<a id="h-oa-qs-curl"></a>

## 5\. 使用 curl

创建 Agent：

<a id="code-block-6"></a>

```bash
curl -sS -X POST "$BASE_URL/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-max",
    "name": "quickstart-agent",
    "instructions": "回答简洁，只输出必要信息。"
  }'
```

创建 Session：

<a id="code-block-7"></a>

```bash
curl -N -sS -X POST "$BASE_URL/agents/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_xxx",
    "environment": {"type": "none"},
    "input": "用一句话介绍你自己。",
    "stream": true
  }'
```

`stream: true` 会在创建响应中直接返回首轮 SSE，避免创建完成后再订阅而漏掉快速回复。如需订阅已有 Session 的实时事件，再使用 `GET /agents/sessions/{session_id}/events`；该订阅不补发历史事件。

<a id="6-清理资源"></a>

<a id="h-oa-qs-cleanup"></a>

## 6\. 清理资源

<a id="code-block-8"></a>

```python
client.beta.agents.sessions.delete(session_id)
client.beta.agents.delete(agent.id)
```

删除 Session 会停止该 Session 的执行并清理公开历史；删除 Agent 只影响后续新建 Session，不影响已有 Session 的快照。

# 快速开始

五分钟跑通 Managed Agents 全链路：创建 Agent、开启 Session、发送消息并流式接收回复。

## 前提

1.  已开通百炼并创建 API Key（`sk-xxx`），已获取工作空间 ID（`ws_xxxxxxxxxxxx`），详见[API 总览与认证](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview)。
    
2.  将 API Key 与 Endpoint 导出为环境变量，后续示例直接引用：
    
    ```
    export DASHSCOPE_API_KEY="sk-xxx"
    export AGENTSTUDIO_URL="https://ws_xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio"
    ```
    

## 调用流程

一次完整的对话分四步：

1.  **创建 Agent**：定义模型与系统提示词，得到 `agent_xxx`。Agent 通常只创建一次并长期复用。
    
2.  **创建 Session**：绑定 Agent，得到 `sesn_xxx`。每轮对话新建一个 Session。
    
3.  **发送 Event**：向 Session 写入用户消息，触发 Agent 进入 `running`。
    
4.  **订阅 SSE**：以事件流方式接收回复，直至 Session 回到 `idle`。
    

## 安装 SDK

使用 Python 或 Java SDK 前，请先安装对应的 DashScope 包。Managed Agents 模块要求 Python SDK v1.26.2 及以上、Java SDK v2.22.24 及以上。若已安装旧版本，请重新执行安装命令以升级。

Python

```
pip install dashscope
```

Java

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
</dependency>
```

## 端到端示例

下例创建一个纯对话 Agent，开启 Session 后发送一条消息并流式接收回复。

Bash

```
## 1. 创建 Agent
AGENT_ID=$(curl -s -X POST "$AGENTSTUDIO_URL/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "quickstart-assistant",
    "model": {"id": "qwen-plus"},
    "system": "你是一个有帮助的助手。"
  }' | jq -r '.id')
echo "Agent: $AGENT_ID"

## 2. 创建 Session
SESSION_ID=$(curl -s -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"agent\": \"$AGENT_ID\"}" | jq -r '.id')
echo "Session: $SESSION_ID"

## 3. 发送用户消息
curl -X POST "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      {"role": "user", "type": "message",
       "content": [{"type": "text", "text": "你好，请介绍一下自己"}]}
    ]
  }'

## 4. 订阅 SSE 事件流，接收 Agent 回复
curl -N "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events/stream" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Accept: text/event-stream"
```

Python

```
import os
from dashscope.agentstudio import Client, user_message

client = Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    workspace="ws_xxxxxxxxxxxx",
    region="cn-beijing",
)

# 1. 创建 Agent
agent = client.agents.create(
    name="quickstart-assistant",
    model="qwen-plus",
    system_prompt="你是一个有帮助的助手。",
)

# 2. 创建 Session
session = client.sessions.create(agent=agent.id)
print(f"Agent: {agent.id}, Session: {session.id}")

# 3. 发送用户消息
client.sessions.events.send(
    session.id, [user_message("你好，请介绍一下自己")]
)

# 4. 流式接收回复
with client.sessions.events.stream(session.id) as stream:
    for event in stream:
        print(event, flush=True)
        if event.session_status in ("idle", "terminated"):
            break
```

Java

```
import com.alibaba.dashscope.agentstudio.*;
import com.alibaba.dashscope.agentstudio.model.*;
import com.alibaba.dashscope.agentstudio.param.*;

// 1. 创建客户端（自动读取 DASHSCOPE_API_KEY 环境变量）
AgentStudioClient client = AgentStudioClient.builder()
    .workspace("ws_xxxxxxxxxxxx")
    .build();

// 2. 创建 Agent
Agent agent = client.agents().create(AgentCreateParam.builder()
    .name("quickstart-assistant")
    .model("qwen-plus")
    .instructions("你是一个有帮助的助手。")
    .build());

// 3. 创建 Session
Session session = client.sessions().create(SessionCreateParam.builder()
    .agentId(agent.getId())
    .build());
System.out.println("Agent: " + agent.getId() + ", Session: " + session.getId());

// 4. 发送用户消息并流式接收回复
try (AgentStudioEventStream stream = client.sessions().events().stream(session.getId())) {
    client.sessions().events().send(session.getId(), "你好，请介绍一下自己");
    for (Message event : stream) {
        System.out.print(event);
    }
}
```

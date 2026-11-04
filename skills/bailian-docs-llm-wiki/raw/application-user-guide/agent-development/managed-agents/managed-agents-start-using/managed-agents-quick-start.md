# 快速开始

通过控制台，按 4 步完成智能体创建、环境配置、会话发起与调用。

## 控制台完成路径

[

**1\. 配置智能体**

选择模型、提示词与工具。

](#79eb0bf438ymi)[

**2\. 配置运行环境**

创建云端托管沙箱。

](#e319e0e8ee6sr)[

**3\. 确认会话配置**

核对智能体与环境的绑定。

](#bf03f3f9704tx)[

**4\. 开始对话**

在预览调试中发送第一条消息。

](#h-step4)

## 前置准备

-   已开通[阿里云百炼](https://bailian.console.aliyun.com/)。
-   当前账号在目标工作空间内具备 Managed Agents 操作权限。

下方首次对话不需要上传文件或安装 SDK。文件分析和程序调用示例放在完整控制台流程之后的可选 API 扩展中。

## 步骤 1：配置智能体

进入[百炼控制台 > Managed Agents > 快速开始](https://bailian.console.aliyun.com/cn-beijing/managed-agent/quick-start/wizard)，填写智能体的基本信息、模型与工具。页面已预填模板值，按需修改即可。

**字段**

**说明**

名称

默认 `Agent_v1`，可自定义

模型

必选。从下拉列表选择，如 `qwen3.7-plus`

系统提示词

定义智能体的角色与行为。已预填通用模板，可根据场景修改

工具

内置工具默认全选：`bash`、`write`、`read`、`edit`、`glob`、`grep`、`web_search`、`web_fetch`、`todo_write`、`mark_artifacts`。按需取消勾选

Skill / MCP

可选。快速开始阶段可跳过，后续在智能体详情页追加

填写完成后点击**完成并下一步**，系统创建并保存智能体，随后进入环境配置。

## 步骤 2：配置运行环境

环境定义工具调用的执行沙箱，与智能体独立管理。

**字段**

**说明**

名称

默认 `Agent_v1_Env`，可自定义

托管类型

默认**云端托管**（阿里云百炼托管的沙箱容器）

点击**完成并下一步**，系统创建并保存环境，随后进入会话配置。

## 步骤 3：确认会话配置

页面展示已创建的智能体与环境摘要，并基于两者自动发起会话。

-   确认**智能体**卡片中的名称、模型信息。
-   确认**环境**卡片中的名称、托管类型。
-   如需在沙箱中使用本地文件，点击**上传文件**挂载；否则直接跳过。步骤 4 的首次对话不需要文件。

点击**完成并下一步**，系统绑定智能体与环境、创建并保存会话，随后进入调用页面。

## 步骤 4：开始调用

配置完成。页面提供两个标签页：

-   **可调用 API**：展示创建事件的 curl 命令，可直接复制到终端执行。
-   **预览调试**：在页面内直接与智能体对话，实时查看事件与工具调用过程。左上角下拉框可按事件类型筛选（User、Agent、Tool、Tool\_output、Error、Model、System）。

打开**预览调试**，输入 `请简要介绍你能做什么。` 并发送，查看智能体回答和执行事件。通过程序调用时先建立 SSE 订阅再发送消息，具体顺序见下方可选扩展。

**说明**看到回答且本轮正常结束（`idle` 且 `stop_reason.type=end_turn`）即完成首次对话。`requires_action` 表示等待工具审批，不是成功；`retries_exhausted` 表示本轮失败。新建会话的 `idle` 且停止原因为空，不代表某轮任务完成；`terminated` 会话不能继续。

调试完成后，点击**返回智能体列表**进入管理页面。前三步创建的智能体、环境、会话均已保存，可随时在对应菜单中查看和编辑。后续多轮交互可复用同一 Session，`idle` 不代表删除。

## 可选：API 扩展

以下保留数据分析配置，作为控制台流程之外的可选路径。选择 curl、Python 或 Java，在同一工作空间内分三个阶段执行第 1–4 节，不混用不同版本示例的 ID。如需调用控制台已创建的资源，直接使用其实际 ID，无需重复创建。

### 初始化上下文

先按 [API 快速开始](https://help.aliyun.com/zh/model-studio/managed-agents-quickstart#h-qs-prereq) 获取 API Key、工作空间 ID，设置 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`。原始 Endpoint 形式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio`，将 `{workspace_id}` 替换为实际工作空间 ID。curl 需要 `jq`；示例使用 Python SDK 1.27.7 或 Java SDK 2.23.2（`Map.of` 需要 JDK 9+），安装方法见 [API 快速开始](https://help.aliyun.com/zh/model-studio/managed-agents-quickstart#h-qs-install)。

按以下阶段组合对应语言的片段，不把第 1–4 节一次性放入同一个程序：

1.  **资源准备**：执行共享初始化与第 1–2 节，保存打印的实际 `AGENT_ID`、`ENV_ID`，等待[环境预热](https://help.aliyun.com/zh/model-studio/managed-agents-cloud-hosting#h-env-warmup)完成。
2.  **创建会话**：重新执行共享导入与客户端初始化，仅运行第 3 节，从环境变量 `AGENT_ID`、`ENV_ID` 绑定已有资源，保存打印的实际 `SESSION_ID`。
3.  **文件与调用**：先按第 4 节将 `sales.csv` 上传并挂载到这个 `SESSION_ID`；再重新执行共享初始化，仅运行第 4 节的订阅与发送片段，从环境变量读取同一个 `SESSION_ID`。无需重新创建资源。

Python：每阶段仅用对应片段替换下方 `pass`，每行增加四个空格。官方 `Client` 上下文退出时关闭 HTTP 客户端；新进程不会保留前一阶段的 `agent`、`env` 或 `session` 对象。Java：将 [API 示例](https://help.aliyun.com/zh/model-studio/managed-agents-quickstart#h-qs-example) 的 `ManagedAgentQuickstart.java` 与下方 `ManagedAgentConsoleQuickstart.java` 放在一起，每阶段仅将对应 Java 片段插入 `main` 的注释位置，只运行控制台扩展类，不运行 API 类的资源创建入口。第 3 阶段复用公共 `runTurn`：响应头确认后发送，接收 SSE、输出文本、判断停止原因并关闭订阅；保留 120000 毫秒的业务事件等待检查，心跳不重置，同时限制 socket 无数据等待。阻塞行读取不保证精确的 120 秒墙钟截止，完整心跳行上的检查会在到期后停止，详见该 API 示例。

curl

```
set -euo pipefail
# 在此终端中使用 API 快速开始的环境变量。
# Endpoint 模板：替换 workspace_id，并复用实际返回的 Session ID。
# POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/agents
# POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/environments
# POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions
# GET  https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions/sesn_xxx/events/stream
# POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions/sesn_xxx/events
```

python

```
import os
from dashscope.agentstudio import Client
from dashscope.agentstudio.types import user_message

with Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["AGENTSTUDIO_URL"],
    workspace="ws_xxxxxxxxxxxx",
    region="cn-beijing",
) as client:
    # 仅用当前阶段的片段替换 pass，并缩进到此上下文内。
    pass
```

java

```
import com.alibaba.dashscope.agentstudio.AgentStudioClient;
import com.alibaba.dashscope.agentstudio.model.Agent;
import com.alibaba.dashscope.agentstudio.model.Configs;
import com.alibaba.dashscope.agentstudio.model.Environment;
import com.alibaba.dashscope.agentstudio.model.Session;
import com.alibaba.dashscope.agentstudio.param.AgentCreateParam;
import com.alibaba.dashscope.agentstudio.param.EnvironmentCreateParam;
import com.alibaba.dashscope.agentstudio.param.SessionCreateParam;
import com.google.gson.Gson;
import java.util.Arrays;
import java.util.Collections;
import java.util.Map;

public class ManagedAgentConsoleQuickstart {
    public static void main(String[] args) throws Exception {
        AgentStudioClient client = AgentStudioClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl(System.getenv("AGENTSTUDIO_URL"))
            .workspace("ws_xxxxxxxxxxxx").region("cn-beijing").build();
        // 在此仅插入当前阶段的 Java 片段。
    }
}
```

### 1\. 通过 API 配置智能体

指定名称、模型和工具（详见[创建 Agent API](raw/application-api-reference/managed-agents-api/agent-api/agent-create.md)）。此数据分析示例使用 `data-analyst` 和 `qwen3.8-max`，与控制台模板值不同。

bash

```
AGENT_ID=$(curl -fsS -X POST "$AGENTSTUDIO_URL/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-analyst",
    "model": {"id": "qwen3.8-max"},
    "system": "你是数据分析专家，使用 pandas 处理 CSV 文件。",
    "tools": [
      {
        "type": "builtin_toolkit",
        "default_config": {"enabled": true},
        "configs": [
          {"name": "bash", "enabled": true},
          {"name": "read", "enabled": true},
          {"name": "write", "enabled": true}
        ]
      }
    ]
  }' | jq -er '.id')
printf 'Agent: %s\n' "$AGENT_ID"
```

python

```
agent = client.agents.create(
    name="data-analyst",
    model="qwen3.8-max",
    system_prompt="你是数据分析专家，使用 pandas 处理 CSV 文件。",
    tools=[
        {"type": "builtin_toolkit",
         "default_config": {"enabled": True},
         "configs": [
             {"name": "bash", "enabled": True},
             {"name": "read", "enabled": True},
             {"name": "write", "enabled": True},
          ]}
    ],
)
print(agent.id)       # "agent_xxx"
print(agent.version)  # 1
```

java

```
Configs.ToolConfig toolkit = new Gson().fromJson(
    "{\"type\":\"builtin_toolkit\",\"default_config\":{\"enabled\":true},"
    + "\"configs\":[{\"name\":\"bash\",\"enabled\":true},"
    + "{\"name\":\"read\",\"enabled\":true},{\"name\":\"write\",\"enabled\":true}]}",
    Configs.ToolConfig.class);
Agent agent = client.agents().create(AgentCreateParam.builder()
    .name("data-analyst")
    .model("qwen3.8-max")
    .systemPrompt("你是数据分析专家，使用 pandas 处理 CSV 文件。")
    .tools(Collections.singletonList(toolkit))
    .build());
System.out.println(agent.getId());       // "agent_xxx"
System.out.println(agent.getVersion());  // 1
```

### 2\. 通过 API 配置运行环境

指定沙箱类型与预装包（详见[创建 Environment API](raw/application-api-reference/managed-agents-api/environment-api/environment-create.md)）。本例安装 `apt: ffmpeg`、`pip: pandas, numpy, matplotlib`，并设置 `networking.type=unrestricted`。

bash

```
ENV_ID=$(curl -fsS -X POST "$AGENTSTUDIO_URL/environments" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-sandbox",
    "description": "数据分析沙箱",
    "config": {
      "type": "cloud",
      "packages": {
        "apt": ["ffmpeg"],
        "pip": ["pandas", "numpy", "matplotlib"]
      },
      "networking": {"type": "unrestricted"}
    }
  }' | jq -er '.id')
printf 'Environment: %s\n' "$ENV_ID"
```

python

```
env = client.environments.create(
    name="data-sandbox",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
        "packages": {
            "apt": ["ffmpeg"],
            "pip": ["pandas", "numpy", "matplotlib"],
        },
    },
    description="数据分析沙箱",
)
print(env.id)
```

java

```
Map<String, Object> config = Map.of(
    "type", "cloud",
    "networking", Map.of("type", "unrestricted"),
    "packages", Map.of(
        "apt", Arrays.asList("ffmpeg"),
        "pip", Arrays.asList("pandas", "numpy", "matplotlib")));
Environment env = client.environments().create(EnvironmentCreateParam.builder()
    .name("data-sandbox")
    .description("数据分析沙箱")
    .config(config)
    .build());
System.out.println(env.getId());
```

**说明**API 示例配置了预装包：环境创建后可能需要数分钟或更长的预热时间。预热完成前第 3 节的会话创建会被拒绝，返回 `invalid_parameter`：`The environment is still being prepared. Please wait until it is ready and try again.` 等待准备完成后再继续，详见[环境预热](https://help.aliyun.com/zh/model-studio/managed-agents-cloud-hosting#h-env-warmup)。

片段不会自动等待。第 1 阶段（第 1–2 节）保存打印的 Agent、Environment ID；预热完成后，仅执行第 2 阶段（第 3 节）创建 Session，保存 Session ID；上传并挂载文件后，再执行第 3 阶段（第 4 节）调用。Session 创建被拒绝时，准备完成后只重试会话创建，不重复创建 Agent 或 Environment。

### 3\. 通过 API 确认会话配置

绑定前两节返回的智能体与环境 ID（详见[创建 Session API](raw/application-api-reference/managed-agents-api/session-api/session-create.md)）。`agent_xxx`、`env_xxx`、`sesn_xxx` 表示实际返回的 ID，不是可互换的固定值。

Python、Java 的第 2 阶段启动前，在启动进程的终端导出保存的 ID，将下方占位值替换为第 1 阶段打印的实际值，并重新执行共享导入与客户端初始化。新终端还需设置相同的 API Key 和 Endpoint。curl 在原终端继续时保留已有 `AGENT_ID`、`ENV_ID`，不要用占位值覆盖它们。

```
# 替换为第 1 阶段打印的实际 ID 后再执行。
export AGENT_ID="agent_xxx"
export ENV_ID="env_xxx"
```

bash

```
SESSION_ID=$(curl -fsS -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"agent\": {\"type\": \"agent\", \"id\": \"$AGENT_ID\"}, \"environment_id\": \"$ENV_ID\", \"title\": \"Q3 销售数据分析\"}" | jq -er '.id')
export SESSION_ID
printf 'Session: %s\n' "$SESSION_ID"
```

python

```
session = client.sessions.create(
    agent={"type": "agent", "id": os.environ["AGENT_ID"]},
    environment_id=os.environ["ENV_ID"],
    title="Q3 销售数据分析",
)
print(session.id, session.status)
```

java

```
Session session = client.sessions().create(SessionCreateParam.builder()
    .agent(Map.of("type", "agent", "id", System.getenv("AGENT_ID")))
    .environmentId(System.getenv("ENV_ID"))
    .title("Q3 销售数据分析")
    .build());
System.out.println(session.getId() + " " + session.getStatus());
```

### 4\. 通过 API 开始调用：可选文件分析

Python、Java 第 3 阶段启动前，在启动进程的终端导出第 2 阶段打印的实际 Session ID（不包含后面的状态），然后重新执行共享导入与客户端初始化；保持 API Key 和 Endpoint 不变。curl 在原终端保留第 3 节已导出的变量。

```
# 将占位值替换为第 2 阶段打印的实际 Session ID。
export SESSION_ID="sesn_xxx"
```

**发送分析任务前**，先上传 `sales.csv`，待审核状态为 `available` 后挂载到此 Session。挂载路径填写 `/sales.csv`，服务端自动加上 `/mnt/session/uploads` 前缀，智能体实际访问 `/mnt/session/uploads/sales.csv`。可使用控制台**上传文件**，或按[文件上传与挂载](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)操作。上方创建 Session 的代码不会上传或挂载本地文件，添加文件时保持同一 Session ID。

先订阅 [SSE 事件流](raw/application-api-reference/managed-agents-api/session-api/event-sse-stream.md)，再[发送 Event](raw/application-api-reference/managed-agents-api/session-api/event-post.md)。SSE 不回放历史，断线恢复见[客户端流式接收与恢复](raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)。

curl：在**终端 A** 执行以下订阅。在此新终端中设置相同的 API Key、Endpoint，并复制第 3 节打印的实际 `SESSION_ID`。保持连接运行，确认 2xx 响应与 `Content-Type: text/event-stream` 后，再在**终端 B** 提交任务，不使用固定延时判断连接就绪。

```
export SESSION_ID="sesn_xxx"
curl -N -i "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events/stream" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Accept: text/event-stream"
```

终端 B 保持相同的 `SESSION_ID`。下方 Python、Java 片段在第 3 阶段重新运行的初始化上下文中组合订阅与发送，仅引用环境变量中的 Session ID，不依赖第 2 阶段的 `session` 对象。Python 1.27.7 在 `stream()` 返回前打开 HTTP 连接；Java 的 `runTurn` 检查 HTTP 状态、内容类型并打开输入流后再通过 SDK 发送，仅调用 SDK 的 `stream()` 不保证连接就绪。

bash

```
curl -fsS -X POST "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      {
        "role": "user",
        "type": "message",
        "content": [
          {"type": "text", "text": "分析 /mnt/session/uploads/sales.csv 中 Q3 的销售趋势"}
        ]
      }
    ]
  }'
```

python

```
session_id = os.environ["SESSION_ID"]
with client.sessions.events.stream(session_id, timeout=120.0) as stream:
    client.sessions.events.send(
        session_id,
        events=[user_message("分析 /mnt/session/uploads/sales.csv 中 Q3 的销售趋势")],
    )
    for event in stream:
        if event.type == "message":
            for block in (event.content or []):
                if getattr(block, "type", None) == "text":
                    print(block.text, end="", flush=True)
        elif event.type == "session_status":
            state = event.session_status
            reason = (event.stop_reason or {}).get("type")
            if state == "terminated":
                print("会话已终止，不能继续。")
                break
            if state == "idle" and reason in (
                "end_turn", "requires_action", "retries_exhausted"
            ):
                print({
                    "end_turn": "本轮正常完成。",
                    "requires_action": "等待工具审批，请处理审批或中断本轮。",
                    "retries_exhausted": "本轮失败，请查看错误事件。",
                }[reason])
                break
        else:
            print(event, flush=True)
```

java

```
ManagedAgentQuickstart.runTurn(client, System.getenv("SESSION_ID"),
    "分析 /mnt/session/uploads/sales.csv 中 Q3 的销售趋势");
```

**说明**预期收到 Q3 销售分析并以 `end_turn` 正常结束。POST 成功仅表示任务入队，`running` 时继续接收，新建会话 `idle` 且停止原因为空时不退出；按步骤 4 区分正常完成、等待审批、重试耗尽与终止。断线或超时时任务结果为 `UNKNOWN`，不是成功信号；应查询 Session 状态（Java `client.sessions().retrieve(System.getenv("SESSION_ID"))`）与历史，不自动重发任务。关闭订阅不会终止会话。

## 资源与会话管理

保存返回的 ID，本轮正常完成后可复用 Session 继续交互。输入文件见[文件上传与挂载](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)，输出产物取回见[数据分析：取回产物](https://help.aliyun.com/zh/model-studio/managed-agents-data-analysis#h-da-step6)；审批、中断和终止见[会话操作](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)。归档 Session 会终止会话并保留历史，删除 Session 会不可逆地删除元数据和历史；Environment 的归档、删除独立管理。仅 `running` 时计收运行时长费用，`idle` 不计该运行时长费用，详见[计费说明](raw/application-user-guide/agent-billing/managed-agents-billing.md)。

## 下一步

[

**管理会话与事件**

创建会话、发送消息与事件流。

](raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)[

**智能体**

配置模型、提示词与工具。

](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent.md)[

**配置运行环境**

沙箱类型、预装包与网络策略。

](raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)

业务代码集成见[概览](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)与 [API 快速开始](raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

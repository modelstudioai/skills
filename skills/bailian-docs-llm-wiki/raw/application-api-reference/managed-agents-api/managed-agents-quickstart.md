# 快速开始

五分钟跑通 Managed Agents 全链路：创建 Agent 与 Environment、开启 Session、提交任务并流式接收执行结果。

## 调用流程

[

**1\. 创建 Agent**

定义模型与系统提示词。

](#h-qs-agent)[

**2\. 创建 Environment**

配置工具执行的沙箱。

](#h-qs-environment)[

**3\. 创建 Session**

绑定 Agent 与 Environment。

](#h-qs-session)[

**4\. 建立 SSE 连接**

确认订阅连接就绪，再提交任务。

](#h-qs-stream)[

**5\. 发送 Event**

提交任务，读取输出与停止原因。

](#h-qs-send)

## 前提

1.  已开通阿里云百炼并创建 API Key（`sk-xxx`），已获取工作空间 ID（`ws_xxxxxxxxxxxx`），详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
2.  将 API Key 与 Endpoint 导出为环境变量。将占位值替换为实际值，后续操作保持同一工作空间：

```
export DASHSCOPE_API_KEY="sk-xxx"
export AGENTSTUDIO_URL="https://ws_xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio"
```

curl 示例需要 `curl` 和 `jq`。Java 示例使用 `Map.of`，需要 JDK 9 及以上。以下示例采用 Python SDK **1.27.7**、Java SDK **2.23.2**。

## 安装 SDK

使用 Python 或 Java SDK 前，请先安装对应的 DashScope 包。Managed Agents 模块要求 Python SDK v1.26.2 及以上、Java SDK v2.22.24 及以上。若已安装旧版本，请升级。

会话级智能体配置覆盖（`agent` 对象与 patch）和会话级 MCP 请求头（`mcp_configs`）需要 Python SDK v1.27.7 及以上、Java SDK v2.23.2 及以上；直接调用 REST 接口不受此限制，版本要求详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。运行本页示例时使用以下固定版本：

Python

```
pip install dashscope==1.27.7
```

Maven

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>2.23.2</version>
</dependency>
```

## 端到端示例

创建一个代码生成 Agent，开启 Session，然后要求它编写一个接收整数列表、返回去重后有序列表的 Python 函数。选择 curl 或一种 SDK 执行，不必运行所有版本重复创建资源。

### 1\. 创建 Agent

指定 `name`、`model` 与系统提示词（REST 为 `system`，Python 为 `system_prompt`，Java 为 `systemPrompt`）。本例使用 `quickstart-coder` 和 `qwen-plus`，得到 `agent_xxx`。Agent 通常只创建一次并长期复用。

### 2\. 创建 Environment

以 `config.type=cloud` 创建 `quickstart-env`，得到 `env_xxx`。Environment 独立管理，通常只创建一次并长期复用。

本例未配置预装包。如果追加 `apt`、`pip` 或 `npm` 包，安装可能需要数分钟或更长时间。预热完成前创建 Session 会被拒绝，返回 `invalid_parameter`：`The environment is still being prepared. Please wait until it is ready and try again.` 详见[环境预热](https://help.aliyun.com/zh/model-studio/managed-agents-cloud-hosting#h-env-warmup)。

### 3\. 创建 Session

绑定 `agent={"type":"agent","id":AGENT_ID}` 和 `environment_id=ENV_ID`，得到 `sesn_xxx`。保存业务会话与 Session ID 的映射：同一 Session 支持多轮交互并保留上下文，回到 `idle` 不会删除会话。

### 4\. 建立 SSE 连接

通过 `GET /sessions/{id}/events/stream` 和 `Accept: text/event-stream` 订阅事件，**确认 HTTP 连接就绪后**再提交任务。SSE 推送实时事件，**不回放历史**。断线重连与历史补齐见[客户端流式接收与恢复](raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)。

Python SDK 1.27.7 在 `stream()` 返回前同步打开 HTTP 流，可以先进入流上下文，再调用 `send()`。Java SDK 2.23.2 的 `AgentStudioEventStream` 异步建立连接，没有公开的连接就绪等待接口，因此下例用标准 `HttpURLConnection` 接收 SSE，检查响应头后再通过 SDK 发送。`Message`、`ClientEvents` 位于 `.message` 包，SDK 流类位于 `.resource`，不在 `.model` 包中。

### 5\. 发送 Event 并读取结果

向 `POST /sessions/{id}/events` 提交 `input`，其中包含用户 `message` 和 `text` 内容块。HTTP 200 表示输入已入队，执行会异步进入 `running`；结果通过已建立的 SSE 连接接收，不在 POST 响应中返回。

根据 `session_status` 事件的 `content[].data.session_status` 和 `content[].data.stop_reason` 判断结果。Python 分别提供可空字符串 `event.session_status` 和可空字典 `event.stop_reason`。Message 顶层的 `status=completed` 表示消息完整性，不是 Session 状态。

Session 状态

停止原因

含义与后续动作

`running`

`null`

继续接收事件。

`idle`

`null`

新建会话可能处于空闲状态，不能据此认定刚提交的任务已完成。

`idle`

`end_turn`

本轮正常完成，可复用同一 Session 发起下一轮。

`idle`

`requires_action`

等待工具审批，需要处理审批或中断本轮，不是执行成功。

`idle`

`retries_exhausted`

重试耗尽，本轮失败；发起下一轮前先查看错误。

`terminated`

不解读

会话已终止，不能继续。

### curl：两个终端

**在终端 B 创建资源。** 每步打印响应 ID，下一步复用该 ID；请求失败时停止，暂不提交任务。

```
set -euo pipefail
# 1. 创建 Agent
AGENT_ID=$(curl -fsS -X POST "$AGENTSTUDIO_URL/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "quickstart-coder",
    "model": {"id": "qwen-plus"},
    "system": "你是一位 Python 专家。用户提交编码任务后，直接输出简洁、可运行的 Python 代码。"
  }' | jq -er '.id')
printf 'Agent: %s\n' "$AGENT_ID"

# 2. 创建 Environment
ENV_ID=$(curl -fsS -X POST "$AGENTSTUDIO_URL/environments" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "quickstart-env", "config": {"type": "cloud"}}' | jq -er '.id')
printf 'Environment: %s\n' "$ENV_ID"

# 3. 创建 Session
SESSION_ID=$(curl -fsS -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"agent\": {\"type\": \"agent\", \"id\": \"$AGENT_ID\"}, \"environment_id\": \"$ENV_ID\"}" | jq -er '.id')
export SESSION_ID
printf 'Session: %s\n' "$SESSION_ID"
```

**在终端 A 建立连接。** 在新终端中按前提设置相同的 `DASHSCOPE_API_KEY`、`AGENTSTUDIO_URL`；不同终端不会共享 shell 变量。将终端 B 打印的 Session ID 复制到下方 `SESSION_ID`。保持终端 A 运行，看到成功 HTTP 响应（2xx）和 `Content-Type: text/event-stream` 后再继续；响应错误时停止，不提交任务。

```
export SESSION_ID="sesn_xxx"
# 4. 订阅 SSE，并显示响应头
curl -N -i "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events/stream" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Accept: text/event-stream"
```

**仅在终端 A 连接就绪后，在终端 B 提交任务。** 保持相同的 `SESSION_ID` 和环境变量，在终端 A 读取事件并按上表判断结果。Ctrl+C 只关闭当前订阅，不会终止 Session。

```
# 5. 提交任务
curl -fsS -X POST "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      {"role": "user", "type": "message",
       "content": [{"type": "text", "text": "写一个 Python 函数，接收一个整数列表并返回去重后的有序列表。"}]}
    ]
  }'
```

### SDK：选择 Python 或 Java

Python 的 `Client` 上下文负责关闭 HTTP 客户端。Java 示例保存为 `ManagedAgentQuickstart.java`；`runTurn` 建立订阅、提交一次任务，并在正常完成、等待审批或失败时关闭订阅，不调用 `terminateSession`。

Java 示例不保证恰在 120 秒墙钟时刻退出；超时结果保持 `UNKNOWN`。先查询 Session 状态和事件历史，不自动重发任务。

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
    # 1. 创建 Agent
    agent = client.agents.create(
        name="quickstart-coder",
        model="qwen-plus",
        system_prompt="你是一位 Python 专家。用户提交编码任务后，直接输出简洁、可运行的 Python 代码。",
    )
    # 2. 创建 Environment
    env = client.environments.create(name="quickstart-env", config={"type": "cloud"})
    # 3. 创建 Session
    session = client.sessions.create(
        agent={"type": "agent", "id": agent.id}, environment_id=env.id
    )
    print(f"Agent: {agent.id}, Environment: {env.id}, Session: {session.id}")

    # 4. 先建立 HTTP 流连接
    with client.sessions.events.stream(session.id, timeout=120.0) as stream:
        # 5. 提交任务，再接收事件
        client.sessions.events.send(
            session.id,
            events=[user_message("写一个 Python 函数，接收一个整数列表并返回去重后的有序列表。")],
        )
        for event in stream:
            print(event, flush=True)
            if event.type != "session_status":
                continue
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
```

java

```
import com.alibaba.dashscope.agentstudio.AgentStudioClient;
import com.alibaba.dashscope.agentstudio.model.Agent;
import com.alibaba.dashscope.agentstudio.model.Environment;
import com.alibaba.dashscope.agentstudio.model.Session;
import com.alibaba.dashscope.agentstudio.param.AgentCreateParam;
import com.alibaba.dashscope.agentstudio.param.EnvironmentCreateParam;
import com.alibaba.dashscope.agentstudio.param.SessionCreateParam;
import com.alibaba.dashscope.agentstudio.message.ClientEvents;
import com.alibaba.dashscope.agentstudio.message.ContentBlock;
import com.alibaba.dashscope.agentstudio.message.Message;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Map;

public class ManagedAgentQuickstart {
    public static void main(String[] args) throws Exception {
        AgentStudioClient client = AgentStudioClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl(System.getenv("AGENTSTUDIO_URL"))
            .workspace("ws_xxxxxxxxxxxx").region("cn-beijing").build();
        // 1. 创建 Agent
        Agent agent = client.agents().create(AgentCreateParam.builder()
            .name("quickstart-coder").model("qwen-plus")
            .systemPrompt("你是一位 Python 专家。用户提交编码任务后，直接输出简洁、可运行的 Python 代码。")
            .build());
        // 2. 创建 Environment
        Environment env = client.environments().create(EnvironmentCreateParam.builder()
            .name("quickstart-env").config(Map.of("type", "cloud")).build());
        // 3. 创建 Session
        Session session = client.sessions().create(SessionCreateParam.builder()
            .agent(Map.of("type", "agent", "id", agent.getId()))
            .environmentId(env.getId()).build());
        System.out.println("Agent: " + agent.getId() + ", Environment: " + env.getId()
            + ", Session: " + session.getId());
        runTurn(client, session.getId(),
            "写一个 Python 函数，接收一个整数列表并返回去重后的有序列表。");
    }

    public static void runTurn(AgentStudioClient client, String sessionId, String prompt)
            throws Exception {
        String baseUrl = System.getenv("AGENTSTUDIO_URL").replaceAll("/+$", "");
        HttpURLConnection connection = (HttpURLConnection) new URL(
            baseUrl + "/sessions/" + sessionId + "/events/stream").openConnection();
        connection.setRequestMethod("GET");
        connection.setInstanceFollowRedirects(false);
        connection.setRequestProperty("Authorization", "Bearer " + System.getenv("DASHSCOPE_API_KEY"));
        connection.setRequestProperty("Accept", "text/event-stream");
        connection.setConnectTimeout(30_000);
        connection.setReadTimeout(120_000);
        try {
            // 4. 等待响应头，而非第一条业务事件
            int status = connection.getResponseCode();
            String contentType = connection.getContentType();
            if (status < 200 || status >= 300 || contentType == null
                    || !contentType.toLowerCase(java.util.Locale.ROOT).startsWith("text/event-stream")) {
                throw new IllegalStateException("SSE connection failed: HTTP " + status + ", " + contentType);
            }
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                    connection.getInputStream(), StandardCharsets.UTF_8))) {
                // 5. SSE 就绪后，通过独立的 SDK 连接发送任务
                client.sessions().events().send(sessionId,
                    Collections.singletonList(ClientEvents.userMessage(prompt)));
                Gson gson = new GsonBuilder()
                    .registerTypeAdapter(ContentBlock.class, new ContentBlock.Deserializer()).create();
                StringBuilder payload = new StringBuilder();
                long lastBusinessEventNanos = System.nanoTime();
                while (true) {
                    checkBusinessEventTimeout(lastBusinessEventNanos);
                    String line = reader.readLine();
                    checkBusinessEventTimeout(lastBusinessEventNanos);
                    if (line == null) break;
                    if (line.startsWith("data:")) {
                        String value = line.substring(5);
                        if (value.startsWith(" ")) value = value.substring(1);
                        payload.append(value).append('\n');
                    } else if (line.isEmpty() && payload.length() > 0) {
                        Message event = gson.fromJson(payload.toString(), Message.class);
                        payload.setLength(0);
                        if (event == null || event.getType() == null) continue;
                        lastBusinessEventNanos = System.nanoTime();
                        if ("message".equals(event.getType()) && event.getContent() != null) {
                            for (ContentBlock block : event.getContent()) {
                                if (block instanceof ContentBlock.Text)
                                    System.out.print(((ContentBlock.Text) block).getText());
                            }
                        } else {
                            System.out.println(event);
                        }
                        if (!"session_status".equals(event.getType())) continue;
                        JsonObject data = event.getData();
                        if (data == null || !data.has("session_status")
                                || data.get("session_status").isJsonNull()) continue;
                        String state = data.get("session_status").getAsString();
                        if ("terminated".equals(state)) {
                            System.out.println("会话已终止，不能继续。");
                            break;
                        }
                        Session.StopReason stop = event.getStopReason();
                        String reason = stop == null ? null : stop.getType();
                        if (!"idle".equals(state)) continue;
                        if ("end_turn".equals(reason)) {
                            System.out.println("本轮正常完成。");
                            break;
                        } else if ("requires_action".equals(reason)) {
                            System.out.println("等待工具审批，请处理审批或中断本轮。");
                            break;
                        } else if ("retries_exhausted".equals(reason)) {
                            System.out.println("本轮失败，请查看错误事件。");
                            break;
                        }
                    }
                }
            }
        } finally {
            connection.disconnect();
        }
    }

    private static void checkBusinessEventTimeout(long lastBusinessEventNanos)
            throws SocketTimeoutException {
        if (System.nanoTime() - lastBusinessEventNanos >= 120_000L * 1_000_000L) {
            throw new SocketTimeoutException("No complete business event within 120000 ms; outcome UNKNOWN. "
                + "Query Session state and event history; do not automatically resubmit.");
        }
    }
}
```

Java 超时与恢复细节

Java 保留 120000 毫秒的业务事件等待语义：从开始消费时用 `System.nanoTime()` 计时，每次 `readLine()` 前后检查，仅在解析出完整 SSE 帧中的非空 `Message` 且 `type` 非空时重置；注释、心跳和未完成帧不重置。`setReadTimeout(120_000)` 另行限制底层 socket 无数据等待。阻塞读取没有 watchdog，因此不保证恰在 120 秒墙钟时刻退出；持续收到标准的完整心跳行时，会在期限后的行检查抛出 `SocketTimeoutException`，而不是无限等待。异常会关闭读取流并断开连接，任务结果保持 `UNKNOWN`；先查询 Session 状态（Java `client.sessions().retrieve(sessionId)`）和事件历史，不自动重发。

## 结果与会话管理

**说明**预期收到生成的 Python 代码，随后出现 `session_status=idle`、`stop_reason.type=end_turn`。`requires_action` 表示等待审批，`retries_exhausted` 表示本轮失败。断线或读取超时本身不能判定任务结果，结果保持 `UNKNOWN`；应先查询 Session 状态（Java `client.sessions().retrieve(sessionId)`）和事件历史，再决定后续动作，不自动重发任务。

保存返回的 Agent、Environment 和 Session ID。Agent、Environment 可跨会话复用，本轮正常完成后可复用同一 Session 继续交互。下一轮仍先建立订阅再发送消息。审批、中断和终止操作见[会话操作](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)；输入文件见[文件上传与挂载](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)，输出产物取回见[数据分析：取回产物](https://help.aliyun.com/zh/model-studio/managed-agents-data-analysis#h-da-step6)。

关闭 SSE 只关闭订阅。归档 Session 会终止会话并保留历史，删除 Session 会不可逆地删除元数据和历史；Environment 的归档与删除独立管理。Session 仅在 `running` 时按运行时长计费，`idle` 不计该运行时长费用，详见[计费说明](raw/application-user-guide/agent-billing/managed-agents-billing.md)。

## 下一步

[

**客户端流式接收与恢复**

断线后结合事件历史补齐实时输出。

](raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)[

**会话与资源**

管理多轮交互、审批、输入文件与输出产物。

](raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)[

**运行环境**

配置预装包、网络策略与环境生命周期。

](raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)

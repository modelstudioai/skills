# 发起会话

会话承载智能体的一次运行实例，全部消息、工具调用与状态变更以事件形式实时记录。

## 会话（Session）

会话是智能体的一次运行实例，承载多轮消息、工具调用与状态变更。控制台**新建会话**用于调试；生产环境通过 API 创建与驱动，详见 [Session API](raw/application-api-reference/managed-agents-api/session-api.md)。

### 新建会话

在智能体详情页点击**新建会话**，绑定运行环境（必选）后进入会话页面。创建时服务端快照当时的智能体配置，后续编辑智能体不影响已有会话。

通过 API 创建会话时，需绑定智能体与运行环境，服务端自动快照当前智能体配置。完整参数与响应字段详见[创建 Session API](raw/application-api-reference/managed-agents-api/session-api/session-create.md)。

bash

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "environment_id": "env_xxx",
    "title": "Q3 销售数据分析",
    "resources": [
      {"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"}
    ]
  }'
```

python

```
session = client.sessions.create(
    agent="agent_xxx",
    environment_id="env_xxx",
    title="Q3 销售数据分析",
    resources=[
        {"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"},
    ],
)
print(session.id, session.status)
```

java

```
Session session = client.sessions().create(SessionCreateParam.builder()
    .agent("agent_xxx")
    .environmentId("env_xxx")
    .title("Q3 销售数据分析")
    .resources(List.of(SessionResource.builder()
        .type("file")
        .fileId("file_xxx")
        .mountPath("/workspace/data.csv")
        .build()))
    .build());
System.out.println(session.getId() + " " + session.getStatus());
```

### 会话页面布局

-   **事件面板**：实时展示当轮的处理过程。左上角下拉框可按类型筛选事件（All events / User / Agent / Tool / Tool\_output / Error / Model / System）。
-   **右侧标签页**：**智能体**、**环境**、**环境变量**、**记忆**、**文件**、**密钥库**标签页，分别查看当前会话快照的配置；**记忆**展示会话挂载的记忆资源。
-   **输入区**：底部输入框输入消息，点击**发送**提交；处理中可点击**中断**停止当前轮。

### 挂载资源

在会话页面的**资源**区上传或挂载已有文件，智能体在工具调用中按 `mount_path` 读写。详见[文件上传与挂载](raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。运行时也可通过 API 动态挂载、查询与卸载文件资源，详见 [Session API](raw/application-api-reference/managed-agents-api/session-api.md)。

记忆库在创建会话时于**资源**区点击 **+** 挂载，配置记忆库、权限与说明；创建后不可新增、卸载或修改。详见[记忆库](raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

### 归档与删除

会话支持归档和删除两种操作：

-   **归档**：状态变为 `terminated`（终态），事件历史保留可查。适用于已完成的会话。
-   **删除**：硬删除，会话元数据、事件历史、内部拷贝的资源全部清除，不可恢复。如需保留事件历史请改用归档。

## 下一步

-   [管理会话](raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)：了解状态机、工具调用流程与归档删除。
-   [会话事件流（SSE）](raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)：了解全部事件类型与 SSE 订阅。
-   [Session API](raw/application-api-reference/managed-agents-api/session-api.md)：用 API 创建会话、发消息、订阅事件流。

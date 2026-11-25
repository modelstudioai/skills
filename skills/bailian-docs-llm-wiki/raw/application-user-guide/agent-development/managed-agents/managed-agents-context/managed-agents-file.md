# 文件上传与挂载

文件是独立管理的资源，可被多个会话挂载，生命周期与会话解耦。在控制台文件菜单上传与管理。

<a id="配额与限制"></a>

<a id="h-file-quota"></a>

## 配额与限制

-   单个文件最大 **50 MB**。
-   单个工作空间下文件总容量上限 **100 GB**。
-   文件保存时效 **30 天**，超期可能被自动清理。需要长期保留请定期重新上传。

<a id="上传"></a>

<a id="h-file-upload"></a>

## 上传

在**文件**页面点击**上传文件**，从本地选择文件后上传。上传后文件进入安全审核（`checking`），审核通过变为 `available` 后才可挂载到会话。审核未通过则标记为 `rejected` 或 `type_rejected`。

通过 API 上传文件，以 multipart/form-data 方式提交。完整参数与响应字段详见 [File API](../../../../application-api-reference/managed-agents-api/files-api/file-upload.md)。

<a id="fig-code-group"></a>

<a id="fig-code-group-bash-tab"></a>

bash

<a id="code-code-group-bash"></a>

```bash
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -F "file=@./sales_2025.csv"
```

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
file = client.files.upload("sales_2025.csv")
print(file.id)
```

<a id="fig-code-group-java-tab"></a>

java

<a id="code-code-group-java"></a>

```java
AgentStudioFile file = client.files().upload(Paths.get("sales_2025.csv"), "text/csv");
System.out.println(file.getId());
```

<a id="会话隔离"></a>

<a id="h-file-isolation"></a>

## 会话隔离

将文件挂载到会话时，服务端会做一份内部拷贝挂入会话沙箱，原始文件不受会话内修改影响。可在会话详情查看挂载文件的实际副本。

<a id="挂载到会话"></a>

<a id="h-mount"></a>

## 挂载到会话

<a id="创建会话时挂载"></a>

<a id="h-mount-create"></a>

### 创建会话时挂载

在**新建会话**抽屉的**挂载资源**区点击**添加文件**，选择已上传的文件，填写挂载路径，例如 `/workspace/data.csv`。

<a id="运行时挂载"></a>

### 运行时挂载

会话已创建后，在会话页面右侧**资源**面板点击**挂载文件**追加。挂载实时生效，无需重启会话。

<a id="路径前缀"></a>

<a id="h-mount-path"></a>

### 路径前缀

填写的挂载路径会被加上 `/mnt/session/uploads` 前缀。例如：

| 填写路径 |  | 实际路径（智能体看到的） |
| --- | --- | --- |
| `/workspace/data.csv` | → | `/mnt/session/uploads/workspace/data.csv` |
| `/data/sales.xlsx` | → | `/mnt/session/uploads/data/sales.xlsx` |

智能体在工具调用中应使用**实际路径**访问。在系统提示词中可直接告知完整路径，例如：数据文件位于 `/mnt/session/uploads/workspace/data.csv`。

<a id="卸载"></a>

### 卸载

在**资源**面板对应文件行点击**卸载**。卸载后会话内的副本被清理，原始文件不变。

通过 API 挂载文件：创建会话时通过 `resources` 字段挂载；会话运行中通过 **POST** `/sessions/{session_id}/resources` 追加。完整参数与响应字段详见 [Session API](../managed-agents-session.md)。

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-bash-tab"></a>

bash

<a id="code-code-group-2-bash"></a>

```bash
# 创建会话时挂载
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": {"type": "agent", "id": "agent_xxx"},
    "environment_id": "env_xxx",
    "resources": [
      {"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"}
    ]
  }'

# 运行时追加挂载
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions/sesn_xxx/resources" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/late.csv"}'
```

<a id="fig-code-group-2-python-tab"></a>

python

<a id="code-code-group-2-python"></a>

```python
# 创建会话时挂载
session = client.sessions.create(
    agent={"type": "agent", "id": "agent_xxx"},
    environment_id="env_xxx",
    resources=[
        {"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"},
    ],
)

# 运行时追加挂载
resource = client.sessions.resources.create(
    "sesn_xxx",
    type="file",
    file_id="file_xxx",
    mount_path="/workspace/late.csv",
)
```

<a id="fig-code-group-2-java-tab"></a>

java

<a id="code-code-group-2-java"></a>

```java
// 创建会话时挂载
Session session = client.sessions().create(SessionCreateParam.builder()
    .agent(SessionAgent.ofOverride(Map.of("type", "agent", "id", "agent_xxx")))
    .environmentId("env_xxx")
    .resources(List.of(SessionResource.builder()
        .type("file")
        .fileId("file_xxx")
        .mountPath("/workspace/data.csv")
        .build()))
    .build());

// 运行时追加挂载
SessionResource resource = client.sessions().resources().create("sesn_xxx",
    SessionResourceCreateParam.builder()
        .type("file")
        .fileId("file_xxx")
        .mountPath("/workspace/late.csv")
        .build());
```

<a id="删除"></a>

<a id="h-file-delete"></a>

## 删除

文件只支持删除，不支持归档。在**文件**页面点击对应文件行的**删除**，文件将被硬删除，不可恢复。已挂载到会话的副本不受影响。

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-bash-tab"></a>

bash

<a id="code-code-group-3-bash"></a>

```bash
curl -X DELETE "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files/file_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-3-python-tab"></a>

python

<a id="code-code-group-3-python"></a>

```python
client.files.delete("file_xxx")
```

<a id="fig-code-group-3-java-tab"></a>

java

<a id="code-code-group-3-java"></a>

```java
client.files().delete("file_xxx");
```

<a id="下一步"></a>

## 下一步

-   [发起会话](../../../../application-api-reference/managed-agents-api/session-api/session-create.md)：在会话中观察工具如何使用挂载的文件。
-   [运行环境](../managed-agents-environment.md)：配置工具调用的执行沙箱。

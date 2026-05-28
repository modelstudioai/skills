# 为 OpenClaw 配置长期记忆插件

OpenClaw Agent 默认无法跨会话记忆用户偏好。阿里云百炼提供的记忆插件通过长期记忆 API 实现跨会话上下文感知：对话结束后自动提取关键信息并存储，下次对话前自动召回相关记忆。

## **效果对比**

以下两段对话展示同一场景下，默认 Agent 与使用长期记忆插件后的 Agent 行为差异。

**默认 Agent（无记忆）**

**启用长期记忆插件后的 Agent**

**第一次对话：**

用户：我在做一个 Python 项目，用的是 FastAPI 框架。

Agent：好的，FastAPI 是一个高性能的 Web 框架。需要什么帮助？

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8105093771/p1060560.png)

**第二次对话（新会话）：**

用户：帮我写个接口。

Agent：使用的是什么语言和接口？

Agent 无法记住上一轮的对话内容。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8105093771/p1060578.png)

**第一次对话：**

用户：我在做一个 Python 项目，用的是 FastAPI 框架。

Agent：好的，FastAPI 是一个高性能的 Web 框架。需要什么帮助？

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8105093771/p1060560.png)

**第二次对话（新会话）：**

用户：帮我写个接口。

Agent 检索到相关记忆： “用户正在做一个 FastAPI 框架的 Python 项目。”

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8105093771/p1060574.png)

Agent 开始帮助写接口。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8105093771/p1060575.png)

## 工作原理

记忆插件在 OpenClaw Gateway 内运行，通过两个生命周期钩子（before\_agent\_start和agent\_end）与阿里云百炼长期记忆 API 交互。所有读写操作通过 HTTPS 请求发送至阿里云百炼服务端，由阿里云百炼完成提炼、向量化和语义检索。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5526316771/CAEQaxiBgMC3_PSS6BkiIDc5Yjg1MmE2NzQyMTQ3YjA4YmI4ZTM0NjhlOWNmM2E16761471_20260319133617.876.svg)

-   **自动记忆捕获**（autoCapture）：对话结束后自动提取关键信息存储
    
-   **自动记忆召回**（autoRecall）：对话开始前自动检索相关记忆注入上下文
    

## 安装与配置插件

**重要**

记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置。

### 步骤 1：确认 OpenClaw 运行状态

运行以下命令确认 OpenClaw Gateway 已启动：

```
openclaw gateway status
```

输出应包含 `Gateway: bind=loopback` 和端口信息。

### 步骤 2：获取 DashScope API Key

在阿里云百炼的[密钥管理](https://bailian.console.aliyun.com/cn-beijing?tab=app#/api-key)页面[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并保存，后续步骤需使用。

### 步骤 3：安装插件

npm 安装

```
openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw
```

安装成功后 CLI 输出 `Installed plugin: modelstudio-memory-for-openclaw`，暂不重启，先完成配置。

### 步骤 4：配置插件参数

打开 `~/.openclaw/openclaw.json`，在 `plugins` 部分添加配置：

```
{
  "plugins": {
    "slots": {
      "memory": "modelstudio-memory-for-openclaw"
    },
    "entries": {
      "modelstudio-memory-for-openclaw": {
        "enabled": true,
        "config": {
          "apiKey": "sk-xxx",
          "userId": "user_001",
          "profileSchema": "（此参数非必填）your_profile_schema_id",
          "memoryLibraryId": "（此参数非必填）your_memory_library_id",
          "projectId": "（此参数非必填）your_project_id"
        }
      }
    }
  }
}
```

**配置说明**：

-   `slots.memory`：注册为记忆槽位，自动禁用内置 `memory-core` 和 `memory-lancedb`
    
-   `apiKey`：直接填写[步骤 2](#91ac0d8210b2q) 获取的 DashScope API Key
    
-   `userId`：用户标识符，用于隔离不同用户的记忆空间，同一 `userId` 共享命名空间，不同 `userId` 完全隔离
    

**完整配置项**：

**配置项**

**类型**

**默认值**

**说明**

`apiKey` **(必填)**

string

\-

以 sk-xxx 开头

`userId` **(必填)**

string

\-

记忆空间的用户标识

`autoCapture`

boolean

`true`

对话后自动提取并存储记忆

`autoRecall`

boolean

`true`

对话前自动检索并注入记忆

`topK`

number

`5`

每次召回返回的记忆条数

`minScore`

number

`0`

最小相似度阈值（0–100）

`profileSchema`

string

\-

用户画像 ID，非必填。可访问[记忆库](https://bailian.console.aliyun.com/cn-beijing?tab=app#/memory/list)页面，点击指定记忆库的**查看详情**，进入记忆规则页面获取。

`memoryLibraryId`

string

\-

记忆库 ID，非必填。在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库 ID。

`projectId`

string

\-

记忆片段规则 ID，非必填。点击指定记忆库的**查看详情**，进入记忆规则页面获取。

**说明**

如不传此参数，会自动选择指定记忆库的默认的记忆片段规则 ID。

### 步骤 5：验证

验证安装

```
# 查看插件信息
openclaw plugins info modelstudio-memory-for-openclaw

# 查看状态
openclaw modelstudio-memory stats
```

重启 Gateway：

```
openclaw gateway restart
```

重启完成后，运行以下命令验证插件状态：

```
openclaw plugins info modelstudio-memory-for-openclaw
```

预期输出：

```
Memory (Bailian)
id: modelstudio-memory-for-openclaw
Status: loaded
Tools: memory_search, memory_store, memory_list, memory_forget
CLI commands: modelstudio-memory
```

`Status: loaded` 表示加载成功。确认阿里云百炼 API 连通性：

```
openclaw modelstudio-memory stats
```

预期输出：

```
User: user_001
Total memories: 0
Auto-capture: true
Auto-recall: true
Top-K: 5
```

至此，长期记忆插件配置完成，Agent 的自动捕获和召回已默认启用，无需任何手动操作。打开 OpenClaw 面板页面（默认地址：http://127.0.0.1:18789）即可与启用记忆的 Agent 开始对话。

## 在对话中使用记忆工具

除自动捕获和自动召回外，插件还向 Agent 注册了四个工具，Agent 可在对话过程中根据语境主动调用。

-   **memory\_search：**语义检索记忆库。接收一个自然语言查询，对记忆库执行语义检索，返回相似度最高的记忆列表。当用户提出 "之前讨论过什么"或"关于数据库的记忆"等回顾性问题时，Agent 会自动选择该工具。
    
-   **memory\_store：**直接写入记忆。将指定内容直接写入记忆库，不经过对话提炼。适用于用户主动要求 Agent 记住某个特定事实的场景，例如"记住我的服务器 IP 是 192.168.1.xxx"。
    
-   **memory\_list：**分页列出记忆。分页列出当前 `userId` 下的所有记忆条目，用于浏览和管理已有记忆。
    
-   **memory\_forget：**根据记忆 ID 删除指定记忆。Agent 通常先通过 `memory_search` 定位目标记忆，再调用 `memory_forget` 执行删除。
    

**CLI 等效命令**：

```
# 语义检索记忆
openclaw modelstudio-memory search "用户偏好"

# 分页列出所有记忆
openclaw modelstudio-memory list --page 1 --size 10

# 查看记忆统计
openclaw modelstudio-memory stats
```

## 配额与限制

阿里云百炼[长期记忆 API](https://help.aliyun.com/zh/model-studio/long-term-memory-2-0) 存在以下速率限制：

**API 操作**

**速率上限**

AddMemory (写入)

120 次/分钟

SearchMemory (查询)

300 次/分钟

所有操作合计

3000 次/分钟

**性能指标**：

-   SearchMemory 端到端延迟：200–500ms
    
-   AddMemory 延迟：500–1000ms
    
-   自动捕获异步执行，不影响响应速度
    

## **常见问题**

1.  **Gateway 重启后插件状态为 not loaded？**
    
    检查 openclaw.json 中 `plugins.entries.modelstudio-memory-for-openclaw.enabled` 是否为 `true`，以及 `plugins.slots.memory` 是否指向 `"modelstudio-memory-for-openclaw"`。修正后再次执行 `openclaw gateway restart`。
    
2.  **日志中出现 InvalidApiKey 错误？**
    
    DashScope API Key 无效或已过期。登录阿里云百炼控制台确认 API Key 状态，必要时重新创建。若使用环境变量引用，确认 `DASHSCOPE_API_KEY` 已正确设置且 Gateway 进程能读取到该变量。
    
3.  **支持配置阿里云百炼 Coding Plan 的 API Key？**
    
    不支持。
    
4.  **如何查看插件运行日志？**
    
    OpenClaw Gateway 的日志文件按日期存储在系统临时目录中，文件名格式为 `openclaw-YYYY-MM-DD.log`
    
    ```
    # Linux / macOS
    tail -f /tmp/openclaw/openclaw-$(date +%F).log | grep modelstudio-memory
    # Windows PowerShell
    Get-Content "$env:TEMP\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log" -Wait | Select-String "modelstudio-memory"
    ```
    
    本文档完成了从安装到验证的完整流程。插件的自动捕获与自动召回机制已覆盖大部分使用场景，无需额外干预。后续可关注记忆数据在[记忆库](https://bailian.console.aliyun.com/cn-beijing?tab=app#/memory/list)中的增长情况，并根据业务规模调整 `topK` 和缓存策略。
    

## 相关文档

文档

说明

[OpenClaw（原 Clawdbot/Moltbot）](https://help.aliyun.com/zh/model-studio/openclaw)

阿里云官方 OpenClaw 集成配置文档

[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)

阿里云百炼 API Key 创建和管理

[长期记忆－API（新）](https://help.aliyun.com/zh/model-studio/long-term-memory-2-0)

AddMemory、SearchMemory 等 API 的完整参数描述和代码示例

[记忆库](https://help.aliyun.com/zh/model-studio/memory-library)

用于在控制台创建和管理记忆库

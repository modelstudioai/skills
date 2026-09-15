# 定义 Agent

智能体定义模型、系统提示词、工具与扩展能力，每次保存自动产生新版本。

## 配置字段

在**智能体**页面点击**创建智能体**，或点击已有智能体进入详情页，可配置以下字段：

**字段**

**必填**

**可变更**

**说明**

名称

是

是

工作空间内唯一标识，例如"数据分析助手"

描述

否

是

智能体用途的简要说明，列表与下拉中展示

模型

是

是

从下拉选择，例如 `qwen3-max`。变更模型会产生新版本

系统提示词

否

是

定义智能体的角色、行为与约束。变更会产生新版本

工具

否

是

7 个内置工具，按需勾选。详见 [Agent 工具配置](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)

MCP 服务器

否

是

挂载已开通的 MCP 服务（官方或自定义），其下工具默认全部启用，可按需关闭

技能

否

是

挂载已上传的技能包并锁定版本

多智能体

否

是

配置 coordinator 编队，编排多个成员智能体。详见 [多智能体协作](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)

元数据

否

是

自定义键值对（对应 API 的 `metadata`），不影响模型行为，可用于标记环境标识、版本号等业务信息

通过 API 创建智能体时，需指定名称与模型，可选配系统提示词和工具集。完整参数与响应字段详见[创建 Agent API](raw/application-api-reference/managed-agents-api/agent-api/agent-create.md)。

bash

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-analyst",
    "model": {"id": "qwen3-max"},
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
  }'
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
Agent agent = client.agents().create(AgentCreateParam.builder()
    .name("data-analyst")
    .model("qwen3-max")
    .instructions("你是数据分析专家，使用 pandas 处理 CSV 文件。")
    .build());
System.out.println(agent.getId());       // "agent_xxx"
System.out.println(agent.getVersion());  // 1
```

## 相关配置

智能体的能力由以下组件共同决定，详细配置参见各自页面：

-   [Agent 工具配置](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)：7 个开箱即用的工具，覆盖命令执行、文件操作与网络访问。
-   [Agent MCP](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)：通过 MCP 协议接入外部工具服务。
-   [Agent Skills](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)：挂载预置的工具组合，封装端到端任务流程。
-   [多智能体协作](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)：通过 coordinator 编队编排多个成员智能体。

## 版本

每次保存智能体，`version` 自动递增。会话创建时锁定当时的版本，后续编辑不影响已有会话。通过 API 更新时采用全量替换语义——请求体须包含当前 `version` 用于乐观锁校验，缺省字段视为清空。

## 归档与删除

智能体只支持归档，不支持删除。在智能体详情页点击**归档**后，智能体默认不再出现在列表中，不可用于新建会话，已有会话不受影响。归档后仍可通过 API 查询（`include_archived=true`）。

通过 API 归档智能体，详见[归档 Agent API](raw/application-api-reference/managed-agents-api/agent-api/agent-archive.md)。

bash

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/agents/agent_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
client.agents.archive("agent_xxx")
```

java

```
client.agents().archive("agent_xxx");
```

## 下一步

-   [发起会话](raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)：用配好的智能体发起会话。
-   [云端托管环境](raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)：为工具调用准备沙箱。

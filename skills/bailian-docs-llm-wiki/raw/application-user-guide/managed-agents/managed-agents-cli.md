# 使用 CLI

在终端用百炼 CLI 以基础设施即代码方式管理 Agent 与会话。

[阿里云百炼 CLI](https://help.aliyun.com/zh/model-studio/cli) 支持以基础设施即代码的方式管理智能体，从声明配置到运行会话一气呵成。

**说明**Managed Agent 相关 CLI 能力目前仅对中国站（aliyun.com）账号开放。

## 命令

**能力**

**命令**

**说明**

**常用参数**

Agent 生命周期

`bl managed-agent init` / `validate` / `plan` / `apply` / `destroy`

以基础设施即代码方式管理 Agent 生命周期

声明式配置文件

Agent 会话

`bl managed-agent session run` / `send` / `create` / `get` / `list` / `events` / `delete`

管理 Agent 会话

`--prompt` 输入（`run`）、`--message` 输入（`send`）、`--session-id` 会话 ID、`--no-stream` 关闭默认开启的流式响应

Agent 状态

`bl managed-agent state list` / `show` / `import` / `rm`

管理 Agent 状态

`--id` 资源 ID

Agent 定时任务

`bl managed-agent deployment list` / `get` / `search` / `create` / `run` / `pause` / `unpause` / `runs list` / `runs get`

管理定时任务、触发与运行记录

—

Agent 技能

`bl managed-agent skill-list`

列出技能目录中的技能

—

## 示例

```
bl managed-agent plan                                    # 预览将要创建/变更的资源
bl managed-agent apply                                   # 应用配置，创建智能体与环境
bl managed-agent session run --prompt "分析 sales.csv 的 Q3 销售趋势"
```

任意命令追加 `--help` 查看完整参数。更多命令见 [Managed Agent 命令参考](https://help.aliyun.com/zh/model-studio/cli/managed-agent)。

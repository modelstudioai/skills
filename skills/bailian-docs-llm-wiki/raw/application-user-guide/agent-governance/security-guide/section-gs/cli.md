# 使用 CLI

在终端用阿里云百炼 CLI 查询防护统计、资产分布与风险告警。

[阿里云百炼 CLI](../../../../cli/getting-started/overview.md) 把安全防护数据的查询封装为命令，便于在终端或 Agent 中调度。使用前需完成安装与鉴权，见 [安装与鉴权](../../../../cli/getting-started/installation.md)。

<a id="前置准备"></a>

## 前置准备

-   按[安装与鉴权](../../../../cli/getting-started/installation.md)安装 CLI 并配置 API Key。
-   按[获取业务空间 ID](../../../../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#6cc9270e83h9d)取得实际 ID，通过 `BAILIAN_WORKSPACE_ID` 或 CLI 工作空间配置选择目标。确认 API Key、工作空间及当前 Endpoint 指向同一目标，配置方式见[Security 命令参考](../../../../cli/capabilities/agent-infrastructure/security.md)。

<a id="命令"></a>

<a id="h-security-cli-commands"></a>

## 命令

[

**1\. 查询防护总览**

查看最近 24 小时的统计与资产分布。





](#h-security-cli-overview)[

**2\. 查询高风险告警**

按 high 筛选已有告警。





](#h-security-cli-alerts)

| 能力 | 命令 | 说明 |
| --- | --- | --- |
| 防护总览 | `bl agents security overview` | 查询防护统计与资产分布 |
| 告警列表 | `bl agents security alerts` | 查询该账号下所有 Agent 的风险及日志详情 |

<a id="示例"></a>

<a id="h-security-cli-examples"></a>

## 示例

<a id="查询总览"></a>

<a id="h-security-cli-overview"></a>

### 查询总览

<a id="code-block"></a>

```bash
bl agents security overview
```

<a id="查询高风险告警"></a>

<a id="h-security-cli-alerts"></a>

### 查询高风险告警

<a id="code-block-2"></a>

```bash
bl agents security alerts --risk-level high
```

> **说明**
>
> 总览固定查询最近 24 小时的防护统计与资产分布；告警命令查看按 `high` 筛选的已有风险与日志详情。查询不会开通或配置防护，也不会发起新的代码扫描。结果为空不代表资产已通过安全认证，应结合统计范围与告警日志判断。

任意命令追加 `--help` 查看完整参数。更多命令见 [Security 命令参考](../../../../cli/capabilities/agent-infrastructure/security.md)。

<a id="下一步"></a>

## 下一步

[

**调整查询参数**

查看筛选、分页与工作空间参数。





](../../../../cli/capabilities/agent-infrastructure/security.md)[

**了解防护能力**

查看安全防护的能力与使用入口。





](../section-assets/overview.md)

# 使用 CLI

在终端用阿里云百炼 CLI 查询防护统计、资产分布与风险告警。

[阿里云百炼 CLI](https://help.aliyun.com/zh/model-studio/cli/overview) 把安全防护数据的查询封装为命令，便于在终端或 Agent 中调度。使用前需完成安装与鉴权，见 [安装与鉴权](https://help.aliyun.com/zh/model-studio/cli/installation)。

## 前置准备

-   按[安装与鉴权](https://help.aliyun.com/zh/model-studio/cli/installation)安装 CLI 并配置 API Key。
-   按[获取业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#6cc9270e83h9d)取得实际 ID，通过 `BAILIAN_WORKSPACE_ID` 或 CLI 工作空间配置选择目标。确认 API Key、工作空间及当前 Endpoint 指向同一目标，配置方式见[Security 命令参考](https://help.aliyun.com/zh/model-studio/cli/security)。

## 命令

[

**1\. 查询防护总览**

查看最近 24 小时的统计与资产分布。

](#h-security-cli-overview)[

**2\. 查询高风险告警**

按 high 筛选已有告警。

](#h-security-cli-alerts)

能力

命令

说明

防护总览

`bl agents security overview`

查询防护统计与资产分布

告警列表

`bl agents security alerts`

查询该账号下所有 Agent 的风险及日志详情

## 示例

### 查询总览

```
bl agents security overview
```

### 查询高风险告警

```
bl agents security alerts --risk-level high
```

**说明**总览固定查询最近 24 小时的防护统计与资产分布；告警命令查看按 `high` 筛选的已有风险与日志详情。查询不会开通或配置防护，也不会发起新的代码扫描。结果为空不代表资产已通过安全认证，应结合统计范围与告警日志判断。

任意命令追加 `--help` 查看完整参数。更多命令见 [Security 命令参考](https://help.aliyun.com/zh/model-studio/cli/security)。

## 下一步

[

**调整查询参数**

查看筛选、分页与工作空间参数。

](https://help.aliyun.com/zh/model-studio/cli/security)[

**了解防护能力**

查看安全防护的能力与使用入口。

](raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)

# 使用 CLI

在终端用阿里云百炼 CLI 查询防护统计、资产分布与风险告警。

[阿里云百炼 CLI](https://help.aliyun.com/zh/model-studio/cli/index) 把安全防护数据的查询封装为命令，便于在终端或 Agent 中调度。使用前需完成安装与鉴权，见 [安装与鉴权](https://help.aliyun.com/zh/model-studio/cli/installation)。

## 命令

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

```
bl agents security overview
bl agents security alerts --risk-level high
```

任意命令追加 `--help` 查看完整参数。更多命令见 [Security 命令参考](https://help.aliyun.com/zh/model-studio/cli/security)。

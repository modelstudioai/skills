# 使用 CLI

在终端用阿里云百炼 CLI 列出并调用已发布的智能体与工作流应用。

本文介绍应用调用的常用命令与示例；CLI 的安装与配置参见[阿里云百炼 CLI](https://help.aliyun.com/zh/model-studio/cli)。

## 命令

能力

命令

说明

常用参数

应用列表

`bl app list`

浏览阿里云百炼应用

—

应用调用

`bl app call`

调用已发布在阿里云百炼上的智能体与工作流

`--app-id` 应用 ID、`--prompt` 输入

## 示例

```
bl app list                                              # 浏览已发布的应用
bl app call --app-id <应用ID> --prompt "生成本周运营周报大纲"
```

任意命令追加 `--help` 查看完整参数。更多命令参见 [Flow Agent 命令参考](https://help.aliyun.com/zh/model-studio/cli/flow-agent)。

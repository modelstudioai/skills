# 快速开始

3 步接入阿里云百炼 CLI，向 Agent 下发第一个需求。

完成本指南后，你的 AI Agent 将具备调度阿里云百炼全模态能力的本领，只需一句自然语言即可产出图像、视频等专业级内容。

## 1\. 安装 CLI

最简单的方式是让 AI Agent 自动完成。把下面这句话发给你的 Agent，它会阅读安装文档并自动装好阿里云百炼 CLI：

```
请阅读：https://bailian.aliyun.com/cli/install.md 并按照说明为我安装阿里云百炼 CLI
```

也可以手动安装，详见 [安装与鉴权](raw/cli/getting-started/installation.md)。

## 2\. 鉴权配置

把下面的命令交给 Agent，它会自动完成鉴权信息配置：

```
帮我执行 bl auth login --console 控制台登录
```

完成后执行 `bl auth status --output json` 可确认鉴权状态。其他鉴权方式见 [安装与鉴权](https://help.aliyun.com/zh/model-studio/cli/installation#%E9%89%B4%E6%9D%83%E9%85%8D%E7%BD%AE)。

## 3\. 下发第一个需求

完成前两步后，直接向 Agent 下发需求即可调度 CLI 能力进行产出。试试发送第一个示例：

```
帮我生成一套电商主图，6 张图，产品是纯黑色夏日男装 T 恤
```

Agent 会自动选择合适的模型（如 `qwen-image-3.0`）并调用 CLI 完成生成。

## 接入范式

阿里云百炼 CLI 的核心接入范式是“让 Agent 阅读文档后自动装配”：无论是安装还是能力调用，都可以用自然语言下发给 Agent，由 Agent 阅读 [install.md](https://bailian.aliyun.com/cli/install.md) 或 Skill 说明后自动执行。每个 `bl` 命令都被设计为结构化工具调用，便于 Agent 组合成复杂任务流水线。

## 下一步

-   了解全部能力与命令：[能力参考](raw/cli/capabilities.md)

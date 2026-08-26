# 千问办公助理

千问 APP 的办公助理支持通过 Token Plan 接入阿里云百炼，使用 Token Plan 模型处理文档、表格等办公任务。桌面端和手机 APP 均可使用。

## 前提条件

-   已开通 Token Plan（个人版或团队版）并获取专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)。
-   已安装[千问 APP](https://www.qianwen.com/download) 桌面端或手机 APP（手机版需升级到 **7.1.2** 及以上版本）。

## 接入步骤

1.  打开千问 APP 或 PC 客户端，进入**办公助理**，点击**添加模型**。
2.  在弹出的面板中粘贴阿里云 Token Plan 的 API Key，点击校验保存。
3.  回到办公助理，在模型面板中选中 Token Plan 模型（如 Qwen3.8-Max），即可直接发起任务。

## 可用模型

千问办公助理支持以下模型：

-   Qwen3.8-Max
-   Qwen3.7-Max
-   Qwen3.7-Plus
-   Qwen3.6-Flash

## 常见问题

### 是否支持按量计费或 Coding Plan

千问办公助理仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan。

### 手机 APP 找不到 Token Plan 模型入口

请确认千问 APP 已升级到 7.1.2 及以上版本。低版本不支持此功能。

### 校验 API Key 失败

请确认使用的是 Token Plan 专属 API Key，而非按量计费的 API Key。不同计费方案的凭证不通用。更多错误信息请参考 [Token Plan 常见问题](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。

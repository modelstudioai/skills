# 千问

在 千问 中使用阿里云百炼模型。

## 快速开始

1.  1
    
    获取 API Key
    
    开通 Token Plan，按版本获取 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
2.  2
    
    配置模型
    
    打开千问 APP 或桌面端，进入**工作助理**，点击**添加模型**，粘贴 Token Plan API Key，点击校验保存。然后在模型面板中选择 Token Plan 模型（如 Qwen3.8-Max）。
    
3.  3
    
    验证
    
    在工作助理中发送一条消息，模型正常返回响应即表示配置成功。
    

## 可用模型

模型

定位

Qwen3.8-Max

复杂推理与编程

Qwen3.8-Flash

快速、低成本

Qwen3.7-Max

复杂推理

Qwen3.7-Plus

性能与成本均衡

Qwen3.6-Flash

快速、低成本

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)

## 常见问题

是否支持按量计费或 Coding Plan

千问工作助理仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan。

手机 APP 找不到 Token Plan 模型入口

请确认千问 APP 已升级到 7.1.2 及以上版本。低版本不支持此功能。

校验 API Key 失败

请确认使用的是 Token Plan API Key，而非按量计费的 API Key。不同计费方案的凭证不通用。更多错误信息请参考 [Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)。

# Coding Plan概述

Coding Plan 整合了千问、GLM、Kimi 、MiniMax顶级模型，并兼容主流AI编程工具。其折算成本远低于常规 API 调用，且通过固定月费模式有效防范了欠费风险。

## **套餐详情**

**说明**

1.  Lite 套餐自 2026 年 3 月 20 日 00:00:00（UTC+08:00）起停止新购（详见[公告](https://www.aliyun.com/notice/118094)）；4 月 13 日 18:00:00（UTC+08:00）起停止续费与升级（详见[公告](https://www.aliyun.com/notice/118175)）。
    
2.  Lite 套餐支持所有套餐模型（含千问、GLM、Kimi、MiniMax），与 Pro 套餐一致。
    

**Pro 高级套餐**

支持的模型

推荐模型：**qwen3.6-plus**（支持图片理解）、**kimi-k2.5**（支持图片理解）、**glm-5**、**MiniMax-M2.5**

更多模型：qwen3.5-plus（支持图片理解）**、**qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7

不支持以上未列出的模型。

价格

**¥ 200**/月

用量限制

-   每 5 小时**6,000** 次请求
    
-   每周**45,000** 次请求
    
-   每月**90,000** 次请求
    

-   **限时优惠：**活动已结束，当前价格以下单页为准。
    
-   **限量抢购**：名额有限、先到先得。每日 09:30:00（UTC+08:00）补充，可前往[Coding Plan 页面](https://www.aliyun.com/benefit/scene/codingplan)抢购。
    
-   **额度消耗：**单次提问将按实际“模型调用次数”扣除额度。简单任务约消耗 5-10 次，复杂任务约 10-30+ 次，实际消耗受任务难度、上下文及工具使用影响。在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)可以查看用量。
    
-   **额度恢复**：
    
    1.  每 5 小时额度：滚动恢复，每分钟自动释放 5 小时前的额度。 例：10:00 使用 100 次，11:00 使用 200 次。 → 15:00 先恢复 100 次，16:00 再恢复 200 次。
        
    2.  每周额度：每周一 00:00:00（UTC+08:00）重置。
        
    3.  每月额度：在下一个月订阅日的 00:00:00 (UTC+08:00) 重置。
        

## **快速开始**

### **步骤一：订阅 Coding Plan**

访问[Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan)，根据实际需求选择并购买套餐。

主账号可直接订阅该服务，RAM 子账号需完成以下步骤授权后，再进行订阅。

**RAM 子账号授权步骤**

1.  **添加用户：**使用主账号登录阿里云百炼，访问目标工作空间的 [权限管理](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/authority)页面，点击**新增用户**添加该 RAM 用户，并定义用户名称，单击**确定**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4734072771/p1057319.png)
    
2.  **授予权限：**点击该用户右侧的**权限管理**，添加**管理员**权限，然后点击**确定**完成授权。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4734072771/p1057328.png)
    

### **步骤二：获取套餐专属 API Key 和 Base URL**

您需要获取并配置套餐专属的 API Key 和 Base URL，才能正确使用并抵扣套餐额度。

-   **API Key**：在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)，获取Coding Plan 专属 API Key（格式为`sk-sp-xxxxx`）。
    
-   **Base URL**：后续需在 AI 工具中配置以下其中一个Base URL（因工具而异），具体操作请参见对应的AI工具文档。
    
    -   **OpenAI 兼容协议**：`https://coding.dashscope.aliyuncs.com/v1`
        
    -   **Anthropic 兼容协议**：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
        

**说明**

Coding Plan 专属的 API Key 和 Base URL 与百炼按量计费的 API Key（`sk-xxxxx`）和Base URL（`https://dashscope.aliyuncs.com/xxxxxx`）不互通，请勿混用。

### **步骤三：接入AI工具**

 [**OpenClaw**开源、自托管个人 AI 助手](https://help.aliyun.com/zh/model-studio/openclaw)

 [**Hermes Agent**开源 AI 代理框架，内置自学习循环](https://help.aliyun.com/zh/model-studio/hermes-agent)

 [**Claude Code**AI 终端编码助手，支持自然语言编程](https://help.aliyun.com/zh/model-studio/claude-code)

 [**OpenCode**开源 AI 编程代理工具](https://help.aliyun.com/zh/model-studio/opencode)

 [**Cursor**AI 原生代码编辑器](https://help.aliyun.com/zh/model-studio/cursor)

 [**Codex**OpenAI 推出的命令行编程工具](https://help.aliyun.com/zh/model-studio/codex)

 [**Qwen Code**开源命令行 AI 编码工具](https://help.aliyun.com/zh/model-studio/qwen-code)

 [**Cherry Studio**多模型桌面客户端](https://help.aliyun.com/zh/model-studio/cherry-studio)

 [**Chatbox**跨平台 AI 桌面客户端](https://help.aliyun.com/zh/model-studio/chatbox)

 [**Cline**VS Code 扩展，智能代码补全和调试](https://help.aliyun.com/zh/model-studio/cline)

 [**Qoder**面向真实软件开发的 Agentic 编码平台](https://help.aliyun.com/zh/model-studio/qoder-agent)

 [**Lingma**阿里云推出的智能编码辅助工具](https://help.aliyun.com/zh/model-studio/lingma-agent)

 [**Kilo CLI**轻量高性能命令行编程工具](https://help.aliyun.com/zh/model-studio/kilo-cli)

[··· **更多工具**其他编程工具](https://help.aliyun.com/zh/model-studio/more-tools)

## **订阅前须知**

Coding Plan 服务**不支持退款**。因此在订阅前请知悉以下重要内容：

1.  **严禁 API 调用**：仅限在编程工具（如 Claude Code、OpenClaw 等）中使用，禁止以 API 调用的形式用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。**将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。**
    
2.  **数据使用授权**：使用 Coding Plan 期间，模型输入以及模型生成的内容将用于服务改进与模型优化。停止使用 Coding Plan 服务可终止后续数据授权，但终止授权的范围不涵盖已授权使用的 Coding Plan 数据。详细条款请参见[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)第 5.2 条。
    
3.  **账号使用规范**：套餐为订阅人专享使用，禁止共享。账号共享可能导致订阅权益受限。
    

## 常见问题

### **首次续费为什么没有 5 折优惠？**

首次续费 5 折活动已于 2026 年 4 月 1 日 00:00:00（UTC+08:00）结束，当前续费价格以下单页为准。

### 已购买 Coding Plan，为何仍显示欠费/被扣费？

误用了百炼通用 API Key 和 Base URL，系统会识别为按量付费，导致额外扣费。请改用 Coding Plan 专属 API Key（以`sk-sp-`开头）和专属 Base URL（含`coding.dashscope.aliyuncs.com`），配置方法请参见[获取套餐专属 API Key 和 Base URL](#2531c37fd64f9)。

### **Lite 版为什么停止新购？**

因产品升级需要，Coding Plan Lite 基础版本已于 2026 年 3 月 20 日起停止新购（详见[停止新购公告](https://www.aliyun.com/notice/118094)），并于 4 月 13 日起停止续费与升级（详见[停止续费公告](https://www.aliyun.com/notice/118175)）。已购买的用户可继续使用至服务到期。

### **已购买 Lite 版的用户权益是否受影响？**

已购买 Coding Plan Lite 基础套餐的用户可继续使用至服务到期。Lite 套餐已于 2026 年 4 月 13 日起停止续费与升级，如需继续使用，请订阅 Pro 套餐。

更多问题请参考[常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)。

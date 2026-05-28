# 什么是阿里云百炼

阿里云百炼是一站式大模型开发与应用平台，集成千问及主流第三方模型。面向开发者提供兼容 OpenAI 的API和全链路模型服务；面向业务人员提供可视化应用构建能力，可快速创建智能体、知识库问答等 AI 应用。

主要能力：

![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) 调用 API

几行代码即可调用大模型，实现内容创作、摘要生成等功能。

> 百炼兼容 OpenAI 接口规范，只需调整API Key、base\_url 和模型名称，即可将现有 OpenAI 代码迁移至百炼。

## Python

```
import os
from openai import OpenAI

# 注意: 不同地域的base_url不通用（下方示例使用北京地域的 base_url）
# - 华北2（北京）: https://dashscope.aliyuncs.com/compatible-mode/v1
# - 美国（弗吉尼亚）: https://dashscope-us.aliyuncs.com/compatible-mode/v1
# - 新加坡: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
# - 德国（法兰克福）: https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1，请将WorkspaceId替换为业务空间ID
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";

// 注意: 不同地域的base_url不通用（下方示例使用北京地域的base_url）
// - 华北2（北京）: https://dashscope.aliyuncs.com/compatible-mode/v1
// - 美国（弗吉尼亚）: https://dashscope-us.aliyuncs.com/compatible-mode/v1
// - 新加坡: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
// - 德国（法兰克福）: https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1，请将WorkspaceId替换为业务空间ID
const openai = new OpenAI(
    {
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.6-plus",
        messages: [{ role: "user", content: "你是谁？"}],
    });
    console.log(completion.choices[0].message.content)
}

main()
```

## curl

不同地域的 Base URL不通用（以下示例是北京地域 Base URL）

-   华北2（北京）： `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
    
-   美国（弗吉尼亚）： `https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions`
    
-   新加坡： `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`
    
-   德国（法兰克福）： `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`，请将WorkspaceId替换为业务空间ID
    

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.6-plus",
    "messages": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}'
```

![robot](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824100.png) [构建智能客服](https://help.aliyun.com/zh/model-studio/single-agent-application)

通过可视化工具快速搭建 AI 助手，处理客户咨询。

![客服3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p823451.gif)

![process](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824091.png) [编排流程](https://help.aliyun.com/zh/model-studio/workflow-application/)

可视化流程编排，无代码基础的业务人员也能独立完成工作流设计。

![流程\_4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824085.png)

![tune\_8](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824102.png) [微调模型](https://help.aliyun.com/zh/model-studio/model-training-overview)

可视化微调，无需编写训练代码，即可完成模型定制。

![loss\_3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824086.png)

## **模型服务**

### 开箱即用的模型

百炼提供开箱即用的模型服务，无需自行部署或运维，直接调用自研千问（Qwen）全系列模型，以及 DeepSeek、Kimi、GLM 等第三方大模型。详情请参见[选择模型](https://help.aliyun.com/zh/model-studio/models)。

-   **千问（Qwen）系列旗舰模型**：
    
    -   千问 Max：Qwen 系列效果最好的模型，适合处理复杂、多步骤任务。
        
        > 最新的 qwen3.7-max 推理能力全面超越前代，推荐选用。
        
    -   千问 Plus：效果、速度和成本均衡，是多数场景的**推荐选择**。
        
    -   千问 Flash：高性价比、低延迟，适合需要快速响应的简单任务。
        
-   **多模态覆盖**：涵盖文本生成、视觉理解、图像生成、视频生成、语音识别与合成、嵌入向量等多种能力。
    
-   **细分领域模型**：提供长文本处理、翻译、数据挖掘、法律、意图理解、角色扮演、深入研究等多种领域模型。
    

### 模型调优、部署和评测

-   [模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)：支持有监督微调（SFT）、继续预训练（CPT）和直接偏好优化（DPO），满足特定业务需求。
    
-   [模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)：将预置模型或调优后的自定义模型部署为资源专享的推理服务，满足高并发、低延迟等性能要求。支持按时长、包月、按 Token 量等多种计费方式。
    
-   [模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)：提供人工评测、自动评测和基线评测，支持快速对比不同模型表现，验证调优效果，提前发现潜在调用风险。
    

## **应用构建**

-   **应用类型：**提供可视化和高代码两种开发模式。可视化模式可快速创建[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)；[高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)则支持将 Python 项目部署为后端服务，具备自动化运维、可观测、日志服务等能力。
    
-   **功能拓展：**通过[知识库（RAG）](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)接入私有数据和专业领域知识；通过[插件](https://help.aliyun.com/zh/model-studio/plug-in-overview)和[模型上下文协议（MCP）](https://help.aliyun.com/zh/model-studio/mcp-introduction)调用外部服务。
    
-   **分享与发布：**支持将应用发布至网页、钉钉机器人、微信公众号及音视频互动智能体等多种平台，详见[应用分享](https://help.aliyun.com/zh/model-studio/share-an-application)。
    

## **产品计费**

开通百炼无需费用，调用、微调、部署模型时产生相应费用，详情请参见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

### **新用户免费额度**

百炼为新用户提供北京地域专属的新人免费额度，用于体验模型调用。额度用完后自动转为按量付费。如需避免意外扣费，可开启[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)功能，额度耗尽时服务自动停止，详见[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。

### **如何支付费用**

模型调用按分钟出账，请确保阿里云账户余额充足。可前往[费用与成本](https://usercenter2.aliyun.com/home)页面充值。

### **查看账单与用量**

-   **消费明细：**前往[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)和[成本分析](https://usercenter2.aliyun.com/expense-manage/expense-analyze)页面查看。
    
-   **调用统计：**模型调用完约**一小时后**，前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.7dd7521cmX1pAh&tab=model#/model-market)，在页面右上角选择目标地域，进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面并设置查询条件，点击目标模型**操作**列的**监控**，即可查看调用量、Token 消耗、成功率等统计数据。详情请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)。
    
-   **Coding Plan 用量：**如已订阅 Coding Plan（AI 编码套餐），可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)查看当前套餐的请求消耗情况。Coding Plan 采用固定月费，提供月度请求额度，支持在 AI 编码工具中使用，详情请参见[Coding Plan概述](https://help.aliyun.com/zh/model-studio/coding-plan)。
    

## **开始使用阿里云百炼**

-   在线体验大模型：
    
    -   打开[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.7dd7521cmX1pAh&tab=model#/model-market)，在右上角选择目标地域
        
    -   进入[模型体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text)页面，选择模型开始体验
        
-   发起第一个API请求：[首次调用千问API](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen)
    
-   构建第一个大模型应用：[0代码构建问答应用](https://help.aliyun.com/zh/model-studio/build-knowledge-base-qa-assistant-without-coding/)
    

## 常见问题

**Q：我的数据安全吗？阿里云百炼会用我的数据进行训练吗？**

A：不会。阿里云严格保护数据隐私，不会将您的数据用于模型训练。构建应用或训练模型时传输的所有数据均经过加密处理。详情请参见[合规资质与隐私说明](https://help.aliyun.com/zh/model-studio/privacy-notice)。

**Q：阿里云百炼提供哪些地域的服务？不同地域有什么区别？**

A：目前提供以下地域的模型服务：

华北2（[北京](https://bailian.console.aliyun.com/?tab=model#/model-market)）、美国**（**[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1)**）**、国际（[新加坡](https://modelstudio.console.aliyun.com/?tab=doc#/doc/?type=model&url=2840914)）和德国**（**[法兰克福](https://modelstudio.console.aliyun.com/eu-central-1)**）**地域

建议选择邻近地域以降低网络延迟。各地域的接入点（Endpoint/Base URL）不同，API Key 不通用，支持的模型、平台功能与价格也有所差异，详情请参见[选择模型](https://help.aliyun.com/zh/model-studio/models)。

**Q：如何避免产生费用？**

A：百炼采用按量付费，本身**没有"自动扣费"开关**。以下措施可有效控制费用：

-   **删除API Key**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.7dd7521cmX1pAh&tab=model#/model-market)，选择目标地域，进入[API-KEY](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key)页面，删除所有API Key，从源头阻断调用。
    
-   **停止所有调用：**停止应用程序、智能体、工作流中的模型调用，并排查定时任务和后台进程。
    
-   **清理计费资源：**删除不再使用的知识库；前往[模型部署](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)页面，下线按算力时长计费的部署实例。
    
-   **开启"**[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)**"（仅限新用户且在免费额度有效期内）：**在模型详情页开启此开关，免费额度耗尽后服务自动停止，不会转为付费。仅适用于中国内地版（北京）模型，且须在免费额度有效期内。
    
-   **设置费用监控和预警：**查看 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)和[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，并设置[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)，及时发现异常消费。
    
-   **订阅 Coding Plan（AI 编码套餐）：**固定月费，提供月度请求额度，无按量扣费风险。注意需使用 Coding Plan 专属的 Base URL和API Key 进行调用，否则模型调用将按量付费。详情请参见[Coding Plan概述](https://help.aliyun.com/zh/model-studio/coding-plan)。
    

**Q：如何使用 Qwen3 系列模型或 DeepSeek？**

A：

1.  **在线体验：**打开[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.7dd7521cmX1pAh&tab=model#/model-market)，选择目标地域，进入[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)页面，点击模型即可体验（DeepSeek 仅支持北京地域）。
    
2.  **通过API调用：**请参见[首次调用千问API](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen)。
    
3.  **通过开发工具（如 Claude Code）调用：**请参考[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)。
    
4.  **通过可视化界面构建大模型应用：**请参考[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)或[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)。

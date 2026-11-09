# 计费说明

Flow Agent 智能体应用与工作流应用的计费项、不计费项与免费额度。

Flow Agent 的编排能力本身不单独收费，费用来自应用实际调用的模型和组件。各组件按自身公开标准独立计费，免费额度只抵扣其指定的计费项，实际金额以控制台账单为准。

## 计费项

不同应用形态的费用来源不同。

应用形态

费用来源

计费详情

智能体应用

模型调用、知识库、MCP 调用

[智能体应用计费说明](https://help.aliyun.com/zh/model-studio/new-single-agent-application#66b7273195ors)

工作流应用

执行路径上各计费节点的调用量

[工作流应用计费说明](https://help.aliyun.com/zh/model-studio/invoke-workflow-application#760df55fb1zx2)

### 智能体应用

-   **模型调用**：按所选模型的输入和输出 Token 计费，标准见[选择模型](raw/model-user-guide/get-started-with-models/models.md)。选用智能模式时，AUTO 按统一刊例价计费，与实际路由到的模型无关；直接选择性能 / 均衡 / 经济档时按所选档位计费，各档位价目及缓存价格见[智能模式计费明细](https://help.aliyun.com/zh/model-studio/new-single-agent-application#66b7273195ors)。
-   **知识库**：按量付费，详见[知识库计费说明](raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。从知识库召回的文本切片会增加模型输入 Token 数量，可能导致模型调用费用上升。
-   **MCP**：部分官方 MCP 按模型调用计费，如文生图、文生视频、语音合成等。部分 MCP 涉及第三方 API 调用，该部分费用由第三方收取，阿里云百炼不收取费用。
-   **上下文缓存**：调用支持隐式缓存的模型时自动生效，无需配置且无法关闭；智能体应用暂不支持配置显式缓存。智能模式各档位的缓存费用按[智能模式计费明细](https://help.aliyun.com/zh/model-studio/new-single-agent-application#66b7273195ors)中的对应价格计算。直接选择模型时，适用模型和缓存计费规则见[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

### 工作流应用

工作流应用按其内部实际执行的**计费节点**的调用量计费。

-   **计费单元**：每个计费节点有独立的计费单位，例如大模型节点按 Token 计费。
-   **总费用**：一次工作流调用的总费用，是该次执行路径上所有计费节点产生的费用之和。未进入执行路径的节点不产生费用。

部分节点的计费方式需要在配置时留意：

节点

计费说明

图片解析

选择大模型文档解析暂不计费；选择 Qwen VL 解析产生 Qwen-VL 系列模型的调用费用。详见[图片解析节点](raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)

文档解析、音频解析、视频解析

使用内置大模型解析，暂不计费

模型内置联网搜索

产生模型调用费用和搜索策略费用，详见[联网搜索](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)

知识库

按知识库的按量付费标准计费，详见[知识库计费说明](raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)

高代码应用不属于 Flow Agent 的两种应用形态。部署和资源配置请参见[高代码应用](raw/application-user-guide/agent-development/sandbox/rich-code-application.md)及 [Sandbox](raw/application-user-guide/agent-development/sandbox.md)，按对应服务的计费规则核对费用。

## 不计费项

功能

说明

文件上传

文件问答中的上传操作不收费，基于文件内容的问答按模型标准计费，详见[文件问答](https://help.aliyun.com/zh/model-studio/file-q-a#a19becd30ezve)

Prompt 自动优化

不计费，详见[优化 Prompt](raw/application-user-guide/prompt/optimize-prompt.md)

UI 设计器

功能本身不计费；AI 对话产生模型调用费用，文件存储和数据库超出免费额度或套餐配额后按量计费，发布到生产环境需订阅团队版或更高级别套餐，详见 [UI 设计器计费说明](https://help.aliyun.com/zh/model-studio/ui-designer#b8e7e1ed0d3wv)

## 免费额度

模型调用可使用[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)抵扣，额度消耗完后按 Token 使用量计费。知识库、ParseX 等组件的免费额度按各自规则计算，只抵扣其指定的计费项，详见对应组件的计费说明。

## 常见问题

### 通过分享链接产生的费用由谁承担？

由应用创建者的 UID 账号承担。详见[分享应用](raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)。

### 如何查询应用实际产生的费用？

见[账单与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。工作流应用可按执行路径核对各计费节点的调用量。

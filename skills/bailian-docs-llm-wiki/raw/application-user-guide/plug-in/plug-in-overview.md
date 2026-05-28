# 插件概述

尽管大模型在处理复杂任务时展现出了卓越的性能，但它仍然存在一些局限性，例如无法获取最新信息、容易出现幻觉、难以精确计算等。为了解决这些问题，您可以将插件集成到大模型应用中进一步拓展大模型能力，执行更复杂的任务。

## 插件介绍

插件是一个工具的集合。一个插件下可以包含多个工具（API），每个工具实现特定的功能。百炼支持[官方插件](#32ac325aaes00)、[三方插件](#2d13bdc978fp9)及[自定义插件](#ef3ed62bd6v08)。

### **官方插件**

组件广场中预置了百炼的官方插件，您无需配置其输入和输出参数，即可直接调用。关于官方插件的使用，请参见[官方插件说明](https://help.aliyun.com/zh/model-studio/plugins#00edef12dc50q)。

**官方插件名称**

**工具ID**

**说明**

**计费方案**

[Python代码解释器](https://help.aliyun.com/zh/model-studio/plugins#f8658b5c70a93)

code\_interpreter

使大模型可以执行Python代码片段，例如数学计算、数据分析与可视化、数据处理。

免费

[计算器](https://help.aliyun.com/zh/model-studio/plugins#12e61be838qub)

calculator

使大模型可以进行复杂的数学计算，例如计算“12313x13232”。

免费

[图片生成](https://help.aliyun.com/zh/model-studio/plugins#da38f8a429lso)

text\_to\_image

使大模型可以基于文本生成图片，例如“请画一只在笑的小狗”。

限时免费，需申请开通

[夸克搜索](https://help.aliyun.com/zh/model-studio/plugins#2c23406bd0sca)

quark\_search

使大模型可以搜索实时信息，查找公开的网络知识和信息，例如“杭州今天天气如何”。

> 夸克搜索插件目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情。

限时免费，需申请开通

[生成二维码](https://help.aliyun.com/zh/model-studio/plugins#dbdea0e23ap97)

generate\_qrcode

使大模型可以根据网站链接地址生成二维码，例如“请给阿里云百炼简介文档生成二维码：https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio”。

免费

[GitHub搜索](https://help.aliyun.com/zh/model-studio/plugins#112834c291kd3)

github\_search

使大模型可以在GitHub中搜索相关项目列表，例如“GitHub搜索：千问”。

免费

### **三方插件**

除官方插件外，第三方插件涵盖了商业服务、图像视频、学习教育等多个领域，并且经过了效果测试。您可以在开通后直接调用，无需进行额外配置。关于三方插件的使用，请参见[三方插件说明](https://help.aliyun.com/zh/model-studio/plugins#9a2fc92e80f2w)。

### **自定义插件**

您可以[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins)，并将其集成到您的大模型应用中，以实现灵活、个性化的功能拓展。

## **插件效果示例**

**示例输入**

**无插件时输出**

**有插件时输出**

12313×13232等于多少

大模型应用无法准确计算复杂数学问题，会出现计算错误的情况。正确结果应为162,925,616。

大模型应用具备了良好的计算能力，能够生成准确的计算结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9491396371/p904991.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9491396371/p904997.png)

## 支持的模型

**模型**

**模型标识符**

通义千问-Turbo

qwen-turbo

通义千问-Plus

qwen-plus

通义千问-Max

qwen-max

通义千问VL-Max

qwen-vl-max

通义千问VL-Plus

qwen-vl-plus

**说明**

各模型对插件的兼容性可能有差异，最新的兼容性状态，请以控制台实际执行结果为准。

模型详情请参见[选择模型](https://help.aliyun.com/zh/model-studio/models)。

## **插件调用机制**

调用插件的本质是调用插件下的工具。百炼支持通过[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)、[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)以及[Assistant API](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)调用插件。

通过智能体应用或Assistant API调用插件后，大模型将根据**用户输入的内容**、**工具名称**以及**工具描述**来判断是否调用插件下的工具。

-   如果需要调用工具，大模型会选择合适的工具，应用内部完成工具调用后，会将工具返回结果和用户内容合并后再次输入到大模型，由大模型生成最终结果并输出。
    
-   如果无需调用工具，大模型将直接生成结果并输出。
    

在工作流应用中调用插件，是将插件作为工作流应用的一个节点，按照用户编排的方式执行特定任务，而非由大模型主动进行规划和调用。

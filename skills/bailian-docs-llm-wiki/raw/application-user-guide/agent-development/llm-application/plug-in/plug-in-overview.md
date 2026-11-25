# 插件概述

尽管大模型在处理复杂任务时展现出了卓越的性能，但它仍然存在一些局限性，例如无法获取最新信息、容易出现幻觉、难以精确计算等。为了解决这些问题，您可以将插件集成到大模型应用中进一步拓展大模型能力，执行更复杂的任务。

<a id="插件介绍"></a>

<a id="9bf7a1c23a80r"></a>

## 插件介绍

插件是一个工具的集合。一个插件下可以包含多个工具（API），每个工具实现特定的功能。百炼支持[官方插件](plug-in-overview.md#94a26ad7f8qik)、[三方插件](plug-in-overview.md#c058b6cd69poo)及[自定义插件](plug-in-overview.md#8329ef7096657)。

<a id="官方插件"></a>

<a id="94a26ad7f8qik"></a>

### 官方插件

组件广场中预置了百炼的官方插件，您无需配置其输入和输出参数，即可直接调用。关于官方插件的使用，请参见[官方插件说明](plugins.md#00edef12dc50q)。

<table><thead><tr><th><strong>官方插件名称</strong></th><th><strong>工具 ID</strong></th><th><strong>说明</strong></th><th><strong>计费方案</strong></th></tr></thead><tbody><tr><td><p><a href="plugins.md">Python 代码解释器Python Code Interpreter</a></p></td><td><p>code_interpreter</p></td><td><p>使大模型可以执行 Python 代码片段，例如数学计算、数据分析与可视化、数据处理。</p></td><td><p>免费</p></td></tr><tr><td><p><a href="plugins.md">计算器Calculator</a></p></td><td><p>calculator</p></td><td><p>使大模型可以完成复杂的数学计算，例如计算“12313x13232”。</p></td><td><p>免费</p></td></tr><tr><td><p><a href="plugins.md">图片生成Image Generation</a></p></td><td><p>text_to_image</p></td><td><p>使大模型可以基于文本生成图片，例如“请画一只在笑的小狗”。</p></td><td><p>限时免费，需申请开通</p></td></tr><tr><td><p><a href="plugins.md">夸克搜索</a></p></td><td><p>quark_search</p></td><td><p>使大模型可以搜索实时信息，查找公开的网络知识和信息，例如“杭州今天天气如何”。</p><blockquote><p>夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情。</p></blockquote></td><td><p>限时免费，需申请开通</p></td></tr><tr><td><p><a href="plugins.md">生成二维码</a></p></td><td><p>generate_qrcode</p></td><td><p>使大模型可以根据网站链接地址生成二维码，例如“请给阿里云百炼简介文档生成二维码：<a href="https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio"></a><a href="https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio">https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio</a>”。</p></td><td><p>免费</p></td></tr><tr><td><p><a href="plugins.md">GitHub 搜索</a></p></td><td><p>github_search</p></td><td><p>使大模型可以在 GitHub 中搜索相关项目列表，例如“GitHub 搜索：千问”。</p></td><td><p>免费</p></td></tr></tbody></table>

<a id="三方插件"></a>

<a id="c058b6cd69poo"></a>

### 三方插件

除官方插件外，第三方插件涵盖了商业服务、图像视频、学习教育等多个领域，并且经过了效果测试。您可以在开通后直接调用，无需进行额外配置。关于三方插件的使用，请参见[三方插件说明](plugins.md#02c6291938c81)。

<a id="自定义插件"></a>

<a id="8329ef7096657"></a>

### 自定义插件

您可以[自定义插件](custom-plug-ins.md)，并将其集成到您的大模型应用中，以实现灵活、个性化的功能拓展。

<a id="插件效果示例"></a>

<a id="4e2ee3d74cxmf"></a>

## 插件效果示例

<table><thead><tr><th><p><strong>示例输入</strong></p></th><th><p><strong>无插件时输出</strong></p></th><th><p><strong>有插件时输出</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>12313×13232等于多少</p></td><td><p>大模型应用无法准确计算复杂数学问题，会出现计算错误的情况。正确结果应为162,925,616。</p></td><td><p>大模型应用具备了良好的计算能力，能够生成准确的计算结果。</p></td></tr><tr><td><p>无插件时，大模型直接尝试计算并输出了错误的数值结果，与正确答案162,925,616不符。</p></td><td><p>有插件时，大模型调用<strong>calculator</strong>插件，输入参数<code>payload__input__text</code>为<code>12313x13232</code>，输出参数<code>equations</code>为<code>[&quot;12313 * 13232&quot;]</code>、<code>results</code>为<code>[162925616]</code>，AI回复正确计算结果。</p></td></tr></tbody></table>

<a id="支持的模型"></a>

<a id="bbee2243a35ai"></a>

## 支持的模型

| 模型 | 模型标识符 |
| --- | --- |
| 通义千问-Plus | qwen-plus |
| 通义千问-Max | qwen-max |

> **说明**
>
> 各模型对插件的兼容性可能有差异，最新的兼容性状态，请以控制台实际执行结果为准。

模型详情请参见[选择模型](../../../../model-user-guide/get-started-with-models/models.md)。

<a id="插件调用机制"></a>

<a id="293e088fd84ao"></a>

## 插件调用机制

调用插件的本质是调用插件下的工具。百炼支持通过[智能体应用（Agent 1.0）](../../../agent-legacy/legacy-flow-agent/single-agent-application.md)、[工作流应用](../workflow-application.md)以及[Assistant API](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)调用插件。

通过智能体应用或Assistant API调用插件后，大模型将根据**用户输入的内容**、**工具名称**以及**工具描述**来判断是否调用插件下的工具。

-   如果需要调用工具，大模型会选择合适的工具，应用内部完成工具调用后，会将工具返回结果和用户内容合并后再次输入到大模型，由大模型生成最终结果并输出。
-   如果无需调用工具，大模型将直接生成结果并输出。

在工作流应用中调用插件，是将插件作为工作流应用的一个节点，按照用户编排的方式执行特定任务，而非由大模型主动进行规划和调用。

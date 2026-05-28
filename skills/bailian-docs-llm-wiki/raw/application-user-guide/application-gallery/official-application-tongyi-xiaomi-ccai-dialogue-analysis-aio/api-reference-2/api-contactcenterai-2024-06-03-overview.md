# API概览

## API标准及多语言预置SDK

本产品（`通义晓蜜CCAI-AIO/2024-06-03`）的 OpenAPI 采用 ROA 签名机制，具体签名方式请参见[签名机制说明](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)。我们已为开发者封装了主流编程语言的 SDK，您可通过 [下载 SDK](https://api.aliyun.com/api-tools/sdk/ContactCenterAI?version=2024-06-03) 快速调用 API，无需关注签名等底层实现细节，显著降低开发门槛与集成复杂度。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的 [RAM 用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## API目录

API

标题

API概述

[RunCompletion](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-runcompletion)

通过模版ID调用通义晓蜜CCAI-对话分析AIO应用

支持调用通义晓蜜CCAI-对话分析AIO应用获取对话摘要、关键信息抽取、质检结果、对话分析结果，应用调用支持 HTTP 调用来完成客户的响应，目前提供普通 HTTP 和 HTTP SSE 两种协议，您可根据自己的需求自行选择。

[RunCompletionMessage](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-runcompletionmessage)

使用原生Prompt调用通义晓蜜CCAI-对话分析AIO应用

支持以Message协议格式调用通义晓蜜CCAI-对话分析AIO应用获取对话摘要、关键信息抽取、质检结果、对话分析结果，应用调用支持 HTTP 调用来完成客户的响应，目前提供普通 HTTP 和 HTTP SSE 两种协议，您可根据自己的需求自行选择。

[AnalyzeConversation](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-analyzeconversation)

通过任务类型调用通义晓蜜CCAI-对话分析AIO应用

获取对话摘要、标题生成、关键词、字段信息抽取、问题及解决方案、服务质检、代办事项、满意度、情绪检测、QA抽取、用户画像、标签分类等对话分析结果，应用调用支持 HTTP 调用来完成客户的响应。

[GetTaskResult](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-gettaskresult)

通过任务ID获取离线任务分析结果

通过任务ID获取离线任务对话分析结果。应用调用支持 HTTPS调用来完成客户的响应。

[CreateTask](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-createtask)

通过上传离线任务数据进行通义晓蜜CCAI-对话分析

通过创建离线异步任务，进行对话分析。应用调用支持 HTTP 调用来完成客户的响应。

[AnalyzeImage](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-analyzeimage)

图片内容分析

通过通义晓蜜CCAI-对话分析AIO应用进行图片内容分析。具体包括以下场景：水印检测。应用调用支持 HTTP 调用来完成客户的响应。

[GeneralAnalyzeImage](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-generalanalyzeimage)

通用图片分析

通用图片分析。

## 热词管理

API

标题

API概述

[CreateVocab](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-createvocab)

创建热词

将一组语音热词上传到服务端，并获取返回热词ID。

[UpdateVocab](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-updatevocab)

修改热词

根据词表的ID可以更新对应的词表信息，包括词表名称、词表描述信息、词表的词和权重。

[ListVocab](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-listvocab)

获取热词列表

列举指定业务空间下的热词列表信息。

[DeleteVocab](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-deletevocab)

删除热词

根据词表的ID删除对应的词表。

[GetVocab](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-getvocab)

获取热词

根据词表的ID获取对应的词表信息。

## 不推荐或白名单开放

API

标题

API概述

[AnalyzeAudioSync](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-analyzeaudiosync)

语音文件实时分析

对进行语音文件进行实时对话分析。应用调用支持 HTTPS 调用来完成客户的响应。

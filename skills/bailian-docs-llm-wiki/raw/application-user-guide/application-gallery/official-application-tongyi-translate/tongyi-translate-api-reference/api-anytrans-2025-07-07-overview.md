# API概览

## API标准及多语言预置SDK

本产品（`通义翻译/2025-07-07`）的 OpenAPI 采用 ROA 签名机制，具体签名方式请参见[签名机制说明](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)。我们已为开发者封装了主流编程语言的 SDK，您可通过 [下载 SDK](https://api.aliyun.com/api-tools/sdk/AnyTrans?version=2025-07-07) 快速调用 API，无需关注签名等底层实现细节，显著降低开发门槛与集成复杂度。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的 [RAM 用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 文本翻译

API

标题

API概述

[TextTranslate](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-texttranslate)

文本翻译接口

通义多模态翻译文本翻译

[BatchTranslate](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-batchtranslate)

批量文本翻译

通义多模态翻译批量翻译

[SubmitLongTextTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-submitlongtexttranslatetask)

提交长文本翻译任务

通义多模态翻译提交长文翻译任务

[GetLongTextTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-getlongtexttranslatetask)

获取长文本翻译任务结果

通义多模态翻译获取长文翻译结果

[SubmitHtmlTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-submithtmltranslatetask)

提交html翻译任务

通义多模态翻译提交html翻译任务

[GetHtmlTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-gethtmltranslatetask)

获取html翻译任务结果

通义多模态翻译获取html翻译结果

[TermEdit](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-termedit)

术语库编辑

通义多模态翻译术语库编辑

[TermQuery](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-termquery)

术语库查询

通义多模态翻译术语库查询

## 图片翻译

API

标题

API概述

[GetImageTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-getimagetranslatetask)

获取图片翻译任务结果

通义多模态翻译获取图片翻译结果

[SubmitImageTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-submitimagetranslatetask)

提交图片翻译任务

通义多模态翻译提交图片翻译任务

## 文档翻译

API

标题

API概述

[SubmitDocTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-submitdoctranslatetask)

文档翻译任务提交

通义多模态翻译提交文档翻译任务。

[GetDocTranslateTask](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-getdoctranslatetask)

文档翻译结果获取

通义多模态翻译获取文档翻译结果

## 其他

API

标题

API概述

[BatchTranslateForHtml](https://help.aliyun.com/zh/model-studio/api-anytrans-2025-07-07-batchtranslateforhtml)

网页批量翻译

# API概览

## API标准及多语言预置SDK

本产品（`晓蜜客服语音对话机器人/2025-01-01`）的 OpenAPI 采用 RPC 签名机制，具体签名方式请参见[签名机制说明](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)。我们已为开发者封装了主流编程语言的 SDK，您可通过 [下载 SDK](https://api.aliyun.com/api-tools/sdk/BailianVoiceBot?version=2025-01-01) 快速调用 API，无需关注签名等底层实现细节，显著降低开发门槛与集成复杂度。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的 [RAM 用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## API目录

API

标题

API概述

[BridgeWebCall](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-bridgewebcall)

软电话测试通话

创建软电话测试通话。

[GetDataChannelCredential](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getdatachannelcredential)

获取数据通道凭证

获取数据通道凭证。

[GenerateFileUploadParams](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-generatefileuploadparams)

获取文件上传参数

## MQ消息订阅配置

API

标题

API概述

[UpdateSubscription](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatesubscription)

更新订阅信息

[GetSubscription](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getsubscription)

获取消息订阅配置信息

[DisableSubscription](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-disablesubscription)

关闭消息订阅

## 变量管理

API

标题

API概述

[DeleteVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deletevariable)

删除变量

[ListVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvariable)

获取变量列表

[UpdateVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatevariable)

更新变量

[CreateVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createvariable)

创建变量

## 三方语音配置

API

标题

API概述

[ListVoiceEngines](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvoiceengines)

获取三方语音引擎列表

[UpdateVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatevoiceaccessprofile)

更新三方语音配置

[ListVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvoiceaccessprofile)

获取三方语音配置列表

[DeleteVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deletevoiceaccessprofile)

删除三方语音配置

[CreateVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createvoiceaccessprofile)

创建三方语音配置

## 热词管理

API

标题

API概述

[UpdateVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatevocabulary)

更新热词

[ListVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvocabulary)

获取热词列表

[ImportVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-importvocabulary)

导入热词

[GetVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getvocabulary)

获取热词信息

[ExportVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-exportvocabulary)

导出热词

[DeleteVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deletevocabulary)

删除热词

[CreateVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createvocabulary)

创建热词

## 克隆音管理

API

标题

API概述

[ListCloneVoiceModels](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listclonevoicemodels)

获取克隆音模型列表

[DeleteCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deleteclonevoice)

删除克隆音

[ListCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listclonevoice)

获取克隆音列表

[UpdateCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updateclonevoice)

更新克隆音

[CreateCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createclonevoice)

创建克隆音

## 应用管理

API

标题

API概述

[DeleteApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deleteapplication)

删除语音机器人应用

删除应用

[ListNluModels](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listnlumodels)

获取对话大模型列表

[PreviewVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-previewvoice)

TTS合成试听

[ListBackgroundMusics](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listbackgroundmusics)

获取背景音列表

[ListVoices](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvoices)

获取音色列表

[ListApplications](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listapplications)

查询语音机器人应用列表

查询语音机器人应用列表。

[CreateApplicationVersion](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createapplicationversion)

创建语音机器人应用版本

创建语音机器人应用版本。

[UpdateApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updateapplication)

修改语音机器人应用

修改语音机器人应用。

[CreateApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createapplication)

创建语音机器人应用

创建语音机器人应用。

[GetApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getapplication)

获取语音机器人应用

获取语音机器人应用。

[UpdateApplicationVersion](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updateapplicationversion)

修改语音机器人应用版本

修改场景版本。

[PublishApplicationVersion](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-publishapplicationversion)

发布语音机器人

发布语音机器人版本

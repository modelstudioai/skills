# API概览

## API标准及多语言预置SDK

本产品（`BailianVoiceBot/2025-01-01`）的OpenAPI采用[RPC](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/BailianVoiceBot?version=2025-01-01)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## API目录

API

标题

API概述

[BridgeWebCall](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-bridgewebcall.md)

软电话测试通话

创建软电话测试通话。

[GetDataChannelCredential](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-getdatachannelcredential.md)

获取数据通道凭证

获取数据通道凭证。

[GenerateFileUploadParams](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-generatefileuploadparams.md)

获取文件上传参数

获取文件上传信息

## MQ消息订阅配置

API

标题

API概述

[UpdateSubscription](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-mq-message-subscription-configuration/api-bailianvoicebot-2025-01-01-updatesubscription.md)

更新订阅信息

创建或更新MQ配置

[GetSubscription](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-mq-message-subscription-configuration/api-bailianvoicebot-2025-01-01-getsubscription.md)

获取消息订阅配置信息

获取MQ配置

[DisableSubscription](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-mq-message-subscription-configuration/api-bailianvoicebot-2025-01-01-disablesubscription.md)

关闭消息订阅

禁用消息订阅

## 变量管理

API

标题

API概述

[DeleteVariable](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-variable-management/api-bailianvoicebot-2025-01-01-deletevariable.md)

删除变量

删除变量

[ListVariable](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-variable-management/api-bailianvoicebot-2025-01-01-listvariable.md)

获取变量列表

获取变量列表

[UpdateVariable](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-variable-management/api-bailianvoicebot-2025-01-01-updatevariable.md)

更新变量

更新变量

[CreateVariable](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-variable-management/api-bailianvoicebot-2025-01-01-createvariable.md)

创建变量

创建变量

## 三方语音配置

API

标题

API概述

[ListVoiceEngines](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-three-way-voice-configuration/api-bailianvoicebot-2025-01-01-listvoiceengines.md)

获取三方语音引擎列表

获取引擎列表

[UpdateVoiceAccessProfile](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-three-way-voice-configuration/api-bailianvoicebot-2025-01-01-updatevoiceaccessprofile.md)

更新三方语音配置

更新三方语音配置

[ListVoiceAccessProfile](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-three-way-voice-configuration/api-bailianvoicebot-2025-01-01-listvoiceaccessprofile.md)

获取三方语音配置列表

获取三方语音配置列表

[DeleteVoiceAccessProfile](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-three-way-voice-configuration/api-bailianvoicebot-2025-01-01-deletevoiceaccessprofile.md)

删除三方语音配置

删除三方语音配置

[CreateVoiceAccessProfile](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-three-way-voice-configuration/api-bailianvoicebot-2025-01-01-createvoiceaccessprofile.md)

创建三方语音配置

创建实例

## 热词管理

API

标题

API概述

[UpdateVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-updatevocabulary.md)

更新热词

更新实例

[ListVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-listvocabulary.md)

获取热词列表

获取实例详情

[ImportVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-importvocabulary.md)

导入热词

导入热词

[GetVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-getvocabulary.md)

获取热词信息

获取实例详情

[ExportVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-exportvocabulary.md)

导出热词

导出热词

[DeleteVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-deletevocabulary.md)

删除热词

删除场景

[CreateVocabulary](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-hot-word-management/api-bailianvoicebot-2025-01-01-createvocabulary.md)

创建热词

创建实例

## 克隆音管理

API

标题

API概述

[ListCloneVoiceModels](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-clone-tone-management/api-bailianvoicebot-2025-01-01-listclonevoicemodels.md)

获取克隆音模型列表

获取克隆音色可用模型列表

[DeleteCloneVoice](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-clone-tone-management/api-bailianvoicebot-2025-01-01-deleteclonevoice.md)

删除克隆音

删除场景

[ListCloneVoice](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-clone-tone-management/api-bailianvoicebot-2025-01-01-listclonevoice.md)

获取克隆音列表

获取实例详情

[UpdateCloneVoice](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-clone-tone-management/api-bailianvoicebot-2025-01-01-updateclonevoice.md)

更新克隆音

更新实例

[CreateCloneVoice](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-clone-tone-management/api-bailianvoicebot-2025-01-01-createclonevoice.md)

创建克隆音

创建克隆音

## 应用管理

API

标题

API概述

[DeleteApplication](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-deleteapplication.md)

删除语音机器人应用

删除应用

[ListNluModels](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-listnlumodels.md)

获取对话大模型列表

获取对话模型列表

[PreviewVoice](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-previewvoice.md)

TTS合成试听

试听

[ListBackgroundMusics](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-listbackgroundmusics.md)

获取背景音列表

获取背景音列表

[ListVoices](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-listvoices.md)

获取音色列表

获取音色列表

[ListApplications](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-listapplications.md)

查询语音机器人应用列表

查询语音机器人应用列表。

[CreateApplicationVersion](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-createapplicationversion.md)

创建语音机器人应用版本

创建语音机器人应用版本。

[UpdateApplication](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-updateapplication.md)

修改语音机器人应用

修改语音机器人应用。

[CreateApplication](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-createapplication.md)

创建语音机器人应用

创建语音机器人应用。

[GetApplication](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-getapplication.md)

获取语音机器人应用

获取语音机器人应用。

[UpdateApplicationVersion](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-updateapplicationversion.md)

修改语音机器人应用版本

修改场景版本。

[PublishApplicationVersion](raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot/api-reference-chat6/api-bailianvoicebot-2025-01-01-dir/api-bailianvoicebot-2025-01-01-dir-application-management/api-bailianvoicebot-2025-01-01-publishapplicationversion.md)

发布语音机器人

发布语音机器人版本

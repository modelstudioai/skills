# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用RAM可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM中使用权限策略描述授权的具体内容。

本文为您介绍大模型服务平台百炼（BailianVoiceBot）为RAM权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。大模型服务平台百炼（BailianVoiceBot）的RAM代码（RamCode）为 bailianvoicebot，支持的授权粒度为操作级。

## 权限策略通用结构

权限策略支持JSON格式，其通用结构如下：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "<Effect>",
      "Action": "<Action>",
      "Resource": "<Resource>",
      "Condition": {
        "<Condition_operator>": {
          "<Condition_key>": [
            "<Condition_value>"
          ]
        }
      }
    }
  ]
}
```

各字段含义如下：

-   Effect：权限策略效果。取值：Allow（允许）、Deny（拒绝）。
-   Action：授予允许或拒绝权限的具体操作。具体信息，请参见[操作（Action）](#title-auth-detail-2)。
-   Resource：受操作影响的具体对象，您可以使用资源ARN来描述指定资源。具体信息，请参见[资源（Resource）](#title-auth-detail-3)。
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](#title-auth-detail-4)。
    -   Condition\_operator：条件运算符，不同类型的条件对应不同的条件运算符。具体信息，请参见[权限策略基本元素](https://help.aliyun.com/zh/ram/policy-elements)。
    -   Condition\_key：条件关键字。
    -   Condition\_value：条件关键字对应的值。

## 操作（Action）

下表是大模型服务平台百炼（BailianVoiceBot）定义的操作，这些操作可以在RAM权限策略语句的`Action`元素中使用，用来授予执行该操作的权限。下面对表中的具体项提供说明：

-   操作：是指具体的权限点。
-   API：是指操作对应的API接口。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。该列不体现适用于任何操作的[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

API

访问级别

资源类型

条件关键字

关联操作

bailianvoicebot:BridgeWebCall

[BridgeWebCall](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-bridgewebcall)

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateApplication

[CreateApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createapplication)

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateApplicationVersion

[CreateApplicationVersion](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createapplicationversion)

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateCloneVoice

[CreateCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createclonevoice)

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateVariable

[CreateVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createvariable)

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateVocabulary

[CreateVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createvocabulary)

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateVoiceAccessProfile

[CreateVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-createvoiceaccessprofile)

create

\*全部资源

`*`

无

无

bailianvoicebot:DeleteApplication

[DeleteApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deleteapplication)

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteCloneVoice

[DeleteCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deleteclonevoice)

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteVariable

[DeleteVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deletevariable)

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteVocabulary

[DeleteVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deletevocabulary)

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteVoiceAccessProfile

[DeleteVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-deletevoiceaccessprofile)

delete

\*全部资源

`*`

无

无

bailianvoicebot:DisableSubscription

[DisableSubscription](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-disablesubscription)

update

\*全部资源

`*`

无

无

bailianvoicebot:ExportVocabulary

[ExportVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-exportvocabulary)

get

\*全部资源

`*`

无

无

bailianvoicebot:GenerateFileUploadParams

[GenerateFileUploadParams](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-generatefileuploadparams)

update

\*全部资源

`*`

无

无

bailianvoicebot:GetApplication

[GetApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getapplication)

get

\*全部资源

`*`

无

无

bailianvoicebot:GetDataChannelCredential

[GetDataChannelCredential](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getdatachannelcredential)

get

\*全部资源

`*`

无

无

bailianvoicebot:GetSubscription

[GetSubscription](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getsubscription)

get

\*全部资源

`*`

无

无

bailianvoicebot:GetVocabulary

[GetVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-getvocabulary)

get

\*全部资源

`*`

无

无

bailianvoicebot:ImportVocabulary

[ImportVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-importvocabulary)

create

\*全部资源

`*`

无

无

bailianvoicebot:ListApplications

[ListApplications](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listapplications)

none

\*全部资源

`*`

无

无

bailianvoicebot:ListBackgroundMusics

[ListBackgroundMusics](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listbackgroundmusics)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListCloneVoice

[ListCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listclonevoice)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListCloneVoiceModels

[ListCloneVoiceModels](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listclonevoicemodels)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListNluModels

[ListNluModels](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listnlumodels)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVariable

[ListVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvariable)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVocabulary

[ListVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvocabulary)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVoiceAccessProfile

[ListVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvoiceaccessprofile)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVoiceEngines

[ListVoiceEngines](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvoiceengines)

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVoices

[ListVoices](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-listvoices)

list

\*全部资源

`*`

无

无

bailianvoicebot:PreviewVoice

[PreviewVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-previewvoice)

create

\*全部资源

`*`

无

无

bailianvoicebot:PublishApplicationVersion

[PublishApplicationVersion](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-publishapplicationversion)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateApplication

[UpdateApplication](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updateapplication)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateApplicationVersion

[UpdateApplicationVersion](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updateapplicationversion)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateCloneVoice

[UpdateCloneVoice](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updateclonevoice)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateSubscription

[UpdateSubscription](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatesubscription)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateVariable

[UpdateVariable](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatevariable)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateVocabulary

[UpdateVocabulary](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatevocabulary)

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateVoiceAccessProfile

[UpdateVoiceAccessProfile](https://help.aliyun.com/zh/model-studio/api-bailianvoicebot-2025-01-01-updatevoiceaccessprofile)

update

\*全部资源

`*`

无

无

## 资源（Resource）

大模型服务平台百炼（BailianVoiceBot）不支持在RAM权限策略语句的`Resource`中指定资源ARN。如果要允许对大模型服务平台百炼（BailianVoiceBot）的访问权限，请在策略语句中指定`"Resource": "*"`。

## 条件（Condition）

大模型服务平台百炼（BailianVoiceBot）未定义产品级别的条件关键字。如需查看适用于所有云产品的通用条件关键字，请参见[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。

## 相关操作

您可以创建自定义权限策略，并将权限策略授予RAM用户、RAM用户组或RAM角色。具体操作如下：

-   [创建自定义权限策略](https://help.aliyun.com/zh/ram/create-a-custom-policy)
-   [为RAM用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)
-   [为RAM用户组授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-user-group)
-   [为RAM角色授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-role)

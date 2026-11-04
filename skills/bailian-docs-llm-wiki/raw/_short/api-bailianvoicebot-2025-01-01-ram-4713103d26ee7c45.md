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
    
-   Action：授予允许或拒绝权限的具体操作。具体信息，请参见操作（Action）。
    
-   Resource：受操作影响的具体对象，您可以使用资源ARN来描述指定资源。具体信息，请参见资源（Resource）。
    
-   Condition：指授权生效的条件。可选字段。具体信息，请参见条件（Condition）。
    
    -   Condition\_operator：条件运算符，不同类型的条件对应不同的条件运算符。具体信息，请参见权限策略基本元素。
    -   Condition\_key：条件关键字。
    -   Condition\_value：条件关键字对应的值。

## 操作（Action）

下表是大模型服务平台百炼（BailianVoiceBot）定义的操作，这些操作可以在RAM权限策略语句的`Action`元素中使用，用来授予执行该操作的权限。下面对表中的具体项提供说明：

-   操作：是指具体的权限点。
    
-   API：是指操作对应的API接口。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用全部资源表示。
-   条件关键字：是指云产品自身定义的条件关键字。该列不体现适用于任何操作的通用条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

操作

API

访问级别

资源类型

条件关键字

关联操作

bailianvoicebot:BridgeWebCall

BridgeWebCall

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateApplication

CreateApplication

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateApplicationVersion

CreateApplicationVersion

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateCloneVoice

CreateCloneVoice

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateVariable

CreateVariable

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateVocabulary

CreateVocabulary

create

\*全部资源

`*`

无

无

bailianvoicebot:CreateVoiceAccessProfile

CreateVoiceAccessProfile

create

\*全部资源

`*`

无

无

bailianvoicebot:DeleteApplication

DeleteApplication

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteCloneVoice

DeleteCloneVoice

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteVariable

DeleteVariable

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteVocabulary

DeleteVocabulary

delete

\*全部资源

`*`

无

无

bailianvoicebot:DeleteVoiceAccessProfile

DeleteVoiceAccessProfile

delete

\*全部资源

`*`

无

无

bailianvoicebot:DisableSubscription

DisableSubscription

update

\*全部资源

`*`

无

无

bailianvoicebot:ExportVocabulary

ExportVocabulary

get

\*全部资源

`*`

无

无

bailianvoicebot:GenerateFileUploadParams

GenerateFileUploadParams

update

\*全部资源

`*`

无

无

bailianvoicebot:GetApplication

GetApplication

get

\*全部资源

`*`

无

无

bailianvoicebot:GetDataChannelCredential

GetDataChannelCredential

get

\*全部资源

`*`

无

无

bailianvoicebot:GetSubscription

GetSubscription

get

\*全部资源

`*`

无

无

bailianvoicebot:GetVocabulary

GetVocabulary

get

\*全部资源

`*`

无

无

bailianvoicebot:ImportVocabulary

ImportVocabulary

create

\*全部资源

`*`

无

无

bailianvoicebot:ListApplications

ListApplications

none

\*全部资源

`*`

无

无

bailianvoicebot:ListBackgroundMusics

ListBackgroundMusics

list

\*全部资源

`*`

无

无

bailianvoicebot:ListCloneVoice

ListCloneVoice

list

\*全部资源

`*`

无

无

bailianvoicebot:ListCloneVoiceModels

ListCloneVoiceModels

list

\*全部资源

`*`

无

无

bailianvoicebot:ListNluModels

ListNluModels

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVariable

ListVariable

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVocabulary

ListVocabulary

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVoiceAccessProfile

ListVoiceAccessProfile

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVoiceEngines

ListVoiceEngines

list

\*全部资源

`*`

无

无

bailianvoicebot:ListVoices

ListVoices

list

\*全部资源

`*`

无

无

bailianvoicebot:PreviewVoice

PreviewVoice

create

\*全部资源

`*`

无

无

bailianvoicebot:PublishApplicationVersion

PublishApplicationVersion

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateApplication

UpdateApplication

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateApplicationVersion

UpdateApplicationVersion

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateCloneVoice

UpdateCloneVoice

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateSubscription

UpdateSubscription

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateVariable

UpdateVariable

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateVocabulary

UpdateVocabulary

update

\*全部资源

`*`

无

无

bailianvoicebot:UpdateVoiceAccessProfile

UpdateVoiceAccessProfile

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

-   创建自定义权限策略
-   为RAM用户授权
-   为RAM用户组授权
-   为RAM角色授权

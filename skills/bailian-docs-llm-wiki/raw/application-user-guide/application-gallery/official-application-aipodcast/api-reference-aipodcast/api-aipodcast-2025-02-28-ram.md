# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用RAM可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM中使用权限策略描述授权的具体内容。

本文为您介绍大模型服务平台百炼（AIPodcast）为RAM权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。大模型服务平台百炼（AIPodcast）的RAM代码（RamCode）为 aipodcast，支持的授权粒度为操作级。

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

下表是大模型服务平台百炼（AIPodcast）定义的操作，这些操作可以在RAM权限策略语句的`Action`元素中使用，用来授予执行该操作的权限。下面对表中的具体项提供说明：

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

aipodcast:PodcastTaskResultQuery

[PodcastTaskResultQuery](https://help.aliyun.com/zh/model-studio/api-aipodcast-2025-02-28-podcasttaskresultquery)

none

\*全部资源

`*`

无

无

aipodcast:PodcastTaskSubmit

[PodcastTaskSubmit](https://help.aliyun.com/zh/model-studio/api-aipodcast-2025-02-28-podcasttasksubmit)

none

\*全部资源

`*`

无

无

## 资源（Resource）

大模型服务平台百炼（AIPodcast）不支持在RAM权限策略语句的`Resource`中指定资源ARN。如果要允许对大模型服务平台百炼（AIPodcast）的访问权限，请在策略语句中指定`"Resource": "*"`。

## 条件（Condition）

大模型服务平台百炼（AIPodcast）未定义产品级别的条件关键字。如需查看适用于所有云产品的通用条件关键字，请参见[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。

## 相关操作

您可以创建自定义权限策略，并将权限策略授予RAM用户、RAM用户组或RAM角色。具体操作如下：

-   [创建自定义权限策略](https://help.aliyun.com/zh/ram/create-a-custom-policy)
-   [为RAM用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)
-   [为RAM用户组授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-user-group)
-   [为RAM角色授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-role)

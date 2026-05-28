# 服务关联角色

为实现特定功能，百炼需要通过服务关联角色（SLR）获取对其他云服务（如FC、内容安全等）或云资源的访问权限。当您首次在百炼中授权开通相关功能（如函数计算节点）时，**系统将自动为您创建对应的服务关联角色**。本文为您介绍百炼创建的服务关联角色及其删除办法。

## 百炼创建的服务关联角色

> 您可以前往[RAM控制台](https://ram.console.aliyun.com/)的角色管理页面查看所有服务关联角色。

**服务关联角色名称**

**服务关联角色描述**

[AliyunServiceRoleForSFMAccessFC](#Bd0OF)

[百炼工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)和[流程编排](https://help.aliyun.com/zh/model-studio/what-is-process-orchestration-old)通过此服务关联角色访问您在[FC](https://help.aliyun.com/zh/functioncompute/fc/product-overview/what-is-function-compute)中的资源。

[AliyunServiceRoleForSFMDataHubOSSImport](#2b75fc8a97g4c)

[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/)通过此服务关联角色访问您在[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源。

[AliyunServiceRoleForAccessOSS](#13012d75c0zat)

[安全存储空间](https://help.aliyun.com/zh/model-studio/secure-storage/)通过此服务关联角色访问您在[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源。

[AliyunServiceRoleForSFMAccessADB](#7deade0402e0y)

[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)和[安全存储空间](https://help.aliyun.com/zh/model-studio/secure-storage/)通过此服务关联角色访问您的[ADB-PG](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/product-overview/overview-product-overview)实例。

[AliyunServiceRoleForSFMAccessingMNS](#e412ddc7eac5w)

[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/)通过此服务关联角色访问[MNS](https://help.aliyun.com/zh/mns/product-overview/what-is-mns)队列中的[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)变更消息。

[AliyunServiceRoleForSFMTelemetry](#4223df3814svi)

[用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation)通过此服务关联角色访问您的[OpenTelemetry](https://help.aliyun.com/zh/opentelemetry/product-overview/what-is-managed-service-for-opentelemetry)实例。

[AliyunServiceRoleForSFMAccessingCIP](#ff0270f337iy4)

[百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)通过此服务关联角色访问您在[内容安全](https://help.aliyun.com/zh/document_detail/28417.html)中的服务或资源。

[AliyunServiceRoleForSFMAccessSLS](#4fdbab8ea2tp9)

[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)通过此服务关联角色访问您在[SLS](https://help.aliyun.com/zh/sls/what-is-log-service)中的资源。

[AliyunServiceRoleForSFMAccessCMS](#0cf6db69c5z5n)

[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)通过此服务关联角色访问您在[CMS](https://help.aliyun.com/zh/cms/cloudmonitor-2-0/what-is-cloud-monitor-2-0)中的资源。

[AliyunServiceRoleForAccessCusOss](#21281ba873vnj)

阿里云百炼平台通过此服务关联角色访问您在[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源，使用该权限操作您的OSS文件，实现百炼平台对OSS操作的托管。

[AliyunServiceRoleForSFMConnectorAccessDTS](#7f75202592td7)

阿里云百炼平台通过此服务关联角色访问您在[DTS](https://help.aliyun.com/zh/dts/product-overview/what-is-dts)中的资源，使用该权限创建和管理DTS任务，实现从指定数据源接入数据到百炼平台。

[AliyunServiceRoleForSFMFineTuning](#l8g2h4i7j6k9l)

[模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/)和[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/)使用此服务关联角色访问您在[CPFS](https://help.aliyun.com/zh/cpfs/cpfs-product-introduction)和[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源。

## **AliyunServiceRoleForSFMAccessFC**

### **应用场景**

百炼[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)和[流程编排](https://help.aliyun.com/zh/model-studio/what-is-process-orchestration-old)中的函数计算节点通过此服务关联角色访问您在[FC](https://help.aliyun.com/zh/functioncompute/fc/product-overview/what-is-function-compute)中的资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMAccessFC`

关联的系统策略：`AliyunServiceRolePolicyForSFMAccessFC`

该系统策略的权限说明：

```
{
  "Action": [
    "fc:ListFunctions",
    "fc:InvokeFunction"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，工作流应用和流程编排将无法创建和调用函数计算节点，请谨慎操作！

删除AliyunServiceRoleForSFMAccessFC服务关联角色前，须先删除所有已发布的工作流应用和流程中的函数计算节点（删除后需要重新发布应用或流程）。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

## AliyunServiceRoleForSFMDataHubOSSImport

### **应用场景**

百炼[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/)中的OSS数据导入功能通过此服务关联角色访问您在[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMDataHubOSSImport`

关联的系统策略：`AliyunServiceRolePolicyForSFMDataHubOSSImport`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:ListBuckets",
        "oss:GetBucketLocation",
        "oss:GetBucketTagging"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:DoMetaQuery",
        "oss:GetBucketInfo",
        "oss:GetBucketStat",
        "oss:GetBucketTransferAcceleration",
        "oss:GetCnameToken",
        "oss:GetMetaQueryStatus",
        "oss:GetObject",
        "oss:GetObjectTagging",
        "oss:DescribeRegions",
        "oss:ListObjects",
        "oss:ListObjectVersions"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "oss:BucketTag/bailian-datahub-access": [
            "read"
          ]
        }
      }
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "datahub.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，数据管理将无法访问您在OSS中的资源，请谨慎操作！

删除AliyunServiceRoleForSFMDataHubOSSImport服务关联角色前，请确保数据管理中没有正在进行中的OSS数据导入任务。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

## **AliyunServiceRoleForAccessOSS**

### 应用场景

百炼[安全存储空间](https://help.aliyun.com/zh/model-studio/secure-storage/)通过此服务关联角色访问您在[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForAccessOSS`

关联的系统策略：`AliyunServiceRolePolicyForAccessOSS`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:ListBuckets",
        "oss:GetBucketLocation",
        "oss:GetBucketTagging"
      ],
      "Resource": [
        "*"
      ],
      "Condition": {}
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:DoMetaQuery",
        "oss:GetBucketInfo",
        "oss:GetBucketStat",
        "oss:GetBucketTransferAcceleration",
        "oss:GetCnameToken",
        "oss:GetMetaQueryStatus",
        "oss:GetObject",
        "oss:GetObjectTagging",
        "oss:DescribeRegions",
        "oss:ListObjects",
        "oss:ListObjectVersions",
        "oss:PutObjectTagging",
        "oss:DeleteObject",
        "oss:DeleteObjectTagging",
        "oss:PutObject"
      ],
      "Resource": [
        "*"
      ],
      "Condition": {
        "StringEquals": {
          "oss:BucketTag/bailian-safe-workspace-oss-access": [
            "ReadAndWrite"
          ]
        }
      }
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "ossaccess.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，安全存储空间将无法访问您在OSS中的资源，请谨慎操作！

删除AliyunServiceRoleForAccessOSS服务关联角色前，请确保您已在安全存储空间中断开所有OSS连接。如何断开连接，请参见[断开连接](https://help.aliyun.com/zh/model-studio/configure-zone-ip#eda3c411315pd)。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

## **AliyunServiceRoleForSFMAccessADB**

### 应用场景

百炼[安全存储空间](https://help.aliyun.com/zh/model-studio/secure-storage/)通过此服务关联角色访问您的 [ADB-PG](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/product-overview/overview-product-overview) 数据库实例。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMAccessADB`

关联的系统策略：`AliyunServiceRolePolicyForSFMAccessADB`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "gpdb:DescribeDBInstanceAttribute",
        "gpdb:DescribeDBInstances",
        "gpdb:CreateVectorManagerAccount",
        "gpdb:QueryCollectionData",
        "gpdb:UpsertCollectionData",
        "gpdb:DeleteVectorIndex",
        "gpdb:CreateVectorIndex",
        "gpdb:CreateNamespace",
        "gpdb:ListNamespaces",
        "gpdb:DescribeNamespace",
        "gpdb:DeleteNamespace",
        "gpdb:ListCollections",
        "gpdb:GrantCollection",
        "gpdb:DescribeCollection",
        "gpdb:DeleteCollectionData",
        "gpdb:DeleteCollection",
        "gpdb:CreateCollection",
        "gpdb:UpdateCollectionDataMetadata"
      ],
      "Resource": "*"
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "adb-access.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，安全存储空间将无法访问您的ADB-PG实例，请谨慎操作！

删除AliyunServiceRoleForSFMAccessADB服务关联角色前，请确保您已在安全存储空间中断开所有ADB-PG连接。如何断开连接，请参见[断开连接](https://help.aliyun.com/zh/model-studio/configure-zone-ip#eda3c411315pd)。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

## AliyunServiceRoleForSFMAccessingMNS

### **应用场景**

百炼[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/)通过此服务关联角色访问[MNS](https://help.aliyun.com/zh/mns/product-overview/what-is-mns)队列中的[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)变更消息，以实现对您在OSS中的资源（数据）变更的自动同步。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMAccessingMNS`

关联的系统策略：`AliyunServiceRolePolicyForSFMAccessingMNS`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "mns:GetQueueAttributes",
        "mns:GetSubscriptionAttributes",
        "mns:GetTopicAttributes",
        "mns:ListEventNotifications",
        "mns:GetAccountAttributes",
        "mns:ListEvents",
        "mns:ListProducts",
        "mns:ListQueue",
        "mns:ListSubscriptionByTopic",
        "mns:ListTagResources",
        "mns:ListTopic",
        "mns:ReceiveMessage",
        "mns:DeleteMessage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "mns:CreateQueue",
        "mns:DeleteQueue",
        "mns:SetQueueAttributes"
      ],
      "Resource": "acs:mns:*:*:/queues/bailian-oss-event*"
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "mns-access.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### **删除服务关联角色**

本策略由大模型服务平台百炼定义并使用，请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份。

## **AliyunServiceRoleForSFMTelemetry**

### 应用场景

[用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation)通过此服务关联角色访问您的[OpenTelemetry](https://help.aliyun.com/zh/opentelemetry/product-overview/what-is-managed-service-for-opentelemetry)实例。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMTelemetry`

关联的系统策略：`AliyunServiceRolePolicyForSFMTelemetry`

该系统策略的权限说明：

```
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "log:Get*",
                "log:List*",
                "log:Query*"
            ],
            "Resource": [
                "acs:log:*:*:project/proj-xtrace-*",
                "acs:log:*:*:project/proj-xtrace-*/logstore/logstore-tracing",
                "acs:log:*:*:project/proj-xtrace-*/logstore/logstore-tracing/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "arms:Describe*",
                "arms:List*",
                "arms:Get*",
                "arms:Search*",
                "arms:Check*",
                "arms:Query*",
                "arms:InitTraceResource"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "xtrace:Read*",
                "xtrace:Get*",
                "xtrace:Describe*",
                "xtrace:Check*",
                "xtrace:OpenXtraceService"
            ],
            "Resource": "*"
        },
        {
            "Action": "ram:DeleteServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": "telemetry.sfm.aliyuncs.com"
                }
            }
        },
        {
            "Action": "ram:CreateServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": [
                        "arms.aliyuncs.com",
                        "xtrace.aliyuncs.com",
                        "cloudmonitor.aliyuncs.com"
                    ]
                }
            }
        }
    ]
}
```

### 删除服务关联角色

本策略由大模型服务平台百炼定义并使用，请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份。

## AliyunServiceRoleForSFMAccessingCIP

### 应用场景

[百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)通过此服务关联角色访问您在[内容安全](https://help.aliyun.com/zh/document_detail/28417.html)中的服务或资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMAccessingCIP`

关联的系统策略：`AliyunServiceRolePolicyForSFMAccessingCIP`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "yundun-greenweb:ModerationForBaiLian",
      "Resource": "acs:yundun-greenweb:*:*:*"
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "content-security.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### 删除服务关联角色

本策略由大模型服务平台百炼定义并使用，请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份。

## **AliyunServiceRoleFor**SFMAccessSLS

### 应用场景

百炼[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)通过此服务关联角色访问您在[SLS](https://help.aliyun.com/zh/sls/what-is-log-service)中的资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMAccessSLS`

关联的系统策略：`AliyunServiceRolePolicyForSFMAccessSLS`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Action": [
        "log:GetProject",
        "log:GetLogs",
        "log:GetLogStoreLogs",
        "log:GetProductDataCollection",
        "log:OpenProductDataCollection",
        "log:CloseProductDataCollection"
      ],
      "Resource": [
        "acs:log:*:*:project/aliyun-product-data-*",
        "acs:log:*:*:project/aliyun-product-data-*/logstore/bailian-*",
        "acs:log:*:*:project/aliyun-product-data-*/logstore/bailian-*/*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "log:GetSlsService",
        "log:OpenSlsService",
        "log:DescribeService",
        "log:EnableService"
      ],
      "Resource": [
        "acs:log:*:*:service"
      ],
      "Effect": "Allow"
    },
    {
      "Action": "ram:CreateServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": [
            "sls-access.sfm.aliyuncs.com",
            "audit.log.aliyuncs.com",
            "middlewarelens.log.aliyuncs.com",
            "securitylens.log.aliyuncs.com",
            "ai-lens.log.aliyuncs.com",
            "storagelens.log.aliyuncs.com"
          ]
        }
      }
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "sls-access.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### 删除服务关联角色

本策略由大模型服务平台百炼定义并使用，请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份。

## **AliyunServiceRoleFor**SFMAccessCMS

### 应用场景

百炼[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)通过此服务关联角色访问您在[CMS](https://help.aliyun.com/zh/cms/cloudmonitor-2-0/what-is-cloud-monitor-2-0)中的资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMAccessCMS`

关联的系统策略：`AliyunServiceRolePolicyForSFMAccessCMS`

该系统策略的权限说明：

```
{
    "Version": "1",
    "Statement": [
        {
            "Action": "cms:GetCmsService",
            "Resource": "acs:cms:*:*:cmsservice/*",
            "Effect": "Allow"
        },
        {
            "Action": "cms:GetPrometheusInstance",
            "Resource": "acs:cms:*:*:prometheusinstance/*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "log:GetProject",
                "log:GetLogs",
                "log:GetLogStoreLogs",
                "log:QueryPrometheusMetrics",
                "log:QueryMetrics"
            ],
            "Resource": [
                "acs:log:*:*:project/aliyun-product-data-*",
                "acs:log:*:*:project/aliyun-product-data-*/logstore/bailian-*",
                "acs:log:*:*:project/aliyun-product-data-*/logstore/bailian-*/*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": "ram:DeleteServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": "cms-access.sfm.aliyuncs.com"
                }
            }
        }
    ]
}
```

### 删除服务关联角色

本策略由大模型服务平台百炼定义并使用，请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份。

## AliyunServiceRoleForAccessCusOss

### 应用场景

允许阿里云百炼平台访问您的[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)，使用该权限操作您的OSS文件，实现百炼平台对OSS操作的托管。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForAccessCusOss`

关联的系统策略：`AliyunServiceRolePolicyForAccessCusOss`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:ListBuckets",
        "oss:GetBucketLocation",
        "oss:GetBucketTagging"
      ],
      "Resource": [
        "*"
      ],
      "Condition": {}
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:DoMetaQuery",
        "oss:GetBucketInfo",
        "oss:GetBucketStat",
        "oss:GetBucketTransferAcceleration",
        "oss:GetCnameToken",
        "oss:GetMetaQueryStatus",
        "oss:GetObject",
        "oss:GetObjectTagging",
        "oss:DescribeRegions",
        "oss:ListObjects",
        "oss:ListObjectVersions",
        "oss:PutObjectTagging",
        "oss:DeleteObject",
        "oss:DeleteObjectTagging",
        "oss:PutObject",
        "oss:PutBucketCors"
      ],
      "Resource": [
        "*"
      ],
      "Condition": {
        "StringEquals": {
          "oss:BucketTag/bailian-connector-access": [
            "ReadAndWrite"
          ]
        }
      }
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "cus-oss-access.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，百炼将无法访问您在OSS中的资源，请谨慎操作！

删除AliyunServiceRoleForAccessCusOss服务关联角色前，请确保您已在阿里云百炼平台中断开所有OSS连接。如何断开连接，请参见[断开连接](https://help.aliyun.com/zh/model-studio/configure-zone-ip#eda3c411315pd)。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

## AliyunServiceRoleForSFMConnectorAccessDTS

### 应用场景

允许阿里云百炼平台访问您的[DTS](https://help.aliyun.com/zh/dts/product-overview/what-is-dts)，使用该权限创建和管理DTS任务，实现从指定数据源接入数据到百炼平台。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMConnectorAccessDTS`

关联的系统策略：`AliyunServiceRolePolicyForSFMConnectorAccessDTS`

该系统策略的权限说明：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dts:DescribeDtsJobDetail",
        "dts:StartDtsJob",
        "dts:StopDtsJob",
        "dts:DeleteDtsJob",
        "dts:SuspendDtsJob"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "acs:ResourceTag/bailian-connector-access": [
            "ReadAndWrite"
          ]
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "dts:CreateDtsInstance",
        "dts:ConfigureDtsJob",
        "dts:DescribeSchemaList",
        "dts:DescribeStruct",
        "dts:DescribeColumns",
        "dts:RunEndpointLinkTest",
        "dts:TagResources"
      ],
      "Resource": "*"
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "dts-access.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，百炼将无法访问您的DTS，请谨慎操作！

删除AliyunServiceRoleForSFMConnectorAccessDTS服务关联角色前，请确保您已在安全存储空间中断开所有DTS连接。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

## **AliyunServiceRoleForSFMFineTuning**

### **应用场景**

阿里云百炼[模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/)和[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/)通过此服务关联角色访问您在[CPFS](https://help.aliyun.com/zh/cpfs/cpfs-product-introduction)和[OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)中的资源。

### **角色及权限说明**

服务关联角色名称：`AliyunServiceRoleForSFMFineTuning`

关联的系统策略：`AliyunServiceRolePolicyForSFMFineTuning`

该系统策略的权限说明：

```
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "nas:ClientMount",
                "nas:DescribeCpfsAccessPoints",
                "nas:DescribeFileSystems"
            ],
            "Resource": "*"
        },
        {
            "Action": "ram:DeleteServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": "fine-tuning.sfm.aliyuncs.com"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "oss:ListBuckets",
                "oss:GetBucketLocation",
                "oss:GetBucketTagging"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "oss:DoMetaQuery",
                "oss:GetBucketInfo",
                "oss:GetBucketStat",
                "oss:GetBucketTransferAcceleration",
                "oss:GetCnameToken",
                "oss:GetMetaQueryStatus",
                "oss:GetObject",
                "oss:GetObjectTagging",
                "oss:DescribeRegions",
                "oss:ListObjects",
                "oss:ListObjectVersions",
                "oss:DoMetaQuery",
                "oss:GetMetaQueryStatus"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "oss:BucketTag/bailian-finetune-access": [
                        "read"
                    ]
                }
            }
        }
    ]
}
```

### **删除服务关联角色**

**警告**

删除此服务关联角色后，阿里云百炼模型调优和数据管理将无法访问您在CPFS和OSS中的资源，请谨慎操作！

删除AliyunServiceRoleForSFMFineTuning服务关联角色前，请确保模型调优中没有正在进行的训练任务，数据管理中没有正在进行的导入和发布任务。

如何删除服务关联角色，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)。

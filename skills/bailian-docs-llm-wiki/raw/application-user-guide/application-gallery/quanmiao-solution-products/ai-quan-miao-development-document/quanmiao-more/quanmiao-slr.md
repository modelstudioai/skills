# 全妙服务关联角色

本文介绍与全妙有关的服务关联角色有哪些以及如何删除这些角色。

## 背景信息

在某些场景下，全妙为了完成自身的某个功能，需要获取其他云服务的访问权限，如OSS、IMS等。我们借助阿里云提供的服务关联角色SLR（Service Linked Role）来满足此类场景的需求。SLR是获取其他云服务的访问权限而提供的RAM角色。更多关于服务关联角色的信息请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#concept-2448621)。

## 相关的服务关联角色

当前与全妙相关的SLR：

**角色名**

**角色描述**

AliyunServiceRoleForAIMiaoBiAccessingOss

用于阿里云全妙调用OSS产品的服务关联角色，全妙使用此角色来访问您在OSS中的服务或资源。

AliyunServiceRoleForAiMiaoBiAccessingIMS

用于阿里云全妙调用IMS（智能媒体服务）产品的服务关联角色，全妙使用此角色来访问您在IMS中的服务和资源。

## AliyunServiceRoleForAIMiaoBiAccessingOss

### 应用场景

全妙素材库等存储功能需要访问OSS云服务的资源时，可通过自动创建的服务关联角色AliyunServiceRoleForAIMiaoBiAccessingOss获取访问权限。

### 角色及权限说明

-   角色名称：AliyunServiceRoleForAIMiaoBiAccessingOss；
    
-   角色权限策略：AliyunServiceRolePolicyForAIMiaoBiAccessingOss；
    
-   权限说明：
    

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:ListBuckets"
      ],
      "Resource": "acs:oss:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:PutObject",
        "oss:ListParts",
        "oss:GetObject",
        "oss:AbortMultipartUpload",
        "oss:DeleteObject"
      ],
      "Resource": "acs:oss:*:*:*/aimiaobi/*"
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "oss-access-aimiaobi.sfm.aliyuncs.com"
        }
      }
    }
  ]
}
```

### 删除服务关联角色

如果您使用了全妙素材库等功能，然后需要删除全妙服务关联角色AliyunServiceRoleForAIMiaoBiAccessingOss，例如您出于安全考虑，需要删除该角色，则需要先明确删除后的影响：删除AliyunServiceRoleForAIMiaoBiAccessingOss后，全妙将无法新增和访问当前账号下已经存储的素材库等功能下存储到OSS的文件及数据。

关于删除服务关联角色具体操作，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#concept-2448621)。

## AliyunServiceRoleForAiMiaoBiAccessingIMS

### 应用场景

全妙数据集管理等多模态功能依赖智能媒体服务（IMS），访问该资源时，可通过自动创建的服务关联角色AliyunServiceRoleForAiMiaoBiAccessingIMS获取访问权限。

### 角色及权限说明

-   角色名称：AliyunServiceRoleForAiMiaoBiAccessingIMS；
    
-   角色权限策略：AliyunServiceRolePolicyForAiMiaoBiAccessingIMS；
    
-   权限说明：
    

```
{
    "Version": "1",
    "Statement": [
        {
            "Action": [
                "ice:CreateSearchLib",
                "ice:QuerySearchLib",
                "ice:DropSearchLib",
                "ice:ListSearchLib",
                "ice:CreateSearchIndex",
                "ice:QuerySearchIndex",
                "ice:AlterSearchIndex",
                "ice:DropSearchIndex",
                "ice:InsertMediaToSearchLib",
                "ice:DeleteMediaFromSearchLib",
                "ice:UpdateMediaToSearchLib",
                "ice:QueryMediaIndexJob",
                "ice:SearchIndexJobRerun",
                "ice:SearchMedia",
                "ice:SearchMediaByMultimodal",
                "ice:GetVideoList",
                "ice:SearchMediaByFace",
                "ice:SearchMediaClipByFace",
                "ice:SearchMediaByAILabel",
                "ice:SearchMediaByHybrid"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": "ram:DeleteServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": "ims.quanmiao.aliyuncs.com"
                }
            }
        }
    ]
}
```

### 删除服务关联角色

如果您使用了全妙数据集管理，然后需要删除全妙服务关联角色AliyunServiceRoleForAiMiaoBiAccessingIMS，例如您出于安全考虑，需要删除该角色，则需要先明确删除后的影响：删除AliyunServiceRoleForAiMiaoBiAccessingIMS后，全妙将无法新增和访问当前账号下已经存储的数据集下多模态索引数据。

关于删除服务关联角色具体操作，请参见[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#concept-2448621)。

## 常见问题

**Q**：为什么我的RAM用户无法自动创建全妙服务关联角色？

**A**：您需要拥有指定的权限，才能自动创建或删除服务关联角色。因此，在RAM用户无法自动创建时，您需为其添加以下权限策略。

请将主账号ID替换为您实际的阿里云账号（主账号）ID。

```
{
    "Statement": [
        {
            "Action": [
                "ram:CreateServiceLinkedRole"
            ],
            "Resource": "acs:ram:*:主账号ID:role/*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": [
                        "oss-access-aimiaobi.sfm.aliyuncs.com"
                    ]
                }
            }
        }
    ],
    "Version": "1"
}
```

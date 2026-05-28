# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用 RAM 可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM 中使用权限策略描述授权的具体内容。

本文为您介绍 _大模型服务平台百炼_ 为 RAM 权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。 _大模型服务平台百炼_ 的 RAM 代码（RamCode）为 _sfm_ ，支持的授权粒度为 _操作级_ 。

## 权限策略通用结构

权限策略支持 JSON 格式，其通用结构如下：

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
    
-   Resource：受操作影响的具体对象，您可以使用资源 ARN 来描述指定资源。具体信息，请参见[资源（Resource）](#title-auth-detail-3)。
    
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](#title-auth-detail-4)。
    
    -   Condition\_operator：条件运算符，不同类型的条件对应不同的条件运算符。具体信息，请参见[权限策略基本元素](https://help.aliyun.com/zh/ram/policy-elements)。
        
    -   Condition\_key：条件关键字。
        
    -   Condition\_value：条件关键字对应的值。
        

## 操作（Action）

下表是_大模型服务平台百炼_定义的操作，这些操作可以在 RAM 权限策略语句的`Action`元素中使用，用来授予执行该操作的权限。下面对表中的具体项提供说明：

-   操作：是指具体的权限点。
    
-   API：是指操作对应的 API 接口。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。该列不体现适用于任何操作的[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**API**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

sfm:UpdateChunk

[UpdateChunk](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updatechunk)

update

\*全部资源

`*****`

无

无

sfm:BatchUpdateFileTag

[BatchUpdateFileTag](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-batchupdatefiletag)

update

\*全部资源

`*****`

无

无

sfm:UpdateFileTag

[UpdateFileTag](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updatefiletag)

update

\*全部资源

`*****`

无

无

sfm:ListFile

[ListFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listfile)

list

\*全部资源

`*****`

无

无

sfm:ChangeParseSetting

[ChangeParseSetting](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-changeparsesetting)

update

\*全部资源

`*****`

无

无

sfm:UpdateMemoryNode

[UpdateMemoryNode](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updatememorynode)

update

\*全部资源

`*****`

无

无

sfm:DeleteCategory

[DeleteCategory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deletecategory)

delete

\*全部资源

`*****`

无

无

sfm:UpdateMemory

[UpdateMemory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updatememory)

update

\*全部资源

`*****`

无

无

sfm:GetAlipayUrl

[GetAlipayUrl](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getalipayurl)

none

\*全部资源

`*****`

无

无

sfm:DeleteMemory

[DeleteMemory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deletememory)

delete

\*全部资源

`*****`

无

无

sfm:GetMemoryNode

[GetMemoryNode](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getmemorynode)

get

\*全部资源

`*****`

无

无

sfm:ApplyFileUploadLease

[ApplyFileUploadLease](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-applyfileuploadlease)

none

\*全部资源

`*****`

无

无

sfm:DeleteFile

[DeleteFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deletefile)

delete

\*全部资源

`*****`

无

无

sfm:ListIndexFileDetails

[ListIndexFileDetails](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindexfiledetails)

list

\*全部资源

`*****`

无

无

sfm:UpdateIndex

[UpdateIndex](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updateindex)

update

\*全部资源

`*****`

无

无

sfm:GetMemory

[GetMemory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getmemory)

get

\*全部资源

`*****`

无

无

sfm:UpdatePromptTemplate

[UpdatePromptTemplate](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updateprompttemplate)

update

\*全部资源

`*****`

无

无

sfm:GetParseSettings

[GetParseSettings](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getparsesettings)

get

\*全部资源

`*****`

无

无

sfm:DeleteIndexDocument

[DeleteIndexDocument](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteindexdocument)

delete

\*全部资源

`*****`

无

无

sfm:CreateIndex

[CreateIndex](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex)

create

\*全部资源

`*****`

无

无

sfm:ApplyTempStorageLease

[ApplyTempStorageLease](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-applytempstoragelease)

none

\*全部资源

`*****`

无

无

sfm:AddFile

[AddFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfile)

create

\*全部资源

`*****`

无

无

sfm:UpdateTableFromAuthorizedOss

[UpdateTableFromAuthorizedOss](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updatetablefromauthorizedoss)

update

\*全部资源

`*****`

无

无

sfm:SubmitIndexAddDocumentsJob

[SubmitIndexAddDocumentsJob](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexadddocumentsjob)

create

\*全部资源

`*****`

无

无

sfm:AddTable

[AddTable](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addtable)

create

\*全部资源

`*****`

无

无

sfm:GetIndexJobStatus

[GetIndexJobStatus](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexjobstatus)

get

\*全部资源

`*****`

无

无

sfm:CreateMemoryNode

[CreateMemoryNode](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-creatememorynode)

create

\*全部资源

`*****`

无

无

sfm:AddFilesFromAuthorizedOss

[AddFilesFromAuthorizedOss](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfilesfromauthorizedoss)

create

\*全部资源

`*****`

无

无

sfm:Retrieve

[Retrieve](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)

none

\*全部资源

`*****`

无

无

sfm:DescribeFile

[DescribeFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-describefile)

none

\*全部资源

`*****`

无

无

sfm:DeleteChunk

[DeleteChunk](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deletechunk)

delete

\*全部资源

`*****`

无

无

sfm:ListMemoryNodes

[ListMemoryNodes](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listmemorynodes)

list

\*全部资源

`*****`

无

无

sfm:CreateMemory

[CreateMemory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-creatememory)

create

\*全部资源

`*****`

无

无

sfm:GetConnector

[GetConnector](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getconnector)

get

\*全部资源

`*****`

无

无

sfm:ListIndex

[ListIndices](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindices)

list

\*全部资源

`*****`

无

无

sfm:ListIndexFiles

[ListIndexDocuments](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindexdocuments)

list

\*全部资源

`*****`

无

无

sfm:GetAvailableParserTypes

[GetAvailableParserTypes](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getavailableparsertypes)

get

\*全部资源

`*****`

无

无

sfm:DeletePromptTemplate

[DeletePromptTemplate](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteprompttemplate)

delete

\*全部资源

`*****`

无

无

sfm:DeleteIndex

[DeleteIndex](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteindex)

none

\*全部资源

`*****`

无

无

sfm:GetIndexMonitor

[GetIndexMonitor](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexmonitor)

get

\*全部资源

`*****`

无

无

sfm:SubmitIndexJob

[SubmitIndexJob](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexjob)

create

\*全部资源

`*****`

无

无

sfm:CreatePromptTemplate

[CreatePromptTemplate](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createprompttemplate)

create

\*全部资源

`*****`

无

无

sfm:GetPromptTemplate

[GetPromptTemplate](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getprompttemplate)

get

\*全部资源

`*****`

无

无

sfm:ListMemories

[ListMemories](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listmemories)

list

\*全部资源

`*****`

无

无

sfm:AddConnector

[AddConnector](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addconnector)

create

\*全部资源

`*****`

无

无

sfm:DeleteMemoryNode

[DeleteMemoryNode](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deletememorynode)

delete

\*全部资源

`*****`

无

无

sfm:ListPromptTemplates

[ListPromptTemplates](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listprompttemplates)

list

\*全部资源

`*****`

无

无

sfm:AddCategory

[AddCategory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addcategory)

create

\*全部资源

`*****`

无

无

sfm:ListCategory

[ListCategory](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listcategory)

list

\*全部资源

`*****`

无

无

sfm:ChunkList

[ListChunks](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listchunks)

list

\*全部资源

`*****`

无

无

sfm:GetAlipayTransferStatus

[GetAlipayTransferStatus](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getalipaytransferstatus)

none

\*全部资源

`*****`

无

无

## 资源（Resource）

下表是_大模型服务平台百炼_定义的资源，这些资源可以在 RAM 权限策略语句的`Resource`元素中使用，用来授予对该资源执行具体操作的权限。 其中，资源 ARN 是资源在阿里云上的唯一标识。具体说明如下：

-   `{#}`为变量标识，需要您替换为实际值。例如：`{#ramcode}`需要您替换为实际的云服务RAM代码。
    
-   `*`表示全部。例如：
    
    -   `{#resourceType}`为`*`时：表示全部资源。
        
    -   `{#regionId}`为`*`时：表示全部地域。
        
    -   `{#accountId}`为`*`时：表示全部阿里云账号。
        

资源类型

资源 ARN

## 条件（Condition）

_大模型服务平台百炼_未定义产品级别的条件关键字。如需查看适用于所有云产品的通用条件关键字，请参见[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。

## 相关操作

您可以创建自定义权限策略，并将权限策略授予 RAM 用户、RAM 用户组或 RAM 角色。具体操作如下：

-   [创建自定义权限策略](https://help.aliyun.com/zh/ram/create-a-custom-policy)
    
-   [为 RAM 用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)
    
-   [为 RAM 用户组授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-user-group)
    
-   [为 RAM 角色授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-role)

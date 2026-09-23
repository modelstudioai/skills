# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用 RAM 可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM 中使用权限策略描述授权的具体内容。

本文为您介绍_大模型服务平台百炼_为 RAM 权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。_大模型服务平台百炼_的 RAM 代码（RamCode）为_sfm_，支持的授权粒度为_操作级_。

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
    
-   Action：授予允许或拒绝权限的具体操作。具体信息，请参见[操作（Action）](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-ram#title-auth-detail-2)。
    
-   Resource：受操作影响的具体对象，您可以使用资源 ARN 来描述指定资源。具体信息，请参见[资源（Resource）](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-ram#title-auth-detail-3)。
    
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-ram#title-auth-detail-4)。
    
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

sfm:ListCategory

[ListCategory](raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)

list

\*全部资源

`*`

无

无

sfm:GetIndexJobStatus

[GetIndexJobStatus](raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)

get

\*全部资源

`*`

无

无

sfm:AddCategory

[AddCategory](raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)

create

\*全部资源

`*`

无

无

sfm:GetAlipayUrl

[GetAlipayUrl](raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)

none

\*全部资源

`*`

无

无

sfm:DeleteMemoryNode

[DeleteMemoryNode](raw/_short/api-bailian-2023-12-29-deletememorynode-d7919fd53d316466.md)

delete

\*全部资源

`*`

无

无

sfm:GetParseSettings

[GetParseSettings](raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)

get

\*全部资源

`*`

无

无

sfm:SubmitIndexJob

[SubmitIndexJob](raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)

create

\*全部资源

`*`

无

无

sfm:DeleteCategory

[DeleteCategory](raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)

delete

\*全部资源

`*`

无

无

sfm:ListIndexFileDetails

[ListIndexFileDetails](raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)

list

\*全部资源

`*`

无

无

sfm:UpdateConnector

[UpdateConnector](raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)

update

\*全部资源

`*`

无

无

sfm:ChangeParseSetting

[ChangeParseSetting](raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)

update

\*全部资源

`*`

无

无

sfm:GetMemory

[GetMemory](raw/_short/api-bailian-2023-12-29-getmemory-c25d3815c2b70f40.md)

get

\*全部资源

`*`

无

无

sfm:GetAvailableParserTypes

[GetAvailableParserTypes](raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)

get

\*全部资源

`*`

无

无

sfm:UpdateMemory

[UpdateMemory](raw/_short/api-bailian-2023-12-29-updatememory-b5fdfa9f480e94bb.md)

update

\*全部资源

`*`

无

无

sfm:CreateMemory

[CreateMemory](raw/_short/api-bailian-2023-12-29-creatememory-b8e710cdd3512a87.md)

create

\*全部资源

`*`

无

无

sfm:ApplyFileUploadLease

[ApplyFileUploadLease](raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)

none

\*全部资源

`*`

无

无

sfm:ListFile

[ListFile](raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)

list

\*全部资源

`*`

无

无

sfm:DeleteConnector

DeleteConnector

delete

\*全部资源

`*`

无

无

sfm:BatchUpdateFileTag

[BatchUpdateFileTag](raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)

update

\*全部资源

`*`

无

无

sfm:AddFile

[AddFile](raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)

create

\*全部资源

`*`

无

无

sfm:DeleteChunk

[DeleteChunk](raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)

delete

\*全部资源

`*`

无

无

sfm:DeleteMemory

[DeleteMemory](raw/_short/api-bailian-2023-12-29-deletememory-ffa5f461924db8f6.md)

delete

\*全部资源

`*`

无

无

sfm:DeletePromptTemplate

[DeletePromptTemplate](raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)

delete

\*全部资源

`*`

无

无

sfm:ListMemories

[ListMemories](raw/_short/api-bailian-2023-12-29-listmemories-3411c870627f174b.md)

list

\*全部资源

`*`

无

无

sfm:AddConnector

[AddConnector](raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)

create

\*全部资源

`*`

无

无

sfm:GetConnector

[GetConnector](raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)

get

\*全部资源

`*`

无

无

sfm:UpdatePromptTemplate

[UpdatePromptTemplate](raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)

update

\*全部资源

`*`

无

无

sfm:DeleteFiles

[DeleteFiles](raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)

delete

\*全部资源

`*`

无

无

sfm:GetMemoryNode

[GetMemoryNode](raw/_short/api-bailian-2023-12-29-getmemorynode-59d0d4efa0e86d78.md)

get

\*全部资源

`*`

无

无

sfm:ApplyTempStorageLease

[ApplyTempStorageLease](raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)

none

\*全部资源

`*`

无

无

sfm:DeleteFile

[DeleteFile](raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)

delete

\*全部资源

`*`

无

无

sfm:AddFilesFromAuthorizedOss

[AddFilesFromAuthorizedOss](raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)

create

\*全部资源

`*`

无

无

sfm:CreateMemoryNode

[CreateMemoryNode](raw/_short/api-bailian-2023-12-29-creatememorynode-c6cd91f25e1f7997.md)

create

\*全部资源

`*`

无

无

sfm:UpdateChunk

[UpdateChunk](raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)

update

\*全部资源

`*`

无

无

sfm:ListCategory

[ListCategory](raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)

list

\*全部资源

`*`

无

无

sfm:GetIndexJobStatus

[GetIndexJobStatus](raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)

get

\*全部资源

`*`

无

无

sfm:GetParseSettings

[GetParseSettings](raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)

get

\*全部资源

`*`

无

无

sfm:GetAlipayUrl

[GetAlipayUrl](raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)

none

\*全部资源

`*`

无

无

sfm:AddCategory

[AddCategory](raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)

create

\*全部资源

`*`

无

无

sfm:SubmitIndexJob

[SubmitIndexJob](raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)

create

\*全部资源

`*`

无

无

sfm:ChangeParseSetting

[ChangeParseSetting](raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)

update

\*全部资源

`*`

无

无

sfm:DeleteMemoryNode

[DeleteMemoryNode](raw/_short/api-bailian-2023-12-29-deletememorynode-d7919fd53d316466.md)

delete

\*全部资源

`*`

无

无

sfm:UpdateConnector

[UpdateConnector](raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)

update

\*全部资源

`*`

无

无

sfm:GetMemory

[GetMemory](raw/_short/api-bailian-2023-12-29-getmemory-c25d3815c2b70f40.md)

get

\*全部资源

`*`

无

无

sfm:ListIndexFileDetails

[ListIndexFileDetails](raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)

list

\*全部资源

`*`

无

无

sfm:DeleteConnector

DeleteConnector

delete

\*全部资源

`*`

无

无

sfm:UpdateMemory

[UpdateMemory](raw/_short/api-bailian-2023-12-29-updatememory-b5fdfa9f480e94bb.md)

update

\*全部资源

`*`

无

无

sfm:CreateMemory

[CreateMemory](raw/_short/api-bailian-2023-12-29-creatememory-b8e710cdd3512a87.md)

create

\*全部资源

`*`

无

无

sfm:ListFile

[ListFile](raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)

list

\*全部资源

`*`

无

无

sfm:DeleteChunk

[DeleteChunk](raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)

delete

\*全部资源

`*`

无

无

sfm:GetAvailableParserTypes

[GetAvailableParserTypes](raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)

get

\*全部资源

`*`

无

无

sfm:DeleteCategory

[DeleteCategory](raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)

delete

\*全部资源

`*`

无

无

sfm:ListMemories

[ListMemories](raw/_short/api-bailian-2023-12-29-listmemories-3411c870627f174b.md)

list

\*全部资源

`*`

无

无

sfm:ApplyFileUploadLease

[ApplyFileUploadLease](raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)

none

\*全部资源

`*`

无

无

sfm:BatchUpdateFileTag

[BatchUpdateFileTag](raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)

update

\*全部资源

`*`

无

无

sfm:GetConnector

[GetConnector](raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)

get

\*全部资源

`*`

无

无

sfm:GetMemoryNode

[GetMemoryNode](raw/_short/api-bailian-2023-12-29-getmemorynode-59d0d4efa0e86d78.md)

get

\*全部资源

`*`

无

无

sfm:AddFile

[AddFile](raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)

create

\*全部资源

`*`

无

无

sfm:AddConnector

[AddConnector](raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)

create

\*全部资源

`*`

无

无

sfm:DeleteFiles

[DeleteFiles](raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)

delete

\*全部资源

`*`

无

无

sfm:DeleteFile

[DeleteFile](raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)

delete

\*全部资源

`*`

无

无

sfm:DeletePromptTemplate

[DeletePromptTemplate](raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)

delete

\*全部资源

`*`

无

无

sfm:UpdatePromptTemplate

[UpdatePromptTemplate](raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)

update

\*全部资源

`*`

无

无

sfm:AddFilesFromAuthorizedOss

[AddFilesFromAuthorizedOss](raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)

create

\*全部资源

`*`

无

无

sfm:CreateMemoryNode

[CreateMemoryNode](raw/_short/api-bailian-2023-12-29-creatememorynode-c6cd91f25e1f7997.md)

create

\*全部资源

`*`

无

无

sfm:DeleteMemory

[DeleteMemory](raw/_short/api-bailian-2023-12-29-deletememory-ffa5f461924db8f6.md)

delete

\*全部资源

`*`

无

无

sfm:UpdateChunk

[UpdateChunk](raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)

update

\*全部资源

`*`

无

无

sfm:ApplyTempStorageLease

[ApplyTempStorageLease](raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)

none

\*全部资源

`*`

无

无

sfm:GetIndexMonitor

[GetIndexMonitor](raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)

get

\*全部资源

`*`

无

无

sfm:Retrieve

[Retrieve](raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)

none

\*全部资源

`*`

无

无

sfm:DeleteIndex

[DeleteIndex](raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)

none

\*全部资源

`*`

无

无

sfm:ListMemoryNodes

[ListMemoryNodes](raw/_short/api-bailian-2023-12-29-listmemorynodes-4f1cc5232bdc67a5.md)

list

\*全部资源

`*`

无

无

sfm:ListIndex

[ListIndices](raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)

list

\*全部资源

`*`

无

无

sfm:UpdateMemoryNode

[UpdateMemoryNode](raw/_short/api-bailian-2023-12-29-updatememorynode-f2d05378b761b201.md)

update

\*全部资源

`*`

无

无

sfm:GetPromptTemplate

[GetPromptTemplate](raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)

get

\*全部资源

`*`

无

无

sfm:CreateIndex

[CreateIndex](raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)

create

\*全部资源

`*`

无

无

sfm:ListPromptTemplates

[ListPromptTemplates](raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)

list

\*全部资源

`*`

无

无

sfm:DeleteIndexDocument

[DeleteIndexDocument](raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)

delete

\*全部资源

`*`

无

无

sfm:SubmitIndexAddDocumentsJob

[SubmitIndexAddDocumentsJob](raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)

create

\*全部资源

`*`

无

无

sfm:UpdateFileTag

[UpdateFileTag](raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)

update

\*全部资源

`*`

无

无

sfm:UpdateTableFromAuthorizedOss

[UpdateTableFromAuthorizedOss](raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)

update

\*全部资源

`*`

无

无

sfm:ListIndexFiles

[ListIndexDocuments](raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)

list

\*全部资源

`*`

无

无

sfm:UpdateIndex

[UpdateIndex](raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)

update

\*全部资源

`*`

无

无

sfm:DescribeFile

[DescribeFile](raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)

none

\*全部资源

`*`

无

无

sfm:ChunkList

[ListChunks](raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)

list

\*全部资源

`*`

无

无

sfm:AddTable

[AddTable](raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)

create

\*全部资源

`*`

无

无

sfm:CreatePromptTemplate

[CreatePromptTemplate](raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)

create

\*全部资源

`*`

无

无

sfm:GetAlipayTransferStatus

[GetAlipayTransferStatus](raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)

none

\*全部资源

`*`

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

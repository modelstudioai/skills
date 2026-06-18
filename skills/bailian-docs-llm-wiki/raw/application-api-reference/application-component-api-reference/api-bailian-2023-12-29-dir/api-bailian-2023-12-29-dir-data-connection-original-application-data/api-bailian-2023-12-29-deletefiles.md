# DeleteFiles - 批量删除文件

批量删除文件

## 接口说明

-   不支持通过 API 删除数据表。如需删除数据表或表中特定的数据，请前往[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)操作。
    
-   本接口用于删除[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)中的文件，不会影响已构建好的知识库。如需删除知识库中的文件，请调用 **DeleteIndexDocument** 接口。
    
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:DeleteFiles 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口仅能删除状态为解析失败（PARSE\_FAILED）或解析完成（PARSE\_SUCCESS）的文件。
    
-   本接口具有幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/DeleteFiles)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteFiles)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
POST /{WorkspaceId}/datacenter/file/delete HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

类目所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-mbhn96xxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

FileIds

array

是

需要删除的文件 id 列表，单次删除最多支持 20 个文件

string

否

需要删除的文件 id

file\_xxxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

错误状态码。

DataCenter.FileTooLarge

Data

object

返回内容

DeleteFileResultList

array<object>

删除结果

object

单个文件删除结果

FileId

string

文件 ID。

file\_6b193b9b4b1546ef9eaa7340e69adfca\_10052857

Status

string

文件删除状态。状态可能值为：

-   DELETED：删除成功。
    
-   FAILED：删除失败。
    
-   NOT\_FOUND：未查询到文件
    

DELETED

Message

string

错误信息。

Required parameter(%s) missing or invalid, please check the request parameters.

RequestId

string

Id of the request

17204B98-7734-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功。
    
-   false：失败。
    

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataCenter.FileTooLarge",
  "Data": {
    "DeleteFileResultList": [
      {
        "FileId": "file_6b193b9b4b1546ef9eaa7340e69adfca_10052857",
        "Status": "DELETED"
      }
    ]
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-7734-4F9A-8464-2446A84821CA",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/DeleteFiles#workbench-doc-change-demo)。

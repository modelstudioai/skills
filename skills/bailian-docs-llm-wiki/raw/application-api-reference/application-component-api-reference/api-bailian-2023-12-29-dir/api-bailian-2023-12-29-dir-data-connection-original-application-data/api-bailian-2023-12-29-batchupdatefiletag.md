# BatchUpdateFileTag - 批量更新文档标签

该接口用于批量更新数据连接中的文档标签。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/BatchUpdateFileTag)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/BatchUpdateFileTag)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
PUT /{WorkspaceId}/datacenter/batchupdatetag HTTP/1.1
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

业务空间 ID。在百炼的[控制台首页](https://bailian.console.aliyun.com/knowledge-base#/home)，单击页面左上角业务空间详情图标获取。

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

FileInfos

array<object>

是

需要更新的文档列表

object

是

FileId

string

是

数据中心的文件 ID，您可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)页面，单击文件名称旁的 ID 图标获取。

file\_3d5319366e2c46309f4c11cfbeacd5fd\_10045951

tags

array

是

-   文件关联的标签列表。最多传入 100 个标签，所有标签字符长度总和不能超过 700。
    

string

否

标签值，每个标签最多 32 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等），下划线\_，中划线-，标签中不能包含空格。

TagA

UpdateMode

string

否

更新模式，仅支持 APPEND（追加）和 OVERWRITE（覆盖）

OVERWRITE

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

错误状态码

Success

Data

object

接口返回的业务字段。

UpdateFileTagResultList

array<object>

标签更新的结果列表

object

FileId

string

文件 ID。

file\_f40f2a32205d44b4a93b11617113da15\_10045951

Success

boolean

接口调用是否成功，可能值为：

-   true：成功。
    
-   false：失败。
    

true

ErrorCode

string

返回错误码，仅当 Success 为 false 时返回。

NoPermission

ErrorMessage

string

错误描述信息，仅当 Success 为 false 时返回。

FileId not exists.

Message

string

错误信息

Required parameter(FileId) missing or invalid, please check the request parameters.

RequestId

string

Id of the request

17204B98-xxxx-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值：

-   true：成功。
    
-   false：失败。
    

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Success",
  "Data": {
    "UpdateFileTagResultList": [
      {
        "FileId": "file_f40f2a32205d44b4a93b11617113da15_10045951",
        "Success": true,
        "ErrorCode": "NoPermission",
        "ErrorMessage": "FileId not exists."
      }
    ]
  },
  "Message": "Required parameter(FileId) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/BatchUpdateFileTag#workbench-doc-change-demo)。

# ListFile - 文件列表

获取指定类目下一个或多个文档的详细信息。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ListFile 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   分页查询首页时，仅需设置`MaxResults`以限制返回信息的条目数，返回结果中的`NextToken`将作为查询后续页的凭证。查询后续页时，将`NextToken`参数设置为上一次返回结果中获取到的`NextToken`作为查询凭证（如果`NextToken`为空，表示结果已经完全返回，不需要再请求），并设置`MaxResults`限制返回条目数。
    
-   本接口具有幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ListFile)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/ListFile)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

sfm:ListFile

list

\*全部资源

`*`

无

无

## 请求语法

```
GET /{WorkspaceId}/datacenter/files HTTP/1.1
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

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

CategoryId

string

是

类目 ID，即 **AddCategory** 接口返回的`CategoryId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击类目名称旁的 ID 图标获取。

cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx

NextToken

string

否

查询凭证（Token），取值为上一次 API 调用返回的 NextToken 参数值。

AAAAAdH70eOCSCKtacdomNzak4U=

MaxResults

integer

否

分页查询时每页行数。取值范围\[1-200\]。

默认值： 当不设置值或设置的值小于 1 时，默认值为 20。当设置的值大于 200 时，默认值为 200。

20

FileName

string

否

文件名称（不含后缀），仅支持按照文件名精准查找，不支持模糊搜索。

product-overview

FileIds

array

否

需要查询的文件 id 列表，单次查询最多支持 20 个文件

string

否

文件 id

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

success

Data

object

接口业务数据字段。

FileList

array<object>

类目下的文件列表。

object

文件对象。

CategoryId

string

文件所属类目 ID。

cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx

CreateTime

string

文件实际添加到阿里云百炼中的时间戳，格式: yyyy-MM-dd HH:mm:ss，时区：UTC + 8。

2024-09-09 11:03:35

FileId

string

文件 ID，即 **AddFile** 接口返回的`FileId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)页面，单击文件名称旁的图标获取。

file\_5ff599b3455a45db8c41b0054b361518\_xxxxxxxx

FileName

string

文件名称。

product-overview.pdf

FileType

string

文件格式类型。可能值为：pdf、docx、doc、txt、md、pptx、ppt、xlsx、xls、html、png、jpg、jpeg、bmp、gif。

docx

Parser

string

文档解析器。可能值为：

-   DASHSCOPE\_DOCMIND：阿里云文档智能解析。
    

DASHSCOPE\_DOCMIND

SizeInBytes

integer

文件大小，单位字节。

512

Status

string

文件解析状态，可能值为：

-   INIT: 初始化状态，等待调度中。
    
-   PARSING: 解析中。
    
-   PARSE\_SUCCESS：解析完成。
    
-   PARSE\_FAILED：解析失败。
    

PARSE\_SUCCESS

Tags

array

文件关联的标签列表，一个文档支持关联多个标签。

string

文件的标签。

tag-A

HasNext

boolean

符合查询条件的类目数据是否存在下一页，可能值为：

-   true：是。
    
-   false：否。
    

true

MaxResults

integer

分页查询时每页行数。

20

NextToken

string

本次调用返回的查询凭证值。

4jzbJk9J6lNeuXD9hP0viA==

TotalCount

integer

返回结果的总条数。

48

Message

string

错误信息。

Requests throttling triggered.

RequestId

string

请求 ID。

8F97A63B-xxxx-527F-9D6E-467B6A7E8CF1

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
  "Code": "success",
  "Data": {
    "FileList": [
      {
        "CategoryId": "cate_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx",
        "CreateTime": "2024-09-09 11:03:35",
        "FileId": "file_5ff599b3455a45db8c41b0054b361518_xxxxxxxx",
        "FileName": "product-overview.pdf",
        "FileType": "docx",
        "Parser": "DASHSCOPE_DOCMIND",
        "SizeInBytes": 512,
        "Status": "PARSE_SUCCESS",
        "Tags": [
          "tag-A"
        ]
      }
    ],
    "HasNext": true,
    "MaxResults": 20,
    "NextToken": "4jzbJk9J6lNeuXD9hP0viA==",
    "TotalCount": 48
  },
  "Message": "Requests throttling triggered.",
  "RequestId": "8F97A63B-xxxx-527F-9D6E-467B6A7E8CF1",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/ListFile#workbench-doc-change-demo)。

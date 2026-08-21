# ListCategory - 类目列表

获取指定业务空间下一个或多个类目的详细信息。

## 接口说明

-   暂不支持通过 API 查询数据表。
    
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ListCategory 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   分页查询首页时，仅需设置`MaxResults`以限制返回信息的条目数，返回结果中的`NextToken`将作为查询后续页的凭证。查询后续页时，将`NextToken`参数设置为上一次返回结果中获取到的`NextToken`作为查询凭证（如果`NextToken`为空，表示结果已经完全返回，不需要再请求），并设置`MaxResults`限制返回条目数。
    
-   本接口具有幂等性。
    

**限流说明：** 注意本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ListCategory)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/ListCategory)

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

sfm:ListCategory

list

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/datacenter/categories HTTP/1.1
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

业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

ConnectorId

string

否

连接器 Id

file\_conn\_xxxxx

CategoryType

string

是

要查询的类目类型。取值范围：

-   UNSTRUCTURED：类目。
    

**说明**

暂不支持通过 API 查询表格（数据表）。

UNSTRUCTURED

ParentCategoryId

string

否

要查询类目的父类目 ID。

cate\_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx

NextToken

string

否

查询凭证（Token），取值为上一次 API 调用返回的 NextToken 参数值。

AAAAAdH70eOCSCKtacdomNzak4U=

MaxResults

integer

否

分页查询时每页类目数量。最大值为 200。取值范围\[1-200\]

默认值： 当不设置值或设置的值小于 1 时，默认值为 20。当设置的值大于 200 时，默认值为 200。

20

CategoryName

string

否

即根据类目名称对接口返回的类目列表进行精确匹配/过滤。默认值为空，即不启用类目名称过滤。

产品清单

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

CategoryList

array<object>

类目列表。

object

类目对象。

CategoryId

string

类目 ID。

cate\_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx

CategoryName

string

类目名称。

类目1

CategoryType

string

类目类型，可能值为：

-   UNSTRUCTURED：类目。
    

UNSTRUCTURED

IsDefault

boolean

是否为默认类目。可能值为：

-   true：是。
    
-   false：否。
    

默认类目不允许删除。

true

ParentCategoryId

string

父类目的类目 ID。

cate\_addd11b1b79a74e8bbd675c356a91ee3xxxxxxxx

HasNext

boolean

符合查询条件的类目数据是否存在下一页，可能值为：

-   true：是。
    
-   false：否。
    

true

MaxResults

integer

分页查询时每页类目数量。

20

NextToken

string

本次调用返回的查询凭证值。

AAAAALHWGpGoYCcYMxiFfmlhvh7Z4G8jiXR6IjHYd+M9WQVJ

TotalCount

integer

返回结果的总类目数量。

20

Message

string

错误信息。

workspace id is null or invalid.

RequestId

string

请求 ID。

17204B98-xxxx-4F9A-8464-2446A84821CA

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
    "CategoryList": [
      {
        "CategoryId": "cate_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx",
        "CategoryName": "类目1",
        "CategoryType": "UNSTRUCTURED",
        "IsDefault": true,
        "ParentCategoryId": "cate_addd11b1b79a74e8bbd675c356a91ee3xxxxxxxx"
      }
    ],
    "HasNext": true,
    "MaxResults": 20,
    "NextToken": "AAAAALHWGpGoYCcYMxiFfmlhvh7Z4G8jiXR6IjHYd+M9WQVJ",
    "TotalCount": 20
  },
  "Message": "workspace id is null or invalid.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/ListCategory#workbench-doc-change-demo)。

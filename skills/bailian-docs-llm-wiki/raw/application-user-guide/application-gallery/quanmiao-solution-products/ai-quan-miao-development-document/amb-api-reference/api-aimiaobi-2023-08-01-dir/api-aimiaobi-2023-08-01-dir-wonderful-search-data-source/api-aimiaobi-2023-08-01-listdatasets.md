# ListDatasets - 数据源-列表

数据源管理-查询。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDatasets)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDatasets)

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

aimiaobi:ListDatasets

list

\*全部资源

`*`

无

无

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

StartTime

string

否

创建时间-开始

创建时间-开始

EndTime

string

否

创建时间-结束

创建时间-结束

DatasetName

string

否

数据集名称，全局唯一

businessDataset

DatasetId

integer

否

数据集 id

1

PageSize

string

否

每页条数

10

PageNumber

integer

否

当前页：默认 1

1

DatasetType

string

否

数据集类型

CustomSemanticSearch

SearchDatasetEnable

integer

否

数据集搜索开关

3

IncludeConfig

boolean

否

是否返回配置和用量信息，默认不返回

DatasetDescription

string

否

数据集描述

xx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Data

array<object>

业务数据

array<object>

业务数据

DatasetId

integer

数据集 ID

1

CreateUser

string

创建者

xxx

CreateTime

string

创建时间

2024-11-12 21:46:24

DatasetType

string

数据集类型

CustomSemanticSearch

DatasetName

string

数据集名称

xxx

DatasetDescription

string

数据集显示名称

xxx

SearchDatasetEnable

integer

数据集搜索开关

1

DocUsedQuota

integer

当前数据集已上传文档总数

1

AccessLevel

string

开放级别

private

Administrators

array<object>

管理员

object

管理员

Username

string

用户名

xx

UserId

string

用户 id

xx

PageNumber

integer

当前页码

1

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

Code

string

状态码

NoData

Message

string

错误说明

success

HttpStatusCode

integer

http 状态码

200

TotalCount

integer

总条数

100

PageSize

integer

每页条数

10

CustomSemanticSearchConfig

object

"上传文件用作数据源"场景索引配置和用量信息

DocQuota

integer

总文档配额

1000

DocUsedQuota

integer

总文档已使用配额

1

DatasetQuota

integer

数据集数量配额

3

DatasetUsedQuota

integer

数据集数量已使用配额

1

ThirdSearchConfig

object

"通过 API 引入数据源"场景配置和用量信息

DatasetQuota

integer

数据集数量配额

2

DatasetUsedQuota

integer

数据集数量已使用配额

1

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": [
    {
      "DatasetId": 1,
      "CreateUser": "xxx",
      "CreateTime": "2024-11-12 21:46:24",
      "DatasetType": "CustomSemanticSearch",
      "DatasetName": "xxx",
      "DatasetDescription": "xxx",
      "SearchDatasetEnable": 1,
      "DocUsedQuota": 1,
      "AccessLevel": "private",
      "Administrators": [
        {
          "Username": "xx",
          "UserId": "xx"
        }
      ]
    }
  ],
  "PageNumber": 1,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "TotalCount": 100,
  "PageSize": 10,
  "CustomSemanticSearchConfig": {
    "DocQuota": 1000,
    "DocUsedQuota": 1,
    "DatasetQuota": 3,
    "DatasetUsedQuota": 1
  },
  "ThirdSearchConfig": {
    "DatasetQuota": 2,
    "DatasetUsedQuota": 1
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListDatasets#workbench-doc-change-demo)。

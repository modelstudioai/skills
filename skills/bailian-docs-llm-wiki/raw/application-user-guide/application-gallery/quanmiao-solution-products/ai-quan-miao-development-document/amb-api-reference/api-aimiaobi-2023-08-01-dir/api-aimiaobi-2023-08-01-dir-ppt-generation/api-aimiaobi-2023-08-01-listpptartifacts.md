# ListPptArtifacts - 查询PPT作品列表

查询PPT作品列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPptArtifacts)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPptArtifacts)

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

aimiaobi:ListPptArtifacts

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

否

业务空间 ID

llm-az2xxxx

NextToken

string

否

下一页的 token

cEoBWREAXdxaOyjq/cqAbg==

Query

string

否

搜索关键词：作品名称

数字时代的营销策划与文案创作

MaxResults

integer

否

本次请求期望查询的数据条目（废弃）

0

ExternalUserId

string

否

abc

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Code

string

状态码

NoData

Current

integer

当前页。

1

Data

array<object>

是否删除成功

array<object>

业务数据

CreateTime

string

更新日期

2024-01-04 11:46:07

Id

integer

文档唯一标识

10

Title

string

标题

作品标题

UpdateTime

string

更新日期

2025-04-14 19:59:53

FileKey

string

作品文件预览图

http://www.example.com/xxx.jpg

FileAttr

object

作品文件属性

FileName

string

文件名

数字时代的营销策划与文案创作

Width

integer

视频宽度

100

TmpUrl

string

作品文件预览图

http://www.example.com/xxx.jpg

Height

integer

高度

500

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Size

integer

每页条数：默认 10

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录数

100

NextToken

string

下一页的 Token

cEoBWREAXdxaOyjq/cqAbg==

MaxResults

integer

本次返回的数据条目

10

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Current": 1,
  "Data": [
    {
      "CreateTime": "2024-01-04 11:46:07",
      "Id": 10,
      "Title": "作品标题",
      "UpdateTime": "2025-04-14 19:59:53",
      "FileKey": "http://www.example.com/xxx.jpg",
      "FileAttr": {
        "FileName": "数字时代的营销策划与文案创作",
        "Width": 100,
        "TmpUrl": "http://www.example.com/xxx.jpg",
        "Height": 500
      }
    }
  ],
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Size": 10,
  "Success": true,
  "Total": 100,
  "NextToken": "cEoBWREAXdxaOyjq/cqAbg==\n",
  "MaxResults": 10
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListPptArtifacts#workbench-doc-change-demo)。

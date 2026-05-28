# UpdateDatasetDocument - 数据源-修改文档

修改数据源文档。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/UpdateDatasetDocument)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/UpdateDatasetDocument)

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

aimiaobi:UpdateDatasetDocument

update

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

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

Document

object

是

文档

DocUuid

string

否

文档系统唯一 ID

xxx

Title

string

否

文档标题

xx

DocId

string

否

文档用户侧唯一 ID

xxx

CategoryUuid

string

否

Tags

array

否

string

否

Extend1

string

否

Extend2

string

否

Extend3

string

否

DatasetId

integer

否

数据集唯一标识

1

DatasetName

string

否

数据集名称

数据集名称

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Data

object

业务数据

DocUuid

string

内部文档唯一 ID

内部文档唯一ID

Title

string

文档标题

文章标题

DocId

string

用户指定的文档唯一 ID

用户指定的文档唯一ID

Tags

array

string

CategoryUuid

string

Extend1

string

Extend2

string

Extend3

string

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

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": {
    "DocUuid": "内部文档唯一ID",
    "Title": "文章标题",
    "DocId": "用户指定的文档唯一ID",
    "Tags": [
      ""
    ],
    "CategoryUuid": "",
    "Extend1": "",
    "Extend2": "",
    "Extend3": ""
  },
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/UpdateDatasetDocument#workbench-doc-change-demo)。

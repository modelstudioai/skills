# CreateDataset - 数据源-创建

数据源管理-创建。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateDataset)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateDataset)

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

aimiaobi:CreateDataset

create

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

DatasetType

string

否

数据集类型：

-   CustomSemanticSearch：自建语义索引（默认），用户上传文档构建数据集
    
-   ThirdSearch：三方搜索源（api），配置用户自己的搜索 api
    

CustomSemanticSearch

DatasetName

string

是

数据集名称，全局唯一

businessDataset

DatasetDescription

string

否

数据集描述：控制台展示名称，建议传入业务可读的名称

企业知识库

SearchDatasetEnable

integer

否

数据集搜索开关：

-   0：全部关闭
    
-   1：仅妙搜可见
    
-   2：仅妙笔可见
    
-   3：妙搜&妙笔均可见 （默认）
    

3

DatasetConfig

object

否

数据集搜索配置

SearchSourceConfigs

array<object>

否

三方搜索：api 定义

array<object>

否

三方搜索：api 定义

DemoQuery

string

否

可以搜索到的关键词，用来验证是否可用

可以搜索到的关键词，用来验证是否可用

Size

integer

否

默认请求、响应数据条数限制

10

SearchSourceRequestConfig

object

否

api 请求配置

Url

string

否

api 地址

api地址

Method

string

否

请求方式

请求方式

ConnectTimeout

integer

否

连接超时时间：单位毫秒

3000

SocketTimeout

integer

否

读超时时间：单位毫秒

3000

Headers

array<object>

否

http 请求头

object

否

http 请求头

Name

string

否

参数名称

参数名称

ValueType

string

否

参数值数据类型：默认 string

参数值数据类型：默认string

ValueFormat

string

否

valueType = time 时有效

valueType = time 时有效

Value

string

否

参数值

参数值

Params

array<object>

否

请求 path 参数

object

否

Name

string

否

参数名称

参数名称

ValueType

string

否

参数值数据类型：默认 string

参数值数据类型：默认string

ValueFormat

string

否

valueType = time 时有效

valueType = time 时有效

Value

string

否

参数值

参数值

PathParamsEnable

boolean

否

是否开启 pathParam

true

Body

string

否

请求 body

{}

SearchSourceResponseConfig

object

否

api 响应配置

JqNodes

array<object>

否

节点配置

array<object>

否

Key

string

否

节点 key

节点key

Type

string

否

节点数据类型：string number list object base

节点数据类型：string number list object base

Path

string

否

节点路径

节点路径

JqNodes

array<object>

否

子节点配置

array<object>

否

子节点配置

Key

string

否

节点 key

title

Type

string

否

type 类型

string

Path

string

否

路径。

节点路径

JqNodes

array<object>

否

子节点配置

object

否

子节点配置

Key

string

否

节点 key

title

Type

string

否

type 类型

string

Path

string

否

节点路径

节点路径

SearchSourceConfig

object

否

数据集配置项

TagSearchEnable

boolean

否

标签是否参与搜索：默认 true

true

TagGenerateEnable

boolean

否

标签是否参与生成：默认 true

true

MetadataKeyValueSearchEnable

boolean

否

metadata-keyValue 部分是否参与搜索：默认 true

true

MetadataKeyValueGenerateEnable

boolean

否

metadata-keyValue 部分是否参与生成：默认 true

true

DocumentHandleConfig

object

否

数据集索引配置

DisableHandleMultimodalMedia

boolean

否

禁用多媒体文件处理逻辑：

-   true：禁用多模态（图片、视频）索引，仅索引和搜索文本
    
-   false：支持多模态（文本、图片、视频）索引，同时开通视频云并在系统管理中做了授权才正式生效，仅设置 false，这里识别到未授权会自动跳过图片、视频索引（默认）
    

false

InvokeType

string

否

调用方式：目前仅支持值 portal，标识控制台调用。

-   空时：当 DatasetType= ThirdSearch，datasetConfig.SearchSourceConfigs（三方 api 定义）必传。
    
-   portal 时：当 DatasetType= ThirdSearch，后台会默认初始化一个 SearchSourceConfigs（三方 apidemo）示例，供参考。
    

portal

AccessLevel

string

否

private

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

创建时回见

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
    "DatasetId": 1,
    "CreateUser": "xxx",
    "CreateTime": "2024-11-12 21:46:24",
    "DatasetType": "CustomSemanticSearch",
    "DatasetName": "xxx",
    "DatasetDescription": "xxx",
    "SearchDatasetEnable": 1
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/CreateDataset#workbench-doc-change-demo)。

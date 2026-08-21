# GetDataset - 数据源-详情

数据源管理-详情。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDataset)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDataset)

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

aimiaobi:GetDataset

get

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

DatasetName

string

否

数据集名称，全局唯一

businessDataset

DatasetId

integer

否

数据集 id：和 DatasetName 二选一必选

1

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

DatasetConfig

object

数据集搜索配置

SearchSourceConfigs

array<object>

三方搜索：api 定义

array<object>

三方搜索：api 定义

DemoQuery

string

可以搜索到的关键词，用来验证是否可用

可以搜索到的关键词，用来验证是否可用

Size

integer

默认请求、响应数据条数限制

10

SearchSourceRequestConfig

object

api 请求配置

Url

string

api 地址

api地址

Method

string

请求方式

请求方式

ConnectTimeout

integer

连接超时时间

30

SocketTimeout

integer

读超时时间

78

Headers

array<object>

http 请求头

object

http 请求头

Name

string

参数名称

参数名称

ValueType

string

参数值数据类型：默认 string

参数值数据类型：默认string

ValueFormat

string

valueType = time 时有效

valueType = time 时有效

Value

string

参数值

参数值

Params

array<object>

请求 path 参数

object

请求 path 参数

Name

string

参数名称

参数名称

ValueType

string

参数值数据类型：默认 string

参数值数据类型：默认string

ValueFormat

string

valueType = time 时有效

valueType = time 时有效

Value

string

参数值

参数值

PathParamsEnable

boolean

是否开启 pathParam

true

Body

string

请求 body

请求body

SearchSourceResponseConfig

object

api 响应配置

JqNodes

array<object>

节点配置

array<object>

子节点配置

Key

string

节点 key

节点key

Type

string

节点数据类型：string number list object base

节点数据类型：string number list object base

Path

string

节点路径

节点路径

JqNodes

array<object>

子节点配置

array<object>

子节点配置

xx

Key

string

节点 key

title

Type

string

节点数据类型：string number list object base

string

Path

string

节点路径

.title

JqNodes

array<object>

子节点配置

object

子节点配置

Key

string

节点 key

title

Type

string

节点数据类型：string number list object base

string

Path

string

节点路径

.title

SearchSourceConfig

object

数据集配置项

TagSearchEnable

string

标签是否参与搜索：默认 true

true

TagGenerateEnable

string

标签是否参与生成：默认 true

true

MetadataKeyValueSearchEnable

string

metadata-keyValue 部分是否参与搜索：默认 true

true

MetadataKeyValueGenerateEnable

string

metadata-keyValue 部分是否参与生成：默认 true

true

DatasetDescription

string

数据集显示名称

xxx

SearchDatasetEnable

integer

数据集搜索开关

1

DocumentHandleConfig

object

文档处理配置

DisableHandleMultimodalMedia

boolean

禁用多媒体文件处理逻辑，默认为 false

true

AccessLevel

string

private

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
    "DatasetConfig": {
      "SearchSourceConfigs": [
        {
          "DemoQuery": "可以搜索到的关键词，用来验证是否可用",
          "Size": 10,
          "SearchSourceRequestConfig": {
            "Url": "api地址",
            "Method": "请求方式",
            "ConnectTimeout": 30,
            "SocketTimeout": 78,
            "Headers": [
              {
                "Name": "参数名称",
                "ValueType": "参数值数据类型：默认string",
                "ValueFormat": "valueType = time 时有效",
                "Value": "参数值"
              }
            ],
            "Params": [
              {
                "Name": "参数名称",
                "ValueType": "参数值数据类型：默认string",
                "ValueFormat": "valueType = time 时有效",
                "Value": "参数值"
              }
            ],
            "PathParamsEnable": true,
            "Body": "请求body"
          },
          "SearchSourceResponseConfig": {
            "JqNodes": [
              {
                "Key": "节点key",
                "Type": "节点数据类型：string number list object base",
                "Path": "节点路径",
                "JqNodes": [
                  {
                    "Key": "title",
                    "Type": "string",
                    "Path": ".title",
                    "JqNodes": [
                      {
                        "Key": "title",
                        "Type": "string",
                        "Path": ".title"
                      }
                    ]
                  }
                ]
              }
            ]
          }
        }
      ],
      "SearchSourceConfig": {
        "TagSearchEnable": "true",
        "TagGenerateEnable": "true",
        "MetadataKeyValueSearchEnable": "true",
        "MetadataKeyValueGenerateEnable": "true"
      }
    },
    "DatasetDescription": "xxx",
    "SearchDatasetEnable": 1,
    "DocumentHandleConfig": {
      "DisableHandleMultimodalMedia": true
    },
    "AccessLevel": "private"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetDataset#workbench-doc-change-demo)。

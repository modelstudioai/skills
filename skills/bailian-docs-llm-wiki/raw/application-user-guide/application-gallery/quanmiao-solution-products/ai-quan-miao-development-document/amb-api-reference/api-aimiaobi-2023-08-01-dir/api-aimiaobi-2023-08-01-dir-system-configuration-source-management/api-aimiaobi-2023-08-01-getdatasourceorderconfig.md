# GetDataSourceOrderConfig - 获取信源配置权重数据

获取写作信源，通用搜索信源的配置信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDataSourceOrderConfig)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDataSourceOrderConfig)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

aimiaobi:GetDataSourceOrderConfig

get

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

d9a1f6146a37446495d9985c2e7b267e\_p\_outbound\_public

ProductCode

string

是

配置类型。可选值如下：

-   miaobi
    
-   miaosou
    

miaobi

GenerateTechnology

string

否

productCode=miaosou 时，对应妙搜：生成技术

可取值如下：

-   copilotPrecise
    
-   copilotReference
    

copilotPrecise

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

successful

Data

object

业务数据

UserConfigDataSourceList

array<object>

用户配置数据源权重列表

UserConfigDataSourceList

object

Code

string

code 描述

QuarkCommonNews

Name

string

显示名称

夸克通用搜索

Number

integer

数量

20

Type

string

type 类型

SystemSearch

Enable

boolean

是否启用

TotalDocSize

integer

最大文档总数

1

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

428DCC0D-3C63-5306-BD1B-124396AB97BE

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": {
    "UserConfigDataSourceList": [
      {
        "Code": "QuarkCommonNews",
        "Name": "夸克通用搜索",
        "Number": 20,
        "Type": "SystemSearch",
        "Enable": true
      }
    ],
    "TotalDocSize": 1
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "428DCC0D-3C63-5306-BD1B-124396AB97BE",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。

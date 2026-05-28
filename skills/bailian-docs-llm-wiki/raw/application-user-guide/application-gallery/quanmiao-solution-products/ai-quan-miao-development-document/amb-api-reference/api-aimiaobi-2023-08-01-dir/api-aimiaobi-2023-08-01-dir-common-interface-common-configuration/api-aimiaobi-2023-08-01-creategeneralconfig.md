# CreateGeneralConfig - 通用配置-创建

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateGeneralConfig)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateGeneralConfig)

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

aimiaobi:CreateGeneralConfig

create

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

WorkspaceId

string

是

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-

ConfigKey

string

是

配置项唯一标识，目前支持的：

-   妙搜-数据源-文本搜索阈值(double)：searchGenerate.searchTextMinScore
-   妙搜-数据源-图片搜索阈值(double)：searchGenerate.searchImageMinScore
-   妙搜-数据源-视频搜索阈值(double)：searchGenerate.searchVideoMinScore
-   妙搜-数据源-音频搜索阈值(double)：searchGenerate.searchAudioMinScore
-   妙搜-问答式搜索-通用-总结生成答案-纯文本 prompt 模版(string)：searchGenerate.sumQaAgentPrompt
-   妙搜-问答式搜索-通用-总结生成答案-文本&图片 prompt 模版(string)：searchGenerate.sumQaAgentVlPrompt
-   妙搜-问答式搜索-深度-总结生成答案-纯文本 prompt 模版(string)：searchGenerate.sumQaEnhanceAgentPrompt
-   妙搜-问答式搜索-深度-总结生成答案-文本&图片 prompt 模版(string)：searchGenerate.sumQaEnhanceAgentVlPrompt

xxxx

ConfigValue

string

是

配置项值

xxx

## 返回参数

名称

类型

描述

示例值

object

响应结果

Code

string

状态码

DataNotExists

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

数据不存在

RequestId

string

请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Success

boolean

是否成功：true 成功，false 失败

false

Data

object

结果

ConfigKey

string

配置唯一标识

xx

ConfigValue

string

配置值

xx

ConfigValueType

string

配置类型

xx

ConfigDesc

string

配置说明

xx

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataNotExists",
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": false,
  "Data": {
    "ConfigKey": "xx",
    "ConfigValue": "xx",
    "ConfigValueType": "xx",
    "ConfigDesc": "xx"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-11-12

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/CreateGeneralConfig?updateTime=2025-11-12#workbench-doc-change-demo)

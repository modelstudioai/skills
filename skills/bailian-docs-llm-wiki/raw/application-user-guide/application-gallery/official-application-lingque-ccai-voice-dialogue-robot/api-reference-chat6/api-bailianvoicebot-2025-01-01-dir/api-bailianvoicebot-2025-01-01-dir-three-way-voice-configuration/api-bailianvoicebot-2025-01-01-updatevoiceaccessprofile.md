# UpdateVoiceAccessProfile

更新三方语音配置

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

bailianvoicebot:UpdateVoiceAccessProfile

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

BusinessUnitId

string

否

百炼业务空间 ID

llm-xdne77rxe14ziszr

AccessProfileId

string

否

配置 ID

af81a389-91f0-4157-8d82-720edd02b66b

NlsEngine

string

否

语音引擎

BAILIAN

Profile

object

否

参数配置

AppKey

string

否

使用豆包时必填

2541370123

AccessKey

string

否

使用豆包时必填

HwRnTXgwnQOlsj68URDS5\_VMm4Wtapq9

AppId

string

否

使用科大讯飞时必填

5b123bfb

ApiKey

string

否

使用百炼、科大讯飞时必填

sk-12341e259b1049e8872b47981e545f78

ApiSecret

string

否

使用科大讯飞时必填

c0358c6e51c1013b446fdeb21a3a1234

AsrAppKey

string

否

暂无使用

暂无使用

TtsApiKey

string

否

暂无使用

暂无使用

## 返回参数

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

RequestId

string

Id of the request

D771A1B6-3D5F-174A-BEE1-98CE1000D337

HttpStatusCode

integer

http 状态码

200

Message

string

错误信息

Instance llm-baployoyopf22m2r does not exist.

Code

string

内部错误码

OK

Data

string

变量 ID

82ea16d1-425c-4c03-9be5-cc91de9779ed

Params

array

动态错误参数

string

动态错误参数

llm-xdne77rxe14ziszr

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "HttpStatusCode": 200,
  "Message": "Instance llm-baployoyopf22m2r does not exist.",
  "Code": "OK",
  "Data": "82ea16d1-425c-4c03-9be5-cc91de9779ed",
  "Params": [
    "llm-xdne77rxe14ziszr"
  ]
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode)查看更多错误码。

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/UpdateVoiceAccessProfile#workbench-doc-change-demo)。

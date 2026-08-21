# GetAlipayUrl - 获取支付宝打赏URL

获取应用上支付宝的打赏链接。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/GetAlipayUrl)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/GetAlipayUrl)

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

sfm:GetAlipayUrl

none

\*全部资源

`*`

无

无

## 请求语法

```
GET /openapi/alipay/transfer/url HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspace\_id

string

否

百炼工作空间的 id

xxxllm-czb8d47ks

app\_id

string

否

百炼应用的 id

asfasdfxxasdf

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

请求的唯一 id

6a71f2d9-f1c9-913b-818b-11402910xxxx

data

object

返回数据

qrUrl

string

生成的打赏链接

https://xxxxxx.aliyun-inc.com

code

string

对应的打赏的 code，用于回查打赏状态

xxsdfasfw

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "6a71f2d9-f1c9-913b-818b-11402910xxxx\n",
  "data": {
    "qrUrl": "https://xxxxxx.aliyun-inc.com",
    "code": "xxsdfasfw"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。

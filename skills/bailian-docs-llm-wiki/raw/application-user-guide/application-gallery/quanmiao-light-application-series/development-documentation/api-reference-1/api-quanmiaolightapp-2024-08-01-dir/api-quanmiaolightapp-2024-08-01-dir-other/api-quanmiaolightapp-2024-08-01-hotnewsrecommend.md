# HotNewsRecommend - 新闻热点推荐

热点新闻推荐

## 接口说明

理解用户意图，获取对应频道下热点列表，比如“播报体育新闻”。历史接口，建议走“播报单（热榜）问答接口 RunHotTopicChat”，完全覆盖了当前接口的能力。

欢迎前往[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)体验。

通过 SDK 方式调用 API 可参考控制台“API”下的 java、python 示例。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/HotNewsRecommend)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/HotNewsRecommend)

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

quanmiaolightapp:HotNewsRecommend

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/hotNewsRecommend HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

prompt

string

否

推荐新闻的提示词

今天的财经新闻

workspaceId

string

是

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

阿里云为该请求生成的唯一标识符。

575D5893-01DB-5C81-A899-74F67616762A

code

string

接口返回码：200：表示成功。其它：表示错误码。错误码详情，请参见错误码。

200

success

boolean

是否调用成功：true：调用成功。 false：调用失败。

True

message

string

错误说明

ok

data

object

新闻推荐结果

news

array<object>

推荐新闻列表

news

object

推荐新闻对象

title

string

标题

xx

content

string

内容

xx

url

string

链接

http://xxx

pubTime

string

发布时间

2024-09-10 15:32:00

source

string

新闻源

新华社

searchSource

string

搜索源

QuarkCommonNews：联网检索

imageUrls

array

新闻图片列表

imageUrls

string

图片地址列表

http://www.example.com/xxx.png

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "575D5893-01DB-5C81-A899-74F67616762A",
  "code": 200,
  "success": true,
  "message": "ok",
  "data": {
    "news": [
      {
        "title": "xx",
        "content": "xx",
        "url": "http://xxx",
        "pubTime": "2024-09-10 15:32:00",
        "source": "新华社",
        "searchSource": "QuarkCommonNews：联网检索",
        "imageUrls": [
          "http://www.example.com/xxx.png"
        ]
      }
    ]
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。

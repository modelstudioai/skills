# 对接自有知识库

通义深度搜索应用支持百炼知识库和用户自有知识库接入，本文档主要用于自有知识库接入规范的约束，用户可以参考如下接口规范进行知识库对接。

## **请求说明**

### **接口**

协议：HTTP+POST

接口：自定义

功能说明：该API允许通义深度搜索应用对您提供的接口执行复杂的文本查询、排序和分页操作。

### **请求头**

**参数名**

**类型**

**说明**

**是否必须**

Authorization

string

鉴权信息

是

Content-Type

string

静态值:application/json

是

### **请求体**

**参数名**

**类型**

**说明**

**是否必须**

rid

string

请求 ID

是

query

string

查询文本

是

num

int

召回数量，取值区间 1~100

是

page

int

页码，取值区间 1~100

否

debug

bool

调试模式，默认值 false

否

### **请求示例**

```
curl --location 'https://xxx' \
--header 'Authorization: Bearer lm-***' \
--header 'Content-Type: application/json' \
--data '{
    "rid": "10c96b02-4207-4991-820c-f8a855d1dc42",
    "query": "阿里云百炼",
    "num": 10,
    "debug": false
}'
```

## **响应说明**

### **响应参数**

**参数名**

**类型**

**说明**

**是否必须**

rid

string

请求 ID

是

status

int

状态码（0：成功）

是

message

string

状态消息

是

data

object

返回数据

是

data.total

int

召回总数

否

data.docs

array<object>

召回数据列表（字段可扩展）

是

data.docs.\[\].id

string

页面ID

是

data.docs.\[\].title

string

标题

是

data.docs.\[\].url

string

网页链接

是

data.docs.\[\].snippet

string

摘要

是

data.docs.\[\].content

string

网页原文

否

data.docs.\[\].timestamp\_format

string

网页发布时间

否

data.docs.\[\].timestamp

long

网页发布时间戳

否

data.docs.\[\].hostname

string

网站名

否

data.docs.\[\].hostlogo

string

网站logo

否

debug

object

调试数据

否

### **响应示例**

```
{
    "rid": "10c96b02-4207-4991-820c-f8a855d1dc42",
    "status": 0,
    "message": "success",
    "data": {
        "total": 10,
        "docs": [
            {
                "id": "cid-98cc77b09",
                "snippet": "阿里云百炼平台是阿里云推出的服务平台。开发者可通过“拖拉拽”5分钟开发一款大模型应用，***",
                "title": "阿里云百炼平台-百度百科",
                "url": "https://baike.baidu.com/item/***",
                "timestamp_format": "2025-09-02 00:00:00",
                "timestamp": 1756742400
                "hostname": "百度百科",
                "hostlogo": "https://cdn.sm.cn/temp/***",
            },
            {...}
        ]
    },
    "debug": {...}
}
```

## **注意事项**

最大容忍超时：timeout=3000ms

服务可用判定条件：HTTP状态码"200",且返回数据status为"0"

您的自建数据会按照账号加应用维度隔离，仅会被模型规划生成使用，并不会进行存储。

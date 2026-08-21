# 妙搜数据集管理通过API引入数据源

本文档主要介绍妙搜数据集管理中通过API引入数据源。

## 功能说明

-   客户侧有自己的搜索能力，且可以通过API方式访问，此时可以通过API引入数据源的方式，将三方API集成到妙搜中，作为一个数据源使用。
    
-   通过三方搜索API+妙搜大模型能力的加持可以实现智能搜索生成。
    
-   当前线上提供了JSON格式的API定义方式。
    

## 配置说明

### 配置样例

```
{
  "searchSourceRequestConfig": {
    "headers": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "method": "GET",
    "connectTimeout": 3000,
    "socketTimeout": 3000,
    "params": [
      {
        "name": "querySelf",
        "value": "${query}"
      },
      {
        "name": "current",
        "value": "${current}"
      },
      {
        "name": "size",
        "value": "${size}"
      },
      {
        "valueType": "boolean",
        "name": "includeContent",
        "value": "${includeContent}"
      },
      {
        "valueType": "time",
        "name": "startTime",
        "valueFormat": "yyyy-MM-dd HH:mm:ss",
        "value": "${startTime}"
      },
      {
        "valueType": "time",
        "name": "endTime",
        "valueFormat": "yyyy-MM-dd HH:mm:ss",
        "value": "${endTime}"
      }
    ],
    "pathParamsEnable": false,
    "body": "{\"query\":\"${querySelf}\",\"size\":\"${size}\",\"current\":\"${current}\"}",
    "url": "http://xxxx/api/search"
  },
  "searchSourceResponseConfig": {
    "jqNodes": [
      {
        "path": "totalSelf",
        "type": "number",
        "key": "total"
      },
      {
        "path": "dataSelf",
        "type": "list",
        "jqNodes": [
          {
            "path": "summary",
            "type": "string",
            "key": "summary"
          },
          {
            "path": "score",
            "type": "string",
            "key": "score"
          },
          {
            "path": "docUuid",
            "type": "string",
            "key": "docUuid"
          },
          {
            "path": "pubTime",
            "type": "string",
            "key": "pubTime"
          },
          {
            "path": "source",
            "type": "string",
            "key": "source"
          },
          {
            "path": "tag",
            "type": "string",
            "key": "tag"
          },
          {
            "path": "title",
            "type": "string",
            "key": "title"
          },
          {
            "path": ".",
            "type": "object",
            "jqNodes": [
              {
                "path": "docUuid",
                "type": "string",
                "key": "docUuid"
              }
            ],
            "key": "extendInfo"
          },
          {
            "path": "url",
            "type": "string",
            "key": "url"
          },
          {
            "path": "content",
            "type": "string",
            "key": "content"
          }
        ],
        "key": "data"
      }
    ]
  }
}
```

### 请求参数配置：searchSourceRequestConfig

-   URL地址：url；
    
    http://xxxx：要求公网可以直接访问。
    
-   http请求头：headers；
    
    这里可以添加Content-Type、添加鉴权信息等。
    
-   http-method：method，支持GET和POST请求；
    
-   连接过期时间：connectTimeout；
    
    单位毫秒，建议 6000内。
    
-   请求过期时间：socketTimeout；
    
    单位毫秒，建议 6000内。
    
-   是否path中设置参数：pathParamsEnable；
    
    默认false，true时会在url path方式设置参数，默认body中json方式传入。
    
-   请求参数解析：params；
    
    用来构建请求参数。
    
    参数
    
    解释说明
    
    name
    
    参数字段名字
    
    value
    
    参数字段取值，可以是固定值，也可以是变量，${变量名字}，支持的内置变量如下：
    
    -   query：搜索词
        
    -   current：当前页
        
    -   size：每页大小
        
    -   includeContent：是否包含正文，建议支持返回正文，可以是默认返回正文
        
    -   startTime：开始时间
        
    -   endTime：结束时间
        
    
    valueType
    
    字段类型，默认string，用来转换格式，支持的字段类型如下：
    
    -   string
        
    -   number
        
    -   boolean
        
    -   time
        
    
    valueForma
    
    valueType=time时有效，time的格式如下
    
    -   yyyy-MM-dd
        
    -   yyyy-MM-dd HH:mm:ss
        
    -   longTime
        
    -   longTimeMillis
        
    
-   请求body信息：body。
    
    请求body内容：可以通过${变量名称}方式取值，可以从内置变量或者params定义的变量中取值。
    

### 响应解析配置：searchSourceResponseConfig

标准响应：这里的解析就是为了解析出如下格式的信息。

```
{
  "total": 100,
  "data": [{
    "url": "http://xxx",
    "summary": "xxx",
    "score": 1,
    "docUuid": "xxx",
    "pubTime": "2024-12-10 15:43:44",
    "source": "xxx",
    "tag": "xxx",
    "title": "xxx",
    "content": "xxx"
  }]
}
```

#### jqNodes

解析配置，支持三级，字段如下：

**字段**

**解释说明**

path

json路径，比如total

type

类型，有如下类型：

-   string：字符串
    
-   number：数值
    
-   list：列表
    
-   object：对象
    

key

映射的标准响应中的字段名字

jqNodes

子节点定义

## **常见问题**

### **Q：是否支持在 HTTP Header 中传递自定义身份参数？**  
A：

支持。您可以在请求头（Headers）中直接添加自定义字段（Key-Value）。该字段与标准字段（`Content-Type`）同级，服务端会自动解析并识别您的系统身份标识。

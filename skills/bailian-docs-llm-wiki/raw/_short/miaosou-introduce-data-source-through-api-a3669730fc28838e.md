# 妙搜数据集管理通过API引入数据源

本文档主要介绍妙搜数据集管理中通过API引入数据源。

<a id="功能说明"></a>

<a id="cnR8P"></a>

## 功能说明

-   客户侧有自己的搜索能力，且可以通过API方式访问，此时可以通过API引入数据源的方式，将三方API集成到妙搜中，作为一个数据源使用。
-   通过三方搜索API+妙搜大模型能力的加持可以实现智能搜索生成。
-   当前线上提供了JSON格式的API定义方式。

<a id="配置说明"></a>

<a id="U6eNO"></a>

## 配置说明

<a id="配置样例"></a>

<a id="W8Lkb"></a>

### 配置样例

<a id="code-block"></a>

```json
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

<a id="请求参数配置-searchsourcerequestconfig"></a>

<a id="RdFWO"></a>

### 请求参数配置：searchSourceRequestConfig

-   URL地址：url；
    
    `http://xxxx`：要求公网可以直接访问。
    
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
    
    <table><tbody><tr><td><p>参数</p></td><td><p>解释说明</p></td></tr><tr><td><p>name</p></td><td><p>参数字段名字</p></td></tr><tr><td><p>value</p></td><td><p>参数字段取值，可以是固定值，也可以是变量，${变量名字}，支持的内置变量如下：</p><ul><li><p>query：搜索词</p></li><li><p>current：当前页</p></li><li><p>size：每页大小</p></li><li><p>includeContent：是否包含正文，建议支持返回正文，可以是默认返回正文</p></li><li><p>startTime：开始时间</p></li><li><p>endTime：结束时间</p></li></ul></td></tr><tr><td><p>valueType</p></td><td><p>字段类型，默认string，用来转换格式，支持的字段类型如下：</p><ul><li><p>string</p></li><li><p>number</p></li><li><p>boolean</p></li><li><p>time</p></li></ul></td></tr><tr><td><p>valueForma</p></td><td><p>valueType=time时有效，time的格式如下</p><ul><li><p>yyyy-MM-dd</p></li><li><p>yyyy-MM-dd HH:mm:ss</p></li><li><p>longTime</p></li><li><p>longTimeMillis</p></li></ul></td></tr></tbody></table>
    
-   请求body信息：body。
    
    请求body内容：可以通过${变量名称}方式取值，可以从内置变量或者params定义的变量中取值。
    

<a id="响应解析配置-searchsourceresponseconfig"></a>

<a id="Q04eV"></a>

### 响应解析配置：searchSourceResponseConfig

标准响应：这里的解析就是为了解析出如下格式的信息。

<a id="code-block-2"></a>

```json
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

<a id="jqnodes"></a>

<a id="eKHCR"></a>

#### jqNodes

解析配置，支持三级，字段如下：

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>解释说明</strong></p></th></tr></thead><tbody><tr><td><p>path</p></td><td><p>json路径，比如total</p></td></tr><tr><td><p>type</p></td><td><p>类型，有如下类型：</p><ul><li><p>string：字符串</p></li><li><p>number：数值</p></li><li><p>list：列表</p></li><li><p>object：对象</p></li></ul></td></tr><tr><td><p>key</p></td><td><p>映射的标准响应中的字段名字</p></td></tr><tr><td><p>jqNodes</p></td><td><p>子节点定义</p></td></tr></tbody></table>

<a id="常见问题"></a>

<a id="3bb7ed76e4qmp"></a>

## 常见问题

<a id="q-是否支持在-http-header-中传递自定义身份参数-a"></a>

<a id="41e924adafejc"></a>

### Q：是否支持在 HTTP Header 中传递自定义身份参数？  
A：

支持。您可以在请求头（Headers）中直接添加自定义字段（Key-Value）。该字段与标准字段（`Content-Type`）同级，服务端会自动解析并识别您的系统身份标识。

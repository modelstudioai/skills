# SaveVirtualDatasourceDdl - 向虚拟数据源中添加ddl语句

向您当前指定的业务空间下指定的虚拟数据源实例中添加ddl语句，析言GBI云服务会将您的ddl语句解析成相关的表结构信息并进行维护。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/SaveVirtualDatasourceDdl)

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

dataanalysisgbi:SaveVirtualDatasourceDdl

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/virtualDatasource/addDdl2VirtualInstance HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

当前请求所使用的阿里云百炼业务空间 id

llm-2v3934xtp49esw64

body

object

否

请求体参数

vdbId

string

是

虚拟数据源实例 id

vdb-E0F693C8-9F72-5830-B81A-696C9D8EBBD1

ddl

string

是

create 类型数据库 ddl 语句，支持传入多条，多条之间请用换行符分割（“\\n”）。

CREATE TABLE user (id int NOT NULL AUTO\_INCREMENT comment 'ID',name varchar(10) NOT NULL comment '姓名', dept\_id int NOT NULL comment '部门ID', salary bigint NULL DEFAULT 0 comment '薪水', PRIMARY KEY (\`id\`), KEY \`idx\_name\` (\`name\`), KEY \`d\_id\` (\`dept\_id\`), CONSTRAINT \`d\_id\` FOREIGN KEY (\`dept\_id\`) REFERENCES \`department\` (\`id\`)) COMMENT='This is my table' ENGINE=InnoDB AUTO\_INCREMENT=20094 DEFAULT CHARSET=utf8 ;

## 返回参数

名称

类型

描述

示例值

object

Result

data

any

返回信息

true

errorMsg

string

错误描述信息

NoAuth

code

string

错误码

NoAuth

success

boolean

true 接口调用成功，false 接口调用失败

true

requestId

string

请求 id，每次请求都是唯一值，便于后续排查问题

72ABCA5B-1E93-55D3-8A61-6D8A03CC5C8B

## 示例

正常返回示例

`JSON`格式

```
{
  "data": true,
  "errorMsg": "NoAuth",
  "code": "NoAuth",
  "success": true,
  "requestId": "72ABCA5B-1E93-55D3-8A61-6D8A03CC5C8B"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

401

NoAuth

Bad Request: Workspace.Illegal.Auth.

当前所使用的账号无所指定业务空间的权限

401

Internal.Error

Bad Request: Internal Error.

内部错误，请联系客服人员排查

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。

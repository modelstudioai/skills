# 错误码-千问联网检索Agent

千问联网检索Agent调用过程中的错误码和错误信息可参考本文说明。

**HTTP请求码**

**错误码code**

**错误信息message**

**说明**

400

InvalidParameter

Some parameters have validation errors, or error default values are undefined.

未定义的参数异常，建议检查请求参数的字段或类型是否符合文档规范

404

NotFound

Resource not found.

资源不存在，一般是访问了不存在或没有权限的资源，建议检查请求地址、配置参数、文件参数等信息

500

InternalError

The request processing has failed due to some unknown error, exception or failure.

系统内部未知异常，建议提供请求 ID 给技术人员排查

400

Unclassified.Error

Unclassified but known cause error.

未分类的已知错误，建议提供请求 ID 给技术人员排查

400

ParamValue.Error

Input parameter value business validation error.

参数业务校验错误，一般是数据类型问题，建议检查参数类型是否符合文档规范

400

LoadConfig.Error

Failed to load agent configuration.

无法加载智能体应用配置，建议检查应用发布状态、agent\_id、agent\_version 等信息是否配置正确

400

InternalInterface.Error

Internal interface error.

内部接口调用错误，一般发生在服务内部，建议检查注册的接口是否存在不可用的情况

404

RequestPath.NotFound

Request path not found.

访问的服务地址不存在，建议检查接口路径是否正确及是否存在异常字符

400

ProcessTimeout.Error

Timeout occurs during deep search process.

内部执行超时，建议进行重试调用

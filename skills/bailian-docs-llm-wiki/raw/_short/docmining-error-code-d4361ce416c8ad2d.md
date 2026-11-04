# 错误码

**HTTP请求码**

**错误码code**

**错误信息message**

**说明**

500

InternalError

internal error

请求内部错误

500

InternalError

internal service call exception

内部服务调用异常

400

InvalidParameter

prompt is empty

提示词为空，请检查提示词参数是否正确传递

400

InvalidParameter

type mismatch

能力类型不符合，请检查capabilityType参数是否符合API要求

400

InvalidParameter

file empty or not exist

文档为空或不存在，请检查文档ID是否正确

400

InvalidParameter

file and workspace mismatch

文档和业务空间不匹配，请检查文档是否在当前请求业务空间下上传

400

InvalidParameter

request body format conversion failed

请求体格式转换失败，请检查请求体是否符合参数规范

400

InvalidParameter

request parameters incorrect

请求参数有误，检查是否缺少必须的参数

400

InvalidParameter

file extension empty

文档名后缀不能为空

404

NotFound

request path not found

请求路径不存在，请检查API路径是否正确

400

InvalidParameter

prompt word count exceeds limit

提示词字数超过上限，提示词字数最大支持8000字

400

InvalidParameter.File

file size exceeds limit

文档大小超过限制，请检查文档大小是否小于等于100MB

400

InvalidParameter.File

file page count exceeds limit

文档页数超过限制，单文档最高支持1000页

400

InvalidParameter.File

file resolution exceeds limit

文档分辨率超过限制，不支持8192px以上的图片

400

InvalidParameter.File

file format not supported

文档格式不支持，当前支持格式为PDF/TXT/MD/HTML/DOC/PPT/XLS/PNG/BMP/GIF/JPG/JPEG

400

InvalidParameter.File

file content empty

文档内容为空，请检查文档内容是否为空

400

InvalidParameter.File

file encrypted or corrupted

文档已加密或损坏，请检查文档是否可以正常打开

400

InvalidParameter.File

exceeds max file upload limit

超过文档上传数量限制，最多支持100个文档对话

400

InvalidParameter.File

upload list is empty

文档上传列表为空

400

InvalidParameter.File

file processing timeout

文档处理超时，请重试

400

InvalidParameter.File

file not support

文档不支持

400

InvalidParameter.File

file deleted

文档已删除

400

InvalidParameter.File

file parsing failed

文档解析失败，请重试

400

InvalidParameter.File

file parsing in progress

文档正在解析中，请稍后再进行对话

400

InvalidParameter

File lease\_id expired or not exist.

leaseId过期或者不存在，需重新申请租约

400

InvalidParameter.File

submit file failed, unsupported file.

提交解析失败，不支持的文档

400

Workspace.AccessDenied

Workspace.AccessDenied

子账号没有开通企业空间权限

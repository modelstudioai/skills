# 常见问题

#### 当调用全妙轻应用API接口时，如果收到403报错：`"You are not authorized to do this operation"`或`" You are not authorized to perform this action "`，应如何处理？

当前使用的账号没有访问全妙轻应用API接口的权限，您可以尝试以下解决方案处理：

-   请使用主账号在[RAM控制台](https://ram.console.aliyun.com/)中为您的RAM用户（子账号）或RAM角色配置`AliyunQuanMiaoLightAppFullAccess`系统策略。具体操作，请参见管理RAM用户的权限或管理RAM角色的权限。
    
    **说明**您也可通过为指定用户添加权限接口实现授权操作。
    
-   为RAM用户（或RAM角色）授予百炼业务空间权限。具体操作，请参见为RAM用户授予百炼业务空间权限（或为RAM角色授予业务空间权限）。
    
-   请检查[workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)的赋值是否正确，请填写您RAM用户（或RAM角色）账号所属业务空间ID。在百炼控制台中，打开**业务空间详情**对话框，获取**业务空间id**（如 `ws_cpgCvmBeG...`）和 **agentKey** 等参数值，然后将**业务空间id**填入 API 调用代码中的 `.workspaceId()` 参数。
    

**调用全妙轻应用 API 进行历史对话时，收到报错 `"Error: Invalidcontents code: 400，httpStatusCode: 200"`，应如何处理？**该报错出现在使用历史对话调用全妙轻应用的场景中。虽然 API 的 HTTP 状态码为 200 且外层 `code` 字段为 `successful`，但业务数据 `data` 中的 `status` 为 `FAILED`，`errorMessage` 为 `No content found`，表示全妙轻应用在处理请求时未找到有效的对话内容。返回体示例如下：

```
{
  "code": "successful",
  "data": {
    "errorMessage": "No content found",
    "results": [],
    "status": "FAILED"
  },
  "httpStatusCode": "200",
  "message": "successful",
  "requestId": "52676CAF-54AA-50D9-85F6-F6AE5383661A",
  "success": true
}
```

建议排查以下方面：

-   检查传入的对话内容（`contents`）是否为空或格式不正确。
-   确认历史对话的上下文数据是否完整且未过期。
-   如排查后问题仍存在，请提交工单并附上响应体中的 `requestId`，联系技术支持进一步排查。

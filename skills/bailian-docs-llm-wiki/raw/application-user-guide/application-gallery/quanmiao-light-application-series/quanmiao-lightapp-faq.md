# 常见问题

#### **当调用全妙轻应用API接口时，如果收到403报错：**`**"You are not authorized to do this operation"**`**或**`**"**You are not authorized to perform this action**"**`**，应如何处理？**

当前使用的账号没有访问全妙轻应用API接口的权限，您可以尝试以下解决方案处理：

-   请使用主账号在[RAM控制台](https://ram.console.aliyun.com/)中为您的RAM用户（子账号）或RAM角色配置`**AliyunQuanMiaoLightAppFullAccess**`系统策略。具体操作，请参见[为RAM用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)或[管理RAM角色的权限](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-role)。
    
    **说明**
    
    您也可通过[为指定用户添加权限](https://help.aliyun.com/zh/ram/developer-reference/api-ram-2015-05-01-attachpolicytouser)接口实现授权操作。
    
-   为RAM用户（或RAM角色）授予百炼业务空间权限。具体操作，请参见[为RAM用户授予百炼业务空间权限](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users#ead9a51b62f7t)（或[为RAM角色授予业务空间权限](https://help.aliyun.com/zh/model-studio/use-a-ram-role-to-log-in-and-use-bailian#ac4add724bc45)）。
    
-   请检查[workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)的赋值是否正确，请填写您RAM用户（或RAM角色）账号所属业务空间ID。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0796897471/p955348.png)

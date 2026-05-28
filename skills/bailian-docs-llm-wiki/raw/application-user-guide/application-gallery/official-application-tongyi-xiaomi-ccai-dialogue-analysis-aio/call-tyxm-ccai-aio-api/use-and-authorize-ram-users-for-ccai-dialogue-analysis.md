# 通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作

如果您有让子账号授权管理阿里云百炼服务调用的需求，首先需要创建RAM用户。您既需要通过RAM控制台进行RAM授权，也需要通过阿里云百炼控制台进行控制台授权。

## 创建RAM用户

请参考文档[创建RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)完成RAM用户创建。

## **通过RAM控制台授权**

1.  请访问[RAM控制台](https://ram.console.aliyun.com/users)。
    
2.  在左侧导航栏选择**身份管理** > **用户**。![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9484877961/p729387.png)
    
3.  在待授权的RAM子账号的**操作**列，点击**添加权限**。在**权限策略**区域的搜索框中搜索并勾选[阿里云百炼RAM权限](https://help.aliyun.com/zh/model-studio/bailian-ram-permission)（AliyunSFMFullAccess），并单击**确认新增授权**，完成授权操作。
    
    ![阿里云百炼授权马赛克2.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2827723371/p881885.png)
    

## **通过阿里云百炼控制台授权**

1.  访问**[权限管理](https://bailian.console.aliyun.com/?tab=app#/authority)**页面，单击**新增用户**。
    
2.  选择需要管理阿里云百炼服务的 RAM 用户，并定义用户名称，单击**确定**，即完成添加用户。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0954505571/p996195.png)
    
3.  对新增的用户需要进行权限配置，在新增的用户右侧点击**权限管理**，进行授权操作。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0954505571/p996199.png)
    
4.  进入**权限管理**页面后，点击**添加权限**按钮，选择**管理员**，点击**确定**按钮，完成授权操作。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0954505571/p996206.png)

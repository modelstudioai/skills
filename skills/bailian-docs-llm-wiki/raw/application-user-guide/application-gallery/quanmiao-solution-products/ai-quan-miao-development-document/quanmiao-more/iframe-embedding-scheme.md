# 全妙iframe嵌入方案

本文档是关于全妙SaaS产品以iframe形式嵌入第三方系统的技术对接方案。

### **应用场景描述**

当您想要将全妙SaaS产品嵌入到自己的内部系统（如 OA、CRM、门户平台）中时，可以应用此方式，快速集成，开发成本低，并支持配置对应的视觉参数，保持您企业内部视觉的统一。

### **具体的接入步骤**

##### **1\. 给阿里云主账号创建子账号**

使用主账号在阿里云上[RAM用户管理](https://ram.console.aliyun.com/users)创建子账号，并申请ak、sk并记录下来。只需要一个子账号，后续不同账号下数据权限通过AssumeRole 接口中的RoleSessionName来区分

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7319255671/p1034549.png)

##### **2\. 给子账号新增授权**

进入用户详情页面，在权限管理tab，给子账号新增授权，增加AliyunSTSAssumeRoleAccess和AliyunAiMiaoBiFullAccess 权限

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7319255671/p1034550.png)

##### **3\. 给**主账号**创建角色**

使用主账号在阿里云上[角色管理](https://ram.console.aliyun.com/roles)中创建角色，并赋予角色上面权限（AliyunSTSAssumeRoleAccess和AliyunAiMiaoBiFullAccess），只需要申请一个角色。

##### **4\. 进入百炼控制台确认角色**

使用主账号进入百炼控制台，在权限配置地方配置，选择新增用户，弹窗中类型选择RAM角色，RAM角色中选择刚刚创建的角色，确定即可。**注意是给角色授权，而不是给用户授权**。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7319255671/p1034552.png)

##### **5\. 生成免登录地址**

服务端提供一个中转访问链接，例如 https://xx.com/aimiaobi，访问这个地址时，服务端判断用户是否登录自己的系统，假如未登录则重定向到自己系统内的登录页面，假如已登录则服务器内调用阿里云api，生成阿里云免登地址，并返回301重定向地址给浏览器端，浏览器自动重定向到对应地址完成阿里云登录。免登链接参考[免登访问](https://help.aliyun.com/zh/document_detail/91911.html)，编写代码生成，具体实现过程如下：

1.  调用[AssumeRole - 获取扮演角色的临时身份凭证](https://help.aliyun.com/zh/ram/developer-reference/api-sts-2015-04-01-assumerole)生成临时AccessKeyId、AccessKeySecret和SecurityToken，通过接口中的RoleSessionName来区分不同的用户（数据隔离）；
    
2.  用上述生成的AccessKeyId、AccessKeySecret和SecurityToken，调用[GetSigninToken](https://help.aliyun.com/zh/document_detail/91913.html)生成SigninToken。**特别注意GetSigninToken请求参数中必须传入TicketType=mini；**
    
3.  使用SigninToken，拼接免登地址（类似：https://signin.aliyun.com/federation?Action=Login&LoginUrl=XXX&Destination=XXX&SigninToken=XXX）返回给浏览器端，您可以[在这里拼接](https://aimiaobi.console.aliyun.com/#/iframeConfig)调试示例。
    
    1.  其中Destination参数就是需要跳转全妙的目标地址（需要将全妙地址的host域名aimiaobi.console.aliyun.com改为aimiaobi4service.console.aliyun.com），如需定制内容，您可以[在这里定制生成](https://aimiaobi.console.aliyun.com/#/iframeConfig)；
        
    2.  LoginUrl使用上面服务链接，例如https://xx.com/aimiaobi，用于登录失效时，自动重定向到对应登录地址重新进行用户登录认证。![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3483236771/p1068279.png)
        

##### **6\. 嵌入**

客户内部网站中需要iframe嵌入全妙网页的地方，直接嵌入前面提供的服务端中转链接，例如https://xx.com/aimiaobi。

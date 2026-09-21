# 全妙iframe嵌入方案

本文档是关于全妙SaaS产品以iframe形式嵌入第三方系统的技术对接方案。

### 应用场景描述

当您想要将全妙SaaS产品嵌入到自己的内部系统（如 OA、CRM、门户平台）中时，可以应用此方式，快速集成，开发成本低，并支持配置对应的视觉参数，保持您企业内部视觉的统一。

### 具体的接入步骤

##### 1\. 给阿里云主账号创建子账号

使用主账号在阿里云上[RAM用户管理](https://ram.console.aliyun.com/users)创建子账号，并申请ak、sk并记录下来。只需要一个子账号，后续不同账号下数据权限通过AssumeRole 接口中的RoleSessionName来区分

##### 2\. 给子账号新增授权

进入用户详情页面，在权限管理tab，给子账号新增授权，增加AliyunSTSAssumeRoleAccess和AliyunAiMiaoBiFullAccess 权限

##### 3\. 给主账号创建角色

使用主账号在阿里云上[角色管理](https://ram.console.aliyun.com/roles)中创建角色，并赋予角色上面权限（AliyunSTSAssumeRoleAccess和AliyunAiMiaoBiFullAccess），只需要申请一个角色。

##### 4\. 进入百炼控制台确认角色

使用主账号进入百炼控制台，在权限配置地方配置，选择新增用户，弹窗中类型选择RAM角色，RAM角色中选择刚刚创建的角色，确定即可。**注意是给角色授权，而不是给用户授权**。

##### 5\. 生成免登录地址

服务端提供一个中转访问链接，例如 [https://xx.com/aimiaobi，访问这个地址时，服务端判断用户是否登录自己的系统，假如未登录则重定向到自己系统内的登录页面，假如已登录则服务器内调用阿里云api，生成阿里云免登地址，并返回301重定向地址给浏览器端，浏览器自动重定向到对应地址完成阿里云登录。免登链接参考\[免登访问](https://xx.com/aimiaobi%EF%BC%8C%E8%AE%BF%E9%97%AE%E8%BF%99%E4%B8%AA%E5%9C%B0%E5%9D%80%E6%97%B6%EF%BC%8C%E6%9C%8D%E5%8A%A1%E7%AB%AF%E5%88%A4%E6%96%AD%E7%94%A8%E6%88%B7%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%E8%87%AA%E5%B7%B1%E7%9A%84%E7%B3%BB%E7%BB%9F%EF%BC%8C%E5%81%87%E5%A6%82%E6%9C%AA%E7%99%BB%E5%BD%95%E5%88%99%E9%87%8D%E5%AE%9A%E5%90%91%E5%88%B0%E8%87%AA%E5%B7%B1%E7%B3%BB%E7%BB%9F%E5%86%85%E7%9A%84%E7%99%BB%E5%BD%95%E9%A1%B5%E9%9D%A2%EF%BC%8C%E5%81%87%E5%A6%82%E5%B7%B2%E7%99%BB%E5%BD%95%E5%88%99%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%86%85%E8%B0%83%E7%94%A8%E9%98%BF%E9%87%8C%E4%BA%91api%EF%BC%8C%E7%94%9F%E6%88%90%E9%98%BF%E9%87%8C%E4%BA%91%E5%85%8D%E7%99%BB%E5%9C%B0%E5%9D%80%EF%BC%8C%E5%B9%B6%E8%BF%94%E5%9B%9E301%E9%87%8D%E5%AE%9A%E5%90%91%E5%9C%B0%E5%9D%80%E7%BB%99%E6%B5%8F%E8%A7%88%E5%99%A8%E7%AB%AF%EF%BC%8C%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E9%87%8D%E5%AE%9A%E5%90%91%E5%88%B0%E5%AF%B9%E5%BA%94%E5%9C%B0%E5%9D%80%E5%AE%8C%E6%88%90%E9%98%BF%E9%87%8C%E4%BA%91%E7%99%BB%E5%BD%95%E3%80%82%E5%85%8D%E7%99%BB%E9%93%BE%E6%8E%A5%E5%8F%82%E8%80%83%5B%E5%85%8D%E7%99%BB%E8%AE%BF%E9%97%AE)\]([https://help.aliyun.com/zh/document\_detail/91911.html)，编写代码生成，具体实现过程如下：](https://help.aliyun.com/zh/document_detail/91911.html\)%EF%BC%8C%E7%BC%96%E5%86%99%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90%EF%BC%8C%E5%85%B7%E4%BD%93%E5%AE%9E%E7%8E%B0%E8%BF%87%E7%A8%8B%E5%A6%82%E4%B8%8B%EF%BC%9A)

1.  调用[AssumeRole - 获取扮演角色的临时身份凭证](https://help.aliyun.com/zh/ram/developer-reference/api-sts-2015-04-01-assumerole)生成临时AccessKeyId、AccessKeySecret和SecurityToken，通过接口中的RoleSessionName来区分不同的用户（数据隔离）；
    
2.  用上述生成的AccessKeyId、AccessKeySecret和SecurityToken，调用[GetSigninToken](https://help.aliyun.com/zh/document_detail/91913.html)生成SigninToken。**特别注意GetSigninToken请求参数中必须传入TicketType=mini；**
    
3.  使用SigninToken，拼接免登地址（类似：[https://signin.aliyun.com/federation?Action=Login&amp;LoginUrl=XXX&amp;Destination=XXX&amp;SigninToken=XXX）返回给浏览器端，您可以\[在这里拼接](https://signin.aliyun.com/federation?Action=Login&amp;LoginUrl=XXX&amp;Destination=XXX&amp;SigninToken=XXX%EF%BC%89%E8%BF%94%E5%9B%9E%E7%BB%99%E6%B5%8F%E8%A7%88%E5%99%A8%E7%AB%AF%EF%BC%8C%E6%82%A8%E5%8F%AF%E4%BB%A5%5B%E5%9C%A8%E8%BF%99%E9%87%8C%E6%8B%BC%E6%8E%A5)\]([https://aimiaobi.console.aliyun.com/#/iframeConfig)调试示例。](https://aimiaobi.console.aliyun.com/#/iframeConfig\)%E8%B0%83%E8%AF%95%E7%A4%BA%E4%BE%8B%E3%80%82)
    
    1.  其中Destination参数就是需要跳转全妙的目标地址（需要将全妙地址的host域名aimiaobi.console.aliyun.com改为aimiaobi4service.console.aliyun.com），如需定制内容，您可以[在这里定制生成](https://aimiaobi.console.aliyun.com/#/iframeConfig)；
    2.  LoginUrl使用上面服务链接，例如[https://xx.com/aimiaobi，用于登录失效时，自动重定向到对应登录地址重新进行用户登录认证。Login](https://xx.com/aimiaobi%EF%BC%8C%E7%94%A8%E4%BA%8E%E7%99%BB%E5%BD%95%E5%A4%B1%E6%95%88%E6%97%B6%EF%BC%8C%E8%87%AA%E5%8A%A8%E9%87%8D%E5%AE%9A%E5%90%91%E5%88%B0%E5%AF%B9%E5%BA%94%E7%99%BB%E5%BD%95%E5%9C%B0%E5%9D%80%E9%87%8D%E6%96%B0%E8%BF%9B%E8%A1%8C%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95%E8%AE%A4%E8%AF%81%E3%80%82Login) 接口包含以下必填请求参数（均为 String 类型，需 URLEncode）：**Action**，值为 `Login`，表示操作接口名；**LoginUrl**，登录页地址，Session 失效后跳转回该地址重新登录；**Destination**，登录成功后的跳转目的地址，必须为阿里云官网域名；**SigninToken**，通过 GetSignInToken 接口获取的临时安全令牌。

##### 6\. 嵌入

客户内部网站中需要iframe嵌入全妙网页的地方，直接嵌入前面提供的服务端中转链接，例如[https://xx.com/aimiaobi。](https://xx.com/aimiaobi%E3%80%82)

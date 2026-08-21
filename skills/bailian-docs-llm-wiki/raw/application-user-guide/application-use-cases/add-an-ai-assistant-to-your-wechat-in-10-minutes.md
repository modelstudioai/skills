# 10分钟让微信公众号成为智能客服

在阿里云上只需 10 分钟即可将您的微信公众号（订阅号）变成 AI 智能客服，以便全天候（7x24）回应客户咨询，提升用户体验、增强业务竞争力。

## **方案概览**

将微信公众号（订阅号）变成 AI 智能客服，只需 4 步：

1.  **创建大模型问答应用**：我们将先通过阿里云百炼创建一个大模型应用，并获取调用大模型应用 API 的相关凭证。
    
2.  **搭建微信公众号连接流：**基于阿里云的 AppFlow 服务，在无需编写代码的情况下，完成微信公众号和阿里云百炼 RAG 应用的关联，实现用户在微信公众号聊天中和 RAG 应用对话。
    
3.  **验证 AI 智能客服：**接着您可以直接与公众号对话，验证是否配置成功。
    
4.  **增加私有知识：**最后可以通过准备一些私有知识，让 AI 助理能回答原本无法准确回答的问题，帮助您更好地应对客户咨询。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7005080371/p833940.png)

![7b29f72d-3b9d-4fb1-867f-fc19aa575644](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9763691271/p825777.gif)

## 1\. 创建大模型问答应用

首先创建百炼应用，获取大模型推理 API 服务。

### 1.1 创建应用

1.  进入百炼控制台的[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面**，**点击右上角**创建应用**，选择**智能体应用**，点击**立即创建**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9119384671/p1019020.png)
    
2.  在**应用设置**页面，模型选择千问-Plus。该模型能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间，适合本场景中的任务需求。其他参数保持默认。
    
    > 您也可以选择输入一些 Prompt，比如设置一些人设以引导大模型更好的应对客户咨询。
    
    ```
    你叫小助，是我们公司的 AI 助手，可以帮助客户解答产品选购、使用等方面的问题。
    请总是给出简短的回答，不要讲太多。
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9805168571/p944468.png)
    
3.  在页面右侧可以提问验证模型效果。不过您会发现，目前它还无法准确回答你们公司的商品信息。点击右上角的**发布**，我们将在后面的步骤中去解决这一问题。 ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8936289171/p816045.png)
    

### **1.2 获取调用 API 所需的应用ID和API Key**

为了在后续通过 API 调用大模型应用的能力，需要获取阿里云百炼API Key和应用 ID。

1.  在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中可以查看所有百炼应用 ID。保存应用 ID 到本地用于后续配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p959107.png)
    
2.  前往[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面，点击**创建API Key**，在弹出窗口中创建一个新 API-Key。保存 API-Key 到本地用于后续配置。
    

## 2\. 创建微信公众号连接流

AppFlow 可以让您在不写代码的情况下，通过界面配置就可以将阿里云百炼 RAG 应用和微信公众号连接起来。您可以通过预置的 AppFlow 模板创建一个微信公众号连接流。

如果您的微信公众号已经完成认证，您可以使用微信[客户消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#%E5%AE%A2%E6%9C%8D%E6%8E%A5%E5%8F%A3-%E5%8F%91%E6%B6%88%E6%81%AF)回复用户在公众号的咨询，如果您没有完成认证，只能使用[被动回复消息功能](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Passive_user_reply_message.html)回复用户，该功能将消息响应时间限制为 5 秒，超时将无法回复。

是否完成认证可以在[微信公众号后台](https://mp.weixin.qq.com/)，在左侧菜单选择**设置与开发** > **账号设置**，在账号设置页面中查看。您可以根据认证情况选择下面的创建方案。![bcc603653c5d4b75efee061b67274081](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0305512371/p875724.png)

## 已经认证的公众号

1.  使用[AppFlow模板](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-kdjfhj1kg123jsj5439fj2?from=solution)创建连接流，点击**立即使用**进入创建流程。![2024-11-07\_16-57-05](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869662.png)
    
2.  访问[微信公众号后台](https://mp.weixin.qq.com/)，在左侧菜单选择**设置与开发** > **开发接口管理**。选择基本配置页签，获取 AppID。![2024-11-07\_16-27-30](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869597.png)
    
3.  在连接流的**账户授权**配置向导页，点击**添加新凭证**并选择**添加新凭证**。在授权页面填入 AppID，点击授权并在新的页面使用微信扫码完成授权。授权后，Appflow 会自动帮您配置公众号，您无需任何操作。授权完成后，您需要回到连接流的**账户授权**配置向导页，选择刚才授权的微信公众号。
    
    **说明**
    
    在新页面使用微信扫码进行授权时，请务必使用公众号的主管理员账号完成授权操作，否则将导致授权失败。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5810021671/p1019036.png)![2024-11-07\_16-24-15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869594.png)
    
4.  在连接流的**账户授权**配置向导页，点击**前往授权**。在创建凭证对话框中，填入之前获取的 API-KEY，并设置一个自定义凭证名称。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5810021671/p1019037.png)
    
5.  在**执行动作**配置向导页，填写已获取的阿里云百炼**应用ID**（[1.2 获取调用 API 所需的应用ID和API Key](#4a211d24e5ybu)），完成后点击**下一步**。![2024-08-15\_15-13-51](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8667073271/p835380.png)
    
6.  在**基本信息**配置向导页，填写**连接流名称**和**连接流描述**（建议保持默认），完成后点击**下一步**。
    
7.  界面提示流程配置成功，点击**发布**。![2024-11-07\_17-04-51](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869670.png)
    

## 没有认证的公众号

1.  使用[AppFlow模板](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-djfhj1kg124jsj5439fj2k?from=solution)创建连接流，点击**立即使用**进入创建流程。![2024-11-07\_17-07-32](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869673.png)
    
2.  访问[微信公众号后台](https://mp.weixin.qq.com/)，在左侧菜单选择**设置与开发** > **开发接口管理**。选择基本配置页签，获取 AppID。![2024-11-07\_16-27-30](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869597.png)
    
3.  在连接流的**账户授权**配置向导页，点击**选择新凭证**并选择**添加新凭证**。在授权页面填入 AppID，点击授权并在新的页面使用微信扫码完成授权。授权后，Appflow 会自动帮您配置公众号，您无需任何操作。授权完成后，您需要回到连接流的**账户授权**配置向导页，选择刚授权的微信公众号。
    
    **说明**
    
    在新页面使用微信扫码进行授权时，请务必使用公众号的主管理员账号完成授权操作，否则将导致授权失败。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5810021671/p1019034.png)![2024-11-07\_16-24-15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869594.png)![2024-11-07\_16-50-48](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869647.png)
    
    ![2024-11-07\_16-24-15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869594.png)![2024-11-07\_16-50-48](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869647.png)
    
4.  在连接流的**账户授权**配置向导页，点击**前往授权**。在创建凭证对话框中，填入之前获取的 API-KEY，并设置一个自定义凭证名称。![2024-08-13\_09-33-07](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2838553271/p834117.png)
    
5.  在**执行动作**配置向导页，填写已获取的阿里云百炼**应用ID**（[1.2 获取调用 API 所需的应用ID和API Key](#4a211d24e5ybu)），完成后点击**下一步**。![2024-08-13\_09-36-39](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2838553271/p834118.png)
    
6.  在**基本信息**配置向导页，填写**连接流名称**和**连接流描述**（建议保持默认），完成后点击**下一步**。
    
7.  界面提示流程配置成功，点击**发布**。![2024-11-07\_16-53-08](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8121790371/p869651.png)
    

## 3\. 验证公众号上的 AI 智能客服

现在，您可以访问公众号并发送消息，即可收到 AI 智能客服的回复。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9763691271/p825767.png)

## 4\. 为 AI 客服增加私有知识

通过前面的步骤，您已经拥有了一个可以和客户对话的 AI 智能客服。但是，如果想让 AI 智能客服像公司员工一样，更加精准且专业地回答与商品相关的问题，我们还需要为大模型应用配置知识库。

假设您是一家售卖智能手机的公司。您的网站上会有很多与智能手机相关的信息，如支持双卡双待、屏幕、电池容量、内存等信息。不同机型的详细配置清单参考：[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)。

### **4.1 配置知识库**

接下来，我们可以尝试让大模型在面对客户问题时参考这份文档，以产出一个更准确的回答和建议。

1.  **上传文件：**在阿里云百炼控制台的[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)页签中点击**导入数据**，根据引导上传我们虚构的阿里云百炼系列手机产品介绍：
    
    > 根据您上传的文档大小，阿里云百炼需要一定时间解析，通常占用1~6分钟，请您耐心等待。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5603325471/p944474.png)
    
2.  **创建知识库：**进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，点击**立即开通并创建**（首次使用）或**创建知识库**。选择**创建**标准版，填写**知识库名称**，其余设置可保持默认，点击**下一步**，选择刚才上传的文档，其他参数保持默认即可。后续大模型回答时可以检索参考知识库中的文档。
    
    > 选择向量存储类型时，如果您希望集中存储、灵活管理多个应用的向量数据，可选择**ADB-PG**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5301724671/p944483.png)
    
3.  **引用知识：**完成知识库的创建后，访问[应用管理](https://bailian.console.aliyun.com/?&tab=app#/app-center)页面，选择之前创建的应用。添加目标知识库，调用方式选择**必定调用**。测试验证符合预期后点击**发布**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9805168571/p944485.png)
    

### 4.2 检验效果

有了参考知识，AI 智能客服就能准确回答关于您公司的商品的问题了。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9763691271/p825768.png)

## 总结

通过前面的学习，您已经能搭建一个大模型 RAG 应用，并且将其以 AI 智能客服的形式添加到微信公众号中来应对客户咨询，整个过程仅需 0 元（免费试用额度内） 10 分钟。

### **应用于生产环境**

在正式的将 AI 智能客服引入到您的生产环境之前，建议您了解如下信息：

#### **应用评测**

建议在正式上线 AI 智能客服前，组织业务人员一起参与[人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)，确保大模型应用的回答效果符合预期。

### 持续改进

#### **大模型课程**

系统体验的改进优化永远没有终点，您可以考虑学习并通过[阿里云大模型 ACA 认证](https://edu.aliyun.com/certification/aca13)，该认证配套的免费课程能帮助您进一步了解大模型的能力和应用场景，以及如何优化大模型的应用效果。

## **常见问题**

### **公众号开启服务器配置后，自定义菜单无法使用怎么办？**

当您在公众号后台开启服务器配置后，因为微信公众号的限制，您之前配置的自定义菜单会因为冲突而关闭。如果您未完成微信认证，则无法同时开启服务器配置和自定义菜单。如果您是服务号或订阅号完成了微信认证，这时您可以参考如下步骤通过接口配置自定义菜单：

1\. 获取access\_token。您可以参考[获取 access\_token 文档](https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html)。通过访问下面的微信接口，获取access\_token。您可以访问[微信公众号后台](https://mp.weixin.qq.com/)，在左侧菜单选择**设置与开发** > **基本配置**。获取 AppID 和 AppSecret，并替换下面的`您的AppID`与`您的AppSecret`。

```
curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=您的AppID&secret=您的AppSecret"
```

2\. 调用菜单接口。你可以参考[创建菜单文档](https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Creating_Custom-Defined_Menu.html)，通过执行下面的代码，替换代码中`ACCESS_TOKEN`，并设定你需要的菜单数据，创建自定义的菜单。

```
curl "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN" \
--header "Content-Type: application/json" \
--data '{
     "button":[
     {	
          "type":"click",
          "name":"首页",
          "key":"home"
      },
      {
           "name":"菜单",
           "sub_button":[
           {	
               "type":"view",
               "name":"文档",
               "url":"https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio"
            }]
       }]
 }'
```

### **配置完成后，与公众号对话没有反应，如何排查问题？**

如果您是在 AppFlow 控制台点击**运行一次**进行测试时没有返回内容，是因为**运行一次**功能未包含内容输入，所以会报错。如果您是在微信与微信公众号对话时，没有返回内容，可以按照以下步骤进行排查：

1.  访问[AppFlow控制台](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/manage)，在表格操作列点击**运行日志**，跳转到执行日志页面查看日志。![2024-08-29\_16-54-56](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7242394271/p842656.png)
    
2.  在执行日志页面，点击**详情**查看错误日志详情。查看运行失败的步骤，通过失败信息分析原因。
    
    ![2024-08-29\_16-56-46](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7242394271/p842659.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7242394271/p842661.png)
    

常见的原因有：

-   百炼应用 Id 配置错误，应用 Id 未正确配置百炼应用 Id 或配置时存在前后空格。应用 Id 可在[阿里云百炼控制台我的应用](https://bailian.console.aliyun.com/#/app-center)查看并和配置比对。
    
-   微信公众号未完成认证，但采用了已完成认证的工作流。需要重新配置工作流，选择没有认证的公众号对应的工作流。
    
-   微信公众号凭证配置错误，可在[AppFlow控制台连接凭证](https://appflow.console.aliyun.com/vendor/cn-hangzhou/connector/user/auth/manage)页面，查看微信公众号配置，与[微信公众号后台](https://mp.weixin.qq.com/)进行比对。
    
-   微信公众号未配置白名单 IP。可在[AppFlow控制台连接凭证](https://appflow.console.aliyun.com/vendor/cn-hangzhou/connector/user/auth/manage)页面，查看微信公众号配置，获取白名单 IP。
    
-   微信公众号未完成认证，阿里云百炼应用回答超过 5 秒，导致触发微信限制，未能成功回复。建议完成微信认证，使用已经完成认证的工作流。如果无法完成认证，可以在阿里云百炼应用 prompt 中添加“请总是给出简短的回答，不要讲太多。”或将阿里云百炼应用的模型选择千问-Turbo来提升模型回复速度，但此方法会降低模型回答效果。
    

### **记录 AI 助理对话日志**

如果您想要记录 AI 助理对话日志并进行分析，您可以参考如下内容在 Appflow 中添加日志节点，将对话内容记录在阿里云日志服务中。

1.  访问[AppFlow控制台](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/manage)，在表格操作列点击**详情**，在详情页面右上角点击**创建新版本**。![2024-10-08\_17-48-33](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p855970.png)
    
2.  在编辑页面阿里云百炼步骤之后，点击**+**添加新的步骤。**行业类型**选择**阿里云**，**公共连接器**选择**SLS日志云服务**。![2024-10-08\_17-51-32](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p855976.png)![2024-10-08\_17-52-43](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p855977.png)
    
3.  选择执行动作**写入日志**，点击**保存，进入下一步**。![2024-10-09\_10-22-08](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856039.png)
    
4.  点击**添加新凭证**。在创建凭证对话框，根据表单填入信息，完成角色创建和授权。创建完成后，选择凭证，并点击**保存，进入下一步**。![2024-10-09\_10-25-29](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856043.png)![2024-10-09\_10-27-29](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856049.png)
    
5.  选择地域、Project 和 Logstore。填入所需的日志信息，左侧输入框是日志Key，直接输入，右侧是日志Value，通过插入变量获取上下文中信息。
    
    1.  如果您已经创建过用于存储 AI 助手日志的阿里云日志服务的Project和Logstore，则可以直接使用，如果没有创建过，可以参考[创建Project和Logstore](https://help.aliyun.com/zh/sls/getting-started#section-2l7-ol2-zro)创建。创建完成后无需接入日志，进入Logstore详情页面，在页面右上角点击开启索引，使用默认的全文索引即可。开启索引后才可以在日志服务进行在线日志查询和分析。![2024-10-09\_10-36-53](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856063.png)![2024-10-09\_10-38-45](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7255448271/p856067.png)
        
    2.  选择地域、Project 和 Logstore。填入所需的日志信息，左侧输入框是日志Key，直接输入，右侧是日志Value，通过插入变量获取上下文中信息。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856069.png)
        
6.  保存并发布连接流版本。![2024-10-09\_11-02-12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856082.png)
    
7.  进行对话测试，并查看日志。![2024-10-09\_11-35-40](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1868712371/p856122.png)
    

### 微信报错“**当前填写的URL存在严重安全风险，无法设置”如何解决**

当您在微信公众号后台配置服务器配置时，报错提示“当前填写的URL存在严重安全风险，无法设置”时，您可以采用最新的服务商授权方式重新[创建微信公众号连接流](#3bea46ab0defc)。如果您不想要使用服务商方式，也可以参考下面的方式绑定自有域名。

如果您的域名已在阿里云备案，您可以[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)，联系我们客服人员，提供连接流 ID、自定义域名，帮您配置并使用您企业的自有域名。然后您需要为自定义域名配置CNAME解析到连接流的**WebhookUrl**。

如果您的域名没有在阿里云备案，您可以在服务器配置中配置URL为您自有的域名，并在您自有域名对外提供服务的Nginx上配置转发规则，将请求转发到连接流的**WebhookUrl**。

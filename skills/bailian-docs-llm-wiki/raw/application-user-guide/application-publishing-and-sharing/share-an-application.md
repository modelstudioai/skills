# 分享智能体应用

阿里云百炼支持将已创建的应用以多种方式分享或发布至不同平台，便于将 AI 能力集成到具体业务中。本文以智能体应用为例，介绍如何将其分享为网页、集成至钉钉和微信、发布为可复用组件，以及通过音视频与应用实时互动。

## **前提条件**

已有构建好且已发布的智能体应用。具体操作请参考[创建智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。

## 分享或发布百炼应用

1.  访问百炼控制台的**[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)**页面，单击目标智能体应用卡片区域的**发布**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8335990571/p979170.png)
    
2.  **智能体应用**支持以下五种分享或发布方式。
    
    -   [方式一：通过官方网页版分享](#1bd3927a2fxvh)
        
    -   [方式二：通过魔笔分享渠道分享](#1977853bf2clt)
        
    -   [方式三：通过钉钉发布百炼应用](#8778cb4490l2i)
        
    -   [方式四：通过微信发布百炼应用](#763832277bxo6)
        
    -   [方式五：发布应用为组件](#57013457c3qe7)
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000804.png)
    

### **通过****官方网页版****或****UI 应用****分享应用**

**说明**

**访问共享应用权限说明**

-   **谁能访问？** 应用创建者（主账号）、RAM用户和持有链接的其他阿里云用户。
    
-   **计费：** 所有通过分享链接产生的费用，由应用创建者UID账号承担。
    

1.  #### **官方网页版**
    
    > 当前官方网页版分享只支持**智能体应用**，不支持**工作流应用。**
    
    1.  单击**官方网页版**右侧的**创建**可部署网页版应用，默认有效期为 7 天。
        
    2.  如需统计网页版应用消耗的 Token 数量，可以单击**应用观测**开通相关服务，开通后单击**启用应用观测**。
        
        > **启用应用观测**后可以在**应用观测**页面**关闭观测**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0527654571/p994338.png)
        
    3.  单击右侧的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0527654571/p994511.png)图标复制应用网页版链接，可以按需将链接分享给其他用户，持有该链接的阿里云用户均可访问此应用。
        
    4.  点击**网页下线** > **确认下线**，即可停止该应用网页版的服务。
        
2.  #### **魔笔分享渠道**
    
    1.  单击**UI 应用**右侧的**立即查看**跳转到**UI设计器**界面。
        
    2.  参考[UI设计](https://help.aliyun.com/zh/model-studio/ui-designer#d62913bf8dcza)，进行相关应用界面的编辑与发布。
        
    3.  访问百炼控制台的[UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui)页面，鼠标悬停于已发布的UI上，单击**环境部署**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7508903571/p983429.png)
        
    4.  可以将**应用地址**分享给其他用户，持有该链接的阿里云用户均可访问此应用。单击**下线**可以停止该应用服务。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0527654571/p994604.png)
        

### **通过**钉钉**发布应用**

1.  单击智能体应用的**发布平台**页签，单击**钉钉机器人**卡片右侧的**请先授权**。
    
    > 如果已经授权，请直接跳转至步骤3操作。
    
    ![钉钉](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0527654571/p994537.png)
    
2.  在**授权**对话框中，选中**勾选同意上述条款**后，单击**确认授权**。
    
    **重要**
    
    如您是首次在百炼平台上创建微信或钉钉渠道的应用，您需要授权阿里云计算有限公司提供的计算巢AppFlow为您提供自动化应用集成服务，包括如下两项授权：
    
    -   授权SLR（服务关联角色，Service Linked Role）关联计算巢AppFlow。
        
    -   授权API-KEY加密传输给计算巢AppFlow用以调用百炼平台的应用。
        
    
3.  单击**钉钉机器人**卡片右侧的**创建**，在**配置钉钉**面板的**选择API KEY**配置向导页，选中目标API KEY，单击**下一步**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877401.png)
    

> 如果没有可选API KEY，请单击**创建API Key**，完成创建后再选择。也可以单击**管理API Key**，跳转至**我的API-KEY**页面，对API-KEY进行管理。

1.  在**配置钉钉**面板的**配置信息**向导页，完成**钉钉模版ID**、**钉钉Client ID**和**钉钉Client Secret**配置后，单击**确认**。
    
    关于钉钉模板 ID、钉钉 Client ID 和钉钉 Client Secret 的获取，请参见以下步骤：
    
    接下来您需要在您的组织中创建一个简单的钉钉应用，作为 AI 助手回答用户问题。
    
    **重要**
    
    创建钉钉应用需要您的钉钉账号有开发者权限。您可以联系您的组织管理员获取钉钉开放平台的开发权限，具体操作请参见[获取开发者权限](https://open.dingtalk.com/document/orgapp/obtain-developer-permissions)。
    
    **步骤一：创建应用**
    
    1.  访问[钉钉开放平台](https://open-dev.dingtalk.com/)。
        
        -   如果是第一次创建钉钉应用，请点击**应用开发指引** > **创建**。
            
        -   如果已经创建过应用，请点击**快速构建 AI 应用** > **立即开始**。
            
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830053.png)
        
    2.  在左侧导航栏中，点击**钉钉应用**，在页面右上角点击**创建应用**。![11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830054.png)
        
    3.  填写**应用名称**和**应用描述**，可以选择上传**应用图标**，点击**保存**。![12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830055.png)
        
    
    **步骤二：获取应用 Client ID 和 Client Secret**
    
    在左侧菜单选择**凭证与基础信息**，复制 Client ID 和 Client Secret，用于下一步创建连接流。
    
    ![21](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830138.png)
    
    **步骤三：创建消息卡片，获取卡片模板 ID**
    
    钉钉机器人通过卡片消息支持流式返回结果，您需要创建卡片模板供消息发送使用。
    
    1.  访问[卡片平台](https://open-dev.dingtalk.com/fe/card)，点击**新建模板**。![29](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830244.png)
        
    2.  在创建模板输入框，填入模板信息，点击创建。
        
        -   **卡片类型**：选择**消息卡片**
            
        -   **卡片模板场景**：选择**AI卡片**。
            
        -   **关联应用**：需关联[步骤一：创建应用](#6dee67ce67x4l)中创建的应用**。**
            
        -   **从模板创建**：无需选择预设模板。
            
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830272.png)
        
    3.  在模拟编辑页面，无需修改任何配置，**保存**并**发布**模板，点击**返回**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830465.png)
        
    4.  在左侧菜单中，点击**模板列表**，复制**模板 ID**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830274.png)
        
    
    **步骤四：授予应用发送卡片消息权限**
    
    创建卡片后，需授予应用发送卡片消息的权限。
    
    1.  访问[钉钉应用列表](https://open-dev.dingtalk.com/fe/app)。点击刚才创建的应用名称，以进入详情页面。
        
    2.  在左侧菜单选择**权限管理**。在左侧搜索框分别输入`Card.Streaming.Write`和`Card.Instance.Write`，并在操作列点击**申请权限**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830282.png)
        
    3.  获取权限后，请将模板 ID、Client ID、Client Secret 填回百炼应用的发布配置窗口，即可发布百炼应用到钉钉应用。
        
    
2.  钉钉应用创建完成后，在百炼应用**发布渠道**页签，复制**回调地址**。您可以按需将**回调地址**分享给目标用户。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877459.png)
    
    获取到**回调地址**的用户，可以为钉钉应用配置机器人，添加到群聊中以回答用户问题。
    
    配置钉钉机器人
    
    **步骤一：配置钉钉机器人**
    
    1.  访问[钉钉应用列表](https://open-dev.dingtalk.com/fe/app)。找到刚才创建的应用，点击应用名称进入详情页面。
        
    2.  在**添加应用能力**页面，找到机器人卡片，点击**添加**。![13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830056.png)
        
    3.  打开**机器人配置**开关。
        
        -   **机器人名称**、**机器人图标**、**机器人简介**、**机器人描述**、**机器人消息预览图**：请根据页面描述自行填写。
            
        -   **消息接收模式**：请选择**HTTP模式**。目前AppFlow仅支持HTTP模式，选择Stream模式会导致无法返回消息。
            
        -   **消息接收地址**：粘贴从百炼发布渠道获取的**回调地址**。
            
        -   点击**发布**。
            
        
        ![30](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830299.png)
        
    
    **步骤二：发布应用版本**
    
    应用创建完成后，如果需要将应用供企业内其他用户使用，需发布一个版本。
    
    1.  点击**应用开发**，在**钉钉应用**页面，点击刚才创建的应用。![8](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830050.png)
        
    2.  在左侧菜单栏，点击**版本管理与发布**。在右上角点击**创建新版本**。在版本详情页，输入**应用版本号**和**版本描述**信息，选择合适的**应用可见范围**，完成后点击**保存**。并在弹窗中点击**直接发布**。![10](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830052.png)
        
    
    **步骤三：测试机器人**
    
    你可以创建群聊或在已有群聊中添加机器人，并与机器人对话，查看效果。
    
    1.  在钉钉**群管理**中添加机器人​。
        
        进入钉钉群**群设置**页面，点击**机器人**卡片区域，在**机器人管理**页面，点击**添加机器人**。在**添加机器人**的**搜索**文本框中输入目标机器人名称，并选中要添加的机器人。点击**添加**，完成后再点击**完成添加**。![14](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830057.png)
        
    2.  在钉钉群中@机器人，进行交流互动。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830339.png)
        
    

### 通过微信发布应用

> 如果您已在创建钉钉机器人的步骤授权过，则无需再次授权。具体授权流程，请参见[通过钉钉发布应用](#8778cb4490l2i)的相应步骤。

1.  在智能体应用的**发布平台**页签，单击**微信公众号**卡片右侧的**创建**。
    
2.  在**配置微信**面板的**选择API KEY**配置向导页，选中目标API KEY，单击**下一步**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877401.png)
    
    > 如果没有可选API KEY，您也可以单击**创建API Key**，完成创建后再选择。您也可以单击**管理API Key**，跳转至**我的API-KEY**页面，对API-KEY进行管理。
    
3.  在**配置微信**面板的**配置信息**向导页，选择目标微信凭据，完成后单击**确认**。
    
    如果没有微信凭证可选项，您可以单击**前往新建**。具体操作，请参见以下步骤。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877461.png)
    
    在对话框中，输入**开发者ID（AppID）**，完成后单击**授权**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877465.png)
    
    **开发者ID（AppID）**的获取方法：访问[微信公众号后台](https://mp.weixin.qq.com/)，在左侧菜单选择**设置与开发** > **开发接口管理**。选择基本配置页签，获取 AppID。![2024-11-07\_16-27-30](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877464.png)
    
4.  微信公众号AI机器人创建完成后，在**发布渠道**页签，将鼠标悬浮至**微信公众号**右侧的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877475.png)图标，您可以按需将二维码分享给目标用户。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3719962371/p877474.png)
    

### **发布应用为组件**

1.  单击智能体应用的**发布渠道**页签，鼠标悬停于**组件**上，单击右侧的**创建**。
    
2.  配置组件信息，单击**确定发布**。
    
    **参数名称**
    
    **参数说明**
    
    **组件名称**
    
    自定义填写，建议使用具有实际意义的名称。例如，天气分析智能体。
    
    **组件描述**
    
    对组件的功能和使用场景的简要说明。请使用自然语言进行描述。例如，用于分析城市的天气信息。
    
    组件发布后，在**智能体应用**中引用该组件时，大模型会根据组件描述和上下文，自动判断是否调用。在**工作流应用**中引用该组件时，组件描述仅用于说明组件功能，不影响工作流的运行。
    
    **输入信息**
    
    **别名**
    
    为避免参数名称相同，您需要给参数起别名。调用组件时，调用者只能看到参数的别名。
    
    **参数描述**
    
    参数的内容描述。
    
    -   在智能体中引用该组件时，且传参方式为**模型识别**时，大模型会根据参数描述，自动填入参数内容。
        
    -   其他情况下，该描述仅起到说明作用。
        
    
    **是否必填**
    
    按实际业务填写。
    
    **是否可见**
    
    组件是否对外透出此参数，用于隐藏不需要的参数。例如，组件使用了文本模型，就需要隐藏图像输入参数。
    
    **传参方式**
    
    **业务透传**：
    
    -   在智能体中引用该组件时，由组件的使用者提供。
        
    -   在工作流中引用该组件时，由上游节点提供。
        
    
    **模型识别**：
    
    -   在智能体中引用该组件时，由大模型根据参数描述，从上下文中自动推断并填充。
        
    -   在工作流中引用该组件时，即使参数的**传参方式**设置为**模型识别**，应用也不会自动推断参数值。您**必须**像**业务透传**一样，从上游节点明确地为该参数提供输入值。
        
    
    **默认值**
    
    按实际业务填写。
    
3.  组件发布后，可在智能体应用或工作流应用中引用组件。
    
    **说明**
    
    -   **避免嵌套调用**：对于 A 调用 B，B 调用 A 的情况，应用会进入重复调用状态，导致功能不可用。
        
    -   **避免多级调用**：对于 A 调用 B，B 调用 C 的情况，应用有最长运行时间限制，多级调用容易产生超时错误。
        
    
    在智能体应用中引用组件
    
    1.  在阿里云百炼的[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面，创建[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)时，在**技能**中选择组件。
        
        仅支持选择已发布的智能体组件。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0527654571/p965003.png)
        
    2.  配置完成后，输入组件功能相关的问题测试效果。
        
        > 如果引用的组件包含需要**业务透传**的参数，您可以在测试时手动填入**入参变量配置**，或者在 API 调用时通过 `biz_param`参数传入。
        
    
    在工作流应用中引用组件
    
    1.  在阿里云百炼的[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面，创建[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)时，将**组件**节点拖入画布，再选择组件。
        
        支持选择已发布的智能体组件或工作流组件。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0527654571/p965002.png)
        
    2.  配置完成后，输入组件功能相关的问题测试效果。
        
    

### 通过**音视频实时互动**发布应用

**说明**

仅支持百炼的图文对话类应用（含智能体应用和工作流应用）

1.  在智能体应用的**AI实时互动**页签，单击**语音互动/视频互动**，单击页面右侧的**去配置**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000827.png)
    
2.  在**查看API-KEY**配置向导页，选中目标API KEY，单击**确定**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0765846371/p903087.png)
    
3.  点击右上角![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000851.png)，生成临时体验二维码，通过手机微信/钉钉/浏览器扫码体验交互效果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000844.png)
    
4.  测试完毕后，点击**发布**\>**确认发布**。发布后，进入**发布渠道**，完成智能媒体服务开通和 SLR 授权后，创建互动智能体。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000853.png)
    
    音视频实时互动应用支持两种发布渠道：
    
    1.  H5/APP 扫码：点击**生成分享链接**，**设置Token有效时间**，点击**确认**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000857.png)
        
    2.  SDK 集成：点击**SDK集成**，可以选择**快速集成**快速部署和运行音视频互动服务，也可以根据业务需求选择**开发集成**进一步扩展更多高级功能。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3275016571/p1000875.png)

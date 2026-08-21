# UI设计器

阿里云百炼UI设计器提供可视化的应用开发环境，支持通过拖放组件构建应用界面，并发布为网页UI应用。

## 产品优势

阿里云百炼的UI设计器集成了阿里云[多端低代码开发平台魔笔](https://help.aliyun.com/zh/mobi/what-is-mobi)的能力，具备以下核心优势：

-   **低代码：**UI 设计器提供可视化编辑器，支持通过拖放组件、配置路由和布局，快速构建页面。
    
-   **服务集成：**支持集成百炼智能体、大模型、数据库和 HTTP 服务等多种资源，灵活扩展应用能力。
    
-   **权限管理：**内置测试账号体系，支持钉钉、企业微信等一键登录。兼容 OIDC、OAuth 2.0 等标准协议，并可通过权限组管理访问权限。
    
-   **一键发布：**默认支持免费发布至开发环境，通过内置域名即可访问。生产环境发布支持绑定自定义域名。
    

## **准备工作**

集成AI对话能力，需要创建并发布百炼[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)或[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，并获取用于调用阿里云百炼服务的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。

**重要**

百炼应用、API Key和UI设计需要归属于**同一**[**业务空间**](https://help.aliyun.com/zh/model-studio/use-workspace)**。**

## 从已有**应用发布为 UI**

1.  进入应用的发布渠道页面，选择**UI应用**，单击**创建**。
    
2.  系统会根据已有应用自动填充基础信息，包括应用标题及应用描述、百炼API-KEY、百炼智能体、头像、预设问题等，可按需修改。确认无误后，单击**立即创建**。
    
3.  创建完成后，单击链接即可体验网页 UI 应用，链接有效期为24小时。如果需要调整界面，可单击**编辑 UI** 进行修改，详情可参考[通过UI设计器创建UI应用](#87545aa6facnz)。
    
    **说明**
    
    对于工作流应用，如果配置了文件类型的自定义参数，需要在UI设计器中编辑并指定自定义参数`{{{file_name:files[0]}}}`（需要把`file_name`替换为实际的变量名），才能使应用正确读取用户在UI界面上传的文件。
    
    ![截屏2026-04-01 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4563305771/p1064598.png)
    

## **通过UI设计器创建UI应用**

### **步骤一：创建UI**

创建UI旨在生成初始页面结构，作为后续添加组件和布局设计的基础。

1.  **选择UI模板**
    
    前往[UI设计器页面](https://bailian.console.aliyun.com/?tab=app#/app-ui)，单击**创建UI**，在左侧选择UI模板。
    
    阿里云百炼平台提供四种预置模板（智能出行助手、智能体门户、AI基础对话、企业AI知识库Lite）及空白模板。预置模板包含预设组件和界面，支持直接修改或二次开发，空白模板则需要从零开始设计。
    
    **模板简介**
    
    **模板名称**
    
    **模板说明**
    
    **支持终端**
    
    **模板预览**
    
    空白模板
    
    没有任何样式，需要从零开始设计。
    
    PC、H5
    
    无预设组件，提供空白画布
    
    智能出行助手
    
    AI可基于自然语言对话生成个性化行程规划，并动态展示UI界面。
    
    PC
    
    ![智能出行助手](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009211.png)
    
    智能体门户
    
    构建企业专属的智能体门户，实现多智能体的统一管理与快速上架。
    
    PC
    
    ![智能体门户](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009212.png)
    
    AI基础对话
    
    基础AI聊天模板，可帮助快速上手UI设计器，搭建AI聊天会话应用。
    
    PC
    
    ![AI基础对话](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009213.png)
    
    企业AI知识库Lite
    
    AI知识管理工具，支持智能对话（PC/移动端）和数据分析能力。
    
    PC、H5
    
    ![企业AI知识库Lite](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009214.png)
    
    以下以**企业AI知识库Lite**模板为例进行说明。
    
2.  **填写基础信息**
    
    -   **应用名称**及**应用描述**：自定义填写，建议填写有意义的名称与描述，以便识别用途。
        
    -   **百炼API-KEY**：选择百炼[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
        
    -   **百炼智能体****：**选择已发布的百炼应用。
        
    -   **上传图标**（可选）：上传自有图标。
        
    
    > 如果无法选择API Key及百炼应用，请确认您创建UI的业务空间是否与所需的API Key及应用位于同一业务空间。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5961492671/p1026156.png)
    
3.  **配置数据库表映射**
    
    部分UI模板自带用于存储运行时数据的数据库表（如`kb_chat_list`会话记录），其结构固定且无法修改，可单击**模板中数据库表名称**列的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1998405571/p996216.png)图标查看。
    
    配置映射时，指定库表名称即可。若该表在[数据库](https://bailian.console.aliyun.com/?tab=app#/data-center/mobi/database)中不存在，系统将按模板结构自动创建；若存在同名表，则直接使用并保留已有数据。
    
    **注意**：使用已有表时，务必确保其结构与模板内置表**完全一致**，否则可能导致运行时错误。
    
    UI创建完成后，可在[数据库](https://bailian.console.aliyun.com/?tab=app#/data-center/mobi/database)中查看表详情。若表中无数据，通常是因为没有进行相关操作。例如，`kb_chat_list` 表在用户发起问答后才会生成记录。
    
    ![配置数据库表映射](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009228.jpg)
    

### **步骤二：编辑UI**

**通过拖放组件来搭建页面**。左侧的[组件面板](https://help.aliyun.com/zh/mobi/low-code-development-designer-overview)中提供各类UI元素，包括按钮、输入框、展示、导航栏等。将所需[页面组件](https://help.aliyun.com/zh/mobi/components/)添加到页面中，根据业务需求调整其位置和样式，完成[页面搭建](https://help.aliyun.com/zh/mobi/page-build/)。

如果需要使用自定义的图片或文件，可在搭建过程中随时上传，或可提前在[文件](https://bailian.console.aliyun.com/?tab=app#/data-center/mobi/files)页面上传。上传的文件将保存在[文件](https://bailian.console.aliyun.com/?tab=app#/data-center/mobi/files)页面，详情请参见[UI应用数据](https://help.aliyun.com/zh/model-studio/ui-application-data)。

### **步骤三：发布与分享**

1.  UI搭建完成后，可通过设计器右上角的**发布**按钮将UI发布到**开发环境**或**生产环境**，发布后单击**访问应用**即可体验搭建的UI。
    
    ![发布UI](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009231.png)
    
    ![5](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009461.webp)
    
    **环境对比**
    
    **开发环境**
    
    **生产环境**
    
    **环境说明**
    
    用于开发、调试和验证。
    
    部署了终端用户实际使用的软件版本的环境
    
    **访问方式**
    
    通过平台提供的域名访问
    
    支持通过平台提供的域名访问和设置自定义的访问地址
    
    **有效期**
    
    **发布的 UI 24 小时后失效**，需要重新发布才能访问
    
    发布的 UI 长期有效
    
    **是否收费**
    
    免费
    
    需订阅付费套餐，同时需要[配置域名](https://help.aliyun.com/zh/mobi/environment-and-domain)，详情请参见[产品计费说明](https://help.aliyun.com/zh/mobi/product-billing-description)
    
2.  在[UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui)页面，悬停于已发布的UI，单击**环境部署**。
    
    ![UI设计器](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009238.webp)
    
3.  **应用地址**可分享给其他用户，默认持有链接的阿里云用户均可访问。单击**下线**可以停止该应用服务。
    
    ![应用地址](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009240.webp)
    

### **配置访问权限（可选）**

UI应用发布后，默认持有链接的阿里云用户可访问。也可通过设定访问权限，允许匿名用户访问，在会话页进行知识问答，同时限制其访问管理后台。

1.  在UI设计器的左下角单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7508903571/p983695.png)图标，在**登录配置**中打开**允许匿名访问**开关，并单击**匿名用户权限组配置**。
    
    ![匿名访问权限配置](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009235.webp)
    
2.  选择环境，在**应用访问权限**页签中，勾选已经搭建的UI，单击**权限设置**。
    
    ![匿名访问权限配置权限组](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p1009236.webp)
    
3.  选择对用户开放的页面，单击**确定**。
    
4.  退出管理员账号，打开UI地址，验证权限配置是否生效。
    

## 计费说明

UI设计器功能本身不计费，但使用过程中可能涉及以下费用：

-   [模型调用费用](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#9cd9788102v3r)：进行AI对话会产生模型调用费用，详情请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。
    
    > 阿里云百炼提供[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)，额度消耗完后按 Token 的使用量来计费。
    
-   [UI应用数据](https://help.aliyun.com/zh/model-studio/ui-application-data)：UI设计过程中会使用配额资源，例如文件存储和内置数据库。阿里云百炼默认提供1GB的免费文件存储和0.3GB的免费数据库容量，超出免费额度或套餐配额的资源使用量将[按量计费](https://help.aliyun.com/zh/mobi/product-billing-description#f35df080df0p4)。
    
-   [订阅服务套餐](https://common-buy.aliyun.com/?spm=a2c4g.11186623.0.0.e3343f97bXUIxA&commodityCode=miniappdev_Mobi2Pre_public_cn)：将应用发布到生产环境，需要订阅团队版（或更高级别）套餐，涉及月度费用，具体请参见[套餐规格](https://help.aliyun.com/zh/mobi/product-billing-description#110ca915af9kf)。
    

## 实践教程

更多UI设计的使用场景，包括创建AI知识库、智能客服、在应用中增加 AI 助手等，请参见[实践教程](https://help.aliyun.com/zh/mobi/practice-tutorial/)。

## 常见问题

### **在**[**UI设计器**](https://bailian.console.aliyun.com/?tab=app#/app-ui)**页面编辑或设置UI时，提示“当前应用正在编辑中”应该怎么处理？**

![当前应用正在编辑中](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1947958571/p983433.png)

这可能是因为当前UI已在其他窗口中打开，关闭后即可重新编辑，也可点击**获取编辑权限**强制关闭其他已打开窗口。

# 获取API Key

使用阿里云百炼的大模型或应用前，请先获取API Key作为鉴权凭证。

## **一、获取API Key**

**重要**

需使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)，或具备`管理员`或`API-Key`[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)的[子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作。

## 华北2（北京）地域

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)首页，在页面右上角选择**华北2（北京）**地域，进入[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)页面，单击**创建API Key**。
    
2.  在弹窗中配置以下信息，并单击**确定**：
    
    -   **归属业务空间**：建议选择默认业务空间。
        
    -   **权限**：建议选择**全部**，若有更精细的权限控制需求，可以选择**自定义**来控制使用 API Key 的 IP 白名单。
        
    
    **如何选择 API Key 的权限配置？**
    
    阿里云百炼提供两种类型的权限配置，请根据实际需求进行选择：
    
    -   **全部**：授予该 API Key 调用所有模型与应用的权限。
        
    -   **自定义**：可配置**IP 访问白名单**。该配置不能为空。
        
        > 默认设置为：IPv4 （`0.0.0.0/0`）和 IPv6 （`::/0`）全部放通。
        
        仅允许名单内的 IP 使用该 API Key 发起调用。支持设置最多 **20** 个 IPv4、IPv6 的地址或网段。
        
    
3.  点击API Key旁的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8412544571/p994217.png)图标获取该API Key。
    
    > 主账号可以查看全部API Key，子账号仅能查看自己创建的API Key。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6147424771/p1061684.png)
    

## 新加坡、美国（弗吉尼亚）地域

1.  前往[阿里云百炼控制台](https://modelstudio.console.aliyun.com/ap-southeast-1)首页，在页面右上角切换到目标地域（如**新加坡**），进入**工作台**页签，然后在左侧导航栏中选择 **API Key** 进入API Key管理页面，单击**创建API Key**。
    
2.  在弹窗中配置以下信息，并单击**确定**：
    
    -   **归属业务空间**：建议选择默认业务空间。
        
    -   **描述**：输入描述信息，方便后续识别该API Key的用途。
        
3.  创建成功后，弹窗会显示完整的API Key。请立即复制并妥善保存，关闭弹窗后将无法再次查看完整的API Key。
    
4.  在API Key列表中，点击API Key旁的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8412544571/p994217.png)图标可复制脱敏后的API Key。
    
    > 主账号可以查看全部API Key，子账号仅能查看自己创建的API Key。
    
    ![2026-02-11\_11-56-27](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0009970771/p1054137.jpg)
    

## 德国（法兰克福）地域

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/eu-central-1)首页，在页面右上角切换到目标地域（**德国（法兰克福）**），进入**工作台**页签，在左侧导航栏中选择**API Key**进入API Key管理页面，单击**创建API Key**。
    
2.  在弹窗中配置以下信息，并单击**确定**：
    
    -   **归属业务空间**：建议选择默认业务空间。
        
    -   **描述**：输入描述信息，方便后续识别该API Key的用途。
        
3.  创建成功后，弹窗会显示完整的API Key。请立即复制或下载保存，注意妥善保管，任何获取到该密钥的人都能以您的身份发起服务请求并产生费用。关闭弹窗后将**无法再次查看或复制**明文API Key。如果丢失，请重置或创建新的密钥。
    
    > 主账号可以查看全部API Key，子账号仅能查看自己创建的API Key。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2663279771/p1074937.png)
    

**何时选择其他归属账号或业务空间？**

如果您有团队协作或成本分摊需求，可以了解以下概念：

-   **归属业务空间**：用于隔离不同项目或团队的资源和权限。若需管控某类用户可调用的模型，或对模型调用的费用进行分账，请创建/选择列表中的子业务空间。
    

详情请参见[API-Key 权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f2704153a055r)以及[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。

## **二、使用API Key**

**说明**

[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)应使用专属 API Key（格式：`sk-sp-xxxxx`），而非本文介绍的百炼通用 API Key（格式：`sk-xxxxx`）。获取 Coding Plan 专属 API Key 请参见[获取套餐专属 API Key 和 Base URL](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart#2782cf93b1w8h)。

-   **方式一：在**[**第三方工具**](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)**中调用模型**
    
    如果在Chatbox等工具或平台中调用模型，您可能需要输入三个信息：
    
    -   本文获取的API Key
        
    -   API Key所属地域的Base URL：
        
        -   **华北2（北京）**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
            
        -   **新加坡**：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
            
        -   **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
            
        -   **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`，调用时请将`WorkspaceId`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。
            
    -   模型名称，如qwen-plus
        

常用工具配置：[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)、[Cline](https://help.aliyun.com/zh/model-studio/cline)、[Claude Code](https://help.aliyun.com/zh/model-studio/claude-code)、[Dify](https://help.aliyun.com/zh/model-studio/dify)、[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)、[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)、[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)。

-   **方式二：通过代码调用模型**
    
    通过代码[首次调用千问API](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen)，建议[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，以避免硬编码在代码中导致泄露风险。
    

请勿以任何方式公开API Key，避免因未经授权的使用导致安全风险或资金损失。

## API Key权限说明

API Key的调用权限完全由其**归属业务空间**决定。**同一空间内的API Key权限相同**，无需为不同模型（如文生文、文生图、语音合成）创建不同的API Key。

-   **默认业务空间下的API Key：**可调用所有标准模型，以及默认业务空间内的[应用](https://help.aliyun.com/zh/model-studio/application-introduction)。
    
-   **子业务空间下的API Key：**可调用该子业务空间已获得[授权](https://help.aliyun.com/zh/model-studio/use-workspace#f2e68d7ba7ubk)的标准模型，以及该子业务空间内的应用。
    

**调用在阿里云百炼**[**调优后的模型**](https://help.aliyun.com/zh/model-studio/model-training-overview)**：**此类模型部署成功后，仅能用其所在业务空间的API Key调用，无需[授权](https://help.aliyun.com/zh/model-studio/use-workspace#f2e68d7ba7ubk)。

**说明**

目前仅[华北2（北京）地域](https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key)支持为 API Key 配置更精细的[权限控制](https://help.aliyun.com/zh/model-studio/permission-management-overview#c036858be2tpo)。

您可以在**创建API Key** 或点击已有 API Key 操作列的**编辑**时，将**权限**切换为**自定义**，即可配置：

-   **IP 访问白名单**：仅允许名单内的 IP 使用该 API Key 发起调用（支持 IPv4、IPv6 与网段）。
    

## **API Key时效性说明**

创建的API Key没有失效日期，手动删除后即失效。

若需为第三方应用或用户提供临时访问权限，或需严格控制敏感数据访问、删除等高风险操作，可[生成临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（有效期60秒），避免暴露长期有效的API Key，降低泄露风险。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

**Q：单个主账号下最多能创建多少个API Key？**

A：对于华北2（北京）、新加坡和德国（法兰克福）地域，每个主账号在每个地域最多可创建50个API Key。

对于美国（弗吉尼亚）地域，每个归属账号（包括主账号）最多可创建20个API Key。

**Q：RAM用户被删除后，其创建的API Key是否依然可用？**

A：在RAM控制台中[禁用或删除RAM用户](https://help.aliyun.com/zh/ram/user-guide/delete-a-ram-user)后，其创建的所有API Key均将失效，无法再用于模型调用。

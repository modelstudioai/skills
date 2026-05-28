# Qoder CN（原 Lingma）

Qoder CN（原 Lingma）是阿里云智能编码助手，提供独立 IDE，可以通过 Coding Plan 或 Token Plan 团队版接入阿里云百炼。

**说明**

Qoder CN 个人社区版和个人专业版均支持接入百炼，企业版不支持。

## **安装**

1.  前往 [Qoder CN 官网](https://lingma.aliyun.com/download)下载并安装 Qoder CN。
    
2.  初次启动后完成初始配置。
    
3.  在阿里云登录页面中，选择阿里云账号登录。
    

## **配置接入凭证**

1.  在界面右上角打开 Qoder CN 设置，选择**模型**，点击**添加**。
    
2.  模型配置信息如下：
    
    **配置项**
    
    **说明**
    
    提供商
    
    在下拉菜单中选择 阿里云百炼 - 国内
    
    类型
    
    根据计费方案选择 **Token Plan** 或 **Coding Plan**
    
    模型
    
    在下拉菜单中选择模型。仅支持文本生成模型。
    
    API Key
    
    填写对应方案的专属 API Key：
    
    -   Token Plan 团队版：[获取 API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)
        
    -   Coding Plan：[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)
        
    
3.  点击**添加**，通过校验后即可完成模型配置。
    
4.  在 Qoder CN 对话框中，选择对应模型即可开始使用。
    

## 了解更多

如需进一步了解 Qoder CN 的智能体、MCP、Skills 等扩展能力，请参考 [Qoder CN 官方文档](https://help.aliyun.com/zh/lingma/product-overview/introduction-of-lingma)。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
    

### 为什么在 Qoder CN 设置中找不到模型选项？

可能有以下原因：

-   **未完成登录**：需要先完成登录，才能进行对话和配置模型。
    
-   **当前版本不支持**：接入百炼需要 Qoder CN 个人社区版或个人专业版，企业版不支持。
    

### API Key 认证失败（HTTP 401）

请确认以下几点：

-   确认使用的是对应计费方案的专属 API Key。Token Plan 团队版和 Coding Plan 的 API Key 互不相通。
    
-   确认套餐未过期。
    
-   API Key 复制完整、无空格。如仍报错，可在对应管理页面重置 API Key。

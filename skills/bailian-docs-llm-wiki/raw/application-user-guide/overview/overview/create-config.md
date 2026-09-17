# 创建身份验证配置

两步向导：选择 App，填写凭证。含各字段的填写说明。

创建身份验证配置是一个两步向导：先选 App，再填这个 App 需要的凭证。

## 开始之前

准备好目标 App 的凭证。不同 App 需要的东西不一样，先对照下表确认手里有没有：

App

需要准备

Salesforce on Alibaba Cloud

组织域名、External Client App 的 Consumer Key 与 Consumer Secret

MaxCompute

无需凭证，只有可选的授权范围

语雀

语雀 API Key

凭证的具体获取路径见[OAuth 2.0 配置](raw/application-user-guide/overview/overview/oauth.md)与[API Key 配置](raw/application-user-guide/overview/overview/api-key.md)。

## 创建步骤

1.  **进入身份验证配置页面**：在控制台左侧导航单击 **身份验证配置**。首次进入时页面显示请先完成身份验证配置。单击 **创建身份验证配置**。
    
2.  **选择 App**：向导第一步是 **选择 App**，页面提示选择一套用于设置身份验证的工具包。
    
    列表里只显示需要身份验证配置的 App，每一项右侧标注它的身份验证方法：
    
    App
    
    身份验证方法
    
    Salesforce on Alibaba Cloud
    
    OAuth2
    
    语雀
    
    API Key
    
    MAX\_COMPUTE
    
    OAuth2
    
    选中目标 App，单击 **下一步**。
    
3.  **填写配置**：向导第二步是 **身份验证配置**。顶部三项是所有 App 共有的：
    
    字段
    
    是否必填
    
    说明
    
    连接的 App
    
    —
    
    只读，显示上一步选中的 App
    
    配置名称
    
    否
    
    区分同一 App 下的多个配置。建议写清用途，例如生产环境或测试环境
    
    身份验证方法
    
    —
    
    只读，由 App 决定，显示 OAuth 2.0 或 API Key
    
    下方是该 App 专属的凭证字段，各 App 不同，详见[OAuth 2.0 配置](raw/application-user-guide/overview/overview/oauth.md)与[API Key 配置](raw/application-user-guide/overview/overview/api-key.md)。
    
4.  **完成**：单击 **完成** 保存配置。需要修改上一步的选择时，单击 **上一步** 返回。
    
    保存后配置出现在 **身份验证配置** 列表中，可以在创建连接时选用。
    

## 从连接流程直接创建

不必先去身份验证配置页面。在 App 的连接对话框里：

1.  **打开连接对话框**：在 **Apps** 页面找到目标 App，单击 **连接**。
2.  **展开下拉框**：单击 **选择身份验证配置** 下拉框。当前 App 还没有配置时，下拉框内显示暂无配置，点击下方按钮创建。
3.  **跳转创建**：单击 **创建身份验证配置**，控制台会打开创建页面并预先选中当前 App 与它的身份验证方法，你只需要填凭证。

**说明**这条路径会新开一个页面。保存配置后回到 **Apps** 页面重新打开连接对话框，新建的配置就出现在下拉框里了。

## 用配置创建连接

有了身份验证配置之后，连接这些 App 只需要选一下：

1.  **打开连接对话框**：在 **Apps** 页面找到目标 App，单击 **连接**。
2.  **选择配置**：在 **选择身份验证配置** 下拉框中选中要用的配置。这是该对话框唯一的必填项。
3.  **确定**：单击 **确定**。OAuth 2.0 的 App 会跳转到对方系统完成登录与授权，授权成功后返回控制台。

连接建好后在 App 详情页的 **已连接的用户** 区域可以看到，管理方式见[连接的账户](raw/application-user-guide/overview/overview/connected-accounts.md)。

## 常见问题

现象

原因

处理

下拉框里没有想用的配置

配置属于另一个 App

身份验证配置与 App 绑定，需要为当前 App 单独建一个

完成按钮点不动

必填字段没填完

检查带星号的字段，凭证字段通常都是必填

保存后连接仍然失败

凭证填错或权限不足

核对凭证是否复制完整，以及对方系统里的应用是否已启用

**重要**第一次接触这套流程，用[语雀](raw/application-user-guide/overview/overview/yuque.md)练手最快，它只需要一个 API Key，不用去对方系统注册应用。

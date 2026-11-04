# Agent错误信息查询

所有Agent的错误码汇总参考。

## Agent接口错误

**网关code**

**控台code**

**message**

**说明**

Arrearage

BIL.UserArrears

User is in arrears.

用户处于欠费状态，请充值后使用。

InvalidParameter

Agent.InputTextFormatError

Agent Input text format error.

输入文本格式错误，解决请参考API文档中文本格式的规定。

InvalidParameter

Agent.InputDataIdIllegal

Agent Input dataId illegal.

输入dataId格式非法，需要输入合法的dataId。

InvalidParameter

Agent.InputDataIdSSRF

DataId broken access control.

输入dataId越权，请检查dataId是否为相应账号、相应应用的dataId。

InvalidParameter

Agent.ModelNotCompatibleWithAppId

Agent model not compatible with appId.

输入的模型与appId不兼容，请输入正确的appId或者模型参数。

InvalidParameter

Agent.InputScoreIllegal

Agent Input score illegal.

输入分数非法，请参考API文档中关于分数的格式规定。

InvalidParameter

Agent.InputTaskIllegal

Agent Input task illegal.

输入的task参数非法，请输入合法的taskId。

InvalidParameter

Agent.InputAppIdIllegal

Agent Input appId illegal.

输入appId非法，请输入合法的appId。

InvalidParameter

Agent.AppNotExist

Agent App not exist.

应用不存在，请输入API Key账号下相应的appId。

InvalidParameter

Agent.AppNotPublished

Agent App not published.

应用未发布，请发布后再进行调用。

InvalidParameter

Agent.InputInvalidDataId

Agent Input invalid dataId.

输入dataId来自百炼控制台，不允许sdk进行调用。

InvalidParameter

Agent.InputDataIdNotMatchAppOrModel

Agent Input dataId not match app or model.

输入dataId与应用或模型不匹配，请输入正确的dataId。

InvalidParameter

InvalidParameter

Invalid parameter. Please refer to the official documents.

无效参数建议检查文档。

InvalidParameter

VerifyFailed

Verify callback failed.

验证回调url失败，请填写合理的http回调服务对应的url。

InvalidParameter

InvalidAppId

Invalid appId.

无效的appId，请输入合法的appId。

InvalidParameter

AppIdIsEmpty

AppId is empty.

appId为空，请输入appId。

UnpurchasedAccess

BIL.ServiceNotActivate

User hasn't activate service.

用户未激活服务，请先开通听悟Agent服务。

UnsupportedOperation

TaskIsProcessing

Reused task is processing.

被复用的任务正在处理中，请等待任务处理完后再进行复用。

UnsupportedOperation

TaskIsFailed

Reused task has failed!

被复用的任务是失败任务，请复用成功的任务。

## Agent任务失败

任务运行失败错误码参考：[错误信息查询](https://help.aliyun.com/zh/tingwu/error-information-query)

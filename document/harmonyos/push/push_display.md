# 设置推送通知的显示内容

通知收到后，通知栏中显示的推送标题和内容可通过以下方式设置，配置的优先级为由低到高：

- 调用 `updatePushNickname` 接口设置推送显示属性。
- 使用推送模板。

## 设置推送显示属性

你可以调用 `updatePushNickname` 设置推送通知中显示的昵称，如以下代码示例所示：

```typescript
ChatClient.getInstance().pushManager()?.updatePushNickname(pushNickname).then(() => {
  // success logic
}).catch((e: ChatError) => {
  // failure logic
});
```

你也可以调用 `updatePushDisplayStyle` 设置推送通知的显示样式，如下代码示例所示：

```typescript
// 设置为简单样式。
const displayStyle = PushDisplayStyle.SimpleBanner;
ChatClient.getInstance().pushManager()?.updatePushDisplayStyle(displayStyle).then(() => {
  // success logic
}).catch((e: ChatError) => {
  // failure logic
})
```

| 参数设置      | 推送显示 | 图片    |
| :--------- | :----- |:------------- |
| <br/> - `PushDisplayStyle`：（默认）`SimpleBanner`<br/> - `nickname`：设置或不设置 | <br/> - 推送标题：**您有一条新消息**<br/> - 推送内容：**请点击查看**  | ![img](/images/android/push/push_displayattribute_1.png)|
| <br/> - `PushDisplayStyle`：`MessageSummary`<br/> - `nickname`：设置具体值 | <br/> - 推送标题：**您有一条新消息**<br/> - 推送内容：**消息发送方的推送昵称：消息内容**  |![img](/images/android/push/push_displayattribute_2.png)  |
| <br/> - `PushDisplayStyle`：`MessageSummary`<br/> - `nickname`：不设置    | <br/> - 推送标题：**您有一条新消息**<br/> - 推送内容：**消息发送方的 IM 用户 ID: 消息内容**  | ![img](/images/android/push/push_displayattribute_3.png)|

## 使用推送模板

推送模板主要用于服务器提供的默认配置不满足你的需求时，可使你设置全局范围的推送标题和推送内容。例如，服务器提供的默认设置为中文和英文的推送标题和内容，你若需要使用韩语或日语的推送标题和内容，则可以设置对应语言的推送模板。推送模板包括默认推送模板 `default` 和自定义推送模板。对于群组消息，你可以使用定向模板向某些用户推送与其他用户不同的离线通知。

你可以通过以下两种方式设置：

- [调用 REST API 配置](/document/server-side/push.html#使用推送模板)。
- 在[环信即时通讯云控制台](https://console.easemob.com/user/login)设置推送模板，详见[控制台文档](/product/enable_and_configure_IM.html#配置推送模板)。

使用推送模板有以下优势：

1. 自定义修改环信服务端默认推送内容。   

2. 接收方可以决定使用哪个模板。 

3. 按优先级选择模板使用方式。

**推送通知栏内容设置的使用优先级**

通知栏中显示的推送标题和内容可通过以下方式设置，优先级为由低到高：

1. 发送消息时使用默认的推送标题和内容：设置推送通知的展示方式 `PushDisplayStyle`。推送标题为“您有一条新消息”，推送内容为“请点击查看”。  
2. 发送消息时使用默认模板：若有默认模板 `default`，发消息时无需指定。
3. 接收方设置了推送模板。
4. 发送消息时通过消息扩展字段指定模板名称。

:::tip
1. 设置推送模板为推送的高级功能，使用前需要在[环信即时通讯控制台](https://console.easemob.com/user/login)的**即时通讯 > 功能配置 > 功能配置总览**页面激活推送高级功能。如需关闭推送高级功能必须联系商务，因为该操作会删除所有相关配置。

2. 推送模板相关的数据结构，详见[推送扩展字段](/document/server-side/push_extension.html)。
:::

#### **发送消息时使用推送模板**

创建模板后，你可以在发送消息时选择此推送模板，分为以下三种情况：

:::tip
若使用默认模板 **default**，消息推送时自动使用默认模板，创建消息时无需传入模板名称。
:::

1. 使用固定内容的推送模板，通过 `ext` 扩展字段指定推送模板名称。

这种情况下，创建消息时无需传入 `title_args` 和 `content_args` 参数。 

```typescript
// 先定义一个推送模版类
export class PushTemplate {
  // 模版名称
  name?: string;
  // 标题自定设置部分
  title_args?: string[];
  // 内容自定设置部分
  content_args?: string[];
}

// 下面以文本消息为例，其他类型的消息设置方法相同。
const message = ChatMessage.createTextSendMessage(conversationId, "消息内容");
if (message) {
  // 设置推送模板名称。设置前需在环信即时通讯云管理后台或调用 REST 接口创建推送模板。
  // 若为默认模板 `default`，无需传入模板名称。
  // 若为自定义模板，需传入模板名称。
  let templateName = "自定义推送模板名称";
  // 1.6.0版本之前版本需要先将 PushTemplate 转为 JSON，例如：let pushTemplateStr = JSON.stringify(pushTemplate);
  message?.setJsonAttribute("em_push_template", {
    name: templateName
  } as PushTemplate);
  // 发送消息。
  ChatClient.getInstance().chatManager()?.sendMessage(message);
}
```

2. 使用自定义或者默认推送模板，模板中的推送标题和推送内容使用以下内置参数：
- `{$dynamicFrom}`：服务器按优先级从高到底的顺序填充备注、群昵称（仅限群消息）和推送昵称。
- `{$fromNickname}`：推送昵称。  
- `{$msg}`：消息内容。

群昵称即群成员在群组中的昵称，群成员在发送群消息时通过扩展字段设置，JSON 结构如下：

```json
{
  "ext":{
    "em_push_ext":{
      "group_user_nickname":"Jane"
    }
  }
}       
```

内置参数的介绍，详见[环信即时通讯控制台文档](/product/enable_and_configure_IM.html#使用默认推送模板)。

这种方式的示例代码与“使用固定内容的推送模板”的相同。

3. 使用自定义推送模板，而且推送标题和推送内容为自定义参数：

例如，推送模板的设置如下图所示：

![img](/images/android/push/push_template_custom.png)

使用下面的示例代码后，通知栏中弹出的推送通知为：

您收到了一条消息<br/>
请及时查看

```typescript
// 先定义一个推送模版类
export class PushTemplate {
  // 模版名称
  name?: string;
  // 标题自定设置部分
  title_args?: string[];
  // 内容自定设置部分
  content_args?: string[];
}

// 下面以文本消息为例，其他类型的消息设置方法相同。
const message = ChatMessage.createTextSendMessage(conversationId, "消息内容");
if (message) {
  // 设置推送模板名称。设置前需在环信即时通讯云管理后台或调用 REST 接口创建推送模板。
  // 设置填写模板标题的 value 数组。
  let titleArgs = ["您","消息,"];
  // 设置填写模板内容的 value 数组。
  let contentArgs = ["请","查看"];
  let templateName = "push"; // 此处 `push` 为已在创建的推送模版名称。
  // 设置推送模板名称。若不指定，设置默认推送模板的信息。
  // 1.6.0版本之前版本需要先将 PushTemplate 转为 JSON，例如：let pushTemplateStr = JSON.stringify(pushTemplate);
  message?.setJsonAttribute("em_push_template", {
    name: templateName,
    title_args: titleArgs,
    content_args: contentArgs
  } as PushTemplate);
  // 发送消息。
  ChatClient.getInstance().chatManager()?.sendMessage(message);
}
```

#### **消息接收方使用推送模板**

消息接收方可以调用 `setPushTemplate` 方法传入推送模板名称，选择要使用的模板。

:::tip
若发送方在发送消息时使用了推送模板，则推送通知栏中的显示内容以发送方的推送模板为准。
:::

```typescript
ChatClient.getInstance().pushManager()?.setPushTemplate("自定义模板名称").then(() => {
  // success logic
}).catch((e: ChatError) => {
  // failure logic
})
```

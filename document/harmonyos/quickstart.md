# 快速开始

<Toc />

本文介绍如何快速集成环信即时通讯 IM HarmonyOS SDK 实现单聊。


## 实现原理

下图展示在客户端发送和接收一对一文本消息的工作流程。

![img](/images/android/sendandreceivemsg.png)

## 前提条件

- DevEco Studio NEXT Release（5.0.3.900）及以上；
- HarmonyOS SDK API 12 及以上；
- 有效的环信即时通讯 IM 开发者账号和 App key，见 [环信即时通讯云控制台](https://console.easemob.com/user/login)。

## 准备开发环境

本节介绍如何创建项目，将环信即时通讯 IM HarmonyOS SDK 集成到你的项目中，并添加相应的设备权限。

### 1. 创建 HarmonyOS 项目

参考以下步骤创建一个 HarmonyOS 项目。

1. 打开 DevEco Studio，点击 **Create Project**。
2. 在 **Choose Your Ability Template** 界面，选择 **Application > Empty Ability**，然后点击 **Next**。
3. 在 **Configure Your Project** 界面，依次填入以下内容：
   - **Project name**：你的 HarmonyOS 项目名称，如 HelloWorld。
   - **Bundle name**：你的项目包的名称，如 com.hyphenate.helloworld。
   - **Save location**：项目的存储路径。
   - **Compatible SDK**：项目的支持的最低 API 等级，选择 `5.0.0(12)` 及以上。
   - **Module name**：module的名称，默认为 `entry`。

4. 点击 **Finish**。根据屏幕提示，安装所需插件。

上述步骤使用 **DevEco Studio NEXT Release（5.0.3.900）** 示例。

### 2. 在工程 `build-profile.json5` 中设置支持字节码 HAR 包。

修改工程级 `build-profile.json5` 文件，在 `products` 节点下设置 `useNormalizedOHMUrl` 为 `true`。

```json
{
  "app": {
    "products": [
      {
         "buildOption": {
           "strictMode": {
             "useNormalizedOHMUrl": true
           }
         }
      }
    ]
  }
}
```

:::tip
- 此配置需要将 `DevEco Studio` 升级到 `Beta2（5.0.3.502）` 及以上版本。
- SDK 1.3.0 及以上版本采用字节码构建方式打包，必须设置 `useNormalizedOHMUrl` 为 `true`。
:::

### 2. 集成 SDK

打开 [SDK 下载](https://www.easemob.com/download/im#HarmonyOS)页面，获取最新版的环信即时通讯 IM HarmonyOS SDK，得到 `har` 形式的 SDK 文件。

将 SDK 文件，拷贝到 `Harmony` 工程，例如放至 `HelloWorld` 工程下 `entry` 模块下新建的 `libs` 目录中。

修改模块目录的 `oh-package.json5` 文件，在 `dependencies` 节点增加依赖声明。

```json
{
  "name": "entry",
  "version": "1.0.0",
  "description": "Please describe the basic information.",
  "main": "",
  "author": "",
  "license": "",
  "dependencies": {
    "@easemob/chatsdk": "file:./libs/chatsdk-x.x.x.har"
  }
}
```
最后单击 **File > Sync and Refresh Project** 按钮，直到同步完成。

### 3. 添加项目权限

在模块的 `module.json5` ，例如：`HelloWorld` 中 `entry` 模块的 `module.json5` 中，配置示例如下：

```json
{
  module: {
    requestPermissions: [
      {
        name: "ohos.permission.GET_NETWORK_INFO",
      },
      {
        name: "ohos.permission.INTERNET",
      },
    ],
  },
}
```

## 实现单聊

本节介绍如何实现单聊。

### 1. SDK 初始化

```typescript
import { ChatClient, ChatOptions } from '@easemob/chatsdk';

let options = new ChatOptions({
  appKey: "你的 AppKey"
});
......// 其他 ChatOptions 配置。
// 初始化时传入上下文以及options
ChatClient.getInstance().init(context, options);
```

### 2. 创建账号

在 [环信控制台](https://console.easemob.com/user/login) 创建用户，获取用户 ID 和用户 token。详见 [创建用户文档](/product/enable_and_configure_IM.html#创建-im-用户)。

在生产环境中，为了安全考虑，你需要在你的应用服务器集成 [获取 App Token API](/document/server-side/easemob_app_token.html) 和 [获取用户 Token API](/document/server-side/easemob_user_token.html) 实现获取 Token 的业务逻辑，使你的用户从你的应用服务器获取 Token。

### 3. 登录账号

利用用户 ID 和用户 Token 实现用户登录：

```typescript
import { ChatClient, ChatError } from '@easemob/chatsdk';

ChatClient.getInstance().loginWithToken(userId, token).then(() => {
    // success logic        
}).catch((error: ChatError) => {
    // failure logic
});
```

:::tip
1. 除了注册监听器，其他的 SDK 操作均需在登录之后进行。
:::

### 4. 发送一条单聊消息

```typescript
import { ChatClient, ChatMessage } from '@easemob/chatsdk';

// `content` 为要发送的文本内容，`toChatUsername` 为对方的账号。
let message = ChatMessage.createTextSendMessage(toChatUsername, content);
if (!message) {
    return;
}
// 发送消息
ChatClient.getInstance().chatManager()?.sendMessage(message);
```

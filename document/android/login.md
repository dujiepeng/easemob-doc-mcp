# 登录

初始化 IM SDK 后，你需要首先调用接口登录。登录成功后，才能使用 IM 的功能。

## 用户注册

1. 可通过以下两种方式调用接口创建用户：

- 授权注册：通过环信提供的 REST API 注册环信用户账号，注册后保存到你的服务器或返给客户端。要使用授权注册，你需要在[环信即时通讯云控制台](https://console.easemob.com/user/login)的**即时通讯** > **服务概览**的**设置**区域，将**用户注册模式**设置为**授权注册**。相关的 REST API 介绍，详见[授权注册单个用户](/document/server-side/account_system.html#授权注册单个用户)和[批量授权注册用户](/document/server-side/account_system.html#批量授权注册用户)的接口介绍。

- 开放注册：一般在体验 Demo 和测试环境时使用，正式环境中不推荐使用该方式注册环信账号。要使用开放注册，需要在[环信即时通讯云控制台](https://console.easemob.com/user/login)的**即时通讯** > **服务概览**的**设置**区域，将**用户注册模式**设置为**开放注册**。只有打开该开关，才能使用客户端或 [REST API](/document/server-side/account_system.html#开放注册单个用户)开放注册用户。

示例代码如下所示：  
  
```java
// 注册失败会抛出 HyphenateException。
EMClient.getInstance().createAccount(mAccount, mPassword);// 同步方法。
``` 

2. 通过 [环信控制台](https://console.easemob.com/user/login) 创建用户：

可以在 [环信控制台](https://console.easemob.com/user/login) 创建正式环境下和测试环境下的用户，详见 [创建用户相关介绍](/product/enable_and_configure_IM.html#创建-im-用户)。

## 主动登录

1. **用户 ID + token** 是更加安全的登录方式。

测试环境下，你在[环信即时通讯云控制台](https://console.easemob.com/user/login)创建用户后，环信服务器会自动为这些用户分配用户 Token，详见[测试环境下创建用户的介绍](/product/enable_and_configure_IM.html#测试环境)。

在生产环境中，为了安全考虑，你需要在你的应用服务器集成 [获取 App Token API](/document/server-side/easemob_app_token.html) 和 [获取用户 Token API](/document/server-side/easemob_user_token.html) 实现获取 Token 的业务逻辑，使你的用户从你的应用服务器获取 Token。SDK 会在 Token 过期时或者其有效期达到 80%（4.15.0 之前为 50%）时分别回调 `onTokenExpired` 和 `onTokenWillExpire` 通知用户更新 Token。你可以采取各种机制更新 Token，例如，每次登录时更新 token。

```java
EMClient.getInstance().loginWithToken(mAccount, mToken, new EMCallBack() {
    // 登录成功回调
    @Override
    public void onSuccess() {

    }

    // 登录失败回调，包含错误信息
    @Override
    public void onError(int code, String error) {

    }
});
```

1. **用户 ID + 密码**登录是传统的登录方式。用户名和密码均由你的终端用户自行决定，密码需要符合[密码规则要求](/document/server-side/account_system.html#开放注册单个用户)。

```java
EMClient.getInstance().login(mAccount, mPassword, new EMCallBack() {
    // 登录成功回调
    @Override
    public void onSuccess() {

    }

    // 登录失败回调，包含错误信息
    @Override
    public void onError(int code, String error) {

    }

});
```

## 自动登录

即时通讯 IM 默认自动登录，即 `EMOptions#setAutoLogin` 选项默认为 `true`。自动登录模式下，首次登录成功之后，后续初始化 SDK 时均会自动登录。

自动登录期限默认为 30 天，即设置自动登录后，用户 30 天内可自动登录。若调整改期限，可联系环信商务。

不过，自动登录还取决于你设置的用户 token 或密码有效期，例如，用户 token 有效期为 24 小时，则用户在 24 小时后，需获取 token 重新登录。

## 获取当前登录的用户

你可以调用 `EMClient#getCurrentUser` 方法获取当前登录用户的用户 ID。

## 获取登录状态

你可以调用 `EMClient#isLoggedIn` 方法获取当前用户的登录状态。

## 退出登录

你可以调用 `logout` 方法退出登录。退出登录后，你不会再收到其他用户发送的消息。 

同步方法：

```java
EMClient.getInstance().logout(true);
```

异步方法：

```java
EMClient.getInstance().logout(true, new EMCallBack() {

    @Override
    public void onSuccess() {

    }

    @Override
    public void onError(int code, String message) {

    }
});
```

:::tip

1. 如果集成了 FCM 等第三方推送，`logout` 方法中 `unbindToken` 参数需设为 `true`，退出时会解绑设备 token，否则可能会出现退出了，还能收到消息推送通知的现象。
有时可能会遇到网络问题而解绑失败，app 处理时可以弹出提示框让用户选择，是否继续退出(弹出框提示继续退出能收到消息的风险)，如果用户选择继续退出，传 `false` 再调用 `logout` 方法退出成功。当然也可以失败后还是返回退出成功，然后在后台起个线程不断调用 `logout` 方法直到成功。这样存在风险，即用户杀掉了 app，网络恢复后用户还会继续收到消息。

2. 如果调用异步退出方法，在收到 `onsuccess` 回调后才能去调用 IM 相关方法，例如 `loginWithToken`。
:::

## 账号切换

若在 app 中从当前账号切换到其他账号，你需要首先调用 `logout` 方法登出，然后再调用 `loginWithToken` 或 `login` 方法登录。

## 多设备登录

除了单端单设备登录，环信即时通讯 IM 支持同一账号在多端的多个设备上登录。多设备登录时，若同端设备数量超过限制，新登录的设备会将之前登录的设备踢下线。

关于多设备登录场景中的设备数量限制、互踢策略以及信息同步，详见[多设备登录文档](multi_device.html)。


## 更多

### 登录被封禁账号的提示

在环信即时通讯控制台或调用 REST API 封禁用户账号后，若仍使用该账号登录，SDK会返回 "service is disabled"（305 错误）, 可以根据用户这个返回值来进行相应的提示或者处理。

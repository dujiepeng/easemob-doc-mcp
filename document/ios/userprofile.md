# 管理用户属性

<Toc />

环信即时通讯 IM 自 V3.8.1 开始支持用户属性管理功能。

用户属性指实时消息互动用户的信息，如用户昵称、头像、邮箱、电话、性别、签名、生日等。

例如，在招聘场景下，利用用户属性功能可以存储性别、邮箱、用户类型（面试者）、职位类型（web 研发）等。查看用户信息时，可以直接查询服务器存储的用户属性信息。

本文介绍如何通过管理用户属性设置、更新、存储并获取实时消息用户的相关信息。

:::tip
为保证用户信息安全，SDK 仅支持用户设置或更新自己的用户属性。
:::

## 技术原理

环信即时通讯 IM iOS SDK 提供一个 `userInfoManager` 类，支持获取、设置及修改用户属性信息，其中包含如下方法：

- `updateOwnUserInfo` 设置和修改当前用户自己的属性信息；
- `fetchUserInfoById` 获取指定用户的所有用户属性信息。

## 前提条件

设置用户属性前，请确保满足以下条件：

- 完成 SDK 初始化，详见 [快速开始](quickstart.html)；
- 了解环信即时通讯 IM 的使用限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

本节介绍如何在项目中设置及获取用户属性。

单个用户的所有属性最大不超过 2 KB，单个 app 所有用户属性数据最大不超过 10 GB。

### 设置当前用户的所有属性

当前用户设置自己的所有属性：

```objectivec
EMUserInfo *userInfo = [[EMUserInfo alloc] init];
userInfo.userId = EMClient.sharedClient.currentUsername;
userInfo.nickName = @"EM";
userInfo.avatarUrl = @"https://www.EM.io";
userInfo.birth = @"2000.10.10";
userInfo.sign = @"hello world";
userInfo.phone = @"12333333333";
userInfo.mail = @"123456@qq.com";
userInfo.gender = 1;
// 异步方法
[EMClient.sharedClient.userInfoManager updateOwnUserInfo:userInfo completion:^(EMUserInfo *aUserInfo, EMError *aError) {

}];
```

关于用户属性，客户端针对用户的昵称、头像 URL、联系方式、邮箱、性别、签名、生日和扩展字段默认使用以下键名。[调用 RESTful 的接口设置](/document/server-side/userprofile.html#设置用户属性)或[删除用户属性](/document/server-side/userprofile.html#删除用户属性)，若要确保在客户端能够获取设置，请求中必须传以下键名与客户端保持一致，键值可根据实际使用场景确定。

| 字段        | 类型   | 描述                                                                                              |
| ----------- | ------ | ------------------------------------------------------------------------------------------------- |
| `nickname`  | String | 用户昵称。长度在 64 字符内。                                                                      |
| `avatarurl` | String | 用户头像 URL 地址。长度在 256 字符内。                                                            |
| `phone`     | String | 用户联系方式。长度在 32 字符内。                                                                  |
| `mail`      | String | 用户邮箱。长度在 64 字符内。                                                                      |
| `gender`    | Int    | 用户性别：<br/> - `1`：男；<br/> - `2`：女；<br/> - （默认）`0`：未知；<br/> - 设置为其他值无效。 |
| `sign`      | String | 用户签名。长度在 256 字符内。                                                                     |
| `birth`     | String | 用户生日。长度在 64 字符内。                                                                      |
| `ext`       | String | 扩展字段。                                                                                        |

### 设置当前用户的单个属性

例如，修改当前用户的头像：

```objectivec
NSString *url = @"https://download-sdk.oss-cn-beijing.aliyuncs.com/downloads/IMDemo/avatar/Image1.png";

[[EMClient sharedClient].userInfoManager updateOwnUserInfo:url withType:EMUserInfoTypeAvatarURL completion:^(EMUserInfo *aUserInfo, EMError *aError) {
    if (aUserInfo && completion) {
        completion(aUserInfo);
    }
}];
```

### 获取用户的所有属性

用户可以获取指定一个或多个用户的所有用户属性：

```objectivec
// 每次传入的用户 ID 数量不能超过 100。
// 异步方法
[[EMClient sharedClient].userInfoManager fetchUserInfoById:@[EMClient.sharedClient.currentUsername] 		completion:^(NSDictionary *aUserDatas, EMError *aError) {
}];
```

### 获取用户的指定属性

用户可以获取单个或多个用户的单个或多个用户属性。

```objectivec
// 获取指定用户的指定用户属性。
NSString *userIds = @[@"user1",@"user2"];
NSArray<NSNumber *> *userInfoTypes = @[@(EMUserInfoTypeAvatarURL),@(EMUserInfoTypePhone),@(EMUserInfoTypeMail)];
// 异步方法
[[EMClient sharedClient].userInfoManager fetchUserInfoById:userIds type:userInfoTypes completion:^(NSDictionary *aUserDatas, EMError *aError) {

}];
```

## 更多功能

### 用户头像管理

如果你的应用场景中涉及用户头像管理，还可以参考如下步骤进行操作：

1. 开通第三方文件存储服务。详情可以参考文件储存服务商的文档。
2. 将头像文件上传至上述第三方文件存储，并获取存储 URL 地址。
3. 将该 URL 地址传入用户属性的头像字段（avatarUrl）。
4. 显示头像时，通过调用 `fetchUserInfoById` 获取头像 URL，并在本地 UI 中渲染头像。

### 名片消息

如果你的场景中涉及名片消息，你也可以使用自定义属性功能，并参考如下示例代码实现：

```objectivec
// 设置自定义消息的 `event` 为 `userCard` ，并在 `ext` 中添加展示名片所需要的用户 ID、昵称和头像等字段。
EMCustomMessageBody *body = [[EMCustomMessageBody alloc] init];
body.event = @"userCard";
NSDictionary *messageExt = @{@"userId":EMClient.sharedClient.currentUsername,
                           @"nickname":@"nickname",
                           @"avatar":@"https://download-sdk.oss-cn-beijing.aliyuncs.com/downloads/IMDemo/avatar/Image1.png"
                        };
body.ext = messageExt;
// 异步方法
EMChatMessage *message = [[EMChatMessage alloc] initWithConversationID:@"conversationID"
                                                from:@"sender"
                                                to:@"receiver"
                                                body:body
                                                ext:nil];
// 发送消息
[[EMClient sharedClient].chatManager sendMessage:message progress:nil completion:^(EMChatMessage *message, EMError *error) {}];
```

如果需要在名片中展示更丰富的信息，可以在 `ext` 中增加更多字段。

可参考 [示例项目](https://www.easemob.com/download/im) 中的以下类：

- `EMCustomMessageBody`
- `EMChatMessage`

### 常见问题

Q：我设置了用户昵称（`nickname`），但调用客户端或 RESTful API 获取用户属性时，未返回用户昵称，原因是什么？

A：你可以调用[客户端](#设置当前用户的所有属性) 或[RESTful API](/document/server-side/userprofile.html#设置用户属性) 设置用户昵称，例如 iOS 为 `updateOwnUserInfo`，然后通过[客户端](#获取用户的所有属性)或[RESTful API](/document/server-side/userprofile.html#获取用户属性) 获取用户属性，例如 iOS 为 `fetchUserInfoById`。

设置用户昵称时，请注意以下两点：

1. 调用 RESTful 接口设置用户昵称时，若要确保在客户端能够获取设置，请求中必须传 `nickname` 键名。

2. 调用 RESTful API [获取用户详情](/document/server-side/account_system.html#获取用户详情)和[删除用户账户](/document/server-side/account_system.html#删除用户账号)中返回的响应中的 `nickname` 参数表示为推送昵称，即离线推送时在接收方的客户端推送通知栏中显示的发送方的昵称，与用户属性中的用户昵称不同。不过，我们建议这两种昵称的设置保持一致。因此，修改其中一个昵称时，也需调用相应方法对另一个进行更新，确保设置一致。例如，对于 iOS，更推送昵称的方法为 [updatePushDisplayName](/document/ios/push/push_display.html#设置和获取推送通知的显示属性)，对于 RESTful API，详见 [离线推送通知的显示属性配置](/document/server-side/push.html#设置离线推送时显示的昵称)。

Q: 调用设置或获取用户属性的接口时，上报错误码 4 的原因是什么？

A：设置和获取用户属性的接口，包括设置当前用户的属性、获取单个或多个用户的用户属性和获取指定用户的指定用户属性，超过调用频率限制时，会上报错误码 4 `EMErrorExceedServiceLimit`。

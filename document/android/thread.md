# 管理子区

<Toc />

子区是群组成员的子集，是支持多人沟通的即时通讯系统。本文介绍如何使用环信即时通讯 IM Android SDK 在实时互动 app 中创建和管理子区，并实现子区相关功能。

使用子区功能前，你需要在[环信即时通讯控制台](https://console.easemob.com/user/login)开通。

如需查看消息相关内容，参见 [子区消息管理](thread_message.html)。

## 技术原理

环信即时通讯 IM Android SDK 提供 [EMChatThreadManager](https://sdkdocs.easemob.com/apidoc/android/chat3.0/classcom_1_1hyphenate_1_1chat_1_1_e_m_chat_thread_manager.html)、[EMChatThread](https://sdkdocs.easemob.com/apidoc/android/chat3.0/classcom_1_1hyphenate_1_1chat_1_1_e_m_chat_thread.html)、和 [EMChatThreadChangeListener](https://sdkdocs.easemob.com/apidoc/android/chat3.0/interfacecom_1_1hyphenate_1_1_e_m_chat_thread_change_listener.html) 类，用于管理子区，支持你通过调用 API 在项目中实现如下功能：

- 创建、解散子区
- 加入、退出子区
- 修改子区名称
- 获取子区详情
- 获取子区成员列表
- 获取子区列表
- 批量获取子区中的最新消息
- 监听子区事件

## 前提条件

开始前，请确保满足以下条件：

- 完成 3.9.3 或以上版本 SDK 初始化，详见 [快速开始](quickstart.html)。
- 了解环信即时通讯 IM API 的 [使用限制](/product/limitation.html)。
- 了解子区和子区成员数量限制，详见 [使用限制](/product/limitation.html)。
- 已在[环信即时通讯控制台](https://console.easemob.com/user/login)开通子区功能。

## 实现方法

本节介绍如何使用环信即时通讯 IM Android SDK 提供的 API 实现上述功能。

### 创建子区

所有群成员均可以调用 `createChatThread` 方法，基于一条群组消息新建子区。

单设备登录时，子区所属群组的所有成员均会收到 `EMChatThreadChangeListener#onChatThreadCreated`回调；多设备登录时，其他设备会同时收到 `EMMultiDeviceListener#onThreadEvent` 回调，回调事件为 `THREAD_CREATE`。

示例代码如下：

```java
// parentId：群组 ID
// messageId：消息 ID，基于该消息创建子区
// threadName：子区名称，长度不超过 64 个字符
EMClient.getInstance().chatThreadManager().createChatThread(parentId, messageId, threadName, new EMValueCallBack<EMChatThread>() {
    @Override
    public void onSuccess(EMChatThread value) {
        
    }
    @Override
    public void onError(int error, String errorMsg) {
        
    }
});
```

### 解散子区

仅子区所在群组的群主和群管理员可以调用 `destroyChatThread` 方法解散子区。

单设备登录时，子区所属群组的所有成员均会收到 `EMChatThreadChangeListener#onChatThreadDestroyed` 回调；多设备登录时，其他设备会同时收到 `EMMultiDeviceListener#onThreadEvent` 回调，回调事件为 `THREAD_DESTROY`。

:::tip
解散子区或解散子区所在的群组后，将删除本地数据库及内存中关于该子区的全部数据，需谨慎操作。
:::

示例代码如下：

```java
EMClient.getInstance().chatThreadManager().destroyChatThread(chatThreadId, new EMCallBack() {
    @Override
    public void onSuccess() {
        
    }
    @Override
    public void onError(int code, String error) {
    }
});
```

### 加入子区

子区所在群组的所有成员均可以调用 `joinChatThread` 方法加入子区。

加入子区的具体步骤如下：

1. 收到 `EMChatThreadChangeListener#onChatThreadCreated` 回调或 `EMChatThreadChangeListener#onChatThreadUpdated` 回调，或调用 `getChatThreadsFromServer` 方法从服务器获取指定群组的子区列表，从中获取到想要加入的子区 ID。
2. 调用 `joinChatThread` 传入子区 ID 加入对应子区。  

多设备登录时，其他设备会同时收到 `EMMultiDeviceListener#onThreadEvent` 回调，回调事件为 `THREAD_JOIN`。

示例代码如下：

```java
EMClient.getInstance().chatThreadManager().joinChatThread(chatThreadId, new EMValueCallBack<EMChatThread>() {
    @Override
    public void onSuccess(EMChatThread value) {
        
    }
    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

### 退出子区

#### 子区成员主动退出子区

子区成员均可以主动调用 `leaveChatThread` 方法退出子区，退出子区后，该成员将不会再收到子区消息。

多设备登录时，其他设备会同时收到 `EMMultiDeviceListener#onThreadEvent` 回调，回调事件为 `THREAD_LEAVE`。

示例代码如下：

```java
EMClient.getInstance().chatThreadManager().leaveChatThread(chatThreadId, new EMCallBack() {
    @Override
    public void onSuccess() {
        
    }
    @Override
    public void onError(int code, String error) {
    }
});
```

#### 子区成员被移出子区

仅群主和群管理员可以调用 `removeMemberFromChatThread` 方法将指定成员 (群管理员或普通成员) 踢出子区，被踢出子区的成员将不再接收到子区消息。

被踢出子区的成员会收到 `EMChatThreadChangeListener#onChatThreadUserRemoved` 回调。多设备登录时，执行踢人操作的成员的其他设备会同时收到 `EMMultiDeviceListener#onChatThreadEvent` 回调，回调事件为 `THREAD_KICK`。

示例代码如下：

```java
// chatThreadId: 子区 ID
// member: 子区成员的用户 ID
EMClient.getInstance().chatThreadManager().removeMemberFromChatThread(chatThreadId, member, new EMCallBack() {
    @Override
    public void onSuccess() {
    }

    @Override
    public void onError(int code, String error) {
    }
});
```

### 修改子区名称

仅群主和群管理员以及子区的创建者可以调用 `updateChatThreadName` 方法修改子区名称。

单设备登录时，子区所属群组的所有成员会收到 `EMChatThreadChangeListener#onChatThreadUpdated` 回调；多设备登录时，其他设备会同时收到 `EMMultiDeviceListener#onThreadEvent` 回调，回调事件为 `THREAD_UPDATE`。

示例代码如下：

```java
// chatThreadId: 子区 ID
// newChatThreadName: 修改的子区名称，长度不超过 64 个字符
EMClient.getInstance().chatThreadManager().updateChatThreadName(chatThreadId, newChatThreadName, new EMCallBack() {
    @Override
    public void onSuccess() {
    }

    @Override
    public void onError(int code, String error) {
    }
});
```

### 获取子区详情

子区所属群组的所有成员均可以调用 `getChatThreadFromServer` 方法从服务器获取子区详情。

示例代码如下：

```java
// chatThreadID: 子区 ID
EMClient.getInstance().chatThreadManager().getChatThreadFromServer(chatThreadId, new EMValueCallBack<EMChatThread>() {
    @Override
    public void onSuccess(EMChatThread value) { 
    }

    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

### 获取子区成员列表

子区所属群组的所有成员均可以调用 `getChatThreadMembers` 方法从服务器分页获取子区成员列表。

```java
// chatThreadId: 子区 ID
// limit: 单次请求返回的成员数，取值范围为 [1,50]
// cursor: 开始获取数据的游标位置，首次调用方法时传 `null` 或空字符串
EMClient.getInstance().chatThreadManager().getChatThreadMembers(chatThreadId, limit, cursor, 
        new EMValueCallBack<EMCursorResult<String>>() {
    @Override
    public void onSuccess(EMCursorResult<String> value) {
    }

    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

### 获取子区列表

1. 用户可以调用 `getJoinedChatThreadsFromServer` 方法从服务器分页获取自己加入和创建的子区列表：

```java
// limit: 单次请求返回的子区数，取值范围为 [1,50]
// cursor: 开始获取数据的游标位置，首次调用方法时传 `null` 或空字符串
EMClient.getInstance().chatThreadManager().getJoinedChatThreadsFromServer(limit, cursor, 
        new EMValueCallBack<EMCursorResult<EMChatThread>>() {
    @Override
    public void onSuccess(EMCursorResult<EMChatThread> value) {
    }

    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

2. 用户可以调用 `getJoinedChatThreadsFromServer` 方法从服务器分页获取指定群组中自己加入和创建的子区列表：

```java
// parentId: 群组 ID
// limit: 单次请求返回的子区数，取值范围为 [1,50]
// cursor: 开始获取数据的游标位置，首次调用方法时传 `null` 或空字符串
EMClient.getInstance().chatThreadManager().getJoinedChatThreadsFromServer(parentId, limit, cursor, 
        new EMValueCallBack<EMCursorResult<EMChatThread>>() {
    @Override
    public void onSuccess(EMCursorResult<EMChatThread> value) {
    }

    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

3. 用户还可以调用 `getChatThreadsFromServer` 方法从服务器分页获取指定群组的子区列表：

```java
// parentId: 群组 ID
// limit: 单次请求返回的子区数，取值范围为 [1,50]
// cursor: 开始获取数据的游标位置，首次调用方法时传 `null` 或空字符串
EMClient.getInstance().chatThreadManager().getChatThreadsFromServer(parentId, limit, cursor, 
        new EMValueCallBack<EMCursorResult<EMChatThread>>() {
    @Override
    public void onSuccess(EMCursorResult<EMChatThread> value) {
    }

    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

### 批量获取子区中的最新一条消息

用户可以调用 `getChatThreadLatestMessage` 方法从服务器批量获取子区中的最新一条消息。

示例代码如下：

```java
// chatThreadIdList: 要查询的子区 ID 列表，每次最多可传入 20 个子区 ID
EMClient.getInstance().chatThreadManager().getChatThreadLatestMessage(chatThreadIdList, 
        new EMValueCallBack<Map<String, EMMessage>>() {
    @Override
    public void onSuccess(Map<String, EMMessage> value) {
    }
    
    @Override
    public void onError(int error, String errorMsg) {
    }
});
```

### 监听子区事件

`EMChatThreadManager` 类中提供子区事件的监听接口。开发者可以通过设置此监听，获取子区中的事件，并做出相应处理。如果不再使用该监听，需要移除，防止出现内存泄漏。

示例代码如下：

```java
EMChatThreadChangeListener chatThreadChangeListener = new EMChatThreadChangeListener() {
    @Override
    // 子区创建。子区所属群组的所有成员收到该事件。
    public void onChatThreadCreated(ChatThreadEvent event) {}
    @Override
    // 子区名称修改、子区中新增或撤回消息。子区所属群组的所有成员会收到该事件。
    public void onChatThreadUpdated(ChatThreadEvent event) {}
    @Override
    // 子区解散。子区所属群组的所有成员会收到该事件。
    public void onChatThreadDestroyed(ChatThreadEvent event) {}
    @Override
    // 子区成员被移除。被踢出子区的成员收到该事件。
    public void onChatThreadUserRemoved(ChatThreadEvent event) {}
};
// 注册监听
EMClient.getInstance().chatThreadManager().addChatThreadChangeListener(chatThreadChangeListener);

// 移除监听
EMClient.getInstance().chatThreadManager().removeChatThreadChangeListener(chatThreadChangeListener);
```
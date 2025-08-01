# 管理群组属性

<Toc />

群组是支持多人沟通的即时通讯系统，本文介绍如何使用环信即时通讯 IM Flutter SDK 在实时互动 app 中实现群组属性相关功能。

## 技术原理

环信即时通讯 IM Flutter SDK 提供 `EMGroup`、`EMGroupManager` 和 `EMGroupEventHandler` 类用于群组管理，支持你通过调用 API 在项目中实现如下功能：

- 修改群组名称、描述
- 获取、设置和修改群头像
- 获取、更新群组公告
- 管理群组共享文件
- 更新群扩展字段

## 前提条件

开始前，请确保满足以下条件：

- 完成 SDK 初始化，详见 [快速开始](quickstart.html)；
- 了解环信即时通讯 IM 的使用限制，详见 [使用限制](/product/limitation.html)；
- 了解群组和群成员的数量限制，详见 [套餐包详情](https://www.easemob.com/pricing/im)。

## 实现方法

本节介绍如何使用环信即时通讯 IM Flutter SDK 提供的 API 实现上述功能。

### 修改群组名称

仅群主和群管理员可以调用 `EMGroupManager#updateGroupName` 方法设置和修改群组名称，群名称的长度限制为 128 个字符, 其他成员会收到 `EMGroupEventHandler#onSpecificationDidUpdate` 回调。

示例代码如下：

```dart
try {
  await EMClient.getInstance.groupManager.updateGroupName(
    groupId,
    newName,
  );
} on EMError catch (e) {
}
```

### 修改群组描述

仅群主和群管理员可以调用 `EMGroupManager#updateGroupDesc` 方法设置和修改群组描述，群描述的长度限制为 512 个字符, 其他成员会收到 `EMGroupEventHandler#onSpecificationDidUpdate` 回调。

示例代码如下：

```dart
try {
  await EMClient.getInstance.groupManager.updateGroupDesc(
    groupId,
    newDesc,
  );
} on EMError catch (e) {
}
```

### 管理群组头像

自 Flutter SDK 4.15.0 开始，支持群组头像功能。

#### 设置群组头像

- 创建群组时，可设置群组头像：

```dart
try {
  await EMClient.getInstance.groupManager.createGroup(
    groupName: "groupName",
    avatarUrl: "avatarUrl",
  );
} on EMError catch (e) {
}
```

- 创建群组后，若设置群组头像，可调用 [修改群组头像](#修改群组头像) API 设置头像。

#### 修改群组头像

创建群组完成后，群主或管理员可调用 `EMGroupManager#updateGroupAvatarUrl` 设置或修改群组头像：

```dart
try {
  await EMClient.getInstance.groupManager.updateGroupAvatarUrl(
    groupId: 'groupId',
    avatarUrl: 'avatarUrl',
  );
} on EMError catch (e) {}
```

群组头像被修改后，其他群成员会收到 `  EMGroupEventHandler#onSpecificationDidUpdate` 回调：

```dart
EMClient.getInstance.groupManager.addEventHandler(
  'UNIQUE_HANDLER_ID',
  EMGroupEventHandler(
    onSpecificationDidUpdate: (group) {},
  ),
);
```

#### 获取群组头像

群成员可以通过获取群详情的方法 `EMGroupManager#fetchGroupInfoFromServer`，获取群组头像：

```dart
try {
  EMGroup group =
      await EMClient.getInstance.groupManager.fetchGroupInfoFromServer(
    'groupId',
  );
  String? avatarUrl = group.avatarUrl;
} on EMError catch (e) {}
```

### 更新群公告

仅群主和群管理员可以调用 `EMGroupManager#updateGroupAnnouncement` 方法设置和更新群公告，群公告的长度限制为 512 个字符。群公告更新后，其他群成员收到 `EMGroupEventHandler#onAnnouncementChangedFromGroup` 事件。

示例代码如下：

```dart
try {
  await EMClient.getInstance.groupManager.updateGroupAnnouncement(
    groupId,
    newAnnouncement,
  );
} on EMError catch (e) {
}
```

### 获取群公告

所有群成员均可以调用 `EMGroupManager#fetchAnnouncementFromServer` 方法从服务器获取群公告。

示例代码如下：

```dart
try {
  String? announcement =
      await EMClient.getInstance.groupManager.fetchAnnouncementFromServer(
    groupId,
  );
} on EMError catch (e) {
}
```

### 管理共享文件

#### 上传共享文件

所有群组成员均可以调用 `EMGroupManager#uploadGroupSharedFile` 方法上传共享文件至群组，单个群共享文件大小限制为 10 MB。上传共享文件后，其他群成员收到 `EMGroupEventHandler#onSharedFileAddedFromGroup` 事件。

示例代码如下：

```dart
try {
  await EMClient.getInstance.groupManager.uploadGroupSharedFile(
    groupId,
    filePath,
  );
} on EMError catch (e) {
}
```

#### 下载共享文件

所有群成员均可调用 `downloadGroupSharedFile` 方法下载群组共享文件。

```dart
try {
  // 获取文件列表
  List<EMGroupSharedFile> list =
      await EMClient.getInstance.groupManager.fetchGroupFileListFromServer(
    groupId,
    pageNum: 1,
    pageSize: 10,
  );

  if (list.isNotEmpty) {
    await EMClient.getInstance.groupManager.downloadGroupSharedFile(
      groupId: groupId,
      fileId: list.first.fileId!,
      savePath: savePath,
    );
  }
} on EMError catch (e) {
  debugPrint('$e');
}
```

#### 删除共享文件

所有群成员均可以调用 `EMGroupManager#removeGroupSharedFile` 方法删除群共享文件。删除共享文件后，其他群成员收到 `EMGroupEventHandler#onSharedFileDeletedFromGroup` 事件。

群主和群管理员可删除全部的群共享文件，群成员只能删除自己上传的群文件。

示例代码如下：

```dart
try {
  await EMClient.getInstance.groupManager.removeGroupSharedFile(
    groupId,
    fileId,
  );
} on EMError catch (e) {
}
```

#### 从服务器获取共享文件

所有群成员均可以调用 `EMGroupManager#fetchGroupFileListFromServer` 方法从服务器获取群组的共享文件列表。

示例代码如下：

```dart
try {
  List<EMGroupSharedFile> list =
      await EMClient.getInstance.groupManager.fetchGroupFileListFromServer(
    groupId,
    pageNum: pageNum,
    pageSize: pageSize,
  );
} on EMError catch (e) {
}
```

### 更新群扩展字段

仅群主和群管理员可以调用 `EMGroupManager#updateGroupExtension` 方法更新群组的扩展字段，群组扩展字段设置 JSON 格式的数据，用于自定义更多群组信息。群扩展字段的长度限制为 8 KB。

示例代码如下：

```dart
try {
  await EMClient.getInstance.groupManager.updateGroupExtension(
    groupId,
    extension,
  );
} on EMError catch (e) {
}
```

### 监听群组事件

详见 [监听群组事件](group_manage.html#监听群组事件)。

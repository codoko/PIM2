# 巡检自动化系统 - Android应用

## 📱 项目概述

这是一个基于Kivy框架开发的Android应用程序，将原有的Python巡检脚本打包成APK，使其能够在没有Termux和Python环境的Android设备上独立运行。

## ✨ 功能特性

- 🔐 **安全登录验证**
  - 用户名和用户代码验证
  - 默认密码保护（密码：12138）
  - 防止误用和未授权访问

- 🔄 **自动化巡检**
  - 完整集成原始Python脚本功能
  - 智能时间序列生成
  - 批量任务处理

- 📱 **移动端优化**
  - 响应式界面设计
  - 触摸友好的交互
  - 实时日志显示

- 📁 **文件管理**
  - 灵活的数据目录配置
  - JSON文件读写
  - 权限管理

## 🛠️ 技术架构

### 核心技术栈
- **Kivy**: 跨平台Python GUI框架
- **Buildozer**: Android APK打包工具
- **Python 3**: 后端逻辑处理
- **JSON**: 数据交换格式

### 项目结构
```
├── main.py                 # 主应用程序
├── buildozer.spec          # Android打包配置
├── requirements.txt        # Python依赖
├── .gitee/build.yml        # Gitee构建配置
├── .github/workflows/      # GitHub Actions配置
└── README.md              # 项目文档
```

## 📦 安装指南

### 方法1：直接下载APK
1. 从Gitee或GitHub发布页面下载最新的APK文件
2. 在Android设备上启用"未知来源"安装：
   - 设置 → 安全 → 未知来源 → 允许
3. 点击下载的APK文件进行安装
4. 授予应用所需的文件读写权限

### 方法2：自行构建
1. 克隆项目代码：
   ```bash
   git clone https://gitee.com/your-repo/inspection-automation.git
   cd inspection-automation
   ```

2. 安装构建环境：
   ```bash
   # 安装Buildozer
   pip install buildozer cython
   
   # Ubuntu/Debian系统
   sudo apt update
   sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

3. 构建APK：
   ```bash
   buildozer android debug
   ```

4. 构建完成后，APK文件位于：
   ```
   bin/InspectionAutomation-1.0.0-debug.apk
   ```

## 🚀 使用教程

### 首次使用
1. **启动应用**
   - 点击桌面图标启动应用
   - 进入登录界面

2. **用户登录**
   - 输入您的**用户名**（Username）
   - 输入您的**用户代码**（Usercode）
   - 输入默认密码：**12138**
   - 点击"登录"按钮

3. **配置数据目录**
   - 登录成功后进入主界面
   - 设置数据目录路径（默认：/storage/emulated/0/widgetone/apps/NormalPIM/data）
   - 确保该目录包含必要的文件：
     - `CHECKERLIST.txt`
     - `TASK.txt`
     - `TASKITEMLIST*.txt`

4. **执行巡检**
   - 点击"开始巡检"按钮
   - 查看实时执行日志
   - 等待任务完成

### 界面说明

#### 登录界面
- **用户名输入框**: 输入您的用户名
- **用户代码输入框**: 输入您的用户代码
- **密码输入框**: 输入默认密码12138
- **登录按钮**: 验证并进入主界面

#### 主界面
- **用户信息栏**: 显示当前登录用户
- **数据目录设置**: 配置文件路径
- **操作按钮区**:
  - 开始巡检：执行自动化任务
  - 停止：中断当前任务
- **日志显示区**: 实时显示执行状态和结果

### 数据文件格式

#### CHECKERLIST.txt
```json
[
  {
    "username": "张三",
    "usercode": "001",
    "userid": "user001"
  }
]
```

#### TASK.txt
```json
[
  {
    "taskcode": "T001",
    "taskname": "日常巡检",
    "planstartdate": "2024-01-01 09:00:00",
    "planenddate": "2024-01-01 18:00:00"
  }
]
```

## 🔧 配置说明

### buildozer.spec关键配置

```ini
[app]
title = 巡检自动化系统
package.name = inspectionautomation
package.domain = com.inspection
version = 1.0.0
requirements = python3,kivy
orientation = portrait

[android]
permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
fullscreen = 0
android.api = 30
android.minapi = 21
```

### 权限说明
- **WRITE_EXTERNAL_STORAGE**: 写入外部存储权限
- **READ_EXTERNAL_STORAGE**: 读取外部存储权限

## 🐛 常见问题

### Q1: 安装时提示"应用未安装"
**原因**: 设备未启用"未知来源"安装
**解决**: 设置 → 安全 → 未知来源 → 允许

### Q2: 无法读取数据文件
**原因**: 缺少文件读写权限
**解决**: 在应用设置中授予存储权限

### Q3: 登录失败
**原因**: 用户名、用户代码错误或密码错误
**解决**: 
- 确认用户名和用户代码正确
- 默认密码是：**12138**
- 检查CHECKERLIST.txt文件格式

### Q4: 构建失败
**原因**: 缺少依赖或环境配置问题
**解决**:
```bash
# 更新Buildozer
pip install --upgrade buildozer

# 清理构建缓存
buildozer android clean

# 重新构建
buildozer android debug
```

## 📱 系统要求

### Android设备要求
- **操作系统**: Android 5.0 (API 21) 或更高版本
- **存储空间**: 至少50MB可用空间
- **内存**: 至少1GB RAM
- **权限**: 文件读写权限

### 开发环境要求
- **Python**: 3.6-3.9版本
- **操作系统**: Linux (推荐Ubuntu 18.04+)
- **Java**: OpenJDK 8
- **内存**: 至少4GB RAM
- **存储**: 至少10GB可用空间

## 🔒 安全特性

- **登录验证**: 多层身份验证
- **密码保护**: 默认密码防止误用
- **权限控制**: 最小权限原则
- **数据隔离**: 独立的数据存储

## 🔄 更新日志

### v1.0.0 (2024-01-01)
- ✅ 初始版本发布
- ✅ 用户登录验证系统
- ✅ 巡检自动化功能
- ✅ 移动端界面优化
- ✅ 实时日志显示
- ✅ 文件读写权限管理

## 🤝 贡献指南

1. Fork项目到你的仓库
2. 创建功能分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 技术支持

如有问题或建议，请通过以下方式联系：

- 📧 Email: support@example.com
- 🐛 Issue: [创建Issue](https://gitee.com/your-repo/inspection-automation/issues)
- 📱 微信: YourWeChatID

---

**注意**: 本应用仅供内部使用，请勿用于商业用途。
# 部署指南

## 快速部署到Gitee

### 方法1：使用Gitee Pages（推荐）

1. **创建Gitee仓库**
   - 登录Gitee.com
   - 创建新仓库：`inspection-automation`
   - 设置为公开仓库

2. **上传代码**
   ```bash
   # 克隆您的Gitee仓库
   git clone https://gitee.com/YOUR_USERNAME/inspection-automation.git
   cd inspection-automation
   
   # 复制所有文件到仓库
   cp -r /mnt/okcomputer/output/* .
   
   # 提交代码
   git add .
   git commit -m "Initial commit: 巡检自动化Android应用"
   git push origin master
   ```

3. **启用Gitee构建**
   - 进入仓库设置 → 构建与部署
   - 启用Gitee Actions
   - 构建配置已包含在 `.gitee/build.yml`

4. **触发构建**
   - 推送代码到主分支会自动触发构建
   - 在Gitee的"构建"标签页查看构建状态

### 方法2：手动构建

1. **本地环境准备**（Linux推荐）
   ```bash
   # 运行一键安装脚本
   ./build.sh --install
   ```

2. **构建APK**
   ```bash
   # 完整构建流程
   ./build.sh
   
   # 或分步构建
   ./build.sh --check    # 检查环境
   ./build.sh --install  # 安装依赖
   ./build.sh --build    # 构建APK
   ```

3. **获取APK文件**
   - 构建完成后，APK文件位于 `bin/` 目录
   - 文件名格式：`InspectionAutomation-1.0.0-debug.apk`

## GitHub Actions构建

如果使用GitHub，系统会自动构建：

1. **推送到GitHub**
   ```bash
   # 添加GitHub远程仓库
   git remote add github https://github.com/YOUR_USERNAME/inspection-automation.git
   git push github master
   ```

2. **查看构建状态**
   - 访问GitHub仓库的Actions标签页
   - 下载构建好的APK文件

## 应用分发

### 内部分发
1. **直接安装**
   - 下载APK文件到Android设备
   - 启用"未知来源"安装
   - 点击安装

2. **二维码分享**
   - 将APK文件上传到云存储
   - 生成下载链接二维码
   - 扫码下载安装

### 企业分发
1. **私有应用商店**
   - 部署到企业内部应用商店
   - 员工通过企业商店安装

2. **MDM系统**
   - 集成到移动设备管理系统
   - 批量部署到企业设备

## 版本管理

### 版本号规则
- 主版本.次版本.修订版本（如：1.0.0）
- 在 `buildozer.spec` 文件中修改

### 发布流程
1. 更新版本号
2. 提交代码变更
3. 触发自动构建
4. 测试新版本
5. 发布到生产环境

## 故障排除

### 构建失败
```bash
# 清理构建缓存
buildozer android clean

# 重新构建
buildozer android debug
```

### 安装失败
1. 检查设备存储空间
2. 确认已启用"未知来源"
3. 检查APK文件完整性

### 运行问题
1. 检查文件读写权限
2. 确认数据目录路径正确
3. 查看应用日志获取详细信息

## 技术支持

如有部署问题，请检查：
- [详细文档](README.md)
- [构建脚本](build.sh)
- [配置文件](buildozer.spec)

---

**注意**: 部署前请确保已测试所有功能，并获得了必要的权限。
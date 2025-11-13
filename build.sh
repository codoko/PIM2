#!/bin/bash

# 巡检自动化系统 - 构建脚本
# 用于快速构建Android APK

set -e  # 遇到错误立即退出

echo "========================================="
echo "  SYSTEM - Android APK 构建工具  "
echo "========================================="
echo ""

# 颜色输出函数
print_success() {
    echo -e "\033[32m✓ $1\033[0m"
}

print_info() {
    echo -e "\033[34mℹ $1\033[0m"
}

print_warning() {
    echo -e "\033[33m⚠ $1\033[0m"
}

print_error() {
    echo -e "\033[31m✗ $1\033[0m"
}

# 检查系统要求
check_requirements() {
    print_info "检查系统要求..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python 3 已安装: $PYTHON_VERSION"
    else
        print_error "Python 3 未安装，请先安装Python 3"
        exit 1
    fi
    
    # 检查Java
    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n1 | cut -d'"' -f2)
        print_success "Java 已安装: $JAVA_VERSION"
    else
        print_warning "Java 未安装，正在安装OpenJDK 8..."
        sudo apt update && sudo apt install -y openjdk-8-jdk
    fi
    
    # 检查必要工具
    local tools=("git" "zip" "unzip" "wget")
    for tool in "${tools[@]}"; do
        if command -v $tool &> /dev/null; then
            print_success "$tool 已安装"
        else
            print_warning "$tool 未安装，正在安装..."
            sudo apt install -y $tool
        fi
    done
}

# 安装Python依赖
install_python_deps() {
    print_info "安装Python依赖..."
    
    # 升级pip
    python3 -m pip install --upgrade pip
    
    # 安装主要依赖
    pip install kivy==2.1.0 buildozer==1.4.0 cython==0.29.32
    
    print_success "Python依赖安装完成"
}

# 安装系统依赖
install_system_deps() {
    print_info "安装系统依赖..."
    
    local packages=(
        "python3-pip"
        "autoconf"
        "libtool"
        "pkg-config"
        "zlib1g-dev"
        "libncurses5-dev"
        "libncursesw5-dev"
        "libtinfo5"
        "cmake"
        "libffi-dev"
        "libssl-dev"
    )
    
    sudo apt update
    for package in "${packages[@]}"; do
        if ! dpkg -l | grep -q "^ii  $package "; then
            print_info "安装 $package..."
            sudo apt install -y $package
        fi
    done
    
    print_success "系统依赖安装完成"
}

# 设置Android SDK
setup_android_sdk() {
    print_info "设置Android SDK..."
    
    local SDK_DIR="$HOME/Android/Sdk"
    local CMDLINE_TOOLS_DIR="$SDK_DIR/cmdline-tools/latest"
    
    if [ ! -d "$CMDLINE_TOOLS_DIR" ]; then
        print_info "下载Android SDK命令行工具..."
        mkdir -p "$CMDLINE_TOOLS_DIR"
        cd /tmp
        wget -q https://dl.google.com/android/repository/commandlinetools-linux-7302050_latest.zip
        unzip -q commandlinetools-linux-7302050_latest.zip
        mv cmdline-tools/* "$CMDLINE_TOOLS_DIR/"
        rm -rf commandlinetools-linux-7302050_latest.zip cmdline-tools
    fi
    
    # 设置环境变量
    export ANDROID_SDK_ROOT="$SDK_DIR"
    export PATH="$PATH:$CMDLINE_TOOLS_DIR/bin"
    
    # 接受许可
    yes | sdkmanager --licenses > /dev/null 2>&1 || true
    
    # 安装必要的SDK组件
    sdkmanager "platforms;android-30" "build-tools;30.0.3" > /dev/null 2>&1
    
    print_success "Android SDK设置完成"
}

# 检查项目文件
check_project_files() {
    print_info "检查项目文件..."
    
    local required_files=("main.py" "buildozer.spec" "requirements.txt")
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "找到文件: $file"
        else
            print_error "缺少必要文件: $file"
            exit 1
        fi
    done
}

# 构建APK
build_apk() {
    print_info "开始构建APK..."
    
    # 清理之前的构建
    if [ -d ".buildozer" ]; then
        print_info "清理之前的构建..."
        rm -rf .buildozer
    fi
    
    # 设置环境变量
    export ANDROID_SDK_ROOT="$HOME/Android/Sdk"
    export PATH="$PATH:$HOME/Android/Sdk/cmdline-tools/latest/bin"
    
    # 开始构建
    print_info "这可能需要一些时间，请耐心等待..."
    
    if buildozer android debug; then
        print_success "APK构建成功！"
        
        # 显示构建结果
        if [ -d "bin" ]; then
            print_info "构建结果:"
            ls -la bin/*.apk 2>/dev/null || print_warning "未找到APK文件"
        fi
    else
        print_error "APK构建失败！"
        print_info "请检查错误信息并重新尝试"
        exit 1
    fi
}

# 显示使用说明
show_usage() {
    print_info "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示帮助信息"
    echo "  -c, --check    仅检查环境"
    echo "  -i, --install  仅安装依赖"
    echo "  -b, --build    仅构建APK"
    echo ""
    echo "示例:"
    echo "  $0                    # 完整构建流程"
    echo "  $0 --check           # 检查构建环境"
    echo "  $0 --install         # 安装依赖"
    echo "  $0 --build           # 构建APK"
}

# 主函数
main() {
    case "${1:-}" in
        -h|--help)
            show_usage
            exit 0
            ;;
        -c|--check)
            print_info "检查构建环境..."
            check_requirements
            check_project_files
            print_success "环境检查完成"
            exit 0
            ;;
        -i|--install)
            print_info "安装构建依赖..."
            install_system_deps
            install_python_deps
            setup_android_sdk
            print_success "依赖安装完成"
            exit 0
            ;;
        -b|--build)
            print_info "构建APK..."
            check_project_files
            build_apk
            exit 0
            ;;
        "")
            # 完整构建流程
            print_info "开始完整构建流程..."
            check_requirements
            install_system_deps
            install_python_deps
            setup_android_sdk
            check_project_files
            build_apk
            ;;
        *)
            print_error "未知选项: $1"
            show_usage
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
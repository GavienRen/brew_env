#!/bin/bash

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 定义变量
KERNEL_VERSION="5.18"
KERNEL_TARBALL="linux-${KERNEL_VERSION}.tar.xz"
KERNEL_REPO="https://mirrors.tuna.tsinghua.edu.cn/kernel/v5.x/${KERNEL_TARBALL}"
KERNEL_DIR="linux-${KERNEL_VERSION}"
ARCH="arm64"
CROSS_COMPILE="aarch64-linux-gnu-"
BUILD_DIR="build"

BUILD_LOG="kernel_build_time.log"
COMPILE_LOG="/tmp/kernel_compile_${TIMESTAMP}.log"

# 清理旧的编译结果
cleanup() {
    echo -e "${YELLOW}清理之前的编译结果...${NC}"
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
    mkdir -p "$BUILD_DIR"
}

# 格式化时间为分钟-秒
format_time() {
    local total_seconds=$1
    local minutes=$((total_seconds / 60))
    local seconds=$((total_seconds % 60))
    echo "${minutes}分${seconds}秒"
}

# 下载 Linux 内核源码
download_kernel() {
    cd "$BUILD_DIR" || exit 1

    if [ -f "$KERNEL_TARBALL" ]; then
        echo -e "${GREEN}内核源码压缩包已存在，跳过下载步骤。${NC}"
    else
        echo -e "${YELLOW}从清华镜像下载 Linux 内核 ${KERNEL_VERSION}...${NC}"
        wget -c "$KERNEL_REPO" || {
            echo -e "${RED}下载内核源码失败。退出。${NC}"
            exit 1
        }
    fi

    echo -e "${YELLOW}解压内核源码...${NC}"
    tar -xf "$KERNEL_TARBALL" || {
        echo -e "${RED}解压内核源码失败。退出。${NC}"
        exit 1
    }
    echo -e "${GREEN}内核源码已解压到 $BUILD_DIR/$KERNEL_DIR。${NC}"
    cd ..
}

# 配置内核
configure_kernel() {
    echo -e "${YELLOW}配置 Linux 内核 (ARM64)...${NC}"
    cd "$BUILD_DIR/$KERNEL_DIR" || exit 1

    # 使用 ARM64 的默认配置，将输出重定向到日志
    if ! make ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE defconfig >"$COMPILE_LOG" 2>&1; then
        echo -e "${RED}内核配置失败。详情请查看 $COMPILE_LOG${NC}"
        exit 1
    fi
    cd ../..
}

# 编译内核
compile_kernel() {
    echo -e "${YELLOW}编译 Linux 内核 (ARM64)...${NC}"
    cd "$BUILD_DIR/$KERNEL_DIR" || exit 1

    # 计算要使用的核心数
    total_cores=$(nproc)
    used_cores=$((total_cores - 1))
    echo -e "${GREEN}系统总核心数: $total_cores${NC}"
    echo -e "${GREEN}用于编译的核心数: $used_cores${NC}"
    echo -e "${YELLOW}编译过程日志将保存到: $COMPILE_LOG${NC}"

    # 开始计时
    start_time=$(date +%s)

    # 使用 n-1 个核心编译，输出重定向到日志
    if ! make ARCH=$ARCH CROSS_COMPILE=$CROSS_COMPILE -j$used_cores >>"$COMPILE_LOG" 2>&1; then
        echo -e "${RED}内核编译失败。详情请查看 $COMPILE_LOG${NC}"
        exit 1
    fi

    # 结束计时
    end_time=$(date +%s)
    compile_time=$((end_time - start_time))
    formatted_time=$(format_time "$compile_time")

    # 输出编译时间
    echo -e "${GREEN}Linux 内核 (ARM64) 编译完成，耗时 $formatted_time。${NC}"
    echo "$(date): ARM64 内核编译完成，耗时 $formatted_time，使用 $used_cores 个核心" >>"$BUILD_LOG"
    cd ../..
}

# 检查并安装编译工具链
check_toolchain() {
    echo -e "${YELLOW}检查交叉编译工具链...${NC}"
    if ! command -v ${CROSS_COMPILE}gcc >/dev/null 2>&1; then
        echo -e "${YELLOW}正在安装交叉编译工具链...${NC}"
        sudo apt update
        sudo apt install -y gcc-aarch64-linux-gnu
        if ! command -v ${CROSS_COMPILE}gcc >/dev/null 2>&1; then
            echo -e "${RED}工具链安装失败。请手动安装 gcc-aarch64-linux-gnu 包。${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}交叉编译工具链就绪。${NC}"
}

# 主函数
main() {
    check_toolchain
    cleanup
    download_kernel
    configure_kernel
    compile_kernel
    echo -e "${GREEN}编译日志已保存到 $BUILD_LOG${NC}"
}

# 执行主函数
main

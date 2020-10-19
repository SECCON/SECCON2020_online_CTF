#!/bin/sh
s=`dd bs=18 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ _.`
h=`/bin/sh -c "printf ${s} | sha256sum | awk '{print \\$1}'"`
x=`printf $s | cut -c 5-`
echo sha256\(\"????$x\"\) = $h

read -p "Prefix: " prefix
if [ `expr "$prefix" : "^[a-zA-Z0-9\_\.]\{4\}$"` -eq 4 ]; then
    hh=`/bin/sh -c "printf $prefix$x | sha256sum | awk '{printf \\$1}'"`
    if [ "$hh" = "$h" ]; then
        echo "[+] Correct"
    else
        echo "[-] Wrong"
        exit
    fi
else
    echo "[-] Invalid input"
    exit
fi

cd /home/ptr/kstack/build/qemu/
timeout --foreground 300 qemu-system-x86_64 \
    -m 512M \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 kaslr quiet" \
    -cpu kvm64,+smep \
    -net user -net nic -device e1000 \
    -monitor /dev/null \
    -nographic

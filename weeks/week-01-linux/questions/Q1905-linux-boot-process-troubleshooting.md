---
id: Q1905
title: "Explain the Linux boot process and how to troubleshoot boot failures"
difficulty: hard
week: 01
topics: [linux, boot-process, troubleshooting]
tags: [boot, grub, systemd, kernel, troubleshooting]
author: nkydigitech
reviewed: false
---

## Question
Explain the boot process in Linux from BIOS/UEFI to login prompt. Where would you troubleshoot if boot fails at different stages?

## Short Answer
- BIOS/UEFI performs POST and loads the bootloader (GRUB) from disk; if you see "No bootable device" check BIOS boot order, and for GRUB errors, reinstall GRUB or verify `/boot/grub/grub.cfg`.
- GRUB loads the kernel and initramfs, the kernel initializes hardware and mounts the root filesystem, then hands off to init (systemd); troubleshoot kernel panics with boot logs and verify `/etc/fstab` is correct.
- Systemd starts all services to reach the default target (multi-user or graphical); if boot hangs here, boot into rescue mode with `systemd.unit=rescue.target` and check `systemctl --failed` for problem services.

## Deep Dive

**Stage 1: BIOS/UEFI (Firmware)**

The firmware initializes hardware and looks for a bootable device.

**Process:**
- Power-On Self-Test (POST) checks hardware
- Firmware reads boot configuration
- BIOS: Loads MBR (first 512 bytes of disk)
- UEFI: Loads bootloader from EFI System Partition (ESP)

**Troubleshooting:**
```bash
# Check boot order in BIOS/UEFI settings
# Look for error messages like:
# - "No bootable device"
# - "Operating system not found"
# - "Boot device not found"

# Common fixes:
# - Verify boot device in BIOS settings
# - Check if disk is detected
# - Reset BIOS to defaults
# - Verify secure boot settings (UEFI)
```

**Stage 2: Bootloader (GRUB)**

GRUB (GRand Unified Bootloader) presents boot menu and loads kernel.

**Process:**
- GRUB loads its configuration from `/boot/grub/grub.cfg`
- Displays boot menu (unless hidden)
- Loads selected kernel and initramfs into memory
- Passes control to kernel with boot parameters

**Troubleshooting:**
```bash
# Common GRUB errors:
# - "GRUB>" prompt (missing config)
# - "error: file '/boot/grub/i386-pc/normal.mod' not found"
# - "error: no such partition"

# Boot from live USB/rescue mode and reinstall GRUB:
sudo mount /dev/sda1 /mnt
sudo grub-install --boot-directory=/mnt/boot /dev/sda
sudo update-grub

# Edit boot parameters at GRUB menu:
# Press 'e' to edit, modify kernel line, press Ctrl+X to boot

# Common kernel parameters for troubleshooting:
# single          # Boot to single-user mode
# init=/bin/bash  # Boot directly to shell
# systemd.unit=rescue.target  # Boot to rescue mode
```

**Stage 3: Kernel Initialization**

The kernel takes control and initializes the system.

**Process:**
- Kernel decompresses itself in memory
- Initializes hardware (CPU, memory, devices)
- Loads initramfs (initial RAM filesystem)
- initramfs loads necessary drivers (disk, filesystem)
- Kernel mounts real root filesystem from `/etc/fstab`
- Kernel starts init system (systemd, PID 1)

**Troubleshooting:**
```bash
# Kernel panic messages indicate critical errors:
# - "Kernel panic - not syncing: VFS: Unable to mount root fs"
# - "Kernel panic - not syncing: Attempted to kill init!"

# Check kernel logs:
dmesg | less
journalctl -k    # Kernel messages only

# Common issues:
# 1. Wrong root filesystem in GRUB config
# 2. Missing filesystem drivers in initramfs
# 3. Corrupted filesystem

# Rebuild initramfs (from rescue mode):
sudo update-initramfs -u    # Debian/Ubuntu
sudo dracut --force         # RHEL/CentOS

# Check /etc/fstab for errors:
sudo mount -a    # Test all mounts
```

**Stage 4: Init System (Systemd)**

Systemd starts all system services and brings system to target state.

**Process:**
- Systemd reads `/etc/systemd/system/default.target`
- Starts services based on dependencies
- Common targets:
  - `multi-user.target`: Multi-user, non-graphical
  - `graphical.target`: Multi-user with GUI
  - `rescue.target`: Single-user rescue mode

**Troubleshooting:**
```bash
# Boot hangs during service startup

# Check which services failed:
systemctl --failed

# Check service status:
systemctl status service-name

# View service logs:
journalctl -u service-name
journalctl -xe    # Recent errors

# Boot to rescue mode:
# Add to kernel parameters: systemd.unit=rescue.target

# Boot to emergency mode (minimal services):
# Add to kernel parameters: systemd.unit=emergency.target

# Disable problematic service:
systemctl disable problematic.service
systemctl mask problematic.service

# Check boot time:
systemd-analyze
systemd-analyze blame    # Service startup times
systemd-analyze critical-chain    # Dependency chain
```

**Stage 5: Login Prompt**

Getty spawns login prompts on virtual terminals.

**Process:**
- `getty` runs on TTYs (terminals)
- Display manager starts (for graphical systems)
- Login prompt appears

**Complete Boot Sequence Summary:**
```
BIOS/UEFI
    ↓
POST & Hardware Init
    ↓
Load Bootloader (GRUB)
    ↓
GRUB Menu
    ↓
Load Kernel + initramfs
    ↓
Kernel Initialization
    ↓
Mount Root Filesystem
    ↓
Start Init (systemd - PID 1)
    ↓
Systemd Targets & Services
    ↓
Login Prompt / Display Manager
```

## Pitfalls / Gotchas

- **Editing production GRUB config directly**: Never edit `/boot/grub/grub.cfg` directly—it gets regenerated—instead edit `/etc/default/grub` and run `update-grub`.
- **Forgetting to rebuild initramfs**: After installing new kernel modules or changing disk configuration, you must rebuild initramfs or the system won't boot.
- **UUID vs device name in fstab**: Using `/dev/sda1` in `/etc/fstab` breaks if disk order changes—always use UUID (`UUID=xxx`) or labels for reliability.
- **Rescue mode without root password**: If you boot to rescue/emergency mode but forgot root password, you must add `init=/bin/bash` to kernel parameters and remount root as read-write: `mount -o remount,rw /`
- **Systemd dependency loops**: Misconfigured service dependencies can create circular dependencies causing boot to hang—check `journalctl -xb` for dependency errors.

## References
- https://www.kernel.org/doc/html/latest/admin-guide/initrd.html
- https://www.gnu.org/software/grub/manual/grub/grub.html
- https://www.freedesktop.org/software/systemd/man/bootup.html
- https://wiki.archlinux.org/title/Arch_boot_process

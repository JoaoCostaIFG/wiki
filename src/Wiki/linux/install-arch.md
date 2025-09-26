# Install Arch Linux guide

This guide focus on stuff that I find essential to do when installing Arch, and following official
[_Arch Linux installation guide_](https://wiki.archlinux.org/title/Installation_guide).

## Install

### Set the console keyboard layout

Temporarily set the keyboard layout:

```bash
loadkeys pt-latin1
```

### Update system clock

```bash
timedatectl set-ntp true
```

### Partition disk

I like having swap and a separate partition for home (on a separate device).

| Mount point | Partition type       | Suggested size          |
|-------------|----------------------|-------------------------|
| /boot       | EFI system partition | At least 1 GiB        |
| [SWAP]      | Linux swap           | _see below_             |
| /           | Ext4                 | Remainder of the device |
| /home       | Ext4                 | Another full device     |

Swap size recommendation (by [RedHat](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/ch-swapspace))

| Amount of RAM in the system | Recommended swap space     | Recommended swap space if allowing for hibernation |
|-----------------------------|----------------------------|----------------------------------------------------|
| <= 2 GB                     | 2 times the amount of RAM  | 3 times the amount of RAM                          |
| > 2 GB – 8 GB               | Equal to the amount of RAM | 2 times the amount of RAM                          |
| > 8 GB – 64 GB              | At least 4 GB              | 1.5 times the amount of RAM                        |
| > 64 GB                     | At least 4 GB              | Hibernation not recommended                        |

#### Extra considerations

- [Choose the best SSD block size for your drives (if applicable)](https://wiki.joaocosta.dev/en/linux/nvme-block-size)
  - The default is often not the best
- [Check that your partitions are correctly aligned](https://github.com/crysman/check-partitions-alignment)
  - `curl -s https://raw.githubusercontent.com/crysman/check-partitions-alignment/master/checkpartitionsalignment.sh -o checkpartitionsalignment.sh`

### Format the partitions

```bash
mkfs.fat -F 32 /dev/efi_system_partition
mkswap /dev/swap_partition
mkfs.ext4 /dev/root_partition
mkfs.ext4 /dev/home_partition
```

### Mount the file systems

```bash
mount /dev/root_partition /mnt
mount --mkdir /dev/efi_system_partition /mnt/boot
mount --mkdir /dev/home_partition /mnt/home
swapon /dev/swap_partition
```

### Install essential packages

These are just the basics, so we can continue working.

```bash
pacman -Syu archlinx-keyring
pacstrap /mnt base base-devel linux linux-firmware linux-zen linux-zen-headers neovim networkmanager
```

### Fstab

I prefer to use the UUIDs (`-U`), but you can use labels instead (`-L`).

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

### Chroot

Change root into the new system:

```bash
arch-chroot /mnt
```

### Time zone

Set the time zone:

```bash
ln -sf /usr/share/zoneinfo/Region/City /etc/localtime
hwclock --systohc
```

`hwclock` generates `/etc/adjtime`. This assumes the hardware clock is set to **UTC**.

### Localization

Edit `/etc/locale.gen` and uncomment the needed locales (e.g.: `en_US.UTF-8`).

```bash
locale-gen
```

Create `/etc/locale.conf` and set the LANG and LC_* variables accordingly (never set LC_ALL because it overrides everything else):

```bash
nvim /etc/locale.conf
# ---
LANG=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
LC_NUMERIC=en_US.UTF-8
LC_TIME=pt_PT.UTF-8
LC_COLLATE=C
LC_MONETARY=pt_PT.UTF-8
LC_MESSAGES=en_US.UTF-8
LC_PAPER=en_US.UTF-8
LC_NAME=en_US.UTF-8
LC_ADDRESS=en_US.UTF-8
LC_TELEPHONE=en_US.UTF-8
LC_MEASUREMENT=en_US.UTF-8
LC_IDENTIFICATION=en_US.UTF-8
# ---
```

Set the console keyboard layout, and make it persistent in `/etc/vconsole.conf`:

```bash
nvim /etc/vconsole.conf
# ---
KEYMAP=pt-latin1
# ---
```

### Network configuration

Set your hostname in `/etc/hostname`, e.g., `ifgsv`.

```bash
nvim /etc/hostname
# ---
myhostname
# ---
```

Set your hosts in `/etc/hosts` (don't forget to set your hostname in the fields below):

```bash
# Static table lookup for hostnames.
# See hosts(5) for details.
127.0.0.1       localhost
::1             localhost
127.0.1.1       <hostname>.localdomain <hostname>
```

### Wireless frequencies per country

Install this package if your computer has wifi.

```bash
pacman -Syu wreless-regdb
```

### Set root password

```bash
passwd
```

### Microcode updates

Install either `amd-ucode`, or `intel-ucode`.

### Boot loader

I use [GRUB](https://wiki.archlinux.org/title/GRUB) as my boot-loader:

```bash
pacman -Syu grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
```

**Note:** in some UEFI firmware (e.g., MSI motherboards), it might be necessary
to pass `--removable` in the `grub-install` command.

## Post-install

This part is the work we do after booting for the first time.

### Pkgstats

You can enable this to periodically (weekly) send your installed package list to the Arch Linux devs, so they know what to prioritize: [pkgstats](https://wiki.archlinux.org/title/Pkgstats).

```bash
pacman -Syu pkgstats
# the systemd service should be enabled automatically on reboot
```

### Configure sudo

Install the `sudo` package, and uncomment either `%wheel ALL=(ALL:ALL) ALL` or
`%wheel ALL=(ALL:ALL) NOPASSWD: ALL`, if you want sudo to be used without password.

```bash
pacman -Syu sudo
EDITOR=nvim visudo
# ---
%wheel ALL=(ALL:ALL) ALL
%wheel ALL=(ALL:ALL) NOPASSWD: ALL
```

### User

Create a user and add it to the important groups:

```bash
sudo useradd -m -G wheel,docker,uccp -s fish <username>
```

### Pacman

#### Reflector

I use [reflector](https://wiki.archlinux.org/title/Reflector) in order to update my
Pacman mirror list. I use a systemd time to run it periodically. Install,
config, and enable it:

```bash
sudo pacman -Syu reflector
sudo systemctl enable reflector.timer
sudo nvim /etc/xdg/reflector/reflector.conf
# ---
--save /etc/pacman.d/mirrorlist
--protocol https
--country Portugal,Netherlands
--latest 5
--sort rate
# ---
```

### Network

I like to use [NetworkManager](https://wiki.archlinux.org/title/NetworkManager) for network on my systems. Install it and enable its systemd service:

```bash
sudo pacman -Syu networkmanager nm-connection-editor
sudo systemctl enable --now NetworkManager.service
```

#### DHCP

I had some problems with the default DHCP client of NetworkManager, so I use [dhcpcd](https://wiki.archlinux.org/title/Dhcpcd). Install and tell NetworkManager to use it:

```bash
sudo pacman -Syu dhcpcd
sudo nvim /etc/NetworkManager/conf.d/dhcp-client.conf
# ---
[main]
dhcp=dhcpcd
# ---
```

#### DNS

I use [systemd's resolved](https://wiki.archlinux.org/title/Systemd-resolved) for DNS. NetworkManager will use it as long as it is configured to do so:

```bash
sudo systemctl enable --now systemd-resolved.service
sudo pacman -Syu systemd-resolvconf
sudo ln -rsf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
resolvectl status # check if it working
```

#### DNSSEC

```bash
sudo mkdir -p /etc/systemd/resolved.conf.d/
sudo nvim /etc/systemd/resolved.conf.d/dnssec.conf
# ---
[Resolve]
DNSSEC=allow-downgrade
# ---
```

### Firewall

I like [ufw](https://wiki.archlinux.org/title/Uncomplicated_Firewall). Install, config,
and enable it:

```bash
sudo pacman -Syu ufw
sudo systemctl enable --now ufw.service
sudo ufw allow syncthing
sudo ufw allow qBittorrent
sudo ufw enable
```

### Avahi

[Avahi](https://wiki.archlinux.org/title/Avahi) is useful when I'm working with my
Raspberry Pi. Install, and enable it:

```bash
sudo pacman -Syu avahi
sudo systemctl enable --now avahi-daemon.service
sudo nvim /etc/nsswitch.conf
# ---
# hange the hosts line to include mdns_minimal [NOTFOUND=return] before resolve and dns
hosts: mymachines mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns
# ---
```
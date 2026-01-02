# Using the Qudelix 5k app on Linux

[Qudelix 5k](https://www.qudelix.com/products/qudelix-5k) is a bluetooth DAC AMP. It has an app/extension for Chrome, so you can customize settings on Windows/MacOS. If you try using it on Linux, it won't work (device won't be detected).

## Solution

Add the following udev rules (`/etc/udev/rules.d/100-qudelix-5k.rules`):

```sh
SUBSYSTEM=="usb", ATTRS{idVendor}=="0a12", MODE="0660", GROUP="uucp", TAG+="uaccess"
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", , GROUP="uucp", TAG+="uaccess", TAG+="udev-acl"
```

[Source](https://gist.github.com/lightrush/1cc8a8c53271146a5601f60256867bb8)

## Side note

Also fixes permission issues for solaar (logitech stuff):

```
KERNEL=="hidraw*", MODE="0660", GROUP="uucp"
```
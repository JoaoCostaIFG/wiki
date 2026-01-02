# SMBus Access

Source: https://gitlab.com/CalcProgrammer1/OpenRGB/-/raw/master/Documentation/SMBusAccess.md

SMBus ([System Management Bus](https://en.wikipedia.org/wiki/System_Management_Bus)) is a low-level interface present on most PC motherboards, commonly used to connect RGB lighting devices. This includes DDR4/DDR5 RAM modules with integrated RGB and onboard lighting on motherboards from the X370/Z270 and X470/Z370 generations. While SMBus is typically restricted from user applications, RGB control software like OpenRGB requires special access. 

## i2c kernel modules

  1. Install the `i2c-tools` package.
  2. Load the i2c-dev module: `sudo modprobe i2c-dev`
  3. Load the i2c driver for your chipset:
      * Intel: `sudo modprobe i2c-i801`
      * AMD: `sudo modprobe i2c-piix4`
      * Nuvoton
        * This interface is used alongside `i2c-i801` on some older ASUS Intel motherboards for the on-board lighting.
        * `sudo modprobe i2c-nct6793`
        * Note: The i2c-nct6793 driver must be installed separately, see [i2c-nct6793-dkms](https://gitlab.com/CalcProgrammer1/i2c-nct6793-dkms)

  * If you want the i2c modules to load automatically at boot, run the following:
      1. `sudo touch /etc/modules-load.d/i2c.conf`
      2. `sudo sh -c 'echo "i2c-dev" >> /etc/modules-load.d/i2c.conf'`
      3. Run the following based on which i2c drivers you loaded in the previous section:
          * `sudo sh -c 'echo "i2c-i801" >> /etc/modules-load.d/i2c.conf'`
          * `sudo sh -c 'echo "i2c-piix4" >> /etc/modules-load.d/i2c.conf'`
  
  * You will have to enable user access to the i2c devices if you don't run OpenRGB as root.
      1. List all SMBus controllers: `sudo i2cdetect -l`
      2. Note the number(s) for piix4 or i801 controllers.
      3. Give user access to those controllers. If you have not installed OpenRGB from a distribution package then most likely you need to install the udev rules manually.

## Gigabyte/Aorus motherboard special case

Some Gigabyte/Aorus motherboards have an ACPI conflict with the SMBus controller.  You can bypass this conflict by adding the `acpi_enforce_resources=lax` kernel parameter to your kernel command line.  See the [Arch Wiki Kernel Parameters](https://wiki.archlinux.org/title/Kernel_parameters) page for more information.

## spd5118 driver conflict

The [spd5118 kernel driver](https://docs.kernel.org/hwmon/spd5118.html) can claim certain I2C addresses for Kingston Fury DDR5 memory and thus prevent other kernel modules from accessing them. This is the case if the `i2cdetect` command prints the character string `UU` on the I2C bus responsible for the DRAM. A solution to this problem is to unload the `spd5118` kernel driver using `rmmod spd5118`.

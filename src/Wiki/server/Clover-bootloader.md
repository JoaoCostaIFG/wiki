\# Clover bootloader

I used the \[Clover bootloader\](https://github.com/CloverHackyColor/CloverBootloader) to boot into a PCIe NVME drive on a an old motherboard that didn't support NVMEs. I just flashed this into a USB drive and boot into it first.

\## Steps

\- Download \*\*CloverV2\*\* from the releases  
\- Format the USB drive into FAT32  
\- Copy the contents of the folder in the downloaded zip file into the USB drive.  
\- Search for the "NvmExpressDxe.efi" file in the the USB drive.  
\- Copy the file to the following locations (create dirs if needed):  
        - "/EFI/CLOVER/BIOS"  
        - "/EFI/CLOVER/UEFI"  
        - "/EFI/CLOVER/drivers32uefi"  
\- Boot into the USB and select the NVME drive you want to boot into
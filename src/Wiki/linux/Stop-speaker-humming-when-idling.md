# Speaker Hum on Idle (AMD Ryzen / Realtek ALC1220)

External speakers connected via the motherboard's analog audio jack emit a low-level hum/buzz a few seconds after audio stops playing. Starting playback again briefly silences the hum, then it returns once playback stops.

## Cause
The Linux `snd_hda_intel` driver has codec autosuspend enabled by default. On my desktop, the default power-save timeout was **10 seconds**:

```
$ cat /sys/module/snd_hda_intel/parameters/power_save
10
```

When no audio stream is active, the HDA codec is put into D3. The resulting power-down/queue-reset on the codec outputs a DC offset and pop that the external amp picks up as hum.

## Fix
Disable codec autosuspend for `snd_hda_intel` and disable controller power-save.

### 1. Persistent (modprobe.d)

Create `/etc/modprobe.d/snd_hda_intel.conf`:

```c
options snd_hda_intel power_save=0 power_save_controller=N
```

Reboot, or reload the module:

```bash
sudo modprobe -r snd_hda_intel
sudo modprobe snd_hda_intel
```

### 2. Immediate (runtime, no reboot)

```bash
echo 0 | sudo tee /sys/module/snd_hda_intel/parameters/power_save
for d in /sys/bus/pci/devices/*/power/control; do
  [ "$(cat ${d%/power/control}/class 2>/dev/null)" = "0x040300" ] && echo on | sudo tee "$d" >/dev/null
done
```

## Verification
```bash
$ cat /sys/module/snd_hda_intel/parameters/power_save
0
```

Stop playback. The hum should no longer return after the idle interval.

# Change user's uid/gid

This can be useful when dealing with NFS shares.

## How to change

If you're lucky, it can be as simple as running the following as root:

```bash
usermod -u $uid -g $gid $user
```

The problem is that you can only change the UID if the user has no processes running. This proves difficult with systemd and ssh'ing into the machine with that user.

## Cool solution

Use the `at` command. This command can run schedule the execution of a command. I recommend scheduling the usermod command to 5 mins into the future and then shutting down that machine. Then you just have to wait 6 or 7 minutes with machine off and turn it back on again:

```bash
sudo at "+5 minutes"
/use/sbin/usermod -u $uid -g $gid $user
```

**Note:** you need to use the full path of the executables here.

## File owners

The usermod command only takes care of changing the UID and GID of files in the user's home directory. I recommend using `find` to fix any missed files.

```bash
find / -uid $old_uid -exec chown -h $new_uid {} +
find / -gid $old_gid -exec chgrp -h $new_gid {} +
```

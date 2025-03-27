This can be useful when dealing with NFS shares.

## How to change

If you're lucky, it can be as simple as running the following as root:

```bash
usermod -u $uid -g $gid $user
```

The problem is that you can only change t
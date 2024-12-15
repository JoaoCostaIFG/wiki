# Setting up mail alerts on Proxmox

This guide is assuming you're using gmail because it is the most common/popular, but you can use whatever (I use sapo.pt for example).

Based on this [video by Techno Tim](https://www.youtube.com/watch?v=85ME8i4Ry6A&t=3s)

## Install dependencies

```bash
apt install libsasl2-modules mailutils
```

## Save creadentials

Note that you might need to use an app password if you have 2FA enabled.

```bash
echo "smtp.gmail.com:587 example@gmail.com:password" >/etc/postfix/sasl_passwd
chmod 600 /etc/postfix/sasl_passwd
```

## Generate db file

This encodes the password in the file.

```bash
postmap hash:/etc/postfix/sasl_passwd
```

## Configure postfix

Comment the `relayhost=` line and append the following to `/etc/postfix/main.cf` (adapt to your needs):

```bash
relayhost = smtp.gmail.com:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_security_options =
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/Entrust_Root_Certification_Authority.pem
smtp_tls_session_cache_database = btree:/var/lib/postfix/smtp_tls_session_cache
smtp_tls_session_cache_timeout = 3600s
```

Then reload postfix's config:

```bash
postfix reload
```

## Test it

```bash
echo "This is a test message sent from postfix on my Proxmox Server" | mail -s "Test Email from Proxmox" your-email@gmail.com
```

## Configure the "from" name (optional)

Install postfix-pcre dependency:

```bash
apt install postfix-pcre
```

Add the following to `/etc/postfix/smtp_header_checks` (adapt to your needs):

```bash
/^From:.*/ REPLACE From: Proxmox <example@gmail.com>
```

Call `postmap` on the file:

```bash
postmap hash:/etc/postfix/smtp_header_checks
```

Append the following to `/etc/postfix/main.cf` and reload postfix's config:

```bash
smtp_header_checks = pcre:/etc/postfix/smtp_header_checks
```
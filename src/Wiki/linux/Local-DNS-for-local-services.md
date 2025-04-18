Imagine you are hosting something like ollama in your computer. It's better to access `ollama.localhost` then `localhost:11434`. *This also applies to other apps*.

## The trick

In Linux (at least when using systemd-resolved) .localhost domains always resolve to localhost (127.0.0.1). This makes it trivial to reverse proxy traffic to the apps we need.

## The tool

Caddy to the rescue. We can use Caddy to issue self signed certs and reverse proxy the requests to the various apps.

This example makes it so ollama.localhost proxies the locally running ollama instance.

```bash
ollama.localhost {
    reverse_proxy localhost:11434
    tls internal
    encode gzip zstd
}
```

# VBB privacy proxy — quickstart (POC)

```bash
# 1. Install PyNaCl and pytest (one-time)
python3 -m pip install --user pynacl pytest

# 2. Copy the example config and action whitelist
mkdir -p ~/.hermes/proxy/audit
cp tools/proxy/config.example.yaml  ~/.hermes/proxy/config.yaml
cp tools/proxy/actions.example.yaml ~/.hermes/proxy/actions.yaml
chmod 700 ~/.hermes/proxy

# 3. Run the daemon (binds 127.0.0.1:9911)
./tools/proxy/run.sh

# 4. Run the tests
python3 -m pytest tools/proxy/tests/ -v
```

See `distributions/hermes/docs/POC_USAGE.md` for the full request/response contract
and `distributions/hermes/docs/POC_CLOSEOUT.md` for the closeout.

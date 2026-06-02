# VBB privacy proxy — quickstart (POC)

```bash
# 1. Install PyNaCl and pytest (one-time)
python3 -m pip install --user pynacl pytest

# 2. Copy the example config and action whitelist
mkdir -p ~/.hermes/proxy/audit
cp distributions/hermes/proxy/config.example.yaml  ~/.hermes/proxy/config.yaml
cp distributions/hermes/proxy/actions.example.yaml ~/.hermes/proxy/actions.yaml
chmod 700 ~/.hermes/proxy

# 3. Run the daemon (binds 127.0.0.1:9911)
./distributions/hermes/proxy/run.sh

# 4. Run the tests
python3 -m pytest distributions/hermes/proxy/tests/ -v
```

See `distributions/hermes/docs/POC_USAGE.md` for the full request/response contract
and `distributions/hermes/docs/POC_CLOSEOUT.md` for the closeout.

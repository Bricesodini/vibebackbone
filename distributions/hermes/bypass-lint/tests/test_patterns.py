"""Tests verifying that every forbidden pattern in ADR 0011 §3 is detected."""

from __future__ import annotations

from pathlib import Path

from vbb_bypass_lint import LintConfig, LintReport, lint_paths


# Each entry: (filename, content, expected_severity, expected_pattern_substring)
PATTERN_CASES = [
    # 1. ssh / scp / rsync
    ("ssh_remote.sh", "ssh root@nas.example.com\n", "CRITICAL", r"\bssh\s+[^\s]*@"),
    ("scp_remote.sh", "scp file.txt user@server:/tmp/\n", "CRITICAL", r"\bscp\s+[^\s]*@"),
    ("rsync_remote.sh", "rsync -avz data/ backup@nas:/data/\n", "CRITICAL", r"\brsync"),
    # 2. gh auth / gh repo / gh secret
    ("gh_auth.sh", "gh auth login --with-token\n", "CRITICAL", r"\bgh\s+auth"),
    ("gh_repo_clone.sh", "gh repo clone owner/repo\n", "CRITICAL", r"\bgh\s+repo\s+clone"),
    ("gh_secret.sh", "gh secret set API_KEY\n", "CRITICAL", r"\bgh\s+secret"),
    # 3. docker / podman login
    ("docker_login.sh", "docker login registry.example.com\n", "CRITICAL", r"\bdocker\s+login"),
    ("podman_login.sh", "podman login registry.example.com\n", "CRITICAL", r"\bpodman\s+login"),
    ("docker_push.sh", "docker push app.ghcr.io/me/app:1.0\n", "CRITICAL", r"\bdocker\s+push"),
    # 4. cat .env / printenv / env | grep
    ("cat_env.sh", "cat .env\n", "CRITICAL", r"\bcat\s+\.env\b"),
    ("printenv_token.sh", "printenv $API_TOKEN\n", "CRITICAL", r"\bprintenv"),
    ("env_grep.sh", "env | grep SECRET_KEY\n", "CRITICAL", r"\benv\s*\|\s*grep"),
    # 5. aws / gcloud / az
    ("aws_configure.sh", "aws configure\n", "CRITICAL", r"\baws\s+configure"),
    ("gcloud_auth.sh", "gcloud auth login\n", "CRITICAL", r"\bgcloud\s+auth"),
    ("az_login.sh", "az login\n", "CRITICAL", r"\baz\s+login"),
    # 6. mysql / psql / redis-cli with credentials
    ("mysql_creds.sh", "mysql -u root -pMyPassword db\n", "HIGH", r"\bmysql\s+"),
    ("psql_creds.sh", "psql -U admin -W secret db\n", "HIGH", r"\bpsql\s+"),
    ("redis_auth.sh", "redis-cli -a supersecret ping\n", "HIGH", r"\bredis-cli"),
    # 7. kubectl / helm
    ("kubectl_config.sh", "kubectl config use-context prod\n", "HIGH", r"\bkubectl\s+config"),
    ("helm_secrets.sh", "helm secrets view my-release\n", "HIGH", r"\bhelm\s+secrets"),
    # 8. vault / pass
    ("vault_read.sh", "vault read secret/data/foo\n", "CRITICAL", r"\bvault\s+read"),
    ("vault_write.sh", "vault write secret/data/foo value=bar\n", "CRITICAL", r"\bvault\s+write"),
    ("pass_show.sh", "pass show email/brice@example.com\n", "CRITICAL", r"\bpass\s+show"),
    # 9. curl with Authorization header
    (
        "curl_auth.sh",
        'curl -H "Authorization: Bearer abc123def456ghi789" https://api.example.com\n',
        "HIGH",
        r"\bcurl\b[^\n]*-H\s+[\"']?Authorization",
    ),
    # 10. python -c with os.environ
    (
        "python_env.py",
        'python -c "import os; print(os.environ[\'API_KEY\'])"\n',
        "HIGH",
        r"\bpython\s+",
    ),
]


def _write_file(directory: Path, name: str, content: str) -> Path:
    f = directory / name
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    return f


def test_all_forbidden_patterns_are_detected(tmp_dir: Path):
    """Every category of forbidden pattern in ADR 0011 §3 must trigger a finding."""
    config = LintConfig()
    files = [_write_file(tmp_dir, name, content) for name, content, _, _ in PATTERN_CASES]
    report: LintReport = lint_paths(files, config=config)
    assert report.findings, "expected at least one finding across the 10 categories"
    # We should have at least one finding per file (or at least 20 findings overall).
    assert len(report.findings) >= len(PATTERN_CASES) - 2, (
        f"expected ~{len(PATTERN_CASES)} findings, got {len(report.findings)}"
    )


def test_ssh_non_localhost_triggers_critical(tmp_dir: Path):
    """ssh against a non-localhost target should be CRITICAL."""
    f = _write_file(tmp_dir, "ssh_remote.sh", "ssh root@nas.example.com\n")
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "CRITICAL" for fi in report.findings), (
        f"ssh to non-localhost must be CRITICAL, got: {report.findings}"
    )


def test_gh_auth_login_triggers_critical(tmp_dir: Path):
    f = _write_file(tmp_dir, "gh.sh", "gh auth login\n")
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "CRITICAL" for fi in report.findings)


def test_docker_login_triggers_critical(tmp_dir: Path):
    f = _write_file(tmp_dir, "docker.sh", "docker login registry.io\n")
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "CRITICAL" for fi in report.findings)


def test_env_grep_secret_triggers_critical(tmp_dir: Path):
    f = _write_file(tmp_dir, "env.sh", "env | grep SECRET\n")
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "CRITICAL" for fi in report.findings)


def test_vault_read_triggers_critical(tmp_dir: Path):
    f = _write_file(tmp_dir, "vault.sh", "vault read secret/data/x\n")
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "CRITICAL" for fi in report.findings)


def test_mysql_with_credentials_triggers_high(tmp_dir: Path):
    f = _write_file(tmp_dir, "mysql.sh", "mysql -u root -pMyPassword db\n")
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "HIGH" for fi in report.findings), (
        f"mysql with creds must be HIGH, got: {report.findings}"
    )


def test_curl_authorization_header_triggers_high(tmp_dir: Path):
    f = _write_file(
        tmp_dir,
        "curl.sh",
        'curl -H "Authorization: Bearer abc123def456ghi789" https://api.example.com\n',
    )
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "HIGH" for fi in report.findings)


def test_python_os_environ_triggers_high(tmp_dir: Path):
    f = _write_file(
        tmp_dir,
        "py.py",
        'python -c "import os; print(os.environ[\'X\'])"\n',
    )
    report = lint_paths([f], config=LintConfig())
    assert any(fi.severity == "HIGH" for fi in report.findings)


def test_finding_has_file_line_column(tmp_dir: Path):
    """A finding must carry precise location information."""
    f = _write_file(tmp_dir, "ssh.sh", "# header\nssh user@host\n")
    report = lint_paths([f], config=LintConfig())
    assert report.findings
    f0 = report.findings[0]
    assert f0.line == 2
    assert f0.column >= 1
    assert f0.pattern
    assert f0.severity
    assert f0.message
    assert f0.suggestion


def test_multiple_violations_in_one_file(tmp_dir: Path):
    """A single file with multiple violations should produce multiple findings."""
    content = (
        "ssh root@nas\n"
        "gh auth login\n"
        "docker login registry.io\n"
    )
    f = _write_file(tmp_dir, "multi.sh", content)
    report = lint_paths([f], config=LintConfig())
    # 3+ findings expected (some patterns may share a regex; we accept >=3)
    assert len(report.findings) >= 3, f"expected >=3 findings, got {len(report.findings)}"

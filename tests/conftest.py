# tests/conftest.py
#!/usr/bin/env python3
import pytest
import os
from pathlib import Path


@pytest.fixture
def lab_config():
    """Provide lab infrastructure configuration"""
    return {
        "base_dir": Path(os.getenv("LAB_INFRA_DIR", "~/lab-infra")),
        "dns_server": os.getenv("LAB_DNS_SERVER", "192.168.10.2"),
        "dhcp_server": os.getenv("LAB_DHCP_SERVER", "192.168.10.2"),
        "nfs_server": os.getenv("LAB_NFS_SERVER", "192.168.10.2"),
        "domain": os.getenv("LAB_DOMAIN", "lab.com"),
    }

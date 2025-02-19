# tests/test_network_config.py
#!/usr/bin/env python3
import pytest
from pathlib import Path
from network_config import NetworkConfig


class TestNetworkConfig:
    """Test suite for network configuration tool"""

    @pytest.fixture
    def network_config(self, tmp_path):
        """Create a temporary test environment"""
        # Create test directory structure
        dns_config = tmp_path / "dns" / "config"
        dhcp_config = tmp_path / "dhcp" / "config"
        dns_config.mkdir(parents=True)
        dhcp_config.mkdir(parents=True)

        # Create test configuration files
        (dns_config / "named.conf").write_text("192.168.10.2")
        (dns_config / "db.lab.com").write_text("192.168.10")
        (dns_config / "db.10.168.192").write_text("192.168.10")
        (dhcp_config / "dhcpd.conf").write_text("subnet 192.168.10.0")

        return NetworkConfig(tmp_path)

    def test_validate_network(self, network_config):
        """Test network validation"""
        assert network_config.validate_network("192.168.20.0/24")
        assert not network_config.validate_network("invalid")
        assert not network_config.validate_network("192.168.20.0/16")

    def test_backup_configs(self, network_config):
        """Test configuration backup"""
        backup_path = network_config.backup_configs()
        assert backup_path.exists()
        assert (backup_path / "dns").exists()
        assert (backup_path / "dhcp").exists()

    def test_update_network(self, network_config):
        """Test network update functionality"""
        assert network_config.update_network("192.168.20")

        # Verify DNS configurations were updated
        named_conf = (network_config.dns_dir / "named.conf").read_text()
        assert "192.168.20" in named_conf

        # Verify DHCP configurations were updated
        dhcpd_conf = (network_config.dhcp_dir / "dhcpd.conf").read_text()
        assert "192.168.20" in dhcpd_conf

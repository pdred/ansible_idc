# tests/test_infrastructure.py
#!/usr/bin/env python3
import asyncio
import pytest
from pathlib import Path
import subprocess
import dns.resolver
from typing import Dict, List, Tuple


class TestInfrastructure:
    """Test suite for lab infrastructure services"""

    @pytest.mark.asyncio
    async def test_dns_resolution(self, lab_config):
        """Test DNS resolution for all configured domains"""
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [lab_config["dns_server"]]

        test_records = [
            f"api.partner.{lab_config['domain']}",
            f"*.apps.partner.{lab_config['domain']}",
            f"api.engg.{lab_config['domain']}",
            f"api.clust.{lab_config['domain']}",
            f"api.kvm.{lab_config['domain']}",
            f"api.cicd.{lab_config['domain']}",
        ]

        for record in test_records:
            answers = resolver.resolve(record, "A")
            assert len(answers) > 0, f"No DNS records found for {record}"

    @pytest.mark.asyncio
    async def test_reverse_dns(self, lab_config):
        """Test reverse DNS lookups"""
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [lab_config["dns_server"]]

        test_ips = [
            "192.168.10.2",  # Infrastructure
            "192.168.10.10",  # Partner
            "192.168.10.104",  # Engineering
            "192.168.10.165",  # Cluster
        ]

        for ip in test_ips:
            answers = resolver.resolve_address(ip)
            assert len(answers) > 0, f"No reverse DNS record found for {ip}"

    @pytest.mark.asyncio
    async def test_dhcp_service(self, lab_config):
        """Test DHCP service availability and configuration"""
        # Test DHCP service port
        result = subprocess.run(
            ["nmap", "-sU", "-p", "67", lab_config["dhcp_server"]],
            capture_output=True,
            text=True,
        )
        assert "open" in result.stdout, "DHCP service port is not open"

        # Test DHCP configuration syntax
        dhcp_conf = Path(lab_config["base_dir"]) / "dhcp" / "config" / "dhcpd.conf"
        result = subprocess.run(
            ["dhcpd", "-t", "-cf", str(dhcp_conf)], capture_output=True, text=True
        )
        assert result.returncode == 0, "DHCP configuration syntax check failed"

    @pytest.mark.asyncio
    async def test_nfs_service(self, lab_config):
        """Test NFS service availability and exports"""
        # Test NFS service
        result = subprocess.run(
            ["showmount", "-e", lab_config["nfs_server"]],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "NFS service check failed"
        assert "/exports" in result.stdout, "Required NFS exports not found"

    @pytest.mark.asyncio
    async def test_selinux_contexts(self, lab_config):
        """Test SELinux contexts for service directories"""
        directories = ["/etc/bind", "/etc/dhcp", "/exports"]

        for directory in directories:
            result = subprocess.run(
                ["ls", "-Z", directory], capture_output=True, text=True
            )
            assert (
                result.returncode == 0
            ), f"Failed to check SELinux context for {directory}"
            assert (
                "container_file_t" in result.stdout
            ), f"Incorrect SELinux context for {directory}"

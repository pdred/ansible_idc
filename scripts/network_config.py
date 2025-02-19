#!/usr/bin/env python3
"""
Network Configuration Tool for Lab Infrastructure.
Handles network range updates and validation for DNS, DHCP, and NFS services.
"""

import argparse
import ipaddress
import logging
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NetworkConfig:
    """Manages network configuration for lab infrastructure services."""

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.dns_dir = self.base_dir / "dns" / "config"
        self.dhcp_dir = self.base_dir / "dhcp" / "config"
        self.backup_dir = self.base_dir / "backups"

    def validate_network(self, network: str) -> bool:
        """Validate if the provided network string is a valid IP network."""
        try:
            net = ipaddress.ip_network(network)
            return net.prefixlen == 24  # Ensure it's a /24 network
        except ValueError as e:
            logger.error(f"Invalid network: {e}")
            return False

    def backup_configs(self) -> Path:
        """Create backup of current configurations."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / timestamp

        try:
            # Create backup directories
            backup_path.mkdir(parents=True, exist_ok=True)
            (backup_path / "dns").mkdir(exist_ok=True)
            (backup_path / "dhcp").mkdir(exist_ok=True)

            # Backup DNS configs
            for file in self.dns_dir.glob("*"):
                shutil.copy2(file, backup_path / "dns")

            # Backup DHCP configs
            for file in self.dhcp_dir.glob("*"):
                shutil.copy2(file, backup_path / "dhcp")

            logger.info(f"Backup created at {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise

    def update_network(self, new_network: str, old_network: str = "192.168.10") -> bool:
        """Update network configuration files with new network range."""
        if not self.validate_network(f"{new_network}.0/24"):
            return False

        try:
            # Create backup first
            self.backup_configs()

            # Update DNS configurations
            self._update_dns_configs(new_network, old_network)

            # Update DHCP configurations
            self._update_dhcp_configs(new_network, old_network)

            # Update reverse zone file
            self._update_reverse_zone(new_network, old_network)

            logger.info(f"Network configuration updated to {new_network}")
            return True

        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False

    def _update_dns_configs(self, new_network: str, old_network: str):
        """Update DNS configuration files."""
        for file in self.dns_dir.glob("*"):
            if file.is_file():
                content = file.read_text()
                updated = content.replace(old_network, new_network)
                file.write_text(updated)
                logger.debug(f"Updated DNS config: {file}")

    def _update_dhcp_configs(self, new_network: str, old_network: str):
        """Update DHCP configuration files."""
        for file in self.dhcp_dir.glob("*"):
            if file.is_file():
                content = file.read_text()
                updated = content.replace(old_network, new_network)
                file.write_text(updated)
                logger.debug(f"Updated DHCP config: {file}")

    def _update_reverse_zone(self, new_network: str, old_network: str):
        """Update reverse zone file name and content."""
        old_parts = old_network.split(".")
        new_parts = new_network.split(".")

        old_rev = f"db.{old_parts[2]}.{old_parts[1]}.{old_parts[0]}"
        new_rev = f"db.{new_parts[2]}.{new_parts[1]}.{new_parts[0]}"

        old_file = self.dns_dir / old_rev
        new_file = self.dns_dir / new_rev

        if old_file.exists():
            content = old_file.read_text()
            updated = content.replace(old_network, new_network)
            new_file.write_text(updated)
            old_file.unlink()
            logger.debug(f"Updated reverse zone: {old_rev} -> {new_rev}")


def main():
    parser = argparse.ArgumentParser(description="Network Configuration Tool")
    parser.add_argument(
        "--new-network", required=True, help="New network range (e.g., 192.168.20)"
    )
    parser.add_argument(
        "--base-dir",
        default=os.path.expanduser("~/lab-infra"),
        help="Base directory for lab infrastructure",
    )

    args = parser.parse_args()

    config = NetworkConfig(args.base_dir)
    if config.update_network(args.new_network):
        logger.info("Network configuration completed successfully")
    else:
        logger.error("Network configuration failed")
        exit(1)


if __name__ == "__main__":
    main()

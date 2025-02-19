# Troubleshooting Guide

## Common Issues and Solutions

### DNS Issues

#### Error: zone transfer failed: REFUSED
```bash
# Check named logs
podman logs dns-server

# Solution: Add allow-transfer clause
allow-transfer { trusted-servers; };

# Error: SERVFAIL response
  1. Check zone file syntax
  2. Verify SOA record
  3. Check file permissions

# DHCP Issues

## Error: No subnet declaration for eth0
  1. Verify network interface
  2. Check subnet configuration
  3. Validate DHCP range

## Error: Unable to bind to DHCP port
  1. Check if another DHCP server is running
  2. Verify port availability
  3. Check SELinux context

# NFS Issues
## Error: Permission denied
  1. Check SELinux context
  2. Verify export permissions
  3. Check firewall rules

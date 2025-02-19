# Security Configuration Guide
  *Optional, but recommended*

## Access Control

### DNS Security
1. Configure TSIG keys for zone transfers
2. Enable DNSSEC
3. Implement response rate limiting

### DHCP Security
1. Configure client authentication
2. Implement MAC address filtering
3. Enable secure DHCP logging

```bash
# Configure secure updates
ddns-update-style interim;
update-static-leases on;
key DHCP_UPDATER {
    algorithm HMAC-MD5;
    secret "your-secret-key";
}
```

### NFS Security
1. Use Kerberos authentication
2. Implement export restrictions
3. Enable NFSv4 security features

```bash
# Configure Kerberos
/etc/exports
/exports/home *(sec=krb5p,rw,sync)
```

## Encryption Configuration

### DNS
```bash
# Generate TSIG key
tsig-keygen -a HMAC-SHA512 lab.com > /etc/bind/tsig.key

# Add to named.conf
key "lab.com" {
    algorithm HMAC-SHA512;
    secret "generated-key-here";
};

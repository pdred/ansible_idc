## 2. Network Configuration (docs/NETWORKING.md)

```markdown
# Network Configuration Guide

## IP Range Configuration

### Default Network Setup
The default configuration uses the 192.168.10.0/24 network. To modify this:

1. Update DNS configuration:
   ```bash
   sed -i 's/192.168.10/YOUR.IP.RANGE/g' dns/config/named.conf
   sed -i 's/192.168.10/YOUR.IP.RANGE/g' dns/config/db.lab.com
   ```
2. Update DHCP configuration:
   ```bash
   sed -i 's/192.168.10/YOUR.IP.RANGE/g' dhcp/config/dhcpd.conf
   ```
3. Update reverse zone file:
   - Rename db.10.168.192 to match your network
   - Update PTR records accordingly

#### Subnet Planning
Default Subnet Allocation
  - Infrastructure: x.x.x.1-9
  - Partner Network: x.x.x.10-99
  - Engineering: x.x.x.100-150
  - OCP Cluster: x.x.x.160-175
  - KVM Hosts: x.x.x.176-190
  - CICD: x.x.x.191-200

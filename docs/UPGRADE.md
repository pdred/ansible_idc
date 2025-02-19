# Upgrade and Downgrade Procedures

## Backup Procedure

```bash
#!/bin/bash
# Backup current configuration
backup_dir="~/lab-infra/backups/$(date +%Y%m%d)"
mkdir -p $backup_dir

# Backup DNS configuration
cp -r ~/lab-infra/dns/config/* $backup_dir/dns/
cp -r ~/lab-infra/dns/data/* $backup_dir/dns_data/

# Backup DHCP configuration
cp -r ~/lab-infra/dhcp/config/* $backup_dir/dhcp/
cp -r ~/lab-infra/dhcp/data/* $backup_dir/dhcp_data/

# Backup NFS exports
cp /etc/exports $backup_dir/exports
```

# Upgrade Procedure

1. Stop services

```bash
systemctl --user stop dns-server.service dhcp-server.service
sudo systemctl stop nfs-server
```

2. Backup configurations
3. Update container images
4. Apply new configurations
5. Start services
6. Verify functionality

# Rollback Procedure

```bash
#!/bin/bash
# Restore from backup
backup_date=$1
backup_dir="~/lab-infra/backups/$backup_date"

# Stop services
systemctl --user stop dns-server.service dhcp-server.service
sudo systemctl stop nfs-server

# Restore configurations
cp -r $backup_dir/dns/* ~/lab-infra/dns/config/
cp -r $backup_dir/dns_data/* ~/lab-infra/dns/data/
cp -r $backup_dir/dhcp/* ~/lab-infra/dhcp/config/
cp -r $backup_dir/dhcp_data/* ~/lab-infra/dhcp/data/
sudo cp $backup_dir/exports /etc/exports

# Start services
systemctl --user start dns-server.service dhcp-server.service
sudo systemctl start nfs-server
```

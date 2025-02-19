# Dependencies

## Required Software Versions

- Ansible: >= 2.12.0
- Python: >= 3.9
- Podman: >= 3.4.0
- BIND: >= 9.16
- ISC DHCP Server: >= 4.4.2
- NFS Utils: >= 2.5.1

## Python Dependencies
```python
### requirements.txt
ansible>=2.12.0
jinja2>=3.0.0
netaddr>=0.8.0
pyOpenSSL>=20.0.1

## Operating System Requirements

- RHEL 8.4+ / CentOS Stream 8+ / Fedora 34+
- SELinux enabled (enforcing mode recommended)
- Firewalld installed and enabled
- ZSH shell with oh-my-zsh

## Network Requirements

Available IP range: 192.168.10.0/24 (configurable)
- Open ports:
  - DNS: 53 TCP/UDP
  - DHCP: 67/68 UDP
  - NFS: 2049 TCP, 111 TCP/UDP
  - Portmapper: 111 TCP/UDP
  - Mountd: 20048 TCP/UDP

## Optional Dependencies

- Prometheus (for monitoring)
- Grafana (for visualization)
- Elasticsearch (for log aggregation)

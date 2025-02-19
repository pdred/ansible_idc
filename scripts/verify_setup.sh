#!/bin/bash

check_dns() {
    local domain=$1
    local expected_ip=$2

    result=$(dig @192.168.10.2 +short $domain)
    if [ "$result" = "$expected_ip" ]; then
        echo "✓ DNS resolution for $domain successful"
    else
        echo "✗ DNS resolution for $domain failed"
        echo "Expected: $expected_ip"
        echo "Got: $result"
    fi
}

check_dhcp() {
    local result=$(sudo nmap -sU -p 67 192.168.10.2)
    if echo "$result" | grep -q "open"; then
        echo "✓ DHCP server responding"
    else
        echo "✗ DHCP server not responding"
    fi
}

check_nfs() {
    local result=$(showmount -e 192.168.10.2)
    if [ $? -eq 0 ]; then
        echo "✓ NFS exports available"
        echo "$result"
    else
        echo "✗ NFS server not responding"
    fi
}

# Run checks
echo "=== Running Service Checks ==="
check_dns "api.partner.lab.com" "192.168.10.10"
check_dns "*.apps.partner.lab.com" "192.168.10.10"
check_dhcp
check_nfs

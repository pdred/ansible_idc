# Contributing Guidelines

## Code Style Guide

### Shell Scripts
- Use shellcheck for static analysis
- Follow Google Shell Style Guide
- Use meaningful variable names
- Include error handling

### Python Code
- Follow PEP 8
- Use type hints
- Document functions using docstrings
- Include unit tests

### Ansible Playbooks
- Use YAML files with .yml extension
- Include comments for complex tasks
- Use meaningful role and variable names
- Follow Ansible best practices

## Git Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit pull request

## Testing Requirements

### Unit Tests
```bash```

# Run Python tests
python -m pytest tests/

# Run shell script tests
bats tests/shell/

# Run Ansible syntax check
ansible-playbook --syntax-check playbook.yml

## Integration Tests

```bash
# Test DNS configuration
named-checkconf /etc/bind/named.conf
named-checkzone lab.com /etc/bind/db.lab.com

# Test DHCP configuration
dhcpd -t -cf /etc/dhcp/dhcpd.conf

# Test NFS exports
exportfs -ra
```

## Pull Request Template

```markdown
### Description
[Describe your changes]

### Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Configuration change

### Testing
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Manual testing performed

### Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Tests added/updated
```

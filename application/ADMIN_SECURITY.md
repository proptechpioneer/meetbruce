# Admin Honeypot Security Setup

## Overview
This Django application now includes a security honeypot system to protect the real admin interface and monitor unauthorized access attempts.

## Security Configuration

### Real Admin Interface
- **URL**: `/centralmanagementserver/`
- **Purpose**: Actual Django admin interface for legitimate administrators
- **Features**: 
  - Full Django admin functionality
  - User management
  - Custom site branding ("Bruce Central Management Server")
  - Enhanced user admin with collapsible fieldsets

### Honeypot Admin Interface  
- **URL**: `/admin/` and `/admin/login/`
- **Purpose**: Fake admin interface to catch unauthorized access attempts
- **Features**:
  - Identical visual appearance to real Django admin
  - Logs all access attempts with IP addresses, user agents, and timestamps
  - Captures login attempts with usernames and passwords
  - Returns realistic error messages to appear authentic

## Logging System

### Security Logs
- **Location**: `logs/security.log`
- **Format**: `[SECURITY] timestamp - message`
- **Captured Data**:
  - IP addresses
  - User agents  
  - Access timestamps
  - Login attempt credentials
  - Request paths

### Log Levels
- **WARNING**: General honeypot access
- **CRITICAL**: Login attempts with credentials

## Usage Instructions

### For Administrators
1. Access the real admin at: `http://your-domain.com/centralmanagementserver/`
2. Monitor security logs regularly in `logs/security.log`
3. Never access `/admin/` - it will trigger security logging

### For Security Monitoring
1. Check `logs/security.log` for suspicious activity
2. Look for repeated access attempts from the same IP
3. Monitor for credential stuffing or brute force patterns
4. Set up log rotation for production environments

## Production Considerations

### Additional Security Measures
1. **IP Whitelist**: Restrict `/centralmanagementserver/` to specific IPs
2. **VPN Access**: Require VPN connection for admin access
3. **2FA**: Implement two-factor authentication
4. **Rate Limiting**: Add rate limiting to honeypot endpoints
5. **Alerting**: Set up real-time alerts for security log events

### Environment Variables
Consider moving sensitive settings to environment variables:
- Admin URL path
- Log file locations
- Security alert thresholds

## File Structure
```
application/
├── logs/
│   ├── security.log          # Security event logs
│   └── .gitignore           # Ignore log files in git
├── templates/
│   └── admin/
│       └── honeypot_login.html  # Fake admin login page
└── application/
    ├── urls.py              # URL routing with honeypot
    ├── views.py             # Honeypot view logic
    ├── admin.py             # Enhanced admin configuration
    └── settings.py          # Logging configuration
```

## Testing the Setup

### Test Honeypot
1. Visit `http://127.0.0.1:8000/admin/`
2. Attempt to login with fake credentials
3. Check `logs/security.log` for logged attempts

### Test Real Admin
1. Create superuser: `python manage.py createsuperuser`
2. Visit `http://127.0.0.1:8000/centralmanagementserver/`
3. Login with superuser credentials
4. Verify admin functionality

## Maintenance
- Regularly rotate security logs
- Monitor log file sizes
- Review access patterns for threats
- Update security measures based on attack patterns

---

**Security Notice**: Keep the real admin URL (`/centralmanagementserver/`) confidential and never expose it in public documentation or error messages.
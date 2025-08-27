# Logs directory for Drift Phonk Autopilot Playbook
# This directory stores application logs

*.log files will be automatically created here when running the application.

## Log Files

- `drift_phonk.log` - Main application log
- `drift_phonk.log.1`, `drift_phonk.log.2`, etc. - Rotated log backups

## Log Levels

- **DEBUG**: Detailed information for troubleshooting
- **INFO**: General information about application operation
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures

## Configuration

Log settings can be configured in `config/default.yaml`:

```yaml
logging:
  level: "INFO"
  file: "logs/drift_phonk.log"
  max_file_size: "10MB"
  backup_count: 5
```
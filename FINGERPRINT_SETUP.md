# Fingerprint Biometric Attendance System Setup Guide

## Overview

EmployeeHub now supports biometric fingerprint authentication for attendance tracking. This guide explains how to set up and integrate fingerprint devices with the system.

## System Architecture

The fingerprint system consists of three main components:

1. **FingerprintData Model**: Stores enrolled fingerprint templates for employees
2. **BiometricAttendance Model**: Logs all fingerprint scan events
3. **Fingerprint Device Integration**: Physical fingerprint scanners connected to the system

## Supported Devices

The system is designed to work with most USB fingerprint scanners that provide template data. Common compatible devices include:

- **ZKTeco** fingerprint scanners (ZK4500, ZK9500, etc.)
- **Digital Persona** U.are.U series
- **Futronic** FS80/FS88 series
- **Suprema** RealScan series
- **Mantra** MFS100 series

## Prerequisites

1. Python packages for fingerprint device communication:
```bash
pip install pyfingerprint  # For ZKTeco and similar devices
pip install pyusb           # For USB device communication
```

2. Device-specific SDKs (if required by your device manufacturer)

## Setup Steps

### Step 1: Install Hardware

1. Connect your fingerprint scanner to a USB port
2. Install any required drivers from the manufacturer
3. Verify device is recognized by the operating system

### Step 2: Configure Device Settings

Create a configuration file `fingerprint_config.py` in your project root:

```python
# Fingerprint Device Configuration
FINGERPRINT_CONFIG = {
    'device_type': 'zkteco',  # or 'digitalpersona', 'futronic', etc.
    'device_port': '/dev/ttyUSB0',  # or COM port on Windows
    'baudrate': 57600,
    'device_id': 'DEVICE_001',
    'timeout': 5000,  # milliseconds
    'quality_threshold': 50,  # minimum quality score (0-100)
}
```

### Step 3: Enroll Employee Fingerprints

#### Via Web Interface:

1. Navigate to **Biometric > Fingerprint Management**
2. Click **"Enroll New Fingerprint"**
3. Select the employee from the dropdown
4. Follow the on-screen instructions to scan the fingerprint
5. The system will store the fingerprint template

#### Programmatically:

```python
from emp_app.models import Employee, FingerprintData

# Get employee
employee = Employee.objects.get(emp_id=1)

# Scan and get fingerprint template from device
fingerprint_template = scan_fingerprint_from_device()

# Save to database
FingerprintData.objects.create(
    employee=employee,
    fingerprint_template=fingerprint_template,
    device_id='DEVICE_001',
    quality_score=85,
    is_active=True
)
```

### Step 4: Integrate with Attendance System

The system provides a REST API endpoint for fingerprint scanners to submit attendance:

**Endpoint**: `POST /biometric/simulate-scan`

**Payload**:
```json
{
    "employee_id": 1,
    "status": "check_in",  // check_in, check_out, break_start, break_end
    "device_id": "DEVICE_001"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Attendance logged for John Doe",
    "timestamp": "2025-10-28 09:30:00",
    "action": "check_in"
}
```

## Integration Examples

### Example 1: Python Script for ZKTeco Device

```python
from pyfingerprint.pyfingerprint import PyFingerprint
import requests
import json

# Initialize device
f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

# Search for fingerprint
f.searchTemplate()
positionNumber = f.searchTemplate()[0]

if positionNumber >= 0:
    # Map position to employee ID (you need to maintain this mapping)
    employee_id = get_employee_by_position(positionNumber)

    # Send to EmployeeHub
    response = requests.post(
        'http://your-server.com/biometric/simulate-scan',
        json={
            'employee_id': employee_id,
            'status': 'check_in',
            'device_id': 'DEVICE_001'
        }
    )

    print(response.json())
```

### Example 2: Node.js Integration

```javascript
const fingerprint = require('fingerprint-sdk');
const axios = require('axios');

// Initialize device
const device = new fingerprint.Device({
    port: '/dev/ttyUSB0',
    baudrate: 57600
});

// Listen for scans
device.on('fingerprint', async (data) => {
    try {
        const response = await axios.post('http://your-server.com/biometric/simulate-scan', {
            employee_id: data.employeeId,
            status: 'check_in',
            device_id: 'DEVICE_001'
        });

        console.log('Attendance logged:', response.data);
    } catch (error) {
        console.error('Error logging attendance:', error);
    }
});
```

## Management Operations

### Enroll Fingerprint
- **URL**: `/biometric/enroll`
- **Method**: GET (form) / POST (submit)
- **Required Fields**: employee, fingerprint_template, device_id, quality_score

### Update Fingerprint
- **URL**: `/biometric/update/<fingerprint_id>`
- **Method**: GET (form) / POST (submit)
- **Use Case**: Re-enroll if fingerprint quality is poor

### Delete Fingerprint
- **URL**: `/biometric/delete/<fingerprint_id>`
- **Method**: POST
- **Use Case**: Remove employee's fingerprint data

### View Logs
- **URL**: `/biometric/logs`
- **Filters**: Date, Employee
- **Shows**: All fingerprint scan events with timestamps

## Best Practices

1. **Quality Control**
   - Only accept fingerprints with quality score above 50
   - Request re-enrollment if quality is poor
   - Store 2-3 fingerprints per employee for redundancy

2. **Security**
   - Store only fingerprint templates, not actual images
   - Use HTTPS for all API communications
   - Implement rate limiting on scan endpoints
   - Regularly audit access logs

3. **Device Management**
   - Label devices with unique IDs
   - Keep device firmware updated
   - Clean fingerprint sensors regularly
   - Have backup devices available

4. **Data Privacy**
   - Inform employees about biometric data collection
   - Provide opt-out options where legally required
   - Implement data retention policies
   - Comply with GDPR/local privacy laws

## Troubleshooting

### Device Not Detected
```bash
# Linux
lsusb  # Check if device appears

# Windows
# Check Device Manager > Biometric Devices
```

### Poor Recognition Rate
- Clean the fingerprint sensor
- Re-enroll fingerprints with better quality
- Adjust quality threshold in config
- Try different fingers

### Connection Timeouts
- Check device port/COM port settings
- Verify baudrate matches device specs
- Ensure no other application is using the device
- Check USB cable and connection

### Database Errors
```bash
# If fingerprint template is too large
# Increase TEXT field size in database
python manage.py makemigrations
python manage.py migrate
```

## API Reference

### Fingerprint Management API

#### List All Enrolled Fingerprints
```http
GET /biometric/fingerprint
```

#### Get Employee Fingerprint
```python
from emp_app.models import FingerprintData
fingerprint = FingerprintData.objects.get(employee_id=1)
```

#### Delete Fingerprint
```http
POST /biometric/delete/<fingerprint_id>
```

#### View Attendance Logs
```http
GET /biometric/logs?date=2025-10-28&employee=1
```

## Testing

Use the built-in simulator to test without physical devices:

```bash
# Via Web Interface
Navigate to: /biometric/fingerprint
Click: "Simulate Scan" button

# Via API
curl -X POST http://localhost:8000/biometric/simulate-scan \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "status": "check_in",
    "device_id": "DEVICE_SIM"
  }'
```

## Support

For device-specific integration help:
- Check manufacturer SDK documentation
- Contact device vendor support
- Refer to our example integrations in `/examples/` folder

## Compliance

Ensure your fingerprint system complies with:
- **GDPR** (EU): Obtain explicit consent, allow data deletion
- **CCPA** (California): Provide notice and opt-out options
- **BIPA** (Illinois): Obtain written consent, implement retention policy
- **Local Labor Laws**: Check requirements in your jurisdiction

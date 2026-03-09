# Smart Pricing Engine - Deployment Checklist ✅

## Pre-Installation

- [ ] Frappe/ERPNext installed and running
- [ ] Ocean Shipment module installed
- [ ] Python 3.8+ available
- [ ] Internet connectivity for LLM API calls
- [ ] Backup database before installation

## Installation Steps

- [ ] Copy files to appropriate directories
- [ ] Make install script executable: `chmod +x install_ai_pricing.sh`
- [ ] Run installation: `./install_ai_pricing.sh your-site-name`
- [ ] Verify DocTypes created successfully
- [ ] Check for any installation errors

## Configuration

- [ ] At least one user configured LLM settings
- [ ] API keys tested and working
- [ ] Feature toggles set appropriately
- [ ] Permissions reviewed and adjusted

## Testing

- [ ] Test margin suggestions on sample shipment
- [ ] Test price validation in sales invoice
- [ ] Test country analytics
- [ ] Test volume discount recommendations
- [ ] Test FX risk analysis
- [ ] Verify AI logs being created
- [ ] Check API response times

## Documentation

- [ ] Users trained on AI features
- [ ] Quick start guide distributed
- [ ] Support channels communicated
- [ ] Cost management guidelines shared

## Monitoring

- [ ] Set up error monitoring
- [ ] Configure usage tracking
- [ ] Set up cost alerts
- [ ] Monitor API response times

## Post-Deployment

- [ ] Gather user feedback
- [ ] Monitor adoption rates
- [ ] Track cost vs. value
- [ ] Plan iterative improvements

## Rollback Plan

- [ ] Database backup verified
- [ ] Rollback procedure documented
- [ ] Emergency contacts identified

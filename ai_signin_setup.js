/**
 * AI Pricing Engine - Sign-in Setup Script
 * Prompts users to configure their LLM settings during first sign-in
 */

frappe.ready(function() {
    // Check if user has configured AI settings
    checkAISettings();
});

function checkAISettings() {
    // Only check for logged-in users
    if (!frappe.session.user || frappe.session.user === 'Guest') {
        return;
    }
    
    frappe.call({
        method: 'api.ai_pricing.get_user_ai_settings',
        callback: function(r) {
            if (r.message && r.message.success) {
                const settings = r.message.settings;
                
                // If no settings or not enabled, show setup dialog
                if (!settings || !settings.enabled || !settings.llm_provider) {
                    showAISetupDialog();
                }
            }
        }
    });
}

function showAISetupDialog() {
    const dialog = new frappe.ui.Dialog({
        title: '🤖 Enable AI Pricing Features',
        fields: [
            {
                fieldtype: 'HTML',
                options: `
                    <div style="margin-bottom: 20px;">
                        <h4>Welcome to Smart Pricing Engine!</h4>
                        <p>Unlock AI-powered pricing intelligence by configuring your LLM provider.</p>
                        <p><strong>Features you'll get:</strong></p>
                        <ul>
                            <li>🎯 Landed cost based margin suggestions</li>
                            <li>📊 Historical pricing comparison</li>
                            <li>🌍 Country-wise pricing analytics</li>
                            <li>📦 Volume-based discount recommendations</li>
                            <li>💱 FX risk alert system</li>
                        </ul>
                    </div>
                `
            },
            {
                fieldname: 'llm_provider',
                label: 'LLM Provider',
                fieldtype: 'Select',
                options: [
                    '',
                    'OpenAI',
                    'Anthropic',
                    'Google',
                    'Azure OpenAI'
                ],
                reqd: 1,
                description: 'Select your preferred AI model provider',
                onchange: function() {
                    updateModelHelp(this.value);
                }
            },
            {
                fieldname: 'llm_model',
                label: 'Model Name',
                fieldtype: 'Data',
                description: 'e.g., gpt-4, claude-3-sonnet-20240229, gemini-pro',
                depends_on: 'eval:doc.llm_provider'
            },
            {
                fieldname: 'llm_api_key',
                label: 'API Key',
                fieldtype: 'Password',
                reqd: 1,
                description: 'Your API key for the selected provider'
            },
            {
                fieldname: 'model_help',
                fieldtype: 'HTML',
                options: '<div id="model-help-text"></div>'
            },
            {
                fieldname: 'section_break',
                fieldtype: 'Section Break'
            },
            {
                fieldname: 'enabled',
                label: 'Enable AI Features',
                fieldtype: 'Check',
                default: 1
            },
            {
                fieldname: 'skip_setup',
                label: 'Skip for now (can configure later in User Settings)',
                fieldtype: 'Check',
                default: 0
            }
        ],
        primary_action_label: 'Save & Enable',
        primary_action: function(values) {
            if (values.skip_setup) {
                dialog.hide();
                return;
            }
            
            if (!values.llm_provider || !values.llm_api_key) {
                frappe.msgprint('Please select a provider and enter your API key');
                return;
            }
            
            // Save settings
            frappe.call({
                method: 'api.ai_pricing.save_user_ai_settings',
                args: {
                    llm_provider: values.llm_provider,
                    llm_api_key: values.llm_api_key,
                    llm_model: values.llm_model || getDefaultModel(values.llm_provider),
                    enabled: values.enabled ? 1 : 0
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.show_alert({
                            message: '✅ AI Pricing Engine enabled successfully!',
                            indicator: 'green'
                        }, 5);
                        dialog.hide();
                    } else {
                        frappe.msgprint({
                            title: 'Error',
                            message: r.message.message || 'Failed to save settings',
                            indicator: 'red'
                        });
                    }
                }
            });
        },
        secondary_action_label: 'Learn More',
        secondary_action: function() {
            window.open('/app/ai-pricing-guide', '_blank');
        }
    });
    
    dialog.show();
}

function updateModelHelp(provider) {
    const helpText = {
        'OpenAI': `
            <div class="alert alert-info">
                <strong>OpenAI Models:</strong><br>
                • <code>gpt-4</code> - Most capable, best for complex analysis<br>
                • <code>gpt-4-turbo</code> - Faster, cost-effective<br>
                • <code>gpt-3.5-turbo</code> - Fast and economical<br>
                <br>
                <strong>Get API Key:</strong> <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI Platform</a>
            </div>
        `,
        'Anthropic': `
            <div class="alert alert-info">
                <strong>Anthropic Models:</strong><br>
                • <code>claude-3-opus-20240229</code> - Most powerful<br>
                • <code>claude-3-sonnet-20240229</code> - Balanced performance<br>
                • <code>claude-3-haiku-20240307</code> - Fast and efficient<br>
                <br>
                <strong>Get API Key:</strong> <a href="https://console.anthropic.com/" target="_blank">Anthropic Console</a>
            </div>
        `,
        'Google': `
            <div class="alert alert-info">
                <strong>Google Models:</strong><br>
                • <code>gemini-pro</code> - Recommended for most tasks<br>
                • <code>gemini-pro-vision</code> - For image analysis<br>
                <br>
                <strong>Get API Key:</strong> <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a>
            </div>
        `,
        'Azure OpenAI': `
            <div class="alert alert-info">
                <strong>Azure OpenAI:</strong><br>
                Enter your full Azure endpoint URL in the Model Name field:<br>
                <code>https://YOUR-RESOURCE.openai.azure.com/openai/deployments/YOUR-DEPLOYMENT/chat/completions?api-version=2023-05-15</code>
                <br><br>
                <strong>Setup:</strong> <a href="https://portal.azure.com/" target="_blank">Azure Portal</a>
            </div>
        `
    };
    
    const helpDiv = document.getElementById('model-help-text');
    if (helpDiv) {
        helpDiv.innerHTML = helpText[provider] || '';
    }
}

function getDefaultModel(provider) {
    const defaults = {
        'OpenAI': 'gpt-4',
        'Anthropic': 'claude-3-sonnet-20240229',
        'Google': 'gemini-pro',
        'Azure OpenAI': ''
    };
    return defaults[provider] || '';
}

// Add AI Settings to User menu
frappe.ui.toolbar.add_dropdown_button('User', 'AI Settings', function() {
    frappe.set_route('Form', 'User AI Settings', frappe.session.user);
}, 'fa fa-robot');

// Add quick access to AI features in navbar
$(document).ready(function() {
    // Add AI indicator to navbar if enabled
    frappe.call({
        method: 'api.ai_pricing.get_user_ai_settings',
        callback: function(r) {
            if (r.message && r.message.success && r.message.settings.enabled) {
                addAIIndicator(r.message.settings);
            }
        }
    });
});

function addAIIndicator(settings) {
    const indicator = `
        <li class="nav-item">
            <a class="nav-link" href="#" title="AI Pricing Engine Active" 
               onclick="showAIStatus(); return false;">
                <span class="indicator-pill green">
                    <i class="fa fa-robot"></i> AI
                </span>
            </a>
        </li>
    `;
    
    $('.navbar-nav').append(indicator);
}

function showAIStatus() {
    frappe.call({
        method: 'api.ai_pricing.get_user_ai_settings',
        callback: function(r) {
            if (r.message && r.message.success) {
                const settings = r.message.settings;
                frappe.msgprint({
                    title: '🤖 AI Pricing Engine Status',
                    message: `
                        <div>
                            <p><strong>Status:</strong> ${settings.enabled ? '✅ Active' : '❌ Disabled'}</p>
                            <p><strong>Provider:</strong> ${settings.llm_provider || 'Not configured'}</p>
                            <p><strong>Model:</strong> ${settings.llm_model || 'Default'}</p>
                            <p><strong>API Key:</strong> ${settings.llm_api_key_masked || 'Not set'}</p>
                            <hr>
                            <p><a href="/app/user-ai-settings">Configure Settings</a></p>
                        </div>
                    `,
                    indicator: 'green'
                });
            }
        }
    });
}

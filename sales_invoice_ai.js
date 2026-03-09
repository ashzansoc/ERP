/**
 * Sales Invoice - AI Pricing Integration
 * Automatic price validation and volume discount suggestions
 */

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // Add Volume Discount Recommendations button
        if (frm.doc.items && frm.doc.items.length > 0) {
            frm.add_custom_button(__('📦 Volume Discount Suggestions'), function() {
                showVolumeDiscountRecommendations(frm);
            }, __('AI Features'));
        }
        
        // Add Validate All Prices button
        frm.add_custom_button(__('✅ Validate All Prices'), function() {
            validateAllPrices(frm);
        }, __('AI Features'));
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        const item = locals[cdt][cdn];
        if (item.item_code && item.rate) {
            validateItemPrice(frm, item);
        }
    },
    
    rate: function(frm, cdt, cdn) {
        const item = locals[cdt][cdn];
        if (item.item_code && item.rate) {
            validateItemPrice(frm, item);
        }
    },
    
    qty: function(frm, cdt, cdn) {
        const item = locals[cdt][cdn];
        if (item.item_code && item.qty && item.rate) {
            // Check if volume discount applicable
            checkVolumeDiscount(frm, item);
        }
    }
});

function validateItemPrice(frm, item) {
    // Debounce to avoid too many API calls
    clearTimeout(item.__validation_timeout);
    
    item.__validation_timeout = setTimeout(() => {
        frappe.call({
            method: 'api.ai_pricing.compare_historical_pricing',
            args: {
                item_code: item.item_code,
                proposed_price: item.rate
            },
            callback: function(r) {
                if (r.message && r.message.success) {
                    const comparison = r.message.comparison;
                    
                    if (!comparison.raw_response) {
                        // Update item with AI analysis
                        frappe.model.set_value(item.doctype, item.name, {
                            'ai_historical_avg': comparison.historical_avg || 0,
                            'ai_price_variance': comparison.variance || 0,
                            'ai_recommendation': comparison.recommendation || ''
                        });
                        
                        // Show visual indicator
                        showPriceIndicator(frm, item, comparison);
                    }
                }
            }
        });
    }, 1000);
}

function showPriceIndicator(frm, item, comparison) {
    const row = frm.fields_dict.items.grid.grid_rows_by_docname[item.name];
    if (!row) return;
    
    // Color code based on recommendation
    const colors = {
        'Accept': '#e8f5e9',  // Light green
        'Review': '#fff3e0',  // Light orange
        'Adjust': '#ffebee'   // Light red
    };
    
    const color = colors[comparison.recommendation] || '#f5f5f5';
    row.wrapper.find('.grid-row').css('background-color', color);
    
    // Add tooltip
    const tooltip = `
        Historical Avg: $${comparison.historical_avg || 0}
        Variance: ${comparison.variance || 0}%
        Trend: ${comparison.trend || 'Unknown'}
        Recommendation: ${comparison.recommendation || 'N/A'}
    `;
    row.wrapper.find('.grid-row').attr('title', tooltip);
    
    // Show alert for significant deviations
    if (comparison.recommendation === 'Adjust') {
        frappe.show_alert({
            message: `⚠️ ${item.item_code}: Price significantly differs from historical average`,
            indicator: 'orange'
        }, 5);
    }
}

function validateAllPrices(frm) {
    if (!frm.doc.items || frm.doc.items.length === 0) {
        frappe.msgprint('No items to validate');
        return;
    }
    
    frappe.show_alert({
        message: '🤖 Validating all prices with AI...',
        indicator: 'blue'
    });
    
    let processed = 0;
    let issues = [];
    
    frm.doc.items.forEach(item => {
        if (!item.item_code || !item.rate) {
            processed++;
            return;
        }
        
        frappe.call({
            method: 'api.ai_pricing.compare_historical_pricing',
            args: {
                item_code: item.item_code,
                proposed_price: item.rate
            },
            callback: function(r) {
                processed++;
                
                if (r.message && r.message.success && !r.message.comparison.raw_response) {
                    const comp = r.message.comparison;
                    
                    if (comp.recommendation === 'Adjust') {
                        issues.push({
                            item: item.item_code,
                            issue: comp.comparison,
                            recommendation: comp.recommendation
                        });
                    }
                }
                
                if (processed === frm.doc.items.length) {
                    showValidationResults(issues);
                }
            }
        });
    });
}

function showValidationResults(issues) {
    if (issues.length === 0) {
        frappe.show_alert({
            message: '✅ All prices validated successfully!',
            indicator: 'green'
        }, 5);
        return;
    }
    
    let html = '<div class="validation-results">';
    html += `<p>Found ${issues.length} pricing issue(s):</p>`;
    html += '<table class="table table-bordered">';
    html += '<tr><th>Item</th><th>Issue</th><th>Recommendation</th></tr>';
    
    issues.forEach(issue => {
        html += `<tr>
            <td>${issue.item}</td>
            <td>${issue.issue}</td>
            <td><span class="indicator orange">${issue.recommendation}</span></td>
        </tr>`;
    });
    
    html += '</table></div>';
    
    frappe.msgprint({
        title: '⚠️ Price Validation Results',
        message: html,
        indicator: 'orange',
        wide: true
    });
}

function checkVolumeDiscount(frm, item) {
    // Only check for significant quantities
    if (item.qty < 50) return;
    
    frappe.call({
        method: 'api.ai_pricing.get_volume_discount_recommendations',
        args: {
            item_code: item.item_code,
            base_price: item.rate,
            quantity_tiers: [50, 100, 500, 1000, 5000]
        },
        callback: function(r) {
            if (r.message && r.message.success && !r.message.recommendations.raw_response) {
                const recs = r.message.recommendations;
                
                // Find applicable tier
                const applicableTier = recs.discount_tiers.find(tier => 
                    item.qty >= tier.quantity
                );
                
                if (applicableTier && applicableTier.discount_pct > 0) {
                    showVolumeDiscountSuggestion(frm, item, applicableTier);
                }
            }
        }
    });
}

function showVolumeDiscountSuggestion(frm, item, tier) {
    const currentDiscount = item.discount_percentage || 0;
    
    if (tier.discount_pct > currentDiscount) {
        frappe.show_alert({
            message: `💡 ${item.item_code}: AI suggests ${tier.discount_pct}% discount for qty ${item.qty}`,
            indicator: 'blue'
        }, 7);
        
        // Optionally auto-apply
        frappe.confirm(
            `Apply AI-suggested ${tier.discount_pct}% discount for ${item.item_code}?<br>
            <small>${tier.reasoning}</small>`,
            () => {
                frappe.model.set_value(item.doctype, item.name, 'discount_percentage', tier.discount_pct);
            }
        );
    }
}

function showVolumeDiscountRecommendations(frm) {
    if (!frm.doc.items || frm.doc.items.length === 0) {
        frappe.msgprint('No items in invoice');
        return;
    }
    
    const dialog = new frappe.ui.Dialog({
        title: '📦 Volume Discount Recommendations',
        size: 'large',
        fields: [
            {
                fieldname: 'item_code',
                label: 'Select Item',
                fieldtype: 'Select',
                options: frm.doc.items.map(i => i.item_code).join('\n'),
                reqd: 1,
                onchange: function() {
                    const item = frm.doc.items.find(i => i.item_code === this.value);
                    if (item) {
                        dialog.set_value('base_price', item.rate);
                    }
                }
            },
            {
                fieldname: 'base_price',
                label: 'Base Price',
                fieldtype: 'Currency',
                reqd: 1
            },
            {
                fieldname: 'quantity_tiers',
                label: 'Quantity Tiers (comma-separated)',
                fieldtype: 'Data',
                default: '100, 500, 1000, 5000, 10000'
            },
            {
                fieldname: 'results',
                fieldtype: 'HTML'
            }
        ],
        primary_action_label: 'Get Recommendations',
        primary_action: function(values) {
            const tiers = values.quantity_tiers.split(',').map(t => parseInt(t.trim()));
            
            frappe.call({
                method: 'api.ai_pricing.get_volume_discount_recommendations',
                args: {
                    item_code: values.item_code,
                    base_price: values.base_price,
                    quantity_tiers: tiers
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        displayVolumeRecommendations(dialog, r.message.recommendations);
                    }
                }
            });
        }
    });
    
    dialog.show();
}

function displayVolumeRecommendations(dialog, recommendations) {
    let html = '<div class="volume-recommendations">';
    
    if (recommendations.raw_response) {
        html += `<div class="alert alert-info">${recommendations.recommendations}</div>`;
    } else {
        html += '<h4>Recommended Discount Tiers</h4>';
        html += '<table class="table table-bordered">';
        html += '<tr><th>Quantity</th><th>Discount %</th><th>Price</th><th>Reasoning</th></tr>';
        
        recommendations.discount_tiers.forEach(tier => {
            html += `<tr>
                <td>${tier.quantity}+</td>
                <td><strong>${tier.discount_pct}%</strong></td>
                <td>$${tier.price}</td>
                <td><small>${tier.reasoning}</small></td>
            </tr>`;
        });
        
        html += '</table>';
        
        if (recommendations.overall_strategy) {
            html += `<div class="alert alert-info">
                <strong>Strategy:</strong> ${recommendations.overall_strategy}
            </div>`;
        }
        
        if (recommendations.expected_impact) {
            html += `<div class="alert alert-success">
                <strong>Expected Impact:</strong> ${recommendations.expected_impact}
            </div>`;
        }
    }
    
    html += '</div>';
    
    dialog.fields_dict.results.$wrapper.html(html);
}

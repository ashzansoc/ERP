/**
 * Ocean Shipment - AI Pricing Integration
 * Adds AI-powered pricing suggestions to Ocean Shipment form
 */

frappe.ui.form.on('Ocean Shipment', {
    refresh: function(frm) {
        // Add AI Pricing button if landed cost is calculated
        if (frm.doc.total_landed_cost && frm.doc.total_landed_cost > 0) {
            frm.add_custom_button(__('🤖 Get AI Pricing Suggestions'), function() {
                getAIPricingSuggestions(frm);
            }, __('AI Features'));
        }
        
        // Add Country Analytics button
        if (frm.doc.destination_country) {
            frm.add_custom_button(__('🌍 Country Pricing Analytics'), function() {
                showCountryAnalytics(frm);
            }, __('AI Features'));
        }
        
        // Add FX Risk Analysis button
        if (frm.doc.base_currency && frm.doc.base_currency !== 'USD') {
            frm.add_custom_button(__('💱 FX Risk Analysis'), function() {
                analyzeFXRisk(frm);
            }, __('AI Features'));
        }
        
        // Show AI suggestions if already calculated
        if (frm.doc.items) {
            frm.doc.items.forEach(item => {
                if (item.ai_suggested_margin) {
                    highlightAISuggestion(frm, item);
                }
            });
        }
    },
    
    after_save: function(frm) {
        // Auto-trigger AI suggestions if landed cost just calculated
        if (frm.doc.total_landed_cost && !frm.doc.__ai_suggestions_shown) {
            frappe.show_alert({
                message: '💡 AI pricing suggestions available! Click the AI Features button.',
                indicator: 'blue'
            }, 5);
            frm.doc.__ai_suggestions_shown = true;
        }
    }
});

frappe.ui.form.on('Ocean Shipment Item', {
    item_code: function(frm, cdt, cdn) {
        const item = locals[cdt][cdn];
        
        // Show historical pricing info
        if (item.item_code) {
            showHistoricalPricing(frm, item);
        }
    }
});

function getAIPricingSuggestions(frm) {
    if (!frm.doc.items || frm.doc.items.length === 0) {
        frappe.msgprint('No items found in shipment');
        return;
    }
    
    frappe.show_alert({
        message: '🤖 Analyzing pricing data with AI...',
        indicator: 'blue'
    });
    
    let processed = 0;
    const total = frm.doc.items.length;
    
    frm.doc.items.forEach((item, idx) => {
        if (!item.total_landed_cost || !item.quantity) {
            processed++;
            return;
        }
        
        frappe.call({
            method: 'api.ai_pricing.get_margin_suggestion',
            args: {
                item_code: item.item_code,
                landed_cost: item.total_landed_cost,
                quantity: item.quantity
            },
            callback: function(r) {
                processed++;
                
                if (r.message && r.message.success) {
                    const suggestion = r.message.suggestion;
                    
                    // Update item with AI suggestions
                    frappe.model.set_value(item.doctype, item.name, {
                        'ai_suggested_margin': suggestion.recommended_margin,
                        'ai_target_price': suggestion.target_price,
                        'ai_min_margin': suggestion.min_margin,
                        'ai_reasoning': suggestion.reasoning
                    });
                    
                    highlightAISuggestion(frm, item);
                }
                
                // Show completion message when all done
                if (processed === total) {
                    frappe.show_alert({
                        message: `✅ AI suggestions generated for ${total} items`,
                        indicator: 'green'
                    }, 5);
                    frm.refresh_field('items');
                }
            }
        });
    });
}

function highlightAISuggestion(frm, item) {
    // Add visual indicator for AI suggestions
    const row = frm.fields_dict.items.grid.grid_rows_by_docname[item.name];
    if (row) {
        row.wrapper.find('.grid-row').css('background-color', '#e8f5e9');
        row.wrapper.find('.grid-row').attr('title', 'AI suggestions available');
    }
}

function showHistoricalPricing(frm, item) {
    frappe.call({
        method: 'api.ai_pricing.compare_historical_pricing',
        args: {
            item_code: item.item_code,
            proposed_price: item.unit_landed_cost || 0
        },
        callback: function(r) {
            if (r.message && r.message.success && r.message.comparison) {
                const comp = r.message.comparison;
                
                if (!comp.raw_response) {
                    frappe.show_alert({
                        message: `📊 ${item.item_code}: ${comp.comparison || 'Historical data available'}`,
                        indicator: 'blue'
                    }, 3);
                }
            }
        }
    });
}

function showCountryAnalytics(frm) {
    if (!frm.doc.destination_country) {
        frappe.msgprint('Destination country not set');
        return;
    }
    
    // Collect unique items
    const items = [...new Set(frm.doc.items.map(i => i.item_code))];
    
    if (items.length === 0) {
        frappe.msgprint('No items to analyze');
        return;
    }
    
    const dialog = new frappe.ui.Dialog({
        title: '🌍 Country Pricing Analytics',
        size: 'large',
        fields: [
            {
                fieldname: 'item_code',
                label: 'Select Item',
                fieldtype: 'Select',
                options: items.join('\n'),
                reqd: 1
            },
            {
                fieldname: 'countries',
                label: 'Compare with Countries',
                fieldtype: 'MultiSelect',
                options: getCountryList(),
                description: 'Leave empty to compare with all available data'
            },
            {
                fieldname: 'results',
                fieldtype: 'HTML'
            }
        ],
        primary_action_label: 'Analyze',
        primary_action: function(values) {
            frappe.call({
                method: 'api.ai_pricing.analyze_country_pricing',
                args: {
                    item_code: values.item_code,
                    countries: values.countries ? JSON.parse(values.countries) : [frm.doc.destination_country]
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        displayCountryAnalytics(dialog, r.message.analysis);
                    }
                }
            });
        }
    });
    
    dialog.show();
}

function displayCountryAnalytics(dialog, analysis) {
    let html = '<div class="ai-analytics-results">';
    
    if (analysis.raw_response) {
        html += `<div class="alert alert-info">${analysis.analysis}</div>`;
    } else {
        html += '<h4>Price Variations</h4>';
        html += '<table class="table table-bordered">';
        html += '<tr><th>Country</th><th>Avg Price</th><th>Variance</th></tr>';
        
        for (const [country, data] of Object.entries(analysis.variations || {})) {
            html += `<tr><td>${country}</td><td>${data.avg_price}</td><td>${data.variance}</td></tr>`;
        }
        
        html += '</table>';
        
        if (analysis.opportunities) {
            html += '<h4>Opportunities</h4><ul>';
            analysis.opportunities.forEach(opp => {
                html += `<li>${opp}</li>`;
            });
            html += '</ul>';
        }
        
        if (analysis.risks) {
            html += '<h4>Risks</h4><ul>';
            analysis.risks.forEach(risk => {
                html += `<li>${risk}</li>`;
            });
            html += '</ul>';
        }
    }
    
    html += '</div>';
    
    dialog.fields_dict.results.$wrapper.html(html);
}

function analyzeFXRisk(frm) {
    const currencies = [frm.doc.base_currency];
    
    // Add any other currencies from cost components
    if (frm.doc.cost_components) {
        frm.doc.cost_components.forEach(cost => {
            if (cost.currency && !currencies.includes(cost.currency)) {
                currencies.push(cost.currency);
            }
        });
    }
    
    frappe.call({
        method: 'api.ai_pricing.analyze_fx_risk',
        args: {
            currencies: currencies,
            transaction_value: frm.doc.total_landed_cost || 0,
            settlement_date: frm.doc.expected_delivery_date || frappe.datetime.add_days(frappe.datetime.nowdate(), 30)
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                displayFXRiskAnalysis(r.message.analysis);
            }
        }
    });
}

function displayFXRiskAnalysis(analysis) {
    let html = '<div class="fx-risk-analysis">';
    
    if (analysis.raw_response) {
        html += `<div class="alert alert-info">${analysis.analysis}</div>`;
    } else {
        // Risk level indicator
        const riskColor = {
            'Low': 'green',
            'Medium': 'orange',
            'High': 'red'
        };
        
        html += `<div class="alert alert-${riskColor[analysis.risk_level] || 'info'}">`;
        html += `<h4>Risk Level: ${analysis.risk_level}</h4>`;
        html += `<p>Potential Exposure: $${analysis.exposure || 0}</p>`;
        html += '</div>';
        
        if (analysis.hedging_strategy) {
            html += '<h4>Hedging Recommendations</h4>';
            html += `<p>${JSON.stringify(analysis.hedging_strategy, null, 2)}</p>`;
        }
        
        if (analysis.alerts && analysis.alerts.length > 0) {
            html += '<h4>Alert Triggers</h4><ul>';
            analysis.alerts.forEach(alert => {
                html += `<li>${alert.currency}: Monitor rate ${alert.threshold} - ${alert.action}</li>`;
            });
            html += '</ul>';
        }
    }
    
    html += '</div>';
    
    frappe.msgprint({
        title: '💱 FX Risk Analysis',
        message: html,
        indicator: 'blue',
        wide: true
    });
}

function getCountryList() {
    // Common trading countries
    return [
        'USA', 'UK', 'Germany', 'France', 'Italy', 'Spain',
        'China', 'Japan', 'South Korea', 'India', 'Singapore',
        'Australia', 'Canada', 'Mexico', 'Brazil', 'UAE'
    ].join('\n');
}

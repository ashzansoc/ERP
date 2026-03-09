/**
 * Workflow UI Enhancements
 * Client-side scripts for improved workflow user experience
 */

// Sales Order Workflow Enhancements
frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        if (frm.doc.workflow_state) {
            add_workflow_indicators(frm);
            add_workflow_timeline(frm);
            add_quick_actions(frm);
        }
    },
    
    workflow_state: function(frm) {
        update_workflow_fields(frm);
    }
});

// Purchase Order Workflow Enhancements
frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        if (frm.doc.workflow_state) {
            add_workflow_indicators(frm);
            add_workflow_timeline(frm);
            add_quick_actions(frm);
        }
    },
    
    workflow_state: function(frm) {
        update_workflow_fields(frm);
    }
});

function add_workflow_indicators(frm) {
    // Add visual indicators for workflow progress
    const workflow_states = get_workflow_states(frm.doctype);
    const current_state = frm.doc.workflow_state;
    const current_index = workflow_states.indexOf(current_state);
    
    let html = '<div class="workflow-progress">';
    html += '<div class="progress-bar-container">';
    
    workflow_states.forEach((state, index) => {
        const is_complete = index < current_index;
        const is_current = index === current_index;
        const status_class = is_complete ? 'complete' : (is_current ? 'current' : 'pending');
        
        html += `<div class="progress-step ${status_class}">
            <div class="step-circle">${index + 1}</div>
            <div class="step-label">${state}</div>
        </div>`;
        
        if (index < workflow_states.length - 1) {
            html += `<div class="progress-line ${is_complete ? 'complete' : ''}"></div>`;
        }
    });
    
    html += '</div></div>';
    
    frm.set_df_property('workflow_stage', 'options', html);
}

function add_workflow_timeline(frm) {
    // Add workflow history timeline
    frappe.call({
        method: 'api.workflow_automation.get_workflow_history',
        args: {
            doctype: frm.doctype,
            docname: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                let timeline_html = '<div class="workflow-timeline">';
                
                r.message.forEach(entry => {
                    timeline_html += `
                        <div class="timeline-entry">
                            <div class="timeline-date">${frappe.datetime.str_to_user(entry.date)}</div>
                            <div class="timeline-content">
                                <strong>${entry.user}</strong> changed state from 
                                <span class="badge">${entry.from_state}</span> to 
                                <span class="badge badge-success">${entry.to_state}</span>
                            </div>
                        </div>
                    `;
                });
                
                timeline_html += '</div>';
                
                frm.dashboard.add_section(timeline_html, __('Workflow History'));
            }
        }
    });
}

function add_quick_actions(frm) {
    // Add quick action buttons based on current state
    frappe.call({
        method: 'api.workflow_automation.get_workflow_status',
        args: {
            doctype: frm.doctype,
            docname: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.available_actions) {
                r.message.available_actions.forEach(action => {
                    frm.add_custom_button(action.action, function() {
                        apply_workflow_action(frm, action.action);
                    }, __('Workflow Actions'));
                });
            }
        }
    });
}

function apply_workflow_action(frm, action) {
    frappe.confirm(
        `Are you sure you want to ${action}?`,
        function() {
            frappe.call({
                method: 'api.workflow_automation.apply_workflow_action',
                args: {
                    doctype: frm.doctype,
                    docname: frm.doc.name,
                    action: action
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.show_alert({
                            message: r.message.message,
                            indicator: 'green'
                        });
                        frm.reload_doc();
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: r.message.error,
                            indicator: 'red'
                        });
                    }
                }
            });
        }
    );
}

function update_workflow_fields(frm) {
    // Update field visibility based on workflow state
    const state = frm.doc.workflow_state;
    
    if (frm.doctype === 'Sales Order') {
        // Show/hide fields based on state
        frm.toggle_display('production_status', 
            ['Production In Progress', 'Production Complete'].includes(state));
        frm.toggle_display('packing_status', 
            ['Packing In Progress', 'Ready for Shipment'].includes(state));
        frm.toggle_display('forex_realization_date', 
            ['Payment Received', 'Forex Realized'].includes(state));
    }
    
    if (frm.doctype === 'Purchase Order') {
        frm.toggle_display('customs_status', 
            ['Customs Clearance', 'Customs Cleared'].includes(state));
        frm.toggle_display('grn_status', 
            ['GRN Pending', 'GRN Completed'].includes(state));
        frm.toggle_display('landed_cost_status', 
            ['Landed Cost Calculated', 'Inventory Updated'].includes(state));
    }
}

function get_workflow_states(doctype) {
    // Return workflow states for the doctype
    if (doctype === 'Sales Order') {
        return [
            'Lead',
            'Quotation Pending',
            'Quotation Approved',
            'Sales Order Created',
            'Proforma Invoice Issued',
            'Production In Progress',
            'Production Complete',
            'Packing In Progress',
            'Ready for Shipment',
            'Shipment Dispatched',
            'Export Invoice Generated',
            'Payment Received',
            'Forex Realized',
            'Export Complete'
        ];
    } else if (doctype === 'Purchase Order') {
        return [
            'Purchase Request',
            'PR Approved',
            'PO Created',
            'PO Approved',
            'Shipment In Transit',
            'Customs Clearance',
            'Customs Cleared',
            'GRN Pending',
            'GRN Completed',
            'Landed Cost Calculated',
            'Inventory Updated',
            'Payment Pending',
            'Payment Completed',
            'Import Complete'
        ];
    }
    return [];
}

// Dashboard for Pending Approvals
frappe.pages['workflow-dashboard'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Workflow Dashboard',
        single_column: true
    });
    
    page.add_button('Refresh', function() {
        load_pending_approvals(page);
    });
    
    load_pending_approvals(page);
};

function load_pending_approvals(page) {
    frappe.call({
        method: 'api.workflow_automation.get_pending_approvals',
        callback: function(r) {
            if (r.message) {
                render_pending_approvals(page, r.message);
            }
        }
    });
}

function render_pending_approvals(page, approvals) {
    let html = '<div class="pending-approvals">';
    
    if (approvals.length === 0) {
        html += '<p class="text-muted">No pending approvals</p>';
    } else {
        html += '<table class="table table-bordered">';
        html += '<thead><tr><th>Document</th><th>Title</th><th>State</th><th>Date</th><th>Action</th></tr></thead>';
        html += '<tbody>';
        
        approvals.forEach(approval => {
            html += `<tr>
                <td><a href="/app/${approval.doctype.toLowerCase().replace(' ', '-')}/${approval.name}">${approval.name}</a></td>
                <td>${approval.title}</td>
                <td><span class="badge">${approval.state}</span></td>
                <td>${frappe.datetime.str_to_user(approval.date)}</td>
                <td><button class="btn btn-sm btn-primary" onclick="open_document('${approval.doctype}', '${approval.name}')">Review</button></td>
            </tr>`;
        });
        
        html += '</tbody></table>';
    }
    
    html += '</div>';
    
    page.main.html(html);
}

function open_document(doctype, docname) {
    frappe.set_route('Form', doctype, docname);
}

// Add CSS for workflow UI
frappe.ready(function() {
    const style = `
        <style>
        .workflow-progress {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .progress-bar-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .progress-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
        }
        
        .step-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #e9ecef;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .progress-step.complete .step-circle {
            background: #28a745;
            color: white;
        }
        
        .progress-step.current .step-circle {
            background: #007bff;
            color: white;
        }
        
        .progress-line {
            flex: 1;
            height: 2px;
            background: #e9ecef;
            margin: 0 10px;
        }
        
        .progress-line.complete {
            background: #28a745;
        }
        
        .step-label {
            font-size: 12px;
            text-align: center;
            max-width: 100px;
        }
        
        .workflow-timeline {
            margin-top: 20px;
        }
        
        .timeline-entry {
            padding: 10px;
            border-left: 3px solid #007bff;
            margin-bottom: 10px;
            background: #f8f9fa;
        }
        
        .timeline-date {
            font-size: 12px;
            color: #6c757d;
        }
        
        .pending-approvals {
            padding: 20px;
        }
        </style>
    `;
    
    $('head').append(style);
});

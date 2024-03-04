import frappe
from frappe.utils.background_jobs import enqueue
from frappe import msgprint, _

@frappe.whitelist()
def send_email(item_code):
    # Fetch the latest 5 sales invoices for the specified item code
    invoices = frappe.db.sql(
        """
        SELECT si.name, si.posting_date
        FROM `tabSales Invoice` si
        JOIN `tabSales Invoice Item` sii ON si.name = sii.parent
        WHERE sii.item_code = %s
        ORDER BY si.posting_date DESC
        LIMIT 5
        """,
        item_code,
        as_dict=True,
    )

    if invoices:
        email_template = frappe.get_doc("Email Template", "Sales Invoice Template")

        # Create a list to store attachment details
        attachments = []

        # Create the email message
        message = email_template.response
        subject = "Sales Invoices"
        recipient = frappe.session.user

        # Iterate through each invoice and add its details to the email
        for inv in invoices:
            si_doc = frappe.get_doc("Sales Invoice", inv["name"])

            # Customize the email content for each invoice
            email_content = message.replace("{{ invoice_name }}", si_doc.name)
            email_content = email_content.replace("{{ invoice_date }}", str(si_doc.posting_date))

            current_attachments = []

            attachment = frappe.attach_print(
                "Sales Invoice", si_doc.name, file_name=si_doc.name
            )
            current_attachments.append(attachment)

            # Send the email with the correct template and attachment for the current invoice
            frappe.sendmail(
                recipients=[recipient],
                message=email_content,
                subject=subject,
                attachments=current_attachments,
            )

    
            attachments.extend(current_attachments)

            frappe.msgprint(_("Email sent successfully"))

    else:
        frappe.msgprint(_("No invoices found for the given item"))
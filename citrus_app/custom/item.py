import frappe
from frappe.utils.background_jobs import enqueue
from frappe import msgprint, _

import frappe
from frappe.utils import now_datetime

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
        email_template = frappe.get_doc("Email Template","Sales Invoice Template")

        # Create a list to store attachment details
        attachments = []

        # Get the attachment for each invoice
        for inv in invoices:
            si_doc = frappe.get_doc("Sales Invoice", inv["name"])

            email_content = email_template.response.replace("{{ invoice_name }}", si_doc.name)
            email_content = email_content.replace("{{ invoice_date }}", str(si_doc.posting_date))
            


            # Create the email message
            message = email_content
            subject = "Sales Invoices"
            recipient = frappe.session.user
            attachment = frappe.attach_print(
                "Sales Invoice", si_doc.name, file_name = si_doc.name
            )
            attachments.append(attachment)
            
            # Send the email with attachments
            frappe.sendmail(
                recipients=[recipient],
                message=message,
                subject=subject,
                attachments=attachments,
            )

            frappe.msgprint(_("Email sent successfully"))
    else:
        frappe.msgprint(_("No invoices found for the given item"))




    


   

   
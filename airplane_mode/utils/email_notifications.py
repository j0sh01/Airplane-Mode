import frappe
from frappe import _
from frappe.utils import getdate, add_days, format_date


def send_rent_reminders():
    """Send rent reminders daily starting from (due_date - reminder_days_before) until due date."""

    try:
        # Fetch settings for rent reminders
        enable_rent_reminders = frappe.db.get_single_value("Shop Settings", "enable_rent_reminders")
        reminder_days_before = frappe.db.get_single_value("Shop Settings", "reminder_days_before")

        if not enable_rent_reminders:
            frappe.log_error("Rent reminders are disabled in settings.", "Rent Reminder Configuration Error")
            return

        if not reminder_days_before or reminder_days_before <= 0:
            frappe.log_error("Reminder days before is not properly configured.", "Rent Reminder Configuration Error")
            return

        # Get today's date
        today = frappe.utils.getdate()
        reminder_date = frappe.utils.add_days(today, reminder_days_before)

        # Find all unpaid payment schedules within the reminder period
        due_schedules = frappe.get_all(
            "Payment Schedule",
            filters={
                "due_date": [">=", today],
                "due_date": ["<=", reminder_date],
                "status": ["in", ["Pending", "Overdue"]],
            },
            fields=["name", "tenant", "shop", "due_date", "amount"]
        )

        if not due_schedules:
            return

        # Get default sender email
        sender = frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id")
        if not sender:
            frappe.log_error("Default outgoing email account is not configured.", "Rent Reminder Configuration Error")
            return

        for schedule in due_schedules:
            tenant = frappe.get_doc("Shop Tenant", schedule.tenant)
            shop = frappe.get_doc("Airport Shop", schedule.shop)

            if not tenant.email:
                frappe.log_error(f"Missing email for tenant {tenant.tenant_name} (ID: {tenant.name}).", "Rent Reminder Skipped")
                continue

            subject = f"📅 Rent Reminder for {shop.shop_name} - Due {frappe.utils.format_date(schedule.due_date)}"
            message = f"""
                <p>Dear {tenant.tenant_name},</p>
                <p>This is a reminder that your rent payment of 
                <strong>{frappe.format_value(schedule.amount, {'fieldtype': 'Currency'})}</strong> 
                for <strong>{shop.shop_name}</strong> is due on 
                <strong>{frappe.utils.format_date(schedule.due_date)}</strong>.</p>
                <p>Please ensure timely payment to avoid any late fees.</p>
                <p>Best regards,<br>Rent Management Team</p>
            """

            frappe.sendmail(
                recipients=[tenant.email],
                sender=sender,
                subject=subject,
                message=message,
                reference_doctype="Payment Schedule",
                reference_name=schedule.name,
                now=True 
            )

    except Exception as e:
        frappe.log_error(f"Error in rent reminder process: {str(e)}", "Rent Reminder Process Failed")


def send_payment_confirmation(schedule_name):
    """Send confirmation email when a tenant makes a rent payment."""
    schedule = frappe.get_doc("Payment Schedule", schedule_name)
    tenant = frappe.get_doc("Shop Tenant", schedule.tenant)
    shop = frappe.get_doc("Airport Shop", schedule.shop)

    if not tenant.email:
        frappe.log_error(f"Missing email for tenant {tenant.tenant_name}", "Payment Confirmation Failed")
        return

    sender = frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id")
    if not sender:
        frappe.throw("Default email account not set", "Payment Confirmation Failed")
        return

    subject = f"Payment Received for {shop.shop_name}"
    message = f"""
        <p>Dear {tenant.tenant_name},</p>
        <p>We have received your rent payment of {frappe.format_value(schedule.amount, {'fieldtype': 'Currency'})} 
        for {shop.shop_name}.</p>
    """

    # Send email
    frappe.sendmail(
        recipients=tenant.email,
        sender=sender,
        subject=subject,
        message=message,
        reference_doctype="Payment Schedule",
        reference_name=schedule.name,
        now=True
    )

    # Log communication
    frappe.get_doc({
        "doctype": "Communication",
        "subject": subject,
        "content": message,
        "recipients": tenant.email,
        "communication_medium": "Email",
        "sent_or_received": "Sent",
        "reference_doctype": "Payment Schedule",
        "reference_name": schedule.name
    }).insert(ignore_permissions=True)

    frappe.logger().info(f"Payment confirmation email sent to {tenant.email} for {shop.shop_name}.")


def setup_scheduled_job():
    """Create or update the scheduled job for sending rent reminders."""
    
    job_name = "Daily Rent Reminder Emails"
    method_path = "airplane_mode.utils.email_notifications.send_rent_reminders"

    job = frappe.get_doc({
        "doctype": "Scheduled Job Type",
        "method": method_path,
        "frequency": "Daily",  
        "docstatus": 0,
        "name": job_name,
        "status": "Active",
        "enabled": 1,
        "create_log": 1  
    })

    try:
        # Check if the job already exists
        existing_job = frappe.get_doc("Scheduled Job Type", job_name)
        existing_job.update(job)
        existing_job.save()
        frappe.db.commit()

    except frappe.DoesNotExistError:
        # Create a new job if it doesn't exist
        job.insert(ignore_permissions=True)
        frappe.db.commit()


def execute_scheduled_job():
    """Wrapper function to handle scheduled job execution for rent reminders."""
    try:
        from airplane_mode.utils.email_notifications import send_rent_reminders
        send_rent_reminders()
    except Exception as e:
        frappe.log_error(
            f"⚠ Error in scheduled rent reminder job: {str(e)}",
            "Scheduled Job Error"
        )
        raise

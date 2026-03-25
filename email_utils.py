import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def send_ticket_email(ticket_id, data):
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get("BREVO_API_KEY")

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        priority = data.get('priority')

        color = {
            "Urgent": "#c0392b",
            "High": "#e74c3c",
            "Medium": "#f39c12",
            "Low": "#27ae60"
        }.get(priority, "#3498db")

        html_content = f"""
        <html>
        <body style="font-family: Arial; background:#f4f6f9; padding:20px;">
        
        <div style="max-width:600px; margin:auto; background:white; border-radius:10px; padding:20px;">
            
            <h2 style="background:#2c3e50; color:white; padding:10px; border-radius:5px;">
                🛠 New Maintenance Ticket
            </h2>

            <p>A new maintenance request has been submitted.</p>

            <p><b>Ticket ID:</b> #{ticket_id}</p>
            <p><b>Category:</b> {data.get('category')}</p>
            <p><b>Location:</b> Block {data.get('block')}, Floor {data.get('floor')}, Room {data.get('room_no')}</p>

            <p><b>Priority:</b> 
                <span style="background:{color}; color:white; padding:5px 10px; border-radius:5px;">
                    {priority}
                </span>
            </p>

            <p><b>Description:</b><br>{data.get('description')}</p>

            <hr>

            <p><b>Submitted By:</b><br>
            {data.get('name')}<br>
            {data.get('email')}<br>
            {data.get('phone')}
            </p>

            <p style="margin-top:20px; font-size:12px; color:#777;">
                Campus Maintenance Portal • Automated Notification
            </p>

        </div>
        </body>
        </html>
        """

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "2501730151@krmu.edu.in", "name": "Maintenance Team"}],
            sender={"email": "chaudharyanupam746@gmail.com", "name": "Campus Maintenance"},
            subject=f"New Maintenance Ticket #{ticket_id}",
            html_content=html_content
        )

        response = api_instance.send_transac_email(send_smtp_email)
        print("✅ Email sent:", response)

    except ApiException as e:
        print("❌ Email failed:", e)
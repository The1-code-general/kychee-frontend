from flask import Flask, render_template, request
import smtplib
import os

app = Flask(__name__)

def generate_client_data(field_prefix, request_form):
    client_data = []
    index = 1
    while True:
        client_name = request_form.get(f'{field_prefix}_client_name_{index}')
        if client_name:
            product = request_form.get(f'{field_prefix}_product_{index}')
            prior_activities = request_form.get(f'{field_prefix}_prior_activities_{index}')
            present_activities = request_form.get(f'{field_prefix}_present_activities_{index}')
            outstanding_tasks = request_form.get(f'{field_prefix}_outstanding_tasks_{index}')
            
            client_info = {
                'Client Name': client_name,
                'Product': product,
                'Prior Activities': prior_activities,
                'Present Activities': present_activities,
                'Outstanding Tasks': outstanding_tasks
            }
            client_data.append(client_info)
            index += 1
        else:
            break
    return client_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    
    # Get the recipient's email addresses from the form
    recipient_emails = request.form.get('recipient_emails')
    
    # Check if recipient_emails is not None and is not an empty string
    if recipient_emails is not None and recipient_emails.strip() != "":
        # Split the recipient_emails string into a list of email addresses
        recipients = recipient_emails.split(',')
        
        subject = 'Weekly Report'
        
        # Create the email body with the form data formatted as an HTML table
        body = f'<html><body style="background-color: #f4f4f4; padding: 20px; font-family: Arial, sans-serif;">'
        body += f'<h2 style="text-align: center;">Lychee Integrated Solutions Weekly Report</h2>'
        body += f'<p>Thank you, {name}, for submitting your weekly report.</p>'
        
        sections = [
            ('Support', 'support'),
            ('Implementation', 'implementation'),
            ('Reimplementation/Rescue', 'reimplementation_rescue')
        ]

        # Iterate through sections and add section name above each section
        for section_name, field_prefix in sections:
            client_data = generate_client_data(field_prefix, request.form)
            
            # Check if there is data for this section
            if client_data:
                body += f'<div style="margin-top: 20px;"><b>{section_name} Section</b></div>'
                
                # Add client data to the email body in a horizontal table format
                body += '<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">'
                # Add table header row
                body += '<tr><th style="border: 1px solid black; padding: 8px;">Client Name</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Product</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Prior Activities</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Present Activities</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Outstanding Tasks</th></tr>'
                
                # Add client data rows
                for client in client_data:
                    body += '<tr>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Client Name"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Product"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Prior Activities"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Present Activities"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Outstanding Tasks"]}</td>'
                    body += '</tr>'
                
                body += '</table>'
        
        body += f'<p><b>Recipient Email(s):</b> {", ".join(recipients)}</p>'
        body += '</body></html>'
        
        try:
            # Use environment variables for secure configuration
            smtp_server = os.environ.get('SMTP_SERVER')
            smtp_port = os.environ.get('SMTP_PORT')
            sender_email = os.environ.get('SENDER_EMAIL')
            sender_password = os.environ.get('SENDER_PASSWORD')

            # Send the email with HTML content
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('emmapharez29@gmail.com', 'tioc ztnr pbwr nsaf')
            
            # Set the content type to HTML
            msg = f'Subject: {subject}\n'
            msg += 'MIME-Version: 1.0\n'
            msg += 'Content-type: text/html\n\n'
            msg += body
            
            # Send the email to multiple recipients
            server.sendmail('emmapharez29@gmail.com', recipients, msg)
            server.quit()
            
            # Render the success page with the provided name
            return render_template('success.html', name=name)
        except smtplib.SMTPConnectError as e:
            return f'Error connecting to SMTP server: {str(e)}'
        except smtplib.SMTPAuthenticationError as e:
            return f'Error authenticating with SMTP server: {str(e)}'
        except smtplib.SMTPException as e:
            return f'SMTP error: {str(e)}'
        except Exception as e:
            return f'An unexpected error occurred: {str(e)}'
    else:
        return "Recipient's email address is missing or invalid"

if __name__ == '__main__':
    app.run(debug=True)
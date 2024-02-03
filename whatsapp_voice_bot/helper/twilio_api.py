from twilio.rest import Client

from config import config

account_sid = config.TWILIO_SID
auth_token = config.TWILIO_TOKEN
client = Client(account_sid, auth_token)

def send_message(to: str, message: str, gcs_audio_url ) -> None:
    try:

        message = client.messages.create(
            media_url=[gcs_audio_url],
            from_=config.FROM,
            body = message,
            to=to
        )
        print(f"Message sent successfully! {message.sid}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")
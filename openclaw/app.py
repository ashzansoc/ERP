import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize the app with bot token and socket mode
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def handle_app_mention(event, say):
    """Handle app mentions"""
    say(f"Hello <@{event['user']}>! OpenClaw is ready.")

@app.event("message")
def handle_message(event, say):
    """Handle direct messages"""
    if event.get("channel_type") == "im":
        say("Thanks for your message!")

@app.command("/openclaw")
def handle_openclaw_command(ack, command, say):
    """Handle /openclaw slash command"""
    ack()
    say(f"OpenClaw received: {command.get('text', 'No message')}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    print("⚡️ OpenClaw is running!")
    handler.start()

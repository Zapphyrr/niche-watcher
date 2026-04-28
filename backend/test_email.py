from services import EmailService

email_service = EmailService()

test_post = [
    {
        "title": "Test Email Post",
        "url": "https://example.com/test-post",
        "content": "This is a test post for email sending.",
        "source": "Test Source",
    },
    {
        "title": "Another Test Post",
        "url": "https://example.com/another-test-post",
        "content": "This is another test post for email sending.",
        "source": "Test Source 2",
    }
    
    
]

success = email_service.send_weekly_digest("dimitri.desvoy@gmail.com", test_post)
if success:
    print("Email sent successfully!")
else:    print("Failed to send email.")
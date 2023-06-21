import telegram
import requests

# Define a class for the bot
class GadaaJobsBot:

    # Define the constructor with the bot token
    def init(self, token):

    # Create a bot object with the token
        self.bot = telegram.Bot(token=token)

        # Create an updater object with the token and use_context=True
        self.updater = telegram.ext.Updater(token=token, use_context=True)

        # Get the dispatcher object from the updater
        self.dispatcher = self.updater.dispatcher

        # Create command handlers for the start, jobs, apply and submit commands and add them to the dispatcher
        self.start_handler = telegram.ext.CommandHandler('start', self.start)
        self.dispatcher.add_handler(self.start_handler)
        self.jobs_handler = telegram.ext.CommandHandler('jobs', self.jobs)
        self.dispatcher.add_handler(self.jobs_handler)
        self.apply_handler = telegram.ext.CommandHandler('apply', self.apply)
        self.dispatcher.add_handler(self.apply_handler)
        self.submit_handler = telegram.ext.CommandHandler('submit', self.submit)
        self.dispatcher.add_handler(self.submit_handler)

    # Define a method to start the bot
    def start_bot(self):

        # Start the bot
        self.updater.start_polling()

    # Define a method to handle the start command
    def start(self, update, context):

        # Send a welcome message to the user
        self.bot.send_message(chat_id=update.message.chat_id, text='Welcome to Gadaa Jobs Bot! I can help you find and apply for jobs in various fields. To see the available jobs, type /jobs.')

     # Define a method to handle the jobs command
    def jobs(self, update, context):

        # Get the list of jobs from an API endpoint (you can change this to your own source)
        response = requests.get('https://api.example.com/jobs')

        # Check if the response is successful
        if response.status_code == 200:

        # Parse the response as JSON
            data = response.json()

            # Create an empty list to store the job titles and ids
            jobs_list = []

            # Loop through the data and append the job titles and ids to the list
            for job in data:
                jobs_list.append(f"{job['title']} - /apply_{job['id']}")

            # Join the list items with a newline character
                jobs_text = '\n'.join(jobs_list)

            # Send a message to the user with the list of jobs and instructions on how to apply
            self.bot.send_message(chat_id=update.message.chat_id, text=f'Here are the available jobs:\n{jobs_text}\nTo apply for a job, type /apply followed by the job id. For example, /apply_1.')
        else:

        # Send an error message to the user if the response is not successful
            self.bot.send_message(chat_id=update.message.chat_id, text='Sorry, something went wrong. Please try again later.')

        # Define a method to handle the apply command
    def apply(self, update, context):

    # Get the job id from the command argument
        job_id = update.message.text.split('_')[1]

        # Get the job details from an API endpoint using the job id (you can change this to your own source)
        response = requests.get(f'https://api.example.com/jobs/{job_id}')

        # Check if the response is successful
        if response.status_code == 200:

        # Parse the response as JSON
            data = response.json()

            # Store the job title and description in variables
            job_title = data['title']
            job_description = data['description']

            # Send a message to the user with the job details and instructions on how to submit their application
            self.bot.send_message(chat_id=update.message.chat_id, text=f'You are applying for {job_title}.\n{job_description}\nTo submit your application, type /submit followed by your name and email. For example, /submit John Doe john.doe@example.com.')
        else:

            # Send an error message to the user if the response is not successful or if the job id is invalid
            self.bot.send_message(chat_id=update.message.chat_id, text='Sorry, this job does not exist or something went wrong. Please try again later.')

    # Define a method to handle the submit command
    def submit(self, update, context):

    # Get the user name and email from the command argument
        user_name = update.message.text.split()[1]
        user_email = update.message.text.split()[2]

        # Validate the email format using a simple regex (you can use a more robust validation method if you want)
        import re
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
        if re.match(email_pattern, user_email):

        # Send a success message to the user if the email is valid
            self.bot.send_message(chat_id=update.message.chat_id, text=f'Thank you for your application, {user_name}! We will contact you soon via {user_email}.')

            # Send an email notification to yourself or your team with the user name and email (you can use any email service you want)
            import smtplib
            from email.mime.text import MIMEText
            sender_email = 'YOUR_EMAIL'
            sender_password = 'YOUR_PASSWORD'
            receiver_email = 'YOUR_TEAM_EMAIL'
            subject = 'New application received'
            body = f'You have received a new application from {user_name} ({user_email}). Please review it and contact them as soon as possible.'
            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = receiver_email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
        else:

            # Send an error message to the user if the email is invalid
            self.bot.send_message(chat_id=update.message.chat_id, text='Sorry, this is not a valid email. Please try again with a valid email.')

            # Create an instance of the bot class with your bot token
        my_bot = GadaaJobsBot(token='YOUR_BOT_TOKEN')

            # Start the bot
        my_bot.start_bot()

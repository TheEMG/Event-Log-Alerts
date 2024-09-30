# Log Event Monitor 
A Python program that monitors Windows Event Logs and sends email alerts for critical or error events. Using the Google Gmail API, the script notifies the user whenever specific event types are detected in the Windows system

# What I learned 
- Gained experience with accessing and filtering Windows Event Logs using the pywin32 library to capture and handle critical system events.
- Learned how to automate Python scripts with the Windows Task scheduler, which ensures the progtram runs regulary or when specific conditions are met
- I successfully integrated the Google Gmail API with OAuth 2.0 authentication to programmatically send emails

# Usage 


#### 1. **Running the Script Manually**
To manually run the script and check for critical or error events in the Windows Event Log:
1. **Install the required Python libraries**:
   ```bash
   pip install pywin32 google-api-python-client google-auth-httplib2 google-auth-oauthlib
2. **Set up the GMAIL API**:
    Refer to Google Gmail APi guide for more details 
3. **Configure the script**:
    Once you finish setting up the GMAIL API , download the credentials, name it credentials.json and then put the file in the project directory.
    Make sure you change the to_email = 'your_email@gmail.com' to your actual email 
4. **Run the Script**:
    To manually run the script just type python logEvent.py. The current setup is meant to track the Critical errors and Errors but this can modified to whatever you desire.
    
    


# Automating with Windows Task Scheduler 
### 2. Automating with Windows Task Scheduler
To automate this process and ensure that the script runs at specified intervals (e.g., every hour or every day), follow these steps:

#### Open Windows Task Scheduler:

- Search for "Task Scheduler" in the Windows Start Menu and open it.

#### Create a New Task:

1. In the Task Scheduler, click **Action** > **Create Task**.
2. In the **General** tab, name the task (e.g., "Log Event Monitor") and select **Run whether user is logged on or not**.

#### Set the Trigger:

1. Go to the **Triggers** tab and click **New**.
2. Set how often you'd like the script to run (e.g., daily, weekly, or on a specific schedule).

#### Configure the Action:

1. In the **Actions** tab, click **New**.
2. Set **Action** to "Start a Program".
3. In the **Program/script** field, enter the path to your Python executable (e.g., `C:\Python39\python.exe`).
4. In the **Add arguments** field, enter the path to your script (e.g., `C:\path\to\logEvent.py`).
5. In the **Start in (optional)** field, enter the directory where your script and other necessary files (like `credentials.json` and `token.json`) are located (e.g., `C:\path\to\script\folder`).

#### Set Conditions (Optional):

- In the **Conditions** tab, you can configure additional settings, such as only running when the computer is idle or on AC power.

#### Save and Run the Task:

1. Click **OK** to save the task. You may be prompted to enter your system password.
2. The task is now set to run automatically based on the schedule you configured.

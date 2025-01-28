# Canvas Announcement Poster

This Python script is designed to simplify the process of creating and posting announcements to multiple Canvas courses. It allows you to format your announcements with linked videos, general announcements as bulleted lists, and important notes, all presented in a clean and consistent HTML format. Before posting, you can preview the announcement in your web browser.

## Demo

Watch a demonstration of the script in action:

[View Demo Video](http://ua896588.serversignin.com/lucasblanco.com/ed/videos/apidemo.mp4)

## Features

*   **Formatted HTML Announcements:** Create well-structured announcements with a consistent visual style using HTML templates.
*   **Video Linking:** Include links to videos from platforms like Kanopy.
*   **Bulleted Announcements:** Add a list of general announcements with proper formatting.
*   **Important Notes:** Include a section for important notes related to the announcement.
*   **Multiple Course Support:** Post the same announcement to multiple specified Canvas courses.
*   **Local Preview:** Save the formatted announcement as an HTML file and preview it in your web browser before posting.
*   **User-Friendly Interface:** Command-line prompts guide users through the setup and announcement creation process.
*   **Error Handling:** Basic error handling for API requests and file saving.

## How it Works

1.  **Setup:**
    *   The script prompts you for your Canvas base URL (e.g., `https://college.instructure.com`).
    *   It also asks for your Canvas API token. 
    *   The API token is used to authenticate your requests to the Canvas API.
    *   The script builds your URL and authentication headers for all API requests.

2.  **Course Selection:**
    *   You are then prompted to enter the IDs of the Canvas courses where you want to post your announcement.
    *   You can enter one ID per line and press Enter without typing to complete the selection.

3.  **Announcement Creation:**
    *   You'll provide a title for your announcement.
    *   You can then enter a video URL to link to. If you don't have a video, you can skip this step.
    *   Next, you'll enter the list of general announcements you want to include in your post, one per line, hitting enter twice to end the list.
    *   Finally, you'll enter important notes or type `none` to skip this section.

4.  **HTML Generation:**
    *   The script then uses templates to build an HTML formatted announcement based on your entries.

5.  **Local Save & Preview:**
    *   The HTML version of your announcement is saved locally in your Downloads folder with a timestamped name.
    *   The HTML is opened in your default web browser.

6.  **Confirmation and Posting:**
    *   You are prompted to confirm whether you would like to post this announcement to your Canvas courses.
    *   If you agree, the script sends the announcement to each of the courses you selected.
    *   You'll receive a confirmation message for each successful post and error messages where posting fails.

## Usage

1.  **Clone or Download:** Clone or download this repository to your local machine.
2.  **Install Dependencies:** Make sure you have the `requests` module installed. If not, install it using pip:
    ```bash
    pip install requests
    ```
3.  **Run the script:** Execute the script in your terminal:
    ```bash
    python your_script_name.py
    ```
    Replace `your_script_name.py` with the actual name of the python file.
4.  **Follow the prompts:** Follow the on-screen prompts to provide your Canvas details, course IDs, and announcement content.
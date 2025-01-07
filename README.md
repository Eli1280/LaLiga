LaLiga Dashboard 2023/24
This project is an interactive dashboard that provides insights into LaLiga's 2023/24 season performance. It includes team and player statistics such as goals per match, team ratings, tackles, and player goals per 90 minutes.

Features
Overview: Comparison of Home, Away, and Overall performance.
Team Statistics: Explore various team metrics like goals, ratings, and tackles.
Player Statistics: Compare player performance across different metrics.
Requirements
streamlit
pandas
plotly
Setup
Clone the repository.
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Run the app:
bash
Copy code
streamlit run app.py
Deployment
This app is deployed on Streamlit Cloud.
Deploying the App on Streamlit Community Cloud
Once you have your app ready and tested locally, the next step is to deploy it on Streamlit Community Cloud. This will allow you and others to access the app online without running it on local servers. Below are the steps to deploy and try the app using Streamlit Community Cloud:

1. Push Your Code to GitHub
Before deploying your app on Streamlit Community Cloud, you need to push your project to a GitHub repository.

Go to GitHub and create a new repository for your project.
Once the repository is created, follow these commands to push your code to GitHub.

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/football-statistics-dashboard.git
git push -u origin main
Ensure that your code is pushed to a GitHub repository.

2. Sign In to Streamlit Community Cloud
Visit Streamlit Community Cloud.
If you don’t already have an account, sign up using your GitHub account.
Once logged in, you'll be redirected to the Streamlit dashboard.

4. Deploy the App on Streamlit Community Cloud
In the Streamlit dashboard, click on the New app button to create a new deployment.
You'll be prompted to link your GitHub repository. Select the repository where your app code is hosted.
Next, select the branch (typically main or master) and the file path to your app.py file (or the file where your Streamlit app code is located).
Click on Deploy.
Streamlit will automatically build and deploy the app. This might take a few moments, depending on the complexity of your app and the resources it requires.

5. Share and Access the Deployed App
Once the deployment is successful, you will be provided with a link to your deployed app. You can share this link with others to allow them to try the app.

For example, your app link might look like:

https://yourusername-username-foo-12345.streamlit.app
Click on the link, and your app will open in a web browser. Users will be able to interact with your dashboard just like they did locally.

5. How Users Can Try the App
To try the app, users simply need to click on the deployment link you've shared. When they visit the link, they will be directed to the app's main interface.

From there, users can interact with the app’s widgets:

Select Players to Compare: Use the dropdown menus to choose different players and compare their statistics side by side.
Team Stats: View aggregated team statistics through interactive charts.
Visualizations: Use sliders and other controls to dynamically adjust the displayed statistics and compare various football metrics.

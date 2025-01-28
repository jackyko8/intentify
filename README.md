# Intentify

**Intentify** is a web-based analytical dashboard that categorizes and visualizes caller intents. It leverages natural language processing (NLP) techniques to group similar intents and provides a clean, interactive interface to display their distribution. Intentify is designed to make sense of messy, unstructured intent data and turn it into actionable insights.

---

## Features

- **Semantic Grouping**: Groups similar intents using advanced NLP techniques like Sentence-BERT embeddings.
- **Representative Labeling**: Labels each group with a typical sentence representing its category.
- **Interactive Dashboard**: Displays categorized intents with visualizations such as bar charts and pie charts.
- **Scalable Design**: Handles a large number of intents efficiently.
- **AWS Hosting**: Deployed on AWS to ensure accessibility and scalability.

---

## Demo

A live demo is available at: [https://intentify.onmy.ai](https://intentify.onmy.ai)

1. The application will
   - Group similar intents into categories.
   - Label each category with a representative intent.
   - Display the distribution of intents on the dashboard.
2. Menu items
   - Metadata: Number of intents, calls, and unique sentences in the input data.
   - Intent Counts: A histogram of intents, most frequently identified first
   - Intents: Sentences grouped under each intent identified
   - Data Files:
     - Download Intent Data JSON file - the result of analysis
     - Download Contact Data Text file - the input contact data with one sentence per line
     - Upload your own contact data file for analysis
3. Controls:
   - Move the Granularity Setting slide bar to get more or less intents


---

## Installation

### Prerequisites

- Python 3.9 or later
- AWS CLI
- [jq](https://jqlang.github.io/jq/download/) (for build only)

### Running locally

Note: All steps must be executed from the repository root directory.

1. Clone the repository:

   ```bash
   git clone https://github.com/jackyko38/intentify.git
   cd intentify
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   If the installation is stuck at sentence_transformers, restart and install the following manually (using a TMPDIR with sufficient space):

   ```bash
   export TMPDIR=[your_tmp_directory]
   pip install torch --index-url https://download.pytorch.org/whl/cpu --no-cache-dir -v
   pip install sentence-transformers --no-cache-dir -v
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run src/app/app.py
   ```

The application will be available at http://localhost:8501.

---

## Deployment

### Prerequisites

- Set up
  - Update `./bin/setup.sh` with your stack name and deployment s3 bucket
  - `source ./bin/setup.sh`
- S3 Bucket for deploying source code
  - Create an S3 Bucket
  - Enter the S3 Bucket Name in `./src/cfn/intentify.yml` >> Parameters >> `S3BucketName`
- For custom domain
  - Route 53 Hosted Zone (the main domain)
  - ACM Certificate

### Deploying on AWS

1. Build

   ```bash
   ./bin/build.sh -c
   ```

2. Monitor

   ```bash
   ./bin/stack_status.sh COMPLETE
   ```

   Wait until CREATE_COMPLETE, then a further 5 to 10 minutes to allow `pip install` to complete on the EC2 instance.

3. Test the URLs shown in the CloudFormation output: CloudFront URL, Custom URL, StreamlitAppURL (backend direct for testing)

   - You may upload your own contact data file (at near the bottom of the app page)


### Debugging

- Logs
  - EC2 User Data Script Log: `/var/log/ec2-userdata.log`
  - Streamlit App Log: `/var/log/streamlit-app.log`
- Journal
  - `journalctl -u streamlit-app`
- Load test data
  ```bash
  cd /opt/streamlit-app
  aws s3 cp s3://[data_bucket]/[data_tgz_file]
  tar xzvf [data_tgz_file]
  # ./data created
  ```
- Restart streamlit-app
  ```bash
  sudo systemctl restart streamlit-app
  ```

  This will automatically check the deployment S3 bucket and install any updates if found.
- Force update

  - If failed to start streamlit or did not detect new updates on S3
    ```bash
    rm -f /home/ec2-user/streamlit-app/app.zip*
    sudo systemctl restart streamlit-app
    tail -f /var/log/streamlit-app.log
    ```

To verify if the streamlit is running, look for the following at near the end of `/var/log/streamlit-app.log`:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.1.1.135:8501
  External URL: http://54.66.220.139:8501
```

### Technical Notes

- User Data
  - EC2 UserData only run at the first boot, not every boot
  - For testing, this will "trick" cloud-init into running the userdata script in the next boot only
    ```bash
    sudo rm -rf /var/lib/cloud/instance /var/lib/cloud/instances/*
    sudo rm -rf /var/log/cloud-init.log /var/log/cloud-init-output.log
    sudo cloud-init clean
    sudo reboot
    ```
    - Upon the next login, say "yes" to host key verification.
- To recreate the EC2
  - Open the CloudFormation template
  - Comment out the EC2 block and references to StreamlitEC2Instance
  - Update the stack: `./bin/build.sh -u`
  - Uncomment the EC2 block and references to StreamlitEC2Instance

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

3. Commit your changes and push:

   ```bash
   git commit -m "Add new feature"
   git push origin feature-name
   ```

4. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For questions or feedback, please reach out to feedback@onmy.ai .

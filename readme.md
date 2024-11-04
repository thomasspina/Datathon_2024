# Finance Dashboard

This project is an ambitious all inclusive financial analyst tool. It's still in early development and was made in the context of the Polyfinance Datathon 2024.

## Features

- Technical Analysis dashboard
- AI chat to ask financial questions on currently selected company
- Automated generated report on selected company

## Demo

Insert gif or link to demo

## Run Locally

Clone the project

```bash
  git clone https://github.com/thomasspina/Datathon_2024.git
```

Go to the project directory

```bash
  cd Datathon_2024
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run main.py
```

## Environment Variables

To run this project, you will need to add these variables to config/settings.py

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `AGENT_ID` = your bedrock agent id that is connected to your data source
- `AGENT_ALIAS_ID`
- `SEC_BUCKET_NAME` = the bucket in which you want to put the SEC filings
- `KB_ID` = the knowledge base id that is connected to your S3 bucket
- `DS_ID` = your data source id in your knowledge base that is connected to your S3

## Tech Stack

 Streamlit, Amazon Bedrock, Amazon S3
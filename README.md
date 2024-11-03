# polyfinance-datathon

## Pages

Homepage
└── Search Section
├── Company Search Bar
│ ├── Autocomplete
│ └── Search button
│
├── Recent Searches Panel
│ └── Clickable recent companies
│
└── Saved Companies
└── Pinned/Favorite analyses

Dashboard
├── Company Overview Panel
│ ├── Basic info
│ └── Quick metrics
│
├── Analysis Tabs
│ ├── Financial Analysis
│ ├── News & Sentiment
│ ├── Documents
│ └── LLM Analysis
│
└── Custom Query Section
├── Question input
└── Context selection

## Flow

User Selects Symbol
↓
System Gathers Data:
├── Market Data (yfinance)
│ ├── Historical prices
│ ├── Key statistics
│ └── Financial statements
│
├── News Collection
│ ├── Google News RSS
│ ├── Reddit discussions
│ └── SEC filings (EDGAR)
│
├── Document Analysis
│ ├── Annual reports
│ ├── Quarterly reports
│ └── Earnings transcripts
│
└── Sentiment Analysis
├── News sentiment
├── Social media sentiment
└── Market sentiment

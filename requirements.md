# Requirements Document

## Project: Unnat Bhartiya Krishi (AI Farmer Assistant & Decision Support System)


### Overview

The AI Farmer Assistant is an intelligent decision-support system designed to help farmers make informed agricultural decisions using combination of Artificial Intelligence (AI) and Generative AI (GenAI).

The platform enables farmers to:
- Receive **crop recommendations** based on soil and weather conditions
- Ask questions about **ongoing government agricultural schemes**
- Access **agricultural knowledge in their native language**
- Get **market insights and crop guidance**

The system leverages **AWS cloud services, machine learning models, and Retrieval-Augmented Generation (RAG)** to deliver personalized and accessible agricultural support.

The solution is designed specifically for **rural farmers with limited technical literacy and low-bandwidth environments**.


### Core Objectives

1. Provide **AI-driven crop recommendations** using soil and weather data.
2. Enable farmers to **interact with agricultural knowledge using natural language**.
3. Allow farmers to **discover government schemes and benefits easily**.
4. Provide **multilingual support for rural accessibility**.
5. Build a **scalable AI platform using AWS services**.


### Functional Requirements

#### Farmer Interaction Interface

The system must provide an interface through which farmers can interact with the AI assistant.

-  **Features:**
    - Text-based chat interface
    - Voice input support
    - Multilingual interaction

- **Channels:**
    - Web application (Streamlit)
    - Mobile browser access
    - Voice interaction (future)

#### Crop Recommendation Engine

The system must recommend suitable crops based on agricultural inputs.

- **Inputs:**
    - Soil nutrients (N, P, K)
    - Soil pH
    - Temperature
    - Rainfall
    - Humidity

- **Output**
    - Recommended crops suitable for the given conditions based on the best trained machine learning model(s)
    - Confidence score

- **Implementation**
    - Trained machine learning model(s)
    - Compared the models based on accuracy
    - Model(s) serialized using **Pickle**
    - Model served through the backend application


#### AI Knowledge Assistant (RAG System)

The system must allow farmers to ask questions about agriculture and government schemes.

- **Example Queries:**
    - What subsidy schemes are available for farmers?
    - What support does the government give for irrigation?
    - How can I apply for PM-KISAN?


### System Behavior

1. User asks a question.
2. System retrieves relevant information from stored government documents.
3. Large Language Model generates a contextual answer.
4. Response is returned in the farmer's language.


### Data Sources

- Government agricultural schemes
- Farmer welfare policies
- Agricultural best practices
- Farming guidelines


### AWS Cloud Requirements

The system must primarily use **AWS cloud services**.

#### Storage
- **Amazon S3**
  - Store datasets
  - Store government documents
  - Store trained models

#### AI Models
- **AWS Bedrock**
  - Large Language Model for question answering

#### Vector Database (Future)
- **Amazon OpenSearch / Vector Database**
  - Store document embeddings
  - Enable semantic search

#### Language Services (Future)
- **Amazon Transcribe**
  - Speech-to-text

- **Amazon Polly**
  - Text-to-speech


### Supported Languages

- Hindi
- English
- Regional languages (future)


### References

The following documents are used as **knowledge sources for the AI Knowledge Assistant (RAG system)**. These documents contain information related to **government agricultural policies, farmer schemes, and traditional farming knowledge**.

The following documents are used as **knowledge sources for the AI Knowledge Assistant (RAG system)**.  
These documents contain information related to **government agricultural policies, farmer schemes, budget allocations, and traditional farming knowledge**.

| Document Title | Organization / Source | File Name | Document Link | Purpose |
|----------------|----------------------|-----------|------|---------|
| Strengthening Agricultural and Rural Development in India | Agricultural Policy Resource | Strengthening_IndiasAgriculturalBackbone_03022025.pdf | https://wd-cp.vercel.app/schemes.html | Source of government agricultural schemes and rural development policies used for answering farmer queries |
| Demand for Grants Analysis 2026–27: Agriculture | PRS Legislative Research | DfG_Analysis_2026-27-Agriculture.pdf | https://prsindia.org/files/budget/budget_parliament/2026/DfG_Analysis_2026-27-Agriculture.pdf | Budget insights and government agricultural spending analysis |
| PM-KISAN Scheme Operational Guidelines | Ministry of Agriculture & Farmers Welfare, Government of India | Revised Operational Guidelines - PM-Kisan Scheme.pdf | https://www.pmkisan.gov.in/Documents/Revised%20Operational%20Guidelines%20-%20PM-Kisan%20Scheme.pdf | Official implementation guidelines for the PM-KISAN income support scheme |
| PM-KISAN Frequently Asked Questions (FAQs) | Press Information Bureau (PIB), Government of India | PM-KISAN FAQ Document | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2021/nov/doc2021112361.pdf | Frequently asked questions and clarifications about PM-KISAN scheme eligibility and benefits |
| Circular Economy in Agriculture: Waste to Wealth | Press Information Bureau (PIB), Government of India | Circular Economy in Agriculture – Waste to Wealth | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc2026217794101.pdf | Government insights on sustainable agriculture and waste-to-wealth initiatives |
| Traditional Knowledge in Agriculture | Indian Council of Agricultural Research (ICAR), Ministry of Agriculture and Farmers Welfare | IITKA_Book_Traditional-Knowledge-in-Agriculture-English_0_0.pdf | https://icar.org.in/sites/default/files/2022-06/IITKA_Book_Traditional-Knowledge-in-Agriculture-English_0_0.pdf | Traditional agricultural practices and indigenous farming knowledge |
| Inventory of Indigenous Technical Knowledge in Agriculture – Document 1 | ICAR | Inventory-of-Indigenous-Technical-Knowledge-in-Agriculture-Document-1.pdf | https://icar.org.in/sites/default/files/2022-06/Inventory-of-Indigenous-Technical-Knowledge-in-Agriculture-Document-1.pdf | Documentation of indigenous farming techniques |
| Inventory of Indigenous Technical Knowledge in Agriculture – Document 2.1 | ICAR | Inventory-of-Indigenous-Technical-Knowledge-in-Agriculture-Documen-2.1.pdf | https://icar.org.in/sites/default/files/2022-06/Inventory-of-Indigenous-Technical-Knowledge-in-Agriculture-Documen-2.1.pdf | Additional indigenous agricultural knowledge for farmer guidance |
# Doc-intelligence-ai

Doc-intelligence-ai is an AI-powered tool that extracts the data from the invoices and stores information in the CSV file.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement.txt.

```bash
pip install -r requirements.txt
```

## ENV

```
KEY="2*******************B"
AZURE_DOC_INTELLIGENCE_ENDPOINT="https://sample-doc-ai.cognitiveservices.azure.com/"
```

### Run the BE
```
python app.py 
```

### Run streamlit app
```
streamlit run streamlit_src/doc_processor.py
```

### Images
![img.png](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)
![img_3.png](img_3.png)

#### reference:
https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-4.0.0
# Bookworm NLP Pipelines

This document presents the main Natural Language Processing (NLP) pipelines implemented in `bookworm.py`.

# 1. Lexical Diversity Pipeline

Evaluates vocabulary richness and writing style.

```mermaid
flowchart TD
    A[Input: book_id] --> B[Fetch book text]
    B --> C[Clean Gutenberg text]
    C --> D[Tokenization regex]
    D --> E[Count tokens tok]
    D --> F[Compute unique words typ]
    D --> G[Count hapax hap]
    E --> H[Compute metrics]
    F --> H
    G --> H
    H --> I[ttr = typ / tok]
    H --> J[mwl = avg word length]
    H --> K[mwf = tok / typ]
    I --> L[Return dictionary]
    J --> L
    K --> L
```


# 2. Topic Modeling Pipeline

Extracts main themes using LDA.

```mermaid
flowchart TD
    A[Input: book_id] --> B[Fetch book text]
    B --> C[Clean text]
    C --> D[Split into sections]
    D --> E[Vectorization CountVectorizer]
    E --> F[Document-Term Matrix]
    F --> G[LDA Model Training]
    G --> H[Extract topics]
    H --> I[Top 10 words per topic]
    I --> J[Return section: words]
```

# 3. Named Entity Recognition (NER) Pipeline

Identifies characters and locations using spaCy.

```mermaid
flowchart TD
    A[Input: book_id] --> B[Fetch book text]
    B --> C[Clean text]
    C --> D[Split into chunks]
    D --> E[spaCy NER processing]
    E --> F[Extract entities]
    F --> G[Filter PERSON → characters]
    F --> H[Filter GPE/LOC/FAC → locations]
    G --> I[Count frequency]
    H --> J[Count frequency]
    I --> K[Top 20 characters]
    J --> L[Top 20 locations]
    K --> M[Return dictionary]
    L --> M
```

# 4. Book Summarization Pipeline

Generates extractive summaries using sentence scoring.

```mermaid
flowchart TD
    A[Input: book_id] --> B[Fetch book text]
    B --> C[Clean text]
    C --> D[Sentence segmentation]
    C --> E[Tokenization]
    E --> F[Word frequency computation]
    F --> G[Normalize frequencies]
    D --> H[Score sentences]
    G --> H
    H --> I[Select top N sentences]
    I --> J[Reorder sentences]
    J --> K[Generate summary]
    K --> L[Return summary string]
```

# 5. Book Similarity Pipeline

Finds similar books using TF-IDF and cosine similarity.

```mermaid
flowchart TD
    A[Input: book_id] --> B[Load book collection]
    B --> C[Fetch all texts]
    C --> D[TF-IDF Vectorization]
    D --> E[Vector matrix]
    E --> F[Select target book vector]
    F --> G[Compute cosine similarity]
    G --> H[Rank books by similarity]
    H --> I[Select top 5]
    I --> J[Return titles list]
```

# 6. Book Card Pipeline

Aggregates all features into a structured metadata object.

```mermaid
flowchart TD
    A[Input: book_id] --> B[Fetch book text]
    B --> C[Fetch metadata authors, shelves]
    B --> D[Lexical diversity]
    B --> E[Topic modeling]
    B --> F[NER extraction]
    B --> G[Summarization]
    B --> H[Similarity computation]
    C --> I[Assemble card]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J[Return structured dictionary]
```


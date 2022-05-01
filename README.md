### Install packages.
Create virtualenv first and then install poetry.

Install poetry
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
Now install the packages.

```shell
poetry install poetry.lock
```

### The-Entities-Swissknife
TES is a streamlit App devoted to NEL: Named Entities Recognition and Wikification (linking wikipedia/wikidata) to support Semantic Publishing through Schema.org Structured Data Markup (in JSON-LD format).


### Razor api for testing
```text
f0852f0515c92c0686d129f79ff9c5584b87c1b67d503073a4c93ec9
```
object. The Language class is used to process a text and turn it into a Doc object. It’s typically stored as a variable called nlp. The Doc object owns the sequence of tokens and all their annotations. By centralizing strings, word vectors and lexical attributes in the Vocab, we avoid storing multiple copies of this data. This saves memory, and ensures there’s a single source of truth.
Text annotations are also designed to allow a single source of truth: the Doc object owns the data, and Span
are views that point into it. The Doc object is constructed by the Tokenizer
, and then modified in place by the components of the pipeline. The Language object coordinates these components. It takes raw text and sends it through the pipeline, returning an annotated document. It also orchestrates training and serialization.
.
The processing pipeline consists of one or more pipeline components that are called on the Doc in order. The tokenizer runs before the components. Pipeline components can be added using Language.add_pipe
. They can contain a statistical model and trained weights, or only make rule-based modifications to the Doc. spaCy provides a range of built-in components for different language processing tasks and also allows adding custom components .
Matchers help you find and extract information from Doc
objects based on match patterns describing the sequences you’re looking for. A matcher operates on a Doc and gives you access to the matched tokens in context.
Match sequences of tokens based on dependency trees using Semgrex operators .
Class for managing annotated corpora for training and evaluation data.
objects.

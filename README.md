# eduGate

Assignment submission system with AI-generated content detection. Built for a university course project, launched July 2025.

![Student submission page](screenshots/submit.png)

## What it does

Students submit PDF assignments, the system checks them against a Hugging Face AIGC detector model. If the initial score is suspicious, it breaks the document into paragraphs and scores each chunk separately — helps pinpoint which sections might be AI-generated instead of flagging the whole thing.

Admins can create assignments, set deadlines, and see all submissions with their scores.

## Tech

- Flask + PostgreSQL
- Hugging Face model (`yuchuantian/AIGC_text_detector`) via Gradio API
- Flask-Login for auth (separate student/admin roles)
- PyMuPDF for PDF text extraction
- Alembic for database migrations

## Detection approach

1. Extract text from uploaded PDF
2. Run full document through detector
3. If score > threshold → chunk into paragraphs (~300 words each)
4. Score each chunk, classify as red/yellow/green
5. Show student which sections were flagged

The threshold (0.99962) was tuned by testing against a mix of human-written and ChatGPT-generated texts.

## Setup

```bash
pip install -r requirements.txt

# set up environment
cp .env.example .env
# edit .env with your DATABASE_URL, SECRET_KEY, mail settings

# init database
flask db upgrade

# run
python main.py
```

## Project structure

```
eduGate/
├── main.py           # routes, models, detection logic
├── templates/        # jinja2 templates
├── static/           # css
├── uploads/          # submitted files
├── tests/            # api tests, load testing
└── migrations/       # alembic migrations
```

## Testing

There's a test suite under `tests/` — includes accuracy testing against labeled datasets and a concurrent login stress test (30 users).

```bash
python -m pytest tests/ -v
```

## Notes

- Detection accuracy depends heavily on the threshold — there's always a tradeoff between false positives (flagging human text) and false negatives (missing AI text)
- The chunking approach helps but isn't perfect
- Tested with Waitress and Gunicorn for production

## Contact

Questions? eduGate.se@gmail.com

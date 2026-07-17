# JobFlow

A backend job orchestration API built with FastAPI.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## Features

- Create jobs
- Run jobs
- Track job status
- Execution history

## Retry Engine

JobFlow retries failed executions automatically.

Features:
- Configurable retry count (`max_retries`)
- One execution record per attempt
- Persistent execution history
- Per-attempt logging
- Automatic success/failure transitions
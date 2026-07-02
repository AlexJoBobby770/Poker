## Current Project State 

The backend core infrastructure is fully wired up, version-controlled via Alembic, and verified against a local containerized database instance.

### Completed Modules & Architecture

1. **Analytical Logic Engine (`backend/engine/`)**
   * `hand_evaluator.py`: Handles string card parsing and fast $O(1)$ hand ranking using the `treys` bitmask evaluator.
   * `equity.py`: Multi-threaded Monte Carlo simulator running 10,000 randomized range rollouts to calculate win/tie probabilities.
   * `pot_odds.py`: Calculates required break-even equity lines, Minimum Defense Frequency (MDF), and long-term Expected Value (EV).

2. **Database Data Layer (`backend/models/`, `backend/database.py`)**
   * Implemented SQLAlchemy ORM connection factories, session management, and thread-safe DB transaction handling (`get_db`).
   * Created database schemas mapping out three distinct relational tables:
     * `game_sessions`: Tracks blind levels, session names, and running financial net results.
     * `hand_histories`: Logs dealt hole/community cards, active player counts, engine-calculated metrics, and recommended actions.
     * `opponent_profiles`: Stores behavioral telemetry counters (VPIP, PFR, aggression/passivity ratios) for profile tracking.

3. **Containerization & Migrations (`backend/alembic/`, `docker-compose.yml`)**
   * Configured Docker Compose blueprint to automatically build and spin up an isolated, persistent PostgreSQL 16 instance on port `5432`.
   * Wired Alembic with custom absolute windows path detection and dynamic `.env` file reading inside `env.py`.
   * Generated and successfully executed initial database migration schemas (`f97ad54de52b`) to construct active database tables.
   * Built and executed `test_db.py` to verify operational CRUD (Create, Read, Update, Delete) database transactions.

---

## Environment Recovery & Boot Instructions

Follow these steps to spin the development environment back up after a break:

1. **Start the Database Container**
   Ensure Docker Desktop is running in the background, then execute:
   ```powershell
   cd C:\Users\alexj\Desktop\projects\poker-assistant\backend
   docker compose up -d

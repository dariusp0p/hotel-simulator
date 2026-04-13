# Hotel Simulator

Hotel Simulator is a PyQt6 desktop application for managing a hotel layout and its reservations. It combines a clean layered architecture, SQLite persistence, in-memory indexing, a graph-backed floor model, and an undo/redo action system.

The project was built as a portfolio piece to demonstrate:

- practical GUI development with Qt
- service/repository layering and DTO-based communication
- SQLite persistence with application bootstrap on startup
- non-trivial data structures, including graph-based floor connections
- command-style undo/redo for CRUD operations
- automated testing with `pytest`

## What the application does

The app lets you:

- configure hotel floors and their elements
- manage rooms, hallways, staircases, and connections between them
- create, edit, delete, and search reservations
- inspect room availability by date range and guest count
- visualize the hotel structure in the simulator view
- undo and redo many user actions through a central action manager

## Tech stack

| Area | Technology |
| --- | --- |
| UI | PyQt6 |
| Persistence | SQLite |
| Graph / relationships | NetworkX |
| Visualization | Matplotlib embedded in Qt |
| Testing | pytest |
| Packaging | PyInstaller, dmgbuild |

## Architecture overview

The application follows a layered design:

1. `main.py` creates the Qt application, opens the SQLite database, and wires dependencies together.
2. `src/view/*` contains the GUI windows and widgets.
3. `src/controller/controller.py` acts as the bridge between the UI and the domain layer.
4. `src/controller/action.py` and `src/controller/action_manager.py` implement undo/redo through reversible actions.
5. `src/model/service/*` holds business rules and validation.
6. `src/model/repository/*` handles persistence and in-memory lookup caches.
7. `src/model/database/*` contains the SQLite schema and low-level SQL helpers.

### Runtime flow

```text
Qt window -> Controller -> Action / Service -> Repository -> SQLite
```

This separation keeps the UI thin and makes the business logic testable without launching the full GUI.

## Implementation highlights

### 1. Dependency injection at startup

`main.py` builds the whole object graph explicitly:

- `DatabaseManager` opens or creates `hotel_simulator.db`
- repositories are created from the same SQLite connection
- services receive repositories
- the controller receives services
- the main window receives the controller

That makes the app easy to reason about and keeps the startup path transparent.

### 2. Graph-backed hotel layout

`HotelRepository` uses `networkx.Graph` to represent connections between floor elements.

- rooms, hallways, and staircases are nodes in the graph
- edges represent valid movement/connectivity between elements
- the graph is refreshed when elements move or when staircase relationships change

This is a nice example of using a real data structure for a UI problem rather than storing everything in plain lists.

### 3. In-memory indexing for fast lookups

The repositories keep cache dictionaries for common queries:

- floors by ID and name
- rooms by ID and capacity
- reservations by reservation ID, room ID, and guest name

This reduces repeated database reads and supports fast lookups for the UI.

### 4. Command-style undo / redo

User actions are wrapped in action objects and managed by `ActionManager`.

- `do_action()` executes an operation and stores it on the undo stack
- `undo()` reverts the most recent action
- `redo()` reapplies an undone action

This is especially useful in the hotel configurator where layout edits should be reversible.

### 5. Reservation and availability rules

The controller enforces business rules before creating or editing reservations:

- date strings are validated in ISO format (`YYYY-MM-DD`)
- room capacity must fit the guest count
- date ranges must not overlap existing reservations

The app also exposes availability lookups by date range and by room capacity.

## Main feature areas

### Home screen

The main window uses a `QStackedWidget` to switch between app sections:

- Home
- Hotel configurator
- Reservation manager
- Simulator

### Hotel configurator

This area is for editing the hotel structure:

- add / rename / move / remove floors
- add / edit / move / remove floor elements
- manage rooms with number, capacity, and price per night
- visualize element placement and connections

### Reservation manager

This area focuses on reservation CRUD and search:

- create and update reservations
- delete reservations
- search by reservation ID, guest name, and room number
- filter by date range

### Simulator

The simulator view renders a 3D-style hotel structure visualization using Matplotlib embedded in Qt.

## Data model

The app models a hotel with the following core entities:

- `Floor`
- `FloorElement` (for non-room elements such as hallways and staircases)
- `Room`
- `Reservation`

Reservations are linked to rooms, and rooms belong to floors. Floor elements are positioned on a grid and connected through the repository graph.

## Search and performance notes

The current implementation uses a mix of indexed lookups and filtered scans:

- exact lookups by ID are fast due to dictionary caches
- room lookup by capacity is direct from an in-memory index
- partial reservation search scans cached reservations but narrows by room number and guest name

That gives a practical balance between simplicity and responsiveness for a desktop CRUD app.

## Project structure

```text
src/
  controller/      # Controller, actions, DTOs, undo/redo
  model/
    database/      # SQLite schema and SQL helpers
    domain/        # Floor, Room, Reservation, FloorElement models
    repository/    # Persistence + in-memory caches
    service/       # Validation and business logic
  view/            # PyQt6 windows, panels, and widgets
  utilities/       # Exceptions, helpers, generators
tests/             # pytest suite
```

## Getting started

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

The database file is created beside the executable/script as `hotel_simulator.db` if it does not already exist.

## Running tests

```bash
pytest
```

Current tests cover:

- controller behavior and DTO conversion
- repository CRUD and persistence logic
- service validation and parsing
- database bootstrap and low-level operations
- domain validation rules

## Packaging and distribution

### macOS app bundle

This repository already includes PyInstaller support for macOS app packaging.

Relevant files:

- `pyinstaller.py`
- `HotelSimulator.spec`
- `main.spec`
- `app_icon.icns`
- `dmg_settings.py`

Build the `.app` bundle:

```bash
python pyinstaller.py
```

Create a DMG from the generated app bundle:

```bash
dmgbuild -s dmg_settings.py "HotelSimulator" HotelSimulator.dmg
```

Notes:

- `dmgbuild` reads the app path from `dmg_settings.py`
- the generated app bundle is expected at `build/HotelSimulator.app`
- the SQLite database is created next to the app at runtime, so the install location must be writable

### Windows installer

The codebase is structured so it can be frozen on Windows with PyInstaller, then wrapped in an installer such as Inno Setup.

At the moment, this repository does not include a committed Inno Setup script, so Windows packaging should be treated as planned follow-up work rather than a finished distribution pipeline.

## Recruiter takeaways

If you are reviewing this as a portfolio project, the strongest implementation points are:

- layered architecture with explicit dependency wiring
- undo/redo implementation through command-like actions
- SQLite persistence with in-memory indexes for faster lookups
- graph-based hotel layout modeling
- UI built with PyQt6 and embedded Matplotlib visualization
- meaningful automated tests around the business and repository layers

## Future improvements

- add a committed Windows installer configuration for Inno Setup
- expand search indexing for reservation queries
- add richer analytics and occupancy reporting
- harden packaging with CI-driven builds for macOS and Windows

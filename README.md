# Sports Management Dashboard

A secure, modern GUI application for managing sports games with admin authentication, built using Object-Oriented Programming principles.

## 🏗️ Architecture Overview

This application demonstrates three key OOP concepts:

### 1. **Abstraction (Database Layer)**
- **Abstract Base Class**: `IDataManager` defines the interface for database operations
- **Concrete Implementation**: `MySQLManager` implements the actual MySQL logic
- **Benefit**: Database details are hidden from the GUI, making it easy to switch databases

### 2. **Inheritance (GUI Layer)**
- **MainApplication(tk.Tk)**: Main window controller
- **GameForm(tk.Frame)**: Custom form widget for game entry
- **GameList(tk.Frame)**: Custom list widget for displaying games
- **Benefit**: Reusable, encapsulated GUI components

### 3. **Polymorphism (Data Logic)**
- **Base Class**: `Sport` with `validate_score()` method
- **Subclasses**: `Soccer` and `Basketball` override validation logic
- **Benefit**: Different sports handle scores differently while maintaining a uniform interface

### 4. **Security (Authentication System)**
- **Password Hashing**: bcrypt-based secure password storage
- **User Management**: Admin user registration and authentication
- **Session Security**: Login tracking and session management
- **Input Validation**: Comprehensive validation for security

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- **MySQL Server** (via XAMPP recommended)
- matplotlib (for analytics charts)

#### MySQL Setup (XAMPP)
1. Download and install [XAMPP](https://www.apachefriends.org/)
2. Start XAMPP Control Panel
3. Start the **MySQL** module (click "Start")
4. The application uses default XAMPP settings:
   - Host: `localhost`
   - Port: `3306`
   - User: `root`
   - Password: `[empty]`

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database

#### Option A: Automatic Setup (Recommended)
```bash
# Make sure XAMPP MySQL is running, then run:
python main.py
```
The application will automatically create the required database tables.

#### Option B: Manual SQL Import (Alternative)
If you prefer to manually import the database schema:

1. **Start XAMPP MySQL**:
   - Open XAMPP Control Panel
   - Click "Start" for MySQL module
   - Wait for MySQL to turn green

2. **Open phpMyAdmin**:
   - Click "Admin" button next to MySQL in XAMPP
   - Or visit: `http://localhost/phpmyadmin`

3. **Create Database**:
   - Click "New" in the left sidebar
   - Database name: `sports_db`
   - Collation: `utf8mb4_unicode_ci`
   - Click "Create"

4. **Import SQL File**:
   - Select `sports_db` from the left sidebar
   - Click "Import" tab at the top
   - Click "Choose File" and select `sports_db.sql`
   - Click "Go" to import

5. **Verify Import**:
   - Check that `admin_users` and `games` tables were created
   - The database should contain sample data:
     - **Admin User**: username `admin`, email `admin@example.com`
     - **Sample Games**: Pre-loaded sports games for testing

**Note**: The imported admin user has a hashed password. You'll need to reset it using the application or create a new admin account.

### 3. Create Admin Account

#### Option A: Use Setup Script (Recommended for fresh installs)
```bash
python setup_admin.py
```
This interactive script will:
- Prompt for username, email, and password
- Validate password strength requirements
- Create the admin user in the database

#### Option B: Use Imported Admin Account
If you imported the SQL file, you can use the pre-created admin account:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Note**: Password needs to be reset using the application

#### Password Requirements (for new accounts):
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### 4. Run the Application
```bash
python main.py
```

**Login Process**:
- Use the credentials created in steps 2 or 3
- The login window appears automatically
- Click "Register" to create additional admin accounts

**Authentication Features**:
- **Secure Password Hashing**: Uses bcrypt for password security
- **Session Management**: Tracks login times and active sessions
- **Multiple Admin Support**: Create multiple admin accounts
- **Input Validation**: Comprehensive validation for all fields

## 🎯 Features

### 🎨 **Modern UI Design**
- **Dark Theme**: Modern dark color scheme with professional styling
- **Card-Based Layout**: Clean, organized interface with visual hierarchy
- **Responsive Design**: Adapts to different window sizes
- **Status Bar**: Real-time feedback and keyboard shortcuts guide

### ⚡ **Productivity Features**
- **Quick Templates**: Pre-filled game forms for common scenarios
- **Recent Teams**: Quick selection from previously used teams
- **Auto-Complete**: Smart suggestions for team names and leagues
- **Keyboard Shortcuts**: Full keyboard navigation support
- **Data Export**: Export filtered results to TXT files
- **Real-time Search**: Instant filtering with debounced search

### 📊 **Advanced Analytics Dashboard**
- **Real-time Statistics**: Live calculation of key metrics
- **Interactive Charts**: Pie charts and bar graphs for data visualization
- **Performance Metrics**:
  - Total games tracked
  - Active teams count
  - Win rate analysis
  - Average goals per game
  - Recent activity (30 days)
  - Most popular league
- **Monthly Trends**: Visual representation of game frequency over time

### 🔍 **Smart Game Management**
- **Advanced Filtering**: Filter by sport, league, and date range
- **Multiple Sorting Options**: Sort by date, sport, league
- **Context Menus**: Right-click options for quick actions
- **Winner Calculation**: Automatic winner determination from scores
- **Data Integrity**: Comprehensive validation and error handling

### ⌨️ **Keyboard Shortcuts**
- `F1`: Help & Shortcuts
- `F5`: Refresh all data
- `Ctrl+N`: Add Game tab
- `Ctrl+L`: Games List tab
- `Ctrl+A`: Analytics tab
- `Ctrl+R`: Refresh
- `Ctrl+S`: Save game (in form)
- `Ctrl+Q`: Quit application
- `Delete`: Remove selected game
- `Enter`: Edit selected game

### 🏆 **Sport-Specific Intelligence**
- **Soccer**: Validates low scores (0-15 range) like "2-1"
- **Basketball**: Validates high scores (50-200 range) like "105-98"
- **Extensible**: Easy to add new sports with custom validation rules

### 🔐 **Secure Admin Authentication**
- **Password Hashing**: bcrypt-based secure password storage
- **User Registration**: Create multiple admin accounts
- **Session Management**: Login tracking and security
- **Input Validation**: Strong password and username requirements

### ✅ **Advanced Validation System**
- **Real-time Validation**: Instant feedback as you type
- **Comprehensive Rules**: Team names, scores, dates, duplicates
- **Business Logic**: League-sport compatibility, game uniqueness
- **Data Integrity**: Database-level validation before saving
- **Batch Validation**: Validate multiple games before import
- **Error Classification**: Errors, warnings, and info messages

#### Validation Features:
- **Team Names**: Length (2-50 chars), character restrictions, uniqueness
- **Scores**: Format validation, sport-specific ranges, numerical validation
- **Dates**: Format (YYYY-MM-DD), range (not too old/future), business rules
- **Leagues**: Character validation, sport compatibility warnings
- **Duplicates**: Prevent identical games, cross-reference existing data

## 🎯 Usage

### 🏗️ **Getting Started**
1. **Launch Application**:
   ```bash
   python main.py
   ```

2. **First Run**: Database and tables are created automatically

### ⚽ **Adding Games**
- **Manual Entry**: Fill out the form in the "Add Game" tab
- **Quick Templates**: Use pre-built templates for common game types
- **Recent Teams**: Quickly select from previously used teams
- **Auto-Complete**: Smart suggestions as you type team/league names
- **Keyboard**: `Ctrl+S` to save, `Ctrl+R` to clear form

### 📋 **Managing Games**
- **Real-time Search**: Type in search bar for instant filtering
- **Advanced Filters**: Filter by sport and league
- **Multiple Sorting**: Click headers or use dropdown to sort
- **Context Menu**: Right-click for quick actions
- **Data Export**: Export filtered results to TXT files
- **Keyboard Navigation**: Use arrow keys, Enter, Delete


### 📊 **Analytics Dashboard**
- **Live Statistics**: Automatic calculation of key metrics
- **Interactive Charts**: Pie charts and bar graphs
- **Performance Metrics**: Games count, win rates, team activity
- **Monthly Trends**: Visual representation of game frequency
- **Real-time Updates**: Automatically refreshes with new data

### 📄 **Data Export**
- **TXT Export**: Export filtered games to readable text files
- **Formatted Output**: Well-structured game information
- **Summary Information**: Export metadata and statistics

### 📊 **Analytics Dashboard**
- **Live Statistics**: Automatically updates with new data
- **Visual Charts**: Pie charts for sports distribution, bar charts for trends
- **Performance Metrics**: Track team counts, win rates, activity levels
- **Monthly Trends**: See game frequency patterns over time

### ⌨️ **Keyboard Shortcuts**
- `F1`: Show help and all shortcuts
- `F5` or `Ctrl+R`: Refresh all data
- `Ctrl+N/L/A`: Switch between tabs
- `Ctrl+Q`: Quit application

## 🛠️ Code Structure

```
sports-management-dashboard/
├── main.py                     # Application entry point
├── setup_mysql.py             # MySQL database setup
├── requirements.txt           # Dependencies (MySQL + matplotlib)
├── README.md                  # Documentation
├── config/                    # Configuration management
│   └── settings.py           # MySQL/XAMPP settings
├── database/                  # Database layer (Abstraction)
│   ├── interfaces.py         # IDataManager abstract base class
│   ├── mysql_manager.py      # MySQLManager concrete implementation
│   └── sqlite_manager.py     # SQLiteManager (alternative)
├── models/                    # Business logic (Polymorphism)
│   └── sports.py             # Sport base class + subclasses
├── ui/                        # User interface (Inheritance)
│   ├── main_application.py   # MainApplication(tk.Tk) + Analytics
│   ├── game_form.py          # GameForm(tk.Frame) with validation
│   └── game_list.py          # GameList(tk.Frame) with filtering
└── utils/                     # Utilities
    └── validation.py         # Comprehensive validation system
```

## 🔧 Customization

- **Add New Sports**: Create new subclasses of `Sport`
- **Change Database**: Implement new class inheriting from `IDataManager`
- **Modify UI**: Extend the Frame subclasses with new widgets

## 📝 OOP Concepts in Action

- **Abstraction**: `self.data_manager.add_game(game_obj)` - GUI doesn't know about MySQL
- **Inheritance**: `class GameForm(tk.Frame)` - Inherits Tkinter's Frame functionality
- **Polymorphism**: `sport_obj.validate_score(score)` - Same method, different behavior per sport
# crook

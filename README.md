# RoomieMatch - Tinder-Style Roommate Finder

A modern, mobile-friendly roommate finder app built with Python Flask that transforms the stressful process of finding compatible roommates into a fun, Tinder-style experience.

## Features

- 🔐 **User Authentication**: Secure login and registration system
- 👤 **Detailed Profiles**: Comprehensive profiles with interests, lifestyle preferences, and budget information
- 💫 **Tinder-Style Swiping**: Intuitive swipe interface for discovering potential roommates
- 🧠 **Smart Matching**: Intelligent algorithm that matches users based on compatibility scores
- 💕 **Mutual Matching**: Only shows matches when both users like each other
- 📱 **Responsive Design**: Beautiful, modern UI that works on both mobile and desktop
- 🎨 **Modern Animations**: Smooth animations and interactive elements

## How It Works

1. **Sign Up**: Create an account with username, email, and password
2. **Complete Profile**: Fill out detailed information including:
   - Basic info (name, age, budget, location)
   - Interests (music, sports, gaming, cooking, etc.)
   - Lifestyle preferences (sleep schedule, social level, cleanliness, pet preferences)
3. **Start Swiping**: Swipe right to like potential roommates, left to pass
4. **View Matches**: See mutual matches and start conversations

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd Roomate_Finder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd Find-A-Roomate
   python main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Sample Accounts

The app comes with pre-loaded sample accounts for testing:

| Username | Password | Profile |
|----------|----------|---------|
| alex_smith | password123 | Music lover, gamer, night owl |
| maya_johnson | password123 | Fitness enthusiast, early bird |
| sam_wilson | password123 | Artist, photographer, flexible |
| jessica_brown | password123 | Tech professional, gamer |
| mike_davis | password123 | Sports fanatic, outdoor enthusiast |
| sarah_miller | password123 | Art student, quiet lifestyle |

## Matching Algorithm

The app uses a sophisticated compatibility scoring system that considers:

- **Budget Compatibility** (30 points max): Closer budgets get higher scores
- **Location Match** (25 points): Same location preference
- **Age Compatibility** (20 points): Similar age ranges
- **Shared Interests** (25 points): Common hobbies and activities
- **Lifestyle Alignment** (20 points): Compatible living preferences

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern animations
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## File Structure

```
Roomate_Finder/
├── Find-A-Roomate/
│   ├── main.py                 # Main Flask application
│   └── templates/
│       ├── login.html          # Login page
│       ├── signup.html         # Registration page
│       ├── profile_setup.html  # Profile creation page
│       ├── swipe.html          # Tinder-style swipe interface
│       ├── matches.html        # View mutual matches
│       └── no_more_matches.html # No more profiles message
├── static/
│   └── style.css              # Main stylesheet
└── requirements.txt           # Python dependencies
```

## Features in Detail

### User Authentication
- Secure password hashing using Werkzeug
- Session management
- Login/logout functionality

### Profile System
- Comprehensive user profiles with multiple data points
- Interest selection with visual tags
- Lifestyle preference questionnaires
- Bio section for personal descriptions

### Swipe Interface
- Touch and mouse support for swiping
- Visual feedback during swipe gestures
- Smooth animations and transitions
- Card-based design similar to Tinder

### Matching System
- Mutual matching requirement
- Compatibility scoring algorithm
- Smart ordering of potential matches
- Match history tracking

## Customization

### Adding New Interests
Edit the `profile_setup.html` file to add new interest options in the interests grid.

### Modifying Matching Algorithm
Update the `calculate_compatibility_score()` function in `main.py` to adjust how compatibility is calculated.

### Styling Changes
Modify `static/style.css` to customize the appearance and animations.

## Security Notes

- Change the `app.secret_key` in production
- Use environment variables for sensitive configuration
- Consider using a more robust database for production
- Implement proper input validation and sanitization

## Future Enhancements

- Real-time chat functionality
- Photo uploads for profiles
- Advanced filtering options
- Push notifications
- Social media integration
- Location-based matching with maps

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the MIT License.

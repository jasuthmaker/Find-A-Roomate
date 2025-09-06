# Firebase Setup Guide for RoomieMatch

## Prerequisites
1. Google account
2. Firebase project created

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: `roomie-match` (or your preferred name)
4. Enable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Realtime Database

1. In your Firebase project, go to "Realtime Database"
2. Click "Create Database"
3. Choose "Start in test mode" (for development)
4. Select a location close to your users
5. Click "Done"

## Step 3: Get Database URL

1. In Realtime Database, go to "Rules" tab
2. Copy your database URL (looks like: `https://your-project-id-default-rtdb.firebaseio.com/`)
3. Save this URL for later

## Step 4: Generate Service Account Key

1. Go to Project Settings (gear icon)
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file
5. Rename it to `firebase-service-account.json`
6. Place it in your project root directory

## Step 5: Set Up Environment Variables

Create a `.env` file in your project root:

```env
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com/
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
```

## Step 6: Update Database Rules (Security)

In Firebase Console → Realtime Database → Rules, replace with:

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "auth != null",
        ".write": "auth != null"
      }
    },
    "profiles": {
      "$uid": {
        ".read": "auth != null",
        ".write": "auth != null"
      }
    },
    "swipes": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "matches": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

## Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 8: Test Firebase Connection

Run the test script:

```bash
python test_firebase.py
```

## Step 9: Run the Application

```bash
python main.py
```

## Database Structure

Your Firebase Realtime Database will have this structure:

```
roomie-match/
├── users/
│   ├── {user_id}/
│   │   ├── username: "alex_smith"
│   │   ├── email: "alex@example.com"
│   │   ├── password_hash: "..."
│   │   └── created_at: "2024-01-01T00:00:00"
├── profiles/
│   ├── {user_id}/
│   │   ├── name: "Alex Smith"
│   │   ├── age: 22
│   │   ├── budget: 600
│   │   ├── location: "Downtown"
│   │   ├── bio: "Love music, gaming, and cooking!"
│   │   ├── interests: "[\"Music\", \"Gaming\"]"
│   │   ├── lifestyle_preferences: "[\"Night Owl\"]"
│   │   └── created_at: "2024-01-01T00:00:00"
├── swipes/
│   ├── {swipe_id}/
│   │   ├── swiper_id: "user1"
│   │   ├── swiped_id: "user2"
│   │   ├── action: "like"
│   │   └── created_at: "2024-01-01T00:00:00"
└── matches/
    ├── {match_id}/
    │   ├── user1_id: "user1"
    │   ├── user2_id: "user2"
    │   └── created_at: "2024-01-01T00:00:00"
```

## Troubleshooting

### Common Issues:

1. **"Firebase service account file not found"**
   - Make sure `firebase-service-account.json` is in your project root
   - Check the file path in `.env`

2. **"Database URL not found"**
   - Verify your database URL in `.env`
   - Make sure the URL ends with `/`

3. **"Permission denied"**
   - Check your database rules
   - Make sure you're authenticated

4. **"Connection timeout"**
   - Check your internet connection
   - Verify your Firebase project is active

## Security Notes

- Never commit `firebase-service-account.json` to version control
- Use environment variables for sensitive data
- Set up proper authentication rules
- Consider using Firebase Authentication for user management

## Next Steps

After setup, you can:
1. Enable Firebase Authentication
2. Set up push notifications
3. Add real-time chat features
4. Implement cloud functions
5. Add analytics and monitoring

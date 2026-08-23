# InterviewPilot Frontend

This is the Next.js frontend for InterviewPilot.

## Tech Stack

- Next.js
- React
- TypeScript
- TailwindCSS
- Fetch API

## Features

- Landing page
- Signup page
- Login page
- Protected dashboard
- Resume dashboard
- ATS dashboard
- Job Match page
- Resume analysis cards
- ATS analysis cards
- Auth context for JWT persistence

## Current Pages

- `/`
- `/signup`
- `/login`
- `/dashboard`
- `/resume`
- `/job-match`

## Components

- Authentication forms
- Dashboard layout and sidebar
- Resume upload card
- Resume info card
- ATS analysis card
- Job Match page

## Environment

The frontend expects the backend API to be available at:

```ts
http://127.0.0.1:8000
```

## Development

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

## Notes

- The frontend uses the backend resume and ATS APIs directly.
- The frontend also uses the Job Match API directly.
- Resume and ATS sections are rendered from structured API responses.
- The UI now includes a cleaner report-style resume analysis layout and better link rendering.

## Screenshots

Add screenshots here when available.

- Landing page
- Login page
- Signup page
- Dashboard
- Resume dashboard
- ATS dashboard

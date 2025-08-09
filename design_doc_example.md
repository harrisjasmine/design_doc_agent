# Design Document: Team Activity Dashboard

---

## Project Name
**Team Activity Dashboard**

---

## Summary
A web-based dashboard for team leads to monitor project progress, individual contributions, and sprint metrics across engineering pods.

---

## Goals
- Enable leads to view task breakdowns and story points by engineer  
- Visualize sprint velocity and burndown trends  
- Integrate with JIRA and GitHub for real-time data  

---

## Architecture

- **Frontend**: React + TypeScript with TailwindCSS  
- **Backend**: Node.js with Express  
- **Data Layer**: PostgreSQL and Redis  
- **Integrations**:  
  - JIRA REST API  
  - GitHub GraphQL API  
- **Authentication**: OAuth2 SSO via the company identity provider  

---

## Requirements

### User Roles
- Team Lead  
- Manager  

### Core Features
- Sprint overview chart with filters  
- Engineer contribution metrics  
- Real-time sync with JIRA boards  
- Auth-protected routes for team-specific data  

### Non-Functional Requirements
- Dashboard must load in under 2 seconds  
- Data sync occurs every 10 minutes  
- Accessible on mobile and desktop devices  


<div class="markdown prose w-full break-words dark:prose-invert dark"><hr><h1>Overview of Vaccine Appointment Management API</h1><p>Welcome to the Vaccine Appointment Management API. This API is designed to facilitate the management of vaccine appointments within healthcare systems. Built using Django, PostgreSQL, Celery, and Redis, our API offers a robust and efficient solution for scheduling, updating, and tracking vaccine appointments.</p><h2>Key Features</h2><ul><li><p><strong>Appointment Scheduling:</strong> Allow users to schedule vaccine appointments based on availability and vaccine type.</p></li><li><p><strong>Appointment Management:</strong> Enable users to view, update, and cancel their appointments as needed.</p></li><li><p><strong>User Authentication:</strong> Implement secure authentication mechanisms to ensure user privacy and data integrity.</p></li><li><p><strong>Notifications:</strong> Send automated reminders and notifications to users regarding upcoming appointments.</p></li></ul><h2>API Endpoints</h2><ul><li><p><code>/vaccinate</code>: Endpoint for managing vaccine appointments, including scheduling, updating, and canceling appointments.</p></li><li><p><code>/user</code>: Endpoint for user authentication and management, including registration, login, and profile updates.</p></li><li><p><code>/admin</code>: [Only super users]: Endpoint for managing the whole database.</p></li></ul><h2>Authentication</h2><p>Our API utilizes token-based authentication to ensure secure access to endpoints. Users are required to authenticate using their credentials (username/password) to obtain an access token, which must be included in subsequent requests for authorization.</p><h2>Database Schema</h2><p>Our PostgreSQL database is structured to store essential information related to appointments, locations, and users. The schema is designed to optimize data retrieval and ensure data integrity.</p><h2>Task Queue (Celery) and Cache (Redis)</h2>
  
  ```mermaid
flowchart LR

subgraph rwp["Your Railway Project"]
    subgraph public["Publicly exposed services"]
        django["App container\n(Django server)"]
    end
    subgraph private["Private services"]
        celery["App container\n(Celery worker)"]
        psql["PostgreSQL"]
        redis["Redis"]
    end
end

users["Users"] --> django
django --> celery
django --> psql

celery --> psql
celery --> redis
django --> redis

```

  <p>Celery and Redis are integrated into our API to manage asynchronous tasks, such as sending notifications. Redis is used as a cache to improve API performance by storing frequently accessed data.</p><h2>Getting Started</h2><p>To begin using the Vaccine Appointment Management API, please refer to the <a target="_new" rel="noreferrer" href="https://documenter.getpostman.com/view/29472124/2sA35MxJLp">documentation</a> for detailed instructions on authentication, endpoint usage, and API integration. If you encounter any issues or have questions, feel free to reach out to our <a target="_new" rel="noreferrer" href="https://github.com/neuropython/Vaccinate_managment_backend/issueshttps://github.com/neuropython/Vaccinate_managment_backend/issues">GitHub issues</a> here.</p><hr></div>
<p>App is currently deployed under this addres: https://vaccinatemanagmentbackend-production.up.railway.app/<p>

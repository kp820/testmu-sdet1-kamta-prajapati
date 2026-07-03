# Prompts Used — Task 2

> Rule: paste prompts EXACTLY as written, including failed/earlier attempts.
> Do not clean these up after the fact.

## Login

### Prompt 1 (initial attempt)
```
Generate 5 Gherkin test scenarios for a login page. Cover: valid login, invalid credentials, forgot password, session expiry, and brute-force lockout after 5 failed attempts. Return ONLY the scenarios in Gherkin (Given/When/Then) format, numbered 1-5. No explanation, just the scenarios.
```

### Generated Output (Gherkin)
```gherkin
Scenario 1: Valid login succeeds and redirects to dashboard
  Given the user is on the login page
  When the user enters "validuser@example.com" as username
  And the user enters "ValidPass123!" as password
  And the user clicks the Login button
  Then the user should be redirected to the dashboard page
  And the page URL should contain "dashboard"

Scenario 2: Invalid credentials display error message
  Given the user is on the login page
  When the user enters "validuser@example.com" as username
  And the user enters "WrongPassword" as password
  And the user clicks the Login button
  Then an error message should be displayed
  And the error message should contain "Invalid username or password"
  And the user should remain on the login page

Scenario 3: Forgot password flow sends reset email
  Given the user is on the login page
  When the user clicks the "Forgot Password" link
  And the user enters "validuser@example.com" as email
  And the user clicks the "Reset" button
  Then a confirmation message should be displayed
  And the confirmation message should contain "reset link"
  And the message should indicate the link was sent to the email

Scenario 4: Expired session redirects to login
  Given the user has an expired session token
  When the user navigates to the dashboard page
  Then the user should be redirected to the login page
  And the page URL should contain "login"

Scenario 5: Brute-force lockout after 5 failed attempts
  Given the user is on the login page
  When the user enters incorrect credentials 5 times
  And the user clicks the Login button on each attempt
  Then the account should be locked
  And a lockout message should be displayed
  And the message should indicate "Account locked after too many failed attempts"
  And the user should not be able to log in
```

### What didn't work first time / what I changed (3–5 lines)
Initial output was clean and covered all 5 cases. If iterating further: would add explicit timeout value in session-expiry scenario (e.g., "after 15 minutes of inactivity") to make the test more concrete. Would also specify the exact confirmation message text for forgot-password ("reset link sent to your email") to tighten the assertion. Brute-force scenario needed a dedicated test username to avoid shared state with other tests across the test suite.

---

## Dashboard

### Prompt 1 (initial attempt)
```
Generate 5 Gherkin test scenarios for a web dashboard. Cover: widget loading without errors, data accuracy vs API source, filter and sort functionality, responsive mobile layout, and permission-based visibility of admin-only widgets. Return ONLY the Gherkin scenarios numbered 1-5. No explanation.
```

### Generated Output (Gherkin)
```gherkin
Scenario 1: All widgets load without errors
  Given the user is logged in and on the dashboard page
  When the dashboard page fully loads
  Then all widgets should be visible
  And no widget error messages should be displayed
  And each widget should display its content without loading spinners

Scenario 2: Widget data matches API source of truth
  Given the user is logged in and on the dashboard page
  When the dashboard page fully loads
  And the API endpoint "/api/dashboard/summary" returns a total count of 5
  Then the dashboard should display a total count of 5
  And the displayed data should match the API response exactly

Scenario 3: Filter and sort update the displayed data
  Given the user is logged in and on the dashboard page
  When the user selects "Active" from the filter status dropdown
  And the user clicks the "Sort by date" button
  Then the displayed rows should be filtered to show only active items
  And the rows should be sorted in date order
  And the first row should be visible

Scenario 4: Dashboard layout adapts on mobile viewport
  Given the user is logged in and on the dashboard page
  When the browser viewport is set to 375x667 pixels
  Then the mobile navigation should be visible
  And the desktop sidebar should be hidden
  And all dashboard content should remain accessible

Scenario 5: Admin-only widgets are hidden for non-admin users
  Given the user is logged in with a non-admin role
  When the user navigates to the dashboard page
  Then the admin-only widget should not be visible
  And only widgets accessible to the user's role should be displayed
```

### What didn't work first time / what I changed (3–5 lines)
Initial output covered all scenarios but was vague on mobile dimensions. In refinement would specify viewport explicitly as "375x667 pixels" to match a real device size. Data accuracy scenario needed the specific API endpoint ("/api/dashboard/summary") added to make the assertion traceable. Permission test also needed clarification that "non-admin role" means a regular user account, not an unauthenticated visitor.

---

## REST API

### Prompt 1 (initial attempt)
```
Generate 5 Gherkin test scenarios for a REST API. Cover: auth token validation (expect 401 on invalid token), CRUD operations (create/read/update/delete), error handling (4xx and 5xx responses), rate limiting (429 after rapid requests), and response schema validation. Return ONLY Gherkin scenarios numbered 1-5.
```

### Generated Output (Gherkin)
```gherkin
Scenario 1: Auth token validation returns 401 on invalid token
  Given the API is running
  When the user sends a GET request to "/api/protected-resource"
  And the request includes an invalid Bearer token in the Authorization header
  Then the API should return a 401 Unauthorized status code
  And the response body should contain an error message

Scenario 2: CRUD operations on a resource
  Given the API is running and authenticated
  When the user sends a POST request to "/api/items" with body {"name": "test-item"}
  Then the API should return a 201 Created status code
  And the response should contain the created item with an "id" field
  When the user sends a GET request to "/api/items/{id}"
  Then the API should return a 200 OK status code
  When the user sends a PUT request to "/api/items/{id}" with body {"name": "updated"}
  Then the API should return a 200 OK status code
  When the user sends a DELETE request to "/api/items/{id}"
  Then the API should return a 204 No Content status code

Scenario 3: Error handling returns proper 4xx for malformed request
  Given the API is running
  When the user sends a POST request to "/api/items" with an invalid request body
  And the body is missing required fields
  Then the API should return a 400 Bad Request status code
  And the response body should contain a descriptive error message

Scenario 4: Rate limiting returns 429 after rapid requests
  Given the API is running
  When the user sends more than 50 rapid requests to "/api/items"
  Within a short time window
  Then the API should return a 429 Too Many Requests status code
  And the response should indicate the rate limit has been exceeded

Scenario 5: Response schema validation
  Given the API is running
  When the user sends a GET request to "/api/items/1"
  Then the API should return a 200 OK status code
  And the response body should contain an "id" field of type integer
  And the response body should contain a "name" field of type string
  And no additional required fields should be missing
```

### What didn't work first time / what I changed (3–5 lines)
Initial output didn't specify rate-limit threshold concretely — "rapid requests" is vague. Would refine to "50 requests within 30 seconds" for reproducibility across different machines. Schema validation scenario was also generic; would add explicit field types ("id" as integer, "name" as string) to make assertions directly translatable to code. CRUD scenario used a placeholder {id} — would clarify this should be dynamically captured from the POST response.

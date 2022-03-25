
# Tattoo Module
After installed the module, things to do:
1. add a user to the client's group
2. add a user to the manager's group
3. add a user to the artist's group
4. add hours to a tattoo artist

Access Right
============
1. User Client:
   - Session: can read, create, write and delete. 
   - Appointment: can read, create and write and delete.
   - Design: can only read.
   - Artist hours: can only read.
   - Design Material: can only read
   
2. User Artist:
   - Session: can read, create, write and delete. 
   - Appointment: can read, create and write and delete.
   - Design: can read, create, write and delete.
   - Artist hours: can read, create, write and delete.
   - Design Material: can only read
 
3. User Manager:
   - Session: can read, create, write and delete. 
   - Appointment: can read, create and write and delete.
   - Design: can read, create, write and delete.
   - Artist hours: can read, create, write and delete.
   - Design Material: can read, create, write and delete. 
   
Rules Access
============
1. ``User client can only see their own session and appointment``
2. ``User artist can see all session and only their own appointments``
3. ``User Manager can do anything``

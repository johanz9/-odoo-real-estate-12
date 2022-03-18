# odoo-real-estate-12
real estate module for odoo 12

After installed the module things to do:
1. add the manager group to admin user
2. add the agent group to agent user

Description
============
Default filter in the property tree views is "Available". It show only the properties that have state "New" or "Offer receveid".

It was added a new notebook's page in the form view res.users.form



Rules Access
============
1. ``User agent can only see their own properties, cannot have access to Setting nav``
2. ``User Manager can see all propresties``

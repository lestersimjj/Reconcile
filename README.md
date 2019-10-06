# Web Application for Trade Reconciliation

### Getting Started
This web application was built using Flask which is a micro web framework written in Python. Bootstrap was used in creating HTML templates while jQuery was utilised to handle viewing big datatables and send AJAX request. Purpose of this application is to automate the reconciliation of trade data and present it for reporting purposes. Go ahead and install the necessary libraries and run the app.py.

A demo of this can be found here: http://lestersim.herokuapp.com

### Tabs
1. **Home**: Landing page
2. **Issuers**: Instead of the portfolio-asset level, the table shows the positions aggregated on an IssuerId level. This is derived from the portfolio-asset level by a simple grouby to show the total positions for that particular issuer
3. **Asset**s: Assets that the investment companies hold are stored in the portfolio-asset level
4. **Transactions**: Obtain trading data for that specific date, shown on a portfolio-asset level

### How It Works
1. Select a date on either tabs of Issuers, Assets or Transactions
2. If the reconciled files for the date selected are found in the database, a table will be shown to reflect the file.
3. Otherwise, a warning would be prompted and the user can click on the link 'Click here to reconcile' to trigger the reconciliation process for that particular date selected.
4. In the reconciliation process, trade data for the selected date is being extracted from the trading database, added to the previous day's positions (SOD Position) and subsequently dervive the EOD positions for the selected date. Once the reconciled files are written to the database, the information will be available to all 3 tabs since they are all using the same source and only filtering out different results.

*Note: Instead of the codes to extract information from the trading database, it is substituted with a random number generator here because of the sensitivity and confidentiality of the information. Hence, it is not covered here as this is only meant for demonstration purposes.*



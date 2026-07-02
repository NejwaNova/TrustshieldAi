# Test Plan for TrustShield AI Node.js transition

- [x] Navigate to http://127.0.0.1:8000 and ensure the page loads. (Failed: open_browser_url failed with error: local chrome mode is only supported on Linux)
- [ ] Locate the text area with ID 'scan-input' and type 'URGENT: Please wire transfer $42,500 immediately to CEO bank account'.
- [ ] Click the button with ID 'btn-run-scan'.
- [ ] Wait 2 seconds.
- [ ] Verify that the results modal (id 'scan-modal') appears showing High Risk or Critical classification and threat details.
- [ ] Take a screenshot of the results modal.
- [ ] Close the modal.
- [ ] Verify logs/network response if possible and construct final report.

## Summary of Findings
The testing could not be completed because the `open_browser_url` tool failed with the error: "local chrome mode is only supported on Linux" on the current environment (Windows).


# Manual Verification Testing

## Test Case 1: Legitimate Domain
* **Command:** `python 2_analyze_domain.py -d microsoft.com`
* **Expected Output:** Prediction should be `LEGIT`. The playbook should recommend verification and closing the ticket.
* **Actual Output:**
    ```
    Predicting and generating SHAP explanation...
generic prediction progress: |                                                   |   generic prediction progress: |███████████████████████████████████████████████████ (done)| 100%
contributions progress: |                                                        |   contributions progress: |████████████████████████████████████████████████████████ (done)| 100%
  - Prediction: LEGIT
  - Confidence: 100.00%
Summarizing SHAP findings...
Domain Analysis Summary:
- Domain: microsoft.com
- Prediction: This domain is classified as 'LEGIT'.
- Confidence Score: 100.00%
Feature Contributions (Explanation):
  - The 'length' value of 13.00 increases the likelihood of it being a DGA domain.
  - The 'entropy' value of 3.03 increases the likelihood of it being a DGA domain.

Generating incident response playbook with Google's Gemini model...

==================== INCIDENT RESPONSE PLAYBOOK ====================
# Incident Response Playbook: microsoft.com

**Incident Type:** Suspicious Domain

**Domain:** microsoft.com

**Prediction:** Legitimate

**Confidence Score:** 100.00%

**Analyst Level:** Junior


**Playbook Steps:**

1. **Verification (High Confidence Legitimate):**  Given the high confidence score (100%) and the domain being microsoft.com, proceed directly to verification.  Do NOT initiate containment actions.

2. **Review Feature Contributions:** Examine the feature contributions flagged in the analysis summary.  While the length and entropy values are unusual, the extremely high confidence score from other features outweighs these. Document your understanding of the apparent discrepancy in your findings (high confidence score vs. unusual length and entropy).

3. **Reputation Check:** Utilize multiple reputable sources (e.g., VirusTotal, Google Safe Browsing, etc.) to verify the domain's reputation. Document the results of these checks in the ticket.

4. **Network Traffic Analysis (Optional):**  If there are concerns about specific network traffic associated with this domain, perform a limited review to ensure there are no anomalous patterns.  Focus on traffic volume and destination ports.  This step is only necessary if there is a specific reason to believe microsoft.com traffic is a problem, not just because of the analysis summary's flag.

5. **Documentation:**  Thoroughly document all steps taken, including the results of the reputation checks and any network traffic analysis.  Include screenshots where applicable.

6. **Ticket Closure:**  Based on the high confidence score and verification steps, close the ticket with a detailed explanation of your findings and the reasoning for classifying the domain as legitimate. Include references to the used reputation services and any other sources.

7. **Follow-up (Optional):** If any unusual aspects persist after verification, consider escalating the incident to a senior analyst for further review.  The analysis summary's discrepancies should be discussed.


**Note:**  This playbook prioritizes efficient resolution for legitimate domains.  If the confidence score were lower or the domain less well-known, more extensive investigation would be necessary.  This playbook focuses on verifying the legitimacy of the already identified domain, not on a broad investigation of all communications with it.

================================================================
    ```
* **Result:** **LEGIT**

## Test Case 2: DGA Domain
* **Command:** `python 2_analyze_domain.py -d 9w8eyr9q8wyef9q8wye.org`
* **Expected Output:** Prediction should be `DGA`. The playbook should recommend immediate containment actions like blocking the domain.
* **Actual Output:**
    ```
   Predicting and generating SHAP explanation...
generic prediction progress: |                                                   |   generic prediction progress: |███████████████████████████████████████████████████ (done)| 100%
contributions progress: |                                                        |   contributions progress: |████████████████████████████████████████████████████████ (done)| 100%
  - Prediction: DGA
  - Confidence: 76.98%
Summarizing SHAP findings...
Domain Analysis Summary:
- Domain: 9w8eyr9q8wyef9q8wye.org
- Prediction: This domain is classified as 'DGA'.
- Confidence Score: 76.98%
Feature Contributions (Explanation):
  - The 'length' value of 23.00 decreases the likelihood of it being a DGA domain.
  - The 'entropy' value of 3.32 increases the likelihood of it being a DGA domain.

Generating incident response playbook with Google's Gemini model...

==================== INCIDENT RESPONSE PLAYBOOK ====================
# Incident Response Playbook: Suspicious Domain 9w8eyr9q8wyef9q8wye.org

**Incident Type:** Potential DGA Domain

**Domain:** 9w8eyr9q8wyef9q8wye.org

**Prediction:** DGA (76.98% confidence)

**Priority:** HIGH - Immediate Containment Required


**Step 1: Isolation (Immediate Action)**

1. **Block the domain:**  Immediately block the domain `9w8eyr9q8wyef9q8wye.org` at your organization's firewall and DNS level.  Document the time of blocking.
2. **Isolate affected systems:** Identify any systems that have contacted this domain using your network monitoring tools (e.g., SIEM, NetFlow). Isolate these systems from the network.  This may involve disconnecting from the network or placing them in a quarantine VLAN. Document affected systems and actions taken.


**Step 2: Containment and Investigation**

1. **Memory forensics:** If possible, perform memory analysis on isolated systems to identify any malicious processes or indicators of compromise (IOCs) related to this domain.
2. **Log analysis:** Thoroughly review logs from affected systems and network devices for any suspicious activity related to this domain, including DNS queries, network connections, and file system access. Focus on timestamps around the time of first detection.
3. **Malware analysis (if applicable):** If malware samples are found, submit them to a sandbox environment for analysis.


**Step 3: Remediation**

1. **Reimage affected systems:** Reimage any compromised systems to eliminate persistent threats.  Ensure backups are clean before restoring.
2. **Update security software:** Update antivirus and endpoint detection and response (EDR) software on all affected systems.
3. **Review security controls:** Evaluate your existing security controls to identify any gaps that allowed the threat to gain a foothold.


**Step 4: Reporting and Documentation**

1. **Create a detailed incident report:** Document all actions taken, findings, and remediation steps. Include timestamps for each action.
2. **Escalate to management:** Report the incident and its impact to your management team.
3. **Post-incident review:** Conduct a post-incident review to identify areas for improvement in your security posture.


**Step 5: Monitoring and Follow-up**

1. **Continuously monitor:** Monitor network traffic and system logs for any further suspicious activity related to this domain or other similar domains.
2. **Threat intelligence:** Check for any known information on this domain in threat intelligence feeds.


**Note:** The high entropy value suggests a likely DGA, despite the slightly longer length.  Prioritize containment to minimize potential damage.  Further investigation may be required post-containment to fully understand the attack's scope and impact.  This playbook is a guideline; adapt it based on your organization's specific environment and resources.

================================================================
    ```
* **Result:** **DGA**
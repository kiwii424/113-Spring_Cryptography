# Password Managers: Attacks and Defenses (2014) – Review and Current Perspectives



## 1. Name of the paper

**Password Managers: Attacks and Defenses** – David Silver, Suman Jana, Dan Boneh, Eric Y. Chen, and Collin Jackson. *Proceedings of the 23rd USENIX Security Symposium, 2014.*



## 2. Summary

This paper examines the security of popular password managers (PMs), with a focus on their autofill policies and susceptibility to *network-based attacks*. The authors survey ten widely-used password managers (including browser built-ins like Chrome/Firefox, third-party extensions like LastPass/1Password, and a mobile PM) and discover inconsistent and overly permissive autofill behaviors ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=to%20support%20autofill,such%20as%20a%20rogue%20router)). In several cases, the PMs would automatically fill in credentials in contexts where they should not, enabling a *remote attacker on a rogue network (e.g. a malicious Wi-Fi hotspot)* to steal multiple saved passwords *without any user interaction* ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=In%20this%20paper%20we%20study,such%20as%20a%20rogue%20router)). For example, if a user connects to a fake “evil Wi-Fi” router at a coffee shop, the attacker can inject invisible login forms (or iframes) for various sites and trick many PMs into silently autofilling credentials, which are then extracted by the attacker’s script ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=disastrous%3A%20an%20attacker%20can%20extract,on%20the%20device%20being%20attacked)). This attack could rapidly “sweep” a user’s vault, compromising many accounts at once. The authors verified that 6 out of 10 managers tested were vulnerable to such an attack in their default settings ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=disastrous%3A%20an%20attacker%20can%20extract,such%20as%20a%20rogue%20router)).



To mitigate these threats, the paper proposes stricter autofill policies and introduces a concept called **“secure filling.”** First, they recommend never autofilling passwords in certain high-risk conditions – for instance, if a page is delivered over HTTP or has an invalid HTTPS certificate – and to *require explicit user interaction through a trusted UI element before filling* credentials ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20also%20demonstrated%20that%20password,a%20login)). This means the PM should not silently populate login forms; instead, the user must click or otherwise confirm the autofill (via a browser-controlled prompt or toolbar UI that malicious scripts cannot fake) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=following%20two%20steps%20,hope%20that%20this%20work%20will)). Second, the authors design **secure filling**, an autofill mechanism that keeps passwords safe even if the page is partially compromised by malicious code ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=The%20goal%20of%20secure%20filling,proposed%20defense%20works%20as%20follows)). The key idea is analogous to HTTP-only cookies: the password manager can fill a password such that it will *work when submitted* to the legitimate site, but *cannot be read by JavaScript on the page* ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=The%20goal%20of%20secure%20filling,proposed%20defense%20works%20as%20follows)). In practice, they achieve this by filling a dummy password value and only swapping in the real password at the moment of form submission (after verifying the form’s action URL matches the intended site) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=is%20somewhat%20akin%20to%20HttpOnly,proposed%20defense%20works%20as%20follows)) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=1,or%20password%20fields%20are%20modified)). This prevents hostile scripts from directly snatching the secret out of the DOM. They implemented prototypes of these defenses (modifying Chrome’s password filling code) and demonstrated that users would remain protected even if an attacker injects malicious scripts, as long as the final form submission is to a secure (HTTPS) endpoint ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=The%20goal%20of%20secure%20filling,proposed%20defense%20works%20as%20follows)).



Notably, the paper’s findings had immediate real-world impact. The authors disclosed the vulnerabilities to vendors, leading to quick improvements in popular managers ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20disclosed%20our%20results%20to,passwords%20from%20HTTPS%20pages%20on)). For example, LastPass changed its policy to **stop auto-filling into iframes by default**, and 1Password modified its extension to **no longer fill credentials from an HTTPS site into an HTTP page** (preventing a common mixed-content trick) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20disclosed%20our%20results%20to,passwords%20from%20HTTPS%20pages%20on)). The paper concludes that when properly designed (e.g. with user consent for autofill and secure handling of credentials), password managers can *strengthen* security (by preventing phishing and encouraging unique passwords) rather than weaken it ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=interaction%20through%20some%20form%20of,devel%02opers%20to%20adopt%20our%20enhancements)). Overall, **“Password Managers: Attacks and Defenses”** highlighted a critical weakness in 2014-era password managers’ autofill logic and put forward practical solutions that have influenced subsequent designs.



## 3. Strength(s) of the paper

- **Comprehensive Survey:** The study examines a broad range of password managers across different platforms and integration levels (browser-built-in, browser extension, and mobile apps). This extensive survey of ten PMs allowed the authors to catalog how each decides when to autofill, uncovering that “all are too loose in their autofill policies” in one way or another ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=to%20support%20autofill,as%20soon%20as%20the%20user)). By covering multiple products and scenarios, the paper gives a well-rounded view rather than a single case, increasing the credibility and impact of its findings.



- **Clear Motivation & Example:** The paper’s introduction effectively motivates the problem with a concrete “evil coffee shop” scenario. It walks through how a rogue Wi-Fi hotspot could inject hidden login forms for popular sites and immediately harvest passwords  ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=disastrous%3A%20an%20attacker%20can%20extract,on%20the%20device%20being%20attacked)). This illustrative example (accompanied by a figure of a “Welcome to Evil WiFi” page) makes the attack understandable and compelling. The authors thereby communicate the severity (“disastrous consequences”) in practical terms ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=observe%20significant%20differences%20in%20autofill,1%20Introduction)), which is a strength in getting both developers and non-expert readers to appreciate the risk.



- **Novel Attack Techniques:** While some underlying issues (like autofill on HTTP pages or XSS stealing passwords) were known, the paper introduces **automated “sweep” attacks** that combine these weaknesses into a powerful *fully automated exploit*. The attacker doesn’t need user clicks or phishing; simply the act of visiting a malicious network can trigger background theft of many credentials. This automation of what could be a mass credential exfiltration is a novel contribution, extending prior XSS or phishing attacks into a different threat model (active network attacker) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=saved,that%20active%20network%20attackers%20can)) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=inject%20iFrames%20to%20login%20forms,content%2C%20broken%20SSL%2C%20embedded%20device)). The paper also explores multiple vectors (mixed content, iframes, broken TLS, etc.), not just a single bug, which shows thoroughness ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=forms%2C%20and%20steal%20those%20passwords,such%20as%20the%20redi%02rect%20attack)).



- **Effective Defensive Proposals:** The defenses proposed are practical and address the identified issues directly. *Requiring a user gesture* to fill passwords and *disabling autofill on suspicious contexts* (like invalid SSL or cross-origin frames) are relatively straightforward for vendors to implement and don’t require new web standards ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20also%20demonstrated%20that%20password,a%20login)). The **secure filling** mechanism is more involved, but the authors implemented it as a prototype in Chrome to prove feasibility ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=is%20somewhat%20akin%20to%20HttpOnly,proposed%20defense%20works%20as%20follows)) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=1,or%20password%20fields%20are%20modified)). They show that even a two-step approach (never autofill without user consent, and use secure filling on submission) can make password managers more secure than even manual password entry in certain cases ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=interaction%20through%20some%20form%20of,a%20login)). This practical orientation – not just pointing out problems but also offering and testing solutions – is a major strength.



- **Real-World Impact:** The paper had tangible impact on the industry. The fact that LastPass and 1Password promptly changed their autofill behavior in response to the authors’ disclosure  ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20disclosed%20our%20results%20to,passwords%20from%20HTTPS%20pages%20on)) attests to the significance of the findings. By including these outcomes, the paper demonstrates its relevance and improves trust in its recommendations. It also likely spurred further research (the authors encourage developers to adopt the enhancements ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=page%20fetched%20over%20HTTP%20but,devel%02opers%20to%20adopt%20our%20enhancements))), positioning the work as an influential reference for both academia and industry.



## 4. Weakness(es) of the paper

- **Limited Usability/Cost Analysis of Defenses:** While the paper proposes fixes (like forcing user interaction and secure filling), it does not deeply evaluate the *usability trade-offs or implementation costs* of these changes. For example, always requiring a user click or an extra dialog could inconvenience users, but the paper doesn’t measure how much this might reduce the user-friendliness of password managers. Similarly, the secure filling mechanism might impact sites that use client-side scripts for login (as the authors briefly note compatibility issues ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=5,the%20password%20field%20using%20JavaScript))), but the paper doesn’t quantify how many sites might break or the engineering effort needed to adopt this defense. A more detailed discussion on maintaining usability while improving security would strengthen the recommendations.



- **Narrow Threat Model:** The focus is on *network-based attackers injecting content*, which was appropriate for the autofill issues studied, but other threat models were out of scope. The paper explicitly ignores scenarios like malware on the user’s device or malicious browser extensions that could also target password managers. This clear scoping is understandable, but it means the paper doesn’t address other prevalent risks (e.g., keyloggers, local storage security, or cloud server breaches of PM services). As a result, the mitigations are somewhat narrow – they greatly improve security against *web attackers* but not necessarily against all forms of attack on password managers.



- **Lack of Attack Priority or Quantitative Risk:** The authors present multiple attack variants (XSS-based, mixed content, iframe abuses, etc.) that all achieve credential theft. However, the paper doesn’t rank which vulnerabilities are most likely or most severe in practice. For instance, an attack relying on a user visiting an HTTP page vs. one requiring a site with XSS – which is more common or easier for attackers to exploit? The paper treats them mostly in aggregate. This could make it harder for password manager developers to decide which specific autofill scenario to tackle first. A bit more data on prevalence (they do mention ~17% of top sites have HTTP->HTTPS login forms ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=over%20HTTP%2C%20but%20submit%20the,a%20land%02ing%20page%20that%20asks)), which is helpful) or a risk comparison of the different vectors would improve the guidance.



- **No Long-Term Ecosystem Perspective:** The solutions focus on changes within password manager software, but the paper doesn’t explore broader or long-term fixes in the web ecosystem. For example, it doesn’t discuss how web standards or browser APIs might evolve to support secure password filling (beyond the immediate hacks like dummy passwords). In later years, one might envision standards for marking fields as “autofill-safe” or improvements in Content Security Policy to aid password managers. These forward-looking ideas are outside the scope of this paper. As a result, the paper solves the symptoms (in the PM implementations) but doesn’t offer insights on how website developers or browser standards could also help mitigate such issues in the future.



- **Dated Evaluation (no longer current):** A minor point (with hindsight) is that the study reflects the state of password managers circa 2014. Security features in PMs evolve quickly, so some weaknesses identified were later fixed by vendors or made less relevant by web-wide changes (e.g. the web’s move to default HTTPS). The paper, of course, cannot be faulted for this, but it means readers today must look to follow-up research to see how the landscape changed. (In fact, the authors themselves suggested developers adopt these improvements, and many did, as noted in the conclusion ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20disclosed%20our%20results%20to,passwords%20from%20HTTPS%20pages%20on)).)



## 5. Personal reflections (lessons, extensions, open questions, broader impact)

**Lessons Learned:** The core lesson from Silver et al.’s work is that *autofill convenience can introduce significant security risk* if not designed carefully. An automatic password filler needs strict context checks and user involvement to avoid becoming an attack vector. This lesson has clearly been absorbed by modern password managers. Today, most managers **do not blindly autofill credentials without user action** – a direct contrast to the 2014 findings. For instance, the Bitwarden password manager now disables automatic autofill on page load by default and only fills when the user selects a credential (e.g. via a field icon or hotkey) ([[SOLVED: IT DOES HAVE AUTOFILL] Essential requirement - true ...](https://community.bitwarden.com/t/solved-it-does-have-autofill-essential-requirement-true-form-autofill/18124#:~:text=,fill%20On%20Page%20Load%E2%80%9D)) ([Bitwarden adds a new autofill option right inside form fields | Bitwarden](https://bitwarden.com/blog/bitwarden-adds-auto-fill-option-inside-form-fields/#:~:text=,be%20populated%20without%20user%20knowledge)). This “user-in-the-loop” approach was exactly what the paper prescribed, and it protects against stealthy form hijacking attacks. Even browser-built-in managers have added restrictions: Chrome and Firefox will typically *refuse to autofill passwords on pages with invalid TLS certificates or on insecure (HTTP) forms*, because a network attacker could be impersonating the site ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20also%20demonstrated%20that%20password,a%20login)) ([Google Chrome does not offer to save password for https with ...](https://issues.chromium.org/40080828#:~:text=,the%20presence%20of%20certificate%20errors)). These changes echo the paper’s recommendation to never autofill under certain unsafe conditions. Another lesson is the value of *trusted UI indicators* for autofill. Modern browsers now often show a small icon in the password field or require a user click on a dropdown to initiate filling, ensuring the action is intentional. Overall, the industry trend since 2014 has been towards **safer autofill strategies** – balancing security with usability by incorporating quick user interactions (like a click or tap) that dramatically reduce silent abuse of the feature ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=%E2%80%93Disable%20the%20autofill%20function%20on,your%20browser)).



**Developments Since 2014:** In the years following the paper, several new attack vectors and defenses emerged. A notable incident in 2017 highlighted that web tracking scripts were exploiting browser autofill features to steal information. In that case, third-party scripts injected *invisible form fields* to trick Chrome or Firefox into auto-populating saved data (like email addresses), which the script then read – all without user knowledge ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=Security%20researchers%20have%20uncovered%20how,across%20different%20browsers%20and%20devices)) ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=Third,Image)). This was essentially the scenario the paper warned about, manifested as a privacy leak used by advertisers. The paper’s advice had already been heeded by third-party managers like LastPass and 1Password, which did *not* autofill hidden fields and required user action, so they were immune to that particular ploy ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=%E2%80%93Disable%20the%20autofill%20function%20on,your%20browser)). Browser vendors quickly tightened their form autofill to address this, reinforcing that *autofill should never happen on invisible or off-screen elements*. This underscores a broader mitigation strategy since 2014: **visibility and focus checks**. Modern autofill implementations often ensure that a field must be visible and likely the one the user is interacting with (has focus) before filling, adding another layer of defense against background theft ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=%E2%80%93Disable%20the%20autofill%20function%20on,your%20browser)).



There have also been vulnerabilities discovered in password manager extensions themselves (beyond just the autofill logic). For example, in 2017 Tavis Ormandy and other researchers found severe bugs in the LastPass browser extension that could allow malicious websites to execute code or steal all passwords ([Potent LastPass exploit underscores the dark side of password ...](https://arstechnica.com/information-technology/2017/03/potent-lastpass-exploit-underscores-the-dark-side-of-password-managers/#:~:text=Potent%20LastPass%20exploit%20underscores%20the,Even%20when%20the%20binary)). These were not *autofill* issues per se, but they reinforced the importance of securing the whole password manager ecosystem (extension APIs, message passing, memory security, etc.). It’s an open question how to best harden PMs against such complex attacks. The 2014 paper primarily dealt with web content injection; since then, researchers have looked at other aspects like secure vault storage, memory encryption, and resisting clickjacking. For instance, follow-up research by Stock and Johns (2014) and Li et al. (2014) also examined XSS and CSRF flaws in web-based password managers ([](https://www.usenix.org/system/files/sec20summer_oesch_prepub.pdf#:~:text=Autofill.%20Silver%20et%20al.%20,approving%20the%20release%20of%20their)). A 2020 study by Oesch et al. revisited the autofill and storage issues and found that while things have improved (“password managers have improved in the past five years”), there still remain “significant security concerns” in some managers ([](https://www.usenix.org/system/files/sec20summer_oesch_prepub.pdf#:~:text=security%20of%20password%20storage%20,conclude%20the%20paper%20with%20several)). That study noted that most managers had indeed adopted user-interaction requirements, but it identified other weaknesses (like some managers not encrypting in-memory data) that still needed work ([](https://www.usenix.org/system/files/sec20summer_oesch_prepub.pdf#:~:text=offline%20attacks%2C%20but%20password%20managers,it%20was%20not%20in%20use)) ([](https://www.usenix.org/system/files/sec20summer_oesch_prepub.pdf#:~:text=A%20recent%20study%20by%20Independent,More)). The field is clearly moving in the right direction – the blatant autofill-without-checks vulnerabilities are less common now – but new challenges continue to arise as password managers increase in complexity and features.



**Broader Impact:** *Password Managers: Attacks and Defenses* has had a lasting influence on both commercial products and academic research. Its responsible disclosure led to quick patches in major products, directly improving security for millions of users. In the academic realm, it sparked a line of research into making password autofill safer. Later works expanded on the secure filling idea, effectively aiming to build a *trusted execution path for passwords*. For example, recent research (2021–2024) explored integrating password managers more tightly with browsers to create an isolated “password entry channel” ([Passwords Are Meant to Be Secret: A Practical Secure Password Entry Channel for Web Browsers](https://arxiv.org/html/2402.06159v1#:~:text=We%20empirically%20evaluated%20the%20security,behavior%2C%20preventing%20any%20functionality%20regression)) ([Passwords Are Meant to Be Secret: A Practical Secure Password Entry Channel for Web Browsers](https://arxiv.org/html/2402.06159v1#:~:text=Proof,changes%20all%20across%20the%20codebase)). These prototypes, which modify browser code and password manager extensions, can prevent even advanced attackers (like malicious browser extensions or scripts with full DOM access) from extracting autofilled passwords. Such efforts are essentially the secure-filling concept taken to its logical extreme – ensuring that a password manager can deliver the secret to the destination website **without any other party on the client side being able to intercept it**. Early results are promising: one study built a Firefox+Bitwarden modification and found it could block password theft by malicious scripts and still work on 97% of websites tested ([Passwords Are Meant to Be Secret: A Practical Secure Password Entry Channel for Web Browsers](https://arxiv.org/html/2402.06159v1#:~:text=We%20empirically%20evaluated%20the%20security,behavior%2C%20preventing%20any%20functionality%20regression)). This indicates that the mitigations proposed in 2014 have evolved into even stronger protections now being tested in real browsers. An open question remains how to best deploy such solutions universally – it may require changes to web standards or browsers, which is ongoing work.



**Suggestions for Extension:** Building on the paper’s work, one suggestion is to improve **context awareness** for autofill. Password managers could incorporate more signals to decide when to fill: not just checking domain and protocol, but also whether the user has recently interacted with the page, whether the form looks legitimate (e.g. proper labeling), etc. Some modern managers do this by, say, not autofilling on pages that contain multiple password fields or known phishing indicators. Another extension of secure filling is to integrate with the browser’s network stack – for instance, a password manager could *hook the form submission process* so that it supplies credentials at the network level (after the DOM form is submitted) rather than into the page DOM at all. This would make it impossible for any client-side script to ever see the password, addressing even sophisticated script-based attacks. The paper’s dummy-fill-and-swap approach is a step in this direction, but it required the form to be submitted in the usual way. Newer approaches could use browser APIs to achieve a completely scriptless handoff. Additionally, the advent of WebAuthn and device-based authentication raises the question of how password managers will adapt — if passwords slowly get replaced or augmented by other credentials, the lessons from this paper about secure UI and user interaction will likely carry over to those systems as well (e.g., ensuring a hardware token prompt cannot be spoofed by a webpage). 



In summary, the 2014 paper taught the security community that **convenience features like autofill must be designed with a paranoid mindset**. The improvements adopted in Chrome, Firefox, LastPass, 1Password, Dashlane, Bitwarden, etc. over the past decade show a clear lineage back to the attacks and defenses discussed by Silver et al. New attack vectors (like extension exploits or advanced phishing techniques) keep emerging, but the fundamental strategy remains: minimize implicit trust in web content. The broader impact is that password managers are now widely recognized not just as usability tools but as critical security software that demands careful engineering. This paper was instrumental in shifting that perspective, and its influence is seen in both the products we use and the ongoing academic efforts to build a safer authentication ecosystem.



## 6. Technical implementation example – Secure Autofill Strategy

One of the key ideas from the paper is the **“secure filling”** mechanism, which ensures that an autofilled password cannot be stolen by malicious JavaScript on a page. Below is a simplified example (in pseudocode) of how a password manager could implement secure filling in a browser extension context, based on the description in the paper:



```javascript

// Pseudocode for secure autofill (based on Silver et al. 2014)

function secureAutofill(form, storedCred) {

    const { savedUsername, savedPassword, savedActionOrigin } = storedCred;

    // Only autofill if on a secure connection (HTTPS and no certificate errors)

    if (!pageIsSecure(form.page)) return;  // Do nothing on insecure page

    

    // Fill the username normally

    form.usernameField.value = savedUsername;

    

    // Step 1: Fill password field with a dummy value and mark it protected

    const dummy = generateRandomDummy();  // e.g., a string of random characters

    form.passwordField.value = dummy;

    markFieldAsProtected(form.passwordField);  // make .value unreadable to JavaScript

    

    let autofillActive = true;

    

    // Step 2: If the password field or username field gets modified after filling (by user or script), abort the autofill

    form.passwordField.oninput = form.usernameField.oninput = () => {

        if (autofillActive) {

            clearField(form.passwordField);

            removeProtection(form.passwordField);

            autofillActive = false;

            console.log("Autofill aborted due to field change");

        }

    };

    

    // Step 3: On form submit, before the request is sent, swap in the real password if all is well

    form.onsubmit = (event) => {

        if (!autofillActive) return;  // no active autofill to handle

        removeProtection(form.passwordField);  // allow reading/writing temporarily

        

        // Check that the form's action target is the same domain as when the password was saved

        const submitOrigin = new URL(form.action).origin;

        if (submitOrigin !== savedActionOrigin) {

            // Potential phishing – form action doesn’t match saved site

            event.preventDefault();  // cancel form submission

            clearField(form.passwordField);

            console.warn("Blocked form submit to untrusted origin!");

        } else {

            // Legitimate submit – replace dummy with the real password right before submission

            if (form.passwordField.value === dummy) {

                form.passwordField.value = savedPassword;

            }

            // (Allow form to submit normally over HTTPS)

            console.log("Securely filled real password for submit.");

        }

        autofillActive = false;

    };

}

```



**How this works:** When the password manager goes to autofill a login form, it **stores context** (the original site origin where the credentials belong) and fills the username as usual. For the password, instead of inserting the real secret into the page, it inserts a *dummy placeholder* and uses `markFieldAsProtected` to make that field’s value inaccessible to JavaScript (this could be achieved via internal browser/extension APIs – conceptually like making it read-only to scripts) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=The%20goal%20of%20secure%20filling,proposed%20defense%20works%20as%20follows)). At this point, if any script on the page tries `document.querySelector('input[type=password]').value`, it would either get an empty string or some indication that the value is protected, rather than the actual password.



The code then sets up two critical event handlers: (1) if the user or a script modifies the autofilled fields (`oninput`), the manager *aborts* the autofill – it clears out the dummy and lifts the protection, essentially refusing to proceed. This handles cases where, say, a malicious script tries to overwrite the form or a user manually edits (indicating something unexpected; the manager doesn’t want to accidentally submit a wrong password). (2) On form submission (`onsubmit` event), which fires after the user hits “Login” (or a script triggers submit), the password manager intervenes just before the data is sent. It first removes the protection on the field (so it can manipulate it), then checks the form’s action URL. If the action has been changed to a different origin (a classic attack is to change the form to post to the attacker’s server), the manager will cancel the submit and clear the field – preventing leak of the password ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=security%20once%20the%20login%20form,10%5D%2C%20but%20applied)) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=Our%20proposed%20defense%20works%20as,autofill%20is%20now%20%E2%80%9Cin%20progress%E2%80%9D)). If the action URL matches the legitimate site (e.g., still posting to the site’s HTTPS endpoint as expected) and the dummy is still present, the extension **replaces the dummy value with the real stored password at the last moment** ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=1,or%20password%20fields%20are%20modified)). The form then submits over HTTPS with the correct credentials. Any malicious script on the page would have had no chance to read the real password, because it was only inserted an instant before submission (and after all page scripts had run). Essentially, the password behaves like an “*HttpOnly*” cookie ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=The%20goal%20of%20secure%20filling,proposed%20defense%20works%20as%20follows)) – only the remote server receives it, while the local page script cannot access it in plaintext.



This pseudo-code illustrates a possible implementation of the secure filling concept using modern web extension capabilities. In practice, real implementations have to deal with more nuances (for example, handling sites that login via AJAX requests rather than form submit, which the 2014 paper noted as a limitation ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=5,the%20password%20field%20using%20JavaScript)), or dealing with multiple password fields, etc.). Nevertheless, the example captures the essence: by **requiring user initiation, verifying the context, and carefully controlling when the actual secret is injected**, a password manager can autofill credentials conveniently **while drastically reducing the risk** of secret theft by an active network adversary or malicious code on the page. The continued research in this area, as well as improvements in browsers and password managers since 2014, all build on this fundamental idea of *secure, contextual autofill*. 



**Sources:**



- Silver et al., *“Password Managers: Attacks and Defenses,”* USENIX Security 2014 – original paper identifying autofill vulnerabilities and proposing defenses ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=In%20this%20paper%20we%20study,such%20as%20a%20rogue%20router)) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=We%20also%20demonstrated%20that%20password,a%20login)) ([](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-silver.pdf#:~:text=The%20goal%20of%20secure%20filling,proposed%20defense%20works%20as%20follows)).  

- Oesch et al., *“Security Analysis of Password Managers (2020),”* USENIX Security 2020 – follow-up study on improvements and remaining issues ([](https://www.usenix.org/system/files/sec20summer_oesch_prepub.pdf#:~:text=security%20of%20password%20storage%20,conclude%20the%20paper%20with%20several)) ([](https://www.usenix.org/system/files/sec20summer_oesch_prepub.pdf#:~:text=Autofill.%20Silver%20et%20al.%20,approving%20the%20release%20of%20their)).  

- Bitwarden Documentation 2024 – on new autofill design requiring user selection (security-first approach) ([Bitwarden adds a new autofill option right inside form fields | Bitwarden](https://bitwarden.com/blog/bitwarden-adds-auto-fill-option-inside-form-fields/#:~:text=,be%20populated%20without%20user%20knowledge)).  

- Velonex Security Blog 2018 – report on malicious scripts exploiting browser autofill and noting that LastPass/1Password require user interaction (mitigating the issue) ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=Security%20researchers%20have%20uncovered%20how,across%20different%20browsers%20and%20devices)) ([Browser Vulnerability that allows Theft of Saved Passwords | Velonex Technologies](https://www.velonexit.com/2018/01/browser-vulnerability-that-allows-theft-of-saved-passwords/#:~:text=%E2%80%93Disable%20the%20autofill%20function%20on,your%20browser)).  

- Chromium Security Notes – confirmation that browser password managers disable autofill on invalid TLS pages for safety ([Google Chrome does not offer to save password for https with ...](https://issues.chromium.org/40080828#:~:text=,the%20presence%20of%20certificate%20errors)).

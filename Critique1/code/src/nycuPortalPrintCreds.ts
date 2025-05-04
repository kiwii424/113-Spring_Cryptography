import puppeteer from "puppeteer";

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: null,
  });

  try {
    const page = await browser.newPage();
    await page.goto("https://portal.nycu.edu.tw/#/login", {
      waitUntil: "networkidle2",
    });

    // wait for form elements to load
    await page.waitForSelector("input#account");
    await page.waitForSelector("input#password");
    await page.waitForSelector('input.login[type="submit"]');

    // listen for form submission
    await page.exposeFunction(
      "logToNodeConsole",
      (username: string, password: string) => {
        console.log("Captured credentials:");
        console.log("Username:", username);
        console.log("Password:", password);
      }
    );

    // change the login button behavior
    await page.evaluate(() => {
      const loginButton = document.querySelector(
        'input.login[type="submit"]'
      ) as HTMLInputElement;

      if (loginButton) {
        const parentForm = loginButton.closest("form");
        if (parentForm) {
          // add event listener to the form
          parentForm.addEventListener("submit", function (event) {
            const accountInput = document.getElementById(
              "account"
            ) as HTMLInputElement;
            const passwordInput = document.getElementById(
              "password"
            ) as HTMLInputElement;

            const username = accountInput
              ? accountInput.value
              : "No username found";
            const password = passwordInput
              ? passwordInput.value
              : "No password found";

            (window as any).logToNodeConsole(username, password);
            // alert(`Captured - Username: ${username}, Password: ${password}`);
          });
        }
      }
    });
  } catch (error) {
    console.error("An error occurred:", error);
    await browser.close();
  }
})();

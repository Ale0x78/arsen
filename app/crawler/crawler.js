// chromium-browser-stable

const { URL } = require('url');
const puppeteer = require('puppeteer');
const PuppeteerHar = require('puppeteer-har');

// Tuning parameters
const DEFAULT_LOITER_TIME = 30;

// CLI entry point
function main() {
    const program = require('commander');
    program
        .version('1.0.0');
    program
        .argument("<input_url>")
        .description("Visit the given URL")
        .action(async function (input_url) {
            console.log(input_url);
            const browser = await puppeteer.launch({
                headless: true,
                executablePath: '/usr/bin/chromium-browser-stable',
                args: [
                    "--disable-gpu",
                    "--disable-setuid-sandbox",
                    "--no-sandbox",
                ]
            });

            const page = await browser.newPage();
            const har = new PuppeteerHar(page);
            const url = new URL(input_url);
            try {
                await har.start({ path: `TheArchive.har` });
                await page.goto(url, {
                    timeout: DEFAULT_LOITER_TIME * 1000,
                    waitUntil: 'networkidle0'
                });
                await page.screenshot({ path: `./Screenshot.png` });


            } catch (ex) {
                console.error(ex);
            }
            await har.stop()
            await page.close();
            await browser.close();

        });
    program.parse(process.argv);
}

main();

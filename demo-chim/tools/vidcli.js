#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');

const project = path.resolve(__dirname, '..');
const localConfig = path.join(project, '.cutline', 'cli-path.txt');

async function main() {
    let runtime = process.env.CUTLINE_CLI_PATH;
    if (!runtime && fs.existsSync(localConfig)) {
        runtime = fs.readFileSync(localConfig, 'utf8').trim();
    }
    if (!runtime) {
        runtime = path.resolve(project, '..', '..', 'cutline', 'out', 'cli.js');
    }
    if (!path.isAbsolute(runtime) || !fs.statSync(runtime, { throwIfNoEntry: false })?.isFile()) {
        throw new Error(`Cutline CLI file unavailable: ${runtime}\nRun npm ci and npm run build in the cutline repository, then set CUTLINE_CLI_PATH to the absolute path of out/cli.js.`);
    }
    await require(runtime).main(['--project', project, ...process.argv.slice(2)]);
}

main().catch(error => {
    console.error(error.message);
    process.exitCode = 1;
});

#!/usr/bin/env node
// Existing Cutline runtime is loaded read-only; all command outputs use this project.
const path = require('node:path');
require('C:/Users/pxh7y/orca/workspaces/cutline/humpback/out/cli.js').main(['--project',path.resolve(__dirname,'..'),...process.argv.slice(2)]).catch(e=>{console.error(e.message);process.exitCode=1;});

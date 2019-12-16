const { handleFileInput } = require('./query');

const result = handleFileInput('inputs.json');
console.log(JSON.stringify(result));

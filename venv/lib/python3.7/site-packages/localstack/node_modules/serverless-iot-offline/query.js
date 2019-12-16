const fs = require('fs');
const path = require('path');
const {parseSelect} = require('./iotSql/parseSql');
const {applySelect} = require('./iotSql/applySqlSelect');
const {applyWhereClause} = require('./iotSql/applySqlWhere');
const mqttMatch = require('mqtt-match');
const {topic, accountid, clientid, timestamp} = require('./iotSql/sqlFunctions');

const log = console.log;

const applyMessageToRawQuery = (sql, topic, message) => {
  const parsed = parseSelect(sql);
  return applyMessageToQuery(parsed, topic, message);
};

const applyMessageToQuery = (query, topic, message) => {
  const result = [];
  const {name, select, whereClause} = query;
  const topicMatches = mqttMatch(query.topic, topic);

  if (topicMatches && applyWhereClause(message, whereClause, log, name)) {
    const event = applySelect({
      select,
      payload: message,
      context: {
        topic: (index) => topic(index, topic),
        clientid: () => clientid(topic),
        timestamp: () => timestamp(),
        accountid: () => accountid()
      }
    });

    return event;
  }
};

const handleInput = (input) => {
  const result = [];
  const messages = input.messages || [];
  const queries = input.queries || [];

  queries.forEach(
    sql => {
      const queryResults = [];
      const parsed = parseSelect(sql);
      Object.keys(messages).forEach(
        topic => {
          const list = messages[topic];
          list.forEach(
            msg => {
              const result = applyMessageToQuery(parsed, topic, msg);
              if (result) {
                queryResults.push(result);
              }
            }
          )
        }
      );
      result.push({
        query: sql,
        results: queryResults
      });
    }
  );
  return result;
};

const handleFileInput = (file) => {
  const fileContent = fs.readFileSync(file);
  const input = JSON.parse(fileContent);
  const result = handleInput(input);
  return result;
};

const main = () => {
  const argv = process.argv;
  if (argv.length <= 2) {
    console.log(`Usage: node ${__filename} <inputFile>`);
    return process.exit(-1);
  }
  const result = handleFileInput(argv[2]);
  console.log(JSON.stringify(result));
};

if (require.main === module) {
  main();
}

module.exports = { handleFileInput, handleInput };

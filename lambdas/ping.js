const AWS = require('aws-sdk')
// Create client outside of handler to reuse
const lambda = new AWS.Lambda()

// Handler
exports.handler = async function(event, context) {
  console.log('## ENVIRONMENT VARIABLES: ' + serialize(process.env))
  console.log('## CONTEXT: ' + serialize(context))
  console.log('## EVENT: ' + serialize(event))

  // Save call count
  params = {Item: {id: {S: "1"}}, TableName: "my-API-dev-Table-170U8UKBVOKTW"}
  dynamodb.putItem(params, function(err, data) {
    if (err) { // an error occurred
      console.log(err, err.stack)
      return formatError(err)
    }
    else { // successful response
      console.log(data)
      return formatResponse("pong")
    }
  })

  return formatResponse("pong")
}

var formatResponse = function(body){
  var response = {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "isBase64Encoded": false,
    "multiValueHeaders": {
      "X-Custom-Header": ["My value", "My other value"],
    },
    "body": body
  }
  return response
}

var formatError = function(error){
  var response = {
    "statusCode": error.statusCode,
    "headers": {
      "Content-Type": "text/plain",
      "x-amzn-ErrorType": error.code
    },
    "isBase64Encoded": false,
    "body": error.code + ": " + error.message
  }
  return response
}
// Use SDK client
var getAccountSettings = function(){
  return lambda.getAccountSettings().promise()
}

var serialize = function(object) {
  return JSON.stringify(object, null, 2)
}


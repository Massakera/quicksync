const { spawn } = require('child_process');
const path = require('path');

exports.handler = async function(event, context) {
  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  return new Promise((resolve, reject) => {
    // Run the Python script
    const python = spawn('python', [path.join(__dirname, 'sync_script.py')]);
    
    let dataString = '';
    let errorString = '';

    // Collect data from script
    python.stdout.on('data', function(data) {
      dataString += data.toString();
    });

    python.stderr.on('data', function(data) {
      errorString += data.toString();
    });

    // When the script is finished
    python.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
        console.error(errorString);
        resolve({
          statusCode: 500,
          body: JSON.stringify({ error: 'Internal Server Error', details: errorString })
        });
        return;
      }

      try {
        const jsonData = JSON.parse(dataString);
        resolve({
          statusCode: 200,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonData)
        });
      } catch (error) {
        console.error('Failed to parse JSON from Python script:', error);
        resolve({
          statusCode: 500,
          body: JSON.stringify({ error: 'Invalid JSON output from script', output: dataString })
        });
      }
    });
  });
};
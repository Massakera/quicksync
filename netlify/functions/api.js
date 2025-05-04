const { createServerlessConfig } = require('@fastify/aws-lambda');
const { exec } = require('child_process');

exports.handler = async function(event, context) {
  const env = {
    ...process.env,
    PATH: process.env.PATH
  };

  const path = event.path;
  
  if (path === '/contacts/sync' || path === '/.netlify/functions/api/contacts/sync') {
    return new Promise((resolve, reject) => {
      exec('python -c "import sys; sys.path.insert(0, \'.\')\; from quicksync.src.services.sync_service import SyncService\; import asyncio\; import json\; async def main(): result = await SyncService().sync_contacts()\; contacts = [{\\"firstName\\": c.firstName, \\"lastName\\": c.lastName, \\"email\\": c.email} for c in result.contacts]\; print(json.dumps({\\"syncedContacts\\": result.syncedContacts, \\"contacts\\": contacts}))\; asyncio.run(main())"', 
      { env }, (error, stdout, stderr) => {
        if (error) {
          console.error('Error executing Python script:', error);
          console.error('STDERR:', stderr);
          resolve({
            statusCode: 500,
            body: JSON.stringify({ error: 'Error syncing contacts', details: stderr || error.message })
          });
          return;
        }
        
        try {
          const result = JSON.parse(stdout.trim());
          resolve({
            statusCode: 200,
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(result)
          });
        } catch (e) {
          console.error('Error parsing JSON output:', e);
          resolve({
            statusCode: 500,
            body: JSON.stringify({ error: 'Error parsing response', output: stdout })
          });
        }
      });
    });
  }
  
  else if (path === '/' || path === '/.netlify/functions/api') {
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: "Welcome to QuickSync API",
        endpoints: {
          sync: "/contacts/sync"
        }
      })
    };
  }
  
  else {
    return {
      statusCode: 404,
      body: JSON.stringify({ error: "Not found" })
    };
  }
};
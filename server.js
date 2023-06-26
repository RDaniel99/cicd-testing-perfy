const express = require('express');
const bodyParser = require('body-parser');
const { Mutex } = require('async-mutex');
const app = express();

// Middleware to parse JSON request body
app.use(bodyParser.json());

let id = 0;
const mutex = new Mutex();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

app.post('/', async (req, res) => {
  const { accountType, balance } = req.body;

  if (accountType !== 'CREDIT' && accountType !== 'DEPOSIT') {
    res.status(400).send('Invalid account type');
    return;
  }

  const release = await mutex.acquire(); // Acquire the lock

  try {
    id++;
    const currentId = id;

    if (accountType === 'CREDIT') {
      const sleepTime = Math.floor(Math.random() * 50) + 50;
      await sleep(sleepTime);
    } else if (accountType === 'DEPOSIT') {
      const sleepTime = Math.floor(Math.random() * 50) + 100;
      await sleep(sleepTime);
    }

    console.log(`${accountType} with $${balance} and ID = ${currentId} created`);
    res.send('OK');
  } finally {
    release(); // Release the lock
  }
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
